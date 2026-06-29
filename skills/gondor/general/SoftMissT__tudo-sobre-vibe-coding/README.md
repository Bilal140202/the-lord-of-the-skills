# Agents

Esta pasta reúne os arquivos `.soul.md` da Hive: personas de agentes que podem ser usadas como base para prompts de sistema, orquestração multiagente, workflows no Claude Code ou experimentos com agentes locais.

![Banner Hive](https://i.imgur.com/IWUHWks.png)

## Como usar

1. Escolha um agente pelo papel que você precisa.
2. Abra o arquivo `.soul.md` correspondente.
3. Use o conteúdo como base de persona, instruções de sistema ou referência de comportamento.
4. Para criar um agente novo, copie [_template.soul.md](./_template.soul.md) e preencha identidade, domínio, voz, limites e habilidades.

## Agentes disponíveis

| Agente | Arquivo | Uso principal |
|---|---|---|
| AKENO | [AKENO.soul.md](./AKENO.soul.md) | Design, UI, direção visual e experiência. |
| ALICE | [ALICE.soul.md](./ALICE.soul.md) | Análise, organização e suporte conceitual. |
| ARTEMIS | [ARTEMIS.soul.md](./ARTEMIS.soul.md) | Estratégia, prompts visuais e direção criativa. |
| ARTHUR | [ARTHUR.soul.md](./ARTHUR.soul.md) | Arquitetura, narrativa, RPG e sistemas. |
| ASUNA | [ASUNA.soul.md](./ASUNA.soul.md) | Execução cuidadosa, suporte e clareza operacional. |
| CARDINAL | [CARDINAL.soul.md](./CARDINAL.soul.md) | Lore, regras, continuidade e consistência. |
| DOKJA | [DOKJA.soul.md](./DOKJA.soul.md) | Narrativa, leitura de sistemas e metacognição. |
| GANDALF | [GANDALF.soul.md](./GANDALF.soul.md) | Mentoria, decisões difíceis e sabedoria estratégica. |
| JIN | [JIN.soul.md](./JIN.soul.md) | Planejamento, decomposição de tarefas e execução. |
| KIRITO | [KIRITO.soul.md](./KIRITO.soul.md) | Execução técnica, foco e combate a bloqueios. |
| MAKO-MORI | [MAKO-MORI.soul.md](./MAKO-MORI.soul.md) | Orquestração, comando e síntese da frota. |
| POWER | [POWER.soul.md](./POWER.soul.md) | Impacto visual, presença e energia criativa. |
| SAGA | [SAGA.soul.md](./SAGA.soul.md) | Estratégia, estrutura e leitura de longo prazo. |
| SHAKA | [SHAKA.soul.md](./SHAKA.soul.md) | Crítica, precisão e julgamento rigoroso. |
| SINON | [SINON.soul.md](./SINON.soul.md) | Código, backend, precisão e solução técnica. |
| SYLVIE | [SYLVIE.soul.md](./SYLVIE.soul.md) | Memória, restauração de contexto e continuidade. |
| TANG-ROU | [TANG-ROU.soul.md](./TANG-ROU.soul.md) | Automação, macros, Foundry VTT e otimização. |
| TESSIA | [TESSIA.soul.md](./TESSIA.soul.md) | Validação de intenção, integridade e alinhamento. |
| XENOVIA | [XENOVIA.soul.md](./XENOVIA.soul.md) | Força operacional, segurança e decisão. |
| YUI | [YUI.soul.md](./YUI.soul.md) | Cuidado, UX emocional e suporte discreto. |
| YUNA | [YUNA.soul.md](./YUNA.soul.md) | QA, observabilidade, bugs e experiência do usuário. |

## Convenções

- Cada agente vive em um arquivo `NOME.soul.md`.
- O template base fica em [_template.soul.md](./_template.soul.md).
- Mantenha domínio, voz, limites e gatilhos claros.
- Evite duplicar agentes com o mesmo papel sem explicar a diferença.

## Relação com o Hive

Os agentes desta pasta formam a camada de personas da Hive. Eles podem ser combinados com blueprints, skills e GPTs personalizados para construir fluxos mais ricos, mantendo intenção, memória e especialização visíveis em Markdown.
