# Comparação de Pilotos

Página `interface/pages/1_Comparacao_Pilotos.py`.

Permite comparar dois ou mais pilotos da sessão selecionada:

- **Tempos de volta**: gráfico de linha com o tempo de cada volta por piloto (`lap_duration`), usando `f1.domain.services.driver_comparison.compare_lap_times`.
- **Melhor volta**: tabela com a volta mais rápida de cada piloto, via `best_lap_per_driver`.
- **Telemetria**: para até 2 pilotos, gráfico de velocidade ao longo do tempo (`speed` de `car_data`), via `compare_telemetry`.

## Exemplo de uso da regra de domínio

```python
from f1.domain.models import Lap
from f1.domain.services.driver_comparison import best_lap_per_driver

laps = [
    Lap(driver_number=1, lap_number=1, lap_duration=90.5),
    Lap(driver_number=1, lap_number=2, lap_duration=89.8),
    Lap(driver_number=44, lap_number=1, lap_duration=91.2),
]

melhores_voltas = best_lap_per_driver(laps, driver_numbers=[1, 44])
```

## Dados utilizados

| Endpoint OpenF1 | Uso |
| --- | --- |
| `drivers` | lista de pilotos disponíveis para seleção |
| `laps` | tempos de volta e setores |
| `car_data` | telemetria (velocidade, RPM, marcha, DRS) |
