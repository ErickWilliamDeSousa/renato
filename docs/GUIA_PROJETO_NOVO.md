# Guia de Projeto Novo — a linha de raciocínio da casa

Para quem está começando a programar. Este é o procedimento que usamos em
todo projeto novo, com o porquê de cada passo. A ideia central é uma só:

> **"Funciona" é opinião. "Esse comando roda e sai isso" é fato.**
> Todo o procedimento existe para transformar opinião em fato o mais cedo possível.

A segunda ideia: **conselho escrito se esquece; mecanismo sobrevive.** Por isso
cada passo aqui tem uma ferramenta ou um registro — não dependemos de memória
nem de força de vontade.

---

## Passo 1 — Pense antes de digitar (as 5 perguntas)

Nenhum arquivo de código nasce antes de responder por escrito:

1. **O que é?** API, site, app completo, ferramenta de linha de comando?
2. **Quem usa?** Pessoa de verdade (tela), outro sistema (API) ou só você (script)?
3. **Onde roda?** Vai pro ar (deploy) ou é só local?
4. **Que dados guarda?** Precisa de banco? Precisa de login?
5. **O que fica DE FORA da primeira versão?** (a pergunta mais importante —
   sem escopo negativo, todo projeto incha e nunca termina)

Se não sabe responder, ainda não é hora de codar — é hora de perguntar.

## Passo 2 — Escolha a tecnologia por avaliação, não por moda

Não existe "a linguagem certa"; existe a certa PARA ESTE caso. Compare no
mínimo 2 opções olhando:

- **Requisitos**: precisa de tempo real? SEO? muito volume?
- **Ecossistema**: a melhor ferramenta pro seu domínio vive em qual linguagem?
  (e-commerce maduro → PHP/Laravel; dados → Python; realtime → Node/Go)
- **Hospedagem**: roda onde você consegue publicar?
- **Manutenção**: quem vai manter conhece? é fácil achar quem conheça?
- **Prazo**: o que entrega a primeira versão mais rápido sem hipotecar o futuro?

**Escreva o comparativo e o porquê da escolha** (aqui registramos em
`DECISIONS.md`). Não é burocracia: daqui a 6 meses você não vai lembrar por
que escolheu — e vai querer trocar pela moda do momento sem motivo real.

## Passo 3 — Use a estrutura que a comunidade já validou

Não invente layout de pastas. Toda stack madura tem uma estrutura oficial
(o scaffold do Laravel, o src-layout do Python, o padrão do Vite). Estrutura
inventada é a primeira coisa que confunde quem chega depois — inclusive você.

Exemplo (API em Python):

```
projeto/
  app/
    main.py        # ponto de entrada
    config.py      # configuracao via ambiente
    routers/       # um arquivo por assunto
    services/      # regra de negocio
  tests/           # espelha o codigo
  .env.example     # variaveis SEM valores reais
  Dockerfile
  README.md
```

## Passo 4 — O "dia zero": fundação antes de qualquer funcionalidade

Nesta ordem, num projeto novo:

1. `git init` + `.gitignore` — histórico desde o primeiro arquivo.
2. Estrutura de pastas (vazia mesmo).
3. `README.md` — o que é, como rodar, como testar.
4. `.env.example` — todo segredo/configuração fora do código, desde já.
5. Ambiente da linguagem (venv, npm install...).
6. **Primeiro teste passando** — um "smoke": o app importa e responde.
7. Primeiros **evals** — 3 a 5 casos "rodo este comando → espero esta saída".
8. Commit inicial.

**Funcionalidade só começa depois do item 8.** Parece lento; é o contrário —
cada um desses itens custa minutos hoje e horas se deixar pra depois.

Na casa, um comando faz tudo isso de uma vez:

```powershell
renatao scaffold --tipo api --nome meu-projeto --decisao "FastAPI vs Express: FastAPI porque ..."
```

## Passo 5 — Desenvolva com contrato

Para cada tarefa:

1. **Critério de aceite antes da primeira linha**: qual comando vou rodar e
   que saída espero ver quando estiver pronto?
2. **Teste antes do código**: escreva o teste, veja falhar, então implemente.
3. **Lotes pequenos**: uma mudança verificável por vez, commit a cada uma.
4. **Evidência antes de "pronto"**: rode o critério de aceite e guarde a
   saída real. Se não rodou, não está pronto — está torcendo.

## Passo 6 — Revise como adversário

Antes de considerar terminado, troque de papel: pare de defender o que fez e
tente QUEBRAR. Escreva 3 hipóteses de como pode estar errado (entrada vazia?
funciona só na sua máquina? quebrou algo antigo?) e teste cada uma de
verdade. Se a revisão não achou nada, desconfie da revisão.

Na casa: `renatao adversary --task "revisar X" --write`.

## Passo 7 — Publique com verificação real

- Container com **healthcheck** (a hospedagem precisa saber se o app está vivo).
- **Dependências auditadas** (uma biblioteca vulnerável entra de graça).
- Depois do deploy, **bata no endpoint de verdade** e guarde a resposta —
  deploy "que passou" não é deploy verificado.

Na casa: `renatao deps-audit`, `renatao ship-check`, `renatao postdeploy --url`.

## Passo 8 — Meça e melhore

Uma nota por projeto (aqui, o **Selo da Casa**, A-F) agregando: tem testes?
evals verdes? README? dependências limpas? healthcheck? sem segredo no
código? A nota só sobe com mecanismo, não com promessa — e o que importa é a
direção ao longo do tempo.

---

## Os 5 inegociáveis (se lembrar de uma coisa, lembre destas)

1. **git desde o dia zero** — sem histórico, todo erro é permanente.
2. **teste desde o dia zero** — sem teste, toda mudança é aposta.
3. **segredo nunca no código** — `.env` + `.env.example`, sempre.
4. **README com como rodar** — o próximo a chegar é você em 6 meses.
5. **evidência antes de "pronto"** — comando + saída, ou não aconteceu.

---

*Gerado pela casa Renatão — protocolos completos em
`RENATAO_PROJECT_STRUCTURE_PROTOCOL.md` e `RENATAO_AI_CRAFT_PROTOCOL.md`.*
