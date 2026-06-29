# Code Style

# Naming Conventions

## Variables and Functions

```typescript
// camelCase for variables and functions
const userName = 'John';
const isActive = true;
const itemCount = 42;

function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Boolean variables: use is/has/can/should prefix
const isValid = validate(input);
const hasPermission = checkPermission(user);
const canEdit = user.role === 'admin';
const shouldRetry = error.code === 'TIMEOUT';

// Collections: use plural names
const users = getUsers();
const activeOrders = orders.filter(o => o.status === 'active');
```

## Constants

```typescript
// UPPER_SNAKE_CASE for constants
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT_MS = 5000;
const API_BASE_URL = 'https://api.example.com';

// Enum-like objects
const ORDER_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled'
} as const;

const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  NOT_FOUND: 404
} as const;
```

## Classes and Types

```typescript
// PascalCase for classes and types
class UserService {
  constructor(private userRepository: UserRepository) {}
}

interface User {
  id: string;
  name: string;
  email: string;
}

type UserRole = 'admin' | 'editor' | 'viewer';

// Avoid prefixes
// ❌ IUser, CUser, TUser
// ✅ User
```

## Files and Modules

```typescript
// kebab-case for files
user-service.ts
order-repository.ts
create-user.dto.ts

// Match file name to primary export
// user-service.ts exports UserService
// order-repository.ts exports OrderRepository
```

## Avoid Bad Names

```typescript
// ❌ Bad - unclear
const d = Date.now();
const tmp = user.name;
const data = fetchData();
const flag = true;

// ✅ Good - descriptive
const currentDate = Date.now();
const originalUserName = user.name;
const customerOrders = fetchCustomerOrders();
const isEmailVerified = true;
```

## Avoid Magic Numbers

```typescript
// ❌ Magic numbers
if (user.age >= 18) { ... }
if (items.length > 100) { ... }
setTimeout(callback, 5000);

// ✅ Named constants
const LEGAL_AGE = 18;
const MAX_BATCH_SIZE = 100;
const DEFAULT_TIMEOUT_MS = 5000;

if (user.age >= LEGAL_AGE) { ... }
if (items.length > MAX_BATCH_SIZE) { ... }
setTimeout(callback, DEFAULT_TIMEOUT_MS);
```

## Consistency

```typescript
// Pick ONE style and stick with it across the project

// ✅ Consistent camelCase in APIs
{
  "userId": 123,
  "firstName": "John",
  "createdAt": "2024-01-01"
}

// ❌ Mixed styles
{
  "user_id": 123,      // snake_case
  "firstName": "John", // camelCase - inconsistent!
}
```


---

# Code Organization

## Function Length

```typescript
// ❌ Function too long (>50 lines)
function processOrder(orderId: string) {
  // 200 lines of validation, payment, inventory, shipping...
}

// ✅ Extract into smaller, focused functions
function processOrder(orderId: string) {
  const order = fetchOrder(orderId);

  validateOrder(order);
  reserveInventory(order.items);
  processPayment(order);
  scheduleShipping(order);
  sendConfirmation(order.customer.email);

  return order;
}
```

## Nesting Depth

```typescript
// ❌ Too much nesting (>3 levels)
if (user) {
  if (user.isActive) {
    if (user.hasPermission('edit')) {
      if (resource.isAvailable) {
        // Deep nesting is hard to follow
      }
    }
  }
}

// ✅ Guard clauses to reduce nesting
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission('edit')) return;
if (!resource.isAvailable) return;

// Clear logic at top level

// ✅ Extract complex conditions
function canEditResource(user: User, resource: Resource): boolean {
  return user &&
         user.isActive &&
         user.hasPermission('edit') &&
         resource.isAvailable;
}

if (canEditResource(user, resource)) {
  // Single level of nesting
}
```

## File Length

```typescript
// ❌ God file (1000+ lines)
// user-service.ts with 50 methods handling users, auth, permissions...

// ✅ Split into focused modules (~200-300 lines each)
// user-service.ts - CRUD operations
// auth-service.ts - login, logout, tokens
// permission-service.ts - role checks
```

## File Organization

```typescript
// Consistent structure within files:

// 1. Imports (grouped and ordered)
import fs from 'fs';                    // Standard library
import express from 'express';          // External dependencies
import { UserService } from './user';   // Internal modules

// 2. Constants and type definitions
const MAX_RETRIES = 3;

interface UserDTO {
  id: string;
  name: string;
}

// 3. Helper functions (if needed)
function validateInput(input: unknown): boolean {
  // ...
}

// 4. Main exports/classes
export class OrderService {
  // ...
}

// 5. Module initialization (if applicable)
export default new OrderService();
```

## Single Responsibility

```typescript
// ❌ Class doing too much
class UserManager {
  createUser() {}
  updateUser() {}
  sendEmail() {}
  hashPassword() {}
  generateToken() {}
}

// ✅ Split by responsibility
class UserRepository {
  create(user: User) {}
  update(id: string, data: Partial<User>) {}
}

class EmailService {
  send(to: string, template: string) {}
}

class PasswordService {
  hash(password: string): string {}
  verify(password: string, hash: string): boolean {}
}

class AuthService {
  generateToken(userId: string): string {}
}
```

## DRY (Don't Repeat Yourself)

```typescript
// ❌ Duplicated logic
function processUserOrder(order: Order) {
  const total = order.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const tax = total * 0.08;
  return total + tax;
}

function processGuestOrder(order: Order) {
  const total = order.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const tax = total * 0.08;
  return total + tax;
}

// ✅ Extract common logic
function calculateOrderTotal(items: Item[]): number {
  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const tax = subtotal * 0.08;
  return subtotal + tax;
}

function processUserOrder(order: Order) {
  return calculateOrderTotal(order.items);
}
```
