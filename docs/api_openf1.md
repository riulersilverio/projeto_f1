# API OpenF1

O projeto consome exclusivamente a [API OpenF1](https://api.openf1.org) pública através de `f1.infrastructure.openf1_client.OpenF1Client`.

- **Base URL:** `https://api.openf1.org/v1/`
- **Formato:** JSON
- **Autenticação:** nenhuma (acesso público)
- **Dados históricos:** disponíveis a partir da temporada de 2023

## Endpoints utilizados

| Endpoint | Método no cliente | Modelo de domínio | Usado em |
| --- | --- | --- | --- |
| `meetings` | `get_meetings` | `Meeting` | Seleção de Grande Prêmio (`app.py`) |
| `sessions` | `get_sessions` | `Session` | Seleção de sessão (`app.py`) |
| `drivers` | `get_drivers` | `Driver` | Todas as páginas de análise |
| `laps` | `get_laps` | `Lap` | [Comparação de Pilotos](paginas/comparacao_pilotos.md) |
| `car_data` | `get_car_data` | `CarData` | [Comparação de Pilotos](paginas/comparacao_pilotos.md) |
| `stints` | `get_stints` | `Stint` | [Estratégia de Pneus](paginas/estrategia_pneus.md) |
| `pit` | `get_pit` | `PitStop` | [Estratégia de Pneus](paginas/estrategia_pneus.md) |
| `intervals` | `get_intervals` | `Interval` | [Ritmo de Corrida](paginas/ritmo_corrida.md) |
| `race_control` | `get_race_control` | `RaceControlMessage` | [Ritmo de Corrida](paginas/ritmo_corrida.md) |
| `weather` | `get_weather` | `Weather` | [Ritmo de Corrida](paginas/ritmo_corrida.md) |

O endpoint `location` (coordenadas X/Y/Z na pista) tem wrapper pronto no cliente (`get_location`), mas ainda não é consumido por nenhuma página.

## Filtros e performance

A API aceita filtros via query string em quase todos os campos (ex: `?driver_number=44`, `?session_key=9158`). O cliente sempre filtra por `session_key` ao buscar dados de uma sessão, conforme recomendação de performance da própria API — evita respostas grandes e lentas.

## Cache

`OpenF1Client` mantém um cache em memória por `(endpoint, parâmetros)`, então repetir a mesma consulta na mesma execução do processo não gera uma nova requisição HTTP. Esse cache é interno ao cliente; a camada de interface adiciona um segundo nível de cache com `st.cache_data` (ver [Tratamento de erros](arquitetura.md#tratamento-de-erros) em Arquitetura).

## Erros

Qualquer falha de rede ou resposta HTTP de erro é convertida em `OpenF1ClientError` por `OpenF1Client.get`. O cliente não trata esse erro — quem trata é a camada de interface (`interface/state.py`), exibindo um aviso ao usuário em vez de quebrar a página.
