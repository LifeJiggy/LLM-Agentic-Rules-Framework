# Integration Domain - Advanced Concepts

## Overview

This document covers advanced integration concepts for LLM/agentic systems, including API gateway patterns, service mesh architectures, webhooks, streaming integrations, and enterprise connectivity patterns. All concepts are production-oriented with implementation guidance.

---

## Table of Contents

1. [API Gateway Pattern](#1-api-gateway-pattern)
2. [Service Mesh Architecture](#2-service-mesh-architecture)
3. [GraphQL Federation](#3-graphql-federation)
4. [Webhook Management](#4-webhook-management)
5. [Streaming Integrations](#5-streaming-integrations)
6. [Event-Driven Integration](#6-event-driven-integration)
7. [Rate Limiting Gateway](#7-rate-limiting-gateway)
8. [API Versioning Strategy](#8-api-versioning-strategy)
9. [Integration Testing Patterns](#9-integration-testing-patterns)
10. [Circuit Breaker Patterns](#10-circuit-breaker-patterns)

---

## 1. API Gateway Pattern

### Production-Ready Gateway

```python
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
import asyncio
import time
from functools import wraps

@dataclass
class Route:
    path: str
    handler: Callable
    methods: List[str]
    rate_limit: int
    timeout: int
    auth_required: bool = True

@dataclass
class RequestContext:
    method: str
    path: str
    headers: Dict[str, str]
    body: Any
    user: Optional[Dict]
    rate_limit_remaining: int
    start_time: float

class APIGateway:
    """Production-ready API gateway with middleware."""
    
    def __init__(self, rate_limiter=None):
        self.routes: Dict[str, Route] = {}
        self.middleware: List[Callable] = []
        self.rate_limiter = rate_limiter
        self.metrics = {
            "requests_total": 0,
            "errors_total": 0,
            "latency_sum": 0
        }
    
    def register_route(self, path: str, handler: Callable, **config) -> None:
        self.routes[path] = Route(
            path=path,
            handler=handler,
            methods=config.get("methods", ["GET"]),
            rate_limit=config.get("rate_limit", 100),
            timeout=config.get("timeout", 30),
            auth_required=config.get("auth_required", True)
        )
    
    def add_middleware(self, middleware: Callable) -> None:
        self.middleware.append(middleware)
    
    async def handle(self, request: Dict) -> Dict:
        ctx = RequestContext(
            method=request.get("method", "GET"),
            path=request.get("path", "/"),
            headers=request.get("headers", {}),
            body=request.get("body"),
            user=None,
            rate_limit_remaining=0,
            start_time=time.time()
        )
        
        # Apply middleware
        for mw in self.middleware:
            ctx = await mw(ctx)
            if ctx is None:
                return {"error": "Middleware rejected", "status": 403}
        
        # Find route
        route = self._find_route(ctx.method, ctx.path)
        if not route:
            return {"error": "Not found", "status": 404}
        
        # Rate limiting
        if self.rate_limiter and not self.rate_limiter.allow(ctx.path):
            return {"error": "Rate limit exceeded", "status": 429}
        
        # Authentication
        if route.auth_required and not ctx.user:
            return {"error": "Unauthorized", "status": 401}
        
        try:
            result = await asyncio.wait_for(
                route.handler(ctx),
                timeout=route.timeout
            )
            self.metrics["requests_total"] += 1
            self.metrics["latency_sum"] += time.time() - ctx.start_time
            return result
        except asyncio.TimeoutError:
            self.metrics["errors_total"] += 1
            return {"error": "Request timeout", "status": 504}
        except Exception as e:
            self.metrics["errors_total"] += 1
            return {"error": str(e), "status": 500}
    
    def _find_route(self, method: str, path: str) -> Optional[Route]:
        for route in self.routes.values():
            if method in route.methods and path == route.path:
                return route
        return None
```

---

## 2. Service Mesh Architecture

### Intelligent Service Routing

```python
import asyncio
from typing import Dict, Any, Optional
import random

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure: float = 0
        self.state = "CLOSED"
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "HALF_OPEN"
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
        self.state = "CLOSED"
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

class ServiceMesh:
    """Service mesh with circuit breaking and load balancing."""
    
    def __init__(self):
        self.services: Dict[str, List[Dict]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.service_stats: Dict[str, Dict] = {}
    
    def register_service(self, name: str, endpoints: List[Dict]) -> None:
        self.services[name] = endpoints
        for endpoint in endpoints:
            self.circuit_breakers[f"{name}:{endpoint['id']}"] = CircuitBreaker()
            self.service_stats[f"{name}:{endpoint['id']}"] = {
                "requests": 0, "failures": 0, "latency_sum": 0
            }
    
    async def call_service(self, name: str, payload: Any) -> Any:
        endpoint = self._select_endpoint(name)
        if not endpoint:
            raise ServiceNotFound(f"No healthy endpoints for {name}")
        
        cb_key = f"{name}:{endpoint['id']}"
        breaker = self.circuit_breakers[cb_key]
        
        start = time.time()
        try:
            result = await breaker.call(endpoint["client"].call, payload)
            self.service_stats[cb_key]["requests"] += 1
            self.service_stats[cb_key]["latency_sum"] += time.time() - start
            return result
        except Exception:
            self.service_stats[cb_key]["failures"] += 1
            raise
    
    def _select_endpoint(self, service_name: str) -> Optional[Dict]:
        endpoints = self.services.get(service_name, [])
        healthy = [ep for ep in endpoints 
                   if self.circuit_breakers[f"{service_name}:{ep['id']}"].state != "OPEN"]
        
        if not healthy:
            return None
        
        # Least loaded endpoint
        return min(healthy, key=lambda ep: 
            self.service_stats[f"{service_name}:{ep['id']}"]
            ["failures"] - self.service_stats[f"{service_name}:{ep['id']}"]
            ["requests"])
```

---

## 3. GraphQL Federation

### Federated Schema Management

```python
from typing import Dict, Any, List, Optional
import asyncio

class GraphQLFederation:
    """Federate queries across multiple GraphQL services."""
    
    def __init__(self):
        self.services: Dict[str, Dict] = {}
        self.schema_registry: Dict[str, Any] = {}
    
    def register_service(self, name: str, url: str, schema: Dict) -> None:
        self.services[name] = {
            "url": url,
            "schema": schema,
            "client": GraphQLClient(url)
        }
        self.schema_registry[name] = schema
    
    async def execute(self, query: str, variables: Dict = None) -> Dict:
        plan = self._create_execution_plan(query)
        
        results = {}
        errors = []
        
        for service_name, service_query in plan.items():
            try:
                client = self.services[service_name]["client"]
                result = await client.execute(service_query, variables)
                results[service_name] = result
            except Exception as e:
                errors.append({"service": service_name, "error": str(e)})
        
        return self._merge_results(results, errors)
    
    def _create_execution_plan(self, query: str) -> Dict[str, str]:
        plan = {}
        # Parse query and route to appropriate services
        # Simplified for example
        for service_name, schema in self.schema_registry.items():
            if self._query_matches_schema(query, schema):
                plan[service_name] = query
        return plan
    
    async def _merge_results(self, results: Dict, errors: List) -> Dict:
        # Merge results from multiple services
        pass
```

---

## 4. Webhook Management

### Reliable Webhook System

```python
import hmac
import hashlib
import json
from typing import Dict, Any, List, Optional
import asyncio
import aiohttp

class WebhookManager:
    """Management system for outgoing webhooks."""
    
    def __init__(self, retry_count: int = 3, timeout: int = 30):
        self.retry_count = retry_count
        self.timeout = timeout
        self.delivery_log: List[Dict] = []
    
    async def deliver(self, url: str, payload: Dict, 
                      secret: str, signature: str = None) -> bool:
        """Deliver webhook with retry logic."""
        if signature and not self._verify_signature(payload, secret, signature):
            raise ValueError("Invalid signature")
        
        for attempt in range(self.retry_count):
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        url,
                        json=payload,
                        timeout=self.timeout,
                        headers={"Content-Type": "application/json"}
                    )
                self.delivery_log.append({
                    "url": url,
                    "status": "success",
                    "attempt": attempt + 1
                })
                return True
            except Exception as e:
                self.delivery_log.append({
                    "url": url,
                    "status": "failed",
                    "attempt": attempt + 1,
                    "error": str(e)
                })
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return False
    
    def _verify_signature(self, payload: Dict, secret: str, 
                          signature: str) -> bool:
        expected = hmac.new(
            secret.encode(),
            json.dumps(payload).encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

class WebhookEndpoint:
    """Incoming webhook handler with security."""
    
    def __init__(self, secret: str):
        self.secret = secret
        self.allowed_ips: List[str] = []
    
    async def handle(self, request: Dict) -> Dict:
        # Verify signature
        signature = request.get("headers", {}).get("X-Hub-Signature-256")
        if not signature or not self._verify_signature(request["body"], signature):
            return {"error": "Invalid signature", "status": 401}
        
        # Verify IP allowlist (if configured)
        client_ip = request.get("client_ip")
        if self.allowed_ips and client_ip not in self.allowed_ips:
            return {"error": "IP not allowed", "status": 403}
        
        # Queue for processing
        await self._queue_webhook(request)
        return {"status": "accepted"}
```

---

## 5. Streaming Integrations

### Real-time Data Streaming

```python
import asyncio
from typing import AsyncGenerator, Callable, Any, Set
import aiohttp

class StreamingClient:
    """Client for streaming LLM responses and data."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.active_streams: Set[str] = set()
    
    async def stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream LLM completion responses."""
        stream_id = f"stream_{int(time.time())}"
        self.active_streams.add(stream_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json={"messages": [{"role": "user", "content": prompt}], 
                          "stream": True},
                    headers=self.headers
                ) as resp:
                    async for line in resp.content:
                        if stream_id not in self.active_streams:
                            break
                        yield self._parse_stream_line(line.decode())
        finally:
            self.active_streams.discard(stream_id)
    
    def _parse_stream_line(self, line: str) -> str:
        if line.startswith("data: "):
            data = json.loads(line[6:])
            return data.get("content", "")
        return ""

class WebSocketIntegration:
    """WebSocket-based real-time integration."""
    
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.ws = None
        self.subscribers = []
    
    async def connect(self) -> None:
        self.ws = await websockets.connect(self.ws_url)
        asyncio.create_task(self._listen())
    
    async def _listen(self) -> None:
        async for message in self.ws:
            data = json.loads(message)
            for subscriber in self.subscribers:
                await subscriber(data)
    
    async def send(self, event: str, data: Any) -> None:
        if self.ws and not self.ws.closed:
            await self.ws.send(json.dumps({"event": event, "data": data}))
```

---

## 6. Event-Driven Integration

### Event Bus Implementation

```python
from typing import Callable, Dict, Any, List
from enum import Enum
import asyncio

class EventType(Enum):
    TOOL_CALL = "tool_call"
    MODEL_RESPONSE = "model_response"
    STATE_CHANGE = "state_change"

class EventBus:
    """Event-driven communication between agents and services."""
    
    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def publish(self, event_type: EventType, payload: Any) -> None:
        event = {"type": event_type, "payload": payload, "timestamp": time.time()}
        await self.event_queue.put(event)
    
    async def start_processing(self) -> None:
        while True:
            event = await self.event_queue.get()
            handlers = self.handlers.get(event["type"], [])
            for handler in handlers:
                try:
                    await handler(event["payload"])
                except Exception as e:
                    logger.error(f"Event handler error: {e}")

class EventPatternMatcher:
    """Match and route events based on patterns."""
    
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.patterns: List[Dict] = []
    
    def add_pattern(self, event_type: EventType, 
                    pattern: Callable[[Any], bool], 
                    handler: Callable) -> None:
        self.patterns.append({
            "type": event_type,
            "pattern": pattern,
            "handler": handler
        })
    
    async def process_event(self, event: Dict) -> None:
        for pattern_config in self.patterns:
            if event["type"] == pattern_config["type"]:
                if pattern_config["pattern"](event["payload"]):
                    await pattern_config["handler"](event["payload"])
```

---

## 7. Rate Limiting Gateway

### Multi-Level Rate Limiting

```python
import time
from collections import defaultdict
from typing import Dict

class TokenBucketRateLimiter:
    """Token bucket algorithm for rate limiting."""
    
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.buckets: Dict[str, Dict] = defaultdict(
            lambda: {"tokens": capacity, "last_update": time.time()}
        )
    
    def allow(self, key: str, tokens: float = 1) -> bool:
        bucket = self.buckets[key]
        now = time.time()
        
        # Refill tokens
        elapsed = now - bucket["last_update"]
        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + elapsed * self.rate
        )
        bucket["last_update"] = now
        
        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return True
        return False

class AdaptiveRateLimiter:
    """Adaptive rate limiting based on service health."""
    
    def __init__(self, base_rate: int = 100):
        self.base_rate = base_rate
        self.current_rates: Dict[str, int] = defaultdict(lambda: base_rate)
        self.error_counts: Dict[str, int] = defaultdict(int)
    
    def allow(self, key: str) -> bool:
        rate = self.current_rates[key]
        bucket = self.buckets[key]
        
        # Reduce rate on errors
        if self.error_counts[key] > 10:
            rate = max(1, rate // 2)
            self.current_rates[key] = rate
        
        return self._check_bucket(key, rate)
    
    def record_error(self, key: str) -> None:
        self.error_counts[key] += 1
```

---

## 8. API Versioning Strategy

### Semantic Versioning for APIs

```python
from typing import Dict, Any, Optional

class APIVersionManager:
    """Manage API versions and backwards compatibility."""
    
    def __init__(self):
        self.versions: Dict[str, Dict] = {}
        self.deprecations: Dict[str, str] = {}
    
    def register_version(self, version: str, handlers: Dict, 
                         deprecation_date: str = None) -> None:
        self.versions[version] = handlers
        if deprecation_date:
            self.deprecations[version] = deprecation_date
    
    def route_request(self, request: Dict) -> Dict:
        version = request.get("headers", {}).get("X-API-Version", "v1")
        
        if version in self.deprecations:
            logger.warning(f"API version {version} is deprecated")
        
        handlers = self.versions.get(version)
        if not handlers:
            raise ValueError(f"Unknown API version: {version}")
        
        endpoint = request["path"]
        handler = handlers.get(endpoint)
        
        return {"handler": handler, "version": version}
```

---

## 9. Integration Testing Patterns

### Contract Testing

```python
import pytest
from unittest.mock import Mock, AsyncMock

class IntegrationTestSuite:
    """Comprehensive integration testing utilities."""
    
    def __init__(self, api_client, mock_server):
        self.api = api_client
        self.mocks = mock_server
    
    @pytest.mark.asyncio
    async def test_api_contract(self, endpoint: str, expected_schema: Dict) -> None:
        """Verify API returns expected schema."""
        self.mocks.expect(endpoint, method="GET").and_return({
            "status": 200,
            "body": {"data": "test"}
        })
        
        response = await self.api.get(endpoint)
        assert response.status == 200
        assert self._validate_schema(response.body, expected_schema)
    
    def _validate_schema(self, data: Any, schema: Dict) -> bool:
        # Validate against expected schema
        pass
```

---

## 11. Schema Registry Integration

### Schema-Based Message Contracts

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
import jsonschema
import json

@dataclass
class SchemaDefinition:
    schema_id: str
    version: str
    definition: Dict
    description: str

class SchemaRegistry:
    """Registry for managing message schemas across services."""
    
    def __init__(self):
        self.schemas: Dict[str, SchemaDefinition] = {}
        self.compatibility_matrix: Dict[str, str] = {}
    
    def register_schema(self, schema_id: str, schema: Dict, 
                       version: str, description: str = "") -> None:
        if schema_id in self.schemas:
            existing = self.schemas[schema_id]
            if not self._check_compatibility(existing.definition, schema):
                raise ValueError(f"Schema {schema_id} is incompatible")
        
        self.schemas[schema_id] = SchemaDefinition(
            schema_id=schema_id,
            version=version,
            definition=schema,
            description=description
        )
    
    def validate_message(self, schema_id: str, message: Dict) -> bool:
        schema_def = self.schemas.get(schema_id)
        if not schema_def:
            raise ValueError(f"Unknown schema: {schema_id}")
        
        try:
            jsonschema.validate(instance=message, schema=schema_def.definition)
            return True
        except jsonschema.ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            return False
    
    def get_schema(self, schema_id: str, version: str = None) -> Optional[Dict]:
        schema_def = self.schemas.get(schema_id)
        if not schema_def:
            return None
        
        if version and schema_def.version != version:
            # Find compatible version
            for sid, sdef in self.schemas.items():
                if sdef.schema_id == schema_id:
                    return sdef.definition
        
        return schema_def.definition
    
    def _check_compatibility(self, old_schema: Dict, new_schema: Dict) -> bool:
        try:
            jsonschema.Draft7Validator.check_schema(new_schema)
            return True
        except jsonschema.SchemaError:
            return False

class MessageSerializer:
    """Serialize and deserialize messages with schema validation."""
    
    def __init__(self, registry: SchemaRegistry):
        self.registry = registry
    
    def encode(self, schema_id: str, message: Dict, 
               version: str = None) -> str:
        if not self.registry.validate_message(schema_id, message):
            raise ValidationError("Message does not match schema")
        
        envelope = {
            "schema_id": schema_id,
            "version": version or self.registry.schemas[schema_id].version,
            "payload": message
        }
        return json.dumps(envelope)
    
    def decode(self, raw_message: str) -> Dict:
        envelope = json.loads(raw_message)
        schema_id = envelope["schema_id"]
        payload = envelope["payload"]
        
        if not self.registry.validate_message(schema_id, payload):
            raise ValidationError("Invalid message schema")
        
        return payload

# Usage
registry = SchemaRegistry()
registry.register_schema(
    schema_id="agent.message",
    schema={
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "prompt": {"type": "string", "maxLength": 50000},
            "context": {"type": "object"}
        },
        "required": ["session_id", "prompt"]
    },
    version="1.0",
    description="Agent message request"
)
```

---

## 12. Kafka Streams Integration

### Real-Time Stream Processing

```python
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.abc import ConsumerRebalanceListener
import asyncio
from collections import defaultdict
from typing import Dict, List, Callable, Any
import json

class StreamProcessor:
    """Process agent events as streaming data."""
    
    def __init__(self, bootstrap_servers: List[str], app_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.app_id = app_id
        self.processors: Dict[str, Callable] = {}
        self.state_store: Dict[str, Any] = {}
    
    def register_processor(self, topic_pattern: str, handler: Callable):
        self.processors[topic_pattern] = handler
    
    async def start(self):
        consumer = AIOKafkaConsumer(
            *self.processors.keys(),
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.app_id,
            auto_offset_reset="latest",
            enable_auto_commit=False
        )
        
        await consumer.start()
        
        try:
            async for msg in consumer:
                topic = msg.topic
                handler = self.processors.get(topic)
                if handler:
                    try:
                        payload = json.loads(msg.value)
                        result = await handler(payload)
                        await consumer.commit()
                    except Exception as e:
                        logger.error(f"Stream processing failed: {e}")
        finally:
            await consumer.stop()

class AgentEventStream:
    """High-level agent event streaming."""
    
    def __init__(self, bootstrap_servers: List[str]):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
    
    async def start(self):
        await self.producer.start()
    
    async def stop(self):
        await self.producer.stop()
    
    async def emit(self, topic: str, event_type: str, 
                   payload: Dict, key: str = None):
        message = {
            "event": event_type,
            "data": payload,
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.app_id
        }
        
        await self.producer.send_and_wait(
            topic=topic,
            value=message,
            key=key.encode() if key else None
        )

class StatefulStreamProcessor(StreamProcessor):
    """Stream processor with state management."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_states: Dict[str, Dict] = defaultdict(dict)
        self.checkpoint_interval = 1000
        self.message_count = 0
    
    async def process_with_state(self, session_id: str, 
                                 payload: Dict) -> Dict:
        state = self.session_states[session_id]
        
        state["message_count"] = state.get("message_count", 0) + 1
        state["last_activity"] = datetime.utcnow().isoformat()
        state.setdefault("messages", []).append(payload)
        
        if state["message_count"] % self.checkpoint_interval == 0:
            await self._checkpoint(session_id)
        
        return state
    
    async def _checkpoint(self, session_id: str):
        state = self.session_states[session_id]
        await self._persist_state(session_id, state)
        logger.info(f"State checkpointed for {session_id}")
    
    async def _persist_state(self, session_id: str, state: Dict):
        pass  # Implementation depends on storage backend
```

---

## 13. Redis Pub/Sub Pattern

### Real-Time Agent Coordination

```python
import redis.asyncio as aioredis
import json
import asyncio
from typing import Dict, List, Callable, Set
from dataclasses import dataclass

@dataclass
class AgentMessage:
    agent_id: str
    task: str
    payload: Dict
    timestamp: float

class RedisPubSubAgent:
    """Coordinates multiple agents via Redis pub/sub."""
    
    def __init__(self, redis_url: str, agent_id: str):
        self.redis = aioredis.from_url(redis_url)
        self.agent_id = agent_id
        self.pubsub = None
        self.subscriptions: Set[str] = set()
        self.handlers: Dict[str, Callable] = {}
    
    async def connect(self):
        self.pubsub = self.redis.pubsub()
    
    async def subscribe(self, channel: str, handler: Callable):
        self.subscriptions.add(channel)
        self.handlers[channel] = handler
        await self.pubsub.subscribe(channel)
        asyncio.create_task(self._listen())
    
    async def _listen(self):
        async for message in self.pubsub.listen():
            if message["type"] != "message":
                continue
            
            channel = message["channel"].decode()
            handler = self.handlers.get(channel)
            
            if handler:
                try:
                    data = json.loads(message["data"])
                    await handler(data)
                except Exception as e:
                    logger.error(f"Handler error: {e}")
    
    async def publish(self, channel: str, message: Dict):
        await self.redis.publish(channel, json.dumps(message))
    
    async def broadcast_task(self, task: str, payload: Dict):
        message = AgentMessage(
            agent_id=self.agent_id,
            task=task,
            payload=payload,
            timestamp=time.time()
        )
        await self.publish("agent:broadcast", message.__dict__)

class DistributedLock:
    """Distributed locking via Redis."""
    
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis
    
    async def acquire(self, lock_key: str, timeout: int = 30) -> bool:
        result = await self.redis.set(
            f"lock:{lock_key}",
            "1",
            nx=True,
            ex=timeout
        )
        return result is True
    
    async def release(self, lock_key: str):
        await self.redis.delete(f"lock:{lock_key}")
    
    async def with_lock(self, lock_key: str, timeout: int = 30):
        lock = DistributedLock(self.redis)
        acquired = await lock.acquire(lock_key, timeout)
        if not acquired:
            raise LockAcquisitionError(f"Could not acquire lock: {lock_key}")
        try:
            yield
        finally:
            await lock.release(lock_key)

class RateLimiterRedis:
    """Redis-based sliding window rate limiter."""
    
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis
    
    async def is_allowed(self, key: str, limit: int, 
                         window: int) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        
        pipe.zremrangebyscore(key, 0, now - window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window)
        
        results = await pipe.execute()
        current_count = results[2]
        
        return current_count < limit
```

---

## 14. Observability & Tracing

### Distributed Tracing for Agent Workflows

```python
import uuid
import time
from contextvars import ContextVar
from typing import Dict, Any, Optional
import opentelemetry.api
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=14268,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)
trace_context: ContextVar[Dict] = ContextVar("trace_context", default={})

class TracedAgent:
    """Wrapper adding tracing to agent operations."""
    
    def __init__(self, agent, service_name: str = "agent-service"):
        self.agent = agent
        self.service_name = service_name
        self.tracer = trace.get_tracer(service_name)
    
    async def process(self, prompt: str, session_id: str, 
                      context: Dict = None) -> str:
        ctx = trace_context.get()
        parent_span = trace.get_current_span()
        
        with self.tracer.start_as_current_span("agent.process") as span:
            span.set_attribute("session_id", session_id)
            span.set_attribute("prompt_length", len(prompt))
            span.set_attribute("service.name", self.service_name)
            
            if context:
                span.set_attribute("context.keys", list(context.keys()))
            
            # Add events
            span.add_event("starting_agent_processing")
            
            start_time = time.time()
            
            try:
                result = await self.agent.process(prompt, session_id, context)
                duration = time.time() - start_time
                
                span.set_attribute("duration_ms", duration * 1000)
                span.set_attribute("status", "success")
                span.add_event("agent_processing_completed")
                
                return result
            
            except Exception as e:
                span.set_attribute("status", "error")
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                span.record_exception(e)
                raise

class MetricCollector:
    """Collect and export metrics."""
    
    def __init__(self):
        self.request_count = Counter(
            "agent_requests_total",
            "Total requests",
            ["endpoint", "status"]
        )
        self.latency = Histogram(
            "agent_latency_seconds",
            "Request latency",
            ["endpoint"]
        )
        self.active_sessions = Gauge(
            "agent_active_sessions",
            "Active sessions"
        )
    
    def record_request(self, endpoint: str, status: str, 
                       duration: float):
        self.request_count.labels(
            endpoint=endpoint, status=status
        ).inc()
        self.latency.labels(endpoint=endpoint).observe(duration)
    
    def increment_sessions(self):
        self.active_sessions.inc()
    
    def decrement_sessions(self):
        self.active_sessions.dec()
```

---

## 15. Multi-Tenant Integration

### Isolated Tenant Configurations

```python
from typing import Dict, Optional
from dataclasses import dataclass, field
import asyncio

@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    api_keys: List[str]
    rate_limit: int
    model_preferences: Dict
    webhook_endpoints: List[str]
    enabled: bool = True
    context: Dict = field(default_factory=dict)

class MultiTenantIntegration:
    """Manage integrations for multiple tenants."""
    
    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.tenant_agents: Dict[str, Any] = {}
        self.default_config = TenantConfig(
            tenant_id="default",
            name="Default Tenant",
            api_keys=[],
            rate_limit=100,
            model_preferences={},
            webhook_endpoints=[]
        )
    
    def register_tenant(self, config: TenantConfig):
        self.tenants[config.tenant_id] = config
        self.tenant_agents[config.tenant_id] = self._create_tenant_agent(config)
    
    def _create_tenant_agent(self, config: TenantConfig):
        agent = Agent(config.model_preferences)
        agent.rate_limit = config.rate_limit
        agent.webhook_endpoints = config.webhook_endpoints
        return agent
    
    async def route_request(self, api_key: str, 
                            request: Dict) -> Dict:
        tenant = self._resolve_tenant(api_key)
        if not tenant or not tenant.enabled:
            raise AuthenticationError("Invalid or disabled tenant")
        
        agent = self.tenant_agents[tenant.tenant_id]
        
        enriched_request = {
            **request,
            "tenant_id": tenant.tenant_id,
            "context": {
                **request.get("context", {}),
                "tenant": tenant.name,
                "tenant_config": tenant.context
            }
        }
        
        if "session_id" not in enriched_request:
            enriched_request["session_id"] = f"{tenant.tenant_id}_{uuid.uuid4()}"
        
        return await agent.process(
            enriched_request["prompt"],
            enriched_request["session_id"],
            enriched_request.get("context")
        )
    
    def _resolve_tenant(self, api_key: str) -> Optional[TenantConfig]:
        for tenant in self.tenants.values():
            if api_key in tenant.api_keys:
                return tenant
        
        if api_key in self.default_config.api_keys:
            return self.default_config
        
        return None
    
    async def notify_all_tenants(self, event: str, payload: Dict):
        tasks = []
        for tenant in self.tenants.values():
            if not tenant.webhook_endpoints:
                continue
            
            for endpoint in tenant.webhook_endpoints:
                tasks.append(self._send_webhook(endpoint, event, payload))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

class TenantRateLimiter:
    """Per-tenant rate limiting."""
    
    def __init__(self):
        self.limits: Dict[str, Dict] = {}
        self.usage: Dict[str, Dict] = defaultdict(lambda: {
            "minute": {"count": 0, "reset": time.time() + 60},
            "hour": {"count": 0, "reset": time.time() + 3600}
        })
    
    def set_limit(self, tenant_id: str, per_minute: int, per_hour: int):
        self.limits[tenant_id] = {
            "minute": per_minute,
            "hour": per_hour
        }
    
    def check(self, tenant_id: str) -> bool:
        if tenant_id not in self.limits:
            return True
        
        limits = self.limits[tenant_id]
        usage = self.usage[tenant_id]
        
        now = time.time()
        for period in ["minute", "hour"]:
            if now >= usage[period]["reset"]:
                usage[period]["count"] = 0
                usage[period]["reset"] = now + (60 if period == "minute" else 3600)
            
            if usage[period]["count"] >= limits[period]:
                return False
            
            usage[period]["count"] += 1
        
        return True
```

---

## 16. Content Moderation Gateway

### Safety Layer for Agent I/O

```python
from typing import Dict, Any, List, Callable
import re

class ContentModerationGateway:
    """Filter and moderate content entering/leaving agent."""
    
    def __init__(self):
        self.input_filters: List[Callable] = []
        self.output_filters: List[Callable] = []
        self.blocked_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in [
                r"password\s*[:=]\s*\S+",
                r"api[_-]?key\s*[:=]\s*\S+",
                r"secret\s*[:=]\s*\S+",
                r"(?i)drop\s+table",
                r"(?i)delete\s+from",
                r"(?i)exec\s*\(",
            ]
        ]
    
    def add_input_filter(self, filter_fn: Callable):
        self.input_filters.append(filter_fn)
    
    def add_output_filter(self, filter_fn: Callable):
        self.output_filters.append(filter_fn)
    
    async def process_input(self, prompt: str, 
                            context: Dict) -> Dict:
        for pattern in self.blocked_patterns:
            if pattern.search(prompt):
                raise ContentPolicyError("Input blocked by moderation")
        
        for filter_fn in self.input_filters:
            prompt = await filter_fn(prompt)
        
        return {"prompt": prompt, "context": context}
    
    async def process_output(self, response: str, 
                             session_id: str) -> str:
        for pattern in self.blocked_patterns:
            if pattern.search(response):
                logger.warning(f"Output blocked for {session_id}")
                return "Response was blocked by content policy."
        
        for filter_fn in self.output_filters:
            response = await filter_fn(response)
        
        return response

class PIIFilter:
    """Detect and redact PII."""
    
    def __init__(self):
        self.patterns = {
            "email": re.compile(r'[\w\.-]+@[\w\.-]+\.\w+'),
            "phone": re.compile(r'\+?[\d\s\-\(\)]{10,}'),
            "ssn": re.compile(r'\d{3}-\d{2}-\d{4}'),
            "credit_card": re.compile(r'\d{4}[\s\-]\d{4}[\s\-]\d{4}[\s\-]\d{4}')
        }
    
    async def filter(self, text: str) -> str:
        for pii_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                logger.warning(f"PII detected: {pii_type} - {matches}")
                text = pattern.sub(f"[REDACTED_{pii_type.upper()}]", text)
        return text

class TokenBudgetFilter:
    """Manage token usage budgets."""
    
    def __init__(self, tokenizer, max_tokens: int = 4096):
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.reserved_output = 500
        self.max_input_tokens = max_tokens - reserved_output
    
    async def filter(self, prompt: str, context: Dict) -> str:
        tokens = self.tokenizer.encode(prompt)
        
        if len(tokens) > self.max_input_tokens:
            prompt = self.tokenizer.decode(tokens[:self.max_input_tokens])
            logger.warning(f"Prompt truncated from {len(tokens)} to {self.max_input_tokens} tokens")
        
        return prompt
```

---

## 17. gRPC Service Mesh

### Production gRPC Deployment

```python
import grpc
from grpc import aio
from prometheus_client import Counter, Histogram
from typing import AsyncIterator

REQUEST_COUNT = Counter(
    "grpc_requests_total",
    "Total gRPC requests",
    ["service", "method"]
)
REQUEST_LATENCY = Histogram(
    "grpc_request_duration_seconds",
    "gRPC request duration",
    ["service", "method"]
)

class AgentGRPCService:
    """gRPC service with interceptors and observability."""
    
    def __init__(self, agent):
        self.agent = agent
        self.server = None
    
    async def start(self, port: int = 50051):
        self.server = aio.server()
        
        interceptors = [
            self._create_metrics_interceptor(),
            self._create_auth_interceptor(),
            self._create_rate_limit_interceptor()
        ]
        
        self.server = aio.server(interceptors=interceptors)
        
        agent_pb2_grpc.add_AgentServiceServicer_to_server(
            AgentServicer(self.agent), self.server
        )
        
        self.server.add_insecure_port(f"[::]:{port}")
        await self.server.start()
        logger.info(f"gRPC server started on port {port}")
        
        await self.server.wait_for_termination()
    
    async def stop(self, grace: int = 5):
        if self.server:
            await self.server.stop(grace)
    
    def _create_metrics_interceptor(self):
        class MetricsInterceptor(aio.ServerInterceptor):
            async def intercept_service(self, continuation, handler_call_details):
                start = time.time()
                method = handler_call_details.method.split("/")[-1]
                
                try:
                    response = await continuation(handler_call_details)
                    REQUEST_COUNT.labels(
                        service="agent", method=method
                    ).inc()
                    return response
                except Exception:
                    REQUEST_COUNT.labels(
                        service="agent", method=method
                    ).inc()
                    raise
        
        return MetricsInterceptor()

class LoadBalancedGRPCClient:
    """Client with load balancing for gRPC."""
    
    def __init__(self, targets: List[str]):
        self.targets = targets
        self.channels = [
            grpc.aio.insecure_channel(target)
            for target in targets
        ]
    
    async def process(self, request, 
                      session_factory) -> AsyncIterator:
        channel = self._select_channel()
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        
        async for response in stub.Stream(request):
            yield response
    
    def _select_channel(self):
        import random
        return random.choice(self.channels)

class BidirectionalStreamHandler:
    """Handle bidirectional streaming."""
    
    def __init__(self, agent):
        self.agent = agent
        self.active_streams: Dict[str, Any] = {}
    
    async def stream(self, request_iterator):
        stream_id = str(uuid.uuid4())
        
        async def process_requests():
            async for request in request_iterator:
                try:
                    result = await self.agent.process(
                        request.prompt,
                        request.session_id,
                        json.loads(request.context)
                    )
                    yield agent_pb2.ProcessResponse(
                        response=result,
                        session_id=request.session_id
                    )
                except Exception as e:
                    yield agent_pb2.ErrorResponse(
                        error=str(e),
                        code="INTERNAL"
                    )
        
        self.active_streams[stream_id] = process_requests()
        try:
            async for response in self.active_streams[stream_id]:
                yield response
        finally:
            del self.active_streams[stream_id]
```

---

## 18. Request Correlation & Distributed Tracing

### Trace Propagation Across Services

```python
import uuid
import time
from contextvars import ContextVar
from typing import Dict, Any, Optional
import json
import httpx

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")
span_id_var: ContextVar[str] = ContextVar("span_id", default="")
parent_span_id_var: ContextVar[str] = ContextVar("parent_span_id", default="")

class TraceContext:
    """Manage trace context across service boundaries."""
    
    @staticmethod
    def create() -> Dict[str, str]:
        return {
            "trace_id": uuid.uuid4().hex,
            "span_id": uuid.uuid4().hex[:16],
            "parent_span_id": ""
        }
    
    @staticmethod
    def from_dict(data: Dict[str, str]):
        trace_id_var.set(data.get("trace_id", ""))
        span_id_var.set(data.get("span_id", ""))
        parent_span_id_var.set(data.get("parent_span_id", ""))
    
    @staticmethod
    def to_dict() -> Dict[str, str]:
        return {
            "trace_id": trace_id_var.get(""),
            "span_id": span_id_var.get(""),
            "parent_span_id": parent_span_id_var.get("")
        }
    
    @staticmethod
    def child_span() -> Dict[str, str]:
        return {
            "trace_id": trace_id_var.get(""),
            "span_id": uuid.uuid4().hex[:16],
            "parent_span_id": span_id_var.get("")
        }

class TracedHTTPClient:
    """HTTP client with automatic trace propagation."""
    
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def request(self, method: str, url: str, **kwargs):
        headers = kwargs.pop("headers", {})
        
        trace_ctx = TraceContext.to_dict()
        if trace_ctx.get("trace_id"):
            headers.update({
                "X-Trace-Id": trace_ctx["trace_id"],
                "X-Span-Id": trace_ctx["span_id"],
                "X-Parent-Span-Id": trace_ctx.get("parent_span_id", "")
            })
        
        kwargs["headers"] = headers
        
        start = time.time()
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        finally:
            duration = time.time() - start
            logger.info(
                "http_request_completed",
                url=url,
                method=method,
                duration=duration,
                trace_id=trace_ctx.get("trace_id")
            )

class RequestCorrelationMiddleware:
    """Correlate incoming requests with traces."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))
        
        trace_id = (
            headers.get(b"x-trace-id", b"").decode() or
            uuid.uuid4().hex
        )
        span_id = uuid.uuid4().hex[:16]
        
        trace_id_var.set(trace_id)
        span_id_var.set(span_id)
        
        scope["trace"] = {
            "trace_id": trace_id,
            "span_id": span_id
        }
        
        await self.app(scope, receive, send)
```

---

## 19. Service Catalog & Discovery

### Dynamic Service Discovery

```python
from typing import Dict, List, Optional
import asyncio
import aiohttp
from datetime import datetime, timedelta

class ServiceInstance:
    def __init__(self, service_id: str, host: str, port: int,
                 health_path: str = "/health", weight: int = 1):
        self.service_id = service_id
        self.host = host
        self.port = port
        self.health_path = health_path
        self.weight = weight
        self.healthy = True
        self.last_check = datetime.utcnow()
        self.latency_ms = 0
    
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"
    
    async def health_check(self, timeout: float = 5.0) -> bool:
        try:
            start = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.url}{self.health_path}",
                    timeout=timeout
                ) as response:
                    self.latency_ms = (time.time() - start) * 1000
                    self.last_check = datetime.utcnow()
                    self.healthy = response.status == 200
                    return self.healthy
        except Exception:
            self.healthy = False
            return False

class ServiceCatalog:
    """Central service catalog with health monitoring."""
    
    def __init__(self, check_interval: int = 30):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.check_interval = check_interval
        self.running = False
    
    def register(self, service_id: str, instance: ServiceInstance):
        if service_id not in self.services:
            self.services[service_id] = []
        self.services[service_id].append(instance)
    
    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        return [i for i in self.services.get(service_id, []) if i.healthy]
    
    def get_instance(self, service_id: str) -> Optional[ServiceInstance]:
        instances = self.get_instances(service_id)
        if not instances:
            return None
        return min(instances, key=lambda i: i.latency_ms)
    
    async def start_health_checks(self):
        self.running = True
        while self.running:
            for instances in self.services.values():
                tasks = [i.health_check() for i in instances]
                await asyncio.gather(*tasks, return_exceptions=True)
            
            await asyncio.sleep(self.check_interval)
    
    async def stop(self):
        self.running = False

class LoadBalancer:
    """Round-robin load balancer with health checks."""
    
    def __init__(self, catalog: ServiceCatalog):
        self.catalog = catalog
        self.counters: Dict[str, int] = {}
    
    async def route(self, service_id: str) -> Optional[str]:
        instances = self.catalog.get_instances(service_id)
        if not instances:
            return None
        
        if service_id not in self.counters:
            self.counters[service_id] = 0
        
        instance = instances[self.counters[service_id] % len(instances)]
        self.counters[service_id] += 1
        
        return instance.url
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)