from f1.domain.models import Driver
from f1.interface.theme import FALLBACK_DRIVER_COLOR, driver_color_map

TEAMMATES = [
    Driver(driver_number=1, team_colour="F47600"),
    Driver(driver_number=4, team_colour="F47600"),
]


def test_driver_color_map_uses_team_colour():
    result = driver_color_map(TEAMMATES)

    assert result[1] == "#F47600"


def test_driver_color_map_lightens_teammate_to_stay_distinguishable():
    result = driver_color_map(TEAMMATES)

    assert result[4] != result[1]
    assert result[4].startswith("#")


def test_driver_color_map_falls_back_when_team_colour_missing():
    result = driver_color_map([Driver(driver_number=99, team_colour=None)])

    assert result[99] == FALLBACK_DRIVER_COLOR
