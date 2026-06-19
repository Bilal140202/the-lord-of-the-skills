---
name: design-system
description: Rules for generating visual interfaces and parsing DESIGN.md files.
---

# UI/UX Generation Protocol

When generating graphical components, interfaces, or any front-end elements, you must follow this exact procedure:

## 1. Locate the Blueprint
Autonomously look for a `DESIGN.md` file in the root of the active workspace. This file dictates the absolute truth for typography, color tokens, margins, and the overall design system.

## 2. Remote Fallback (awesome-design-md)
If the user specifies a known brand style (e.g., "make it look like Vercel" or "Vercel style") and no local `DESIGN.md` exists, fetch the standard from `https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/[brand]/DESIGN.md` using web search or URL reading tools.

## 3. The "Minimal Glass" Protocol (Default Fallback)
If no `DESIGN.md` exists and no brand is specified:
- Never use solid primary colors.
- Use `bg-white/5` or `bg-black/40` with `backdrop-blur-xl`.
- Shadows must be subtle and layered.
- Add micro-animations on hover (`scale-105 duration-300`).
- Ensure WCAG AA contrast on overlays.
- Keep typography strictly modern (no Times New Roman, avoid standard Arial/Roboto if alternatives like Geist or Inter are available).
