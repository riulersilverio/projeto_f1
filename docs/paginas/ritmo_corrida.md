# Ritmo de Corrida

Página `interface/pages/3_Ritmo_Corrida.py`.

Acompanha a evolução da corrida ao longo do tempo:

- **Evolução do gap ao líder**: gráfico de linha com `gap_to_leader` por piloto ao longo da sessão, via `f1.domain.services.race_pace.build_gap_evolution`. Disponível apenas em sessões de corrida/sprint (a API não fornece `intervals` para treinos e qualificação).
- **Eventos de pista**: tabela com bandeiras e ocorrências de Safety Car/Virtual Safety Car, via `build_race_events`.
- **Clima**: gráficos de temperatura do ar/pista e chuva ao longo da sessão, via `build_weather_timeline`.

## Exemplo de uso da regra de domínio

```python
from f1.domain.models import RaceControlMessage
from f1.domain.services.race_pace import build_race_events

mensagens = [
    RaceControlMessage(category="SafetyCar", message="SAFETY CAR DEPLOYED", lap_number=12),
    RaceControlMessage(category="Flag", flag="YELLOW", lap_number=13),
]

eventos = build_race_events(mensagens)
```

## Dados utilizados

| Endpoint OpenF1 | Uso |
| --- | --- |
| `drivers` | rótulo dos pilotos nos gráficos |
| `intervals` | intervalo/gap ao carro da frente e ao líder |
| `race_control` | bandeiras, Safety Car e demais mensagens oficiais |
| `weather` | temperatura, umidade, vento e chuva |

!!! note
    Caso a API não retorne dados para um endpoint nesta sessão (ex: `intervals` em uma sessão de treino), a página exibe um aviso informativo em vez de falhar.
