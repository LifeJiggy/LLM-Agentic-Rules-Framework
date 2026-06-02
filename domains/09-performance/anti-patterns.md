# Performance Domain - Anti-Patterns

## Overview

Performance anti-patterns.

## Anti-Patterns

### Premature Optimization

```python
# Bad - Optimize before measuring
def process():
    return [x for x in items]  # Already fine

# Good - Measure first, optimize if needed
def process():
    return list(items)  # Only optimize when proven slow
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
