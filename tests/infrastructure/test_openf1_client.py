import pytest
import requests

from f1.infrastructure.openf1_client import OpenF1Client, OpenF1ClientError

BASE_URL = "https://api.openf1.org/v1/"


def test_get_returns_json_list(requests_mock):
    requests_mock.get(f"{BASE_URL}sessions", json=[{"session_key": 9158, "session_name": "Race"}])

    client = OpenF1Client()
    result = client.get("sessions", session_key="latest")

    assert result == [{"session_key": 9158, "session_name": "Race"}]


def test_get_sends_query_params(requests_mock):
    requests_mock.get(f"{BASE_URL}laps", json=[])

    client = OpenF1Client()
    client.get("laps", session_key=9158, driver_number=44)

    assert requests_mock.last_request.qs == {"session_key": ["9158"], "driver_number": ["44"]}


def test_get_omits_none_params(requests_mock):
    requests_mock.get(f"{BASE_URL}drivers", json=[])

    client = OpenF1Client()
    client.get("drivers", session_key=9158, driver_number=None)

    assert requests_mock.last_request.qs == {"session_key": ["9158"]}


def test_get_caches_repeated_calls(requests_mock):
    requests_mock.get(f"{BASE_URL}weather", json=[{"air_temperature": 25}])

    client = OpenF1Client()
    client.get("weather", session_key=9158)
    client.get("weather", session_key=9158)

    assert requests_mock.call_count == 1


def test_clear_cache_forces_new_request(requests_mock):
    requests_mock.get(f"{BASE_URL}weather", json=[{"air_temperature": 25}])

    client = OpenF1Client()
    client.get("weather", session_key=9158)
    client.clear_cache()
    client.get("weather", session_key=9158)

    assert requests_mock.call_count == 2


def test_get_raises_openf1_client_error_on_http_failure(requests_mock):
    requests_mock.get(f"{BASE_URL}sessions", status_code=500)

    client = OpenF1Client()
    with pytest.raises(OpenF1ClientError):
        client.get("sessions", session_key="latest")


def test_get_raises_openf1_client_error_on_connection_error(requests_mock):
    requests_mock.get(f"{BASE_URL}sessions", exc=requests.ConnectionError)

    client = OpenF1Client()
    with pytest.raises(OpenF1ClientError):
        client.get("sessions", session_key="latest")


def test_get_handles_empty_response(requests_mock):
    requests_mock.get(f"{BASE_URL}pit", json=[])

    client = OpenF1Client()
    result = client.get("pit", session_key=9158)

    assert result == []


@pytest.mark.parametrize(
    "method_name,endpoint",
    [
        ("get_meetings", "meetings"),
        ("get_sessions", "sessions"),
        ("get_drivers", "drivers"),
        ("get_laps", "laps"),
        ("get_car_data", "car_data"),
        ("get_location", "location"),
        ("get_intervals", "intervals"),
        ("get_stints", "stints"),
        ("get_pit", "pit"),
        ("get_race_control", "race_control"),
        ("get_weather", "weather"),
    ],
)
def test_typed_wrappers_call_expected_endpoint(requests_mock, method_name, endpoint):
    requests_mock.get(f"{BASE_URL}{endpoint}", json=[{"ok": True}])

    client = OpenF1Client()
    result = getattr(client, method_name)(session_key=9158)

    assert result == [{"ok": True}]
    assert requests_mock.last_request.path == f"/v1/{endpoint}"
