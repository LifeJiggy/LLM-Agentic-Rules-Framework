# Tools Troubleshooting - LLM & Agentic Rules Framework

## Overview

This document provides practical solutions for common issues encountered during tool integration.

## Issue 1: Tool Authentication Failures

### Symptoms

- Tool invocations fail with authentication errors
- Cannot access external services
- Credentials rejected
- Access denied

### Root Cause

- Expired credentials
- Incorrect credentials
- Permission changes
- Account lockout

### Resolution

#### Step 1: Verify Credentials

```python
def verify_credentials(tool_config):
    """Verify tool credentials are valid."""
    checks = []
    
    # Check credential existence
    if not tool_config.credentials:
        checks.append({"check": "credentials_exist", "passed": False})
        return checks
    
    # Check credential format
    if not validate_credential_format(tool_config.credentials):
        checks.append({"check": "credential_format", "passed": False})
        return checks
    
    # Check credential expiration
    if is_credential_expired(tool_config.credentials):
        checks.append({"check": "credential_freshness", "passed": False})
        return checks
    
    # Test credential
    if not test_credential(tool_config.credentials):
        checks.append({"check": "credential_validity", "passed": False})
        return checks
    
    checks.append({"check": "all_checks", "passed": True})
    return checks
```

#### Step 2: Rotate Credentials

```yaml
credential_rotation:
  process:
    - step: "generate_new_credential"
      action: "vault_write"
      path: "secret/tools/{tool_name}"
    
    - step: "update_tool_config"
      action: "update_configuration"
      path: "tools/{tool_name}/config.yaml"
    
    - step: "test_new_credential"
      action: "test_tool_connection"
      timeout: "30 seconds"
    
    - step: "revoke_old_credential"
      action: "vault_delete"
      path: "secret/tools/{tool_name}/previous"
      delay: "24 hours"
  
  schedule:
    frequency: "quarterly"
    notification: "7_days_before"
```

#### Step 3: Verify Permissions

```yaml
permission_verification:
  checks:
    - check: "role_assigned"
      description: "Verify role is assigned to tool"
      action: "check_role_assignment"
    
    - check: "permissions_match"
      description: "Verify permissions match requirements"
      action: "compare_permissions"
    
    - check: "constraints_satisfied"
      description: "Verify constraints are satisfied"
      action: "check_constraints"
  
  remediation:
    - action: "assign_role"
      when: "role_not_assigned"
    
    - action: "update_permissions"
      when: "permissions_mismatch"
    
    - action: "satisfy_constraints"
      when: "constraints_not_satisfied"
```

### Prevention

- Rotate credentials regularly
- Monitor credential expiration
- Verify permissions periodically
- Implement credential validation

## Issue 2: Rate Limiting Issues

### Symptoms

- Tool invocations rejected with 429 status
- Cannot make API calls
- Performance degraded
- User complaints

### Root Cause

- Rate limits too restrictive
- Too many concurrent requests
- Burst traffic exceeded limits
- Shared rate limit across users

### Resolution

#### Step 1: Analyze Rate Limit Usage

```python
def analyze_rate_limit_usage(tool_metrics):
    """Analyze rate limit usage patterns."""
    analysis = {
        "total_requests": sum(tool_metrics["requests_per_minute"]),
        "average_requests": sum(tool_metrics["requests_per_minute"]) / len(tool_metrics["requests_per_minute"]),
        "peak_requests": max(tool_metrics["requests_per_minute"]),
        "limit_breaches": sum(1 for r in tool_metrics["requests_per_minute"] if r > tool_metrics["rate_limit"])
    }
    
    return analysis
```

#### Step 2: Optimize Rate Limiting

```yaml
rate_limit_optimization:
  strategies:
    - strategy: "request_batching"
      description: "Batch multiple requests into one"
      implementation: "batch_requests()"
      expected_improvement: "50-70%"
    
    - strategy: "request_caching"
      description: "Cache frequent requests"
      implementation: "cache_requests()"
      expected_improvement: "30-50%"
    
    - strategy: "request_throttling"
      description: "Throttle requests to stay under limit"
      implementation: "throttle_requests()"
      expected_improvement: "100%"
    
    - strategy: "limit_increase"
      description: "Request rate limit increase"
      implementation: "request_limit_increase()"
      expected_improvement: "depends_on_provider"
  
  monitoring:
    - metric: "requests_per_minute"
      target: "< rate_limit * 0.8"
      alert: "approaching_limit"
    
    - metric: "rate_limit_breaches"
      target: 0
      alert: "breach_detected"
```

#### Step 3: Implement Request Queuing

```python
import queue
import threading
import time

class RequestQueue:
    def __init__(self, rate_limit: int):
        self.rate_limit = rate_limit
        self.queue = queue.Queue()
        self.processing = False
        self.lock = threading.Lock()
    
    def add_request(self, request):
        """Add request to queue."""
        self.queue.put(request)
        self.process_queue()
    
    def process_queue(self):
        """Process queued requests."""
        with self.lock:
            if self.processing:
                return
            
            self.processing = True
        
        while not self.queue.empty():
            request = self.queue.get()
            
            # Wait if at rate limit
            if self.at_rate_limit():
                time.sleep(1)
            
            # Process request
            self.process_request(request)
            
            self.queue.task_done()
        
        with self.lock:
            self.processing = False
    
    def at_rate_limit(self):
        """Check if at rate limit."""
        # Implement rate limit check
        return False
    
    def process_request(self, request):
        """Process a single request."""
        # Implement request processing
        pass
```

### Prevention

- Monitor rate limit usage
- Implement request queuing
- Use caching strategically
- Request limit increases when needed

## Issue 3: Tool Timeout Issues

### Symptoms

- Tool invocations timeout
- Requests take too long
- User complaints about slow responses
- Performance degraded

### Root Cause

- Timeout too short
- External service slow
- Network issues
- Resource constraints

### Resolution

#### Step 1: Analyze Timeout Patterns

```python
def analyze_timeout_patterns(tool_metrics):
    """Analyze timeout patterns."""
    analysis = {
        "total_timeouts": sum(1 for m in tool_metrics["invocations"] if m["duration"] > tool_metrics["timeout"]),
        "average_duration": sum(m["duration"] for m in tool_metrics["invocations"]) / len(tool_metrics["invocations"]),
        "max_duration": max(m["duration"] for m in tool_metrics["invocations"]),
        "timeout_rate": sum(1 for m in tool_metrics["invocations"] if m["duration"] > tool_metrics["timeout"]) / len(tool_metrics["invocations"])
    }
    
    return analysis
```

#### Step 2: Optimize Timeout Configuration

```yaml
timeout_optimization:
  strategies:
    - strategy: "increase_timeout"
      description: "Increase timeout for slow operations"
      implementation: "update_timeout()"
      when: "external_service_slow"
    
    - strategy: "async_processing"
      description: "Process asynchronously"
      implementation: "async_process()"
      when: "operation_not_time_sensitive"
    
    - strategy: "cached_responses"
      description: "Use cached responses"
      implementation: "cache_responses()"
      when: "operation_frequently_repeated"
    
    - strategy: "circuit_breaker"
      description: "Stop calling failing service"
      implementation: "circuit_breaker()"
      when: "external_service_failing"
  
  monitoring:
    - metric: "timeout_rate"
      target: "< 1%"
      alert: "increasing_timeout_rate"
    
    - metric: "average_duration"
      target: "< timeout * 0.5"
      alert: "approaching_timeout"
```

#### Step 3: Implement Circuit Breaker

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### Prevention

- Set appropriate timeouts
- Monitor timeout rates
- Implement circuit breakers
- Use async processing when possible

## Issue 4: Tool Data Quality Issues

### Symptoms

- Tool returns incorrect data
- Data validation failures
- Inconsistent results
- User complaints about data quality

### Root Cause

- Data source issues
- Transformation errors
- Validation gaps
- Data inconsistency

### Resolution

#### Step 1: Analyze Data Quality

```python
def analyze_data_quality(tool_results):
    """Analyze data quality issues."""
    analysis = {
        "total_results": len(tool_results),
        "valid_results": sum(1 for r in tool_results if r["valid"]),
        "invalid_results": sum(1 for r in tool_results if not r["valid"]),
        "validation_errors": {}
    }
    
    for result in tool_results:
        if not result["valid"]:
            error_type = result["error_type"]
            if error_type not in analysis["validation_errors"]:
                analysis["validation_errors"][error_type] = 0
            analysis["validation_errors"][error_type] += 1
    
    return analysis
```

#### Step 2: Improve Data Validation

```yaml
data_validation:
  rules:
    - rule: "type_check"
      description: "Validate data types"
      implementation: "validate_types()"
    
    - rule: "format_check"
      description: "Validate data format"
      implementation: "validate_format()"
    
    - rule: "range_check"
      description: "Validate data ranges"
      implementation: "validate_ranges()"
    
    - rule: "consistency_check"
      description: "Validate data consistency"
      implementation: "validate_consistency()"
  
  error_handling:
    - action: "reject"
      when: "validation_fails"
      response: "Invalid data"
    
    - action: "clean"
      when: "data_can_be_cleaned"
      response: "cleaned_data"
    
    - action: "fallback"
      when: "validation_fails"
      response: "fallback_data"
```

#### Step 3: Implement Data Quality Monitoring

```yaml
data_quality_monitoring:
  metrics:
    - metric: "validity_rate"
      description: "Percentage of valid data"
      target: "> 99%"
      alert: "validity_rate < 99%"
    
    - metric: "completeness_rate"
      description: "Percentage of complete data"
      target: "> 95%"
      alert: "completeness_rate < 95%"
    
    - metric: "consistency_rate"
      description: "Percentage of consistent data"
      target: "> 99%"
      alert: "consistency_rate < 99%"
  
  monitoring_frequency: "daily"
  reporting: "weekly"
```

### Prevention

- Implement comprehensive validation
- Monitor data quality metrics
- Validate data sources
- Implement data cleaning

## Diagnostic Commands

| Purpose | Command | Expected Output |
|---------|---------|-----------------|
| Check tool status | `tool --status` | Current tool state |
| View tool logs | `tool --logs` | Tool execution logs |
| Test tool connection | `tool --test-connection` | Connection test results |
| Check rate limits | `tool --rate-limits` | Rate limit status |
| Validate configuration | `tool --validate-config` | Configuration validation results |

## Escalation Criteria

| Condition | Action | Contact |
|-----------|--------|---------|
| Authentication failures > 5/hour | Escalate to security | Security Team |
| Rate limit breaches > 10/hour | Escalate to operations | Operations Team |
| Timeout rate > 10% | Escalate to engineering | Engineering Lead |
| Data quality issues > 5% | Escalate to data team | Data Team |
| Security concern | Immediate escalation | Security Team |

## References

- Tool fundamentals: `tools-fundamentals.md`
- Tool best practices: `tools-best-practices.md`
- Tool anti-patterns: `tools-anti-patterns.md`
- Tool checklist: `tools-checklist.md`
- Tool examples: `tools-examples.md`
- Tool advanced: `tools-advanced.md`
