# Guia do Fluxo — do código ao ar (git → Coolify → Contabo)

Para quem está começando. Este guia explica como tudo se interliga no nosso
fluxo de publicação: onde o código vive, onde o container roda, onde o banco
de dados mora e onde a informação fica guardada de verdade.

A ideia que resolve 90% da confusão:

> **Cada coisa mora num lugar diferente — e o container é descartável.**
> Container é gado, não bicho de estimação: morre e renasce a cada deploy.
> Tudo que precisa sobreviver mora FORA dele.

---

## Os 5 personagens (quem é quem)

### 1. A sua máquina (desenvolvimento)

Onde o código **nasce**. Você programa, roda em modo teste, tem o seu `.env`
local com segredos de teste. Nada que roda aqui afeta o que está no ar.

### 2. O Git (o cartório do código)

O repositório guarda o **histórico do código** — cada versão, pra sempre.

- O que vive no git: código, `Dockerfile`, `.env.example`, testes, README.
- O que **NUNCA** vive no git: `.env` real, senhas, banco de dados, uploads.
- Importante: o git **não roda nada**. É um arquivo histórico, um cartório.
  Fazer push não coloca nada no ar por si só — ele só avisa quem está ouvindo.

### 3. O Contabo (o computador alugado)

A VPS do Contabo é um **computador físico de verdade**, num datacenter na
Europa, ligado 24 horas por dia, com um endereço público na internet (IP).

Tudo que está "no ar" está, na real, **rodando dentro desse computador**.
"Nuvem" é isso: o computador dos outros, alugado.

### 4. O Coolify (o gerente de obras)

O Coolify é um **programa instalado dentro do Contabo**. Ele não é um lugar —
é um administrador que mora no servidor e faz o trabalho chato:

- fica **ouvindo o git**: quando você faz push, ele percebe;
- **constrói a imagem** da aplicação usando o Dockerfile;
- **derruba o container antigo e sobe o novo**;
- **injeta as variáveis de ambiente** (o `.env` real vive no painel dele);
- configura **domínio, HTTPS e o proxy** que direciona os visitantes;
- vigia o **healthcheck** pra saber se a aplicação está viva.

### 5. Docker: imagem e container (a caixa que roda)

- A **imagem** é a receita congelada: sistema + dependências + seu código,
  tudo empacotado (construída a partir do `Dockerfile`).
- O **container** é a receita em execução — a aplicação rodando de verdade.
- **O container é descartável.** A cada deploy, o antigo morre e um novo
  nasce da imagem nova. Qualquer arquivo salvo dentro dele **some**.

## O mapa (o que mora dentro do quê)

```
SUA MÁQUINA                    GIT (GitHub)              CONTABO (VPS)
┌──────────────┐   git push   ┌─────────────┐   puxa   ┌─────────────────────────────┐
│ código        │ ───────────> │ histórico   │ <─────── │  COOLIFY (gerente)          │
│ .env local    │              │ do código   │  avisa   │  ┌───────────────────────┐  │
│ banco de teste│              │ Dockerfile  │ ───────> │  │ PROXY (porta 80/443)  │  │
└──────────────┘              │ .env.example │          │  └───────┬───────────────┘  │
                              └─────────────┘          │          │                  │
                                                       │  ┌───────▼───────────────┐  │
        usuário ──── https://seuapp.com ────────────── │  │ CONTAINER da aplicação│  │
                     (chega no proxy, nunca            │  │ (descartável!)        │  │
                      direto no container)             │  └───────┬───────────────┘  │
                                                       │          │ rede interna     │
                                                       │  ┌───────▼───────────────┐  │
                                                       │  │ CONTAINER do banco    │  │
                                                       │  │   └── VOLUME ─────────┼──┼─> disco do
                                                       │  │  (a informação mora   │  │   Contabo
                                                       │  │   AQUI e sobrevive)   │  │
                                                       │  └───────────────────────┘  │
                                                       └─────────────────────────────┘
```

## A viagem do código (o que acontece num deploy)

1. **Você programa e commita** na sua máquina.
2. **`git push`** — o código vai pro repositório.
3. **O Coolify percebe** (webhook) e puxa o código novo pra dentro do Contabo.
4. **Constrói a imagem** seguindo o Dockerfile (instala dependências etc.).
5. **Troca os containers**: sobe o novo com as variáveis do painel injetadas,
   healthcheck confirma que está vivo, o antigo morre.
6. **O proxy aponta o domínio** pro container novo.
7. **O usuário acessa** `https://seuapp.com` → proxy → container da app →
   (rede interna) → container do banco → resposta volta.

Repare: você nunca "copia arquivos pro servidor" à mão. O git é o único
caminho de entrada do código. Editar direto no servidor é proibido — o
próximo deploy apaga.

## ONDE cada coisa fica guardada (a tabela que mata a dúvida)

| O quê | Onde vive | Sobrevive ao deploy? |
|---|---|---|
| Código | Git (+ cópia em cada máquina) | Sim |
| Segredos reais (.env) | Painel do Coolify (variáveis de ambiente) | Sim |
| Container da aplicação | Memória do Contabo, recriado a cada deploy | **NÃO** |
| **Dados do banco** | **Volume: pasta no disco do Contabo** | **Sim** |
| Uploads de usuários | Volume (SE você configurar um!) | Só com volume |
| Logs do container | Dentro do container | Não (por isso log externo) |
| Backup do banco | **Fora do Contabo** (outro lugar) | Sim — é o plano B |

A resposta curta pra "onde está a informação?": **num volume — uma pasta no
disco do Contabo que o Docker conecta pra dentro do container do banco.**
O container do banco pode morrer e renascer; o volume fica.

## Os 5 erros clássicos de quem está começando

1. **Salvar arquivo dentro do container** (upload, relatório gerado...) —
   some no próximo deploy. Solução: volume ou storage externo.
2. **SQLite dentro do container sem volume** — banco zerado a cada deploy.
   Em produção: Postgres em container próprio com volume.
3. **Commitar o `.env`** — segredo vai pro histórico do git pra sempre.
   O `.env` real vive no painel do Coolify.
4. **Editar código direto no servidor** — o próximo deploy sobrescreve.
   Todo caminho passa pelo git.
5. **"Funciona na minha máquina"** — o ambiente de verdade é o que o
   Dockerfile descreve. Se não está no Dockerfile, não existe em produção.

## Perguntas que o júnior sempre faz

**"Se o container morre a cada deploy, como o site não cai?"**
O Coolify sobe o novo antes de matar o antigo, e o healthcheck confirma que
o novo responde antes do proxy trocar o direcionamento.

**"O banco também é atualizado quando eu faço push?"**
Não! O push atualiza só o container da APLICAÇÃO. O container do banco e o
volume ficam intocados. (Mudanças de estrutura do banco são migrations, que
a aplicação roda ao subir.)

**"Por que não consigo acessar o banco pelo IP do servidor?"**
De propósito. O banco só escuta na rede interna do Docker — só a aplicação
fala com ele. Banco exposto na internet é o erro de segurança nº 1.

**"E se o Contabo pegar fogo?"**
Por isso backup **fora** do servidor. Volume protege contra deploy; backup
off-site protege contra desastre. São coisas diferentes.

---

## Resumo em uma frase

O código viaja (máquina → git → Coolify constrói → container roda),
os segredos moram no painel do Coolify, e **a informação mora no volume,
no disco do Contabo** — tudo que está fora desses lugares é descartável.

*Guia da casa Renatão — o fluxo completo de deploy está em
`RENATAO_WORKFLOW_PROTOCOL.md` e nos comandos `renatao coolify-*`,
`renatao ship-check` e `renatao postdeploy`.*
