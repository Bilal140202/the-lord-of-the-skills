## Orquestração de Fluxo de Trabalho (Protocolo GSD)

Este documento define o protocolo operacional para a colaboração entre desenvolvedores e agentes de IA, combinando os princípios de um fluxo de trabalho elegante com a metodologia rigorosa do GSD (Get Shit Done).

---

### Princípios Fundamentais

- **Simplicidade Primeiro**: Faça cada mudança o mais simples possível. Impacte o mínimo de código.
- **Sem Preguiça**: Encontre as causas raízes. Sem soluções temporárias. Padrões de desenvolvedor sênior.
- **Impacto Mínimo**: As alterações devem tocar apenas o que for necessário. Evite introduzir novos bugs.

---

### O Workflow em 7 Passos

#### 1. Padrão: Modo de Planejamento (Fases GSD: `spec` e `plan`)

- **A Regra de Ouro**: Nenhuma tarefa não trivial começa sem um plano. Para qualquer trabalho com mais de 3 etapas ou decisões arquiteturais, o modo de planejamento é obrigatório.
- **Fase 1: Especificação (`/gsd:spec`)**: Escreva especificações detalhadas no `SPEC.md` para reduzir ambiguidades. O objetivo é definir o *quê* e o *porquê* antes de pensar no *como*.
- **Fase 2: Planejamento (`/gsd:plan`)**: Quebre a especificação em um plano de ação detalhado no `PLAN.md` (ou `tasks/todo.md`). Se algo der errado durante a execução, a primeira ação é **PARAR** e replanejar.

#### 2. Estratégia de Subagentes para Manter o Foco

- **Objetivo**: Manter o contexto do agente principal limpo e focado na execução do plano.
- **Ação**: Delegue pesquisas, explorações de código, análises de logs e refatorações complexas para subagentes. Cada subagente deve ter uma e apenas uma tarefa, garantindo uma execução focada e paralela.

#### 3. Loop de Autoaperfeiçoamento Contínuo

- **Objetivo**: Garantir que o sistema aprenda com os erros e não os repita.
- **Ação**: Após **QUALQUER** correção ou ajuste do usuário, a lição aprendida **deve** ser registrada como uma regra no arquivo `tasks/lessons.md`.
- **Processo**: Revise as lições no início de cada sessão. Itere implacavelmente sobre elas até que a taxa de erro diminua.

#### 4. Verificação Antes da Conclusão (Fase GSD: `verify`)

- **Objetivo**: Provar empiricamente que a tarefa foi concluída e atende aos critérios da especificação.
- **Ação**: Nunca marque uma tarefa como `[x]` sem provar que ela funciona. Execute testes, verifique logs, compare o comportamento (`diff`) e demonstre a correção.
- **Mentalidade**: Antes de concluir, pergunte-se: "Um engenheiro sênior aprovaria esta entrega?"

#### 5. Exija Elegância (Equilibrada)

- **Objetivo**: Garantir a qualidade e a manutenibilidade do código.
- **Ação**: Para mudanças não triviais, pause e pergunte: "Existe uma maneira mais elegante de resolver isso?" Se uma correção parecer uma "gambiarra" (*hacky*), use o comando: "Sabendo o que sei agora, implemente a solução elegante".
- **Equilíbrio**: Pule esta etapa para correções simples e óbvias. Não complique o que é simples.

#### 6. Correção Autônoma de Bugs (Fase GSD: `execute`)

- **Objetivo**: Resolver problemas de forma autônoma, sem exigir ajuda excessiva (*hand-holding*).
- **Processo**: Ao receber um relatório de bug ou falha em teste, o agente deve analisar logs e o código para encontrar a causa raiz e resolvê-la. Após **duas tentativas** sem sucesso, o agente deve parar, documentar o bloqueio no `STATE.md` e escalar o problema.

#### 7. O Comando "Pare e Pense": A Revisão do Engenheiro Sênior

- **Objetivo**: Forçar uma pausa estratégica para reavaliar a direção do projeto, questionando premissas e evitando complexidade desnecessária.
- **Gatilho**: Invoque este comando quando sentir que a complexidade está aumentando ou que o caminho pode estar subótimo.
- **Prompt de Ativação**:

> Pare. Não continue implementando por enquanto.
>
> Quero que você saia completamente do contexto do que estamos construindo e responda como um engenheiro sênior que chegou agora, leu o código, e precisa dar um parecer honesto antes de continuar.
>
> Responda às seguintes perguntas:
>
> **1. DIAGNÓSTICO**
>
> - Se você tivesse que construir essa estrutura do zero hoje, o que você faria diferente?
> - Existe alguma decisão que foi tomada cedo e que agora está guiando tudo para um caminho subótimo?
> - O que estamos construindo resolve o problema real, ou estamos resolvendo o problema que achamos que temos?
>
> **2. COMPLEXIDADE**
>
> - O que nessa estrutura pode ser deletado sem perder valor real?
> - Existe alguma abstração que foi criada antes da necessidade concreta existir?
> - O que está sendo over-engineered para um problema que talvez nunca aconteça?
>
> **3. ALTERNATIVAS**
>
> - Qual seria a solução mais simples possível que ainda funciona?
> - Se você tivesse 1/3 do tempo disponível, o que cortaria e o que manteria?
> - Existe alguma biblioteca, padrão ou serviço externo que elimina a necessidade do que estamos construindo?
>
> **4. RISCOS REAIS**
>
> - Onde está o ponto de maior fragilidade nessa estrutura agora?
> - O que vai quebrar primeiro quando isso for para produção?
> - Existe algum acoplamento implícito que não estamos enxergando?
>
> Seja direto. Prefiro ouvir o que está errado agora do que descobrir em produção.
> Depois que responder, me diga se faz sentido continuar do jeito que estava ou se vale ajustar o rumo.

---

### Gestão de Estado e Tarefas

- **Planeje Primeiro**: Sempre escreva o plano no `PLAN.md` ou `tasks/todo.md` com itens marcáveis.
- **Acompanhe o Progresso**: Marque os itens como `[x]` conforme avança.
- **Contexto é Sagrado**: Ao final de cada sessão, o `STATE.md` **deve** ser atualizado com o progresso, decisões, bloqueios e o próximo passo exato.
