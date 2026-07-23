# Modelos de Domínio

Definidos em `f1.domain.models`, todos herdam de `OpenF1Model` (`pydantic.BaseModel` com `extra="ignore"`) — campos desconhecidos retornados pela API são descartados em vez de causar erro de validação, já que a API pode evoluir seu schema sem aviso prévio.

Apenas os campos usados pelo projeto são declarados; a resposta real da API costuma trazer mais campos.

| Modelo | Campo obrigatório | Representa |
| --- | --- | --- |
| `Meeting` | `meeting_key`, `meeting_name` | Um fim de semana de corrida (Grande Prêmio) |
| `Session` | `session_key`, `session_name` | Uma sessão específica (treino, classificação, corrida) |
| `Driver` | `driver_number` | Um piloto participante de uma sessão |
| `Lap` | `driver_number` | Uma volta completada, com tempos totais e por setor |
| `CarData` | `driver_number` | Um ponto de telemetria do carro (velocidade, RPM, marcha, DRS...) |
| `Stint` | `driver_number` | Um jogo de pneus (composto, volta inicial/final) |
| `PitStop` | `driver_number` | Uma parada nos boxes (volta, duração) |
| `Interval` | `driver_number` | Gap ao líder e intervalo ao carro da frente |
| `Weather` | — | Condições climáticas registradas na sessão |
| `RaceControlMessage` | — | Mensagem oficial da direção de prova (bandeira, Safety Car etc.) |

Todos os campos além do obrigatório são opcionais (`| None = None`), pois a API pode omitir valores conforme o tipo de sessão — por exemplo, `intervals` não é populado em treinos e qualificação, apenas em corrida/sprint.

## Por que Pydantic

- Validação e conversão de tipo na borda (ex: `date_start: datetime`), evitando que dado malformado da API se propague para os `services` de domínio.
- Modelos servem de contrato explícito entre `infrastructure` (que devolve `list[dict]`) e `domain/services` (que recebem `list[Lap]`, `list[Stint]` etc.) — a conversão dict → modelo acontece nas páginas de interface antes de chamar os services.
