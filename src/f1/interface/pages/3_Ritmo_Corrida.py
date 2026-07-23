"""Página de ritmo de corrida: gaps, eventos de pista e clima."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from f1.domain.models import Driver, Interval, RaceControlMessage, Weather
from f1.domain.services.race_pace import (
    build_gap_evolution,
    build_race_events,
    build_weather_timeline,
)
from f1.interface.state import (
    fetch_drivers,
    fetch_intervals,
    fetch_race_control,
    fetch_weather,
    require_session,
)

st.set_page_config(page_title="Ritmo de Corrida", page_icon="📈", layout="wide")
st.title("📈 Ritmo de Corrida")

session_key = require_session()

drivers = {driver["driver_number"]: Driver(**driver) for driver in fetch_drivers(session_key)}
intervals = [Interval(**interval) for interval in fetch_intervals(session_key)]
messages = [RaceControlMessage(**message) for message in fetch_race_control(session_key)]
weather = [Weather(**entry) for entry in fetch_weather(session_key)]


def _driver_label(driver_number: int) -> str:
    driver = drivers.get(driver_number)
    return driver.name_acronym if driver and driver.name_acronym else str(driver_number)


st.subheader("Evolução do gap ao líder")
gap_table = build_gap_evolution(intervals)
if gap_table.empty:
    st.info("Sem dados de intervals para esta sessão (comum em treinos e qualificação).")
else:
    gap_table["gap_to_leader"] = pd.to_numeric(gap_table["gap_to_leader"], errors="coerce")
    gap_table["piloto"] = gap_table["driver_number"].map(_driver_label)
    gap_fig = px.line(gap_table, x="date", y="gap_to_leader", color="piloto")
    st.plotly_chart(gap_fig, width="stretch")

st.subheader("Eventos de pista (bandeiras / Safety Car)")
events_table = build_race_events(messages)
if events_table.empty:
    st.info("Nenhum evento relevante registrado nesta sessão.")
else:
    st.dataframe(events_table, width="stretch")

st.subheader("Clima")
weather_table = build_weather_timeline(weather)
if weather_table.empty:
    st.info("Sem dados climáticos para esta sessão.")
else:
    temperature_fig = px.line(weather_table, x="date", y=["air_temperature", "track_temperature"])
    st.plotly_chart(temperature_fig, width="stretch")

    rainfall_fig = px.bar(weather_table, x="date", y="rainfall")
    st.plotly_chart(rainfall_fig, width="stretch")
