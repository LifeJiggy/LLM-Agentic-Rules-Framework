# Deployment Anti-Patterns for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Manual Deployments](#manual-deployments)
3. [No Rollback Plan](#no-rollback-plan)
4. [Skipping Testing](#skipping-testing)
5. [Configuration Drift](#configuration-drift)
6. [Secrets in Code](#secrets-in-code)
7. [No Monitoring](#no-monitoring)
8. [Big Bang Deployments](#big-bang-deployments)
9. [Ignoring Dependencies](#ignoring-dependencies)
10. [Inadequate Documentation](#inadequate-documentation)
11. [Conclusion](#conclusion)

---

## Overview

Anti-patterns are common but ineffective or counterproductive practices that appear beneficial but actually lead to problems. In deployment, these anti-patterns can cause downtime, security vulnerabilities, and operational nightmares.

This document identifies the most common deployment anti-patterns and provides solutions to avoid them.

### Why Anti-Patterns Matter

- **Increased Risk**: Anti-patterns make deployments more likely to fail
- **Longer Recovery**: When things go wrong, recovery takes longer
- **Technical Debt**: Anti-patterns accumulate technical debt over time
- **Team Frustration**: Teams become frustrated with unreliable processes

---

## Manual Deployments

### The Problem

Manual deployments involve human intervention at multiple steps, increasing the risk of errors and inconsistencies.

```
Manual Deployment Flow (Anti-Pattern):
1. Developer SSHs into server
2. Pulls latest code from Git
3. Installs dependencies manually
4. Restarts services manually
5. Tests manually
6. Forgets to update configuration
7. Service breaks in production
```

### Why It's Bad

- **Human Error**: Manual steps are prone to mistakes
- **Inconsistency**: Different people deploy differently
- **No Audit Trail**: Hard to track what was deployed and when
- **Slow**: Manual processes take longer than automated ones
- **Not Repeatable**: Difficult to replicate exactly

### The Solution

```yaml
# automated-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  annotations:
    deployment.kubernetes.io/revision: "1"
    kubernetes.io/change-cause: "Automated deployment via CI/CD"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
  template:
    metadata:
      labels:
        app: llm-api
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          ports:
            - containerPort: 8080
```

```yaml
# .github/workflows/automated-deploy.yaml
name: Automated Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: pytest tests/ -v

      - name: Build and push image
        run: |
          docker build -t llm-api:${{ github.sha }} .
          docker push llm-api:${{ github.sha }}

      - name: Deploy to production
        run: |
          kubectl set image deployment/llm-api \
            llm-api=llm-api:${{ github.sha }} \
            --namespace=production
          kubectl rollout status deployment/llm-api \
            --namespace=production \
            --timeout=300s
```

---

## No Rollback Plan

### The Problem

Deploying without a clear rollback plan means that when things go wrong, there's no quick way to recover.

```
No Rollback Plan (Anti-Pattern):
1. Deploy new version
2. New version has critical bug
3. Panic: "How do we go back?"
4. Manual intervention required
5. Downtime increases
6. Revenue lost
```

### Why It's Bad

- **Extended Downtime**: Without rollback, issues take longer to resolve
- **Increased Risk**: Teams are afraid to deploy because recovery is hard
- **Data Loss**: In extreme cases, data may be lost during manual recovery
- **Team Stress**: On-call engineers face high-pressure situations

### The Solution

```yaml
# rollback-strategy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3
```

```bash
#!/bin/bash
# rollback.sh - Automated rollback script

set -e

DEPLOYMENT_NAME="llm-api"
NAMESPACE="${1:-production}"
REVISION="${2:-}"

echo "Rolling back deployment: $DEPLOYMENT_NAME in namespace: $NAMESPACE"

if [ -n "$REVISION" ]; then
    echo "Rolling back to revision: $REVISION"
    kubectl rollout undo deployment/$DEPLOYMENT_NAME \
        --namespace=$NAMESPACE \
        --to-revision=$REVISION
else
    echo "Rolling back to previous revision"
    kubectl rollout undo deployment/$DEPLOYMENT_NAME \
        --namespace=$NAMESPACE
fi

echo "Waiting for rollout to complete..."
kubectl rollout status deployment/$DEPLOYMENT_NAME \
    --namespace=$NAMESPACE \
    --timeout=300s

echo "Rollback complete!"
kubectl get pods -l app=$DEPLOYMENT_NAME -n $NAMESPACE
```

---

## Skipping Testing

### The Problem

Skipping tests before deployment is a gamble that often fails. Without proper testing, bugs slip into production.

```
Skipping Tests (Anti-Prompt):
1. "We don't have time for tests"
2. Deploy directly to production
3. Bug causes outage
4. Customer complaints
5. Emergency hotfix
6. More time spent fixing than testing would have taken
```

### Why It's Bad

- **Bugs in Production**: Undetected bugs reach users
- **Increased Downtime**: Bugs cause outages that take time to fix
- **Customer Impact**: Users experience poor service
- **Technical Debt**: Quick fixes accumulate technical debt

### The Solution

```yaml
# testing-gate.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: testing-gate
data:
  test-stages.json: |
    {
      "stages": [
        {
          "name": "unit-tests",
          "command": "pytest tests/unit/ -v --tb=short",
          "required": true,
          "timeout": "10m"
        },
        {
          "name": "integration-tests",
          "command": "pytest tests/integration/ -v",
          "required": true,
          "timeout": "20m"
        },
        {
          "name": "smoke-tests",
          "command": "pytest tests/smoke/ -v --api-url=https://staging.llm-api.example.com",
          "required": true,
          "timeout": "10m"
        },
        {
          "name": "load-tests",
          "command": "locust -f tests/load/locustfile.py --host=https://staging.llm-api.example.com --headless -u 100 -r 10 --run-time 5m",
          "required": true,
          "timeout": "10m"
        }
      ]
    }
```

---

## Configuration Drift

### The Problem

Configuration drift occurs when environments become inconsistent over time due to manual changes or untracked modifications.

```
Configuration Drift (Anti-Pattern):
Development:  MODEL_CACHE_SIZE=100
Staging:      MODEL_CACHE_SIZE=500
Production:   MODEL_CACHE_SIZE=1000 (manually changed)
Result:       Inconsistent behavior across environments
```

### Why It's Bad

- **Inconsistent Behavior**: Same code behaves differently in different environments
- **Debugging Difficulty**: Hard to reproduce issues in development
- **Security Risks**: Untracked changes may introduce vulnerabilities
- **Compliance Issues**: Hard to prove environments are configured correctly

### The Solution

```yaml
# configuration-management.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-api-config
  namespace: production
  labels:
    app: llm-api
    environment: production
    managed-by: terraform
  annotations:
    terraform.io/module: llm-api-config
data:
  MODEL_CACHE_SIZE: "2000"
  MAX_CONCURRENT_REQUESTS: "200"
  LOG_LEVEL: "WARNING"
  ENABLE_TRACING: "true"
```

```bash
#!/bin/bash
# drift-detection.sh - Detect configuration drift

echo "Checking for configuration drift..."

# Get current configmap
CURRENT_CONFIG=$(kubectl get configmap llm-api-config -n production -o yaml)

# Compare with expected config
EXPECTED_CONFIG=$(cat k8s/configmaps/production.yaml)

if [ "$CURRENT_CONFIG" != "$EXPECTED_CONFIG" ]; then
    echo "Configuration drift detected!"
    echo "Applying expected configuration..."
    kubectl apply -f k8s/configmaps/production.yaml -n production
    echo "Configuration drift corrected."
else
    echo "No configuration drift detected."
fi
```

---

## Secrets in Code

### The Problem

Hardcoding secrets (API keys, passwords, tokens) in source code is a serious security vulnerability.

```python
# ANTI-PATTERN: Secrets in code
import os

# NEVER DO THIS
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "supersecretpassword"
REDIS_PASSWORD = "redispassword123"

# Even worse - in configuration files
# config.py
CONFIG = {
    "api_key": "sk-1234567890abcdef",
    "database_url": "postgresql://admin:supersecretpassword@db:5432/llm_api"
}
```

### Why It's Bad

- **Security Risk**: Secrets exposed in version control
- **Access Control**: Hard to rotate or revoke secrets
- **Compliance Violations**: Violates security policies and regulations
- **Audit Trail**: Hard to track who has access to secrets

### The Solution

```python
# CORRECT: Environment variables
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    redis_password: str = os.getenv("REDIS_PASSWORD")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: llm-api-secrets
  namespace: production
type: Opaque
data:
  api-key: c2stMTIzNDU2Nzg5MGFiY2RlZg==  # base64 encoded
  database-password: c3VwZXJzZWNyZXRwYXNzd29yZA==  # base64 encoded
  redis-password: cmVkaXNwYXNzd29yZDEyMw==  # base64 encoded
```

```yaml
# k8s/deployment-with-secrets.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          envFrom:
            - secretRef:
                name: llm-api-secrets
          env:
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: llm-api-secrets
                  key: api-key
```

---

## No Monitoring

### The Problem

Deploying without proper monitoring means you won't know something is wrong until users complain.

```
No Monitoring (Anti-Pattern):
1. Deploy new version
2. New version has performance issue
3. No monitoring detects the issue
4. Users experience slow response times
5. User complaints flood in
6. Team discovers issue hours later
7. Extended period of degraded service
```

### Why It's Bad

- **Delayed Detection**: Issues go unnoticed for hours
- **Poor User Experience**: Users suffer without your knowledge
- **Reactive Response**: Team is always firefighting instead of preventing
- **No Baseline**: Hard to measure improvement without metrics

### The Solution

```yaml
# monitoring-stack.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: monitoring-config
data:
  prometheus.yaml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "alerts/*.yaml"
    
    alerting:
      alertmanagers:
        - static_configs:
            - targets:
                - alertmanager:9093
    
    scrape_configs:
      - job_name: 'llm-api'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - production
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
  
  alerts.yaml: |
    groups:
      - name: llm-api-alerts
        rules:
          - alert: HighErrorRate
            expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "High error rate detected"
              description: "Error rate is {{ $value }}%"
          
          - alert: HighLatency
            expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High latency detected"
              description: "99th percentile latency is {{ $value }}s"
          
          - alert: HighMemoryUsage
            expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High memory usage"
              description: "Memory usage is {{ $value | humanizePercentage }}"
```

---

## Big Bang Deployments

### The Problem

Deploying all changes at once to all users simultaneously increases risk and makes rollback difficult.

```
Big Bang Deployment (Anti-Pattern):
1. Accumulate many changes
2. Deploy everything at once
3. If something breaks, impossible to identify which change caused it
4. Rollback means reverting all changes, even good ones
```

### Why It's Bad

- **High Risk**: More changes mean more potential failure points
- **Difficult Debugging**: Hard to identify which change caused an issue
- **All-or-Nothing Rollback**: Either keep all changes or revert everything
- **Long Deployment Window**: Large deployments take longer and require more coordination

### The Solution

```yaml
# feature-flags.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  flags.yaml: |
    flags:
      enable-new-embedding-model:
        description: "Enable the new sentence-transformers embedding model"
        enabled: false
        type: release
        variations:
          - name: enabled
            value: true
          - name: disabled
            value: false
        rules:
          - variation: enabled
            conditions:
              - attribute: user_segment
                operator: in
                values: ["beta_testers", "internal"]
        default_variation: disabled

      enable-agentic-tools:
        description: "Enable tool-use capabilities for the LLM agent"
        enabled: true
        type: release
        variations:
          - name: enabled
            value: true
          - name: disabled
            value: false
        rules:
          - variation: enabled
            conditions:
              - attribute: subscription_tier
                operator: in
                values: ["enterprise", "pro"]
        default_variation: disabled
```

---

## Ignoring Dependencies

### The Problem

Deploying changes without considering dependencies on other services or components can cause cascading failures.

```
Ignoring Dependencies (Anti-Pattern):
1. Service A depends on Service B
2. Service B is updated with breaking changes
3. Service A is not updated to handle new API
4. Service A fails in production
5. Cascading failure across the system
```

### Why It's Bad

- **Cascading Failures**: One service failure can take down others
- **Integration Issues**: Services may not work together after independent updates
- **Testing Difficulty**: Hard to test all dependencies together
- **Coordination Overhead**: Teams must coordinate deployments manually

### The Solution

```yaml
# dependency-management.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-dependencies
data:
  dependencies.yaml: |
    services:
      llm-api:
        dependencies:
          - name: database
            type: postgresql
            required: true
            health_check: /health/database
          - name: redis
            type: redis
            required: true
            health_check: /health/redis
          - name: embedding-service
            type: http
            required: false
            health_check: /health/embeddings
            fallback: cache
    
    deployment_order:
      - database
      - redis
      - embedding-service
      - llm-api
    
    rollback_triggers:
      - service: database
        condition: unhealthy
        action: rollback
      - service: redis
        condition: unhealthy
        action: rollback
      - service: embedding-service
        condition: unhealthy
        action: warn
```

---

## Inadequate Documentation

### The Problem

Deploying without proper documentation makes it difficult for team members to understand and maintain the system.

```
Inadequate Documentation (Anti-Pattern):
1. Deploy new version
2. Team member asks: "How do I deploy this?"
3. No one remembers the exact steps
4. Mistakes made during deployment
5. Deployment takes longer than expected
```

### Why It's Bad

- **Knowledge Silos**: Only a few people know how to deploy
- **Onboarding Difficulty**: New team members struggle to contribute
- **Deployment Errors**: Without clear steps, mistakes happen
- **Slow Recovery**: During incidents, lack of documentation delays resolution

### The Solution

```yaml
# deployment-documentation.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: deployment-documentation
data:
  deployment-runbook.md: |
    # Deployment Runbook
    
    ## Prerequisites
    - Access to production cluster
    - kubectl configured with correct context
    - Helm 3.x installed
    
    ## Deployment Steps
    
    1. **Pre-deployment checks**
       ```bash
       # Verify current state
       kubectl get pods -n production
       kubectl get deployment llm-api -n production
       ```
    
    2. **Deploy new version**
       ```bash
       # Update deployment
       kubectl set image deployment/llm-api \
         llm-api=llm-api:1.3.0 \
         --namespace=production
       
       # Wait for rollout
       kubectl rollout status deployment/llm-api \
         --namespace=production \
         --timeout=300s
       ```
    
    3. **Verify deployment**
       ```bash
       # Check pod status
       kubectl get pods -l app=llm-api -n production
       
       # Run smoke tests
       curl -f https://llm-api.example.com/health/ready
       ```
    
    4. **Rollback (if needed)**
       ```bash
       # Rollback to previous version
       kubectl rollout undo deployment/llm-api \
         --namespace=production
       
       # Wait for rollback
       kubectl rollout status deployment/llm-api \
         --namespace=production \
         --timeout=300s
       ```
    
    ## Troubleshooting
    
    ### Pod not starting
    - Check events: `kubectl describe pod <pod-name> -n production`
    - Check logs: `kubectl logs <pod-name> -n production`
    
    ### Health check failing
    - Verify database connectivity
    - Verify Redis connectivity
    - Check model loading status
  ```

---

## Conclusion

Avoiding these deployment anti-patterns is crucial for maintaining reliable, secure, and maintainable AI/LLM systems. By automating deployments, implementing proper testing, managing configuration, securing secrets, monitoring systems, and documenting processes, teams can deploy with confidence and minimize risk.

Key takeaways:

1. **Automate everything** - Manual processes are error-prone
2. **Always have a rollback plan** - Recovery should be quick and predictable
3. **Test thoroughly** - Never skip testing stages
4. **Manage configuration properly** - Prevent drift and inconsistencies
5. **Secure secrets** - Never hardcode sensitive information
6. **Monitor everything** - Detect issues before users do
7. **Deploy small changes** - Small, frequent deployments reduce risk
8. **Consider dependencies** - Coordinate with dependent services
9. **Document processes** - Make knowledge accessible to the team

---

## Quick Reference: Anti-Pattern to Solution Mapping

| Anti-Pattern | Impact | Solution |
|--------------|--------|----------|
| Manual Deployments | Human error, inconsistency | CI/CD automation |
| No Rollback Plan | Extended downtime | Automated rollback procedures |
| Skipping Testing | Bugs in production | Multi-stage testing pipeline |
| Configuration Drift | Inconsistent environments | Infrastructure as Code |
| Secrets in Code | Security vulnerabilities | Secret management systems |
| No Monitoring | Delayed issue detection | Comprehensive observability |
| Big Bang Deployments | High risk, difficult debugging | Feature flags, canary deployments |
| Ignoring Dependencies | Cascading failures | Dependency mapping, circuit breakers |
| Inadequate Documentation | Knowledge silos | Runbooks, automated documentation |

---

## Common Anti-Pattern Recovery Strategies

### If You Have Manual Deployments

```
Immediate: Document current process
Short-term: Create CI/CD pipeline for critical paths
Long-term: Automate all deployments
Timeline: 2-4 weeks
```

### If You Have No Rollback Plan

```
Immediate: Document current deployment state
Short-term: Implement rollback scripts
Long-term: Automated rollback with health checks
Timeline: 1-2 weeks
```

### If You Skip Testing

```
Immediate: Add basic smoke tests
Short-term: Implement unit and integration tests
Long-term: Complete test coverage with automation
Timeline: 4-8 weeks
```

### If You Have Configuration Drift

```
Immediate: Document current configuration
Short-term: Implement ConfigMaps/Secrets
Long-term: Full Infrastructure as Code
Timeline: 2-4 weeks
```

### If You Have Secrets in Code

```
Immediate: Rotate exposed secrets
Short-term: Move to environment variables
Long-term: Implement secret management system
Timeline: 1-2 weeks
```

### If You Have No Monitoring

```
Immediate: Add basic health checks
Short-term: Implement metrics and logging
Long-term: Full observability stack
Timeline: 2-4 weeks
```

---

## Anti-Pattern Prevention Checklist

### Process Checklist

- [ ] Deployment process is documented
- [ ] Rollback procedure is documented
- [ ] Testing stages are defined
- [ ] Configuration management is defined
- [ ] Secret management is defined
- [ ] Monitoring strategy is defined
- [ ] Communication plan is defined
- [ ] Training is provided to team

### Technical Checklist

- [ ] CI/CD pipeline is configured
- [ ] Automated tests are implemented
- [ ] Infrastructure as Code is implemented
- [ ] Secret management is implemented
- [ ] Monitoring and alerting is configured
- [ ] Logging is configured
- [ ] Health checks are implemented
- [ ] Rollback automation is implemented

### Cultural Checklist

- [ ] Team understands anti-patterns
- [ ] Team is trained on best practices
- [ ] Team follows deployment checklist
- [ ] Team communicates during deployments
- [ ] Team learns from incidents
- [ ] Team shares knowledge
- [ ] Team improves processes continuously
- [ ] Team celebrates successful deployments
