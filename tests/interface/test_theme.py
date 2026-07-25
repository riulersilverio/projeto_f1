from f1.domain.models import Driver
from f1.interface.theme import (
    FALLBACK_DRIVER_COLOR,
    _avatar_html,
    _driver_card_html,
    _roster_html,
    driver_color_map,
)

TEAMMATES = [
    Driver(driver_number=1, team_colour="F47600"),
    Driver(driver_number=4, team_colour="F47600"),
]

NORRIS = Driver(
    driver_number=4,
    name_acronym="NOR",
    full_name="Lando Norris",
    team_name="McLaren",
    team_colour="F47600",
    headshot_url="https://example.com/norris.png",
)

NO_PHOTO_DRIVER = Driver(driver_number=99, name_acronym="XXX", team_colour="808080")


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


def test_avatar_html_uses_photo_when_available():
    result = _avatar_html(NORRIS, NORRIS.driver_number, "#F47600")

    assert "<img" in result
    assert "https://example.com/norris.png" in result


def test_avatar_html_falls_back_to_acronym_without_photo():
    result = _avatar_html(NO_PHOTO_DRIVER, NO_PHOTO_DRIVER.driver_number, "#808080")

    assert "<img" not in result
    assert "XXX" in result


def test_avatar_html_falls_back_to_driver_number_without_driver():
    result = _avatar_html(None, 55, "#808080")

    assert "<img" not in result
    assert "55" in result


def test_driver_card_html_includes_name_team_and_extra():
    result = _driver_card_html(NORRIS, NORRIS.driver_number, "#F47600", extra="🥇 P1")

    assert "Lando Norris" in result
    assert "McLaren" in result
    assert "🥇 P1" in result


def test_driver_card_html_escapes_unsafe_characters():
    unsafe_driver = Driver(driver_number=7, full_name="<script>alert(1)</script>")

    result = _driver_card_html(unsafe_driver, 7, "#808080")

    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_roster_html_renders_one_chip_per_driver():
    result = _roster_html([NORRIS, NO_PHOTO_DRIVER], {NORRIS.driver_number: "#F47600"})

    assert result.count('class="f1-roster-chip"') == 2
    assert "NOR" in result
    assert "XXX" in result
