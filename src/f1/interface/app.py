"""Home do Streamlit: seleção de ano, Grande Prêmio e sessão."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from f1.domain.models import Driver, Position
from f1.domain.services.race_pace import latest_classification
from f1.interface.state import fetch_drivers, fetch_meetings, fetch_position, fetch_sessions
from f1.interface.theme import configure_page

configure_page(
    "F1 Dashboard",
    "🏎️",
    subtitle="Dados em tempo real e históricos da Fórmula 1, via OpenF1.",
)

current_year = datetime.now().year
years = list(range(2023, current_year + 1))[::-1]

st.sidebar.header("Seleção de sessão")
selected_year = st.sidebar.selectbox("Ano", years)

meetings = fetch_meetings(selected_year)
if not meetings:
    st.sidebar.warning("Nenhum Grande Prêmio encontrado para o ano selecionado.")
    st.stop()

meeting_options = {meeting["meeting_name"]: meeting["meeting_key"] for meeting in meetings}
selected_meeting_name = st.sidebar.selectbox("Grande Prêmio", list(meeting_options.keys()))
meeting_key = meeting_options[selected_meeting_name]

sessions = fetch_sessions(meeting_key)
if not sessions:
    st.sidebar.warning("Nenhuma sessão encontrada para este Grande Prêmio.")
    st.stop()

session_options = {session["session_name"]: session["session_key"] for session in sessions}
selected_session_name = st.sidebar.selectbox("Sessão", list(session_options.keys()))
session_key = session_options[selected_session_name]

st.session_state["session_key"] = session_key
st.session_state["meeting_name"] = selected_meeting_name
st.session_state["session_name"] = selected_session_name

st.success(f"Sessão selecionada: **{selected_meeting_name} — {selected_session_name}**")
st.info("Use o menu lateral para navegar até as páginas de análise.")

session_info = next((s for s in sessions if s["session_key"] == session_key), None)
if session_info:
    col1, col2, col3 = st.columns(3)
    col1.metric("Local", session_info.get("location", "-"))
    col2.metric("País", session_info.get("country_name", "-"))
    col3.metric("Início", str(session_info.get("date_start", "-")))

st.subheader("Classificação (top 3)")
positions = [Position(**point) for point in fetch_position(session_key)]
classification = latest_classification(positions)
if classification.empty:
    st.info("Classificação não disponível para esta sessão (comum em treinos livres).")
else:
    drivers_by_number = {
        driver["driver_number"]: Driver(**driver) for driver in fetch_drivers(session_key)
    }
    medals = ["🥇", "🥈", "🥉"]
    top_columns = st.columns(3)
    top_rows = classification.head(3).itertuples()
    for col, medal, row in zip(top_columns, medals, top_rows, strict=False):
        driver = drivers_by_number.get(row.driver_number)
        label = driver.name_acronym if driver and driver.name_acronym else str(row.driver_number)
        col.metric(f"{medal} P{int(row.position)}", label)
        col.caption(driver.team_name if driver and driver.team_name else "-")
