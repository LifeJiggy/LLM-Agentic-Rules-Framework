# Operations Domain - Advanced Concepts

## Overview

This document covers advanced operations concepts for LLM/agentic systems.

## Advanced Patterns

### 1. GitOps

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: agent-system
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    path: deploy
  destination:
    server: https://kubernetes.default.svc
    namespace: production
```

### 2. Service Mesh

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: agent-service
spec:
  hosts:
  - agent-service
  http:
  - route:
    - destination:
        host: agent-service
        subset: v1
      weight: 90
    - destination:
        host: agent-service
        subset: v2
      weight: 10
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
