# Frontend — Kanban Studio

## Overview

Next.js 16 (App Router) app: login (`AuthGate`), authenticated Kanban board backed by FastAPI (`/api/*`), and a docked **AI chat** sidebar (`ChatSidebar`) that calls `POST /api/chat` and refreshes board state when the model returns mutations.

## Stack

| Concern | Choice |
|---|---|
| Framework | Next.js 16, App Router, TypeScript |
| Styling | Tailwind CSS v4 (`@import "tailwindcss"` via PostCSS) |
| Drag and drop | @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities |
| Utility | clsx |
| Unit / integration tests | Vitest 3 + @testing-library/react + jsdom |
| E2E tests | Playwright |

## Directory Structure (high level)

```
frontend/
├── src/
│   ├── app/                 # layout, globals.css, page (AuthGate + KanbanBoard), login
│   ├── components/
│   │   ├── KanbanBoard.tsx  # Loads board from API, DnD, header, chat toggle
│   │   ├── KanbanColumn.tsx # Droppable column, equal-height row on lg, scrollable card list
│   │   ├── KanbanCard.tsx, KanbanCardPreview.tsx, NewCardForm.tsx
│   │   ├── ChatSidebar.tsx  # Session chat UI; sendChat; onBoardSynced(board)
│   │   ├── AuthGate.tsx
│   │   └── *.test.tsx
│   ├── lib/
│   │   ├── kanban.ts        # Types, initialData (seed parity), moveCard, findCardPlacement
│   │   ├── api.ts           # fetchBoard, persistBoard, column/card routes, sendChat
│   │   └── session.ts       # login/logout helpers
│   └── test/setup.ts        # jest-dom; scrollIntoView stub for jsdom
└── tests/                   # Playwright specs
```

## Data flow

- After login, `KanbanBoard` loads with `GET /api/board` (`fetchBoard`). Mutations use granular APIs in `api.ts`; responses include `{ board }` where applicable.
- `sendChat(message, history)` posts to `/api/chat` with `credentials: "include"`. Prior turns go in `history`; the current user text is only in `message` (matches backend contract).
- When `mutations_applied` is non-empty, `ChatSidebar` calls `onBoardSynced(data.board)` so the UI updates without a full refetch.

## Key components

### KanbanBoard
- Client state from API; debounced column rename; drag uses `patchCard` with `column_id` + `index`.
- Header: **AI chat** opens/closes `ChatSidebar` (button hidden while open; **Close** inside sidebar).
- Layout: `main` + sidebar in a flex row; when chat is open, `main` uses full width up to the sidebar (`max-w-none`).

### ChatSidebar
- Message list, composer, loading and error states; scroll stays inside the message panel (no `scrollIntoView` on the document).

### KanbanColumn
- `h-full` in the board grid; card area `flex-1 min-h-0 overflow-y-auto`; **Add a card** pinned with `mt-auto` so column footers align on large screens.

## Design tokens (globals.css)

| Variable | Value | Use |
|---|---|---|
| `--color-accent` | `#ecad0a` | Accent lines, highlights |
| `--color-primary` | `#209dd7` | Links, key sections |
| `--color-secondary` | `#753991` | Submit buttons, important actions |
| `--color-navy` | `#032147` | Main headings |
| `--color-gray` | `#888888` | Supporting text, labels |

## Tests

```
npm run test:unit
npm run test:e2e
npm run test:all
```

Unit tests mock `fetch` for board and chat routes where needed.
