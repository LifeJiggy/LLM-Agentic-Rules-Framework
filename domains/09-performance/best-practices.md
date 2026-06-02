# Performance Domain - Best Practices

## Overview

Performance best practices.

## Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(x):
    return compute(x)
```

## Async Operations

```python
import asyncio

async def fetch_all(urls):
    return await asyncio.gather(*[fetch(url) for url in urls])
```

## Database Optimization

```sql
-- Use indexes
CREATE INDEX idx_user_email ON users(email);
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
