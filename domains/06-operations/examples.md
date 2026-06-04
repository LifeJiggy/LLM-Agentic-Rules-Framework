# Operations Domain - Examples

## Overview

This document provides concrete code examples for implementing operations patterns in LLM/agentic systems.

---

## Example 1: Health Check Endpoint

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health_check():
    checks = {
        "database": check_database(),
        "redis": check_redis(),
        "model_api": check_model_api()
    }
    
    healthy = all(checks.values())
    status = 200 if healthy else 503
    
    return jsonify({
        "status": "healthy" if healthy else "unhealthy",
        "checks": checks
    }), status

def check_database():
    try:
        db.ping()
        return True
    except:
        return False

def check_redis():
    try:
        redis.ping()
        return True
    except:
        return False

def check_model_api():
    try:
        client.models.list()
        return True
    except:
        return False
```

---

## Example 2: Deployment Configuration

```yaml
# kubernetes/deployment.yaml
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
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              name: agent-config
              key: model
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Example 3: Logging Configuration

```python
import structlog
import logging

def configure_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

def log_agent_operation(operation, session_id, duration_ms, success=True):
    logger.info(
        "agent.operation",
        operation=operation,
        session_id=session_id,
        duration_ms=duration_ms,
        success=success
    )
```

---

## Example 4: Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

# Create metrics
agent_requests = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["method", "endpoint", "status"]
)
agent_duration = Histogram(
    "agent_request_duration_seconds",
    "Request duration",
    ["endpoint"]
)
active_sessions = Gauge(
    "agent_active_sessions",
    "Currently active sessions"
)

# Instrument endpoint
@app.route("/api/agent/<session_id>/process")
def process(session_id):
    start = time.time()
    
    try:
        result = agent.process(session_id)
        agent_requests.labels(
            method="POST",
            endpoint="/process",
            status="200"
        ).inc()
        return jsonify(result)
    except Exception as e:
        agent_requests.labels(
            method="POST",
            endpoint="/process",
            status="500"
        ).inc()
        raise
    finally:
        agent_duration.labels(endpoint="/process").observe(time.time() - start)
```

---

## Example 5: Autoscaling Configuration

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
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

---

## Example 6: Backup Script

```python
import asyncio
import boto3
from datetime import datetime

async def backup_database():
    """Daily database backup to S3."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"backups/agent_db_{timestamp}.sql.gz"
    
    # Dump database
    proc = await asyncio.create_subprocess_exec(
        "pg_dump",
        "-h", os.getenv("DB_HOST"),
        "-U", os.getenv("DB_USER"),
        "-d", os.getenv("DB_NAME"),
        stdout=asyncio.subprocess.PIPE
    )
    
    stdout, _ = await proc.communicate()
    
    # Compress and upload
    compressed = gzip.compress(stdout)
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="agent-backups",
        Key=filename,
        Body=compressed,
        ServerSideEncryption="AES256"
    )
    
    # Cleanup old backups (keep last 30 days)
    await cleanup_old_backups("agent-backups", "backups/", days=30)
    
    return {"backup": filename, "size": len(compressed)}

async def cleanup_old_backups(bucket: str, prefix: str, days: int):
    s3 = boto3.client("s3")
    cutoff = datetime.utcnow() - timedelta(days=days)
    paginator = s3.get_paginator("list_objects_v2")
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["LastModified"].replace(tzinfo=None) < cutoff:
                s3.delete_object(Bucket=bucket, Key=obj["Key"])
```

---

## Example 7: Rolling Update Script

```python
class RollingUpdater:
    def __init__(self, k8s_client, image: str):
        self.k8s = k8s_client
        self.image = image
        self.deployment = "agent-service"
    
    async def update(self, max_unavailable: str = "25%", 
                    max_surge: str = "25%"):
        patch = {
            "spec": {
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {
                        "maxUnavailable": max_unavailable,
                        "maxSurge": max_surge
                    }
                },
                "template": {
                    "spec": {
                        "containers": [{
                            "name": "agent",
                            "image": self.image
                        }]
                    }
                }
            }
        }
        
        await self.k8s.patch_deployment(self.deployment, patch)
        await self._wait_for_ready()
    
    async def _wait_for_ready(self, timeout: int = 600):
        start = time.time()
        while time.time() - start < timeout:
            status = await self.k8s.get_deployment_status(self.deployment)
            if (status["replicas"] == status["updated_replicas"] 
                == status["available_replicas"]):
                logger.info(f"Rolling update completed for {self.deployment}")
                return True
            await asyncio.sleep(10)
        raise TimeoutError(f"Deployment {self.deployment} did not complete in time")

# Usage
updater = RollingUpdater(k8s_client, "agent:v2.0.0")
await updater.update()
```

---

## Example 8: Canary Deployment

```python
class CanaryDeployer:
    def __init__(self, k8s_client, traffic_client):
        self.k8s = k8s_client
        self.traffic = traffic_client
        self.deployment = "agent-service"
        self.canary_deployment = "agent-service-canary"
        self.steps = [5, 20, 50, 100]
    
    async def deploy(self, image: str):
        # Deploy canary with 0 replicas
        await self.k8s.create_deployment(self.canary_deployment, image, replicas=1)
        await self.k8s.create_service(self.canary_deployment)
        
        # Progressive traffic shift
        for weight in self.steps:
            await self.traffic.set_weight("agent-service", {
                "v1": 100 - weight,
                "canary": weight
            })
            
            # Monitor and wait
            await asyncio.sleep(60)
            healthy = await self._check_health()
            if not healthy:
                await self._rollback()
                raise CanaryFailed("Health check failed during canary")
        
        # Full promotion
        await self.k8s.patch_deployment(self.deployment, {
            "spec": {"template": {"spec": {
                "containers": [{"name": "agent", "image": image}]
            }}}
        })
        await self.k8s.scale_deployment(self.canary_deployment, 0)
    
    async def _check_health(self) -> bool:
        errors = await self._get_error_rate()
        latency = await self._get_p99_latency()
        return errors < 0.01 and latency < 5.0
    
    async def _rollback(self):
        await self.traffic.set_weight("agent-service", {"v1": 100, "canary": 0})
        await self.k8s.scale_deployment(self.canary_deployment, 0)
```

---

## Example 9: Alert Rule Definitions

```yaml
# Prometheus alert rules
groups:
- name: agent_alerts
  rules:
  - alert: HighErrorRate
    expr: |
      rate(agent_requests_total{status=~"5.."}[5m]) 
      / rate(agent_requests_total[5m]) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value | humanizePercentage }}"
  
  - alert: HighLatency
    expr: |
      histogram_quantile(0.99, 
        rate(agent_request_duration_seconds_bucket[5m])
      ) > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High latency detected"
  
  - alert: ModelAPIErrors
    expr: |
      rate(model_api_errors_total[5m]) > 0.1
    for: 3m
    labels:
      severity: critical
    annotations:
      summary: "Model API returning errors"
  
  - alert: QueueDepthHigh
    expr: agent_queue_depth > 1000
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Message queue backing up"
```

---

## Example 10: Runbook Automation

```python
class RunbookExecutor:
    def __init__(self, command_runner, metrics_client):
        self.runner = command_runner
        self.metrics = metrics_client
        self.runbooks = {}
    
    def register(self, name: str, steps: list):
        self.runbooks[name] = steps
    
    async def execute(self, name: str, context: dict):
        steps = self.runbooks.get(name)
        if not steps:
            raise ValueError(f"Unknown runbook: {name}")
        
        results = []
        for step in steps:
            if "condition" in step:
                if not self._evaluate(step["condition"], context):
                    continue
            result = await self.runner.run(step["command"])
            results.append({"step": step["name"], "result": result})
            if not result.get("ok") and step.get("critical", True):
                return {"status": "failed", "failed_at": step["name"], "results": results}
        
        return {"status": "completed", "results": results}

# Example runbooks
REGISTERED_RUNBOOKS = {
    "high_error_rate": [
        {"name": "check_deployments", "command": "kubectl rollout history deployment/agent", "critical": False},
        {"name": "review_logs", "command": "kubectl logs -l app=agent --tail=100", "critical": False},
        {"name": "check_model_status", "command": "curl https://status.openai.com/api/v2/status.json", "critical": False},
        {"name": "scale_up", "condition": "error_rate > 0.1", "command": "kubectl scale deployment/agent --replicas=10"},
        {"name": "rollback", "condition": "error_rate > 0.3", "command": "kubectl rollout undo deployment/agent", "critical": True}
    ],
    "latency_spike": [
        {"name": "check_prometheus", "command": "curl -s localhost:9090/api/v1/query?query=histogram_quantile(0.99,rate(agent_latency_seconds_bucket[5m]))", "critical": False},
        {"name": "check_db_queries", "command": "kubectl exec -it $(kubectl get pod -l app=agent -o jsonpath='{.items[0].metadata.name}') -- psql -c 'SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5'", "critical": False},
        {"name": "reduce_context", "condition": "prompt_tokens > 8000", "command": "kubectl set env deployment/agent MAX_CONTEXT_TOKENS=4000"}
    ]
}

executor = RunbookExecutor(CommandRunner(), MetricsClient())
executor.register("high_error_rate", REGISTERED_RUNBOOKS["high_error_rate"])
result = await executor.execute("high_error_rate", {"error_rate": 0.25})
```

---

## Example 11: Configuration Management

```python
from pydantic import BaseSettings, validator, Field
import os

class AgentConfig(BaseSettings):
    model_name: str = Field(default="gpt-4", env="MODEL_NAME")
    api_key: str = Field(..., env="API_KEY")
    max_tokens: int = Field(default=4096, ge=1, le=128000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout_seconds: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    environment: str = Field(default="production", env="ENV")
    
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

config = AgentConfig()

def reload_config():
    global config
    config = AgentConfig()
    logger.info("Configuration reloaded")
```

---

## Example 12: Deployment Pipeline

```yaml
# GitHub Actions workflow
name: Agent Deployment Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install ruff mypy
      - run: ruff check src/
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
        options: --health-cmd pg_isready --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest tests/ --cov=src --cov-report=xml -x
      - uses: codecov/codecov-action@v4

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install bandit safety semgrep
      - run: bandit -r src/
      - run: safety check --json
      - run: semgrep --config auto src/

  deploy-staging:
    needs: [lint, test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          tags: agent:${{ github.sha }}
          push: true
      - run: kubectl set image deployment/agent agent=agent:${{ github.sha }} -n staging

  deploy-production:
    needs: [lint, test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          tags: agent:${{ github.sha }}
          push: true
      - run: kubectl set image deployment/agent agent=agent:${{ github.sha }} -n production
```

---

## Example 13: Chaos Engineering Experiment

```python
# Experiment: Verify system recovers from database failure
class DatabaseKillExperiment:
    def __init__(self, chaos_client, app_client):
        self.chaos = chaos_client
        self.client = app_client
        self.target_pod_label = "app=agent"
    
    async def run(self, duration_seconds: int = 60) -> dict:
        pod = await self.chaos.get_pod(self.target_pod_label)
        start_time = time.time()
        
        try:
            await self.chaos.kill_pod(pod["name"])
            logger.info("Database pod killed")
            
            # Assert graceful degradation
            for _ in range(10):
                response = await self.client.post("/api/process", json={"prompt": "test"})
                if response.status == 503:
                    break
                await asyncio.sleep(1)
            
            # Wait for recovery
            await asyncio.sleep(duration_seconds)
            
            # Verify recovery
            response = await self.client.post("/api/process", json={"prompt": "test"})
            recovered = response.status == 200
            
            return {
                "experiment": "db_kill",
                "duration_seconds": time.time() - start_time,
                "recovered": recovered,
                "status": "pass" if recovered else "fail"
            }
        finally:
            await self.chaos.restore_pod(pod["name"])
```

---

## Example 14: Graceful Shutdown Handler

```python
import signal
import asyncio
from contextlib import asynccontextmanager

class GracefulShutdown:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.cleanup_tasks = []
    
    def register_cleanup(self, name: str, cleanup_fn):
        self.cleanup_tasks.append((name, cleanup_fn))
    
    def setup_handlers(self):
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._handle_shutdown)
    
    def _handle_shutdown(self):
        logger.info("Shutdown signal received")
        self.shutdown_event.set()
    
    async def wait_for_shutdown(self):
        await self.shutdown_event.wait()
    
    async def cleanup(self):
        for name, cleanup_fn in self.cleanup_tasks:
            try:
                logger.info(f"Running cleanup: {name}")
                await cleanup_fn()
            except Exception as e:
                logger.error(f"Cleanup failed for {name}", error=str(e))

shutdown = GracefulShutdown()
shutdown.register_cleanup("database", lambda: db.close())
shutdown.register_cleanup("redis", lambda: redis.close())
shutdown.register_cleanup("http_client", lambda: http_client.close())

shutdown.setup_handlers()

async def main():
    await startup()
    await shutdown.wait_for_shutdown()
    await shutdown.cleanup()
    logger.info("Shutdown complete")

asyncio.run(main())
```

---

## Example 15: Rate Limiting Middleware

```python
from flask import Flask, request, jsonify
from functools import wraps
import time
from collections import defaultdict

app = Flask(__name__)

class RateLimiter:
    def __init__(self):
        self.buckets = defaultdict(lambda: {"tokens": 100, "last_update": time.time()})
        self.rate = 10  # tokens per second
        self.capacity = 100
    
    def allow(self, key: str) -> bool:
        bucket = self.buckets[key]
        now = time.time()
        elapsed = now - bucket["last_update"]
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + elapsed * self.rate)
        bucket["last_update"] = now
        
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        return False

limiter = RateLimiter()

@app.before_request
def check_rate_limit():
    client_id = request.headers.get("X-Client-Id", request.remote_addr)
    if not limiter.allow(client_id):
        return jsonify({"error": "Rate limit exceeded", "retry_after": 10}), 429

@app.route("/api/agent/process", methods=["POST"])
@limiter.limit(max_requests=10, window=60)  # Custom decorator
def process():
    return agent_process(request.json)
```

---

## Example 16: Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=14268,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)

class TracedHTTPClient:
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def get(self, url: str, **kwargs):
        with tracer.start_as_current_span("http.client") as span:
            span.set_attribute("http.method", "GET")
            span.set_attribute("http.url", url)
            try:
                response = await self.client.get(url, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                return response
            except Exception as e:
                span.set_attribute("http.error", str(e))
                raise
```

---

## Example 17: Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure = 0
        self.state = "closed"
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "half_open"
            else:
                raise ServiceUnavailable("Circuit breaker open")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failures = 0
        self.state = "closed"
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"

# Usage
breaker = CircuitBreaker()

async def call_model_api(prompt: str):
    return await breaker.call(model_api.generate, prompt)
```

---

## Example 18: Secrets Management

```python
import hvac
import os

class SecretsManager:
    def __init__(self, vault_url: str, vault_token: str):
        self.client = hvac.Client(url=vault_url, token=vault_token)
    
    async def get(self, path: str, key: str) -> str:
        response = self.client.secrets.kv.read_secret_version(path=path)
        return response["data"]["data"][key]
    
    async def get_integration_config(self, integration: str) -> dict:
        path = f"integrations/{integration}"
        try:
            response = self.client.secrets.kv.read_secret_version(path=path)
            return response["data"]["data"]
        except hvac.exceptions.InvalidPath:
            return {}
    
    async def rotate(self, path: str, key: str, value: str):
        self.client.secrets.kv.create_or_update_secret(
            path=path,
            secret={key: value}
        )

# Usage
secrets = SecretsManager(
    vault_url=os.getenv("VAULT_URL"),
    vault_token=os.getenv("VAULT_TOKEN")
)
api_key = await secrets.get("api/keys", "openai_key")
```

---

## Example 19: Backup Verification Script

```bash
#!/bin/bash
# verify-backup.sh

BACKUP_FILE=$1
TEMP_DIR=$(mktemp -d)

echo "Verifying backup: $BACKUP_FILE"

# Extract
gzip -dc "$BACKUP_FILE" > "$TEMP_DIR/backup.sql"

# Check schema
if grep -q "CREATE TABLE" "$TEMP_DIR/backup.sql"; then
    echo "Schema check: PASS"
else
    echo "Schema check: FAIL"
    exit 1
fi

# Count rows
TABLE_COUNT=$(grep -c "COPY" "$TEMP_DIR/backup.sql" || true)
echo "Tables backed up: $TABLE_COUNT"

# Test restore to temp database
TEMP_DB="backup_test_$(date +%s)"
createdb "$TEMP_DB"
psql "$TEMP_DB" < "$TEMP_DIR/backup.sql" > /dev/null 2>&1
RESTORE_EXIT=$?

if [ $RESTORE_EXIT -eq 0 ]; then
    echo "Restore test: PASS"
else
    echo "Restore test: FAIL"
    dropdb "$TEMP_DB" 2>/dev/null
    exit 1
fi

dropdb "$TEMP_DB"
rm -rf "$TEMP_DIR"
echo "Backup verification complete: $BACKUP_FILE"
```

---

## Example 20: Canary Analysis with Prometheus

```python
class CanaryAnalyzer:
    def __init__(self, prometheus_client):
        self.prom = prometheus_client
    
    async def analyze(self, canary: str, baseline: str, 
                      duration_minutes: int = 30) -> dict:
        canary_metrics = await self._get_metrics(canary, duration_minutes)
        baseline_metrics = await self._get_metrics(baseline, duration_minutes)
        
        error_rate_comparison = self._compare_error_rate(
            canary_metrics, baseline_metrics
        )
        latency_comparison = self._compare_latency(
            canary_metrics, baseline_metrics
        )
        
        return {
            "canary": canary,
            "baseline": baseline,
            "error_rate_ratio": error_rate_comparison,
            "latency_ratio": latency_comparison,
            "passed": (
                error_rate_comparison["ratio"] < 1.1 and 
                latency_comparison["ratio"] < 1.1
            )
        }
    
    async def _get_metrics(self, service: str, duration: int):
        # Query Prometheus
        error_rate = await self.prom.query(
            f'sum(rate(agent_requests_total{{service="{service}",status=~"5.."}}[{duration}m]))'
        )
        latency_p99 = await self.prom.query(
            f'histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket{{service="{service}"}}[{duration}m]))'
        )
        return {"error_rate": error_rate, "p99_latency": latency_p99}
    
    def _compare_error_rate(self, canary: dict, baseline: dict) -> dict:
        canary_rate = canary["error_rate"]
        baseline_rate = baseline["error_rate"]
        ratio = canary_rate / max(baseline_rate, 0.001)
        return {"canary": canary_rate, "baseline": baseline_rate, "ratio": ratio}
    
    def _compare_latency(self, canary: dict, baseline: dict) -> dict:
        canary_lat = canary["p99_latency"]
        baseline_lat = baseline["p99_latency"]
        ratio = canary_lat / max(baseline_lat, 0.001)
        return {"canary": canary_lat, "baseline": baseline_lat, "ratio": ratio}
```

---

## Example 21: Load Testing Script

```python
import asyncio
import aiohttp
from dataclasses import dataclass
from typing import List

@dataclass
class LoadTestResult:
    total_requests: int
    success_requests: int
    failed_requests: int
    latencies: List[float]
    errors: List[dict]

async def run_load_test(
    url: str,
    concurrency: int = 50,
    total_requests: int = 1000,
    payload: dict = None
) -> LoadTestResult:
    semaphore = asyncio.Semaphore(concurrency)
    results = []
    errors = []
    latencies = []
    
    async def make_request(session, idx):
        async with semaphore:
            start = time.time()
            try:
                async with session.post(url, json=payload or {"prompt": "test"}) as resp:
                    await resp.text()
                    latency = time.time() - start
                    latencies.append(latency)
                    results.append(resp.status < 400)
            except Exception as e:
                errors.append({"request": idx, "error": str(e)})
                results.append(False)
    
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, i) for i in range(total_requests)]
        await asyncio.gather(*tasks)
    
    return LoadTestResult(
        total_requests=total_requests,
        success_requests=sum(1 for r in results if r),
        failed_requests=sum(1 for r in results if not r),
        latencies=latencies,
        errors=errors
    )

def print_report(result: LoadTestResult):
    success_rate = result.success_requests / result.total_requests * 100
    avg_latency = sum(result.latencies) / len(result.latencies) if result.latencies else 0
    sorted_latencies = sorted(result.latencies)
    p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0
    p95 = sorted_latencies[int(len(sorted_latencies) * 0.95)] if sorted_latencies else 0
    p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)] if sorted_latencies else 0
    
    print(f"Load Test Results")
    print(f"  Total Requests: {result.total_requests}")
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"  Avg Latency: {avg_latency*1000:.1f}ms")
    print(f"  P50 Latency: {p50*1000:.1f}ms")
    print(f"  P95 Latency: {p95*1000:.1f}ms")
    print(f"  P99 Latency: {p99*1000:.1f}ms")
    print(f"  Errors: {len(result.errors)}")

# Usage
result = asyncio.run(run_load_test(
    url="http://localhost:8080/api/agent/process",
    concurrency=50,
    total_requests=1000,
    payload={"prompt": "test", "session_id": "load-test"}
))
print_report(result)
```

---

## Example 22: Canary Analysis

```python
class CanaryAnalyzer:
    def __init__(self, prometheus_client):
        self.prom = prometheus_client
    
    async def analyze(self, canary: str, baseline: str, 
                      duration_minutes: int = 30) -> dict:
        canary_metrics = await self._get_metrics(canary, duration_minutes)
        baseline_metrics = await self._get_metrics(baseline, duration_minutes)
        
        error_rate_comparison = self._compare_error_rate(
            canary_metrics, baseline_metrics
        )
        latency_comparison = self._compare_latency(
            canary_metrics, baseline_metrics
        )
        
        return {
            "canary": canary,
            "baseline": baseline,
            "error_rate_ratio": error_rate_comparison["ratio"],
            "latency_ratio": latency_comparison["ratio"],
            "passed": error_rate_comparison["ratio"] < 1.1 and latency_comparison["ratio"] < 1.1
        }
    
    async def _get_metrics(self, service: str, duration: int):
        error_rate = await self.prom.query(
            f'rate(agent_requests_total{{service="{service}",status=~"5.."}}[{duration}m])'
        )
        latency_p99 = await self.prom.query(
            f'histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket{{service="{service}"}}[{duration}m]))'
        )
        return {"error_rate": error_rate, "p99_latency": latency_p99}
```

---

## Example 23: Deployment Pipeline

```yaml
# GitHub Actions workflow
name: Agent Deployment Pipeline
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=src
      - uses: actions/upload-artifact@v4
        with: {name: coverage, path: coverage.xml}
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t agent:${{ github.sha }} .
      - run: docker push agent:${{ github.sha }}
      - run: kubectl set image deployment/agent agent=agent:${{ github.sha }}
```

---

## Example 24: Capability Scoring

```python
class Scoring:
    def score(items: list[dict]) -> float:
        total = len(items)
        if total == 0:
            return 0.0
        done = sum(1 for i in items if i.get("done"))
        return (done / total) * 100

    def classify(score: float) -> str:
        if score >= 90:
            return "production ready"
        elif score >= 70:
            return "needs minor fixes"
        elif score >= 50:
            return "needs significant work"
        return "not production ready"
```

---

## Example 25: Scoring Summary

```text
score >= 90  production ready
score >= 70  needs minor fixes
score >= 50  needs significant work
score <  50  not production ready
```

---

## Example 26: Incident Review Checklist

```markdown
- [ ] User impact and timeline documented.
- [ ] Failing dependency or behavior identified.
- [ ] Prompt, model, retrieval, and tool versions recorded.
- [ ] Logs reviewed with sensitive data controls.
- [ ] Immediate mitigation applied.
- [ ] Permanent fix assigned.
- [ ] Related checklist or troubleshooting guidance updated.
```

---

## Example 27: Model Behavior Rollback

```python
async def rollback_model(release: dict, target: dict):
    from kubernetes import client
    
    api = client.AppsV1Api()
    deployment = api.read_namespaced_deployment(
        name=release["name"],
        namespace=release["namespace"]
    )
    
    for container in deployment.spec.template.spec.containers:
        if container.name == "agent":
            container.env = [
                env for env in (container.env or [])
                if env.name != "MODEL_VERSION"
            ] + [client.V1EnvVar(
                name="MODEL_VERSION",
                value=target["model_version"]
            )]
    
    api.patch_namespaced_deployment(
        name=release["name"],
        namespace=release["namespace"],
        body=deployment
    )
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)