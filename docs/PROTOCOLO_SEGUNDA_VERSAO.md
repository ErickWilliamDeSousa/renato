# Protocolo: Regra da Segunda Versão

## A tese

**A primeira versão que funciona ancora o pensamento.** Quem escreveu a v1 —
humano ou IA — passa a defendê-la em vez de questioná-la. A regra quebra a
âncora por construção: a v1 nunca é entregue.

## A regra, por classificação

Antes da primeira linha, classifique a tarefa (e registre — reclassificar
para baixo depois de pronto é assinatura de falso-feito):

- **Trivial** (typo, texto, config): fora da regra. Siga em frente.
- **Relevante** (qualquer lógica — o default): **v1 → 3 críticas concretas →
  reescrita v2**. Na dúvida, é relevante.
- **Crítico** (auth, pagamento, dados, segurança): **torneio de 3 abordagens**
  partindo de ângulos declarados antes (ex.: simplicidade, robustez,
  performance), julgadas por tabela — correção, simplicidade, testabilidade,
  risco. A vencedora herda o melhor das perdedoras, e ainda passa pela
  crítica e reescrita.

## Por que reescrever 1x com crítica em vez de refazer 5x

Refazer do zero repetidas vezes tende a produzir variações da mesma ideia —
a IA regride à abordagem mais provável dela; o humano, à mais confortável.
O ganho real vem de **pontos de partida diferentes + julgamento explícito**,
não de repetição. Três críticas concretas forçam a troca de papel: de autor
para adversário.

## O que é uma crítica concreta

Não vale "poderia ser mais limpo". Vale: "a função X não trata entrada vazia",
"este loop refaz a query N vezes", "o nome do parâmetro mente sobre o tipo".
Crítica concreta aponta **onde** e **o que quebra ou confunde**.

## A trilha no recibo

Toda tarefa relevante registra no recibo de execução: o que a v1 fazia,
as 3 críticas, o que mudou na v2. **Reescrever é repensar, não renomear** —
uma v2 que só troca nomes de variáveis é a v1 com disfarce.

## Exceções honestas

- Emergência em produção: conserta primeiro; a v2 vira follow-up imediato registrado.
- Código gerado por scaffold/template da casa: já passou pela regra na origem.
