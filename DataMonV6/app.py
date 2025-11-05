# app.py
import streamlit as st
from streamlit.components.v1 import html

from answer_checker_ui import render_answer_checker
from memory_bank_ui import render_memory_bank
from electro_flash_ui import render_electro_flash

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Datamon Web", page_icon="🧮")

st.title("🧮 Datamon — Web Edition")

# --- PLAYER POINTS ---
if "player_points" not in st.session_state:
    st.session_state.player_points = 0

st.sidebar.header("Player Points")
st.sidebar.metric("Total Points", st.session_state.player_points)

# --- SECTION SELECTOR ---
SECTIONS = ["Answer Checker", "Memory Bank", "Electro Flash"]
st.session_state.setdefault("active_section", SECTIONS[0])

choice = st.sidebar.radio(
    "Sections",
    SECTIONS,
    index=SECTIONS.index(st.session_state["active_section"]),
)
st.session_state["active_section"] = choice

# --- ✨ Prevent sidebar focus highlight after pressing Enter ---
html("""
<style>
  /* Remove focus ring from radios in the sidebar */
  [data-testid="stSidebar"] input[type="radio"]:focus {
    outline: none !important;
    box-shadow: none !important;
  }
</style>
<script>
(function(){
  const doc = window.parent.document;
  const sidebar = doc.querySelector('[data-testid="stSidebar"]');
  if (!sidebar) return;

  // Blur any focused control in the sidebar
  const active = doc.activeElement;
  if (active && sidebar.contains(active)) {
    active.blur();
  }

  // Auto-blur if sidebar radios ever get focus
  sidebar.querySelectorAll('input[type="radio"]').forEach(el => {
    el.addEventListener('focus', () => el.blur(), { once: false });
  });
})();
</script>
""", height=0)

# --- SECTION RENDERING ---
st.divider()

if choice == "Answer Checker":
    render_answer_checker()
elif choice == "Memory Bank":
    render_memory_bank()
else:
    render_electro_flash()
