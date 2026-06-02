# Data Domain - Fundamentals

## Overview

This document covers data handling fundamentals for LLM/agentic systems.

## Data Principles

### 1. Data Validation

```python
def validate_user_data(data: dict) -> bool:
    """Validate incoming user data."""
    required_fields = ["name", "email"]
    return all(field in data for field in required_fields)
```

### 2. Data Serialization

```python
import json

def serialize(data):
    return json.dumps(data)

def deserialize(data):
    return json.loads(data)
```

### 3. Data Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_data(key):
    return fetch_from_db(key)
```

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
