# Contexto é orçamento — como o Renato gasta menos para dizer o mesmo

Cada tool exposta, cada memória injetada e cada lembrete repetido ocupa a
janela de contexto do agente. Contexto cheio de ruído é agente mais lento,
mais caro e mais distraído. Em 2026 o Renato passou por uma dieta medida.

## 1. Perfil de tools: 16 em vez de 37

O servidor completo tem 37 tools. A maioria das sessões usa um núcleo de 16
(sessão, memória, checkpoints, segurança, conclusão). O padrão passou a ser
o perfil **core**; o perfil **all** existe para quem precisa (interface,
grandes tarefas, deploy guiado). A descrição de cada tool é texto que o
modelo lê em toda conversa: menos tools, menos leitura.

Mesmo critério para MCPs de terceiros: três servidores de apps de mídia
custavam cerca de 56 mil tokens de descrição. Foram trocados por **uma** tool
com lista fechada de operações.

## 2. Abertura de sessão enxuta

A resposta do `session_start` cortou o que já chega por outro caminho
(protocolo estático que está no `CLAUDE.md` global): **57% menor**, mesma
informação útil. A memória entra como *gist* (uma linha por item, as mais
úteis primeiro) e o resto fica a um `recall` de distância.

## 3. SESSION_BRIEF: o resumo que substitui o handoff bruto

Ao encerrar, o handoff gera um `SESSION_BRIEF.md` com **teto de 2.000
caracteres**:

- heurística local sempre (estado do git, erros, recibos);
- um LLM refina o texto quando há chave, com **cache por hash** das fontes e
  da versão do prompt: só roda de novo quando algo mudou;
- falha do LLM degrada para a heurística. Há um interruptor para desligar.

A próxima sessão lê o brief primeiro; o handoff completo fica como fallback.

## 4. START_HERE com revelação progressiva

Antes: mais de 30 leituras obrigatórias (~60 KB) para "entrar no projeto".
Depois: um **núcleo de 4 leituras** (o brief primeiro) e um mapa sob demanda,
uma linha por artefato. O agente lê o que precisa quando precisa.

## 5. Lembrete uma vez, não a cada prompt

Hooks que injetam protocolo fazem isso **no primeiro prompt** da sessão e na
abertura real de contexto. Em retomada ou compactação, silêncio.

## 6. Modo de trabalho persistente

O Renato tem três modos: **pedagogo** (explica decisões e trade-offs, nível
sênior mentorando), **turbo** (executa sem explicar) e **colaborativo**.
A preferência passou a sobreviver entre sessões, com precedência explícita:

```
gatilho no texto da tarefa  >  variável de ambiente  >  preferência do workspace
  >  preferência global  >  colaborativo
```

O gatilho no texto ("vai direto", "me explica") vale **para aquela tarefa** e
não persiste. Mudança duradoura é ato deliberado, por comando. Assim uma
frase solta não reconfigura o projeto sem você perceber.

## 7. Telemetria por chamada

Toda chamada de tool vira uma linha local: nome, duração, sucesso e tamanho
da resposta. Só metadado: nenhum conteúdo, e o caminho do workspace entra
como hash. "Qual tool é cara?" deixou de ser palpite: é consulta.

## A regra por trás

> Medir antes de cortar. Cada corte acima tem um número antes e depois.
> Corte sem medição é só outra forma de opinião.
