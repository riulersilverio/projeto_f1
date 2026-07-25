"""Página de ritmo de corrida: gaps, eventos de pista e clima."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from f1.domain.models import Driver, Interval, Position, RaceControlMessage, Weather
from f1.domain.services.race_pace import (
    build_gap_evolution,
    build_position_evolution,
    build_race_events,
    build_weather_timeline,
)
from f1.interface.state import (
    fetch_drivers,
    fetch_intervals,
    fetch_position,
    fetch_race_control,
    fetch_weather,
    require_session,
)
from f1.interface.theme import configure_page, driver_color_map, driver_roster

configure_page("Ritmo de Corrida", "📈")

session_key = require_session()

drivers_list = [Driver(**driver) for driver in fetch_drivers(session_key)]
drivers = {driver.driver_number: driver for driver in drivers_list}
color_map = driver_color_map(drivers_list)
intervals = [Interval(**interval) for interval in fetch_intervals(session_key)]
positions = [Position(**point) for point in fetch_position(session_key)]
messages = [RaceControlMessage(**message) for message in fetch_race_control(session_key)]
weather = [Weather(**entry) for entry in fetch_weather(session_key)]

driver_roster(st, drivers_list, color_map)


def _driver_label(driver_number: int) -> str:
    driver = drivers.get(driver_number)
    return driver.name_acronym if driver and driver.name_acronym else str(driver_number)


label_color_map = {_driver_label(number): color for number, color in color_map.items()}
events_table = build_race_events(messages)


def _overlay_race_events(fig: go.Figure) -> go.Figure:
    """Sobrepõe bandeiras/Safety Car como linhas verticais tracejadas."""
    for event in events_table.itertuples():
        if event.date is None:
            continue
        fig.add_vline(
            x=event.date,
            line_dash="dash",
            line_color="#8E8E93",
            opacity=0.6,
            annotation_text=event.flag or event.category,
            annotation_position="top",
            annotation_textangle=-90,
            annotation_font_size=10,
            annotation_yshift=10,
        )
    return fig


st.subheader("Classificação ao longo da corrida")
position_table = build_position_evolution(positions)
if position_table.empty:
    st.info("Sem dados de posição para esta sessão (comum em treinos livres e qualificação).")
else:
    position_table["piloto"] = position_table["driver_number"].map(_driver_label)
    position_fig = px.line(
        position_table,
        x="date",
        y="position",
        color="piloto",
        color_discrete_map=label_color_map,
        markers=True,
    )
    position_fig.update_yaxes(autorange="reversed", dtick=1, title="Posição")
    st.plotly_chart(_overlay_race_events(position_fig), width="stretch")

st.subheader("Evolução do gap ao líder")
gap_table = build_gap_evolution(intervals)
if gap_table.empty:
    st.info("Sem dados de intervals para esta sessão (comum em treinos e qualificação).")
else:
    gap_table["gap_to_leader"] = pd.to_numeric(gap_table["gap_to_leader"], errors="coerce")
    gap_table["piloto"] = gap_table["driver_number"].map(_driver_label)
    gap_fig = px.line(
        gap_table, x="date", y="gap_to_leader", color="piloto", color_discrete_map=label_color_map
    )
    st.plotly_chart(_overlay_race_events(gap_fig), width="stretch")

st.subheader("Eventos de pista (bandeiras / Safety Car)")
if events_table.empty:
    st.info("Nenhum evento relevante registrado nesta sessão.")
else:
    st.dataframe(events_table, width="stretch")

st.subheader("Clima")
weather_table = build_weather_timeline(weather)
if weather_table.empty:
    st.info("Sem dados climáticos para esta sessão.")
else:
    weather_col1, weather_col2 = st.columns(2)
    temperature_fig = px.line(weather_table, x="date", y=["air_temperature", "track_temperature"])
    weather_col1.plotly_chart(temperature_fig, width="stretch")

    rainfall_fig = px.bar(weather_table, x="date", y="rainfall")
    weather_col2.plotly_chart(rainfall_fig, width="stretch")
