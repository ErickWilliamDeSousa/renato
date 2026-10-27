# Hooks para o Claude Code — o protocolo como bloqueio

Instrução no prompt é conselho: o modelo lê, concorda e, trinta mensagens
depois, esquece. Hook é mecanismo: o Claude Code chama um processo externo
em cada evento, e o processo pode **negar** a ação.

`gate_claude.py` transforma o fluxo do Renato em regra mecânica:

| Evento | O que acontece |
|---|---|
| Editar código sem `session_start` | **negado**, com a instrução do que chamar |
| Editar código sem `iniciar_tarefa` | **negado**: classifique e anuncie o plano primeiro |
| Encerrar o turno com código editado e sem `task_complete` | **bloqueado uma vez**: rode os testes e cole a evidência, ou diga o que falta |

## Instalar

1. Copie o conteúdo de [`settings_exemplo.json`](settings_exemplo.json) para
   `~/.claude/settings.json` (vale para todos os projetos) ou para
   `.claude/settings.json` do projeto.
2. Troque `C:/renato-main/starter` pelo caminho real da sua pasta.
3. Os matchers `mcp__renato-starter__*` assumem que o servidor foi registrado
   com o nome `renato-starter` (`claude mcp add renato-starter -- python .../servidor_mcp.py`).
   Nome diferente, matcher diferente.
4. Crie um `AGENTS.md` na raiz de cada projeto que deve ser protegido.

## Decisões de desenho (e por quê)

- **Só morde onde há `AGENTS.md`.** Permite instalar no escopo global sem
  travar pasta aleatória. O sinal nunca é `.renatao/`: o próprio gate cria
  essa pasta, e qualquer projeto se auto-promoveria na primeira edição.
- **Silêncio, não `allow`.** Quando o gate não se aplica, o script não emite
  decisão. Um `allow` explícito pularia o prompt de permissão do usuário — o
  gate existe para somar trava, nunca para tirar.
- **Avisa uma vez por ciclo.** Cada bloqueio do `Stop` custa uma geração extra
  do modelo. Repetir o mesmo aviso a cada fim de turno só queima tokens; nova
  edição re-arma o gate.
- **`stop_hook_active` é respeitado.** Sem isso, um `Stop` que bloqueia pode
  entrar em laço infinito.
- **Artefatos internos ficam fora.** Editar `.claude/` ou `.renatao/` nunca é
  bloqueado — senão o gate impediria a manutenção do próprio gate.
- **Erro interno é silêncio.** Hook que lança exceção não pode derrubar a
  sessão; o erro vai para o stderr, para diagnóstico.
- **Markers por sessão**, em `.renatao/.claude_gates/<session_id>/`, com o id
  saneado (um `session_id` como `../../x` não escapa da pasta).

Testes: `pytest tests/test_hook_claude.py` (12 casos, cada um chamando o hook
como o Claude Code chama: processo separado, JSON no stdin).

No Renato completo o mesmo gate cobra `checkpoint('pre-code')` com
classificação trivial/relevante/crítico e injeta o protocolo na abertura da
sessão via `SessionStart`. A semente fica com o essencial: começar certo e
não terminar sem evidência.
