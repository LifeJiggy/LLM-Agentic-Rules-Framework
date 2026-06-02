# Development Domain - Best Practices

## Overview

This document outlines recommended development practices for LLM/agentic systems.

## Code Organization

### Project Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
├── tests/
├── config/
├── docs/
└── requirements.txt
```

### Modular Design

```python
# Bad - All in one file
class DataProcessor:
    def process(self): ...
    def validate(self): ...
    def save(self): ...
    def notify(self): ...

# Good - Separate concerns
class DataProcessor:
    def __init__(self, validator, saver, notifier):
        self.validator = validator
        self.saver = saver
        self.notifier = notifier
```

## Error Handling

### Graceful Degradation

```python
def get_user_data(user_id):
    try:
        data = fetch_from_cache(user_id)
        if not data:
            data = fetch_from_database(user_id)
        return data
    except DatabaseError:
        return get_default_user_data()
```

### Custom Exceptions

```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class PromptError(AgentError):
    """Prompt-related errors."""
    pass

class ToolError(AgentError):
    """Tool execution errors."""
    pass
```

## Documentation

### Docstrings

```python
def calculate_score(items: list) -> float:
    """Calculate average score from list of items.
    
    Args:
        items: List of numeric values
        
    Returns:
        Average score as float
        
    Raises:
        ValueError: If items list is empty
        
    Example:
        >>> calculate_score([10, 20, 30])
        20.0
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    return sum(items) / len(items)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
