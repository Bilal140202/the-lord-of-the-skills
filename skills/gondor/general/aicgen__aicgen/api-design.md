# API Design

# API Basics

## HTTP Methods

Use the right method for each operation:

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Read data | Get list of users |
| POST | Create new resource | Create a new user |
| PUT | Replace entire resource | Update all user fields |
| PATCH | Update part of resource | Update user's email only |
| DELETE | Remove resource | Delete a user |

## GET - Reading Data

```pseudocode
// Get all items
route GET "/api/users":
    users = getAllUsers()
    return JSON(users)

// Get single item by ID
route GET "/api/users/:id":
    user = getUserById(params.id)
    if user is null:
        return status 404, JSON({ error: "User not found" })
    return JSON(user)
```

## POST - Creating Data

```pseudocode
route POST "/api/users":
    name = request.body.name
    email = request.body.email

    // Validate input
    if name is empty or email is empty:
        return status 400, JSON({ error: "Name and email required" })

    newUser = createUser({ name, email })

    // Return 201 Created with new resource
    return status 201, JSON(newUser)
```

## PUT - Replacing Data

```pseudocode
route PUT "/api/users/:id":
    id = params.id
    name = request.body.name
    email = request.body.email

    user = getUserById(id)
    if user is null:
        return status 404, JSON({ error: "User not found" })

    updated = replaceUser(id, { name, email })
    return JSON(updated)
```

## PATCH - Updating Data

```pseudocode
route PATCH "/api/users/:id":
    id = params.id
    updates = request.body  // Only fields to update

    user = getUserById(id)
    if user is null:
        return status 404, JSON({ error: "User not found" })

    updated = updateUser(id, updates)
    return JSON(updated)
```

## DELETE - Removing Data

```pseudocode
route DELETE "/api/users/:id":
    id = params.id

    user = getUserById(id)
    if user is null:
        return status 404, JSON({ error: "User not found" })

    deleteUser(id)

    // 204 No Content - successful deletion
    return status 204
```

## HTTP Status Codes

### Success Codes (2xx)

```pseudocode
// 200 OK - Request succeeded
return status 200, JSON(data)

// 201 Created - New resource created
return status 201, JSON(newResource)

// 204 No Content - Success with no response body
return status 204
```

### Client Error Codes (4xx)

```pseudocode
// 400 Bad Request - Invalid input
return status 400, JSON({ error: "Invalid email format" })

// 401 Unauthorized - Not authenticated
return status 401, JSON({ error: "Login required" })

// 403 Forbidden - Authenticated but not allowed
return status 403, JSON({ error: "Admin access required" })

// 404 Not Found - Resource doesn't exist
return status 404, JSON({ error: "User not found" })

// 409 Conflict - Resource already exists
return status 409, JSON({ error: "Email already registered" })
```

### Server Error Codes (5xx)

```pseudocode
// 500 Internal Server Error - Unexpected error
return status 500, JSON({ error: "Internal server error" })

// 503 Service Unavailable - Temporary issue
return status 503, JSON({ error: "Database unavailable" })
```

## URL Structure

Use clear, hierarchical URLs:

```
✅ Good
GET  /api/users           # List all users
GET  /api/users/123       # Get user 123
POST /api/users           # Create user
GET  /api/users/123/posts # Get posts by user 123

❌ Bad
GET  /api/getUsers
POST /api/createUser
GET  /api/user?id=123
```

## Request and Response Format

### JSON Request Body

```
// Client sends
POST /api/users
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}
```

### JSON Response

```
// Server responds
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

## Query Parameters

Use query parameters for filtering, sorting, and pagination:

```pseudocode
// Filter by status
// GET /api/orders?status=pending
route GET "/api/orders":
    status = query.status
    orders = getOrders({ status })
    return JSON(orders)

// Sort by field
// GET /api/users?sort=name

// Pagination
// GET /api/users?page=2&limit=20
```

## Error Responses

Always return consistent error format:

```pseudocode
// ✅ Good: Structured error
return status 400, JSON({
    error: {
        code: "VALIDATION_ERROR",
        message: "Invalid input",
        details: {
            email: "Email format is invalid"
        }
    }
})

// ❌ Bad: Inconsistent
return status 400, "Bad request"
return status 400, JSON({ msg: "Error" })
```

## Best Practices

1. **Use correct HTTP methods** - GET for reading, POST for creating, etc.
2. **Use appropriate status codes** - 200 for success, 404 for not found, etc.
3. **Return JSON** - Standard format for APIs
4. **Validate input** - Check data before processing
5. **Handle errors** - Return clear error messages

```pseudocode
// Complete example
route POST "/api/products":
    name = request.body.name
    price = request.body.price

    // Validate
    if name is empty or price is empty:
        return status 400, JSON({
            error: "Name and price are required"
        })

    if price < 0:
        return status 400, JSON({
            error: "Price cannot be negative"
        })

    // Check for duplicates
    if productExists(name):
        return status 409, JSON({
            error: "Product already exists"
        })

    // Create
    product = createProduct({ name, price })

    // Return success
    return status 201, JSON(product)
```

## Common Mistakes

```pseudocode
// ❌ Wrong method for operation
route GET "/api/users/delete/:id"  // Should be DELETE

// ❌ Wrong status code
route POST "/api/users":
    user = createUser(body)
    return status 200, JSON(user)  // Should be 201

// ❌ Not handling missing resources
route GET "/api/users/:id":
    user = getUserById(params.id)
    return JSON(user)  // What if user is null?

// ✅ Correct
route DELETE "/api/users/:id"

route POST "/api/users":
    user = createUser(body)
    return status 201, JSON(user)

route GET "/api/users/:id":
    user = getUserById(params.id)
    if user is null:
        return status 404, JSON({ error: "User not found" })
    return JSON(user)
```


---

# REST API Design

## Resource-Oriented URLs

```
✅ Good (nouns, plural)
GET    /api/v1/books           # List books
GET    /api/v1/books/123       # Get book
POST   /api/v1/books           # Create book
PUT    /api/v1/books/123       # Replace book
PATCH  /api/v1/books/123       # Update book
DELETE /api/v1/books/123       # Delete book

❌ Bad (verbs, actions)
POST /api/v1/createBook
GET  /api/v1/getBookById/123
POST /api/v1/updateBook/123
```

## HTTP Methods

```typescript
// GET - Read (safe, idempotent)
app.get('/api/v1/users/:id', async (req, res) => {
  const user = await userService.findById(req.params.id);
  res.json({ data: user });
});

// POST - Create (not idempotent)
app.post('/api/v1/users', async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201)
    .location(`/api/v1/users/${user.id}`)
    .json({ data: user });
});

// PUT - Replace entire resource (idempotent)
app.put('/api/v1/users/:id', async (req, res) => {
  const user = await userService.replace(req.params.id, req.body);
  res.json({ data: user });
});

// PATCH - Partial update (idempotent)
app.patch('/api/v1/users/:id', async (req, res) => {
  const user = await userService.update(req.params.id, req.body);
  res.json({ data: user });
});

// DELETE - Remove (idempotent)
app.delete('/api/v1/users/:id', async (req, res) => {
  await userService.delete(req.params.id);
  res.status(204).end();
});
```

## Status Codes

```typescript
// Success
200 OK           // GET, PUT, PATCH succeeded
201 Created      // POST succeeded
204 No Content   // DELETE succeeded

// Client errors
400 Bad Request  // Validation failed
401 Unauthorized // Not authenticated
403 Forbidden    // Authenticated but not allowed
404 Not Found    // Resource doesn't exist
409 Conflict     // Duplicate, version conflict
422 Unprocessable // Business rule violation

// Server errors
500 Internal Server Error
```

## Response Format

```typescript
// Single resource
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// Collection with pagination
{
  "data": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

## Hierarchical Resources

```
✅ Limit nesting to 2-3 levels
GET /api/v1/authors/456/books       # Books by author
GET /api/v1/orders/789/items        # Items in order

❌ Too deep
GET /api/v1/publishers/1/authors/2/books/3/reviews/4

✅ Use query parameters instead
GET /api/v1/reviews?bookId=3
```

## API Versioning

```
✅ Always version from the start
/api/v1/books
/api/v2/books

❌ No version
/api/books
```


---

# API Pagination

## Always Paginate Collections

```typescript
// ✅ Paginated endpoint
app.get('/api/v1/books', async (req, res) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);

  const { data, total } = await bookService.findAll({ page, limit });

  res.json({
    data,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrevious: page > 1
    }
  });
});
```

## Offset-Based Pagination

```typescript
// Simple but has issues with large datasets
GET /api/v1/books?page=1&limit=20
GET /api/v1/books?page=2&limit=20

// Implementation
const getBooks = async (page: number, limit: number) => {
  const offset = (page - 1) * limit;

  const [data, total] = await Promise.all([
    db.query('SELECT * FROM books ORDER BY id LIMIT ? OFFSET ?', [limit, offset]),
    db.query('SELECT COUNT(*) FROM books')
  ]);

  return { data, total };
};
```

## Cursor-Based Pagination

```typescript
// Better for large datasets and real-time data
GET /api/v1/books?cursor=eyJpZCI6MTIzfQ&limit=20

// Response includes next cursor
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}

// Implementation
const getBooks = async (cursor: string | null, limit: number) => {
  let query = 'SELECT * FROM books';

  if (cursor) {
    const { id } = decodeCursor(cursor);
    query += ` WHERE id > ${id}`;
  }

  query += ` ORDER BY id LIMIT ${limit + 1}`;
  const data = await db.query(query);

  const hasMore = data.length > limit;
  const items = hasMore ? data.slice(0, limit) : data;

  return {
    data: items,
    pagination: {
      nextCursor: hasMore ? encodeCursor({ id: items[items.length - 1].id }) : null,
      hasMore
    }
  };
};
```

## Keyset Pagination

```sql
-- Most efficient for large tables
-- First page
SELECT * FROM products
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Next page (using last item's values)
SELECT * FROM products
WHERE (created_at, id) < ('2024-01-15 10:00:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## HATEOAS Links

```typescript
// Include navigation links
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150
  },
  "links": {
    "self": "/api/v1/books?page=2&limit=20",
    "first": "/api/v1/books?page=1&limit=20",
    "prev": "/api/v1/books?page=1&limit=20",
    "next": "/api/v1/books?page=3&limit=20",
    "last": "/api/v1/books?page=8&limit=20"
  }
}
```

## Pagination Best Practices

```typescript
// ✅ Set reasonable defaults and limits
const page = parseInt(req.query.page) || 1;
const limit = Math.min(parseInt(req.query.limit) || 20, 100);

// ✅ Include total count (when practical)
const total = await db.count('books');

// ✅ Use consistent response structure
{
  "data": [],
  "pagination": { ... }
}

// ❌ Don't return unlimited results
// ❌ Don't allow page < 1 or limit < 1
```


---

# API Versioning

## Versioning Strategies

### URL Path Versioning
```
GET /api/v1/users
GET /api/v2/users
```

### Header Versioning
```
GET /api/users
Accept: application/vnd.api+json; version=2
```

### Query Parameter
```
GET /api/users?version=2
```

## Implementation

```typescript
// URL path versioning
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header versioning middleware
function versionMiddleware(req, res, next) {
  const version = req.headers['api-version'] || '1';
  req.apiVersion = parseInt(version);
  next();
}

app.get('/users', versionMiddleware, (req, res) => {
  if (req.apiVersion >= 2) {
    return handleV2(req, res);
  }
  return handleV1(req, res);
});
```

## Deprecation Strategy

```typescript
// Add deprecation headers
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 01 Jan 2025 00:00:00 GMT');
res.setHeader('Link', '</api/v2/users>; rel="successor-version"');
```

## Best Practices

- Version from the start
- Support at least N-1 versions
- Document deprecation timeline
- Provide migration guides
- Use semantic versioning for breaking changes
- Consider backwards-compatible changes first
