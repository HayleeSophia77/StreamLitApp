# memory_bank_ui.py
import streamlit as st
from memorybank import safe_eval, fun_feedback
import math, random

PROB_KEY    = "mb_problems"
CURR_KEY    = "mb_current"
ANS_KEY     = "mb_answer"
ATT_KEY     = "mb_attempts"
COR_KEY     = "mb_correct"
ADD_KEY     = "mb_add_input"
ADD_MSG_KEY = "mb_add_msg"   # flash message after adding

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(PROB_KEY, [])
    st.session_state.setdefault(CURR_KEY, None)
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(ATT_KEY, 0)
    st.session_state.setdefault(COR_KEY, 0)
    st.session_state.setdefault(ADD_KEY, "")
    st.session_state.setdefault(ADD_MSG_KEY, None)

def _flash(msg, kind="success"):
    # store a one-shot message to show after rerun
    st.session_state[ADD_MSG_KEY] = (kind, msg)

def _add_problem():
    """Handles both Enter on the add box and clicking the Add button."""
    raw = st.session_state.get(ADD_KEY, "").strip()
    if not raw:
        _flash("Please enter a problem first.", "warning")
        return
    try:
        safe_eval(raw)  # validate
        st.session_state[PROB_KEY].append(raw)
        _flash("Added!", "success")
        # clear the input so user can type the next one quickly
        st.session_state[ADD_KEY] = ""
    except Exception as e:
        _flash(f"Invalid problem: {e}", "error")

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
        st.session_state[ANS_KEY] = ""
        # pick another at random (keep full bank for now)
        st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    else:
        st.warning("Not quite. Try again!")
        st.session_state[ANS_KEY] = ""  # quick retry

def render_memory_bank():
    _ensure_state()
    st.subheader("Memory Bank")

    with st.expander("➕ Add Problems", expanded=True):
        # Hitting Enter here will call _add_problem()
        st.text_input(
            "Enter a problem (e.g., 5+5, (2+3)*4, 10-3*2, 2**3)",
            key=ADD_KEY,
            on_change=_add_problem,   # ENTER adds
        )
        # Mouse users can still click Add — same handler
        if st.button("Add"):
            _add_problem()

        # show one-shot flash after rerun
        flash = st.session_state.get(ADD_MSG_KEY)
        if flash:
            kind, msg = flash
            if kind == "success":
                st.success(msg)
            elif kind == "warning":
                st.warning(msg)
            else:
                st.error(msg)
            st.session_state[ADD_MSG_KEY] = None

        if st.session_state[PROB_KEY]:
            st.write("Problems in bank:")
            st.code("\n".join(st.session_state[PROB_KEY]))

    c1, c2 = st.columns([1, 1])
    if c1.button("🧪 Start Practice Round"):
        _start_round()
    if c2.button("End Round"):
        if st.session_state[ATT_KEY] > 0:
            st.info(fun_feedback(st.session_state[COR_KEY], st.session_state[ATT_KEY]))
        else:
            st.info("No attempts yet.")

    current = st.session_state.get(CURR_KEY)
    if current:
        st.markdown(f"### Solve: `{current}`")
        # ENTER submits the answer
        st.text_input("Your Answer", key=ANS_KEY, on_change=_submit_answer)
        if st.button("Submit"):
            _submit_answer()

    if st.session_state[ATT_KEY] > 0:
        st.caption(fun_feedback(st.session_state[COR_KEY], st.session_state[ATT_KEY]))
