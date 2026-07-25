"""Regras de negócio para estratégia de pneus: stints e pit stops.

Módulo puro — recebe dados já buscados pela infraestrutura e devolve
estruturas prontas para exibição.
"""

from __future__ import annotations

import pandas as pd

from f1.domain.models import Lap, PitStop, Stint


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


def build_stint_pace(
    laps: list[Lap], stints: list[Stint], driver_numbers: list[int] | None = None
) -> pd.DataFrame:
    """Estima a degradação de pneu de cada stint (segundos perdidos por volta).

    Compara o tempo médio de volta no primeiro terço do stint com o do
    último terço, dividindo pela distância (em voltas) entre esses dois
    blocos. Voltas de entrada/saída de boxes e stints muito curtos (menos
    de 3 voltas válidas) são ignorados por não representarem ritmo de
    corrida real.

    Args:
        laps: voltas de uma sessão (todos os pilotos).
        stints: stints de uma sessão.
        driver_numbers: se informado, filtra apenas estes pilotos.

    Returns:
        DataFrame com uma linha por stint analisável, ordenado por piloto
        e número do stint.
    """
    columns = ["driver_number", "stint_number", "compound", "degradation_s_per_lap"]
    selected_stints = (
        stints
        if driver_numbers is None
        else [stint for stint in stints if stint.driver_number in driver_numbers]
    )
    if not selected_stints:
        return pd.DataFrame(columns=columns)

    laps_by_driver: dict[int, list[Lap]] = {}
    for lap in laps:
        if lap.lap_duration is None or lap.lap_number is None or lap.is_pit_out_lap:
            continue
        laps_by_driver.setdefault(lap.driver_number, []).append(lap)
    for driver_laps in laps_by_driver.values():
        driver_laps.sort(key=lambda lap: lap.lap_number)

    rows = []
    for stint in selected_stints:
        if stint.lap_start is None or stint.lap_end is None:
            continue
        stint_laps = [
            lap
            for lap in laps_by_driver.get(stint.driver_number, [])
            if stint.lap_start <= lap.lap_number <= stint.lap_end
        ]
        third = len(stint_laps) // 3
        if third == 0:
            continue

        early, late = stint_laps[:third], stint_laps[-third:]
        early_avg_duration = sum(lap.lap_duration for lap in early) / third
        late_avg_duration = sum(lap.lap_duration for lap in late) / third
        lap_span = (sum(lap.lap_number for lap in late) - sum(lap.lap_number for lap in early)) / (
            third
        )
        rows.append(
            {
                "driver_number": stint.driver_number,
                "stint_number": stint.stint_number,
                "compound": stint.compound,
                "degradation_s_per_lap": (late_avg_duration - early_avg_duration) / lap_span,
            }
        )
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
