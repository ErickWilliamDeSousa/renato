"""Gate de qualidade mensurável — testes escritos antes do código.

Regra da casa: função com até 100 linhas e complexidade ciclomática
abaixo de 15. Medido por AST da stdlib: zero dependência nova.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import qualidade


def _funcao_com_linhas(n: int) -> str:
    corpo = "\n".join(f"    x{i} = {i}" for i in range(n - 1))
    return f"def longa():\n{corpo}\n"


def _funcao_com_ifs(n: int) -> str:
    corpo = "\n".join(f"    if a == {i}:\n        return {i}" for i in range(n))
    return f"def ramificada(a):\n{corpo}\n    return -1\n"


def test_funcao_com_100_linhas_passa():
    assert qualidade.medir_fonte(_funcao_com_linhas(100), "a.py") == []


def test_funcao_com_101_linhas_reprova():
    violacoes = qualidade.medir_fonte(_funcao_com_linhas(101), "a.py")
    assert len(violacoes) == 1
    v = violacoes[0]
    assert v["regra"] == "linhas"
    assert v["valor"] == 101
    assert v["funcao"] == "longa"
    assert v["linha"] == 1


def test_complexidade_14_passa_e_15_reprova():
    assert qualidade.medir_fonte(_funcao_com_ifs(13), "b.py") == []  # 1 + 13 = 14
    violacoes = qualidade.medir_fonte(_funcao_com_ifs(14), "b.py")   # 1 + 14 = 15
    assert [v["regra"] for v in violacoes] == ["complexidade"]
    assert violacoes[0]["valor"] == 15


def test_operadores_booleanos_e_excecoes_contam():
    codigo = (
        "def f(a, b, c):\n"
        "    if a and b and c:\n"      # if +1, BoolOp com 3 operandos +2
        "        pass\n"
        "    try:\n"
        "        pass\n"
        "    except ValueError:\n"     # +1
        "        pass\n"
        "    return [x for x in a if x]\n"  # compreensão +1, filtro +1
    )
    assert qualidade.complexidade_de_fonte(codigo, "f") == 7


def test_metodos_async_e_aninhadas_sao_medidas_separadamente():
    codigo = (
        "class C:\n"
        "    async def m(self):\n"
        "        def interna():\n"
        + "".join(f"            if self == {i}: return {i}\n" for i in range(15))
        + "        return interna\n"
    )
    nomes = {v["funcao"] for v in qualidade.medir_fonte(codigo, "c.py")}
    # a complexidade da interna não infla a externa
    assert nomes == {"C.m.interna"}


def test_arquivo_com_erro_de_sintaxe_vira_violacao_nao_excecao():
    violacoes = qualidade.medir_fonte("def quebrado(:\n", "ruim.py")
    assert violacoes[0]["regra"] == "sintaxe"


def test_analisar_caminhos_resume_veredito(tmp_path):
    bom = tmp_path / "bom.py"
    bom.write_text("def f():\n    return 1\n", encoding="utf-8")
    ruim = tmp_path / "ruim.py"
    ruim.write_text(_funcao_com_ifs(20), encoding="utf-8")
    resultado = qualidade.analisar([bom, ruim])
    assert resultado["aprovado"] is False
    assert resultado["arquivos"] == 2
    assert len(resultado["violacoes"]) == 1
    assert "ruim.py" in qualidade.relatorio(resultado)


def test_analisar_lista_vazia_aprova_mas_avisa():
    resultado = qualidade.analisar([])
    assert resultado["aprovado"] is True
    assert "nenhum arquivo" in qualidade.relatorio(resultado).lower()


def test_arquivos_alterados_fora_de_repo_git_degrada_para_vazio(tmp_path):
    assert qualidade.arquivos_alterados(tmp_path) == []


def test_arquivos_alterados_lista_py_modificados_e_novos(tmp_path):
    def git(*args):
        # config local explícita: o teste não pode depender do git de quem instala
        # (assinatura GPG global, hooks, identidade ausente)
        base = ["git", "-c", "user.email=t@t", "-c", "user.name=t",
                "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
        subprocess.run([*base, *args], cwd=tmp_path, check=True,
                       stdin=subprocess.DEVNULL, capture_output=True)
    try:
        git("init", "-q")
        (tmp_path / "velho.py").write_text("x = 1\n", encoding="utf-8")
        (tmp_path / "leia.md").write_text("doc\n", encoding="utf-8")
        git("add", ".")
        git("commit", "-qm", "base")
    except (OSError, subprocess.CalledProcessError):
        import pytest
        pytest.skip("git indisponível ou sem permissão para commitar")
    (tmp_path / "velho.py").write_text("x = 2\n", encoding="utf-8")
    (tmp_path / "novo.py").write_text("y = 1\n", encoding="utf-8")
    (tmp_path / "relação.py").write_text("z = 1\n", encoding="utf-8")
    nomes = sorted(p.name for p in qualidade.arquivos_alterados(tmp_path))
    # v1 perdia "relação.py": git escapa acento sem -z e o gate aprovava vazio
    assert nomes == ["novo.py", "relação.py", "velho.py"]


def test_arquivos_alterados_em_subpasta_do_repo(tmp_path):
    # achado no dogfooding: porcelain devolve caminho relativo à RAIZ do repo;
    # medido de dentro de starter/, a v2 juntava starter/starter/x.py e
    # aprovava por vacuidade
    try:
        subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True,
                       stdin=subprocess.DEVNULL, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        import pytest
        pytest.skip("git indisponível")
    sub = tmp_path / "starter"
    sub.mkdir()
    (sub / "dentro.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "fora.py").write_text("x = 1\n", encoding="utf-8")
    nomes = [p.name for p in qualidade.arquivos_alterados(sub)]
    assert nomes == ["dentro.py"]   # só o que está sob a pasta pedida


def test_limite_reportado_e_o_maximo_permitido():
    v = qualidade.medir_fonte(_funcao_com_ifs(14), "b.py")[0]
    assert v["limite"] == qualidade.MAX_COMPLEXIDADE == 14
    v = qualidade.medir_fonte(_funcao_com_linhas(101), "a.py")[0]
    assert v["limite"] == qualidade.MAX_LINHAS == 100


def test_resolver_alvos_confina_ao_projeto(tmp_path):
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    alvos, recusados = qualidade.resolver_alvos(tmp_path, "ok.py, ../fora.py, C:/Windows/x.py")
    assert [p.name for p in alvos] == ["ok.py"]
    assert len(recusados) == 2
