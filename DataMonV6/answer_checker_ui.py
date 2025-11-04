# answer_checker_ui.py
import streamlit as st
from AnswerChecker import check_answer

# Keys used in session_state for this tab
EQ_KEY = "ac_equation"
ANS_KEY = "ac_answer"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(EQ_KEY, "")
    st.session_state.setdefault(ANS_KEY, "")

def _submit_answer():
    """Handle both Enter and the Submit button."""
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
        # Optional: clear the answer box so you can type the next one quickly
        st.session_state[ANS_KEY] = ""
    else:
        st.error("❌ Incorrect! Try again.")

def render_answer_checker():
    _ensure_state()

    st.subheader("Answer Checker")

    # No form: this removes the 'Press Enter to apply' hint and lets us control Enter behavior
    st.text_input("Equation", placeholder="e.g., 4+4", key=EQ_KEY)

    # Pressing Enter in this input will run _submit_answer()
    st.text_input(
        "Your Answer",
        placeholder="e.g., 8",
        key=ANS_KEY,
        on_change=_submit_answer,  # ENTER triggers the same action as the button
    )

    # Mouse users can still click the button — same behavior
    if st.button("Check Answer"):
        _submit_answer()

