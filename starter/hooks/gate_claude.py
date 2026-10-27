"""Gate de protocolo para o Claude Code — o método virando bloqueio.

Instrução no prompt se esquece; hook não. Este script é chamado pelo
Claude Code em eventos do ciclo de vida (ver settings_exemplo.json) e
transforma o fluxo da casa em regra mecânica:

  precode-gate   PreToolUse Edit|Write   nega edição de código sem
                                         session_start e iniciar_tarefa
  session-mark   PostToolUse session_start        registra sessão aberta
  rota-mark      PostToolUse iniciar_tarefa       registra tarefa classificada
  edit-mark      PostToolUse Edit|Write           registra edição de código
  complete-mark  PostToolUse task_complete        fecha o ciclo
  stop-gate      Stop                             cobra task_complete, 1x por ciclo

Só morde onde existe AGENTS.md na raiz — instale no escopo global sem
travar pasta aleatória. Erro interno nunca derruba a sessão: em dúvida,
silêncio (o fluxo normal de permissões do Claude Code segue valendo).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

EXTENSOES_CODIGO = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".vue", ".svelte",
    ".html", ".css", ".scss", ".sql", ".sh", ".ps1", ".bat", ".php", ".rb",
    ".go", ".rs", ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".kt", ".swift",
}
# Bloquear a manutenção do próprio hook ou dos artefatos criaria deadlock.
SEGMENTOS_INTERNOS = {".claude", ".renatao"}


def ler_entrada() -> dict:
    try:
        dados = json.loads(sys.stdin.read() or "{}")
        return dados if isinstance(dados, dict) else {}
    except (ValueError, OSError):
        return {}


def raiz_projeto(entrada: dict) -> Path:
    # CLAUDE_PROJECT_DIR é estável; cwd acompanha o `cd` do shell da sessão.
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or entrada.get("cwd") or os.getcwd())


def pasta_markers(entrada: dict) -> Path:
    sessao = re.sub(r"[^A-Za-z0-9_\-]", "_", str(entrada.get("session_id") or "padrao"))[:80]
    return raiz_projeto(entrada) / ".renatao" / ".claude_gates" / sessao


def marcar(entrada: dict, nome: str) -> None:
    pasta = pasta_markers(entrada)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / nome).write_text("1", encoding="utf-8")


def desmarcar(entrada: dict, nome: str) -> None:
    (pasta_markers(entrada) / nome).unlink(missing_ok=True)


def tem(entrada: dict, nome: str) -> bool:
    return (pasta_markers(entrada) / nome).exists()


def e_codigo(caminho: str | None) -> bool:
    if not caminho:
        return False
    partes = Path(caminho.replace("\\", "/")).parts
    if SEGMENTOS_INTERNOS & set(partes):
        return False
    return Path(caminho).suffix.lower() in EXTENSOES_CODIGO


def e_projeto_renato(entrada: dict) -> bool:
    # Nunca usar .renatao/ como sinal: o próprio gate cria essa pasta.
    return (raiz_projeto(entrada) / "AGENTS.md").exists()


def arquivo_alvo(entrada: dict) -> str | None:
    ferramenta = entrada.get("tool_input") or {}
    return ferramenta.get("file_path") or ferramenta.get("notebook_path")


def negar(motivo: str) -> dict:
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": motivo,
    }}


def precode_gate(entrada: dict):
    if not e_codigo(arquivo_alvo(entrada)) or not e_projeto_renato(entrada):
        return None
    if not tem(entrada, "sessao"):
        return negar("Protocolo: sessão não aberta. Chame session_start(tema) antes "
                     "de editar código — ele injeta identidade, regras e memórias.")
    if not tem(entrada, "rota"):
        return negar("Protocolo: tarefa não classificada. Chame iniciar_tarefa(descricao) "
                     "e anuncie o plano antes de editar código.")
    return None  # silêncio, não "allow": allow explícito pularia o prompt do usuário


def stop_gate(entrada: dict):
    if entrada.get("stop_hook_active") or not e_projeto_renato(entrada):
        return None
    # Cada bloqueio custa uma geração extra do modelo: avisa uma vez por ciclo.
    if tem(entrada, "avisado") or not tem(entrada, "edicoes"):
        return None
    marcar(entrada, "avisado")
    return {"decision": "block",
            "reason": "Protocolo: houve edição de código sem task_complete. Rode os "
                      "testes, chame task_complete(resumo, evidencia) com a saída real, "
                      "ou diga explicitamente o que falta e por que não concluiu."}


def edit_mark(entrada: dict):
    if e_codigo(arquivo_alvo(entrada)):
        marcar(entrada, "edicoes")
        desmarcar(entrada, "avisado")  # nova edição re-arma o stop-gate


def complete_mark(entrada: dict):
    desmarcar(entrada, "edicoes")
    desmarcar(entrada, "avisado")


MODOS = {
    "precode-gate": precode_gate,
    "stop-gate": stop_gate,
    "session-mark": lambda e: marcar(e, "sessao"),
    "rota-mark": lambda e: marcar(e, "rota"),
    "edit-mark": edit_mark,
    "complete-mark": complete_mark,
}


def main() -> None:
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    acao = MODOS.get(modo)
    if acao is None:
        return
    resposta = acao(ler_entrada())
    if resposta:
        sys.stdout.write(json.dumps(resposta, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # hook nunca derruba a sessão
        sys.stderr.write(f"gate_claude: {exc}")
