"""Servidor MCP mínimo — a semente do seu próprio Renato.

Quatro ferramentas que demonstram o coração do método:

  session_start   → injeta identidade + memórias na conversa do agente
  iniciar_tarefa  → roteia a tarefa (determinístico) e cobra o pacote de método
  memoria_gravar  → grava no acervo local (com leak-scan na ingestão)
  task_complete   → GATE: recusa "pronto" sem evidência real, e colhe a lição

Rodar:  python servidor_mcp.py   (transporte stdio — é o que o IDE espera)
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

import gates
import memoria
import roteador

mcp = FastMCP("renato-starter")

IDENTIDADE = """\
Você está operando sob o método da casa. Regras que não são sugestões:

1. ACEITE COMO CONTRATO — antes da primeira linha: qual comando vou rodar e
   que saída espero ver? "Funciona" é opinião; "esse comando roda e sai isso" é fato.
2. TEST-FIRST — escreva o teste, rode, confirme a falha pelo motivo esperado,
   só então implemente. Sem teste falhando primeiro, não há implementação.
3. REGRA DA SEGUNDA VERSÃO — código relevante nunca entrega a v1:
   v1 → 3 críticas concretas → reescrita v2, com a trilha registrada.
4. EVIDÊNCIA ANTES DE "PRONTO" — cole a saída real. Recibo em branco é recusado.
"""


@mcp.tool()
def session_start(tema: str = "") -> str:
    """Inicia a sessão: identidade da casa + memórias relevantes ao tema."""
    partes = [IDENTIDADE]
    if tema:
        lembradas = memoria.recall(tema)
        if lembradas:
            partes.append("Memórias relevantes de sessões anteriores:")
            partes += [f"- [{m['topico']}] {m['conteudo']}" for m in lembradas]
    return "\n".join(partes)


@mcp.tool()
def iniciar_tarefa(descricao: str) -> str:
    """Classifica a tarefa (função pura, zero LLM) e devolve o método cobrado."""
    rota = roteador.rotear(descricao)
    linhas = [
        f"Domínio: {rota['dominio']} (pontuação {rota['pontuacao']})",
        "Método desta tarefa — cada item é cobrado, não sugerido:",
    ]
    linhas += [f"{i}. {p}" for i, p in enumerate(rota["protocolos"], 1)]
    return "\n".join(linhas)


@mcp.tool()
def memoria_gravar(topico: str, conteudo: str) -> str:
    """Grava uma decisão ou lição no acervo local (leak-scan roda antes)."""
    resultado = memoria.gravar(topico, conteudo)
    aviso = f" ⚠ {resultado['redigidos']} segredo(s) redigido(s)." if resultado["redigidos"] else ""
    if not resultado["gravado"]:
        return f"Não gravado: {resultado['motivo']}.{aviso}"
    return f"Memória gravada.{aviso}"


@mcp.tool()
def task_complete(resumo: str, evidencia: str) -> str:
    """GATE de conclusão: sem evidência real, não existe 'pronto'."""
    recusa = gates.validar_evidencia(evidencia)
    if recusa:
        return recusa
    memoria.gravar(
        f"tarefa concluída: {resumo[:60]}",
        f"{resumo}\nEvidência: {evidencia.strip()[:400]}",
    )
    return "Tarefa aceita. Evidência registrada e lição colhida para o acervo."


if __name__ == "__main__":
    mcp.run()
