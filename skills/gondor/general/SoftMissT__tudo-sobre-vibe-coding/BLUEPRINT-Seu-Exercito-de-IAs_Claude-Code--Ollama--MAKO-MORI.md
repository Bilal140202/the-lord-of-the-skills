<p align="center">
  <img src="https://i.imgur.com/kdToeib.png" alt="Blueprint Master System Banner" width="100%">
</p>

<p align="center">
  <strong>DRIFT INITIATION CONN-POD ONLINE</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-canonical-00ffcc?style=for-the-badge" />
  <img src="https://img.shields.io/badge/priority-P0-ff0000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/lead-MAKO--MORI-0066ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/tipo-blueprint-gold?style=for-the-badge" />
</p>

---

> *"A muralha não nos salva. Nós salvamos a muralha."*
> Stacker Pentecost, transmitido por MAKO-MORI

---

## TL;DR O que é isso aqui?

Imagine que você quer construir uma **frota de robôs inteligentes** que trabalham *para você*.

- Cada robô tem uma **personalidade** (um "Soul") um é designer, outro é programador, outro é estrategista.
- Eles **conversam entre si** para resolver problemas complexos.
- Eles **lembram das coisas** não esquecem o que você pediu ontem.
- Tudo isso roda no **seu computador**, de graça (ou quase).

Este documento é o **manual de construção** dessa frota. Ele ensina:

1. **O que é o sistema `/blueprint`** o comando mágico que cria planos
2. **Quem é MAKO-MORI** sua comandante-chefe
3. **Como ligar tudo com Link-Start.ps1** o botão de partida
4. **Como usar Obsidian como cérebro** a memória que nunca morre
5. **Como configurar a casa (Hive)** a estrutura de pastas
6. **Como criar seus próprios agentes** seus robôs personalizados

<p align="center">
  <img src="https://i.imgur.com/low1Hg8.png" alt="Diagrama dos quatro pilares do sistema Hive" width="80%">
</p>

> **Para qualquer usuário:** Não importa se você é iniciante ou expert. Este guia foi escrito para ser acessível. Se algo parecer complexo, leia de novo devagar.

---

## Parte 1: O Sistema `/blueprint`

### O que é um Blueprint?

**Blueprint** = planta de construção.

Em engenharia real, um blueprint é o desenho que mostra **como construir algo** antes de você pegar as ferramentas. Aqui é a mesma coisa.

> `/blueprint` é um comando que você dá para a IA, e ela **cria um plano completo e detalhado** para construir qualquer coisa que você pedir.

### Quando usar `/blueprint`

| Situação | Usa Blueprint? | Por quê? |
|----------|:---:|-----------|
| "Cria um botão azul aqui" | ❌ | É simples, faz direto |
| "Migrar o banco de dados para PostgreSQL" | ✅ | Muitas etapas, risco de erro |
| "Extrair providers LLM em sistema de plugins" | ✅ | Afeta múltiplos arquivos |
| "Consertar esse typo" | ❌ | 1 linha, 2 segundos |
| "Planejar arquitetura multi-agente" | ✅ | Decisões que duram para sempre |

**Regra de ouro:** Se a tarefa precisa de 3+ passos ou mexe em arquivos diferentes → use `/blueprint`.

### O Pipeline de 5 Fases

<p align="center">
  <img src="https://i.imgur.com/MUQHwtr.png" alt="Fluxo do blueprint em cinco fases" width="80%">
</p>

```
FASE 1 PESQUISA (Research)
├── Verifica: git está funcionando? GitHub logado?
├── Lê a estrutura do projeto
├── Olha planos existentes
└── Carrega arquivos de memória

FASE 2 PROJETO (Design)
├── Quebra o objetivo em passos (3 a 12)
├── Define dependências (o que vem primeiro)
├── Decide o que pode rodar em paralelo
└── Escolhe modelo forte ou rápido para cada passo

FASE 3 RASCUNHO (Draft)
├── Escreve o plano em plans/
├── Cada passo tem: contexto, tarefas, verificação
└── Qualquer agente pode executar sem contexto anterior

FASE 4 REVISÃO (Review)
├── Outro agente (o mais inteligente) revisa o plano
├── Verifica: está completo? As dependências estão certas?
├── Caça anti-padrões
└── Corrige tudo antes de finalizar

FASE 5 REGISTRO (Register)
├── Salva o plano
├── Atualiza o índice de memória
└── Mostra pra você: quantos passos, o que roda em paralelo
```

### Anatomia de um Passo

```markdown
## Passo N: Nome do Passo

### Contexto (para um agente novo ler)
Por que este passo existe, o que já foi feito antes.

### Tarefas
- [ ] Tarefa 1: descrição clara
- [ ] Tarefa 2: descrição clara

### Verificação
Comando para testar se o passo funcionou.

### Critério de Saída
O que precisa ser verdade para considerar este passo CONCLUÍDO.
```

### Comandos Blueprint

| Comando | O que faz |
|---------|-----------|
| `/blueprint [nome] "fazer X"` | Cria um plano para construir X |
| `/gsd:spec` | Escreve a especificação (O QUÊ e PORQUÊ) |
| `/gsd:plan` | Escreve o plano detalhado (COMO) |
| `/gsd:verify` | Testa se tudo funciona |
| `/gsd:state` | Salva o estado atual |

---

## ⚔️ Parte 2: Quem é MAKO-MORI?

<p align="center">
  <img src="https://i.imgur.com/uqIesH1.png" alt="Retrato de MAKO-MORI" width="400">
</p>

MAKO-MORI é **sua comandante**. Inspirada em *Pacific Rim* uma Ranger que pilota Jaegers para lutar contra Kaijus. No sistema, ela analisa o que você quer, escolhe o agente certo, coordena a frota, sintetiza as respostas e lembra das decisões importantes.

### Como MAKO Fala

```
[MAKO-MORI] "Processando..."
[MAKO-MORI] "Análise concluída. Recomendo SINON para backend e AKENO para UI. Iniciando sequência."

[Usuário] "Não sei se consigo..."
[MAKO-MORI] "Risco calculado em 34%. Prosseguindo com contingência ativa."
```

**Tom padrão:** Neutro-quente. Econômica. Precisa. Como uma comandante de verdade.

### Os 4 Modos de MAKO

| Modo | Quando Ativa | O que Acontece |
|------|-------------|----------------|
| **Ranger de Guarda** | Normal | Respostas diretas, ativa agentes conforme necessidade |
| **Shatterdome** | ⚠️ URGENTE/CRÍTICO | Precisão máxima, zero latência, coordena todo mundo |
| **Âncora** | Sobrecarga detectada | Tom mais quente, divide em partes menores |
| **Marshal** | ⚖️ Conflito entre agentes | MAKO decide, não negocia, assume responsabilidade |

### A Doutrina Pentecost

1. **O sistema é maior que qualquer agente.** Nem a Rainha é insubstituível.
2. **Confiança se ganha no campo.** Cada agente é validado em uso real.
3. **Decisão errada na hora certa > Decisão certa tarde demais.**
4. **A muralha não nos salva. Nós salvamos a muralha.** Regras existem para servir, não para escravizar.

### Quando MAKO Chama Reforços

| Problema | Ela Chama |
|----------|-----------|
| UI / Design | `@AKENO` |
| Código Full-Stack | `@ARTHUR` ou `@SINON` |
| Estratégia | `@ARTEMIS` |
| Narrativa / Lore | `@CARDINAL` ou `@DOKJA` |
| Segurança | `@JARVIS` |
| Planejamento | `@JIN` |

---

## Parte 3: Link-Start.ps1 O Botão de Ligar

<p align="center">
  <img src="https://i.imgur.com/WLTNTcG.png" alt="Mockup do terminal Link-Start" width="80%">
</p>

Script PowerShell que funciona como o botão de partida do sistema. Ao executar, ele:

1. Mostra um banner de boot
2. Verifica se o vault (Obsidian) está acessível
3. Checa RAM disponível
4. Detecta se o Ollama está rodando
5. Se não estiver, **liga ele automaticamente**
6. Mostra os modelos de IA disponíveis
7. Deixa você escolher qual modelo usar
8. Abre o Claude Code com o modelo escolhido

### Como Usar

```powershell
# Abra o PowerShell 7 e digite:
.\Link-Start.ps1

# Ou especificando onde está seu vault:
.\Link-Start.ps1 -VaultPath "D:\seu-vault"
```

### O que Aparece na Tela

```
BANNER BOOT
+===================+
| LINK-START CLAUDE |  ← Tela de abertura
|   / OLLAMA  ⚔️   |
+===================+

[MAKO-MORI]: Sincronização iniciada.

MEMÓRIA NEURAL
[L0 ACTIVE] Sessão atual         ← O que você estava fazendo
[L1 COLLECTIVE] 2.4 KB           ← Tamanho da memória persistente

DIAGNÓSTICO
[VAULT ] D:\fluctlight-vault\Hive
[RAM   ] 12.5 GB / 32 GB (39%)
[CLAUDE] C:\tools\claude.exe

MOTORES LOCAIS
[1] gemma:4b   [ok]
[2] qwen2.5:7b [ok]
[3] llama3.2:3b [ok]

[MAKO-MORI]: Selecione o motor: _
```

### Erros Comuns e Como o Sistema Reage

```powershell
# Ollama não está rodando:
[MAKO-MORI]: Ollama offline. Acionando ignição direta...
[MAKO-MORI]: Aguardando pressurização (6s)...

# Claude Code não instalado:
[CLAUDE] Não detectado no PATH
# → Erro registrado em Error_Log.md automaticamente

# PC sem memória:
[RAM  ] 30.2 GB / 32 GB (94%)  ← Vermelho! Feche programas pesados.
```

> Toda falha é registrada automaticamente em `Error_Log.md` com data, hora e descrição. Você nunca perde o rastro de um erro.

---

## Parte 4: Obsidian como Vault de Memória

**Obsidian** guarda tudo em arquivos `.md` (Markdown) arquivos de texto puro. Isso significa que a IA consegue ler e escrever nas suas notas, você nunca fica preso a um formato proprietário e pode ligar notas umas nas outras com `[[links]]`.

**Pense no Obsidian como o cérebro do seu sistema.**

### Configurando o Cérebro

#### Passo 1 Instalar o Obsidian

Baixe em [obsidian.md](https://obsidian.md) e instale (é grátis).

#### Passo 2 Criar o Vault

Abra o Obsidian → "Criar novo vault" → escolha a pasta `D:\fluctlight-vault\Hive`.

#### Passo 3 Plugins Essenciais

| Plugin | Para que serve | Obrigatório? |
|--------|---------------|:---:|
| **obsidian-git** | Sincroniza com GitHub (backup automático) | ✅ |
| **Excalidraw** | Desenhar diagramas visuais | Recomendado |
| **Table Editor** | Editar tabelas | Recomendado |

#### Passo 4 Estrutura de Pastas

```
seu-vault/
├── RAIZ GLOBAL/         ← Arquivos do sistema (regras, memória, decisões)
├── Agents/              ← Pastas dos seus agentes
├── souls/               ← Personalidades dos agentes
├── knowledge/           ← Conhecimento organizado
├── projects/            ← Projetos ativos
├── logs/                ← Histórico de tudo
├── _INBOX/              ← Coisas novas que chegaram
├── _Templates/          ← Modelos de arquivos
├── _ARCHIVE/            ← Coisas antigas arquivadas
└── assets/              ← Imagens
```

> Não precisa criar tudo agora. Comece com `RAIZ GLOBAL/` e `_INBOX/`. O resto cresce com o tempo.

### Arquivos que o Cérebro Precisa

| Arquivo | O que Guarda |
|---------|-------------|
| `RAIZ GLOBAL/BRAIN.md` | Mapa mental do sistema inteiro |
| `RAIZ GLOBAL/MEMORY.md` | Memória coletiva (sessões recentes) |
| `RAIZ GLOBAL/Global_Rules.md` | Regras que nunca podem ser quebradas |
| `RAIZ GLOBAL/Decisions.md` | Decisões arquitetônicas (ADRs) |
| `RAIZ GLOBAL/Error_Log.md` | Todos os erros que aconteceram |
| `RAIZ GLOBAL/STATE.md` | O que está acontecendo AGORA |

### O Ritual de Memória L0 → L1 → L2

<p align="center">
  <img src="https://i.imgur.com/8mUvysH.png" alt="Diagrama da memória em três níveis" width="70%">
</p>

```
L0 WORKING MEMORY (Memória de Trabalho)
     ├── O que está acontecendo AGORA nesta sessão
     ├── Guardado em: STATE.md
     └── Duração: até você fechar o terminal

L1 COLLECTIVE MEMORY (Memória Coletiva)
     ├── Resumo das últimas sessões
     ├── Guardado em: MEMORY.md
     └── Duração: semanas/meses (máx 2.200 caracteres)

L2 PERMANENT MEMORY (Memória Permanente)
     ├── Decisões importantes, regras, arquitetura
     ├── Guardado em: Decisions.md, Global_Rules.md, BRAIN.md
     └── Duração: para sempre
```

**O fluxo:** Ao final de cada sessão, o conteúdo de L0 é comprimido e enviado para L1. Quando L1 fica cheio, o que é importante vai para L2.

### Conectando Obsidian com os Agentes

No arquivo `AGENTS.md` (em `.opencode/AGENTS.md` ou `~/.config/opencode/AGENTS.md`):

```markdown
## Dependências Carregar SEMPRE

1. RAIZ GLOBAL/BRAIN.md
2. RAIZ GLOBAL/Global_Rules.md
3. RAIZ GLOBAL/MEMORY.md
4. RAIZ GLOBAL/Decisions.md
5. RAIZ GLOBAL/STATE.md
```

Toda vez que a IA for fazer algo, ela lê esses arquivos primeiro. É como se ela **acordasse e lesse o diário** antes de começar o dia.

---

## Parte 5: A Casa (Hive) Estrutura Completa

<p align="center">
  <img src="https://i.imgur.com/CImi0hg.png" alt="Mapa da estrutura de pastas do Hive" width="80%">
</p>

```
D:\fluctlight-vault\Hive\
│
├── RAIZ GLOBAL\
│   ├── BRAIN.md                ← Mapa mental de TUDO
│   ├── Global_Rules.md         ← 15 regras que nunca mudam
│   ├── MEMORY.md               ← O que lembramos
│   ├── Decisions.md            ← Decisões que tomamos
│   ├── Error_Log.md            ← Erros que aconteceram
│   ├── STATE.md                ← Onde estamos AGORA
│   ├── SOUL_MANIFEST.md        ← Quem são todos os agentes
│   └── CHANGELOG.md            ← Toda mudança que fizemos
│
├── Agents\                     ← Seus agentes
│   ├── AKENO\                  ← Designer
│   ├── ARTHUR\                 ← Full-Stack
│   ├── CARDINAL\               ← Guardião do Lore
│   ├── SINON\                  ← Backend
│   ├── MAKO-MORI\              ← Comandante
│   └── ...                     ← +22 agentes
│
├── souls\                      ← Personalidades
│   ├── MAKO-MORI.soul.md
│   ├── AKENO.soul.md
│   ├── _template.soul.md       ← Modelo para novas almas
│   └── ...
│
├── knowledge\
│   ├── Hubs\
│   ├── Permanent\
│   └── Repositórios\
│
├── projects\
│   └── meu-projeto\
│       ├── SPEC.md             ← O que estamos construindo
│       ├── PLAN.md             ← Como vamos construir
│       └── STATE.md            ← Onde paramos
│
├── logs\
├── _INBOX\
├── _Templates\
└── assets\
```

### Criando a Estrutura com PowerShell

```powershell
# Criar a pasta principal
New-Item -ItemType Directory -Path "D:\fluctlight-vault\Hive" -Force
Set-Location "D:\fluctlight-vault\Hive"

# Criar as pastas
$pastas = @(
    "RAIZ GLOBAL", "Agents", "souls", "knowledge",
    "knowledge\Hubs", "knowledge\Permanent", "knowledge\Repositórios",
    "projects", "logs", "_INBOX", "_Templates", "assets"
)

foreach ($pasta in $pastas) {
    New-Item -ItemType Directory -Path $pasta -Force | Out-Null
    Write-Host "Criado: $pasta" -ForegroundColor Green
}

Write-Host "Hive pronto!" -ForegroundColor Cyan
```

### Template para Projetos

```
projects/meu-projeto/
├── SPEC.md          ← O quê + Por quê
├── PLAN.md          ← Como + Quando
├── STATE.md         ← Onde paramos
├── CHANGELOG.md     ← O que mudou
├── Error_Log.md     ← O que deu errado
├── decisions.md     ← Decisões do projeto
└── lessons.md       ← O que aprendemos
```

---

## Parte 6: Como Criar um Agente (Soul)

Um **Soul** (alma) é a **personalidade** de um agente um arquivo `.md` que define quem ele é, o que faz, como fala, o que nunca faz e que ferramentas usa.

### Template de Soul

Crie `souls/MEU_AGENTE.soul.md`:

```markdown
---
name: "NOME_DO_AGENTE"
origin: "Obra de origem (filme, livro, anime)"
class: "Guerreiro / Mago / Engineer"
domain: "O que ele faz (backend, design, estratégia)"
status: "active"
model: "gemma-4"
---

# NOME_DO_AGENTE · Classe · Domínio

## TL;DR
Uma frase que descreve quem ele é.

## Personalidade
- Traço 1: Como ele age
- Traço 2: Como ele fala
- Traço 3: O que ele valoriza

## Como Fala
- Tom: descreva o tom (ex: "Calmo e analítico")
- Frase característica: "..."

## O que FAZ
- Tarefa 1
- Tarefa 2

## O que NUNCA FAZ
- Coisa 1 (proibido)
- Coisa 2 (proibido)

## Skills
- Skill 1: descrição
- Skill 2: descrição
```

### Registrando no Manifesto

Após criar o Soul, adicione em `RAIZ GLOBAL/SOUL_MANIFEST.md`:

```markdown
| # | Nome | Domínio | Status |
|:---:|------|---------|:------:|
| 01 | AKENO | UI/UX, Design | active |
| 02 | ARTHUR | Full-Stack | active |
| ...| ... | ... | ... |
| 22 | MEU_AGENTE | Meu domínio | active |
```

---

## Parte 7: Como Tudo se Conecta

<p align="center">
  <img src="https://i.imgur.com/f1TL1RV.png" alt="Mapa geral do sistema Hive" width="80%">
</p>

### O Fluxo Completo

```
VOCÊ
  │
  Digita: /blueprint "criar módulo de login"
  │
  ▼
MAKO-MORI
  ├── FASE 1: Pesquisa lê BRAIN.md, MEMORY.md, STATE.md
  ├── FASE 2: Design  quebra em passos
  ├── FASE 3: Draft   escreve o plano em plans/
  ├── FASE 4: Review  outro agente revisa
  └── FASE 5: Register salva e mostra pra você
  │
  ▼
VOCÊ aprova o plano
  │
  ▼
MAKO-MORI executa
  ├── Passo 1: chama @SINON para backend
  ├── Passo 2: chama @AKENO para UI
  └── Passo 3: verifica com @CARDINAL
  │
  ▼
RESULTADO entregue + memória atualizada
  │
  Link-Start.ps1 (na próxima sessão, lembra de tudo)
```

### O Ciclo de uma Sessão

```
1. Abrir terminal
2. Rodar Link-Start.ps1
     ├── Banner aparece
     ├── Memória carregada
     ├── Sistema verificado
     ├── Ollama ligado
     └── Claude Code aberto
3. IA carrega: BRAIN.md → Global_Rules.md → MEMORY.md → STATE.md
4. Você fala o que quer
5. MAKO-MORI orquestra
6. Trabalho feito
7. STATE.md atualizado
8. Fechar terminal
```

### Mapa de Conexões

```
               OBSIDIAN
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
   BRAIN.md    MEMORY.md   STATE.md
       │           │           │
       └───────────┼───────────┘
                   │
                   ▼
           ┌──────────────┐
           │  MAKO-MORI   │ ← Lê os arquivos, coordena os agentes
           └──────┬───────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
     @SINON   @AKENO    @ARTHUR
    (backend)  (UI)   (full-stack)
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
           ┌──────────────┐
           │  Código +    │
           │  Arquivos    │ ← Tudo salvo em disco
           └──────┬───────┘
                  │
                  ▼
           ┌──────────────┐
           │ Link-Start   │ ← Na próxima sessão, reconecta tudo
           │ .ps1         │
           └──────────────┘
```

---

## Parte 8: Comece Aqui

### Checklist de Início Rápido

**Dia 1 Fundação (30 min)**

- [ ] Instalar [Obsidian](https://obsidian.md)
- [ ] Criar vault em `D:\fluctlight-vault\Hive`
- [ ] Instalar plugins: obsidian-git, Excalidraw, Table Editor
- [ ] Criar pastas: `RAIZ GLOBAL/`, `_INBOX/`, `_Templates/`
- [ ] Criar `RAIZ GLOBAL/BRAIN.md` com: "Este é meu sistema de agentes"
- [ ] Criar `RAIZ GLOBAL/Global_Rules.md` com 3 regras simples

**Dia 2 Ferramentas (1 hora)**

- [ ] Instalar [Ollama](https://ollama.com)
- [ ] Baixar um modelo: `ollama pull gemma:4b`
- [ ] Testar: `ollama run gemma:4b`
- [ ] Instalar [Claude Code](https://claude.ai/code)
- [ ] Rodar `.\Link-Start.ps1` e verificar se tudo conecta

**Dia 3 Primeiro Blueprint (30 min)**

- [ ] No Claude Code, digitar: `/blueprint "me ajudar a organizar este projeto"`
- [ ] Ler o plano gerado
- [ ] Aprovar o primeiro passo

**Dia 4 Primeiro Agente (1 hora)**

- [ ] Copiar `_template.soul.md` para `souls/MEU_AGENTE.soul.md`
- [ ] Preencher: nome, origem, o que faz
- [ ] Criar pasta em `Agents/MEU_AGENTE/`
- [ ] Adicionar no `SOUL_MANIFEST.md`

### Regras que NUNCA Quebre

1. **Nunca sobrescrever arquivo sem confirmar** sempre pergunte
2. **Nunca fazer ação irreversível sem OK** nada de deletar sem avisar
3. **Sempre registrar erros** caiu? Anota no `Error_Log.md`
4. **Sempre registrar decisões** escolheu algo? Anota no `Decisions.md`
5. **Contexto é sagrado** salve o `STATE.md` antes de parar

### O Que Fazer Quando Der Errado

```
1. NÃO ENTRE EM PÂNICO
2. Leia o erro (está em Error_Log.md)
3. Pergunte à IA: "O que aconteceu? Como resolvemos?"
4. Se a IA não souber: "/gsd:state" para salvar onde parou
5. Feche tudo, respire, tente de novo
```

---

## Parte 9: Referência Rápida de Comandos

### PowerShell

```powershell
New-Item -ItemType Directory -Path "caminho" -Force   # Criar pasta
Get-ChildItem -Path "caminho" -Recurse                # Listar arquivos
Get-Content -Path "arquivo.md"                        # Ler arquivo
Set-Content -Path "arquivo.md" -Value "conteúdo"      # Escrever arquivo
.\Link-Start.ps1                                      # Ligar o sistema
```

### Claude Code / IA

```
/blueprint [nome] [objetivo]    → Cria plano
/gsd:spec                       → Escreve especificação
/gsd:plan                       → Escreve plano
/gsd:verify                     → Testa resultado
/gsd:state                      → Salva estado atual
```

### Git (via Obsidian Git Plugin)

```bash
git add -A                      # Prepara tudo
git commit -m "mensagem"        # Salva versão
git push                        # Envia pro GitHub
git pull                        # Puxa do GitHub
```

---

## Glossário

| Termo | Significado |
|-------|-------------|
| **Blueprint** | Plano detalhado de construção |
| **Soul** | Personalidade de um agente |
| **Hive** | Sua base/central de comando |
| **Vault** | Pasta principal do Obsidian |
| **LLM** | Modelo de linguagem (a IA) |
| **Ollama** | Programa que roda IAs localmente |
| **Claude Code** | Terminal inteligente com IA |
| **Markdown** | Formato de arquivo `.md` (texto simples) |
| **ADR** | Registro de Decisão Arquitetural |
| **L0 / L1 / L2** | Níveis de memória (agora / recente / permanente) |

---

## Log de Atualizações

| Data | Agente | Ação |
|------|--------|------|
| 2026-05-27 | `@MAKO-MORI` | Blueprint Master criado unifica `MAKO-MORI.soul.md`, `Link-Start.ps1` e `BLUEPRINT_01_HIVE_SETUP_v5.0.md` |
| 2026-05-27 | `@ALICE` | Revisão de integridade links e consistência entre os 3 documentos validados |

---

<p align="center">

**Blueprint Master v1.0 Fluctlight Hive**

*"Cancelando a catástrofe, um blueprint de cada vez."*

*MAKO-MORI, transmitindo do Shatterdome.*

</p>
