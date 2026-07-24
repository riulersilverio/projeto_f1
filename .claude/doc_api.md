# Documentação da API OpenF1

A OpenF1 é uma API gratuita e de código aberto que fornece dados em tempo real e históricos sobre a Fórmula 1. Os dados são extraídos diretamente do cronometragem oficial da F1.

## 📌 Informações Gerais
- **Base URL:** `https://api.openf1.org/v1/`
- **Formato de Resposta:** JSON
- **Autenticação:** Não é necessária (Acesso Público).

---

## 🛠 Principais Endpoints

Os endpoints permitem consultar dados específicos utilizando filtros na URL (ex: `?session_key=9158`).

### 1. Sessões e Eventos
- **`meetings`**: Informações sobre o fim de semana de corrida (nome do GP, localização, país, ano).
- **`sessions`**: Detalhes de sessões específicas (Treino Livre, Qualificação, Corrida). Contém o `session_key`, essencial para filtrar outros dados.

### 2. Dados dos Pilotos
- **`drivers`**: Lista de pilotos em uma sessão. Inclui número, nome abreviado, nome completo, cor da equipe e link para a foto do piloto.

### 3. Telemetria e Posição
- **`car_data`**: Telemetria em tempo real (velocidade, RPM, marcha, acelerador, freio, DRS).
- **`location`**: Coordenadas X, Y, Z dos carros no circuito, permitindo mapear a posição exata na pista.

### 4. Tempos e Performance
- **`laps`**: Detalhes de cada volta (tempo da volta, tempos de setores S1, S2, S3, se a volta foi a melhor pessoal).
- **`intervals`**: Intervalos de tempo entre os carros na pista.

### 5. Estratégia e Pista
- **`stints`**: Informações sobre os jogos de pneus usados (composto, durabilidade, volta inicial/final).
- **`pit`**: Dados de paradas nos boxes (entrada, saída e duração).
- **`race_control`**: Mensagens oficiais da direção de prova (bandeiras amarelas/vermelhas, Safety Car, investigações, DRS ativado/desativado).

### 6. Condições Ambientais
- **`weather`**: Dados climáticos (temperatura do ar e da pista, umidade, pressão, velocidade do vento e ocorrência de chuva).

---

## 🔍 Filtragem de Dados

A API suporta filtros via *query strings* para quase todos os campos. Exemplos comuns:

*   **Por Piloto:** `?driver_number=44`
*   **Por Sessão:** `?session_key=latest` (ou o ID numérico)
*   **Por Composto de Pneu:** `?compound=SOFT`
*   **Combinado:** `?session_key=9158&driver_number=1&speed=>300`

> **Nota de Performance:** Sempre que possível, utilize o `session_key` para limitar a quantidade de dados retornados e evitar lentidão.

---

## 🚀 Exemplo de Uso (Python)

```python
import requests

# Buscar dados da última sessão disponível
response = requests.get('https://api.openf1.org/v1/sessions?session_key=latest')
session_data = response.json()

print(f"Sessão: {session_data[0]['session_name']} em {session_data[0]['location']}")
```

---

## 📖 Notas Adicionais
- **Dados Históricos:** A API contém dados desde a temporada de 2023.
- **Latência:** Em dias de corrida, os dados são atualizados quase instantaneamente (tempo real).
- **Rate Limit:** Embora gratuita, recomenda-se não sobrecarregar o servidor com requisições desnecessárias.
