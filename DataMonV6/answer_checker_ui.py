# answer_checker_ui.py
import streamlit as st
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
        # clear both fields, move focus back to Equation
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

    # Equation field
    st.text_input("Equation", placeholder="e.g., 4+4", key=EQ_KEY)

    # Answer field (ENTER = submit)
    st.text_input(
        "Your Answer",
        placeholder="e.g., 8",
        key=ANS_KEY,
        on_change=_submit_answer,
    )

    if st.button("Check Answer"):
        _submit_answer()

    # If flagged, re-focus the Equation box after a correct answer
    if st.session_state.get(FOCUS_FLAG):
        st.session_state[FOCUS_FLAG] = False
        st.markdown(
            """
            <script>
            const eqInput = document.querySelector('input[aria-label="Equation"]');
            if (eqInput) { eqInput.focus(); }
            </script>
            """,
            unsafe_allow_html=True,
        )
