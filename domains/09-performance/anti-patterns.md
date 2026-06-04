# Performance Domain - Anti-Patterns

## Overview

This document outlines performance anti-patterns in LLM/agentic systems that degrade user experience, increase costs, and waste engineering effort. Understanding these patterns helps teams avoid common pitfalls and build more efficient, reliable systems.

## Table of Contents

1. [Premature Optimization](#1-premature-optimization)
2. [Unnecessary Context Length](#2-unnecessary-context-length)
3. [Blocking External Calls](#3-blocking-external-calls)
4. [No Caching Strategy](#4-no-caching-strategy)
5. [Unbounded Resource Usage](#5-unbounded-resource-usage)
6. [Ignoring Streaming Potential](#6-ignoring-streaming-potential)
7. [Sequential Independent Operations](#7-sequential-independent-operations)
8. [Ignoring Model Selection](#8-ignoring-model-selection)
9. [Over-Engineering for Theoretical Scale](#9-over-engineering-for-theoretical-scale)
10. [Neglecting Observability](#10-neglecting-observability)
11. [Wrong Granularity for Caching](#11-wrong-granularity-for-caching)
12. [Tight Coupling to Provider APIs](#12-tight-coupling-to-provider-apis)
13. [Ignoring Rate Limits](#13-ignoring-rate-limits)
14. [Retry Without Backoff](#14-retry-without-backoff)
15. [Context Corruption via Full History](#15-context-corruption-via-full-history)
16. [Logging PII in Traces](#16-logging-pii-in-traces)
17. [Ignoring Connection Lifecycle](#17-ignoring-connection-lifecycle)
18. [Testing Only Happy Paths](#18-testing-only-happy-paths)
19. [Ignoring Circuit Breakers](#19-ignoring-circuit-breakers)
20. [Synchronous Tool Execution](#20-synchronous-tool-execution)
21. [No Timeout Configuration](#21-no-timeout-configuration)
22. [Ignoring Backpressure](#22-ignoring-backpressure)
23. [Memory Leaks in Long-Running Processes](#23-memory-leaks-in-long-running-processes)
24. [Ignoring Token Counting](#24-ignoring-token-counting)
25. [Over-Caching Dynamic Data](#25-over-caching-dynamic-data)
26. [Ignoring Cache Invalidation](#26-ignoring-cache-invalidation)
27. [No Graceful Degradation](#27-no-graceful-degradation)
28. [Ignoring Error Budgets](#28-ignoring-error-budgets)
29. [Premature Scaling](#29-premature-scaling)
30. [Ignoring Security Implications](#30-ignoring-security-implications)

---

## 1. Premature Optimization

**Problem:** Optimizing before identifying bottlenecks wastes time and reduces code clarity.

```python
# Bad - Complex caching before knowing if needed
class OverOptimizedCache:
    def __init__(self):
        self.l1_cache = {}
        self.l2_cache = {}
        self.l3_cache = {}
        self.write_behind_queue = []
        self.compression_enabled = True
        # 500 lines of over-engineering

# Good - Simple caching, optimize when needed
class SimpleCache:
    def __init__(self, ttl: int = 300):
        self.cache = TTLCache(maxsize=1000, ttl=ttl)
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value
```

**Impact:** Slow feature delivery, harder maintenance, cognitive overhead for new engineers, and wasted engineering budget.

**Symptoms:**
- Codebase has abstractions for problems that have not occurred.
- Engineers spend more time tuning configs than shipping features.
- PRs take longer because reviewers must understand unnecessary complexity.

**Remediation:** instrument first. Add metrics around latency, token count, and cost. Optimize only the top two bottlenecks.

### Real-World Example

A team added a three-tier caching system with write-behind queues before shipping their first feature. Six months later, they discovered the cache hit rate was only 12% because user queries were too unique to benefit from caching. The complex system added 2000 lines of code that needed to be maintained.

**Cost:** 2 engineer-months of wasted effort, plus ongoing maintenance burden.

---

## 2. Unnecessary Context Length

**Problem:** Including redundant context increases token costs and latency.

```python
# Bad - Unlimited context growth
def build_prompt(session_id):
    history = get_full_history(session_id)
    return f"{system_prompt}\n{history}\n{user_input}"

# Good - Context-aware prompting
def build_prompt(session_id, max_tokens=4000):
    context = get_relevant_context(session_id, max_tokens)
    return f"{system_prompt}\n{context}\n{user_input}"
```

**Impact:** Higher API costs, slower TTFB, context window exhaustion on summarization steps, and degraded quality from cramming irrelevant text.

**Symptoms:**
- Prompt tokens grow linearly with session duration.
- Summarization becomes a recurring bottleneck.
- Quality degrades over long conversations.

**Remediation:** Enforce a token budget. Summarize or prune old turns. Use retrieval to keep only relevant history.

### Token Cost Calculation

```python
class TokenCostCalculator:
    def __init__(self, price_per_1k_prompt: float, price_per_1k_completion: float):
        self.prompt_price = price_per_1k_prompt
        self.completion_price = price_per_1k_completion
    
    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        prompt_cost = (prompt_tokens / 1000) * self.prompt_price
        completion_cost = (completion_tokens / 1000) * self.completion_price
        return prompt_cost + completion_cost
```

### Context Length Monitoring

```python
class ContextMonitor:
    def __init__(self, max_context: int = 12000):
        self.max_context = max_context
        self.warnings: List[str] = []
    
    def check_context(self, prompt: str, tokenizer) -> bool:
        tokens = len(tokenizer.encode(prompt))
        if tokens > self.max_context:
            self.warnings.append(f"Context overflow: {tokens} > {self.max_context}")
            return False
        return True
```

---

## 3. Blocking External Calls

**Problem:** Sequential API calls waste time waiting.

```python
# Bad - Sequential calls
def process_multiple_queries(queries):
    results = []
    for q in queries:
        results.append(call_model(q))  # Wait each time
    return results

# Good - Parallel calls
async def process_multiple_queries(queries):
    tasks = [call_model(q) for q in queries]
    return await asyncio.gather(*tasks)
```

**Impact:** Wall-clock time scales linearly instead of in parallel. Throughput is capped at one call at a time.

**Symptoms:**
- Batch processing time is N times the single-request latency.
- Worker processes sit idle while awaiting.

**Remediation:** use `asyncio.gather`, thread pools, or task queues for independent work.

### Parallel Execution Pattern

```python
async def parallel_tool_calls(tools: List[Dict], context: Dict) -> List[Any]:
    """Execute multiple tools in parallel with error handling."""
    semaphore = asyncio.Semaphore(5)
    
    async def execute_one(tool):
        async with semaphore:
            return await call_tool(tool["name"], tool["args"])
    
    tasks = [execute_one(t) for t in tools]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

---

## 4. No Caching Strategy

**Problem:** Repeated identical work explodes costs.

```python
# Bad - Always call API
def get_answer(question):
    return call_model(question)

# Good - Cache frequent queries
cache = TTLCache(maxsize=1000, ttl=3600)

def get_answer(question):
    if question in cache:
        return cache[question]
    result = call_model(question)
    cache[question] = result
    return result
```

**Impact:** Redundant token spend. Higher latency. Poor user experience for repeated queries.

**Symptoms:**
- Cost per request is linear forever.
- Identical questions in quick succession pay full price each time.

**Remediation:** Add memory cache for hot items, Redis for shared caching, and prompt-level deduplication.

### Multi-Level Caching

```python
class MultiLevelCache:
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
```

---

## 5. Unbounded Resource Usage

**Problem:** Unlimited resource consumption causes OOM and crashes.

```python
# Bad - Unbounded growth
class UnlimitedCache:
    def __init__(self):
        self.items = []  # Never trimmed
    
    def add(self, item):
        self.items.append(item)

# Good - Bounded with eviction
class BoundedCache:
    def __init__(self, max_size=1000):
        self.items = collections.deque(maxlen=max_size)
```

**Impact:** Memory pressure spills into swap, then crashes, then downtime.

**Symptoms:**
- RSS grows without bound.
- OOM killer terminates processes.
- Response times degrade before crash.

**Remediation:** Set `maxlen` on queues. Use TTL caches. Monitor RSS via `/metrics`.

### Resource Monitoring

```python
class ResourceMonitor:
    def __init__(self):
        self.memory_threshold = 0.8  # 80% of available memory
        self.check_interval = 60  # seconds
    
    async def monitor(self):
        while True:
            await asyncio.sleep(self.check_interval)
            memory_usage = self.get_memory_usage()
            if memory_usage > self.memory_threshold:
                self.trigger_cleanup()
    
    def get_memory_usage(self) -> float:
        # Implementation depends on platform
        return psutil.virtual_memory().percent / 100.0
    
    def trigger_cleanup(self):
        # Clear caches, close idle connections, etc.
        pass
```

---

## 6. Ignoring Streaming Potential

**Problem:** Eagerly awaiting full responses increases perceived latency even when partial output is valuable.

```python
# Bad - Wait for full response
result = await model.generate(prompt)
return result

# Good - Stream for UX
return StreamingResponse(model.stream(prompt), media_type="text/plain")
```

**Impact:** User waits longer to see first output. UX feels worse even if total wall time is similar.

**Symptoms:**
- Users refresh pages thinking the agent is stuck.
- Time-to-first-token is minutes while total generation is seconds longer.

**Remediation:** stream partial output. Update progress bars. Return structured events for agent frameworks.

### Streaming Implementation

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

---

## 7. Sequential Independent Operations

**Problem:** Running independent steps serially wastes parallelism.

```python
# Bad
summary = summarize(article)
keywords = extract_keywords(article)
entities = extract_entities(article)

# Good
summary, keywords, entities = asyncio.gather(
    summarize(article),
    extract_keywords(article),
    extract_entities(article),
)
```

**Impact:** Latency is the sum of independent operations instead of the max.

**Symptoms:**
- Pipeline time equals the sum of step durations.
- CPU or network is idle while awaiting.

**Remediation:** profile dependency graph. Parallelize reads and lightweight CPU-bound work.

### Dependency Graph Analysis

```python
class DependencyGraph:
    def __init__(self):
        self.graph = {}
    
    def add_dependency(self, task: str, depends_on: str):
        if task not in self.graph:
            self.graph[task] = []
        self.graph[task].append(depends_on)
    
    def find_parallel_tasks(self) -> List[List[str]]:
        # Find tasks that can run in parallel
        visited = set()
        parallel_groups = []
        
        for task in self.graph:
            if task not in visited:
                group = self._find_parallel_group(task, visited)
                if group:
                    parallel_groups.append(group)
        
        return parallel_groups
    
    def _find_parallel_group(self, task: str, visited: set) -> List[str]:
        # Implementation details omitted
        pass
```

---

## 8. Ignoring Model Selection

**Problem:** Using largest model for all tasks wastes cost and latency.

```python
# Bad
for task in tasks:
    response = model_large(task)

# Good
for task in tasks:
    model = router.select(task)
    response = model(task)
```

**Impact:** Simple tasks pay for an oversized model's latency and pricing tier.

**Symptoms:**
- Latency budget is exceeded by straightforward extraction tasks.
- Cost per request is dominated by classification of trivial intents.

**Remediation:** route to smaller or cheaper models for simple tasks. Use a lightweight classifier or confidence gate.

### Model Router Implementation

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

---

## 9. Over-Engineering for Theoretical Scale

**Problem:** Building for million-user scale before validating the actual traffic pattern.

```python
# Bad - Complex sharding before need
class OverShardedCache:
    def __init__(self):
        self.shards = [Cache() for _ in range(256)]
        self.consistent_hash = ConsistentHashRing([f"shard{i}" for i in range(256)])

# Good - Simple cache
cache = TTLCache(maxsize=10000, ttl=600)
```

**Impact:** Increased cognitive load, more failure modes, and slower iteration.

**Symptoms:**
- Engineers debate sharding strategy for weeks before launch.
- System complexity exceeds traffic complexity.

**Remediation:** start simple. add sharding only when a single node cannot hold working set or throughput.

### Scaling Decision Framework

```python
class ScalingDecisionFramework:
    def __init__(self):
        self.scaling_thresholds = {
            "memory": 0.8,  # 80% memory usage
            "cpu": 0.7,     # 70% CPU usage
            "latency": 5000,  # 5 seconds p95
            "error_rate": 0.05,  # 5% error rate
        }
    
    def should_scale(self, metrics: Dict[str, float]) -> bool:
        return any(
            metrics.get(k, 0) > v
            for k, v in self.scaling_thresholds.items()
        )
```

---

## 10. Neglecting Observability

**Problem:** Performance problems are invisible until users complain.

```python
# Bad
async def handle(request):
    return await pipeline(request)

# Good
async def handle(request):
    start = time.perf_counter()
    with tracer.start("pipeline"):
        result = await pipeline(request)
    duration = (time.perf_counter() - start) * 1000
    metrics.latency.observe(duration)
    return result
```

**Impact:** Unknown failure modes, slow incident response, and blind optimization.

**Symptoms:**
- Alerts are based on user complaints, not on metrics.
- Latency regressions are discovered post-release.

**Remediation:** instrument from day one. Track latency, tokens, errors, and cost per request.

### Observability Checklist

```python
class ObservabilityChecker:
    def __init__(self):
        self.required_metrics = [
            "latency_p50",
            "latency_p95",
            "latency_p99",
            "error_rate",
            "cache_hit_rate",
            "token_count",
            "cost_per_request",
        ]
    
    def check_instrumentation(self, code: str) -> List[str]:
        missing = []
        for metric in self.required_metrics:
            if metric not in code:
                missing.append(f"Missing metric: {metric}")
        return missing
```

---

## 11. Wrong Granularity for Caching

**Problem:** Caching too aggressively or coarsely causes stale data or low hit rates.

```python
# Bad - Cache entire documents
cache.set("doc", entire_document)

# Good - Cache chunks or summaries
cache.set("doc:chunk:0", chunk_0)
cache.set("doc:summary", summary)
```

**Impact:** Cache invalidates frequently if backing document changes often. Hit rate is low if chunks are too fine.

**Symptoms:**
- Cache hit rate is near zero.
- Users receive stale information after content updates.

**Remediation:** Cache at the granularity of actual query patterns. Invalidate on known update events.

### Cache Granularity Analysis

```python
class CacheGranularityAnalyzer:
    def __init__(self):
        self.query_patterns = []
        self.cache_hits = {}
    
    def analyze_query_patterns(self, queries: List[str]) -> Dict[str, int]:
        patterns = {}
        for query in queries:
            # Normalize query
            normalized = self.normalize_query(query)
            patterns[normalized] = patterns.get(normalized, 0) + 1
        return patterns
    
    def normalize_query(self, query: str) -> str:
        # Remove variable parts, standardize formatting
        return re.sub(r'\d+', 'N', query.strip().lower())
```

---

## 12. Tight Coupling to Provider APIs

**Problem:** Switching providers requires rewriting call sites.

```python
# Bad
import openai

# Hardcoded provider
response = openai.ChatCompletion.create(model="gpt-4o", ...)

# Good - Adapter pattern
class ModelClient:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
    
    async def complete(self, messages):
        # Delegate to provider-specific adapter
        return await adapter.dispatch(self.provider, self.model, messages)
```

**Impact:** Switching from provider A to B is an embarrassing refactor instead of a config change.

**Symptoms:**
- Team is locked into one vendor due to code coupling.
- New features are delayed because of missing provider-native features.

**Remediation:** abstract provider interfaces behind adapters. Test with multiple providers in CI.

### Provider Adapter Pattern

```python
class ModelAdapter(ABC):
    @abstractmethod
    async def complete(self, messages: List[dict], **kwargs) -> str:
        pass

class OpenAIAdapter(ModelAdapter):
    async def complete(self, messages: List[dict], **kwargs) -> str:
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

class AnthropicAdapter(ModelAdapter):
    async def complete(self, messages: List[dict], **kwargs) -> str:
        response = await anthropic.Client().completion(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.completion

class ModelClient:
    def __init__(self, adapter: ModelAdapter):
        self.adapter = adapter
    
    async def complete(self, messages: List[dict], **kwargs) -> str:
        return await self.adapter.complete(messages, **kwargs)
```

---

## 13. Ignoring Rate Limits

**Problem:** Hard-coding request rates causes 429 errors and request loss.

```python
# Bad
async def send_requests(requests):
    return await asyncio.gather(*[client.post(r) for r in requests])

# Good
limiter = asyncio.Semaphore(max_concurrent=10)

async def send_requests(requests):
    async def bounded(request):
        async with limiter:
            return await client.post(request)
    return await asyncio.gather(*[bounded(r) for r in requests])
```

**Impact:** 429 errors cause retries that amplify load. Thundering-herd effects cascade across services.

**Symptoms:**
- Spike in HTTP 429 responses after traffic increases.
- Downstream services receive retry storms.

**Remediation:** add per-provider rate limiter. Respect `Retry-After` headers. Use exponential backoff with jitter.

### Rate Limiter Implementation

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

---

## 14. Retry Without Backoff

**Problem:** Aggressive retries hammer failing services and make outages worse.

```python
# Bad
for _ in range(5):
    try:
        return await api.call()
    except Exception:
        await asyncio.sleep(0.1)  # Fixed sleep is insufficient
        continue
raise MaxRetriesExceeded()

# Good
@backoff.on_exception(backoff.expo, Exception, max_tries=5, max_time=30)
async def resilient_call():
    return await api.call()
```

**Impact:** Thundering-herd retries crash already struggling services. Amplified latency during incidents.

**Symptoms:**
- Outages last longer than the original failure.
- Downstream systems show retry spikes correlated with upper-layer failures.

**Remediation:** use exponential backoff with full jitter. Set max total timeout. Implement circuit breakers.

### Exponential Backoff with Jitter

```python
async def call_with_backoff(fn, max_retries=5, base_delay=0.5, max_delay=30):
    for attempt in range(max_retries):
        try:
            return await fn()
        except TransientError:
            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, delay)
            await asyncio.sleep(delay + jitter)
    raise MaxRetriesExceeded()
```

---

## 15. Context Corruption via Full History

**Problem:** Passing the entire conversation history to every prompt keeps stale, contradictory, or redundant context.

```python
# Bad - Include everything
prompt = system_prompt + "\n" + full_history + "\n" + user_input

# Good - Sliding window + summary
prompt = system_prompt + "\n" + summarize_recent(full_history, window=20) + "\n" + user_input
```

**Impact:** Token budget exhaustion. Quality degradation as model weighs contradictory older context against recent facts.

**Symptoms:**
- Long conversations produce answers opposite to recent user statements.
- Token usage grows unbounded.

**Remediation:** implement summarization. Use sliding windows. Deduplicate repeated tool outputs.

### Context Management Strategies

```python
class ContextManager:
    def __init__(self, max_tokens: int = 12000, summary_threshold: int = 8000):
        self.max_tokens = max_tokens
        self.summary_threshold = summary_threshold
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
    
    def build_context(self, messages: List[dict]) -> List[dict]:
        current_tokens = sum(len(self.tokenizer.encode(m["content"])) for m in messages)
        
        if current_tokens <= self.max_tokens:
            return messages
        
        # Keep system message and last N messages
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-10:]
        
        # Summarize middle
        middle = messages[1:-10]
        summary = self.summarize(middle)
        
        return system + [summary] + recent
    
    def summarize(self, messages: List[dict]) -> dict:
        combined = "\n".join(m["content"] for m in messages)
        return {
            "role": "system",
            "content": f"[Summary of {len(messages)} earlier messages]"
        }
```

---

## 16. Logging PII in Traces

**Problem:** Capturing full prompt and completion content in observability tools leaks sensitive data.

```python
# Bad
span.set_attribute("prompt", full_prompt)
span.set_attribute("completion", full_completion)

# Good - Hash or redact
prompt_hash = hashlib.sha256(full_prompt.encode()).hexdigest()[:16]
span.set_attribute("prompt_hash", prompt_hash)
span.set_attribute("prompt_token_count", count_tokens(full_prompt))
```

**Impact:** Regulatory violations. Data breach risk. Customer trust loss.

**Symptoms:**
- PagerDuty or Datadog reports contain user data.
- Compliance audits flag traces for PII.

**Remediation:** log hashes and counts, not raw text. Redact PII before emitting spans.

### PII Redaction

```python
class PIIRedactor:
    def __init__(self):
        self.patterns = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]'),
            (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),
            (r'\b[A-Z]{2}\d{7}\b', '[PASSPORT]'),
        ]
    
    def redact(self, text: str) -> str:
        redacted = text
        for pattern, replacement in self.patterns:
            redacted = re.sub(pattern, replacement, redacted)
        return redacted
    
    def hash_if_needed(self, text: str, threshold: int = 100) -> str:
        if len(text) > threshold:
            return hashlib.sha256(text.encode()).hexdigest()[:16]
        return text
```

---

## 17. Ignoring Connection Lifecycle

**Problem:** Creating new HTTP sessions for every request causes connection churn and TLS overhead.

```python
# Bad - New session per request
async def call(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

# Good - Reuse pooled session
class PooledClient:
    _session = None
    @classmethod
    async def session(cls):
        if cls._session is None:
            cls._session = aiohttp.ClientSession()
        return cls._session
```

**Impact:** High latency from TLS handshakes. Resource leakage from unclosed sessions.

**Symptoms:**
- Connection churn visible in OS-level socket stats.
- TLS renegotiation dominates latency.

**Remediation:** use connection pools. Set keepalive. Close sessions gracefully on shutdown.

### Connection Pool Best Practices

```python
class PooledHttpClient:
    """Reuse HTTP connections for performance."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=200,
                    limit_per_host=30,
                    ttl_dns_cache=600,
                    enable_cleanup_closed=True,
                ),
                timeout=aiohttp.ClientTimeout(total=30, connect=5, sock_read=10),
            )
        return cls._instance
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
```

---

## 18. Testing Only Happy Paths

**Problem:** Performance tests only run under ideal conditions, missing degradation under stress.

```python
# Bad
def test_single_request():
    response = await model.complete(prompt)
    assert len(response) > 0

# Good
@pytest.mark.parametrize("concurrency", [1, 10, 50, 100])
async def test_scaling(concurrency):
    tasks = [model.complete(prompt) for _ in range(concurrency)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    failures = [r for r in responses if isinstance(r, Exception)]
    assert len(failures) / concurrency < 0.01
```

**Impact:** Regressions slip to production. Latency under load is unknown until cascading failures occur.

**Symptoms:**
- Load tests pass but prod SLOs are violated.
- p99 latency is five times the average in production.

**Remediation:** run load tests at peak concurrency plus margin. Measure tail latency. Test with failure injection.

---

## 19. Ignoring Circuit Breakers

**Problem:** Without circuit breakers, failures cascade through the system.

```python
# Bad - No circuit breaker
async def call_external():
    response = await api.call()
    return response

# Good - With circuit breaker
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"
        self.failures = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
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
        if self.failures >= self.failure_threshold:
            self.state = "open"
            # Schedule recovery
            asyncio.get_event_loop().call_later(
                self.recovery_timeout, self._try_half_open
            )
    
    def _try_half_open(self):
        self.state = "half-open"
```

**Impact:** Cascading failures take down entire systems. Recovery takes much longer than necessary.

**Symptoms:**
- One failing service brings down multiple dependent services.
- Recovery time is hours instead of minutes.

**Remediation:** add circuit breakers to all external calls. Configure appropriate thresholds.

---

## 20. Synchronous Tool Execution

**Problem:** Running tools sequentially when they could run in parallel.

```python
# Bad - Sequential execution
def run_tools(tools):
    results = []
    for tool in tools:
        results.append(tool.execute())
    return results

# Good - Parallel execution
async def run_tools_parallel(tools):
    tasks = [tool.execute() for tool in tools]
    return await asyncio.gather(*tasks)
```

**Impact:** Agent response time is the sum of all tool latencies instead of the maximum.

**Symptoms:**
- Agent response time grows linearly with number of tools.
- Users wait unnecessarily long for parallelizable operations.

**Remediation:** identify independent tools and execute them concurrently.

### Tool Dependency Analysis

```python
class ToolDependencyAnalyzer:
    def __init__(self):
        self.dependencies = {}
    
    def add_dependency(self, tool: str, depends_on: str):
        if tool not in self.dependencies:
            self.dependencies[tool] = set()
        self.dependencies[tool].add(depends_on)
    
    def get_execution_order(self) -> List[List[str]]:
        # Topological sort to find parallel execution groups
        visited = set()
        result = []
        
        def visit(tool):
            if tool in visited:
                return
            visited.add(tool)
            deps = self.dependencies.get(tool, set())
            for dep in deps:
                visit(dep)
            # Add to current group
            if not result:
                result.append([])
            result[-1].append(tool)
        
        for tool in self.dependencies:
            visit(tool)
        
        return result
```

---

## 21. No Timeout Configuration

**Problem:** External calls without timeouts can hang indefinitely.

```python
# Bad - No timeout
response = await requests.get(url)

# Good - With timeout
response = await requests.get(url, timeout=10)
```

**Impact:** Hanging requests consume resources and degrade system performance.

**Symptoms:**
- Thread pool exhaustion.
- Increasing memory usage.
- Unresponsive services.

**Remediation:** set reasonable timeouts on all external calls. Implement connection pool limits.

### Timeout Configuration

```python
class TimeoutConfig:
    def __init__(self):
        self.default_timeout = 10
        self.connection_timeout = 5
        self.read_timeout = 30
    
    def get_timeout(self, operation: str) -> int:
        timeouts = {
            "api_call": 10,
            "database": 5,
            "cache": 2,
            "file_io": 15,
        }
        return timeouts.get(operation, self.default_timeout)
```

---

## 22. Ignoring Backpressure

**Problem:** Systems don't handle load gracefully, leading to OOM or crashes.

```python
# Bad - Ignore backpressure
def produce_data(queue, data_source):
    for data in data_source:
        queue.put(data)  # Can grow unbounded

# Good - Respect backpressure
async def produce_data(queue, data_source):
    for data in data_source:
        await queue.put(data)  # Will backpressure if full
```

**Impact:** Memory exhaustion, queue overflow, system crashes.

**Symptoms:**
- Memory usage grows linearly with load.
- Queue sizes grow without bound.
- System becomes unresponsive.

**Remediation:** use bounded queues, implement flow control, add circuit breakers.

---

## 23. Memory Leaks in Long-Running Processes

**Problem:** Resources not properly released leak memory over time.

```python
# Bad - Leaking resources
class LeakyCache:
    def __init__(self):
        self.cache = {}
    
    def add(self, key, value):
        self.cache[key] = value  # Never removes old entries

# Good - Bounded cache
class BoundedCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def add(self, key, value):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = value
```

**Impact:** Gradual performance degradation, eventual crashes, increased costs.

**Symptoms:**
- Memory usage increases over time.
- Garbage collection becomes more frequent.
- Response times degrade.

**Remediation:** implement resource cleanup, use weak references, monitor memory.

---

## 24. Ignoring Token Counting

**Problem:** Not tracking token usage leads to unexpected costs and errors.

```python
# Bad - No token tracking
response = await model.complete(prompt)

# Good - Track tokens
response, usage = await model.complete(prompt, return_usage=True)
logger.info(f"Tokens used: {usage.prompt_tokens} + {usage.completion_tokens}")
```

**Impact:** Unexpected API costs, hitting token limits, budget overruns.

**Symptoms:**
- Monthly bills are higher than expected.
- Requests fail with token limit errors.
- Budget alerts trigger unexpectedly.

**Remediation:** track token usage per request, set budgets, implement warnings.

---

## 25. Over-Caching Dynamic Data

**Problem:** Caching data that changes frequently serves stale results.

```python
# Bad - Cache dynamic data
cache.set("user:123:profile", user_profile, ttl=3600)

# Good - Short TTL or no cache
cache.set("user:123:profile", user_profile, ttl=60)
```

**Impact:** Users see outdated information, incorrect behavior, data inconsistencies.

**Symptoms:**
- Users report seeing old data.
- Data updates don't appear immediately.
- Inconsistent behavior across requests.

**Remediation:** use appropriate TTLs, implement cache invalidation, consider event-driven invalidation.

---

## 26. Ignoring Cache Invalidation

**Problem:** Cache invalidation is hard, but ignoring it leads to stale data.

```python
# Bad - Never invalidate
cache.set("data", data)

# Good - Invalidate on update
def update_data(key, new_data):
    db.update(key, new_data)
    cache.delete(key)
```

**Impact:** Stale data served to users, incorrect decisions, data corruption.

**Symptoms:**
- Data updates don't appear in responses.
- Old data persists after updates.
- Inconsistent state between cache and database.

**Remediation:** implement explicit invalidation, use versioning, monitor cache hit rates.

---

## 27. No Graceful Degradation

**Problem:** System fails completely instead of degrading gracefully.

```python
# Bad - All or nothing
if not cache.get("data"):
    raise CacheMissError()

# Good - Graceful degradation
data = cache.get("data") or await fetch_from_db()
```

**Impact:** Complete service outages, poor user experience, cascading failures.

**Symptoms:**
- Services fail entirely when one component fails.
- Users get error pages instead of degraded content.
- Cascading failures across services.

**Remediation:** implement fallbacks, use default values, add circuit breakers.

---

## 28. Ignoring Error Budgets

**Problem:** No tracking of acceptable error rates leads to quality degradation.

```python
# Bad - No error budget
# Just keep retrying

# Good - Track error budget
class ErrorBudget:
    def __init__(self, budget_percent: float = 0.1):
        self.budget = budget_percent
        self.errors = 0
        self.total = 0
    
    def record(self, success: bool):
        self.total += 1
        if not success:
            self.errors += 1
    
    def remaining(self) -> float:
        if self.total == 0:
            return 1.0
        error_rate = self.errors / self.total
        return max(0, self.budget - error_rate)
```

**Impact:** Uncontrolled error rates, degraded user experience, missed SLOs.

**Remediation:** define error budgets, monitor them, take action when exhausted.

---

## 29. Premature Scaling

**Problem:** Scaling components before they're needed wastes resources.

```python
# Bad - Scale immediately
def __init__(self):
    self.shards = [Connection() for _ in range(16)]
    self.load_balancer = LoadBalancer(self.shards)

# Good - Scale when needed
def __init__(self):
    self.connection = Connection()
    self.shards = None
    self.load_balancer = None
    
    async def get_connection(self):
        if self.shards is None:
            # Scale based on actual load
            pass
        return self.load_balancer.get_connection()
```

**Impact:** Unnecessary complexity, higher costs, harder debugging.

**Symptoms:**
- Infrastructure costs are higher than necessary.
- System complexity exceeds actual needs.
- Engineers spend time optimizing non-bottlenecks.

**Remediation:** start simple, measure, then scale based on actual metrics.

---

## 30. Ignoring Security Implications

**Problem:** Performance optimizations that compromise security.

```python
# Bad - Disable SSL for performance
connector = aiohttp.TCPConnector(ssl=False)

# Good - Secure and performant
connector = aiohttp.TCPConnector(
    ssl=True,
    ssl_context=ssl.create_default_context(),
    limit=100,
    enable_cleanup_closed=True,
)
```

**Impact:** Security vulnerabilities, data breaches, compliance violations.

**Symptoms:**
- Security scans flag issues.
- Data transmitted insecurely.
- Compliance failures.

**Remediation:** never compromise security for performance. Use secure defaults.

---

## Decision Framework for Anti-Pattern Prevention

### Pre-Deployment Checklist

- [ ] All external calls have timeouts
- [ ] Connection pooling is configured
- [ ] Caching strategy is appropriate
- [ ] Token usage is tracked
- [ ] Error budgets are defined
- [ ] Circuit breakers are in place
- [ ] Logs are sanitized
- [ ] Tests cover failure scenarios
- [ ] Observability is implemented
- [ ] Security review passed

### Incident Review Template

When a performance incident occurs:

1. **Timeline:** When did it start? When was it detected? When was it resolved?
2. **Impact:** How many users affected? What was the business impact?
3. **Root Cause:** What anti-pattern contributed? Why wasn't it caught earlier?
4. **Remediation:** What was done to fix it?
5. **Prevention:** What will prevent recurrence?

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
