# Integration Domain - Anti-Patterns

## Overview

This document outlines integration anti-patterns to avoid in LLM/agentic systems. Anti-patterns are problematic approaches that lead to security vulnerabilities, reliability issues, and operational complexity.

---

## API Anti-Patterns

### 1. Unversioned APIs

```python
# Bad - No versioning
@app.route("/api/users")
def get_users():
    return jsonify(users)

# Good - Versioned
@app.route("/api/v1/users")
def get_users_v1():
    return jsonify(users_v1)

@app.route("/api/v2/users")
def get_users_v2():
    return jsonify(users_v2)
```

### 2. No Rate Limiting

```python
# Bad - Unlimited access
@app.route("/api/generate")
def generate():
    return llm.generate(request.json["prompt"])

# Good - Rate limited
@app.route("/api/generate")
@limiter.limit("60/minute")
def generate():
    return llm.generate(request.json["prompt"])
```

### 3. Exposing Internal Errors

```python
# Bad - Leaking internals
@app.route("/api/data")
def get_data():
    try:
        return db.query("SELECT * FROM data")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Good - Safe errors
@app.route("/api/data")
def get_data():
    try:
        return db.query("SELECT * FROM data")
    except Exception:
        logger.error("Database error occurred")
        return jsonify({"error": "Service unavailable"}), 500
```

### 4. Tight Coupling to External APIs

```python
# Bad - Direct coupling
class AgentService:
    def __init__(self):
        self.model = OpenAI(api_key="sk-...")
    
    def process(self, prompt):
        return self.model.generate(prompt)

# Good - Interface-based
class ModelClient(Protocol):
    def generate(self, prompt: str) -> str: ...

class AgentService:
    def __init__(self, model: ModelClient):
        self.model = model
    
    def process(self, prompt):
        return self.model.generate(prompt)
```

### 5. No Request Validation

```python
# Bad - Trusting all inputs
@app.route("/api/process", methods=["POST"])
def process():
    data = request.json
    return agent.run(data["prompt"])

# Good - Validate inputs
@app.route("/api/process", methods=["POST"])
def process():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing prompt"}), 400
    if len(data["prompt"]) > 10000:
        return jsonify({"error": "Prompt too long"}), 400
    return agent.run(data["prompt"])
```

---

## Webhook Anti-Patterns

### 1. Fire-and-Forget Webhooks

```python
# Bad - No reliability
def send_webhook(url, data):
    requests.post(url, json=data)

# Good - With retry
async def send_webhook(url, data, max_retries=3):
    for i in range(max_retries):
        try:
            resp = await aiohttp.post(url, json=data)
            if resp.status < 300:
                return True
        except:
            if i == max_retries - 1:
                raise
            await asyncio.sleep(2 ** i)
```

### 2. No Signature Verification

```python
# Bad - Trusting all requests
@app.route("/webhook", methods=["POST"])
def webhook():
    return process_webhook(request.json)

# Good - Verify signature
@app.route("/webhook", methods=["POST"])
def webhook():
    sig = request.headers.get("X-Hub-Signature")
    if not verify_signature(request.data, sig):
        return "Unauthorized", 401
    return process_webhook(request.json)
```

### 3. Synchronous Webhook Processing

```python
# Bad - Blocking webhook handler
@app.route("/webhook", methods=["POST"])
def webhook():
    process_webhook_synchronously(request.json)  # May timeout
    return "OK"

# Good - Async processing
@app.route("/webhook", methods=["POST"])
async def webhook():
    asyncio.create_task(process_webhook_async(request.json))
    return "Accepted", 202
```

### 4. No Duplicate Detection

```python
# Bad - Process duplicates
@app.route("/webhook", methods=["POST"])
def webhook():
    process_event(request.json)  # Could process same event twice
    return "OK"

# Good - Idempotent handling
processed_events = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    event_id = request.json.get("id")
    if event_id in processed_events:
        return "Already processed", 200
    process_event(request.json)
    processed_events.add(event_id)
    return "OK"
```

---

## Streaming Anti-Patterns

### 1. No Backpressure Handling

```python
# Bad - Unbounded output
async def stream_response(prompt):
    while True:
        chunk = await model.generate_stream(prompt)
        yield chunk

# Good - With backpressure
async def stream_response(prompt, max_queue=100):
    queue = asyncio.Queue(maxsize=max_queue)
    
    async def producer():
        async for chunk in model.generate_stream(prompt):
            await queue.put(chunk)
        await queue.put(None)
    
    async def consumer():
        async for chunk in producer():
            yield chunk
```

### 2. Ignoring Connection Failures

```python
# Bad - No error handling
async def stream_to_client(websocket):
    async for chunk in generate_stream():
        await websocket.send(chunk)

# Good - Handle disconnects
async def stream_to_client(websocket):
    try:
        async for chunk in generate_stream():
            if websocket.closed:
                break
            await websocket.send(chunk)
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
```

---

## Authentication Anti-Patterns

### 1. Hardcoded Credentials

```python
# Bad - Credentials in code
API_KEY = "sk-proj-1234567890abcdef"

# Good - Environment-based
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise ConfigurationError("OPENAI_API_KEY not configured")
```

### 2. No Token Refresh

```python
# Bad - Token never refreshes
def get_headers():
    return {"Authorization": f"Bearer {token}"}

# Good - Automatic refresh
class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = 0
    
    async def get_token(self) -> str:
        if time.time() > self.expires_at - 60:
            await self._refresh()
        return self.token
```

---

## Data Format Anti-Patterns

### 1. Inconsistent Response Formats

```python
# Bad - Different formats
@app.route("/api/user")
def get_user():
    return {"user": user_data}

@app.route("/api/order")
def get_order():
    return {"order": order_data}

# Good - Consistent envelope
def format_response(data: Dict, meta: Dict = None) -> Dict:
    return {
        "data": data,
        "meta": meta or {},
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## Data Format Anti-Patterns

### 1. Inconsistent Response Formats

```python
# Bad - Different formats
@app.route("/api/user")
def get_user():
    return {"user": user_data}

@app.route("/api/order")
def get_order():
    return {"order": order_data}

# Good - Consistent envelope
def format_response(data: Dict, meta: Dict = None) -> Dict:
    return {
        "data": data,
        "meta": meta or {},
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## Error Handling Anti-Patterns

### 1. Silent Failures

```python
# Bad - Swallowing errors
async def process_webhook(data):
    try:
        await handle(data)
    except Exception:
        pass

# Good - Log and report
async def process_webhook(data):
    try:
        await handle(data)
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}", exc_info=True)
        await metrics.increment("webhook.errors")
        raise
```

### 2. Generic Error Messages

```python
# Bad - Unhelpful errors
except Exception as e:
    return {"error": str(e)}, 500

# Good - Structured errors with codes
except ValidationError as e:
    return {
        "error": {
            "code": "validation_error",
            "message": "Invalid request parameters",
            "fields": e.errors()
        }
    }, 422
```

### 3. No Timeout Configuration

```python
# Bad - Infinite wait
response = requests.get("https://api.example.com/data")

# Good - With timeout and retry
try:
    response = requests.get(
        "https://api.example.com/data",
        timeout=(5, 30)  # (connect, read)
    )
except Timeout:
    logger.error("Request timeout")
```

---

## Security Anti-Patterns

### 1. Exposed Internal Endpoints

```python
# Bad - Internal service public
@app.route("/internal/admin/reset")
def internal_reset():
    reset_cache()

# Good - Protected with mTLS/network policy
@app.route("/internal/admin/reset")
@require_internal_auth
def internal_reset():
    reset_cache()
```

### 2. Insufficient CORS

```python
# Bad - Allow all origins
CORS(app, origins="*")

# Good - Restrict origins
CORS(app, origins=[
    "https://app.example.com",
    "https://admin.example.com"
])
```

### 3. Logging Sensitive Data

```python
# Bad - Logging secrets
logger.info(f"Request headers: {request.headers}")

# Good - Redact sensitive fields
safe_headers = {k: v for k, v in request.headers.items()
                if k.lower() not in ["authorization", "x-api-key"]}
logger.info(f"Request headers: {safe_headers}")
```

### 4. Weak Webhook Validation

```python
# Bad - Accepting any POST
@app.route("/webhook", methods=["POST"])
def webhook():
    return process(request.json)

# Good - Validate signature and IP
@app.route("/webhook", methods=["POST"])
def webhook():
    if not verify_signature(request.data, request.headers):
        return "Unauthorized", 401
    if not is_trusted_ip(request.remote_addr):
        return "Forbidden", 403
    return process(request.json)
```

---

## Resilience Anti-Patterns

### 1. No Circuit Breaker

```python
# Bad - Blind retries
async def call_external_api():
    for attempt in range(10):
        await external_api.call()

# Good - Circuit breaker pattern
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def call_external_api():
    return await external_api.call()
```

### 2. Unbounded Resource Usage

```python
# Bad - Unbounded queue
queue = asyncio.Queue()

# Good - Bounded queue with backpressure
queue = asyncio.Queue(maxsize=1000)

async def produce():
    try:
        await queue.put(item)
    except asyncio.QueueFull:
        logger.warning("Queue full, applying backpressure")
        await asyncio.sleep(0.1)
```

### 3. Cascading Failures

```python
# Bad - No bulkhead
async def process_request(request):
    result1 = await service_a.call()
    result2 = await service_b.call()
    result3 = await service_c.call()

# Good - Bulkhead isolation
async def process_request(request):
    async with asyncio.TaskGroup() as tg:
        task_a = tg.create_task(service_a.call())
        task_b = tg.create_task(service_b.call())
        task_c = tg.create_task(service_c.call())
    return combine(task_a.result(), task_b.result(), task_c.result())
```

### 4. No Graceful Degradation

```python
# Bad - Hard failure on service outage
async def get_recommendations(user_id):
    recs = await recommendation_service.get(user_id)
    return recs

# Good - Fallback to defaults
async def get_recommendations(user_id):
    try:
        recs = await recommendation_service.get(user_id)
        return recs
    except ServiceUnavailable:
        logger.warning("Rec service down, using defaults")
        return get_default_recommendations()
```

---

## Data Consistency Anti-Patterns

### 1. No Idempotency

```python
# Bad - Duplicates on retry
@app.route("/payment", methods=["POST"])
def process_payment():
    charge(data)
    return {"status": "charged"}

# Good - Idempotency keys
processed = set()

@app.route("/payment", methods=["POST"])
def process_payment():
    idempotency_key = request.headers.get("Idempotency-Key")
    if idempotency_key in processed:
        return {"status": "already_processed"}
    charge(data)
    processed.add(idempotency_key)
    return {"status": "charged"}
```

### 2. Stale Data Propagation

```python
# Bad - No cache invalidation
cache.set("user:123", user_data)

# Good - TTL and explicit invalidation
cache.set("user:123", user_data, ttl=300)

async def update_user(user_id, data):
    await db.update(user_id, data)
    await cache.delete(f"user:{user_id}")
```

### 3. Missing Transaction Boundaries

```python
# Bad - Partial updates
async def create_session(data):
    session = await db.create_session(data)
    await cache.set(f"session:{session.id}", session)
    await emit_event("session.created", session)
    # If emit fails, cache has stale data

# Good - Compensating transactions
async def create_session(data):
    try:
        session = await db.create_session(data)
        await cache.set(f"session:{session.id}", session)
        await emit_event("session.created", session)
    except Exception as e:
        await compensate_create_session(session.id)
        raise
```

---

## Monitoring Anti-Patterns

### 1. Logging Without Context

```python
# Bad - No traceability
logger.info("Processing request")

# Good - Structured logging with context
logger.info(
    "Processing request",
    extra={
        "trace_id": trace_id,
        "session_id": session_id,
        "endpoint": request.path
    }
)
```

### 2. No Health Check Implementation

```python
# Bad - No health endpoint
# Users blindly hitting failing service

# Good - Comprehensive health checks
@app.get("/health")
async def health():
    checks = await run_health_checks()
    status = "healthy" if all(checks.values()) else "degraded"
    return {"status": status, "checks": checks}
```

### 3. Ignoring Metrics

```python
# Bad - No observability
async def process(data):
    return await agent.run(data)

# Good - Instrumented
@timed("process.duration")
@counter("process.count")
async def process(data):
    return await agent.run(data)
```

---

## Deployment Anti-Patterns

### 1. No Feature Flags

```python
# Bad - Hardcoded behavior
@app.route("/api/v2/chat")
def chat_v2():
    return new_chat_engine().run()

# Good - Feature-flagged rollout
@app.route("/api/v2/chat")
def chat_v2():
    if feature_flags.is_enabled("chat_v2", request.user):
        return new_chat_engine().run()
    return legacy_chat_engine().run()
```

### 2. Monolithic Configuration

```python
# Bad - Scattered configs
MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
REDIS_URL = "redis://localhost:6379"

# Good - Centralized, typed configuration
class Settings(BaseSettings):
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    redis_url: str

settings = Settings()
```

### 3. No Canary Deployment

```python
# Bad - Big bang deploy
# All traffic hits new version immediately

# Good - Canary with traffic splitting
@app.route("/api/v1/process")
async def process():
    if traffic_splitter.is_canary(percentage=10):
        return await new_version_handler()
    return await stable_version_handler()
```

---

## Vendor & Third-Party Anti-Patterns

### 1. No Abstraction Layer

```python
# Bad - Direct vendor SDK usage throughout codebase
@app.route("/api/process")
def process():
    return openai.Completion.create(...).choices[0].text

# Good - Adapter pattern
class LLMAdapter(Protocol):
    async def complete(self, prompt: str, **kwargs) -> str:
        ...

class OpenAIAdapter:
    async def complete(self, prompt: str, **kwargs):
        return openai.Completion.create(prompt=prompt, **kwargs).choices[0].text

@app.route("/api/process")
def process():
    return llm_adapter.complete(request.json["prompt"])
```

### 2. Ignoring Breaking Changes

```python
# Bad - No version pinning
openai = OpenAI()

# Good - Pin version and track changelog
openai = OpenAI(version="1.0.0")
MONITORED_APIS = {
    "openai": {"current_version": "1.0.0", "breaking_versions": ["2.0.0"]}
}
```

### 3. Vendor Outage Blindness

```python
# Bad - No fallback
@app.route("/process")
def process():
    return openai.process(request.json["prompt"])

# Good - Timeout, fallback, health check
@app.route("/process")
def process():
    try:
        return asyncio.wait_for(
            openai.process(request.json["prompt"]),
            timeout=10
        )
    except TimeoutError:
        return fallback_service.process(request.json["prompt"])
```

---

## Data Integrity Anti-Patterns

### 1. No Event Ordering Guarantees

```python
# Bad - Concurrent processing breaks ordering
async def process_events(events):
    await asyncio.gather(*[handle(e) for e in events])

# Good - Sequence-based ordering
async def process_events(events):
    sorted_events = sorted(events, key=lambda e: e["sequence"])
    for event in sorted_events:
        await handle(event)
```

### 2. Missing Idempotency Keys

```python
# Bad - Duplicates on retry
@app.route("/webhooks/payment", methods=["POST"])
def payment_webhook():
    charge_customer(request.json)
    return "OK"
```

### 3. Inconsistent State Across Services

```python
# Bad - Partial updates
await db.update_user(user_id, data)
await cache.update_user(user_id, data)
await notifications.send(user_id, "Profile updated")
# If step 3 fails, notification is missed

# Good - Saga pattern with compensation
class SagaOrchestrator:
    async def execute(self, steps):
        executed = []
        try:
            for step in steps:
                await step.execute()
                executed.append(step)
        except Exception as e:
            for step in reversed(executed):
                await step.compensate()
            raise
```

---

## Configuration Management Anti-Patterns

### 1. Hardcoded Endpoints

```python
# Bad - URLs everywhere
url = "https://api.openai.com/v1/chat/completions"

# Good - Centralized configuration
class IntegrationConfig(BaseSettings):
    openai_url: str = "https://api.openai.com/v1"
    openai_api_key: str
    timeout: int = 30
    retries: int = 3

config = IntegrationConfig()
url = f"{config.openai_url}/chat/completions"
```

### 2. No Environment Separation

```python
# Bad
DATABASE_URL = "postgresql://prod-db:5432/db"

# Good
ENV = os.environ.get("ENV", "dev")
DATABASE_URL = os.environ.get(f"DATABASE_URL_{ENV.upper()}")
```

### 3. Missing Defaults

```python
# Bad
API_TIMEOUT = int(os.environ.get("API_TIMEOUT"))

# Good
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "30"))
```

---

## Testing Anti-Patterns

### 1. No Integration Tests

```python
# Bad - Only unit tests
def test_process():
    agent = MockAgent()
    result = agent.process("test")
    assert result == "mocked"

# Good - Integration test against real service
@pytest.mark.integration
async def test_process_with_real_api():
    agent = RealAgent(api_key=TEST_API_KEY)
    result = await agent.process("test", session_id="test-123")
    assert result is not None
    assert isinstance(result, str)
```

### 2. Flaky Tests

```python
# Bad - Non-deterministic
def test_rate_limit():
    result = api.call()  # May fail during peak hours
    assert result.status == 200

# Good - Controlled, repeatable
def test_rate_limit():
    with mock_rate_limit(requests_per_minute=0):
        result = api.call()
        assert result.status == 429
```

---

## API Design Anti-Patterns

### 1. Chatty APIs

```python
# Bad - Multiple round trips
user = api.get_user(id)
addresses = api.get_addresses(user.id)
orders = api.get_orders(user.id)
payments = api.get_payments(user.id)

# Good - Single API call with projection7
profile = api.get_user_profile(id, include=["addresses", "orders", "payments"])
```

### 2. No Schema Documentation

```python
# Bad - No OpenAPI
@app.route("/api/process", methods=["POST"])
def process():
    return agent.run(request.json)

# Good - Auto-documented
class ProcessRequest(BaseModel):
    prompt: str = Field(..., description="User prompt", max_length=10000)
    session_id: str = Field(..., description="Session identifier")

@app.route("/api/process", methods=["POST"])
def process(request: ProcessRequest):
    return agent.run(request.prompt)
```

### 3. Blocking I/O in Async Context

```python
# Bad - Blocking async handlers
@app.route("/api/process", methods=["POST"])
async def process():
    result = requests.post(REMOTE_URL, json=request.json).json()
    return jsonify(result)

# Good - Async HTTP client
@app.route("/api/process", methods=["POST"])
async def process():
    async with aiohttp.ClientSession() as client:
        async with client.post(REMOTE_URL, json=request.json) as resp:
            result = await resp.json()
    return jsonify(result)
```

---

## Observability Anti-Patterns

### 1. Logging Without Structure

```python
# Bad - Unstructured logs
logger.info("Processing request " + str(request))

# Good - Structured JSON
logger.info("Processing request", extra={
    "endpoint": request.path,
    "method": request.method,
    "trace_id": trace_id,
    "user_agent": request.headers.get("User-Agent")
})
```

### 2. No Alerting Rules

```python
# Bad - Dashboards without alerts
# Nobody knows when things break

# Good - Proactive alerting
ALERTS = {
    "high_latency": {
        "condition": "p99_latency > 1s",
        "duration": "5m",
        "severity": "warning"
    },
    "error_rate": {
        "condition": "error_rate > 0.01",
        "duration": "2m",
        "severity": "critical"
    }
}
```

### 3. Missing Correlation IDs

```python
# Bad - Cannot trace requests across services
async def process(data):
    result = await service_a.call(data)
    return result

# Good - Propagate trace context
async def process(data):
    trace_id = request.headers.get("X-Trace-Id", generate_trace_id())
    async with tracer.start_span("process", trace_id=trace_id):
        result = await service_a.call(data, trace_id=trace_id)
    return result
```

---

## Maintenance Anti-Patterns

### 1. Untested Upgrades

```python
# Bad - Upgrade without testing
pip install --upgrade openai

# Good - Pinned versions with test suite
REQUIREMENTS = """
openai==1.0.0
aiohttp==3.9.0
pydantic==2.0.0
"""

# CI pipeline runs tests on all dependency updates
```

### 2. No Deprecation Policy

```python
# Bad - Breaking changes without notice
@app.route("/api/v1/process")
def process_v1():
    return {"result": new_format}  # Changed from old format

# Good - Versioned with deprecation warnings
DEPRECATIONS = {
    "/api/v1/process": {"sunset": "2024-12-31", "replacement": "/api/v2/process"}
}

@app.route("/api/v1/process")
def process_v1():
    response = jsonify({"result": new_format})
    response.headers["Sunset"] = DEPRECATIONS["/api/v1/process"]["sunset"]
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/process>; rel="successor-version"'
    return response
```

### 3. Accumulated Technical Debt

```python
# Bad - Temporary workarounds that become permanent
if service == "legacy":
    # TODO: Remove after migration
    result = await legacy_processor(data)
else:
    result = await modern_processor(data)

# Good - Track tech debt
TODO_TRACKING = [
    {
        "description": "Remove legacy processor fallback",
        "ticket": "PROJ-1234",
        "deadline": "2024-06-30",
        "code_location": "processor.py:45"
    }
]
```

---

## Observability Anti-Patterns

### 1. Logging Without Structure

```python
# Bad - Unstructured logs
logger.info("Processing request " + str(request))

# Good - Structured JSON
logger.info("Processing request", extra={
    "endpoint": request.path,
    "method": request.method,
    "trace_id": trace_id,
    "user_agent": request.headers.get("User-Agent")
})
```

### 2. No Alerting Rules

```python
# Bad - Dashboards without alerts
# Nobody knows when things break

# Good - Proactive alerting
ALERTS = {
    "high_latency": {
        "condition": "p99_latency > 1s",
        "duration": "5m",
        "severity": "warning"
    },
    "error_rate": {
        "condition": "error_rate > 0.01",
        "duration": "2m",
        "severity": "critical"
    }
}
```

### 3. Missing Correlation IDs

```python
# Bad - Cannot trace requests across services
async def process(data):
    result = await service_a.call(data)
    return result

# Good - Propagate trace context
async def process(data):
    trace_id = request.headers.get("X-Trace-Id", generate_trace_id())
    async with tracer.start_span("process", trace_id=trace_id):
        result = await service_a.call(data, trace_id=trace_id)
    return result
```

---

## Maintenance Anti-Patterns

### 1. Untested Upgrades

```python
# Bad - Upgrade without testing
pip install --upgrade openai

# Good - Pinned versions with test suite
REQUIREMENTS = """
openai==1.0.0
aiohttp==3.9.0
pydantic==2.0.0
"""

# CI pipeline runs tests on all dependency updates
```

### 2. No Deprecation Policy

```python
# Bad - Breaking changes without notice
@app.route("/api/v1/process")
def process_v1():
    return {"result": new_format}  # Changed from old format

# Good - Versioned with deprecation warnings
DEPRECATIONS = {
    "/api/v1/process": {"sunset": "2024-12-31", "replacement": "/api/v2/process"}
}

@app.route("/api/v1/process")
def process_v1():
    response = jsonify({"result": new_format})
    response.headers["Sunset"] = DEPRECATIONS["/api/v1/process"]["sunset"]
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/process>; rel="successor-version"'
    return response
```

### 3. Accumulated Technical Debt

```python
# Bad - Temporary workarounds that become permanent
if service == "legacy":
    # TODO: Remove after migration
    result = await legacy_processor(data)
else:
    result = await modern_processor(data)

# Good - Track tech debt
TODO_TRACKING = [
    {
        "description": "Remove legacy processor fallback",
        "ticket": "PROJ-1234",
        "deadline": "2024-06-30",
        "code_location": "processor.py:45"
    }
]
```

---

## Error Handling Anti-Patterns

### 1. Silent Failures

```python
# Bad - Swallowing errors
async def process_webhook(data):
    try:
        await handle(data)
    except Exception:
        pass

# Good - Log and report
async def process_webhook(data):
    try:
        await handle(data)
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}", exc_info=True)
        await metrics.increment("webhook.errors")
        raise
```

### 2. Generic Error Messages

```python
# Bad - Unhelpful errors
except Exception as e:
    return {"error": str(e)}, 500

# Good - Structured errors with codes
except ValidationError as e:
    return {
        "error": {
            "code": "validation_error",
            "message": "Invalid request parameters",
            "fields": e.errors()
        }
    }, 422
```

### 3. No Timeout Configuration

```python
# Bad - Infinite wait
response = requests.get("https://api.example.com/data")

# Good - With timeout and retry
try:
    response = requests.get(
        "https://api.example.com/data",
        timeout=(5, 30)  # (connect, read)
    )
except Timeout:
    logger.error("Request timeout")
```

---

## Security Anti-Patterns

### 1. Exposed Internal Endpoints

```python
# Bad - Internal service public
@app.route("/internal/admin/reset")
def internal_reset():
    reset_cache()

# Good - Protected with mTLS/network policy
@app.route("/internal/admin/reset")
@require_internal_auth
def internal_reset():
    reset_cache()
```

### 2. Insufficient CORS

```python
# Bad - Allow all origins
CORS(app, origins="*")

# Good - Restrict origins
CORS(app, origins=[
    "https://app.example.com",
    "https://admin.example.com"
])
```

### 3. Logging Sensitive Data

```python
# Bad - Logging secrets
logger.info(f"Request headers: {request.headers}")

# Good - Redact sensitive fields
safe_headers = {k: v for k, v in request.headers.items()
                if k.lower() not in ["authorization", "x-api-key"]}
logger.info(f"Request headers: {safe_headers}")
```

### 4. Weak Webhook Validation

```python
# Bad - Accepting any POST
@app.route("/webhook", methods=["POST"])
def webhook():
    return process(request.json)

# Good - Validate signature and IP
@app.route("/webhook", methods=["POST"])
def webhook():
    if not verify_signature(request.data, request.headers):
        return "Unauthorized", 401
    if not is_trusted_ip(request.remote_addr):
        return "Forbidden", 403
    return process(request.json)
```

---

## Resilience Anti-Patterns

### 1. No Circuit Breaker

```python
# Bad - Blind retries
async def call_external_api():
    for attempt in range(10):
        await external_api.call()

# Good - Circuit breaker pattern
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def call_external_api():
    return await external_api.call()
```

### 2. Unbounded Resource Usage

```python
# Bad - Unbounded queue
queue = asyncio.Queue()

# Good - Bounded queue with backpressure
queue = asyncio.Queue(maxsize=1000)

async def produce():
    try:
        await queue.put(item)
    except asyncio.QueueFull:
        logger.warning("Queue full, applying backpressure")
        await asyncio.sleep(0.1)
```

### 3. Cascading Failures

```python
# Bad - No bulkhead
async def process_request(request):
    result1 = await service_a.call()
    result2 = await service_b.call()
    result3 = await service_c.call()

# Good - Bulkhead isolation
async def process_request(request):
    async with asyncio.TaskGroup() as tg:
        task_a = tg.create_task(service_a.call())
        task_b = tg.create_task(service_b.call())
        task_c = tg.create_task(service_c.call())
    return combine(task_a.result(), task_b.result(), task_c.result())
```

### 4. No Graceful Degradation

```python
# Bad - Hard failure on service outage
async def get_recommendations(user_id):
    recs = await recommendation_service.get(user_id)
    return recs

# Good - Fallback to defaults
async def get_recommendations(user_id):
    try:
        recs = await recommendation_service.get(user_id)
        return recs
    except ServiceUnavailable:
        logger.warning("Rec service down, using defaults")
        return get_default_recommendations()
```

---

## Data Consistency Anti-Patterns

### 1. No Idempotency

```python
# Bad - Duplicates on retry
@app.route("/payment", methods=["POST"])
def process_payment():
    charge(data)
    return {"status": "charged"}

# Good - Idempotency keys
processed = set()

@app.route("/payment", methods=["POST"])
def process_payment():
    idempotency_key = request.headers.get("Idempotency-Key")
    if idempotency_key in processed:
        return {"status": "already_processed"}
    charge(data)
    processed.add(idempotency_key)
    return {"status": "charged"}
```

### 2. Stale Data Propagation

```python
# Bad - No cache invalidation
cache.set("user:123", user_data)

# Good - TTL and explicit invalidation
cache.set("user:123", user_data, ttl=300)

async def update_user(user_id, data):
    await db.update(user_id, data)
    await cache.delete(f"user:{user_id}")
```

### 3. Missing Transaction Boundaries

```python
# Bad - Partial updates
async def create_session(data):
    session = await db.create_session(data)
    await cache.set(f"session:{session.id}", session)
    await emit_event("session.created", session)
    # If emit fails, cache has stale data

# Good - Compensating transactions
async def create_session(data):
    try:
        session = await db.create_session(data)
        await cache.set(f"session:{session.id}", session)
        await emit_event("session.created", session)
    except Exception as e:
        await compensate_create_session(session.id)
        raise
```

---

## Monitoring Anti-Patterns

### 1. Logging Without Context

```python
# Bad - No traceability
logger.info("Processing request")

# Good - Structured logging with context
logger.info(
    "Processing request",
    extra={
        "trace_id": trace_id,
        "session_id": session_id,
        "endpoint": request.path
    }
)
```

### 2. No Health Check Implementation

```python
# Bad - No health endpoint
# Users blindly hitting failing service

# Good - Comprehensive health checks
@app.get("/health")
async def health():
    checks = await run_health_checks()
    status = "healthy" if all(checks.values()) else "degraded"
    return {"status": status, "checks": checks}
```

### 3. Ignoring Metrics

```python
# Bad - No observability
async def process(data):
    return await agent.run(data)

# Good - Instrumented
@timed("process.duration")
@counter("process.count")
async def process(data):
    return await agent.run(data)
```

---

## Deployment Anti-Patterns

### 1. No Feature Flags

```python
# Bad - Hardcoded behavior
@app.route("/api/v2/chat")
def chat_v2():
    return new_chat_engine().run()

# Good - Feature-flagged rollout
@app.route("/api/v2/chat")
def chat_v2():
    if feature_flags.is_enabled("chat_v2", request.user):
        return new_chat_engine().run()
    return legacy_chat_engine().run()
```

### 2. Monolithic Configuration

```python
# Bad - Scattered configs
MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
REDIS_URL = "redis://localhost:6379"

# Good - Centralized, typed configuration
class Settings(BaseSettings):
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    redis_url: str

settings = Settings()
```

### 3. No Canary Deployment

```python
# Bad - Big bang deploy
# All traffic hits new version immediately

# Good - Canary with traffic splitting
@app.route("/api/v1/process")
async def process():
    if traffic_splitter.is_canary(percentage=10):
        return await new_version_handler()
    return await stable_version_handler()
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)