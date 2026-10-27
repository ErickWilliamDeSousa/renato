# Novidades

O que mudou no método e na semente, em ordem do mais recente. Cada item
aponta para o mecanismo, não para a promessa.

## Outubro de 2026 — o protocolo vira bloqueio

Três meses de uso diário do Renato completo (de 699 para 1.509 testes na
suíte, uma auditoria geral com achados P0 a P3) trazidos para o público.

### Na semente (`starter/`), tudo test-first — de 15 para 72 testes

- **`protecao.py`** — a fronteira do servidor MCP stdio:
  - `redigir_saida`: redação de segredo no que **sai** para o modelo, só com
    padrões de alta precisão (hashes de prova ficam intactos);
  - `nao_confiavel`: memória entregue como `<dados-nao-confiaveis>`, com a tag
    de fechamento neutralizada por dentro;
  - `rodar`: subprocess com `stdin=DEVNULL`, sem shell, `GIT_TERMINAL_PROMPT=0`
    e teto de parede que mata a **árvore** de processos.
- **Decorador `blindar`** no servidor: toda tool passa pelo redator, inclusive
  mensagens de erro (o erro é reportado, nunca suprimido nem vazado).
- **Tool `qualidade`** (`qualidade.py`): função com até 100 linhas e complexidade
  ciclomática até 14, medidas por AST da stdlib. Sem argumentos, mede só os
  `.py` alterados no git.
- **`hooks/gate_claude.py`**: gate de protocolo para o Claude Code — nega editar
  código sem `session_start` e `iniciar_tarefa`, cobra `task_complete` antes de
  encerrar (uma vez por ciclo). Só age onde há `AGENTS.md`.
- `session_start` passou a entregar memórias como dado não confiável.

Trilha da Regra da Segunda Versão desta entrega — a v1 também passou nos
testes, e mesmo assim foi reescrita:

| Fraqueza da v1 | Como a v2 resolve |
|---|---|
| `subprocess.run(timeout=)` mata o filho mas volta a ler o pipe sem teto: um neto segurando o stdout pendura a tool | saída em arquivo temporário + `taskkill /T` / grupo de processos; teste com neto real |
| `git status` sem `-z` escapa nomes com acento: o arquivo "some" e o gate aprova vazio | `-z` + teste com `relação.py` |
| exceção de tool saía crua (com possível segredo); `qualidade` aceitava `../` | `blindar` captura e redige; `resolver_alvos` confina ao projeto |

E o dogfooding (rodar o gate no próprio starter) achou um quarto bug que os
testes não pegavam: em subpasta do repo, o `git status` devolve caminhos
relativos à raiz e o gate aprovava vazio. Virou teste e correção.

### Na documentação

- **Novo:** [Lições de servidor MCP stdio](docs/LICOES_MCP_STDIO.md) — sete regras,
  cada uma de um incidente real.
- **Novo:** [Renato no Claude Code](docs/CLAUDE_CODE.md) — escopo de usuário, hooks,
  e as decisões de desenho de um gate que não atrapalha.
- **Novo:** [Contexto é orçamento](docs/CONTEXTO.md) — perfil de 16 tools,
  abertura 57% menor, SESSION_BRIEF, START_HERE progressivo, modos persistentes,
  telemetria por chamada.
- [Segurança](docs/SEGURANCA.md): camadas 9 a 11 (redação na saída, memória como
  dado, subprocess seguro), laudo com Selo de Fonte e a pré-checagem de shell
  descrita como ela é — checagem, não sandbox.
- [Memória](docs/MEMORIA.md): recall com prazo e cooldown, memória automática
  rebaixada no ranking, vetores em float32.
- [Arquitetura](docs/ARQUITETURA.md): hooks do editor no desenho, números atualizados.

### No Renato completo (fica em casa, descrito aqui)

- Laudo de segurança com bateria medida, SBOM, varredura do histórico git,
  carimbo RFC 3161 e Selo de Fonte verificável.
- Auditoria geral de outubro: todos os subprocess com `stdin=DEVNULL`, redação
  na saída de toda tool, namespace de tools completado, código morto arquivado
  fora da árvore com instrução de restauração.
- Modo de trabalho persistente com precedência explícita e template pedagogo
  completo entregue pelo MCP.

## Julho de 2026 — lançamento público

Repositório, landing com o roteador ao vivo, dossiê de 18 seções, protocolos,
guias e a semente MCP com 15 testes, instalador de um clique e diagnóstico.
