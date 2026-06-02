# Data Domain - Best Practices

## Overview

This document outlines data best practices for LLM/agentic systems.

## Data Management

### 1. Use Transactions

```python
def transfer_funds(from_acc, to_acc, amount):
    with db.transaction():
        db.debit(from_acc, amount)
        db.credit(to_acc, amount)
```

### 2. Prepared Statements

```python
def get_user(user_id):
    return db.query(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
```

### 3. Data Partitioning

```python
def get_shard(user_id, num_shards):
    return user_id % num_shards
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
