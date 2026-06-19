---
name: stitch-design-taste
description: >-
  Guia al agente para generar interfaces de alta calidad con Google Stitch.
  Usar cuando se creen pantallas con stitch_generate_screen, se exporte
  diseño a frameworks, o se necesite un design system coherente.
  Proporciona criterios de diseño (no valores fijos) para evitar
  interfaces genericas y producir resultados premium.
---

# Stitch Design Taste — Criterios de Diseño para Agentes

Guia de criterios para generar interfaces no-genericas con Google Stitch.
No prescribe valores fijos — enseña **como tomar decisiones de diseño**.
Los valores reales (colores, fuentes, spacing) salen del `DESIGN.md` del
proyecto generado con `stitch-mcp-cli design-md`.

## Regla fundamental

Siempre que exista un `DESIGN.md` en el proyecto o en `.stitch/metadata.json`,
usarlo como fuente de verdad. Esta skill complementa ese archivo con
criterios de calidad, no lo reemplaza.

## Anti-Slop Rules

**Prohibido — estos patrones producen interfaces genericas de IA:**

- Hero sections centradas con heading + subheading + CTA en columna vertical
- Cards identicas en grid de 3 con icono + titulo + descripcion
- Fuentes genericas como unica opcion: Inter, Roboto, Arial, system-ui
- Estetica neon, degradados arcoiris, o "glassmorphism" excesivo
- Copy con "Revolutionize", "Seamless", "Cutting-edge", "Next-gen", "Empower"
- Todo con el mismo border-radius (todo redondo o todo cuadrado)
- Sombras apiladas o excesivas
- Espaciado uniforme entre todos los elementos

**Obligatorio — senales de calidad:**

- Cada pantalla tiene un **foco visual unico** — el ojo sabe donde ir
- Contraste de tamano real entre elementos (no todo el mismo peso visual)
- Al menos un elemento inesperado o memorable por pantalla
- Espacio negativo deliberado, no accidental
- Jerarquia tipografica con diferencia de tamano >= 1.25x entre niveles
- Asimetria cuando el layout lo permite

## Color

### Como calibrar (no que colores usar)

Stitch interpreta colores como descripciones semanticas. Siempre dar contexto,
no solo valores hex:

```
Bien:  "Azul profundo para acciones primarias, transmite confianza sin ser corporativo"
Mal:   "#1E3A5F"
```

### Criterios

- Maximo 4 colores con rol activo por pantalla
- El color de acento cubre <= 10% de la superficie visible
- Fondos oscuros requieren colores mas vivos (saturacion), no mas brillantes (luminosidad)
- Probar la paleta en escala de grises: si no hay jerarquia sin color, la paleta falla
- Nunca negro puro (#000) para texto — usar casi-negro con tinte
- Nunca blanco puro (#FFF) para fondos — usar blanco con tinte calido o frio segun la paleta

### Como derivar la paleta del DESIGN.md

Si el proyecto tiene `customColor`, generar la paleta completa a partir de ese
unico color:

1. **Primary** = el customColor del proyecto
2. **Accent** = complementario o analogo al primary, con contraste suficiente
3. **Background** = tinte muy sutil derivado del primary (calido si primary es calido, etc.)
4. **Surface** = version mas clara del background
5. **Text** = casi-negro con tinte del primary

## Tipografia

### Criterios de pairing

Regla: **una fuente con personalidad + una neutral**. Nunca dos decorativas.

| Rol | Caracteristicas | Evitar |
|-----|----------------|--------|
| Display/Heading | Seriff geometrico o sans con caracter. Peso 700-900 | Fuentes system genericas |
| Body | Humanist sans, legible a tamano pequeno. Peso 400 | Fuentes display para body |
| Mono/Codigo | Monospace con personalidad | Courier |

### Jerarquia

- Diferencia de tamano entre niveles consecutivos: >= 1.25x
- H1 a H2, H2 a Body — cada salto debe ser visible
- Si dos niveles se ven iguales, la jerarquia falla
- Line-height: headings 1.1-1.2, body 1.5-1.6

## Componentes

### Botones

- Primario vs secundario vs ghost — 3 niveles claros de enfasis
- Disabled: opacidad 40%, cursor not-allowed, sin hover
- Tamano touch-friendly: minimo 44px de alto en mobile
- Hover: cambio sutil (color o sombra), nunca animacion dramatica

### Cards

- Sombra sutil de un solo nivel, no apilada
- Hover: sombra elevada, sin scale exagerado
- Borde con tinte del accent (no gris plano)
- Border-radius consistente con el resto del sistema

### Inputs

- Altura minima 48px (touch-friendly)
- Label fuera del input, nunca como placeholder que desaparece
- Placeholder a 40% opacidad, diferente del label
- Focus: anillo visible del color principal
- Error: borde rojo + mensaje contextual + icono

### Empty States

- Ilustracion o icono grande (80px+) con color reducido
- Titulo descriptivo ("No hay proyectos todavia", no "404" ni "Empty")
- CTA que resuelve el problema, no solo un enlace generico

### Loaders

- Skeleton (shimmer) para contenido que carga, no spinners
- Spinner solo para acciones muy cortas (< 3 segundos)
- Progress bar para operaciones con duracion estimable

## Layout

### Principios

- **Mobile-first**: disenar para 375px, expandir
- **Asimetria preferida**: grids con columnas desiguales (2fr 1fr, etc.)
- **Recorrido visual**: Z-pattern para paginas, F-pattern para listas densas
- **Proximidad**: elementos relacionados juntos, separados de otros grupos

### Spacing

Usar una escala consistente (4, 8, 16, 24, 32, 48) en vez de valores
arbitrarios. La relacion entre spacing tokens debe ser evidente (cada nivel
es ~1.5-2x el anterior).

### Responsive

- Mobile: 1 columna, full-width, nav colapsada
- Tablet: 2 columnas, sidebar colapsable
- Desktop: grid completo, sidebar expandida

### Anti-patterns de layout

- No usar carousel para contenido critico
- No apilar mas de 3 cards en fila en mobile
- No usar tablas densas en mobile — convertir a card list
- No esconder navegacion principal detras de menus obscuros

## Motion

### Filosofia

Las animaciones **comunican**, no decoran. Si una animacion no transmite
informacion (estado, relacion espacial, cambio), no es necesaria.

### Criterios

- Duracion base: 200-300ms para transiciones, 150ms para hover
- Entradas: slide + fade (no solo fade)
- Salidas: fade rapido (150ms) — el usuario ya decidio irse
- Hover en botones: 150ms, solo background y transform
- Listas: stagger de 50ms entre items, no todos a la vez
- Nunca animar propiedades que causen reflow — usar transform y opacity
- Preferir curvas ease-out para entradas, ease-in para salidas

## Como usar esta skill con stitch-mcp-cli

### Antes de generar pantallas

1. Verificar si existe `DESIGN.md` o `.stitch/metadata.json` en el proyecto
2. Si existe, extraer: paleta, fuente, roundness, color mode
3. Si no existe, sugerir ejecutar `stitch-mcp-cli design-md` primero
4. Aplicar los criterios de esta skill sobre la base del DESIGN.md

### Al generar con `stitch_generate_screen`

Incluir en el prompt las decisiones de diseño basadas en esta skill:

```
Genera una pantalla de [descripcion]. 

Design system:
- Atmosfera: [descripcion narrativa del tono visual]
- Colores: [paleta derivada del DESIGN.md con contexto semantico]
- Tipografia: [fuentes con jerarquia clara]
- Layout: [patron elegido con justificacion]
- Componentes: [specs segun los criterios de esta skill]
```

### Al exportar con `stitch_export_framework`

La skill no afecta la exportacion tecnica — los templates de framework
en `src/templates/` manejan eso. Pero si el agente necesita ajustar el
diseno antes de exportar, aplicar los criterios de color, tipografia y
componentes.
