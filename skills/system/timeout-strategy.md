# Timeout Strategy

Use this guide when configuring timeouts for external calls, internal operations, and agentic workflows.

## Timeout Principles

### Why Timeouts Matter

Timeouts prevent cascading failures, resource exhaustion, and poor user experience. Without proper timeout configuration:

- A single slow dependency can exhaust connection pools
- Users wait indefinitely for responses
- Resources remain tied up waiting for slow operations
- Circuit breakers cannot detect failures
- System recovery is delayed

### Timeout Philosophy

**Fail Fast Principle**
- Detect failures quickly
- Free resources immediately
- Allow retry or fallback
- Maintain system responsiveness

**Timeout Hierarchy**
Every operation should have multiple timeout layers:

1. **Connection Timeout**: Time to establish TCP connection
   - Typical: 1-5 seconds
   - Purpose: Detect network issues quickly

2. **Request Timeout**: Time to send complete request
   - Typical: 5-30 seconds
   - Purpose: Detect slow or unresponsive servers

3. **Response Timeout**: Time to receive complete response
   - Typical: 5-60 seconds
   - Purpose: Detect slow processing or large responses

4. **Total Operation Timeout**: Maximum time for complete operation
   - Typical: 10-120 seconds
   - Purpose: Bound total operation including retries

### Timeout vs. Retry

Timeouts and retries work together:

- **Timeout** defines how long to wait for a single attempt
- **Retry** defines what to do when timeout occurs
- Combined, they bound total operation time

**Formula:**
```
Total Time = (Timeout × Retry Count) + (Backoff Delays)
```

**Example:**
- Timeout: 10 seconds
- Retries: 3
- Backoff: 1s, 2s, 4s
- Total Time: (10 × 3) + (1 + 2 + 4) = 37 seconds

## Timeout Configuration by Service Type

### HTTP/REST APIs

**Connection Timeout**
- Default: 5 seconds
- Fast services: 1-2 seconds
- Slow services: 10 seconds
- Internal services: 2 seconds
- External services: 5-10 seconds

**Request Timeout**
- Simple queries: 5-10 seconds
- Complex queries: 30-60 seconds
- File uploads: 60-300 seconds
- File downloads: 60-600 seconds
- Streaming: No timeout or very long timeout

**Response Timeout**
- JSON responses: 5-30 seconds
- Large responses: 30-120 seconds
- Batch operations: 60-600 seconds
- Report generation: 120-3600 seconds

**Total Operation Timeout**
- Critical user operations: 10-30 seconds
- Background operations: 60-3600 seconds
- Batch operations: 300-7200 seconds

### Database Operations

**Connection Timeout**
- Default: 5 seconds
- Connection pool acquisition: 10-30 seconds
- Local database: 1-2 seconds
- Remote database: 5-10 seconds

**Query Timeout**
- Simple queries: 1-5 seconds
- Complex queries: 10-60 seconds
- Report queries: 60-300 seconds
- Batch operations: 300-3600 seconds

**Transaction Timeout**
- Short transactions: 5-30 seconds
- Long transactions: 60-600 seconds
- Batch transactions: 600-7200 seconds

**Connection Pool Timeout**
- Wait for connection: 10-30 seconds
- Connection validation: 1-5 seconds
- Idle connection timeout: 600-3600 seconds

### Message Queues

**Connection Timeout**
- Default: 5 seconds
- Broker connection: 5-10 seconds

**Operation Timeout**
- Send message: 5-30 seconds
- Receive message: 1-60 seconds
- Acknowledge message: 1-10 seconds
- Batch operations: 30-300 seconds

**Consumer Timeout**
- Message processing: 5-120 seconds
- Batch processing: 60-600 seconds
- Long-running jobs: 600-3600 seconds

**Visibility Timeout**
- Short processing: 30-300 seconds
- Long processing: 300-3600 seconds
- Very long processing: 3600-86400 seconds

### External Tools and Services

**CLI Tool Execution**
- Fast commands: 5-30 seconds
- Medium commands: 30-300 seconds
- Long commands: 300-3600 seconds
- Build commands: 600-7200 seconds
- Test suites: 600-7200 seconds

**Model Inference**
- Small models: 1-10 seconds
- Medium models: 10-60 seconds
- Large models: 60-300 seconds
- Batch inference: 300-3600 seconds

**File Operations**
- Small files: 1-10 seconds
- Large files: 10-300 seconds
- Directory operations: 5-60 seconds
- Compression/decompression: 10-600 seconds
- Network file operations: 30-600 seconds

**Search Operations**
- Simple search: 1-10 seconds
- Complex search: 10-60 seconds
- Full-text search: 5-30 seconds
- Vector search: 1-30 seconds
- Aggregation queries: 30-300 seconds

## Timeout Implementation Patterns

### Python

**requests Library**
```python
import requests
from requests.exceptions import Timeout

try:
    response = requests.get(
        'https://api.example.com/data',
        timeout=(5, 30)  # (connect, read)
    )
except Timeout:
    # Handle timeout
    pass
```

**aiohttp Library**
```python
import aiohttp
import asyncio

async def fetch_data():
    timeout = aiohttp.ClientTimeout(
        total=30,
        connect=5,
        sock_read=10,
        sock_connect=5
    )
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get('https://api.example.com/data') as response:
            return await response.json()
```

**SQLAlchemy**
```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@host/db',
    connect_args={'connect_timeout': 10},
    execution_options={
        'stream_results': True,
    }
)

# Query timeout
from sqlalchemy.sql.expression import text

query = text('SELECT * FROM large_table').execution_options(
    timeout=30
)
```

### JavaScript/TypeScript

**axios**
```typescript
import axios, { AxiosError } from 'axios';

const client = axios.create({
  timeout: 10000,  // 10 seconds
  timeoutErrorMessage: 'Request timeout',
});

// Per-request timeout
try {
  const response = await client.get('/api/data', {
    timeout: 5000,  // 5 seconds for this request
  });
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNABORTED') {
      // Handle timeout
    }
  }
}
```

**fetch with AbortController**
```typescript
async function fetchWithTimeout(
  url: string,
  timeout: number
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      signal: controller.signal,
    });
    return response;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request timeout');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

**Node.js HTTP**
```typescript
import http from 'http';

const options = {
  hostname: 'api.example.com',
  port: 80,
  path: '/data',
  method: 'GET',
  timeout: 5000,  // 5 seconds
};

const request = http.request(options, (response) => {
  // Handle response
});

request.on('timeout', () => {
  console.error('Request timeout');
  request.destroy();
});

request.on('error', (error) => {
  console.error('Request error:', error);
});

request.end();
```

### Go

**HTTP Client**
```go
import (
    "context"
    "net/http"
    "time"
)

func createHTTPClient() *http.Client {
    return &http.Client{
        Timeout: 30 * time.Second,
        Transport: &http.Transport{
            DialContext: (&net.Dialer{
                Timeout:   5 * time.Second,
                KeepAlive: 30 * time.Second,
            }).DialContext,
            TLSHandshakeTimeout: 5 * time.Second,
            ResponseHeaderTimeout: 10 * time.Second,
        },
    }
}

func fetchWithContext(ctx context.Context, url string) (*http.Response, error) {
    client := createHTTPClient()
    
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    
    return client.Do(req)
}
```

**Database**
```go
import (
    "context"
    "database/sql"
    "time"
)

func queryWithTimeout(ctx context.Context, db *sql.DB, query string) (*sql.Rows, error) {
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel()
    
    return db.QueryContext(ctx, query)
}
```

### Java

**Spring WebClient**
```java
import reactor.netty.http.client.HttpClient;
import reactor.netty.tcp.TcpClient;
import java.time.Duration;

HttpClient httpClient = HttpClient.create()
    .responseTimeout(Duration.ofSeconds(30))
    .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
    .doOnConnected(conn -> 
        conn.addHandlerLast(new ReadTimeoutHandler(10))
            .addHandlerLast(new WriteTimeoutHandler(10))
    );

WebClient webClient = WebClient.builder()
    .clientConnector(new ReactorClientHttpConnector(httpClient))
    .build();
```

**JDBC**
```java
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;

try (Connection conn = dataSource.getConnection()) {
    conn.setNetworkTimeout(executor, 10000);  // 10 seconds
    
    try (Statement stmt = conn.createStatement()) {
        stmt.setQueryTimeout(30);  // 30 seconds
        
        try (ResultSet rs = stmt.executeQuery("SELECT * FROM table")) {
            while (rs.next()) {
                // Process results
            }
        }
    }
}
```

## Timeout Testing

### Testing Strategies

**Unit Testing**
- Mock slow responses
- Test timeout handling
- Verify retry behavior
- Check error messages

**Integration Testing**
- Test with actual slow services
- Simulate network delays
- Test timeout at various loads
- Verify system behavior under timeout

**Chaos Testing**
- Inject artificial delays
- Test timeout under load
- Verify recovery from timeouts
- Test cascading timeout effects

### Test Scenarios

**Scenario 1: Normal Operation**
- Service responds within timeout
- Verify successful completion
- Check no unnecessary delays

**Scenario 2: Slow Response**
- Service responds just before timeout
- Verify success or appropriate failure
- Check timeout margin

**Scenario 3: Timeout Occurrence**
- Service does not respond
- Verify timeout triggers correctly
- Check error handling
- Verify resource cleanup

**Scenario 4: Partial Response**
- Service sends partial response
- Verify timeout handles correctly
- Check for data corruption
- Verify retry behavior

**Scenario 5: Cascading Timeouts**
- Multiple services timeout
- Verify circuit breakers activate
- Check fallback behavior
- Verify system stability

## Timeout Monitoring

### Metrics to Collect

**Timeout Occurrences**
- Count of timeout errors by service
- Timeout rate by endpoint
- Timeout trends over time
- Timeout distribution (actual vs. configured)

**Timeout Impact**
- User impact from timeouts
- Retry rate after timeout
- Fallback activation rate
- User abandonment rate

**Timeout Configuration**
- Current timeout values
- Timeout change history
- Timeout vs. actual response times
- Optimal timeout recommendations

### Alerting Thresholds

**Warning Thresholds**
- Timeout rate > 1% for 5 minutes
- P95 response time > 80% of timeout
- Increasing timeout trend

**Critical Thresholds**
- Timeout rate > 5% for 5 minutes
- P99 response time > timeout
- Multiple services timing out simultaneously
- Timeout rate > 20% for 2 minutes

## Timeout Best Practices

### General Principles

**1. Set Timeouts Everywhere**
- Every external call needs a timeout
- Every internal call with external dependency needs timeout
- Every user-facing operation needs timeout
- No operation should wait indefinitely

**2. Set Appropriate Values**
- Base on actual service performance
- Consider user experience requirements
- Account for network variability
- Leave margin for processing time

**3. Use Hierarchical Timeouts**
- Connection timeout < Request timeout < Total timeout
- Each layer serves different purpose
- Tune each layer independently

**4. Make Timeouts Configurable**
- Different environments may need different timeouts
- Timeouts may need adjustment over time
- Allow override for special cases
- Document default values and rationale

**5. Test Timeout Behavior**
- Test normal operation
- Test timeout scenarios
- Test retry behavior
- Test fallback activation

**6. Monitor Timeout Effectiveness**
- Track timeout occurrences
- Analyze timeout patterns
- Adjust timeouts based on data
- Alert on abnormal timeout rates

**7. Handle Timeouts Gracefully**
- Return appropriate error messages
- Log timeout context
- Clean up resources
- Enable retry or fallback

**8. Document Timeout Decisions**
- Record why each timeout value was chosen
- Document expected behavior
- Note any special considerations
- Update documentation when timeouts change

### Common Mistakes

**Mistake 1: No Timeouts**
- Impact: System hangs indefinitely
- Solution: Always set timeouts

**Mistake 2: Timeouts Too Short**
- Impact: False failures, poor user experience
- Solution: Base on actual performance data

**Mistake 3: Timeouts Too Long**
- Impact: Slow failure detection, resource exhaustion
- Solution: Set based on SLA requirements

**Mistake 4: Single Timeout Value**
- Impact: Cannot distinguish failure types
- Solution: Use hierarchical timeouts

**Mistake 5: Hardcoded Timeouts**
- Impact: Cannot adapt to changing conditions
- Solution: Make timeouts configurable

**Mistake 6: Ignoring Timeout Errors**
- Impact: Failures go undetected
- Solution: Always handle timeout errors

**Mistake 7: Retrying Without Bounds**
- Impact: Amplifies failures
- Solution: Combine timeouts with retry limits

## Timeout Configuration by Environment

### Development Environment
- Longer timeouts for debugging
- Detailed timeout logging
- Mock services with controllable delays
- No production impact from timeouts

### Staging Environment
- Production-like timeout values
- Load testing with timeouts
- Monitoring timeout behavior
- Validate timeout handling

### Production Environment
- Optimized timeout values
- Comprehensive monitoring
- Alerting on timeout issues
- Continuous optimization based on data

## Timeout and Circuit Breaker Integration

### Circuit Breaker with Timeout

Circuit breakers and timeouts work together:

**Timeout detects slow failures**
- Circuit breaker counts timeout failures
- Timeouts help circuit breaker open

**Circuit breaker prevents timeout storms**
- After threshold failures, circuit opens
- No more timeouts during open state
- System recovers without timeout pressure

**Integration Pattern**
```python
class TimeoutCircuitBreaker:
    def __init__(self, timeout, failure_threshold, recovery_timeout):
        self.timeout = timeout
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func_with_timeout(func, self.timeout, *args, **kwargs)
            self.on_success()
            return result
        except TimeoutError:
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
```

## Advanced Timeout Patterns

### Adaptive Timeouts

Adjust timeouts based on observed performance:

**Dynamic Timeout Calculation**
```python
class AdaptiveTimeout:
    def __init__(self, initial_timeout, min_timeout, max_timeout):
        self.current_timeout = initial_timeout
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self.response_times = []
        self.window_size = 100
    
    def record_response_time(self, response_time):
        self.response_times.append(response_time)
        if len(self.response_times) > self.window_size:
            self.response_times.pop(0)
        
        # Adjust timeout based on percentiles
        if len(self.response_times) >= 10:
            p95 = percentile(self.response_times, 95)
            self.current_timeout = min(max(p95 * 2, self.min_timeout), self.max_timeout)
    
    def get_timeout(self):
        return self.current_timeout
```

### Distributed Timeouts

Coordinate timeouts in distributed systems:

**Deadline Propagation**
- Set absolute deadline at entry point
- Propagate deadline through service calls
- Each service checks remaining time
- Fail fast when deadline approached

**Implementation**
```python
from datetime import datetime, timedelta

class Deadline:
    def __init__(self, timeout_seconds):
        self.deadline = datetime.now() + timedelta(seconds=timeout_seconds)
    
    def remaining(self):
        return (self.deadline - datetime.now()).total_seconds()
    
    def is_expired(self):
        return datetime.now() >= self.deadline

# Usage
deadline = Deadline(30)  # 30 second deadline

def call_service_a():
    if deadline.is_expired():
        raise DeadlineExceededError()
    # Call service A
    # Pass deadline to service B

def call_service_b():
    if deadline.is_expired():
        raise DeadlineExceededError()
    remaining = deadline.remaining()
    # Use remaining time for timeout
    # Call service B
```

### Timeout Budget

Allocate total time budget across operations:

**Budget Allocation**
```python
class TimeoutBudget:
    def __init__(self, total_budget_ms):
        self.total_budget = total_budget_ms
        self.remaining = total_budget_ms
    
    def allocate(self, operation_name, timeout_ms):
        if self.remaining < timeout_ms:
            raise InsufficientBudgetError(
                f"Cannot allocate {timeout_ms}ms to {operation_name}. "
                f"Only {self.remaining}ms remaining."
            )
        self.remaining -= timeout_ms
    
    def remaining_budget(self):
        return self.remaining
```

## Timeout Debugging

### Debug Information

When timeouts occur, collect:

**Request Information**
- Request URL and parameters
- Request headers
- Request body (sanitized)
- Request timestamp

**Timeout Configuration**
- Configured timeout value
- Timeout type (connection, request, total)
- Retry configuration
- Circuit breaker state

**Response Information**
- Response headers (if any)
- Partial response body (if any)
- Response status code (if any)
- Response timestamp

**System Information**
- Network latency
- System load
- Resource utilization
- Recent system events

### Debug Logging

Enable debug logging for timeout analysis:

```python
import logging

logger = logging.getLogger(__name__)

def call_with_debug_timeout(url, timeout):
    logger.debug(f"Calling {url} with timeout {timeout}s")
    start_time = time.time()
    
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start_time
        logger.debug(f"Request to {url} completed in {elapsed:.2f}s")
        return response
    except Timeout:
        elapsed = time.time() - start_time
        logger.warning(
            f"Timeout calling {url} after {elapsed:.2f}s "
            f"(configured: {timeout}s)"
        )
        raise
```

## Timeout Tuning Process

### Data Collection Phase

1. **Baseline Measurement**
   - Measure current response times
   - Identify slow operations
   - Document timeout failures
   - Collect performance metrics

2. **Analysis**
   - Analyze response time distribution
   - Identify outliers
   - Determine appropriate percentiles
   - Assess user impact

3. **Proposal**
   - Propose new timeout values
   - Justify based on data
   - Consider user experience
   - Plan implementation

### Implementation Phase

4. **Configuration**
   - Update timeout configuration
   - Deploy to staging
   - Test timeout behavior
   - Verify no regressions

5. **Monitoring**
   - Deploy to production
   - Monitor timeout metrics
   - Track success/failure rates
   - Collect feedback

6. **Iteration**
   - Adjust based on data
   - Optimize timeouts
   - Document final values
   - Share learnings

### Optimization Targets

**P50 Response Time**: Timeout = 3-5× P50
**P95 Response Time**: Timeout = 2-3× P95
**P99 Response Time**: Timeout = 1.5-2× P99
**User Experience**: Timeout < 10 seconds for interactive operations

## Timeout Checklist

### Implementation Checklist

- [ ] All external calls have timeouts configured
- [ ] Timeout values are appropriate for operation type
- [ ] Hierarchical timeouts are implemented
- [ ] Timeout errors are handled appropriately
- [ ] Timeout configuration is centralized
- [ ] Timeouts are configurable per environment
- [ ] Timeouts are tested under various conditions
- [ ] Timeout metrics are collected
- [ ] Alerts are configured for timeout issues
- [ ] Timeout values are documented

### Review Checklist

- [ ] Timeout values match SLA requirements
- [ ] Timeouts are not too aggressive
- [ ] Timeouts are not too lenient
- [ ] Retry configuration works with timeouts
- [ ] Circuit breakers work with timeouts
- [ ] Fallback behavior is tested
- [ ] User experience is acceptable
- [ ] System stability is maintained
- [ ] Resource utilization is optimal
- [ ] Documentation is complete

## Appendix: Timeout Reference Values

### Quick Reference

| Operation Type | Connection Timeout | Request Timeout | Total Timeout |
|----------------|-------------------|-----------------|---------------|
| REST API (simple) | 5s | 10s | 30s |
| REST API (complex) | 5s | 30s | 60s |
| Database query | 5s | 10s | 30s |
| Database transaction | 10s | 60s | 120s |
| Message queue | 5s | 10s | 30s |
| Model inference | N/A | 30s | 120s |
| File upload | 10s | 60s | 300s |
| File download | 10s | 120s | 600s |
| CLI command | N/A | 30s | 300s |
| Search query | 5s | 10s | 30s |

### Environment-Specific

| Environment | Timeout Multiplier | Rationale |
|-------------|-------------------|-----------|
| Development | 3-5× | Slower hardware, debugging overhead |
| Staging | 1.5-2× | Shared resources, test data |
| Production | 1× | Optimized for performance |
| Disaster Recovery | 2-3× | Reduced capacity, network latency |

## Appendix: Timeout Troubleshooting

### Common Timeout Issues

**Issue: Too Many Timeouts**
- Causes: Service degradation, network issues, timeout values too low
- Diagnosis: Check service metrics, network metrics, timeout configuration
- Solution: Adjust timeouts, fix underlying issues, add capacity

**Issue: Timeouts Happening at Exact Timeout Value**
- Causes: Timeout too low, service at capacity
- Diagnosis: Analyze response time distribution
- Solution: Increase timeout, optimize service

**Issue: Intermittent Timeouts**
- Causes: Network instability, service load spikes
- Diagnosis: Correlate timeouts with metrics
- Solution: Add retry with backoff, improve stability

**Issue: Cascading Timeouts**
- Causes: Multiple dependent services timing out
- Diagnosis: Trace timeout propagation
- Solution: Implement circuit breakers, add timeouts at all layers

**Issue: Timeout Not Working**
- Causes: Incorrect implementation, library bug, misconfiguration
- Diagnosis: Review implementation, test with controlled delays
- Solution: Fix implementation, update library, correct configuration
