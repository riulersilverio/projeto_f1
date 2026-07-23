# Plano de Criação — Projeto F1 (Dashboard de Análise de Dados)

Este plano define os passos para construir o projeto do zero até um MVP funcional, em conformidade com os padrões definidos em [.claude/skill.md](.claude/skill.md) e consumindo a [API OpenF1](.claude/doc_api.md).

## Objetivo

Pipeline + dashboard interativo (**Streamlit**) que consome a API OpenF1, processa os dados (pandas) e apresenta análises de Fórmula 1 em 3 frentes (MVP):

1. **Comparação de pilotos** — tempos de volta, setores e telemetria.
2. **Estratégia de pneus / pit stops** — stints, compostos e paradas nos boxes.
3. **Ritmo de corrida / posições** — intervals, bandeiras/SC (`race_control`) e clima (`weather`).

---

## Fase 0 — Setup do Ambiente

- [ ] Confirmar versão do Python no `pyproject.toml` (atualmente `>=3.12`) e alinhar com `poetry env use`.
- [ ] Adicionar dependências de runtime via Poetry (nunca `pip install`):
  ```bash
  poetry add requests pandas streamlit plotly pydantic
  ```
- [ ] Adicionar dependências de dev:
  ```bash
  poetry add --group dev pytest pytest-cov ruff mkdocs-material requests-mock
  ```
- [ ] Preencher `README.md` (atualmente corrompido/vazio) com descrição do projeto, como rodar (`poetry install`, `poetry run streamlit run src/f1/interface/app.py`) e link para `docs/`.
- [ ] Criar `.gitignore` (venv, `__pycache__`, `.pytest_cache`, `htmlcov/`, `site/`).

## Fase 1 — Estrutura de Diretórios

Seguindo a estrutura fixa do `skill.md`, com separação **Domínio / Infraestrutura / Interface** dentro de `src/f1`:

```text
src/f1/
├── __init__.py
├── infrastructure/
│   ├── __init__.py
│   └── openf1_client.py      # cliente HTTP para api.openf1.org
├── domain/
│   ├── __init__.py
│   ├── models.py              # entidades: Session, Driver, Lap, Stint, PitStop, Interval, Weather, RaceControlMessage
│   └── services/
│       ├── __init__.py
│       ├── driver_comparison.py
│       ├── tyre_strategy.py
│       └── race_pace.py
└── interface/
    ├── __init__.py
    ├── app.py                 # Home do Streamlit (seleção de meeting/session)
    └── pages/
        ├── 1_Comparacao_Pilotos.py
        ├── 2_Estrategia_Pneus.py
        └── 3_Ritmo_Corrida.py

tests/
├── infrastructure/test_openf1_client.py
├── domain/
│   ├── test_driver_comparison.py
│   ├── test_tyre_strategy.py
│   └── test_race_pace.py

docs/
├── index.md
├── arquitetura.md
└── paginas/
    ├── comparacao_pilotos.md
    ├── estrategia_pneus.md
    └── ritmo_corrida.md

mkdocs.yml
```

## Fase 2 — Camada de Infraestrutura (`infrastructure/openf1_client.py`)

- [ ] Cliente único responsável por toda comunicação com `https://api.openf1.org/v1/` (base URL configurável).
- [ ] Função genérica `get(endpoint: str, **params) -> list[dict]` que monta query string (ex: `session_key`, `driver_number`) e trata erros de rede/HTTP.
- [ ] Wrappers tipados por recurso, cobrindo os endpoints citados no `doc_api.md`: `get_meetings`, `get_sessions`, `get_drivers`, `get_laps`, `get_car_data`, `get_location`, `get_intervals`, `get_stints`, `get_pit`, `get_race_control`, `get_weather`.
- [ ] Cache simples em memória (ex: `functools.lru_cache` ou dict com TTL) para evitar chamadas repetidas ao mesmo `session_key` — conforme nota de performance do `doc_api.md`.
- [ ] Sem lógica de negócio nesta camada — apenas acesso a dados.

## Fase 3 — Camada de Domínio (`domain/`)

- [ ] `models.py`: entidades tipadas (dataclasses ou Pydantic) que representam a resposta JSON de cada endpoint relevante, com *type hints* completos.
- [ ] `services/driver_comparison.py`: dado um `session_key` e uma lista de `driver_number`, retorna comparação de tempos de volta/setores (`laps`) e telemetria (`car_data`) — regras puras, sem I/O direto (recebe dados já buscados pela infra).
- [ ] `services/tyre_strategy.py`: a partir de `stints` e `pit`, monta a linha do tempo de composto de pneus e duração das paradas por piloto.
- [ ] `services/race_pace.py`: a partir de `intervals`, `race_control` e `weather`, calcula evolução de posição/gap ao longo da corrida e marca eventos relevantes (SC, bandeiras, chuva).
- [ ] Funções pequenas, puras e testáveis — sem dependência do Streamlit.

## Fase 4 — Camada de Interface (`interface/`, Streamlit)

- [ ] `app.py`: tela inicial para escolher `meeting` → `session` (usando `get_meetings`/`get_sessions`, com `session_key=latest` como padrão).
- [ ] Página **Comparação de Pilotos**: seleção de pilotos (`get_drivers`), gráficos de tempo de volta/setor e telemetria (Plotly).
- [ ] Página **Estratégia de Pneus**: gráfico de stints por composto + tabela de pit stops.
- [ ] Página **Ritmo de Corrida**: gráfico de posição/gap ao longo da corrida com marcações de `race_control` e clima.
- [ ] Interface consome apenas os `services` do domínio — nunca chama `infrastructure` diretamente.

## Fase 5 — Testes (Pytest)

- [ ] Testes unitários dos `services` de domínio com dados mockados (sem rede).
- [ ] Testes do `openf1_client` usando `requests-mock` para simular respostas da API (sucesso, erro HTTP, resposta vazia).
- [ ] Rodar com cobertura e garantir mínimo de 50%:
  ```bash
  poetry run pytest --cov=src/f1 --cov-report=term-missing
  ```

## Fase 6 — Documentação (MkDocs Material)

- [ ] `mkdocs.yml` configurado com tema `material`.
- [ ] `docs/index.md`: visão geral do projeto e como rodar.
- [ ] `docs/arquitetura.md`: explicação da separação Domínio/Infraestrutura/Interface.
- [ ] Uma página por funcionalidade do dashboard (`docs/paginas/*.md`) com exemplos de uso.
- [ ] Validar build sem erros:
  ```bash
  poetry run mkdocs build
  ```

## Fase 7 — Checklist de Entrega (obrigatório antes de qualquer PR)

Conforme seção 7 e 8 do `skill.md`:

1. [ ] `poetry run ruff check . --fix && poetry run ruff format .`
2. [ ] `poetry run pytest --cov=src/f1 --cov-report=term-missing` (cobertura ≥ 50%)
3. [ ] `poetry run mkdocs build` (sem avisos)
4. [ ] `pyproject.toml` / `poetry.lock` atualizados, sem dependências instaladas manualmente fora do Poetry.

## Ordem de Execução Sugerida

`Fase 0` → `Fase 1` → `Fase 2` (infra) → `Fase 3` (domínio, com testes já junto) → `Fase 5` (testes de infra) → `Fase 4` (interface Streamlit) → `Fase 6` (docs) → `Fase 7` (checklist final).
