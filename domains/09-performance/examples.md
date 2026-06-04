# Performance Domain - Examples

## Overview

This document provides code examples for performance optimization in LLM/agentic systems.

## Table of Contents

1. [Response Caching](#example-1-response-caching)
2. [Streaming for Fast Responses](#example-2-streaming-for-fast-responses)
3. [Parallel Tool Execution](#example-3-parallel-tool-execution)
4. [Semantic Cache Lookup](#example-4-semantic-cache-lookup)
5. [Prompt Deduplication](#example-5-prompt-deduplication)
6. [Token-Aware Context Pruning](#example-6-token-aware-context-pruning)
7. [Connection Pooling](#example-7-connection-pooling)
8. [Resilient API Calls with Retries](#example-8-resilient-api-calls-with-retries)
9. [Circuit Breaker for External APIs](#example-9-circuit-breaker-for-external-apis)
10. [Model Router](#example-10-model-router)
11. [Adaptive Batching](#example-11-adaptive-batching)
12. [Streaming to Frontend](#example-12-streaming-to-frontend)
13. [Distributed Tracing](#example-13-distributed-tracing)
14. [Budget Enforcement](#example-14-budget-enforcement)
15. [Multi-Level Cache with Write-Through](#example-15-multi-level-cache-with-write-through)
16. [Token Counting with Provider Tokenizer](#example-16-token-counting-with-provider-tokenizer)
17. [Parallel Retrieval](#example-17-parallel-retrieval)
18. [Graceful Degradation](#example-18-graceful-degradation)
19. [Token Compression](#example-19-token-compression)
20. [Adaptive Concurrency Control](#example-20-adaptive-concurrency-control)
21. [Semantic Cache with Redis](#example-21-semantic-cache-with-redis)
22. [Hot Key Detection](#example-22-hot-key-detection)
23. [Cache Stampede Avoidance](#example-23-cache-stampede-avoidance)
24. [Structured Concurrency](#example-24-structured-concurrency)
25. [Memory Management with Pooling](#example-25-memory-management-with-pooling)
26. [Context Window Sliding Sum](#example-26-context-window-sliding-sum)
27. [Rate Limiter Implementation](#example-27-rate-limiter-implementation)
28. [Token Budget per Component](#example-28-token-budget-per-component)
29. [Multi-Tier Cache Invalidation](#example-29-multi-tier-cache-invalidation)
30. [Real-Time Cost Tracking](#example-30-real-time-cost-tracking)

---

## Example 1: Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_generation(prompt_hash: str) -> str:
    """Cache deterministic responses."""
    # Lookup in persistent cache
    pass

async def optimize_response(prompt: str) -> str:
    """Get response with caching."""
    key = hash(prompt)
    
    # Check memory cache
    cached = cached_generation(key)
    if cached:
        return cached
    
    # Generate and cache
    response = await call_model(prompt)
    cache.setex(f"response:{key}", 3600, response)
    
    return response
```

### Variations

- Use `cachetools.TTLCache` for in-process expiry.
- Use `redis.asyncio` for shared cache across replicas.

### Production Hardening

- Include model and policy version in cache key.
- Set different TTLs for different content types.
- Monitor cache hit rate per key prefix.

```python
class ProductionCache:
    def __init__(self, redis_client, default_ttl: int = 3600):
        self.redis = redis_client
        self.default_ttl = default_ttl
        self.metrics = Counter()
    
    async def get(self, key: str):
        value = await self.redis.get(key)
        if value:
            self.metrics.increment("hit")
        else:
            self.metrics.increment("miss")
        return value
    
    async def set(self, key: str, value: str, ttl: int = None):
        await self.redis.setex(key, ttl or self.default_ttl, value)
```

---

## Example 2: Streaming for Fast Responses

```python
async def stream_response(prompt: str) -> AsyncGenerator[str, None]:
    """Stream response for immediate user feedback."""
    buffer = ""
    
    async for chunk in model.stream(prompt):
        buffer += chunk
        yield chunk
    
    # Cache complete response
    cache.set(hash(prompt), buffer)
```

### Variations

- Use `Server-Sent Events` for browser delivery.
- Buffer steady-state chunks before flushing to reduce overhead.

### WebSocket Streaming

```python
from fastapi import WebSocket

@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    async for message in ws.iter_text():
        async for chunk in model.stream(message):
            await ws.send_text(chunk)
    await ws.close()
```

### SSE Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/sse/chat")
async def sse_chat(prompt: str):
    async def generate():
        async for chunk in model.stream(prompt):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## Example 3: Parallel Tool Execution

```python
async def execute_tools_parallel(tools: List[Dict], context: Dict) -> List[Any]:
    """Execute multiple tools in parallel."""
    semaphore = asyncio.Semaphore(5)
    
    async def execute_one(tool):
        async with semaphore:
            return await call_tool(tool["name"], tool["args"])
    
    tasks = [execute_one(t) for t in tools]
    return await asyncio.gather(*tasks)
```

### Variations

- Use `TaskGroup` for structured concurrency.
- Collect tool errors instead of letting first failure cancel siblings.

### Structured Concurrency

```python
async def execute_tools_structured(tools: List[Dict], context: Dict) -> List[Any]:
    async def execute_one(tool):
        return await call_tool(tool["name"], tool["args"], context)
    
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(execute_one(t)) for t in tools]
    
    results = [task.result() for task in tasks]
    return results
```

---

## Example 4: Semantic Cache Lookup

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
```

### Variations

- Use approximate nearest neighbor index (FAISS, hnswlib) for larger stores.
- Embed system prompt and user prompt jointly.

### With FAISS

```python
import faiss
import numpy as np

class FAISSCache:
    def __init__(self, embedding_fn, dimension: int = 1536):
        self.embedding_fn = embedding_fn
        self.index = faiss.IndexFlatL2(dimension)
        self.entries = []
    
    async def get(self, query: str, k: int = 1):
        query_emb = self.embedding_fn(query)
        distances, indices = self.index.search(np.array([query_emb]), k)
        if distances[0][0] < 0.5:  # Threshold
            return self.entries[indices[0][0]]
        return None
    
    async def set(self, query: str, value):
        query_emb = self.embedding_fn(query)
        self.index.add(np.array([query_emb]))
        self.entries.append(value)
```

---

## Example 5: Prompt Deduplication

```python
class DeduplicatingCache:
    def __init__(self):
        self._seen: Set[str] = set()
        self._lock = asyncio.Lock()
    
    async def get_or_generate(self, prompt: str, generate_fn):
        fingerprint = hashlib.sha256(prompt.encode()).hexdigest()
        async with self._lock:
            if fingerprint in self._seen:
                existing = await cache.get(f"prompt:{fingerprint}")
                if existing:
                    return existing
            result = await generate_fn(prompt)
            await cache.setex(f"prompt:{fingerprint}", 600, result)
            self._seen.add(fingerprint)
            return result
```

### Deduplication with Bloom Filter

```python
class BloomFilterDeduplicator:
    def __init__(self, capacity: int = 100000, error_rate: float = 0.01):
        self.filter = BloomFilter(capacity, error_rate)
    
    def is_duplicate(self, prompt: str) -> bool:
        return prompt in self.filter
    
    def mark_seen(self, prompt: str):
        self.filter.add(prompt)
```

---

## Example 6: Token-Aware Context Pruning

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

### Sliding Window Pruner

```python
class SlidingWindowPruner:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
    
    def prune(self, messages: List[dict]) -> List[dict]:
        if len(messages) <= self.window_size:
            return messages
        
        # Keep system message and last N messages
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-self.window_size:]
        return system + recent
```

---

## Example 7: Connection Pooling

```python
class PooledClient:
    _session: Optional[aiohttp.ClientSession] = None
    
    @classmethod
    async def session(cls):
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=200,
                    limit_per_host=30,
                    ttl_dns_cache=600,
                ),
                timeout=aiohttp.ClientTimeout(total=30, connect=5, sock_read=10),
            )
        return cls._session
```

### Connection Monitoring

```python
class MonitoredPool:
    def __init__(self):
        self.pool = {}
        self.metrics = {
            "active": Counter(),
            "idle": Counter(),
            "total": Gauge(),
        }
    
    async def acquire(self, name: str):
        conn = await self.pool[name].acquire()
        self.metrics["active"].labels(pool=name).inc()
        return conn
    
    async def release(self, name: str, conn):
        await self.pool[name].release(conn)
        self.metrics["active"].labels(pool=name).dec()
```

---

## Example 8: Resilient API Calls with Retries

```python
async def call_with_retry(fn, *, max_retries=5, base_delay=0.5, max_delay=30):
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

### Using `tenacity` Library

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type((TransientError,)),
)
async def resilient_call():
    return await api.call()
```

---

## Example 9: Circuit Breaker for External APIs

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.state = "closed"
        self.failures = 0
        self.successes = 0
        self.last_failure_time = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError("Circuit is open")
        try:
            result = await func(*args, **kwargs)
        except Exception:
            self._failure()
            raise
        else:
            self._success()
            return result
    
    def _success(self):
        if self.state == "half-open":
            self.successes += 1
            if self.successes >= self.success_threshold:
                self.state = "closed"
                self.failures = 0
        else:
            self.failures = 0
    
    def _failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.state == "half-open" or self.failures >= self.failure_threshold:
            self.state = "open"
```

---

## Example 10: Model Router

```python
class ModelRouter:
    def __init__(self):
        self.routes = {
            "simple":  {"model": "fast-model",  "params": {"temperature": 0}},
            "balanced":{"model": "gpt-4o",      "params": {"temperature": 0.7}},
            "complex": {"model": "o3",           "params": {"temperature": 1.0}},
        }
    
    def select(self, task: str, complexity: float) -> dict:
        if complexity < 0.3:
            return self.routes["simple"]
        if complexity < 0.7:
            return self.routes["balanced"]
        return self.routes["complex"]
```

### Complexity Estimation

```python
class ComplexityEstimator:
    def estimate(self, prompt: str) -> float:
        features = self.extract_features(prompt)
        score = (
            0.3 * features["has_code"] +
            0.2 * features["has_math"] +
            0.2 * features["has_multi_step"] +
            0.15 * features["length"] +
            0.15 * features["has_entities"]
        )
        return min(1.0, max(0.0, score))
    
    def extract_features(self, prompt: str) -> dict:
        return {
            "has_code": 1.0 if "```" in prompt else 0.0,
            "has_math": 1.0 if any(op in prompt for op in ["+", "-", "*", "/", "="]) else 0.0,
            "has_multi_step": 1.0 if "step" in prompt.lower() else 0.0,
            "length": min(1.0, len(prompt) / 1000),
            "has_entities": 1.0 if any(c.isupper() for c in prompt) else 0.0,
        }
```

---

## Example 11: Adaptive Batching

```python
class AdaptiveBatcher:
    def __init__(self, target_latency: float = 1.0, min_batch: int = 1, max_batch: int = 64):
        self.target_latency = target_latency
        self.current_batch = min_batch
        self.latencies: deque = deque(maxlen=20)
    
    async def process(self, items: List[Any], process_fn):
        batch_size = self.current_batch
        start = time.perf_counter()
        result = await process_fn(items[:batch_size])
        elapsed = time.perf_counter() - start
        self.latencies.append(elapsed)
        self._tune_batch()
        return result
    
    def _tune_batch(self):
        if not self.latencies:
            return
        avg = sum(self.latencies) / len(self.latencies)
        if avg < self.target_latency * 0.5:
            self.current_batch = min(self.current_batch + 1, 64)
        elif avg > self.target_latency * 1.5:
            self.current_batch = max(self.current_batch - 1, 1)
```

---

## Example 12: Streaming to Frontend

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/stream")
async def chat_stream(prompt: str):
    async def generate():
        async for chunk in model.stream(prompt):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")
```

### Variations

- Use WebSockets for bidirectional streaming.
- Use Server-Sent Events for simple server-to-client push.

### With Backpressure

```python
class BackpressureStreamer:
    def __init__(self, max_queue: int = 100):
        self.queue = asyncio.Queue(maxsize=max_queue)
    
    async def stream(self):
        while True:
            chunk = await self.queue.get()
            yield chunk
            self.queue.task_done()
```

---

## Example 13: Distributed Tracing

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class TracedAgent:
    async def process(self, prompt: str):
        with tracer.start_as_current_span("agent.process") as span:
            span.set_attribute("prompt.length", len(prompt))
            span.set_attribute("prompt.tokens", estimate_tokens(prompt))
            
            with tracer.start_as_current_span("model.call"):
                response = await self._call_model(prompt)
            
            with tracer.start_as_current_span("tool.execute"):
                tools_result = await self._execute_tools(response)
            
            span.set_attribute("response.length", len(tools_result))
            return tools_result
```

---

## Example 14: Budget Enforcement

```python
class BudgetEnforcer:
    def __init__(self, daily_limit_usd: float, price_per_1k_prompt: float, price_per_1k_completion: float):
        self.daily_limit_usd = daily_limit_usd
        self.price_per_1k_prompt = price_per_1k_prompt
        self.price_per_1k_completion = price_per_1k_completion
        self.spend: Dict[str, float] = defaultdict(float)
    
    def estimate_cost(self, prompt_tokens: int, max_completion_tokens: int) -> float:
        prompt_cost = prompt_tokens / 1000 * self.price_per_1k_prompt
        completion_cost = max_completion_tokens / 1000 * self.price_per_1k_completion
        return prompt_cost + completion_cost
    
    def allow(self, user_id: str, prompt_tokens: int, max_completion_tokens: int) -> bool:
        estimated = self.estimate_cost(prompt_tokens, max_completion_tokens)
        return self.spend[user_id] + estimated <= self.daily_limit_usd
    
    def record(self, user_id: str, actual_prompt_tokens: int, actual_completion_tokens: int):
        actual = self.estimate_cost(actual_prompt_tokens, actual_completion_tokens)
        self.spend[user_id] += actual
```

---

## Example 15: Multi-Level Cache with Write-Through

```python
import redis.asyncio as redis
from functools import lru_cache

class MultiLevelCache:
    def __init__(self, redis_url: str, default_ttl: int = 300):
        self.l1 = lru_cache(maxsize=1000)
        self.l2 = redis.from_url(redis_url)
        self.default_ttl = default_ttl
    
    async def get(self, key: str):
        value = self.l1.get(key)
        if value is not None:
            return value
        value = await self.l2.get(key)
        if value is not None:
            self.l1.set(key, value)
        return value
    
    async def set(self, key: str, value: str) -> None:
        self.l1.set(key, value)
        await self.l2.setex(key, self.default_ttl, value)
```

### Variations

- Use `cachetools.LRUCache` instead of `lru_cache` for mutable state.
- Add a disk tier for very large objects.

---

## Example 16: Token Counting with Provider Tokenizer

```python
from tiktoken import encoding_for_model

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    enc = encoding_for_model(model)
    return len(enc.encode(text))

# Estimate from prompt budget
class TokenBudgetManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.allocations = {
            "system_prompt": 0.1,
            "retrieval_context": 0.3,
            "conversation_history": 0.4,
            "response": 0.2,
        }
    
    def allowable(self, component: str) -> int:
        return int(self.max_tokens * self.allocations[component])
```

---

## Example 17: Parallel Retrieval

```python
async def retrieve_parallel(sources: List[str], query: str) -> List[dict]:
    async def fetch(source: str):
        return await vector_store.search(source, query, top_k=5)
    
    results = await asyncio.gather(*[fetch(s) for s in sources])
    return [r for group in results for r in group]
```

### Parallel Retrieval with Semantic Rerank

```python
async def retrieve_with_rerank(sources: List[str], query: str, embed_fn, top_k: int = 5) -> List[dict]:
    raw_results = await retrieve_parallel(sources, query)
    query_emb = embed_fn(query)
    scored = []
    for doc in raw_results:
        doc_emb = embed_fn(doc["content"])
        sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
        scored.append((sim, doc))
    scored.sort(reverse=True)
    return [doc for _, doc in scored[:top_k]]
```

---

## Example 18: Graceful Degradation

```python
class GracefulAgent:
    async def process(self, prompt: str):
        try:
            context = await retrieval.get(prompt)
            return await model.complete(prompt, context)
        except RetrievalTimeoutError:
            return await model.complete(prompt, context=None)
        except ModelProviderError:
            return {"error": "Model temporarily unavailable", "retry_after": 30}
```

### Fallback Strategies

```python
class FallbackPipeline:
    def __init__(self, primary, secondary, fallback):
        self.primary = primary
        self.secondary = secondary
        self.fallback = fallback
    
    async def execute(self, prompt: str):
        try:
            return await self.primary(prompt)
        except PrimaryError:
            try:
                return await self.secondary(prompt)
            except SecondaryError:
                return await self.fallback(prompt)
```

---

## Example 19: Token Compression

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

### Lossless Compression

```python
def compress_lossless(text: str) -> str:
    import zlib
    import base64
    compressed = zlib.compress(text.encode())
    return base64.b64encode(compressed).decode()
```

---

## Example 20: Adaptive Concurrency Control

```python
class AdaptiveConcurrency:
    def __init__(self, initial: int = 10, min_c: int = 1, max_c: int = 100):
        self.semaphore = asyncio.Semaphore(initial)
        self.current = initial
        self.min = min_c
        self.max = max_c
        self.errors: deque = deque(maxlen=100)
    
    def record_success(self):
        if not self.errors:
            self.current = min(self.max, self.current + 1)
            self.semaphore = asyncio.Semaphore(self.current)
    
    def record_failure(self):
        self.errors.append(1)
        if len(self.errors) / 100 > 0.05:
            self.current = max(self.min, self.current - 1)
            self.semaphore = asyncio.Semaphore(self.current)
```

---

## Example 21: Semantic Cache with Redis

```python
import redis.asyncio as redis
import numpy as np

class SemanticRedisCache:
    def __init__(self, redis_url: str, embedding_fn, dimension: int = 1536):
        self.redis = redis.from_url(redis_url)
        self.embedding_fn = embedding_fn
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.key_map: List[str] = []
    
    async def get(self, query: str, k: int = 1):
        query_emb = self.embedding_fn(query)
        distances, indices = self.index.search(np.array([query_emb]), k)
        if distances[0][0] < 0.5:
            key = self.key_map[indices[0][0]]
            return await self.redis.get(key)
        return None
    
    async def set(self, query: str, value: str):
        query_emb = self.embedding_fn(query)
        key = hashlib.sha256(query.encode()).hexdigest()
        self.index.add(np.array([query_emb]))
        self.key_map.append(key)
        await self.redis.setex(key, 3600, value)
```

---

## Example 22: Hot Key Detection

```python
class HotKeyDetector:
    def __init__(self, threshold: int = 100):
        self.threshold = threshold
        self.access_counts: Counter = Counter()
    
    def record(self, key: str):
        self.access_counts[key] += 1
    
    def get_hot_keys(self) -> List[str]:
        return [key for key, count in self.access_counts.items() if count >= self.threshold]
    
    def reset(self):
        self.access_counts.clear()
```

### Hot Key Mitigation

```python
class HotKeyMitigator:
    def __init__(self, cache):
        self.cache = cache
        self.local_cache = {}
    
    async def get(self, key: str):
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try distributed cache
        value = await self.cache.get(key)
        if value:
            self.local_cache[key] = value
            return value
        
        return None
    
    def invalidate(self, key: str):
        self.local_cache.pop(key, None)
```

---

## Example 23: Cache Stampede Avoidance

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

## Example 24: Structured Concurrency

```python
async def parallel_with_taskgroup(tasks: List[Callable]):
    async with asyncio.TaskGroup() as tg:
        return [tg.create_task(task()) for task in tasks]

# Usage
async def main():
    results = await parallel_with_taskgroup([
        fetch_user_data,
        fetch_orders,
        fetch_recommendations,
    ])
```

---

## Example 25: Memory Management with Pooling

```python
class ObjectPool:
    def __init__(self, factory, max_size: int = 100):
        self.factory = factory
        self.pool: deque = deque(maxlen=max_size)
    
    def acquire(self):
        if self.pool:
            return self.pool.popleft()
        return self.factory()
    
    def release(self, obj):
        self.pool.append(obj)
```

### Message Pool

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

---

## Example 26: Context Window Sliding Sum

```python
class SlidingWindowContext:
    def __init__(self, window_size: int = 10, max_tokens: int = 8000):
        self.window_size = window_size
        self.max_tokens = max_tokens
        self.messages: List[dict] = []
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._enforce_limits()
    
    def _enforce_limits(self):
        # Remove oldest messages if over window or token limit
        while (
            len(self.messages) > self.window_size or
            self.count_tokens() > self.max_tokens
        ):
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(i)
                    break
    
    def count_tokens(self) -> int:
        return sum(len(self.tokenizer.encode(m["content"])) for m in self.messages)
    
    def get_messages(self) -> List[dict]:
        return self.messages.copy()
```

---

## Example 27: Rate Limiter Implementation

```python
class RateLimiter:
    def __init__(self, rate: int, period: int = 60):
        self.rate = rate
        self.period = period
        self.tokens = rate
        self.last_update = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        async with self.lock:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(self.rate, self.tokens + time_passed * (self.rate / self.period))
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    async def wait(self):
        while not await self.acquire():
            await asyncio.sleep(0.1)
```

### Sliding Window Rate Limiter

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

---

## Example 28: Token Budget per Component

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
    
    def allocate(self, component: str, used: int) -> int:
        available = self.max_for(component)
        return min(available, used)
```

---

## Example 29: Multi-Tier Cache Invalidation

```python
class MultiTierCache:
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
    
    async def get(self, key: str):
        value = await self.l1.get(key)
        if value:
            return value
        value = await self.l2.get(key)
        if value:
            await self.l1.set(key, value)
            return value
        value = await self.l3.get(key)
        if value:
            await self.l2.set(key, value)
            return value
        return None
```

---

## Example 30: Real-Time Cost Tracking

```python
class CostTracker:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pricing = {
            "gpt-4o": {"prompt": 0.0025, "completion": 0.01},
            "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
        }
    
    async def track_request(self, user_id: str, model: str, prompt_tokens: int, completion_tokens: int):
        prices = self.pricing.get(model, {"prompt": 0, "completion": 0})
        cost = (prompt_tokens / 1000) * prices["prompt"] + (completion_tokens / 1000) * prices["completion"]
        await self.redis.hincrbyfloat(f"cost:{user_id}:{date.today().isoformat()}", "total", cost)
        await self.redis.hincrby(f"cost:{user_id}:{date.today().isoformat()}", "requests", 1)
    
    async def get_user_cost(self, user_id: str, date_str: str) -> float:
        data = await self.redis.hgetall(f"cost:{user_id}:{date_str}")
        return float(data.get(b"total", 0))
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Advanced](./advanced.md)
