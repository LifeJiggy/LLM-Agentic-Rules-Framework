# Integration Domain - Fundamentals

## Overview

This document covers API and integration fundamentals for LLM/agentic systems.

## API Design Principles

### 1. RESTful Conventions

```python
# Use proper HTTP methods
GET    - Retrieve resources
POST   - Create resources
PUT    - Update entire resource
PATCH  - Partial update
DELETE - Remove resources
```

### 2. Versioning

```python
# Include version in URL
@app.route("/api/v1/users")
def get_users():
    pass

@app.route("/api/v2/users")
def get_users_v2():
    pass
```

### 3. Error Handling

```python
from flask import jsonify

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
