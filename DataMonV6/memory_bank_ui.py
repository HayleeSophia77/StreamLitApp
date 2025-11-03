import streamlit as st
from memorybank import safe_eval, fun_feedback
import math, random

def render_memory_bank():
    st.subheader("Memory Bank")

    if "mb_problems" not in st.session_state:
        st.session_state.mb_problems = []
        st.session_state.mb_attempts = 0
        st.session_state.mb_correct = 0

    with st.expander("➕ Add Problems"):
        new_prob = st.text_input("Enter a problem (e.g., 5+5)")
        if st.button("Add"):
            try:
                safe_eval(new_prob)
                st.session_state.mb_problems.append(new_prob)
                st.success("Added!")
            except Exception:
                st.error("Invalid problem.")

    if not st.session_state.mb_problems:
        st.info("Add some problems to start!")
        return

    if st.button("🧪 Start Practice Round"):
        st.session_state.mb_attempts = 0
        st.session_state.mb_correct = 0
        st.session_state.current = random.choice(st.session_state.mb_problems)

    if "current" in st.session_state and st.session_state.current:
        prob = st.session_state.current
        st.write(f"### Solve: `{prob}`")
        ans = st.text_input("Your Answer")
        if st.button("Submit"):
            correct = float(safe_eval(prob))
            user_val = float(ans)
            st.session_state.mb_attempts += 1
            if math.isclose(correct, user_val, rel_tol=1e-9):
                st.session_state.mb_correct += 1
                st.session_state.player_points += 1
                st.success("Correct!")
                st.session_state.current = None
            else:
                st.warning("Try again!")

    if st.session_state.mb_attempts > 0:
        st.caption(fun_feedback(st.session_state.mb_correct, st.session_state.mb_attempts))
