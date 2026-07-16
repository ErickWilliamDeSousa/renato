# AGENTS.md — o manual que viaja com o repo

Regras da casa para qualquer agente (ou humano) que chegar neste projeto:

1. **Aceite como contrato** — antes da primeira linha: qual comando vou rodar
   e que saída espero ver? Preencha `GSD_TASK.md`.
2. **Test-first** — teste antes do código; veja falhar pelo motivo esperado
   (`TEST_FIRST_PLAN.md`), então implemente a menor mudança.
3. **Segunda Versão** — código relevante nunca entrega a v1:
   v1 → 3 críticas concretas → reescrita v2, trilha no recibo.
4. **Evidência antes de "pronto"** — cole a saída real em `EXECUTION_RECEIPT.md`.
5. **Revisão adversarial** — 3 hipóteses de quebra testadas de verdade antes de aprovar.
6. **Segredo nunca no código** — `.env` + `.env.example`, sempre.

> Desobedecer deve dar mais trabalho que obedecer. Se alguma regra daqui está
> sendo pulada com frequência, o problema não é disciplina — falta um gate.
