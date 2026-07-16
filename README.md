# RENATO — método de engenharia para a era dos agentes de IA

> **"A vida é isso: conhecimento só serve se compartilhado."**

Seu agente de IA escreve rápido. O Renato faz ele escrever **certo**.

O Renato é um cérebro central local (servidor MCP + CLI determinística) que dá ao agente
do seu IDE três coisas que faltam nele: **memória que persiste** entre sessões,
**método que não depende de boa vontade** e **gates que não aceitam "confia"**.

📖 **Leia o dossiê completo:** [página do projeto](https://SEU-USUARIO.github.io/renato/) — 18 seções
cobrindo a tese, a arquitetura, os protocolos, a segurança e o modelo de trabalho.

## O que está aqui — e o que não está

Este repositório **não é o Renato inteiro**. É o conceito completo + uma semente funcional:

| Aberto (aqui) | Em casa (não publicado) |
|---|---|
| O método e os protocolos | As 1.200+ skills indexadas |
| A arquitetura e as decisões | Os evals e o Selo da Casa de produção |
| Um starter MCP funcional mínimo | A memória acumulada (o acervo é de quem constrói o seu) |
| Os templates de artefatos | Segredos e chaves — **sempre** |

A ideia: você não clona o Renato — você **inicia o seu**. O caminho está mapeado;
a caminhada (e o acervo que ela gera) é sua.

## Comece em 5 minutos

```bash
cd starter
pip install -r requirements.txt
python -m pytest tests/ -q        # o starter nasce com teste passando (dogfooding)
python servidor_mcp.py            # sobe o servidor MCP via stdio
```

Depois conecte no seu IDE (Antigravity, VS Code, Cursor — qualquer um que fale MCP).
Instruções completas em [`starter/README.md`](starter/README.md).

## Os 5 conceitos que a semente demonstra

1. **Identidade injetada** — as regras da casa entram *dentro da conversa* do agente,
   via MCP; ele não precisa abrir arquivo nenhum.
2. **Roteamento determinístico** — a tarefa é classificada por keywords ponderadas,
   **zero LLM no caminho crítico**: mesmo pedido, mesmo método, sempre.
3. **Memória local** — SQLite + FTS5, com leak-scan na ingestão: credencial vira
   `[REDACTED]` antes de tocar o disco.
4. **Gate de evidência** — o `task_complete` recusa "pronto" sem saída real colada.
   "Funciona" é opinião; "esse comando roda e sai isso" é fato.
5. **Artefatos, não conversa** — contrato da tarefa, plano de teste e recibo de
   execução viram arquivos no projeto ([`starter/templates/`](starter/templates/)).

## Os protocolos (leitura recomendada, nesta ordem)

1. [Test-first como gate](docs/PROTOCOLO_TEST_FIRST.md) — teste antes do código, falha esperada antes da implementação
2. [Regra da Segunda Versão](docs/PROTOCOLO_SEGUNDA_VERSAO.md) — a v1 nunca é entregue
3. [Revisão adversarial](docs/PROTOCOLO_ADVERSARIAL.md) — 3 hipóteses de quebra testadas de verdade
4. [Guia de projeto novo](docs/GUIA_PROJETO_NOVO.md) — o dia zero: fundação antes de funcionalidade
5. [Guia do fluxo de deploy](docs/GUIA_FLUXO_DEPLOY.md) — do git ao container vigiado
6. [Guia de segurança](docs/GUIA_SEGURANCA.md) — defesa em profundidade para ferramenta local

## O caminho de evolução (depois da semente)

Quando o seu starter estiver rodando, a escada natural é:

1. **Evals por projeto** — casos `comando → saída esperada` que bloqueiam deploy se falharem
2. **Recall semântico** — embeddings + fusão RRF por cima do FTS5 (degrade para textual offline)
3. **Checkpoints como gates** — pre-code, pre-test, pre-commit recusando etapa pulada
4. **Selo do projeto** — nota A–F determinística, medida no tempo
5. **Colheita automática** — memória extraída ao concluir, sem depender de anotar

Cada degrau está descrito conceitualmente no [dossiê](https://SEU-USUARIO.github.io/renato/).

## Filosofia

O Renato nasceu de uma necessidade real: trabalho solo, várias empresas, e a urgência
de transformar velocidade de IA em software de verdade. Ele não nasceu para ser exclusivo.
Os segredos e as chaves ficam em casa — **o conhecimento, não**.

Use, adapte, melhore — e repasse.

## Licença

[MIT](LICENSE) — feito em português, no Brasil, com método brasileiro:
avaliação em vez de dogma, evidência em vez de juramento — e a porta aberta.
