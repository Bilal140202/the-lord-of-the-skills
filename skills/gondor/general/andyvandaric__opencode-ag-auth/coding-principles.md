## 🎯 Universal Coding Principles

### Core Philosophy

**KISS (Keep It Simple)**
- Simplest solution that works
- Easy to understand > clever code
- Avoid premature optimization
- No over-engineering

**DRY (Don't Repeat Yourself)**
- Extract common logic into functions
- Create reusable components
- Share utilities across modules
- Avoid copy-paste programming

**YAGNI (You Aren't Gonna Need It)**
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

---

## 🔒 Immutability Pattern (CRITICAL)

```typescript
// ✅ ALWAYS use spread operator
const updatedUser = {
  ...user,
  name: 'New Name'
};

const updatedArray = [...items, newItem];

// ❌ NEVER mutate directly
user.name = 'New Name';  // BAD - breaks reactivity
items.push(newItem);     // BAD - mutation
```

```rust
// ✅ Rust: Clone if needed
let updated = Person { name: "New".to_string(), ..existing };

// ✅ Use .clone() for owned values when needed
let items_copy = items.clone();
```

---

## ⚠️ Error Handling Patterns

### TypeScript/JavaScript
```typescript
// ✅ GOOD: Comprehensive error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw new Error('Failed to fetch data');
  }
}
```

### Rust
```rust
// ✅ GOOD: Use Result<T, E> for fallible operations
fn read_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

// ✅ Use .map_err() to convert error types
fn process() -> Result<(), String> {
    read_file().map_err(|e| e.to_string())?;
    Ok(())
}
```

---

## ⚡ Async/Await Best Practices

```typescript
// ✅ GOOD: Parallel execution when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
]);

// ❌ BAD: Sequential when unnecessary (slower)
const users = await fetchUsers();
const markets = await fetchMarkets();  // Waits for users first!
const stats = await fetchStats();      // Waits for markets!
```

```rust
// ✅ Rust parallel with tokio
let (users, markets) = tokio::join!(
    fetch_users(),
    fetch_markets()
);
```

---

## 🌐 API Design Standards

### REST Conventions
```
GET    /api/items              # List all
GET    /api/items/:id          # Get one
POST   /api/items              # Create
PUT    /api/items/:id          # Update (full)
PATCH  /api/items/:id          # Update (partial)
DELETE /api/items/:id          # Delete

# Query parameters for filtering
GET /api/items?status=active&limit=10&offset=0
```

### Consistent Response Format
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  meta?: { total: number; page: number };
}

// Success
return { success: true, data: items };

// Error
return { success: false, error: 'Invalid request' };
```

### Input Validation (Zod)
```typescript
import { z } from 'zod';

const CreateItemSchema = z.object({
  name: z.string().min(1).max(200),
  priority: z.number().min(0).max(3),
  tags: z.array(z.string()).optional()
});

// Validate
const validated = CreateItemSchema.parse(requestBody);
```

---

## ⚡ Performance Patterns

### React/Solid Memoization
```typescript
// ✅ Memoize expensive computations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => b.score - a.score);
}, [items]);

// ✅ Memoize callbacks
const handleClick = useCallback(() => {
  doSomething();
}, []);
```

### Lazy Loading
```typescript
// ✅ Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));

<Suspense fallback={<Spinner />}>
  <HeavyChart />
</Suspense>
```

### Database/API
```typescript
// ✅ Select only needed columns
const { data } = await db.from('items').select('id, name, status').limit(10);

// ❌ Don't select everything
const { data } = await db.from('items').select('*');
```

---

## 🧪 Testing Standards (AAA Pattern)

```typescript
test('calculates total correctly', () => {
  // Arrange - Setup test data
  const items = [{ price: 10 }, { price: 20 }];

  // Act - Execute the function
  const total = calculateTotal(items);

  // Assert - Verify result
  expect(total).toBe(30);
});
```

### Test Naming
```typescript
// ✅ GOOD: Descriptive test names
test('returns empty array when no items match query', () => {});
test('throws error when API key is missing', () => {});

// ❌ BAD: Vague names
test('works', () => {});
test('test search', () => {});
```

---

## 🚨 Code Smell Detection

### 1. Long Functions (> 50 lines)
```typescript
// ❌ BAD: Monolithic function
function processData() { /* 100 lines */ }

// ✅ GOOD: Split into smaller functions
function processData() {
  const validated = validateData();
  const transformed = transformData(validated);
  return saveData(transformed);
}
```

### 2. Deep Nesting (> 3 levels)
```typescript
// ❌ BAD: 5+ levels of nesting
if (user) {
  if (user.isAdmin) {
    if (item) {
      if (item.isActive) {
        // Do something
      }
    }
  }
}

// ✅ GOOD: Early returns (guard clauses)
if (!user) return;
if (!user.isAdmin) return;
if (!item) return;
if (!item.isActive) return;
// Do something
```

### 3. Magic Numbers
```typescript
// ❌ BAD: Unexplained numbers
if (retryCount > 3) {}
setTimeout(callback, 500);

// ✅ GOOD: Named constants
const MAX_RETRIES = 3;
const DEBOUNCE_MS = 500;

if (retryCount > MAX_RETRIES) {}
setTimeout(callback, DEBOUNCE_MS);
```

---

## 💬 Comment Guidelines

### When to Comment (WHY, not WHAT)
```typescript
// ✅ GOOD: Explain WHY
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000);

// Deliberately using mutation here for performance with large arrays
items.push(newItem);

// ❌ BAD: Stating the obvious
// Increment counter by 1
count++;
```

### JSDoc for Public APIs
```typescript
/**
 * Searches items using fuzzy matching.
 *
 * @param query - Search query string
 * @param limit - Maximum results (default: 10)
 * @returns Array of items sorted by relevance
 * @throws {Error} If search index unavailable
 */
export function searchItems(query: string, limit = 10): Item[] {
  // Implementation
}
```

---

## 📏 File Size & Refactoring Rules

> Prevent files from becoming unmaintainable monoliths.

| Lines | Status | Action |
|-------|--------|--------|
| < 500 | ✅ OK | Normal development |
| 500-800 | ⚠️ WARN | Consider splitting |
| 800-1000 | 🔴 REVIEW | Notify user, plan refactor |
| 1000+ | 🚫 BLOCK | Refactor mandatory first |

### When to Split
- Single file handles multiple unrelated concerns
- Functions exceed 50 lines
- Class has > 10 public methods
- Too many imports at top of file

### Refactoring Strategies
```typescript
// ❌ BAD: Monolithic component
// components/Dashboard.tsx (1200 lines)

// ✅ GOOD: Split by concern
// components/Dashboard/
//   ├── Dashboard.tsx       (orchestrator, ~100 lines)
//   ├── DashboardHeader.tsx
//   ├── DashboardStats.tsx
//   ├── DashboardCharts.tsx
//   └── hooks/useDashboardData.ts
```
