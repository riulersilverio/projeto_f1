from f1.domain.models import CarData, Lap
from f1.domain.services.driver_comparison import (
    best_lap_per_driver,
    compare_lap_times,
    compare_sectors,
    compare_telemetry,
    speed_trap_summary,
)

LAPS = [
    Lap(
        driver_number=1,
        lap_number=1,
        lap_duration=90.5,
        duration_sector_1=30.1,
        duration_sector_2=30.2,
        duration_sector_3=30.2,
        st_speed=310,
    ),
    Lap(
        driver_number=1,
        lap_number=2,
        lap_duration=89.8,
        duration_sector_1=29.9,
        duration_sector_2=29.9,
        duration_sector_3=30.0,
        st_speed=315,
    ),
    Lap(
        driver_number=44,
        lap_number=1,
        lap_duration=91.2,
        duration_sector_1=30.5,
        duration_sector_2=30.4,
        duration_sector_3=30.3,
        st_speed=305,
    ),
    Lap(driver_number=44, lap_number=2, lap_duration=None),
    Lap(driver_number=16, lap_number=1, lap_duration=88.0),
]

CAR_DATA = [
    CarData(driver_number=1, date="2024-01-01T00:00:00Z", speed=300, rpm=11000, n_gear=8),
    CarData(driver_number=44, date="2024-01-01T00:00:01Z", speed=280, rpm=10500, n_gear=7),
]


def test_compare_lap_times_filters_by_driver_and_drops_none_duration():
    result = compare_lap_times(LAPS, driver_numbers=[1, 44])

    assert list(result["driver_number"]) == [1, 1, 44]
    assert 16 not in result["driver_number"].tolist()


def test_compare_lap_times_returns_empty_dataframe_with_columns_when_no_match():
    result = compare_lap_times(LAPS, driver_numbers=[999])

    assert result.empty
    assert "lap_duration" in result.columns


def test_best_lap_per_driver_picks_minimum_duration():
    result = best_lap_per_driver(LAPS, driver_numbers=[1, 44])

    row_1 = result[result["driver_number"] == 1].iloc[0]
    assert row_1["lap_duration"] == 89.8
    row_44 = result[result["driver_number"] == 44].iloc[0]
    assert row_44["lap_duration"] == 91.2


def test_best_lap_per_driver_empty_input():
    result = best_lap_per_driver(LAPS, driver_numbers=[999])

    assert result.empty


def test_compare_sectors_uses_best_lap_per_driver():
    result = compare_sectors(LAPS, driver_numbers=[1, 44])

    driver_1_sectors = result[result["driver_number"] == 1]
    assert set(driver_1_sectors["sector"]) == {"S1", "S2", "S3"}
    s1 = driver_1_sectors[driver_1_sectors["sector"] == "S1"].iloc[0]["duration"]
    assert s1 == 29.9


def test_compare_sectors_empty_input_has_expected_columns():
    result = compare_sectors(LAPS, driver_numbers=[999])

    assert result.empty
    assert list(result.columns) == ["driver_number", "sector", "duration"]


def test_speed_trap_summary_picks_max_speed_and_sorts_descending():
    result = speed_trap_summary(LAPS, driver_numbers=[1, 44])

    assert list(result["driver_number"]) == [1, 44]
    assert result.iloc[0]["top_speed"] == 315


def test_speed_trap_summary_empty_input_has_expected_columns():
    result = speed_trap_summary(LAPS, driver_numbers=[999])

    assert result.empty
    assert list(result.columns) == ["driver_number", "top_speed"]


def test_compare_telemetry_filters_by_driver():
    result = compare_telemetry(CAR_DATA, driver_numbers=[1])

    assert len(result) == 1
    assert result.iloc[0]["driver_number"] == 1
    assert result.iloc[0]["speed"] == 300


def test_compare_telemetry_empty_input_has_expected_columns():
    result = compare_telemetry([], driver_numbers=[1])

    assert result.empty
    assert list(result.columns) == [
        "driver_number",
        "date",
        "speed",
        "rpm",
        "n_gear",
        "throttle",
        "brake",
        "drs",
    ]
