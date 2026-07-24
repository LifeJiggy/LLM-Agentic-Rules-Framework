# Monitoring Best Practices for AI/LLM Systems

## Patterns and Implementation Guidelines

---

## Table of Contents

1. [Structured Logging](#structured-logging)
2. [Distributed Tracing](#distributed-tracing)
3. [Metric Cardinality Management](#metric-cardinality-management)
4. [Alert Fatigue Reduction](#alert-fatigue-reduction)
5. [Runbook Automation](#runbook-automation)
6. [Capacity Planning](#capacity-planning)
7. [LLM-Specific Best Practices](#llm-specific-best-practices)
8. [Implementation Patterns](#implementation-patterns)
9. [Cost Optimization](#cost-optimization)
10. [Security Monitoring](#security-monitoring)

---

## Structured Logging

### Why Structured Logging Matters

Structured logging transforms unstructured text logs into machine-parseable data, enabling powerful querying, aggregation, and analysis capabilities essential for LLM systems.

### JSON Log Format Standard

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "INFO",
  "service": "llm-gateway",
  "version": "1.2.3",
  "environment": "production",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user_123",
  "session_id": "sess_456",
  "request_id": "req_789",
  "event": "llm_request_complete",
  "message": "LLM request processed successfully",
  "duration_ms": 2345,
  "model": {
    "name": "gpt-4-turbo",
    "version": "2024-04-09",
    "provider": "openai"
  },
  "tokens": {
    "prompt": 150,
    "completion": 450,
    "total": 600
  },
  "cost": {
    "usd": 0.045,
    "budget_remaining": 95.50
  },
  "metadata": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
    "stream": false
  },
  "http": {
    "method": "POST",
    "url": "/api/v1/chat",
    "status_code": 200,
    "user_agent": "Mozilla/5.0"
  },
  "tags": {
    "feature": "customer-support",
    "tier": "premium"
  }
}
```

### Log Field Taxonomy

```yaml
standard_fields:
  required:
    - name: "timestamp"
      type: "ISO8601"
      description: "When the event occurred"
      format: "2025-01-15T10:30:45.123Z"
      
    - name: "level"
      type: "enum"
      values: ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
      description: "Severity level"
      
    - name: "service"
      type: "string"
      description: "Service name"
      example: "llm-gateway"
      
    - name: "event"
      type: "string"
      description: "Event type identifier"
      example: "llm_request_complete"
      
    - name: "message"
      type: "string"
      description: "Human-readable message"
      
  recommended:
    - name: "trace_id"
      type: "string"
      description: "Distributed trace identifier"
      
    - name: "span_id"
      type: "string"
      description: "Current span identifier"
      
    - name: "user_id"
      type: "string"
      description: "Authenticated user identifier"
      
    - name: "request_id"
      type: "string"
      description: "Unique request identifier"
      
  llm_specific:
    - name: "model"
      type: "object"
      fields:
        - name: "name"
          type: "string"
          description: "Model identifier"
        - name: "provider"
          type: "string"
          description: "API provider"
          
    - name: "tokens"
      type: "object"
      fields:
        - name: "prompt"
          type: "integer"
          description: "Input token count"
        - name: "completion"
          type: "integer"
          description: "Output token count"
          
    - name: "cost"
      type: "object"
      fields:
        - name: "usd"
          type: "number"
          description: "Cost in US dollars"

log_levels_guidelines:
  DEBUG:
    when: "Detailed diagnostic information"
    examples:
      - "Token-by-token generation"
      - "Prompt template variables"
      - "Cache lookup details"
    retention: "24 hours"
    production: "Rarely enabled"
    
  INFO:
    when: "Normal operation events"
    examples:
      - "Request started/completed"
      - "Model loaded/unloaded"
      - "Cache hit/miss statistics"
    retention: "30 days"
    production: "Always enabled"
    
  WARN:
    when: "Potential issues detected"
    examples:
      - "Approaching rate limits"
      - "Elevated error rates"
      - "Resource usage warnings"
    retention: "90 days"
    production: "Always enabled"
    
  ERROR:
    when: "Failures requiring attention"
    examples:
      - "API call failures"
      - "Authentication errors"
      - "Timeout exceeded"
    retention: "1 year"
    production: "Always enabled"
    
  FATAL:
    when: "Critical system failures"
    examples:
      - "Service crash"
      - "Data corruption"
      - "Security breach"
    retention: "Permanent"
    production: "Always enabled"
```

### Python Implementation

```python
# logging/structured_logger.py
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from contextvars import ContextVar
import uuid

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default='')
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')

class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self._get_service_name(),
            "event": getattr(record, 'event', record.name),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add context variables
        request_id = request_id_var.get('')
        if request_id:
            log_entry["request_id"] = request_id
            
        trace_id = trace_id_var.get('')
        if trace_id:
            log_entry["trace_id"] = trace_id
            
        user_id = user_id_var.get('')
        if user_id:
            log_entry["user_id"] = user_id
            
        # Add exception info
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
            
        # Add extra fields
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in logging.LogRecord('','','','','','','','').__dict__
            and k not in ['message', 'msg', 'args', 'exc_info', 'exc_text']
        }
        if extra_fields:
            log_entry["metadata"] = extra_fields
            
        return json.dumps(log_entry, default=str)
    
    def _get_service_name(self) -> str:
        return getattr(self, 'service_name', 'unknown')

class LLMStructuredLogger:
    """Specialized logger for LLM operations"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)
        
    def log_llm_request(
        self,
        model: str,
        provider: str,
        prompt_tokens: int,
        completion_tokens: int,
        duration_ms: float,
        cost_usd: float,
        status: str,
        **kwargs
    ):
        """Log LLM request completion"""
        self.logger.info(
            "llm_request_complete",
            event="llm_request_complete",
            model={"name": model, "provider": provider},
            tokens={
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": prompt_tokens + completion_tokens
            },
            duration_ms=duration_ms,
            cost_usd=cost_usd,
            status=status,
            **kwargs
        )
        
    def log_model_load(
        self,
        model_name: str,
        load_time_ms: float,
        memory_mb: float
    ):
        """Log model loading event"""
        self.logger.info(
            "model_loaded",
            event="model_loaded",
            model=model_name,
            load_time_ms=load_time_ms,
            memory_mb=memory_mb
        )
        
    def log_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log error with context"""
        self.logger.error(
            "error_occurred",
            event="error",
            error_type=error_type,
            error_message=error_message,
            context=context or {}
        )

# Usage example
logger = LLMStructuredLogger("llm-gateway")
logger.log_llm_request(
    model="gpt-4-turbo",
    provider="openai",
    prompt_tokens=150,
    completion_tokens=450,
    duration_ms=2345,
    cost_usd=0.045,
    status="success"
)
```

### Node.js Implementation

```javascript
// logging/structured-logger.js
const winston = require('winston');
const { v4: uuidv4 } = require('uuid');

// Context storage for request tracking
const asyncLocalStorage = require('async_hooks').AsyncLocalStorage;
const requestContext = new asyncLocalStorage();

// Custom JSON format
const jsonFormat = winston.format.printf((info) => {
  const context = requestContext.getStore() || {};
  
  const logEntry = {
    timestamp: new Date().toISOString(),
    level: info.level,
    service: process.env.SERVICE_NAME || 'llm-service',
    event: info.event || info.message,
    message: info.message,
    ...context,
    ...info.metadata
  };
  
  if (info.stack) {
    logEntry.exception = {
      stack: info.stack
    };
  }
  
  return JSON.stringify(logEntry);
});

// Create logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    jsonFormat
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ 
      filename: 'logs/error.log', 
      level: 'error' 
    }),
    new winston.transports.File({ 
      filename: 'logs/combined.log' 
    })
  ]
});

// Middleware for request context
function requestContextMiddleware(req, res, next) {
  const requestId = req.headers['x-request-id'] || uuidv4();
  const traceId = req.headers['x-trace-id'] || '';
  const userId = req.user?.id || '';
  
  const store = {
    requestId,
    traceId,
    userId,
    service: process.env.SERVICE_NAME
  };
  
  requestContext.run(store, () => {
    req.requestId = requestId;
    req.traceId = traceId;
    next();
  });
}

// LLM-specific logging helper
const llmLogger = {
  logRequest: (data) => {
    logger.info('llm_request_complete', {
      event: 'llm_request_complete',
      model: data.model,
      provider: data.provider,
      tokens: {
        prompt: data.promptTokens,
        completion: data.completionTokens,
        total: data.promptTokens + data.completionTokens
      },
      duration_ms: data.durationMs,
      cost_usd: data.costUsd,
      status: data.status
    });
  },
  
  logModelLoad: (data) => {
    logger.info('model_loaded', {
      event: 'model_loaded',
      model: data.model,
      load_time_ms: data.loadTimeMs,
      memory_mb: data.memoryMb
    });
  },
  
  logError: (error, context = {}) => {
    logger.error('error_occurred', {
      event: 'error',
      error_type: error.name,
      error_message: error.message,
      stack: error.stack,
      context
    });
  }
};

module.exports = { logger, llmLogger, requestContextMiddleware };
```

---

## Distributed Tracing

### OpenTelemetry Integration

```yaml
# otel-config.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
        
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
        
exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: false
      
  prometheus:
    endpoint: 0.0.0.0:8889
    
  logging:
    loglevel: info
    
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [jaeger, logging]
      
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
```

### Python OpenTelemetry Setup

```python
# tracing/otel_setup.py
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

def setup_tracing(service_name: str = "llm-service"):
    """Configure OpenTelemetry tracing"""
    
    resource = Resource.create({
        SERVICE_NAME: service_name,
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        "service.version": os.getenv("SERVICE_VERSION", "1.0.0")
    })
    
    provider = TracerProvider(resource=resource)
    
    # Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
        agent_port=int(os.getenv("JAEGER_PORT", "6831")),
    )
    
    # OTLP exporter (for collectors)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_ENDPOINT", "localhost:4317"),
        insecure=True
    )
    
    # Add processors
    provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    provider.add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )
    
    trace.set_tracer_provider(provider)
    
    # Auto-instrument libraries
    FastAPIInstrumentor.instrument()
    HTTPXClientInstrumentor.instrument()
    OpenAIInstrumentor.instrument()
    
    return trace.get_tracer(service_name)

# Custom span attributes for LLM operations
def add_llm_attributes(span, model, tokens, duration_ms):
    """Add LLM-specific attributes to span"""
    span.set_attribute("llm.model.name", model)
    span.set_attribute("llm.tokens.prompt", tokens.get("prompt", 0))
    span.set_attribute("llm.tokens.completion", tokens.get("completion", 0))
    span.set_attribute("llm.duration_ms", duration_ms)
    
# Usage
tracer = setup_tracing()

def process_llm_request(prompt, model="gpt-4"):
    with tracer.start_as_current_span("llm_request") as span:
        span.set_attribute("llm.prompt.length", len(prompt))
        
        # Call LLM
        response = call_llm(prompt, model)
        
        span.set_attribute("llm.response.length", len(response))
        span.set_attribute("llm.model", model)
        
        return response
```

### Node.js OpenTelemetry Setup

```javascript
// tracing/otel-setup.js
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { BatchSpanProcessor, SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');

function setupTracing(serviceName = 'llm-service') {
  const provider = new NodeTracerProvider({
    resource: new Resource({
      [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
      [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.ENVIRONMENT || 'production',
      [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION || '1.0.0'
    })
  });

  // Jaeger exporter
  const jaegerExporter = new JaegerExporter({
    serviceName,
    host: process.env.JAEGER_HOST || 'localhost',
    port: parseInt(process.env.JAEGER_PORT || '6831')
  });

  // OTLP exporter
  const otlpExporter = new OTLPTraceExporter({
    url: process.env.OTEL_ENDPOINT || 'http://localhost:4317'
  });

  provider.addSpanProcessor(new BatchSpanProcessor(jaegerExporter));
  provider.addSpanProcessor(new BatchSpanProcessor(otlpExporter));

  provider.register();

  // Auto-instrumentations
  registerInstrumentations({
    instrumentations: [
      getNodeAutoInstrumentations({
        '@opentelemetry/instrumentation-http': { enabled: true },
        '@opentelemetry/instrumentation-express': { enabled: true },
        '@opentelemetry/instrumentation-redis': { enabled: true },
        '@opentelemetry/instrumentation-pg': { enabled: true }
      })
    ]
  });

  return provider;
}

// Custom span creation for LLM operations
function createLLMSpan(tracer, operation, attributes = {}) {
  return tracer.startSpan(operation, {
    attributes: {
      'llm.provider': attributes.provider || 'unknown',
      'llm.model': attributes.model || 'unknown',
      'llm.tokens.prompt': attributes.promptTokens || 0,
      'llm.tokens.completion': attributes.completionTokens || 0,
      ...attributes
    }
  });
}

module.exports = { setupTracing, createLLMSpan };
```

---

## Metric Cardinality Management

### Understanding Cardinality

```yaml
cardinality_concepts:
  definition: "The number of unique label combinations for a metric"
  
  example:
    metric: "http_requests_total"
    labels:
      method: ["GET", "POST", "PUT", "DELETE"]  # 4 values
      status: ["200", "400", "500"]              # 3 values
      endpoint: ["/api/v1/*"]                     # 100 endpoints
    cardinality: 4 × 3 × 100 = 1,200 time series
    
  impact:
    memory: "Each time series consumes ~1-2KB of memory"
    query_performance: "High cardinality slows PromQL queries"
    storage: "More time series = more disk usage"
    
  limits:
    recommended: "< 10,000 time series per metric"
    absolute_maximum: "100,000 time series per metric"
    label_values: "< 1,000 unique values per label"
```

### Cardinality Control Strategies

```yaml
strategies:
  avoid_high_cardinality_labels:
    problematic:
      - label: "user_id"
        cardinality: "millions"
        solution: "Use as metadata, not label"
        
      - label: "request_id"
        cardinality: "unbounded"
        solution: "Log it, don't metric it"
        
      - label: "timestamp"
        cardinality: "infinite"
        solution: "Use time series, not label"
        
    acceptable:
      - label: "model"
        cardinality: "10-100"
        
      - label: "status"
        cardinality: "5-10"
        
      - label: "environment"
        cardinality: "3-5"
        
  aggregation_strategies:
    pre_aggregation:
      description: "Aggregate before exposing metrics"
      example: "Count per model, not per user"
      
    sampling:
      description: "Sample high-cardinality data"
      example: "Log 1% of requests for analysis"
      
    bucketing:
      description: "Group continuous values"
      example: "Response time buckets instead of exact values"
```

### Python Cardinality-Aware Metrics

```python
# metrics/cardinality_manager.py
from prometheus_client import Counter, Histogram, Gauge, REGISTRY
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class CardinalityManager:
    """Manages metric cardinality to prevent explosion"""
    
    def __init__(self, max_cardinality: int = 10000):
        self.max_cardinality = max_cardinality
        self.cardinality_tracker: Dict[str, Set[str]] = {}
        
    def check_cardinality(self, metric_name: str, label_key: str, label_value: str) -> bool:
        """Check if adding this label value would exceed limits"""
        key = f"{metric_name}:{label_key}"
        
        if key not in self.cardinality_tracker:
            self.cardinality_tracker[key] = set()
            
        current_count = len(self.cardinality_tracker[key])
        
        if current_count >= self.max_cardinality:
            logger.warning(
                f"Cardinality limit reached for {key}: {current_count}"
            )
            return False
            
        self.cardinality_tracker[key].add(label_value)
        return True
        
    def safe_label(self, metric_name: str, label_key: str, label_value: str, fallback: str = "other") -> str:
        """Return label value or fallback if cardinality would be exceeded"""
        if self.check_cardinality(metric_name, label_key, label_value):
            return label_value
        return fallback

# Create cardinality-aware metrics
cardinality_mgr = CardinalityManager(max_cardinality=1000)

# Safe counter with cardinality control
SAFE_REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status', 'user_tier']  # Controlled cardinality
)

def record_request(model: str, status: str, user_id: str):
    """Record request with cardinality-safe labels"""
    # Don't use user_id as label - too high cardinality
    # Instead, log it separately
    user_tier = get_user_tier(user_id)  # Returns: free, pro, enterprise
    
    SAFE_REQUEST_COUNT.labels(
        model=cardinality_mgr.safe_label("llm_requests_total", "model", model),
        status=status,
        user_tier=user_tier
    ).inc()
```

---

## Alert Fatigue Reduction

### Alert Fatigue Causes and Solutions

```yaml
causes:
  too_many_alerts:
    description: "More alerts than humans can process"
    solution: "Consolidate and prioritize"
    
  false_positives:
    description: "Alerts that don't require action"
    solution: "Tune thresholds and add conditions"
    
  unclear_escalation:
    description: "No clear ownership or response process"
    solution: "Define escalation paths"
    
  no_context:
    description: "Alerts without enough information"
    solution: "Enrich alerts with context"

solutions:
  alert_consolidation:
    before:
      alerts:
        - "High CPU on server-1"
        - "High CPU on server-2"
        - "High CPU on server-3"
    after:
      alerts:
        - "High CPU on 3 servers in cluster-1"
        
  progressive_escalation:
    stages:
      - stage: 1
        trigger: "Alert fires"
        action: "Notify on-call via Slack"
        timeout: "15 minutes"
        
      - stage: 2
        trigger: "No acknowledgment"
        action: "Page on-call"
        timeout: "30 minutes"
        
      - stage: 3
        trigger: "No resolution"
        action: "Escalate to team lead"
        timeout: "1 hour"
        
      - stage: 4
        trigger: "Critical impact"
        action: "Escalate to management"
        
  maintenance_windows:
    description: "Suppress alerts during planned maintenance"
    implementation: "Alertmanager silence rules"
    
  alert_correlation:
    description: "Group related alerts together"
    example: "All alerts related to same service"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '<slack-webhook-url>'
  
route:
  receiver: 'default-receiver'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  
  routes:
    # Critical alerts
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      group_wait: 0s
      continue: true
      
    # Warning alerts
    - match:
        severity: warning
      receiver: 'slack-warnings'
      group_wait: 30s
      
    # Info alerts
    - match:
        severity: info
      receiver: 'slack-info'
      repeat_interval: 4h
      
    # LLM-specific alerts
    - match_re:
        alertname: 'LLM.*'
      receiver: 'llm-team-slack'
      group_by: ['alertname', 'model']
      
receivers:
  - name: 'default-receiver'
    slack_configs:
      - channel: '#alerts'
        
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<key>'
        description: '{{ .GroupLabels.alertname }}'
        
  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-warnings'
        title: '⚠️ {{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'
        
  - name: 'slack-info'
    slack_configs:
      - channel: '#alerts-info'
        
  - name: 'llm-team-slack'
    slack_configs:
      - channel: '#llm-alerts'
        
inhibit_rules:
  # Don't alert on warnings if critical is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster']
    
  # Don't alert on info if warning is firing
  - source_match:
      severity: 'warning'
    target_match:
      severity: 'info'
    equal: ['alertname', 'cluster']
    
  # Suppress duplicate alerts
  - source_match:
      alertname: 'NodeDown'
    target_match:
      alertname: '.*/Down$'
    equal: ['instance']
```

---

## Runbook Automation

### Runbook Structure

```yaml
runbook_template:
  metadata:
    title: "LLM Service High Error Rate"
    id: "RUNBOOK-001"
    severity: "P1"
    last_updated: "2025-01-15"
    owner: "llm-team"
    
  alert_description:
    summary: "Error rate exceeds 10% for 5+ minutes"
    impact: "Users experiencing failed requests"
    metric: "rate(llm_requests_total{status='error'}[5m])"
    
  investigation_steps:
    - step: 1
      action: "Check service health"
      command: "kubectl get pods -l app=llm-service"
      expected: "All pods in Running state"
      
    - step: 2
      action: "Check recent deployments"
      command: "kubectl rollout history deployment/llm-service"
      expected: "No recent deployments or known good version"
      
    - step: 3
      action: "Check upstream dependencies"
      command: "curl -s http://llm-provider/health"
      expected: "Provider API responding"
      
    - step: 4
      action: "Check error logs"
      command: "kubectl logs -l app=llm-service --tail=100 | grep ERROR"
      expected: "No critical errors"
      
  remediation_steps:
    - step: 1
      action: "If provider issue, enable fallback"
      command: |
        kubectl set env deployment/llm-service \
          FALLBACK_MODEL=gpt-3.5-turbo
      rollback: "Remove FALLBACK_MODEL env var"
      
    - step: 2
      action: "If memory issue, restart pods"
      command: "kubectl rollout restart deployment/llm-service"
      rollback: "None - restart is safe"
      
    - step: 3
      action: "If config issue, rollback deployment"
      command: "kubectl rollout undo deployment/llm-service"
      rollback: "Re-apply the config change"
      
  escalation:
    after_15_minutes: "Page team lead"
    after_30_minutes: "Page engineering manager"
    after_1_hour: "Incident commander"
    
  post_incident:
    - "Update runbook with new findings"
    - "Add monitoring for root cause"
    - "Schedule post-mortem"
```

### Automated Runbook Execution

```python
# runbooks/auto_executor.py
import subprocess
from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RunbookStep:
    step_id: int
    action: str
    command: str
    expected: str
    timeout: int = 60
    rollback: str = ""

@dataclass
class Runbook:
    id: str
    title: str
    severity: str
    steps: List[RunbookStep]

class RunbookExecutor:
    """Automated runbook execution"""
    
    def __init__(self):
        self.runbooks: Dict[str, Runbook] = {}
        self.execution_log: List[Dict[str, Any]] = []
        
    def register_runbook(self, runbook: Runbook):
        """Register a runbook for execution"""
        self.runbooks[runbook.id] = runbook
        logger.info(f"Registered runbook: {runbook.id} - {runbook.title}")
        
    def execute_step(self, step: RunbookStep) -> Dict[str, Any]:
        """Execute a single runbook step"""
        logger.info(f"Executing step {step.step_id}: {step.action}")
        
        try:
            result = subprocess.run(
                step.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=step.timeout
            )
            
            success = result.returncode == 0
            
            execution = {
                "step_id": step.step_id,
                "action": step.action,
                "command": step.command,
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            self.execution_log.append(execution)
            return execution
            
        except subprocess.TimeoutExpired:
            logger.error(f"Step {step.step_id} timed out")
            return {
                "step_id": step.step_id,
                "action": step.action,
                "success": False,
                "error": "timeout"
            }
            
    def execute_runbook(self, runbook_id: str) -> bool:
        """Execute all steps in a runbook"""
        if runbook_id not in self.runbooks:
            logger.error(f"Runbook {runbook_id} not found")
            return False
            
        runbook = self.runbooks[runbook_id]
        logger.info(f"Executing runbook: {runbook.title}")
        
        for step in runbook.steps:
            result = self.execute_step(step)
            
            if not result.get("success"):
                logger.error(f"Step {step.step_id} failed: {result}")
                return False
                
        logger.info(f"Runbook {runbook_id} completed successfully")
        return True

# Example usage
executor = RunbookExecutor()

# Define a runbook
high_error_runbook = Runbook(
    id="RUNBOOK-001",
    title="LLM Service High Error Rate",
    severity="P1",
    steps=[
        RunbookStep(
            step_id=1,
            action="Check pod status",
            command="kubectl get pods -l app=llm-service",
            expected="All pods Running"
        ),
        RunbookStep(
            step_id=2,
            action="Enable fallback model",
            command="kubectl set env deployment/llm-service FALLBACK_MODEL=gpt-3.5-turbo",
            expected="Environment variable set"
        )
    ]
)

executor.register_runbook(high_error_runbook)

# Execute when alert fires
executor.execute_runbook("RUNBOOK-001")
```

---

## Capacity Planning

### Resource Prediction Models

```yaml
capacity_planning:
  metrics_to_track:
    request_volume:
      - "Requests per second"
      - "Peak vs average ratio"
      - "Growth rate (week-over-week)"
      
    resource_utilization:
      - "CPU usage distribution"
      - "Memory usage distribution"
      - "GPU utilization"
      - "Network bandwidth"
      
    cost_metrics:
      - "Cost per request"
      - "Total daily cost"
      - "Cost trend"
      
  planning_horizons:
    short_term:
      duration: "1-4 weeks"
      focus: "Immediate scaling needs"
      actions:
        - "Auto-scaling adjustments"
        - "Resource right-sizing"
        
    medium_term:
      duration: "1-3 months"
      focus: "Capacity procurement"
      actions:
        - "Reserved instances"
        - "Contract negotiations"
        
    long_term:
      duration: "3-12 months"
      focus: "Architecture decisions"
      actions:
        - "Infrastructure investment"
        - "Technology choices"
        
  prediction_methods:
    linear_regression:
      description: "Simple trend extrapolation"
      best_for: "Stable, predictable workloads"
      
    seasonal_decomposition:
      description: "Account for daily/weekly patterns"
      best_for: "Workloads with clear cycles"
      
    machine_learning:
      description: "ML-based forecasting"
      best_for: "Complex, non-linear patterns"
```

### Prometheus Queries for Capacity Planning

```yaml
# Capacity planning PromQL queries
queries:
  # Request volume trends
  request_volume_7d_avg: |
    avg_over_time(
      sum(rate(llm_requests_total[1h]))[7d:1h]
    )
    
  request_volume_growth: |
    (
      sum(rate(llm_requests_total[1h])) offset 7d
      -
      sum(rate(llm_requests_total[1h]))
    ) / sum(rate(llm_requests_total[1h])) offset 7d * 100
    
  # Resource utilization
  cpu_utilization_95th: |
    histogram_quantile(0.95, 
      rate(cpu_usage_seconds_total[5m])
    )
    
  memory_utilization_avg: |
    avg(
      process_resident_memory_bytes / machine_memory_bytes
    ) * 100
    
  # Cost projections
  daily_cost_current: |
    increase(llm_cost_dollars_total[24h])
    
  daily_cost_30d_avg: |
    avg_over_time(
      increase(llm_cost_dollars_total[24h])[30d:24h]
    )
    
  # Capacity thresholds
  capacity_remaining: |
    (1 - (
      sum(rate(llm_requests_total[5m])) 
      / 
      llm_capacity_limit
    )) * 100
    
  days_until_capacity: |
    (llm_capacity_limit - sum(rate(llm_requests_total[5m])))
    /
    (sum(rate(llm_requests_total[5m])) - sum(rate(llm_requests_total[5m] offset 7d)))
```

---

## LLM-Specific Best Practices

### Model Performance Monitoring

```yaml
model_monitoring:
  quality_metrics:
    response_relevance:
      description: "How relevant responses are to queries"
      method: "Embedding similarity between query and response"
      target: "> 0.8 similarity score"
      
    hallucination_rate:
      description: "Rate of factually incorrect statements"
      method: "Fact-checking against knowledge base"
      target: "< 5% of responses"
      
    consistency:
      description: "Same query produces similar results"
      method: "Compare responses across multiple runs"
      target: "< 10% variance"
      
  latency_metrics:
    time_to_first_token:
      description: "Time until first token generated"
      target: "< 500ms"
      alert: "> 2s for 5 minutes"
      
    tokens_per_second:
      description: "Generation throughput"
      target: "> 50 tokens/sec"
      alert: "< 20 tokens/sec for 5 minutes"
      
    end_to_end_latency:
      description: "Total request duration"
      target: "p95 < 3s"
      alert: "p95 > 5s for 5 minutes"
      
  cost_metrics:
    cost_per_token:
      description: "Average cost per token"
      tracking: "Model-specific pricing"
      
    cost_per_request:
      description: "Average cost per request"
      target: "Within budget"
      
    daily_spend:
      description: "Total daily cost"
      alert: "> 120% of budget"
```

### Prompt Monitoring

```yaml
prompt_monitoring:
  input_analysis:
    token_count:
      description: "Track prompt token usage"
      histogram_buckets: [100, 500, 1000, 2000, 4000, 8000]
      
    complexity_score:
      description: "Estimated task complexity"
      method: "Classifier model"
      
    language_detection:
      description: "Input language"
      method: "Language detection API"
      
  output_analysis:
    quality_score:
      description: "Response quality assessment"
      method: "Quality classifier"
      
    safety_score:
      description: "Content safety assessment"
      method: "Safety classifier"
      threshold: "< 0.8 triggers review"
      
    coherence_score:
      description: "Response coherence"
      method: "LLM-as-judge"
```

---

## Cost Optimization

### Cost Monitoring Framework

```yaml
cost_monitoring:
  tracking:
    api_costs:
      - provider: "OpenAI"
        models:
          gpt-4-turbo:
            input: 0.01  # per 1K tokens
            output: 0.03
          gpt-3.5-turbo:
            input: 0.0005
            output: 0.0015
            
    compute_costs:
      - resource: "GPU"
        hourly_rate: 3.50  # per hour
        
      - resource: "CPU"
        hourly_rate: 0.10
        
    storage_costs:
      - resource: "Logs"
        per_gb_month: 0.50
        
      - resource: "Metrics"
        per_gb_month: 0.10
        
  optimization_strategies:
    caching:
      description: "Cache identical prompts"
      potential_savings: "30-50% of API costs"
      implementation: "Redis cache with semantic similarity"
      
    model_selection:
      description: "Use cheaper models for simple tasks"
      potential_savings: "40-60% for simple queries"
      implementation: "Task classifier + model router"
      
    prompt_optimization:
      description: "Reduce token usage"
      potential_savings: "20-30% of token costs"
      implementation: "Prompt compression, few-shot reduction"
      
    batching:
      description: "Batch similar requests"
      potential_savings: "10-20% through efficiency"
      implementation: "Request queue + batch processing"
```

---

## Security Monitoring

### Security Event Tracking

```yaml
security_monitoring:
  authentication_events:
    - event: "login_success"
      level: "INFO"
      retention: "90 days"
      
    - event: "login_failure"
      level: "WARN"
      alert_threshold: "5 failures in 5 minutes"
      
    - event: "password_reset"
      level: "INFO"
      retention: "1 year"
      
  authorization_events:
    - event: "permission_denied"
      level: "WARN"
      alert_threshold: "10 per minute"
      
    - event: "role_changed"
      level: "INFO"
      retention: "1 year"
      
  data_access_events:
    - event: "sensitive_data_access"
      level: "INFO"
      retention: "1 year"
      
    - event: "data_export"
      level: "WARN"
      alert_threshold: "Any export"
      
  llm_specific_events:
    - event: "prompt_injection_detected"
      level: "CRITICAL"
      alert_threshold: "Immediate"
      
    - event: "content_filtered"
      level: "INFO"
      retention: "30 days"
      
    - event: "abuse_detected"
      level: "CRITICAL"
      alert_threshold: "Immediate"
```

---

## Implementation Checklist

### Monitoring Setup Checklist

```yaml
pre_deployment:
  metrics:
    - [ ] All services expose /metrics endpoint
    - [ ] Custom business metrics defined
    - [ ] Histogram buckets configured
    - [ ] Labels are low-cardinality
    - [ ] Metric naming follows conventions
    
  logging:
    - [ ] Structured logging implemented
    - [ ] Log levels configured
    - [ ] Sensitive data redacted
    - [ ] Log aggregation configured
    - [ ] Retention policies set
    
  tracing:
    - [ ] OpenTelemetry SDK integrated
    - [ ] Trace context propagation configured
    - [ ] Sampling rate appropriate
    - [ ] Exporter configured
    - [ ] Service name set
    
  alerting:
    - [ ] Critical alerts defined
    - [ ] Alert routing configured
    - [ ] Escalation policies in place
    - [ ] Runbooks documented
    - [ ] On-call schedule set
    
  dashboards:
    - [ ] Executive dashboard created
    - [ ] Operational dashboards created
    - [ ] Debug dashboards created
    - [ ] Alert panels included
    - [ ] Variables configured

post_deployment:
  validation:
    - [ ] Metrics flowing to Prometheus
    - [ ] Logs appearing in aggregation
    - [ ] Traces visible in Jaeger
    - [ ] Test alerts fire correctly
    - [ ] Dashboards render correctly
    
  optimization:
    - [ ] Alert thresholds tuned
    - [ ] Dashboard refresh rates set
    - [ ] Retention policies reviewed
    - [ ] Cost optimization applied
    - [ ] Documentation updated
```

---

## References

- OpenTelemetry Best Practices: https://opentelemetry.io/docs/
- Prometheus Best Practices: https://prometheus.io/docs/practices/
- Google SRE Workbook: https://sre.google/workbook/table-of-contents/
- Grafana Dashboard Design: https://grafana.com/docs/grafana/latest/

---

*Last Updated: January 2025*
*Version: 1.0.0*
