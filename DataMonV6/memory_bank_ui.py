# memory_bank_ui.py
import streamlit as st
from streamlit.components.v1 import html
import math, random, re

PROB_KEY     = "mb_problems"
CURR_KEY     = "mb_current"
ANS_KEY      = "mb_answer"
ATT_KEY      = "mb_attempts"
COR_KEY      = "mb_correct"
ADD_KEY      = "mb_add_input"
ADD_MSG_KEY  = "mb_add_msg"        # flash message after adding
FOCUS_ADD    = "_mb_focus_add"     # flag to focus Add box
FOCUS_ANSWER = "_mb_focus_answer"  # flag to focus Answer box

# Accept: 12+3, 9-8, 9/2, 4*2, 7.5*2 (ints or decimals), single operator only
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
    st.session_state.setdefault(FOCUS_ADD, False)
    st.session_state.setdefault(FOCUS_ANSWER, False)

def _flash(msg, kind="success"):
    st.session_state[ADD_MSG_KEY] = (kind, msg)

def _is_basic(expr: str):
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
    """Handles both Enter on the add box and clicking the Add button."""
    raw = st.session_state.get(ADD_KEY, "").strip()
    if not raw:
        _flash("Please enter a problem first.", "warning")
        # refocus add box
        st.session_state[FOCUS_ADD] = True
        return
    try:
        if not _is_basic(raw):
            raise ValueError("Only basic problems like 5+6, 9-8, 9/2, 4*2 are allowed.")
        _ = _eval_basic(raw)  # validate (e.g., divide-by-zero)
        st.session_state[PROB_KEY].append(raw)
        _flash("Added!", "success")
        st.session_state[ADD_KEY] = ""  # clear for quick next entry
        # keep focus on add so user can enter the next one fast
        st.session_state[FOCUS_ADD] = True
    except Exception as e:
        _flash(f"Invalid problem: {e}", "error")
        st.session_state[FOCUS_ADD] = True

def _start_round():
    if not st.session_state[PROB_KEY]:
        st.warning("Add some problems first.")
        st.session_state[FOCUS_ADD] = True
        return
    st.session_state[ATT_KEY] = 0
    st.session_state[COR_KEY] = 0
    st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
    st.session_state[ANS_KEY] = ""
    # focus the answer box when round begins
    st.session_state[FOCUS_ANSWER] = True

def _submit_answer():
    prob = st.session_state.get(CURR_KEY)
    if not prob:
        st.warning("Start a round first.")
        st.session_state[FOCUS_ADD] = True
        return
    ans_str = st.session_state.get(ANS_KEY, "").strip()
    if not ans_str:
        st.warning("Please enter an answer.")
        st.session_state[FOCUS_ANSWER] = True
        return

    try:
        correct_val = float(_eval_basic(prob))
        user_val = float(ans_str)
    except Exception as e:
        st.error(f"Invalid input: {e}")
        st.session_state[FOCUS_ANSWER] = True
        return

    st.session_state[ATT_KEY] += 1
    if math.isclose(user_val, correct_val, rel_tol=1e-9, abs_tol=1e-9):
        st.session_state[COR_KEY] += 1
        st.session_state.player_points += 1
        st.success("✅ Correct!")
        st.session_state[ANS_KEY] = ""
        # pick another at random (keep bank intact)
        st.session_state[CURR_KEY] = random.choice(st.session_state[PROB_KEY])
        # keep you in the flow: focus the answer for the next question
        st.session_state[FOCUS_ANSWER] = True
    else:
        st.warning("Not quite. Try again!")
        st.session_state[ANS_KEY] = ""  # quick retry
        st.session_state[FOCUS_ANSWER] = True

def _focus_add_input():
    # Robust focus for the "Add problem" text box
    html("""
        <script>
        (function(){
          const doc = window.parent.document;
          const tryFocus = () => {
            // by label
            let input = Array.from(doc.querySelectorAll('label'))
              .find(l => /Enter a problem \(e\.g\., 5\+6, 9-8, 9\/2, 4\*2\)/i.test(l.textContent));
            if (input) {
              input = input.parentElement?.querySelector('input, textarea');
              if (input) { input.focus(); input.select && input.select(); return true; }
            }
            // by placeholder fallback
            const ph = Array.from(doc.querySelectorAll('input'))
              .find(el => el.placeholder && el.placeholder.includes('5+6'));
            if (ph) { ph.focus(); ph.select && ph.select(); return true; }
            return false;
          };
          if (!tryFocus()) setTimeout(tryFocus, 50);
          setTimeout(tryFocus, 150);
        })();
        </script>
    """, height=0)

def _focus_answer_input():
    # Robust focus for the "Your Answer" box
    html("""
        <script>
        (function(){
          const doc = window.parent.document;
          const tryFocus = () => {
            // by label
            let input = Array.from(doc.querySelectorAll('label'))
              .find(l => /Your Answer/i.test(l.textContent));
            if (input) {
              input = input.parentElement?.querySelector('input');
              if (input) { input.focus(); input.select && input.select(); return true; }
            }
            // by placeholder fallback (none by default)
            const any = Array.from(doc.querySelectorAll('input')).find(el => el.type === 'text');
            if (any) { any.focus(); any.select && any.select(); return true; }
            return false;
          };
          if (!tryFocus()) setTimeout(tryFocus, 50);
          setTimeout(tryFocus, 150);
        })();
        </script>
    """, height=0)

def render_memory_bank():
    _ensure_state()
    st.subheader("Memory Bank")

    with st.expander("➕ Add Problems", expanded=True):
        # ENTER here adds the problem (same as clicking Add)
        st.text_input(
            "Enter a problem (e.g., 5+6, 9-8, 9/2, 4*2)",
            key=ADD_KEY,
            on_change=_add_problem,
        )
        if st.button("Add"):
            _add_problem()

        # one-shot flash after rerun
        flash = st.session_state.get(ADD_MSG_KEY)
        if flash:
            kind, msg = flash
            getattr(st, kind)(msg) if hasattr(st, kind) else st.info(msg)
            st.session_state[ADD_MSG_KEY] = None

        if st.session_state[PROB_KEY]:
            st.write("Problems in bank:")
            st.code("\n".join(st.session_state[PROB_KEY]))

        # focus add input if flagged
        if st.session_state.get(FOCUS_ADD):
            st.session_state[FOCUS_ADD] = False
            _focus_add_input()

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
        # ENTER submits the answer
        st.text_input("Your Answer", key=ANS_KEY, on_change=_submit_answer)
        if st.button("Submit"):
            _submit_answer()

    # focus answer input if flagged (after start round / after submit)
    if st.session_state.get(FOCUS_ANSWER):
        st.session_state[FOCUS_ANSWER] = False
        _focus_answer_input()

    if st.session_state[ATT_KEY] > 0:
        st.caption(f"Correct: {st.session_state[COR_KEY]} / Attempts: {st.session_state[ATT_KEY]}")
