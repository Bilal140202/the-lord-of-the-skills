# Performance Optimization — Cursor Rules
# Comprehensive rules for writing performant code across the stack

## Project Context
You are working on a performance-sensitive application. The codebase must be efficient
in terms of response time, memory usage, CPU utilization, and network bandwidth. Every
code change should consider its performance implications. However, always profile before
optimizing — never guess where bottlenecks are.

## Core Principles
- Measure first, optimize second — use profiling tools, not intuition
- Optimize the critical path — 80% of time is spent in 20% of code
- Premature optimization is the root of all evil (but known patterns should be followed)
- Readability matters — don't sacrifice clarity for marginal gains
- Set performance budgets and test against them

## Frontend Performance

### Loading Performance
- **Bundle size**: Set budgets (e.g., <200KB JS gzipped for initial load)
- **Code splitting**: Split by route and load on demand
- **Tree shaking**: Use ES modules, avoid side effects in imports
- **Lazy loading**: `React.lazy()`, `defineAsyncComponent()`, dynamic `import()`
- **Preloading**: Use `<link rel="preload">` for critical resources
- **Font loading**: Use `font-display: swap`, subset fonts, use `next/font`

### Image Optimization
```tsx
// GOOD — responsive images with lazy loading
<img
  src="/images/hero.webp"
  srcSet="/images/hero-400.webp 400w, /images/hero-800.webp 800w, /images/hero-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  loading="lazy"
  decoding="async"
  alt="Product hero"
  width={800}
  height={600}
/>

// Or use framework image components
// Next.js: <Image src="..." width={800} height={600} />
// Nuxt: <NuxtImg src="..." />
```

### Rendering Performance
- Avoid layout thrashing — batch DOM reads and writes
- Use `transform` and `opacity` for animations (GPU-accelerated)
- Use `will-change` sparingly for elements that will animate
- Use `content-visibility: auto` for off-screen content
- Debounce scroll/resize handlers (150-300ms)
- Use `requestAnimationFrame` for visual updates
- Virtualize long lists (react-window, vue-virtual-scroller)

### React-Specific
```tsx
// Memoize expensive components (only when profiling shows re-render issues)
const ExpensiveList = React.memo(function ExpensiveList({ items }) {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />);
});

// useMemo for expensive computations
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.price - b.price),
  [items]
);

// useCallback for stable function references passed to memoized children
const handleSelect = useCallback((id: string) => {
  setSelectedId(id);
}, []);

// Avoid: creating objects/arrays in render
// BAD
<MyComponent style={{ color: 'red' }} options={[1, 2, 3]} />
// GOOD — lift constants
const style = { color: 'red' };
const options = [1, 2, 3];
<MyComponent style={style} options={options} />
```

### Core Web Vitals Targets
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID/INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **TTFB** (Time to First Byte): < 800ms

## Backend Performance

### Database Query Optimization
```sql
-- Use EXPLAIN ANALYZE to find slow queries
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Add indexes for frequently filtered/sorted columns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Use pagination — never return unbounded results
SELECT * FROM products WHERE category = 'electronics'
ORDER BY created_at DESC LIMIT 20 OFFSET 0;

-- Use EXISTS instead of COUNT for existence checks
SELECT EXISTS(SELECT 1 FROM users WHERE email = 'test@example.com');

-- Avoid SELECT * — fetch only needed columns
SELECT id, name, price FROM products WHERE category = $1;
```

### N+1 Query Prevention
```ts
// BAD — N+1: 1 query for orders + N queries for users
const orders = await db.order.findMany();
for (const order of orders) {
  order.user = await db.user.findUnique({ where: { id: order.userId } });
}

// GOOD — eager loading
const orders = await db.order.findMany({
  include: { user: { select: { id: true, name: true } } },
});

// GOOD — batch loading
const orders = await db.order.findMany();
const userIds = [...new Set(orders.map(o => o.userId))];
const users = await db.user.findMany({ where: { id: { in: userIds } } });
const userMap = new Map(users.map(u => [u.id, u]));
orders.forEach(o => { o.user = userMap.get(o.userId); });
```

### Caching Strategy
```
Request → CDN Cache → Application Cache → Database Cache → Database
```

- **CDN/Edge**: Static assets, public pages (Cache-Control headers)
- **Application**: Frequently accessed data (Redis, in-memory)
- **Database**: Query result cache, materialized views
- **HTTP caching**: `Cache-Control`, `ETag`, `Last-Modified` headers

### Caching Patterns
```ts
// Cache-Aside (Lazy Loading)
async function getUser(id: string): Promise<User> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id } });
  if (user) {
    await redis.setex(`user:${id}`, 3600, JSON.stringify(user)); // 1 hour TTL
  }
  return user;
}

// Cache invalidation on write
async function updateUser(id: string, data: UpdateUserInput) {
  const user = await db.user.update({ where: { id }, data });
  await redis.del(`user:${id}`); // Invalidate cache
  return user;
}
```

### Connection Pooling
- Use connection pools for database connections (don't open/close per request)
- Size pool appropriately: 2-4x CPU cores for database connections
- Monitor pool utilization and adjust
- Set connection timeouts to prevent pool exhaustion

## API Performance
- Compress responses (gzip/brotli)
- Paginate all list endpoints
- Use GraphQL or sparse fieldsets to avoid over-fetching
- Batch related API calls where possible
- Use HTTP/2 for multiplexed requests
- Implement request deduplication for concurrent identical requests

## Algorithmic Efficiency

### Common Patterns
```ts
// Use Map/Set for lookups instead of Array.find/includes (O(1) vs O(n))
// BAD
const user = users.find(u => u.id === targetId); // O(n)

// GOOD
const userMap = new Map(users.map(u => [u.id, u]));
const user = userMap.get(targetId); // O(1)

// Use Set for membership checks
// BAD
const isAllowed = allowedIds.includes(id); // O(n)

// GOOD
const allowedSet = new Set(allowedIds);
const isAllowed = allowedSet.has(id); // O(1)
```

### Avoid Unnecessary Work
```ts
// BAD — recomputing on every call
function getExpensiveData() {
  return rawData.map(transform).filter(validate).sort(compare);
}

// GOOD — compute once, cache result
let cachedResult: Data[] | null = null;
function getExpensiveData() {
  if (!cachedResult) {
    cachedResult = rawData.map(transform).filter(validate).sort(compare);
  }
  return cachedResult;
}
```

## Memory Management
- Avoid memory leaks: clean up event listeners, timers, subscriptions
- Use weak references (`WeakMap`, `WeakRef`) for caches of large objects
- Stream large files instead of loading into memory
- Paginate large database result sets
- Profile memory with Chrome DevTools or `process.memoryUsage()`
- Watch for closure-captured variables keeping objects alive

## Monitoring and Profiling

### Tools
- **Frontend**: Chrome DevTools Performance tab, Lighthouse, WebPageTest
- **Backend**: Application Performance Monitoring (Datadog, New Relic, OpenTelemetry)
- **Database**: `EXPLAIN ANALYZE`, `pg_stat_statements`, slow query logs
- **Node.js**: `--inspect` flag, `clinic.js`, `0x` for flame graphs
- **Python**: `cProfile`, `py-spy`, `memory_profiler`

### What to Monitor
- Response time (p50, p95, p99)
- Error rate
- Throughput (requests per second)
- Database query time and count per request
- Memory usage over time
- CPU utilization
- Cache hit rate

## Common Pitfalls
- Optimizing without profiling (solving the wrong problem)
- Premature optimization at the cost of readability
- N+1 database queries (most common backend performance issue)
- Not using indexes on frequently queried columns
- Loading entire datasets when only a page is needed
- Missing cache invalidation (stale data)
- Not compressing API responses
- Blocking the event loop with synchronous operations (Node.js)
- Creating objects in hot loops (GC pressure)
- Not setting memory limits on containers (OOM kills)
