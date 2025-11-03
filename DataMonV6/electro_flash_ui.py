import streamlit as st
import random, math, time

def render_electro_flash():
    st.subheader("Electro Flash ⚡")

    base = st.number_input("Base Number", min_value=1, max_value=12, value=2)
    op = st.selectbox("Operation", ["+", "-", "*", "/"])
    total = st.number_input("Number of Questions", min_value=1, max_value=12, value=5)

    if "ef_active" not in st.session_state:
        st.session_state.ef_active = False

    if st.button("Start Game"):
        st.session_state.ef_active = True
        st.session_state.ef_score = 0
        st.session_state.ef_start = time.time()
        st.session_state.ef_numbers = random.sample(range(1, 13), total)
        st.session_state.ef_idx = 0

    if st.session_state.ef_active:
        idx = st.session_state.ef_idx
        if idx < total:
            n = st.session_state.ef_numbers[idx]
            st.write(f"**Problem {idx+1}/{total}: {base} {op} {n} = ?**")
            user = st.text_input("Answer", key=f"ef_ans_{idx}")
            if st.button("Submit", key=f"ef_submit_{idx}"):
                correct = eval(f"{base}{op}{n}")
                if math.isclose(float(user), float(correct), rel_tol=1e-2):
                    st.success("Correct!")
                    st.session_state.ef_score += 1
                else:
                    st.error(f"Wrong! Correct answer: {correct}")
                st.session_state.ef_idx += 1
        else:
            st.success(f"Done! Score: {st.session_state.ef_score}/{total}")
            st.session_state.player_points += st.session_state.ef_score
            st.session_state.ef_active = False
