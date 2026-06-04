---
name: system
description: Apply system-level hardening, reliability, and error-handling checks for LLM, agentic, adapter, CLI, IDE, plugin, validation, and release workflows. Use when work involves failure modes, retries, timeouts, rollback, observability, safe writes, install safety, or production readiness.
---

# System Reliability Hardening

Use this skill when a change can fail at runtime, during install, during validation, or during agentic execution.

## Operating Model

System reliability hardening follows a structured approach that ensures production-ready systems with minimal failure impact. This skill provides the framework for evaluating, designing, and implementing resilient systems across LLM, agentic, adapter, CLI, IDE, plugin, validation, and release workflows.

## Workflow

1. Identify the user-facing or operator-facing failure modes.
2. Classify each failure as blocking, recoverable, degraded, or informational.
3. Check timeout, retry, cancellation, and fallback behavior.
4. Check that partial writes, partial installs, and partial state transitions are recoverable.
5. Confirm errors are observable through logs, summaries, reports, or release evidence.
6. Require rollback or disablement steps for production-impacting changes.

## Failure Mode Analysis

### Identifying Failure Modes

Every system has multiple layers where failures can occur. For LLM and agentic systems, common failure points include:

**API and Network Failures**
- Timeout errors when external services are slow or unresponsive
- Rate limiting errors when exceeding API quotas
- Authentication failures due to expired or invalid credentials
- Network connectivity issues between components
- DNS resolution failures for external dependencies

**Data and State Failures**
- Invalid or malformed input data that cannot be parsed
- Database connection pool exhaustion under high load
- Transaction failures that leave partial state
- File system permission errors during writes or reads
- Memory pressure causing garbage collection pauses or OOM errors

**Agentic Execution Failures**
- Tool invocation failures when external tools are unavailable
- Prompt parsing errors that cause malformed requests
- Context window overflow in long-running conversations
- Tool output format violations that break parsing
- Agent state corruption during multi-step workflows

**Deployment and Install Failures**
- Dependency conflicts during package installation
- File system permission errors during deployment
- Configuration validation failures at startup
- Migration failures that leave databases in inconsistent states
- Service startup failures after configuration changes

### Failure Classification Taxonomy

**Blocking Failures (P0)**
- System cannot operate safely or correctly
- Data loss or corruption is possible
- Security vulnerabilities are introduced
- Service is completely unavailable
- Examples: database migration failure, authentication system failure, configuration file corruption

**Recoverable Failures (P1)**
- System can continue with reduced functionality
- Automatic recovery mechanisms exist
- User experience is degraded but functional
- Examples: external API timeout with retry, cache miss, secondary service failure

**Degraded Performance Failures (P2)**
- System operates but with reduced performance
- Some features may be slower or less responsive
- Workarounds may be available to users
- Examples: database connection pool nearing capacity, high memory usage, slow query performance

**Informational Failures (P3)**
- Failures that don't affect system operation
- Useful for monitoring and debugging
- Can be addressed in future iterations
- Examples: non-critical telemetry failures, optional feature toggles that don't work

## Timeout Configuration

### Timeout Principles

Every external interaction must have a defined timeout. Timeouts prevent indefinite blocking and ensure system responsiveness.

**Timeout Hierarchy**
- Request timeout: Maximum time to wait for a complete response
- Connection timeout: Maximum time to establish a connection
- Read timeout: Maximum time to wait for data after connection
- Total operation timeout: Maximum time for complete operation including retries

**Recommended Timeout Values**

Based on service type and criticality:

```
Critical Path (User-facing operations):
- API requests: 5-10 seconds
- Database queries: 1-5 seconds
- External tool calls: 10-30 seconds
- File operations: 5-30 seconds

Background Operations:
- Batch processing: 5-60 minutes
- Model inference: 30-300 seconds
- Report generation: 60-600 seconds
- Data synchronization: 60-3600 seconds
```

### Timeout Implementation Patterns

**Exponential Backoff with Timeout**
```python
class TimeoutConfig:
    def __init__(self, base_timeout, max_timeout, backoff_factor):
        self.base_timeout = base_timeout
        self.max_timeout = max_timeout
        self.backoff_factor = backoff_factor
    
    def get_timeout(self, attempt):
        timeout = self.base_timeout * (self.backoff_factor ** attempt)
        return min(timeout, self.max_timeout)
```

**Circuit Breaker with Timeout**
- Track consecutive failures
- Open circuit after threshold failures
- Wait for recovery period before attempting reset
- Half-open state to test recovery

**Deadline Propagation**
- Set absolute deadlines for multi-step operations
- Propagate deadlines through call chains
- Fail fast when deadline is exceeded
- Clean up resources on deadline breach

## Retry Strategies

### Retry Decision Framework

Not all failures should be retried. The decision to retry depends on:

**Retryable Failures**
- Network timeouts and transient errors
- Rate limiting (with backoff)
- Temporary service unavailability
- Lock contention in databases
- Rate limit exceeded (with appropriate delay)

**Non-Retryable Failures**
- Authentication failures (invalid credentials)
- Authorization failures (insufficient permissions)
- Validation errors (malformed input)
- Not found errors (resource doesn't exist)
- Business logic violations

### Retry Pattern Selection

**Linear Retry**
- Use for: Idempotent operations with consistent failure rates
- Pattern: Fixed delay between retries
- Example: Database deadlocks, temporary locks
- Pros: Simple, predictable
- Cons: May not adapt to changing conditions

**Exponential Backoff**
- Use for: Rate limiting, API throttling, resource exhaustion
- Pattern: Delay increases exponentially with each retry
- Example: External API calls with rate limits
- Pros: Reduces load on failing service
- Cons: Longer total retry time

**Exponential Backoff with Jitter**
- Use for: Distributed systems, preventing thundering herd
- Pattern: Exponential backoff plus random jitter
- Example: Microservice retries, distributed locks
- Pros: Prevents synchronized retries
- Cons: Slightly more complex implementation

**Decorrelated Jitter**
- Use for: High-traffic systems, load balancers
- Pattern: Random delay based on previous delay
- Example: Cloud service integrations
- Pros: Optimal distribution of retry attempts
- Cons: Requires careful tuning

### Retry Bounds and Safety

**Mandatory Retry Bounds**
- Maximum retry count: 3-5 attempts typical
- Maximum total time: Define absolute deadline
- Retry budget: Limit percentage of requests that can retry
- Circuit breaker: Stop retries when failure rate exceeds threshold

**Side Effect Prevention**
- Idempotency: Ensure operations can be safely repeated
- Exactly-once semantics: Use unique request IDs
- Deduplication: Track completed operations
- Compensation: Undo partial work on failure

## Cancellation and Flow Control

### Cancellation Patterns

**Cooperative Cancellation**
- Check cancellation tokens at safe points
- Propagate cancellation through call chains
- Clean up resources on cancellation
- Return partial results when appropriate

**Cancellation Token Implementation**
```python
class CancellationToken:
    def __init__(self):
        self.cancelled = False
        self.callbacks = []
    
    def cancel(self):
        self.cancelled = True
        for callback in self.callbacks:
            callback()
    
    def register(self, callback):
        self.callbacks.append(callback)
    
    def is_cancelled(self):
        return self.cancelled
```

**Timeout-Based Cancellation**
- Combine timeout with cancellation token
- Cancel operation when timeout expires
- Ensure cleanup happens in finally blocks
- Propagate timeout exceptions appropriately

### Flow Control Mechanisms

**Backpressure**
- Limit concurrent operations
- Queue overflow handling
- Drop or reject excess requests
- Signal senders to slow down

**Bulkhead Pattern**
- Isolate critical resources
- Separate thread pools for different operation types
- Prevent cascading failures
- Resource allocation per service

**Rate Limiting**
- Token bucket algorithm for smooth rate limiting
- Sliding window for burst control
- Distributed rate limiting for multi-instance deployments
- Graceful degradation when limits are exceeded

## Fallback Behavior

### Fallback Strategy Design

**Primary and Secondary Services**
- Define primary service as default
- Identify secondary fallback services
- Define trigger conditions for fallback activation
- Test fallback paths regularly

**Fallback Types**

**Cached Fallback**
- Return cached data when primary is unavailable
- Mark cache entries with freshness timestamps
- Background refresh of cache when primary recovers
- Appropriate for: Read-heavy operations, tolerance for stale data

**Default Value Fallback**
- Return sensible defaults when data unavailable
- Document expected behavior with defaults
- Appropriate for: Optional features, non-critical data

**Degraded Mode Fallback**
- Reduce functionality but maintain core operation
- Disable non-essential features
- Simplify complex operations
- Appropriate for: High-availability systems, critical services

**Queue-and-Retry Fallback**
- Queue failed operations for later processing
- Process queue when system recovers
- Prioritize queued operations
- Appropriate for: Write operations, asynchronous tasks

### Fallback Implementation

**Circuit Breaker with Fallback**
- Monitor failure rates
- Open circuit when threshold exceeded
- Return fallback response immediately
- Periodically test for recovery
- Close circuit when service recovers

**Graceful Degradation Hierarchy**
1. Full functionality (primary service)
2. Reduced functionality (secondary service)
3. Minimal functionality (cached/default data)
4. Complete failure (error message with guidance)

## Partial Work Recovery

### Partial Write Recovery

**Atomic Write Strategies**
- Write to temporary file first
- Rename file atomically after validation
- Use file system transactions where available
- Clean up temporary files on failure

**Write Validation**
- Validate writes before committing
- Verify file integrity after write
- Check file permissions after creation
- Confirm file exists and is readable

**Partial State Recovery**
- Transaction rollback for database operations
- Compensating transactions for distributed systems
- State snapshots for recovery points
- Idempotent operations for safe retry

### Partial Install Recovery

**Install Phases**
1. Dependency download and verification
2. Configuration validation
3. File deployment
4. Service registration
5. Health check verification

**Recovery Points**
- Create restore points before each phase
- Enable rollback to previous restore point
- Clean up partial installations
- Verify system state after recovery

**Rollback Triggers**
- Phase validation failure
- Health check failure
- Dependency conflict
- Configuration validation error

### State Transition Recovery

**State Machine Design**
- Define valid state transitions
- Track current state explicitly
- Validate transitions before execution
- Log all state changes

**Recovery Strategies**
- Resume from last known good state
- Replay event stream from checkpoint
- Rebuild state from authoritative source
- Manual intervention for complex failures

## Observability Requirements

### Error Observability

**Structured Logging**
- Use structured log formats (JSON)
- Include request ID, user ID, operation
- Log error type, severity, and context
- Include stack traces for exceptions
- Avoid logging sensitive data

**Error Context Requirements**
- Timestamp with timezone
- Operation being performed
- Input parameters (sanitized)
- Error message and type
- Stack trace for exceptions
- Request correlation ID
- System state at failure time

**Log Levels and Usage**

```
ERROR: Failures that require immediate attention
- Service unavailable
- Data loss or corruption
- Security violations
- Configuration failures

WARN: Conditions that may indicate future problems
- High resource usage
- Deprecated API usage
- Performance degradation
- Retry attempts approaching limit

INFO: Normal operational events
- Service startup and shutdown
- Configuration loaded
- Health check results
- User authentication (success)

DEBUG: Detailed diagnostic information
- Request and response payloads
- Detailed state information
- Internal processing steps
- Performance metrics
```

### Metrics and Monitoring

**Golden Signals**
- Latency: Time to service requests
- Traffic: Request volume per time unit
- Errors: Rate of failed requests
- Saturation: Resource utilization

**Operational Metrics**
- Request rate by endpoint
- Error rate by type
- Response time distribution (p50, p95, p99)
- Active connection count
- Queue depth and processing rate
- Resource utilization (CPU, memory, disk)
- Cache hit/miss rates

**Alert Thresholds**
- Error rate > 5% for 5 minutes: Warning
- Error rate > 20% for 2 minutes: Critical
- Latency p99 > 5 seconds for 5 minutes: Warning
- Latency p99 > 10 seconds for 2 minutes: Critical
- Resource saturation > 80% for 10 minutes: Warning
- Resource saturation > 95% for 5 minutes: Critical

### Tracing and Correlation

**Distributed Tracing**
- Generate trace IDs for each request
- Propagate trace IDs across service boundaries
- Record span information for each operation
- Include timing and status information

**Correlation Requirements**
- Unique request ID for each user operation
- Correlation across logs, metrics, and traces
- Link related operations in complex workflows
- Track operations across agentic tool calls

## Rollback and Disablement

### Rollback Strategy

**Rollback Triggers**
- P0 failures that block production
- P1 failures with accepted risk threshold exceeded
- Security vulnerabilities discovered
- Data integrity issues
- Performance degradation beyond thresholds

**Rollback Process**
1. Detect failure through monitoring or alerts
2. Assess impact and determine rollback necessity
3. Notify stakeholders of rollback decision
4. Execute rollback procedure
5. Verify system state after rollback
6. Document rollback reason and actions
7. Schedule fix and re-deployment

**Rollback Time Objectives**
- Decision time: < 5 minutes
- Execution time: < 10 minutes
- Verification time: < 5 minutes
- Total rollback time: < 20 minutes

### Disablement Procedures

**Feature Disablement**
- Use feature flags for gradual disablement
- Disable for new users first, then existing
- Maintain data compatibility during disablement
- Document disablement criteria and process

**Emergency Disablement**
- One-click disable for critical features
- Automated disablement for security vulnerabilities
- Communication plan for affected users
- Recovery plan for re-enablement

### Rollback Testing

**Regular Rollback Drills**
- Test rollback procedures monthly
- Verify rollback scripts work correctly
- Measure actual rollback time
- Update runbooks based on drill results

**Rollback Verification**
- Verify system functionality after rollback
- Check data integrity
- Confirm monitoring and alerting operational
- Validate user-facing functionality

## Safe Write Operations

### Write Safety Principles

**Pre-Write Validation**
- Validate output paths before writing
- Check file system permissions
- Verify sufficient disk space
- Ensure destination is not a directory or symlink

**Atomic Write Operations**
- Write to temporary location first
- Validate written content
- Rename atomically to final location
- Clean up temporary files on failure

**Backup and Versioning**
- Create backup before overwriting existing files
- Use version numbers for iterative changes
- Maintain backup retention policy
- Enable quick restoration from backups

### Write Conflict Resolution

**Concurrent Write Handling**
- Use file locks for exclusive access
- Implement optimistic concurrency control
- Detect and resolve write conflicts
- Fail safely when conflicts cannot be resolved

**Partial Write Recovery**
- Detect incomplete writes
- Rollback to previous version
- Log partial write incidents
- Alert on repeated partial writes

## Install Safety

### Dependency Management

**Dependency Verification**
- Verify checksums of downloaded packages
- Use locked dependency versions
- Validate package signatures
- Scan for known vulnerabilities

**Install Isolation**
- Use virtual environments or containers
- Separate dependencies by project
- Avoid global package installation
- Document dependency requirements

**Install Rollback**
- Snapshot system state before install
- Enable quick rollback on failure
- Verify system state after install
- Clean up failed installations

### Migration Safety

**Migration Planning**
- Document migration steps
- Identify rollback points
- Test migrations in staging
- Prepare rollback scripts

**Migration Execution**
- Backup data before migration
- Execute migrations in transaction
- Validate migration results
- Enable monitoring for post-migration issues

## Production Readiness

### Production Readiness Criteria

**Functional Requirements**
- All P0 requirements implemented
- All P1 requirements addressed or accepted
- Core functionality tested and verified
- Edge cases handled appropriately

**Non-Functional Requirements**
- Performance benchmarks met
- Security review completed
- Monitoring and alerting configured
- Documentation complete

**Operational Requirements**
- Runbooks and procedures documented
- On-call rotation established
- Escalation paths defined
- Incident response plan ready

### Release Gates

**Mandatory Gates**
- P0 failures must be resolved before release
- P1 failures require explicit acceptance
- Security review for authentication/authorization changes
- Performance testing for high-traffic features
- Documentation review for user-facing changes

**Optional Gates**
- Code review for all changes
- Automated test coverage verification
- Accessibility review for UI changes
- Localization review for multi-language support

### Release Evidence

**Required Evidence**
- Test execution results with pass/fail status
- Performance benchmark results
- Security scan results
- Manual testing sign-off
- Documentation updates

**Evidence Retention**
- Store evidence with release artifacts
- Link evidence to specific release version
- Archive evidence for compliance requirements
- Make evidence accessible for post-release review

## Required References

- Read `reliability-checklist.md` before reviewing implementation or release readiness.
- Read `recovery-playbook.md` when the task involves install, migration, rollout, rollback, or partial failure.
- Read `timeout-strategy.md` for detailed timeout configuration patterns.
- Read `retry-policy.md` for comprehensive retry strategy guidelines.
- Read `observability-standards.md` for logging and monitoring requirements.
- Read `deployment-safety.md` for deployment and release safety procedures.

## Default Output

When asked to harden a system, return:

1. Critical failure modes.
2. Missing error handling.
3. Reliability improvements made or recommended.
4. Verification commands and results.
5. Remaining risk, if any.

## Advanced Topics

### Chaos Engineering Principles

**Failure Injection**
- Inject failures in controlled environments
- Test system behavior under failure conditions
- Identify weaknesses before production
- Build confidence in recovery mechanisms

**Game Days**
- Regular failure simulation exercises
- Test incident response procedures
- Validate monitoring and alerting
- Train team on recovery procedures

### Resilience Patterns

**Retry Pattern**
- Automatic retry of failed operations
- Exponential backoff with jitter
- Circuit breaker to prevent cascading failures
- Appropriate for transient failures

**Circuit Breaker Pattern**
- Monitor failure rates
- Open circuit when failures exceed threshold
- Return fallback response immediately
- Periodically test for recovery

**Bulkhead Pattern**
- Isolate critical resources
- Separate thread pools for different operation types
- Prevent cascading failures
- Resource allocation per service

**Timeout Pattern**
- Set absolute time limits on operations
- Fail fast when timeout exceeded
- Clean up resources on timeout
- Return appropriate error response

**Fallback Pattern**
- Provide alternative behavior when primary fails
- Cache responses for fallback
- Return sensible defaults
- Maintain service availability

### Anti-Patterns to Avoid

**Retry Storms**
- Too many clients retrying simultaneously
- Overwhelms already struggling service
- Solution: Exponential backoff with jitter

**Cascading Failures**
- Failure in one component causes failures in others
- Solution: Circuit breakers and bulkheads

**Retry Without Bounds**
- Infinite retry loops
- Wastes resources and time
- Solution: Maximum retry count and total timeout

**Ignoring Failure Context**
- Retrying non-retryable failures
- Wastes time and resources
- Solution: Classify failures before retry

**Missing Observability**
- Cannot diagnose failures
- Cannot verify recovery
- Solution: Comprehensive logging and metrics

## Compliance and Audit

### Audit Requirements

**Change Documentation**
- Document all reliability changes
- Record failure modes identified
- Document recovery procedures
- Maintain change history

**Incident Documentation**
- Record all incidents and outages
- Document root cause analysis
- Record remediation steps
- Track time to resolution

**Testing Documentation**
- Document all reliability tests
- Record test results
- Document test coverage
- Maintain test history

### Regulatory Considerations

**Data Retention**
- Retain logs for required periods
- Archive evidence for compliance
- Ensure log immutability
- Protect sensitive log data

**Audit Trails**
- Record all configuration changes
- Track deployment history
- Document rollback events
- Maintain access logs

**Reporting Requirements**
- Generate required compliance reports
- Track key reliability metrics
- Document exception handling
- Maintain evidence for audits

## Implementation Guidance

### Language-Specific Considerations

**Python**
- Use `tenacity` library for retry logic
- Use `circuitbreaker` library for circuit breakers
- Use `asyncio` timeout features
- Use `logging` module with structured logging

**JavaScript/TypeScript**
- Use `axios-retry` for HTTP retries
- Use `opossum` for circuit breakers
- Use `Promise.race` for timeout implementation
- Use `winston` or `pino` for logging

**Java**
- Use `resilience4j` for resilience patterns
- Use `Hystrix` or `Sentinel` for circuit breakers
- Use `CompletableFuture` with timeout
- Use `SLF4J` with structured logging

**Go**
- Use `go-retryablehttp` for retries
- Implement circuit breaker manually or with library
- Use `context` package for timeouts
- Use structured logging with `zap` or `logrus`

### Framework Integration

**Web Frameworks**
- Implement middleware for timeout and retry
- Add health check endpoints
- Integrate with monitoring systems
- Implement graceful shutdown

**Message Queues**
- Configure dead letter queues
- Implement message retry with backoff
- Handle poison messages appropriately
- Monitor queue depth and processing rate

**Databases**
- Configure connection pool limits
- Implement query timeouts
- Handle connection failures gracefully
- Monitor query performance

## Maintenance and Evolution

### Ongoing Maintenance

**Regular Reviews**
- Review failure modes monthly
- Update retry policies based on observed failures
- Adjust timeout values based on performance data
- Refine circuit breaker thresholds

**Continuous Improvement**
- Learn from incidents and outages
- Update recovery procedures based on experience
- Improve monitoring and alerting
- Enhance documentation

### Evolution Planning

**Capacity Planning**
- Monitor growth trends
- Plan for increased load
- Scale components proactively
- Test at expected future load

**Technology Evolution**
- Evaluate new resilience libraries and patterns
- Update dependencies regularly
- Adopt improved practices
- Maintain backward compatibility

## Checklist

### Pre-Implementation Checklist

- [ ] Failure modes identified and documented
- [ ] Failure classification complete (blocking, recoverable, degraded, informational)
- [ ] Timeout values defined for all external calls
- [ ] Retry strategy selected and configured
- [ ] Circuit breaker thresholds defined
- [ ] Fallback behavior specified and tested
- [ ] Observability requirements documented
- [ ] Rollback procedures defined
- [ ] Safe write patterns implemented
- [ ] Install safety procedures documented

### Post-Implementation Checklist

- [ ] Timeouts tested under various load conditions
- [ ] Retries tested with simulated failures
- [ ] Circuit breaker tested with sustained failures
- [ ] Fallback tested with primary service failure
- [ ] Partial write recovery tested
- [ ] Partial install recovery tested
- [ ] Observability verified (logs, metrics, traces)
- [ ] Rollback procedure tested
- [ ] Performance benchmarks met
- [ ] Documentation complete

## References

- `reliability-checklist.md` - Detailed reliability checklist
- `recovery-playbook.md` - Recovery procedures for failures
- `timeout-strategy.md` - Timeout configuration patterns
- `retry-policy.md` - Retry strategy guidelines
- `observability-standards.md` - Logging and monitoring requirements
- `deployment-safety.md` - Deployment and release safety
