"""Memória local — SQLite + FTS5, com leak-scan na ingestão.

Dois princípios inegociáveis, em miniatura:

1. O acervo é LOCAL: um arquivo SQLite ao lado do código. Nada viaja.
2. Credencial NUNCA toca o disco em texto: o leak-scan roda ANTES da
   gravação e substitui por [REDACTED].

Caminho de evolução: dedup semântico na ingestão, embeddings + fusão RRF
por cima do FTS5 (com degrade para textual quando offline) e colheita
automática ao concluir tarefas.
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

DB_PADRAO = Path(__file__).parent / "memoria.db"

# Padrões mínimos de credencial. O Renato completo usa um detector bem mais
# rico — mas o conceito é este: a fronteira de ingestão é um gate, não um aviso.
PADROES_SEGREDO = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                       # AWS access key
    re.compile(r"ghp_[A-Za-z0-9]{36}"),                    # GitHub token clássico
    re.compile(r"github_pat_[A-Za-z0-9_]{22,}"),           # GitHub fine-grained
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),                  # chaves estilo sk-...
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),           # Slack
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{16,}"),      # header Authorization
    re.compile(r"(?i)(senha|password|api[_-]?key|token)\s*[:=]\s*\S+"),
]


def redigir(texto: str) -> tuple[str, int]:
    """Substitui credenciais por [REDACTED]. Retorna (texto, quantidade)."""
    total = 0
    for padrao in PADROES_SEGREDO:
        texto, n = padrao.subn("[REDACTED]", texto)
        total += n
    return texto, total


def conectar(db_path: Path | None = None) -> sqlite3.Connection:
    con = sqlite3.connect(db_path or DB_PADRAO)
    con.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS memorias USING fts5(topico, conteudo)"
    )
    return con


def gravar(topico: str, conteudo: str, db_path: Path | None = None) -> dict:
    """Grava uma memória — depois do leak-scan e de um dedup exato simples."""
    topico, n1 = redigir(topico)
    conteudo, n2 = redigir(conteudo)
    con = conectar(db_path)
    try:
        ja_existe = con.execute(
            "SELECT COUNT(*) FROM memorias WHERE topico = ? AND conteudo = ?",
            (topico, conteudo),
        ).fetchone()[0]
        if ja_existe:
            return {"gravado": False, "motivo": "duplicata exata", "redigidos": n1 + n2}
        con.execute("INSERT INTO memorias VALUES (?, ?)", (topico, conteudo))
        con.commit()
        return {"gravado": True, "redigidos": n1 + n2}
    finally:
        con.close()


def contar(db_path: Path | None = None) -> int:
    """Quantas memórias existem no acervo — usado pela ferramenta `verificar`."""
    con = conectar(db_path)
    try:
        return con.execute("SELECT COUNT(*) FROM memorias").fetchone()[0]
    finally:
        con.close()


def recall(consulta: str, limite: int = 5, db_path: Path | None = None) -> list[dict]:
    """Busca textual FTS5. Termos são aspeados um a um — entrada nunca vira sintaxe."""
    termos = [t for t in re.findall(r"\w+", consulta) if len(t) > 1]
    if not termos:
        return []
    query = " OR ".join(f'"{t}"' for t in termos)
    con = conectar(db_path)
    try:
        linhas = con.execute(
            "SELECT topico, conteudo FROM memorias WHERE memorias MATCH ? "
            "ORDER BY rank LIMIT ?",
            (query, limite),
        ).fetchall()
        return [{"topico": t, "conteudo": c} for t, c in linhas]
    finally:
        con.close()
