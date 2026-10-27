"""Gate de qualidade mensurável — regra da casa virando número.

"Função curta e simples" é conselho. Isto é mecanismo:

- função com no máximo MAX_LINHAS (100) linhas
- complexidade ciclomática de no máximo MAX_COMPLEXIDADE (14)

Medido pela AST da stdlib: zero dependência, determinístico, auditável.
Sem argumentos, mede só os .py alterados no git — dívida legada não bloqueia
por si; a regra prática é não piorar os números.
"""
from __future__ import annotations

import ast
from pathlib import Path

import protecao

# Ambos são o MÁXIMO PERMITIDO: reprova acima deles. Um nome, um sentido.
MAX_LINHAS = 100
MAX_COMPLEXIDADE = 14

_RAMOS = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler,
          ast.With, ast.AsyncWith, ast.Assert)
_FUNCOES = (ast.FunctionDef, ast.AsyncFunctionDef)


def _complexidade(no: ast.AST) -> int:
    """McCabe simplificado: 1 + pontos de decisão, sem entrar em funções aninhadas."""
    total = 1
    pilha = list(ast.iter_child_nodes(no))
    while pilha:
        filho = pilha.pop()
        if isinstance(filho, (*_FUNCOES, ast.Lambda, ast.ClassDef)):
            continue  # aninhada é medida à parte
        if isinstance(filho, _RAMOS):
            total += 1
        elif isinstance(filho, ast.BoolOp):
            total += len(filho.values) - 1
        elif isinstance(filho, ast.comprehension):
            total += 1 + len(filho.ifs)
        elif isinstance(filho, ast.match_case):
            total += 1
        pilha.extend(ast.iter_child_nodes(filho))
    return total


def _funcoes(arvore: ast.AST, prefixo: str = ""):
    """Gera (nome qualificado, nó) para cada função, inclusive métodos e aninhadas."""
    for no in ast.iter_child_nodes(arvore):
        if isinstance(no, _FUNCOES):
            nome = f"{prefixo}{no.name}"
            yield nome, no
            yield from _funcoes(no, f"{nome}.")
        elif isinstance(no, ast.ClassDef):
            yield from _funcoes(no, f"{prefixo}{no.name}.")
        else:
            yield from _funcoes(no, prefixo)


def complexidade_de_fonte(codigo: str, nome: str) -> int:
    """Complexidade de uma função pelo nome qualificado — usado nos testes."""
    for qualificado, no in _funcoes(ast.parse(codigo)):
        if qualificado == nome:
            return _complexidade(no)
    raise KeyError(nome)


def medir_fonte(codigo: str, arquivo: str) -> list[dict]:
    """Lista as violações de um código-fonte. Erro de sintaxe vira violação."""
    try:
        arvore = ast.parse(codigo)
    except SyntaxError as exc:
        return [{"arquivo": arquivo, "linha": exc.lineno or 0, "funcao": "-",
                 "regra": "sintaxe", "valor": 0, "limite": 0}]
    violacoes = []
    for nome, no in _funcoes(arvore):
        medidas = {
            "linhas": ((no.end_lineno or no.lineno) - no.lineno + 1, MAX_LINHAS),
            "complexidade": (_complexidade(no), MAX_COMPLEXIDADE),
        }
        for regra, (valor, maximo) in medidas.items():
            if valor > maximo:
                violacoes.append({"arquivo": arquivo, "linha": no.lineno, "funcao": nome,
                                  "regra": regra, "valor": valor, "limite": maximo})
    return violacoes


def analisar(caminhos) -> dict:
    """Mede uma lista de arquivos .py e devolve o veredito agregado."""
    violacoes = []
    arquivos = 0
    for caminho in map(Path, caminhos):
        try:
            codigo = caminho.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            violacoes.append({"arquivo": str(caminho), "linha": 0, "funcao": "-",
                              "regra": "leitura", "valor": 0, "limite": 0, "erro": str(exc)})
            continue
        arquivos += 1
        violacoes += medir_fonte(codigo, str(caminho))
    return {"aprovado": not violacoes, "arquivos": arquivos, "violacoes": violacoes}


def arquivos_alterados(raiz) -> list[Path]:
    """.py modificados ou novos no git. Fora de repo (ou git ausente): lista vazia.

    Duas armadilhas que fariam o gate aprovar vazio:
    - sem `-z`, o git escapa nomes com acento ("rela\\303\\247ao.py");
    - o porcelain devolve caminho relativo à RAIZ do repo, não à pasta pedida.
      Por isso: pathspec "." (só o que está sob `raiz`) e junção pelo toplevel.
    """
    raiz = Path(raiz)
    topo = protecao.rodar(["git", "rev-parse", "--show-toplevel"], teto_s=10, cwd=raiz)
    if not topo["ok"]:
        return []
    raiz_repo = Path(topo["saida"].strip())
    r = protecao.rodar(["git", "status", "--porcelain", "-z", "--untracked-files=all", "--", "."],
                       teto_s=10, cwd=raiz)
    if not r["ok"]:
        return []
    alterados = []
    entradas = iter(r["saida"].split("\0"))
    for entrada in entradas:
        estado, nome = entrada[:2], entrada[3:]
        if estado[:1] in "RC":
            next(entradas, None)  # renomeado/copiado: a próxima entrada é a origem
        if "D" in estado or not nome.endswith(".py"):
            continue
        alvo = raiz_repo / nome
        if alvo.is_file():
            alterados.append(alvo)
    return alterados


def resolver_alvos(raiz, lista: str) -> tuple[list[Path], list[str]]:
    """Converte 'a.py, b.py' em caminhos DENTRO do projeto; o resto é recusado."""
    raiz = Path(raiz).resolve()
    alvos, recusados = [], []
    for item in (p.strip() for p in lista.split(",")):
        if not item:
            continue
        alvo = (raiz / item).resolve()
        if alvo.is_relative_to(raiz):
            alvos.append(alvo)
        else:
            recusados.append(item)
    return alvos, recusados


def relatorio(resultado: dict) -> str:
    """Texto curto para o agente: veredito + arquivo:linha de cada violação."""
    if not resultado["arquivos"] and not resultado["violacoes"]:
        return "Nenhum arquivo .py para medir (nada alterado no git?). Aprovado por vacuidade."
    if resultado["aprovado"]:
        return (f"APROVADO: {resultado['arquivos']} arquivo(s), funções com até "
                f"{MAX_LINHAS} linhas e complexidade até {MAX_COMPLEXIDADE}.")
    linhas = [f"REPROVADO: {len(resultado['violacoes'])} violação(ões) em "
              f"{resultado['arquivos']} arquivo(s)."]
    for v in sorted(resultado["violacoes"], key=lambda v: -v["valor"]):
        linhas.append(f"- {v['arquivo']}:{v['linha']} {v['funcao']} — "
                      f"{v['regra']} {v['valor']} (limite {v['limite']})")
    return "\n".join(linhas)
