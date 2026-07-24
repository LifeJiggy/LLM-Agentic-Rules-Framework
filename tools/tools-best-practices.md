# Tools Best Practices - LLM & Agentic Rules Framework

## Overview

This document provides recommended patterns, standards, and approaches for tool integration in LLM and agentic systems.

## Best Practice 1: Least Privilege Principle

### Pattern

Grant tools only the minimum permissions necessary for their function.

**Permission Levels**:

| Level | Description | Use Case |
|-------|-------------|----------|
| Read-only | Can only read data | Data lookup, search |
| Write | Can create and update data | Data entry, updates |
| Delete | Can remove data | Data cleanup, soft delete |
| Admin | Can manage configurations | System administration |

**Implementation**:

```yaml
tool_permissions:
  tool: "database_query"
  permissions:
    - "read:customers"
    - "read:orders"
    - "read:products"
  restrictions:
    - "no_write"
    - "no_delete"
    - "no_schema_changes"
  audit: true
  approval_required: false

tool_permissions:
  tool: "email_send"
  permissions:
    - "send:email"
  restrictions:
    - "only_verified_recipients"
    - "no_attachments"
    - "rate_limit:10_per_hour"
  audit: true
  approval_required: true
  approval_threshold: "external_recipients"
```

## Best Practice 2: Comprehensive Error Handling

### Pattern

Implement robust error handling with retry logic, fallbacks, and clear error messages.

**Error Handling Strategy**:

```yaml
error_handling:
  retry:
    enabled: true
    max_retries: 3
    backoff:
      initial_delay: "100ms"
      max_delay: "30 seconds"
      multiplier: 2
      jitter: true
    retryable_errors:
      - "timeout"
      - "rate_limit"
      - "temporary_server_error"
  
  fallback:
    enabled: true
    strategy: "cached_response"
    cache_ttl: "1 hour"
    fallback_response: "I'm unable to complete this action right now. Please try again later."
  
  error_messages:
    user_friendly: true
    include_suggestion: true
    log_details: true
```

## Best Practice 3: Comprehensive Audit Logging

### Pattern

Log all tool invocations for security, debugging, and compliance.

**Audit Log Structure**:

```yaml
audit_logging:
  enabled: true
  fields:
    - "tool_id"
    - "user_id"
    - "timestamp"
    - "parameters"
    - "result"
    - "success"
    - "duration_ms"
    - "error_message"
  
  sensitive_fields:
    - "credentials"
    - "personal_data"
    - "financial_data"
  
  retention: "1_year"
  storage: "immutable_log_store"
  integrity: "hash_chain"
  
  alerts:
    - condition: "failed_authentication"
      severity: "high"
      action: "alert_security_team"
    
    - condition: "unusual_pattern"
      severity: "medium"
      action: "alert_operations"
```

## Best Practice 4: Rate Limiting and Quotas

### Pattern

Implement rate limiting to prevent abuse and ensure fair usage.

**Rate Limiting Configuration**:

```yaml
rate_limiting:
  global:
    requests_per_minute: 100
    requests_per_hour: 1000
  
  per_user:
    requests_per_minute: 10
    requests_per_hour: 100
  
  per_tool:
    database_query:
      requests_per_minute: 50
      requests_per_hour: 500
    
    email_send:
      requests_per_minute: 5
      requests_per_hour: 50
    
    file_upload:
      requests_per_minute: 2
      requests_per_hour: 20
  
  response:
    status_code: 429
    message: "Rate limit exceeded. Please try again later."
    retry_after: "30 seconds"
```

## Best Practice 5: Input Validation

### Pattern

Validate all tool inputs to prevent errors and security issues.

**Validation Rules**:

```yaml
input_validation:
  enabled: true
  rules:
    - rule: "type_check"
      description: "Validate input types"
      action: "reject"
    
    - rule: "length_limit"
      description: "Enforce maximum input length"
      max_length: 1000
      action: "truncate"
    
    - rule: "format_check"
      description: "Validate input format"
      patterns:
        - "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        - "phone": "^\\+?[1-9]\\d{1,14}$"
      action: "reject"
    
    - rule: "sanitization"
      description: "Sanitize input for safety"
      remove:
        - "<script>"
        - "javascript:"
        - "onload="
      action: "sanitize"
  
  error_response:
    status_code: 400
    message: "Invalid input"
    details: "Please check your input and try again."
```

## Best Practice 6: Caching Strategy

### Pattern

Implement caching to improve performance and reduce external calls.

**Caching Configuration**:

```yaml
caching:
  enabled: true
  strategy: "write_through"
  
  cache_rules:
    - rule: "data_lookup"
      ttl: "5 minutes"
      invalidation: "on_write"
    
    - rule: "configuration"
      ttl: "1 hour"
      invalidation: "on_change"
    
    - rule: "static_data"
      ttl: "24 hours"
      invalidation: "on_deploy"
  
  cache_storage:
    type: "redis"
    host: "cache.internal"
    port: 6379
    db: 0
  
  monitoring:
    metrics:
      - "cache_hit_rate"
      - "cache_miss_rate"
      - "cache_size"
    alerts:
      - condition: "hit_rate < 0.8"
        severity: "medium"
        action: "review_caching_strategy"
```

## Best Practice 7: Timeout Configuration

### Pattern

Configure appropriate timeouts to prevent hanging requests.

**Timeout Configuration**:

```yaml
timeouts:
  global:
    default: "30 seconds"
    max: "5 minutes"
  
  per_tool:
    database_query:
      timeout: "10 seconds"
      retry_on_timeout: true
    
    email_send:
      timeout: "30 seconds"
      retry_on_timeout: false
    
    file_upload:
      timeout: "2 minutes"
      retry_on_timeout: true
    
    external_api:
      timeout: "30 seconds"
      retry_on_timeout: true
  
  escalation:
    on_timeout:
      action: "return_cached_response"
      fallback: "return_error_message"
      alert: "notify_operations"
```

## Best Practice Documentation

### Tool Specification Template

```yaml
tool_specification:
  tool_id: string
  name: string
  description: string
  category: string
  version: string
  
  input_schema:
    type: object
    properties: object
    required: [list]
  
  output_schema:
    type: object
    properties: object
  
  permissions:
    required: [list]
    scope: string
  
  rate_limit:
    requests_per_minute: integer
    burst_limit: integer
  
  timeout:
    default: string
    max: string
  
  error_handling:
    retryable_errors: [list]
    max_retries: integer
    fallback: string
```

### Tool Monitoring Dashboard Template

```yaml
monitoring_dashboard:
  name: "Tool Monitoring Dashboard"
  refresh: "real_time"
  
  panels:
    - name: "Tool Performance"
      metrics:
        - "latency_p50"
        - "latency_p95"
        - "throughput"
        - "error_rate"
    
    - name: "Tool Usage"
      metrics:
        - "invocation_count"
        - "unique_users"
        - "popular_tools"
    
    - name: "Tool Health"
      metrics:
        - "availability"
        - "success_rate"
        - "error_rate"
    
    - name: "Tool Costs"
      metrics:
        - "cost_per_invocation"
        - "total_cost"
        - "cost_by_tool"
```

## References

- Tool fundamentals: `tools-fundamentals.md`
- Tool anti-patterns: `tools-anti-patterns.md`
- Tool checklist: `tools-checklist.md`
- Tool examples: `tools-examples.md`
- Tool troubleshooting: `tools-troubleshooting.md`
- Tool advanced: `tools-advanced.md`
