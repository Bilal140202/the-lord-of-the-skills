# AGENTS.md (Antigravity-S2W)

## Repository Purpose

Antigravity-S2W is a VS Code extension that converts installed AI skill definition
folders (typically containing `SKILL.md`) into executable Antigravity workflow
Markdown files.

## Agent Operating Notes

- Prefer small, focused changes.
- Avoid adding new tooling unless requested.
- Do not `git commit` unless the user asks.

## Cursor / Copilot Rules

No Cursor rules were found (no `.cursor/rules/` or `.cursorrules`).
No Copilot instructions were found (no `.github/copilot-instructions.md`).

## Commands

### Install

- `npm ci` (preferred for CI/reproducible installs)
- `npm install` (acceptable for local development)

### Build

- `npm run compile` (Webpack dev build)
- `npm run watch` (Webpack watch)
- `npm run package` (Production build)
- `npm run vscode:prepublish` (Publish-time build)

### Lint

- `npm run lint` (ESLint over `src/**/*.ts`)

### Tests

- `npm test` (runs `node ./out/test/runTest.js`)
- `npm run pretest` (runs `compile-tests`, `compile`, `lint`)
- `npm run compile-tests` (compiles tests to `out/`)
- `npm run watch-tests` (watch test compilation)

#### Run A Single Test

This repo currently has no first-party test files checked in. If you add tests
(compiled to `out/test/`), run a single test file with:

```bash
npx mocha "out/test/yourTestFile.js"
```

Or run all compiled tests with a pattern:

```bash
npx mocha "out/test/**/*.js" --grep "pattern"
```

## Tech Stack

- TypeScript (`strict: true`), CommonJS, target ES6.
- Build via Webpack (Node target) + `ts-loader`.
- VS Code API externalized as `vscode` in webpack.
- ZIP handling uses `jszip`.

## System Architecture & Data Flow

This extension follows a **Model-View-Controller (MVC)** pattern:

1. **View (Frontend)**: `webview/` (HTML/JS/CSS). Runs in an iframe.
    - **Action**: User clicks button -> `vscode.postMessage({ command: 'install', ... })`
    - **Update**: Listens for `window.addEventListener('message', ...)` to update DOM.

2. **Controller (Backend)**: `SkillsViewProvider.ts`.
    - **Action**: Receives commands via `webview.onDidReceiveMessage`.
    - **Logic**: Dispatches to specific `Service` or `Installer`.
    - **Feedback**: Sends data back via `_view.webview.postMessage({ command: 'status', ... })`.

3. **Model (Services)**: `services/*.ts`.
    - **Logic**: Handles file I/O, Git operations, and Workflow generation.
    - **State**: Stateless mostly; relies on file system markers (`.davila-installed`, etc.).

---

## Project Layout & Responsibility

### 1. Application Layer (Backend)

| File | Responsibility |
| :--- | :--- |
| **`src/extension.ts`** | **Entry Point**. Registers `AntigravityS2W` command and activates `SkillsViewProvider`. |
| **`src/SkillsViewProvider.ts`** | **Main Controller**. Handles all Webview messages, manages lifecycle, and orchestrates services. |

### 2. Domain Services (Logic)

| File | Responsibility |
| :--- | :--- |
| **`src/services/WorkflowGenerator.ts`** | **Core Business Logic**. Scans skill folders and converting them to `.md` workflows. |
| **`src/services/PathManager.ts`** | **Configuration**. Single source of truth for `~/.gemini/antigravity/` paths. |
| **`src/services/*Installer.ts`** | **OneKey Installers**. Handles Git operations (Clone/Sparse Checkout) for specific skill sources. |

### 3. Presentation Layer (Frontend)

| File | Responsibility |
| :--- | :--- |
| **`src/webview/index.html`** | **Structure**. Defines the layout: OneKey tables, Manager grid, Modals. |
| **`src/webview/main.js`** | **Behavior**. Handles UI state, button clicks, and renders data received from Backend. |
| **`src/webview/style.css`** | **Appearance**. Implements "Refined Utility" theme, Grid layouts, and VS Code theme integration. |

```txt
# Quick Directory Reference
src/
├── extension.ts
├── SkillsViewProvider.ts
├── services/
│   ├── DavilaSkillsInstaller.ts
│   ├── AnthropicSkillsInstaller.ts
│   ├── SuperpowersInstaller.ts
│   ├── WorkflowGenerator.ts
│   └── PathManager.ts
└── webview/
    ├── index.html
    ├── main.js
    └── style.css
```

## Code Style Guidelines

### Formatting

- Indentation: tabs.
- Semicolons: required.
- Keep lines readable (aim ~100 chars).

### Imports

- Prefer namespace imports for Node/VS Code built-ins:
  - `import * as fs from "fs";`
  - `import * as path from "path";`
  - `import * as vscode from "vscode";`
- Local imports use relative paths.
- Prefer double quotes for new code; avoid quote-style churn.

### Naming

- Classes / types / interfaces: `PascalCase`.
- Functions / methods / variables: `camelCase`.
- Private VS Code provider fields: `_prefix` (e.g., `_view`).

### Types

- Keep strict TypeScript compatibility.
- Add explicit return types for exported/public methods.
- Prefer precise types over `any` (use `any` only when unavoidable).
- Async APIs return `Promise<T>`.

### Error Handling

- Use `try/catch` around file I/O, network calls, and workflow generation.
- Prefer `catch (e: any)` when you need `e.message`.
- Log unexpected errors via `console.error(...)`.
- User-facing errors should use `vscode.window.showErrorMessage(...)`.
- Webview errors should use `postMessage({ command: "status", type: "error", ... })`.

### File I/O

- Existence checks: `fs.existsSync(...)`.
- Create directories: `fs.mkdirSync(dir, { recursive: true })`.
- Remove files/folders: `fs.rmSync(path, { recursive: true, force: true })`.
- Prefer `path.join(...)` and `path.normalize(...)`.

### Async/Await

- Prefer `async/await` over raw Promises.
- Prefer `fs.promises.*` in async code.

### VS Code Patterns

- Commands are registered in `src/extension.ts`.
- Webview message handling uses `switch (data.command)`.
- Open files via `vscode.commands.executeCommand("vscode.open", uri)`.

### JSZip / TypeScript Interop

- `@ts-ignore` is acceptable only for known JSZip typing mismatches.
- Keep ignores localized and justified by types.

## Domain Notes

### Architecture Change (v0.3.0+)

- **Layer 2 Operations**: The extension now operates directly on "Layer 2" skills (raw skill folders/files).
- **No Conversion**: The "Layer 1" conversion logic (symlinks, `~/.antigravity/` intermediate folder) has been removed.
- **Direct Download**: Skills are downloaded directly from GitHub to the target directory using Sparse Checkout.

### IDE & Target Environment Support (v0.5.0+)

- **Target IDE Selection**: Supports writing workflows in specific formats based on the requested Target Agent (`.gemini`, `.github`, `.agents`, etc.).
- **Installation Modes**: Workflows can now be generated globally (`os.homedir()`) or locally relative to `vscode.workspace.workspaceFolders`.

### Skill Sources & Paths

- **Standard Path**: `~/.gemini/antigravity/skills/`
- **Prefix Policy**: No vendor prefixes (e.g., `superpowers_` is removed). Skills are installed with their original directory names.

### OneKey Install System

- **Supported Sources**:
  1. **Superpowers**: `obra/superpowers`
  2. **Anthropic Skills**: `anthropics/skills`
  3. **Community Skills (Davila7)**: `davila7/claude-code-templates` (Categorized)
- **Sync Mechanism**:
  - **Apply Changes**: Synchronizes selected categories (Install/Uninstall) in one batch.
  - **Manual Update**: `↻` buttons trigger a re-download/update from GitHub. Auto-update on startup is disabled.
- **UI Feedback**: Unified status reporting via `onekey-status` bar in the Webview.

### Output Location

Generated workflows (`.md` files) are written to:

- `~/.gemini/antigravity/global_workflows/`

## Generated Artifacts

- `dist/` is the webpack output.
- `out/` is the TypeScript output for tests.
- Both are ignored via `.gitignore`.
