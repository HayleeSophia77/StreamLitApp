import streamlit as st
from answer_checker_ui import render_answer_checker
from memory_bank_ui import render_memory_bank
from electro_flash_ui import render_electro_flash

st.set_page_config(page_title="Datamon Web", page_icon="🧮")

st.title("🧮 Datamon — Web Edition")
st.sidebar.header("Player Points")

if "player_points" not in st.session_state:
    st.session_state.player_points = 0

st.sidebar.metric("Total Points", st.session_state.player_points)

tab1, tab2, tab3 = st.tabs(["Answer Checker", "Memory Bank", "Electro Flash"])

with tab1:
    render_answer_checker()

with tab2:
    render_memory_bank()

with tab3:
    render_electro_flash()