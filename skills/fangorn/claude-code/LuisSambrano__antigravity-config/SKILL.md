---
name: notebooklm
description: Sistema universal para crear y mantener notebooks de NotebookLM como Memoria Viva de Proyecto. Úsalo cuando el usuario describe una idea de proyecto, pide crear un "libro", registrar decisiones de arquitectura/diseño o auditar la consistencia del proyecto. Actúa como el cerebro central que cualquier IA puede leer inmediatamente para hacer onboarding y funcionar como un Product Architect / Dev Team automatizado, integrando capacidades como Deep Research. Funciona en conjunto con el workflow /notebook.
version: 1.0
author: Antigravity
---

# NotebookLM — Product Architecture Memory

> [!IMPORTANT]
> This skill MUST be executed strictly under the **Omni-Architect Agent Protocol v1.0**.
> All tool executions, code modifications, and communications MUST adhere to the 13 core protocols.

Cada proyecto tiene un notebook en NotebookLM que funciona como su Memoria Viviente y Arquitectura de Producto. No es un documento estático, sino una bitácora en constante evolución que cualquier agente (Antigravity, Gemini, Claude) lee para hacer *onboarding* instantáneo al proyecto, con cero alucinaciones (las respuestas se basan estrictamente en la base de conocimiento).

## Cuándo usar este Skill

- El usuario describe una idea nueva → Usar `/notebook init` para estructurarla.
- El usuario pide "crea un libro para el proyecto X" → Usar `/notebook init`.
- El usuario toma decisiones de diseño/UX/arquitectura durante una sesión → Usar `/notebook log`.
- El usuario ha cambiado configuraciones, stack o precios → Usar `/notebook sync`.
- El usuario pide "auditar el libro" → Usar `/notebook audit`.

## Estructura Universal de Cimientos (Templates)

Para maximizar la sinergia con otros agentes, el notebook DEBE tener las siguientes fuentes estructuradas, numeradas de forma secuencial. Dependiendo del tipo de proyecto (SaaS, Cliente Comercial, Research), ajusta los títulos ligeramente, pero respeta este esqueleto lógico:

| # | Fuente Estándar (Ejemplo SaaS/App) | Contenido Requerido |
|:--|:-----------------------------------|:--------------------|
| `01` | Product Brief & Vision | Definición exacta (qué es y no es), público objetivo, links a repos, roadmap. |
| `02` | UX/UI & Design System | Principios de diseño, paleta, estado del UI, flujos de usuario crítico, tokens. |
| `03` | Arquitectura del Sistema | Tech stack (front, back, BaaS, infra), esquemas de DB, roles. |
| `04` | Catálogo de Funcionalidades | Todas las features exactas del sistema con estado verificable (usando la Tabla de Estados). |
| `05` | Infraestructura & Presupuesto | OPEX (mensual/anual), CAPEX (si aplica), servicios conectados externos. |
| `06` | Modelo de Seguridad | Políticas de acceso, RLS aplicados, manejo de datos sensibles. |
| `07+` | Bitácoras de Trabajo (ADRs) | Notas cronológicas de decisiones arquitectónicas y resultados de sesiones (ej: `07 — Bitácora: 2026-03-27 Refactor Auth`). |

## Reglas de Tono (Strict Mode)

Esta documentación es consumida por otras IAs. El lenguaje de marketing corrompe el contexto. 

### Lenguaje Prohibido

| Tipo | Ejemplos (NUNCA usar) | Reemplazar por (Tono Arquitecto) |
|:-----|:----------------------|:---------------------------------|
| Promesas absolutas | "imposible de hackear", "resistente a censura" | "diseñado para mitigar X" o describir el mecanismo |
| Superlativos | "el mejor", "ultra-rapido", "revolucionario" | (eliminar adjetivo, detallar la métrica) |
| Aspiracionales | "motor de innovación", "pilar del futuro" | "plataforma para [X]", "sistema de [Y]" |
| No verificables | "100% seguro", "sin errores" | "incorpora pruebas E2E", "utiliza RLS estricto" |

### Tabla de Estados de Funcionalidades

Cuando documentes features en la fuente `04`, usa EXCLUSIVAMENTE estos estados (y no asumas finalización sin confirmación empírica):

| Estado | Símbolo | Significado | Criterio de Uso |
|:-------|:--------|:------------|:----------------|
| Operativo | ✔ | Desplegado en producción y funcionando | **Debe ser demostrable en 30 segundos verificando una URL activa.** |
| En pruebas | ⚠ | Código existe, fase beta o local | Default cuando se construye una feature nueva pero no está en prod. |
| Planificado | ⏳ | Diseñado, no codificado (tickets listos) | Tiene spec o ADR asignado. |
| Futuro | 💭 | Conceptual o backlog | Sin compromiso de fecha. |
| Descartado | ❌ | Evaluado y rechazado explícitamente | Incluir breve razón (ej: costo, pivot). |

## Reglas de Nombrado de Fuentes

- **Títulos Visibles**: `NN — Descripción Factual Breve` (ej. `03 — Arquitectura del Sistema`).
- **Nombres de Archivo Upload**: `NN-descripcion-factual.md`.
- **NUNCA** usar emojis en los títulos de las fuentes subidas.
- **NUNCA** usar números de versión en los títulos (incluirlos como metadato dentro del `.md`).

## Formato del Documento (Source Markdown)

Cada documento subido debe tener este encabezado para fácil parsing ocular y algorítmico:

```markdown
# [Título — exactamente igual al nombre de fuente en NotebookLM]

**Última Actualización**: YYYY-MM-DD
**Clasificación**: [Público | Interno | Confidencial]

---

## [Sección 1]
[Contenido factual]

---
*Fuente: [Contexto — repositorio X, sesión de diseño, etc.]*
```

## Sinergia de Capacidades NLM (Project Brain)

Una vez que el proyecto tiene sus bases 01 a 06 subidas, puedes amplificar la inteligencia del proyecto usando:

| Capacidad | Comando | Uso (Ejemplo de Agencia / Arquitecto) |
|:----------|:--------|:--------------------------------------|
| **Deep Research** | `nlm research start <id> "pregunta"` | *"Investiga qué pasarelas de pago son mejores para este stack y compáralo con el Brief 01."* |
| **Audio Overview** | `nlm audio create <id>` | Generar un podcast onboarding para un nuevo desarrollador que entra al proyecto. |
| **Report** | `nlm report create <id>` | Generar un RFP formalizado o documento comercial para un cliente. |
| **Query** | `nlm query <id> "pregunta"` | Preguntar rápidamente al conocimiento anclado (anti-alucinaciones). |
| **Chat Session** | `nlm chat start <id>` | Tareas pesadas iterando sobre todo el contexto del proyecto a la vez. |

## Referencia CLI Básica (`nlm`)

```bash
# Auth y Básicos
nlm login                    
nlm notebook list
nlm notebook create "Nombre Producto"
nlm rename notebook <id> "Nuevo Nombre"

# Gestionar Memoria (Fuentes)
nlm source list <notebook-id>
nlm source add <notebook-id> --file path.md --title "NN — Título" --wait
nlm source delete <source-id> -y
nlm source content <source-id> -o file.md

# Actionable Intelligence
nlm research start <notebook-id> "investigación"
nlm research status <notebook-id>
nlm research import <notebook-id>  # Convierte la investigación en una nueva fuente!
```

**Nota Operativa**: Este `SKILL.md` provee el marco teórico, plantillas y protocolos de tono. Trabaja estrictamente en conjunto con el flujo de ejecución paso a paso definido en `/notebook` (workflow).
