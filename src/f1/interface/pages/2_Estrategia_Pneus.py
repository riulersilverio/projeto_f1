"""Página de estratégia de pneus: stints, compostos e paradas nos boxes."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from f1.domain.models import Driver, PitStop, Stint
from f1.domain.services.tyre_strategy import build_pit_stop_summary, build_stint_timeline
from f1.interface.state import fetch_drivers, fetch_pit, fetch_stints, require_session

st.set_page_config(page_title="Estratégia de Pneus", page_icon="🛞", layout="wide")
st.title("🛞 Estratégia de Pneus")

session_key = require_session()

drivers = {driver["driver_number"]: Driver(**driver) for driver in fetch_drivers(session_key)}
stints = [Stint(**stint) for stint in fetch_stints(session_key)]
pit_stops = [PitStop(**pit) for pit in fetch_pit(session_key)]


def _driver_label(driver_number: int) -> str:
    driver = drivers.get(driver_number)
    return driver.name_acronym if driver and driver.name_acronym else str(driver_number)


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
        orientation="h",
        hover_data=["lap_start", "lap_end", "tyre_age_at_start"],
    )
    st.plotly_chart(stint_fig, width="stretch")

st.subheader("Paradas nos boxes")
pit_table = build_pit_stop_summary(pit_stops)
if pit_table.empty:
    st.info("Sem pit stops registrados nesta sessão.")
else:
    pit_table["piloto"] = pit_table["driver_number"].map(_driver_label)
    st.dataframe(pit_table, width="stretch")
