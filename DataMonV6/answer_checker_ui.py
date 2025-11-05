# answer_checker_ui.py
import streamlit as st
from AnswerChecker import check_answer

EQ_KEY  = "ac_equation"
ANS_KEY = "ac_answer"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(EQ_KEY, "")
    st.session_state.setdefault(ANS_KEY, "")

def _submit_answer():
    """Runs on Enter in the Answer box and on button click."""
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
        # Award point and clear BOTH fields to move on to next problem
        st.session_state.player_points += 1
        st.success("✅ Correct! +1 point")
        st.session_state[EQ_KEY] = ""
        st.session_state[ANS_KEY] = ""
    else:
        # Keep the equation, clear only the answer for a quick retry
        st.error("❌ Incorrect! Try again.")
        st.session_state[ANS_KEY] = ""

def render_answer_checker():
    _ensure_state()

    st.subheader("Answer Checker")

    # Keep this basic; we only auto-submit from the Answer field
    st.text_input("Equation", placeholder="e.g., 4+4", key=EQ_KEY)

    # Pressing Enter here submits; button below does the same
    st.text_input(
        "Your Answer",
        placeholder="e.g., 8",
        key=ANS_KEY,
        on_change=_submit_answer,
    )

    if st.button("Check Answer"):
        _submit_answer()