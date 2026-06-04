# Operations Domain - Fundamentals

## Overview

This document covers fundamental operations concepts for LLM/agentic systems, including deployment, monitoring, scaling, and reliability patterns essential for production systems.

---

## Core Operations Principles

### 1. Deployment Fundamentals

```yaml
# Standard container deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: registry.example.com/agent:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              name: agent-config
              key: model
```

### 2. Health Check Patterns

```python
@app.route("/health")
def health():
    checks = {
        "database": _check_database_connection(),
        "model_api": _check_model_api(),
        "cache": _check_cache_connection()
    }
    healthy = all(checks.values())
    return {"healthy": healthy, "checks": checks}, 200 if healthy else 500

@app.route("/ready")
def ready():
    # Check if system can handle traffic
    return {"ready": _can_serve_traffic()}
```

### 3. Configuration Management

```python
class AgentConfig:
    """Environment-aware configuration."""
    
    def __init__(self):
        self.model_name = os.getenv("MODEL_NAME", "gpt-4")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.timeout_seconds = int(os.getenv("TIMEOUT_SECONDS", "30"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def from_file(cls, path: str):
        with open(path) as f:
            config = yaml.safe_load(f)
        return cls(**config)
```

---

## Monitoring Fundamentals

### Key Metrics for AI Systems

| Metric | Purpose | Threshold |
|--------|---------|-----------|
| Request latency | Response time | p50 < 1s, p95 < 5s |
| Error rate | Reliability | < 1% |
| Token usage | Cost control | Budget alert at 80% |
| Active sessions | Concurrency | Scale at 100/session |

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

def log_request(request_id: str, endpoint: str, duration_ms: float, 
               user_id: str = None, tokens: int = 0):
    logger.info(
        "api.request",
        request_id=request_id,
        endpoint=endpoint,
        duration_ms=duration_ms,
        user_id=user_id or "anonymous",
        tokens=tokens
    )
```

---

## Scaling Fundamentals

### Horizontal Scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Incident Response

### Basic Runbook Structure

```markdown
# Incident: High Error Rate

## Symptoms
- Error rate > 5%
- User complaints

## Resolution Steps
1. Check recent deployments
2. Review error logs
3. If model-related, switch to backup model
4. If infrastructure, scale up instances
```

---

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)