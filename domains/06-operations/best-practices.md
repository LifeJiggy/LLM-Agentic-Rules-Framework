# Operations Domain - Best Practices

## Overview

This document outlines comprehensive operations best practices for LLM/agentic systems, covering deployment, monitoring, scaling, reliability, incident response, and production operations.

---

## Table of Contents

1. [Deployment Best Practices](#1-deployment-best-practices)
2. [Monitoring Best Practices](#2-monitoring-best-practices)
3. [Scaling Best Practices](#3-scaling-best-practices)
4. [Configuration Management](#4-configuration-management)
5. [Security & Compliance](#5-security--compliance)
6. [Cost Optimization](#6-cost-optimization)
7. [Reliability Patterns](#7-reliability-patterns)
8. [Team & Process](#8-team--process)
9. [Tooling & Automation](#9-tooling--automation)
10. [Lifecycle Management](#10-lifecycle-management)

---

## 1. Deployment Best Practices

### Health Checks

```python
@app.route("/health")
def health():
    return {
        "status": "healthy",
        "checks": {
            "database": _check_db(),
            "model": _check_model(),
            "cache": _check_cache()
        }
    }

@app.route("/ready")
def ready():
    return {"ready": all_systems_operational()}
```

### Resource Limits

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Deployment Automation

```yaml
# GitHub Actions CI/CD
name: Deploy Agent
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        run: |
          docker build -t agent:${{ github.sha }} .
          docker push agent:${{ github.sha }}
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/agent agent=agent:${{ github.sha }}
```

### Rollback Procedures

```python
class RollbackManager:
    def __init__(self, deployment_client):
        self.client = deployment_client
        self.rollback_history = []
    
    async def rollback(self, deployment_name: str, revision: int = None):
        current = await self.client.get_deployment(deployment_name)
        await self.client.rollout_undo(deployment_name, revision=revision)
        self.rollback_history.append({
            "deployment": deployment_name,
            "from_revision": current.revision,
            "timestamp": datetime.utcnow()
        })
        logger.info(f"Rolled back {deployment_name}")
```

### Deployment Validation

```python
class DeploymentValidator:
    def __init__(self):
        self.checks = []
    
    def add_check(self, name: str, check_fn, critical: bool = True):
        self.checks.append({"name": name, "fn": check_fn, "critical": critical})
    
    async def validate(self) -> dict:
        results = {}
        failed_critical = []
        for check in self.checks:
            try:
                ok = await check["fn"]()
                results[check["name"]] = {"status": "pass" if ok else "fail", "critical": check["critical"]}
                if not ok and check["critical"]:
                    failed_critical.append(check["name"])
            except Exception as e:
                results[check["name"]] = {"status": "error", "error": str(e)}
                if check["critical"]:
                    failed_critical.append(check["name"])
        return {"healthy": len(failed_critical) == 0, "checks": results, "failed_critical": failed_critical}
```

### Progressive Delivery

```python
class TrafficSplitter:
    def __init__(self):
        self.splits = {}
    
    def set_split(self, service: str, version_weights: dict):
        self.splits[service] = version_weights
    
    def route(self, service: str, user_id: str) -> str:
        weights = self.splits.get(service, {})
        # Simple weighted random with sticky sessions
        import hashlib
        h = int(hashlib.md5(f"{service}:{user_id}".encode()).hexdigest(), 16)
        cumulative = 0
        for version, weight in weights.items():
            cumulative += weight
            if h % 100 < cumulative:
                return version
        return list(weights.keys())[0]
```

---

## 2. Monitoring Best Practices

### Structured Logging

```python
import structlog
logger = structlog.get_logger()

def log_agent_operation(operation: str, duration_ms: float, **metadata):
    logger.info(
        "agent.operation",
        operation=operation,
        duration=duration_ms,
        **metadata
    )
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

requests = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["method", "endpoint", "status"]
)
duration = Histogram(
    "agent_request_duration_seconds",
    "Request duration",
    ["endpoint"]
)
active = Gauge(
    "agent_active_sessions",
    "Active sessions"
)

def observe_request(method, endpoint, status, dur):
    requests.labels(method=method, endpoint=endpoint, status=status).inc()
    duration.labels(endpoint=endpoint).observe(dur)
```

### Alerting Strategy

```python
ALERT_RULES = {
    "high_latency": {
        "expr": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m])) > 5",
        "for": "2m",
        "severity": "warning",
        "summary": "High latency detected"
    },
    "error_rate": {
        "expr": "rate(agent_requests_total{status=~\"5..\"}[5m]) / rate(agent_requests_total[5m]) > 0.05",
        "for": "1m",
        "severity": "critical",
        "summary": "Error rate too high"
    },
    "queue_depth": {
        "expr": "agent_queue_depth > 1000",
        "for": "5m",
        "severity": "warning",
        "summary": "Message queue backing up"
    }
}

class AlertManager:
    def __init__(self, notifier):
        self.notifier = notifier
        self.rules = ALERT_RULES
    
    async def evaluate(self, metrics: dict):
        for rule_name, rule in self.rules.items():
            if self._matches(metrics, rule):
                await self.notifier.send({
                    "alert": rule_name,
                    "severity": rule["severity"],
                    "summary": rule["summary"],
                    "metrics": metrics
                })
    
    def _matches(self, metrics: dict, rule: dict) -> bool:
        return False  # PromQL evaluation logic
```

### Dashboarding

```python
DASHBOARD_CONFIG = {
    "title": "Agent Operations",
    "panels": [
        {"title": "Request Rate", "query": "sum(rate(agent_requests_total[5m]))", "type": "graph"},
        {"title": "Latency P50/P95/P99", "query": "histogram_quantile(0.99, ...)", "type": "graph"},
        {"title": "Error Budget", "query": "1 - (error_rate / total_rate)", "type": "gauge"},
        {"title": "Active Sessions", "query": "agent_active_sessions", "type": "stat"},
        {"title": "Token Usage", "query": "sum(rate(agent_tokens_total[1h]))", "type": "graph"},
        {"title": "Cache Hit Ratio", "query": "cache_hits / (cache_hits + cache_misses)", "type": "stat"}
    ]
}
```

---

## 3. Scaling Best Practices

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

### Vertical Scaling

```python
class ResourceManager:
    def __init__(self):
        self.scaling_policies = {
            "small": {"cpu": "500m", "memory": "1Gi", "replicas": 2},
            "medium": {"cpu": "2", "memory": "4Gi", "replicas": 4},
            "large": {"cpu": "4", "memory": "8Gi", "replicas": 8}
        }
    
    def recommend_resources(self, request_rate: int, avg_tokens: int) -> dict:
        if request_rate < 100 and avg_tokens < 1000:
            return self.scaling_policies["small"]
        elif request_rate < 1000 and avg_tokens < 4000:
            return self.scaling_policies["medium"]
        return self.scaling_policies["large"]
```

### Load Balancing

```python
class LoadBalancer:
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self.instances = []
    
    def add_instance(self, host, port, weight=1):
        self.instances.append({"host": host, "port": port, "weight": weight, "connections": 0})
    
    def select(self):
        if self.strategy == "round_robin":
            instance = self.instances[self._index % len(self.instances)]
            self._index += 1
            return instance
        elif self.strategy == "least_connections":
            return min(self.instances, key=lambda i: i["connections"])
        elif self.strategy == "weighted":
            return random.choices(self.instances, weights=[i["weight"] for i in self.instances])[0]
```

### Autoscaling Policies

```python
class AutoscalingPolicy:
    def __init__(self):
        self.metrics_window = []
        self.scale_up_threshold = 0.8
        self.scale_down_threshold = 0.3
        self.cooldown_period = 300
    
    def evaluate(self, metrics) -> dict:
        cpu_util = metrics.get("cpu_utilization", 0)
        queue_depth = metrics.get("queue_depth", 0)
        
        if cpu_util > self.scale_up_threshold or queue_depth > 1000:
            return {"action": "scale_up", "reason": f"cpu={cpu_util}, queue={queue_depth}"}
        elif cpu_util < self.scale_down_threshold and queue_depth < 100:
            return {"action": "scale_down", "reason": f"cpu={cpu_util}"}
        return {"action": "none"}
```

---

## 4. Configuration Management

### Environment-Based Configuration

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    environment: str = "production"
    log_level: str = "INFO"
    database_url: str
    redis_url: str
    model_name: str = "gpt-4"
    max_tokens: int = 4096
    temperature: float = 0.7
    api_timeout: int = 30
    max_retries: int = 3
    
    class Config:
        env_file = f".env.{os.getenv('ENV', 'production')}"
        case_sensitive = False

settings = Settings()
```

### Secrets Management

```python
class SecretsManager:
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_url = vault_url
        self.vault_token = vault_token
    
    async def get_secret(self, path: str, key: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.vault_url}/v1/secret/{path}",
                headers={"X-Vault-Token": self.vault_token}
            ) as resp:
                data = await resp.json()
                return data["data"]["data"][key]
    
    async def rotate_api_key(self, service: str):
        new_key = await self._generate_key()
        await self._vault_write(f"integrations/{service}", {"api_key": new_key})
        logger.info(f"Rotated API key for {service}")
```

### Hot Configuration Updates

```python
class ConfigWatcher:
    def __init__(self, config_path: str, callback):
        self.config_path = config_path
        self.callback = callback
        self.last_modified = 0
    
    async def watch(self, interval: int = 5):
        while True:
            try:
                stat = os.stat(self.config_path)
                if stat.st_mtime > self.last_modified:
                    self.last_modified = stat.st_mtime
                    with open(self.config_path) as f:
                        new_config = yaml.safe_load(f)
                    await self.callback(new_config)
            except FileNotFoundError:
                pass
            await asyncio.sleep(interval)
```

---

## 5. Security & Compliance

### mTLS Configuration

```yaml
# Kubernetes mTLS configuration
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: agent-system
spec:
  mtls:
    mode: STRICT
```

### Audit Logging

```python
class AuditLogger:
    def __init__(self, log_sink):
        self.sink = log_sink
    
    async def log_access(self, user_id: str, action: str, resource: str, outcome: str, metadata: dict = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "outcome": outcome,
            "metadata": metadata or {},
            "source_ip": request.remote_addr
        }
        await self.sink.write(entry)
    
    async def log_admin_action(self, admin_id: str, action: str, target: str):
        await self.log_access(admin_id, f"admin.{action}", target, "initiated")
        # Also send to security SIEM
        await self.siems.send(entry)
```

### Secrets Rotation Policy

```python
class SecretRotationPolicy:
    def __init__(self):
        self.rotation_intervals = {
            "api_keys": timedelta(days=90),
            "jwt_secrets": timedelta(days=30),
            "database_passwords": timedelta(days=60),
            "tls_certificates": timedelta(days=30)
        }
        self.rotation_history = {}
    
    def is_due(self, secret_type: str, last_rotated: datetime) -> bool:
        interval = self.rotation_intervals.get(secret_type)
        if not interval:
            return False
        return datetime.utcnow() - last_rotated > interval
```

---

## 6. Cost Optimization

### Token Budget Management

```python
class TokenBudgetManager:
    def __init__(self, monthly_budget: int):
        self.monthly_budget = monthly_budget
        self.current_usage = 0
        self.reset_date = self._next_month()
    
    def _next_month(self) -> datetime:
        now = datetime.utcnow()
        if now.month == 12:
            return datetime(now.year + 1, 1, 1)
        return datetime(now.year, now.month + 1, 1)
    
    def can_spend(self, tokens: int) -> bool:
        if datetime.utcnow() > self.reset_date:
            self.current_usage = 0
            self.reset_date = self._next_month()
        projected = self.current_usage + tokens
        return projected <= self.monthly_budget
    
    def record_usage(self, tokens: int):
        self.current_usage += tokens
```

### Cost Attribution

```python
class CostAttributor:
    def __init__(self):
        self.costs = defaultdict(float)
        self.token_prices = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
    
    def record_request(self, model: str, input_tokens: int, output_tokens: int, tenant: str):
        prices = self.token_prices.get(model, {"input": 0.01, "output": 0.03})
        cost = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1000
        self.costs[tenant] += cost
```

### Caching Strategy

```python
CACHE_POLICIES = {
    "static_content": {"ttl": 86400, "strategy": "cache_first"},
    "user_sessions": {"ttl": 1800, "strategy": "cache_first"},
    "model_responses": {"ttl": 3600, "strategy": "stale_while_revalidate"},
    "search_results": {"ttl": 600, "strategy": "network_first"}
}
```

---

## 7. Reliability Patterns

### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "closed"
        self.last_failure = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "half_open"
            else:
                raise ServiceUnavailable("Circuit open")
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
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
```

### Bulkhead Isolation

```python
class BulkheadManager:
    def __init__(self):
        self.bulkheads = {}
    
    def register(self, name: str, limit: int):
        self.bulkheads[name] = asyncio.Semaphore(limit)
    
    async def execute(self, name: str, coro):
        async with self.bulkheads[name]:
            return await coro
```

### Retry Policies

```python
from tenacity import retry, stop_after_attempt, wait_exponential

retry_policy = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((TimeoutError, ConnectionError))
)

@retry_policy
async def call_external_service(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            resp.raise_for_status()
            return await resp.json()
```

### Timeout Management

```python
class TimeoutManager:
    def __init__(self):
        self.timeouts = {
            "database": 5,
            "model_api": 30,
            "external_api": 10,
            "cache": 1
        }
    
    def get_timeout(self, service: str) -> int:
        return self.timeouts.get(service, 10)
    
    async def with_timeout(self, service: str, coro):
        timeout = self.get_timeout(service)
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            logger.error(f"Timeout on {service} after {timeout}s")
            raise
```

### Graceful Degradation

```python
class GracefulDegradation:
    def __init__(self):
        self.fallbacks = {}
    
    def register_fallback(self, service: str, fallback_fn):
        self.fallbacks[service] = fallback_fn
    
    async def call_with_fallback(self, service: str, primary_fn, *args, **kwargs):
        try:
            return await primary_fn(*args, **kwargs)
        except (TimeoutError, ServiceUnavailable) as e:
            logger.warning(f"Service {service} degraded, using fallback")
            fallback = self.fallbacks.get(service)
            if fallback:
                return await fallback(*args, **kwargs)
            raise
```

---

## 8. Team & Process

### Incident Management

```python
class IncidentManager:
    def __init__(self, alert_channel, on_call_rotation):
        self.alert_channel = alert_channel
        self.on_call = on_call_rotation
        self.active_incidents = {}
    
    async def create_incident(self, severity: str, description: str, metrics: dict):
        incident_id = str(uuid.uuid4())
        responder = self.on_call.get_current()
        
        self.active_incidents[incident_id] = {
            "id": incident_id,
            "severity": severity,
            "description": description,
            "responder": responder,
            "created_at": datetime.utcnow(),
            "status": "open",
            "metrics": metrics
        }
        
        await self.alert_channel.send({
            "incident_id": incident_id,
            "severity": severity,
            "responder": responder,
            "description": description
        })
        
        return incident_id
    
    async def resolve(self, incident_id: str, resolution: str):
        incident = self.active_incidents.get(incident_id)
        if incident:
            incident["status"] = "resolved"
            incident["resolved_at"] = datetime.utcnow()
            incident["resolution"] = resolution
            await self.alert_channel.send({
                "incident_id": incident_id,
                "status": "resolved",
                "resolution": resolution
            })
```

### Runbook Management

```python
class RunbookManager:
    def __init__(self, runbook_dir: str):
        self.runbook_dir = runbook_dir
        self.runbooks = {}
        self._load_runbooks()
    
    def _load_runbooks(self):
        for filename in os.listdir(self.runbook_dir):
            if filename.endswith(".md"):
                runbook_id = filename[:-3]
                with open(os.path.join(self.runbook_dir, filename)) as f:
                    self.runbooks[runbook_id] = f.read()
    
    def get_runbook(self, incident_type: str) -> str:
        return self.runbooks.get(incident_type, self.runbooks.get("generic"))
    
    async def execute_runbook(self, runbook_id: str, context: dict):
        runbook = self.get_runbook(runbook_id)
        for step in self._parse_steps(runbook):
            result = await step.execute(context)
            if not result.success:
                return {"status": "failed", "step": step.name, "error": result.error}
        return {"status": "completed"}
```

---

## 9. Tooling & Automation

### CI/CD Pipelines

```yaml
name: Agent CI/CD
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
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
        options: --health-cmd pg_isready
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install bandit safety
      - run: bandit -r src/
      - run: safety check

  deploy:
    needs: [lint, test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          tags: agent:${{ github.sha }}
          push: true
      - run: kubectl set image deployment/agent agent=agent:${{ github.sha }}
```

### GitOps Configuration

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: agent-production
spec:
  project: ml-platform
  source:
    repoURL: https://github.com/org/agent-config
    path: prod
    helm:
      valueFiles:
      - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: agent-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Chaos Engineering

```python
class ChaosEngine:
    def __init__(self, experiment_dir: str):
        self.experiment_dir = experiment_dir
        self.experiments = {}
        self._load_experiments()
    
    def _load_experiments(self):
        for filename in os.listdir(self.experiment_dir):
            if filename.endswith(".yaml"):
                with open(os.path.join(self.experiment_dir, filename)) as f:
                    self.experiments[filename] = yaml.safe_load(f)
    
    async def run_experiment(self, name: str, duration: int = 60):
        exp = self.experiments.get(name)
        if not exp:
            raise ValueError(f"Unknown experiment: {name}")
        
        logger.info(f"Starting chaos experiment: {name}")
        await self._apply(exp["fault"])
        
        await asyncio.sleep(duration)
        
        await self._revert(exp["fault"])
        
        metrics = await self._collect_metrics(exp["hypothesis"])
        return {
            "experiment": name,
            "status": "completed",
            "metrics": metrics,
            "blasted_radius": exp.get("blast_radius", "service")
        }
```

---

## 10. Lifecycle Management

### Version Management

```python
class VersionManager:
    def __init__(self):
        self.versions = {}
        self.deprecation_schedule = {}
    
    def register_version(self, version: str, config: dict, sunset_date: str = None):
        self.versions[version] = config
        if sunset_date:
            self.deprecation_schedule[version] = sunset_date
    
    def is_deprecated(self, version: str) -> bool:
        sunset = self.deprecation_schedule.get(version)
        if not sunset:
            return False
        return datetime.utcnow() > datetime.fromisoformat(sunset)
    
    def get_active_versions(self) -> list:
        return [v for v in self.versions if not self.is_deprecated(v)]
```

### Backup Verification

```python
class BackupVerifier:
    def __init__(self, backup_store):
        self.store = backup_store
    
    async def verify(self, backup_id: str) -> dict:
        meta = await self.store.get_metadata(backup_id)
        checksum = await self.store.get_checksum(backup_id)
        
        # Download and verify
        data = await self.store.download(backup_id)
        computed = hashlib.sha256(data).hexdigest()
        
        valid = computed == checksum
        return {
            "backup_id": backup_id,
            "valid": valid,
            "size": len(data),
            "created": meta.get("created_at"),
            "checksum_match": valid
        }
    
    async def test_restore(self, backup_id: str) -> dict:
        # Restore to test environment
        test_db = await self._create_test_db()
        try:
            await self.store.restore(backup_id, test_db)
            record_count = await test_db.count_records()
            return {"success": True, "records_restored": record_count}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await self._destroy_test_db(test_db)
```

### Data Retention

```python
class RetentionManager:
    def __init__(self, storage):
        self.storage = storage
        self.retention_policies = {
            "conversations": timedelta(days=90),
            "logs": timedelta(days=30),
            "metrics": timedelta(days=365),
            "audit": timedelta(days=2555)  # 7 years
        }
    
    async def enforce_retention(self):
        for data_type, ttl in self.retention_policies.items():
            cutoff = datetime.utcnow() - ttl
            deleted = await self.storage.delete_older_than(data_type, cutoff)
            logger.info(f"Retention: deleted {deleted} {data_type} records")
    
    async def archive_old_data(self, archive_bucket: str):
        for data_type, ttl in self.retention_policies.items():
            if ttl.days > 365:
                cutoff = datetime.utcnow() - ttl
                await self.storage.archive(data_type, archive_bucket, cutoff)
```

---

## Deeper Operational Guidance

### Deployment Validation and Rollout Control

```python
class ProductionGate:
    def __init__(self, checks: list):
        self.checks = checks
    
    async def evaluate(self) -> bool:
        for check in self.checks:
            result = await check.run()
            if not result.passed:
                logger.error(f"Gate failed: {check.name}")
                return False
        return True

# Example checks
checks = [
    HealthCheck(name="api_health", endpoint="/health"),
    TestSuite(name="smoke_tests", suite="smoke"),
    SecurityScan(name="image_scan", image="agent:latest"),
    PerformanceBenchmark(name="latency", p99_threshold=5.0)
]
gate = ProductionGate(checks)
if await gate.evaluate():
    await promote_to_production()
```

### Operations Metrics and SLOs

```python
class SLOMonitor:
    def __init__(self):
        self.slos = {
            "availability": {"target": 0.999, "window": "30d"},
            "latency_p99": {"target": 5.0, "window": "7d"},
            "error_budget": {"target": 0.001, "window": "30d"}
        }
    
    def evaluate(self, metrics) -> dict:
        results = {}
        for slo_name, config in self.slos.items():
            actual = self._compute(metrics, slo_name, config["window"])
            results[slo_name] = {
                "target": config["target"],
                "actual": actual,
                "status": "met" if actual >= config["target"] else "violated",
                "remaining_budget": self._remaining_budget(actual, config["target"])
            }
        return results
    
    def _compute(self, metrics, slo_name, window):
        # Compute SLO from time series metrics
        return 0.999  # placeholder
    
    def _remaining_budget(self, actual, target):
        return max(0, actual - target)
```

### Operations Playbooks

```python
PLAYBOOKS = {
    "high_error_rate": {
        "description": "Investigate and remediate elevated error rates",
        "steps": [
            {"action": "check_deployments", "command": "kubectl rollout history deployment/agent"},
            {"action": "review_logs", "command": "kubectl logs -l app=agent --tail=100"},
            {"action": "check_model_status", "command": "curl https://status.openai.com/api/v2/status.json"},
            {"action": "scale_up", "condition": "error_rate > 0.1", "command": "kubectl scale deployment/agent --replicas=10"},
            {"action": "rollback", "condition": "error_rate > 0.3", "command": "kubectl rollout undo deployment/agent"}
        ],
        "escalation": {"after_minutes": 15, "channel": "#incidents-critical"}
    },
    "latency_spike": {
        "description": "Diagnose and resolve latency degradation",
        "steps": [
            {"action": "check_prometheus", "query": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))"},
            {"action": "check_db_queries", "command": "pg_stat_statements top 5"},
            {"action": "check_retriever_latency", "command": "curl /metrics | grep retrieval"},
            {"action": "reduce_context", "condition": "prompt_tokens > 8000", "command": "kubectl set env deployment/agent MAX_TOKENS=4000"}
        ]
    }
}
```

```python
class PlaybookExecutor:
    def __init__(self, command_runner, metrics_client):
        self.command_runner = command_runner
        self.metrics = metrics_client
        self.playbooks = PLAYBOOKS
    
    async def execute(self, playbook_name: str, context: dict):
        playbook = self.playbooks.get(playbook_name)
        if not playbook:
            raise ValueError(f"Unknown playbook: {playbook_name}")
        
        logger.info(f"Executing playbook: {playbook_name}")
        results = []
        for step in playbook["steps"]:
            if "condition" in step:
                if not self._evaluate_condition(step["condition"], context, self.metrics):
                    continue
            result = await self.command_runner.run(step["command"])
            results.append({"step": step["action"], "result": result})
        
        if "escalation" in playbook:
            await self._check_escalation(playbook["escalation"], results)
        
        return results
```

### Change Management

```python
class ChangeManager:
    def __init__(self, approvals_db, deployment_scheduler):
        self.approvals = approvals_db
        self.scheduler = deployment_scheduler
    
    async def submit_change(self, change: dict, requester: str) -> str:
        change_id = str(uuid.uuid4())
        change_record = {
            "id": change_id,
            "requester": requester,
            "description": change["description"],
            "risk_level": change.get("risk_level", "medium"),
            "rollback_plan": change.get("rollback_plan"),
            "status": "pending_approval",
            "created_at": datetime.utcnow()
        }
        await self.approvals.create(change_record)
        
        if change_record["risk_level"] == "high":
            await self._request_cab_approval(change_id)
        
        return change_id
    
    async def approve(self, change_id: str, approver: str):
        change = await self.approvals.get(change_id)
        change["status"] = "approved"
        change["approved_by"] = approver
        change["approved_at"] = datetime.utcnow()
        change["scheduled_at"] = self.scheduler.next_window(change["risk_level"])
        await self.approvals.update(change)
    
    async def _request_cab_approval(self, change_id: str):
        await self.cab_channel.send(f"Change {change_id} requires CAB approval")
```

### Capacity Planning

```python
class CapacityPlanner:
    def __init__(self, metrics_store):
        self.metrics = metrics_store
    
    def recommend_capacity(self, forecast_days: int = 30) -> dict:
        history = self.metrics.get_last_90_days()
        
        current_peak = max(day["peak_qps"] for day in history)
        avg_growth = self._calculate_growth(history)
        
        projected = current_peak * (1 + avg_growth * forecast_days / 30)
        headroom = projected * 1.2  # 20% buffer
        
        return {
            "recommended_qps_capacity": round(headroom),
            "recommended_replicas": math.ceil(headroom / 100),
            "forecast_period_days": forecast_days,
            "growth_rate": f"{avg_growth:.2%}",
            "current_peak": current_peak,
            "confidence": "medium"
        }
    
    def _calculate_growth(self, history: list) -> float:
        # Simple linear regression on daily peak
        if len(history) < 7:
            return 0.0
        n = len(history)
        x = list(range(n))
        y = [d["peak_qps"] for d in history]
        return self._linear_slope(x, y)
    
    def _linear_slope(self, x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        return numerator / denominator if denominator else 0
```

### Patch and Upgrade Management

```python
class UpgradeManager:
    def __init__(self):
        self.upgrade_schedule = {}
        self.maintenance_windows = {
            "prod": ["sun 02:00-06:00"],
            "staging": ["sat 00:00-04:00"]
        }
    
    def schedule_upgrade(self, component: str, target_version: str, env: str):
        windows = self.maintenance_windows.get(env, [])
        next_window = self._next_window(windows)
        
        upgrade = {
            "component": component,
            "target_version": target_version,
            "scheduled_at": next_window,
            "env": env,
            "status": "scheduled",
            "abort_conditions": ["error_rate > 0.01", "p99_latency > 10s"]
        }
        self.upgrade_schedule[component] = upgrade
        return upgrade
    
    def _next_window(self, windows: list) -> datetime:
        # Find next maintenance window
        return datetime.utcnow() + timedelta(days=7)
    
    async def execute_upgrade(self, component: str) -> dict:
        upgrade = self.upgrade_schedule.get(component)
        if not upgrade:
            return {"status": "not_scheduled"}
        
        logger.info(f"Upgrading {component} to {upgrade['target_version']}")
        await self._backup_current(component)
        await self._apply_upgrade(component, upgrade["target_version"])
        
        health = await self._verify_health(component)
        if not health:
            await self._rollback(component)
            return {"status": "failed", "action": "rolled_back"}
        
        upgrade["status"] = "completed"
        return {"status": "success"}
```

### Operations Review Meeting Structure

```markdown
# Weekly Operations Review

## Agenda (30 minutes)

1. **Reliability Metrics Review** (5 min)
   - Availability target: 99.9% | Actual: 99.95%
   - Error budget remaining: 50%
   - P95 latency: 2.1s (target: <5s)

2. **Incident Post-Mortems** (10 min)
   - P0 incidents this week: 0
   - P1 incidents: 1 (memory pressure - root cause: leak in cache client)
   - Action items assigned and tracked

3. **Change Review** (5 min)
   - Deployments this week: 12
   - Failed deployments: 0
   - Rollbacks: 0

4. **Capacity and Scaling** (5 min)
   - Current peak: 450 QPS
   - Projected in 30 days: 520 QPS
   - Recommendation: Scale to 8 replicas

5. **Open Items** (5 min)
   - Technical debt items
   - Security patches pending
```

### Disaster Recovery Runbook

```python
DR_CONFIG = {
    "rto_minutes": 15,
    "rpo_minutes": 5,
    "backup_frequency_hours": 6,
    "backup_retention_days": 30,
    "cross_region_replication": True,
    "failover_endpoint": "https://dr.agent.example.com"
}

class DisasterRecoveryManager:
    def __init__(self):
        self.last_drill = None
        self.drill_interval = timedelta(days=90)
    
    async def failover(self, target_region: str):
        """Execute disaster recovery failover."""
        start = time.time()
        logger.critical(f"Initiating DR failover to {target_region}")
        
        tasks = [
            self._promote_read_replica(target_region),
            self._update_dns(target_region),
            self._verify_endpoint_health(target_region),
            self._notify_stakeholders(target_region)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        duration = time.time() - start
        logger.info(f"DR failover completed in {duration:.1f}s")
        
        if duration * 60 > DR_CONFIG["rto_minutes"]:
            logger.error(f"DR failover exceeded RTO: {duration:.1f}s")
        
        return {"duration_seconds": duration, "results": results}
    
    async def promote_read_replica(self, region: str):
        # Promote replica to primary
        pass
    
    async def update_dns(self, region: str):
        # Update DNS to point to DR region
        pass
    
    async def notify_stakeholders(self, region: str):
        # Notify users and teams
        pass
```

### Change Freeze and Maintenance Windows

```python
class MaintenanceWindowManager:
    def __init__(self):
        self.windows = {
            "prod": {
                "days": [6],  # Sunday
                "hours": [(2, 6)],  # 2 AM - 6 AM
                "timezone": "UTC"
            }
        }
        self.freeze_periods = [
            {"start": "2024-11-25", "end": "2024-11-30", "reason": "Black Friday"},
            {"start": "2024-12-20", "end": "2025-01-02", "reason": "Holiday season"}
        ]
    
    def is_maintenance_window(self, env: str) -> bool:
        now = datetime.utcnow()
        window = self.windows.get(env)
        if not window:
            return False
        if now.weekday() not in window["days"]:
            return False
        hour = now.hour
        return any(start <= hour < end for start, end in window["hours"])
    
    def is_freeze_period(self) -> bool:
        now = datetime.utcnow().date()
        for freeze in self.freeze_periods:
            start = date.fromisoformat(freeze["start"])
            end = date.fromisoformat(freeze["end"])
            if start <= now <= end:
                return True
        return False
```

### Ops Team Communication Protocols

```python
class IncidentCommunicationPlan:
    SEVERITY_RESPONSES = {
        "P0": {
            "initial_response": "15 minutes",
            "updates": "Every 15 minutes",
            "escalation": "After 30 minutes",
            "channels": ["#incidents-critical", "email-all-hands"]
        },
        "P1": {
            "initial_response": "1 hour",
            "updates": "Every 30 minutes",
            "escalation": "After 2 hours",
            "channels": ["#incidents", "slack-manager"]
        },
        "P2": {
            "initial_response": "4 hours",
            "updates": "Every 2 hours",
            "escalation": "Next business day",
            "channels": ["#ops-alerts"]
        }
    }
    
    def get_response_plan(self, severity: str) -> dict:
        return self.SEVERITY_RESPONSES.get(severity, self.SEVERITY_RESPONSES["P2"])
```

### Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

## Summary
- **Date**: YYYY-MM-DD
- **Duration**: X hours Y minutes
- **Severity**: P0/P1/P2
- **Impact**: X users affected

## Timeline
- HH:MM - Detected
- HH:MM - Responder joined
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Service restored

## Root Cause
[Detailed explanation]

## Action Items
| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P0 | Fix primary cause | @name | YYYY-MM-DD |
| P1 | Improve monitoring | @name | YYYY-MM-DD |
| P2 | Update runbook | @name | YYYY-MM-DD |
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)