from f1.domain.models import PitStop, Stint
from f1.domain.services.tyre_strategy import build_pit_stop_summary, build_stint_timeline

STINTS = [
    Stint(driver_number=1, stint_number=1, compound="SOFT", lap_start=1, lap_end=15),
    Stint(driver_number=1, stint_number=2, compound="HARD", lap_start=16, lap_end=40),
    Stint(driver_number=44, stint_number=1, compound="MEDIUM", lap_start=1, lap_end=20),
]

PIT_STOPS = [
    PitStop(driver_number=1, lap_number=15, pit_duration=2.3),
    PitStop(driver_number=44, lap_number=20, pit_duration=2.8),
]


def test_build_stint_timeline_computes_lap_count():
    result = build_stint_timeline(STINTS, driver_numbers=[1])

    assert len(result) == 2
    first = result.iloc[0]
    assert first["compound"] == "SOFT"
    assert first["lap_count"] == 15


def test_build_stint_timeline_without_driver_filter_returns_all():
    result = build_stint_timeline(STINTS)

    assert len(result) == 3


def test_build_stint_timeline_empty_input():
    result = build_stint_timeline([])

    assert result.empty
    assert "lap_count" in result.columns


def test_build_pit_stop_summary_filters_by_driver():
    result = build_pit_stop_summary(PIT_STOPS, driver_numbers=[44])

    assert len(result) == 1
    assert result.iloc[0]["driver_number"] == 44
    assert result.iloc[0]["pit_duration"] == 2.8


def test_build_pit_stop_summary_empty_input():
    result = build_pit_stop_summary([])

    assert result.empty
    assert list(result.columns) == ["driver_number", "lap_number", "pit_duration", "date"]
