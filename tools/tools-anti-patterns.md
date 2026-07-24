# Tools Anti-Patterns - LLM & Agentic Rules Framework

## Overview

This document describes common mistakes, failure modes, and dangerous approaches to avoid when integrating tools in LLM and agentic systems.

## Anti-Pattern 1: Overly Broad Permissions

### Description

Granting tools more permissions than necessary for their function.

### Why It Fails

- Increases attack surface
- Enables privilege escalation
- Violates least privilege principle
- Increases blast radius of compromises

### Warning Signs

- Tools have admin access when not needed
- Tools can access all data types
- Tools can perform any action
- No permission scoping

### Correct Approach

```yaml
correct_permissions:
  principle: "least_privilege"
  
  tool: "database_query"
  permissions:
    - "read:customers"
    - "read:orders"
  restrictions:
    - "no_write"
    - "no_delete"
    - "no_schema_changes"
  
  tool: "email_send"
  permissions:
    - "send:email"
  restrictions:
    - "only_verified_recipients"
    - "no_attachments"
    - "rate_limit:10_per_hour"
```

## Anti-Pattern 2: No Error Handling

### Description

Tool invocations without proper error handling or recovery.

### Why It Fails

- Transient errors cause immediate failure
- No retry for temporary issues
- Poor user experience
- System instability

### Warning Signs

- No try-catch blocks
- No retry logic
- No fallback behavior
- No error logging

### Correct Approach

```yaml
error_handling:
  retry:
    enabled: true
    max_retries: 3
    backoff:
      initial_delay: "100ms"
      max_delay: "30 seconds"
      multiplier: 2
  
  fallback:
    enabled: true
    strategy: "cached_response"
    cache_ttl: "1 hour"
    fallback_response: "I'm unable to complete this action right now."
  
  logging:
    enabled: true
    fields: ["error_type", "message", "tool_id", "timestamp"]
```

## Anti-Pattern 3: Missing Audit Logging

### Description

Tool invocations without audit logging for security and compliance.

### Why It Fails

- No evidence for security incidents
- Cannot investigate issues
- Compliance violations
- No accountability

### Warning Signs

- No audit logs
- Logs not retained
- Logs not monitored
- No integrity protection

### Correct Approach

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
  
  retention: "1_year"
  storage: "immutable_log_store"
  integrity: "hash_chain"
  
  monitoring:
    - condition: "failed_authentication"
      severity: "high"
      action: "alert_security_team"
```

## Anti-Pattern 4: No Rate Limiting

### Description

Tool invocations without rate limiting, allowing abuse.

### Why It Fails

- Enables abuse and denial of service
- Causes resource exhaustion
- Impacts other users
- Increases costs

### Warning Signs

- No rate limits configured
- Unlimited API calls
- No usage tracking
- No abuse detection

### Correct Approach

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
  
  response:
    status_code: 429
    message: "Rate limit exceeded. Please try again later."
    retry_after: "30 seconds"
```

## Anti-Pattern 5: Hardcoded Credentials

### Description

Storing tool credentials directly in code or configuration.

### Why It Fails

- Credentials exposed in version control
- Cannot rotate credentials
- Cannot control access
- Security vulnerability

### Warning Signs

- API keys in code
- Passwords in configuration files
- Tokens in environment variables
- No secret management

### Correct Approach

```yaml
credential_management:
  provider: "hashicorp_vault"
  
  secrets:
    - name: "database_password"
      path: "secret/tools/database"
      rotation: "monthly"
    
    - name: "api_key"
      path: "secret/tools/api"
      rotation: "quarterly"
  
  access:
    - role: "tool_service"
      secrets: ["database_password", "api_key"]
      constraints: ["ip_based", "time_based"]
  
  audit:
    enabled: true
    events: ["read", "write", "rotate"]
    retention: "1_year"
```

## Anti-Pattern 6: No Input Validation

### Description

Tool invocations without input validation, allowing injection attacks.

### Why It Fails

- Enables injection attacks
- Causes data corruption
- Creates security vulnerabilities
- Impacts system stability

### Warning Signs

- No input validation
- No sanitization
- No schema validation
- No length limits

### Correct Approach

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

## Anti-Pattern 7: No Monitoring

### Description

Tool invocations without monitoring or alerting.

### Why It Fails

- Cannot detect issues
- Cannot measure performance
- Cannot optimize usage
- Cannot plan for growth

### Warning Signs

- No metrics collected
- No dashboards configured
- No alerts configured
- No performance tracking

### Correct Approach

```yaml
monitoring:
  enabled: true
  
  metrics:
    - metric: "latency"
      description: "Tool invocation latency"
      target: "< 1 second"
    
    - metric: "error_rate"
      description: "Tool error rate"
      target: "< 1%"
    
    - metric: "throughput"
      description: "Tool invocations per second"
      target: "> 10"
  
  dashboards:
    - name: "Tool Performance"
      metrics: ["latency", "error_rate", "throughput"]
      refresh: "real_time"
  
  alerts:
    - condition: "error_rate > 5%"
      severity: "high"
      action: "alert_operations"
    
    - condition: "latency > 5 seconds"
      severity: "medium"
      action: "alert_engineering"
```

## Anti-Pattern Summary Table

| Anti-Pattern | Risk Level | Impact | Detection Difficulty | Remediation Effort |
|--------------|------------|--------|---------------------|-------------------|
| Overly broad permissions | High | Privilege escalation, data exposure | Easy | Medium |
| No error handling | Medium | Poor UX, system instability | Easy | Low |
| Missing audit logging | High | Security blind spots, compliance violations | Easy | Low |
| No rate limiting | Medium | Abuse, resource exhaustion | Easy | Low |
| Hardcoded credentials | Critical | Credential exposure, security breach | Easy | Medium |
| No input validation | High | Injection attacks, data corruption | Easy | Low |
| No monitoring | Medium | Cannot detect issues, cannot optimize | Easy | Low |

## Prevention Strategies

### Code Review Checklist

```yaml
code_review:
  tool_review:
    - "permissions_are_minimal"
    - "error_handling_implemented"
    - "audit_logging_enabled"
    - "rate_limiting_configured"
    - "credentials_in_vault"
    - "input_validation_implemented"
    - "monitoring_configured"
    - "documentation_complete"
```

### Automated Detection

```yaml
anti_pattern_detection:
  rules:
    - rule: "detect_overly_broad_permissions"
      condition: "tool_has_admin_access"
      action: "alert_security_team"
    
    - rule: "detect_no_error_handling"
      condition: "no_try_catch_in_tool_call"
      action: "alert_developer"
    
    - rule: "detect_missing_audit"
      condition: "no_audit_logging"
      action: "alert_security_team"
    
    - rule: "detect_no_rate_limiting"
      condition: "no_rate_limit_configured"
      action: "alert_operations"
    
    - rule: "detect_hardcoded_credentials"
      condition: "credentials_in_code"
      action: "alert_security_team"
```

## References

- Tool fundamentals: `tools-fundamentals.md`
- Tool best practices: `tools-best-practices.md`
- Tool checklist: `tools-checklist.md`
- Tool examples: `tools-examples.md`
- Tool troubleshooting: `tools-troubleshooting.md`
- Tool advanced: `tools-advanced.md`
