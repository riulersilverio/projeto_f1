"""Regras de negócio para ritmo de corrida: intervals, bandeiras e clima.

Módulo puro — recebe dados já buscados pela infraestrutura e devolve
estruturas prontas para exibição.
"""

from __future__ import annotations

import pandas as pd

from f1.domain.models import Interval, Position, RaceControlMessage, Weather


def build_position_evolution(
    positions: list[Position], driver_numbers: list[int] | None = None
) -> pd.DataFrame:
    """Monta a evolução de posição de cada piloto ao longo da sessão.

    Args:
        positions: posições registradas de uma sessão.
        driver_numbers: se informado, filtra apenas estes pilotos.

    Returns:
        DataFrame ordenado por piloto e data com a posição em cada instante.
    """
    selected = (
        positions
        if driver_numbers is None
        else [point for point in positions if point.driver_number in driver_numbers]
    )
    rows = [
        {
            "driver_number": point.driver_number,
            "date": point.date,
            "position": point.position,
        }
        for point in selected
    ]
    columns = ["driver_number", "date", "position"]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values(["driver_number", "date"]).reset_index(drop=True)


def latest_classification(positions: list[Position]) -> pd.DataFrame:
    """Retorna a última posição conhecida de cada piloto, ordenada por posição.

    Args:
        positions: posições registradas de uma sessão (todos os pilotos).

    Returns:
        DataFrame com uma linha por piloto (posição mais recente), ordenado
        do 1º colocado em diante. Pilotos sem `date` são ignorados.
    """
    table = build_position_evolution(positions)
    dated = table.dropna(subset=["date"])
    if dated.empty:
        return dated
    latest_idx = dated.groupby("driver_number")["date"].idxmax()
    return dated.loc[latest_idx].sort_values("position").reset_index(drop=True)


def build_gap_evolution(
    intervals: list[Interval], driver_numbers: list[int] | None = None
) -> pd.DataFrame:
    """Monta a evolução do intervalo/gap ao líder ao longo da corrida.

    Args:
        intervals: intervalos de uma sessão.
        driver_numbers: se informado, filtra apenas estes pilotos.

    Returns:
        DataFrame ordenado por piloto e data com gap_to_leader e interval.
    """
    selected = (
        intervals
        if driver_numbers is None
        else [point for point in intervals if point.driver_number in driver_numbers]
    )
    rows = [
        {
            "driver_number": point.driver_number,
            "date": point.date,
            "gap_to_leader": point.gap_to_leader,
            "interval": point.interval,
        }
        for point in selected
    ]
    columns = ["driver_number", "date", "gap_to_leader", "interval"]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values(["driver_number", "date"]).reset_index(drop=True)


def build_race_events(messages: list[RaceControlMessage]) -> pd.DataFrame:
    """Filtra mensagens da direção de prova relevantes para o ritmo de corrida.

    Considera relevantes bandeiras (amarela, vermelha, verde) e ocorrências
    de Safety Car / Virtual Safety Car.

    Args:
        messages: mensagens de race_control de uma sessão.

    Returns:
        DataFrame com uma linha por evento relevante, ordenado por data.
    """
    relevant_categories = {"SafetyCar", "Flag"}
    selected = [
        message
        for message in messages
        if message.category in relevant_categories
        or (message.message and "SAFETY CAR" in message.message.upper())
    ]
    rows = [
        {
            "date": message.date,
            "category": message.category,
            "flag": message.flag,
            "scope": message.scope,
            "lap_number": message.lap_number,
            "message": message.message,
        }
        for message in selected
    ]
    columns = ["date", "category", "flag", "scope", "lap_number", "message"]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def build_weather_timeline(weather: list[Weather]) -> pd.DataFrame:
    """Monta a série temporal de condições climáticas da sessão.

    Args:
        weather: registros climáticos de uma sessão.

    Returns:
        DataFrame ordenado por data com temperatura, umidade, vento e chuva.
    """
    rows = [
        {
            "date": entry.date,
            "air_temperature": entry.air_temperature,
            "track_temperature": entry.track_temperature,
            "humidity": entry.humidity,
            "wind_speed": entry.wind_speed,
            "rainfall": entry.rainfall,
        }
        for entry in weather
    ]
    columns = ["date", "air_temperature", "track_temperature", "humidity", "wind_speed", "rainfall"]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
