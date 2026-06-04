# Retry Policy

Use this guide when implementing retry logic for external calls, internal operations, and agentic workflows.

## Retry Philosophy

### When to Retry

Retries are appropriate for transient failures that are likely to succeed on subsequent attempts. Retrying permanent failures wastes time, resources, and can make problems worse.

**Retryable Failures**
- Network timeouts and connection failures
- Rate limiting (429 Too Many Requests)
- Service temporarily unavailable (503 Service Unavailable)
- Gateway timeouts (504 Gateway Timeout)
- Database deadlocks
- Lock contention
- Temporary resource exhaustion
- Load balancer health check failures

**Non-Retryable Failures**
- Authentication failures (401 Unauthorized)
- Authorization failures (403 Forbidden)
- Not found errors (404 Not Found)
- Validation errors (400 Bad Request)
- Malformed request (400 Bad Request)
- Business logic violations
- Invalid input data
- Quota exceeded (not rate limiting)
- Account or subscription issues

### Retry Decision Flowchart

```
Request Failed
    |
    v
Is error transient? --- No ---> Do NOT retry
    |
    Yes
    |
    v
Is operation idempotent? --- No ---> Do NOT retry (or use exactly-once)
    |
    Yes
    |
    v
Have retries been exhausted? --- Yes ---> Do NOT retry
    |
    No
    |
    v
RETRY with appropriate strategy
```

## Retry Strategy Selection

### Strategy Comparison

| Strategy | Use Case | Pros | Cons | Complexity |
|----------|----------|------|------|------------|
| No Retry | Non-retryable errors, idempotency unclear | Simple, predictable | No recovery from transient failures | Low |
| Fixed Delay | Simple retry scenarios | Easy to implement, predictable | Can cause thundering herd | Low |
| Linear Backoff | Gradually increasing load | Better than fixed, simple | Still can herd | Low |
| Exponential Backoff | Rate limiting, API throttling | Reduces load effectively | Longer total retry time | Medium |
| Exponential Backoff with Jitter | Distributed systems | Prevents thundering herd | Requires random number generation | Medium |
| Decorrelated Jitter | High-traffic systems | Optimal distribution | Requires careful tuning | High |
| Fibonacci Backoff | Specialized use cases | Smooth progression | Less common, harder to tune | Medium |

### Strategy Selection Guide

**No Retry**
- Non-idempotent operations
- Non-retryable errors
- When retry makes things worse
- When immediate feedback is required

**Fixed Delay**
- Simple, single-service scenarios
- Known consistent failure patterns
- Internal services with predictable behavior
- Examples: Database deadlocks, temporary locks

**Linear Backoff**
- Gradually escalating failures
- Need to reduce request rate
- Internal services with load issues
- Examples: Rate limiting with linear escalation

**Exponential Backoff**
- External API rate limiting
- Service throttling
- Distributed systems
- Cloud services with backoff recommendations
- Examples: Third-party APIs, microservices

**Exponential Backoff with Jitter**
- High-traffic production systems
- Multiple clients retrying same service
- Preventing synchronized retries
- Examples: Load balancers, distributed caches

**Decorrelated Jitter**
- Very high traffic systems
- Complex distributed architectures
- When optimal retry distribution is critical
- Examples: Large-scale microservices, CDN integrations

## Retry Configuration Parameters

### Essential Parameters

Every retry configuration should define:

**max_retries**
- Maximum number of retry attempts
- Typical values: 3-5
- Considerations:
  - More retries = longer total time
  - More retries = more load on failing service
  - Diminishing returns after 3-5 retries
- Recommendation: Start with 3, increase to 5 for critical operations

**base_delay**
- Initial delay before first retry
- Typical values: 0.5-2 seconds
- Considerations:
  - Too short: immediate retry may fail again
  - Too long: slow recovery
- Recommendation: 1 second for most cases

**max_delay**
- Maximum delay between retries
- Typical values: 30-120 seconds
- Considerations:
  - Prevents extremely long waits
  - Bounds total retry time
- Recommendation: 60 seconds

**backoff_multiplier**
- Factor by which delay increases
- Typical values: 2-3
- Considerations:
  - Higher = faster escalation
  - Lower = gentler escalation
- Recommendation: 2 (doubling)

**jitter**
- Random variation in delay
- Typical values: 0-100% of delay
- Considerations:
  - Reduces synchronization
  - Spreads retry load
- Recommendation: 20-50% of delay

**timeout**
- Timeout for each individual attempt
- Should be less than total operation timeout
- Typically: 5-30 seconds per attempt

**retryable_errors**
- List of error types/codes that trigger retry
- Must be explicitly defined
- Should match actual transient errors
- Should exclude permanent errors

### Example Configurations

**Conservative (Safe)**
```yaml
max_retries: 3
base_delay: 1s
max_delay: 30s
backoff_multiplier: 2
jitter: 0.25
timeout: 10s
retryable_errors:
  - ECONNREFUSED
  - ECONNRESET
  - ETIMEDOUT
  - 503
  - 504
```

**Moderate (Balanced)**
```yaml
max_retries: 4
base_delay: 0.5s
max_delay: 60s
backoff_multiplier: 2
jitter: 0.3
timeout: 15s
retryable_errors:
  - ECONNREFUSED
  - ECONNRESET
  - ETIMEDOUT
  - ENOTFOUND
  - 429
  - 503
  - 504
```

**Aggressive (High Availability)**
```yaml
max_retries: 5
base_delay: 0.1s
max_delay: 120s
backoff_multiplier: 3
jitter: 0.5
timeout: 30s
retryable_errors:
  - ECONNREFUSED
  - ECONNRESET
  - ETIMEDOUT
  - ENOTFOUND
  - 429
  - 503
  - 504
  - EPIPE
```

## Retry Implementation Patterns

### Basic Retry Pattern

**Python**
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1, max_delay=60):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries:
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.3)
            total_delay = delay + jitter
            
            time.sleep(total_delay)
```

**JavaScript**
```javascript
async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000, maxDelay = 60000) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries || !isRetryable(error)) {
        throw error;
      }
      
      const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
      const jitter = Math.random() * delay * 0.3;
      await sleep(delay + jitter);
    }
  }
}
```

**Go**
```go
import (
    "math"
    "math/rand"
    "time"
)

func retryWithBackoff(fn func() error, maxRetries int, baseDelay, maxDelay time.Duration) error {
    var err error
    for attempt := 0; attempt <= maxRetries; attempt++ {
        err = fn()
        if err == nil {
            return nil
        }
        
        if attempt == maxRetries || !isRetryable(err) {
            return err
        }
        
        delay := time.Duration(math.Min(
            float64(baseDelay) * math.Pow(2, float64(attempt)),
            float64(maxDelay),
        ))
        jitter := time.Duration(rand.Float64() * float64(delay) * 0.3)
        
        time.Sleep(delay + jitter)
    }
    return err
}
```

### Advanced Retry Pattern with Circuit Breaker

```python
import time
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic

T = TypeVar('T')

@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_multiplier: float = 2.0
    jitter: float = 0.3
    timeout: float = 10.0
    retryable_exceptions: tuple = (Exception,)

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except self.retryable_exceptions as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

class RetryWithCircuitBreaker(Generic[T]):
    def __init__(self, config: RetryConfig, circuit_breaker: CircuitBreaker):
        self.config = config
        self.circuit_breaker = circuit_breaker
    
    def execute(self, func: Callable[[], T]) -> T:
        for attempt in range(self.config.max_retries + 1):
            try:
                return self.circuit_breaker.call(func)
            except CircuitBreakerOpenError:
                raise
            except self.config.retryable_exceptions as e:
                if attempt == self.config.max_retries:
                    raise
                
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
        
        raise MaxRetriesExceededError()
    
    def _calculate_delay(self, attempt: int) -> float:
        delay = self.config.base_delay * (self.config.backoff_multiplier ** attempt)
        delay = min(delay, self.config.max_delay)
        jitter = delay * self.config.jitter * (2 * random.random() - 1)
        return max(0, delay + jitter)
```

### Exactly-Once Semantics

For non-idempotent operations, use exactly-once semantics:

**Idempotency Keys**
```python
import uuid

class IdempotentOperation:
    def __init__(self, operation_id=None):
        self.operation_id = operation_id or str(uuid.uuid4())
    
    def execute(self, func):
        # Check if operation already completed
        if self.is_completed():
            return self.get_result()
        
        # Execute with idempotency key
        result = func(self.operation_id)
        
        # Record completion
        self.record_completion(result)
        
        return result
```

**Deduplication**
```python
class OperationDeduplicator:
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    def execute(self, operation_id, func):
        # Check if operation already executed
        existing = self.storage.get(operation_id)
        if existing:
            return existing['result']
        
        # Execute operation
        result = func()
        
        # Store result
        self.storage.set(operation_id, {
            'result': result,
            'timestamp': time.time(),
        })
        
        return result
```

## Retry Budget and Throttling

### Retry Budget

Limit the percentage of requests that can retry:

```python
class RetryBudget:
    def __init__(self, budget_percentage=10, window_size=60):
        self.budget_percentage = budget_percentage
        self.window_size = window_size
        self.total_requests = 0
        self.retry_requests = 0
        self.window_start = time.time()
    
    def allow_retry(self):
        self._reset_window_if_needed()
        
        if self.total_requests == 0:
            return True
        
        current_retry_rate = (self.retry_requests / self.total_requests) * 100
        return current_retry_rate < self.budget_percentage
    
    def record_request(self, is_retry=False):
        self._reset_window_if_needed()
        self.total_requests += 1
        if is_retry:
            self.retry_requests += 1
    
    def _reset_window_if_needed(self):
        if time.time() - self.window_start > self.window_size:
            self.total_requests = 0
            self.retry_requests = 0
            self.window_start = time.time()
```

### Retry Throttling

Prevent retry storms:

```python
class RetryThrottler:
    def __init__(self, max_concurrent_retries=10, retry_queue_size=100):
        self.max_concurrent_retries = max_concurrent_retries
        self.retry_queue_size = retry_queue_size
        self.active_retries = 0
        self.retry_queue = []
    
    def request_retry(self, operation):
        if self.active_retries >= self.max_concurrent_retries:
            if len(self.retry_queue) >= self.retry_queue_size:
                return False  # Reject retry
            self.retry_queue.append(operation)
            return True
        
        self.active_retries += 1
        self._execute_retry(operation)
        return True
    
    def _execute_retry(self, operation):
        try:
            operation()
        finally:
            self.active_retries -= 1
            if self.retry_queue:
                next_operation = self.retry_queue.pop(0)
                self._execute_retry(next_operation)
```

## Retry Context and Metadata

### Retry Context Propagation

Propagate retry context through call chains:

```python
@dataclass
class RetryContext:
    operation_id: str
    attempt: int
    max_retries: int
    last_error: Optional[Exception] = None
    retry_history: List[Dict] = field(default_factory=list)
    
    def record_attempt(self, error, delay):
        self.retry_history.append({
            'attempt': self.attempt,
            'error': str(error),
            'error_type': type(error).__name__,
            'delay': delay,
            'timestamp': time.time(),
        })
    
    def to_dict(self):
        return {
            'operation_id': self.operation_id,
            'attempt': self.attempt,
            'max_retries': self.max_retries,
            'retry_history': self.retry_history,
        }
```

### Retry-Aware Logging

Include retry context in logs:

```python
def log_retry_attempt(context: RetryContext):
    logger.warning(
        f"Retry attempt {context.attempt}/{context.max_retries} "
        f"for operation {context.operation_id}",
        extra={
            'operation_id': context.operation_id,
            'attempt': context.attempt,
            'max_retries': context.max_retries,
            'last_error': str(context.last_error),
            'retry_history': context.retry_history,
        }
    )
```

### Retry Metrics

Track retry behavior:

```python
class RetryMetrics:
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    def record_retry_attempt(self, operation, attempt, error_type):
        self.metrics.increment(
            'retry.attempt',
            tags={
                'operation': operation,
                'attempt': attempt,
                'error_type': error_type,
            }
        )
    
    def record_retry_success(self, operation, attempts):
        self.metrics.histogram(
            'retry.success_attempts',
            attempts,
            tags={'operation': operation}
        )
    
    def record_retry_exhausted(self, operation):
        self.metrics.increment(
            'retry.exhausted',
            tags={'operation': operation}
        )
```

## Retry for Specific Scenarios

### HTTP Requests

**Configurable Retry Middleware**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError))
)
def fetch_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
```

**Conditional Retry Based on Status Code**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

def retry_on_status_code(retry_after_header=True):
    def is_retryable(exception):
        if isinstance(exception, requests.HTTPError):
            if exception.response.status_code in [429, 503, 504]:
                if retry_after_header:
                    # Use Retry-After header if present
                    retry_after = exception.response.headers.get('Retry-After')
                    if retry_after:
                        return True
                return True
        return False
    
    return is_retryable

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_on_status_code()
)
def fetch_with_status_retry(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
```

### Database Operations

**Database Retry with Exponential Backoff**
```python
import time
from sqlalchemy.exc import OperationalError, DisconnectionError

def retry_db_operation(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except (OperationalError, DisconnectionError) as e:
            if attempt == max_retries - 1:
                raise
            
            delay = 2 ** attempt + random.uniform(0, 1)
            time.sleep(delay)
            continue
```

**Transaction Retry**
```python
from sqlalchemy.exc import OperationalError

def retry_transaction(session, operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = operation(session)
            session.commit()
            return result
        except OperationalError as e:
            session.rollback()
            if attempt == max_retries - 1:
                raise
            
            delay = 2 ** attempt + random.uniform(0, 1)
            time.sleep(delay)
            continue
```

### Message Queue Operations

**Message Send Retry**
```python
import time

def send_message_with_retry(queue, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            queue.send(message)
            return True
        except QueueFullError:
            if attempt == max_retries - 1:
                raise
            
            delay = 2 ** attempt + random.uniform(0, 1)
            time.sleep(delay)
            continue
```

**Message Processing Retry**
```python
def process_message_with_retry(handler, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            handler(message)
            return True
        except ProcessingError as e:
            if attempt == max_retries - 1:
                # Send to dead letter queue
                send_to_dlq(message, error=e)
                raise
            
            delay = 2 ** attempt + random.uniform(0, 1)
            time.sleep(delay)
            continue
```

### Model Inference

**Model Inference Retry**
```python
def call_model_with_retry(model, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate(prompt)
            validate_response(response)
            return response
        except ModelTimeoutError:
            if attempt == max_retries - 1:
                raise
            
            delay = 2 ** attempt + random.uniform(0, 1)
            time.sleep(delay)
            continue
        except ModelOverloadError:
            if attempt == max_retries - 1:
                # Fallback to alternative model
                return fallback_model.generate(prompt)
            
            delay = 5 * (2 ** attempt) + random.uniform(0, 5)
            time.sleep(delay)
            continue
```

## Retry Testing

### Test Categories

**1. Success Path Testing**
- Verify retry not triggered on success
- Verify metrics recorded correctly
- Verify no unnecessary delays

**2. Retry Trigger Testing**
- Verify retry triggered for retryable errors
- Verify retry not triggered for non-retryable errors
- Verify correct number of retries
- Verify correct error propagation after exhaustion

**3. Backoff Testing**
- Verify delay calculation correct
- Verify jitter applied
- Verify delays increase exponentially
- Verify maximum delay enforced

**4. Circuit Breaker Testing**
- Verify circuit opens after threshold
- Verify circuit closes after recovery
- Verify half-open state works
- Verify metrics recorded

**5. Concurrency Testing**
- Verify thread-safe implementation
- Verify no race conditions
- Verify correct behavior under load
- Verify retry budget enforced

**6. Integration Testing**
- Test with actual failing services
- Test with network failures
- Test with service degradation
- Test recovery scenarios

### Test Implementation

**Python with pytest**
```python
import pytest
from unittest.mock import Mock, patch
import time

def test_retry_succeeds_on_third_attempt():
    mock_func = Mock(side_effect=[TemporaryError(), TemporaryError(), "success"])
    
    result = retry_with_backoff(mock_func, max_retries=3)
    
    assert result == "success"
    assert mock_func.call_count == 3

def test_retry_exhausts_after_max_retries():
    mock_func = Mock(side_effect=PermanentError())
    
    with pytest.raises(PermanentError):
        retry_with_backoff(mock_func, max_retries=3)
    
    assert mock_func.call_count == 4  # Initial + 3 retries

def test_no_retry_for_non_retryable_error():
    mock_func = Mock(side_effect=ValidationError())
    
    with pytest.raises(ValidationError):
        retry_with_backoff(mock_func, max_retries=3)
    
    assert mock_func.call_count == 1  # No retry

def test_exponential_backoff_timing():
    mock_func = Mock(side_effect=[TemporaryError(), TemporaryError(), "success"])
    
    start_time = time.time()
    retry_with_backoff(mock_func, max_retries=2, base_delay=1)
    elapsed = time.time() - start_time
    
    # Should take approximately 1 + 2 = 3 seconds (plus jitter)
    assert 2.5 < elapsed < 4.0
```

**JavaScript with Jest**
```javascript
describe('retryWithBackoff', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });
  
  afterEach(() => {
    jest.useRealTimers();
  });
  
  test('retries on retryable error', async () => {
    const mockFn = jest.fn()
      .mockRejectedValueOnce(new TemporaryError())
      .mockRejectedValueOnce(new TemporaryError())
      .mockResolvedValue('success');
    
    const promise = retryWithBackoff(mockFn, 3);
    
    await jest.advanceTimersByTimeAsync(100);  // First retry delay
    await promise;
    
    expect(mockFn).toHaveBeenCalledTimes(3);
  });
  
  test('does not retry on non-retryable error', async () => {
    const mockFn = jest.fn().mockRejectedValue(new ValidationError());
    
    await expect(retryWithBackoff(mockFn, 3))
      .rejects.toThrow(ValidationError);
    
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
```

### Chaos Testing for Retry

Inject failures to test retry behavior:

```python
class RetryChaosTest:
    def __init__(self, failure_rate=0.3, failure_type='transient'):
        self.failure_rate = failure_rate
        self.failure_type = failure_type
        self.call_count = 0
    
    def unreliable_service(self):
        self.call_count += 1
        if random.random() < self.failure_rate:
            if self.failure_type == 'transient':
                raise TemporaryError()
            else:
                raise PermanentError()
        return "success"
    
    def test_retry_under_chaos(self):
        chaos = RetryChaosTest(failure_rate=0.5)
        
        successes = 0
        failures = 0
        
        for _ in range(100):
            try:
                retry_with_backoff(chaos.unreliable_service, max_retries=3)
                successes += 1
            except Exception:
                failures += 1
        
        print(f"Successes: {successes}, Failures: {failures}")
        print(f"Total calls: {chaos.call_count}")
        print(f"Retry efficiency: {successes/(successes+failures):.2%}")
```

## Retry Monitoring and Alerting

### Key Metrics

**Retry Volume**
- Total retry attempts per operation
- Retry rate by operation
- Retry rate by error type
- Retry rate by time of day

**Retry Success**
- Retry success rate
- Attempts until success distribution
- Retry efficiency (successes / total retries)
- Time to success after retry

**Retry Impact**
- Added latency from retries
- Additional load from retries
- User impact from retry delays
- Resource utilization increase

### Alerting Thresholds

**Warning**
- Retry rate > 5% for 5 minutes
- P95 retry attempts > 2
- Retry success rate < 90%

**Critical**
- Retry rate > 20% for 2 minutes
- Retry success rate < 50%
- Circuit breaker opened
- Retry budget exhausted

## Retry Best Practices

### General Principles

**1. Make Retries Explicit**
- Clearly document retry behavior
- Make retry configuration visible
- Log retry attempts
- Include retry count in error messages

**2. Respect Idempotency**
- Only retry idempotent operations
- Use idempotency keys for non-idempotent operations
- Document idempotency guarantees
- Test idempotency thoroughly

**3. Use Appropriate Delays**
- Start with small delays
- Increase exponentially
- Add jitter to prevent herd behavior
- Cap maximum delay

**4. Set Clear Bounds**
- Maximum retry count
- Maximum total time
- Retry budget
- Circuit breaker threshold

**5. Handle Failures Gracefully**
- Return appropriate errors after exhaustion
- Include retry context in errors
- Log failures for debugging
- Enable fallback after retries exhausted

**6. Monitor Retry Behavior**
- Track retry rates
- Alert on abnormal retry patterns
- Analyze retry effectiveness
- Optimize based on data

**7. Test Retry Logic**
- Unit tests for retry behavior
- Integration tests with failures
- Chaos testing for resilience
- Load testing for retry storms

**8. Document Retry Decisions**
- Why each operation retries
- What errors trigger retry
- Expected retry behavior
- Maximum retry limits

### Common Retry Anti-Patterns

**Anti-Pattern: Retry Without Bounds**
- Problem: Infinite retry loops
- Impact: Resource exhaustion, cascading failures
- Solution: Always set maximum retries and total timeout

**Anti-Pattern: Immediate Retry**
- Problem: Retrying without delay
- Impact: Overwhelms failing service
- Solution: Always use backoff with delays

**Anti-Pattern: Synchronized Retries**
- Problem: All clients retry at same time
- Impact: Thundering herd problem
- Solution: Add jitter to delays

**Anti-Pattern: Retry All Errors**
- Problem: Retrying permanent failures
- Impact: Wastes resources, makes problems worse
- Solution: Classify errors, only retry transient ones

**Anti-Pattern: No Observability**
- Problem: Cannot see retry behavior
- Impact: Cannot diagnose issues
- Solution: Log and metric all retry attempts

**Anti-Pattern: Retry Side Effects**
- Problem: Retrying causes duplicate side effects
- Impact: Data corruption, duplicate notifications
- Solution: Ensure idempotency or use exactly-once semantics

**Anti-Pattern: Ignoring Circuit Breakers**
- Problem: Retrying against failed circuit
- Impact: Wasted retries, delayed recovery
- Solution: Check circuit breaker state before retry

**Anti-Pattern: Retry Without Timeout**
- Problem: Retry loop has no timeout
- Impact: Indefinite waiting
- Solution: Set total operation timeout

## Retry Checklist

### Implementation Checklist

- [ ] Retry strategy is selected for operation type
- [ ] Maximum retries is defined
- [ ] Backoff strategy is implemented
- [ ] Jitter is added to prevent herd behavior
- [ ] Retryable errors are explicitly defined
- [ ] Non-retryable errors are excluded
- [ ] Circuit breaker is integrated
- [ ] Retry budget is configured
- [ ] Timeouts are set for each attempt
- [ ] Total operation timeout is defined
- [ ] Idempotency is ensured
- [ ] Retry context is propagated
- [ ] Retry metrics are collected
- [ ] Retry logs are comprehensive
- [ ] Alerts are configured for retry issues

### Testing Checklist

- [ ] Unit tests cover retry logic
- [ ] Integration tests with failures
- [ ] Chaos tests for resilience
- [ ] Load tests for retry storms
- [ ] Timeout behavior tested
- [ ] Circuit breaker behavior tested
- [ ] Fallback behavior tested
- [ ] Error handling tested
- [ ] Metrics collection tested
- [ ] Documentation is complete

## Appendix: Retry Reference

### Common Retryable Errors

**HTTP Status Codes**
- 408 Request Timeout
- 429 Too Many Requests
- 503 Service Unavailable
- 504 Gateway Timeout

**Network Errors**
- ECONNREFUSED: Connection refused
- ECONNRESET: Connection reset
- ETIMEDOUT: Connection timed out
- ENOTFOUND: Host not found
- EPIPE: Broken pipe
- ECONNABORTED: Connection aborted

**Database Errors**
- Deadlock found
- Lock timeout
- Connection dropped
- Temporary failure

**Message Queue Errors**
- Queue full
- Broker unavailable
- Connection lost

### Common Non-Retryable Errors

**HTTP Status Codes**
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 Method Not Allowed
- 409 Conflict
- 410 Gone
- 422 Unprocessable Entity
- 429 (with Retry-After in past)
- 500 Internal Server Error (if persistent)
- 501 Not Implemented

**Application Errors**
- Validation errors
- Authentication errors
- Authorization errors
- Business rule violations
- Data integrity errors
- Malformed data

### Retry by Service Type

| Service | Retry Strategy | Max Retries | Base Delay | Max Delay | Notes |
|---------|---------------|-------------|------------|-----------|-------|
| REST API | Exp. Backoff + Jitter | 3-5 | 1s | 60s | Respect Retry-After |
| Database | Linear | 3 | 0.5s | 10s | Handle deadlocks |
| Message Queue | Exp. Backoff | 3-5 | 1s | 30s | Check DLQ |
| Model Inference | Exp. Backoff | 2-3 | 2s | 30s | Have fallback model |
| File Storage | Linear | 3 | 1s | 10s | Check file locks |
| Cache | Exp. Backoff | 2-3 | 0.5s | 10s | Cache miss is OK |
| DNS | Linear | 3 | 1s | 10s | Cache results |
