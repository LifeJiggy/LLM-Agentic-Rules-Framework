# Operations Domain - Best Practices

## Overview

This document outlines operations best practices for LLM/agentic systems.

## Deployment Best Practices

### 1. Blue-Green Deployment

```python
class BlueGreenDeployment:
    def __init__(self):
        self.active = "blue"
    
    def deploy(self, version):
        # Deploy to inactive environment
        target = "green" if self.active == "blue" else "blue"
        self._deploy_to(target, version)
        
        # Switch traffic
        self.active = target
    
    def rollback(self):
        # Switch back to previous
        self.active = "blue" if self.active == "green" else "green"
```

### 2. Health Checks

```python
@app.route("/health")
def health():
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "api": check_api()
    }
    
    if all(checks.values()):
        return {"status": "healthy"}, 200
    return {"status": "unhealthy", "checks": checks}, 503
```

### 3. Log Aggregation

```python
import logging
import json

class StructuredLogger:
    def __init__(self, service_name: str):
        self.service = service_name
    
    def log(self, level: str, message: str, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service,
            "level": level,
            "message": message,
            **kwargs
        }
        print(json.dumps(log_entry))
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
