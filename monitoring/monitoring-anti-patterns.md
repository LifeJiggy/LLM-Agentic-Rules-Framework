# Monitoring Anti-Patterns for AI/LLM Systems

## Common Mistakes and How to Avoid Them

---

## Table of Contents

1. [Alert Fatigue](#alert-fatigue)
2. [Missing Baseline](#missing-baseline)
3. [No Correlation](#no-correlation)
4. [Log Spam](#log-spam)
5. [Dashboard Overload](#dashboard-overload)
6. [No Escalation Path](#no-escalation-path)
7. [Metric Cardinality Explosion](#metric-cardinality-explosion)
8. [Alert Noise](#alert-noise)
9. [Missing Context](#missing-context)
10. [Anti-Pattern Solutions](#anti-pattern-solutions)

---

## Alert Fatigue

### The Problem

Alert fatigue occurs when teams receive so many alerts that they begin to ignore or dismiss them, potentially missing critical issues.

### Warning Signs

```yaml
symptoms:
  - "Alerts acknowledged without investigation"
  - "Alerts silenced for long periods"
  - "Team members stop checking alert channels"
  - "Response times to alerts increase"
  - "False positive alerts become normalized"
  
metrics_to_watch:
  alert_volume:
    description: "Total alerts per day"
    healthy: "< 20 per day"
    warning: "20-50 per day"
    critical: "> 50 per day"
    
  alert_ack_rate:
    description: "Percentage of alerts acknowledged"
    healthy: "> 90% within SLA"
    warning: "70-90% within SLA"
    critical: "< 70% within SLA"
    
  alert_action_rate:
    description: "Percentage of alerts requiring action"
    healthy: "> 80%"
    warning: "50-80%"
    critical: "< 50%"
```

### Common Causes

```yaml
causes:
  threshold_too_sensitive:
    example: "Alert on any CPU > 80%"
    impact: "Constant alerts during normal operation"
    fix: "Use sustained thresholds (e.g., > 80% for 10 minutes)"
    
  missing_baselines:
    example: "Using static thresholds without understanding normal patterns"
    impact: "Alerts during expected fluctuations"
    fix: "Establish baselines and use dynamic thresholds"
    
  too_many_services:
    example: "Alerting on every microservice independently"
    impact: "Cascade of alerts during partial outages"
    fix: "Implement alert correlation and grouping"
    
  insufficient_filtering:
    example: "All alerts go to all team members"
    impact: "Irrelevant alerts cause desensitization"
    fix: "Route alerts based on severity and ownership"
```

### Anti-Pattern Example

```yaml
# BAD: Too many low-value alerts
alerts:
  - name: "CPU High"
    expr: "cpu_usage > 80"
    for: "0s"  # Fires immediately
    
  - name: "Memory High"
    expr: "memory_usage > 80"
    for: "0s"
    
  - name: "Disk High"
    expr: "disk_usage > 80"
    for: "0s"
    
  - name: "Network High"
    expr: "network_usage > 80"
    for: "0s"
    
  - name: "CPU Critical"
    expr: "cpu_usage > 90"
    for: "0s"
    
  - name: "Memory Critical"
    expr: "memory_usage > 90"
    for: "0s"
    
  # This generates 6 alerts for a single resource spike!
```

### Solution Pattern

```yaml
# GOOD: Consolidated, meaningful alerts
alerts:
  - name: "ResourcePressure"
    expr: |
      (cpu_usage > 85 or memory_usage > 85) and
      (cpu_usage > 85)[10m:1m]  # Sustained for 10 minutes
    for: "5m"
    labels:
      severity: warning
    annotations:
      summary: "Sustained resource pressure detected"
      description: |
        CPU: {{ $labels.cpu_usage }}%
        Memory: {{ $labels.memory_usage }}%
        Duration: 10+ minutes
        
  - name: "ResourceCritical"
    expr: |
      (cpu_usage > 95 or memory_usage > 95)
    for: "2m"
    labels:
      severity: critical
    annotations:
      summary: "Critical resource usage"
```

---

## Missing Baseline

### The Problem

Without establishing what "normal" looks like, you cannot detect anomalies or set appropriate thresholds.

### Warning Signs

```yaml
symptoms:
  - "Alerts fire during expected peak hours"
  - "Alerts fire during batch processing"
  - "Thresholds based on gut feeling"
  - "No understanding of traffic patterns"
  - "Cannot distinguish anomaly from normal variation"
```

### Baseline Types

```yaml
baseline_types:
  static_baseline:
    description: "Fixed threshold based on historical average"
    example: "Average daily requests: 10,000"
    limitation: "Doesn't account for growth or patterns"
    
  dynamic_baseline:
    description: "Threshold that adjusts based on patterns"
    example: "Alert if > 2x the same time yesterday"
    advantage: "Accounts for daily/weekly patterns"
    
  seasonal_baseline:
    description: "Threshold that accounts for seasonal patterns"
    example: "Alert if > 3x the same day last week"
    advantage: "Handles weekly/monthly cycles"
    
  adaptive_baseline:
    description: "Machine learning-based threshold"
    example: "Anomaly detection based on learned patterns"
    advantage: "Automatically adapts to changes"
```

### Missing Baseline Anti-Pattern

```yaml
# BAD: Static thresholds without baseline
alerts:
  - name: "HighLatency"
    expr: "histogram_quantile(0.99, latency) > 1000"
    # Problem: What if normal p99 is 2000ms?
    # Problem: What if normal varies by time of day?
    
  - name: "LowThroughput"
    expr: "rate(requests[5m]) < 100"
    # Problem: What if it's 3 AM and 100 is peak?
    
  - name: "HighErrorRate"
    expr: "rate(errors[5m]) / rate(requests[5m]) > 0.05"
    # Problem: What if 5% is normal for this endpoint?
```

### Solution Pattern

```yaml
# GOOD: Dynamic baseline with time-of-day awareness
recording_rules:
  - record: llm:latency:p99:7d_avg
    expr: |
      avg_over_time(
        histogram_quantile(0.99, rate(llm_latency_bucket[5m]))[7d:5m]
      )
      
  - record: llm:requests:rate:7d_avg
    expr: |
      avg_over_time(
        sum(rate(llm_requests_total[5m]))[7d:5m]
      )
      
alerts:
  - name: "HighLatency"
    expr: |
      histogram_quantile(0.99, rate(llm_latency_bucket[5m]))
      >
      2 * llm:latency:p99:7d_avg
    for: "5m"
    annotations:
      summary: "Latency 2x above baseline"
      
  - name: "LowThroughput"
    expr: |
      sum(rate(llm_requests_total[5m]))
      <
      0.5 * llm:requests:rate:7d_avg
    for: "10m"
    annotations:
      summary: "Throughput 50% below baseline"
```

---

## No Correlation

### The Problem

When alerts and metrics are not correlated, it becomes difficult to understand the root cause and relationships between issues.

### Warning Signs

```yaml
symptoms:
  - "Multiple alerts fire simultaneously"
  - "Cannot determine which alert is the root cause"
  - "Investigation requires jumping between multiple dashboards"
  - "No request-level correlation across services"
  - "Traces don't connect related spans"
```

### Correlation Anti-Pattern

```yaml
# BAD: Isolated metrics without correlation
metrics:
  - name: "api_gateway_requests"
    labels: ["method", "status"]
    # No service correlation
    
  - name: "llm_service_requests"
    labels: ["model", "status"]
    # No request ID correlation
    
  - name: "database_queries"
    labels: ["query_type", "status"]
    # No trace correlation

# When error rate spikes, you can't tell:
# - Which API endpoint caused it
# - Which downstream service failed
# - Which database query was slow
```

### Solution Pattern

```yaml
# GOOD: Correlated metrics with trace IDs
metrics:
  - name: "api_gateway_requests"
    labels: ["method", "status", "trace_id", "service"]
    # Includes trace ID for correlation
    
  - name: "llm_service_requests"
    labels: ["model", "status", "trace_id", "parent_service"]
    # Includes parent service for upstream correlation
    
  - name: "database_queries"
    labels: ["query_type", "status", "trace_id", "span_id"]
    # Full trace correlation

# Dashboard with correlated view
dashboard:
  panels:
    - title: "Request Flow"
      type: "trace"
      query: "trace_id = $trace_id"
      
    - title: "Service Dependencies"
      type: "service-map"
      query: "service = $service"
      
    - title: "Error Correlation"
      type: "table"
      query: |
        errors by service, endpoint, error_type
        where trace_id in ($affected_traces)
```

### Trace Correlation Implementation

```python
# correlation/trace_correlator.py
from opentelemetry import trace
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TraceCorrelator:
    """Correlate events across services using trace IDs"""
    
    def __init__(self):
        self.trace_store: Dict[str, list] = {}
        
    def add_event(
        self,
        trace_id: str,
        span_id: str,
        service: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Add event to trace correlation store"""
        if trace_id not in self.trace_store:
            self.trace_store[trace_id] = []
            
        event = {
            "span_id": span_id,
            "service": service,
            "event_type": event_type,
            "data": data
        }
        
        self.trace_store[trace_id].append(event)
        
    def get_trace_events(self, trace_id: str) -> list:
        """Get all events for a trace"""
        return self.trace_store.get(trace_id, [])
        
    def correlate_errors(self, trace_id: str) -> Dict[str, Any]:
        """Find root cause of errors in a trace"""
        events = self.get_trace_events(trace_id)
        
        errors = [
            e for e in events 
            if e["event_type"] == "error"
        ]
        
        if not errors:
            return {"status": "no_errors"}
            
        # Find earliest error (likely root cause)
        root_cause = min(errors, key=lambda e: e["data"].get("timestamp", 0))
        
        return {
            "status": "errors_found",
            "root_cause": root_cause,
            "all_errors": errors,
            "services_affected": list(set(e["service"] for e in errors))
        }

# Usage
correlator = TraceCorrelator()

# When API gateway receives request
correlator.add_event(
    trace_id="abc123",
    span_id="span1",
    service="api-gateway",
    event_type="request_received",
    data={"method": "POST", "endpoint": "/api/chat"}
)

# When LLM service processes
correlator.add_event(
    trace_id="abc123",
    span_id="span2",
    service="llm-service",
    event_type="llm_call",
    data={"model": "gpt-4", "tokens": 500}
)

# When error occurs
correlator.add_event(
    trace_id="abc123",
    span_id="span2",
    service="llm-service",
    event_type="error",
    data={"error": "rate_limit_exceeded", "timestamp": 1234567890}
)

# Correlate errors
result = correlator.correlate_errors("abc123")
print(result)
# {'status': 'errors_found', 'root_cause': ..., 'services_affected': ['llm-service']}
```

---

## Log Spam

### The Problem

Excessive, low-value logs that consume storage, increase costs, and make it difficult to find important information.

### Warning Signs

```yaml
symptoms:
  - "Log storage costs increasing rapidly"
  - "Difficult to find relevant logs"
  - "Log aggregation system overwhelmed"
  - "Important logs buried in noise"
  - "Query performance degraded"
```

### Log Spam Anti-Pattern

```yaml
# BAD: Excessive logging in hot paths
code_examples:
  python: |
    def process_request(request):
        logger.debug(f"Processing request: {request}")  # Logs full request object
        logger.debug(f"Request headers: {request.headers}")  # Logs all headers
        logger.debug(f"Request body: {request.body}")  # Logs full body
        
        for token in generate_tokens(request):
            logger.debug(f"Generated token: {token}")  # Logs every token!
            
        logger.debug(f"Response: {response}")  # Logs full response
        logger.info(f"Request completed")  # Duplicate completion log
        
  javascript: |
    function processRequest(req) {
      console.log('Processing request:', req);  // Logs full request
      console.log('Headers:', req.headers);  // Logs all headers
      console.log('Body:', req.body);  // Logs full body
      
      for (const chunk of response) {
        console.log('Chunk:', chunk);  // Logs every chunk!
      }
      
      console.log('Response:', response);  // Logs full response
      console.log('Request completed');  // Duplicate
    }
```

### Solution Pattern

```yaml
# GOOD: Structured, level-appropriate logging
code_examples:
  python: |
    def process_request(request):
        request_id = request.headers.get('X-Request-ID')
        
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            endpoint=request.endpoint
            # Don't log full request object
        )
        
        try:
            response = generate_response(request)
            
            logger.info(
                "request_completed",
                request_id=request_id,
                status="success",
                duration_ms=duration
                # Don't log full response
            )
            
        except RateLimitError as e:
            logger.warning(
                "rate_limit_hit",
                request_id=request_id,
                retry_after=e.retry_after
                # Structured, actionable
            )
            
        except Exception as e:
            logger.error(
                "request_failed",
                request_id=request_id,
                error_type=type(e).__name__,
                error_message=str(e)[:200]  # Truncate long messages
            )
            
  javascript: |
    function processRequest(req) {
      const requestId = req.headers['x-request-id'];
      
      logger.info('request_started', {
        requestId,
        method: req.method,
        endpoint: req.path
      });
      
      try {
        const response = generateResponse(req);
        
        logger.info('request_completed', {
          requestId,
          status: 'success',
          durationMs: duration
        });
        
      } catch (error) {
        logger.error('request_failed', {
          requestId,
          errorType: error.name,
          errorMessage: error.message.slice(0, 200)
        });
      }
    }
```

### Log Level Guidelines

```yaml
log_levels:
  DEBUG:
    when: "Development troubleshooting"
    examples:
      - "Variable values"
      - "Function entry/exit"
      - "Loop iterations"
    production: "Disabled by default"
    storage: "Temporary, 24h retention"
    
  INFO:
    when: "Normal operations"
    examples:
      - "Request started/completed"
      - "Service health checks"
      - "Configuration loaded"
    production: "Always enabled"
    storage: "30 days retention"
    
  WARN:
    when: "Potential issues"
    examples:
      - "Approaching limits"
      - "Deprecated usage"
      - "Fallback triggered"
    production: "Always enabled"
    storage: "90 days retention"
    
  ERROR:
    when: "Failures requiring attention"
    examples:
      - "Request failed"
      - "External service error"
      - "Validation error"
    production: "Always enabled"
    storage: "1 year retention"
    
  FATAL:
    when: "Critical failures"
    examples:
      - "Service crash"
      - "Data corruption"
      - "Security breach"
    production: "Always enabled"
    storage: "Permanent"
```

---

## Dashboard Overload

### The Problem

Too many dashboards, too many panels, or poorly organized dashboards that make it difficult to find relevant information.

### Warning Signs

```yaml
symptoms:
  - "Team doesn't know which dashboard to use"
  - "Dashboards take too long to load"
  - "Similar information on multiple dashboards"
  - "Dashboards are rarely updated"
  - "New team members overwhelmed"
```

### Dashboard Overload Anti-Pattern

```yaml
# BAD: Too many dashboards with overlapping information
dashboards:
  - name: "API Gateway Metrics"
    panels: 50  # Too many panels
    overlap: ["LLM Service Metrics"]
    
  - name: "LLM Service Metrics"
    panels: 45
    overlap: ["API Gateway Metrics", "Model Performance"]
    
  - name: "Model Performance"
    panels: 35
    overlap: ["LLM Service Metrics"]
    
  - name: "Production Overview"
    panels: 60
    overlap: ["Everything"]
    
  - name: "Debug Dashboard"
    panels: 100  # Unmanageable
    overlap: ["All of the above"]
```

### Solution Pattern

```yaml
# GOOD: Hierarchical dashboard structure
dashboard_hierarchy:
  level_1_executive:
    name: "Executive Overview"
    panels: 6
    refresh: "5 minutes"
    audience: "C-suite, stakeholders"
    content:
      - "Revenue Impact"
      - "User Satisfaction"
      - "System Availability"
      - "Cost vs Budget"
      
  level_2_operational:
    name: "Service Health"
    panels: 12
    refresh: "30 seconds"
    audience: "SRE, DevOps"
    content:
      - "Request Rate"
      - "Error Rate"
      - "Latency Distribution"
      - "Resource Utilization"
      
  level_3_debug:
    name: "Debug View"
    panels: 8
    refresh: "Real-time"
    audience: "Developers, SREs"
    content:
      - "Request Traces"
      - "Log Stream"
      - "Detailed Metrics"
      - "Model Performance"
      
  level_4_component:
    name: "Component Deep Dive"
    panels: 15
    refresh: "10 seconds"
    audience: "Component owners"
    content:
      - "Detailed component metrics"
      - "Internal state"
      - "Debug information"
```

### Dashboard Design Rules

```yaml
design_rules:
  panel_limit:
    max_panels_per_dashboard: 12
    recommended: 6-10
    
  layout:
    use_grid: true
    rows: 4
    columns: 3
    panel_size: "medium"
    
  organization:
    group_by: "function"
    order: "most_important_first"
    highlight: "critical_metrics"
    
  variables:
    max_variables: 5
    use_defaults: true
    group_related: true
    
  performance:
    max_query_time: "5 seconds"
    use_recording_rules: true
    cache_results: true
```

---

## No Escalation Path

### The Problem

When alerts fire but there's no clear process for who responds, how to escalate, or what actions to take.

### Warning Signs

```yaml
symptoms:
  - "Alerts acknowledged but not acted on"
  - "No clear owner for alerts"
  - "Team members unsure who to contact"
  - "Incidents drag on without resolution"
  - "No post-incident follow-up"
```

### No Escalation Anti-Pattern

```yaml
# BAD: Alert without context or escalation
alerts:
  - name: "ServiceDown"
    expr: "up == 0"
    for: "1m"
    annotations:
      summary: "Service is down"
      # Missing: Who to contact
      # Missing: What to do
      # Missing: Escalation path
      # Missing: Impact assessment
```

### Solution Pattern

```yaml
# GOOD: Complete alert with escalation
alerts:
  - name: "ServiceDown"
    expr: "up == 0"
    for: "1m"
    labels:
      severity: critical
      team: "platform"
      oncall: "platform-oncall"
    annotations:
      summary: "Service {{ $labels.job }} is down"
      description: |
        Service {{ $labels.job }} has been unreachable for 1 minute.
        
        Impact: Users unable to access the service
        
        Investigation steps:
        1. Check service status: kubectl get pods -l app={{ $labels.job }}
        2. Check recent deployments: kubectl rollout history {{ $labels.job }}
        3. Check logs: kubectl logs -l app={{ $labels.job }} --tail=100
        
        Escalation:
        - After 5 minutes: Page platform-oncall
        - After 15 minutes: Page platform-lead
        - After 30 minutes: Page engineering-manager
        
        Runbook: https://wiki/runbooks/service-down

# Escalation policy
escalation_policies:
  - name: "platform-critical"
    rules:
      - delay: 0
        targets: ["platform-oncall"]
        channels: ["pagerduty"]
        
      - delay: 5m
        targets: ["platform-lead"]
        channels: ["pagerduty", "slack"]
        
      - delay: 15m
        targets: ["engineering-manager"]
        channels: ["pagerduty", "slack", "email"]
        
      - delay: 30m
        targets: ["vp-engineering"]
        channels: ["pagerduty", "slack", "email", "phone"]
```

---

## Metric Cardinality Explosion

### The Problem

Metrics with too many unique label combinations, causing storage issues, query performance problems, and potential system crashes.

### Warning Signs

```yaml
symptoms:
  - "Prometheus memory usage increasing"
  - "Query performance degrading"
  - "Storage costs increasing rapidly"
  - "Metrics scraping timing out"
  - "Cardinality limit warnings"
```

### Cardinality Explosion Anti-Pattern

```yaml
# BAD: High-cardinality labels
metrics:
  - name: "http_requests_total"
    labels:
      - "user_id"  # Millions of users!
      - "request_id"  # Every request is unique!
      - "timestamp"  # Infinite cardinality!
      - "session_id"  # Every session is unique!
      
  - name: "llm_tokens_total"
    labels:
      - "prompt_text"  # Infinite cardinality!
      - "response_text"  # Infinite cardinality!
      - "conversation_id"  # Every conversation is unique!
```

### Solution Pattern

```yaml
# GOOD: Controlled cardinality
metrics:
  - name: "http_requests_total"
    labels:
      - "method"  # ~10 values
      - "status"  # ~10 values
      - "endpoint"  # ~100 values
      - "service"  # ~10 values
    # Total cardinality: 10 × 10 × 100 × 10 = 100,000 (manageable)
    
  - name: "llm_tokens_total"
    labels:
      - "model"  # ~10 values
      - "token_type"  # 2 values (prompt/completion)
      - "user_tier"  # 3 values (free/pro/enterprise)
    # Total cardinality: 10 × 2 × 3 = 60 (very manageable)
    
# High-cardinality data goes to logs, not metrics
logs:
  - event: "llm_request_complete"
    fields:
      - "request_id"  # High cardinality, but in logs
      - "user_id"  # High cardinality, but in logs
      - "prompt_text"  # High cardinality, but in logs
```

### Cardinality Control Implementation

```python
# metrics/cardinality_control.py
from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class CardinalityController:
    """Control metric cardinality to prevent explosion"""
    
    def __init__(self, max_label_values: int = 1000):
        self.max_label_values = max_label_values
        self.label_counts: Dict[str, Set[str]] = {}
        
    def validate_label(
        self, 
        metric_name: str, 
        label_key: str, 
        label_value: str
    ) -> str:
        """Validate and potentially sanitize label value"""
        key = f"{metric_name}:{label_key}"
        
        if key not in self.label_counts:
            self.label_counts[key] = set()
            
        if len(self.label_counts[key]) >= self.max_label_values:
            logger.warning(
                f"Cardinality limit reached for {key}, "
                f"using 'other' as value"
            )
            return "other"
            
        self.label_counts[key].add(label_value)
        return label_value

# Create cardinality-controlled metrics
controller = CardinalityController(max_label_values=1000)

SAFE_REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status', 'user_tier']  # Low cardinality
)

def record_request(model: str, status: str, user_id: str):
    """Record request with cardinality-safe labels"""
    # Don't use user_id as label - too high cardinality
    # Derive user_tier from user_id instead
    user_tier = get_user_tier(user_id)  # free, pro, enterprise
    
    SAFE_REQUEST_COUNT.labels(
        model=controller.validate_label("llm_requests_total", "model", model),
        status=status,
        user_tier=user_tier
    ).inc()
```

---

## Alert Noise

### The Problem

Alerts that fire frequently but don't require action, causing teams to ignore or dismiss them.

### Warning Signs

```yaml
symptoms:
  - "Same alert fires multiple times per day"
  - "Alerts fire during expected behavior"
  - "Team dismisses alerts without investigation"
  - "Alerts fire for known issues"
  - "No differentiation between actionable and informational"
```

### Alert Noise Anti-Pattern

```yaml
# BAD: Noisy alerts
alerts:
  - name: "HighLatency"
    expr: "histogram_quantile(0.99, latency) > 500"
    for: "0s"
    # Problem: Fires during normal variation
    
  - name: "LowThroughput"
    expr: "rate(requests[1m]) < 10"
    for: "0s"
    # Problem: Fires during low-traffic periods
    
  - name: "ErrorRate"
    expr: "rate(errors[1m]) > 0"
    for: "0s"
    # Problem: Fires on any single error
```

### Solution Pattern

```yaml
# GOOD: Noise-reduced alerts
alerts:
  - name: "HighLatency"
    expr: |
      histogram_quantile(0.99, rate(llm_latency_bucket[5m]))
      >
      2 * llm:latency:p99:baseline
    for: "10m"  # Sustained for 10 minutes
    labels:
      severity: warning
    annotations:
      summary: "P99 latency 2x above baseline for 10+ minutes"
      
  - name: "LowThroughput"
    expr: |
      sum(rate(llm_requests_total[5m]))
      <
      0.3 * llm:requests:rate:baseline
    for: "30m"  # Sustained for 30 minutes
    labels:
      severity: warning
    annotations:
      summary: "Throughput 70% below baseline for 30+ minutes"
      
  - name: "ErrorRate"
    expr: |
      sum(rate(llm_requests_total{status="error"}[5m]))
      /
      sum(rate(llm_requests_total[5m]))
      >
      0.1
    for: "5m"  # Sustained for 5 minutes
    labels:
      severity: critical
    annotations:
      summary: "Error rate above 10% for 5+ minutes"
```

---

## Missing Context

### The Problem

Alerts and logs that don't provide enough information to understand and resolve issues.

### Warning Signs

```yaml
symptoms:
  - "Team asks 'what does this alert mean?'"
  - "No way to determine impact"
  - "Cannot reproduce issues from alerts"
  - "No correlation to business metrics"
  - "Missing service ownership information"
```

### Missing Context Anti-Pattern

```yaml
# BAD: Alerts without context
alerts:
  - name: "Error"
    expr: "rate(errors[5m]) > 0"
    annotations:
      summary: "Error occurred"
      # Missing: Which service?
      # Missing: What type of error?
      # Missing: What's the impact?
      # Missing: What to do?
      
# BAD: Logs without context
logs:
  - level: "ERROR"
    message: "Request failed"
    # Missing: Which request?
    # Missing: What was the error?
    # Missing: User affected?
    # Missing: How to reproduce?
```

### Solution Pattern

```yaml
# GOOD: Alerts with complete context
alerts:
  - name: "LLMHighErrorRate"
    expr: |
      sum(rate(llm_requests_total{status="error"}[5m]))
      /
      sum(rate(llm_requests_total[5m]))
      >
      0.1
    for: "5m"
    labels:
      severity: critical
      service: "llm-gateway"
      team: "ai-platform"
      oncall: "ai-platform-oncall"
    annotations:
      summary: "LLM Gateway error rate above 10%"
      description: |
        The LLM Gateway is experiencing a high error rate.
        
        Current error rate: {{ $value | humanizePercentage }}
        Duration: 5+ minutes
        
        Impact:
        - Users unable to get LLM responses
        - Potential revenue impact
        
        Investigation steps:
        1. Check service health: kubectl get pods -l app=llm-gateway
        2. Check error logs: kubectl logs -l app=llm-gateway --tail=100 | grep ERROR
        3. Check upstream: curl http://llm-provider/health
        
        Escalation:
        - After 5 minutes: Page ai-platform-oncall
        - After 15 minutes: Page ai-platform-lead
        
        Runbook: https://wiki/runbooks/llm-high-error-rate
        
# GOOD: Logs with complete context
logs:
  - level: "ERROR"
    event: "llm_request_failed"
    message: "LLM request failed"
    metadata:
      request_id: "req_123"
      user_id: "user_456"
      model: "gpt-4-turbo"
      error_type: "rate_limit_exceeded"
      error_message: "Rate limit exceeded for organization"
      http_status: 429
      retry_after: 60
      endpoint: "/api/v1/chat"
      trace_id: "abc123"
```

---

## Anti-Pattern Solutions Summary

### Quick Reference

| Anti-Pattern | Solution | Priority |
|--------------|----------|----------|
| Alert Fatigue | Consolidate, prioritize, tune thresholds | P0 |
| Missing Baseline | Establish baselines, use dynamic thresholds | P0 |
| No Correlation | Implement distributed tracing, correlate events | P1 |
| Log Spam | Use appropriate log levels, structured logging | P1 |
| Dashboard Overload | Hierarchical dashboards, limit panels | P2 |
| No Escalation Path | Document escalation, create runbooks | P0 |
| Cardinality Explosion | Control labels, use recording rules | P1 |
| Alert Noise | Sustained thresholds, baseline comparison | P1 |
| Missing Context | Enrich alerts and logs with metadata | P0 |

### Implementation Checklist

```yaml
anti_pattern_prevention:
  alerting:
    - [ ] Establish baselines for all metrics
    - [ ] Use sustained thresholds (not instant)
    - [ ] Implement alert correlation
    - [ ] Define escalation paths
    - [ ] Create runbooks for common alerts
    - [ ] Review and tune alerts monthly
    
  logging:
    - [ ] Implement structured logging
    - [ ] Define log levels per component
    - [ ] Set retention policies
    - [ ] Monitor log volume
    - [ ] Redact sensitive data
    
  dashboards:
    - [ ] Create hierarchical dashboard structure
    - [ ] Limit panels per dashboard (max 12)
    - [ ] Group related metrics
    - [ ] Use variables for filtering
    - [ ] Document dashboard purpose
    
  metrics:
    - [ ] Control label cardinality
    - [ ] Use recording rules for complex queries
    - [ ] Monitor metric count and cardinality
    - [ ] Set alerts for cardinality explosion
    - [ ] Review metrics quarterly
```

---

## References

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- Prometheus Best Practices: https://prometheus.io/docs/practices/
- Grafana Anti-Patterns: https://grafana.com/docs/grafana/latest/

---

*Last Updated: January 2025*
*Version: 1.0.0*
