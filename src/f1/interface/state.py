"""Utilitários compartilhados pelas páginas Streamlit: cliente cacheado e buscas.

Centraliza o acesso à camada de infraestrutura para que as páginas não
precisem instanciar o cliente HTTP nem repetir chamadas de rede a cada
interação do usuário (via `st.cache_data`/`st.cache_resource`).
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from f1.infrastructure.openf1_client import OpenF1Client, OpenF1ClientError

CACHE_TTL_SECONDS = 300


@st.cache_resource
def get_client() -> OpenF1Client:
    """Retorna uma instância única e cacheada do cliente OpenF1."""
    return OpenF1Client()


def _safe_get(endpoint: str, **params: Any) -> list[dict]:
    """Busca um endpoint tratando falhas da API de forma amigável.

    A API OpenF1 pode retornar erro (ex: HTTP 404 quando não há dados
    para o filtro, ou HTTP 422 quando a consulta é grande demais). Nesses
    casos exibimos um aviso e devolvemos lista vazia em vez de quebrar a
    página inteira.
    """
    try:
        return get_client().get(endpoint, **params)
    except OpenF1ClientError as exc:
        st.warning(f"Não foi possível obter dados de '{endpoint}': {exc}")
        return []


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_meetings(year: int) -> list[dict]:
    """Busca os meetings (fins de semana de corrida) de um ano."""
    return _safe_get("meetings", year=year)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_sessions(meeting_key: int) -> list[dict]:
    """Busca as sessões de um meeting."""
    return _safe_get("sessions", meeting_key=meeting_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_drivers(session_key: int) -> list[dict]:
    """Busca os pilotos participantes de uma sessão."""
    return _safe_get("drivers", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_laps(session_key: int) -> list[dict]:
    """Busca as voltas de uma sessão."""
    return _safe_get("laps", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_car_data(session_key: int, driver_number: int) -> list[dict]:
    """Busca a telemetria de um piloto em uma sessão."""
    return _safe_get("car_data", session_key=session_key, driver_number=driver_number)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_stints(session_key: int) -> list[dict]:
    """Busca os stints (jogos de pneus) de uma sessão."""
    return _safe_get("stints", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_pit(session_key: int) -> list[dict]:
    """Busca as paradas nos boxes de uma sessão."""
    return _safe_get("pit", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_intervals(session_key: int) -> list[dict]:
    """Busca os intervalos entre carros de uma sessão."""
    return _safe_get("intervals", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_race_control(session_key: int) -> list[dict]:
    """Busca as mensagens da direção de prova de uma sessão."""
    return _safe_get("race_control", session_key=session_key)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_weather(session_key: int) -> list[dict]:
    """Busca os dados climáticos de uma sessão."""
    return _safe_get("weather", session_key=session_key)


def require_session() -> int:
    """Garante que uma sessão foi selecionada na página inicial.

    Interrompe a renderização da página (via `st.stop()`) caso nenhuma
    sessão tenha sido selecionada ainda.

    Returns:
        O `session_key` selecionado.
    """
    session_key = st.session_state.get("session_key")
    if session_key is None:
        st.warning("Selecione um Grande Prêmio e uma sessão na página inicial primeiro.")
        st.stop()
    return session_key
