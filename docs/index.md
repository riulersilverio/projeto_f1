# F1 Dashboard

Pipeline + dashboard interativo, construído com **Streamlit**, que consome a [API OpenF1](https://api.openf1.org) pública, processa os dados com **pandas** e apresenta análises de Fórmula 1 em três frentes:

1. **[Comparação de pilotos](paginas/comparacao_pilotos.md)** — tempos de volta, setores e telemetria.
2. **[Estratégia de pneus / pit stops](paginas/estrategia_pneus.md)** — stints, compostos e paradas nos boxes.
3. **[Ritmo de corrida / posições](paginas/ritmo_corrida.md)** — intervals, bandeiras/Safety Car e clima.

## Como rodar

```bash
poetry install
poetry run streamlit run src/f1/interface/app.py
```

Abra o navegador em `http://localhost:8501`, selecione o ano, o Grande Prêmio e a sessão na barra lateral e navegue pelas páginas de análise.

## Desenvolvimento

```bash
# Lint e formatação
poetry run task lint

# Testes com cobertura
poetry run task test

# Servidor local de documentação
poetry run task docs

# Rodar o dashboard
poetry run task app
```

Veja a organização do código em [Arquitetura](arquitetura.md), os endpoints consumidos em [API OpenF1](api_openf1.md) e as entidades tipadas em [Modelos de Domínio](modelos.md).
