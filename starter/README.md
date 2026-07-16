# Manual do Starter — a semente do seu próprio Renato

Um servidor MCP mínimo e **funcional** com os conceitos-chave do método.
~300 linhas no total, sem mágica: leia tudo antes de rodar — é o ponto.

## O mapa

| Arquivo | Conceito que demonstra | Linhas |
|---|---|---|
| `servidor_mcp.py` | identidade injetada na conversa + as 4 ferramentas | ~90 |
| `roteador.py` | classificação determinística — zero LLM no caminho crítico | ~90 |
| `memoria.py` | acervo local SQLite/FTS5 + leak-scan na ingestão | ~100 |
| `gates.py` | gates como funções puras — recusa recibo em branco | ~30 |
| `templates/` | os artefatos: contrato, plano de teste, recibo, AGENTS.md | — |
| `tests/test_smoke.py` | o método aplicado a si mesmo: nasceu test-first | 10 testes |

---

## 1. Instalação

**Requisitos:** Python 3.10+ ([python.org](https://python.org) — marque *"Add to PATH"* na instalação).

```bash
git clone https://github.com/ErickWilliamDeSousa/renato.git
cd renato/starter
pip install -r requirements.txt
```

**Prove que está vivo antes de qualquer coisa** (aceite como contrato — o nosso próprio):

```bash
python -m pytest tests/ -q
```

Saída esperada: `10 passed`. Se apareceu isso, a semente está saudável.

## 2. Conectar no seu IDE

O servidor fala MCP via stdio. A configuração é a mesma ideia em todo editor:
*"rode este comando e converse com ele"*. Ajuste o caminho para onde você clonou.

### Claude Code
```bash
claude mcp add renato-starter -- python C:/caminho/para/renato/starter/servidor_mcp.py
```

### Cursor — arquivo `~/.cursor/mcp.json` (ou `.cursor/mcp.json` no projeto)
```json
{
  "mcpServers": {
    "renato-starter": {
      "command": "python",
      "args": ["C:/caminho/para/renato/starter/servidor_mcp.py"]
    }
  }
}
```

### VS Code (Copilot/MCP) — arquivo `.vscode/mcp.json` no projeto
```json
{
  "servers": {
    "renato-starter": {
      "type": "stdio",
      "command": "python",
      "args": ["C:/caminho/para/renato/starter/servidor_mcp.py"]
    }
  }
}
```

### Antigravity e outros
Mesmo padrão: painel de servidores MCP → novo servidor stdio → comando `python`,
argumento com o caminho do `servidor_mcp.py`.

> **Dica Windows:** use barras normais `/` ou barras duplas `\\` no JSON — barra
> simples `\` quebra o parse.

## 3. Uma sessão de exemplo

Com o servidor conectado, converse com o agente do IDE assim:

**Você:** *"Chame session_start com o tema 'api de pedidos'."*
→ O agente recebe a identidade da casa (aceite como contrato, test-first, segunda
versão, evidência) + memórias de sessões anteriores sobre o tema. **A partir daqui
ele trabalha sob as regras.**

**Você:** *"Chame iniciar_tarefa: 'fazer o deploy do container em produção'."*
→ Resposta: domínio `deploy`, com o método cobrado — suíte antes do push,
HEALTHCHECK obrigatório, smoke no endpoint real. Rode duas vezes: **a resposta é
idêntica** — determinismo é feature.

**Você:** *"Grave na memória: decidimos FastAPI em vez de Express porque o time domina Python."*
→ `memoria_gravar` guarda no acervo local. Se houver uma credencial no texto, ela
vira `[REDACTED]` **antes** de tocar o disco — teste você mesmo.

**Você:** *"Chame task_complete com o resumo e a evidência."*
→ Se a evidência for vazia ou template: **RECUSADO**. Cole a saída real do comando
de aceite e ele aceita — e colhe a lição para a próxima sessão.

## 4. Os templates no seu projeto

Copie `templates/` para uma pasta `.renatao/` no seu projeto e use em toda tarefa:

1. `GSD_TASK.md` — preencha ANTES da primeira linha (objetivo + comando → saída esperada)
2. `TEST_FIRST_PLAN.md` — o teste e a falha esperada, antes de implementar
3. `EXECUTION_RECEIPT.md` — a evidência real + a trilha v1 → críticas → v2
4. `AGENTS.md` — copie para a raiz do repo: é o manual que qualquer agente lê ao chegar

## 5. Estendendo a semente (por onde crescer)

**Novo domínio no roteador** — adicione uma entrada em `DOMINIOS` e o pacote
correspondente em `PACOTES` (`roteador.py`). Escreva o teste primeiro: *"tarefa X
deve rotear para o domínio Y"*.

**Nova regra na identidade** — edite `IDENTIDADE` em `servidor_mcp.py`. Regra boa
tem verbo e consequência ("X é recusado sem Y"), não conselho vago.

**Novo padrão no leak-scan** — adicione o regex em `PADROES_SEGREDO`
(`memoria.py`) e um teste provando que ele redige.

**Novo gate** — função pura em `gates.py` (entrada → recusa ou None) + o wrapper
de uma linha no servidor. Gates testáveis são gates confiáveis.

## 6. O caminho de evolução (na ordem que compensa)

1. **Colheita automática** — o `task_complete` já grava a lição; evolua para extrair
   decisões estruturadas de cada conclusão.
2. **Evals por projeto** — um arquivo de casos `comando → saída esperada`; rode todos
   antes de qualquer deploy e **bloqueie** se falhar.
3. **Checkpoints como gates** — pre-code (classificação), pre-test (falha esperada
   confirmada), pre-commit (trilha v1→v2 conferida).
4. **Recall semântico** — embeddings + fusão RRF por cima do FTS5, com degrade para
   busca textual offline ([como funciona](../docs/MEMORIA.md)).
5. **Selo do projeto** — nota A–F determinística, medida ao longo do tempo.

> A regra de ouro: **cada prática só está pronta quando virou mecanismo** — algo que
> bloqueia, não que aconselha.

## 7. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `python` não é reconhecido | Python fora do PATH | reinstale marcando *Add to PATH*, ou use `py` no lugar de `python` |
| `ModuleNotFoundError: mcp` | dependências não instaladas | `pip install -r requirements.txt` na pasta `starter/` |
| IDE não lista as ferramentas | caminho errado no JSON | use o caminho ABSOLUTO do `servidor_mcp.py`, com `/` |
| `no such module: fts5` | Python muito antigo | atualize para 3.10+ (o FTS5 vem embutido no SQLite dele) |
| acentos estranhos no Windows | console em cp1252 | `set PYTHONIOENCODING=utf-8` antes de rodar |
