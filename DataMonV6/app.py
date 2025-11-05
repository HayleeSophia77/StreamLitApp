# app.py
import streamlit as st
from answer_checker_ui import render_answer_checker
from memory_bank_ui import render_memory_bank
from electro_flash_ui import render_electro_flash

st.set_page_config(page_title="Datamon Web", page_icon="🧮")

# Remember selected section across reruns
SECTIONS = ["Answer Checker", "Memory Bank", "Electro Flash"]
st.session_state.setdefault("active_section", SECTIONS[0])

st.title("🧮 Datamon — Web Edition")
st.sidebar.header("Player Points")
if "player_points" not in st.session_state:
    st.session_state.player_points = 0
st.sidebar.metric("Total Points", st.session_state.player_points)

# Controlled navigation (no more tab snap-back)
choice = st.radio(
    "Sections",
    SECTIONS,
    index=SECTIONS.index(st.session_state["active_section"]),
    horizontal=True,
)
st.session_state["active_section"] = choice

st.divider()

if choice == "Answer Checker":
    render_answer_checker()
elif choice == "Memory Bank":
    render_memory_bank()
else:
    render_electro_flash()
