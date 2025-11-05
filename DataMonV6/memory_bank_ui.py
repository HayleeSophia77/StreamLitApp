# memory_bank_ui.py
import streamlit as st
import math, random, re

PROB_KEY    = "mb_problems"
CURR_KEY    = "mb_current"
ANS_KEY     = "mb_answer"
ATT_KEY     = "mb_attempts"
COR_KEY     = "mb_correct"
ADD_KEY     = "mb_add_input"
ADD_MSG_KEY = "mb_add_msg"

_BASIC_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*([+\-*/])\s*([0-9]+(?:\.[0-9]+)?)\s*$")

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
    st.session_state[ADD_MSG_KEY] = (kind, msg)

def _is_basic(expr: str) -> bool:
    return _BASIC_RE.match(expr or "") is not None

def _eval_basic(expr: str) -> float:
    m = _BASIC_RE.match(expr or "")
    if not m:
        raise ValueError("Only basic problems like 5+6, 9-8, 9/2, 4*2 are allowed.")
    a_str, op, b_str = m.groups()
    a = float(a_str); b = float(b_str)
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0: raise ValueError("Division by zero is not allowed.")
        return a / b
    raise ValueError("Unsupported operator.")

def _add_problem():
    raw = st.session_state.get(ADD_KEY, "").strip()
    if not raw:
        _flash("Please enter a problem first.", "warning")
        return
    try:
        if not _is_basic(raw):
            raise ValueError("Only basic problems like 5+6, 9-8, 9/2, 4*2 are allowed.")
        _ = _eval_basic(raw)  # validate (e.g., /0)
        st.session_state[PROB_KEY].append(raw)
        _flash("Added!", "success")
        st.session_state[ADD_KEY] = ""
    except Exception as e:
        _flash(f"Invalid problem: {e}", "error")

def _start_round():
    if not st.session_state[PROB_KEY]:
        st.warning("Add some problems first.")
        st.session_state["scroll_to"] = "mb"
        return
    st.session_state[ATT_KEY] = 0
    st.session_state[COR_KEY] = 0
    st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    st.session_state[ANS_KEY] = ""
    st.session_state["scroll_to"] = "mb"

def _submit_answer():
    prob = st.session_state.get(CURR_KEY)
    if not prob:
        st.warning("Start a round first.")
        st.session_state["scroll_to"] = "mb"
        return
    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if not ans_str:
        st.warning("Please enter an answer.")
        st.session_state["scroll_to"] = "mb"
        return

    try:
        correct_val = float(_eval_basic(prob))
        user_val = float(ans_str)
    except Exception as e:
        st.error(f"Invalid input: {e}")
        st.session_state["scroll_to"] = "mb"
        return

    st.session_state[ATT_KEY] += 1
    if math.isclose(user_val, correct_val, rel_tol=1e-9, abs_tol=1e-9):
        st.session_state[COR_KEY] += 1
        st.session_state.player_points += 1
        st.success("✅ Correct!")
        st.session_state[ANS_KEY] = ""
        # next problem
        st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    else:
        st.warning("Not quite. Try again!")
        st.session_state[ANS_KEY] = ""

    st.session_state["scroll_to"] = "mb"

def render_memory_bank():
    _ensure_state()
    st.subheader("Memory Bank")

    with st.expander("➕ Add Problems", expanded=True):
        # Enter adds; button adds too
        st.text_input(
            "Enter a problem (e.g., 5+6, 9-8, 9/2, 4*2)",
            key=ADD_KEY,
            on_change=_add_problem,
        )
        if st.button("Add"):
            _add_problem()

        flash = st.session_state.get(ADD_MSG_KEY)
        if flash:
            kind, msg = flash
            getattr(st, kind)(msg) if hasattr(st, kind) else st.info(msg)
            st.session_state[ADD_MSG_KEY] = None

        if st.session_state[PROB_KEY]:
            st.write("Problems in bank:")
            st.code("\n".join(st.session_state[PROB_KEY]))

    c1, c2 = st.columns([1, 1])
    if c1.button("🧪 Start Practice Round"):
        _start_round()
    if c2.button("End Round"):
        if st.session_state[ATT_KEY] > 0:
            ratio = (st.session_state[COR_KEY] / st.session_state[ATT_KEY]) if st.session_state[ATT_KEY] else 0
            if ratio == 1 and st.session_state[ATT_KEY] != 0:
                st.info("Perfect score! You're a math wizard!")
            elif ratio > 0.75:
                st.info("Great job! You really know your stuff.")
            elif ratio > 0.5:
                st.info("Not bad! Keep practicing and you'll get even better.")
            elif st.session_state[COR_KEY] > 0:
                st.info("You got some right! Don’t give up — try again!")
            else:
                st.info("Oof, tough round! Time to hit the books.")
        else:
            st.info("No attempts yet.")

    current = st.session_state.get(CURR_KEY)
    if current:
        st.markdown(f"### Solve: `{current}`")
        # Enter submits; button submits as well
        st.text_input("Your Answer", key=ANS_KEY, on_change=_submit_answer)
        if st.button("Submit"):
            _submit_answer()

    if st.session_state[ATT_KEY] > 0:
        st.caption(f"Correct: {st.session_state[COR_KEY]} / Attempts: {st.session_state[ATT_KEY]}")

