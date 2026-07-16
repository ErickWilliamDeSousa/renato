# Artefatos — o método não mora na conversa: vira arquivo no projeto

Conversa evapora; **arquivo fica, versiona e audita**. Cada gate do Renato lê um
artefato — nunca a boa intenção de quem escreveu. Todos são texto puro
(markdown/JSON), legíveis por humano e por máquina, dentro do próprio repositório.

## A papelada que trabalha (`.renatao/` no seu projeto)

| Artefato | O que registra |
|---|---|
| `GSD_TASK.md` | o contrato da tarefa: objetivo + critério de aceite (comando → saída esperada) |
| `TEST_FIRST_PLAN.md` | o teste planejado antes do código — e a falha esperada dele |
| `EXECUTION_RECEIPT.md` | o recibo: saída real colada; template em branco é recusado |
| `FULL_TEST_RUN` | prova de suíte verde com carimbo de tempo — relatório velho não vale |
| `ADVERSARIAL_REVIEW` | as 3 hipóteses de quebra e o resultado real de cada uma |
| `DECISIONS.md` | decisões de stack e arquitetura com o porquê e as alternativas descartadas |
| `EVALS.jsonl` | os casos comando → saída que vigiam o projeto a cada mudança |
| `SEAL_HISTORY.jsonl` | a série temporal da nota A–F — a direção importa mais que a foto |
| `AGENTS.md` | o manual que viaja com o repo: regras da casa para qualquer agente que chegar |

Templates prontos para copiar: [`starter/templates/`](../starter/templates/)

## Dois níveis, uma lógica

**Por projeto**, o `.renatao/` guarda o que pertence àquele código: contratos,
recibos, decisões, evals, selo. Quem clona o repositório leva o contexto junto —
inclusive um agente novo, de outra ferramenta, meses depois.

**Na casa**, o cérebro central guarda o que atravessa projetos: memória, skills,
protocolos, histórico. A fronteira é deliberada: o que é do projeto viaja com o
projeto; o que é da casa (e os segredos) **não sai dela**.

## Auditoria sem arqueologia

Seis meses depois, "por que escolhemos isso?" se responde com um arquivo — não com
a memória de quem já saiu do projeto. O custo é minutos por tarefa; a alternativa é
reconstruir contexto por horas, ou decidir de novo no escuro.
