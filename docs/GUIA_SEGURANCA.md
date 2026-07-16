# Guia de Segurança — a linha de raciocínio da casa

Para quem está começando a programar. Versão didática dos protocolos da casa
(Aegis, para escrever código seguro; ProdSec, para blindar o que já está no ar).

A ideia central:

> **Segurança não é auditoria no final — é hábito desde a primeira linha.**
> Consertar depois custa 100x mais que fazer certo agora. E a pergunta nunca é
> "será que alguém vai tentar?" — na internet, bots tentam TODO endereço
> público, todos os dias, sem exceção.

A postura mental: **toda entrada é hostil até prova em contrário** — o que vem
de formulário, de URL, de arquivo, de webhook e até de IA.

---

## Passo 1 — Antes de codar: conheça seus dados

Responda por escrito:

- O que **entra** no sistema? O que fica **guardado**? O que **sai**?
- Tem dado pessoal (nome, e-mail, CPF), financeiro, senha ou saúde?
- Se isso vazar amanhã, qual o tamanho do estrago?

Se tem dado pessoal/financeiro/credencial → é **alto risco** e todos os passos
abaixo deixam de ser opcionais. No Brasil, dado pessoal tem lei (LGPD).

## Passo 2 — Segredo nunca no código

A causa nº 1 de invasão de projeto iniciante: senha/chave de API commitada.

- Todo segredo vive em `.env` (que está no `.gitignore`) — nunca no código.
- O `.env.example` versionado mostra QUAIS variáveis existem, sem os valores.
- Segredo nunca aparece em log, em mensagem de erro, nem em print de debug.
- Vazou? **Rotacione na hora** (troque a chave) — apagar o commit não basta,
  o histórico do git lembra.

## Passo 3 — Nunca confie em entrada

- Valide **tamanho, tipo e formato** de tudo que chega, no backend.
- Banco de dados: **sempre query parametrizada** (ou ORM). Nunca monte SQL
  colando texto do usuário — é assim que nasce SQL injection.
- Upload de arquivo: limite de tamanho, lista de extensões permitidas,
  guardado fora da pasta do código.
- O frontend valida para ajudar o usuário; o **backend valida para se defender**.
  Só a validação do backend conta.

## Passo 4 — Autorização no backend, testada no "não"

- Esconder o botão não é segurança: a pergunta "esse usuário PODE fazer isso
  com ESTE recurso?" é respondida no servidor, a cada requisição.
- Nunca confie em flag vinda do cliente ("admin: true" no request é piada).
- Se o sistema tem clientes/empresas separadas: **todo** filtro de banco leva
  o dono junto — senão o cliente A lê os dados do B.
- E o teste que quase ninguém escreve: **teste o acesso NEGADO** (anônimo,
  logado sem permissão, dono errado). O caminho feliz todo mundo testa.

## Passo 5 — Senhas e criptografia: nunca invente

- Senha de usuário nunca é guardada — guarda-se o **hash** (bcrypt ou
  Argon2). MD5/SHA1 para senha é vulnerabilidade, não proteção.
- Criptografia é sempre de **biblioteca madura** — algoritmo próprio é o
  erro clássico de quem está começando.
- HTTPS/TLS em tudo que está no ar. Sem exceção, nem "só no admin".

## Passo 6 — Erros que não entregam o mapa

- Mensagem de erro **externa** é genérica: "não foi possível processar".
- O detalhe técnico (stack trace, query, caminho de arquivo) vai pro **log
  interno** — stack trace na tela é mapa do tesouro pro atacante.
- Log interno tem contexto (o quê, onde, com que entrada) mas **nunca**
  senha, token ou dado pessoal.

## Passo 7 — Dependências são código seu

Quando você instala uma biblioteca, o código dela roda com os mesmos poderes
do seu.

- Prefira bibliotecas populares e mantidas (última atualização recente).
- Rode o scanner da sua stack de tempos em tempos e antes de todo deploy:
  `pip-audit` (Python), `npm audit` (Node).
- Use lockfile (requirements fixado, package-lock) — versão surpresa é risco.

*(Foi assim que encontramos 18 vulnerabilidades num frontend da casa — sem o
scanner, invisíveis.)*

## Passo 8 — Em produção: feche tudo, abra o mínimo

- **Portas fechadas por padrão** — só 80/443 (web) abertas pro mundo.
- **Banco de dados NUNCA escuta no IP público** — só a aplicação fala com ele,
  pela rede interna.
- Container roda como usuário **non-root**, com healthcheck.
- **Rate limit** em login, cadastro e "esqueci a senha" — mata força bruta.
- MFA (dois fatores) em todo painel administrativo (hospedagem, domínio, cloud).
- **Backup fora do servidor** e **testado**: backup que nunca foi restaurado
  é fé, não backup.
- Logue as falhas de login; ferramentas como Fail2ban banem quem fica tentando.

## Bônus — Trabalhando com IA

- Resposta de IA é **entrada não confiável** como qualquer outra: valide antes
  de executar, nunca rode comando sugerido sem entender.
- Nunca cole segredo em chat de IA.
- Peça pra IA revisar segurança do próprio código dela ("tente quebrar isso")
  — ela acha coisa que deixou passar ao escrever.

---

## Os 5 inegociáveis da segurança

1. **Segredo nunca no código** — `.env` + rotação imediata se vazar.
2. **Toda entrada é hostil** até validada no backend.
3. **Autorização no servidor, testada no "não"** — esconder botão não conta.
4. **Banco nunca exposto na internet** — rede interna, sempre.
5. **Backup fora do servidor e restaurado de teste** — senão é fé.

---

*Versão didática dos protocolos da casa Renatão — completos em
`SECURITY_PROTOCOL.md` (Aegis) e `RENATAO_PRODSEC_PROTOCOL.md` (ProdSec).
Na casa: `renatao security --task "..."` e `renatao prodsec --task "..."`.*
