# Deep-dive de engenharia — como e por quê

> Companion técnico da [ARQUITETURA.md](ARQUITETURA.md). Lá está o **o quê** em
> linguagem de conceito; aqui está o **como** e o **por quê**, para quem vai
> avaliar, estender ou reimplementar. Vale o método da casa: cada decisão vem
> com o trade-off explícito, nada de "confia".
>
> O `starter/` é a implementação mínima **executável** deste desenho. A versão
> de produção (privada) é o mesmo desenho em escala.

## 1. Os três déficits que nenhum prompt resolve

Agentes de IA em IDE têm problemas estruturais que instrução no prompt não cura:

1. **Amnésia** — cada sessão nasce do zero; decisões e convenções se perdem
   entre conversas e entre repositórios.
2. **Método não-executável** — o agente *sabe* boas práticas, mas nada o
   *obriga* a segui-las sob prazo. Vira sugestão opcional.
3. **Não-determinismo no processo** — o mesmo pedido pode gerar dois fluxos
   diferentes. Ótimo para *gerar código*, inaceitável para *garantir processo*.

A tese: **empurrar cada prática na escada de enforcement** — de documento (se
esquece) a mecanismo que roda sozinho (sobrevive).

```
documento → artefato → gate → verificação automática → métrica no tempo
```

## 2. Núcleo único, dois transportes

- **Servidor MCP (stdio)** — injeta contexto e expõe ferramentas *dentro da
  conversa* do agente do editor.
- **CLI determinística** — o mesmo núcleo por linha de comando, para humanos,
  hooks de CI e scripts.

O núcleo é o mesmo objeto chamado pelos dois. Trocar de transporte não muda uma
regra — e é por isso que gates são funções puras (§4).

## 3. Roteamento determinístico — a decisão contra-intuitiva

Classificar a tarefa por **keywords ponderadas** (soma decide o domínio), com
**zero LLM** no caminho crítico. O porquê, explícito:

- **Reprodutibilidade** — mesmo input, mesmo método, sempre. Processo não pode
  ser probabilístico.
- **Auditabilidade** — revisar o roteamento é ler uma tabela de pesos
  (`DOMINIOS`), não interrogar um modelo. O diff de comportamento é um diff de
  dados.
- **Custo e latência zero** — sem chamada de rede no caminho crítico.

A criatividade fica onde deve: no código gerado, nas abordagens do torneio da
Segunda Versão. O checklist de aviação não é criativo de propósito.

**Bug real que a fronteira de palavra pegou:** o matching usa `\b` + prefixo,
não substring crua. Sem isso, `"reiniciar o servidor"` casaria `"iniciar"` e
rotearia para *projeto novo* em vez de *deploy*. O prefixo em fronteira preserva
flexões do português (`"revisar"` ainda casa `"revisarmos"`) sem o falso
positivo. Travado por `test_roteador_nao_casa_termo_dentro_de_palavra`.

## 4. Gates como funções puras

Um gate é `entrada → (veredito | None)`. Só isso — e isso é o design:

- **Testável** isolado, sem subir servidor nem mockar MCP.
- **Portável** — o mesmo gate roda no MCP, na CLI e num hook de CI.
- **Auditável** — a razão de uma recusa é uma string determinística.

`task_complete` recusa recibo em branco ou com marca de template. "Funciona" é
opinião; "esse comando roda e sai isso" é fato colado no recibo.

## 5. Memória: leak-scan na ingestão + recall híbrido

O starter usa **FTS5 puro** (busca léxica). Produção soma um índice semântico e
funde os rankings com **RRF** (Reciprocal Rank Fusion):

```
score(doc) = Σ  1 / (k + rank_i(doc))     para cada índice i ∈ {léxico, vetorial}
```

O léxico acha o **termo exato** (`"coolify"`, nome de função); o semântico acha
o **conceito** (`"app caiu depois do deploy"` encontra `"healthcheck falhou"`).
RRF dispensa calibração frágil de pesos: quem ranqueia bem nos dois, sobe.

**Boundary de ingestão é um gate.** O leak-scan roda **antes** de qualquer
gravação: credencial vira `[REDACTED]` antes de tocar o disco. Padrões cobrem
AWS, GitHub (clássico e fine-grained), Slack, `Bearer`, `sk-…` e o par
`chave: valor`.

**Honestidade sobre dados:** acervo, índices, segredos e backups ficam na
máquina. Para gerar o vetor, o texto da memória viaja a uma API de embedding —
mas só **depois** do leak-scan. Sem chave ou sem internet, o recall degrada para
léxico puro: menos esperto, **nunca quebrado** (fail-open documentado).

## 6. Fluxo de uma tarefa

```
session_start(tema)  ──► IDENTIDADE + recall(tema)                 [contexto]
iniciar_tarefa(desc) ──► classificar() → PACOTES[domínio]          [método cobrado]
   ── agente: escreve teste → vê falhar → implementa ──
task_complete(resumo, evidência)
   └─► gates.validar_evidencia(evidência)                          [GATE]
        ├─ recusa → agente cola a saída real
        └─ aceita → memoria.gravar(lição)                          [colheita]
```

A colheita alimenta o próximo `session_start` — o sistema aprende com o que foi
concluído, sem depender de alguém anotar.

## 7. Do starter ao Renato de produção

O starter é semente honesta (conceito rodando, não demo de fachada). A escada de
evolução — cada degrau é mecanismo, não conselho:

1. **Colheita estruturada** — decisões tipadas de cada `task_complete`.
2. **Evals por projeto** — casos `comando → saída` em `EVALS.jsonl` que
   **bloqueiam deploy** se falharem.
3. **Checkpoints reais** — pre-code, pre-test (falha esperada + janela de
   tempo), pre-commit (trilha v1→v2).
4. **Recall semântico** — índice vetorial + RRF (§5).
5. **Selo A–F** — determinístico, série temporal (a direção > a foto).
6. **Skills sob demanda** — acervo indexado por relevância.

Não migra para o público, por decisão: skills de produção, acervo de memória,
evals internos, segredos. Método aberto; a casa é da casa.

## 8. Decisões e trade-offs

| Decisão | Alternativa rejeitada | Por quê |
|---|---|---|
| Roteamento por keywords | classificador LLM | reprodutibilidade + custo/latência zero + auditabilidade |
| SQLite + FTS5 | Postgres/serviço de busca | zero dependência externa; offline; FTS5 embutido |
| RRF para fundir rankings | pesos manuais léxico/semântico | robusto sem calibração; degrada bem |
| Gates como funções puras | validação acoplada ao handler | testável, portável entre transportes |
| Leak-scan na **ingestão** | scan só na saída | credencial nunca toca o disco em texto |
| Fail-open documentado | fail-closed | ferramenta local não trava por falta de lib; risco por escrito |
| MCP como canal primário | plugin proprietário por IDE | um protocolo, N editores |

## 9. Estender (contrato de contribuição ao método)

- **Domínio de roteamento**: entrada em `DOMINIOS` + pacote em `PACOTES`
  (`roteador.py`). Teste primeiro: *"tarefa X → domínio Y"*.
- **Regra de identidade**: `IDENTIDADE` em `servidor_mcp.py` — verbo e
  consequência ("X é recusado sem Y"), não conselho.
- **Padrão de segredo**: regex em `PADROES_SEGREDO` (`memoria.py`) + teste da
  redação (nunca sem teste — leak-scan é segurança).
- **Gate**: função pura em `gates.py` + wrapper de uma linha no servidor.

Tudo sob a Regra da Segunda Versão: a v1 nunca é entregue; v1 → 3 críticas → v2.
Código crítico exige o torneio de 3 abordagens julgadas.

---

[ARQUITETURA (conceito)](ARQUITETURA.md) ·
[test-first](PROTOCOLO_TEST_FIRST.md) ·
[Segunda Versão](PROTOCOLO_SEGUNDA_VERSAO.md) ·
[adversarial](PROTOCOLO_ADVERSARIAL.md) ·
[dossiê completo](https://erickwilliamdesousa.github.io/renato/)
