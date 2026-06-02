# Documentation Domain - Best Practices

## Overview

This document outlines documentation best practices.

## Best Practices

### Keep Documentation Close to Code

```
docs/
├── api/
│   └── endpoints.md
├── guides/
│   └── getting-started.md
└── src/
    └── module.py  # Use docstrings
```

### Use OpenAPI/Swagger

```yaml
# openapi.yaml
paths:
  /users:
    get:
      summary: Get users
      responses:
        '200':
          description: List of users
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
