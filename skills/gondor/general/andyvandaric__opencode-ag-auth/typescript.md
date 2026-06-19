## 📘 TypeScript/JavaScript Development Rules

### Naming Conventions
| Context | Convention | Example |
|---------|------------|---------|
| Variables/functions | camelCase | `userList`, `handleClick` |
| Types/Interfaces/Classes | PascalCase | `UserService`, `TaskProps` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Files (Components) | PascalCase | `Button.tsx`, `TaskCard.tsx` |
| Files (Utilities) | camelCase/kebab | `utils.ts`, `crud.ts` |

### Function Naming (Verb-Noun Pattern)
```typescript
// ✅ GOOD: Verb-noun pattern
async function fetchUserData(userId: string) {}
function calculateTotal(items: Item[]) {}
function isValidEmail(email: string): boolean {}

// ❌ BAD: Unclear or noun-only
async function user(id: string) {}
function total(items) {}
function email(e) {}
```

### Type Safety

> **CRITICAL**: Never use `any` - use proper types or `unknown`.

```typescript
// ✅ GOOD: Proper types
interface Task {
  id: string;
  title: string;
  status: 'backlog' | 'doing' | 'done';
}

function getTask(id: string): Promise<Task> {}

// ❌ BAD: Using 'any'
function getTask(id: any): Promise<any> {}  // NEVER DO THIS
```

### Build & Test Commands
```bash
pnpm typecheck    # Type checking
pnpm test         # Run tests
pnpm build        # Production build
pnpm dev          # Dev server
```

### Best Practices
- Use TypeScript strict mode
- Define interfaces for all props and API responses
- Use `async/await` instead of `.then()` chains
- Prefer `const` over `let`, never use `var`
- Use named exports over default exports

---

## 🚫 Constants & Hardcoding Rules

> **CRITICAL**: Eliminate magic strings and hardcoded values.

### ❌ DO NOT
- Hardcode IDs, keys, or configuration values
- Repeat string literals across files
- Use magic numbers without named constants
- Define same constants in multiple components

### ✅ DO
- Create centralized constants file (e.g., `lib/constants.ts`, `config.rs`)
- Use enums or const objects for type safety
- Name constants descriptively: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS`
- Structure constants for i18n compatibility (labels separate from values)
- Import constants from shared module instead of redefining

### i18n-Ready Structure
```typescript
// ✅ GOOD - Ready for multi-language
export const PRIORITIES = [
  { value: 0, labelKey: "priority.critical" },
  { value: 1, labelKey: "priority.high" },
] as const;

// ❌ BAD - Hardcoded labels
const PRIORITIES = [
  { value: 0, label: "🔴 Critical" },
];
```

### Example Clean Structure
```
src-ui/
├── lib/
│   ├── constants.ts   # STATUSES, TYPES, PRIORITIES
│   ├── crud.ts        # invokeWithFeedback, createTask
│   └── i18n.ts        # t() function, translations
├── components/
│   └── TaskCard.tsx   # imports from lib/constants
```
