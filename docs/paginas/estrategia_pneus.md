# Estratégia de Pneus

Página `interface/pages/2_Estrategia_Pneus.py`.

Mostra a estratégia de pneus utilizada na sessão selecionada:

- **Linha do tempo de compostos**: gráfico de barras horizontais com a duração (em voltas) de cada stint por piloto, colorido por composto (`compound`), via `f1.domain.services.tyre_strategy.build_stint_timeline`.
- **Paradas nos boxes**: tabela com volta, duração e horário de cada pit stop, via `build_pit_stop_summary`.

## Exemplo de uso da regra de domínio

```python
from f1.domain.models import Stint
from f1.domain.services.tyre_strategy import build_stint_timeline

stints = [
    Stint(driver_number=1, stint_number=1, compound="SOFT", lap_start=1, lap_end=15),
    Stint(driver_number=1, stint_number=2, compound="HARD", lap_start=16, lap_end=40),
]

linha_do_tempo = build_stint_timeline(stints)
```

## Dados utilizados

| Endpoint OpenF1 | Uso |
| --- | --- |
| `drivers` | rótulo dos pilotos nos gráficos e tabelas |
| `stints` | composto, volta inicial/final de cada jogo de pneus |
| `pit` | volta, duração e horário das paradas nos boxes |
