# Deployment Best Practices for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Infrastructure as Code](#infrastructure-as-code)
   - [Terraform](#terraform)
   - [Pulumi](#pulumi)
   - [CloudFormation](#cloudformation)
3. [Containerization](#containerization)
   - [Docker Best Practices](#docker-best-practices)
   - [Multi-Stage Builds](#multi-stage-builds)
   - [Image Optimization](#image-optimization)
4. [Immutable Deployments](#immutable-deployments)
   - [Principles](#principles)
   - [Implementation](#implementation)
5. [Progressive Delivery](#progressive-delivery)
   - [渐进式交付策略](#渐进式交付策略)
   - [Automation](#automation)
6. [Deployment Gates](#deployment-gates)
   - [Gate Types](#gate-types)
   - [Gate Configuration](#gate-configuration)
7. [Smoke Testing](#smoke-testing)
   - [Pre-Deploy Smoke Tests](#pre-deploy-smoke-tests)
   - [Post-Deploy Smoke Tests](#post-deploy-smoke-tests)
8. [Health Checks](#health-checks)
   - [Liveness Probes](#liveness-probes)
   - [Readiness Probes](#readiness-probes)
   - [Startup Probes](#startup-probes)
9. [Summary](#summary)

---

## Overview

Best practices in deployment ensure reliability, scalability, and maintainability of AI/LLM systems. This document covers proven patterns and techniques that teams should adopt to deploy their systems confidently and efficiently.

### Core Principles

- **Automate Everything**: Manual processes are error-prone; automate repetitive tasks
- **Fail Fast**: Detect issues early in the pipeline before they reach production
- **Observe Everything**: Monitor, log, and trace all deployments
- **Version Everything**: Infrastructure, configuration, models, and code should all be versioned
- **Test in Production**: Use feature flags and canary deployments to test safely

---

## Infrastructure as Code

### Terraform

```hcl
# main.tf - LLM API Infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0"

  name = "llm-api-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = var.environment != "production"
  enable_dns_hostnames = true

  tags = {
    Environment = var.environment
    Project     = "llm-api"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0"

  cluster_name    = "llm-api-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 10

      instance_types = ["m5.xlarge"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }
    }

    gpu = {
      desired_size = var.environment == "production" ? 2 : 1
      min_size     = 1
      max_size     = 5

      instance_types = ["p3.2xlarge"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "gpu"
      }

      taints = [{
        key    = "nvidia.com/gpu"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  tags = {
    Environment = var.environment
    Project     = "llm-api"
  }
}

# RDS PostgreSQL
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.0"

  identifier = "llm-api-${var.environment}"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.environment == "production" ? "db.r6g.xlarge" : "db.t4g.medium"

  allocated_storage     = var.environment == "production" ? 100 : 20
  max_allocated_storage = var.environment == "production" ? 500 : 50

  db_name  = "llm_api"
  username = "admin"
  port     = 5432

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids             = module.vpc.private_subnets

  maintenance_window      = "Mon:00:00-Mon:03:00"
  backup_window           = "03:00-06:00"
  backup_retention_period = var.environment == "production" ? 30 : 7

  tags = {
    Environment = var.environment
    Project     = "llm-api"
  }
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id = "llm-api-${var.environment}"
  description          = "Redis cluster for LLM API"

  node_type            = var.environment == "production" ? "cache.r6g.large" : "cache.t4g.medium"
  num_cache_clusters   = var.environment == "production" ? 3 : 1

  port = 6379

  subnet_group_name  = aws_elasticache_subnet_group.redis.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  tags = {
    Environment = var.environment
    Project     = "llm-api"
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

# Outputs
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "database_endpoint" {
  value = module.db.db_instance_endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
}
```

### Variables File

```hcl
# terraform.tfvars
environment = "production"
aws_region  = "us-east-1"
```

---

## Containerization

### Docker Best Practices

```dockerfile
# Dockerfile - Multi-stage build for LLM API

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Create non-root user
RUN groupadd -r llmapi && useradd -r -g llmapi -d /app -s /sbin/nologin llmapi

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/llmapi/.local

# Copy application code
COPY --chown=llmapi:llmapi . .

# Set environment variables
ENV PATH=/home/llmapi/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health/live || exit 1

# Switch to non-root user
USER llmapi

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

### Image Optimization

```yaml
# .dockerignore
.git
.github
.gitignore
.env
.env.*
*.md
tests/
docs/
__pycache__
*.pyc
.mypy_cache
.pytest_cache
.ruff_cache
node_modules/
.DS_Store
Thumbs.db
```

```yaml
# docker-compose.yaml for local development
version: '3.8'

services:
  llm-api:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/llm_api
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=DEBUG
      - MODEL_CACHE_DIR=/models
    volumes:
      - model-cache:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: llm_api
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  model-cache:
  postgres-data:
  redis-data:
```

---

## Immutable Deployments

### Principles

```
1. Never modify running instances
2. Deploy new versions, don't patch
3. Roll back by deploying previous version
4. All changes go through CI/CD
5. Configuration is baked into images
```

### Implementation

```yaml
# immutable-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  labels:
    app: llm-api
    version: v1.3.0
    commit: abc1234
    build: "456"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: llm-api
        version: v1.3.0
        commit: abc1234
        build: "456"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: llm-api
          image: llm-api:1.3.0-abc1234
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: llm-api-config
            - secretRef:
                name: llm-api-secrets
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"
            limits:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
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
          startupProbe:
            httpGet:
              path: /health/startup
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
      imagePullSecrets:
        - name: registry-credentials
```

---

## Progressive Delivery

### 渐进式交付策略

Progressive delivery combines continuous delivery with progressive delivery techniques to reduce risk.

```
┌─────────────────────────────────────────────────────────┐
│                  Progressive Delivery Flow              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────┐│
│  │ Deploy  │───▶│ Canary  │───▶│ Analyze │───▶│Promote││
│  │  5%     │    │Monitor  │    │Metrics  │    │ 100% ││
│  └─────────┘    └─────────┘    └─────────┘    └──────┘│
│       │              │              │              │     │
│       │              │              │              │     │
│       ▼              ▼              ▼              ▼     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────┐│
│  │ Rollback│    │ Alert   │    │Decision │    │Complete│
│  │   0%    │    │  Fire   │    │  Gate   │    │       ││
│  └─────────┘    └─────────┘    └─────────┘    └──────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Automation

```yaml
# progressive-delivery-config.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: llm-api
  namespace: production
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
    trafficPolicy:
      tls:
        mode: DISABLE
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
    webhooks:
      loadtest:
        name: load-test
        url: http://flagger-loadtester.flagger-system/
        timeout: 15s
        metadata:
          type: bash
          cmd: "curl -sd 'test' http://llm-api-canary.test.svc.cluster.local:8080/api/v1/completions"
```

---

## Deployment Gates

### Gate Types

```
┌─────────────────────────────────────────────────────────┐
│                    Deployment Gates                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Gate 1: Build Verification                       │  │
│  │ ✓ Code compiles                                  │  │
│  │ ✓ Unit tests pass                                │  │
│  │ ✓ Code coverage > 80%                            │  │
│  │ ✓ No critical security vulnerabilities           │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Gate 2: Integration Verification                 │  │
│  │ ✓ Integration tests pass                         │  │
│  │ ✓ API contract tests pass                        │  │
│  │ ✓ Performance benchmarks meet thresholds         │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Gate 3: Staging Verification                     │  │
│  │ ✓ Deployed to staging successfully               │  │
│  │ ✓ Smoke tests pass                               │  │
│  │ ✓ No errors in staging logs                      │  │
│  │ ✓ Resource utilization acceptable                │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Gate 4: Production Approval                      │  │
│  │ ✓ Manual approval from team lead                 │  │
│  │ ✓ Change window check                            │  │
│  │ ✓ No conflicting deployments                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Gate Configuration

```yaml
# deployment-gates.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: deployment-gates
data:
  gates.json: |
    {
      "gates": [
        {
          "name": "build-verification",
          "stage": "build",
          "checks": [
            {
              "name": "unit-tests",
              "command": "pytest tests/unit/ -v --tb=short",
              "required": true,
              "timeout": "10m"
            },
            {
              "name": "code-coverage",
              "command": "pytest tests/unit/ --cov=src --cov-fail-under=80",
              "required": true,
              "timeout": "10m"
            },
            {
              "name": "security-scan",
              "command": "trivy image --severity HIGH,CRITICAL llm-api:latest",
              "required": true,
              "timeout": "5m"
            }
          ]
        },
        {
          "name": "integration-verification",
          "stage": "integration",
          "checks": [
            {
              "name": "integration-tests",
              "command": "pytest tests/integration/ -v",
              "required": true,
              "timeout": "20m"
            },
            {
              "name": "api-contract-tests",
              "command": "schemathesis run https://staging.llm-api.example.com/openapi.json",
              "required": true,
              "timeout": "15m"
            }
          ]
        },
        {
          "name": "staging-verification",
          "stage": "staging",
          "checks": [
            {
              "name": "smoke-tests",
              "command": "pytest tests/smoke/ -v --api-url=https://staging.llm-api.example.com",
              "required": true,
              "timeout": "10m"
            },
            {
              "name": "health-check",
              "command": "curl -f https://staging.llm-api.example.com/health/ready",
              "required": true,
              "timeout": "1m"
            },
            {
              "name": "log-errors",
              "command": "kubectl logs -l app=llm-api -n staging --tail=1000 | grep -i error | wc -l | xargs test 0 -eq",
              "required": true,
              "timeout": "2m"
            }
          ]
        }
      ]
    }
```

---

## Smoke Testing

### Pre-Deploy Smoke Tests

```yaml
# smoke-tests-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: smoke-tests
data:
  pre-deploy.yaml: |
    tests:
      - name: health-endpoint
        method: GET
        url: /health/live
        expected_status: 200
        expected_body:
          status: "ok"

      - name: readiness-endpoint
        method: GET
        url: /health/ready
        expected_status: 200
        expected_body:
          status: "ready"

      - name: api-version
        method: GET
        url: /api/version
        expected_status: 200
        expected_body:
          version: "1.3.0"

      - name: completions-endpoint
        method: POST
        url: /api/v1/completions
        body:
          prompt: "Hello, world!"
          max_tokens: 10
        expected_status: 200
        expected_body:
          choices:
            - text:
                $exists: true

      - name: embeddings-endpoint
        method: POST
        url: /api/v1/embeddings
        body:
          input: "Test embedding"
          model: "text-embedding-ada-002"
        expected_status: 200
        expected_body:
          data:
            - embedding:
                $type: array
                $minLength: 1500
```

### Post-Deploy Smoke Tests

```yaml
# post-deploy-smoke-tests.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: post-deploy-smoke-tests
spec:
  template:
    spec:
      containers:
        - name: smoke-tests
          image: llm-api-smoke-tests:latest
          env:
            - name: API_URL
              value: "https://llm-api.example.com"
            - name: TEST_API_KEY
              valueFrom:
                secretKeyRef:
                  name: test-api-keys
                  key: smoke-test-key
          command: ["python", "-m", "pytest", "tests/smoke/post-deploy/", "-v"]
      restartPolicy: Never
  backoffLimit: 1
```

---

## Health Checks

### Liveness Probes

```yaml
# health-checks.yaml
apiVersion: v1
kind: Pod
metadata:
  name: llm-api
spec:
  containers:
    - name: llm-api
      image: llm-api:1.3.0
      livenessProbe:
        httpGet:
          path: /health/live
          port: 8080
        initialDelaySeconds: 60
        periodSeconds: 15
        timeoutSeconds: 5
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3
      startupProbe:
        httpGet:
          path: /health/startup
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 5
        timeoutSeconds: 5
        failureThreshold: 30
        successThreshold: 1
```

### Health Check Implementation

```python
# src/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import redis
import time

router = APIRouter()

class HealthStatus:
    def __init__(self):
        self.checks = {}
        self.start_time = time.time()

health = HealthStatus()

@router.get("/health/live")
async def liveness():
    """Liveness probe - is the service alive?"""
    return {"status": "ok", "timestamp": time.time()}

@router.get("/health/ready")
async def readiness(db: Session = Depends(get_db)):
    """Readiness probe - is the service ready to accept traffic?"""
    checks = {}
    
    # Check database connectivity
    try:
        db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
    
    # Check Redis connectivity
    try:
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
    
    # Check model availability
    try:
        model_loaded = check_model_loaded()
        checks["model"] = "ok" if model_loaded else "loading"
    except Exception as e:
        checks["model"] = f"error: {str(e)}"
    
    # Determine overall status
    all_ok = all(v == "ok" for v in checks.values())
    status = "ready" if all_ok else "not_ready"
    
    return {
        "status": status,
        "checks": checks,
        "uptime": time.time() - health.start_time
    }

@router.get("/health/startup")
async def startup():
    """Startup probe - has the service started successfully?"""
    return {
        "status": "started",
        "timestamp": time.time(),
        "version": "1.3.0"
    }

@router.get("/health/deep")
async def deep_health(db: Session = Depends(get_db)):
    """Deep health check - comprehensive status"""
    checks = {}
    
    # Database check
    try:
        start = time.time()
        db.execute("SELECT 1")
        checks["database"] = {
            "status": "ok",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["database"] = {"status": "error", "message": str(e)}
    
    # Redis check
    try:
        start = time.time()
        redis_client.ping()
        checks["redis"] = {
            "status": "ok",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["redis"] = {"status": "error", "message": str(e)}
    
    # Model check
    try:
        start = time.time()
        model_loaded = check_model_loaded()
        checks["model"] = {
            "status": "ok" if model_loaded else "loading",
            "latency_ms": (time.time() - start) * 1000
        }
    except Exception as e:
        checks["model"] = {"status": "error", "message": str(e)}
    
    # GPU check
    try:
        gpu_info = get_gpu_info()
        checks["gpu"] = {
            "status": "ok",
            "memory_used_mb": gpu_info.memory_used,
            "memory_total_mb": gpu_info.memory_total
        }
    except Exception as e:
        checks["gpu"] = {"status": "error", "message": str(e)}
    
    # Overall status
    all_ok = all(
        v.get("status") == "ok" 
        for v in checks.values() 
        if isinstance(v, dict)
    )
    
    return {
        "status": "healthy" if all_ok else "degraded",
        "checks": checks,
        "uptime": time.time() - health.start_time,
        "version": "1.3.0"
    }
```

---

## Summary

Best practices for deploying LLM and agentic systems include:

1. **Infrastructure as Code**: Use Terraform, Pulumi, or CloudFormation for reproducible infrastructure
2. **Containerization**: Build optimized, multi-stage Docker images with proper security
3. **Immutable Deployments**: Never modify running instances; deploy new versions instead
4. **Progressive Delivery**: Use canary deployments and feature flags for safe rollouts
5. **Deployment Gates**: Implement automated checks at each stage of the pipeline
6. **Smoke Testing**: Run pre-deploy and post-deploy smoke tests to catch issues early
7. **Health Checks**: Implement comprehensive liveness, readiness, and startup probes

By following these best practices, teams can achieve reliable, scalable, and maintainable deployments for their AI/LLM systems.
