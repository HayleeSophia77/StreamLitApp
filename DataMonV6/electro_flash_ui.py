# electro_flash_ui.py
import streamlit as st
import random, math, time

BASE_KEY   = "ef_base"
OP_KEY     = "ef_op"
TOT_KEY    = "ef_total"
IDX_KEY    = "ef_idx"
NUMS_KEY   = "ef_numbers"
ANS_KEY    = "ef_answer_input"
SCORE_KEY  = "ef_score"
START_KEY  = "ef_start"
ACTIVE_KEY = "ef_active"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(BASE_KEY, 2)
    st.session_state.setdefault(OP_KEY, "*")
    st.session_state.setdefault(TOT_KEY, 5)
    st.session_state.setdefault(IDX_KEY, 0)
    st.session_state.setdefault(NUMS_KEY, [])
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(SCORE_KEY, 0)
    st.session_state.setdefault(START_KEY, None)
    st.session_state.setdefault(ACTIVE_KEY, False)

def _start_game():
    st.session_state[ACTIVE_KEY] = True
    st.session_state[SCORE_KEY] = 0
    st.session_state[START_KEY] = time.time()
    total = int(st.session_state[TOT_KEY])
    st.session_state[NUMS_KEY] = random.sample(range(1, 13), total)
    st.session_state[IDX_KEY] = 0
    st.session_state[ANS_KEY] = ""
    st.session_state["scroll_to"] = "ef"

def _end_game():
    st.session_state.player_points += st.session_state[SCORE_KEY]
    st.session_state[ACTIVE_KEY] = False

def _problem_for(idx):
    """Return (visible_index, total, first, op, second, correct)."""
    total = int(st.session_state[TOT_KEY])
    base  = int(st.session_state[BASE_KEY])
    op    = st.session_state[OP_KEY]
    n     = st.session_state[NUMS_KEY][idx]

    if op == "+":
        first, second = base, n
        correct = first + second
    elif op == "-":
        # Keep non-negative: (n+base) - base = n
        first, second = n + base, base
        correct = first - second
    elif op == "*":
        first, second = base, n
        correct = first * second
    elif op == "/":
        # Divisible: (n*base) / base = n
        first, second = n * base, base
        correct = first / second
    else:
        first, second = base, n
        correct = first * second

    return (idx + 1, total, first, op, second, float(correct))

def _current_problem():
    idx = st.session_state[IDX_KEY]
    total = int(st.session_state[TOT_KEY])
    if idx >= total:
        return None
    return _problem_for(idx)

def _submit_answer():
    prob = _current_problem()
    if not prob:
        st.session_state["scroll_to"] = "ef"
        return
    _, total, first, op, second, correct = prob

    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if ans_str == "":
        st.warning("Please enter an answer.")
        st.session_state["scroll_to"] = "ef"
        return

    try:
        user_val = float(ans_str)
    except Exception:
        st.error("Please enter a valid number.")
        st.session_state["scroll_to"] = "ef"
        return

    if math.isclose(user_val, correct, rel_tol=1e-2, abs_tol=1e-2):
        st.success("✅ Correct!")
        st.session_state[SCORE_KEY] += 1
    else:
        st.error(f"❌ Wrong. Correct answer: {correct:g}")

    # Advance
    st.session_state[IDX_KEY] += 1
    st.session_state[ANS_KEY] = ""

    if st.session_state[IDX_KEY] >= total:
        st.success(f"Game Over! Score: {st.session_state[SCORE_KEY]}/{total}")
        _end_game()
    # Always return to this section & keep focus on Answer
    st.session_state["scroll_to"] = "ef"

def render_electro_flash():
    _ensure_state()
    st.subheader("Electro Flash ⚡")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state[BASE_KEY] = st.number_input("Base Number", min_value=1, max_value=20, value=st.session_state[BASE_KEY])
    with c2:
        st.session_state[OP_KEY] = st.selectbox("Operation", ["+", "-", "*", "/"], index=["+","-","*","/"].index(st.session_state[OP_KEY]))
    with c3:
        st.session_state[TOT_KEY] = st.number_input("Number of Questions", min_value=1, max_value=12, value=st.session_state[TOT_KEY])

    b1, b2 = st.columns([1,1])
    if b1.button("Start Game"):
        _start_game()
    if b2.button("Reset"):
        # soft reset
        st.session_state[ACTIVE_KEY] = False
        st.session_state[IDX_KEY] = 0
        st.session_state[NUMS_KEY] = []
        st.session_state[SCORE_KEY] = 0
        st.session_state[ANS_KEY] = ""
        st.session_state["scroll_to"] = "ef"

    if st.session_state[ACTIVE_KEY]:
        prob = _current_problem()
        if prob:
            idx, total, first, op, second, _ = prob
            st.markdown(f"### Problem {idx}/{total}: **{first} {op} {second} = ?**")

            # Enter submits; button does the same
            st.text_input("Answer", key=ANS_KEY, on_change=_submit_answer)
            if st.button("Submit"):
                _submit_answer()
