# app.py
# Streamlit Datamon Answer Checker — single-file app
# Run with: streamlit run app.py

import re
from typing import Tuple, Optional

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Datamon Answer Checker",
    page_icon="✅",
    layout="centered",
)

# -----------------------------
# Pluggable checker mechanism
# -----------------------------
def normalize(text: str, *, casefold=True, strip=True, collapse_ws=True, remove_punct=False) -> str:
    if text is None:
        return ""
    s = text
    if strip:
        s = s.strip()
    if casefold:
        s = s.casefold()
    if collapse_ws:
        s = re.sub(r"\s+", " ", s)
    if remove_punct:
        s = re.sub(r"[^\w\s]", "", s)
    return s

def fallback_check(datamon: str, answer: str, *, opts: dict) -> Tuple[bool, str, Optional[str]]:
    """
    Very simple default checker:
    - If an expected answer is embedded like '... | expected=XYZ', it will use that.
    - Otherwise, it compares normalized datamon and answer strings (placeholder logic).
    Returns: (is_correct, message, expected_if_known)
    """
    # Try to discover an explicit expected answer pattern: expected=...
    m = re.search(r"(?:^|\s)\bexpected\s*=\s*(.+)$", datamon, flags=re.IGNORECASE)
    expected = m.group(1).strip() if m else None

    if expected is not None:
        norm_expected = normalize(expected, **opts)
        norm_proposed = normalize(answer, **opts)
        ok = norm_proposed == norm_expected
        msg = "Matched expected answer." if ok else "Did not match the expected answer."
        return ok, msg, expected

    # Placeholder heuristic: treat the datamon string as a prompt that may contain an answer after 'answer='
    m2 = re.search(r"(?:^|\s)\banswer\s*=\s*(.+)$", datamon, flags=re.IGNORECASE)
    implied = m2.group(1).strip() if m2 else None
    if implied is not None:
        ok = normalize(answer, **opts) == normalize(implied, **opts)
        msg = "Matched implied answer in datamon." if ok else "Did not match implied answer in datamon."
        return ok, msg, implied

    # Last-resort placeholder: equality of normalized strings
    ok = normalize(answer, **opts) == normalize(datamon, **opts)
    msg = (
        "Answer equals the datamon text (normalized)."
        if ok
        else "No expected answer found; simple normalized equality failed."
    )
    return ok, msg, None

def try_external_checker(datamon: str, answer: str, *, opts: dict) -> Optional[Tuple[bool, str, Optional[str]]]:
    """
    If you already have a console/library checker (e.g., `datamon_checker.check(datamon, answer)`),
    you can drop it in the same folder and this will use it automatically.
    """
    try:
        import importlib
        checker = importlib.import_module("datamon_checker")
        if hasattr(checker, "check"):
            # Expecting: check(datamon: str, answer: str) -> (bool, message, expected_str_or_None)
            result = checker.check(datamon, answer)
            # If external checker returns only bool, adapt it:
            if isinstance(result, tuple):
                return result
            else:
                return (bool(result), "External checker verdict.", None)
    except Exception:
        pass
    return None

# -----------------------------
# Sidebar options
# -----------------------------
st.sidebar.header("Normalization Options")
norm_opts = {
    "casefold": st.sidebar.checkbox("Case-insensitive", value=True),
    "strip": st.sidebar.checkbox("Trim leading/trailing spaces", value=True),
    "collapse_ws": st.sidebar.checkbox("Collapse repeated spaces", value=True),
    "remove_punct": st.sidebar.checkbox("Ignore punctuation", value=False),
}

st.sidebar.markdown("---")
st.sidebar.subheader("Batch Processing (CSV)")
st.sidebar.caption("Optional: upload a CSV with columns **datamon** and **answer**.")
batch_file = st.sidebar.file_uploader(
    "Upload CSV", type=["csv"], accept_multiple_files=False, label_visibility="collapsed"
)

# -----------------------------
# Header
# -----------------------------
st.title("✅ Datamon Answer Checker (Streamlit)")
st.write(
    "Enter a **datamon** prompt and a proposed **answer**, then click **Check**. "
    "If you have your own checker module (e.g., `datamon_checker.py` with a `check()` function), "
    "place it next to this file and it will be used automatically."
)

# -----------------------------
# Single check form
# -----------------------------
with st.form("single_check_form", clear_on_submit=False):
    datamon_text = st.text_area(
        "Datamon", 
        placeholder="Paste your Datamon prompt here. (Optional: add 'expected=...')",
        height=140,
    )
    answer_text = st.text_input(
        "Answer",
        placeholder="Type the answer to verify…",
    )
    submitted = st.form_submit_button("Check")

if submitted:
    if not datamon_text.strip() or not answer_text.strip():
        st.error("Please provide both **Datamon** and **Answer**.")
    else:
        external = try_external_checker(datamon_text, answer_text, opts=norm_opts)
        if external is not None:
            ok, msg, expected = external
            source = "External checker"
        else:
            ok, msg, expected = fallback_check(datamon_text, answer_text, opts=norm_opts)
            source = "Built-in fallback"

        verdict = "✅ Correct" if ok else "❌ Incorrect"
        st.markdown(f"### {verdict}")
        st.write(msg)
        st.caption(f"Verifier: {source}")
        if expected is not None:
            st.info(f"Expected: `{expected}`")

# -----------------------------
# Batch mode (optional)
# -----------------------------
if batch_file is not None:
    try:
        df = pd.read_csv(batch_file)
        missing = [c for c in ("datamon", "answer") if c not in df.columns]
        if missing:
            st.error(f"CSV is missing required column(s): {', '.join(missing)}")
        else:
            st.subheader("Batch Results")
            results = []
            for i, row in df.iterrows():
                d = str(row["datamon"])
                a = str(row["answer"])
                external = try_external_checker(d, a, opts=norm_opts)
                if external is not None:
                    ok, msg, expected = external
                    src = "external"
                else:
                    ok, msg, expected = fallback_check(d, a, opts=norm_opts)
                    src = "fallback"
                results.append({
                    "datamon": d,
                    "answer": a,
                    "correct": bool(ok),
                    "message": msg,
                    "expected": expected if expected is not None else "",
                    "checker": src,
                })
            out = pd.DataFrame(results)
            st.dataframe(out, use_container_width=True)
            # Download button
            csv_bytes = out.to_csv(index=False).encode("utf-8")
            st.download_button("Download Results CSV", data=csv_bytes, file_name="datamon_batch_results.csv")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")

# -----------------------------
# Footer help
# -----------------------------
with st.expander("How to plug in your own checker"):
    st.markdown(
        """
        1) Create a file `datamon_checker.py` in the same folder as `app.py`  
        2) Implement a function:
           ```python
           # datamon_checker.py
           def check(datamon: str, answer: str):
               # return either:
               #   True/False
               # or: (True/False, "message", "expected answer or None")
               ...
           ```
        3) Restart the app. If the module imports, the app will use it automatically.
        """
    )
