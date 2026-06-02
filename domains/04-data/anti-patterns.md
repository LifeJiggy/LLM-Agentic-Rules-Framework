# Data Domain - Anti-Patterns

## Overview

This document outlines data anti-patterns to avoid.

## Anti-Patterns

### 1. Storing Sensitive Data in Plain Text

```python
# Bad
def save_password(user_id, password):
    db.execute(f"UPDATE users SET password = '{password}' WHERE id = {user_id}")

# Good
def save_password(user_id, password):
    hashed = hash_password(password)
    db.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))
```

### 2. Not Using Indexes

```python
# Bad - Full table scan
def find_user(name):
    return db.query("SELECT * FROM users WHERE name = ?", (name,))

# Good - With index
# CREATE INDEX idx_name ON users(name)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
