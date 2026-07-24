# Monitoring Fundamentals for AI/LLM Systems

## Core Concepts and Observability Pillars

---

## Table of Contents

1. [Introduction](#introduction)
2. [Observability Pillars](#observability-pillars)
3. [Monitoring vs Observability](#monitoring-vs-observability)
4. [SLIs, SLOs, and SLAs](#slis-slos-and-slas)
5. [Alerting Strategies](#alerting-strategies)
6. [Dashboard Design](#dashboard-design)
7. [LLM-Specific Monitoring](#llm-specific-monitoring)
8. [Implementation Patterns](#implementation-patterns)
9. [Examples and Configurations](#examples-and-configurations)
10. [Checklists](#checklists)

---

## Introduction

Monitoring AI and LLM systems requires a fundamentally different approach than traditional software monitoring. These systems exhibit non-deterministic behavior, have complex resource consumption patterns, and can fail in ways that are difficult to detect without specialized observability.

### Why LLM Monitoring Matters

- **Cost Control**: API calls and compute resources can escalate rapidly
- **Quality Assurance**: Model outputs degrade silently without monitoring
- **Latency Management**: Response times directly impact user experience
- **Security**: Prompt injection and abuse require real-time detection
- **Compliance**: Audit trails for regulated industries

### Monitoring Maturity Levels

```
Level 0: No monitoring - reactive firefighting
Level 1: Basic metrics - uptime, response time, error rate
Level 2: Structured logging - searchability, correlation
Level 3: Distributed tracing - request flow visualization
Level 4: Proactive alerting - predictive, anomaly-based
Level 5: AIOps - self-healing, auto-scaling, optimization
```

---

## Observability Pillars

### The Three Pillars

#### 1. Metrics

Quantitative measurements over time. For LLM systems:

```yaml
# Core metric categories for LLM systems
categories:
  request_metrics:
    - requests_total
    - request_duration_seconds
    - request_size_bytes
    - response_size_bytes
    
  model_metrics:
    - model_inference_latency_seconds
    - model_tokens_per_second
    - model_memory_usage_bytes
    - model_gpu_utilization_percent
    
  quality_metrics:
    - response_relevance_score
    - hallucination_detection_rate
    - user_satisfaction_score
    - task_completion_rate
    
  cost_metrics:
    - api_cost_dollars_total
    - tokens_consumed_total
    - compute_cost_dollars_total
    - cost_per_request_dollars
    
  system_metrics:
    - cpu_usage_percent
    - memory_usage_bytes
    - disk_io_bytes
    - network_io_bytes
```

**Metric Types**:

```yaml
metric_types:
  counter:
    description: "Monotonically increasing value"
    examples:
      - requests_total
      - errors_total
      - tokens_consumed_total
    use_case: "Rate calculations, cumulative totals"
    
  gauge:
    description: "Value that can go up or down"
    examples:
      - current_connections
      - queue_depth
      - memory_usage_percent
    use_case: "Current state measurements"
    
  histogram:
    description: "Distribution of values over buckets"
    examples:
      - request_duration_seconds
      - response_size_bytes
      - token_count_distribution
    use_case: "Latency percentiles, size distributions"
    
  summary:
    description: "Similar to histogram but computed client-side"
    examples:
      - api_response_time
      - processing_duration
    use_case: "When client-side computation is preferred"
```

#### 2. Logs

Unstructured or structured event records:

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "INFO",
  "service": "llm-gateway",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user_123",
  "request_id": "req_456",
  "event": "llm_request_complete",
  "model": "gpt-4-turbo",
  "prompt_tokens": 150,
  "completion_tokens": 450,
  "latency_ms": 2345,
  "cost_usd": 0.045,
  "metadata": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9
  }
}
```

**Log Levels for LLM Systems**:

```yaml
log_levels:
  DEBUG:
    description: "Detailed diagnostic information"
    examples:
      - Token-by-token generation
      - Prompt template rendering
      - Cache lookups
    retention: "24 hours"
    
  INFO:
    description: "Normal operation events"
    examples:
      - Request completed
      - Model loaded
      - Cache hit/miss
    retention: "30 days"
    
  WARN:
    description: "Potential issues"
    examples:
      - High latency detected
      - Rate limit approaching
      - Model fallback triggered
    retention: "90 days"
    
  ERROR:
    description: "Failures requiring attention"
    examples:
      - API call failed
      - Model timeout
      - Authentication error
    retention: "1 year"
    
  FATAL:
    description: "Critical system failures"
    examples:
      - System crash
      - Data corruption
      - Security breach
    retention: "Permanent"
```

#### 3. Traces

Request flow through distributed systems:

```yaml
trace_structure:
  trace_id: "unique_identifier_for_entire_request"
  spans:
    - span_id: "span_1"
      operation: "http_request"
      service: "api_gateway"
      duration_ms: 2500
      status: "OK"
      
    - span_id: "span_2"
      parent_span_id: "span_1"
      operation: "llm_inference"
      service: "model_service"
      duration_ms: 2300
      status: "OK"
      attributes:
        model: "gpt-4-turbo"
        tokens_generated: 450
        
    - span_id: "span_3"
      parent_span_id: "span_2"
      operation: "token_generation"
      service: "gpu_worker"
      duration_ms: 1800
      status: "OK"
```

---

## Monitoring vs Observability

### Key Differences

```yaml
monitoring:
  definition: "Collecting and analyzing predefined metrics"
  focus: "What is broken?"
  approach: "Reactive - detect known failure modes"
  examples:
    - CPU usage alerts
    - Error rate thresholds
    - Uptime checks
    
observability:
  definition: "Understanding system state from external outputs"
  focus: "Why is it broken?"
  approach: "Proactive - explore unknown failure modes"
  examples:
    - Distributed tracing
    - Structured logging
    - High-cardinality metrics
```

### When to Use Each

| Scenario | Monitoring | Observability |
|----------|------------|---------------|
| Known failure modes | Best | Good |
| Unknown failures | Limited | Best |
| Simple systems | Best | Overkill |
| Distributed systems | Good | Best |
| Real-time debugging | Limited | Best |
| Historical analysis | Good | Good |

---

## SLIs, SLOs, and SLAs

### Service Level Indicators (SLIs)

```yaml
llm_slis:
  availability:
    description: "Percentage of successful requests"
    formula: "successful_requests / total_requests"
    measurement:
      method: "synthetic_probes"
      interval: "1 minute"
      window: "5 minutes"
      
  latency:
    description: "Response time distribution"
    formula: "percentile(95, request_duration)"
    measurement:
      method: "real_user_monitoring"
      histogram_buckets: [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
      
  quality:
    description: "Model output relevance"
    formula: "relevant_responses / total_responses"
    measurement:
      method: "automated_scoring"
      scoring_model: "quality_classifier"
      
  throughput:
    description: "Requests handled per second"
    formula: "total_requests / time_window"
    measurement:
      method: "counter_derivation"
      resolution: "1 second"
```

### Service Level Objectives (SLOs)

```yaml
llm_slos:
  latency:
    target: "99th percentile < 3 seconds"
    measurement_window: "30 days"
    error_budget: "0.1% of requests may exceed 3s"
    
  availability:
    target: "99.9% uptime"
    measurement_window: "30 days"
    error_budget: "43.2 minutes of downtime per month"
    
  quality:
    target: "95% relevance score"
    measurement_window: "7 days"
    error_budget: "5% may score below threshold"
    
  throughput:
    target: "1000 requests/second sustained"
    measurement_window: "5 minutes"
    error_budget: "Can drop to 500 rps for 1 minute"
```

### Service Level Agreements (SLAs)

```yaml
llm_slas:
  availability:
    target: "99.95% uptime"
    penalty: "10% credit per 0.1% below target"
    measurement: "monthly"
    exclusions:
      - "Scheduled maintenance windows"
      - "Force majeure events"
      
  latency:
    target: "95th percentile < 5 seconds"
    penalty: "5% credit per 100ms above target"
    measurement: "daily"
    
  support:
    response_time:
      critical: "1 hour"
      high: "4 hours"
      medium: "24 hours"
      low: "72 hours"
```

---

## Alerting Strategies

### Alert Taxonomy

```yaml
alert_severity:
  P0_Critical:
    description: "Complete service outage or data loss"
    response_time: "< 5 minutes"
    notification: "PagerDuty + Phone + Slack"
    escalation: "Immediate to on-call + management"
    examples:
      - "LLM API returning 100% errors"
      - "Complete model service failure"
      - "Data breach detected"
      
  P1_High:
    description: "Major feature degraded, no workaround"
    response_time: "< 15 minutes"
    notification: "PagerDuty + Slack"
    escalation: "After 15 minutes to team lead"
    examples:
      - "Response latency > 10s for 5+ minutes"
      - "Error rate > 10% for 3+ minutes"
      - "Model quality dropped significantly"
      
  P2_Medium:
    description: "Minor feature impaired, workaround exists"
    response_time: "< 1 hour"
    notification: "Slack"
    escalation: "After 2 hours to team lead"
    examples:
      - "Cache hit rate dropped below 50%"
      - "Rate limit warnings frequent"
      - "Non-critical model fallback triggered"
      
  P3_Low:
    description: "Cosmetic or minor issue"
    response_time: "< 4 hours"
    notification: "Slack (low priority channel)"
    escalation: "After 24 hours to team lead"
    examples:
      - "Minor latency increase"
      - "Documentation gaps"
      - "Non-urgent optimization opportunities"
```

### Alert Rules (Prometheus)

```yaml
groups:
  - name: llm_critical_alerts
    rules:
      - alert: LLMServiceDown
        expr: up{job="llm-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "LLM service is down"
          description: "LLM service has been unreachable for more than 1 minute"
          
      - alert: HighErrorRate
        expr: |
          rate(llm_requests_total{status="error"}[5m]) / 
          rate(llm_requests_total[5m]) > 0.1
        for: 3m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
          
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, 
            rate(llm_request_duration_seconds_bucket[5m])
          ) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency"
          description: "p99 latency is {{ $value }}s"
          
      - alert: CostBudgetExceeded
        expr: |
          increase(llm_cost_dollars_total[24h]) > 1000
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Daily cost budget exceeded"
          description: "Spent ${{ $value }} in last 24h"
```

### Alert Routing (Alertmanager)

```yaml
global:
  resolve_timeout: 5m
  
route:
  receiver: 'slack-notifications'
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
      
    - match:
        severity: warning
      receiver: 'slack-warnings'
      
    - match:
        severity: info
      receiver: 'slack-info'
      
receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
        
  - name: 'slack-notifications'
    slack_configs:
      - api_url: '<slack-webhook-url>'
        channel: '#llm-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'
        
  - name: 'slack-warnings'
    slack_configs:
      - api_url: '<slack-webhook-url>'
        channel: '#llm-warnings'
        
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

---

## Dashboard Design

### Dashboard Hierarchy

```yaml
dashboard_levels:
  executive:
    purpose: "Business health overview"
    audience: "C-suite, stakeholders"
    refresh_rate: "5 minutes"
    panels:
      - "Total Requests (24h)"
      - "Cost vs Budget"
      - "Availability SLA"
      - "User Satisfaction"
      
  operational:
    purpose: "System health monitoring"
    audience: "SRE, DevOps"
    refresh_rate: "30 seconds"
    panels:
      - "Request Rate by Model"
      - "Latency Distribution"
      - "Error Rate Trend"
      - "Resource Utilization"
      
  debug:
    purpose: "Troubleshooting and investigation"
    audience: "Developers, SREs"
    refresh_rate: "Real-time"
    panels:
      - "Request Traces"
      - "Log Stream"
      - "Detailed Metrics"
      - "Model Performance"
```

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "LLM Service Overview",
    "tags": ["llm", "ai", "production"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(llm_requests_total[5m])) by (model)",
            "legendFormat": "{{model}}"
          }
        ],
        "yaxes": [
          {"format": "reqps"},
          {"format": "short"}
        ]
      },
      {
        "title": "Latency Distribution",
        "type": "heatmap",
        "targets": [
          {
            "expr": "sum(rate(llm_request_duration_seconds_bucket[5m])) by (le)",
            "legendFormat": "{{le}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(llm_requests_total{status=\"error\"}[5m])) / sum(rate(llm_requests_total[5m]))",
            "legendFormat": "Error Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 0.05},
                {"color": "red", "value": 0.1}
              ]
            }
          }
        }
      }
    ],
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

---

## LLM-Specific Monitoring

### Model Performance Metrics

```yaml
model_metrics:
  generation_quality:
    - metric: "perplexity_score"
      description: "Language model confidence"
      target: "< 20"
      
    - metric: "bleu_score"
      description: "Translation quality"
      target: "> 0.7"
      
    - metric: "semantic_similarity"
      description: "Response relevance"
      target: "> 0.8"
      
  generation_speed:
    - metric: "tokens_per_second"
      description: "Generation throughput"
      target: "> 50"
      
    - metric: "time_to_first_token"
      description: "Initial response latency"
      target: "< 500ms"
      
  resource_efficiency:
    - metric: "gpu_utilization"
      description: "GPU compute usage"
      target: "70-90%"
      
    - metric: "memory_usage"
      description: "GPU memory consumption"
      target: "< 85%"
      
    - metric: "batch_efficiency"
      description: "Effective batch size utilization"
      target: "> 80%"
```

### Prompt and Response Monitoring

```yaml
content_monitoring:
  prompt_patterns:
    - metric: "prompt_length_distribution"
      description: "Track input token counts"
      buckets: [100, 500, 1000, 2000, 4000, 8000]
      
    - metric: "prompt_complexity_score"
      description: "Estimated task complexity"
      source: "classifier_model"
      
  response_patterns:
    - metric: "response_length_distribution"
      description: "Track output token counts"
      buckets: [100, 500, 1000, 2000, 4000]
      
    - metric: "response_quality_score"
      description: "Automated quality assessment"
      source: "quality_scorer"
      
    - metric: "hallucination_rate"
      description: "Detected factual inaccuracies"
      source: "fact_checker"
      
  safety_patterns:
    - metric: "content_filtered_count"
      description: "Responses blocked by safety filters"
      severity: "critical"
      
    - metric: "toxicity_score"
      description: "Detected harmful content"
      threshold: "> 0.8 triggers alert"
```

---

## Implementation Patterns

### Python Monitoring Setup

```python
# monitoring/setup.py
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge, Summary
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
import structlog
import time
from functools import wraps

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.BoundLogger,
    cache_logger_on_first_use=True,
)

# Define metrics
REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'llm_request_duration_seconds',
    'LLM request latency',
    ['model', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0]
)

TOKEN_COUNT = Counter(
    'llm_tokens_total',
    'Total tokens processed',
    ['model', 'token_type']  # token_type: prompt/completion
)

COST_COUNTER = Counter(
    'llm_cost_dollars_total',
    'Total API cost in dollars',
    ['model']
)

ACTIVE_REQUESTS = Gauge(
    'llm_active_requests',
    'Currently processing requests',
    ['model']
)

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("llm-service")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

def monitor_request(func):
    """Decorator to monitor LLM requests"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        with tracer.start_as_current_span("llm_request") as span:
            model = kwargs.get('model', 'unknown')
            ACTIVE_REQUESTS.labels(model=model).inc()
            
            try:
                result = await func(*args, **kwargs)
                
                REQUEST_COUNT.labels(
                    model=model,
                    status='success',
                    endpoint=func.__name__
                ).inc()
                
                span.set_status(trace.StatusCode.OK)
                return result
                
            except Exception as e:
                REQUEST_COUNT.labels(
                    model=model,
                    status='error',
                    endpoint=func.__name__
                ).inc()
                
                span.set_status(trace.StatusCode.ERROR)
                span.record_exception(e)
                raise
                
            finally:
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(
                    model=model,
                    endpoint=func.__name__
                ).observe(duration)
                ACTIVE_REQUESTS.labels(model=model).dec()
                
                structlog.get_logger().info(
                    "llm_request_complete",
                    model=model,
                    duration=duration,
                    status='completed'
                )
    
    return wrapper
```

### Node.js Monitoring Setup

```javascript
// monitoring/metrics.js
const promClient = require('prom-client');

// Collect default metrics
promClient.collectDefaultMetrics({ prefix: 'llm_' });

// Define custom metrics
const requestCounter = new promClient.Counter({
  name: 'llm_requests_total',
  help: 'Total LLM requests',
  labelNames: ['model', 'status', 'endpoint']
});

const requestDuration = new promClient.Histogram({
  name: 'llm_request_duration_seconds',
  help: 'LLM request latency',
  labelNames: ['model', 'endpoint'],
  buckets: [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0]
});

const tokenCounter = new promClient.Counter({
  name: 'llm_tokens_total',
  help: 'Total tokens processed',
  labelNames: ['model', 'token_type']
});

const activeRequests = new promClient.Gauge({
  name: 'llm_active_requests',
  help: 'Currently processing requests',
  labelNames: ['model']
});

// Middleware for monitoring
function monitoringMiddleware(req, res, next) {
  const start = Date.now();
  const model = req.body?.model || 'unknown';
  
  activeRequests.inc({ model });
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const status = res.statusCode < 400 ? 'success' : 'error';
    
    requestCounter.inc({ model, status, endpoint: req.path });
    requestDuration.observe({ model, endpoint: req.path }, duration);
    activeRequests.dec({ model });
  });
  
  next();
}

// Trace context propagation
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');

const provider = new NodeTracerProvider();
const exporter = new JaegerExporter({
  serviceName: 'llm-service',
  host: 'localhost',
  port: 6831
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

module.exports = {
  requestCounter,
  requestDuration,
  tokenCounter,
  activeRequests,
  monitoringMiddleware
};
```

---

## Examples and Configurations

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  
scrape_configs:
  - job_name: 'llm-service'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    
  - job_name: 'model-servers'
    static_configs:
      - targets: 
          - 'model-server-1:8001'
          - 'model-server-2:8001'
          - 'model-server-3:8001'
          
  - job_name: 'redis-cache'
    static_configs:
      - targets: ['redis:6379']
      
  - job_name: 'postgres-db'
    static_configs:
      - targets: ['postgres:5432']
```

### Docker Compose for Monitoring Stack

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
      
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "6831:6831/udp"  # Agent
      - "14268:14268"  # Collector
      
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
      
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
      
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
      
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

volumes:
  prometheus_data:
  grafana_data:
```

---

## Checklists

### Pre-Production Monitoring Checklist

- [ ] **Metrics Collection**
  - [ ] All services expose Prometheus metrics
  - [ ] Custom business metrics defined
  - [ ] Histogram buckets appropriate for expected latencies
  - [ ] Labels are low-cardinality
  - [ ] Metric naming follows conventions

- [ ] **Logging**
  - [ ] Structured logging implemented
  - [ ] Log levels configured appropriately
  - [ ] Sensitive data not logged
  - [ ] Log aggregation configured
  - [ ] Retention policies set

- [ ] **Tracing**
  - [ ] OpenTelemetry SDK integrated
  - [ ] Trace context propagation configured
  - [ ] Sampling rate appropriate
  - [ ] Span attributes defined
  - [ ] Exporter configured

- [ ] **Alerting**
  - [ ] Critical alerts defined
  - [ ] Alert routing configured
  - [ ] Escalation policies in place
  - [ ] Runbooks documented
  - [ ] Alert fatigue analyzed

- [ ] **Dashboards**
  - [ ] Executive dashboard created
  - [ ] Operational dashboards created
  - [ ] Debug dashboards created
  - [ ] Dashboard templates saved
  - [ ] Access controls configured

---

## References

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- OpenTelemetry Documentation: https://opentelemetry.io/docs/
- Prometheus Best Practices: https://prometheus.io/docs/practices/
- Grafana Dashboard Design: https://grafana.com/docs/grafana/latest/dashboards/

---

*Last Updated: January 2025*
*Version: 1.0.0*
