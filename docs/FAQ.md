# FAQ — o que sempre perguntam, sem marketing

### "Meu agente já é ótimo. Para que isso?"
Ele é ótimo em **escrever** e péssimo em **lembrar e se cobrar**. O Renato não
compete com o agente — coordena: memória entre sessões, método que não depende de
boa vontade e gates que não aceitam "confia". Velocidade sem método é protótipo
disfarçado de produto.

### "Funciona com qual IDE?"
Qualquer um que fale **MCP** — Antigravity, VS Code, Cursor. Identidade, memórias e
gates chegam dentro da conversa do agente; a CLI determinística cobre o resto, e
humanos também podem usá-la direto.

### "Quanto custa rodar?"
O caminho crítico é local e de **custo zero**: roteamento sem LLM, memória em
SQLite, gates como funções puras. Chamadas pagas são periféricas e opcionais
(vetores de memória) — e vivem sob **teto diário de custo** com bloqueio automático.

### "Meus dados saem da máquina?"
Acervo, índices, segredos e backups: **não**. O texto de uma memória viaja apenas
para gerar o vetor semântico — **depois** do leak-scan — e o sistema inteiro degrada
para busca local pura se você cortar a internet.

### "Isso não burocratiza o trabalho?"
Tarefa trivial fica **fora dos gates** por classificação. Nas relevantes, o custo é
minutos — contra horas de retrabalho do bug que o gate teria segurado. E, por
construção, **desobedecer dá mais trabalho que obedecer**.

### "Por que não usar LLM no roteamento?"
**Reprodutibilidade e auditoria**: mesmo pedido, mesmo método, custo zero, latência
zero. Auditar é ler uma tabela de pesos — não interrogar um modelo sobre o que ele
decidiu ontem.

### "E se o Renato quebrar?"
O agente continua funcionando — o Renato coordena, não executa. Os artefatos ficam
no projeto, legíveis **sem a ferramenta**. E o cérebro tem backup com verificação de
integridade: restaurado de verdade, não por fé.

### "Por onde eu começo?"
Pela [semente](../starter/README.md) (5 minutos) ou, sem instalar nada, pela
[escada de adoção](ADOCAO.md) — uma prática por semana, à mão.
