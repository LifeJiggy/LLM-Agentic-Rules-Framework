# Development Domain - Examples

## Overview

This document provides concrete code examples for implementing development best practices in LLM/agentic systems, including dependency injection, event handling, repository patterns, testing strategies, and configuration management.

---

## Example 1: Clean Agent Architecture

```python
from abc import ABC, abstractmethod
from typing import Protocol, Optional, Dict, Any, List
import asyncio


class ModelClient(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...


class ToolRegistry(Protocol):
    def execute(self, tool_name: str, args: Dict) -> Any: ...


class EventBus(Protocol):
    def publish(self, event: str, data: Any) -> None: ...


class AgentCore:
    def __init__(
        self,
        model: ModelClient,
        tools: ToolRegistry,
        bus: EventBus,
        config: Optional[Dict] = None
    ):
        self.model = model
        self.tools = tools
        self.bus = bus
        self.config = config or {}

    def process(self, prompt: str, context: Optional[Dict] = None) -> str:
        self.bus.publish("agent.started", {"prompt": prompt})
        try:
            validated = self._validate(prompt)
            structured = self.model.generate(validated, **self.config.get("model_options", {}))
            self.bus.publish("agent.completed", {"prompt": prompt, "response": structured})
            return structured
        except Exception as e:
            self.bus.publish("agent.error", {"prompt": prompt, "error": str(e)})
            raise

    def _validate(self, prompt: str) -> str:
        if len(prompt) > self.config.get("max_length", 4000):
            raise ValueError("Prompt too long")
        return prompt


class AgentOrchestrator:
    def __init__(self, agent: AgentCore, planner: Any):
        self.agent = agent
        self.planner = planner

    async def run(self, task: str) -> str:
        plan = self.planner.plan(task)
        results = []
        for step in plan.steps:
            if step.type == "prompt":
                result = self.agent.process(step.content)
            elif step.type == "tool":
                result = self.agent.tools.execute(step.tool_name, step.args)
            results.append(result)
        return self._synthesize(results)

    def _synthesize(self, results: List[str]) -> str:
        return "\n".join(str(r) for r in results if r)
```

---

## Example 2: Dependency Injection Container

```python
class Container:
    def __init__(self):
        self._services = {}
        self._factories = {}

    def register(self, name: str, service, singleton: bool = False):
        if singleton:
            self._services[name] = service
        else:
            self._factories[name] = service

    def resolve(self, name: str):
        if name in self._services:
            return self._services[name]
        if name in self._factories:
            return self._factories[name]()
        raise KeyError(f"Service {name} not found")


container = Container()
container.register("model", lambda: OpenAIClient(api_key=os.environ["OPENAI_KEY"]), singleton=True)
container.register("tools", ToolRegistry, singleton=True)
container.register("bus", EventBus, singleton=True)
container.register("agent", lambda: AgentCore(
    model=container.resolve("model"),
    tools=container.resolve("tools"),
    bus=container.resolve("bus")
))
```

---

## Example 3: Event-Driven Agent System

```python
class EventBus:
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event: str, handler):
        self._handlers.setdefault(event, []).append(handler)

    def publish(self, event: str, data):
        for handler in self._handlers.get(event, []):
            handler(data)


class AgentEventManager:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self._register_handlers()

    def _register_handlers(self):
        self.bus.subscribe("user.message", self._handle_user_message)
        self.bus.subscribe("agent.thinking", self._log_thinking)
        self.bus.subscribe("agent.response", self._log_response)

    def _handle_user_message(self, data):
        print(f"Received: {data.get('content')}")

    def _log_thinking(self, data):
        pass

    def _log_response(self, data):
        print(f"Response: {data.get('response')}")
```

---

## 4. Repository Pattern for Agent Memory

### 4.1 Abstract Repository

```python
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import asyncio


class AgentMemoryRepository(ABC):
    @abstractmethod
    async def save_interaction(self, session_id: str, user_input: str, agent_output: str) -> None: ...

    @abstractmethod
    async def get_context(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]: ...

    @abstractmethod
    async def clear_session(self, session_id: str) -> None: ...


class RedisAgentMemory(AgentMemoryRepository):
    def __init__(self, redis_client):
        self.redis = redis_client
        self._max_context = 100

    async def save_interaction(self, session_id: str, user_input: str, agent_output: str) -> None:
        message = {
            "user": user_input,
            "assistant": agent_output,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.redis.lpush(f"session:{session_id}:messages", json.dumps(message))
        await self.redis.ltrim(f"session:{session_id}:messages", 0, self._max_context - 1)

    async def get_context(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        messages = await self.redis.lrange(f"session:{session_id}:messages", 0, limit - 1)
        return [json.loads(m) for m in reversed(messages)]

    async def clear_session(self, session_id: str) -> None:
        await self.redis.delete(f"session:{session_id}:messages")
```

---

## 5. Circuit Breaker Pattern for Model Calls

```python
import asyncio
import time
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_retry():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _should_retry(self) -> bool:
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _on_success(self) -> None:
        self.failures = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN


class ModelCircuitBreaker:
    def __init__(self, breaker: CircuitBreaker, model_client):
        self.breaker = breaker
        self.model = model_client

    async def generate(self, prompt: str, **kwargs) -> str:
        return await self.breaker.call(self.model.generate, prompt, **kwargs)
```

---

## 6. Rate Limiter Implementation

```python
import time
import threading
from collections import defaultdict
from typing import Dict, Optional


class TokenBucketRateLimiter:
    def __init__(self, tokens_per_second: float, max_tokens: int):
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.buckets: Dict[str, float] = {}
        self.last_update: Dict[str, float] = {}
        self._lock = threading.Lock()

    def consume(self, key: str, tokens: int = 1) -> bool:
        with self._lock:
            now = time.time()
            if key not in self.buckets:
                self.buckets[key] = self.max_tokens
                self.last_update[key] = now
            else:
                elapsed = now - self.last_update[key]
                self.buckets[key] = min(
                    self.max_tokens,
                    self.buckets[key] + elapsed * self.tokens_per_second
                )
                self.last_update[key] = now

            if self.buckets[key] >= tokens:
                self.buckets[key] -= tokens
                return True
            return False


class RateLimitedAgent:
    def __init__(self, limiter: TokenBucketRateLimiter):
        self.limiter = limiter

    async def process(self, session_id: str, prompt: str) -> str:
        if not self.limiter.consume(f"agent:{session_id}", 100):
            raise RateLimitError("Rate limit exceeded")
        return await self._process(prompt)
```

---

## 7. Testing Double for Agent Components

```python
class FakeModelClient:
    def __init__(self, predetermined_responses=None):
        self.responses = predetermined_responses or {}
        self.calls = []

    async def generate(self, prompt: str, **kwargs):
        self.calls.append({"prompt": prompt, "kwargs": kwargs})
        response = self.responses.get(prompt, "Default response")
        return response


class SpyToolRegistry:
    def __init__(self):
        self.executed_tools = []

    async def execute(self, tool_name: str, args: dict):
        self.executed_tools.append({"name": tool_name, "args": args})
        return f"Tool {tool_name} executed with {args}"


class TestAgentIntegration:
    def test_multi_turn_conversation(self):
        model = FakeModelClient({"Hello": "Hi!", "How are you": "I'm fine"})
        tools = SpyToolRegistry()
        agent = AgentCore(model=model, tools=tools, bus=Mock())

        r1 = agent.process("Hello")
        r2 = agent.process("How are you")

        assert len(tools.executed_tools) == 0
        assert r1 == "Hi!"
        assert r2 == "I'm fine"
```

---

## 8. Configuration Management Examples

### 8.1 Environment-Aware Configuration

```python
from pydantic import BaseSettings, Field, validator
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AgentConfiguration(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    log_level: str = Field(default="INFO")
    max_input_length: int = Field(default=4000, ge=1, le=50000)
    max_output_tokens: int = Field(default=4096, ge=1, le=100000)
    rate_limit_rpm: int = Field(default=60, ge=1)
    model_temperature: float = Field(default=0.7, ge=0, le=2)
    model_name: str = Field(default="gpt-4")
    cache_ttl_seconds: int = Field(default=300, ge=1)
    timeout_seconds: int = Field(default=30, ge=1, le=300)

    @validator("model_temperature")
    def validate_temperature(cls, v, values):
        if values.get("environment") == Environment.PRODUCTION and v > 1.0:
            raise ValueError("Production use should limit temperature to 1.0")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = AgentConfiguration()
```

### 8.2 Feature Flag Pattern

```python
class FeatureFlags:
    def __init__(self):
        self._flags = {
            "use_new_planner": os.getenv("USE_NEW_PLANNER", "false").lower() == "true",
            "enable_caching": os.getenv("ENABLE_CACHING", "true").lower() == "true",
            "require_mfa": os.getenv("REQUIRE_MFA", "false").lower() == "true",
        }

    def is_enabled(self, feature: str) -> bool:
        return self._flags.get(feature, False)

    def require_true(self, feature: str):
        if not self.is_enabled(feature):
            raise FeatureDisabledError(feature)


flags = FeatureFlags()

def process_with_features(prompt: str) -> str:
    if flags.is_enabled("use_new_planner"):
        return new_planner.process(prompt)
    return legacy_planner.process(prompt)
```

---

## 9. Error Handling Examples

### 9.1 Graceful Degradation Pattern

```python
class FallbackStrategy:
    def __init__(self):
        self.primary = OpenAIModel()
        self.fallback = AnthropicModel()
        self.cache = InMemoryCache()

    async def generate(self, prompt: str) -> str:
        # Try cache first
        cached = self.cache.get(prompt)
        if cached:
            return cached

        # Try primary
        try:
            response = await self.primary.generate(prompt)
            if self._is_good_response(response):
                self.cache.set(prompt, response, ttl=300)
                return response
        except (TimeoutError, RateLimitError) as e:
            logger.warning(f"Primary failed: {e}")

        # Fallback
        try:
            response = await self.fallback.generate(prompt)
            self.cache.set(prompt, response, ttl=300)
            return response
        except Exception as e:
            logger.error(f"Fallback failed: {e}")
            return "Service temporarily unavailable"

    def _is_good_response(self, response: str) -> bool:
        # Basic quality check
        return len(response) > 10 and "error" not in response.lower()
```

### 9.2 Retry with Backoff

```python
import asyncio
import random


async def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0
):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return await func()
        except (TimeoutError, ConnectionError, RateLimitError) as e:
            last_exception = e
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, 0.1 * delay)
            await asyncio.sleep(delay + jitter)
```

---

## 10. Performance Optimization Examples

### 10.1 Streaming Response Handler

```python
async def stream_response(model_client, prompt: str):
    full_response = ""
    async for chunk in model_client.stream(prompt):
        yield chunk
        full_response += chunk
    logger.info(f"Full response length: {len(full_response)}")
    return full_response
```

### 10.2 Connection Pooling

```python
import aiohttp


class PooledHttpClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=100,
                    limit_per_host=10,
                    ttl_dns_cache=300
                )
            )
        return cls._instance

    async def get(self, url: str) -> aiohttp.ClientResponse:
        return await self.session.get(url, timeout=aiohttp.ClientTimeout(total=30))
```

---

## 11. Observability Examples

### 11.1 Structured Logging

```python
import structlog
from opentelemetry import trace


logger = structlog.get_logger()


async def traced_agent_process(prompt: str, session_id: str):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("agent.process") as span:
        span.set_attribute("session_id", session_id)
        span.set_attribute("prompt_length", len(prompt))

        logger.info("agent.processing_started", session_id=session_id)

        try:
            result = await agent.process(prompt)
            span.set_attribute("response_length", len(result))
            logger.info("agent.processing_completed", session_id=session_id)
            return result
        except Exception as e:
            span.record_exception(e)
            logger.error("agent.processing_failed", session_id=session_id, error=str(e))
            raise
```

### 11.2 Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge


class AgentMetrics:
    REQUESTS = Counter("agent_requests_total", "Total agent requests", ["model", "success"])
    DURATION = Histogram("agent_request_duration_seconds", "Request duration", ["model"])
    ACTIVE_SESSIONS = Gauge("agent_active_sessions", "Currently active sessions")

    @classmethod
    def record_request(cls, model: str, duration: float, success: bool):
        cls.REQUESTS.labels(model=model, success=str(success)).inc()
        cls.DURATION.labels(model=model).observe(duration)


def timed_agent_call(model_name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                AgentMetrics.record_request(model_name, time.perf_counter() - start, True)
                return result
            except Exception as e:
                AgentMetrics.record_request(model_name, time.perf_counter() - start, False)
                raise
        return wrapper
    return decorator
```

---

## 12. Advanced Agent Patterns

### 12.1 Retry with Exponential Backoff

```python
import asyncio
import random


async def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0
):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return await func()
        except (TimeoutError, ConnectionError, RateLimitError) as e:
            last_exception = e
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, 0.1 * delay)
            await asyncio.sleep(delay + jitter)


class RetryableModelClient:
    async def generate(self, prompt: str) -> str:
        return await retry_with_backoff(
            lambda: self._call_model(prompt),
            max_retries=3
        )

    async def _call_model(self, prompt: str) -> str:
        # Actual model call
        pass
```

### 12.2 Circuit Breaker for Resilience

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
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
        self.failures = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
```

### 12.3 Context Summarization

```python
class ContextSummarizer:
    def __init__(self, model_client):
        self.model = model_client
        self.max_tokens = 4000
        self.keep_recent = 10

    async def summarize_if_needed(self, messages: List[dict]) -> List[dict]:
        if not self._needs_summarization(messages):
            return messages

        recent = messages[-self.keep_recent:]
        old = messages[:-self.keep_recent]

        summary = await self._summarize_messages(old)
        return [{"role": "system", "content": f"Previous conversation summary: {summary}"}] + recent

    def _needs_summarization(self, messages: List[dict]) -> bool:
        total_tokens = sum(len(m.get("content", "").split()) for m in messages)
        return total_tokens > self.max_tokens

    async def _summarize_messages(self, messages: List[dict]) -> str:
        content = "\n".join(m.get("content", "") for m in messages)
        prompt = f"Summarize this conversation:\n\n{content}"
        return await self.model.generate(prompt)
```

---

## 13. Testing Patterns

### 13.1 Fake Implementations for Testing

```python
class FakeModel:
    def __init__(self, responses=None):
        self.responses = responses or {"default": "Test response"}
        self.calls = []

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.responses.get(prompt, self.responses.get("default", ""))


class FakeToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, func):
        self.tools[name] = func

    def execute(self, name: str, args: dict):
        if name not in self.tools:
            raise ToolNotFoundError(name)
        return self.tools[name](**args)


# Usage in tests
def test_agent_with_fakes():
    model = FakeModel({"Hello": "Hi there!"})
    tools = FakeToolRegistry()
    tools.register("search", lambda q: f"Results for: {q}")
    agent = AgentCore(model=model, tools=tools)
    assert agent.process("Hello") == "Hi there!"
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)