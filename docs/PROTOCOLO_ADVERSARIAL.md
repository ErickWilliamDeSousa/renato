# Protocolo: Revisão adversarial

## A tese

**O autor jura. O adversário acha.** Quem acabou de fazer um trabalho é a
pior pessoa para julgá-lo — está no modo "defender", não no modo "quebrar".
A revisão adversarial é a troca de papel institucionalizada.

## O ritual

Antes de considerar qualquer trabalho terminado:

1. **Escreva 3 hipóteses de como pode estar quebrado.** Concretas:
   - entrada vazia / nula / gigante quebra?
   - funciona só na minha máquina (caminho, encoding, dependência local)?
   - quebrou algo antigo que ninguém rodou de novo?
2. **Teste cada hipótese DE VERDADE** — rode o comando, provoque o caso,
   cole a saída. Hipótese não testada é decoração.
3. **Registre o resultado das 3** — inclusive as que passaram.

Se a revisão não achou nada, **desconfie da revisão** — hipóteses fracas
demais são a forma educada de não revisar.

## A caça ao falso-feito

Assinaturas conhecidas de trabalho que parece pronto e não está:

- Sucesso declarado **sem saída colada** ("rodei e funcionou")
- **Teste que não testa** (não falharia se o código estivesse errado)
- `except: pass` e afins — erro engolido é bug agendado
- v1 entregue **sem crítica** (viola a Segunda Versão)
- Reclassificação para baixo depois de pronto ("pensando bem, era trivial")

## Lente de produto (quando há interface)

Além de "está correto?", pergunte "alguém consegue usar?":
- O primeiro uso funciona **sem manual**?
- As mensagens de erro **ensinam** o que fazer?
- O estado vazio **orienta** em vez de assustar?

## Como virar mecanismo

Acione a revisão automaticamente nos momentos de maior risco: todo deploy,
toda mudança em código crítico, todo "pronto" de tarefa relevante. Revisão
que depende de alguém lembrar é revisão que não acontece na semana cheia.
