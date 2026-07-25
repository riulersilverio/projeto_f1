"""Página de estratégia de pneus: stints, compostos e paradas nos boxes."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from f1.domain.models import Driver, Lap, PitStop, Stint
from f1.domain.services.tyre_strategy import (
    build_pit_stop_summary,
    build_stint_pace,
    build_stint_timeline,
)
from f1.interface.state import fetch_drivers, fetch_laps, fetch_pit, fetch_stints, require_session
from f1.interface.theme import TYRE_COMPOUND_COLORS, configure_page, driver_color_map, driver_roster

configure_page("Estratégia de Pneus", "🛞")

session_key = require_session()

drivers = {driver["driver_number"]: Driver(**driver) for driver in fetch_drivers(session_key)}
stints = [Stint(**stint) for stint in fetch_stints(session_key)]
pit_stops = [PitStop(**pit) for pit in fetch_pit(session_key)]
laps = [Lap(**lap) for lap in fetch_laps(session_key)]


def _driver_label(driver_number: int) -> str:
    driver = drivers.get(driver_number)
    return driver.name_acronym if driver and driver.name_acronym else str(driver_number)


driver_roster(st, list(drivers.values()), driver_color_map(list(drivers.values())))

st.subheader("Linha do tempo de compostos")
stint_table = build_stint_timeline(stints)
if stint_table.empty:
    st.warning("Sem dados de stints para esta sessão.")
else:
    stint_table["piloto"] = stint_table["driver_number"].map(_driver_label)
    stint_fig = px.bar(
        stint_table,
        x="lap_count",
        y="piloto",
        color="compound",
        color_discrete_map=TYRE_COMPOUND_COLORS,
        orientation="h",
        hover_data=["lap_start", "lap_end", "tyre_age_at_start"],
    )
    st.plotly_chart(stint_fig, width="stretch")

st.subheader("Degradação de pneus")
pace_table = build_stint_pace(laps, stints)
if pace_table.empty:
    st.info("Sem voltas suficientes para estimar a degradação dos stints.")
else:
    pace_table["piloto"] = pace_table["driver_number"].map(_driver_label)
    pace_table["stint"] = "Stint " + pace_table["stint_number"].astype(str)
    pace_fig = px.bar(
        pace_table,
        x="piloto",
        y="degradation_s_per_lap",
        color="compound",
        color_discrete_map=TYRE_COMPOUND_COLORS,
        barmode="group",
        hover_data=["stint"],
        labels={"degradation_s_per_lap": "Degradação (s/volta)"},
    )
    st.plotly_chart(pace_fig, width="stretch")

st.subheader("Paradas nos boxes")
pit_table = build_pit_stop_summary(pit_stops)
if pit_table.empty:
    st.info("Sem pit stops registrados nesta sessão.")
else:
    pit_table["piloto"] = pit_table["driver_number"].map(_driver_label)
    fastest_pit = pit_table.loc[pit_table["pit_duration"].idxmin()]
    st.metric(
        "Pit mais rápido",
        f"{fastest_pit['pit_duration']:.1f} s",
        fastest_pit["piloto"],
        delta_color="off",
    )
    st.dataframe(pit_table, width="stretch")
