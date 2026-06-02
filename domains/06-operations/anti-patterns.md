# Operations Domain - Anti-Patterns

## Overview

This document outlines operations anti-patterns to avoid.

## Anti-Patterns

### 1. Manual Deployments

```python
# Bad - Manual deployment
def deploy():
    # Copy files via FTP
    # Run commands on server
    # Hope it works

# Good - Automated deployment
def deploy():
    pipeline.run("deploy")
```

### 2. No Rollback Plan

```python
# Bad
def deploy():
    update_production()

# Good
def deploy():
    backup_current()
    try:
        update_production()
    except:
        rollback()
```

### 3. Ignoring Monitoring

```python
# Bad
def process():
    result = do_work()
    return result

# Good
def process():
    result = do_work()
    metrics.increment("processed")
    logger.info(f"Processed: {result}")
    return result
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Troubleshooting](./troubleshooting.md)
