# SKILL.MD: Padrões de Desenvolvimento Python

Este documento define os padrões obrigatórios de desenvolvimento, qualidade, testes e documentação para este repositório. O cumprimento destas diretrizes é mandatório para todos os desenvolvedores e agentes de IA.

## 1. Gerenciamento de Ambiente e Dependências

O projeto utiliza exclusivamente o **Poetry** para gestão de dependências e ambientes virtuais.

*   **Proibição:** Não utilize `pip install` diretamente no sistema ou ambiente global.
*   **Ativação do Ambiente:**
    ```bash
    poetry shell
    ```
*   **Execução de Comandos:** Utilize `poetry run <comando>` para garantir o contexto do projeto.
*   **Versão do Python:** Definida no `pyproject.toml`. Para configurar a versão local:
    ```bash
    poetry env use python3.11  # ou a versão específica definida
    ```

## 2. Estrutura do Projeto

A estrutura de diretórios é fixa e deve ser respeitada:

```text
projeto/
├── src/
│   └── projeto/      # Código-fonte principal
├── tests/            # Testes automatizados (Pytest)
├── docs/             # Documentação em Markdown
├── mkdocs.yml        # Configuração do MkDocs
├── pyproject.toml    # Dependências e configurações de ferramentas
├── README.md         # Visão geral do projeto
└── .gitignore        # Exclusões do Git
```

## 3. Qualidade de Código e Formatação

Utilizamos o **Ruff** como ferramenta unificada para linting, formatação e organização de imports.

### Regras Obrigatórias:
*   Nenhum código com erros de lint pode ser commitado.
*   O código deve ser formatado antes de qualquer Pull Request.
*   Imports devem ser organizados automaticamente pelo Ruff.

### Comandos:
```bash
# Verificar erros (Lint)
poetry run ruff check .

# Corrigir erros automaticamente
poetry run ruff check . --fix

# Formatar código
poetry run ruff format .
```

## 4. Testes e Cobertura

O framework oficial de testes é o **Pytest**.

### Regras de Ouro:
*   **Localização:** Todos os testes devem residir na pasta `tests/`.
*   **Cobertura Mínima:** **50%**. Pull Requests que reduzam a cobertura abaixo deste nível ou não atinjam o mínimo serão rejeitados.
*   **Tipologia:** Priorizar testes unitários para lógica de negócio e regras de domínio.

### Execução:
```bash
# Executar todos os testes
poetry run pytest

# Executar com relatório de cobertura
poetry run pytest --cov=src/projeto --cov-report=term-missing
```

## 5. Documentação

A documentação técnica é gerada via **MkDocs** com o tema **Material for MkDocs**.

### Requisitos:
*   Toda funcionalidade pública deve ser documentada.
*   Incluir exemplos de uso (`code blocks`) em novas features.
*   Manter a documentação técnica sincronizada com as mudanças de código.

### Comandos:
```bash
# Servidor local de documentação
poetry run mkdocs serve

# Gerar build estático
poetry run mkdocs build
```

## 6. Dependências de Desenvolvimento

Para configurar o ambiente de desenvolvimento, utilize:
```bash
poetry add --group dev pytest pytest-cov ruff mkdocs-material
```

## 7. Fluxo de Trabalho (Checklist de Entrega)

Antes de finalizar qualquer tarefa ou abrir um Pull Request, execute obrigatoriamente nesta ordem:

1.  **Limpeza e Estilo:** `poetry run ruff check . --fix && poetry run ruff format .`
2.  **Testes:** `poetry run pytest --cov=src/projeto --cov-report=term-missing` (Garantir > 50%)
3.  **Docs:** `poetry run mkdocs build` (Garantir que não há erros de renderização)

## 8. Critérios de Aceitação (Definition of Done)

Uma entrega só é considerada **concluída** quando:
1.  **Ruff:** Zero erros reportados.
2.  **Formatação:** Código seguindo estritamente o padrão Ruff.
3.  **Testes:** 100% de passagem nos testes existentes e novos.
4.  **Cobertura:** Mínimo de 50% atingido/mantido.
5.  **Documentação:** Atualizada e build do MkDocs sem avisos.
6.  **Poetry:** `pyproject.toml` e `poetry.lock` atualizados sem dependências manuais externas.

## 9. Boas Práticas Técnicas

*   **Pythonic Code:** Seguir a PEP 8.
*   **Tipagem:** Utilizar *Type Hints* em todas as assinaturas de funções e métodos.
*   **Modularização:** Funções pequenas, puras (sempre que possível) e reutilizáveis.
*   **Princípios:** Aplicar SOLID e evitar código duplicado (DRY).
*   **Legibilidade:** O código deve ser legível por humanos; otimizações prematuras devem ser evitadas.
*   **Arquitetura:** Manter separação clara entre Domínio (Regras de Negócio), Infraestrutura (Banco, APIs externas) e Interface.

---
*Este documento é a "Fonte da Verdade" para a saúde técnica do projeto. Em caso de dúvida, a regra definida aqui prevalece.*