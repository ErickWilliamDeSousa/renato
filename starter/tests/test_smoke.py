"""A semente nasce com teste passando — dogfooding do próprio método."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import memoria
import roteador


def test_roteador_e_deterministico():
    a = roteador.rotear("fazer o deploy do container em producao")
    b = roteador.rotear("fazer o deploy do container em producao")
    assert a == b, "mesmo pedido, mesmo método — sempre"
    assert a["dominio"] == "deploy"


def test_roteador_ignora_acentos_e_caixa():
    assert roteador.classificar("REVISÃO do módulo")[0] == "revisao"


def test_roteador_sem_match_cai_no_geral():
    dominio, pontos = roteador.classificar("qualquer coisa sem termos conhecidos")
    assert dominio == "geral"
    # o pacote geral sempre cobra test-first e aceite como contrato
    rota = roteador.rotear("qualquer coisa sem termos conhecidos")
    assert any("teste antes do código" in p for p in rota["protocolos"])


def test_memoria_grava_e_recall(tmp_path):
    db = tmp_path / "teste.db"
    r = memoria.gravar("decisão de stack", "FastAPI vence Express para esta API", db_path=db)
    assert r["gravado"] is True
    achadas = memoria.recall("stack fastapi", db_path=db)
    assert len(achadas) == 1
    assert "FastAPI" in achadas[0]["conteudo"]


def test_memoria_recusa_duplicata_exata(tmp_path):
    db = tmp_path / "teste.db"
    memoria.gravar("licao", "sempre rodar a suite antes do push", db_path=db)
    r = memoria.gravar("licao", "sempre rodar a suite antes do push", db_path=db)
    assert r["gravado"] is False


def test_leak_scan_redige_antes_de_tocar_o_disco(tmp_path):
    db = tmp_path / "teste.db"
    r = memoria.gravar("config", "a api_key = sk-abcdefghij1234567890XYZ do projeto", db_path=db)
    assert r["redigidos"] >= 1
    achadas = memoria.recall("config projeto", db_path=db)
    assert "sk-abcdefghij" not in achadas[0]["conteudo"]
    assert "[REDACTED]" in achadas[0]["conteudo"]


def test_recall_nao_quebra_com_entrada_maliciosa(tmp_path):
    db = tmp_path / "teste.db"
    memoria.gravar("t", "conteudo qualquer", db_path=db)
    # aspas e sintaxe FTS na consulta não podem virar erro nem injeção
    assert memoria.recall('") OR (topico MATCH "x', db_path=db) is not None


def test_roteador_nao_casa_termo_dentro_de_palavra():
    # bug real da v1: "reiniciar" continha "iniciar" e roteava projeto_novo
    dominio, _ = roteador.classificar("reiniciar o servidor de producao")
    assert dominio == "deploy", "'iniciar' não pode casar dentro de 'reiniciar'"


def test_roteador_prefixo_preserva_flexoes():
    # a fronteira é só no início: "revisar" ainda casa "revisarmos"
    assert roteador.classificar("vamos revisarmos o modulo")[0] == "revisao"


def test_leak_scan_pega_github_fine_grained(tmp_path):
    db = tmp_path / "t.db"
    r = memoria.gravar("t", "use github_pat_11ABCDEFGH0123456789ab_XYZ para clonar", db_path=db)
    assert r["redigidos"] >= 1
    assert "github_pat_" not in memoria.recall("clonar", db_path=db)[0]["conteudo"]


def test_memoria_contar(tmp_path):
    db = tmp_path / "t.db"
    assert memoria.contar(db_path=db) == 0
    memoria.gravar("a", "primeira licao", db_path=db)
    assert memoria.contar(db_path=db) == 1


def test_diagnostico_reporta_tudo_verde():
    import importlib.util
    import pytest
    if importlib.util.find_spec("mcp") is None:
        pytest.skip("pacote mcp não instalado")
    import servidor_mcp
    assert "TUDO VERDE" in servidor_mcp.diagnostico()


def test_gate_recusa_recibo_em_branco():
    import gates
    assert "RECUSADO" in gates.validar_evidencia("   ")


def test_gate_recusa_template_nao_preenchido():
    import gates
    assert "RECUSADO" in gates.validar_evidencia("<cole aqui a saida do comando de aceite>")


def test_gate_aceita_evidencia_real():
    import gates
    saida = "$ pytest -q\n7 passed in 0.31s"
    assert gates.validar_evidencia(saida) is None
