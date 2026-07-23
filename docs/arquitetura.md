# Arquitetura

O código em `src/f1` segue separação em três camadas, conforme o padrão definido em `.claude/skill.md`:

```text
src/f1/
├── infrastructure/
│   └── openf1_client.py   # cliente HTTP para api.openf1.org
├── domain/
│   ├── models.py           # entidades tipadas (Pydantic)
│   └── services/           # regras de negócio, puras e testáveis
│       ├── driver_comparison.py
│       ├── tyre_strategy.py
│       └── race_pace.py
└── interface/
    ├── app.py               # Home do Streamlit
    ├── state.py              # cache de cliente e buscas na API
    └── pages/                 # páginas de análise
```

## Infraestrutura

`OpenF1Client` (`infrastructure/openf1_client.py`) é o único ponto de acesso à API OpenF1. Expõe:

- `get(endpoint, **params)`: método genérico que monta a query string e trata erros de rede/HTTP, levantando `OpenF1ClientError` em caso de falha.
- Wrappers tipados por recurso: `get_meetings`, `get_sessions`, `get_drivers`, `get_laps`, `get_car_data`, `get_location`, `get_intervals`, `get_stints`, `get_pit`, `get_race_control`, `get_weather`.
- Cache em memória por `(endpoint, parâmetros)`, evitando chamadas repetidas para a mesma consulta.

Esta camada não contém nenhuma regra de negócio — apenas acesso a dados.

## Domínio

`domain/models.py` define entidades Pydantic que representam a resposta de cada endpoint (`Meeting`, `Session`, `Driver`, `Lap`, `CarData`, `Stint`, `PitStop`, `Interval`, `Weather`, `RaceControlMessage`), todas tolerantes a campos extras retornados pela API.

`domain/services/` contém funções puras — sem I/O — que recebem listas de entidades já buscadas pela infraestrutura e devolvem `pandas.DataFrame` prontos para exibição:

- **`driver_comparison.py`**: tempos de volta/setor e telemetria comparada entre pilotos.
- **`tyre_strategy.py`**: linha do tempo de stints e resumo de pit stops.
- **`race_pace.py`**: evolução de gap ao líder, eventos de pista (bandeiras/Safety Car) e clima.

Por serem puras, essas funções são testadas com dados mockados, sem qualquer chamada de rede.

## Interface

A aplicação Streamlit (`interface/`) é responsável apenas por:

1. Orquestrar buscas na API via `interface/state.py` (que encapsula o `OpenF1Client` com cache do Streamlit e tratamento de erros de API).
2. Transformar os dados usando os `services` do domínio.
3. Renderizar os resultados com Plotly e componentes nativos do Streamlit.

`app.py` é a página inicial, onde o usuário seleciona ano, Grande Prêmio e sessão — o `session_key` escolhido fica em `st.session_state` e é reutilizado pelas páginas em `interface/pages/`. Cada página chama `state.require_session()` antes de buscar dados, interrompendo a renderização (via `st.stop()`) com um aviso caso nenhuma sessão tenha sido selecionada ainda.

### Tratamento de erros

`interface/state.py` centraliza toda busca à API por trás de funções `fetch_*` decoradas com `st.cache_data(ttl=300)`, uma por endpoint. Internamente elas chamam `_safe_get`, que captura `OpenF1ClientError` (levantado pelo cliente em falhas de rede ou HTTP) e devolve lista vazia após exibir `st.warning`, em vez de deixar a exceção quebrar a página inteira. `get_client()` mantém uma única instância do `OpenF1Client` via `st.cache_resource`, compartilhada entre todas as páginas.

Veja os endpoints e o formato de cada resposta em [API OpenF1](api_openf1.md) e os modelos tipados correspondentes em [Modelos de Domínio](modelos.md).
