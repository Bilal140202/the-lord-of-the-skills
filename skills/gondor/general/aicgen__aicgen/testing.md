# Testing

# Unit Testing Fundamentals

## Arrange-Act-Assert Pattern

```typescript
describe('UserService', () => {
  it('should create user with hashed password', async () => {
    // Arrange - Set up test data and dependencies
    const userData = { email: 'test@example.com', password: 'secret123' };
    const mockRepo = { save: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
    const service = new UserService(mockRepo);

    // Act - Execute the behavior being tested
    const result = await service.createUser(userData);

    // Assert - Verify the outcomes
    expect(result.id).toBe('1');
    expect(mockRepo.save).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'test@example.com' })
    );
  });
});
```

## Test Observable Behavior, Not Implementation

```typescript
// ❌ Bad: Testing implementation details
it('should call validateEmail method', () => {
  const spy = jest.spyOn(service, 'validateEmail');
  service.createUser({ email: 'test@example.com' });
  expect(spy).toHaveBeenCalled();
});

// ✅ Good: Testing observable behavior
it('should reject invalid email', async () => {
  await expect(
    service.createUser({ email: 'invalid-email' })
  ).rejects.toThrow('Invalid email format');
});

it('should accept valid email', async () => {
  const result = await service.createUser({ email: 'valid@example.com' });
  expect(result.email).toBe('valid@example.com');
});
```

## One Assertion Per Test Concept

```typescript
// ❌ Bad: Multiple unrelated assertions
it('should validate user input', () => {
  expect(() => validate({ age: -1 })).toThrow();
  expect(() => validate({ age: 200 })).toThrow();
  expect(() => validate({ name: '' })).toThrow();
});

// ✅ Good: One test per scenario
it('should reject negative age', () => {
  expect(() => validate({ age: -1 })).toThrow('Age must be positive');
});

it('should reject age over 150', () => {
  expect(() => validate({ age: 200 })).toThrow('Age must be under 150');
});

it('should reject empty name', () => {
  expect(() => validate({ name: '' })).toThrow('Name is required');
});
```

## Descriptive Test Names

```typescript
// ❌ Vague names
it('should work correctly', () => {});
it('handles edge case', () => {});

// ✅ Descriptive names - describe the scenario and expected outcome
it('should return empty array when no users match filter', () => {});
it('should throw ValidationError when email is empty', () => {});
it('should retry failed payment up to 3 times before giving up', () => {});
```

## Tests Should Be Independent

```typescript
// ❌ Bad: Tests depend on each other
let userId: string;

it('should create user', async () => {
  const user = await service.createUser(data);
  userId = user.id; // Shared state!
});

it('should update user', async () => {
  await service.updateUser(userId, newData); // Depends on previous test
});

// ✅ Good: Each test is self-contained
it('should update user', async () => {
  const user = await service.createUser(data);
  const updated = await service.updateUser(user.id, newData);
  expect(updated.name).toBe(newData.name);
});
```

## Test Edge Cases

```typescript
describe('divide', () => {
  it('should divide two positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should throw when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  it('should return zero when numerator is zero', () => {
    expect(divide(0, 5)).toBe(0);
  });
});
```


---

# Test Doubles and Mocking

## Types of Test Doubles

```typescript
// STUB: Returns canned responses
const stubUserRepo = {
  findById: () => ({ id: '1', name: 'Test User' })
};

// MOCK: Pre-programmed with expectations
const mockPaymentGateway = {
  charge: jest.fn()
    .mockResolvedValueOnce({ success: true, transactionId: 'tx1' })
    .mockResolvedValueOnce({ success: false, error: 'Declined' })
};

// SPY: Records calls for verification
const spy = jest.spyOn(emailService, 'send');

// FAKE: Working implementation (not for production)
class FakeDatabase implements Database {
  private data = new Map<string, any>();

  async save(id: string, entity: any) { this.data.set(id, entity); }
  async find(id: string) { return this.data.get(id); }
}
```

## When to Mock

```typescript
// ✅ Mock external services (APIs, databases)
const mockHttpClient = {
  get: jest.fn().mockResolvedValue({ data: userData })
};

// ✅ Mock time-dependent operations
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-15'));

// ✅ Mock random/non-deterministic functions
jest.spyOn(Math, 'random').mockReturnValue(0.5);

// ❌ Don't mock the code you're testing
// ❌ Don't mock simple data structures
```

## Mock Verification

```typescript
it('should send welcome email after registration', async () => {
  const mockEmail = { send: jest.fn().mockResolvedValue(true) };
  const service = new UserService({ emailService: mockEmail });

  await service.register({ email: 'new@example.com' });

  expect(mockEmail.send).toHaveBeenCalledWith({
    to: 'new@example.com',
    template: 'welcome',
    subject: 'Welcome!'
  });
  expect(mockEmail.send).toHaveBeenCalledTimes(1);
});
```

## Partial Mocks

```typescript
// Mock only specific methods
const service = new OrderService();

jest.spyOn(service, 'validateOrder').mockReturnValue(true);
jest.spyOn(service, 'calculateTotal').mockReturnValue(100);
// Other methods use real implementation

const result = await service.processOrder(orderData);
expect(result.total).toBe(100);
```

## Resetting Mocks

```typescript
describe('PaymentService', () => {
  const mockGateway = { charge: jest.fn() };
  const service = new PaymentService(mockGateway);

  beforeEach(() => {
    jest.clearAllMocks(); // Clear call history
    // or jest.resetAllMocks() to also reset return values
  });

  it('should process payment', async () => {
    mockGateway.charge.mockResolvedValue({ success: true });
    await service.charge(100);
    expect(mockGateway.charge).toHaveBeenCalledTimes(1);
  });
});
```

## Mock Modules

```typescript
// Mock entire module
jest.mock('./email-service', () => ({
  EmailService: jest.fn().mockImplementation(() => ({
    send: jest.fn().mockResolvedValue(true)
  }))
}));

// Mock with partial implementation
jest.mock('./config', () => ({
  ...jest.requireActual('./config'),
  API_KEY: 'test-key'
}));
```


---

# Integration Testing

## Testing Real Dependencies

```typescript
describe('UserRepository Integration', () => {
  let db: Database;
  let repository: UserRepository;

  beforeAll(async () => {
    db = await createTestDatabase();
    repository = new UserRepository(db);
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear('users'); // Clean slate for each test
  });

  it('should persist and retrieve user', async () => {
    const userData = { email: 'test@example.com', name: 'Test User' };

    const created = await repository.create(userData);
    const found = await repository.findById(created.id);

    expect(found).toEqual(expect.objectContaining(userData));
  });
});
```

## API Integration Tests

```typescript
describe('POST /api/users', () => {
  let app: Express;
  let db: Database;

  beforeAll(async () => {
    db = await createTestDatabase();
    app = createApp(db);
  });

  afterEach(async () => {
    await db.clear('users');
  });

  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'new@example.com', name: 'New User' })
      .expect(201);

    expect(response.body.data).toEqual(
      expect.objectContaining({
        email: 'new@example.com',
        name: 'New User'
      })
    );

    // Verify in database
    const user = await db.findOne('users', { email: 'new@example.com' });
    expect(user).toBeTruthy();
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## Database Transaction Testing

```typescript
describe('OrderService Integration', () => {
  it('should rollback on payment failure', async () => {
    const order = await orderService.createOrder({ items: [...] });

    // Mock payment to fail
    paymentGateway.charge.mockRejectedValue(new Error('Declined'));

    await expect(
      orderService.processOrder(order.id)
    ).rejects.toThrow('Payment failed');

    // Verify order status unchanged
    const updatedOrder = await orderRepository.findById(order.id);
    expect(updatedOrder.status).toBe('pending');

    // Verify inventory not deducted
    const inventory = await inventoryRepository.findByProductId(productId);
    expect(inventory.quantity).toBe(originalQuantity);
  });
});
```

## Test Data Builders

```typescript
class UserBuilder {
  private data: Partial<User> = {
    email: 'default@example.com',
    name: 'Default User',
    role: 'user'
  };

  withEmail(email: string) { this.data.email = email; return this; }
  withRole(role: string) { this.data.role = role; return this; }
  asAdmin() { this.data.role = 'admin'; return this; }

  build(): User { return this.data as User; }

  async save(db: Database): Promise<User> {
    return db.insert('users', this.data);
  }
}

// Usage
const admin = await new UserBuilder()
  .withEmail('admin@example.com')
  .asAdmin()
  .save(db);
```

## Test Isolation

```typescript
// Use transactions that rollback
describe('IntegrationTests', () => {
  beforeEach(async () => {
    await db.beginTransaction();
  });

  afterEach(async () => {
    await db.rollbackTransaction();
  });
});

// Or use test containers
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container: PostgreSqlContainer;

beforeAll(async () => {
  container = await new PostgreSqlContainer().start();
  db = await connect(container.getConnectionUri());
});

afterAll(async () => {
  await container.stop();
});
```


---

# Testing Basics

## Your First Unit Test

A unit test verifies that a small piece of code works correctly.

```pseudocode
// Function to test
function add(a, b):
    return a + b

// Test for the function
test "add should sum two numbers":
    result = add(2, 3)
    expect result equals 5
```

## Test Structure

Every test has three parts:

1. **Setup** - Prepare what you need
2. **Execute** - Run the code
3. **Verify** - Check the result

```pseudocode
test "should create user with name":
    // 1. Setup
    userName = "Alice"

    // 2. Execute
    user = createUser(userName)

    // 3. Verify
    expect user.name equals "Alice"
```

## Common Assertions

```pseudocode
// Equality
expect value equals 5
expect value equals { id: 1 }

// Truthiness
expect value is truthy
expect value is falsy
expect value is null
expect value is undefined

// Numbers
expect value > 3
expect value < 10

// Strings
expect text contains "hello"

// Arrays/Lists
expect array contains item
expect array length equals 3
```

## Testing Expected Errors

```pseudocode
test "should throw error for invalid input":
    expect error when:
        divide(10, 0)
    with message "Cannot divide by zero"
```

## Async Tests

```pseudocode
test "should fetch user data" async:
    user = await fetchUser(123)
    expect user.id equals 123
```

## Test Naming

Use clear, descriptive names:

```pseudocode
// ❌ Bad
test "test1"
test "it works"

// ✅ Good
test "should return user when ID exists"
test "should throw error when ID is invalid"
```

## Running Tests

```bash
# Run all tests
run-tests

# Run specific test file
run-tests user-test

# Watch mode (re-run on changes)
run-tests --watch
```

## Best Practices

1. **One test, one thing** - Test one behavior per test
2. **Independent tests** - Tests should not depend on each other
3. **Clear names** - Name should describe what is being tested
4. **Fast tests** - Tests should run quickly

```pseudocode
// ❌ Bad: Testing multiple things
test "user operations":
    expect createUser("Bob").name equals "Bob"
    expect deleteUser(1) equals true
    expect listUsers().length equals 0

// ✅ Good: One test per operation
test "should create user with given name":
    user = createUser("Bob")
    expect user.name equals "Bob"

test "should delete user by ID":
    result = deleteUser(1)
    expect result equals true

test "should return empty list when no users":
    users = listUsers()
    expect users.length equals 0
```

## When to Write Tests

- **Before fixing bugs** - Write test that fails, then fix
- **For new features** - Test expected behavior
- **For edge cases** - Empty input, null values, large numbers

## What to Test

✅ **Do test:**
- Public functions and methods
- Edge cases (empty, null, zero, negative)
- Error conditions

❌ **Don't test:**
- Private implementation details
- Third-party libraries (they're already tested)
- Getters/setters with no logic
