"""Roteador determinístico — zero LLM no caminho crítico.

A classificação de uma tarefa é uma função pura: keywords ponderadas por
domínio, soma decide. Mesmo pedido, mesmo método, sempre — auditar é ler
esta tabela, não interrogar um modelo.

Este é o conceito em miniatura. O caminho de evolução: mais domínios, pesos
calibrados pelo seu histórico real e um "pacote" mais rico por domínio
(protocolos completos, skills sob demanda, memórias relevantes).
"""
from __future__ import annotations

import unicodedata

# Cada domínio tem termos com pesos. A soma dos pesos dos termos presentes
# na tarefa decide o domínio vencedor. Ajuste à sua realidade — e mantenha
# em código: tabela versionada é tabela auditável.
DOMINIOS: dict[str, dict[str, int]] = {
    "deploy": {
        "deploy": 5, "publicar": 4, "producao": 4, "container": 3,
        "docker": 3, "healthcheck": 3, "servidor": 2, "subir": 2,
    },
    "revisao": {
        "revisar": 5, "auditar": 5, "revisao": 4, "bug": 3,
        "quebrado": 3, "erro": 2, "verificar": 2,
    },
    "projeto_novo": {
        "projeto novo": 6, "criar projeto": 5, "iniciar": 3, "scaffold": 5,
        "estrutura": 3, "stack": 3, "do zero": 4,
    },
    "seguranca": {
        "segredo": 5, "senha": 5, "credencial": 5, "vazamento": 4,
        "seguranca": 4, "vulnerabilidade": 4, "auditoria de dependencias": 5,
    },
}

# O pacote de método cobrado em cada domínio. No Renato completo isso vira
# protocolos inteiros, checkpoints e skills; aqui, o esqueleto do conceito.
PACOTES: dict[str, list[str]] = {
    "deploy": [
        "GATE: rode a suíte de testes e cole a saída ANTES do deploy.",
        "GATE: Dockerfile precisa de HEALTHCHECK — sem isso, não embarca.",
        "Depois do deploy, bata no endpoint REAL e guarde a resposta no recibo.",
    ],
    "revisao": [
        "Troque de papel: escreva 3 hipóteses de como o trabalho pode estar quebrado.",
        "Teste cada hipótese DE VERDADE — se a revisão não achou nada, desconfie dela.",
        "Caça a falso-feito: sucesso sem saída colada, teste que não testa.",
    ],
    "projeto_novo": [
        "Responda por escrito as 5 perguntas — inclusive 'o que fica DE FORA da v1?'.",
        "Stack por avaliação (mínimo 2 opções comparadas), registrada em DECISIONS.md.",
        "Dia zero antes de funcionalidade: git, README, .env.example, primeiro teste verde.",
    ],
    "seguranca": [
        "Segredo NUNCA no código nem no acervo — .env + .env.example, sempre.",
        "Rode a varredura de vazamento antes de qualquer entrega pública.",
        "Backup que nunca foi restaurado é fé, não backup.",
    ],
    "geral": [
        "GATE: escreva o critério de aceite antes da primeira linha (comando → saída esperada).",
        "GATE: teste antes do código — veja falhar pelo motivo esperado, então implemente.",
        "Código relevante segue a Regra da Segunda Versão: v1 → 3 críticas → reescrita v2.",
    ],
}


def normalizar(texto: str) -> str:
    """Remove acentos e caixa — a comparação nunca depende de grafia exata."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.lower().strip()


def classificar(tarefa: str) -> tuple[str, int]:
    """Retorna (domínio vencedor, pontuação). Empate ou zero → 'geral'."""
    texto = normalizar(tarefa)
    placar = {
        dominio: sum(peso for termo, peso in termos.items() if termo in texto)
        for dominio, termos in DOMINIOS.items()
    }
    vencedor = max(placar, key=lambda d: placar[d])
    pontos = placar[vencedor]
    if pontos == 0 or list(placar.values()).count(pontos) > 1:
        return "geral", pontos
    return vencedor, pontos


def rotear(tarefa: str) -> dict:
    """A função que o servidor MCP chama: tarefa → domínio + pacote de método."""
    dominio, pontos = classificar(tarefa)
    protocolos = PACOTES["geral"] if dominio == "geral" else PACOTES[dominio] + PACOTES["geral"]
    return {"dominio": dominio, "pontuacao": pontos, "protocolos": protocolos}
