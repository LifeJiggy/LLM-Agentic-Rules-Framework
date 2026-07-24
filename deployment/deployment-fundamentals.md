# Deployment Fundamentals for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Deployment Strategies](#deployment-strategies)
   - [Blue-Green Deployment](#blue-green-deployment)
   - [Canary Deployment](#canary-deployment)
   - [Rolling Deployment](#rolling-deployment)
   - [Shadow Deployment](#shadow-deployment)
   - [Feature Flag Deployment](#feature-flag-deployment)
3. [CI/CD Pipelines](#cicd-pipelines)
   - [Pipeline Architecture](#pipeline-architecture)
   - [Build Stage](#build-stage)
   - [Test Stage](#test-stage)
   - [Deploy Stage](#deploy-stage)
   - [Post-Deploy Stage](#post-deploy-stage)
4. [Environment Management](#environment-management)
   - [Environment Hierarchy](#environment-hierarchy)
   - [Environment Configuration](#environment-configuration)
   - [Environment Promotion](#environment-promotion)
5. [Configuration Management](#configuration-management)
   - [Configuration Sources](#configuration-sources)
   - [Configuration Validation](#configuration-validation)
   - [Dynamic Configuration](#dynamic-configuration)
6. [Feature Flags](#feature-flags)
   - [Feature Flag Types](#feature-flag-types)
   - [Feature Flag Strategies](#feature-flag-strategies)
   - [Feature Flag Lifecycle](#feature-flag-lifecycle)
7. [Rollback Procedures](#rollback-procedures)
   - [Automatic Rollback](#automatic-rollback)
   - [Manual Rollback](#manual-rollback)
   - [Partial Rollback](#partial-rollback)
8. [LLM-Specific Deployment Considerations](#llm-specific-deployment-considerations)
9. [Summary](#summary)

---

## Overview

Deployment is the process of releasing software changes to production environments in a controlled, reliable, and repeatable manner. For LLM and agentic systems, deployment carries additional complexity due to model versioning, GPU resource management, inference latency requirements, and the need for gradual rollout strategies that minimize risk.

This document covers the core concepts and practices essential for deploying AI/LLM systems effectively.

### Key Principles

- **Reliability**: Deployments should succeed consistently without human intervention
- **Reversibility**: Every deployment must have a clear rollback path
- **Observability**: Every deployment must be accompanied by monitoring and alerting
- **Automation**: Manual steps are error-prone; automate everything possible
- **Gradual Rollout**: Never expose all users to untested changes simultaneously

### Deployment vs Release

```
Deployment = Making code available in a target environment
Release    = Making features available to end users

Deployment can happen without release (behind feature flags)
Release can happen without deployment (feature flag toggle)
```

---

## Deployment Strategies

### Blue-Green Deployment

Blue-green deployment maintains two identical production environments. At any time, only one serves live traffic.

#### How It Works

```
┌─────────────┐     ┌─────────────┐
│   Blue       │     │   Green      │
│  (Active)    │     │  (Standby)  │
│  v1.2.0      │     │  v1.3.0     │
└──────┬───────┘     └──────┬──────┘
       │                     │
       └──────────┬──────────┘
                  │
            ┌─────┴─────┐
            │  Load     │
            │  Balancer │
            └───────────┘
```

#### Deployment Process

1. Deploy new version to Green environment
2. Run smoke tests against Green
3. Switch load balancer from Blue to Green
4. Keep Blue as rollback target
5. After validation period, decommission Blue

#### YAML Configuration

```yaml
# blue-green-deployment.yaml
apiVersion: v1
kind: Service
metadata:
  name: llm-api-service
  labels:
    app: llm-api
spec:
  type: LoadBalancer
  selector:
    app: llm-api
    slot: blue  # Switch to 'green' during deployment
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api-blue
  labels:
    app: llm-api
    slot: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
      slot: blue
  template:
    metadata:
      labels:
        app: llm-api
        slot: blue
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.2.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
            limits:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api-green
  labels:
    app: llm-api
    slot: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
      slot: green
  template:
    metadata:
      labels:
        app: llm-api
        slot: green
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
            limits:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
```

#### Advantages

- Zero downtime deployments
- Instant rollback by switching traffic back
- Full testing of production environment before go-live
- Simple to understand and implement

#### Disadvantages

- Double the infrastructure cost
- Database schema changes require careful planning
- Stateful services complicate the approach
- Session persistence issues during switchover

---

### Canary Deployment

Canary deployment gradually shifts traffic from the old version to the new version, monitoring for issues at each stage.

#### How It Works

```
Phase 1: 95% old / 5% new
    ┌──────────────────────────────────────┐
    │ ████████████████████████████░░░░░░░░ │
    │          v1.2.0          │ v1.3.0    │
    └──────────────────────────────────────┘

Phase 2: 80% old / 20% new
    ┌──────────────────────────────────────┐
    │ ██████████████████████░░░░░░░░░░░░░ │
    │          v1.2.0       │   v1.3.0    │
    └──────────────────────────────────────┘

Phase 3: 50% old / 50% new
    ┌──────────────────────────────────────┐
    │ ████████████████░░░░░░░░░░░░░░░░░░░ │
    │      v1.2.0     │      v1.3.0       │
    └──────────────────────────────────────┘

Phase 4: 0% old / 100% new
    ┌──────────────────────────────────────┐
    │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
    │              v1.3.0                  │
    └──────────────────────────────────────┘
```

#### YAML Configuration

```yaml
# canary-deployment.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: llm-api-canary
spec:
  hosts:
    - llm-api.example.com
  http:
    - route:
        - destination:
            host: llm-api-stable
            port:
              number: 8080
          weight: 95
        - destination:
            host: llm-api-canary
            port:
              number: 8080
          weight: 5
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: llm-api-destination
spec:
  host: llm-api
  subsets:
    - name: stable
      labels:
        version: v1.2.0
    - name: canary
      labels:
        version: v1.3.0
```

#### Canary Analysis

```yaml
# canary-analysis.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: llm-api-canary
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  progressDeadlineSeconds: 600
  service:
    port: 8080
    targetPort: 8080
    gateways:
      - llm-api-gateway
    hosts:
      - llm-api.example.com
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
      - name: llm-inference-latency-p99
        thresholdRange:
          max: 2000
        interval: 30s
      - name: llm-error-rate
        thresholdRange:
          max: 1
        interval: 1m
```

---

### Rolling Deployment

Rolling deployment incrementally replaces instances of the previous version with the new version.

#### How It Works

```
Step 1: [v1] [v1] [v1] [v1]
Step 2: [v2] [v1] [v1] [v1]
Step 3: [v2] [v2] [v1] [v1]
Step 4: [v2] [v2] [v2] [v1]
Step 5: [v2] [v2] [v2] [v2]
```

#### YAML Configuration

```yaml
# rolling-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  labels:
    app: llm-api
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: llm-api
  template:
    metadata:
      labels:
        app: llm-api
        version: v1.3.0
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 15
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
            limits:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
```

---

### Shadow Deployment

Shadow deployment sends a copy of production traffic to the new version without affecting users.

#### How It Works

```
                    ┌───────────────┐
                    │  Load Balancer│
                    └───────┬───────┘
                            │
               ┌────────────┼────────────┐
               │            │            │
               ▼            ▼            ▼
         ┌──────────┐ ┌──────────┐ ┌──────────┐
         │  v1.2.0  │ │  v1.2.0  │ │  v1.3.0  │
         │ (Active) │ │ (Active) │ │ (Shadow) │
         └──────────┘ └──────────┘ └──────────┘
               │            │            │
               ▼            ▼            ▼
         ┌──────────┐ ┌──────────┐ ┌──────────┐
         │ Response │ │ Response │ │ Metrics  │
         │ to User  │ │ to User  │ │ & Logs   │
         └──────────┘ └──────────┘ └──────────┘
```

#### YAML Configuration

```yaml
# shadow-deployment.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: llm-api-shadow
spec:
  hosts:
    - llm-api.example.com
  http:
    - route:
        - destination:
            host: llm-api-stable
            port:
              number: 8080
      mirror:
        host: llm-api-shadow
        port:
          number: 8080
      mirrorPercentage:
        value: 100
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api-shadow
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
      slot: shadow
  template:
    metadata:
      labels:
        app: llm-api
        slot: shadow
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
            limits:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
```

---

### Feature Flag Deployment

Feature flag deployment decouples deployment from release, allowing code to be deployed but not activated until a flag is toggled.

#### How It Works

```yaml
# feature-flag-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  enable-new-llm-model.json: |
    {
      "enabled": false,
      "rules": [
        {
          "variation": "enabled",
          "conditions": [
            {
              "attribute": "user_id",
              "operator": "in",
              "values": ["test-user-1", "test-user-2"]
            }
          ]
        }
      ],
      "variations": [
        { "value": true, "name": "enabled" },
        { "value": false, "name": "disabled" }
      ]
    }
  enable-agentic-tools.json: |
    {
      "enabled": true,
      "rules": [
        {
          "variation": "enabled",
          "conditions": [
            {
              "attribute": "beta_user",
              "operator": "equals",
              "value": "true"
            }
          ]
        }
      ],
      "variations": [
        { "value": true, "name": "enabled" },
        { "value": false, "name": "disabled" }
      ]
    }
```

---

## CI/CD Pipelines

### Pipeline Architecture

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Source  │───▶│  Build  │───▶│  Test   │───▶│ Deploy  │───▶│ Monitor │
│  Control │    │         │    │         │    │         │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  Git Push      Docker Build   Unit Tests    Blue-Green     Metrics
  PR Merge      Model Fetch    Integration   Canary         Logs
  Webhook       Dep Install    Load Tests    Rolling        Alerts
```

### GitHub Actions Pipeline

```yaml
# .github/workflows/llm-deploy.yaml
name: LLM Deployment Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/llm-api
  MODEL_REGISTRY: models.example.com

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint and type check
        run: |
          ruff check src/
          mypy src/

      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml

      - name: Build Docker image
        run: |
          docker build \
            --build-arg MODEL_VERSION=${{ github.sha }} \
            --tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest .

      - name: Push to registry
        if: github.event_name != 'pull_request'
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ${{ env.REGISTRY }} -u ${{ github.actor }} --password-stdin
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  integration-test:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name != 'pull_request'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          kubectl set image deployment/llm-api-staging \
            llm-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/llm-api-staging \
            --namespace=staging \
            --timeout=300s

      - name: Run integration tests
        run: |
          pytest tests/integration/ -v \
            --api-url=https://staging.llm-api.example.com

      - name: Run load tests
        run: |
          locust -f tests/load/locustfile.py \
            --host=https://staging.llm-api.example.com \
            --headless \
            -u 100 -r 10 \
            --run-time 5m

  canary-deploy:
    needs: integration-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy canary
        run: |
          kubectl apply -f k8s/canary/

      - name: Update canary weight
        run: |
          kubectl patch virtualservice llm-api-canary \
            --type merge \
            -p '{"spec":{"http":[{"route":[{"destination":{"host":"llm-api-stable","port":{"number":8080}},"weight":95},{"destination":{"host":"llm-api-canary","port":{"number":8080}},"weight":5}]}]}}'

      - name: Monitor canary metrics
        run: |
          for i in {1..12}; do
            echo "Checking canary metrics (iteration $i)..."
            ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~'5..',version='canary'}[5m])/rate(http_requests_total{version='canary'}[5m])*100" | jq '.data.result[0].value[1]' -r)
            if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
              echo "Canary error rate too high: $ERROR_RATE%"
              exit 1
            fi
            sleep 300
          done

      - name: Promote canary to stable
        run: |
          kubectl set image deployment/llm-api-stable \
            llm-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/llm-api-stable --timeout=300s
```

---

## Environment Management

### Environment Hierarchy

```
Development (Local)
    │
    ▼
Integration (Shared)
    │
    ▼
Staging (Production-like)
    │
    ▼
Production (Live)
```

### Environment Configuration

```yaml
# environments/development.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-api-config
  namespace: development
data:
  LOG_LEVEL: "DEBUG"
  MODEL_CACHE_SIZE: "100"
  MAX_CONCURRENT_REQUESTS: "10"
  ENABLE_TRACING: "true"
  ENABLE_METRICS: "false"
  REDIS_URL: "redis://redis-dev:6379"
  DATABASE_URL: "postgresql://dev:dev@postgres-dev:5432/llm_api"
---
# environments/staging.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-api-config
  namespace: staging
data:
  LOG_LEVEL: "INFO"
  MODEL_CACHE_SIZE: "500"
  MAX_CONCURRENT_REQUESTS: "50"
  ENABLE_TRACING: "true"
  ENABLE_METRICS: "true"
  REDIS_URL: "redis://redis-staging:6379"
  DATABASE_URL: "postgresql://staging:secret@postgres-staging:5432/llm_api"
---
# environments/production.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-api-config
  namespace: production
data:
  LOG_LEVEL: "WARNING"
  MODEL_CACHE_SIZE: "2000"
  MAX_CONCURRENT_REQUESTS: "200"
  ENABLE_TRACING: "true"
  ENABLE_METRICS: "true"
  REDIS_URL: "redis://redis-prod:6379"
  DATABASE_URL: "postgresql://prod:secret@postgres-prod:5432/llm_api"
```

---

## Configuration Management

### Configuration Sources

```
┌─────────────────────────────────────────────┐
│              Configuration Sources          │
├─────────────┬─────────────┬─────────────────┤
│  Defaults   │  Environment│  Config Files   │
│  (Code)     │  Variables  │  (YAML/JSON)   │
├─────────────┼─────────────┼─────────────────┤
│  ConfigMaps │  Secrets    │  Feature Flags  │
│  (K8s)      │  (K8s)      │  (LaunchDarkly) │
└─────────────┴─────────────┴─────────────────┘
```

### Configuration Validation

```yaml
# configmap-validator.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-api-config-validator
data:
  validate-config.py: |
    import os
    import sys
    import json

    required_vars = [
        'MODEL_NAME',
        'MODEL_VERSION',
        'MAX_TOKENS',
        'TEMPERATURE',
        'REDIS_URL',
        'DATABASE_URL'
    ]

    numeric_vars = {
        'MAX_TOKENS': (1, 4096),
        'TEMPERATURE': (0.0, 2.0),
        'TOP_P': (0.0, 1.0),
        'MAX_CONCURRENT_REQUESTS': (1, 1000),
        'MODEL_CACHE_SIZE': (1, 10000)
    }

    def validate_config():
        errors = []

        for var in required_vars:
            if var not in os.environ:
                errors.append(f"Missing required variable: {var}")

        for var, (min_val, max_val) in numeric_vars.items():
            if var in os.environ:
                try:
                    value = float(os.environ[var])
                    if value < min_val or value > max_val:
                        errors.append(f"{var}={value} out of range [{min_val}, {max_val}]")
                except ValueError:
                    errors.append(f"{var} is not a valid number")

        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            sys.exit(1)

        print("Configuration validation passed")
        return True

    if __name__ == '__main__':
        validate_config()
```

---

## Feature Flags

### Feature Flag Types

```
Release Flags    → Gradual rollout of features
Experiment Flags → A/B testing and experiments
Ops Flags        → Operational toggles (circuit breakers)
Permission Flags → User/role-based access control
```

### Feature Flag Configuration

```yaml
# feature-flags-configmap.yaml
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

      max-context-window:
        description: "Maximum context window size"
        enabled: true
        type: ops
        variations:
          - name: standard
            value: 8192
          - name: extended
            value: 32768
          - name: max
            value: 131072
        rules:
          - variation: max
            conditions:
              - attribute: subscription_tier
                operator: equals
                value: enterprise
          - variation: extended
            conditions:
              - attribute: subscription_tier
                operator: equals
                value: pro
        default_variation: standard
```

---

## Rollback Procedures

### Automatic Rollback

```yaml
# rollback-deployment.yaml
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
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 15
            failureThreshold: 3
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: llm-api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: llm-api
```

### Manual Rollback Script

```bash
#!/bin/bash
# rollback.sh - Manual rollback script

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

## LLM-Specific Deployment Considerations

### Model Versioning

```yaml
# model-registry.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: model-registry
data:
  models.json: |
    {
      "models": {
        "gpt-4-turbo": {
          "version": "2024-04-09",
          "endpoint": "https://api.openai.com/v1",
          "max_tokens": 128000,
          "cost_per_1k_tokens": 0.01
        },
        "claude-3-opus": {
          "version": "20240229",
          "endpoint": "https://api.anthropic.com/v1",
          "max_tokens": 200000,
          "cost_per_1k_tokens": 0.015
        },
        "llama-3-70b": {
          "version": "2024-04-01",
          "endpoint": "http://llama-inference:8080",
          "max_tokens": 8192,
          "cost_per_1k_tokens": 0.0
        }
      }
    }
```

### GPU Resource Management

```yaml
# gpu-resources.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: llm-inference
spec:
  hard:
    requests.nvidia.com/gpu: "8"
    limits.nvidia.com/gpu: "8"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: llm-inference-high
value: 1000000
globalDefault: false
description: "High priority for LLM inference workloads"
---
apiVersion: v1
kind: Pod
metadata:
  name: llm-inference-worker
spec:
  priorityClassName: llm-inference-high
  containers:
    - name: inference
      image: llm-inference:latest
      resources:
        requests:
          memory: "16Gi"
          cpu: "4"
          nvidia.com/gpu: "1"
        limits:
          memory: "32Gi"
          cpu: "8"
          nvidia.com/gpu: "1"
      env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        - name: MODEL_CACHE_DIR
          value: "/models"
      volumeMounts:
        - name: model-storage
          mountPath: /models
  volumes:
    - name: model-storage
      persistentVolumeClaim:
        claimName: model-pvc
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
```

---

## Summary

Deployment fundamentals for LLM and agentic systems require careful consideration of:

1. **Strategy Selection**: Choose the right deployment strategy based on risk tolerance, infrastructure cost, and rollback requirements
2. **CI/CD Automation**: Automate the entire pipeline from code commit to production deployment
3. **Environment Management**: Maintain consistent, production-like environments for testing
4. **Configuration Management**: Use validated, version-controlled configuration with proper secret management
5. **Feature Flags**: Decouple deployment from release for safer rollouts
6. **Rollback Procedures**: Always have a clear, tested rollback path
7. **LLM-Specific Concerns**: Account for GPU resources, model versioning, and inference performance

By following these fundamentals, teams can deploy AI/LLM systems with confidence, minimize risk, and maintain high availability.
