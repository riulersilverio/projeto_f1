"""Regras de negócio para estratégia de pneus: stints e pit stops.

Módulo puro — recebe dados já buscados pela infraestrutura e devolve
estruturas prontas para exibição.
"""

from __future__ import annotations

import pandas as pd

from f1.domain.models import PitStop, Stint


def build_stint_timeline(
    stints: list[Stint], driver_numbers: list[int] | None = None
) -> pd.DataFrame:
    """Monta a linha do tempo de composto de pneus por piloto.

    Args:
        stints: stints de uma sessão.
        driver_numbers: se informado, filtra apenas estes pilotos.

    Returns:
        DataFrame com uma linha por stint, incluindo a duração em voltas.
    """
    selected = (
        stints
        if driver_numbers is None
        else [stint for stint in stints if stint.driver_number in driver_numbers]
    )
    rows = [
        {
            "driver_number": stint.driver_number,
            "stint_number": stint.stint_number,
            "compound": stint.compound,
            "lap_start": stint.lap_start,
            "lap_end": stint.lap_end,
            "tyre_age_at_start": stint.tyre_age_at_start,
            "lap_count": (
                stint.lap_end - stint.lap_start + 1
                if stint.lap_start is not None and stint.lap_end is not None
                else None
            ),
        }
        for stint in selected
    ]
    columns = [
        "driver_number",
        "stint_number",
        "compound",
        "lap_start",
        "lap_end",
        "tyre_age_at_start",
        "lap_count",
    ]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values(["driver_number", "stint_number"]).reset_index(drop=True)


def build_pit_stop_summary(
    pit_stops: list[PitStop], driver_numbers: list[int] | None = None
) -> pd.DataFrame:
    """Monta a tabela de paradas nos boxes por piloto.

    Args:
        pit_stops: paradas nos boxes de uma sessão.
        driver_numbers: se informado, filtra apenas estes pilotos.

    Returns:
        DataFrame com uma linha por pit stop, ordenado por piloto e volta.
    """
    selected = (
        pit_stops
        if driver_numbers is None
        else [stop for stop in pit_stops if stop.driver_number in driver_numbers]
    )
    rows = [
        {
            "driver_number": stop.driver_number,
            "lap_number": stop.lap_number,
            "pit_duration": stop.pit_duration,
            "date": stop.date,
        }
        for stop in selected
    ]
    columns = ["driver_number", "lap_number", "pit_duration", "date"]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values(["driver_number", "lap_number"]).reset_index(drop=True)
