# Performance Domain - Fundamentals

## Overview

This document covers fundamental performance principles for LLM/agentic systems, including latency optimization, caching strategies, resource management, and cost control.

## Table of Contents

1. [Measure First](#1-measure-first)
2. [Profile Before Optimizing](#2-profile-before-optimizing)
3. [Token Budget Management](#3-token-budget-management)
4. [Key Performance Metrics](#4-key-performance-metrics)
5. [Latency Fundamentals](#5-latency-fundamentals)
6. [Caching Fundamentals](#6-caching-fundamentals)
7. [Async I/O Fundamentals](#7-async-io-fundamentals)
8. [Token Economics](#8-token-economics)
9. [Resource Lifecycle](#9-resource-lifecycle)
10. [Error Handling Fundamentals](#10-error-handling-fundamentals)
11. [Observability Fundamentals](#11-observability-fundamentals)
12. [Cost Fundamentals](#12-cost-fundamentals)
13. [Testing Fundamentals](#13-testing-fundamentals)
14. [Infrastructure Fundamentals](#14-infrastructure-fundamentals)
15. [Performance Budgets](#15-performance-budgets)
16. [Latency Budgets](#16-latency-budgets)
17. [Token Budgets](#17-token-budgets)
18. [Resource Management](#18-resource-management)
19. [Context Management](#19-context-management)
20. [Tool Execution Fundamentals](#20-tool-execution-fundamentals)
21. [Retry and Backoff](#21-retry-and-backoff)
22. [Circuit Breakers](#22-circuit-breakers)
23. [Bulkhead Pattern](#23-bulkhead-pattern)
24. [Rate Limiting](#24-rate-limiting)
25. [Monitoring Fundamentals](#25-monitoring-fundamentals)
26. [Logging Fundamentals](#26-logging-fundamentals)
27. [Alerting Fundamentals](#27-alerting-fundamentals)
28. [Dashboards and Visualization](#28-dashboards-and-visualization)
29. [Cost Management](#29-cost-management)
30. [Provider Economics](#30-provider-economics)

---

## 1. Measure First

```python
import time
from contextlib import contextmanager
from typing import Dict

@contextmanager
def timer(name: str):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    logger.info(f"PERF: {name}", duration_ms=elapsed * 1000)

class PerformanceMetrics:
    """Track performance metrics for agent operations."""
    
    def __init__(self):
        self.measurements: Dict[str, list] = {}
    
    def record(self, operation: str, duration_ms: float) -> None:
        if operation not in self.measurements:
            self.measurements[operation] = []
        self.measurements[operation].append(duration_ms)
    
    def get_percentile(self, operation: str, percentile: float) -> float:
        values = sorted(self.measurements.get(operation, []))
        if not values:
            return 0
        idx = int(len(values) * percentile / 100)
        return values[min(idx, len(values) - 1)]
    
    def summary(self) -> Dict:
        return {
            op: {
                "count": len(vals),
                "p50": self.get_percentile(op, 50),
                "p95": self.get_percentile(op, 95),
                "p99": self.get_percentile(op, 99)
            }
            for op, vals in self.measurements.items()
        }
```

### Profiling in Production

```python
import cProfile
import pstats

def profile_agent_call(prompt: str) -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    
    response = agent.process(prompt)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    return response
```

### Tracing Best Practices

Use distributed tracing to correlate request-level tokens, latency, and cost.

---

## 2. Profile Before Optimizing

Profile the agent end-to-end. Identify the top three functions by cumulative time.

```python
def profile_agent_call(prompt: str) -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    
    response = agent.process(prompt)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
    
    return response
```

### Flame Graph Generation

```bash
python -m cProfile -o agent.prof agent.py
py-spy record -d 30 --pid $(pidof agent) -o flame.svg
```

---

## 3. Token Budget Management

```python
class TokenBudgetManager:
    """Manage token usage for optimal performance."""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.allocations = {
            "system_prompt": 0.1,
            "retrieval_context": 0.3,
            "conversation_history": 0.4,
            "response": 0.2
        }
    
    def get_allocation(self, component: str) -> int:
        return int(self.max_tokens * self.allocations.get(component, 0))
    
    def optimize_context(self, messages: list, retrieval: list) -> list:
        """Optimize context within token budget."""
        total_tokens = sum(self._estimate_tokens(m["content"]) for m in messages)
        
        optimized = []
        current_tokens = 0
        
        for msg in reversed(messages):
            msg_tokens = self._estimate_tokens(msg["content"])
            if current_tokens + msg_tokens <= self.get_allocation("conversation_history"):
                optimized.insert(0, msg)
                current_tokens += msg_tokens
        
        return optimized
    
    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)
```

### Budget Enforcement Pattern

```python
class BudgetEnforcer:
    def __init__(self, budget: int):
        self.budget = budget
    
    def enforce(self, messages: list) -> list:
        tokens = sum(len(m["content"]) for m in messages)
        if tokens <= self.budget:
            return messages
        # trim oldest messages
        return messages[: len(messages) - self.budget]
```

---

## 4. Key Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to First Token | < 500ms | p50 latency |
| Response Completion | < 5s | p95 latency |
| Token Efficiency | High | Output/input ratio |
| Cost per Request | Budget | API cost tracking |
| Cache Hit Rate | > 80% | Cache metrics |

### Metric Definitions

- **Time to First Token (TTFT)**: time from request arrival to first byte of response.
- **Time to Completion (TTC)**: time from request arrival to full response.
- **Cache Hit Rate**: percentage of requests served by cache.
- **Cost per Request**: API spend divided by number of requests.

---

## 5. Latency Fundamentals

Latency is the time from request to first byte and to full completion. Optimize both independently.

### Latency Budgets

```python
class LatencyBudget:
    def __init__(self):
        self.budgets = {
            "queue": 0.05,
            "retrieval": 0.20,
            "model_p95": 0.50,
            "tool_execution": 0.15,
            "serialization": 0.10,
        }
    
    def remaining(self, spent: Dict[str, float]) -> Dict[str, float]:
        return {k: max(0, self.budgets[k] - spent.get(k, 0)) for k in self.budgets}
```

### P99 is the Real Customer Experience

Average latency hides tail pain. Monitor p95 and p99 alongside p50.

```python
class TailLatencyMonitor:
    def __init__(self, samples: int = 1000):
        self.samples: deque = deque(maxlen=samples)
    
    def record(self, latency_ms: float):
        self.samples.append(latency_ms)
    
    def p95(self) -> float:
        return float(np.percentile(self.samples, 95))
    
    def p99(self) -> float:
        return float(np.percentile(self.samples, 99))
```

### Latency Reduction Tactics

1. Streaming reduces TTFB.
2. Parallelizing tool calls reduces TTC.
3. Smaller models reduce model latency.
4. Caching eliminates round trips.

---

## 6. Caching Fundamentals

Cache at the granularity of actual query patterns. Invalidate on known update events.

### Cache Patterns

```python
class CacheAsideExample:
    async def get(self, key: str):
        cached = await cache.get(key)
        if cached is not None:
            return cached
        value = await db_fetch(key)
        if value is not None:
            await cache.setex(key, 3600, value)
        return value
```

### Cache Key Hygiene

```python
class CacheKeyHygiene:
    @staticmethod
    def build(prompt: str, model: str, policy_version: str) -> str:
        normal = CacheKeyHygiene._normalize(prompt)
        raw = f"{policy_version}:{model}:{normal}"
        return hashlib.sha256(raw.encode()).hexdigest()
    
    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip()).lower()
```

### Cache Invalidation Triggers

- Data update events (write-through, write-behind signal).
- Scheduled timeouts (TTL).
- Semantic version bumps for prompts or policies.

---

## 7. Async I/O Fundamentals

Use async for all I/O. Avoid blocking calls in the event loop.

```python
async def fetch_all(urls: List[str]) -> List[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.text() for r in responses]
```

### Thread Pool Offloading

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def run_blocking(fn, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, fn, *args)
```

### Structured Concurrency

```python
async def parallel_with_taskgroup(tasks: List[Callable]):
    async with asyncio.TaskGroup() as tg:
        return [tg.create_task(task()) for task in tasks]
```

---

## 8. Token Economics

Track prompt tokens, completion tokens, and cost per request.

### Cost per Request Formula

```
cost = (prompt_tokens / 1000) * prompt_price + (completion_tokens / 1000) * completion_price + retrieval_cost + tool_cost
```

```python
class TokenEconomics:
    def __init__(self, price_per_1k_prompt: float, price_per_1k_completion: float):
        self.prompt_price = price_per_1k_prompt
        self.completion_price = price_per_1k_completion
    
    def cost_for(self, prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens / 1000) * self.prompt_price + (completion_tokens / 1000) * self.completion_price
```

### Cost Control Strategies

1. Move simple tasks to cheaper models.
2. Cache stable intermediate results.
3. Compress prompts aggressively.
4. Cap retries.

---

## 9. Resource Lifecycle

Manage memory, file handles, and connections across the request lifecycle.

```python
class ResourceManager:
    def __init__(self):
        self._allocations: Set[Any] = set()
    
    def track(self, resource):
        self._allocations.add(resource)
    
    def release_all(self):
        for r in self._allocations:
            r.close()
        self._allocations.clear()
```

---

## 10. Error Handling Fundamentals

Use retries with backoff. Avoid retrying permanent errors.

```python
class RetryPolicy:
    def __init__(self, max_attempts: int = 3, base_delay: float = 0.5):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
    
    async def execute(self, fn, *args, **kwargs):
        last_exception = None
        for attempt in range(self.max_attempts):
            try:
                return await fn(*args, **kwargs)
            except RetryableError as e:
                last_exception = e
                await asyncio.sleep(self.base_delay * (2 ** attempt))
        raise last_exception
```

---

## 11. Observability Fundamentals

Log events with timestamps, latency, and token counts. Emit metrics for latency, errors, and cost.

```python
class Observability:
    def __init__(self):
        self.latency_ms: deque = deque(maxlen=1000)
        self.error_count = 0
        self.request_count = 0
    
    def record_request(self, latency_ms: float, error: bool = False):
        self.latency_ms.append(latency_ms)
        self.request_count += 1
        if error:
            self.error_count += 1
    
    def error_rate(self) -> float:
        return self.error_count / self.request_count if self.request_count else 0.0
```

### Structured Logging Example

```python
class StructuredLogger:
    def log_request(self, request_id: str, prompt_tokens: int, completion_tokens: int, latency_ms: float):
        logger.info("request.completed", extra={
            "request_id": request_id,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "latency_ms": latency_ms,
        })
```

---

## 12. Cost Fundamentals

### Cost Per Request Formula

```
cost = (prompt_tokens / 1000) * prompt_price + (completion_tokens / 1000) * completion_price + retrieval_cost + tool_cost
```

### Daily Budget Tracking

```python
class DailyBudget:
    def __init__(self, limit_usd: float):
        self.limit = limit_usd
        self.spend_usd = 0.0
    
    def add_cost(self, cost_usd: float):
        self.spend_usd += cost_usd
    
    def over_budget(self) -> bool:
        return self.spend_usd >= self.limit
```

---

## 13. Testing Fundamentals

### Unit Testing

```python
import pytest

@pytest.mark.asyncio
async def test_cache_hit():
    cache.set("key", "value")
    assert await cache.get("key") == "value"
```

### Load Testing

```python
import pytest

@pytest.mark.asyncio
async def test_scaling():
    concurrency = 50
    tasks = [process_request(prompt) for _ in range(concurrency)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    failures = [r for r in results if isinstance(r, Exception)]
    assert len(failures) / concurrency < 0.01
```

---

## 14. Infrastructure Fundamentals

### Autoscaling

Scale worker replicas based on queue depth or latency percentiles.

```python
class QueueScalingPolicy:
    def __init__(self, min_replicas: int = 2, max_replicas: int = 20, target_queue: int = 10):
        self.min = min_replicas
        self.max = max_replicas
        self.target = target_queue
    
    def desired_replicas(self, current: int, queue_length: int) -> int:
        desired = int((queue_length / self.target) * current)
        return max(self.min, min(self.max, desired))
```

### Health Checks

```python
class HealthCheck:
    async def check(self):
        try:
            await cache.ping()
            await model.health()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "reason": str(e)}
```

---

## 15. Performance Budgets

Set explicit budgets for latency, cost, and throughput.

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

## 16. Latency Budgets

### Component-Level Budgets

```python
class ComponentLatencyBudget:
    def __init__(self):
        self.budgets = {
            "model_inference": 2.0,
            "tool_execution": 0.5,
            "retrieval": 1.0,
            "context_building": 0.3,
            "serialization": 0.2,
        }
    
    def check(self, component: str, actual_ms: float) -> bool:
        budget_ms = self.budgets.get(component, 1.0) * 1000
        return actual_ms <= budget_ms
```

### Cumulative Latency Tracking

```python
class CumulativeLatencyTracker:
    def __init__(self):
        self.segments: Dict[str, float] = {}
    
    def start(self, segment: str):
        self.segments[segment] = {"start": time.perf_counter()}
    
    def end(self, segment: str):
        if segment in self.segments:
            start = self.segments[segment]["start"]
            self.segments[segment]["duration"] = time.perf_counter() - start
    
    def report(self):
        for segment, data in self.segments.items():
            print(f"{segment}: {data.get('duration', 0) * 1000:.2f}ms")
```

---

## 17. Token Budgets

### Per-Request Allocation

```python
class RequestTokenBudget:
    def __init__(self, max_tokens: int = 12000):
        self.max_tokens = max_tokens
        self.allocations = {
            "system": 0.10,
            "retrieval": 0.25,
            "history": 0.40,
            "response": 0.25,
        }
    
    def allocate(self, component: str) -> int:
        return int(self.max_tokens * self.allocations[component])
    
    def remaining(self, component: str, used: int) -> int:
        allocated = self.allocate(component)
        return max(0, allocated - used)
```

### Per-User Token Limits

```python
class UserTokenLimiter:
    def __init__(self, daily_limit: int = 100000):
        self.daily_limit = daily_limit
        self.usage: Dict[str, int] = defaultdict(int)
    
    def consume(self, user_id: str, tokens: int) -> bool:
        if self.usage[user_id] + tokens <= self.daily_limit:
            self.usage[user_id] += tokens
            return True
        return False
    
    def reset_daily(self):
        self.usage.clear()
```

---

## 18. Resource Management

### Connection Pooling

```python
class ConnectionPool:
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.connections: deque = deque(maxlen=max_size)
    
    async def acquire(self):
        if self.connections:
            return self.connections.popleft()
        return await self.create_connection()
    
    async def release(self, conn):
        if len(self.connections) < self.max_size:
            self.connections.append(conn)
        else:
            await conn.close()
    
    async def create_connection(self):
        # Implementation depends on connection type
        pass
```

### Worker Pool Management

```python
class WorkerPool:
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.workers: List[Worker] = []
        self.task_queue: asyncio.Queue = asyncio.Queue()
    
    async def start(self):
        for i in range(self.num_workers):
            worker = Worker(id=i, queue=self.task_queue)
            self.workers.append(worker)
            asyncio.create_task(worker.run())
    
    async def submit(self, task):
        await self.task_queue.put(task)
    
    async def shutdown(self):
        for worker in self.workers:
            await worker.stop()
        self.workers.clear()
```

### Memory Management

```python
class MemoryManager:
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.allocated = 0
    
    def allocate(self, size: int):
        if self.allocated + size > self.max_memory:
            self.collect_garbage()
            if self.allocated + size > self.max_memory:
                raise MemoryError("Out of memory")
        self.allocated += size
    
    def collect_garbage(self):
        # Force garbage collection
        gc.collect()
        self.allocated = self.get_current_memory_usage()
    
    def get_current_memory_usage(self) -> int:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss
```

---

## 19. Context Management

### Conversation State Management

```python
class ConversationState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turn_count = 0
        self.messages: List[dict] = []
        self.metadata = {}
    
    def add_message(self, role: str, content: str):
        self.turn_count += 1
        self.messages.append({
            "role": role,
            "content": content,
            "turn": self.turn_count,
        })
    
    def get_context(self, max_turns: int = 10) -> List[dict]:
        # Return last N messages plus system prompt
        recent = self.messages[-max_turns:]
        return [{"role": "system", "content": "You are a helpful assistant."}] + recent
    
    def summarize(self) -> str:
        # Create summary of conversation
        return f"Conversation with {self.turn_count} turns"
```

### Session Management

```python
class SessionManager:
    def __init__(self, max_sessions: int = 10000):
        self.sessions: Dict[str, ConversationState] = {}
        self.max_sessions = max_sessions
    
    def get_or_create(self, session_id: str) -> ConversationState:
        if session_id not in self.sessions:
            if len(self.sessions) >= self.max_sessions:
                # Evict oldest session
                oldest = min(self.sessions.items(), key=lambda x: x[1].last_accessed)
                del self.sessions[oldest[0]]
            self.sessions[session_id] = ConversationState(session_id)
        return self.sessions[session_id]
    
    def cleanup_expired(self, ttl_hours: int = 24):
        now = time.time()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session.last_accessed > ttl_hours * 3600
        ]
        for sid in expired:
            del self.sessions[sid]
```

---

## 20. Tool Execution Fundamentals

### Tool Registry

```python
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.timeouts: Dict[str, float] = {}
    
    def register(self, name: str, fn, timeout: float = 30.0):
        self.tools[name] = Tool(name, fn, timeout)
        self.timeouts[name] = timeout
    
    async def execute(self, name: str, args: dict) -> Any:
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        tool = self.tools[name]
        try:
            return await asyncio.wait_for(
                tool.execute(args),
                timeout=self.timeouts[name]
            )
        except asyncio.TimeoutError:
            raise ToolTimeoutError(f"Tool {name} timed out after {self.timeouts[name]}s")
```

### Tool Call Optimization

```python
class ToolOptimizer:
    def __init__(self):
        self.cache = {}
    
    def optimize_calls(self, calls: List[ToolCall]) -> List[ToolCall]:
        # Deduplicate identical calls
        unique_calls = {}
        for call in calls:
            key = self._call_key(call)
            if key not in unique_calls:
                unique_calls[key] = call
        
        # Sort by dependency
        return self._sort_by_dependency(list(unique_calls.values()))
    
    def _call_key(self, call: ToolCall) -> str:
        return f"{call.name}:{json.dumps(call.args, sort_keys=True)}"
    
    def _sort_by_dependency(self, calls: List[ToolCall]) -> List[ToolCall]:
        # Topological sort based on dependencies
        return calls
```

---

## 21. Retry and Backoff

### Exponential Backoff

```python
class ExponentialBackoff:
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0, max_retries: int = 5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
    
    async def execute(self, fn, *args, **kwargs):
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                last_exception = e
                delay = min(self.max_delay, self.base_delay * (2 ** attempt))
                jitter = random.uniform(0, delay * 0.1)
                await asyncio.sleep(delay + jitter)
        raise last_exception
```

### Retry Budgets

```python
class RetryBudget:
    def __init__(self, max_retries: int, budget_window: int = 60):
        self.max_retries = max_retries
        self.budget_window = budget_window
        self.retries: deque = deque()
    
    def allow_retry(self) -> bool:
        now = time.time()
        # Remove old entries
        while self.retries and self.retries[0] < now - self.budget_window:
            self.retries.popleft()
        return len(self.retries) < self.max_retries
    
    def record_retry(self):
        self.retries.append(time.time())
```

---

## 22. Circuit Breakers

### Circuit Breaker States

```python
class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.failure_count = 0
            else:
                raise CircuitOpenError("Circuit is open")
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
```

---

## 23. Bulkhead Pattern

Isolate failures by resource type.

```python
class Bulkhead:
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_count = 0
    
    async def execute(self, coro):
        async with self.semaphore:
            self.active_count += 1
            try:
                return await coro
            finally:
                self.active_count -= 1
    
    def utilization(self) -> float:
        return self.active_count / self.semaphore._value
```

---

## 24. Rate Limiting

### Token Bucket

```python
class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
```

### Sliding Window

```python
class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque = deque()
    
    def allow(self) -> bool:
        now = time.time()
        while self.requests and self.requests[0] < now - self.window_seconds:
            self.requests.popleft()
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
```

---

## 25. Monitoring Fundamentals

### Metrics Collection

```python
class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
    
    def record(self, name: str, value: float):
        self.metrics[name].append(value)
    
    def get_stats(self, name: str) -> Dict[str, float]:
        values = self.metrics.get(name, [])
        if not values:
            return {}
        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "p95": np.percentile(values, 95),
            "p99": np.percentile(values, 99),
        }
```

---

## 26. Logging Fundamentals

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

class StructuredLogger:
    @staticmethod
    def log_request(request_id: str, method: str, path: str, latency_ms: float, status: int):
        logger.info("request.completed",
            request_id=request_id,
            method=method,
            path=path,
            latency_ms=latency_ms,
            status=status,
        )
    
    @staticmethod
    def log_error(request_id: str, error: str, stack_trace: str = None):
        logger.error("request.failed",
            request_id=request_id,
            error=error,
            stack_trace=stack_trace,
        )
```

### Log Levels

- `DEBUG`: Detailed diagnostic information.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: Unexpected behavior but not an error.
- `ERROR`: Serious problem that needs attention.
- `CRITICAL`: System is unusable.

---

## 27. Alerting Fundamentals

### Alert Design Principles

1. Actionable: Every alert should require human action.
2. Relevant: Avoid noisy alerts.
3. Timely: Alerts should fire before users are affected.
4. Complete: Include enough context to diagnose.

### Alert Thresholds

```python
class AlertThresholds:
    def __init__(self):
        self.thresholds = {
            "latency_p95": {"warning": 3000, "critical": 5000},
            "error_rate": {"warning": 0.02, "critical": 0.05},
            "cache_hit_rate": {"warning": 0.6, "critical": 0.4},
        }
    
    def evaluate(self, metric: str, value: float) -> str:
        if metric not in self.thresholds:
            return "unknown"
        thresholds = self.thresholds[metric]
        if value >= thresholds["critical"]:
            return "critical"
        if value >= thresholds["warning"]:
            return "warning"
        return "ok"
```

---

## 28. Dashboards and Visualization

### Key Dashboard Panels

1. **Request Rate**: Requests per second over time.
2. **Error Rate**: Percentage of failed requests.
3. **Latency Heatmap**: p50, p95, p99 latency distribution.
4. **Cache Hit Rate**: Cache performance over time.
5. **Token Usage**: Prompt and completion token trends.
6. **Cost per Request**: Average cost over time.
7. **Model Distribution**: Which models are being used.

### Visualization Best Practices

- Use time-series charts for trends.
- Use histograms for latency distributions.
- Use heatmaps for correlation analysis.
- Use tables for current state.

---

## 29. Cost Management

### Cost Model

```python
class CostModel:
    def __init__(self):
        self.pricing = {
            "gpt-4o": {"prompt": 0.0025, "completion": 0.01},
            "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
            "o3": {"prompt": 0.015, "completion": 0.06},
        }
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        prices = self.pricing.get(model, {"prompt": 0, "completion": 0})
        prompt_cost = (prompt_tokens / 1000) * prices["prompt"]
        completion_cost = (completion_tokens / 1000) * prices["completion"]
        return prompt_cost + completion_cost
    
    def estimate_monthly_cost(self, requests_per_day: int, avg_prompt_tokens: int, avg_completion_tokens: int, model: str) -> float:
        cost_per_request = self.calculate_cost(model, avg_prompt_tokens, avg_completion_tokens)
        return cost_per_request * requests_per_day * 30
```

### Cost Optimization Strategies

1. **Model Routing**: Use cheaper models for simple tasks.
2. **Caching**: Reduce redundant API calls.
3. **Token Optimization**: Minimize prompt and completion tokens.
4. **Batch Processing**: Process multiple requests together.

---

## 30. Provider Economics

### Provider Comparison

| Provider | Model | Input Price (per 1K) | Output Price (per 1K) | Latency | Quality |
|----------|-------|----------------------|-----------------------|---------|---------|
| OpenAI | gpt-4o-mini | $0.00015 | $0.0006 | Fast | Good |
| OpenAI | gpt-4o | $0.0025 | $0.01 | Medium | Excellent |
| OpenAI | o3 | $0.015 | $0.06 | Slow | Best |
| Anthropic | claude-3-haiku | $0.00025 | $0.00125 | Fast | Good |
| Anthropic | claude-3-sonnet | $0.003 | $0.015 | Medium | Excellent |
| Anthropic | claude-3-opus | $0.015 | $0.075 | Slow | Best |

### Provider Selection Criteria

- **Latency**: Fast for interactive experiences.
- **Cost**: Cheaper for high-volume or simple tasks.
- **Quality**: Better for complex reasoning.
- **Availability**: Redundant providers for reliability.

### Multi-Provider Strategy

```python
class ProviderManager:
    def __init__(self):
        self.providers = {
            "fast": OpenAIProvider(model="gpt-4o-mini"),
            "balanced": OpenAIProvider(model="gpt-4o"),
            "powerful": AnthropicProvider(model="claude-3-opus"),
        }
    
    def select_provider(self, task_complexity: float) -> Provider:
        if task_complexity < 0.3:
            return self.providers["fast"]
        if task_complexity < 0.7:
            return self.providers["balanced"]
        return self.providers["powerful"]
```

---

## Related Files

- [Best Practices](./best-practices.md)
- [Advanced](./advanced.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
