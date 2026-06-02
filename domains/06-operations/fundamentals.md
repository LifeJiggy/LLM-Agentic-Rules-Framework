# Operations Domain - Fundamentals

## Overview

This document covers operations fundamentals for LLM/agentic systems.

## CI/CD Fundamentals

### 1. Pipeline Stages

```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
      - name: Lint
        run: pylint
```

### 2. Docker Fundamentals

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### 3. Monitoring Basics

```python
import logging

logger = logging.getLogger(__name__)

def log_metric(name: str, value: float, tags: dict = None):
    """Log a metric for monitoring."""
    logger.info(f"METRIC: {name}={value} tags={tags}")
```

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
