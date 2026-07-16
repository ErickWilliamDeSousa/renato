# Segurança — cada ameaça mapeada tem uma camada com nome

Uma ferramenta local com acesso a shell e memória persistente exige **desconfiança
por padrão**. Cada risco vira um mecanismo — e o que não dá para proteger de verdade,
o sistema **recusa** em vez de fingir.

## Defesa em profundidade

| # | Ameaça | Camada | Tipo |
|---|---|---|---|
| 1 | segredo entrando no acervo | leak-scan na ingestão: credencial vira **[REDACTED]** antes de tocar o disco | GATE |
| 2 | segredo saindo em público | segredos fora do git + varredura de vazamento no ship-check | GATE |
| 3 | comando destrutivo no shell | jail com sandbox de SO quando existe; **sem sandbox real, recusa rodar por padrão** — não finge proteger | RECUSA |
| 4 | injeção de prompt | texto vindo de fora (páginas, arquivos, saídas) é **sanitizado** antes de entrar em qualquer prompt | GATE |
| 5 | URL maliciosa ou interna | toda URL de saída passa por validação anti-SSRF | GATE |
| 6 | API externa em falha | **circuit breaker**: para de insistir quando a API cai, reabre sozinho | auto |
| 7 | custo fugindo do controle | **teto diário de custo** + limite de ações/hora; estourou, chamadas pagas bloqueiam | GATE |
| 8 | perda do cérebro | backup com **verificação de integridade** e rotação | GATE |

## Honestidade também é camada: fail-open documentado

Sem a biblioteca de confiabilidade instalada, as ferramentas locais seguem
funcionando **e avisam** — disponibilidade escolhida conscientemente para ferramenta
local, com o risco por escrito. Segurança que finge é teatro; aqui, cada exceção tem
nome, motivo e log.

> O conceito da camada 1 funcionando: [`starter/memoria.py`](../starter/memoria.py)
> (função `redigir` — o leak-scan roda ANTES da gravação, sempre)

## Para o seu projeto (o essencial)

O [Guia de segurança](GUIA_SEGURANCA.md) cobre o básico que evita a causa nº 1 de
invasão de projeto iniciante: `.env` + `.env.example`, hash de senha (bcrypt/Argon2,
nunca MD5/SHA1), rate limit em login, e dependências auditadas.
