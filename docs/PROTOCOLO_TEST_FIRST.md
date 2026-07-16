# Protocolo: Test-first como gate, não como conselho

## A regra

Nenhum código de produção nasce antes do teste. O ciclo, sem atalho:

1. **Escreva o teste** — antes de qualquer linha de implementação.
2. **Rode e confirme a falha pelo motivo esperado** — se falhou por outro
   motivo, pare: você não entendeu o problema ainda.
3. **Implemente a menor mudança** que faz o teste passar.
4. **Rode de novo → verde** — e guarde a saída real como evidência.

## Por que "pelo motivo esperado" importa

Um teste que falha por import quebrado, fixture errada ou typo não prova nada
sobre o comportamento que você quer construir. A falha esperada é o único
momento em que você verifica que **o teste testa o que você acha que testa**.
Pular essa confirmação é a origem do "teste que não testa" — a pior classe de
falso-feito, porque dá confiança sem dar cobertura.

## Como virar mecanismo (a escada de enforcement)

| Nível | Como fica |
|---|---|
| Documento | este arquivo — necessário, insuficiente |
| Artefato | `TEST_FIRST_PLAN.md` preenchido antes de codar (template no starter) |
| Gate | a conclusão da tarefa exige prova de suíte verde **recente** — relatório velho não prova que os testes rodaram para ESTA tarefa |
| Verificação automática | CI recusa merge sem testes novos tocando o código mudado |
| Métrica | % de tarefas com trilha test-first completa, medida no tempo |

## Exceções honestas

- **Spike/exploração**: código descartável para aprender não precisa de teste —
  mas é descartável de verdade: não vira produção por promoção silenciosa.
- **Emergência em produção**: conserta primeiro; o teste que teria pegado o
  problema vira follow-up imediato e registrado.

> Sem teste falhando primeiro, não há implementação.
