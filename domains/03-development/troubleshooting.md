# Development Domain - Troubleshooting

## Overview

This document covers common development issues and solutions for LLM/agentic systems, providing guidance for debugging, performance optimization, and resolving typical problems.

---

## Common Issues and Solutions

### Issue 1: Agent Not Responding

**Symptoms:**
- Long delays in agent responses
- HTTP timeouts
- No error messages

**Solutions:**
- Check model API status and credentials
- Verify network connectivity
- Add explicit timeouts to all external calls
- Implement circuit breaker pattern
- Check rate limiting configuration

### Issue 2: Tool Execution Failures

**Symptoms:**
- Tool calls return errors
- Unexpected tool behavior
- Missing tool results in context

**Solutions:**
- Validate tool arguments before execution
- Check tool connectivity and permissions
- Verify tool is registered correctly
- Implement retry logic with exponential backoff
- Add proper error handling and logging

### Issue 3: Context Overflow

**Symptoms:**
- Model returns truncated responses
- Poor quality responses
- Out of memory errors

**Solutions:**
- Implement context window limits
- Trim old context messages
- Prioritize recent and relevant context
- Use summarization for long context
- Monitor token usage

### Issue 4: Rate Limiting Errors

**Symptoms:**
- HTTP 429 errors
- Requests blocked
- High costs

**Solutions:**
- Implement client-side rate limiting
- Add request queuing
- Use exponential backoff
- Cache responses where appropriate
- Request rate limit increases from provider

### Issue 5: Memory Issues

**Symptoms:**
- Process killed (OOM)
- Slow performance
- High memory usage

**Solutions:**
- Use streaming for large responses
- Implement response caching with TTL
- Monitor memory usage in production
- Profile memory hotspots
- Consider memory-mapped storage for large datasets

---

### Issue 6: Inconsistent Responses

**Symptoms:**
- Different responses to same input
- Random failures
- Non-deterministic behavior

**Solutions:**
- Set temperature to 0 for consistency
- Set seed for reproducibility
- Log all inputs and outputs
- Check for race conditions in async code

### Issue 7: Slow Response Times

**Symptoms:**
- Responses taking longer than expected
- High latency
- Timeout errors

**Solutions:**
- Profile code for bottlenecks
- Check model response times
- Implement parallel processing where safe
- Add response caching
- Optimize context size

### Issue 8: Authentication Problems

**Symptoms:**
- 401/403 errors from APIs
- Invalid token errors
- Permission denied

**Solutions:**
- Check token expiration
- Verify credentials in secret store
- Review IAM permissions
- Implement token refresh logic

---

## Debugging Strategies

### 1. Logging Approach

Add structured logging at key points:
- Prompt construction
- Model calls
- Tool execution
- Response parsing

Example implementation:
```python
import structlog

logger = structlog.get_logger()

def process_prompt(prompt: str) -> str:
    logger.info("processing_prompt", prompt_length=len(prompt))
    try:
        response = model.generate(prompt)
        logger.info("prompt_processed", response_length=len(response))
        return response
    except Exception as e:
        logger.error("prompt_failed", error=str(e))
        raise
```

### 2. REPL Testing

Test components interactively to understand behavior.

```python
# In Python REPL or Jupyter
from src.agent.core import AgentCore
agent = AgentCore(model=FakeModel(), tools=MockRegistry())
result = agent.process("Hello")
print(result)
# Inspect intermediate state
agent._last_prompt
agent._last_context
```

### 3. Mock Testing

Create deterministic tests with mocked external dependencies.

```python
class TestModel:
    def __init__(self, fixed_response="Test response"):
        self.response = fixed_response

    def generate(self, prompt):
        return self.response
```

---

## Performance Optimization

### 1. Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_response(prompt_hash: str) -> Optional[str]:
    return redis_client.get(f"response:{prompt_hash}")
```

### 2. Connection Pooling

```python
import aiohttp

class PooledModelClient:
    def __init__(self):
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=100)
        )
```

### 3. Asynchronous Processing

```python
async def process_batch(prompts: List[str]) -> List[str]:
    tasks = [asyncio.create_task(process_one(p)) for p in prompts]
    return await asyncio.gather(*tasks)
```

---

## Deployment Troubleshooting

### 1. Container Issues

```bash
# Check container logs
docker logs agent-container

# Check resource usage
docker stats agent-container

# Enter container for debugging
docker exec -it agent-container /bin/bash
```

### 2. Network Problems

```bash
# Check connectivity
curl -v https://api.openai.com/v1/models

# Check DNS resolution
nslookup api.openai.com

# Check firewall rules
iptables -L
```

### 3. Secret Loading

```python
def verify_secrets():
    required = ["OPENAI_API_KEY", "DATABASE_URL"]
    missing = [s for s in required if not os.getenv(s)]
    if missing:
        raise RuntimeError(f"Missing secrets: {missing}")
```

---

## Diagnostic Tools

### Tool 1: Memory Profiling

```python
import tracemalloc

tracemalloc.start()
agent.process(large_prompt)
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024} MB, Peak: {peak / 1024 / 1024} MB")
tracemalloc.stop()
```

### Tool 2: Timing Analysis

```python
import time

def timed_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    duration = time.perf_counter() - start
    logger.info(f"{func.__name__} took {duration:.3f}s")
    return result
```

---

## Common Error Messages and Meanings

### Error: "Connection timeout"

Likely causes:
- Network connectivity issues
- API unreachable
- Firewall blocking requests

### Error: "Rate limit exceeded"

Likely causes:
- Too many requests in short time
- Shared API key across multiple instances
- Missing backoff strategy

### Error: "Context length exceeded"

Likely causes:
- Too much history in context
- Large document uploads
- Missing context management

---

## Monitoring Dashboards

### Key Metrics to Display

1. Request rate (requests/minute)
2. Error rate by type
3. Response time percentiles
4. Token usage per model
5. Cache hit ratio
6. Active sessions

Dashboard query examples:
```
rate(agent_requests_total[5m])
histogram_quantile(0.95, rate(agent_response_time_seconds_bucket[5m]))
```

---

## Recovery Procedures

### Procedure 1: Handle Model Outage

1. Switch to fallback model if available
2. Return cached responses where possible
3. Rate limit incoming requests to prevent queue buildup
4. Alert development team

### Procedure 2: Recover from Corrupted State

1. Identify corrupted session
2. Clear session data
3. Restart agent with clean context
4. Log incident for post-mortem

---

## Diagnostic Procedures

### Procedure 1: Investigate Slow Responses

Step by step investigation:

1. **Check recent changes**
   ```bash
   git log --oneline -20
   git diff HEAD~1
   ```

2. **Review recent deployments**
   ```bash
   kubectl get pods -n agent-system
   kubectl logs -n agent-system deployment/agent-api
   ```

3. **Analyze metrics**
   - Response time percentiles
   - Error rates
   - Resource utilization

4. **Reproduce locally**
   ```python
   # Use same input that's slow in production
   result = agent.process("same prompt")
   # Add timing
   start = time.time()
   result = agent.process(prompt)
   print(f"Duration: {time.time() - start}")
   ```

5. **Profile the code**
   ```python
   import cProfile

   cProfile.run('agent.process(large_prompt)')
   ```

### Procedure 2: Debug Tool Execution Issues

Investigation checklist:

- [ ] Verify tool is registered in registry
- [ ] Check tool permissions for user
- [ ] Review tool timeout settings
- [ ] Examine tool logs for errors
- [ ] Validate tool arguments format
- [ ] Check tool external service connectivity

Example debugging session:
```python
# 1. List available tools
print(tool_registry.list_tools())

# 2. Check specific tool
tool = tool_registry.get_tool("file_read")
print(tool.permissions)

# 3. Test tool directly
result = tool.execute(path="/tmp/test.txt")
print(result)

# 4. Check with context
ctx = AuthContext(user_id="test", roles={Role.VIEWER})
print(tool.has_permission(ctx))
```

---

## Common Error Patterns

### Pattern 1: Timeout Cascades

When external services slow down, your agent makes more parallel calls, worsening the problem.

Mitigation:
- Implement circuit breakers
- Use bulkheads to isolate resources
- Add jitter to retries
- Reduce concurrency under load

### Pattern 2: Context Accumulation

Long conversations grow context beyond model limits, causing poor responses.

Mitigation:
- Implement context summarization
- Use sliding window of recent messages
- Clear context on topic change
- Limit total session length

### Pattern 3: Cache Poisoning

Bad responses get cached and served repeatedly.

Mitigation:
- Only cache successful responses
- Add cache invalidation triggers
- Use short TTL for volatile data
- Implement cache health checks

---

## Monitoring Queries

### Query 1: Error Rate Analysis

```
sum(rate(agent_errors_total[5m])) by (error_type)
```

### Query 2: Slowest Endpoints

```
histogram_quantile(0.95, rate(agent_request_duration_seconds_bucket[5m]))
```

### Query 3: Cache Effectiveness

```
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
```

---

## Rollback Procedure

When a deployment causes issues:

1. **Stop the rollout**
   ```bash
   kubectl rollout undo deployment/agent-api
   ```

2. **Verify rollback**
   ```bash
   kubectl rollout status deployment/agent-api
   ```

3. **Test functionality**
   ```bash
   curl https://api.agent.system/health
   ```

4. **Notify stakeholders**
   - Update incident channel
   - Send status update

5. **Document root cause**
   - Update post-mortem
   - Add preventive measures

---

## Performance Tuning Guide

### Tuning 1: Optimize Context Size

```python
def optimize_context(messages: List[dict], max_tokens: int) -> List[dict]:
    # Keep system message
    system = [m for m in messages if m["role"] == "system"]
    # Trim user/assistant messages
    others = [m for m in messages if m["role"] != "system"]
    return system + others[-max_tokens:]
```

### Tuning 2: Connection Pool Sizing

```python
# For N concurrent agents, M concurrent requests each
# Connection pool should be N * M * 1.2 (20% buffer)

class ConnectionPool:
    def __init__(self, min_size: int = 10, max_size: int = 100):
        self.pool = asyncio.Semaphore(max_size)
        self.min_size = min_size
```

---

## Production Checklist

### Daily Checks

- [ ] Check error dashboard for spikes
- [ ] Verify all services healthy
- [ ] Review slow query logs
- [ ] Check disk and memory usage
- [ ] Verify backups ran successfully

### Weekly Checks

- [ ] Review security scans
- [ ] Update dependencies
- [ ] Audit access logs
- [ ] Review performance metrics
- [ ] Test disaster recovery

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)