from f1.domain.models import Interval, Position, RaceControlMessage, Weather
from f1.domain.services.race_pace import (
    build_gap_evolution,
    build_position_evolution,
    build_race_events,
    build_weather_timeline,
    latest_classification,
)

INTERVALS = [
    Interval(driver_number=1, date="2024-01-01T00:00:00Z", gap_to_leader=0, interval=0),
    Interval(driver_number=44, date="2024-01-01T00:00:00Z", gap_to_leader=1.5, interval=1.5),
]

POSITIONS = [
    Position(driver_number=1, date="2024-01-01T00:00:00Z", position=2),
    Position(driver_number=1, date="2024-01-01T00:05:00Z", position=1),
    Position(driver_number=44, date="2024-01-01T00:00:00Z", position=1),
    Position(driver_number=44, date="2024-01-01T00:05:00Z", position=2),
]

MESSAGES = [
    RaceControlMessage(category="Flag", flag="YELLOW", date="2024-01-01T00:00:00Z", lap_number=5),
    RaceControlMessage(
        category="SafetyCar",
        date="2024-01-01T00:01:00Z",
        message="SAFETY CAR DEPLOYED",
        lap_number=6,
    ),
    RaceControlMessage(category="Other", date="2024-01-01T00:02:00Z", message="DRS enabled"),
]

WEATHER = [
    Weather(date="2024-01-01T00:00:00Z", air_temperature=24.5, track_temperature=32.0, rainfall=0),
    Weather(date="2024-01-01T00:05:00Z", air_temperature=24.8, track_temperature=33.1, rainfall=1),
]


def test_build_gap_evolution_filters_by_driver():
    result = build_gap_evolution(INTERVALS, driver_numbers=[44])

    assert len(result) == 1
    assert result.iloc[0]["driver_number"] == 44


def test_build_gap_evolution_without_filter_returns_all():
    result = build_gap_evolution(INTERVALS)

    assert len(result) == 2


def test_build_position_evolution_filters_by_driver():
    result = build_position_evolution(POSITIONS, driver_numbers=[44])

    assert len(result) == 2
    assert set(result["driver_number"]) == {44}


def test_build_position_evolution_without_filter_returns_all():
    result = build_position_evolution(POSITIONS)

    assert len(result) == 4


def test_build_position_evolution_empty_input():
    result = build_position_evolution([])

    assert result.empty
    assert "position" in result.columns


def test_latest_classification_picks_most_recent_position_per_driver():
    result = latest_classification(POSITIONS)

    assert list(result["driver_number"]) == [1, 44]
    assert list(result["position"]) == [1, 2]


def test_latest_classification_empty_input():
    result = latest_classification([])

    assert result.empty


def test_build_race_events_keeps_only_relevant_categories():
    result = build_race_events(MESSAGES)

    assert len(result) == 2
    assert set(result["category"]) == {"Flag", "SafetyCar"}


def test_build_race_events_empty_input():
    result = build_race_events([])

    assert result.empty
    assert "message" in result.columns


def test_build_weather_timeline_orders_by_date():
    result = build_weather_timeline(WEATHER)

    assert len(result) == 2
    assert result.iloc[0]["air_temperature"] == 24.5
    assert result.iloc[1]["rainfall"] == 1


def test_build_weather_timeline_empty_input():
    result = build_weather_timeline([])

    assert result.empty
