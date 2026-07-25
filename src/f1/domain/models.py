"""Entidades tipadas que representam as respostas da API OpenF1.

Todos os modelos ignoram campos desconhecidos, já que a API pode evoluir
seu schema sem aviso prévio.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OpenF1Model(BaseModel):
    """Base comum: ignora campos extras retornados pela API."""

    model_config = ConfigDict(extra="ignore")


class Meeting(OpenF1Model):
    """Um fim de semana de corrida (Grande Prêmio)."""

    meeting_key: int
    meeting_name: str
    meeting_official_name: str | None = None
    location: str | None = None
    country_name: str | None = None
    country_code: str | None = None
    circuit_short_name: str | None = None
    year: int | None = None
    date_start: datetime | None = None


class Session(OpenF1Model):
    """Uma sessão específica (treino, classificação, corrida)."""

    session_key: int
    meeting_key: int | None = None
    session_name: str
    session_type: str | None = None
    location: str | None = None
    country_name: str | None = None
    circuit_short_name: str | None = None
    year: int | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None


class Driver(OpenF1Model):
    """Um piloto participante de uma sessão."""

    driver_number: int
    session_key: int | None = None
    meeting_key: int | None = None
    broadcast_name: str | None = None
    full_name: str | None = None
    name_acronym: str | None = None
    team_name: str | None = None
    team_colour: str | None = None
    headshot_url: str | None = None
    country_code: str | None = None


class Lap(OpenF1Model):
    """Uma volta completada por um piloto, com tempos por setor."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    lap_number: int | None = None
    date_start: datetime | None = None
    lap_duration: float | None = None
    duration_sector_1: float | None = None
    duration_sector_2: float | None = None
    duration_sector_3: float | None = None
    i1_speed: float | None = None
    i2_speed: float | None = None
    st_speed: float | None = None
    is_pit_out_lap: bool | None = None


class CarData(OpenF1Model):
    """Um ponto de telemetria do carro."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    date: datetime | None = None
    speed: float | None = None
    rpm: float | None = None
    n_gear: int | None = None
    throttle: float | None = None
    brake: float | None = None
    drs: int | None = None


class Stint(OpenF1Model):
    """Um stint (jogo de pneus) utilizado por um piloto."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    stint_number: int | None = None
    compound: str | None = None
    lap_start: int | None = None
    lap_end: int | None = None
    tyre_age_at_start: int | None = None


class PitStop(OpenF1Model):
    """Uma parada nos boxes."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    lap_number: int | None = None
    pit_duration: float | None = None
    date: datetime | None = None


class Interval(OpenF1Model):
    """Diferença de tempo entre um piloto e o líder/carro à frente."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    gap_to_leader: float | str | None = None
    interval: float | str | None = None
    date: datetime | None = None


class Position(OpenF1Model):
    """A posição de um piloto em um instante da sessão."""

    session_key: int | None = None
    meeting_key: int | None = None
    driver_number: int
    date: datetime | None = None
    position: int | None = None


class Weather(OpenF1Model):
    """Condições climáticas registradas durante a sessão."""

    session_key: int | None = None
    meeting_key: int | None = None
    date: datetime | None = None
    air_temperature: float | None = None
    track_temperature: float | None = None
    humidity: float | None = None
    pressure: float | None = None
    wind_direction: float | None = None
    wind_speed: float | None = None
    rainfall: float | None = None


class RaceControlMessage(OpenF1Model):
    """Mensagem oficial da direção de prova (bandeiras, SC, investigações)."""

    session_key: int | None = None
    meeting_key: int | None = None
    date: datetime | None = None
    category: str | None = None
    flag: str | None = None
    scope: str | None = None
    sector: int | None = None
    driver_number: int | None = None
    lap_number: int | None = None
    message: str | None = None
