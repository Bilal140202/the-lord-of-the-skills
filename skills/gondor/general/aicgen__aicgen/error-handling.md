# Error Handling

# Error Handling Strategy

## Custom Error Classes

```typescript
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

// Usage
if (!user) {
  throw new NotFoundError('User', userId);
}
```

## Never Swallow Errors

```typescript
// ❌ Silent failure - dangerous!
try {
  await criticalOperation();
} catch (error) {
  // Error ignored
}

// ✅ Log and handle appropriately
try {
  await criticalOperation();
} catch (error) {
  logger.error('Critical operation failed', { error });
  throw error; // Or handle gracefully
}
```

## Specific Error Messages

```typescript
// ❌ Not actionable
throw new Error('Something went wrong');

// ✅ Specific and actionable
throw new ValidationError('Email must be a valid email address', {
  field: 'email',
  value: userInput.email
});
```

## Centralized Error Handler

```typescript
// Express error middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        message: err.message,
        code: err.code,
        details: err.details
      }
    });
  }

  // Log unexpected errors
  console.error('Unexpected error:', err);

  // Don't expose internal details
  res.status(500).json({
    error: {
      message: 'Internal server error',
      code: 'INTERNAL_ERROR'
    }
  });
});
```

## Async Error Wrapper

```typescript
// Wrap async handlers to catch errors automatically
const asyncHandler = (fn: RequestHandler) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Usage
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
}));
```

## Result Type Pattern

```typescript
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

// Usage - forces explicit error handling
const result = parseJSON<User>(data);
if (result.success) {
  console.log(result.value.name);
} else {
  console.error(result.error);
}
```

## Error Boundaries (React)

```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('UI Error', { error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

## Retry with Limits

```typescript
// ❌ Infinite retries
while (true) {
  try {
    await operation();
    break;
  } catch (error) {
    // Retry forever - exhausts resources
  }
}

// ✅ Limited retries with backoff
const maxRetries = 3;
for (let i = 0; i < maxRetries; i++) {
  try {
    await operation();
    break;
  } catch (error) {
    if (i === maxRetries - 1) throw error;
    await sleep(Math.pow(2, i) * 1000); // Exponential backoff
  }
}
```


---

# Error Handling Basics

## Throwing Errors

Use `throw` to signal when something goes wrong.

```pseudocode
function divide(a, b):
    if b == 0:
        throw Error("Cannot divide by zero")
    return a / b
```

## Try-Catch

Use `try-catch` to handle errors gracefully.

```pseudocode
try:
    result = divide(10, 0)
    print(result)
catch error:
    print("Error:", error.message)
    // Continue with fallback behavior
```

## Always Provide Error Messages

Make error messages clear and actionable.

```pseudocode
// ❌ Bad: Vague error
throw Error("Invalid")

// ✅ Good: Specific error
throw Error("Email must be a valid email address")

// ✅ Good: Include context
throw Error("User with ID " + userId + " not found")
```

## Async Error Handling

Always use try-catch with async operations.

```pseudocode
async function loadUser(id):
    try:
        user = await fetchUser(id)
        return user
    catch error:
        log("Failed to load user:", error)
        throw error  // Re-throw if caller should know
```

## When to Catch Errors

### Catch When You Can Handle It

```pseudocode
// ✅ Good: Can provide fallback
async function getUserName(id):
    try:
        user = await fetchUser(id)
        return user.name
    catch error:
        return "Unknown User"  // Fallback value
```

### Don't Catch If You Can't Handle

```pseudocode
// ❌ Bad: Catching but doing nothing
try:
    await criticalOperation()
catch error:
    // Empty catch - error lost!

// ✅ Good: Let it propagate
await criticalOperation()  // Caller will handle
```

## Validate Input Early

Check for problems before they cause errors.

```pseudocode
function createUser(email, age):
    // Validate inputs first
    if email is empty:
        throw Error("Email is required")

    if not email.contains("@"):
        throw Error("Email must be valid")

    if age < 0:
        throw Error("Age cannot be negative")

    // Now proceed with creation
    return { email: email, age: age }
```

## Logging Errors

Always log errors for debugging.

```pseudocode
try:
    await processPayment(orderId)
catch error:
    // Log with context
    log("Payment processing failed:", {
        orderId: orderId,
        error: error.message,
        timestamp: currentTime()
    })
    throw error
```

## Error Handling Patterns

### Return Error Status

```pseudocode
function parseNumber(input):
    num = parseInt(input)
    if isNaN(num):
        return null  // Indicate failure without throwing
    return num

// Usage
result = parseNumber(userInput)
if result is null:
    print("Invalid number")
else:
    print("Number:", result)
```

### Return Success/Error Object

```pseudocode
function safeDivide(a, b):
    if b == 0:
        return { success: false, error: "Cannot divide by zero" }
    return { success: true, data: a / b }

// Usage
result = safeDivide(10, 2)
if result.success:
    print("Result:", result.data)
else:
    print("Error:", result.error)
```

## Common Mistakes

### Don't Swallow Errors

```pseudocode
// ❌ Bad: Error disappears
try:
    await importantOperation()
catch error:
    // Nothing here - error lost!

// ✅ Good: Log at minimum
try:
    await importantOperation()
catch error:
    log("Operation failed:", error)
    throw error  // Or handle appropriately
```

### Don't Use Errors for Flow Control

```pseudocode
// ❌ Bad: Using errors for normal logic
try:
    user = findUser(id)
    // ...
catch error:
    // User not found - this is expected, not an error!

// ✅ Good: Return null for expected cases
user = findUser(id)
if user is null:
    print("User not found")
    return
```

### Don't Throw Non-Error Objects

```pseudocode
// ❌ Bad
throw "Something went wrong"  // String
throw { code: 500 }           // Plain object

// ✅ Good
throw Error("Something went wrong")
```

## Best Practices

1. **Fail fast** - Validate input early and throw immediately
2. **Be specific** - Provide detailed, actionable error messages
3. **Log errors** - Always log for debugging
4. **Don't hide errors** - Let them propagate if you can't handle them
5. **Clean up resources** - Close connections, files in finally blocks

```pseudocode
file = null
try:
    file = await openFile("data.txt")
    await processFile(file)
catch error:
    log("File processing failed:", error)
    throw error
finally:
    // Always runs, even if error thrown
    if file is not null:
        await file.close()
```
