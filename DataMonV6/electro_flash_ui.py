# electro_flash_ui.py
import streamlit as st
from streamlit.components.v1 import html
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
FOCUS_ANS  = "_ef_focus_answer"   # flag to focus Answer box

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
    st.session_state.setdefault(FOCUS_ANS, False)

def _start_game():
    st.session_state[ACTIVE_KEY] = True
    st.session_state[SCORE_KEY] = 0
    st.session_state[START_KEY] = time.time()
    total = int(st.session_state[TOT_KEY])
    st.session_state[NUMS_KEY] = random.sample(range(1, 13), total)
    st.session_state[IDX_KEY] = 0
    st.session_state[ANS_KEY] = ""
    st.session_state[FOCUS_ANS] = True  # focus answer when starting

def _end_game():
    st.session_state.player_points += st.session_state[SCORE_KEY]
    st.session_state[ACTIVE_KEY] = False

def _current_problem():
    idx = st.session_state[IDX_KEY]
    total = int(st.session_state[TOT_KEY])
    if idx >= total:
        return None
    base = int(st.session_state[BASE_KEY])
    op = st.session_state[OP_KEY]
    n = st.session_state[NUMS_KEY][idx]
    # compute correct answer
    if op == "+":
        correct = base + n
    elif op == "-":
        correct = (n + base) - base  # always positive left-side
        correct = n  # but we use expression display below; compute separately
        correct = (n + base) - base
    elif op == "*":
        correct = base * n
    elif op == "/":
        correct = (n * base) / base
    else:
        correct = base * n
    return (idx+1, total, base, op, n, correct)

def _submit_answer():
    prob = _current_problem()
    if not prob:
        return
    _, total, base, op, n, correct = prob
    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if ans_str == "":
        st.warning("Please enter an answer.")
        st.session_state[FOCUS_ANS] = True
        return

    try:
        user_val = float(ans_str)
        corr_val = float(correct)
    except Exception:
        st.error("Please enter a valid number.")
        st.session_state[FOCUS_ANS] = True
        return

    if math.isclose(user_val, corr_val, rel_tol=1e-2, abs_tol=1e-2):
        st.success("✅ Correct!")
        st.session_state[SCORE_KEY] += 1
    else:
        st.error(f"❌ Wrong. Correct answer: {corr_val}")

    st.session_state[IDX_KEY] += 1
    st.session_state[ANS_KEY] = ""  # clear for next

    if st.session_state[IDX_KEY] >= total:
        st.success(f"Game Over! Score: {st.session_state[SCORE_KEY]}/{total}")
        _end_game()
    else:
        st.session_state[FOCUS_ANS] = True  # focus for next question

def _focus_answer_input():
    # Robust focus for the "Answer" input
    html("""
        <script>
        (function(){
          const doc = window.parent.document;
          const tryFocus = () => {
            // Prefer label match
            let input = Array.from(doc.querySelectorAll('label'))
              .find(l => /Answer/i.test(l.textContent));
            if (input) {
              input = input.parentElement?.querySelector('input');
              if (input) { input.focus(); input.select && input.select(); return true; }
            }
            // Fallback: first text input on the page
            const any = Array.from(doc.querySelectorAll('input')).find(el => el.type === 'text');
            if (any) { any.focus(); any.select && any.select(); return true; }
            return false;
          };
          if (!tryFocus()) setTimeout(tryFocus, 50);
          setTimeout(tryFocus, 150);
        })();
        </script>
    """, height=0)

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
        _ensure_state()

    if st.session_state[ACTIVE_KEY]:
        prob = _current_problem()
        if prob:
            idx, total, base, op, n, correct = prob
            # Display expression nicely (add/sub/div logic to match console version)
            if op == "+":
                first, second = base, n
            elif op == "-":
                first, second = n + base, base
            elif op == "*":
                first, second = base, n
            elif op == "/":
                first, second = n * base, base
            else:
                first, second = base, n

            st.markdown(f"### Problem {idx}/{total}: **{first} {op} {second} = ?**")

            # ENTER submits; button does the same
            st.text_input("Answer", key=ANS_KEY, on_change=_submit_answer)
            if st.button("Submit"):
                _submit_answer()

            # focus Answer when flagged
            if st.session_state.get(FOCUS_ANS):
                st.session_state[FOCUS_ANS] = False
                _focus_answer_input()
        else:
            st.success(f"Game Over! Score: {st.session_state[SCORE_KEY]}/{int(st.session_state[TOT_KEY])}")