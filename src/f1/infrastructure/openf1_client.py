"""Cliente HTTP para a API OpenF1 (https://api.openf1.org/v1/).

Esta camada é responsável exclusivamente pelo acesso a dados externos.
Nenhuma regra de negócio deve residir aqui.
"""

from __future__ import annotations

from typing import Any

import requests

DEFAULT_BASE_URL = "https://api.openf1.org/v1/"
DEFAULT_TIMEOUT_SECONDS = 10


class OpenF1ClientError(Exception):
    """Erro genérico de comunicação com a API OpenF1."""


class OpenF1Client:
    """Cliente para consumo dos endpoints da API OpenF1.

    Mantém um cache em memória por (endpoint, parâmetros) para evitar
    chamadas repetidas à mesma consulta, conforme recomendação de
    performance da API (preferir sempre filtrar por ``session_key``).
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        session: requests.Session | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/") + "/"
        self._timeout = timeout
        self._session = session or requests.Session()
        self._cache: dict[tuple[str, tuple[tuple[str, Any], ...]], list[dict[str, Any]]] = {}

    def clear_cache(self) -> None:
        """Limpa o cache em memória de respostas já buscadas."""
        self._cache.clear()

    def get(self, endpoint: str, **params: Any) -> list[dict[str, Any]]:
        """Busca dados de um endpoint da API, aplicando filtros via query string.

        Args:
            endpoint: nome do recurso (ex: "sessions", "laps").
            **params: filtros aceitos pela API (ex: session_key=9158).

        Returns:
            Lista de registros (dicts) retornados pela API.

        Raises:
            OpenF1ClientError: em caso de falha de rede ou resposta HTTP de erro.
        """
        clean_params = {key: value for key, value in params.items() if value is not None}
        cache_key = (endpoint, tuple(sorted(clean_params.items())))
        if cache_key in self._cache:
            return self._cache[cache_key]

        url = f"{self._base_url}{endpoint.lstrip('/')}"
        try:
            response = self._session.get(url, params=clean_params, timeout=self._timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise OpenF1ClientError(f"Falha ao consultar {url}: {exc}") from exc

        data = response.json()
        self._cache[cache_key] = data
        return data

    def get_meetings(self, **params: Any) -> list[dict[str, Any]]:
        """Busca informações sobre fins de semana de corrida (meetings)."""
        return self.get("meetings", **params)

    def get_sessions(self, **params: Any) -> list[dict[str, Any]]:
        """Busca sessões (treino, classificação, corrida)."""
        return self.get("sessions", **params)

    def get_drivers(self, **params: Any) -> list[dict[str, Any]]:
        """Busca pilotos participantes de uma sessão."""
        return self.get("drivers", **params)

    def get_laps(self, **params: Any) -> list[dict[str, Any]]:
        """Busca voltas (tempo total e por setor)."""
        return self.get("laps", **params)

    def get_car_data(self, **params: Any) -> list[dict[str, Any]]:
        """Busca telemetria do carro (velocidade, RPM, marcha, DRS etc.)."""
        return self.get("car_data", **params)

    def get_location(self, **params: Any) -> list[dict[str, Any]]:
        """Busca coordenadas de posição dos carros na pista."""
        return self.get("location", **params)

    def get_intervals(self, **params: Any) -> list[dict[str, Any]]:
        """Busca intervalos de tempo entre os carros."""
        return self.get("intervals", **params)

    def get_stints(self, **params: Any) -> list[dict[str, Any]]:
        """Busca stints (jogos de pneus usados durante a sessão)."""
        return self.get("stints", **params)

    def get_pit(self, **params: Any) -> list[dict[str, Any]]:
        """Busca dados de paradas nos boxes (pit stops)."""
        return self.get("pit", **params)

    def get_race_control(self, **params: Any) -> list[dict[str, Any]]:
        """Busca mensagens oficiais da direção de prova."""
        return self.get("race_control", **params)

    def get_weather(self, **params: Any) -> list[dict[str, Any]]:
        """Busca dados climáticos da sessão."""
        return self.get("weather", **params)
