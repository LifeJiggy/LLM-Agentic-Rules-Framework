# Documentation Domain - Anti-Patterns

## Overview

This document outlines documentation anti-patterns.

## Anti-Patterns

### 1. Outdated Documentation

```python
# Bad - Docs don't match code
def process():
    """Process takes one parameter."""
    pass  # Actually takes two now

# Good - Keep docs updated
def process(user, data):
    """Process user data.
    
    Args:
        user: User object
        data: Data dict
    """
```

### 2. No Examples

```python
# Bad - No usage example
def authenticate(token):
    """Authenticate using token."""
    pass

# Good - With examples
def authenticate(token):
    """Authenticate using token.
    
    Example:
        >>> authenticate("abc123")
        User(id=1)
    """
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
