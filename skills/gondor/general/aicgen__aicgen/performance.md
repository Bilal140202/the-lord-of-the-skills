# Performance

# Performance Basics

## Choose the Right Data Structure

Different data structures have different speeds for different operations.

### Arrays vs Objects vs Maps

```pseudocode
// ❌ Slow: Looking up in array (O(n))
users = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
    // ... 1000 more
]
user = users.find(u => u.id == 500)  // Checks 500 items

// ✅ Fast: Looking up in Map (O(1))
users = Map()
users.set(1, { id: 1, name: 'Alice' })
users.set(2, { id: 2, name: 'Bob' })

user = users.get(500)  // Instant lookup
```

### Arrays vs Sets

```pseudocode
// ❌ Slow: Checking if item exists in array
items = [1, 2, 3, 4, 5, ... 1000 more]
if items.contains(500):  // Checks every item

// ✅ Fast: Checking if item exists in Set
items = Set([1, 2, 3, 4, 5, ... 1000 more])
if items.has(500):  // Instant check
```

### When to Use Each

| Data Structure | Good For |
|----------------|----------|
| **Array/List** | Ordered items, iteration |
| **Object/Dict** | Key-value pairs (string keys) |
| **Map** | Key-value pairs (any type keys), frequent lookups |
| **Set** | Unique values, membership checks |

## Avoid N+1 Queries

One of the most common performance problems.

```pseudocode
// ❌ BAD: N+1 queries (1 + N database calls)
orders = database.query("SELECT * FROM orders")

for each order in orders:
    // Separate query for EACH order! 😱
    customer = database.query(
        "SELECT * FROM customers WHERE id = ?",
        [order.customer_id]
    )
    order.customer = customer
// If 100 orders = 101 database calls!

// ✅ GOOD: Single query with JOIN
ordersWithCustomers = database.query("
    SELECT
        orders.*,
        customers.name as customer_name,
        customers.email as customer_email
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
")
// Only 1 database call!
```

## Don't Load What You Don't Need

```pseudocode
// ❌ Bad: Fetching entire object when you only need one field
user = database.query("SELECT * FROM users WHERE id = ?", [id])
print(user.email)

// ✅ Good: Fetch only what you need
result = database.query(
    "SELECT email FROM users WHERE id = ?",
    [id]
)
print(result.email)

// ❌ Bad: Loading all records
users = database.query("SELECT * FROM users")

// ✅ Good: Add LIMIT
users = database.query("SELECT * FROM users LIMIT 100")
```

## Use Async for I/O Operations

Don't block the program waiting for slow operations.

```pseudocode
// ❌ Slow: Blocking operations (synchronous)
file1 = readFileSync("file1.txt")
file2 = readFileSync("file2.txt")
file3 = readFileSync("file3.txt")
// Total: 300ms (100ms each, one after another)

// ✅ Fast: Async operations (parallel)
files = await Promise.all([
    readFile("file1.txt"),
    readFile("file2.txt"),
    readFile("file3.txt")
])
// Total: 100ms (all at once)
```

## Avoid Unnecessary Work in Loops

```pseudocode
// ❌ Bad: Work done every iteration
for i in 0 to items.length:
    total = calculateTotal(items)  // Recalculated each time!
    if items[i].price > total * 0.1:
        // ...

// ✅ Good: Work done once
total = calculateTotal(items)
for i in 0 to items.length:
    if items[i].price > total * 0.1:
        // ...

// ❌ Bad: Array length calculated each time
for i in 0 to items.length:
    // ...

// ✅ Good: Length cached (minor improvement)
len = items.length
for i in 0 to len:
    // ...

// ✅ Best: Modern for-each loop
for each item in items:
    // ...
```

## Index Your Database

Indexes make lookups fast, but slow down writes.

```sql
-- Without index: Checks every row
SELECT * FROM users WHERE email = 'alice@example.com';
-- With 1 million users: ~1 second

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Now same query is instant
SELECT * FROM users WHERE email = 'alice@example.com';
-- With 1 million users: ~1 millisecond
```

### When to Add Indexes

- Columns used in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY

```sql
-- Frequently queried
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_users_email ON users(email);

-- Used in joins
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

## Cache Expensive Results

Don't recalculate the same thing repeatedly.

```pseudocode
// ❌ Bad: Calculating every time
function getReport(userId):
    data = expensiveCalculation(userId)  // 5 seconds
    return data

// Called 100 times = 500 seconds!

// ✅ Good: Cache results
cache = Map()

function getReport(userId):
    if cache.has(userId):
        return cache.get(userId)  // Instant

    data = expensiveCalculation(userId)
    cache.set(userId, data)
    return data

// First call: 5 seconds, next 99 calls: instant
```

## Batch Operations

Process multiple items together instead of one at a time.

```pseudocode
// ❌ Bad: Individual database calls
for each user in users:
    database.execute("INSERT INTO users (name) VALUES (?)", [user.name])
// 100 users = 100 database calls

// ✅ Good: Batch insert
database.execute("
    INSERT INTO users (name)
    VALUES " + users.map(u => "(?)").join(", "),
    users.map(u => u.name)
)
// 100 users = 1 database call
```

## Profile Before Optimizing

Don't guess where the problem is - measure!

```pseudocode
// Measure execution time
startTime = currentTime()
result = await slowOperation()
endTime = currentTime()
print("Operation took:", endTime - startTime, "ms")

// Measure specific parts
startDB = currentTime()
data = await database.query("...")
print("Database:", currentTime() - startDB, "ms")

startProcess = currentTime()
processed = processData(data)
print("Processing:", currentTime() - startProcess, "ms")
```

## Common Performance Mistakes

### Mistake 1: Nested Loops with Database Queries

```pseudocode
// ❌ TERRIBLE: Nested queries
for each user in users:
    for each order in orders:
        product = await database.query(
            "SELECT * FROM products WHERE id = ?",
            [order.product_id]
        )
// 100 users × 50 orders = 5000 database calls!

// ✅ GOOD: Load all data first
products = await database.query("SELECT * FROM products")
productMap = Map()
for each p in products:
    productMap.set(p.id, p)

for each user in users:
    for each order in orders:
        product = productMap.get(order.product_id)  // Instant
```

### Mistake 2: Loading Everything into Memory

```pseudocode
// ❌ Bad: Loading 1 million records
allUsers = await database.query("SELECT * FROM users")
// Crashes with out of memory!

// ✅ Good: Process in batches
BATCH_SIZE = 1000
offset = 0

while true:
    users = await database.query(
        "SELECT * FROM users LIMIT ? OFFSET ?",
        [BATCH_SIZE, offset]
    )

    if users.length == 0:
        break

    await processUsers(users)
    offset = offset + BATCH_SIZE
```

### Mistake 3: Not Using Indexes

```sql
-- ❌ Slow: No index on email column
SELECT * FROM users WHERE email = 'alice@example.com';
-- 1 million rows: ~2 seconds

-- ✅ Fast: Add index
CREATE INDEX idx_users_email ON users(email);
-- Same query: ~2 milliseconds
```

## Quick Performance Checklist

- [ ] Use Map/Set for lookups instead of Array
- [ ] Avoid N+1 queries (use JOINs)
- [ ] Add database indexes on frequently queried columns
- [ ] Don't load all records (use LIMIT)
- [ ] Cache expensive calculations
- [ ] Run independent operations in parallel
- [ ] Move work outside of loops
- [ ] Batch database operations
- [ ] Profile before optimizing

## When to Optimize

1. **Measure first** - Is there actually a problem?
2. **Find the bottleneck** - What's slow?
3. **Fix the biggest problem** - Don't waste time on small gains
4. **Measure again** - Did it help?

Don't optimize prematurely - write clear code first, optimize when needed!


---

# Caching Strategies

## In-Memory Caching

```typescript
class Cache<T> {
  private cache = new Map<string, { value: T; expiry: number }>();

  set(key: string, value: T, ttlMs: number = 60000): void {
    this.cache.set(key, {
      value,
      expiry: Date.now() + ttlMs
    });
  }

  get(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.value;
  }
}

// Usage
const userCache = new Cache<User>();

async function getUser(id: string): Promise<User> {
  const cached = userCache.get(id);
  if (cached) return cached;

  const user = await db.findUser(id);
  userCache.set(id, user, 300000); // 5 minutes
  return user;
}
```

## Redis Caching

```typescript
import Redis from 'ioredis';

const redis = new Redis();

async function getCachedUser(id: string): Promise<User | null> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.findUser(id);
  await redis.setex(`user:${id}`, 300, JSON.stringify(user)); // 5 min TTL
  return user;
}

// Cache invalidation on update
async function updateUser(id: string, data: Partial<User>) {
  const user = await db.updateUser(id, data);
  await redis.del(`user:${id}`); // Invalidate cache
  return user;
}
```

## HTTP Caching

```typescript
// Cache-Control headers
app.get('/api/products', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  res.json(products);
});

// ETag for conditional requests
app.get('/api/user/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  const etag = generateETag(user);

  res.set('ETag', etag);

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end(); // Not Modified
  }

  res.json(user);
});
```

## Cache-Aside Pattern

```typescript
// Also called "lazy loading"
async function getProduct(id: string): Promise<Product> {
  // 1. Check cache
  const cached = await redis.get(`product:${id}`);
  if (cached) return JSON.parse(cached);

  // 2. Cache miss - load from database
  const product = await db.findProduct(id);

  // 3. Store in cache
  await redis.setex(`product:${id}`, 600, JSON.stringify(product));

  return product;
}
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

// Cache expensive computations
const calculateDiscount = memoize((price: number, tier: string) => {
  // Complex calculation
  return result;
});
```

## Cache Invalidation Strategies

```typescript
// Time-based expiry
await redis.setex(key, 300, value); // Expires after 5 minutes

// Event-based invalidation
async function updateProduct(id: string, data: ProductUpdate) {
  await db.updateProduct(id, data);
  await redis.del(`product:${id}`);
  await redis.del('products:list'); // Invalidate list cache too
}

// Cache warming
async function warmCache() {
  const popularProducts = await db.getMostViewed(100);
  for (const product of popularProducts) {
    await redis.setex(`product:${product.id}`, 3600, JSON.stringify(product));
  }
}
```


---

# Async Performance Patterns

## Parallel Execution

```typescript
// ❌ Sequential - slow
async function getUserData(userId: string) {
  const user = await fetchUser(userId);       // 100ms
  const posts = await fetchPosts(userId);     // 150ms
  const comments = await fetchComments(userId); // 120ms
  return { user, posts, comments }; // Total: 370ms
}

// ✅ Parallel - fast
async function getUserData(userId: string) {
  const [user, posts, comments] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchComments(userId)
  ]);
  return { user, posts, comments }; // Total: 150ms
}

// ✅ Partial parallel with dependencies
async function getOrderDetails(orderId: string) {
  const order = await fetchOrder(orderId); // Must fetch first

  const [customer, items, shipping] = await Promise.all([
    fetchCustomer(order.customerId),
    fetchOrderItems(orderId),
    fetchShippingInfo(orderId)
  ]);

  return { order, customer, items, shipping };
}
```

## Promise.allSettled for Partial Failures

```typescript
// Return partial data instead of complete failure
async function getDashboard(userId: string) {
  const [user, orders, stats] = await Promise.allSettled([
    getUser(userId),
    getOrders(userId),
    getStats(userId)
  ]);

  return {
    user: user.status === 'fulfilled' ? user.value : null,
    orders: orders.status === 'fulfilled' ? orders.value : [],
    stats: stats.status === 'fulfilled' ? stats.value : null,
    errors: {
      user: user.status === 'rejected' ? user.reason.message : null,
      orders: orders.status === 'rejected' ? orders.reason.message : null,
      stats: stats.status === 'rejected' ? stats.reason.message : null
    }
  };
}
```

## Batch Processing

```typescript
// ❌ One at a time - slow
async function processUsers(userIds: string[]) {
  for (const id of userIds) {
    await updateUser(id);
  }
}

// ✅ Batch processing
async function processUsers(userIds: string[]) {
  const BATCH_SIZE = 50;

  for (let i = 0; i < userIds.length; i += BATCH_SIZE) {
    const batch = userIds.slice(i, i + BATCH_SIZE);
    await Promise.all(batch.map(id => updateUser(id)));
  }
}

// ✅ Bulk database operations
async function createUsers(users: User[]) {
  await db.query(`
    INSERT INTO users (name, email)
    VALUES ${users.map(() => '(?, ?)').join(', ')}
  `, users.flatMap(u => [u.name, u.email]));
}
```

## Debouncing and Throttling

```typescript
// Debounce: Wait until user stops typing
const debounce = <T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

// Throttle: Execute at most once per interval
const throttle = <T extends (...args: any[]) => any>(
  fn: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

// Usage
const searchUsers = debounce(query => api.search(query), 300);
const handleScroll = throttle(() => console.log('scroll'), 100);
```

## Rate Limiting Concurrent Operations

```typescript
async function processWithLimit<T>(
  items: T[],
  fn: (item: T) => Promise<void>,
  concurrency: number
): Promise<void> {
  const chunks = [];
  for (let i = 0; i < items.length; i += concurrency) {
    chunks.push(items.slice(i, i + concurrency));
  }

  for (const chunk of chunks) {
    await Promise.all(chunk.map(fn));
  }
}

// Usage: Process 100 items, max 10 at a time
await processWithLimit(users, updateUser, 10);
```


---

# Caching Strategies

## Cache Patterns

### Cache-Aside (Lazy Loading)
```typescript
async function getUser(id: string): Promise<User> {
  const cached = await cache.get(`user:${id}`);
  if (cached) return cached;

  const user = await db.findUser(id);
  await cache.set(`user:${id}`, user, { ttl: 3600 });
  return user;
}
```

### Write-Through
```typescript
async function updateUser(user: User): Promise<void> {
  await db.saveUser(user);
  await cache.set(`user:${user.id}`, user);
}
```

### Write-Behind (Write-Back)
```typescript
async function updateUser(user: User): Promise<void> {
  await cache.set(`user:${user.id}`, user);
  await queue.add('sync-to-db', { user }); // Async persistence
}
```

## Cache Invalidation

```typescript
// Time-based expiration
await cache.set('key', value, { ttl: 3600 });

// Event-based invalidation
eventBus.on('user.updated', async (userId) => {
  await cache.delete(`user:${userId}`);
});

// Pattern-based invalidation
await cache.deleteByPattern('user:*');
```

## HTTP Caching

```typescript
// Cache-Control headers
res.setHeader('Cache-Control', 'public, max-age=3600');
res.setHeader('ETag', etag(content));

// Conditional requests
if (req.headers['if-none-match'] === currentEtag) {
  return res.status(304).end();
}
```

## Best Practices

- Cache at appropriate layers (CDN, app, DB)
- Use consistent cache keys
- Set appropriate TTLs
- Monitor cache hit rates
- Plan for cache failures (fallback to source)
- Avoid caching sensitive data
