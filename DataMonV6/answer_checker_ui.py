import streamlit as st
from AnswerChecker import check_answer

def render_answer_checker():
    st.subheader("Answer Checker")

    with st.form("ac_form"):
        eq = st.text_input("Equation", placeholder="e.g., 4+4")
        ans = st.text_input("Your Answer", placeholder="e.g., 8")
        submitted = st.form_submit_button("Check Answer")

    if submitted:
        result = check_answer(f"{eq}={ans}")
        if result:
            st.session_state.player_points += 1
            st.success("✅ Correct! +1 point")
        else:
            st.error("❌ Incorrect! Try again.")
