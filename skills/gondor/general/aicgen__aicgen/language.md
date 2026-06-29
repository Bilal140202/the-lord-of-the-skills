# Language

# TypeScript Fundamentals

## Strict Mode (Required)

Always use strict mode in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

## Type Annotations

Use explicit types for clarity:

```typescript
// Function signatures
function calculateTotal(items: CartItem[], taxRate: number): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * (1 + taxRate);
}

// Variable declarations
const userName: string = "Alice";
const age: number = 30;
const isActive: boolean = true;
```

## Avoid `any`

Never use `any` - use `unknown` with type guards:

```typescript
// ❌ Bad
function processData(data: any) {
  return data.value;
}

// ✅ Good
function processData(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return String(data.value);
  }
  throw new Error('Invalid data structure');
}
```

## Type Guards

Implement custom type guards:

```typescript
interface User {
  id: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    typeof value.id === 'string' &&
    typeof value.email === 'string'
  );
}

// Usage
if (isUser(data)) {
  console.log(data.email); // Type: User
}
```

## Naming Conventions

- Classes/Interfaces: `PascalCase`
- Functions/Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Files: `kebab-case.ts`
- No `I` prefix for interfaces


---

# Async/Await Patterns

## Prefer async/await

Always use async/await over promise chains:

```typescript
// ✅ Good
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return await response.json();
}

// ❌ Avoid
function fetchUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`)
    .then(res => res.json());
}
```

## Error Handling

Always wrap async operations in try/catch:

```typescript
async function safeOperation(): Promise<Result> {
  try {
    const data = await riskyOperation();
    return { success: true, data };
  } catch (error) {
    logger.error('Operation failed', error);
    return { success: false, error: error.message };
  }
}
```

## Parallel Execution

Use `Promise.all()` for independent operations:

```typescript
// ✅ Good - parallel (fast)
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments()
]);

// ❌ Bad - sequential (slow)
const users = await fetchUsers();
const posts = await fetchPosts();
const comments = await fetchComments();
```

## Handling Failures

Use `Promise.allSettled()` when some failures are acceptable:

```typescript
const results = await Promise.allSettled([
  fetchData1(),
  fetchData2(),
  fetchData3()
]);

results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`Success ${index}:`, result.value);
  } else {
    console.error(`Failed ${index}:`, result.reason);
  }
});
```

## Retry Pattern

Implement retry with exponential backoff:

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxRetries - 1) {
        const delay = 1000 * Math.pow(2, attempt);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
}
```


---

# TypeScript Types & Interfaces

## Prefer Interfaces for Public APIs

```typescript
// ✅ Use interfaces for object shapes
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// ✅ Use type aliases for unions and complex types
type UserRole = 'admin' | 'editor' | 'viewer';
type ResponseHandler = (response: Response) => void;
```

## Discriminated Unions

```typescript
// ✅ Use discriminated unions for variant types
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handleResult(result: Result<User>) {
  if (result.success) {
    console.log(result.data.name); // TypeScript knows data exists
  } else {
    console.error(result.error); // TypeScript knows error exists
  }
}
```

## Utility Types

```typescript
// Use built-in utility types
type PartialUser = Partial<User>;           // All fields optional
type RequiredUser = Required<User>;         // All fields required
type ReadonlyUser = Readonly<User>;         // All fields readonly
type UserKeys = keyof User;                 // 'id' | 'name' | 'email' | 'createdAt'
type PickedUser = Pick<User, 'id' | 'name'>; // Only id and name
type OmittedUser = Omit<User, 'createdAt'>; // Everything except createdAt
```

## Type Guards

```typescript
// ✅ Use type guards for runtime checking
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Usage
const data: unknown = fetchData();
if (isUser(data)) {
  console.log(data.email); // TypeScript knows it's a User
}
```

## Avoid `any`

```typescript
// ❌ Never use any
function process(data: any) {
  return data.name; // No type safety
}

// ✅ Use unknown with type guards
function process(data: unknown) {
  if (isUser(data)) {
    return data.name; // Type-safe
  }
  throw new Error('Invalid data');
}
```


---

# TypeScript Generics

## Basic Generic Functions

```typescript
// ✅ Generic function for type-safe operations
function first<T>(array: T[]): T | undefined {
  return array[0];
}

const numbers = [1, 2, 3];
const firstNumber = first(numbers); // Type: number | undefined

const users = [{ name: 'John' }];
const firstUser = first(users); // Type: { name: string } | undefined
```

## Generic Interfaces

```typescript
// ✅ Generic repository pattern
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(entity: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    return this.db.users.findUnique({ where: { id } });
  }
  // ... other methods
}
```

## Generic Constraints

```typescript
// ✅ Constrain generic types
interface HasId {
  id: string;
}

function getById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Works with any type that has an id
getById(users, '123');
getById(products, '456');
```

## Mapped Types

```typescript
// ✅ Create transformed types
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

type NullableUser = Nullable<User>;
// { id: string | null; name: string | null; ... }

// ✅ Conditional types
type ExtractArrayType<T> = T extends Array<infer U> ? U : never;

type StringArrayElement = ExtractArrayType<string[]>; // string
```

## Default Generic Parameters

```typescript
// ✅ Provide defaults for flexibility
interface ApiResponse<T = unknown, E = Error> {
  data?: T;
  error?: E;
  status: number;
}

// Can use with or without type parameters
const response1: ApiResponse<User> = { data: user, status: 200 };
const response2: ApiResponse = { status: 500, error: new Error('Failed') };
```


---

# TypeScript Error Handling

## Custom Error Classes

```typescript
// ✅ Create structured error hierarchy
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public details?: unknown
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 404, 'NOT_FOUND', { resource, id });
  }
}

class ValidationError extends AppError {
  constructor(message: string, details: unknown) {
    super(message, 400, 'VALIDATION_ERROR', details);
  }
}
```

## Async Error Handling

```typescript
// ✅ Always handle promise rejections
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      throw new NotFoundError('User', id);
    }
    throw new AppError('Failed to fetch user', 500, 'FETCH_ERROR', { userId: id });
  }
}

// ✅ Use wrapper for Express async handlers
const asyncHandler = (fn: RequestHandler) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
```

## Result Type Pattern

```typescript
// ✅ Explicit success/failure without exceptions
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

function parseJSON<T>(json: string): Result<T, string> {
  try {
    return { success: true, value: JSON.parse(json) };
  } catch {
    return { success: false, error: 'Invalid JSON' };
  }
}

// Usage
const result = parseJSON<User>(data);
if (result.success) {
  console.log(result.value.name);
} else {
  console.error(result.error);
}
```

## Centralized Error Handler

```typescript
// ✅ Express error middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { message: err.message, code: err.code, details: err.details }
    });
  }

  console.error('Unexpected error:', err);
  res.status(500).json({
    error: { message: 'Internal server error', code: 'INTERNAL_ERROR' }
  });
});
```


---

# TypeScript Testing

## Test Structure: Arrange-Act-Assert

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with hashed password', async () => {
      // Arrange
      const userData = { email: 'test@example.com', password: 'password123' };
      const mockRepo = { save: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
      const service = new UserService(mockRepo);

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result.id).toBe('1');
      expect(mockRepo.save).toHaveBeenCalledWith(
        expect.objectContaining({ email: 'test@example.com' })
      );
    });
  });
});
```

## Test Observable Behavior, Not Implementation

```typescript
// ❌ Testing implementation details
it('should call validateEmail method', () => {
  const spy = jest.spyOn(service, 'validateEmail');
  service.createUser({ email: 'test@example.com' });
  expect(spy).toHaveBeenCalled(); // Brittle - breaks if refactored
});

// ✅ Testing observable behavior
it('should reject invalid email', async () => {
  await expect(
    service.createUser({ email: 'invalid' })
  ).rejects.toThrow('Invalid email');
});
```

## Test Doubles

```typescript
// Stub: Returns canned responses
const stubDatabase = {
  findUser: () => ({ id: '1', name: 'Test User' })
};

// Mock: Pre-programmed with expectations
const mockPayment = {
  charge: jest.fn()
    .mockResolvedValueOnce({ success: true })
    .mockResolvedValueOnce({ success: false })
};

// Fake: Working implementation (not for production)
class FakeDatabase implements Database {
  private data = new Map<string, any>();

  async save(id: string, data: any) { this.data.set(id, data); }
  async find(id: string) { return this.data.get(id); }
}
```

## One Test Per Condition

```typescript
// ❌ Multiple assertions for different scenarios
it('should validate user input', () => {
  expect(() => validate({ age: -1 })).toThrow();
  expect(() => validate({ age: 200 })).toThrow();
  expect(() => validate({ name: '' })).toThrow();
});

// ✅ One test per condition
it('should reject negative age', () => {
  expect(() => validate({ age: -1 })).toThrow('Age must be positive');
});

it('should reject age over 150', () => {
  expect(() => validate({ age: 200 })).toThrow('Age must be under 150');
});
```

## Keep Tests Independent

```typescript
// ✅ Each test is self-contained
it('should update user', async () => {
  const user = await service.createUser({ name: 'Test' });
  const updated = await service.updateUser(user.id, { name: 'Updated' });
  expect(updated.name).toBe('Updated');
});
```


---

# TypeScript Configuration

## tsconfig.json Best Practices

```json
{
  "compilerOptions": {
    // Strict type checking
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,

    // Module resolution
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "resolveJsonModule": true,

    // Output
    "target": "ES2022",
    "outDir": "./dist",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Path aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@services/*": ["src/services/*"],
      "@models/*": ["src/models/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Path Aliases Setup

```typescript
// With path aliases configured:
import { UserService } from '@services/user';
import { User } from '@models/user';

// Instead of relative paths:
import { UserService } from '../../../services/user';
```

## Project References (Monorepo)

```json
// packages/shared/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist"
  }
}

// packages/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "references": [
    { "path": "../shared" }
  ]
}
```

## Environment-Specific Configs

```json
// tsconfig.build.json - for production builds
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "sourceMap": false,
    "removeComments": true
  },
  "exclude": ["**/*.test.ts", "**/*.spec.ts"]
}
```


---

# TypeScript Performance

## Choose Right Data Structures

```typescript
// ❌ Array for lookups (O(n))
const users: User[] = [];
const findUser = (id: string) => users.find(u => u.id === id);

// ✅ Map for O(1) lookups
const users = new Map<string, User>();
const findUser = (id: string) => users.get(id);

// ❌ Array for membership checks
const hasPermission = (perms: string[], perm: string) => perms.includes(perm);

// ✅ Set for O(1) membership
const hasPermission = (perms: Set<string>, perm: string) => perms.has(perm);
```

## Avoid N+1 Queries

```typescript
// ❌ N+1 queries
const getOrdersWithCustomers = async () => {
  const orders = await db.query('SELECT * FROM orders');
  for (const order of orders) {
    order.customer = await db.query('SELECT * FROM customers WHERE id = ?', [order.customerId]);
  }
  return orders;
};

// ✅ Single JOIN query
const getOrdersWithCustomers = async () => {
  return db.query(`
    SELECT orders.*, customers.name as customer_name
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
  `);
};

// ✅ Using ORM with eager loading
const getOrdersWithCustomers = async () => {
  return orderRepository.find({ relations: ['customer'] });
};
```

## Parallel Execution

```typescript
// ❌ Sequential (slow)
const getUserData = async (userId: string) => {
  const user = await fetchUser(userId);       // 100ms
  const posts = await fetchPosts(userId);     // 150ms
  const comments = await fetchComments(userId); // 120ms
  return { user, posts, comments }; // Total: 370ms
};

// ✅ Parallel (fast)
const getUserData = async (userId: string) => {
  const [user, posts, comments] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchComments(userId)
  ]);
  return { user, posts, comments }; // Total: 150ms
};
```

## Memoization

```typescript
const memoize = <T extends (...args: any[]) => any>(fn: T): T => {
  const cache = new Map<string, ReturnType<T>>();

  return ((...args: any[]) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
};

const expensiveCalc = memoize((n: number) => {
  // Expensive computation
  return result;
});
```

## Batch Processing

```typescript
// ✅ Process in batches
const processUsers = async (userIds: string[]) => {
  const BATCH_SIZE = 50;

  for (let i = 0; i < userIds.length; i += BATCH_SIZE) {
    const batch = userIds.slice(i, i + BATCH_SIZE);
    await Promise.all(batch.map(id => updateUser(id)));
  }
};
```
