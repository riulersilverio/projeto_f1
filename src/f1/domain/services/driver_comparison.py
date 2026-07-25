"""Regras de negócio para comparação de pilotos: voltas, setores e telemetria.

Este módulo é puro — não realiza nenhuma chamada de rede. Recebe os dados
já buscados pela camada de infraestrutura e devolve estruturas prontas
para exibição (ex: DataFrames do pandas).
"""

from __future__ import annotations

import pandas as pd

from f1.domain.models import CarData, Lap


def compare_lap_times(laps: list[Lap], driver_numbers: list[int]) -> pd.DataFrame:
    """Monta uma tabela de tempos de volta e setores para os pilotos informados.

    Args:
        laps: voltas de uma sessão (todos os pilotos).
        driver_numbers: números dos pilotos a comparar.

    Returns:
        DataFrame com uma linha por volta válida, ordenado por piloto e volta.
    """
    selected = [lap for lap in laps if lap.driver_number in driver_numbers]
    rows = [
        {
            "driver_number": lap.driver_number,
            "lap_number": lap.lap_number,
            "lap_duration": lap.lap_duration,
            "duration_sector_1": lap.duration_sector_1,
            "duration_sector_2": lap.duration_sector_2,
            "duration_sector_3": lap.duration_sector_3,
        }
        for lap in selected
        if lap.lap_duration is not None
    ]
    if not rows:
        return pd.DataFrame(
            columns=[
                "driver_number",
                "lap_number",
                "lap_duration",
                "duration_sector_1",
                "duration_sector_2",
                "duration_sector_3",
            ]
        )
    return pd.DataFrame(rows).sort_values(["driver_number", "lap_number"]).reset_index(drop=True)


def best_lap_per_driver(laps: list[Lap], driver_numbers: list[int]) -> pd.DataFrame:
    """Retorna a melhor volta (menor tempo) de cada piloto informado.

    Args:
        laps: voltas de uma sessão (todos os pilotos).
        driver_numbers: números dos pilotos a comparar.

    Returns:
        DataFrame com uma linha por piloto contendo sua melhor volta.
    """
    table = compare_lap_times(laps, driver_numbers)
    if table.empty:
        return table
    best_idx = table.groupby("driver_number")["lap_duration"].idxmin()
    return table.loc[best_idx].sort_values("lap_duration").reset_index(drop=True)


def compare_sectors(laps: list[Lap], driver_numbers: list[int]) -> pd.DataFrame:
    """Compara os tempos de setor da melhor volta de cada piloto.

    Args:
        laps: voltas de uma sessão (todos os pilotos).
        driver_numbers: números dos pilotos a comparar.

    Returns:
        DataFrame no formato longo, com uma linha por (piloto, setor).
    """
    columns = ["driver_number", "sector", "duration"]
    best_laps = best_lap_per_driver(laps, driver_numbers)
    if best_laps.empty:
        return pd.DataFrame(columns=columns)

    sector_labels = {
        "duration_sector_1": "S1",
        "duration_sector_2": "S2",
        "duration_sector_3": "S3",
    }
    melted = best_laps.melt(
        id_vars="driver_number",
        value_vars=list(sector_labels),
        var_name="sector",
        value_name="duration",
    )
    melted["sector"] = melted["sector"].map(sector_labels)
    return (
        melted.dropna(subset=["duration"])
        .sort_values(["driver_number", "sector"])
        .reset_index(drop=True)
    )


def speed_trap_summary(laps: list[Lap], driver_numbers: list[int]) -> pd.DataFrame:
    """Retorna a velocidade máxima (speed trap) registrada por cada piloto.

    Args:
        laps: voltas de uma sessão (todos os pilotos).
        driver_numbers: números dos pilotos a comparar.

    Returns:
        DataFrame com uma linha por piloto, ordenado da maior para a menor
        velocidade máxima.
    """
    columns = ["driver_number", "top_speed"]
    selected = [
        lap for lap in laps if lap.driver_number in driver_numbers and lap.st_speed is not None
    ]
    if not selected:
        return pd.DataFrame(columns=columns)

    rows = [{"driver_number": lap.driver_number, "top_speed": lap.st_speed} for lap in selected]
    return (
        pd.DataFrame(rows)
        .groupby("driver_number", as_index=False)["top_speed"]
        .max()
        .sort_values("top_speed", ascending=False)
        .reset_index(drop=True)
    )


def compare_telemetry(car_data: list[CarData], driver_numbers: list[int]) -> pd.DataFrame:
    """Monta uma série temporal de telemetria (velocidade, RPM, marcha, DRS).

    Args:
        car_data: pontos de telemetria de uma sessão (todos os pilotos).
        driver_numbers: números dos pilotos a comparar.

    Returns:
        DataFrame ordenado por piloto e data com os dados de telemetria.
    """
    selected = [point for point in car_data if point.driver_number in driver_numbers]
    rows = [
        {
            "driver_number": point.driver_number,
            "date": point.date,
            "speed": point.speed,
            "rpm": point.rpm,
            "n_gear": point.n_gear,
            "throttle": point.throttle,
            "brake": point.brake,
            "drs": point.drs,
        }
        for point in selected
    ]
    if not rows:
        return pd.DataFrame(
            columns=["driver_number", "date", "speed", "rpm", "n_gear", "throttle", "brake", "drs"]
        )
    return pd.DataFrame(rows).sort_values(["driver_number", "date"]).reset_index(drop=True)
