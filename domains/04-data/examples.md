# Data Domain - Examples

## Overview

This document provides data handling examples for LLM/agentic systems.

## Example: Data Repository

```python
class DataRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def find_by_id(self, table, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (id,))
        return cursor.fetchone()
    
    def insert(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        cursor.execute(sql, list(data.values()))
        return cursor.lastrowid
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
