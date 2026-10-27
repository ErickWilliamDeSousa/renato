# Renato no Claude Code — do conselho ao bloqueio

O Renato nasceu falando com o agente do Antigravity. Em 2026 ganhou uma
integração completa com o Claude Code, e ela ensinou uma coisa: **um protocolo
que depende do modelo lembrar de segui-lo é um protocolo que falha na
mensagem 30.** A integração tem três camadas, da mais fraca para a mais forte.

## Camada 1 — Instrução (escopo de usuário)

Um `CLAUDE.md` global (`~/.claude/CLAUDE.md`) com a identidade e o fluxo,
e o servidor MCP registrado **no escopo de usuário**, não por projeto:

```bash
claude mcp add --scope user renato-starter -- python C:/renato-main/starter/servidor_mcp.py
```

Resultado: todo projeto aberto já nasce com as tools e o protocolo, sem setup
por pasta. É necessário, mas é só conselho.

## Camada 2 — Empurrão no momento certo

Hooks de `SessionStart` e `UserPromptSubmit` injetam o lembrete **quando ele
importa**:

- na abertura real de contexto (`startup`/`clear`): "chame `session_start` e
  `recall` antes de qualquer ação". Em `resume`/`compact`, silêncio: a sessão
  já está andando e repetir só gera ruído e custa token;
- no primeiro prompt da sessão, o protocolo completo; depois, nada.
  O protocolo já está no `CLAUDE.md`; repetir a cada prompt é custo sem sinal novo.

## Camada 3 — Gate que nega

Hooks de `PreToolUse` e `Stop` que **recusam**:

| Situação | Resposta do gate |
|---|---|
| editar código antes de `session_start` | nega, dizendo o que chamar |
| editar código antes do checkpoint de pré-código | nega: classifique e anuncie o plano |
| encerrar o turno com código editado sem `task_complete` | bloqueia uma vez por ciclo |

A versão da semente está pronta para usar:
[`starter/hooks/`](../starter/hooks/README.md), com 12 testes que chamam o
hook como o Claude Code chama (processo separado, JSON no stdin).

## Decisões que valem para qualquer gate

- **Escopo pelo `AGENTS.md`.** Gate instalado globalmente só morde em projeto
  que declarou o protocolo. Nunca use uma pasta que o próprio gate cria como
  sinal: ele se auto-promoveria.
- **Silêncio em vez de `allow`.** Um gate soma trava; `allow` explícito
  pularia o prompt de permissão do usuário.
- **Um aviso por ciclo.** Cada bloqueio de `Stop` custa uma geração inteira
  do modelo.
- **`stop_hook_active`.** Sem respeitar essa flag, o `Stop` entra em laço.
- **Modo spike.** Em exploração descartável, um arquivo marcador criado *pelo
  usuário* desliga a cobrança de conclusão (nunca a de edição). Nasce por
  decisão explícita, some apagando o arquivo.
- **Markers idempotentes.** Com config global e de projeto ativas ao mesmo
  tempo, o mesmo hook dispara duas vezes; o marker garante efeito único.

## O que mudou na prática

Antes dos gates, o fluxo era seguido "quase sempre". Depois, o desvio passou
a ter custo visível: o agente recebe a negação com a instrução exata e se
corrige na hora, sem o humano precisar policiar. É a escada de enforcement
na sua forma mais literal: **documento → gate**.
