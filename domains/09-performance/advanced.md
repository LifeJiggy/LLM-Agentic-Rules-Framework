# Performance Domain - Advanced Concepts

## Overview

Advanced performance concepts for LLM/agentic systems, covering caching patterns, load balancing, distributed architectures, circuit breakers, backpressure, and monitoring at scale.

## Table of Contents

1. [Load Balancing](#load-balancing)
2. [Advanced Caching Patterns](#advanced-caching-patterns)
3. [Semantic Caching](#semantic-caching)
4. [Distributed Caching Architectures](#distributed-caching-architectures)
5. [Cache Stampede Protection](#cache-stampede-protection)
6. [Advanced Load Balancing](#advanced-load-balancing)
7. [Connection Pooling Deep Dive](#connection-pooling-deep-dive)
8. [Circuit Breaker Patterns](#circuit-breaker-patterns)
9. [Backpressure and Flow Control](#backpressure-and-flow-control)
10. [Adaptive Batching](#adaptive-batching)
11. [Predictive Prefetching](#predictive-prefetching)
12. [Advanced Token Optimization](#advanced-token-optimization)
13. [Monitoring and Observability at Scale](#monitoring-and-observability-at-scale)
14. [Distributed Tracing](#distributed-tracing)
15. [Performance Budgets](#performance-budgets)
16. [Autoscaling and Scaling Policies](#autoscaling-and-scaling-policies)
17. [Queue Processing and Backpressure](#queue-processing-and-backpressure)
18. [Token Compression and Summarization](#token-compression-and-summarization)
19. [Zero-Copy Techniques and Memory Optimization](#zero-copy-techniques-and-memory-optimization)
20. [Performance Testing at Scale](#performance-testing-at-scale)
21. [Consistent Hashing](#consistent-hashing)
22. [Distributed Locking](#distributed-locking)
23. [Rate Limiting Algorithms](#rate-limiting-algorithms)
24. [Memory-Mapped Caching](#memory-mapped-caching)
25. [Hierarchical Cache Invalidation](#hierarchical-cache-invalidation)
26. [Request Coalescing](#request-coalescing)
27. [Observability Pipelines](#observability-pipelines)
28. [Performance Profiling in Production](#performance-profiling-in-production)
29. [Custom Metrics and Dashboards](#custom-metrics-and-dashboards)
30. [Autoscaling with Predictive Models](#autoscaling-with-predictive-models)

---

## Load Balancing

```python
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

### Load Balancer Design Considerations

- **Health Checks:** Periodically probe backends. Remove unhealthy instances.
- **Concurrency Limits:** Different backends may have different capacities.
- **Session Affinity:** Preserve session state when necessary.
- **Failover:** Gracefully shift traffic during outages.
- **Sticky Sessions:** Use consistent hashing when stateful routing is required.

---

## Advanced Caching Patterns

### Cache-Aside (Lazy Loading)

The cache sits alongside the data store. On cache miss, the application loads from the backing store and writes into cache.

```python
class CacheAsideStore:
    def __init__(self, cache, db_fetch):
        self.cache = cache
        self.db_fetch = db_fetch
    
    async def get(self, key: str):
        cached = await self.cache.get(key)
        if cached is not None:
            return cached
        value = await self.db_fetch(key)
        if value is not None:
            await self.cache.setex(key, 3600, value)
        return value
```

**Use cases:** Datasets where reads far exceed writes. Works best with predictable query patterns.

### Write-Through

Writes go to both cache and backing store before acknowledgement. Guarantees strong consistency at the cost of write latency.

```python
class WriteThroughStore:
    def __init__(self, cache, db_write):
        self.cache = cache
        self.db_write = db_write
    
    async def set(self, key: str, value: str):
        await self.db_write(key, value)
        await self.cache.setex(key, 3600, value)
```

**Use cases:** Systems where data loss is unacceptable and write volume is moderate.

### Write-Behind (Write-Back)

Writes are queued and flushed to backing store asynchronously. Reduces write latency but risks data loss on crash.

```python
class WriteBehindStore:
    def __init__(self, cache, db_write, flush_interval: int = 5):
        self.cache = cache
        self.db_write = db_write
        self.flush_interval = flush_interval
        self.dirty: Dict[str, str] = {}
        self._lock = asyncio.Lock()
        asyncio.create_task(self._periodic_flush())
    
    async def set(self, key: str, value: str):
        self.dirty[key] = value
        await self.cache.setex(key, 3600, value)
    
    async def _periodic_flush(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            if not self.dirty:
                continue
            async with self._lock:
                snapshot = dict(self.dirty)
                self.dirty.clear()
            await self.db_write.bulk_write(snapshot)
```

**Use cases:** High-throughput write paths like analytics pipelines.

### Around Pattern

Cache is updated around the backing store call.

```python
class AroundStore:
    async def get(self, key: str):
        cached = await self.cache.get(key)
        if cached is not None:
            return cached
        raw = await self.db_fetch(key)
        normalized = self._normalize(raw)
        await self.cache.setex(key, 3600, normalized)
        return normalized
```

### Eventual Consistency Strategies

When strict consistency is not required, use TTLs and refresh-ahead to keep data fresh.

```python
class RefreshAheadCache:
    def __init__(self, cache, db_fetch, refresh_margin: int = 300):
        self.cache = cache
        self.db_fetch = db_fetch
        self.refresh_margin = refresh_margin
    
    async def get(self, key: str):
        value = await self.cache.get(key)
        ttl = await self.cache.ttl(key)
        if value is not None and ttl > self.refresh_margin:
            return value
        fresh = await self.db_fetch(key)
        if fresh is not None:
            await self.cache.setex(key, 3600, fresh)
        return fresh
```

---

## Semantic Caching

### Embedding-Based Similarity Cache

Store embeddings alongside cached results. On query, compute embedding similarity to find semantically equivalent prior queries.

```python
import numpy as np

class SemanticCache:
    def __init__(self, embedding_fn, similarity_threshold: float = 0.95):
        self.embedding_fn = embedding_fn
        self.similarity_threshold = similarity_threshold
        self.entries: List[Tuple[np.ndarray, Any]] = []
    
    async def get(self, query: str):
        query_emb = self.embedding_fn(query)
        for entry_emb, value in self.entries:
            sim = np.dot(query_emb, entry_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(entry_emb)
            )
            if sim >= self.similarity_threshold:
                return value
        return None
    
    async def set(self, query: str, value):
        query_emb = self.embedding_fn(query)
        self.entries.append((query_emb, value))
```

**Considerations:**
- Embedding dimension and storage cost.
- ANN index for large stores.
- Cache eviction when the store grows.

### Hybrid Cache Key Strategy

Combine exact hash with semantic fingerprint for robust cacheability.

```python
class HybridCacheKey:
    def __init__(self, model_id: str, prompt_version: str):
        self.model_id = model_id
        self.prompt_version = prompt_version
    
    def build(self, prompt: str, params: dict) -> str:
        exact = hashlib.sha256(
            f"{self.model_id}:{self.prompt_version}:{prompt}:{params}".encode()
        ).hexdigest()
        semantic = hashlib.md5(prompt.encode()).hexdigest()[:8]
        return f"hybrid:{exact}:{semantic}"
```

---

## Distributed Caching Architectures

### Redis Cluster Topology

Use consistent hashing or Redis Cluster for horizontal scale. Separate cache tiers by volatility and size.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Hot L1     │    │  Warm L2    │    │  Cool L3    │
│  (Memory)   │───▶│  (Redis)    │───▶│  (Disk /    │
│  < 1% data  │    │  10% data   │    │  S3)        │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Cache Stampede Protection

Use probabilistic early expiration (randomized TTL jitter) plus request coalescing.

```python
async def get_with_jitter(cache, key: str, fetch_fn, base_ttl: int = 300):
    cached = await cache.get(key)
    if cached:
        return json.loads(cached)
    lock_key = f"lock:{key}"
    acquired = await cache.set(lock_key, "1", ex=5, nx=True)
    if not acquired:
        await asyncio.sleep(0.1)
        return await get_with_jitter(cache, key, fetch_fn, base_ttl)
    try:
        value = await fetch_fn()
        jitter = base_ttl * 0.1
        ttl = base_ttl + random.randint(-int(jitter), int(jitter))
        await cache.setex(key, ttl, json.dumps(value))
        await cache.delete(lock_key)
        return value
    except Exception:
        await cache.delete(lock_key)
        raise
```

---

## Advanced Load Balancing

### Weighted Round Robin

```python
class WeightedRoundRobin:
    def __init__(self, servers: Dict[str, int]):
        self.servers = []
        self.weights = []
        for server, weight in servers.items():
            self.servers.append(server)
            self.weights.append(weight)
        self.current = 0
        self.current_weight = 0
    
    def get_server(self) -> str:
        while True:
            self.current = (self.current + 1) % len(self.servers)
            if self.current == 0:
                self.current_weight -= 1
            if self.current_weight <= 0:
                self.current_weight = self.weights[self.current]
            if self.current_weight > 0:
                return self.servers[self.current]
```

### Consistent Hashing

```python
class ConsistentHashRing:
    def __init__(self, nodes: List[str], replicas: int = 150):
        self.replicas = replicas
        self.ring = {}
        for node in nodes:
            for i in range(replicas):
                hash_key = hashlib.md5(f"{node}:{i}".encode()).hexdigest()
                self.ring[hash_key] = node
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key: str) -> str:
        if not self.sorted_keys:
            raise ValueError("No nodes available")
        hash_key = hashlib.md5(key.encode()).hexdigest()
        idx = bisect.bisect(self.sorted_keys, hash_key) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]
```

---

## Connection Pooling Deep Dive

### TCP Connector Configuration

```python
class AdvancedConnectionPool:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=200,
                    limit_per_host=30,
                    ttl_dns_cache=600,
                    ssl=False,
                    keepalive_timeout=30,
                    enable_cleanup_closed=True,
                ),
                timeout=aiohttp.ClientTimeout(total=30, connect=5, sock_read=10),
                trust_env=True,
            )
        return cls._instance
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
```

### Connection Health Monitoring

Track open connections, errors, and latency per host.

```python
class MonitoredConnector(aiohttp.TCPConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = {"connections_opened": 0, "connections_closed": 0, "errors": 0}
    
    async def _create_connection(self, req, ...):
        self.metrics["connections_opened"] += 1
        try:
            conn = await super()._create_connection(req, ...)
            return conn
        except Exception as e:
            self.metrics["errors"] += 1
            raise
```

---

## Circuit Breaker Patterns

### State Machine Implementation

```python
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = 0
        self.successes = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.successes = 0
            else:
                raise CircuitOpenError("Circuit is open")
        
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            self._record_failure()
            raise e
        else:
            self._record_success()
            return result
    
    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failures = 0
```

---

## Backpressure and Flow Control

### Bounded Channel Pattern

```python
class BoundedChannel:
    def __init__(self, capacity: int):
        self._queue = asyncio.Queue(maxsize=capacity)
        self._closed = False
    
    async def send(self, item):
        if self._closed:
            raise ClosedChannelError()
        await self._queue.put(item)
    
    async def receive(self):
        if self._queue.empty() and self._closed:
            raise ClosedChannelError()
        return await self._queue.get()
    
    def close(self):
        self._closed = True
```

### Adaptive Rate Limiting

```python
class AdaptiveRateLimiter:
    def __init__(self, initial_rate: int = 100):
        self.current_rate = initial_rate
        self.min_rate = 10
        self.max_rate = 500
        self.error_window: Deque[float] = deque(maxlen=100)
        self.latency_window: Deque[float] = deque(maxlen=100)
    
    def record_result(self, success: bool, latency_ms: float):
        self.error_window.append(0 if success else 1)
        self.latency_window.append(latency_ms)
        self._adjust_rate()
    
    def _adjust_rate(self):
        if not self.error_window or not self.latency_window:
            return
        error_rate = sum(self.error_window) / len(self.error_window)
        avg_latency = sum(self.latency_window) / len(self.latency_window)
        if error_rate > 0.1 or avg_latency > 3000:
            self.current_rate = max(self.min_rate, int(self.current_rate * 0.8))
        elif error_rate < 0.01 and avg_latency < 1000:
            self.current_rate = min(self.max_rate, int(self.current_rate * 1.2))
    
    def allow(self) -> bool:
        return random.random() < (self.current_rate / self.max_rate)
```

---

## Adaptive Batching

### Dynamic Batch Size Based on Load

```python
class AdaptiveBatcher:
    def __init__(self, target_latency: float = 1.0, min_batch: int = 1, max_batch: int = 64):
        self.target_latency = target_latency
        self.min_batch = min_batch
        self.max_batch = max_batch
        self.current_batch = min_batch
        self.latency_samples: Deque[float] = deque(maxlen=20)
    
    async def process(self, items: List[Any], process_fn):
        batch_size = self.current_batch
        start = time.perf_counter()
        result = await process_fn(items[:batch_size])
        elapsed = time.perf_counter() - start
        self.latency_samples.append(elapsed)
        self._tune_batch()
        return result
    
    def _tune_batch(self):
        if not self.latency_samples:
            return
        avg = sum(self.latency_samples) / len(self.latency_samples)
        if avg < self.target_latency * 0.5:
            self.current_batch = min(self.max_batch, self.current_batch + 1)
        elif avg > self.target_latency * 1.5:
            self.current_batch = max(self.min_batch, self.current_batch - 1)
```

---

## Predictive Prefetching

### User Interaction Prediction

```python
class PredictivePrefetcher:
    def __init__(self, model, cache, trigger_threshold: float = 0.7):
        self.model = model
        self.cache = cache
        self.trigger_threshold = trigger_threshold
    
    async def maybe_prefetch(self, user_state: dict):
        predicted = self.model.predict_next(user_state)
        if predicted["confidence"] >= self.trigger_threshold:
            await self.cache.prefetch(predicted["query"])
```

---

## Advanced Token Optimization

### Semantic Compression

```python
class SemanticCompressor:
    def __init__(self, embedding_fn, target_ratio: float = 0.5):
        self.embedding_fn = embedding_fn
        self.target_ratio = target_ratio
    
    def compress(self, messages: List[dict]) -> List[dict]:
        if len(messages) <= 4:
            return messages
        keep = messages[:2] + messages[-2:]
        to_compress = messages[2:-2]
        summary = self._summarize(to_compress)
        keep.insert(2, summary)
        return keep
    
    def _summarize(self, messages: List[dict]) -> dict:
        combined = "\n".join(m["content"] for m in messages)
        emb = self.embedding_fn(combined)
        return {
            "role": "system",
            "content": f"[Summary: {len(messages)} earlier messages compressed]",
            "embedding": emb.tolist(),
        }
```

### Structured Output Token Counting

```python
def count_structured_tokens(schema: dict) -> int:
    schema_str = json.dumps(schema)
    return len(schema_str.split()) + len(json.dumps(schema)) // 4

class TokenBudgetedStructuredCall:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.schema_overhead = 50
    
    def remaining_for_generation(self, input_tokens: int) -> int:
        return max(0, self.max_tokens - input_tokens - self.schema_overhead)
```

### Token-Aware Context Pruning

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

---

## Monitoring and Observability at Scale

### RED Metrics (Rate, Errors, Duration)

```python
class REDMetrics:
    def __init__(self):
        self.rate = Counter()
        self.errors = Counter()
        self.durations = Histogram()
    
    async def record_request(self, endpoint: str, status: int, duration_ms: float):
        self.rate.labels(endpoint=endpoint).inc()
        self.durations.labels(endpoint=endpoint).observe(duration_ms)
        if status >= 400:
            self.errors.labels(endpoint=endpoint, code=status).inc()
```

### USE Method (Utilization, Saturation, Errors)

```python
class USEMetrics:
    def __init__(self):
        self.utilization = Gauge()
        self.saturation = Gauge()
        self.errors = Counter()
    
    def record_resource(self, resource: str, used: float, total: float, saturated: bool):
        self.utilization.labels(resource=resource).set(used / total)
        self.saturation.labels(resource=resource).set(1.0 if saturated else 0.0)
```

### Instrumentation Decorators

```python
def instrument_latency(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            latency_histogram.observe(duration_ms)
    return wrapper

def instrument_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_counter.labels(type=type(e).__name__, function=func.__name__).inc()
            raise
    return wrapper
```

---

## Distributed Tracing

### Trace Context Propagation

```python
import opentelemetry as otel
from opentelemetry.trace import get_current_span

class TracedAgent:
    async def process(self, prompt: str):
        with otel.trace.get_tracer(__name__).start_as_current_span("agent.process") as span:
            span.set_attribute("prompt.length", len(prompt))
            span.set_attribute("prompt.tokens", estimate_tokens(prompt))
            
            with otel.trace.get_tracer(__name__).start_as_current_span("model.call"):
                response = await self._call_model(prompt)
            
            with otel.trace.get_tracer(__name__).start_as_current_span("tool.execute"):
                tools_result = await self._execute_tools(response)
            
            span.set_attribute("response.length", len(tools_result))
            return tools_result
```

### Baggage and Context Propagation

Pass trace identifiers through cache keys and event queues to correlate cross-service behavior.

---

## Performance Budgets

### SLO Definitions

```python
class PerformanceBudget:
    def __init__(self):
        self.budgets = {
            "time_to_first_token_ms": 500,
            "response_completion_p95_ms": 5000,
            "cache_hit_rate": 0.80,
            "max_tokens_per_request": 12000,
            "max_cost_per_request_usd": 0.10,
        }
    
    def check(self, metrics: dict) -> List[str]:
        violations = []
        for metric, threshold in self.budgets.items():
            value = metrics.get(metric)
            if isinstance(threshold, float) and value < threshold:
                violations.append(f"{metric} below budget: {value} < {threshold}")
            elif isinstance(threshold, int) and value > threshold:
                violations.append(f"{metric} over budget: {value} > {threshold}")
        return violations
```

---

## Autoscaling and Scaling Policies

### Queue-Length-Based Scaling

```python
class QueueScalingPolicy:
    def __init__(self, min_replicas: int = 2, max_replicas: int = 20, target_queue: int = 10):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_queue = target_queue
    
    def desired_replicas(self, current_replicas: int, queue_length: int) -> int:
        desired = int((queue_length / self.target_queue) * current_replicas)
        return max(self.min_replicas, min(self.max_replicas, desired))
```

---

## Queue Processing and Backpressure

### Bounded Channel Pattern

```python
class BoundedChannel:
    def __init__(self, capacity: int):
        self._queue = asyncio.Queue(maxsize=capacity)
        self._closed = False
    
    async def send(self, item):
        if self._closed:
            raise ClosedChannelError()
        await self._queue.put(item)
    
    async def receive(self):
        if self._queue.empty() and self._closed:
            raise ClosedChannelError()
        return await self._queue.get()
    
    def close(self):
        self._closed = True
```

### Backpressure via Semaphores

```python
class MaxConcurrencyLimiter:
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run(self, coro):
        async with self.semaphore:
            return await coro
```

---

## Token Compression and Summarization

### Semantic Compression

```python
class SemanticCompressor:
    def __init__(self, embedding_fn, target_ratio: float = 0.5):
        self.embedding_fn = embedding_fn
        self.target_ratio = target_ratio
    
    def compress(self, messages: List[dict]) -> List[dict]:
        if len(messages) <= 4:
            return messages
        keep = messages[:2] + messages[-2:]
        to_compress = messages[2:-2]
        summary = self._summarize(to_compress)
        keep.insert(2, summary)
        return keep
    
    def _summarize(self, messages: List[dict]) -> dict:
        combined = "\n".join(m["content"] for m in messages)
        emb = self.embedding_fn(combined)
        return {
            "role": "system",
            "content": f"[Summary: {len(messages)} earlier messages compressed]",
            "embedding": emb.tolist(),
        }
```

### Extract-Then-Summarize

First extract facts, then summarize extracted facts to minimize information loss.

```python
class ExtractThenSummarize:
    def __init__(self, model):
        self.model = model
    
    async def compress(self, messages: List[dict]) -> dict:
        extraction = await self.model.extract_facts(messages)
        summary = await self.model.summarize(extraction)
        return {"role": "system", "content": summary}
```

---

## Zero-Copy Techniques and Memory Optimization

### MemoryView and Buffer Reuse

Use `memoryview` to avoid copying large strings in hot paths.

```python
class EfficientBuffer:
    def __init__(self):
        self.buffer = bytearray(4096)
        self.view = memoryview(self.buffer)
    
    def write(self, data: bytes) -> memoryview:
        self.buffer[:len(data)] = data
        return self.view[:len(data)]
```

### Avoid Holding Large Objects

Do not accumulate raw tool outputs or retrieval documents. Normalize to the minimum representation.

```python
session_context.append({
    "title": doc["title"],
    "snippet": doc["snippet"][:200],
})
```

---

## Performance Testing at Scale

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
    assert duration < concurrency * base_latency * 2
```

### Chaos Engineering

Test system behavior under partial failure conditions.

```python
@pytest.mark.parametrize("failure_rate", [0.0, 0.1, 0.3, 0.5])
async def test_resilience(failure_rate):
    failing_client = FaultInjector(failure_rate=failure_rate)
    results = await run_pipeline(failing_client)
    assert results.error_rate() < 0.05
```

---

## Consistent Hashing

### Implementation

```python
class ConsistentHashRing:
    def __init__(self, nodes: List[str], replicas: int = 150):
        self.replicas = replicas
        self.ring = {}
        for node in nodes:
            for i in range(replicas):
                hash_key = hashlib.md5(f"{node}:{i}".encode()).hexdigest()
                self.ring[hash_key] = node
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key: str) -> str:
        if not self.sorted_keys:
            raise ValueError("No nodes available")
        hash_key = hashlib.md5(key.encode()).hexdigest()
        idx = bisect.bisect(self.sorted_keys, hash_key) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]
```

### Use Cases

- Distributed caching across nodes.
- Sharded databases for horizontal scaling.
- Load balancing with minimal rebalancing on node changes.

---

## Distributed Locking

### Implementation with Redis

```python
class DistributedLock:
    def __init__(self, redis_client, lock_key: str, ttl: int = 10):
        self.redis = redis_client
        self.lock_key = lock_key
        self.ttl = ttl
        self.identifier = str(uuid.uuid4())
    
    async def acquire(self) -> bool:
        return await self.redis.set(self.lock_key, self.identifier, ex=self.ttl, nx=True)
    
    async def release(self):
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(lua_script, 1, self.lock_key, self.identifier)
    
    async def __aenter__(self):
        while not await self.acquire():
            await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()
```

---

## Rate Limiting Algorithms

### Token Bucket

```python
class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Sliding Window

```python
class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque = deque()
        self.lock = asyncio.Lock()
    
    async def allow(self) -> bool:
        async with self.lock:
            now = time.time()
            while self.requests and self.requests[0] < now - self.window_seconds:
                self.requests.popleft()
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False
```

### Fixed Window

```python
class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.current_window_start = time.time()
        self.request_count = 0
        self.lock = asyncio.Lock()
    
    async def allow(self) -> bool:
        async with self.lock:
            now = time.time()
            if now - self.current_window_start >= self.window_seconds:
                self.current_window_start = now
                self.request_count = 0
            if self.request_count < self.max_requests:
                self.request_count += 1
                return True
            return False
```

---

## Memory-Mapped Caching

### mmap for Large Files

Use memory-mapped files for read-only caches of large data structures.

```python
import mmap

class MMapCache:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.mmap = None
    
    def load(self):
        with open(self.filepath, "r+b") as f:
            self.mmap = mmap.mmap(f.fileno(), 0)
    
    def get(self, offset: int, length: int) -> bytes:
        if self.mmap is None:
            self.load()
        self.mmap.seek(offset)
        return self.mmap.read(length)
    
    def close(self):
        if self.mmap:
            self.mmap.close()
```

### Buffer Pooling

Reuse bytearray buffers for network and serialization workloads.

```python
class ByteArrayPool:
    def __init__(self, size: int = 4096, max_pool: int = 100):
        self._pool: deque = deque(maxlen=max_pool)
        self._size = size
    
    def acquire(self) -> bytearray:
        if self._pool:
            return self._pool.popleft()
        return bytearray(self._size)
    
    def release(self, buf: bytearray):
        self._pool.append(buf)
```

### Structure of Arrays for Vectors

Pack embedding vectors into a single buffer to reduce allocation overhead.

```python
class SoAEmbeddings:
    def __init__(self, num_vectors: int, dim: int):
        self.data = np.zeros((num_vectors, dim), dtype=np.float32)
    
    def set(self, idx: int, vector: np.ndarray):
        self.data[idx] = vector
    
    def get(self, idx: int) -> np.ndarray:
        return self.data[idx]
```

---

## Hierarchical Cache Invalidation

### Multi-Tier Invalidation

When backing store changes, invalidate from hot to cold.

```python
class InvalidatingCache:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
    
    async def invalidate(self, key: str):
        await asyncio.gather(
            self.l1.delete(key),
            self.l2.delete(key),
            self.l3.delete(key),
        )
```

### Event-Driven Invalidation

Listen to database change events (CDC) to invalidate affected keys.

```python
class CDCInvalidator:
    def __init__(self, cache, consumer):
        self.cache = cache
        self.consumer = consumer
    
    async def listen(self):
        async for event in self.consumer:
            await self.cache.invalidate(event["key"])
```

---

## Request Coalescing

### Group Identical Requests

Multiple concurrent requests for the same cache key should resolve from a single fetch.

```python
class CoalescingCache:
    def __init__(self, cache, fetch_fn):
        self.cache = cache
        self.fetch_fn = fetch_fn
        self.inflight: Dict[str, asyncio.Task] = {}
        self.lock = asyncio.Lock()
    
    async def get(self, key: str):
        cached = await self.cache.get(key)
        if cached:
            return json.loads(cached)
        async with self.lock:
            if key in self.inflight:
                return await self.inflight[key]
            task = asyncio.create_task(self._fetch(key))
            self.inflight[key] = task
            try:
                return await task
            finally:
                del self.inflight[key]
    
    async def _fetch(self, key: str):
        value = await self.fetch_fn(key)
        await self.cache.setex(key, 3600, json.dumps(value))
        return value
```

---

## Observability Pipelines

### Sampling and Aggregation

High-cardinality traces sampled at a fixed rate.

```python
class AdaptiveSampler:
    def __init__(self, target_sample_rate: float = 0.01):
        self.target_sample_rate = target_sample_rate
    
    def should_sample(self, trace_id: str, latency_ms: float, error: bool) -> bool:
        if error:
            return True
        if latency_ms > 5000:
            return True
        # hash-based probabilistic sampling
        h = int(hashlib.md5(trace_id.encode()).hexdigest(), 16)
        return (h % 10000) / 10000 < self.target_sample_rate
```

### Metrics Aggregation

Roll up high-resolution metrics before ingestion.

```python
class MetricsAggregator:
    def __init__(self, flush_interval: int = 10):
        self.flush_interval = flush_interval
        self.samples: Dict[str, List[float]] = defaultdict(list)
        asyncio.create_task(self._flush_loop())
    
    def add(self, metric: str, value: float):
        self.samples[metric].append(value)
    
    async def _flush_loop(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            snapshot = dict(self.samples)
            self.samples.clear()
            for metric, values in snapshot.items():
                await exporter.export(metric, values)
```

---

## Performance Profiling in Production

### Low-Overhead Sampling Profiler

```python
import cProfile
import pstats
import io

class ProductionProfiler:
    def __init__(self, sample_interval: float = 0.001):
        self.sample_interval = sample_interval
        self.profiler = cProfile.Profile()
    
    def start(self):
        self.profiler.enable()
    
    def stop(self):
        self.profiler.disable()
        s = io.StringIO()
        self.profiler.dump_stats(s)
        return s.getvalue()
```

### Flame Graph Generation

```python
class FlameGraphGenerator:
    @staticmethod
    def generate(profiler_output: str, output_path: str):
        # Use py-spy or flamegraph.pl to generate SVG
        stats = pstats.Stats(io.StringIO(profiler_output))
        stats.sort_stats("cumulative")
        # Convert to collapsed stack format for flamegraph
        # ...
```

---

## Custom Metrics and Dashboards

### Performance Dashboard Components

Key panels:
- Request rate and error rate over time.
- p50, p95, p99 latency heatmap.
- Token usage by model and endpoint.
- Cache hit rate by key prefix.
- Cost per user and per endpoint.
- Circuit breaker state transitions.
- Queue depth and consumer lag.

### Metric Registration Pattern

```python
class MetricRegistry:
    def __init__(self, prefix: str = "agent"):
        self.prefix = prefix
    
    def counter(self, name: str, labels: List[str] = None):
        return Counter(f"{self.prefix}_{name}", labels or [])
    
    def histogram(self, name: str, labels: List[str] = None, buckets: List[float] = None):
        return Histogram(f"{self.prefix}_{name}", labels or [], buckets or [])
```

---

## Autoscaling with Predictive Models

### Time-Series Forecasting

Predict load spikes based on historical patterns.

```python
class PredictiveScaler:
    def __init__(self, model, min_replicas: int = 2, max_replicas: int = 20):
        self.model = model
        self.min = min_replicas
        self.max = max_replicas
    
    def desired_replicas(self, current: int, history: List[float]) -> int:
        forecast = self.model.predict(history)
        if forecast > current * 1.5:
            return min(self.max, current + 2)
        if forecast < current * 0.5:
            return max(self.min, current - 1)
        return current
```

### Load Shedding

When load exceeds capacity, preferentially drop low-value requests.

```python
class LoadShedder:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.current_load = 0
        self.shed_threshold = 0.9
    
    def allow(self, priority: float = 1.0) -> bool:
        load = self.current_load / self.capacity
        if load >= self.shed_threshold:
            return priority > (1.0 - load)
        return True
```

---

## Heterogeneous Computing

### CPU vs GPU Considerations

LLM inference benefits from GPU when:
- Batch size is large.
- Model is large (70B+ parameters).
- Latency target is aggressive.

Use CPU for:
- Small models (<3B).
- Low-concurrency inference.
- Cost-sensitive workloads.

### Mixed-Precision Inference

```python
class MixedPrecisionInference:
    def __init__(self, model):
        self.model = model
    
    async def infer(self, prompt: str, precision: str = "auto"):
        if precision == "auto":
            precision = "fp16" if len(prompt) > 1000 else "fp32"
        # Use appropriate precision for inference
        return await self.model.generate(prompt, precision=precision)
```

---

## Conclusion

Advanced performance engineering combines layered caching, intelligent routing, flow control, and observability. The goal is predictable latency, bounded cost, and graceful degradation under load.

Key advanced concepts include consistent hashing, distributed locking, rate limiting algorithms, memory-mapped caching, hierarchical cache invalidation, request coalescing, observability pipelines, and performance profiling in production.

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Checklist](./checklist.md)
- [Anti-Patterns](./anti-patterns.md)
