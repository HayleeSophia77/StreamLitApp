# answer_checker_ui.py
import streamlit as st
from streamlit.components.v1 import html
from AnswerChecker import check_answer

ANCHOR_ID   = "ac_anchor"         # a stable anchor to scroll back to this section
EQ_KEY      = "ac_equation"
ANS_KEY     = "ac_answer"
FOCUS_FLAG  = "_ac_focus_eq"      # set True after a correct answer to re-focus & scroll here

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(EQ_KEY, "")
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(FOCUS_FLAG, False)

def _submit_answer():
    eq = st.session_state.get(EQ_KEY, "").strip()
    ans = st.session_state.get(ANS_KEY, "").strip()
    if not eq or not ans:
        st.warning("Please enter both an equation and an answer.")
        return

    try:
        ok = bool(check_answer(f"{eq}={ans}"))
    except Exception as e:
        st.error(f"Error checking answer: {e}")
        return

    if ok:
        # Award point, clear both fields, and set focus/scroll flag
        st.session_state.player_points += 1
        st.success("✅ Correct! +1 point")
        st.session_state[EQ_KEY] = ""
        st.session_state[ANS_KEY] = ""
        st.session_state[FOCUS_FLAG] = True
    else:
        # Keep equation, clear only answer for retry
        st.error("❌ Incorrect! Try again.")
        st.session_state[ANS_KEY] = ""

def render_answer_checker():
    _ensure_state()

    st.subheader("Answer Checker")

    # Anchor: gives us a stable target for scrolling back after reruns
    st.markdown(f'<div id="{ANCHOR_ID}"></div>', unsafe_allow_html=True)

    # Inputs (Enter on Answer submits)
    st.text_input("Equation", placeholder="e.g., 4+4", key=EQ_KEY)
    st.text_input("Your Answer", placeholder="e.g., 8", key=ANS_KEY, on_change=_submit_answer)

    if st.button("Check Answer"):
        _submit_answer()

    # If a correct answer was just submitted, scroll to this section and focus Equation.
    if st.session_state.get(FOCUS_FLAG):
        st.session_state[FOCUS_FLAG] = False
        # Use a component so the script actually runs in the Cloud environment.
        html(f"""
            <script>
            (function() {{
              const doc = window.parent.document;

              const focusEq = () => {{
                // Scroll to the anchor first
                const anchor = doc.getElementById("{ANCHOR_ID}");
                if (anchor && anchor.scrollIntoView) anchor.scrollIntoView({{behavior: 'smooth', block: 'start'}});

                // Then try to focus the Equation input
                let input = doc.querySelector('input[aria-label="Equation"]');
                if (!input) {{
                  // fallback: find input near a label containing "Equation"
                  const lbl = Array.from(doc.querySelectorAll('label')).find(l => /\\bEquation\\b/i.test(l.textContent));
                  if (lbl) input = lbl.parentElement && lbl.parentElement.querySelector('input');
                }}
                if (!input) {{
                  // fallback by placeholder
                  input = Array.from(doc.querySelectorAll('input')).find(el => el.placeholder && el.placeholder.includes('4+4'));
                }}
                if (input) {{
                  input.focus();
                  if (input.select) input.select();
                  return true;
                }}
                return false;
              }};

              // Try a few times as Streamlit lays out the DOM
              if (!focusEq()) setTimeout(focusEq, 80);
              setTimeout(focusEq, 180);
              setTimeout(focusEq, 350);
            }})();
            </script>
        """, height=0)