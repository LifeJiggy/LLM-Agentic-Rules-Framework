# Integration Domain - Best Practices

## Overview

This document outlines integration best practices for LLM/agentic systems, covering API design, webhook patterns, streaming, security, reliability, and operational excellence.

---

## Table of Contents

1. [RESTful Endpoint Design](#1-restful-endpoint-design)
2. [Versioning Strategy](#2-versioning-strategy)
3. [Webhook Best Practices](#3-webhook-best-practices)
4. [Reliable Delivery](#4-reliable-delivery)
5. [Streaming Integration](#5-streaming-integration)
6. [Security Best Practices](#6-security-best-practices)
7. [Rate Limiting](#7-rate-limiting)
8. [Circuit Breaker Pattern](#8-circuit-breaker-pattern)
9. [Caching at Integration Layer](#9-caching-at-integration-layer)
10. [Monitoring Integration Health](#10-monitoring-integration-health)

---

## 1. RESTful Endpoint Design

```python
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, validator
import asyncio

app = Flask(__name__)

class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    session_id: str = Field(..., min_length=32)
    max_tokens: int = Field(default=4096, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0, le=2)
    
    @validator("session_id")
    def validate_session(cls, v):
        if not v.isalnum():
            raise ValueError("Session ID must be alphanumeric")
        return v

@app.route("/api/v1/agent/process", methods=["POST"])
async def process_agent_request():
    try:
        req = AgentRequest(**request.json)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    result = await agent.process(req.prompt, req.session_id)
    return jsonify({"result": result})
```

### Pagination Standards

```python
class PaginatedResponse(BaseModel):
    data: List[Dict]
    total: int
    page: int
    page_size: int
    has_more: bool

def paginate_query(query, page: int = 1, page_size: int = 20):
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        data=[item.to_dict() for item in items],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < total
    )
```

---

## 2. Versioning Strategy

```python
class APIRouter:
    """Route requests to appropriate API version."""
    
    def __init__(self):
        self.versions = {}
    
    def register_version(self, version: str, routes: Dict):
        self.versions[version] = routes
    
    def route(self, request):
        version = request.headers.get("API-Version", "v1")
        routes = self.versions.get(version)
        
        if not routes:
            return {"error": "API version not supported"}, 400
        
        handler = routes.get(request.path)
        if not handler:
            return {"error": "Endpoint not found"}, 404
        
        return handler(request)
```

### Deprecation Handling

```python
class DeprecationManager:
    def __init__(self):
        self.deprecated_routes = {}
    
    def deprecate(self, path: str, version: str, sunset_date: str):
        self.deprecated_routes[path] = {
            "version": version,
            "sunset": sunset_date,
            "message": f"This endpoint is deprecated. Migrate to version {version}"
        }
    
    def check_deprecation(self, path: str, request_headers: Dict):
        if path in self.deprecated_routes:
            deprecation = self.deprecated_routes[path]
            return {
                "header": "Sunset",
                "value": deprecation["sunset"],
                "warning": deprecation["message"]
            }
        return None
```

---

## 3. Webhook Best Practices

### Reliable Delivery

```python
import asyncio
import aiohttp
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class WebhookDelivery:
    url: str
    payload: Dict[str, Any]
    attempt: int
    max_attempts: int = 3
    timeout: int = 30

class WebhookSender:
    """Send webhooks with reliability and security."""
    
    def __init__(self, secret: str):
        self.secret = secret
        self.delivery_log = []
    
    async def send(self, url: str, event: str, data: Any) -> bool:
        payload = {"event": event, "data": data, "timestamp": time.time()}
        
        for attempt in range(3):
            try:
                signature = self._sign_payload(payload)
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        json=payload,
                        headers={"X-Hub-Signature-256": signature},
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        if resp.status < 300:
                            self.delivery_log.append({"url": url, "status": "success"})
                            return True
            except Exception as e:
                self.delivery_log.append({"url": url, "status": "failed", "error": str(e)})
                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)
        
        return False
    
    def _sign_payload(self, payload: Dict) -> str:
        import hmac
        import hashlib
        signature = hmac.new(
            self.secret.encode(),
            json.dumps(payload).encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"
```

### Idempotent Webhooks

```python
class IdempotentWebhookHandler:
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    async def handle(self, delivery_id: str, payload: Dict) -> Dict:
        existing = await self.storage.get(f"webhook:{delivery_id}")
        if existing:
            return {"status": "already_processed", "original_result": existing}
        
        result = await self._process(payload)
        await self.storage.set(f"webhook:{delivery_id}", result, ttl=86400)
        return result
```

---

## 4. Reliable Delivery

### Retry with Exponential Backoff

```python
class RetryPolicy:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
    
    def get_delay(self, attempt: int) -> float:
        return self.base_delay * (2 ** attempt)
    
    def should_retry(self, attempt: int, error: Exception) -> bool:
        if attempt >= self.max_attempts:
            return False
        return isinstance(error, (TimeoutError, ConnectionError))
```

### Dead Letter Queue

```python
class DeadLetterQueue:
    def __init__(self, queue_client):
        self.queue = queue_client
    
    async def enqueue(self, message: Dict, reason: str):
        await self.queue.send({
            "original_message": message,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
            "retry_count": message.get("retry_count", 0)
        })
```

---

## 5. Streaming Integration

### Server-Sent Events

```python
from flask import Response, stream_with_context
import json

@app.route("/api/v1/agent/stream")
def stream_agent_response():
    prompt = request.args.get("prompt", "")
    
    def generate():
        async for chunk in agent.stream_response(prompt):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )
```

### WebSocket Integration

```python
import websockets

class WebSocketHandler:
    def __init__(self):
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
    
    async def register(self, websocket):
        self.connections.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.connections.remove(websocket)
    
    async def broadcast(self, message: str):
        if self.connections:
            await asyncio.gather(
                *[ws.send(message) for ws in self.connections],
                return_exceptions=True
            )
```

---

## 6. Security Best Practices

### Authentication

```python
import jwt
from datetime import datetime, timedelta

def require_api_key(f):
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key or not validate_api_key(api_key):
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated

def validate_api_key(key: str) -> bool:
    try:
        decoded = jwt.decode(key, SECRET_KEY, algorithms=["HS256"])
        return decoded["exp"] > time.time()
    except Exception:
        return False
```

### Input Validation

```python
from pydantic import BaseModel, validator

class IntegrationInput(BaseModel):
    data: str = Field(..., max_length=50000)
    
    @validator("data")
    def validate_prompt(cls, v):
        if len(v) > 50000:
            raise ValueError("Input exceeds maximum length")
        return v.strip()
```

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://example.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 7. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/v1/agent/process", methods=["POST"])
@limiter.limit("10 per minute")
async def process():
    return await agent.process(request.json)
```

### Adaptive Rate Limiting

```python
class AdaptiveRateLimiter:
    def __init__(self):
        self.limits: Dict[str, Dict] = {}
    
    def adjust_limit(self, client_id: str, current_usage: int, error_rate: float):
        if error_rate > 0.1:
            self.limits[client_id] = {"rate": 10, "per": "minute"}
        elif current_usage < self.limits[client_id]["rate"] * 0.5:
            self.limits[client_id] = {"rate": self.limits[client_id]["rate"] * 1.2, "per": "minute"}
```

---

## 8. Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time: float = 0
        self.state = "CLOSED"
    
    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise ServiceUnavailable("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failures = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
```

---

## 9. Caching at Integration Layer

```python
class IntegrationCache:
    def __init__(self, cache_client, default_ttl: int = 300):
        self.cache = cache_client
        self.default_ttl = default_ttl
    
    async def get_or_fetch(self, key: str, fetch_fn: Callable) -> Any:
        cached = await self.cache.get(key)
        if cached is not None:
            return json.loads(cached)
        
        result = await fetch_fn()
        await self.cache.setex(key, self.default_ttl, json.dumps(result))
        return result
```

---

## 10. Monitoring Integration Health

```python
class IntegrationMonitor:
    def __init__(self):
        self.metrics = {
            "requests_total": Counter("integration_requests_total", "Total requests", ["endpoint"]),
            "errors_total": Counter("integration_errors_total", "Total errors", ["endpoint", "error_type"]),
            "latency": Histogram("integration_latency_seconds", "Request latency", ["endpoint"])
        }
    
    def record_request(self, endpoint: str, duration: float, success: bool):
        self.metrics["requests_total"].labels(endpoint=endpoint).inc()
        self.metrics["latency"].labels(endpoint=endpoint).observe(duration)
        if not success:
            self.metrics["errors_total"].labels(endpoint=endpoint, error_type="failed").inc()
```

---

## 11. Idempotency Design

### Idempotent Endpoint Implementation

```python
from typing import Dict, Any, Optional
import hashlib
import json
from datetime import datetime

class IdempotencyManager:
    """Enforce idempotent processing."""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    async def process_idempotent(self, idempotency_key: str, 
                                 processor: Callable, 
                                 ttl: int = 86400) -> Any:
        existing = await self.storage.get(f"idempotency:{idempotency_key}")
        if existing:
            logger.info(f"Idempotency hit: {idempotency_key}")
            return json.loads(existing)
        
        result = await processor()
        await self.storage.setex(
            f"idempotency:{idempotency_key}",
            ttl,
            json.dumps(result)
        )
        return result

class IdempotentAPI:
    """Decorator for idempotent API endpoints."""
    
    def __init__(self, storage):
        self.storage = storage
    
    async def process_with_idempotency(self, key: str, processor):
        existing = await self.storage.get(f"idemp:{key}")
        if existing:
            return {"status": "already_processed", "result": json.loads(existing)}
        
        result = await processor()
        await self.storage.setex(f"idemp:{key}", 3600, json.dumps(result))
        return result

@app.route("/api/v1/process", methods=["POST"])
async def process_endpoint():
    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        return {"error": "Idempotency-Key header required"}, 400
    
    manager = IdempotencyManager(redis_client)
    result = await manager.process_idempotent(
        idempotency_key,
        lambda: agent.process(request.json["prompt"], request.json["session_id"])
    )
    return result
```

### Webhook Idempotency

```python
class IdempotentWebhookHandler:
    def __init__(self, storage, handler):
        self.storage = storage
        self.handler = handler
    
    async def handle(self, delivery_id: str, payload: Dict, signature: str):
        if not verify_signature(payload, signature):
            raise UnauthorizedError("Invalid signature")
        
        existing = await self.storage.get(f"wh:{delivery_id}")
        if existing:
            logger.info(f"Duplicate webhook: {delivery_id}")
            return json.loads(existing)
        
        # Prevent duplicate processing
        lock_acquired = await self.storage.set(
            f"wh:lock:{delivery_id}", "1", nx=True, ex=60
        )
        if not lock_acquired:
            return {"status": "already_processing"}
        
        try:
            result = await self.handler(payload)
            await self.storage.setex(
                f"wh:{delivery_id}", 86400, json.dumps(result)
            )
            return result
        finally:
            await self.storage.delete(f"wh:lock:{delivery_id}")
```

---

## 12. Graceful Degradation

### Fallback Strategies

```python
class FallbackAgent:
    """Agent with fallback capabilities."""
    
    def __init__(self, primary_agent, fallback_agent=None):
        self.primary = primary_agent
        self.fallback = fallback_agent
    
    async def process(self, prompt: str, session_id: str, context: Dict):
        try:
            result = await asyncio.wait_for(
                self.primary.process(prompt, session_id, context),
                timeout=30
            )
            return result
        except (TimeoutError, ServiceUnavailable) as e:
            logger.warning(f"Primary agent failed: {e}")
            if self.fallback:
                return await self.fallback.process(prompt, session_id, context)
            raise
    
    async def process_with_defaults(self, prompt: str, 
                                     session_id: str, 
                                     context: Dict):
        try:
            return await self.process(prompt, session_id, context)
        except Exception as e:
            logger.error(f"All agents failed: {e}")
            return {
                "response": "Service temporarily unavailable. Please try again.",
                "error": "degraded_service",
                "session_id": session_id
            }

class CapacityManager:
    """Manage capacity and shed load."""
    
    def __init__(self, max_concurrent: int = 100):
        self.max_concurrent = max_concurrent
        self.current = 0
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def with_capacity(self, coro):
        if self.current >= self.max_concurrent:
            raise ServiceUnavailable("Service at capacity")
        
        async with self.semaphore:
            self.current += 1
            try:
                return await coro
            finally:
                self.current -= 1
    
    def capacity_ratio(self) -> float:
        return self.current / self.max_concurrent

class GracefulDegradationMiddleware:
    def __init__(self, app, capacity_manager):
        self.app = app
        self.capacity = capacity_manager
    
    async def __call__(self, request):
        ratio = self.capacity.capacity_ratio()
        
        if ratio > 0.9:
            return {"error": "Service overloaded", "retry_after": 5}, 503
        
        return await self.app(request)
```

---

## 13. Resource Management

### Connection Pooling & Lifecycle

```python
from contextlib import asynccontextmanager
import aiohttp
import asyncpg
import aioredis
from typing import Optional
import asyncio

class ResourceManager:
    """Centralized resource management."""
    
    def __init__(self):
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.db_pool: Optional[asyncpg.Pool] = None
        self.redis: Optional[aioredis.Redis] = None
    
    async def initialize(self, config: Dict):
        self.http_session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=config.get("http_max_connections", 100),
                limit_per_host=config.get("http_per_host", 10)
            )
        )
        
        self.db_pool = await asyncpg.create_pool(
            config["database_url"],
            min_size=5,
            max_size=config.get("db_max_connections", 20),
            command_timeout=60
        )
        
        self.redis = aioredis.from_url(
            config["redis_url"],
            max_connections=config.get("redis_max_connections", 50),
            decode_responses=True
        )
    
    async def close(self):
        if self.http_session and not self.http_session.closed:
            await self.http_session.close()
        
        if self.db_pool:
            await self.db_pool.close()
        
        if self.redis:
            await self.redis.close()
    
    @asynccontextmanager
    async def http(self):
        if not self.http_session:
            raise RuntimeError("HTTP session not initialized")
        yield self.http_session
    
    @asynccontextmanager
    async def db(self):
        if not self.db_pool:
            raise RuntimeError("DB pool not initialized")
        async with self.db_pool.acquire() as conn:
            yield conn
    
    @asynccontextmanager
    async def cache(self):
        if not self.redis:
            raise RuntimeError("Redis not initialized")
        yield self.redis

class AsyncResourceContext:
    """Context manager for resource lifecycle."""
    
    def __init__(self, resources: Dict[str, Any]):
        self.resources = resources
        self.initialized = False
    
    async def __aenter__(self):
        await self.initialize()
        self.initialized = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.initialized:
            await self.close()
    
    async def initialize(self):
        for name, resource in self.resources.items():
            if hasattr(resource, "initialize"):
                await resource.initialize()
    
    async def close(self):
        for name, resource in reversed(list(self.resources.items())):
            if hasattr(resource, "close"):
                await resource.close()
```

---

## 14. Contract Testing

### Consumer-Driven Contracts

```python
from typing import Dict, Any, List
import pytest
import json

class Contract:
    """Consumer-driven contract definition."""
    
    def __init__(self, consumer: str, provider: str):
        self.consumer = consumer
        self.provider = provider
        self.requests: List[Dict] = []
        self.responses: List[Dict] = []
    
    def add_request(self, method: str, path: str, 
                    headers: Dict = None, body: Dict = None):
        self.requests.append({
            "method": method,
            "path": path,
            "headers": headers or {},
            "body": body
        })
    
    def add_response(self, method: str, path: str, 
                     status: int, schema: Dict):
        self.responses.append({
            "method": method,
            "path": path,
            "status": status,
            "schema": schema
        })

class ContractVerifier:
    """Verify provider satisfies consumer contracts."""
    
    def __init__(self, provider_client):
        self.client = provider_client
        self.contracts: List[Contract] = []
    
    def load_contract(self, contract: Contract):
        self.contracts.append(contract)
    
    async def verify_all(self):
        results = []
        for contract in self.contracts:
            result = await self.verify_contract(contract)
            results.append(result)
        return results
    
    async def verify_contract(self, contract: Contract) -> Dict:
        failures = []
        
        for req in contract.requests:
            response = await self.client.request(
                method=req["method"],
                path=req["path"],
                headers=req["headers"],
                body=req["body"]
            )
            
            expected = next(
                (r for r in contract.responses 
                 if r["method"] == req["method"] 
                 and r["path"] == req["path"]),
                None
            )
            
            if not expected:
                failures.append(f"Missing response spec for {req}")
                continue
            
            if response.status != expected["status"]:
                failures.append(
                    f"Status mismatch: expected {expected['status']}, "
                    f"got {response.status}"
                )
            
            if not self._validate_schema(response.body, expected["schema"]):
                failures.append("Schema validation failed")
        
        return {
            "contract": f"{contract.consumer}->{contract.provider}",
            "passed": len(failures) == 0,
            "failures": failures
        }
    
    def _validate_schema(self, data: Any, schema: Dict) -> bool:
        try:
            import jsonschema
            jsonschema.validate(instance=data, schema=schema)
            return True
        except Exception:
            return False

class PactMockServer:
    """Mock server for contract testing."""
    
    def __init__(self, contract: Contract):
        self.contract = contract
        self.routes: Dict[str, Dict] = {}
    
    def setup_routes(self):
        for resp in self.contract.responses:
            key = f"{resp['method']}:{resp['path']}"
            self.routes[key] = resp
    
    def handle_request(self, method: str, path: str) -> Dict:
        key = f"{method}:{path}"
        route = self.routes.get(key)
        if not route:
            return {"status": 404, "body": {"error": "Not found"}}
        return {
            "status": route["status"],
            "body": self._generate_mock(route["schema"])
        }
    
    def _generate_mock(self, schema: Dict) -> Dict:
        # Simplified mock generation
        return {}
```

---

## 15. Secrets & Credential Management

### Secure Integration with Vault

```python
import hvac
import os
from typing import Dict, Any

class SecretsManager:
    """Manage secrets for integrations."""
    
    def __init__(self, vault_url: str, vault_token: str):
        self.client = hvac.Client(url=vault_url, token=vault_token)
    
    async def get_secret(self, path: str, key: str) -> str:
        try:
            response = await asyncio.to_thread(
                self.client.secrets.kv.read_secret_version,
                path=path
            )
            return response["data"]["data"][key]
        except Exception as e:
            logger.error(f"Failed to read secret {path}/{key}: {e}")
            raise
    
    async def get_integration_config(self, integration: str) -> Dict[str, str]:
        secret_path = f"integrations/{integration}"
        try:
            response = await asyncio.to_thread(
                self.client.secrets.kv.read_secret_version,
                path=secret_path
            )
            return response["data"]["data"]
        except hvac.exceptions.InvalidPath:
            return {}
    
    async def rotate_secret(self, path: str, key: str, 
                            new_value: str):
        await asyncio.to_thread(
            self.client.secrets.kv.create_or_update_secret,
            path=path,
            secret={key: new_value}
        )
        logger.info(f"Secret rotated: {path}/{key}")

class IntegrationConfig:
    """Load and validate integration configs."""
    
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets = secrets_manager
        self._cache: Dict[str, Dict] = {}
    
    async def load(self, integration: str) -> Dict[str, Any]:
        if integration in self._cache:
            return self._cache[integration]
        
        config = await self.secrets.get_integration_config(integration)
        
        required = ["api_url", "api_key", "timeout"]
        missing = [r for r in required if r not in config]
        if missing:
            raise ConfigurationError(f"Missing config keys: {missing}")
        
        self._cache[integration] = config
        return config
    
    async def get_api_key(self, integration: str) -> str:
        config = await self.load(integration)
        return config["api_key"]
```

---

## 16. Logging & Audit Trail

### Structured Logging for Integrations

```python
import structlog
import json
from datetime import datetime
from typing import Dict, Any

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

class AuditLogger:
    """Audit trail for integration events."""
    
    async def log_event(self, event_type: str, 
                        integration: str, 
                        outcome: str,
                        metadata: Dict = None):
        logger.info(
            "integration_event",
            event_type=event_type,
            integration=integration,
            outcome=outcome,
            timestamp=datetime.utcnow().isoformat(),
            **(metadata or {})
        )
    
    async def log_request(self, endpoint: str, method: str, 
                          status: int, duration: float,
                          trace_id: str = None):
        logger.info(
            "http_request",
            endpoint=endpoint,
            method=method,
            status_code=status,
            duration_ms=duration * 1000,
            trace_id=trace_id
        )
    
    async def log_webhook(self, delivery_id: str, url: str,
                          status: str, attempt: int, 
                          error: str = None):
        logger.info(
            "webhook_delivery",
            delivery_id=delivery_id,
            url=url,
            status=status,
            attempt=attempt,
            error=error
        )

class RequestLoggerMiddleware:
    """Log all requests with correlation."""
    
    def __init__(self, app, audit_logger: AuditLogger):
        self.app = app
        self.audit = audit_logger
    
    async def __call__(self, request, call_next, trace_id: str):
        start = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start
            
            await self.audit.log_request(
                endpoint=request.url.path,
                method=request.method,
                status=response.status_code,
                duration=duration,
                trace_id=trace_id
            )
            
            response.headers["X-Trace-Id"] = trace_id
            return response
        except Exception as e:
            duration = time.time() - start
            await self.audit.log_request(
                endpoint=request.url.path,
                method=request.method,
                status=500,
                duration=duration,
                trace_id=trace_id
            )
            raise
```

---

## 17. SLA & SLO Management

### Service Level Objectives

```python
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

@dataclass
class SLO:
    name: str
    target: float
    measurement_window: timedelta
    error_budget: float
    current_budget: float

class SLOMonitor:
    """Track SLO compliance."""
    
    def __init__(self):
        self.slos: Dict[str, SLO] = {}
        self.metrics: Dict[str, List[float]] = defaultdict(list)
    
    def register_slo(self, name: str, target: float, 
                     window_days: int = 30):
        self.slos[name] = SLO(
            name=name,
            target=target,
            measurement_window=timedelta(days=window_days),
            error_budget=1.0 - target,
            current_budget=1.0 - target
        )
    
    def record_request(self, slo_name: str, duration: float, 
                       success: bool):
        if slo_name not in self.slos:
            return
        
        self.metrics[slo_name].append({
            "timestamp": datetime.utcnow(),
            "duration": duration,
            "success": success
        })
    
    def calculate_slo(self, slo_name: str) -> Dict:
        slo = self.slos[slo_name]
        cutoff = datetime.utcnow() - slo.measurement_window
        
        relevant = [
            m for m in self.metrics[slo_name]
            if m["timestamp"] > cutoff
        ]
        
        if not relevant:
            return {"status": "no_data", "slo": slo.name, "target": slo.target}
        
        total = len(relevant)
        failures = sum(1 for m in relevant if not m["success"])
        success_rate = (total - failures) / total
        
        return {
            "slo": slo.name,
            "target": slo.target,
            "current": success_rate,
            "remaining_budget": slo.error_budget - (1 - success_rate),
            "status": "met" if success_rate >= slo.target else "violated",
            "total_requests": total,
            "failures": failures
        }
    
    def burn_rate_alert(self, slo_name: str) -> bool:
        slo = self.slos[slo_name]
        cutoff = datetime.utcnow() - timedelta(hours=1)
        
        recent = [
            m for m in self.metrics[slo_name]
            if m["timestamp"] > cutoff
        ]
        
        if len(recent) < 10:
            return False
        
        error_rate = sum(1 for m in recent if not m["success"]) / len(recent)
        
        return error_rate > slo.error_budget * 5  # 5x burn rate
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)