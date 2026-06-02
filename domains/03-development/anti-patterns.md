# Development Domain - Anti-Patterns

## Overview

This document outlines common development mistakes to avoid.

## Code Anti-Patterns

### 1. God Classes

```python
# Bad - One class doing everything
class GodClass:
    def process(self): ...
    def validate(self): ...
    def save(self): ...
    def email(self): ...
    def report(self): ...

# Good - Focused classes
class Processor: ...
class Validator: ...
class Storage: ...
class Notifier: ...
class Reporter: ...
```

### 2. Magic Numbers

```python
# Bad
if status == 1:
    retry(5)
    wait(3600)

# Good
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 3600
```

### 3. Copy-Paste Code

```python
# Bad - Repeated code
def get_user(id):
    user = db.query(...)
    if user:
        return user
    return None

def get_order(id):
    order = db.query(...)
    if order:
        return order
    return None

# Good - Reusable function
def get_by_id(model, id):
    result = db.query(model, id)
    return result if result else None
```

### 4. Deep Nesting

```python
# Bad
def process(data):
    if data:
        if data.is_valid:
            if data.has_items:
                for item in data.items:
                    process_item(item)

# Good - Early returns
def process(data):
    if not data:
        return
    if not data.is_valid:
        return
    if not data.has_items:
        return
    
    for item in data.items:
        process_item(item)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
