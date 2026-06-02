# Performance Domain - Fundamentals

## Overview

This document covers performance fundamentals.

## Performance Principles

### 1. Measure First

```python
import time

def measure_time(func):
    start = time.time()
    result = func()
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed}s")
    return result
```

### 2. Profile Before Optimizing

```bash
# Use profiler
python -m cProfile -s cumulative script.py
```

### 3. Core Web Vitals

- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
