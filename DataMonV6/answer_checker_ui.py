# answer_checker_ui.py
import streamlit as st
from streamlit.components.v1 import html  # <-- use components to run JS
from AnswerChecker import check_answer

EQ_KEY  = "ac_equation"
ANS_KEY = "ac_answer"
FOCUS_FLAG = "_focus_equation"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(EQ_KEY, "")
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(FOCUS_FLAG, False)

def _submit_answer():
    eq = st.session_state.get(EQ_KEY, "").strip()
    ans = st.session_state.get(ANS_KEY, "").strip()

    if not eq or not ans:
        st.warning("Please enter both an equation and an answer.")
        return

    try:
        ok = bool(check_answer(f"{eq}={ans}"))
    except Exception as e:
        st.error(f"Error checking answer: {e}")
        return

    if ok:
        st.session_state.player_points += 1
        st.success("✅ Correct! +1 point")
        # clear both fields, then set flag to focus Equation on the rerun
        st.session_state[EQ_KEY] = ""
        st.session_state[ANS_KEY] = ""
        st.session_state[FOCUS_FLAG] = True
    else:
        st.error("❌ Incorrect! Try again.")
        # keep equation, clear only answer
        st.session_state[ANS_KEY] = ""

def render_answer_checker():
    _ensure_state()
    st.subheader("Answer Checker")

    # Inputs (Enter on Answer submits)
    st.text_input("Equation", placeholder="e.g., 4+4", key=EQ_KEY)
    st.text_input(
        "Your Answer",
        placeholder="e.g., 8",
        key=ANS_KEY,
        on_change=_submit_answer,
    )
    if st.button("Check Answer"):
        _submit_answer()

    # Robust auto-focus using a component (runs JS inside an iframe and reaches parent DOM)
    if st.session_state.get(FOCUS_FLAG):
        st.session_state[FOCUS_FLAG] = False
        html(
            """
            <script>
            (function() {
              // Try multiple selectors to be resilient across Streamlit versions
              const tryFocus = () => {
                const doc = window.parent.document;
                let target =
                  doc.querySelector('input[aria-label="Equation"]') ||
                  Array.from(doc.querySelectorAll('label')).find(l => /Equation/i.test(l.textContent))?.parentElement?.querySelector('input') ||
                  Array.from(doc.querySelectorAll('input')).find(el => el.placeholder && el.placeholder.includes('4+4'));
                if (target) { target.focus(); target.select && target.select(); return true; }
                return false;
              };
              // Try immediately, and a couple more times in case layout isn’t ready yet
              if (!tryFocus()) setTimeout(tryFocus, 50);
              setTimeout(tryFocus, 150);
            })();
            </script>
            """,
            height=0,
        )
