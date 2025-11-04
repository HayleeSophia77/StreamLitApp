# memory_bank_ui.py
import streamlit as st
from memorybank import safe_eval, fun_feedback
import math, random

PROB_KEY = "mb_problems"
CURR_KEY = "mb_current"
ANS_KEY  = "mb_answer"
ATT_KEY  = "mb_attempts"
COR_KEY  = "mb_correct"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(PROB_KEY, [])
    st.session_state.setdefault(CURR_KEY, None)
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(ATT_KEY, 0)
    st.session_state.setdefault(COR_KEY, 0)

def _start_round():
    if not st.session_state[PROB_KEY]:
        st.warning("Add some problems first.")
        return
    st.session_state[ATT_KEY] = 0
    st.session_state[COR_KEY] = 0
    st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    st.session_state[ANS_KEY] = ""

def _submit_answer():
    prob = st.session_state.get(CURR_KEY)
    if not prob:
        st.warning("Start a round first.")
        return
    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if not ans_str:
        st.warning("Please enter an answer.")
        return

    try:
        correct_val = float(safe_eval(prob))
        user_val = float(ans_str)
    except Exception as e:
        st.error(f"Invalid input: {e}")
        return

    st.session_state[ATT_KEY] += 1
    if math.isclose(user_val, correct_val, rel_tol=1e-9, abs_tol=1e-9):
        st.session_state[COR_KEY] += 1
        st.session_state.player_points += 1
        st.success("✅ Correct!")
        # Move to a new random problem (if any remain)
        st.session_state[ANS_KEY] = ""
        # Optional: remove solved problem from the bank to avoid repeats
        # st.session_state[PROB_KEY].remove(prob)
        st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    else:
        st.warning(f"Not quite. Try again!")
        # keep same problem; just clear the answer for quick retry
        st.session_state[ANS_KEY] = ""

def render_memory_bank():
    _ensure_state()
    st.subheader("Memory Bank")

    with st.expander("➕ Add Problems"):
        new_prob = st.text_input("Enter a problem (e.g., 5+5)", key="mb_add_input")
        if st.button("Add"):
            if not new_prob.strip():
                st.warning("Please enter something.")
            else:
                try:
                    safe_eval(new_prob.strip())
                    st.session_state[PROB_KEY].append(new_prob.strip())
                    st.success("Added!")
                except Exception as e:
                    st.error(f"Invalid problem: {e}")

    if st.session_state[PROB_KEY]:
        st.write("Problems in bank:")
        st.code("\n".join(st.session_state[PROB_KEY]))

    col1, col2 = st.columns([1,2])
    if col1.button("🧪 Start Practice Round"):
        _start_round()
    if col2.button("End Round"):
        if st.session_state[ATT_KEY] > 0:
            st.info(fun_feedback(st.session_state[COR_KEY], st.session_state[ATT_KEY]))
        else:
            st.info("No attempts yet.")

    current = st.session_state.get(CURR_KEY)
    if current:
        st.markdown(f"### Solve: `{current}`")
        # Enter here triggers _submit_answer (same as clicking Submit)
        st.text_input("Your Answer", key=ANS_KEY, on_change=_submit_answer)
        if st.button("Submit"):
            _submit_answer()

    # Show running feedback
    if st.session_state[ATT_KEY] > 0:
        st.caption(fun_feedback(st.session_state[COR_KEY], st.session_state[ATT_KEY]))
