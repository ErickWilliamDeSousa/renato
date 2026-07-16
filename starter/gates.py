"""Gates são funções puras: entrada → veredito, testáveis uma a uma.

O servidor MCP só embrulha o que está aqui. Se um dia você trocar de
transporte (CLI, hook de CI, outro protocolo), os gates vêm junto intactos.
"""
from __future__ import annotations

# Marcas inequívocas de template não preenchido. Cuidado ao adicionar termos
# genéricos: "todo" recusaria evidência legítima em português ("todos passaram").
MARCAS_DE_TEMPLATE = ("<cole aqui", "<saida aqui", "<preencha", "todo:", "fixme:")


def validar_evidencia(evidencia: str) -> str | None:
    """Retorna a mensagem de recusa, ou None se a evidência é aceitável.

    O gate não julga se a evidência é BOA — julga se ela EXISTE de verdade:
    recibo em branco, curto demais ou template não passa.
    """
    ev = evidencia.strip()
    if len(ev) < 20:
        return (
            "RECUSADO: evidência ausente ou curta demais. "
            "Rode o critério de aceite e cole a SAÍDA REAL do comando."
        )
    baixa = ev.lower()
    if any(marca in baixa for marca in MARCAS_DE_TEMPLATE):
        return (
            "RECUSADO: a evidência ainda contém texto de template. "
            "Substitua pelo resultado real da execução."
        )
    return None
