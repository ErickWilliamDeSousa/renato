<div align="center">

# RENATO

### Seu agente de IA escreve rápido. O Renato faz ele escrever **certo**.

*Método de engenharia para a era dos agentes — memória persistente, protocolos executáveis
e gates que não aceitam "confia".*

[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-2ea44f)](LICENSE)
[![Testes](https://img.shields.io/badge/testes-72%20passando-2ea44f)](starter/tests)
[![MCP](https://img.shields.io/badge/protocolo-MCP-blue)](https://modelcontextprotocol.io)
[![Feito no Brasil](https://img.shields.io/badge/feito%20no-Brasil-ffdf00)](#filosofia)

**[Leia o dossiê completo](https://erickwilliamdesousa.github.io/renato/)** — 18 seções: tese, arquitetura, protocolos, segurança, números e o modelo de trabalho

</div>

---

## O problema

Ferramentas de IA escrevem código numa velocidade impensável há dois anos. Mas velocidade
não é qualidade. O agente entrega a primeira versão que funciona — e quase todo mundo
aceita. O resultado é **protótipo disfarçado de produto**: "funciona na minha máquina",
segredo vazado no commit, e o mesmo erro repetido projeto após projeto, porque a IA
não lembra do que já foi decidido.

Disciplina de engenharia não pode depender de força de vontade — ainda mais quando quem
escreve o código é uma IA confiante e apressada. Documento se ignora, checklist se pula,
boa intenção se esquece. **Tem que virar sistema.**

## A tese: a escada de enforcement

Toda prática de engenharia sobe uma escada — e só descansa quando vira mecanismo:

```
documento → artefato → gate → verificação automática → métrica no tempo
(se esquece) (sobrevive)
```

O trabalho do Renato é empurrar cada regra da casa o mais para a direita possível.
**Conselho se esquece. Mecanismo sobrevive.**

## Como funciona

O Renato é um cérebro central **local**: um servidor MCP + CLI determinística que se
conecta ao agente do seu editor (Claude Code, Antigravity, VS Code, Cursor — qualquer um que fale MCP).

```mermaid
flowchart LR
    A["AGENTE DO IDE<br/><small>quem escreve o código</small>"] <-->|MCP| B["SERVIDOR RENATO<br/><small>identidade · checkpoints · gates<br/>100% local</small>"]
    B --> C["SEU PROJETO<br/><small>artefatos .renatao/<br/>trilha auditável</small>"]
```

Ele dá ao agente três coisas que faltam nele:

| Falta no agente | O Renato entrega |
|---|---|
| **Memória** | acervo local (SQLite FTS5 + embeddings) que atravessa sessões e projetos, com colheita automática ao concluir |
| **Método** | protocolos injetados *dentro da conversa*, roteados por classificação determinística — zero LLM no caminho crítico |
| **Cobrança** | gates que recusam: "pronto" sem evidência, deploy com eval falhando, Dockerfile sem healthcheck |

## Os dois ciclos centrais

```mermaid
flowchart TD
    subgraph SV["REGRA DA SEGUNDA VERSÃO"]
        direction TB
        E["v1 — RASCUNHO<br/><small>nunca é entregue</small>"] --> F["3 CRÍTICAS CONCRETAS<br/><small>trocar de papel e atacar</small>"]
        F --> G["v2 — REESCRITA<br/><small>repensar, não renomear</small>"]
        G --> H["TRILHA NO RECIBO<br/><small>v1 → críticas → v2</small>"]
    end
    subgraph TF["CICLO TEST-FIRST (XP)"]
        direction TB
        A2["1 · ESCREVE O TESTE<br/><small>antes do código</small>"] --> B2["2 · RODA → FALHA<br/><small>pelo motivo esperado</small>"]
        B2 --> C2["3 · IMPLEMENTA<br/><small>a menor mudança</small>"]
        C2 --> D2["4 · RODA → VERDE<br/><small>evidência real</small>"]
    end
```

Sem teste falhando primeiro, não há implementação. E a primeira versão que funciona
ancora o pensamento — por isso **a v1 nunca é entregue**. Código crítico (auth,
pagamento, dados) exige torneio de 3 abordagens julgadas.

## Manifesto — cada frase tem um mecanismo atrás

| A frase | O mecanismo |
|---|---|
| *"Funciona" é opinião. "Esse comando roda e sai isso" é fato.* | critério de aceite como contrato |
| *Conselho se esquece. Mecanismo sobrevive.* | a escada de enforcement |
| *A v1 nunca é entregue.* | Regra da Segunda Versão |
| *O autor jura. O adversário acha.* | revisão adversarial |
| *Container é gado, não bicho de estimação.* | guia do fluxo de deploy |
| *Backup que nunca foi restaurado é fé, não backup.* | backup com verificação de integridade |
| *A nota só sobe com mecanismo, nunca com promessa.* | Selo da Casa (A–F) |
| *Avaliação, não dogma: se PHP for a melhor saída, PHP vence.* | decisão de stack registrada |

## Novidades — outubro de 2026

Três meses de uso diário viraram mecanismo. O que mudou (detalhes no [CHANGELOG](CHANGELOG.md)):

| O que | Por que importa |
|---|---|
| **Gates no Claude Code** — hooks que negam editar código sem abrir a sessão e cobram `task_complete` antes de encerrar | o protocolo deixou de depender de o modelo lembrar dele ([como](docs/CLAUDE_CODE.md); [hooks prontos](starter/hooks/README.md)) |
| **Lições de servidor MCP stdio** — subprocess sem herdar stdin, teto que mata a árvore, nada de import pesado dentro da chamada | cada regra veio de um travamento real diagnosticado ao vivo ([as sete regras](docs/LICOES_MCP_STDIO.md)) |
| **Redação de segredo na saída** de toda tool, e memória entregue como `<dados-nao-confiaveis>` | segredo antigo não volta pelo recall; memória envenenada não dá ordem |
| **Gate de qualidade mensurável** — função com até 100 linhas e complexidade até 14, por AST | "código simples" virou número, sem dependência nova |
| **Dieta de contexto** — 16 tools por padrão (eram 37), abertura de sessão 57% menor, resumo de sessão com teto | agente mais barato e menos distraído ([números](docs/CONTEXTO.md)) |
| **Laudo de segurança** com Selo de Fonte (sha256 por arquivo + hash da árvore git), SBOM e varredura do histórico | prova *qual versão* foi auditada |

Tudo que cabe na semente foi para ela, test-first: o starter foi de 15 para **72 testes**.

## O que está aqui — e o que não está

Este repositório **não é o Renato inteiro**. É o conceito completo + uma semente funcional:

| Aberto (aqui) | Em casa (não publicado) |
|---|---|
| O método e os protocolos, na íntegra conceitual | As 1.200+ skills indexadas |
| A arquitetura e todas as decisões | Os evals e o Selo da Casa de produção |
| Um starter MCP **funcional** (menos de 900 linhas, 72 testes) | A memória acumulada — o acervo é de quem constrói o seu |
| Os templates de artefatos | Segredos e chaves — **sempre** |

A ideia: você não clona o Renato — você **inicia o seu**. O caminho está mapeado;
a caminhada (e o acervo que ela gera) é sua.

## Comece agora

**Nunca programou?** Sem problema — o guia foi feito pra você:
**[Do zero ao Renato funcionando](starter/README.md)** — baixar o ZIP, instalar o
Python, dar **duplo clique em `INSTALAR.bat`** (ele instala tudo, roda os testes
e gera a configuração do Antigravity prontinha) e dar o primeiro comando. ~10 min.

**Já é dev?**

```bash
git clone https://github.com/ErickWilliamDeSousa/renato.git
cd renato/starter
pip install -r requirements.txt
python -m pytest tests/ -q # a semente nasce verde: 72 testes
python servidor_mcp.py # servidor MCP no ar
```

Config por editor, exemplo de sessão e guia de extensão: [manual do starter](starter/README.md#para-quem-é-técnico).

## Documentação

| Doc | O que responde |
|---|---|
| [Dossiê completo (página)](https://erickwilliamdesousa.github.io/renato/) | tudo, com a narrativa inteira — comece por aqui |
| [Manifesto](docs/MANIFESTO.md) | as frases da casa e o mecanismo por trás de cada uma |
| [Arquitetura](docs/ARQUITETURA.md) | componentes, o fluxo de uma tarefa (9 passos, 6 gates) |
| [**Deep-dive de engenharia**](docs/ENGENHARIA.md) | **para dev sênior**: RRF, gates puros, decisões e trade-offs, como o starter vira produção |
| [**Lições de servidor MCP stdio**](docs/LICOES_MCP_STDIO.md) | **novo**: sete regras que custaram incidentes reais — stdin herdado, timeout que não corta, import pesado, segredo na saída |
| [**Renato no Claude Code**](docs/CLAUDE_CODE.md) | **novo**: do conselho ao bloqueio — escopo de usuário e hooks que negam edição fora do fluxo |
| [**Contexto é orçamento**](docs/CONTEXTO.md) | **novo**: 16 tools em vez de 37, abertura 57% menor, SESSION_BRIEF de 2.000 caracteres, modos persistentes |
| [Roteamento](docs/ROTEAMENTO.md) | por que zero LLM no caminho crítico |
| [Memória](docs/MEMORIA.md) | recall híbrido (FTS5 + embeddings + RRF), colheita, honestidade sobre dados |
| [Artefatos](docs/ARTEFATOS.md) | a papelada que trabalha: GSD, recibo, evals, selo |
| [Segurança](docs/SEGURANCA.md) | defesa em profundidade: 8 ameaças → 8 camadas |
| [Protocolo test-first](docs/PROTOCOLO_TEST_FIRST.md) | o ciclo como gate, não como conselho |
| [Protocolo Segunda Versão](docs/PROTOCOLO_SEGUNDA_VERSAO.md) | v1 → críticas → v2, e o torneio |
| [Protocolo adversarial](docs/PROTOCOLO_ADVERSARIAL.md) | 3 hipóteses de quebra + caça ao falso-feito |
| [Guia de projeto novo](docs/GUIA_PROJETO_NOVO.md) | o dia zero: fundação antes de funcionalidade |
| [Guia do fluxo de deploy](docs/GUIA_FLUXO_DEPLOY.md) | git → build → container → produção vigiada |
| [Guia de segurança](docs/GUIA_SEGURANCA.md) | o essencial para não ser invadido no primeiro mês |
| [Leve para o seu time](docs/ADOCAO.md) | o método **sem** a ferramenta: uma prática por semana |
| [FAQ](docs/FAQ.md) | as objeções de sempre, respondidas sem marketing |

## Filosofia

> **"A vida é isso: conhecimento só serve se compartilhado."**

O Renato nasceu de uma necessidade real: trabalho solo, várias empresas e projetos ao
mesmo tempo, e a urgência de transformar velocidade de IA em software de verdade. Ele
não nasceu para ser exclusivo. Os segredos e as chaves ficam em casa — **o conhecimento, não**.

Use, adapte, melhore — e repasse.

## Licença

[MIT](LICENSE) — feito em português, no Brasil, com método brasileiro:
avaliação em vez de dogma, evidência em vez de juramento — **e a porta aberta**.
