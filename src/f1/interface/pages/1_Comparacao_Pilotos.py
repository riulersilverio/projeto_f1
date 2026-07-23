"""Página de comparação de pilotos: tempos de volta, setores e telemetria."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from f1.domain.models import CarData, Driver, Lap
from f1.domain.services.driver_comparison import (
    best_lap_per_driver,
    compare_lap_times,
    compare_telemetry,
)
from f1.interface.state import fetch_car_data, fetch_drivers, fetch_laps, require_session

st.set_page_config(page_title="Comparação de Pilotos", page_icon="🏁", layout="wide")
st.title("🏁 Comparação de Pilotos")

session_key = require_session()

drivers = [Driver(**driver) for driver in fetch_drivers(session_key)]
if not drivers:
    st.warning("Nenhum piloto encontrado para esta sessão.")
    st.stop()

driver_labels = {
    f"{driver.name_acronym} — {driver.full_name}": driver.driver_number for driver in drivers
}
default_labels = list(driver_labels.keys())[:2]
selected_labels = st.multiselect("Pilotos", list(driver_labels.keys()), default=default_labels)
driver_numbers = [driver_labels[label] for label in selected_labels]

if not driver_numbers:
    st.info("Selecione ao menos um piloto para comparar.")
    st.stop()

laps = [Lap(**lap) for lap in fetch_laps(session_key)]

st.subheader("Tempos de volta")
lap_table = compare_lap_times(laps, driver_numbers)
if lap_table.empty:
    st.info("Sem dados de voltas para os pilotos selecionados.")
else:
    lap_fig = px.line(
        lap_table, x="lap_number", y="lap_duration", color="driver_number", markers=True
    )
    st.plotly_chart(lap_fig, width="stretch")

    st.subheader("Melhor volta")
    st.dataframe(best_lap_per_driver(laps, driver_numbers), width="stretch")

st.subheader("Telemetria")
if len(driver_numbers) > 2:
    st.info("Selecione até 2 pilotos para comparar telemetria.")
else:
    car_data = [
        CarData(**point)
        for driver_number in driver_numbers
        for point in fetch_car_data(session_key, driver_number)
    ]
    telemetry = compare_telemetry(car_data, driver_numbers)
    if telemetry.empty:
        st.info("Sem dados de telemetria disponíveis para os pilotos selecionados.")
    else:
        speed_fig = px.line(telemetry, x="date", y="speed", color="driver_number")
        st.plotly_chart(speed_fig, width="stretch")
