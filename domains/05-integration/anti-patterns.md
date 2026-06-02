# Integration Domain - Anti-Patterns

## Overview

This document outlines integration anti-patterns to avoid.

## Anti-Patterns

### 1. No Timeout on External Calls

```python
# Bad - No timeout
requests.get(url)

# Good - With timeout
requests.get(url, timeout=5)
```

### 2. Hardcoded URLs

```python
# Bad
api_url = "http://localhost:8000"

# Good
api_url = os.environ.get("API_URL")
```

### 3. Not Handling API Errors

```python
# Bad
result = api.call()

# Good
try:
    result = api.call()
except APIError as e:
    logger.error(f"API call failed: {e}")
    return fallback()
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
