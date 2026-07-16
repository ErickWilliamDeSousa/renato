# Manifesto — o que a gente acredita *e mecaniza*

Cada frase abaixo nasceu de um erro real e virou **regra executável**. Nenhuma é
decoração: todas têm um gate, um checklist ou um teste por trás.

---

### *"Funciona" é opinião. "Esse comando roda e sai isso" é fato.*
**Critério de aceite como contrato.** Antes da primeira linha: qual comando vou rodar
e que saída espero ver? Ao final, a saída real é colada no recibo — e a conclusão é
bloqueada com recibo em branco.

### *Conselho se esquece. Mecanismo sobrevive.*
**A escada de enforcement.** Documento → artefato → gate → verificação automática →
métrica no tempo. Toda regra da casa é empurrada o mais para a direita possível.

### *A primeira versão que funciona ancora o pensamento. A v1 nunca é entregue.*
**Regra da Segunda Versão.** Todo código relevante segue v1 → 3 críticas concretas →
reescrita v2, com trilha registrada. Crítico exige torneio de 3 abordagens.

### *O autor jura. O adversário acha.*
**Revisão adversarial.** Trocar de papel: 3 hipóteses de como pode estar quebrado,
testadas de verdade. Se a revisão não achou nada, desconfie da revisão.

### *Container é gado, não bicho de estimação — o que precisa sobreviver mora fora dele.*
**Guia do fluxo de deploy.** Dados em volume, segredos no painel, backup fora do
servidor. O container morre e renasce a cada deploy — por design.

### *Backup que nunca foi restaurado é fé, não backup.*
**Verificação de integridade.** Todo backup do cérebro passa por restauração de teste
e rotação. Fé não recupera banco de dados.

### *A nota só sobe com mecanismo — nunca com promessa.*
**Selo da Casa.** Nota A–F determinística por projeto (testes? evals? README?
dependências limpas? segredos fora do código?), medida em série temporal. A direção
importa mais que a foto.

### *Avaliação, não dogma: se PHP for a melhor saída, PHP vence.*
**Decisão de stack registrada.** Não existe "a linguagem certa"; existe a certa PARA
ESTE caso. Mínimo 2 opções comparadas, porquê registrado em `DECISIONS.md`.

---

## Aconteceu de verdade: a regra que pediu a própria regra

Quando a Regra da Segunda Versão foi implantada, a primeira versão da implantação
parecia completa — e foi auditada adversarialmente antes do "pronto". Resultado:
**6 caminhos sem a regra**, incluindo o principal (o canal MCP que o agente do IDE
realmente usa). A v1 foi criticada e reescrita. A regra exigiu a própria segunda
versão — e provou o próprio ponto.
