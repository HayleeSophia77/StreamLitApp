# electro_flash_ui.py
import streamlit as st
from streamlit.components.v1 import html
import random, math, time

# --- Keys & flags ---
BASE_KEY    = "ef_base"
OP_KEY      = "ef_op"
TOT_KEY     = "ef_total"
IDX_KEY     = "ef_idx"
NUMS_KEY    = "ef_numbers"
ANS_KEY     = "ef_answer_input"
SCORE_KEY   = "ef_score"
START_KEY   = "ef_start"
ACTIVE_KEY  = "ef_active"
FOCUS_FLAG  = "_ef_focus_answer"   # set when we should focus answer
ANCHOR_FLAG = "_ef_anchor_scroll"  # set when we should scroll back to this section
ANCHOR_ID   = "ef_anchor"          # stable anchor id for scrolling

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
    st.session_state.setdefault(FOCUS_FLAG, False)
    st.session_state.setdefault(ANCHOR_FLAG, False)

def _start_game():
    st.session_state[ACTIVE_KEY] = True
    st.session_state[SCORE_KEY] = 0
    st.session_state[START_KEY] = time.time()
    total = int(st.session_state[TOT_KEY])
    st.session_state[NUMS_KEY] = random.sample(range(1, 13), total)
    st.session_state[IDX_KEY] = 0
    st.session_state[ANS_KEY] = ""
    # after starting, we want to be at this section and focused
    st.session_state[FOCUS_FLAG] = True
    st.session_state[ANCHOR_FLAG] = True

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
        # non-negative: (n+base) - base = n
        first, second = n + base, base
        correct = first - second
    elif op == "*":
        first, second = base, n
        correct = first * second
    elif op == "/":
        # divisible: (n*base) / base = n
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
        return
    _, total, first, op, second, correct = prob

    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if ans_str == "":
        st.warning("Please enter an answer.")
        st.session_state[FOCUS_FLAG] = True
        st.session_state[ANCHOR_FLAG] = True
        return

    try:
        user_val = float(ans_str)
    except Exception:
        st.error("Please enter a valid number.")
        st.session_state[FOCUS_FLAG] = True
        st.session_state[ANCHOR_FLAG] = True
        return

    if math.isclose(user_val, correct, rel_tol=1e-2, abs_tol=1e-2):
        st.success("✅ Correct!")
        st.session_state[SCORE_KEY] += 1
    else:
        st.error(f"❌ Wrong. Correct answer: {correct:g}")

    # advance to next (or end)
    st.session_state[IDX_KEY] += 1
    st.session_state[ANS_KEY] = ""

    if st.session_state[IDX_KEY] >= total:
        st.success(f"Game Over! Score: {st.session_state[SCORE_KEY]}/{total}")
        _end_game()
    else:
        # after each submit, keep user here and focus next answer
        st.session_state[FOCUS_FLAG] = True
        st.session_state[ANCHOR_FLAG] = True

def _scroll_and_focus_answer():
    """Scroll back to Electro Flash section and focus the Answer input."""
    st.session_state[ANCHOR_FLAG] = False
    st.session_state[FOCUS_FLAG] = False
    html(rf"""
        <script>
        (function() {{
          const doc = window.parent.document;
          const scrollToAnchor = () => {{
            const a = doc.getElementById("{ANCHOR_ID}");
            if (a && a.scrollIntoView) a.scrollIntoView({{behavior: 'smooth', block: 'start'}});
          }};
          const focusAnswer = () => {{
            // Prefer a label that says "Answer"
            let lbl = Array.from(doc.querySelectorAll('label')).find(l => /\bAnswer\b/i.test(l.textContent));
            let input = lbl ? (lbl.parentElement && lbl.parentElement.querySelector('input')) : null;
            if (!input) {{
              // fallback: first visible text input
              input = Array.from(doc.querySelectorAll('input'))
                .find(el => el.type === 'text' && el.offsetParent !== null);
            }}
            if (input) {{
              input.focus(); input.select && input.select();
              return true;
            }}
            return false;
          }};
          const doBoth = () => {{ scrollToAnchor(); focusAnswer(); }};
          // Try a few times to handle Streamlit layout timing
          doBoth();
          setTimeout(doBoth, 80);
          setTimeout(doBoth, 180);
          setTimeout(doBoth, 320);
        }})();
        </script>
    """, height=0)

def render_electro_flash():
    _ensure_state()
    st.subheader("Electro Flash ⚡")

    # ---- anchor for scroll-back ----
    st.markdown(f'<div id="{ANCHOR_ID}"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state[BASE_KEY] = st.number_input(
            "Base Number", min_value=1, max_value=20, value=st.session_state[BASE_KEY]
        )
    with c2:
        st.session_state[OP_KEY] = st.selectbox(
            "Operation", ["+", "-", "*", "/"], index=["+","-","*","/"].index(st.session_state[OP_KEY])
        )
    with c3:
        st.session_state[TOT_KEY] = st.number_input(
            "Number of Questions", min_value=1, max_value=12, value=st.session_state[TOT_KEY]
        )

    b1, b2 = st.columns([1,1])
    if b1.button("Start Game"):
        _start_game()
    if b2.button("Reset"):
        st.session_state[ACTIVE_KEY] = False
        st.session_state[IDX_KEY] = 0
        st.session_state[NUMS_KEY] = []
        st.session_state[SCORE_KEY] = 0
        st.session_state[ANS_KEY] = ""
        st.session_state[FOCUS_FLAG] = False
        st.session_state[ANCHOR_FLAG] = True  # scroll back to the section

    if st.session_state[ACTIVE_KEY]:
        prob = _current_problem()
        if prob:
            idx, total, first, op, second, _ = prob
            st.markdown(f"### Problem {idx}/{total}: **{first} {op} {second} = ?**")

            # ENTER submits; button does the same
            st.text_input("Answer", key=ANS_KEY, on_change=_submit_answer)
            if st.button("Submit"):
                _submit_answer()

    # After start/submit/reset, if flagged, scroll back & focus the Answer box
    if st.session_state.get(ANCHOR_FLAG) or st.session_state.get(FOCUS_FLAG):
        _scroll_and_focus_answer()
