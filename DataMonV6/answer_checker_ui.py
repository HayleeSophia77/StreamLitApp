# answer_checker_ui.py
import streamlit as st
from AnswerChecker import check_answer

EQ_KEY = "ac_equation"
ANS_KEY = "ac_answer"
FOCUS_ANS_FLAG = "_focus_answer"

def _ensure_state():
    if "player_points" not in st.session_state:
        st.session_state.player_points = 0
    st.session_state.setdefault(EQ_KEY, "")
    st.session_state.setdefault(ANS_KEY, "")
    st.session_state.setdefault(FOCUS_ANS_FLAG, False)

def _submit_answer():
    eq = st.session_state.get(EQ_KEY, "").strip()
    ans = st.session_state.get(ANS_KEY, "").strip()

    if not eq or not ans:
        st.warning("Please enter both an equation and an answer.")
        return

    ok = bool(check_answer(f"{eq}={ans}"))
    if ok:
        st.session_state.player_points += 1
        st.success("✅ Correct! +1 point")
        # Optional: clear just the answer for quick next entry
        st.session_state[ANS_KEY] = ""
    else:
        st.error("❌ Incorrect! Try again.")

def _focus_answer_on_enter():
    # Called when you press Enter in the Equation field
    st.session_state[FOCUS_ANS_FLAG] = True

def render_answer_checker():
    _ensure_state()
    st.subheader("Answer Checker")

    # 1) Equation input — pressing Enter sets a flag to focus the Answer box
    st.text_input(
        "Equation",
        placeholder="e.g., 4+4",
        key=EQ_KEY,
        on_change=_focus_answer_on_enter,  # ENTER here moves focus to Answer
    )

    # 2) Answer input — pressing Enter submits
    st.text_input(
        "Your Answer",
        placeholder="e.g., 8",
        key=ANS_KEY,
        on_change=_submit_answer,          # ENTER here submits
    )

    # 3) The button still works (same handler)
    if st.button("Check Answer"):
        _submit_answer()

    # 4) If the flag is set, inject tiny JS to focus the Answer field, then clear flag
    if st.session_state.get(FOCUS_ANS_FLAG):
        st.session_state[FOCUS_ANS_FLAG] = False
        st.markdown(
            """
            <script>
              // Try by aria-label (label text) first:
              const byLabel = document.querySelector('input[aria-label="Your Answer"]');
              if (byLabel) { byLabel.focus(); byLabel.select(); }
              else {
                // Fallback: try by placeholder
                const byPh = Array.from(document.querySelectorAll('input'))
                  .find(el => el.placeholder && el.placeholder.includes('e.g., 8'));
                if (byPh) { byPh.focus(); byPh.select(); }
              }
            </script>
            """,
            unsafe_allow_html=True
        )
