---
title: Parallelize Independent Async Operations
paths:
  - "src/**/*"
---

# Parallelize Independent Async Operations

Independent asynchronous operations that share no data dependency must run concurrently, not sequentially. Sequential execution adds each operation's latency together. Concurrent execution reduces total latency to the slowest single operation.

This applies to any I/O-bound work: HTTP requests, database queries, RPC calls, file reads, message-broker publishes, cache lookups, external API calls, child-process invocations, and similar. The same principle holds across runtimes and languages — only the syntax differs (e.g., `Promise.all` in JavaScript/TypeScript, `asyncio.gather` in Python, `errgroup`/goroutines in Go, structured concurrency in Kotlin, `tokio::join!` in Rust, threads or `CompletableFuture` in Java).

## How to identify violations

Scan for these patterns regardless of language:

- Two or more consecutive `await` (or equivalent blocking) calls where the second does **not** read from the first.
- A `for` / `while` loop that `await`s one independent operation per iteration instead of dispatching all and awaiting once.
- Sequential calls to different services, different endpoints, or different keys against the same service.
- "Warm-up" or "prefetch" steps performed serially before the main work begins.

## Incorrect

Two independent service calls awaited one after the other. Total latency = `latency(A) + latency(B)`.

```ts
const dataA = await serviceA.getData(key);
const dataB = await serviceB.getData(key);
```

A loop awaiting one independent request at a time. Total latency = `N * latency(request)`.

```ts
const results: Item[] = [];
for (const id of ids) {
  results.push(await api.fetchItem(id));
}
```

## Correct

Both calls dispatched simultaneously. Total latency = `max(latency(A), latency(B))`.

```ts
const [dataA, dataB] = await Promise.all([
  serviceA.getData(key),
  serviceB.getData(key),
]);
```

All requests dispatched concurrently, awaited once. Total latency ≈ `max(latency(request_i))`.

```ts
const results = await Promise.all(ids.map((id) => api.fetchItem(id)));
```


## When NOT to apply

- **Data dependency.** A later operation reads from an earlier operation's result.
- **Ordering or causality.** The operations must observably happen in a specific order (e.g., write-then-read against a non-linearizable store).
- **Rate limits, quotas, or backpressure.** Parallelism would exceed downstream limits; prefer a bounded-concurrency primitive (e.g., a worker pool, `p-limit`, semaphore) instead of full parallelism.
- **Resource contention.** The operations contend for a single connection, lock, or transaction.
- **Failure-handling differences.** When one failure must short-circuit and cancel siblings, or when partial success must be reported per-item, choose the right primitive (`Promise.allSettled`, `errgroup` with context cancellation, `asyncio.gather(return_exceptions=True)`, etc.) instead of naive "all-or-nothing".
