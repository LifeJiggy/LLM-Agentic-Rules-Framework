# Integration Domain - Fundamentals

## Overview

This document covers fundamental integration concepts for LLM/agentic systems, including API design principles, authentication patterns, webhook fundamentals, streaming concepts, and production integration patterns. All concepts are presented with implementation guidance and real-world considerations.

---

## Table of Contents

1. [Resource-Based API Design](#1-resource-based-api-design)
2. [HTTP Status Codes](#2-http-status-codes)
3. [Authentication Patterns](#3-authentication-patterns)
4. [Webhook Fundamentals](#4-webhook-fundamentals)
5. [Streaming Data Fundamentals](#5-streaming-data-fundamentals)
6. [Error Handling Fundamentals](#6-error-handling-fundamentals)
7. [Data Format Standards](#7-data-format-standards)
8. [Connection Management](#8-connection-management)
9. [Service Discovery](#9-service-discovery)
10. [API Versioning](#10-api-versioning)

---

## 1. Resource-Based API Design

### Resource-Based Design

```python
# RESTful resources
GET    /api/users     - List users
POST   /api/users     - Create user
GET    /api/users/{id} - Get user
PUT    /api/users/{id} - Update user
DELETE /api/users/{id} - Delete user
```

### Agent-Specific Resources

```python
# Agent-specific endpoints
GET    /api/agents/{id}/sessions
POST   /api/agents/{id}/sessions
POST   /api/sessions/{id}/messages
GET    /api/sessions/{id}/context
POST   /api/tools/{name}/execute
GET    /api/tools
```

### Naming Conventions

```python
class ResourceNaming:
    @staticmethod
    def user_resource(user_id: str) -> str:
        return f"/api/v1/users/{user_id}"
    
    @staticmethod
    def session_resource(user_id: str, session_id: str) -> str:
        return f"/api/v1/users/{user_id}/sessions/{session_id}"
    
    @staticmethod
    def tool_resource(tool_name: str) -> str:
        return f"/api/v1/tools/{tool_name}"
```

---

## 2. HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/wrong auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource missing |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Internal error |

### Agent-Specific Status Codes

```python
class AgentStatusCode:
    SESSION_EXPIRED = 440  # Login Timeout
    CONTEXT_OVERFLOW = 449  # Retry With
    TOOL_UNAVAILABLE = 503  # Service Unavailable
    MODEL_RATE_LIMITED = 429  # Too Many Requests

@app.errorhandler(AgentStatusCode.CONTEXT_OVERFLOW)
def context_overflow(error):
    return jsonify({
        "error": "Context window exceeded",
        "suggestion": "Start new session"
    }), 440
```

---

## 3. Authentication Patterns

### API Keys

```python
def require_api_key(handler):
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not validate_key(key):
            return {"error": "Invalid key"}, 401
        return handler(*args, **kwargs)
    return wrapper
```

### JWT Tokens

```python
def require_jwt(handler):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            request.user = payload
            return handler(*args, **kwargs)
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
    return wrapper
```

### OAuth2 Integration

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/auth/google')
def auth_google():
    redirect_uri = url_for('auth_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    return jsonify(user_info)
```

### mTLS for Service-to-Service

```python
import ssl
import requests

def service_call(service_url: str, payload: dict):
    context = ssl.create_default_context(cafile='/path/to/ca.pem')
    context.load_cert_chain('/path/to/client.pem', '/path/to/client-key.pem')
    
    response = requests.post(
        service_url,
        json=payload,
        cert=('/path/to/client.pem', '/path/to/client-key.pem'),
        verify='/path/to/ca.pem'
    )
    return response.json()
```

---

## 4. Webhook Fundamentals

### Webhook Structure

```python
webhook_payload = {
    "event": "user.message.received",
    "data": {"message_id": "123", "content": "Hello"},
    "timestamp": 1234567890,
    "signature": "sha256=abc123..."
}
```

### Signature Verification

```python
def verify_signature(payload, signature, secret):
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### Webhook Event Schema

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class WebhookEvent:
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    delivery_id: str
    retry_count: int = 0

class WebhookEventFormatter:
    @staticmethod
    def format_agent_event(event_type: str, payload: Dict) -> WebhookEvent:
        return WebhookEvent(
            event_type=f"agent.{event_type}",
            data=payload,
            timestamp=datetime.utcnow(),
            source="agent-system",
            delivery_id=str(uuid.uuid4())
        )
```

### Webhook Retry Logic

```python
class WebhookRetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def should_retry(self, attempt: int, response_code: int) -> bool:
        if attempt >= self.max_retries:
            return False
        return response_code in [408, 429, 500, 502, 503, 504]
    
    def get_retry_delay(self, attempt: int) -> float:
        return self.backoff_factor ** attempt
```

---

## 5. Streaming Data Fundamentals

### Event Streaming Basics

```python
import asyncio
from typing import AsyncGenerator

class EventStream:
    def __init__(self):
        self.subscribers: List[Callable] = []
    
    async def subscribe(self, handler: Callable):
        self.subscribers.append(handler)
    
    async def publish(self, event: Dict):
        for handler in self.subscribers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Handler error: {e}")
```

### Streaming Patterns

```python
class StreamProcessor:
    async def process_stream(self, input_stream: AsyncGenerator) -> AsyncGenerator:
        buffer = []
        async for chunk in input_stream:
            buffer.append(chunk)
            if len(buffer) >= 10:
                processed = await self._process_batch(buffer)
                for item in processed:
                    yield item
                buffer = []
        
        if buffer:
            processed = await self._process_batch(buffer)
            for item in processed:
                yield item
```

---

## 6. Error Handling Fundamentals

### Error Response Format

```python
class ErrorResponse:
    def __init__(self, code: str, message: str, details: Dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp
            }
        }
```

### Common Error Codes

```python
class IntegrationErrorCodes:
    INVALID_REQUEST = "invalid_request"
    AUTH_FAILED = "auth_failed"
    RATE_LIMITED = "rate_limited"
    RESOURCE_NOT_FOUND = "resource_not_found"
    INTERNAL_ERROR = "internal_error"
    TIMEOUT = "timeout"
    PAYLOAD_TOO_LARGE = "payload_too_large"
```

---

## 7. Data Format Standards

### Request/Response Format

```python
from pydantic import BaseModel

class AgentRequest(BaseModel):
    prompt: str
    session_id: str
    context: Optional[Dict] = None
    parameters: Optional[Dict] = None

class AgentResponse(BaseModel):
    response: str
    session_id: str
    tokens_used: int
    model: str
    metadata: Dict = {}

# Serialization with validation
def serialize_request(data: dict) -> str:
    validated = AgentRequest(**data)
    return validated.json()

def deserialize_response(data: str) -> AgentResponse:
    return AgentResponse(**json.loads(data))
```

### Content Negotiation

```python
class ContentNegotiator:
    @staticmethod
    def negotiate(formats: List[str], accepted: str) -> str:
        if accepted in formats:
            return accepted
        # Return default
        return "application/json"
```

---

## 8. Connection Management

### Connection Pooling

```python
import aiohttp

class ConnectionManager:
    def __init__(self, max_connections: int = 100):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=10,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )
        self.session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(connector=self.connector)
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
```

### Retry Pattern

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def resilient_api_call(url: str, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
```

---

## 9. Service Discovery

### Service Registry

```python
class ServiceRegistry:
    def __init__(self):
        self.services: Dict[str, Dict] = {}
    
    def register(self, name: str, endpoint: str, health_endpoint: str):
        self.services[name] = {
            "endpoint": endpoint,
            "health": health_endpoint,
            "registered_at": datetime.utcnow(),
            "healthy": True
        }
    
    def get(self, name: str) -> Optional[Dict]:
        return self.services.get(name)
    
    async def health_check(self, name: str) -> bool:
        service = self.services.get(name)
        if not service:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(service["health"], timeout=5) as resp:
                    return resp.status == 200
        except Exception:
            return False

registry = ServiceRegistry()
registry.register("agent-api", "http://agent-api:8080", "/health")
```

---

## 10. API Versioning

### URL Versioning

```python
class VersionedRouter:
    def __init__(self):
        self.routes: Dict[str, Dict] = {}
    
    def add_route(self, version: str, path: str, handler: Callable):
        if version not in self.routes:
            self.routes[version] = {}
        self.routes[version][path] = handler
    
    def route(self, request) -> Callable:
        version = request.headers.get("API-Version", "v1")
        path = request.path
        
        if version in self.routes and path in self.routes[version]:
            return self.routes[version][path]
        
        raise NotFoundError(f"No handler for {version} {path}")

router = VersionedRouter()

@router.route("v1")
def get_users_v1():
    return {"version": "v1", "users": []}

@router.route("v2")
def get_users_v2():
    return {"version": "v2", "users": [], "meta": {}}
```

---

## 11. Load Balancing Fundamentals

### Load Balancing Strategies

```python
import random
import hashlib
from typing import List, Dict
import asyncio

class LoadBalancer:
    """Load balancing across service instances."""
    
    STRATEGIES = ["round_robin", "least_connections", "weighted", "ip_hash"]
    
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self.instances: List[Dict] = []
        self.current_index = 0
        self.connection_counts: Dict[str, int] = {}
    
    def add_instance(self, host: str, port: int, weight: int = 1):
        key = f"{host}:{port}"
        self.instances.append({
            "host": host,
            "port": port,
            "weight": weight,
            "key": key,
            "healthy": True
        })
        self.connection_counts[key] = 0
    
    def select_instance(self, client_ip: str = None) -> Dict:
        healthy = [i for i in self.instances if i["healthy"]]
        if not healthy:
            raise NoHealthyInstancesError("No healthy instances available")
        
        if self.strategy == "round_robin":
            instance = healthy[self.current_index % len(healthy)]
            self.current_index += 1
            return instance
        
        elif self.strategy == "least_connections":
            return min(healthy, 
                       key=lambda i: self.connection_counts[i["key"]])
        
        elif self.strategy == "weighted":
            return random.choices(
                healthy,
                weights=[i["weight"] for i in healthy]
            )[0]
        
        elif self.strategy == "ip_hash" and client_ip:
            hash_value = int(hashlib.md5(
                client_ip.encode()
            ).hexdigest(), 16)
            return healthy[hash_value % len(healthy)]
        
        return random.choice(healthy)
    
    def increment_connections(self, instance: Dict):
        self.connection_counts[instance["key"]] += 1
    
    def decrement_connections(self, instance: Dict):
        self.connection_counts[instance["key"]] = max(
            0, self.connection_counts[instance["key"]] - 1
        )

class HealthAwareLoadBalancer(LoadBalancer):
    """Load balancer with active health checking."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_interval = 30
    
    async def start_health_checks(self, path: str = "/health"):
        while True:
            for instance in self.instances:
                await self._check_instance(instance, path)
            await asyncio.sleep(self.check_interval)
    
    async def _check_instance(self, instance: Dict, path: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://{instance['host']}:{instance['port']}{path}",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    instance["healthy"] = response.status == 200
                    instance["last_check"] = datetime.utcnow()
        except Exception:
            instance["healthy"] = False
            instance["last_check"] = datetime.utcnow()
    
    def select_instance(self, client_ip: str = None) -> Dict:
        healthy = [i for i in self.instances if i["healthy"]]
        if not healthy:
            raise ServiceUnavailable("All instances unhealthy")
        
        return super().select_instance(client_ip)
```

---

## 12. Message Queue Patterns

### Reliable Message Processing

```python
from dataclasses import dataclass
from typing import Dict, Callable, Any, Optional
import uuid

@dataclass
class Message:
    id: str
    body: Dict[str, Any]
    headers: Dict[str, str]
    timestamp: float
    retry_count: int = 0
    max_retries: int = 3

class MessageQueue:
    """Abstract message queue with acknowledgment."""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.processing = set()
    
    async def publish(self, topic: str, message: Dict, 
                      headers: Dict = None):
        msg = Message(
            id=str(uuid.uuid4()),
            body=message,
            headers=headers or {},
            timestamp=time.time()
        )
        await self._enqueue(topic, msg)
    
    async def consume(self, topic: str, handler: Callable):
        self.handlers[topic] = handler
        async for msg in self._dequeue(topic):
            if msg.id in self.processing:
                continue
            
            self.processing.add(msg.id)
            
            try:
                await handler(msg.body, msg.headers)
                await self._ack(msg)
            except TemporaryError as e:
                msg.retry_count += 1
                if msg.retry_count < msg.max_retries:
                    await self._nack(msg, delay=self._backoff(msg.retry_count))
                else:
                    await self._dead_letter(msg, str(e))
            except PermanentError:
                await self._dead_letter(msg, "Permanent failure")
            except Exception:
                await self._nack(msg, delay=60)
            finally:
                self.processing.discard(msg.id)
    
    def _backoff(self, attempt: int) -> int:
        return min(2 ** attempt * 1000, 60000)
    
    async def _ack(self, msg: Message):
        pass  # Implementation specific
    
    async def _nack(self, msg: Message, delay: int):
        pass
    
    async def _dead_letter(self, msg: Message, reason: str):
        pass

class DeadLetterHandler:
    """Handle messages that failed processing."""
    
    def __init__(self, queue: MessageQueue):
        self.queue = queue
    
    async def process_dead_letter(self, msg: Message, reason: str):
        await self.queue.publish(
            topic="dead_letter",
            message={
                "original": msg.body,
                "reason": reason,
                "original_id": msg.id,
                "retry_count": msg.retry_count
            },
            headers={"x-original-topic": msg.headers.get("topic", "")}
        )
```

### Priority Queue Pattern

```python
import heapq
import asyncio
from typing import Any, Tuple

class PriorityMessage:
    def __init__(self, priority: int, message: Any):
        self.priority = priority
        self.message = message
    
    def __lt__(self, other):
        return self.priority < other.priority

class PriorityQueue:
    """Priority-based message queue."""
    
    def __init__(self):
        self.queue: List[PriorityMessage] = []
        self.lock = asyncio.Lock()
    
    async def enqueue(self, priority: int, message: Any):
        async with self.lock:
            heapq.heappush(self.queue, PriorityMessage(priority, message))
    
    async def dequeue(self) -> Any:
        async with self.lock:
            if not self.queue:
                await asyncio.sleep(0.1)
                return None
            msg = heapq.heappop(self.queue)
            return msg.message
    
    async def process(self, handler: Callable):
        while True:
            message = await self.dequeue()
            if message:
                await handler(message)
            else:
                await asyncio.sleep(0.1)
```

---

## 13. SLA & Timeout Fundamentals

### Circuit Breaker Fundamentals

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: float = 60.0,
                 success_threshold: int = 2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = 0.0
    
    async def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitOpenError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### Bulkhead Isolation

```python
from asyncio import Semaphore
from typing import Dict
import asyncio

class BulkheadManager:
    """Isolate resources to prevent cascade failures."""
    
    def __init__(self):
        self.bulkheads: Dict[str, Semaphore] = {}
        self.max_concurrent: Dict[str, int] = {}
        self.running: Dict[str, int] = {}
    
    def register(self, name: str, max_concurrent: int):
        self.bulkheads[name] = Semaphore(max_concurrent)
        self.max_concurrent[name] = max_concurrent
        self.running[name] = 0
    
    async def execute(self, name: str, coro):
        if name not in self.bulkheads:
            raise ValueError(f"Unknown bulkhead: {name}")
        
        async with self.bulkheads[name]:
            self.running[name] += 1
            try:
                return await coro
            finally:
                self.running[name] -= 1
    
    def utilization(self, name: str) -> float:
        if name not in self.max_concurrent:
            return 0.0
        max_c = self.max_concurrent[name]
        running = self.running.get(name, 0)
        return running / max_c if max_c > 0 else 0.0
```

### Retry Fundamentals

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from tenacity import retry_if_exception_type, before_sleep_log
import logging

def create_retry_decorator(max_attempts: int = 3,
                           min_wait: int = 1,
                           max_wait: int = 10,
                           retryable_exceptions: tuple = (TimeoutError,)):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type(retryable_exceptions),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )

# Usage
@create_retry_decorator(max_attempts=3)
async def resilient_api_call(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

class RetryContext:
    def __init__(self):
        self.attempts = 0
        self.last_exception = None
    
    async def execute(self, func: Callable, *args, **kwargs):
        max_retries = kwargs.pop("max_retries", 3)
        backoff = kwargs.pop("backoff", 1.0)
        
        for attempt in range(max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self.last_exception = e
                self.attempts = attempt + 1
                if attempt < max_retries:
                    await asyncio.sleep(backoff * (2 ** attempt))
                else:
                    raise
```

---

## 14. Data Serialization Standards

### Serialization Patterns

```python
import json
import pickle
from typing import Any, Dict
from dataclasses import dataclass, asdict
from datetime import datetime, date

class SerializationFormat:
    JSON = "json"
    MSGPACK = "msgpack"
    PROTOBUF = "protobuf"
    AVRO = "avro"
    PICKLE = "pickle"

class MessageSerializer:
    """Serialize messages with format negotiation."""
    
    @staticmethod
    def serialize(data: Any, format: str = SerializationFormat.JSON) -> bytes:
        if format == SerializationFormat.JSON:
            return json.dumps(data, default=str).encode()
        elif format == SerializationFormat.PICKLE:
            return pickle.dumps(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @staticmethod
    def deserialize(data: bytes, format: str = SerializationFormat.JSON) -> Any:
        if format == SerializationFormat.JSON:
            return json.loads(data.decode())
        elif format == SerializationFormat.PICKLE:
            return pickle.loads(data)
        else:
            raise ValueError(f"Unsupported format: {format}")

class TypedResponse:
    """Type-safe response encoding."""
    
    def __init__(self, data: Any, metadata: Dict = None):
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            "data": self._serialize(self.data),
            "meta": {
                **self.metadata,
                "timestamp": self.timestamp,
                "type": type(self.data).__name__
            }
        }
    
    def _serialize(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return obj.decode()
        elif isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._serialize(item) for item in obj]
        return obj

class ContentTypeNegotiator:
    """Content negotiation for API responses."""
    
    def __init__(self):
        self.formatters = {
            "application/json": lambda d: json.dumps(d, default=str),
            "application/msgpack": lambda d: msgpack.dumps(d),
            "text/plain": lambda d: str(d)
        }
    
    def format_response(self, data: Any, accept: str) -> str:
        if accept in self.formatters:
            return self.formatters[accept](data)
        return json.dumps(data, default=str)
```

---

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)