---
description: Glass
---

# Glassmorphism SaaS Landing Page Workflow

## Description
This workflow guides the agent through creating a premium SaaS landing page using glassmorphism UI principles.
It ensures consistent design, readable code, responsive layout, and performance-conscious blur usage.
Use this workflow when building or scaffolding modern frontend landing pages.

---

## Step 1 — Context & Scope Confirmation

- Confirm the target stack:
  - React or Next.js
  - Tailwind CSS availability
- Confirm page scope:
  - Full landing page OR
  - Specific sections (hero, pricing, etc.)
- Do NOT assume additional requirements.
- If any detail is missing, ask a clarification question and STOP.

---

## Step 2 — Activate Relevant Skill

- Check available skills for UI and frontend design.
- Activate the **frontend-glassmorphism** skill.
- Read the full SKILL.md instructions before proceeding.
- Follow the design tokens, patterns, and decision tree defined in the skill.

---

## Step 3 — Page Structure Planning

- Propose a high-level page structure:
  - Hero
  - Social proof (logos or metrics)
  - Features (3–6 cards)
  - Pricing
  - FAQ
  - Final CTA
- Present the structure as a simple ordered list.
- WAIT for user approval before generating code.

---

## Step 4 — Hero Section Generation

- Generate a `HeroGlass.tsx` component.
- Requirements:
  - Glass card with backdrop blur
  - Clear headline and subtext
  - Primary + secondary CTA
  - Mobile responsive
- Keep the component self-contained.
- Do NOT generate unrelated components.

---

## Step 5 — Feature & Pricing Sections

- Generate:
  - `FeaturesGlass.tsx` (card-based grid)
  - `PricingGlass.tsx` (tiered cards)
- Each section must:
  - Use consistent glass surface styling
  - Respect spacing and readability
  - Avoid excessive animation or blur

---

## Step 6 — Performance & UX Check

- Review generated components for:
  - Overuse of blur or heavy shadows
  - Text contrast and readability
  - Responsive behavior
- If issues are found:
  - Adjust the components
  - Explain what was changed and why

---

## Step 7 — Final Output & Summary

- Present:
  - A list of generated files
  - Short usage instructions
  - Optional next steps (clearly marked as optional)
- Do NOT perform refactors or enhancements unless explicitly requested.

---

## Completion Rule

- Stop execution after Step 7.
- Do not extend scope.
- Do not add extra features.
