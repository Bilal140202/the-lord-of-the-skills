## 🗄️ Database Design & Schema Rules

> Best practices for database schema design, migrations, and security

---

### Schema Design Principles

#### Table Structure
```sql
-- ✅ GOOD: Complete table with all essentials
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,                           -- Unique identifier
    title TEXT NOT NULL,                           -- Required fields use NOT NULL
    description TEXT,                              -- Optional fields allow NULL
    status TEXT NOT NULL DEFAULT 'pending',        -- Defaults for common values
    priority INTEGER DEFAULT 2,
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),  -- Use Unix timestamps
    updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
    FOREIGN KEY (parent_id) REFERENCES items(id) ON DELETE CASCADE
);

-- ✅ Create indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
CREATE INDEX IF NOT EXISTS idx_items_parent ON items(parent_id);
```

#### ID Generation Patterns
```rust
// ✅ Type-prefixed IDs (readable + type info)
fn generate_id(prefix: &str) -> String {
    let hash = format!("{:04x}", (SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis() % 0xFFFF) as u16);
    format!("{}-{}", prefix, hash)  // → "task-a3f2", "doc-8b1c"
}

// ✅ UUID v4 for distributed systems
let id = uuid::Uuid::new_v4().to_string();
```

---

### Migration Best Practices

```rust
// ✅ Safe migrations: Use IF NOT EXISTS and ignore errors for ALTER
pub fn init_db(conn: &Connection) -> Result<(), String> {
    // Create table (idempotent)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items (...)",
        []
    ).map_err(|e| e.to_string())?;
    
    // Add new columns (ignore if already exists)
    let _ = conn.execute("ALTER TABLE items ADD COLUMN new_field TEXT", []);
    let _ = conn.execute("ALTER TABLE items ADD COLUMN priority INTEGER", []);
    
    // Create indexes (idempotent)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_status ON items(status)", [])
        .map_err(|e| e.to_string())?;
    
    Ok(())
}
```

### Migration Rules
| DO ✅ | DON'T ❌ |
|-------|---------|
| Use `IF NOT EXISTS` for tables | Assume table doesn't exist |
| Wrap `ALTER TABLE` in `let _ =` | Let ALTER errors crash app |
| Add columns as nullable first | Add NOT NULL without default |
| Create indexes after data loads | Drop indexes without backup |

---

### Security Best Practices

#### SQL Injection Prevention
```rust
// ✅ ALWAYS use parameterized queries
conn.execute(
    "INSERT INTO items (id, title) VALUES (?, ?)",
    params![&id, title]
)?;

// ✅ Use query_row with params
let item = conn.query_row(
    "SELECT * FROM items WHERE id = ?",
    [id],
    |row| Ok(Item { ... })
)?;

// ❌ NEVER concatenate user input
let sql = format!("SELECT * FROM items WHERE id = '{}'", id);  // DANGEROUS!
```

#### Access Control
```sql
-- ✅ Use workspace_id for multi-tenant isolation
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    workspace_id TEXT REFERENCES workspaces(id),
    ...
);

-- ✅ Always filter by workspace
SELECT * FROM items WHERE workspace_id = ? AND id = ?;
```

---

### Data Integrity

#### Foreign Keys
```sql
-- ✅ Define relationships with proper constraints
CREATE TABLE task_checklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    item TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

#### Cascading Deletes
| Relationship | On Delete |
|--------------|-----------|
| Parent-Child (comments) | `CASCADE` |
| Reference (workspace) | `SET NULL` |
| Required Reference | `RESTRICT` |

---

### Timestamps & Auditing

```sql
-- ✅ Always include audit timestamps
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    -- ... other fields
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
    started_at INTEGER,   -- For workflow tracking
    completed_at INTEGER  -- For completion tracking
);

-- ✅ Activity log for audit trail
CREATE TABLE item_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    action TEXT NOT NULL,        -- 'created', 'updated', 'status_change'
    actor TEXT,                  -- Who made the change
    details TEXT,                -- JSON or description
    status_from TEXT,            -- For status changes
    status_to TEXT,
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);
```

---

### Query Performance

```sql
-- ✅ Select only needed columns
SELECT id, title, status FROM items WHERE status = 'active';

-- ❌ Don't select everything
SELECT * FROM items;

-- ✅ Use LIMIT for large tables
SELECT id, title FROM items ORDER BY created_at DESC LIMIT 100;

-- ✅ Use indexes for WHERE clauses
CREATE INDEX idx_items_status ON items(status);
CREATE INDEX idx_items_created ON items(created_at);
```

---

### Full-Text Search (FTS5)

```sql
-- ✅ SQLite FTS5 for search functionality
CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
    item_id,
    title,
    description,
    summary,
    tokenize='porter unicode61'  -- Stemming for better search
);

-- Index item for search
INSERT INTO items_fts (item_id, title, description, summary)
VALUES (?, ?, ?, ?);

-- Search with ranking
SELECT item_id, rank FROM items_fts 
WHERE items_fts MATCH ? 
ORDER BY rank;
```

---

### Backup & Recovery

```bash
# ✅ Before destructive operations
cp database.db "database_backup_$(date +%Y%m%d_%H%M%S).db"

# ✅ SQLite backup command
sqlite3 database.db ".backup 'backup.db'"
```

```rust
// ✅ Programmatic backup before dangerous ops
fn backup_db_before_migration(db_path: &Path) -> Result<PathBuf, String> {
    let timestamp = chrono::Utc::now().format("%Y%m%d_%H%M%S");
    let backup_path = db_path.with_extension(format!("backup_{}.db", timestamp));
    std::fs::copy(db_path, &backup_path)
        .map_err(|e| format!("Backup failed: {}", e))?;
    Ok(backup_path)
}
```

---

### Schema Documentation

```rust
/// Database schema documentation
/// 
/// ## Tables
/// - `items` - Main entity table
/// - `item_checklist` - Child checklist items
/// - `item_activity` - Audit log
/// - `items_fts` - Full-text search index
/// 
/// ## Indexes
/// - `idx_items_status` - Filter by status
/// - `idx_items_created` - Sort by creation date
```
