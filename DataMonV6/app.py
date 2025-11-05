# app.py
import streamlit as st
from streamlit.components.v1 import html

from answer_checker_ui import render_answer_checker
from memory_bank_ui import render_memory_bank
from electro_flash_ui import render_electro_flash

st.set_page_config(page_title="Datamon Web", page_icon="🧮")

st.title("🧮 Datamon — Web Edition")

# Sidebar: points + section selector (keeps the main area stable on rerun)
if "player_points" not in st.session_state:
    st.session_state.player_points = 0

st.sidebar.header("Player Points")
st.sidebar.metric("Total Points", st.session_state.player_points)

SECTIONS = ["Answer Checker", "Memory Bank", "Electro Flash"]
st.session_state.setdefault("active_section", SECTIONS[0])

choice = st.sidebar.radio(
    "Sections",
    SECTIONS,
    index=SECTIONS.index(st.session_state["active_section"]),
)
st.session_state["active_section"] = choice

# ---- Anchors for each section (stable IDs) ----
AC_ANCHOR = "ac_anchor"
MB_ANCHOR = "mb_anchor"
EF_ANCHOR = "ef_anchor"

def _anchor_div(anchor_id: str):
    st.markdown(f'<div id="{anchor_id}"></div>', unsafe_allow_html=True)

st.divider()

# Render selected section with its anchor just above it
if choice == "Answer Checker":
    _anchor_div(AC_ANCHOR)
    render_answer_checker()
elif choice == "Memory Bank":
    _anchor_div(MB_ANCHOR)
    render_memory_bank()
else:
    _anchor_div(EF_ANCHOR)
    render_electro_flash()

# ---- Global post-render scroll & focus handler ----
# Any section can set st.session_state['scroll_to'] to 'ac'/'mb'/'ef'
target = st.session_state.get("scroll_to")
if target:
    # Clear the flag so it runs once
    st.session_state["scroll_to"] = None

    # Map which anchor & which input label to focus
    mapping = {
        "ac": (AC_ANCHOR, "Equation"),
        "mb": (MB_ANCHOR, "Your Answer"),
        "ef": (EF_ANCHOR, "Answer"),
    }
    anchor_id, input_label = mapping.get(target, (None, None))

    if anchor_id and input_label:
        # Scroll to the section and focus the desired input.
        # Multiple retries handle Streamlit's layout timing on Cloud.
        html(
            f"""
            <script>
            (function() {{
              const doc = window.parent.document;
              const scrollAndFocus = () => {{
                // scroll to anchor
                const anchor = doc.getElementById("{anchor_id}");
                if (anchor && anchor.scrollIntoView) {{
                  anchor.scrollIntoView({{behavior: 'instant', block: 'start'}});
                }}
                // focus input by label
                let lbl = Array.from(doc.querySelectorAll('label'))
                  .find(l => /\\b{input_label}\\b/i.test(l.textContent));
                let input = lbl ? (lbl.parentElement && lbl.parentElement.querySelector('input')) : null;
                // fallback: first visible text input
                if (!input) {{
                  input = Array.from(doc.querySelectorAll('input'))
                    .find(el => el.type === 'text' && el.offsetParent !== null);
                }}
                if (input) {{
                  input.focus();
                  if (input.select) input.select();
                  return true;
                }}
                return false;
              }};
              // Try a few times for reliability
              if (!scrollAndFocus()) setTimeout(scrollAndFocus, 60);
              setTimeout(scrollAndFocus, 140);
              setTimeout(scrollAndFocus, 260);
            }})();
            </script>
            """,
            height=0,
        )
