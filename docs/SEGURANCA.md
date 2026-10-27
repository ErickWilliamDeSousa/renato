# Segurança — cada ameaça mapeada tem uma camada com nome

Uma ferramenta local com acesso a shell e memória persistente exige **desconfiança
por padrão**. Cada risco vira um mecanismo — e o que não dá para proteger de verdade,
o sistema **recusa** em vez de fingir.

## Defesa em profundidade

| # | Ameaça | Camada | Tipo |
|---|---|---|---|
| 1 | segredo entrando no acervo | leak-scan na ingestão: credencial vira **[REDACTED]** antes de tocar o disco | GATE |
| 2 | segredo saindo em público | segredos fora do git + varredura de vazamento no ship-check | GATE |
| 3 | comando destrutivo no shell | pré-checagem (`LIBERADO`/`BLOQUEADO`) de padrões perigosos, `.env`/`.ssh` e caminho fora do workspace — **não executa e não se diz sandbox**: o comando roda no terminal do editor, sob os olhos do usuário | GATE |
| 4 | injeção de prompt | texto vindo de fora (páginas, arquivos, saídas) é **sanitizado** antes de entrar em qualquer prompt | GATE |
| 5 | URL maliciosa ou interna | toda URL de saída passa por validação anti-SSRF | GATE |
| 6 | API externa em falha | **circuit breaker**: para de insistir quando a API cai, reabre sozinho | auto |
| 7 | custo fugindo do controle | **teto diário de custo** + limite de ações/hora; estourou, chamadas pagas bloqueiam | GATE |
| 8 | perda do cérebro | backup com **verificação de integridade**, rotação e espelho em segundo disco | GATE |
| 9 | segredo saindo pela resposta de uma tool | **redação na SAÍDA** de toda tool, inclusive mensagens de erro — padrões de alta precisão, que preservam hashes de prova | GATE |
| 10 | memória envenenada dando ordens | memória, handoff e arquivos entram como `<dados-nao-confiaveis>`; a tag de fechamento é neutralizada por dentro | GATE |
| 11 | servidor travado por subprocess | todo filho nasce com `stdin=DEVNULL`, sem shell e com teto de parede que mata a árvore | GATE |

As camadas 9 a 11 vieram de incidentes reais de 2026, contados em
[Lições de servidor MCP stdio](LICOES_MCP_STDIO.md).

## Laudo de segurança com validade documental

No Renato completo, a conclusão de um projeto pode emitir um **laudo**:
bateria de scanners (análise estática, segredos no código **e no histórico
git**, dependências vulneráveis, SBOM), carimbo de tempo RFC 3161 e um
**Selo de Fonte** — manifesto sha256 de cada arquivo mais o hash da árvore
git, que prova *qual versão* foi auditada e detecta alteração depois.
Ferramenta só entra na bateria depois de medida: uma alternativa popular foi
reprovada por número, não por opinião. O laudo roda sob demanda, fora da
chamada MCP (ver regra 5 das lições).

## Honestidade também é camada: fail-open documentado

Sem a biblioteca de confiabilidade instalada, as ferramentas locais seguem
funcionando **e avisam** — disponibilidade escolhida conscientemente para ferramenta
local, com o risco por escrito. Segurança que finge é teatro; aqui, cada exceção tem
nome, motivo e log.

> O conceito funcionando na semente:
> - camada 1: [`starter/memoria.py`](../starter/memoria.py) (função `redigir` — o leak-scan roda ANTES da gravação, sempre)
> - camadas 9 a 11: [`starter/protecao.py`](../starter/protecao.py) (`redigir_saida`, `nao_confiavel`, `rodar`), aplicadas a toda tool pelo decorador `blindar` do servidor

## Para o seu projeto (o essencial)

O [Guia de segurança](GUIA_SEGURANCA.md) cobre o básico que evita a causa nº 1 de
invasão de projeto iniciante: `.env` + `.env.example`, hash de senha (bcrypt/Argon2,
nunca MD5/SHA1), rate limit em login, e dependências auditadas.
