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

---

## Deployment Anti-Patterns

### 1. No Health Checks

```python
# Bad
app.run()

# Good
@app.route("/health")
def health():
    checks = {
        "database": check_db(),
        "cache": check_cache(),
        "model_api": check_model_api()
    }
    status = 200 if all(checks.values()) else 503
    return {"status": checks}, status
```

### 2. Stateless Scaling Assumption

```python
# Bad - State in memory, breaks on horizontal scale
user_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    session_id = request.json["session_id"]
    history = user_sessions[session_id]
    response = model.generate(history)
    user_sessions[session_id].append(response)
    return response

# Good - Externalized state
@app.route("/chat", methods=["POST"])
def chat():
    session_id = request.json["session_id"]
    history = session_store.get(session_id)
    response = model.generate(history)
    session_store.append(session_id, response)
    return response
```

### 3. No Resource Limits

```yaml
# Bad - No resource constraints
containers:
- name: model
  resources: {}

# Good - Enforce limits
containers:
- name: model
  resources:
    requests:
      memory: "2Gi"
      cpu: "1"
    limits:
      memory: "4Gi"
      cpu: "2"
```

### 4. Deploying Without Canarying

```python
# Bad - Big bang deployment
@app.route("/predict")
def predict():
    return model_v2.predict(request.json)

# Good - Canary
@app.route("/predict")
def predict():
    version = traffic_splitter.get_version(request.headers.get("X-User-Id"))
    if version == "v2":
        return model_v2.predict(request.json)
    return model_v1.predict(request.json)
```

---

## Monitoring Anti-Patterns

### 1. Logging Without Structure

```python
# Bad
logger.info(f"Processing request from {user_id}")

# Good
logger.info("request_processed", user_id=user_id, duration=duration, model=model_name)
```

### 2. No SLI/SLO Definition

```python
# Bad - No targets defined
requests = Counter("requests_total")

# Good - With SLO tracking
requests = Counter("requests_total", ["endpoint", "status"])
errors = Counter("errors_total", ["type"])
latency = Histogram("request_duration", ["endpoint"])

SLOS = {
    "availability": {"target": 0.999, "window": "30d"},
    "latency": {"target": 0.95, "p99_threshold": 5.0}
}
```

### 3. Alert Fatigue

```python
# Bad - Every error page triggers an alert
@atexit.register
def alert_on_exit():
    send_alert("Process exited")

# Good - Coherent alerting
throttle = AlertThrottle(window=300, max_alerts=5)

def should_alert(event):
    return throttle.check(event.id)

ALERT_ROUTING = {
    "critical": ["@ops-team", "#incidents-critical"],
    "warning": ["#ops-alerts"],
    "info": []
}
```

---

## Scaling Anti-Patterns

### 1. Vertical Scaling Only

```python
# Bad - One big server
class SingleServer:
    def __init__(self):
        self.instance = EC2(t2.xlarge)

# Good - Horizontal scaling
class AutoScalingPool:
    def __init__(self):
        self.pool = ECS(cluster="agent", min=2, max=20)
```

### 2. Ignoring Queue Backpressure

```python
# Bad
for event in event_stream:
    asyncio.create_task(process(event))

# Good - Limited concurrency
semaphore = asyncio.Semaphore(100)

async def process_event(event):
    async with semaphore:
        return await handle(event)

tasks = [process_event(e) for e in events]
await asyncio.gather(*tasks)
```

### 3. Scaling on Wrong Metrics

```python
# Bad - Scale on memory (lagging indicator)
scaler.scale_if("mem > 80%")

# Good - Scale on queue depth (leading indicator)
scaler.scale_if("queue_depth > 1000", cooldown=120)
```

---

## Reliability Anti-Patterns

### 1. No Circuit Breaker

```python
# Bad
def call_external():
    return requests.post(EXTERNAL_URL, timeout=10).json()

# Good
@circuit_breaker(threshold=5, recovery=60)
def call_external():
    return requests.post(EXTERNAL_URL, timeout=10).json()
```

### 2. Assuming External Uptime

```python
# Bad
response = model_api.generate(prompt)
assistant.reply(response)

# Good
try:
    response = model_api.generate(prompt, timeout=10)
except ModelAPIError:
    logger.warning("Model API unavailable, using cached response")
    response = get_cached_response(prompt)
```

### 3. No Graceful Shutdown

```python
# Bad
def serve():
    app.run(host="0.0.0.0", port=8080)

# Good
def serve():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(SIGTERM, graceful_shutdown)
    app.run(host="0.0.0.0", port=8080)
```

### 4. Missing SLA/SLO Tracking

```python
# Bad
# Launch without operational targets

# Good
SLOs = {
    "latency_p99": 5.0,  # seconds
    "availability": 0.999,
    "error_rate": 0.001
}

class SLOTracker:
    def __init__(self, slos):
        self.slos = slos
        self.budget = self._compute_error_budget()
    
    def evaluate(self, metrics):
        for slo, target in self.slos.items():
            actual = compute_slo(slo, metrics)
            if actual < target:
                self._alert(f"SLO violated: {slo}")
```

---

## Incident Response Anti-Patterns

### 1. No Runbook

```python
# Bad - Diagnose from scratch every time
# How do we fix this again?

# Good
class Runbook:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps
    
    async def execute(self, context):
        for step in self.steps:
            result = await step.run(context)
            if not result.ok:
                return {"failed": step.name, "error": result.error}
        return {"status": "resolved"}

RUNBOOKS = {
    "high_error_rate": Runbook(
        "High Error Rate",
        [
            CheckRecentDeployments(),
            ReviewErrorLogs(),
            SwitchToBackupModel(),
            ScaleUpInstances(+2)
        ]
    )
}
```

### 2. Blaming Humans

```python
# Bad
logger.error(f"User {user_id} caused error")

# Good
logger.error(f"Validation failed for input", user_id=user_id, error_code="VALIDATION_FAILED")
# Focus on process, not person
```

### 3. Skipping Post-Mortems

```python
# Bad
# Fix the bug, move on

# Good
class PostMortem:
    def __init__(self, incident_id):
        self.incident_id = incident_id
    
    def generate(self) -> str:
        return f"""
# Post-Mortem: {self.incident_id}

## Timeline
- {format_time(self.start)} - Detected
- {format_time(self.resolved)} - Resolved

## Root Cause
{self.root_cause}

## Action Items
{self.action_items}
        """
```

### 4. Slow Escalation

```python
# Bad
# PagerDuty waits 30 minutes before escalating

# Good
ESCALATION_POLICY = {
    "P0": {"timeout": 300, "escalate_to": ["engineering-manager", "director"]},
    "P1": {"timeout": 900, "escalate_to": ["senior-engineer"]},
    "P2": {"timeout": 3600, "escalate_to": ["on-call"]}
}

class IncidentEscalator:
    def __init__(self):
        self.active = {}
    
    def start(self, incident_id: str, severity: str, initial_responder: str):
        policy = ESCALATION_POLICY[severity]
        self.active[incident_id] = {
            "severity": severity,
            "responder": initial_responder,
            "deadline": time.time() + policy["timeout"]
        }
```

---

## Configuration Anti-Patterns

### 1. Hardcoded Secrets

```python
# Bad
API_KEY = "sk-1234567890abcdef"

# Good
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ConfigurationError("API_KEY is required")
```

### 2. No Environment Separation

```python
# Bad
DATABASE_URL = "postgresql://prod-db:5432/agent"

# Good
ENV = os.environ.get("ENV", "development")
DATABASE_URL = os.environ.get(f"DATABASE_URL_{ENV.upper()}")
```

### 3. Unversioned Configuration

```python
# Bad
MODEL = "gpt-4"
TEMPERATURE = 0.7

# Good
CONFIG_VERSION = "1.2"
config = load_config(version=CONFIG_VERSION)
```

### 4. Missing Validation

```python
# Bad
config = json.load(file)
TIMEOUT = config["timeout"]

# Good
from pydantic import BaseSettings, validator
class Config(BaseSettings):
    timeout: int = 30
    max_retries: int = 3
    model_name: str
    
    @validator("timeout")
    def valid_timeout(cls, v):
        if v < 1 or v > 300:
            raise ValueError("timeout must be 1-300")
        return v
```

---

## Data Management Anti-Patterns

### 1. No Backup Strategy

```python
# Bad - No backups
# If data is lost, it's gone forever

# Good
BACKUP_SCHEDULE = {
    "database": {"frequency": "6h", "retention": "30d"},
    "logs": {"frequency": "1d", "retention": "90d"},
    "models": {"frequency": "on_change", "retention": "365d"}
}
```

### 2. Ignoring Data Growth

```python
# Bad
query = "SELECT * FROM conversations WHERE session_id = %s"

# Good
query = "SELECT * FROM conversations WHERE session_id = %s AND created_at > %s LIMIT 1000"
```

### 3. No Data Retention Policy

```python
# Bad - Keep everything forever, database grows unbounded

# Good
class RetentionPolicy:
    def __init__(self):
        self.policies = {
            "conversations": timedelta(days=90),
            "logs": timedelta(days=30),
            "metrics": timedelta(days=365)
        }
    
    async def enforce(self):
        for table, ttl in self.policies.items():
            await db.execute(
                f"DELETE FROM {table} WHERE created_at < NOW() - INTERVAL :ttl",
                {"ttl": ttl}
            )
```

---

## Cost Anti-Patterns

### 1. Unbounded Token Usage

```python
# Bad
response = model.generate(prompt)

# Good
tokenizer = get_tokenizer(model_name)
tokens = tokenizer.encode(prompt)
if len(tokens) > MAX_INPUT_TOKENS:
    raise TokenBudgetError(f"Prompt exceeds limit: {len(tokens)}")
```

### 2. Unmonitored spend

```python
# Bad
# Bill arrives as a surprise

# Good
class CostMonitor:
    def __init__(self, daily_budget: float):
        self.daily_budget = daily_budget
        self.spend = 0.0
    
    def check(self, estimated_cost: float):
        if self.spend + estimated_cost > self.daily_budget:
            raise BudgetExceededError(f"Daily budget ${self.daily_budget} exceeded")
        self.spend += estimated_cost
```

### 3. No Cost Attribution

```python
# Bad - All costs lumped together

# Good
@cost_tracker(tenant=user.tenant_id)
async def process_request(request):
    ...
```

---

## Organizational Anti-Patterns

### 1. Single Points of Failure

```python
# Bad - Only one engineer knows the system

# Good
class KnowledgeSharing:
    def __init__(self):
        self.access_matrix = defaultdict(set)
        self.runbook_coverage = 0.0
    
    def ensure_coverage(self, service: str, min_owners: int = 2):
        owners = self.access_matrix[service]
        if len(owners) < min_owners:
            logger.warning(f"Service {service} has {len(owners)} owners, minimum is {min_owners}")
```

### 2. Technical Debt Accumulation

```python
# Bad
# TODO: Remove hack in 6 months
delayed_fix()
# ...6 months pass...

# Good
class TechDebtTracker:
    def __init__(self):
        self.items = []
    
    def register(self, description: str, ticket: str, deadline: str):
        self.items.append({
            "description": description,
            "ticket": ticket,
            "deadline": deadline,
            "status": "open",
            "created_at": datetime.utcnow()
        })
    
    def generate_report(self) -> str:
        return f"Open tech debt items: {len(self.items)}"
```

### 3. Ignoring On-Call Burnout

```python
# Bad - Same person on call every week
on_call_schedule = ["alice", "alice", "alice"]

# Good - Fair rotation
on_call_schedule = ["alice", "bob", "charlie", "alice", "bob", "charlie"]

class OnCallManager:
    def __init__(self):
        self.schedule = []
        self.incident_counts = defaultdict(int)
    
    def assign_shift(self, engineer: str):
        self.schedule.append(engineer)
    
    def track_incident(self, responder: str):
        self.incident_counts[responder] += 1
    
    def is_fair(self) -> bool:
        counts = list(self.incident_counts.values())
        if not counts:
            return True
        return max(counts) - min(counts) <= 2
```

### 4. No Capacity Planning

```python
# Bad
# Upgrade infrastructure only after outage

# Good
class CapacityPlanner:
    def __init__(self):
        self.forecasts = []
    
    def project_growth(self, history: list, days_ahead: int = 90):
        # Linear regression on usage history
        growth_rate = calculate_growth_rate(history)
        projected = history[-1] * (1 + growth_rate * days_ahead / 30)
        recommended = projected * 1.2  # 20% headroom
        return {"projected": projected, "recommended": recommended}
```

---

## Observability Anti-Patterns

### 1. Observability as Afterthought

```python
# Bad - Instrumentation added after incidents

# Good
class ObservabilityByDesign:
    @staticmethod
    def instrument(endpoint_name):
        def decorator(fn):
            @functools.wraps(fn)
            async def wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    result = await fn(*args, **kwargs)
                    record_request(endpoint_name, "success", time.perf_counter() - start)
                    return result
                except Exception as e:
                    record_request(endpoint_name, "error", time.perf_counter() - start)
                    raise
            return wrapper
        return decorator
```

### 2. Spammy Logging

```python
# Bad - Every request logs at DEBUG in prod
logger.debug(f"Request from {ip}")

# Good
LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")
if LOG_LEVEL == "DEBUG":
    logger.debug("Request from %s", ip)
```

### 3. Ignoring Observability Debt

```python
# Bad - Missing metrics for critical paths

# Good
OBSERVABILITY_REQUIREMENTS = {
    "endpoints": ["all"],
    "metrics": ["latency_p99", "error_rate", "throughput"],
    "logs": ["structured_json"],
    "traces": ["sample_rate >= 0.1"]
}
```

---

## Testing Anti-Patterns

### 1. No Chaos Testing

```python
# Bad - Tests pass, production fails

# Good
class ChaosTest:
    async def kill_database(self):
        db_client.kill()
        await self.assert_graceful_degradation()
    
    async def inject_latency(self, service, ms=5000):
        chaos.inject_latency(service, ms)
        await self.assert_retry_behavior()
```

### 2. Flaky Production Tests

```python
# Bad - Pipeline passes with flaky tests
test_pipeline.run(ignore_failures=True)

# Good
test_pipeline.run(strict=True)
flaky_tracker.quarantine("test_e2e_agent_session")
```

### 3. No Disaster Recovery Testing

```python
# Bad
backup.verify_file_exists()

# Good
async def test_backup_restore():
    await backup.restore_to_test()
    count = await test_db.count("conversations")
    assert count > 0
```

---

## Lifecycle Anti-Patterns

### 1. No Deprecation Process

```python
# Bad - Remove endpoint without warning
@app.route("/api/v1/process")
def process():
    return new_implementation()

# Good - Deprecation headers
@app.route("/api/v1/process")
def process():
    response = jsonify(new_implementation())
    response.headers["Sunset"] = "2024-12-31"
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/process>; rel="successor-version"'
    return response
```

### 2. Untracked Dependencies

```python
# Bad - Dependency updates cause silent breakage
pip install --upgrade requests

# Good
REQUIREMENTS = {
    "requests": "==2.31.0",
    "aiohttp": "==3.9.0",
    "pydantic": "==2.5.0"
}
```

### 3. No Vendor Exit Strategy

```python
# Bad
model = OpenAI()  # One vendor, no alternative

# Good
class VendorFailover:
    def __init__(self):
        self.primary = OpenAI()
        self.fallback = Anthropic()
    
    async def complete(self, **kwargs):
        try:
            return await self.primary.complete(**kwargs)
        except Exception:
            logger.warning("Primary failed, using fallback")
            return await self.fallback.complete(**kwargs)
```

---

## Operational Security Anti-Patterns

### 1. No Least Privilege

```python
# Bad
service_account = "admin-full-access"

# Good
service_account = "agent-service-account"
permissions = ["read:conversations", "write:sessions"]
apply_policy(service_account, permissions)
```

### 2. Shared Credentials

```python
# Bad
API_KEY = "team-shared-key"
for user in users:
    user.api_key = API_KEY

# Good
def provision_user(user):
    user.api_key = generate_unique_key()
    vault.store(f"users/{user.id}/api_key", user.api_key)
```

### 3. No Audit Trail

```python
# Bad
@admin.route("/reset")
def reset():
    reset_cache()

# Good
@admin.route("/reset")
@require_auth("admin")
@audit_log(action="cache_reset")
def reset():
    reset_cache()
    return {"status": "reset", "timestamp": datetime.utcnow().isoformat()}
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)