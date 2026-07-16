# Starter — a semente do seu próprio Renato

Um servidor MCP mínimo e funcional com os conceitos-chave do método.
~300 linhas no total, sem mágica: leia tudo antes de rodar — é o ponto.

## Rodar

```bash
pip install -r requirements.txt
python -m pytest tests/ -q     # 10 testes — a semente nasce verde
python servidor_mcp.py         # servidor MCP via stdio
```

## Conectar no IDE

Qualquer editor que fale MCP. Exemplo de configuração (ajuste o caminho):

```json
{
  "mcpServers": {
    "renato-starter": {
      "command": "python",
      "args": ["C:/caminho/para/starter/servidor_mcp.py"]
    }
  }
}
```

- **VS Code / Cursor**: bloco acima no arquivo de configuração MCP do editor.
- **Antigravity e similares**: mesmo formato, no painel de servidores MCP.

Depois de conectado, peça ao agente: *"chame session_start com o tema da tarefa"*
— e observe a identidade e as memórias entrarem na conversa.

## O que cada arquivo demonstra

| Arquivo | Conceito |
|---|---|
| `servidor_mcp.py` | identidade injetada na conversa + as 4 ferramentas |
| `roteador.py` | classificação determinística — zero LLM no caminho crítico |
| `memoria.py` | acervo local SQLite/FTS5 + leak-scan na ingestão |
| `gates.py` | gates como funções puras — o task_complete recusa recibo em branco |
| `templates/` | os artefatos: contrato, plano de teste, recibo, AGENTS.md |
| `tests/` | o método aplicado a si mesmo: nasceu test-first |

## O caminho de evolução (na ordem que compensa)

1. **Colheita automática** — o `task_complete` já grava a lição; evolua para
   extrair decisões estruturadas de cada conclusão.
2. **Evals por projeto** — um arquivo de casos `comando → saída esperada`;
   rode todos antes de qualquer deploy e **bloqueie** se falhar.
3. **Checkpoints como gates** — pre-code (classificação), pre-test (falha
   esperada confirmada), pre-commit (trilha v1→v2 conferida).
4. **Recall semântico** — embeddings + fusão RRF por cima do FTS5, com
   degrade para busca textual quando offline. O léxico acha o termo exato;
   o semântico acha o conceito.
5. **Selo do projeto** — nota A–F determinística (testes? evals? README?
   segredos fora do código?), medida ao longo do tempo.

Cada conceito está explicado no [dossiê](../index.html) e nos [protocolos](../docs/).

> A regra de ouro: **cada prática só está pronta quando virou mecanismo** —
> algo que bloqueia, não que aconselha. Documento que não bloqueia nada
> volta a ser conselho, e conselho se esquece.
