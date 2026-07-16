# Leve para o seu time — o método sem a ferramenta

O Renato é a **automação** do método — mas o método funciona à mão, hoje, sem
instalar nada. A escada de adoção que a casa recomenda:

## Uma prática por semana

| Quando | Prática | Como |
|---|---|---|
| **Semana 1** | Aceite como contrato | antes de cada tarefa: *qual comando vou rodar e que saída espero?* Escreva — 2 minutos que matam o "funciona na minha máquina" |
| **Semana 2** | Test-first no que importa | teste antes do código em toda lógica nova; veja **falhar pelo motivo esperado** antes de implementar |
| **Semana 3** | Evals do projeto | 5 casos **comando → saída esperada** num arquivo; rode todos antes de qualquer deploy |
| **Semana 4** | Revisão adversarial | 3 hipóteses de como pode estar quebrado, **testadas de verdade**, antes do "pronto" |
| **Mês 2** | Segunda versão + selo mensal | reescrita crítica no código relevante; nota A–F por checklist, uma vez por mês |

## A regra de ouro da adoção

**Uma prática por vez** — quatro mudanças simultâneas morrem juntas na primeira
semana cheia. E cada prática precisa subir a escada de enforcement do time:

- o **aceite** vai para o template do PR;
- os **evals** vão para o CI;
- o **selo** vira uma reunião mensal de 15 minutos com checklist.

Documento que não bloqueia nada volta a ser conselho — **e conselho se esquece**.
A pergunta de cada semana é sempre a mesma: *"o que impede, mecanicamente, de pular
esta etapa?"* Enquanto a resposta for "boa vontade", o trabalho não terminou.

## O que é aberto · o que fica em casa

Abertos: os protocolos, a arquitetura, o método e as lições — inclusive os erros.
Em casa: segredos, chaves e a memória. **Use, adapte, melhore — e repasse.**
Se uma ideia daqui melhorar o jeito do seu time construir software, o projeto já
cumpriu o propósito.
