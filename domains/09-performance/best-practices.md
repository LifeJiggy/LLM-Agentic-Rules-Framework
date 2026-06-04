# Performance Domain - Best Practices

## Overview

This document outlines performance best practices for LLM/agentic systems, covering caching, async operations, token optimization, and resource management.

## Table of Contents

1. [Caching Strategy](#1-caching-strategy)
2. [Async Operations](#2-async-operations)
3. [Token Optimization](#3-token-optimization)
4. [Connection Pooling](#4-connection-pooling)
5. [Error Handling and Resilience](#5-error-handling-and-resilience)
6. [Streaming and Progressive Responses](#6-streaming-and-progressive-responses)
7. [Monitoring and Observability](#7-monitoring-and-observability)
8. [Cost Management](#8-cost-management)
9. [Testing Performance](#9-testing-performance)
10. [Memory Management](#10-memory-management)
11. [Rate Limiting and Backpressure](#11-rate-limiting-and-backpressure)
12. [Security and Privacy](#12-security-and-privacy)
13. [Context Management](#13-context-management)
14. [Tool Execution Optimization](#14-tool-execution-optimization)
15. [Provider Integration](#15-provider-integration)
16. [Infrastructure and Deployment](#16-infrastructure-and-deployment)
17. [Team Practices](#17-team-practices)
18. [Performance Reviews](#18-performance-reviews)

---

## 1. Caching Strategy

```python
from functools import lru_cache
import asyncio
import redis.asyncio as redis

class MultiLevelCache:
    """L1 (memory) + L2 (Redis) caching."""
    
    def __init__(self, redis_url: str, default_ttl: int = 300):
        self.l1 = lru_cache(maxsize=1000)
        self.l2 = redis.from_url(redis_url)
        self.default_ttl = default_ttl
    
    async def get(self, key: str):
        # Try L1 first
        value = self.l1.get(key)
        if value is not None:
            return value
        
        # Try L2
        value = await self.l2.get(key)
        if value is not None:
            self.l1.set(key, value)
        
        return value
    
    async def set(self, key: str, value: str) -> None:
        self.l1.set(key, value)
        await self.l2.setex(key, self.default_ttl, value)

# Usage
cache = MultiLevelCache(redis_url="redis://localhost:6379")
result = await cache.get("user_history_123")
```

### Cache Design Principles

Cache at the granularity of actual query patterns. Invalidate on known update events.

Use consistent cache key construction: include model version, prompt version, and system policy in the key.

Prefer write-through for consistency. Use write-behind only when write latency matters more than consistency.

Always set TTLs. A cache without TTL is a memory leak.

### Cache Key Best Practices

```python
class CacheKeyBuilder:
    @staticmethod
    def build(prompt: str, model: str, temperature: float, top_p: float) -> str:
        normalized = CacheKeyBuilder._normalize_prompt(prompt)
        key_components = {
            "model": model,
            "temperature": round(temperature, 2),
            "top_p": round(top_p, 2),
            "prompt": normalized,
        }
        serialized = json.dumps(key_components, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    @staticmethod
    def _normalize_prompt(prompt: str) -> str:
        # collapse whitespace, remove trailing spaces
        return re.sub(r"\s+", " ", prompt.strip()).lower()
```

### Cache Invalidation Patterns

```python
class VersionedCache:
    def __init__(self, cache):
        self.cache = cache
        self.current_version = 1
    
    async def get(self, key: str, version: int):
        if version != self.current_version:
            await self.cache.delete(key)
            return None
        return await self.cache.get(key)
    
    async def invalidate(self):
        await self.cache.flushdb()
        self.current_version += 1
```

### Semantic Key Matching

Use embedding similarity to find near-identical queries. Map semantic matches to the same cache entry until coverage is acceptable.

```python
class SemanticCachePolicy:
    def __init__(self, similarity_fn, threshold: float = 0.97):
        self.similarity_fn = similarity_fn
        self.threshold = threshold
    
    def map_query(self, query: str, existing_queries: List[str]) -> Optional[str]:
        if not existing_queries:
            return None
        for existing in existing_queries:
            sim = self.similarity_fn(query, existing)
            if sim >= self.threshold:
                return existing
        return None
```

---

## 2. Async Operations

```python
import asyncio
from typing import List

class AsyncBatchProcessor:
    """Process multiple requests efficiently."""
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_batch(self, requests: List[str]) -> List[str]:
        tasks = [self._process_one(req) for req in requests]
        return await asyncio.gather(*tasks)
    
    async def _process_one(self, prompt: str) -> str:
        async with self.semaphore:
            return await call_model(prompt)

# Usage
processor = AsyncBatchProcessor(max_concurrent=5)
results = await processor.process_batch(prompts)
```

### Event Loop Best Practices

Do not block the event loop with CPU-heavy work. Offload to thread or process pools.

```python
class CPUOffloaded:
    def __init__(self, executor):
        self.executor = executor
    
    async def run(self, fn, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, fn, *args)
```

### Async-Generator Streaming

```python
async def stream_response(prompt: str) -> AsyncGenerator[str, None]:
    async for chunk in model.stream(prompt):
        yield chunk
```

### Structured Concurrency

Prefer `asyncio.TaskGroup` for structured concurrency. This cancels sibling tasks when one fails, preventing hidden work.

```python
async def parallel_with_taskgroup(tasks: List[Callable]):
    async with asyncio.TaskGroup() as tg:
        return [tg.create_task(task()) for task in tasks]
```

---

## 3. Token Optimization

```python
class TokenOptimizer:
    """Optimize token usage in prompts."""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
    
    def compress_context(self, messages: list) -> list:
        """Reduce context to fit token budget."""
        total = sum(self._count_tokens(m["content"]) for m in messages)
        
        if total <= self.max_tokens:
            return messages
        
        # Prioritize recent and important messages
        return self._summarize_oldest(messages, total)
    
    def _summarize_oldest(self, messages: list, current_tokens: int) -> list:
        keep_tokens = int(self.max_tokens * 0.8)
        keep_chars = keep_tokens * 4
        
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-10:]  # Keep last 10 messages
        
        return system + recent
    
    @staticmethod
    def _count_tokens(text: str) -> int:
        return len(text) // 4
```

### Token Counting Accuracy

Use the provider tokenizer when available. `chars // 4` is a rough estimate only.

```python
class AccurateTokenizer:
    def __init__(self, provider: str):
        self.tokenizer = Tokenizer.for_model(provider)
    
    def count(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
```

### Token Budget Allocation

```python
class TokenBudgetAllocator:
    def __init__(self, total: int = 4096):
        self.total = total
        self.reserved = 64  # safety margin
        self.allocation = {
            "system": 0.10,
            "history": 0.35,
            "retrieval": 0.35,
            "response": 0.20,
        }
    
    def max_for(self, component: str) -> int:
        return int((self.total - self.reserved) * self.allocation[component])
```

### Context Pruning Strategy

```python
class ContextPruner:
    def __init__(self, tokenizer, budget: int = 4096):
        self.tokenizer = tokenizer
        self.budget = budget
    
    def prune(self, messages: List[dict]) -> List[dict]:
        tokens = sum(len(self.tokenizer.encode(m["content"])) for m in messages)
        if tokens <= self.budget:
            return messages
        keep = [m for m in messages if m["role"] == "system"]
        for msg in reversed(messages):
            if tokens <= self.budget:
                break
            msg_tokens = len(self.tokenizer.encode(msg["content"]))
            keep.append(msg)
            tokens -= msg_tokens
        return keep
```

### Tool Output Compression

Compress tool outputs before placing them in the prompt. Summarize structured data. Drop irrelevant fields.

```python
def compress_tool_output(output: dict, schema: dict) -> dict:
    allowed_fields = [k for k, v in schema["properties"].items() if v.get("performance_priority")]
    return {k: output[k] for k in allowed_fields if k in output}
```

---

## 4. Connection Pooling

```python
import aiohttp
from contextlib import asynccontextmanager

class PooledHttpClient:
    """Reuse HTTP connections for performance."""
    
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
    
    @asynccontextmanager
    async def get(self):
        yield self.session
```

### Graceful Shutdown

Always close sessions on shutdown. Use atexit or signal handlers to prevent leaked connectors.

```python
import signal

async def shutdown(session: aiohttp.ClientSession):
    await session.close()
    # await redis.close()
```

---

## 5. Error Handling and Resilience

### Retry with Exponential Backoff and Jitter

```python
import random

async def call_with_retry(fn, max_retries=5, base_delay=0.5, max_delay=30):
    for attempt in range(max_retries):
        try:
            return await fn()
        except TransientError as e:
            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, delay * 0.5)
            await asyncio.sleep(delay + jitter)
        except PermanentError:
            raise
    raise MaxRetriesExceeded()
```

### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"
        self.failures = 0
        self.last_failure_time = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError()
        try:
            result = await func(*args, **kwargs)
            self._success()
            return result
        except Exception:
            self._failure()
            raise
    
    def _success(self):
        self.failures = 0
        self.state = "closed"
    
    def _failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
```

### Bulkhead Pattern

Isolate failures by resource type. A failure in retrieval should not exhaust connections for model calls.

```python
class Bulkhead:
    def __init__(self, max_connections: int = 10):
        self.semaphore = asyncio.Semaphore(max_connections)
    
    async def call(self, func):
        async with self.semaphore:
            return await func()
```

---

## 6. Streaming and Progressive Responses

### Stream Tokens as They Arrive

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/stream")
async def stream_endpoint(prompt: str):
    async def generate():
        async for chunk in model.stream(prompt):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")
```

### Buffer Size Tuning

Small buffers reduce latency; large buffers reduce system-call overhead. Pick based on chunk size.

```python
CHUNK_BUFFER_SIZE = 1024  # bytes
```

### WebSocket Streaming

```python
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    async for message in ws.iter_text():
        async for chunk in model.stream(message):
            await ws.send_text(chunk)
```

---

## 7. Monitoring and Observability

### Latency Histograms

Track p50, p95, and p99. P99 is the most informative tail-latency indicator.

```python
class LatencyTracker:
    def __init__(self):
        self.samples: deque = deque(maxlen=1000)
    
    def record(self, duration_ms: float):
        self.samples.append(duration_ms)
    
    def p50(self) -> float:
        return np.percentile(self.samples, 50)
    
    def p95(self) -> float:
        return np.percentile(self.samples, 95)
    
    def p99(self) -> float:
        return np.percentile(self.samples, 99)
```

### Token Usage Tracking

Per-request token counts. Per-model cost aggregation. Per-user budget enforcement.

```python
class TokenUsageTracker:
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.request_count = 0
    
    def record(self, prompt_tokens: int, completion_tokens: int):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.request_count += 1
    
    def cost_summary(self, price_per_1k_prompt: float, price_per_1k_completion: float) -> dict:
        prompt_cost = self.total_prompt_tokens / 1000 * price_per_1k_prompt
        completion_cost = self.total_completion_tokens / 1000 * price_per_1k_completion
        return {
            "total_cost_usd": prompt_cost + completion_cost,
            "average_cost_per_request_usd": (prompt_cost + completion_cost) / self.request_count,
        }
```

### Alert Configuration

| Metric                | Warning      | Critical     |
|-----------------------|--------------|--------------|
| p95 Latency           | > 3s         | > 5s         |
| p99 Latency           | > 8s         | > 12s        |
| Cache Hit Rate        | < 60%        | < 40%        |
| Error Rate            | > 2%         | > 5%         |
| Token Cost per Request| > $0.08      | > $0.15      |

---

## 8. Cost Management

### Provider Routing by Cost Tier

Route simple tasks to cheaper models automatically. Quality gates ensure thresholds are met.

```python
class CostAwareRouter:
    def __init__(self):
        self.model_tiers = {
            "fast":   {"model": "gpt-4o-mini", "max_cost": 0.005},
            "balanced": {"model": "gpt-4o", "max_cost": 0.03},
            "powerful": {"model": "o3", "max_cost": 0.10},
        }
    
    def select(self, task_complexity: float) -> str:
        if task_complexity < 0.3:
            return self.model_tiers["fast"]["model"]
        if task_complexity < 0.7:
            return self.model_tiers["balanced"]["model"]
        return self.model_tiers["powerful"]["model"]
```

### Budget Guardrails

```python
class BudgetGuard:
    def __init__(self, daily_limit_usd: float):
        self.daily_limit_usd = daily_limit_usd
        self.spend: Dict[str, float] = defaultdict(float)
    
    def check(self, user_id: str, estimated_cost: float) -> bool:
        return self.spend[user_id] + estimated_cost <= self.daily_limit_usd
    
    def record(self, user_id: str, actual_cost: float):
        self.spend[user_id] += actual_cost
```

---

## 9. Testing Performance

### Load Testing

```python
import pytest
import asyncio

@pytest.mark.parametrize("concurrency", [1, 10, 50, 100])
async def test_scaling(concurrency):
    tasks = [process_request(prompt) for _ in range(concurrency)]
    start = time.perf_counter()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = time.perf_counter() - start
    failures = [r for r in results if isinstance(r, Exception)]
    assert len(failures) / concurrency < 0.01
    assert duration < concurrency * base_latency * 2  # rough throughput check
```

### chaos Engineering Questions

- What happens when cache returns null for 10% of requests?
- What happens when model provider latency doubles?
- What happens when 30% of tool calls fail?

---

## 10. Memory Management

### Object Pooling

```python
class MessagePool:
    def __init__(self, max_size: int = 1000):
        self._pool: deque = deque(maxlen=max_size)
    
    def acquire(self, content: str) -> dict:
        if self._pool:
            msg = self._pool.popleft()
            msg["content"] = content
            return msg
        return {"role": "user", "content": content}
    
    def release(self, msg: dict):
        self._pool.append(msg)
```

### Avoid Holding Large Objects

Do not accumulate raw tool outputs or retrieval documents. Normalize to the minimum representation.

```python
# Bad
session_context.append(full_retrieval_results)

# Good
session_context.append({
    "title": doc["title"],
    "snippet": doc["snippet"][:200],
})
```

---

## 11. Rate Limiting and Backpressure

### Per-User and Per-Model Rate Limits

```python
class RateLimiter:
    def __init__(self, rate_per_minute: int):
        self.rate = rate_per_minute
        self.tokens = rate_per_minute
        self.last_update = time.time()
    
    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / 60))
        self.last_update = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Adaptive Concurrency

Reduce concurrency when error rate rises. Increase when latency is healthy.

```python
class AdaptiveConcurrency:
    def __init__(self, initial: int = 10, min_c: int = 1, max_c: int = 100):
        self.semaphore = asyncio.Semaphore(initial)
        self.current = initial
        self.min = min_c
        self.max = max_c
        self.errors: deque = deque(maxlen=100)
    
    def record_success(self):
        if len(self.errors) == 0:
            self.current = min(self.max, self.current + 1)
            self._resize()
    
    def record_failure(self):
        self.errors.append(1)
        if len(self.errors) / 100 > 0.05:
            self.current = max(self.min, self.current - 1)
            self._resize()
    
    def _resize(self):
        self.semaphore = asyncio.Semaphore(self.current)
```

---

## 12. Security and Privacy

### Redaction in Production Logs

Hash prompt content. Log token counts and model IDs, not raw text.

```python
def redact_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]
```

### TLS and Certificate Pinning

```python
connector = aiohttp.TCPConnector(
    ssl=True,
    ssl_context=ssl.create_default_context(),
    enable_cleanup_closed=True,
)
```

---

## 13. Context Management

### Conversation Window Management

Maintain a sliding window of conversation history to keep token usage bounded.

```python
class ConversationWindow:
    def __init__(self, max_messages: int = 20, max_tokens: int = 8000):
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.messages: List[dict] = []
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._enforce_limits()
    
    def _enforce_limits(self):
        while (
            len(self.messages) > self.max_messages or
            self.count_tokens() > self.max_tokens
        ):
            # Remove oldest non-system message
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(i)
                    break
    
    def count_tokens(self) -> int:
        return sum(len(self.tokenizer.encode(m["content"])) for m in self.messages)
    
    def get_messages(self) -> List[dict]:
        return self.messages.copy()
```

### Context Summarization

```python
class ContextSummarizer:
    def __init__(self, model):
        self.model = model
    
    async def summarize(self, messages: List[dict]) -> dict:
        if len(messages) <= 4:
            return messages
        
        # Keep system prompt and recent messages
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-4:]
        
        # Summarize the middle
        middle = messages[1:-4]
        if middle:
            summary = await self._summarize_messages(middle)
            return system + [summary] + recent
        return system + recent
    
    async def _summarize_messages(self, messages: List[dict]) -> dict:
        combined = "\n".join(m["content"] for m in messages)
        summary = await self.model.complete(
            f"Summarize this conversation:\n{combined}"
        )
        return {
            "role": "system",
            "content": f"Summary: {summary}"
        }
```

---

## 14. Tool Execution Optimization

### Parallel Tool Calls

```python
async def execute_tools_parallel(
    tools: List[Dict[str, Any]],
    context: Dict[str, Any],
    max_concurrent: int = 5
) -> List[Any]:
    """Execute multiple tools in parallel with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute_one(tool: Dict[str, Any]):
        async with semaphore:
            name = tool["name"]
            args = tool.get("args", {})
            return await call_tool(name, args, context)
    
    tasks = [execute_one(t) for t in tools]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            processed_results.append({
                "tool": tools[i]["name"],
                "error": str(result),
                "success": False
            })
        else:
            processed_results.append({
                "result": result,
                "success": True
            })
    
    return processed_results
```

### Tool Result Caching

```python
class ToolResultCache:
    def __init__(self, cache_client, ttl: int = 3600):
        self.cache = cache_client
        self.ttl = ttl
    
    async def get_or_execute(self, tool_name: str, args: dict, executor):
        key = self._make_key(tool_name, args)
        cached = await self.cache.get(key)
        if cached:
            return json.loads(cached)
        
        result = await executor(tool_name, args)
        await self.cache.setex(key, self.ttl, json.dumps(result))
        return result
    
    def _make_key(self, tool_name: str, args: dict) -> str:
        args_str = json.dumps(args, sort_keys=True)
        return f"tool:{tool_name}:{hashlib.md5(args_str.encode()).hexdigest()}"
```

---

## 15. Provider Integration

### Multi-Provider Support

```python
class ModelProvider(ABC):
    @abstractmethod
    async def complete(self, messages: List[dict], **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream(self, messages: List[dict], **kwargs) -> AsyncGenerator[str, None]:
        pass

class OpenAIProvider(ModelProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def complete(self, messages: List[dict], **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    async def stream(self, messages: List[dict], **kwargs) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **kwargs
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

### Provider Failover

```python
class ProviderFailover:
    def __init__(self, providers: List[ModelProvider]):
        self.providers = providers
    
    async def complete_with_failover(self, messages: List[dict], **kwargs) -> str:
        last_error = None
        for provider in self.providers:
            try:
                return await provider.complete(messages, **kwargs)
            except Exception as e:
                last_error = e
                continue
        raise last_error or RuntimeError("All providers failed")
```

---

## 16. Infrastructure and Deployment

### Horizontal Scaling

Run multiple stateless replicas behind a load balancer. Ensure session affinity is not required unless explicitly needed.

```python
class StatelessAgentReplica:
    def __init__(self):
        self.cache = redis.from_url("redis://localhost:6379")
        self.model_client = ModelClient(provider="openai")
    
    async def process(self, request: dict) -> dict:
        session_id = request["session_id"]
        context = await self.cache.get(f"ctx:{session_id}")
        response = await self.model_client.complete(context)
        await self.cache.setex(f"ctx:{session_id}", 3600, response)
        return {"response": response, "session_id": session_id}
```

### Autoscaling Configuration

```yaml
# Kubernetes HorizontalPodAutoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent
  minReplicas: 2
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: queue_depth
        target:
          type: AverageValue
          averageValue: "10"
```

---

## 17. Team Practices

### Performance Budgets in RFCs

Every feature RFC must include:
- Expected latency impact.
- Expected token usage.
- Expected cost impact.
- Cache hit rate expectations.
- SLO targets.

### Regular Performance Reviews

Schedule monthly reviews to:
- Review latency trends.
- Audit cache hit rates.
- Check cost per request.
- Identify new bottlenecks.
- Update performance budgets.

### Performance Champions

Assign one engineer per team as the performance champion. Responsibilities:
- Monitor weekly metrics.
- Raise issues early.
- Drive optimization efforts.
- Maintain performance documentation.

---

## 18. Performance Reviews

### Quarterly Performance Audit

Review the following metrics and trends:
- p50, p95, p99 latency.
- Error rate and retry rate.
- Cache hit rate.
- Token usage per request.
- Cost per request and per user.
- Memory and CPU utilization.
- Connection pool saturation.
- Provider API latency.

### Performance Improvement Plan

When an SLO is violated:
1. Identify the root cause within 24 hours.
2. Implement a fix within 72 hours.
3. Add monitoring to prevent recurrence.
4. Update runbooks.
5. Conduct a blameless post-mortem.

---

## Checklist Summary

- [ ] Caching implemented for repeated queries
- [ ] Streaming enabled for long responses
- [ ] Async used for all I/O
- [ ] Token budgets enforced
- [ ] Connection pooling enabled
- [ ] Retries use exponential backoff with jitter
- [ ] Circuit breakers protect downstream services
- [ ] p95, p99 latency monitored
- [ ] Cost tracked per request and per user
- [ ] Memory bounded with TTL or maxlen
- [ ] PII redacted from logs
- [ ] Tests run under load
- [ ] All external calls have timeouts
- [ ] Backpressure mechanisms in place
- [ ] Context window managed and summarized
- [ ] Tool outputs compressed before insertion
- [ ] Model routing by complexity active
- [ ] Security review passed
- [ ] Autoscaling configured
- [ ] Performance budgets documented

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Advanced](./advanced.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
