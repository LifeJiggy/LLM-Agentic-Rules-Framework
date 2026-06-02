# Performance Domain - Examples

## Overview

Performance examples.

## Example: Benchmarking

```python
import timeit

def benchmark(func, iterations=1000):
    result = timeit.timeit(func, number=iterations)
    print(f"{iterations} iterations: {result:.4f}s")
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
