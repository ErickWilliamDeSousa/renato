"""Gate de protocolo para o Claude Code — testes escritos antes do hook.

O hook roda como processo separado (é assim que o Claude Code o chama):
recebe JSON no stdin, responde JSON no stdout ou fica em silêncio.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).parent.parent / "hooks" / "gate_claude.py"


def chamar(modo, projeto, payload=None, stdin_cru=None):
    entrada = stdin_cru if stdin_cru is not None else json.dumps(
        {"session_id": "s1", "cwd": str(projeto), **(payload or {})}
    )
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(projeto)}
    r = subprocess.run(
        [sys.executable, str(HOOK), modo],
        input=entrada, capture_output=True, text=True, timeout=20, env=env,
    )
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout) if r.stdout.strip() else None


def editar(arquivo):
    return {"tool_input": {"file_path": arquivo}}


def projeto_renato(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# protocolo\n", encoding="utf-8")
    return tmp_path


def negado(resposta):
    return (resposta or {}).get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def test_fora_de_projeto_renato_o_gate_fica_em_silencio(tmp_path):
    assert chamar("precode-gate", tmp_path, editar(str(tmp_path / "app.py"))) is None


def test_sem_session_start_a_edicao_de_codigo_e_negada(tmp_path):
    projeto = projeto_renato(tmp_path)
    resposta = chamar("precode-gate", projeto, editar(str(projeto / "app.py")))
    assert negado(resposta)
    assert "session_start" in resposta["hookSpecificOutput"]["permissionDecisionReason"]


def test_com_sessao_mas_sem_rota_ainda_nega(tmp_path):
    projeto = projeto_renato(tmp_path)
    chamar("session-mark", projeto)
    resposta = chamar("precode-gate", projeto, editar(str(projeto / "app.py")))
    assert negado(resposta)
    assert "iniciar_tarefa" in resposta["hookSpecificOutput"]["permissionDecisionReason"]


def test_sessao_e_rota_liberam_em_silencio(tmp_path):
    projeto = projeto_renato(tmp_path)
    chamar("session-mark", projeto)
    chamar("rota-mark", projeto)
    # silêncio, não "allow": allow explícito pularia o prompt de permissão
    assert chamar("precode-gate", projeto, editar(str(projeto / "app.py"))) is None


def test_arquivo_que_nao_e_codigo_nunca_e_bloqueado(tmp_path):
    projeto = projeto_renato(tmp_path)
    assert chamar("precode-gate", projeto, editar(str(projeto / "README.md"))) is None


def test_artefatos_internos_ficam_fora_do_gate(tmp_path):
    # bloquear a manutenção do próprio hook criaria deadlock
    projeto = projeto_renato(tmp_path)
    alvo = str(projeto / ".claude" / "hooks" / "gate_claude.py")
    assert chamar("precode-gate", projeto, editar(alvo)) is None


def test_stop_gate_cobra_task_complete_uma_vez_por_ciclo(tmp_path):
    projeto = projeto_renato(tmp_path)
    assert chamar("stop-gate", projeto) is None          # nada editado: livre
    chamar("edit-mark", projeto, editar(str(projeto / "app.py")))
    primeira = chamar("stop-gate", projeto)
    assert primeira["decision"] == "block"
    assert "task_complete" in primeira["reason"]
    assert chamar("stop-gate", projeto) is None          # avisa uma vez só
    chamar("edit-mark", projeto, editar(str(projeto / "app.py")))
    assert chamar("stop-gate", projeto)["decision"] == "block"  # nova edição re-arma
    chamar("complete-mark", projeto)
    assert chamar("stop-gate", projeto) is None          # ciclo fechado


def test_stop_gate_respeita_stop_hook_active(tmp_path):
    projeto = projeto_renato(tmp_path)
    chamar("edit-mark", projeto, editar(str(projeto / "app.py")))
    assert chamar("stop-gate", projeto, {"stop_hook_active": True}) is None


def test_sessoes_nao_se_misturam(tmp_path):
    projeto = projeto_renato(tmp_path)
    chamar("session-mark", projeto)
    chamar("rota-mark", projeto)
    outra = {"session_id": "s2", **editar(str(projeto / "app.py"))}
    assert negado(chamar("precode-gate", projeto, outra))


def test_session_id_malicioso_nao_escapa_da_pasta_de_markers(tmp_path):
    projeto = projeto_renato(tmp_path)
    chamar("session-mark", projeto, {"session_id": "../../fora"})
    assert not (tmp_path.parent / "fora").exists()
    assert not (projeto / "fora").exists()


def test_stdin_invalido_nunca_derruba_a_sessao(tmp_path):
    projeto = projeto_renato(tmp_path)
    assert chamar("precode-gate", projeto, stdin_cru="isso nao e json") is None


def test_modo_desconhecido_fica_em_silencio(tmp_path):
    assert chamar("modo-inventado", projeto_renato(tmp_path)) is None
