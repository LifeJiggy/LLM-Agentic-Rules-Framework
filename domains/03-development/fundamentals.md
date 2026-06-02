# Development Domain - Fundamentals

## Overview

This document covers the fundamental software development principles for LLM/agentic systems.

## Core Development Principles

### 1. Clean Code

```python
# Good code characteristics:
# - Readable
# - Testable
# - Maintainable
# - Simple

def calculate_average(numbers: list) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
```

### 2. SOLID Principles

- **S**ingle Responsibility: One class, one purpose
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable
- **I**nterface Segregation: Many specific interfaces better than one general
- **D**ependency Inversion: Depend on abstractions, not concretions

### 3. Test-Driven Development

```python
def test_calculate_average():
    """Test average calculation."""
    assert calculate_average([1, 2, 3]) == 2.0
    assert calculate_average([]) == 0.0
    assert calculate_average([10]) == 10.0
```

## Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "Add my feature"

# Push and create PR
git push origin feature/my-feature
```

## Code Style

### Naming Conventions

```python
# Variables - snake_case
user_name = "John"
is_active = True

# Functions - snake_case
def get_user_by_id(user_id):
    pass

# Classes - PascalCase
class UserService:
    pass

# Constants - UPPER_SNAKE_CASE
MAX_RETRIES = 3
```

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
