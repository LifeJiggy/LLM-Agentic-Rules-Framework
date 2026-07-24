# Monitoring Examples for AI/LLM Systems

## Practical Configurations and Implementations

---

## Table of Contents

1. [Prometheus/Grafana Setup](#prometheusgrafana-setup)
2. [Distributed Tracing with Jaeger](#distributed-tracing-with-jaeger)
3. [Structured Logging with ELK](#structured-logging-with-elk)
4. [Alerting with PagerDuty](#alerting-with-pagerduty)
5. [LLM-Specific Monitoring](#llm-specific-monitoring)
6. [Cost Monitoring](#cost-monitoring)
7. [Model Performance Monitoring](#model-performance-monitoring)
8. [Security Monitoring](#security-monitoring)
9. [Complete Monitoring Stack](#complete-monitoring-stack)
10. [Production Examples](#production-examples)

---

## Prometheus/Grafana Setup

### Prometheus Configuration

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'
    
# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
          
# Rule files
rule_files:
  - 'rules/*.yml'
  
# Scrape configurations
scrape_configs:
  # LLM Service
  - job_name: 'llm-service'
    static_configs:
      - targets: ['llm-service:8080']
        labels:
          service: 'llm-gateway'
          environment: 'production'
    metrics_path: '/metrics'
    scrape_interval: 10s
    
  # Model Servers
  - job_name: 'model-servers'
    static_configs:
      - targets:
          - 'model-server-1:8081'
          - 'model-server-2:8081'
          - 'model-server-3:8081'
        labels:
          service: 'model-server'
    metrics_path: '/metrics'
    scrape_interval: 10s
    
  # Redis Cache
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
        labels:
          service: 'cache'
    metrics_path: '/metrics'
    
  # PostgreSQL
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
        labels:
          service: 'database'
    metrics_path: '/metrics'
    
  # Kubernetes API
  - job_name: 'kubernetes-nodes'
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
```

### Recording Rules

```yaml
# prometheus/rules/recording_rules.yml
groups:
  - name: llm_recording_rules
    interval: 10s
    rules:
      # Request rate per second
      - record: llm:requests:rate5m
        expr: sum(rate(llm_requests_total[5m])) by (model, status)
        
      # Error rate
      - record: llm:errors:rate5m
        expr: |
          sum(rate(llm_requests_total{status="error"}[5m])) by (model)
          /
          sum(rate(llm_requests_total[5m])) by (model)
          
      # Latency percentiles
      - record: llm:latency:p50:5m
        expr: histogram_quantile(0.5, rate(llm_latency_seconds_bucket[5m])) by (model)
        
      - record: llm:latency:p95:5m
        expr: histogram_quantile(0.95, rate(llm_latency_seconds_bucket[5m])) by (model)
        
      - record: llm:latency:p99:5m
        expr: histogram_quantile(0.99, rate(llm_latency_seconds_bucket[5m])) by (model)
        
      # Cost per minute
      - record: llm:cost:per_minute
        expr: rate(llm_cost_dollars_total[5m]) * 60
        
      # Tokens per second
      - record: llm:tokens:rate5m
        expr: rate(llm_tokens_total[5m]) by (model, token_type)
```

### Alert Rules

```yaml
# prometheus/rules/alert_rules.yml
groups:
  - name: llm_alerts
    rules:
      # Service Down
      - alert: LLMServiceDown
        expr: up{job="llm-service"} == 0
        for: 1m
        labels:
          severity: critical
          team: ai-platform
        annotations:
          summary: "LLM service is down"
          description: "LLM service has been unreachable for more than 1 minute"
          runbook: "https://wiki/runbooks/llm-service-down"
          
      # High Error Rate
      - alert: LLMHighErrorRate
        expr: |
          llm:errors:rate5m > 0.1
        for: 5m
        labels:
          severity: critical
          team: ai-platform
        annotations:
          summary: "LLM error rate above 10%"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "https://wiki/runbooks/llm-high-error-rate"
          
      # High Latency
      - alert: LLMHighLatency
        expr: |
          llm:latency:p99:5m > 5
        for: 10m
        labels:
          severity: warning
          team: ai-platform
        annotations:
          summary: "LLM p99 latency above 5s"
          description: "p99 latency is {{ $value }}s"
          runbook: "https://wiki/runbooks/llm-high-latency"
          
      # Cost Budget Exceeded
      - alert: LLMCostBudgetExceeded
        expr: |
          increase(llm_cost_dollars_total[24h]) > 1000
        for: 1h
        labels:
          severity: warning
          team: finance
        annotations:
          summary: "Daily cost budget exceeded"
          description: "Spent ${{ $value }} in last 24h"
          runbook: "https://wiki/runbooks/llm-cost-budget"
          
      # Rate Limit Hit
      - alert: LLMRateLimitHit
        expr: |
          rate(llm_rate_limit_hits_total[5m]) > 0
        for: 1m
        labels:
          severity: warning
          team: ai-platform
        annotations:
          summary: "Rate limit being hit"
          description: "Rate limit hits detected"
          runbook: "https://wiki/runbooks/llm-rate-limit"
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "id": null,
    "title": "LLM Service Overview",
    "tags": ["llm", "ai", "production"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(llm_requests_total[5m])) by (model)",
            "legendFormat": "{{model}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "custom": {
              "drawStyle": "line",
              "lineWidth": 2,
              "fillOpacity": 10
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "llm:errors:rate5m",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 0.05},
                {"color": "red", "value": 0.1}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "P99 Latency",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0},
        "targets": [
          {
            "expr": "llm:latency:p99:5m",
            "legendFormat": "{{model}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 2},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      },
      {
        "id": 4,
        "title": "Latency Distribution",
        "type": "heatmap",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "sum(rate(llm_latency_seconds_bucket[5m])) by (le)",
            "legendFormat": "{{le}}",
            "format": "heatmap",
            "refId": "A"
          }
        ]
      },
      {
        "id": 5,
        "title": "Cost per Hour",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "rate(llm_cost_dollars_total[5m]) * 3600",
            "legendFormat": "{{model}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyUSD"
          }
        }
      },
      {
        "id": 6,
        "title": "Token Usage",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "rate(llm_tokens_total[5m]) by (model, token_type)",
            "legendFormat": "{{model}} - {{token_type}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short"
          }
        }
      },
      {
        "id": 7,
        "title": "Active Requests",
        "type": "gauge",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
        "targets": [
          {
            "expr": "llm_active_requests",
            "legendFormat": "{{model}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 50},
                {"color": "red", "value": 100}
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
    "refresh": "30s",
    "templating": {
      "list": [
        {
          "name": "model",
          "type": "query",
          "query": "label_values(llm_requests_total, model)",
          "refresh": 2,
          "multi": true,
          "includeAll": true
        }
      ]
    }
  }
}
```

---

## Distributed Tracing with Jaeger

### Jaeger Configuration

```yaml
# jaeger/jaeger.yml
service:
  name: llm-service
  
collector:
  endpoints:
    - host: jaeger-collector
      port: 14267
      protocol: http
    - host: jaeger-collector
      port: 14250
      protocol: grpc
      
agent:
  host: jaeger-agent
  port: 6831
  protocol: udp
  
sampling:
  default_strategy:
    type: probabilistic
    param: 0.1  # Sample 10% of traces
    
  service_strategies:
    - service: llm-service
      type: probabilistic
      param: 0.5  # Sample 50% for LLM service
      
    - service: model-server
      type: probabilistic
      param: 0.2  # Sample 20% for model server
      
  per_operation_strategies:
    - operation: POST /api/v1/chat
      type: probabilistic
      param: 1.0  # Sample 100% of chat requests
      
    - operation: POST /api/v1/completions
      type: probabilistic
      param: 0.5  # Sample 50% of completions
```

### OpenTelemetry Configuration

```yaml
# otel/otel-collector.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
        
  prometheus:
    config:
      scrape_configs:
        - job_name: 'otel-collector'
          static_configs:
            - targets: ['localhost:8888']
            
processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
    
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128
    
  attributes:
    actions:
      - key: llm.model
        action: upsert
      - key: llm.tokens.prompt
        action: upsert
      - key: llm.tokens.completion
        action: upsert
      - key: llm.cost.usd
        action: upsert
        
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    expected_new_traces_per_sec: 1000
    policies:
      - name: error-policy
        type: status_code
        status_code: {status_codes: [ERROR]}
        
      - name: latency-policy
        type: latency
        latency: {threshold_ms: 1000}
        
      - name: probabilistic-policy
        type: probabilistic
        probabilistic: {sampling_percentage: 10}
        
exporters:
  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: false
      
  logging:
    loglevel: debug
    
  prometheus:
    endpoint: 0.0.0.0:8889
    
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, tail_sampling, batch]
      exporters: [jaeger, logging]
      
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
```

### Python Jaeger Integration

```python
# tracing/jaeger_integration.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
import os

def setup_tracing():
    """Configure OpenTelemetry with Jaeger"""
    
    resource = Resource.create({
        SERVICE_NAME: os.getenv("SERVICE_NAME", "llm-service"),
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        "service.version": os.getenv("SERVICE_VERSION", "1.0.0")
    })
    
    provider = TracerProvider(resource=resource)
    
    # Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
        agent_port=int(os.getenv("JAEGER_PORT", "6831")),
    )
    
    # OTLP exporter for collector
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_ENDPOINT", "localhost:4317"),
        insecure=True
    )
    
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    
    trace.set_tracer_provider(provider)
    
    # Auto-instrument
    FastAPIInstrumentor.instrument()
    HTTPXClientInstrumentor.instrument()
    OpenAIInstrumentor.instrument()
    
    return trace.get_tracer(os.getenv("SERVICE_NAME", "llm-service"))

# Custom span for LLM operations
def create_llm_span(model, operation="llm_request"):
    """Create a span for LLM operation"""
    tracer = trace.get_tracer("llm-service")
    
    span = tracer.start_span(
        operation,
        attributes={
            "llm.model": model,
            "llm.provider": "openai"
        }
    )
    
    return span

# Example usage
tracer = setup_tracing()

def process_llm_request(prompt, model="gpt-4"):
    with tracer.start_as_current_span("llm_request") as span:
        span.set_attribute("llm.prompt.length", len(prompt))
        
        # Call LLM
        response = call_llm(prompt, model)
        
        span.set_attribute("llm.response.length", len(response))
        span.set_attribute("llm.tokens.used", count_tokens(response))
        
        return response
```

---

## Structured Logging with ELK

### Elasticsearch Configuration

```yaml
# elasticsearch/elasticsearch.yml
cluster.name: llm-logs
network.host: 0.0.0.0
discovery.type: single-node

xpack.security.enabled: false
xpack.monitoring.collection.enabled: true

# Index lifecycle management
xpack.ilm.enabled: true
```

### Logstash Pipeline

```ruby
# logstash/pipeline/llm-logs.conf
input {
  beats {
    port => 5044
  }
  
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["llm-logs"]
    codec => json
  }
}

filter {
  # Parse timestamp
  date {
    match => ["timestamp", "ISO8601"]
    target => "@timestamp"
  }
  
  # Parse JSON fields
  json {
    source => "message"
    target => "parsed"
  }
  
  # Extract fields
  if [parsed][request_id] {
    mutate {
      add_field => { "request_id" => "%{[parsed][request_id]}" }
    }
  }
  
  if [parsed][model] {
    mutate {
      add_field => { "model" => "%{[parsed][model]}" }
    }
  }
  
  # Add geoip if needed
  geoip {
    source => "client_ip"
    target => "geoip"
  }
  
  # Remove sensitive fields
  mutate {
    remove_field => ["password", "secret", "token"]
  }
  
  # Add metadata
  mutate {
    add_field => {
      "environment" => "%{[env][ENVIRONMENT]}"
      "service" => "%{[env][SERVICE_NAME]}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "llm-logs-%{+YYYY.MM.dd}"
    manage_template => true
    template_name => "llm-logs"
    template_overwrite => true
  }
  
  # Debug output
  stdout {
    codec => rubydebug
  }
}
```

### Kibana Configuration

```yaml
# kibana/kibana.yml
server.name: kibana
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://elasticsearch:9200"]

# Index patterns
# Create via UI or API:
# - llm-logs-*
# - llm-metrics-*
```

### Python Structured Logger

```python
# logging/elk_logger.py
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from contextvars import ContextVar
import uuid

# Context variables
request_id_var: ContextVar[str] = ContextVar('request_id', default='')
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')

class ELKFormatter(logging.Formatter):
    """Formatter optimized for ELK stack"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": os.getenv("SERVICE_NAME", "llm-service"),
            "environment": os.getenv("ENVIRONMENT", "production"),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add context
        request_id = request_id_var.get('')
        if request_id:
            log_entry["request_id"] = request_id
            
        trace_id = trace_id_var.get('')
        if trace_id:
            log_entry["trace_id"] = trace_id
            
        # Add extra fields
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in logging.LogRecord('','','','','','','','').__dict__
            and k not in ['message', 'msg', 'args', 'exc_info', 'exc_text']
        }
        if extra_fields:
            log_entry["metadata"] = extra_fields
            
        return json.dumps(log_entry)

class LLMELKLogger:
    """Logger for ELK stack"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ELKFormatter())
        self.logger.addHandler(handler)
        
    def log_llm_request(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        duration_ms: float,
        cost_usd: float,
        status: str
    ):
        """Log LLM request with ELK-optimized format"""
        self.logger.info(
            "llm_request_complete",
            extra={
                "event": "llm_request",
                "model": model,
                "tokens": {
                    "prompt": prompt_tokens,
                    "completion": completion_tokens,
                    "total": prompt_tokens + completion_tokens
                },
                "duration_ms": duration_ms,
                "cost_usd": cost_usd,
                "status": status
            }
        )

# Usage
logger = LLMELKLogger("llm-service")
logger.log_llm_request(
    model="gpt-4-turbo",
    prompt_tokens=150,
    completion_tokens=450,
    duration_ms=2345,
    cost_usd=0.045,
    status="success"
)
```

---

## Alerting with PagerDuty

### PagerDuty Configuration

```yaml
# pagerduty/pd.yml
services:
  - name: "LLM Production"
    id: "PXXXXXX"
    escalation_policy:
      name: "AI Platform On-Call"
      id: "PXXXXXX"
      
integrations:
  - type: "generic_events_v1"
    name: "Alertmanager"
    integration_key: "YOUR_INTEGRATION_KEY"
    
escalation_policies:
  - name: "AI Platform On-Call"
    escalation_rules:
      - escalation_delay: 0
        targets:
          - type: "user"
            id: "PXXXXXX"
            
      - escalation_delay: 300  # 5 minutes
        targets:
          - type: "user"
            id: "PXXXXXX"
            
      - escalation_delay: 900  # 15 minutes
        targets:
          - type: "user"
            id: "PXXXXXX"
          - type: "schedule"
            id: "PXXXXXX"
```

### Alertmanager PagerDuty Integration

```yaml
# alertmanager/pagerduty.yml
global:
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'
  
route:
  receiver: 'pagerduty-critical'
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      
    - match:
        severity: warning
      receiver: 'slack-warnings'
      
receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<your-service-key>'
        description: '{{ .GroupLabels.alertname }}'
        severity: '{{ .GroupLabels.severity }}'
        details:
          num_firing: '{{ .Alerts.Firing | len }}'
          num_resolved: '{{ .Alerts.Resolved | len }}'
          firing: |
            {{ range .Alerts.Firing }}
            - {{ .Annotations.summary }}
            {{ end }}
          resolved: |
            {{ range .Alerts.Resolved }}
            - {{ .Annotations.summary }}
            {{ end }}
            
  - name: 'slack-warnings'
    slack_configs:
      - api_url: '<slack-webhook-url>'
        channel: '#llm-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'
```

### PagerDuty Event Integration

```python
# alerting/pagerduty_client.py
import requests
from typing import Dict, Any, Optional
import os

class PagerDutyClient:
    """PagerDuty Events API v2 client"""
    
    def __init__(self, integration_key: str):
        self.integration_key = integration_key
        self.url = "https://events.pagerduty.com/v2/enqueue"
        
    def trigger_event(
        self,
        summary: str,
        severity: str,
        source: str,
        component: str,
        group: str,
        class_name: str,
        custom_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Trigger a PagerDuty event"""
        
        payload = {
            "routing_key": self.integration_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "severity": severity,
                "source": source,
                "component": component,
                "group": group,
                "class": class_name,
                "custom_details": custom_details or {}
            }
        }
        
        response = requests.post(
            self.url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
        
    def resolve_event(self, dedup_key: str) -> Dict[str, Any]:
        """Resolve a PagerDuty event"""
        
        payload = {
            "routing_key": self.integration_key,
            "event_action": "resolve",
            "dedup_key": dedup_key
        }
        
        response = requests.post(
            self.url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()

# Usage
client = PagerDutyClient(os.getenv("PAGERDUTY_KEY"))

# Trigger alert
client.trigger_event(
    summary="LLM High Error Rate",
    severity="critical",
    source="llm-service",
    component="api",
    group="llm",
    class_name="performance",
    custom_details={
        "error_rate": "15%",
        "affected_models": ["gpt-4", "gpt-3.5-turbo"],
        "duration": "5 minutes"
    }
)

# Resolve alert
client.resolve_event("llm-high-error-rate")
```

---

## LLM-Specific Monitoring

### Model Performance Metrics

```yaml
# monitoring/llm_metrics.yml
metrics:
  # Request metrics
  - name: "llm_requests_total"
    type: "counter"
    labels: ["model", "provider", "status", "endpoint"]
    description: "Total LLM requests"
    
  - name: "llm_request_duration_seconds"
    type: "histogram"
    labels: ["model", "provider", "endpoint"]
    buckets: [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
    description: "LLM request duration"
    
  # Token metrics
  - name: "llm_tokens_total"
    type: "counter"
    labels: ["model", "token_type"]
    description: "Total tokens processed"
    
  - name: "llm_tokens_per_second"
    type: "gauge"
    labels: ["model"]
    description: "Token generation rate"
    
  # Cost metrics
  - name: "llm_cost_dollars_total"
    type: "counter"
    labels: ["model", "provider"]
    description: "Total API cost in dollars"
    
  # Quality metrics
  - name: "llm_quality_score"
    type: "gauge"
    labels: ["model"]
    description: "Response quality score"
    
  - name: "llm_hallucination_rate"
    type: "gauge"
    labels: ["model"]
    description: "Hallucination detection rate"
    
  # Safety metrics
  - name: "llm_safety_filtered_total"
    type: "counter"
    labels: ["model", "filter_type"]
    description: "Safety-filtered responses"
    
  # Cache metrics
  - name: "llm_cache_hits_total"
    type: "counter"
    labels: ["cache_type"]
    description: "Cache hits"
    
  - name: "llm_cache_misses_total"
    type: "counter"
    labels: ["cache_type"]
    description: "Cache misses"
```

### Python LLM Monitoring

```python
# monitoring/llm_monitor.py
from prometheus_client import Counter, Histogram, Gauge, Summary
from opentelemetry import trace
import time
from functools import wraps

# Define metrics
LLM_REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'provider', 'status', 'endpoint']
)

LLM_REQUEST_LATENCY = Histogram(
    'llm_request_duration_seconds',
    'LLM request latency',
    ['model', 'provider', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

LLM_TOKEN_COUNT = Counter(
    'llm_tokens_total',
    'Total tokens processed',
    ['model', 'token_type']
)

LLM_TOKENS_PER_SECOND = Gauge(
    'llm_tokens_per_second',
    'Token generation rate',
    ['model']
)

LLM_COST = Counter(
    'llm_cost_dollars_total',
    'Total API cost',
    ['model', 'provider']
)

LLM_QUALITY_SCORE = Gauge(
    'llm_quality_score',
    'Response quality score',
    ['model']
)

LLM_HALLUCINATION_RATE = Gauge(
    'llm_hallucination_rate',
    'Hallucination rate',
    ['model']
)

LLM_SAFETY_FILTERED = Counter(
    'llm_safety_filtered_total',
    'Safety-filtered responses',
    ['model', 'filter_type']
)

LLM_CACHE_HITS = Counter(
    'llm_cache_hits_total',
    'Cache hits',
    ['cache_type']
)

LLM_CACHE_MISSES = Counter(
    'llm_cache_misses_total',
    'Cache misses',
    ['cache_type']
)

tracer = trace.get_tracer("llm-monitor")

def monitor_llm_request(func):
    """Decorator to monitor LLM requests"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        with tracer.start_as_current_span("llm_request") as span:
            model = kwargs.get('model', 'unknown')
            provider = kwargs.get('provider', 'openai')
            endpoint = func.__name__
            
            try:
                result = await func(*args, **kwargs)
                
                # Record success
                LLM_REQUEST_COUNT.labels(
                    model=model,
                    provider=provider,
                    status='success',
                    endpoint=endpoint
                ).inc()
                
                span.set_status(trace.StatusCode.OK)
                return result
                
            except Exception as e:
                # Record failure
                LLM_REQUEST_COUNT.labels(
                    model=model,
                    provider=provider,
                    status='error',
                    endpoint=endpoint
                ).inc()
                
                span.set_status(trace.StatusCode.ERROR)
                span.record_exception(e)
                raise
                
            finally:
                duration = time.time() - start_time
                
                # Record latency
                LLM_REQUEST_LATENCY.labels(
                    model=model,
                    provider=provider,
                    endpoint=endpoint
                ).observe(duration)
                
                # Record tokens if available
                if hasattr(result, 'usage'):
                    LLM_TOKEN_COUNT.labels(
                        model=model,
                        token_type='prompt'
                    ).inc(result.usage.prompt_tokens)
                    
                    LLM_TOKEN_COUNT.labels(
                        model=model,
                        token_type='completion'
                    ).inc(result.usage.completion_tokens)
                    
                    # Calculate tokens per second
                    if duration > 0:
                        tokens_per_sec = (
                            result.usage.completion_tokens / duration
                        )
                        LLM_TOKENS_PER_SECOND.labels(
                            model=model
                        ).set(tokens_per_sec)
    
    return wrapper

def record_cost(model: str, provider: str, cost_usd: float):
    """Record API cost"""
    LLM_COST.labels(model=model, provider=provider).inc(cost_usd)

def record_quality(model: str, score: float):
    """Record quality score"""
    LLM_QUALITY_SCORE.labels(model=model).set(score)

def record_hallucination(model: str, rate: float):
    """Record hallucination rate"""
    LLM_HALLUCINATION_RATE.labels(model=model).set(rate)

def record_safety_filter(model: str, filter_type: str):
    """Record safety filter event"""
    LLM_SAFETY_FILTERED.labels(
        model=model,
        filter_type=filter_type
    ).inc()

def record_cache_hit(cache_type: str):
    """Record cache hit"""
    LLM_CACHE_HITS.labels(cache_type=cache_type).inc()

def record_cache_miss(cache_type: str):
    """Record cache miss"""
    LLM_CACHE_MISSES.labels(cache_type=cache_type).inc()
```

---

## Cost Monitoring

### Cost Tracking Configuration

```yaml
# monitoring/cost_tracking.yml
pricing:
  openai:
    gpt-4-turbo:
      input: 0.01  # per 1K tokens
      output: 0.03
    gpt-4:
      input: 0.03
      output: 0.06
    gpt-3.5-turbo:
      input: 0.0005
      output: 0.0015
      
  anthropic:
    claude-3-opus:
      input: 0.015
      output: 0.075
    claude-3-sonnet:
      input: 0.003
      output: 0.015
    claude-3-haiku:
      input: 0.00025
      output: 0.00125
      
  self-hosted:
    gpu_hourly_rate: 3.50
    storage_monthly_rate: 0.10
    
budgets:
  daily: 1000
  weekly: 5000
  monthly: 20000
  
alerts:
  - threshold: 0.8
    severity: warning
    message: "Approaching 80% of budget"
    
  - threshold: 1.0
    severity: critical
    message: "Budget exceeded"
    
  - threshold: 1.2
    severity: critical
    message: "Budget exceeded by 20%"
    action: "disable_non_critical"
```

### Python Cost Tracker

```python
# monitoring/cost_tracker.py
from prometheus_client import Counter, Gauge
from typing import Dict, Any
import datetime

# Define cost metrics
COST_TOTAL = Counter(
    'llm_cost_dollars_total',
    'Total cost in dollars',
    ['model', 'provider', 'team']
)

COST_BY_MODEL = Gauge(
    'llm_cost_by_model_dollars',
    'Cost by model',
    ['model']
)

COST_BY_TEAM = Gauge(
    'llm_cost_by_team_dollars',
    'Cost by team',
    ['team']
)

DAILY_COST = Gauge(
    'llm_daily_cost_dollars',
    'Daily cost'
)

class CostTracker:
    """Track and monitor LLM costs"""
    
    def __init__(self):
        self.pricing = {
            "openai": {
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
            },
            "anthropic": {
                "claude-3-opus": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015}
            }
        }
        
        self.budgets = {
            "daily": 1000,
            "weekly": 5000,
            "monthly": 20000
        }
        
    def calculate_cost(
        self,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for a request"""
        if provider not in self.pricing:
            return 0.0
            
        if model not in self.pricing[provider]:
            return 0.0
            
        pricing = self.pricing[provider][model]
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
        
    def record_cost(
        self,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        team: str = "default"
    ):
        """Record cost for a request"""
        cost = self.calculate_cost(model, provider, input_tokens, output_tokens)
        
        # Record to Prometheus
        COST_TOTAL.labels(
            model=model,
            provider=provider,
            team=team
        ).inc(cost)
        
        # Update daily cost
        DAILY_COST.set(self.get_daily_cost())
        
        return cost
        
    def get_daily_cost(self) -> float:
        """Get total cost for today"""
        # Query Prometheus or cache
        return 0.0  # Placeholder
        
    def check_budget(self, team: str = None) -> Dict[str, Any]:
        """Check if budget is being exceeded"""
        daily_cost = self.get_daily_cost()
        daily_budget = self.budgets["daily"]
        
        usage_percent = daily_cost / daily_budget
        
        return {
            "daily_cost": daily_cost,
            "daily_budget": daily_budget,
            "usage_percent": usage_percent,
            "exceeded": usage_percent > 1.0,
            "warning": usage_percent > 0.8
        }

# Usage
tracker = CostTracker()

# Record a cost
tracker.record_cost(
    model="gpt-4-turbo",
    provider="openai",
    input_tokens=150,
    output_tokens=450,
    team="ai-platform"
)

# Check budget
budget_status = tracker.check_budget()
print(f"Budget status: {budget_status}")
```

---

## Model Performance Monitoring

### Performance Metrics Configuration

```yaml
# monitoring/model_performance.yml
metrics:
  # Latency metrics
  - name: "llm_time_to_first_token_seconds"
    type: "histogram"
    labels: ["model"]
    buckets: [0.1, 0.25, 0.5, 1.0, 2.0]
    description: "Time to first token"
    
  - name: "llm_generation_time_seconds"
    type: "histogram"
    labels: ["model"]
    buckets: [0.5, 1.0, 2.0, 5.0, 10.0]
    description: "Total generation time"
    
  # Throughput metrics
  - name: "llm_tokens_per_second"
    type: "gauge"
    labels: ["model"]
    description: "Token generation rate"
    
  - name: "llm_requests_per_second"
    type: "gauge"
    labels: ["model"]
    description: "Request throughput"
    
  # Quality metrics
  - name: "llm_response_quality_score"
    type: "gauge"
    labels: ["model"]
    description: "Response quality score (0-1)"
    
  - name: "llm_relevance_score"
    type: "gauge"
    labels: ["model"]
    description: "Response relevance score (0-1)"
    
  - name: "llm_coherence_score"
    type: "gauge"
    labels: ["model"]
    description: "Response coherence score (0-1)"
    
  # Safety metrics
  - name: "llm_safety_score"
    type: "gauge"
    labels: ["model"]
    description: "Safety classification score (0-1)"
    
  - name: "llm_toxicity_score"
    type: "gauge"
    labels: ["model"]
    description: "Toxicity detection score (0-1)"
    
  # Error metrics
  - name: "llm_hallucination_detected_total"
    type: "counter"
    labels: ["model"]
    description: "Detected hallucinations"
    
  - name: "llm_factual_error_total"
    type: "counter"
    labels: ["model"]
    description: "Detected factual errors"
```

### Python Performance Monitor

```python
# monitoring/model_performance.py
from prometheus_client import Counter, Gauge, Histogram
import time
from typing import Dict, Any, Optional

class ModelPerformanceMonitor:
    """Monitor model performance metrics"""
    
    def __init__(self):
        self.ttft_histogram = Histogram(
            'llm_time_to_first_token_seconds',
            'Time to first token',
            ['model'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.0]
        )
        
        self.generation_time_histogram = Histogram(
            'llm_generation_time_seconds',
            'Generation time',
            ['model'],
            buckets=[0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        self.tps_gauge = Gauge(
            'llm_tokens_per_second',
            'Tokens per second',
            ['model']
        )
        
        self.quality_gauge = Gauge(
            'llm_response_quality_score',
            'Quality score',
            ['model']
        )
        
        self.relevance_gauge = Gauge(
            'llm_relevance_score',
            'Relevance score',
            ['model']
        )
        
        self.safety_gauge = Gauge(
            'llm_safety_score',
            'Safety score',
            ['model']
        )
        
        self.hallucination_counter = Counter(
            'llm_hallucination_detected_total',
            'Hallucinations detected',
            ['model']
        )
        
    def record_ttft(self, model: str, ttft: float):
        """Record time to first token"""
        self.ttft_histogram.labels(model=model).observe(ttft)
        
    def record_generation_time(self, model: str, duration: float):
        """Record generation time"""
        self.generation_time_histogram.labels(model=model).observe(duration)
        
    def record_tokens_per_second(self, model: str, tps: float):
        """Record tokens per second"""
        self.tps_gauge.labels(model=model).set(tps)
        
    def record_quality_score(self, model: str, score: float):
        """Record quality score"""
        self.quality_gauge.labels(model=model).set(score)
        
    def record_relevance_score(self, model: str, score: float):
        """Record relevance score"""
        self.relevance_gauge.labels(model=model).set(score)
        
    def record_safety_score(self, model: str, score: float):
        """Record safety score"""
        self.safety_gauge.labels(model=model).set(score)
        
    def record_hallucination(self, model: str):
        """Record hallucination detection"""
        self.hallucination_counter.labels(model=model).inc()
        
    def analyze_response(
        self,
        model: str,
        prompt: str,
        response: str,
        ttft: float,
        total_time: float,
        tokens_generated: int
    ) -> Dict[str, Any]:
        """Analyze and record all metrics"""
        
        # Record TTFT
        self.record_ttft(model, ttft)
        
        # Record generation time
        self.record_generation_time(model, total_time)
        
        # Calculate and record TPS
        if total_time > 0:
            tps = tokens_generated / total_time
            self.record_tokens_per_second(model, tps)
        
        # Quality analysis (simplified - use real quality scorer)
        quality_score = self._calculate_quality_score(response)
        self.record_quality_score(model, quality_score)
        
        # Relevance analysis
        relevance_score = self._calculate_relevance_score(prompt, response)
        self.record_relevance_score(model, relevance_score)
        
        # Safety analysis
        safety_score = self._calculate_safety_score(response)
        self.record_safety_score(model, safety_score)
        
        # Hallucination detection
        if self._detect_hallucination(response):
            self.record_hallucination(model)
            
        return {
            "ttft": ttft,
            "generation_time": total_time,
            "tps": tokens_generated / total_time if total_time > 0 else 0,
            "quality_score": quality_score,
            "relevance_score": relevance_score,
            "safety_score": safety_score
        }
        
    def _calculate_quality_score(self, response: str) -> float:
        """Calculate quality score (simplified)"""
        # In production, use a quality scoring model
        return 0.85
        
    def _calculate_relevance_score(self, prompt: str, response: str) -> float:
        """Calculate relevance score (simplified)"""
        # In production, use embedding similarity
        return 0.9
        
    def _calculate_safety_score(self, response: str) -> float:
        """Calculate safety score (simplified)"""
        # In production, use safety classifier
        return 0.95
        
    def _detect_hallucination(self, response: str) -> bool:
        """Detect hallucination (simplified)"""
        # In production, use fact-checking model
        return False

# Usage
monitor = ModelPerformanceMonitor()

# Analyze a response
result = monitor.analyze_response(
    model="gpt-4-turbo",
    prompt="What is the capital of France?",
    response="The capital of France is Paris.",
    ttft=0.5,
    total_time=2.0,
    tokens_generated=10
)

print(f"Analysis: {result}")
```

---

## Security Monitoring

### Security Event Configuration

```yaml
# monitoring/security_events.yml
events:
  authentication:
    - name: "login_success"
      level: "INFO"
      retention: "90 days"
      
    - name: "login_failure"
      level: "WARN"
      alert_threshold: "5 failures in 5 minutes"
      
    - name: "password_reset"
      level: "INFO"
      retention: "1 year"
      
    - name: "mfa_enabled"
      level: "INFO"
      retention: "1 year"
      
  authorization:
    - name: "permission_denied"
      level: "WARN"
      alert_threshold: "10 per minute"
      
    - name: "role_changed"
      level: "INFO"
      retention: "1 year"
      
    - name: "privilege_escalation"
      level: "CRITICAL"
      alert_threshold: "Immediate"
      
  data_access:
    - name: "sensitive_data_access"
      level: "INFO"
      retention: "1 year"
      
    - name: "data_export"
      level: "WARN"
      alert_threshold: "Any export"
      
    - name: "bulk_data_access"
      level: "WARN"
      alert_threshold: "> 1000 records"
      
  llm_specific:
    - name: "prompt_injection_detected"
      level: "CRITICAL"
      alert_threshold: "Immediate"
      
    - name: "content_filtered"
      level: "INFO"
      retention: "30 days"
      
    - name: "abuse_detected"
      level: "CRITICAL"
      alert_threshold: "Immediate"
```

### Security Monitor Implementation

```python
# monitoring/security_monitor.py
from prometheus_client import Counter, Gauge
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SecurityMonitor:
    """Monitor security events"""
    
    def __init__(self):
        self.login_attempts = Counter(
            'security_login_attempts_total',
            'Login attempts',
            ['status', 'method']
        )
        
        self.permission_denied = Counter(
            'security_permission_denied_total',
            'Permission denied events',
            ['resource', 'action']
        )
        
        self.data_access = Counter(
            'security_data_access_total',
            'Data access events',
            ['resource', 'type']
        )
        
        self.prompt_injections = Counter(
            'security_prompt_injections_total',
            'Prompt injection attempts',
            ['model']
        )
        
        self.content_filtered = Counter(
            'security_content_filtered_total',
            'Content filtered events',
            ['filter_type']
        )
        
        self.abuse_detected = Counter(
            'security_abuse_detected_total',
            'Abuse detected events',
            ['type']
        )
        
    def record_login(
        self,
        user_id: str,
        success: bool,
        method: str = "password"
    ):
        """Record login attempt"""
        status = "success" if success else "failure"
        
        self.login_attempts.labels(
            status=status,
            method=method
        ).inc()
        
        logger.info(
            "login_attempt",
            user_id=user_id,
            success=success,
            method=method
        )
        
    def record_permission_denied(
        self,
        user_id: str,
        resource: str,
        action: str
    ):
        """Record permission denied"""
        self.permission_denied.labels(
            resource=resource,
            action=action
        ).inc()
        
        logger.warning(
            "permission_denied",
            user_id=user_id,
            resource=resource,
            action=action
        )
        
    def record_data_access(
        self,
        user_id: str,
        resource: str,
        access_type: str,
        record_count: int
    ):
        """Record data access"""
        self.data_access.labels(
            resource=resource,
            type=access_type
        ).inc(record_count)
        
        logger.info(
            "data_access",
            user_id=user_id,
            resource=resource,
            access_type=access_type,
            record_count=record_count
        )
        
    def record_prompt_injection(
        self,
        user_id: str,
        model: str,
        prompt: str
    ):
        """Record prompt injection attempt"""
        self.prompt_injections.labels(model=model).inc()
        
        logger.critical(
            "prompt_injection_detected",
            user_id=user_id,
            model=model,
            prompt=prompt[:200]  # Truncate for safety
        )
        
    def record_content_filtered(
        self,
        user_id: str,
        filter_type: str,
        content: str
    ):
        """Record content filter event"""
        self.content_filtered.labels(filter_type=filter_type).inc()
        
        logger.warning(
            "content_filtered",
            user_id=user_id,
            filter_type=filter_type
        )
        
    def record_abuse(
        self,
        user_id: str,
        abuse_type: str,
        details: Dict[str, Any]
    ):
        """Record abuse event"""
        self.abuse_detected.labels(type=abuse_type).inc()
        
        logger.critical(
            "abuse_detected",
            user_id=user_id,
            abuse_type=abuse_type,
            details=details
        )

# Usage
monitor = SecurityMonitor()

# Record events
monitor.record_login("user123", success=True)
monitor.record_permission_denied("user123", "admin_panel", "read")
monitor.record_prompt_injection("user123", "gpt-4", "ignore previous instructions")
```

---

## Complete Monitoring Stack

### Docker Compose

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
      
  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      
  # Jaeger
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "6831:6831/udp"
      - "14268:14268"
      
  # Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
      
  # Kibana
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
      
  # Logstash
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    ports:
      - "5044:5044"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      
  # Alertmanager
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      
  # Loki
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
      
  # Promtail
  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./promtail/promtail.yml:/etc/promtail/promtail.yml
      - /var/log:/var/log
      
  # OTel Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317"
      - "4318:4318"
      - "8888:8888"
    volumes:
      - ./otel/otel-collector.yml:/etc/otel-collector/config.yml

volumes:
  prometheus_data:
  grafana_data:
  elasticsearch_data:
```

---

## Production Examples

### Production Monitoring Configuration

```yaml
# production/monitoring-config.yml
environment: production
cluster: us-east-1

services:
  llm-gateway:
    metrics:
      enabled: true
      port: 8080
      path: /metrics
    logging:
      level: INFO
      format: json
      aggregation: elasticsearch
    tracing:
      enabled: true
      sampler: probabilistic
      sample_rate: 0.1
    alerts:
      - name: HighErrorRate
        threshold: 0.1
        duration: 5m
        severity: critical
      - name: HighLatency
        threshold: 5s
        duration: 10m
        severity: warning
        
  model-server:
    metrics:
      enabled: true
      port: 8081
      path: /metrics
    logging:
      level: INFO
      format: json
      aggregation: elasticsearch
    tracing:
      enabled: true
      sampler: probabilistic
      sample_rate: 0.2
    alerts:
      - name: GPUHighUsage
        threshold: 0.9
        duration: 5m
        severity: warning
      - name: OutOfMemory
        threshold: 0.95
        duration: 1m
        severity: critical

dashboards:
  executive:
    refresh: 5m
    panels: 6
  operational:
    refresh: 30s
    panels: 12
  debug:
    refresh: real-time
    panels: 15

alerting:
  pagerduty:
    enabled: true
    service_key: ${PAGERDUTY_KEY}
  slack:
    enabled: true
    webhook: ${SLACK_WEBHOOK}
    channels:
      critical: '#alerts-critical'
      warning: '#alerts-warnings'
      info: '#alerts-info'
```

---

## References

- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- Jaeger: https://www.jaegertracing.io/docs/
- ELK Stack: https://www.elastic.co/what-is/elk-stack

---

*Last Updated: January 2025*
*Version: 1.0.0*
