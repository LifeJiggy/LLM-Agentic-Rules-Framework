# Deployment Examples for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Docker Deployment](#docker-deployment)
   - [Dockerfile Examples](#dockerfile-examples)
   - [Docker Compose](#docker-compose)
   - [Docker Swarm](#docker-swarm)
3. [Kubernetes Deployment](#kubernetes-deployment)
   - [Basic Deployment](#basic-deployment)
   - [Advanced Deployment](#advanced-deployment)
   - [Helm Charts](#helm-charts)
4. [Serverless Deployment](#serverless-deployment)
   - [AWS Lambda](#aws-lambda)
   - [Google Cloud Functions](#google-cloud-functions)
   - [Azure Functions](#azure-functions)
5. [Model Deployment](#model-deployment)
   - [Model Serving with TFServing](#model-serving-with-tfserving)
   - [Model Serving with Triton](#model-serving-with-triton)
   - [Model Serving with BentoML](#model-serving-with-bentoml)
6. [CI/CD Pipeline Examples](#cicd-pipeline-examples)
7. [Summary](#summary)

---

## Overview

This document provides practical examples of deploying AI/LLM systems using various technologies and platforms. Each example includes complete configurations and explanations.

---

## Docker Deployment

### Dockerfile Examples

#### Python LLM API

```dockerfile
# Dockerfile.python-api
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

#### Node.js LLM API

```dockerfile
# Dockerfile.node-api
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Stage 2: Runtime
FROM node:20-alpine as runtime

# Create non-root user
RUN addgroup -g 1001 -S llmapi && \
    adduser -S llmapi -u 1001

WORKDIR /app

# Copy application code and dependencies
COPY --from=builder --chown=llmapi:llmapi /app .

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/health/live || exit 1

# Switch to non-root user
USER llmapi

# Expose port
EXPOSE 3000

# Run the application
CMD ["node", "src/server.js"]
```

#### Go LLM API

```dockerfile
# Dockerfile.go-api
FROM golang:1.21-alpine as builder

WORKDIR /app

# Copy go mod file
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/server

# Stage 2: Runtime
FROM alpine:latest as runtime

# Install ca-certificates and curl
RUN apk --no-cache add ca-certificates curl

# Create non-root user
RUN addgroup -g 1001 -S llmapi && \
    adduser -S llmapi -u 1001

WORKDIR /root/

# Copy the binary from builder
COPY --from=builder /app/main .

# Copy configuration
COPY --from=builder /app/config.yaml .

# Set environment variables
ENV GIN_MODE=release

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health/live || exit 1

# Switch to non-root user
USER llmapi

# Expose port
EXPOSE 8080

# Run the application
CMD ["./main"]
```

### Docker Compose

```yaml
# docker-compose.yaml
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
    networks:
      - llm-network

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
    networks:
      - llm-network

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
    networks:
      - llm-network

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - llm-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - llm-network

networks:
  llm-network:
    driver: bridge

volumes:
  model-cache:
  postgres-data:
  redis-data:
  grafana-data:
```

### Docker Swarm

```yaml
# docker-stack.yaml
version: '3.8'

services:
  llm-api:
    image: llm-api:1.3.0
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/llm_api
      - REDIS_URL=redis://redis:6379
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 5s
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - llm-network

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: llm_api
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data
    deploy:
      replicas: 1
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    networks:
      - llm-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    deploy:
      replicas: 1
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    networks:
      - llm-network

networks:
  llm-network:
    driver: overlay

volumes:
  postgres-data:
  redis-data:
```

---

## Kubernetes Deployment

### Basic Deployment

```yaml
# k8s/basic-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  labels:
    app: llm-api
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
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: llm-api-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: llm-api-secrets
                  key: redis-url
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
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: llm-api
spec:
  selector:
    app: llm-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### Advanced Deployment

```yaml
# k8s/advanced-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  labels:
    app: llm-api
    version: v1.3.0
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
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: llm-api
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: llm-api
          image: llm-api:1.3.0
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
              protocol: TCP
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
            timeoutSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 15
            timeoutSeconds: 5
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /health/startup
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
          volumeMounts:
            - name: model-storage
              mountPath: /models
            - name: config-volume
              mountPath: /config
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
        - name: config-volume
          configMap:
            name: llm-api-configmap
      imagePullSecrets:
        - name: registry-credentials
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - gpu
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
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 1000
```

### Helm Charts

```yaml
# helm/llm-api/values.yaml
replicaCount: 3

image:
  repository: llm-api
  pullPolicy: IfNotPresent
  tag: "1.3.0"

service:
  type: LoadBalancer
  port: 80
  targetPort: 8080

resources:
  requests:
    memory: "4Gi"
    cpu: "2"
    nvidia.com/gpu: "1"
  limits:
    memory: "8Gi"
    cpu: "4"
    nvidia.com/gpu: "1"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
  hosts:
    - host: llm-api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: llm-api-tls
      hosts:
        - llm-api.example.com

config:
  LOG_LEVEL: "INFO"
  MODEL_CACHE_SIZE: "2000"
  MAX_CONCURRENT_REQUESTS: "200"
  ENABLE_TRACING: "true"
  ENABLE_METRICS: "true"

secrets:
  DATABASE_URL: "postgresql://admin:secret@postgres:5432/llm_api"
  REDIS_URL: "redis://redis:6379"
  API_KEY: "sk-1234567890abcdef"
```

```yaml
# helm/llm-api/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "llm-api.fullname" . }}
  labels:
    {{- include "llm-api.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "llm-api.selectorLabels" . | nindent 6 }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        {{- include "llm-api.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "llm-api.fullname" . }}-config
            - secretRef:
                name: {{ include "llm-api.fullname" . }}-secrets
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 60
            periodSeconds: 15
          startupProbe:
            httpGet:
              path: /health/startup
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
```

---

## Serverless Deployment

### AWS Lambda

```yaml
# serverless.yaml (Serverless Framework)
service: llm-api

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  memorySize: 3008
  timeout: 30
  environment:
    DATABASE_URL: ${ssm:/llm-api/database-url}
    REDIS_URL: ${ssm:/llm-api/redis-url}
    MODEL_CACHE_DIR: /tmp/models
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - s3:GetObject
            - s3:PutObject
          Resource: "arn:aws:s3:::llm-models/*"
        - Effect: Allow
          Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
          Resource: "arn:aws:logs:*:*:*"

functions:
  completions:
    handler: src.handlers.completions.handler
    events:
      - http:
          path: /api/v1/completions
          method: post
          cors: true
    layers:
      - arn:aws:lambda:us-east-1:xxx:layer:python-requests:31
    vpc:
      securityGroupIds:
        - sg-xxx
      subnetIds:
        - subnet-xxx
        - subnet-yyy

  embeddings:
    handler: src.handlers.embeddings.handler
    events:
      - http:
          path: /api/v1/embeddings
          method: post
          cors: true
    layers:
      - arn:aws:lambda:us-east-1:xxx:layer:python-requests:31
    vpc:
      securityGroupIds:
        - sg-xxx
      subnetIds:
        - subnet-xxx
        - subnet-yyy

  health:
    handler: src.handlers.health.handler
    events:
      - http:
          path: /health
          method: get
          cors: true

plugins:
  - serverless-python-requirements
  - serverless-layers
  - serverless-domain-manager

custom:
  pythonRequirements:
    dockerizePip: true
    slim: true
    strip: false
    noDeploy:
      - pytest
      - mypy
      - ruff
  domainManager:
    domainName: llm-api.example.com
    certificateArn: arn:aws:acm:us-east-1:xxx:certificate/xxx
    endpointType: regional
    securityPolicy: TLS_1_2
```

### Google Cloud Functions

```yaml
# deployment.yaml (gcloud deploy)
apiVersion: deploy.googleapis.com/v1
kind: DeliveryPipeline
metadata:
  name: llm-api-pipeline
description: LLM API delivery pipeline
serialPipeline:
  stages:
    - targetId: staging
      profiles: []
    - targetId: production
      profiles: []

---
apiVersion: deploy.googleapis.com/v1
kind: Target
metadata:
  name: staging
description: Staging environment
gke:
  cluster: projects/my-project/locations/us-central1/clusters/staging
  project: my-project

---
apiVersion: deploy.googleapis.com/v1
kind: Target
metadata:
  name: production
description: Production environment
gke:
  cluster: projects/my-project/locations/us-central1/clusters/production
  project: my-project
requireApproval: true
```

```yaml
# cloudfunction-deployment.yaml
import functions_framework
from flask import jsonify
import os

@functions_framework.http
def completions(request):
    """HTTP Cloud Function for LLM completions."""
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    
    try:
        request_json = request.get_json()
        
        if not request_json or 'prompt' not in request_json:
            return jsonify({'error': 'Missing prompt parameter'}), 400
        
        prompt = request_json['prompt']
        max_tokens = request_json.get('max_tokens', 100)
        
        # Process completion
        result = process_completion(prompt, max_tokens)
        
        return jsonify(result), 200, headers
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500, headers
```

### Azure Functions

```yaml
# host.json
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "functionTimeout": "00:10:00",
  "extensions": {
    "http": {
      "routePrefix": "api",
      "maxOutstandingRequests": 200,
      "maxConcurrentRequests": 100
    }
  },
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  }
}

# local.settings.json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DATABASE_URL": "postgresql://admin:secret@postgres:5432/llm_api",
    "REDIS_URL": "redis://redis:6379"
  }
}

# function.json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["post"],
      "route": "v1/completions"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
```

---

## Model Deployment

### Model Serving with TFServing

```yaml
# tfserving-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving
  labels:
    app: tf-serving
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tf-serving
  template:
    metadata:
      labels:
        app: tf-serving
    spec:
      containers:
        - name: tf-serving
          image: tensorflow/serving:2.14.0
          args:
            - "--model_name=llm_model"
            - "--model_base_path=/models/llm_model"
            - "--rest_api_port=8501"
            - "--grpc_port=8500"
            - "--enable_batching=true"
            - "--batching_parameters_file=/config/batching.config"
          ports:
            - containerPort: 8501
              name: http
            - containerPort: 8500
              name: grpc
          volumeMounts:
            - name: model-storage
              mountPath: /models
            - name: config
              mountPath: /config
          resources:
            requests:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
            limits:
              memory: "16Gi"
              cpu: "8"
              nvidia.com/gpu: "1"
          readinessProbe:
            httpGet:
              path: /v1/models/llm_model
              port: 8501
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /v1/models/llm_model
              port: 8501
            initialDelaySeconds: 60
            periodSeconds: 15
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
        - name: config
          configMap:
            name: tfserving-config
---
apiVersion: v1
kind: Service
metadata:
  name: tf-serving
spec:
  selector:
    app: tf-serving
  ports:
    - name: http
      port: 8501
      targetPort: 8501
    - name: grpc
      port: 8500
      targetPort: 8500
  type: ClusterIP
```

### Model Serving with Triton

```yaml
# triton-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-server
  labels:
    app: triton-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: triton-server
  template:
    metadata:
      labels:
        app: triton-server
    spec:
      containers:
        - name: triton-server
          image: nvcr.io/nvidia/tritonserver:23.10-py3
          args:
            - "--model-repository=/models"
            - "--http-port=8000"
            - "--grpc-port=8001"
            - "--metrics-port=8002"
            - "--strict-model-config=false"
            - "--strict-readiness=false"
          ports:
            - containerPort: 8000
              name: http
            - containerPort: 8001
              name: grpc
            - containerPort: 8002
              name: metrics
          volumeMounts:
            - name: model-storage
              mountPath: /models
          resources:
            requests:
              memory: "16Gi"
              cpu: "8"
              nvidia.com/gpu: "1"
            limits:
              memory: "32Gi"
              cpu: "16"
              nvidia.com/gpu: "2"
          readinessProbe:
            httpGet:
              path: /v2/health/ready
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /v2/health/live
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 15
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
```

### Model Serving with BentoML

```yaml
# bentoml-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-service
  labels:
    app: bentoml-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bentoml-service
  template:
    metadata:
      labels:
        app: bentoml-service
    spec:
      containers:
        - name: bentoml-service
          image: llm-bentoml:1.3.0
          ports:
            - containerPort: 3000
              name: http
            - containerPort: 3001
              name: grpc
          env:
            - name: BENTOML_CONFIG
              value: /config/bentoml.yaml
          volumeMounts:
            - name: config
              mountPath: /config
            - name: model-storage
              mountPath: /bentoml/models
          resources:
            requests:
              memory: "8Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
            limits:
              memory: "16Gi"
              cpu: "8"
              nvidia.com/gpu: "1"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 60
            periodSeconds: 15
      volumes:
        - name: config
          configMap:
            name: bentoml-config
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
```

---

## CI/CD Pipeline Examples

```yaml
# .github/workflows/deploy.yaml
name: Deploy LLM API

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/llm-api

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

      - name: Run tests
        run: pytest tests/ -v

      - name: Build Docker image
        run: |
          docker build \
            --tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} .

      - name: Push to registry
        if: github.event_name != 'pull_request'
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ${{ env.REGISTRY }} -u ${{ github.actor }} --password-stdin
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          kubectl set image deployment/llm-api-staging \
            llm-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging
          kubectl rollout status deployment/llm-api-staging \
            --namespace=staging \
            --timeout=300s

      - name: Run smoke tests
        run: |
          pytest tests/smoke/ -v --api-url=https://staging.llm-api.example.com

      - name: Deploy to production
        run: |
          kubectl set image deployment/llm-api \
            llm-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production
          kubectl rollout status deployment/llm-api \
            --namespace=production \
            --timeout=300s

      - name: Verify deployment
        run: |
          curl -f https://llm-api.example.com/health/ready
```

---

## Summary

This document provides comprehensive examples of deploying AI/LLM systems using various technologies:

1. **Docker**: Dockerfiles, Docker Compose, and Docker Swarm configurations
2. **Kubernetes**: Basic and advanced deployments, Helm charts, and service meshes
3. **Serverless**: AWS Lambda, Google Cloud Functions, and Azure Functions
4. **Model Serving**: TFServing, Triton, and BentoML configurations
5. **CI/CD**: Complete pipeline examples with GitHub Actions

Each example includes production-ready configurations that can be adapted to specific use cases.
