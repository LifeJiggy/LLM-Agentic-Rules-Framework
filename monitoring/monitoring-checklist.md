# Monitoring Checklist for AI/LLM Systems

## Comprehensive Verification Checks

---

## Table of Contents

1. [Checklist Overview](#checklist-overview)
2. [P0 Critical Checks](#p0-critical-checks)
3. [P1 High Priority Checks](#p1-high-priority-checks)
4. [P2 Medium Priority Checks](#p2-medium-priority-checks)
5. [P3 Low Priority Checks](#p3-low-priority-checks)
6. [Metrics Checklist](#metrics-checklist)
7. [Logging Checklist](#logging-checklist)
8. [Tracing Checklist](#tracing-checklist)
9. [Alerting Checklist](#alerting-checklist)
10. [Dashboard Checklist](#dashboard-checklist)
11. [Security Checklist](#security-checklist)
12. [Cost Monitoring Checklist](#cost-monitoring-checklist)
13. [LLM-Specific Checklist](#llm-specific-checklist)
14. [Pre-Deployment Checklist](#pre-deployment-checklist)
15. [Post-Deployment Checklist](#post-deployment-checklist)
16. [Incident Response Checklist](#incident-response-checklist)
17. [Review Schedule](#review-schedule)

---

## Checklist Overview

### Priority Levels

```yaml
priority_definitions:
  P0_Critical:
    description: "Must be complete before production deployment"
    timeframe: "Before go-live"
    owner: "Engineering Lead"
    examples:
      - "Basic health checks"
      - "Error rate monitoring"
      - "Critical alerting"
      
  P1_High:
    description: "Must be complete within first week of production"
    timeframe: "Week 1"
    owner: "SRE Team"
    examples:
      - "Distributed tracing"
      - "Log aggregation"
      - "Performance dashboards"
      
  P2_Medium:
    description: "Must be complete within first month"
    timeframe: "Month 1"
    owner: "Platform Team"
    examples:
      - "Cost monitoring"
      - "Advanced alerting"
      - "Capacity planning"
      
  P3_Low:
    description: "Should be complete within quarter"
    timeframe: "Quarter 1"
    owner: "DevOps Team"
    examples:
      - "AIOps integration"
      - "Predictive monitoring"
      - "Advanced analytics"
```

### Checklist Usage Guidelines

```yaml
usage_guidelines:
  frequency: "Review checklist before each deployment"
  responsible: "Engineering Lead owns checklist completion"
  documentation: "Mark items as complete with date and owner"
  exceptions: "Document any exceptions with justification"
  
  workflow:
    - "Before deployment: Complete P0 checks"
    - "Week 1: Complete P1 checks"
    - "Month 1: Complete P2 checks"
    - "Quarter 1: Complete P3 checks"
    
  sign_off:
    required: "Engineering Lead sign-off for P0"
    recommended: "SRE Lead sign-off for P1"
    optional: "Team Lead sign-off for P2/P3"
```

---

## P0 Critical Checks

### Service Health

```yaml
health_checks:
  - id: "P0-001"
    category: "Health"
    check: "Service exposes health endpoint"
    description: "Every service must have a /health or /healthz endpoint"
    verification: |
      curl -f http://service:8080/health
    expected: "HTTP 200 OK"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P0-002"
    category: "Health"
    check: "Health endpoint checks dependencies"
    description: "Health endpoint verifies database, cache, and external service connectivity"
    verification: |
      curl -s http://service:8080/health | jq '.dependencies'
    expected: "All dependencies report healthy"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P0-003"
    category: "Health"
    check: "Readiness probe configured"
    description: "Kubernetes readiness probe prevents traffic to unready pods"
    verification: |
      kubectl get deployment llm-service -o jsonpath='{.spec.template.spec.containers[0].readinessProbe}'
    expected: "Probe configuration exists"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P0-004"
    category: "Health"
    check: "Liveness probe configured"
    description: "Kubernetes liveness probe restarts unresponsive pods"
    verification: |
      kubectl get deployment llm-service -o jsonpath='{.spec.template.spec.containers[0].livenessProbe}'
    expected: "Probe configuration exists"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P0-005"
    category: "Health"
    check: "Startup probe configured"
    description: "Kubernetes startup probe handles slow-starting containers"
    verification: |
      kubectl get deployment llm-service -o jsonpath='{.spec.template.spec.containers[0].startupProbe}'
    expected: "Probe configuration exists"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
```

### Error Monitoring

```yaml
error_monitoring:
  - id: "P0-006"
    category: "Errors"
    check: "Error rate metric exposed"
    description: "Service exposes error rate metric"
    verification: |
      curl -s http://service:8080/metrics | grep "errors_total"
    expected: "Error counter metric exists"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P0-007"
    category: "Errors"
    check: "Error rate alert configured"
    description: "Alert fires when error rate exceeds threshold"
    verification: |
      curl -s http://prometheus:9090/api/v1/alerts | jq '.data.alerts[] | select(.labels.alertname=="HighErrorRate")'
    expected: "Alert rule exists"
    automatable: true
    owner: "SRE Team"
    status: "pending"
    
  - id: "P0-008"
    category: "Errors"
    check: "Error logging implemented"
    description: "Errors are logged with sufficient context"
    verification: |
      grep -r "logger.error" src/
    expected: "Error logging found in code"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P0-009"
    category: "Errors"
    check: "Error tracking integrated"
    description: "Sentry, Datadog, or similar error tracking configured"
    verification: |
      grep -r "sentry\|datadog\|bugsnag" src/
    expected: "Error tracking integration found"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P0-010"
    category: "Errors"
    check: "Error alerts notification configured"
    description: "Critical errors trigger immediate notifications"
    verification: |
      cat alertmanager.yml | grep -A 10 "receiver: 'pagerduty-critical'"
    expected: "PagerDuty integration configured"
    automatable: false
    owner: "SRE Team"
    status: "pending"
```

### Availability Monitoring

```yaml
availability_monitoring:
  - id: "P0-011"
    category: "Availability"
    check: "Uptime monitoring configured"
    description: "External uptime monitoring (Pingdom, UptimeRobot, etc.)"
    verification: |
      # Check monitoring service API
    expected: "Uptime check exists for service"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P0-012"
    category: "Availability"
    check: "SLA metrics defined"
    description: "Service Level Agreement metrics documented"
    verification: |
      cat docs/sla.md | grep -i "availability\|uptime"
    expected: "SLA targets documented"
    automatable: false
    owner: "Product Team"
    status: "pending"
    
  - id: "P0-013"
    category: "Availability"
    check: "Incident response process defined"
    description: "On-call rotation and escalation process documented"
    verification: |
      cat docs/oncall.md
    expected: "On-call schedule and escalation process exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P0-014"
    category: "Availability"
    check: "Backup and recovery procedures"
    description: "Data backup and recovery procedures documented"
    verification: |
      cat docs/backup-recovery.md
    expected: "Backup and recovery procedures exist"
    automatable: false
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P0-015"
    category: "Availability"
    check: "Disaster recovery plan"
    description: "Disaster recovery plan documented and tested"
    verification: |
      cat docs/disaster-recovery.md
    expected: "DR plan exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
```

---

## P1 High Priority Checks

### Distributed Tracing

```yaml
tracing_checks:
  - id: "P1-001"
    category: "Tracing"
    check: "OpenTelemetry SDK integrated"
    description: "Service uses OpenTelemetry for distributed tracing"
    verification: |
      grep -r "opentelemetry" requirements.txt package.json
    expected: "OpenTelemetry dependency found"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-002"
    category: "Tracing"
    check: "Trace context propagated"
    description: "W3C Trace Context headers propagated between services"
    verification: |
      # Check that traceparent header is forwarded
    expected: "Trace context propagation implemented"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-003"
    category: "Tracing"
    check: "Trace exporter configured"
    description: "Traces exported to Jaeger, Zipkin, or collector"
    verification: |
      grep -r "jaeger\|zipkin\|otlp" src/
    expected: "Trace exporter configured"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-004"
    category: "Tracing"
    check: "Sampling rate appropriate"
    description: "Sampling rate balances visibility and cost"
    verification: |
      grep -r "sampling" src/
    expected: "Sampling configuration found"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P1-005"
    category: "Tracing"
    check: "Span attributes defined"
    description: "Custom attributes added to spans for context"
    verification: |
      grep -r "set_attribute\|addTag" src/
    expected: "Custom span attributes found"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-006"
    category: "Tracing"
    check: "Trace visualization accessible"
    description: "Jaeger/Zipkin UI accessible and functional"
    verification: |
      curl -f http://jaeger:16686/health
    expected: "Trace UI is accessible"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
```

### Structured Logging

```yaml
logging_checks:
  - id: "P1-007"
    category: "Logging"
    check: "Structured logging implemented"
    description: "Logs are in JSON or structured format"
    verification: |
      grep -r "json.dumps\|JSONRenderer\|structlog" src/
    expected: "Structured logging implementation found"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-008"
    category: "Logging"
    check: "Log levels configured"
    description: "Appropriate log levels used (DEBUG, INFO, WARN, ERROR)"
    verification: |
      grep -r "logger.debug\|logger.info\|logger.warn\|logger.error" src/
    expected: "Multiple log levels used"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-009"
    category: "Logging"
    check: "Request ID in logs"
    description: "Every log entry includes request ID for correlation"
    verification: |
      grep -r "request_id\|trace_id" src/
    expected: "Request ID propagation found"
    automatable: false
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-010"
    category: "Logging"
    check: "Log aggregation configured"
    description: "Logs shipped to ELK, Loki, or CloudWatch"
    verification: |
      grep -r "elasticsearch\|loki\|cloudwatch" docker-compose.yml
    expected: "Log aggregation configured"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P1-011"
    category: "Logging"
    check: "Sensitive data redacted"
    description: "PII and secrets not logged"
    verification: |
      grep -r "password\|secret\|token" src/ | grep -v "redact\|mask\|sanitize"
    expected: "No sensitive data in logs"
    automatable: false
    owner: "Security Team"
    status: "pending"
    
  - id: "P1-012"
    category: "Logging"
    check: "Log retention policy configured"
    description: "Log retention configured per level"
    verification: |
      cat logstash/pipeline/llm-logs.conf | grep "retention"
    expected: "Retention policy configured"
    automatable: false
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P1-013"
    category: "Logging"
    check: "Log volume monitoring"
    description: "Log volume metrics exposed"
    verification: |
      curl -s http://service:8080/metrics | grep "log_volume"
    expected: "Log volume metrics exist"
    automatable: true
    owner: "SRE Team"
    status: "pending"
```

### Performance Metrics

```yaml
performance_checks:
  - id: "P1-014"
    category: "Performance"
    check: "Latency metrics exposed"
    description: "Request latency histogram exposed"
    verification: |
      curl -s http://service:8080/metrics | grep "latency\|duration"
    expected: "Latency metric exists"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-015"
    category: "Performance"
    check: "Throughput metrics exposed"
    description: "Requests per second metric exposed"
    verification: |
      curl -s http://service:8080/metrics | grep "requests_total"
    expected: "Request counter exists"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-016"
    category: "Performance"
    check: "Resource utilization metrics"
    description: "CPU, memory, disk metrics exposed"
    verification: |
      curl -s http://service:8080/metrics | grep "cpu\|memory\|disk"
    expected: "Resource metrics exist"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P1-017"
    category: "Performance"
    check: "Performance dashboard created"
    description: "Grafana dashboard with performance metrics"
    verification: |
      # Check Grafana API
    expected: "Performance dashboard exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P1-018"
    category: "Performance"
    check: "Performance alerts configured"
    description: "Alerts for high latency, low throughput"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name=="HighLatency")'
    expected: "Performance alerts exist"
    automatable: true
    owner: "SRE Team"
    status: "pending"
    
  - id: "P1-019"
    category: "Performance"
    check: "Performance baselines established"
    description: "Baseline metrics documented"
    verification: |
      cat docs/performance-baselines.md
    expected: "Baselines documented"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P1-020"
    category: "Performance"
    check: "Load testing completed"
    description: "Load testing results documented"
    verification: |
      cat docs/load-test-results.md
    expected: "Load test results exist"
    automatable: false
    owner: "QA Team"
    status: "pending"
```

---

## P2 Medium Priority Checks

### Cost Monitoring

```yaml
cost_checks:
  - id: "P2-001"
    category: "Cost"
    check: "API cost metrics exposed"
    description: "LLM API costs tracked per request"
    verification: |
      curl -s http://service:8080/metrics | grep "cost"
    expected: "Cost metrics exist"
    automatable: true
    owner: "Development Team"
    status: "pending"
    
  - id: "P2-002"
    category: "Cost"
    check: "Daily cost dashboard"
    description: "Dashboard showing daily/weekly/monthly costs"
    verification: |
      # Check Grafana API
    expected: "Cost dashboard exists"
    automatable: false
    owner: "Finance Team"
    status: "pending"
    
  - id: "P2-003"
    category: "Cost"
    check: "Cost alerts configured"
    description: "Alerts when cost exceeds budget"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Cost"))'
    expected: "Cost alerts exist"
    automatable: true
    owner: "SRE Team"
    status: "pending"
    
  - id: "P2-004"
    category: "Cost"
    check: "Cost allocation tags"
    description: "Costs attributed to teams/services"
    verification: |
      curl -s http://service:8080/metrics | grep "cost" | head -5
    expected: "Cost metrics have team/service labels"
    automatable: false
    owner: "Finance Team"
    status: "pending"
    
  - id: "P2-005"
    category: "Cost"
    check: "Budget thresholds defined"
    description: "Monthly budget and alert thresholds documented"
    verification: |
      cat docs/budget.md
    expected: "Budget and thresholds documented"
    automatable: false
    owner: "Finance Team"
    status: "pending"
    
  - id: "P2-006"
    category: "Cost"
    check: "Cost optimization strategies"
    description: "Cost optimization opportunities documented"
    verification: |
      cat docs/cost-optimization.md
    expected: "Optimization strategies documented"
    automatable: false
    owner: "Engineering Team"
    status: "pending"
    
  - id: "P2-007"
    category: "Cost"
    check: "Cost forecasting"
    description: "Cost projections based on trends"
    verification: |
      cat docs/cost-forecast.md
    expected: "Cost forecast exists"
    automatable: false
    owner: "Finance Team"
    status: "pending"
```

### Capacity Planning

```yaml
capacity_checks:
  - id: "P2-008"
    category: "Capacity"
    check: "Capacity metrics tracked"
    description: "Resource utilization trends monitored"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=capacity_used
    expected: "Capacity metrics exist"
    automatable: true
    owner: "SRE Team"
    status: "pending"
    
  - id: "P2-009"
    category: "Capacity"
    check: "Growth projections"
    description: "Usage growth projections documented"
    verification: |
      cat docs/capacity-plan.md
    expected: "Capacity plan exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P2-010"
    category: "Capacity"
    check: "Auto-scaling configured"
    description: "Horizontal pod autoscaler or similar configured"
    verification: |
      kubectl get hpa
    expected: "HPA configuration exists"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P2-011"
    category: "Capacity"
    check: "Resource limits set"
    description: "CPU and memory limits defined for all containers"
    verification: |
      kubectl get deployment llm-service -o jsonpath='{.spec.template.spec.containers[0].resources}'
    expected: "Resource limits configured"
    automatable: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P2-012"
    category: "Capacity"
    check: "Scaling policies defined"
    description: "Scaling policies documented"
    verification: |
      cat docs/scaling-policies.md
    expected: "Scaling policies exist"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P2-013"
    category: "Capacity"
    check: "Capacity alerts configured"
    description: "Alerts for capacity thresholds"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Capacity"))'
    expected: "Capacity alerts exist"
    automatable: true
    owner: "SRE Team"
    status: "pending"
```

### Security Monitoring

```yaml
security_checks:
  - id: "P2-014"
    category: "Security"
    check: "Authentication events logged"
    description: "Login attempts and failures logged"
    verification: |
      grep -r "auth\|login\|token" logs/
    expected: "Auth events in logs"
    automatable: false
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-015"
    category: "Security"
    check: "Authorization failures tracked"
    description: "Permission denied events logged and alerted"
    verification: |
      grep -r "permission_denied\|unauthorized" logs/
    expected: "Auth failures logged"
    automatable: false
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-016"
    category: "Security"
    check: "Security alerts configured"
    description: "Alerts for suspicious activity"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.labels.severity=="critical")'
    expected: "Security alerts exist"
    automatable: true
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-017"
    category: "Security"
    check: "Audit logging enabled"
    description: "Audit trail for data access"
    verification: |
      grep -r "audit" src/
    expected: "Audit logging found"
    automatable: false
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-018"
    category: "Security"
    check: "Secrets management"
    description: "Secrets not hardcoded, using vault/KMS"
    verification: |
      grep -r "AKIA\|password=" src/ | grep -v "test\|example"
    expected: "No hardcoded secrets"
    automatable: false
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-019"
    category: "Security"
    check: "Security scanning integrated"
    description: "SAST/DAST scanning configured"
    verification: |
      cat .github/workflows/security-scan.yml
    expected: "Security scanning configured"
    automatable: true
    owner: "Security Team"
    status: "pending"
    
  - id: "P2-020"
    category: "Security"
    check: "Incident response plan"
    description: "Security incident response plan documented"
    verification: |
      cat docs/security-incident-response.md
    expected: "Security incident response plan exists"
    automatable: false
    owner: "Security Team"
    status: "pending"
```

---

## P3 Low Priority Checks

### Advanced Monitoring

```yaml
advanced_checks:
  - id: "P3-001"
    category: "Advanced"
    check: "AIOps integration"
    description: "Machine learning-based anomaly detection"
    verification: |
      # Check for ML monitoring tools
    expected: "AIOps platform configured"
    automatable: false
    owner: "Platform Team"
    status: "pending"
    
  - id: "P3-002"
    category: "Advanced"
    check: "Predictive monitoring"
    description: "Predictive alerts for capacity issues"
    verification: |
      # Check for predictive analytics
    expected: "Predictive monitoring configured"
    automatable: false
    owner: "Platform Team"
    status: "pending"
    
  - id: "P3-003"
    category: "Advanced"
    check: "Custom dashboards"
    description: "Role-specific dashboards created"
    verification: |
      # Check Grafana API
    expected: "Multiple dashboard types exist"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P3-004"
    category: "Advanced"
    check: "Monitoring documentation"
    description: "Comprehensive monitoring guide"
    verification: |
      cat docs/monitoring-guide.md
    expected: "Monitoring documentation exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P3-005"
    category: "Advanced"
    check: "Runbook automation"
    description: "Automated runbook execution"
    verification: |
      grep -r "runbook\|playbook" src/
    expected: "Runbook automation found"
    automatable: false
    owner: "DevOps Team"
    status: "pending"
    
  - id: "P3-006"
    category: "Advanced"
    check: "Self-healing systems"
    description: "Automatic remediation configured"
    verification: |
      grep -r "self_heal\|auto_remediate" src/
    expected: "Self-healing configured"
    automatable: false
    owner: "Platform Team"
    status: "pending"
    
  - id: "P3-007"
    category: "Advanced"
    check: "Chaos engineering"
    description: "Chaos testing integrated"
    verification: |
      cat docs/chaos-engineering.md
    expected: "Chaos engineering plan exists"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P3-008"
    category: "Advanced"
    check: "Monitoring cost optimization"
    description: "Monitoring costs tracked and optimized"
    verification: |
      cat docs/monitoring-costs.md
    expected: "Monitoring costs documented"
    automatable: false
    owner: "Finance Team"
    status: "pending"
    
  - id: "P3-009"
    category: "Advanced"
    check: "Monitoring SLAs"
    description: "Monitoring system SLAs defined"
    verification: |
      cat docs/monitoring-sla.md
    expected: "Monitoring SLAs documented"
    automatable: false
    owner: "SRE Team"
    status: "pending"
    
  - id: "P3-010"
    category: "Advanced"
    check: "Monitoring training"
    description: "Team training on monitoring tools"
    verification: |
      cat docs/monitoring-training.md
    expected: "Training materials exist"
    automatable: false
    owner: "SRE Team"
    status: "pending"
```

---

## Metrics Checklist

### Core Metrics

```yaml
core_metrics:
  - id: "M-001"
    metric: "requests_total"
    type: "counter"
    description: "Total number of requests"
    labels: ["method", "endpoint", "status"]
    required: true
    owner: "Development Team"
    status: "pending"
    
  - id: "M-002"
    metric: "request_duration_seconds"
    type: "histogram"
    description: "Request latency distribution"
    labels: ["method", "endpoint"]
    buckets: [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    required: true
    owner: "Development Team"
    status: "pending"
    
  - id: "M-003"
    metric: "request_size_bytes"
    type: "histogram"
    description: "Request size distribution"
    labels: ["method", "endpoint"]
    required: false
    owner: "Development Team"
    status: "pending"
    
  - id: "M-004"
    metric: "response_size_bytes"
    type: "histogram"
    description: "Response size distribution"
    labels: ["method", "endpoint"]
    required: false
    owner: "Development Team"
    status: "pending"
    
  - id: "M-005"
    metric: "active_requests"
    type: "gauge"
    description: "Currently processing requests"
    labels: ["endpoint"]
    required: true
    owner: "Development Team"
    status: "pending"
    
  - id: "M-006"
    metric: "errors_total"
    type: "counter"
    description: "Total number of errors"
    labels: ["error_type", "endpoint"]
    required: true
    owner: "Development Team"
    status: "pending"
```

### LLM-Specific Metrics

```yaml
llm_metrics:
  - id: "LLM-001"
    metric: "llm_requests_total"
    type: "counter"
    description: "Total LLM API requests"
    labels: ["model", "provider", "status"]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-002"
    metric: "llm_tokens_total"
    type: "counter"
    description: "Total tokens processed"
    labels: ["model", "token_type"]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-003"
    metric: "llm_cost_dollars_total"
    type: "counter"
    description: "Total API cost"
    labels: ["model", "provider"]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-004"
    metric: "llm_latency_seconds"
    type: "histogram"
    description: "LLM response latency"
    labels: ["model", "provider"]
    buckets: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-005"
    metric: "llm_tokens_per_second"
    type: "gauge"
    description: "Generation throughput"
    labels: ["model"]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-006"
    metric: "llm_time_to_first_token_seconds"
    type: "histogram"
    description: "Time to first token"
    labels: ["model"]
    buckets: [0.1, 0.25, 0.5, 1.0, 2.0]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-007"
    metric: "llm_quality_score"
    type: "gauge"
    description: "Response quality assessment"
    labels: ["model"]
    required: false
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-008"
    metric: "llm_hallucination_rate"
    type: "gauge"
    description: "Detected hallucination rate"
    labels: ["model"]
    required: false
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-009"
    metric: "llm_safety_filtered_total"
    type: "counter"
    description: "Safety-filtered responses"
    labels: ["model", "filter_type"]
    required: true
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-010"
    metric: "llm_cache_hit_rate"
    type: "gauge"
    description: "Cache hit rate"
    labels: ["cache_type"]
    required: false
    owner: "AI Team"
    status: "pending"
```

### Infrastructure Metrics

```yaml
infrastructure_metrics:
  - id: "INF-001"
    metric: "cpu_usage_percent"
    type: "gauge"
    description: "CPU utilization"
    labels: ["instance"]
    required: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "INF-002"
    metric: "memory_usage_bytes"
    type: "gauge"
    description: "Memory utilization"
    labels: ["instance"]
    required: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "INF-003"
    metric: "disk_usage_percent"
    type: "gauge"
    description: "Disk utilization"
    labels: ["instance", "mount"]
    required: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "INF-004"
    metric: "network_io_bytes"
    type: "counter"
    description: "Network I/O"
    labels: ["instance", "interface", "direction"]
    required: true
    owner: "DevOps Team"
    status: "pending"
    
  - id: "INF-005"
    metric: "gpu_utilization_percent"
    type: "gauge"
    description: "GPU utilization"
    labels: ["instance", "gpu_id"]
    required: false
    owner: "AI Team"
    status: "pending"
    
  - id: "INF-006"
    metric: "gpu_memory_usage_bytes"
    type: "gauge"
    description: "GPU memory utilization"
    labels: ["instance", "gpu_id"]
    required: false
    owner: "AI Team"
    status: "pending"
```

---

## Logging Checklist

### Log Configuration

```yaml
log_configuration:
  - id: "LOG-001"
    check: "Structured logging format"
    description: "Logs in JSON or structured format"
    verification: |
      # Check log output format
    expected: "Structured logs"
    owner: "Development Team"
    status: "pending"
    
  - id: "LOG-002"
    check: "Log levels configured"
    description: "Appropriate log levels for each component"
    verification: |
      grep -r "LOG_LEVEL" .env*
    expected: "Log level configuration found"
    owner: "Development Team"
    status: "pending"
    
  - id: "LOG-003"
    check: "Log retention policy"
    description: "Log retention configured per level"
    verification: |
      # Check ELK/Loki retention settings
    expected: "Retention policy configured"
    owner: "DevOps Team"
    status: "pending"
    
  - id: "LOG-004"
    check: "Log rotation"
    description: "Log files rotated to prevent disk full"
    verification: |
      cat /etc/logrotate.d/*
    expected: "Log rotation configured"
    owner: "DevOps Team"
    status: "pending"
    
  - id: "LOG-005"
    check: "Sensitive data redaction"
    description: "PII and secrets not logged"
    verification: |
      grep -r "password\|secret\|token" logs/ | grep -v "redact\|mask"
    expected: "No sensitive data in logs"
    owner: "Security Team"
    status: "pending"
    
  - id: "LOG-006"
    check: "Log aggregation pipeline"
    description: "Log shipping configured"
    verification: |
      cat docker-compose.yml | grep -A 5 "logstash\|loki"
    expected: "Log pipeline configured"
    owner: "DevOps Team"
    status: "pending"
    
  - id: "LOG-007"
    check: "Log search capability"
    description: "Logs searchable in Kibana/Grafana"
    verification: |
      curl -f http://kibana:5601/api/status
    expected: "Kibana accessible"
    owner: "DevOps Team"
    status: "pending"
    
  - id: "LOG-008"
    check: "Log alerting"
    description: "Alerts based on log patterns"
    verification: |
      # Check for log-based alerts
    expected: "Log alerts configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "LOG-009"
    check: "Log documentation"
    description: "Log format and usage documented"
    verification: |
      cat docs/logging-guide.md
    expected: "Logging documentation exists"
    owner: "Development Team"
    status: "pending"
    
  - id: "LOG-010"
    check: "Log testing"
    description: "Log output verified in staging"
    verification: |
      # Check staging logs
    expected: "Logs verified in staging"
    owner: "QA Team"
    status: "pending"
```

---

## Tracing Checklist

### Trace Configuration

```yaml
trace_configuration:
  - id: "TRACE-001"
    check: "OpenTelemetry SDK installed"
    description: "OpenTelemetry dependencies added"
    verification: |
      grep -r "opentelemetry" requirements.txt package.json
    expected: "OpenTelemetry found"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-002"
    check: "Trace provider configured"
    description: "TracerProvider initialized with resource"
    verification: |
      grep -r "TracerProvider" src/
    expected: "TracerProvider configured"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-003"
    check: "Trace exporter configured"
    description: "Traces exported to backend"
    verification: |
      grep -r "jaeger\|zipkin\|otlp" src/
    expected: "Trace exporter configured"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-004"
    check: "Sampling rate set"
    description: "Appropriate sampling rate configured"
    verification: |
      grep -r "sampling\|Sampler" src/
    expected: "Sampling configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "TRACE-005"
    check: "Context propagation"
    description: "W3C Trace Context headers propagated"
    verification: |
      grep -r "traceparent\|tracestate" src/
    expected: "Context propagation implemented"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-006"
    check: "Span naming"
    description: "Spans have meaningful names"
    verification: |
      grep -r "start_span\|start_as_current_span" src/
    expected: "Spans with meaningful names"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-007"
    check: "Span attributes"
    description: "Custom attributes added to spans"
    verification: |
      grep -r "set_attribute\|addTag" src/
    expected: "Custom attributes found"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-008"
    check: "Span events"
    description: "Important events recorded in spans"
    verification: |
      grep -r "add_event\|log" src/
    expected: "Span events found"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-009"
    check: "Error recording"
    description: "Errors recorded in spans"
    verification: |
      grep -r "record_exception\|set_status" src/
    expected: "Error recording implemented"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-010"
    check: "Trace visualization"
    description: "Traces visible in Jaeger/Zipkin UI"
    verification: |
      # Check Jaeger UI
    expected: "Traces visible in UI"
    owner: "DevOps Team"
    status: "pending"
    
  - id: "TRACE-011"
    check: "Trace documentation"
    description: "Tracing setup documented"
    verification: |
      cat docs/tracing-guide.md
    expected: "Tracing documentation exists"
    owner: "Development Team"
    status: "pending"
    
  - id: "TRACE-012"
    check: "Trace testing"
    description: "Traces verified in staging"
    verification: |
      # Check staging traces
    expected: "Traces verified in staging"
    owner: "QA Team"
    status: "pending"
```

---

## Alerting Checklist

### Alert Configuration

```yaml
alert_configuration:
  - id: "ALERT-001"
    check: "Critical alerts defined"
    description: "Alerts for P0 issues configured"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.labels.severity=="critical")'
    expected: "Critical alerts exist"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-002"
    check: "Warning alerts defined"
    description: "Alerts for P1 issues configured"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.labels.severity=="warning")'
    expected: "Warning alerts exist"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-003"
    check: "Alert routing configured"
    description: "Alerts routed to appropriate channels"
    verification: |
      cat alertmanager.yml
    expected: "Alert routing configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-004"
    check: "Escalation policy defined"
    description: "Escalation path documented"
    verification: |
      cat docs/escalation.md
    expected: "Escalation policy exists"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-005"
    check: "On-call rotation"
    description: "On-call schedule configured"
    verification: |
      cat docs/oncall-schedule.md
    expected: "On-call schedule exists"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-006"
    check: "Alert descriptions"
    description: "Alerts have clear descriptions"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[].annotations.description'
    expected: "Descriptions present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-007"
    check: "Runbooks linked"
    description: "Alerts link to runbooks"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[].annotations.runbook'
    expected: "Runbook links present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-008"
    check: "Alert thresholds tested"
    description: "Alert thresholds validated"
    verification: |
      # Check for threshold testing
    expected: "Thresholds tested"
    owner: "QA Team"
    status: "pending"
    
  - id: "ALERT-009"
    check: "Alert noise analyzed"
    description: "False positive rate tracked"
    verification: |
      # Check alert metrics
    expected: "Alert noise metrics tracked"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-010"
    check: "Alert maintenance"
    description: "Regular alert review scheduled"
    verification: |
      cat docs/alert-review-cadence.md
    expected: "Review cadence documented"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-011"
    check: "PagerDuty integration"
    description: "PagerDuty integration configured"
    verification: |
      cat alertmanager.yml | grep "pagerduty"
    expected: "PagerDuty configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-012"
    check: "Slack integration"
    description: "Slack notification configured"
    verification: |
      cat alertmanager.yml | grep "slack"
    expected: "Slack configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-013"
    check: "Alert testing"
    description: "Alerts tested in staging"
    verification: |
      # Check staging alerts
    expected: "Alerts tested in staging"
    owner: "QA Team"
    status: "pending"
    
  - id: "ALERT-014"
    check: "Alert documentation"
    description: "Alerting setup documented"
    verification: |
      cat docs/alerting-guide.md
    expected: "Alerting documentation exists"
    owner: "SRE Team"
    status: "pending"
    
  - id: "ALERT-015"
    check: "Alert review process"
    description: "Process for reviewing and tuning alerts"
    verification: |
      cat docs/alert-tuning-process.md
    expected: "Alert review process exists"
    owner: "SRE Team"
    status: "pending"
```

---

## Dashboard Checklist

### Dashboard Configuration

```yaml
dashboard_configuration:
  - id: "DASH-001"
    check: "Executive dashboard"
    description: "High-level overview for leadership"
    verification: |
      # Check Grafana API
    expected: "Executive dashboard exists"
    owner: "Product Team"
    status: "pending"
    
  - id: "DASH-002"
    check: "Operational dashboard"
    description: "System health for SRE/DevOps"
    verification: |
      # Check Grafana API
    expected: "Operational dashboard exists"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-003"
    check: "Debug dashboard"
    description: "Detailed debugging view"
    verification: |
      # Check Grafana API
    expected: "Debug dashboard exists"
    owner: "Development Team"
    status: "pending"
    
  - id: "DASH-004"
    check: "Dashboard variables"
    description: "Filterable by environment, service, etc."
    verification: |
      # Check dashboard JSON
    expected: "Variables configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-005"
    check: "Dashboard permissions"
    description: "Appropriate access controls"
    verification: |
      # Check Grafana API
    expected: "Permissions configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-006"
    check: "Panel limit"
    description: "No more than 12 panels per dashboard"
    verification: |
      # Count panels in dashboard JSON
    expected: "Panel count <= 12"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-007"
    check: "Refresh rate"
    description: "Appropriate refresh rates"
    verification: |
      # Check dashboard settings
    expected: "Refresh rate configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-008"
    check: "Time range"
    description: "Default time range appropriate"
    verification: |
      # Check dashboard settings
    expected: "Time range configured"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-009"
    check: "Alert panels"
    description: "Alert status visible on dashboard"
    verification: |
      # Check dashboard JSON
    expected: "Alert panel exists"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-010"
    check: "Documentation"
    description: "Dashboard purpose documented"
    verification: |
      # Check dashboard description
    expected: "Description present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "DASH-011"
    check: "Dashboard testing"
    description: "Dashboards verified in staging"
    verification: |
      # Check staging dashboards
    expected: "Dashboards tested"
    owner: "QA Team"
    status: "pending"
    
  - id: "DASH-012"
    check: "Dashboard backup"
    description: "Dashboards backed up"
    verification: |
      cat docs/dashboard-backup.md
    expected: "Dashboard backup exists"
    owner: "DevOps Team"
    status: "pending"
```

---

## Security Checklist

### Authentication Monitoring

```yaml
auth_monitoring:
  - id: "SEC-001"
    check: "Login attempts logged"
    description: "All login attempts logged"
    verification: |
      grep -r "login\|authentication" logs/
    expected: "Login events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-002"
    check: "Failed logins tracked"
    description: "Failed login attempts tracked"
    verification: |
      grep -r "failed.*login\|invalid.*credentials" logs/
    expected: "Failed logins tracked"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-003"
    check: "Brute force detection"
    description: "Alerts for repeated failed attempts"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("BruteForce"))'
    expected: "Brute force alert exists"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-004"
    check: "Session monitoring"
    description: "Session creation/termination logged"
    verification: |
      grep -r "session.*create\|session.*destroy" logs/
    expected: "Session events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-005"
    check: "Privilege escalation alerts"
    description: "Alerts for privilege changes"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Privilege"))'
    expected: "Privilege alert exists"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-006"
    check: "MFA monitoring"
    description: "Multi-factor authentication events logged"
    verification: |
      grep -r "mfa\|two_factor" logs/
    expected: "MFA events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-007"
    check: "API key monitoring"
    description: "API key usage tracked"
    verification: |
      grep -r "api_key\|apikey" logs/
    expected: "API key events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-008"
    check: "Token validation"
    description: "JWT/token validation events logged"
    verification: |
      grep -r "token.*valid\|jwt" logs/
    expected: "Token events logged"
    owner: "Security Team"
    status: "pending"
```

### Data Access Monitoring

```yaml
data_access:
  - id: "SEC-009"
    check: "Data access logging"
    description: "Sensitive data access logged"
    verification: |
      grep -r "data.*access\|read.*sensitive" logs/
    expected: "Data access logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-010"
    check: "Export tracking"
    description: "Data export events tracked"
    verification: |
      grep -r "export\|download" logs/
    expected: "Export events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-011"
    check: "Anomalous access alerts"
    description: "Alerts for unusual data access patterns"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Anomalous"))'
    expected: "Anomalous access alert exists"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-012"
    check: "Audit trail"
    description: "Complete audit trail for compliance"
    verification: |
      grep -r "audit" logs/
    expected: "Audit events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-013"
    check: "Data retention"
    description: "Security logs retained per policy"
    verification: |
      # Check retention configuration
    expected: "Retention policy configured"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-014"
    check: "Encryption monitoring"
    description: "Encryption status tracked"
    verification: |
      grep -r "encrypt\|decrypt" logs/
    expected: "Encryption events logged"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-015"
    check: "Certificate monitoring"
    description: "TLS certificate expiry tracked"
    verification: |
      # Check certificate monitoring
    expected: "Certificate monitoring exists"
    owner: "Security Team"
    status: "pending"
    
  - id: "SEC-016"
    check: "Vulnerability scanning"
    description: "Vulnerability scan results tracked"
    verification: |
      cat docs/vulnerability-scan-results.md
    expected: "Vulnerability scan results exist"
    owner: "Security Team"
    status: "pending"
```

---

## Cost Monitoring Checklist

### Cost Tracking

```yaml
cost_tracking:
  - id: "COST-001"
    check: "API cost metrics"
    description: "LLM API costs tracked"
    verification: |
      curl -s http://service:8080/metrics | grep "cost"
    expected: "Cost metrics exist"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-002"
    check: "Compute cost metrics"
    description: "Compute resource costs tracked"
    verification: |
      curl -s http://service:8080/metrics | grep "compute_cost"
    expected: "Compute costs tracked"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-003"
    check: "Storage cost metrics"
    description: "Storage costs tracked"
    verification: |
      curl -s http://service:8080/metrics | grep "storage_cost"
    expected: "Storage costs tracked"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-004"
    check: "Cost attribution"
    description: "Costs attributed to teams/services"
    verification: |
      curl -s http://service:8080/metrics | grep "cost" | grep "team"
    expected: "Cost attribution labels"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-005"
    check: "Cost forecasting"
    description: "Cost projections based on trends"
    verification: |
      # Check forecasting system
    expected: "Cost forecasting configured"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-006"
    check: "Budget alerts"
    description: "Alerts when approaching budget"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Budget"))'
    expected: "Budget alert exists"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-007"
    check: "Anomaly alerts"
    description: "Alerts for unusual cost spikes"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("CostAnomaly"))'
    expected: "Cost anomaly alert exists"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-008"
    check: "Cost optimization alerts"
    description: "Alerts for optimization opportunities"
    verification: |
      curl -s http://prometheus:9090/api/v1/rules | jq '.data.rules[] | select(.name|contains("Optimization"))'
    expected: "Optimization alert exists"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-009"
    check: "Cost dashboard"
    description: "Cost visualization dashboard"
    verification: |
      # Check Grafana API
    expected: "Cost dashboard exists"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-010"
    check: "Cost reports"
    description: "Regular cost reports generated"
    verification: |
      ls reports/cost-*
    expected: "Cost reports exist"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-011"
    check: "Cost documentation"
    description: "Cost monitoring documented"
    verification: |
      cat docs/cost-monitoring.md
    expected: "Cost documentation exists"
    owner: "Finance Team"
    status: "pending"
    
  - id: "COST-012"
    check: "Cost review process"
    description: "Regular cost review meetings"
    verification: |
      cat docs/cost-review-process.md
    expected: "Cost review process exists"
    owner: "Finance Team"
    status: "pending"
```

---

## LLM-Specific Checklist

### Model Monitoring

```yaml
model_monitoring:
  - id: "LLM-CHK-001"
    check: "Model availability"
    description: "Monitor model API availability"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=up{job="llm-api"}
    expected: "Model availability metric exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-002"
    check: "Model latency"
    description: "Monitor model response time"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=llm_latency_seconds
    expected: "Model latency metric exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-003"
    check: "Token usage"
    description: "Track token consumption"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=llm_tokens_total
    expected: "Token usage metric exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-004"
    check: "Model errors"
    description: "Track model API errors"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=llm_errors_total
    expected: "Model error metric exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-005"
    check: "Rate limiting"
    description: "Track rate limit hits"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=llm_rate_limit_hits
    expected: "Rate limit metric exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-006"
    check: "Response quality scoring"
    description: "Automated quality assessment"
    verification: |
      grep -r "quality_score\|relevance" src/
    expected: "Quality scoring implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-007"
    check: "Hallucination detection"
    description: "Detect factually incorrect responses"
    verification: |
      grep -r "hallucination\|fact_check" src/
    expected: "Hallucination detection implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-008"
    check: "Safety filtering"
    description: "Block harmful content"
    verification: |
      grep -r "safety\|content_filter" src/
    expected: "Safety filtering implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-009"
    check: "User feedback tracking"
    description: "Track user satisfaction"
    verification: |
      grep -r "feedback\|rating" src/
    expected: "Feedback tracking implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-010"
    check: "A/B testing"
    description: "Compare model versions"
    verification: |
      grep -r "a_b_test\|experiment" src/
    expected: "A/B testing implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-011"
    check: "Model versioning"
    description: "Track model versions"
    verification: |
      grep -r "model_version\|version" src/
    expected: "Model versioning implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-012"
    check: "Drift detection"
    description: "Monitor model drift"
    verification: |
      grep -r "drift\|distribution" src/
    expected: "Drift detection implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-013"
    check: "Prompt monitoring"
    description: "Track prompt patterns"
    verification: |
      grep -r "prompt.*monitor\|prompt.*track" src/
    expected: "Prompt monitoring implemented"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-014"
    check: "Model documentation"
    description: "Monitoring setup documented"
    verification: |
      cat docs/llm-monitoring.md
    expected: "LLM monitoring documentation exists"
    owner: "AI Team"
    status: "pending"
    
  - id: "LLM-CHK-015"
    check: "Model testing"
    description: "Monitoring verified in staging"
    verification: |
      # Check staging LLM monitoring
    expected: "LLM monitoring tested"
    owner: "QA Team"
    status: "pending"
```

---

## Pre-Deployment Checklist

### Code Review

```yaml
code_review:
  - id: "PRE-001"
    check: "Metrics implemented"
    description: "All required metrics implemented"
    verification: |
      grep -r "Counter\|Histogram\|Gauge" src/
    expected: "Metrics found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-002"
    check: "Logging implemented"
    description: "Structured logging implemented"
    verification: |
      grep -r "logger\|logging" src/
    expected: "Logging found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-003"
    check: "Tracing implemented"
    description: "Distributed tracing implemented"
    verification: |
      grep -r "tracer\|trace" src/
    expected: "Tracing found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-004"
    check: "Error handling"
    description: "Proper error handling and logging"
    verification: |
      grep -r "try.*catch\|except\|error" src/
    expected: "Error handling found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-005"
    check: "Health endpoint"
    description: "Health check endpoint implemented"
    verification: |
      grep -r "health\|healthz" src/
    expected: "Health endpoint found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-006"
    check: "Prometheus metrics endpoint"
    description: "/metrics endpoint exposed"
    verification: |
      grep -r "\/metrics" src/
    expected: "Metrics endpoint found"
    owner: "Development Team"
    status: "pending"
    
  - id: "PRE-007"
    check: "Alert rules updated"
    description: "New alert rules added if needed"
    verification: |
      # Check for new alert rules
    expected: "Alert rules reviewed"
    owner: "SRE Team"
    status: "pending"
    
  - id: "PRE-008"
    check: "Dashboard updated"
    description: "Dashboard updated if needed"
    verification: |
      # Check dashboard changes
    expected: "Dashboard reviewed"
    owner: "SRE Team"
    status: "pending"
    
  - id: "PRE-009"
    check: "Runbooks updated"
    description: "Runbooks updated for new features"
    verification: |
      # Check runbook updates
    expected: "Runbooks reviewed"
    owner: "SRE Team"
    status: "pending"
    
  - id: "PRE-010"
    check: "Monitoring documentation"
    description: "Monitoring setup documented"
    verification: |
      cat docs/monitoring-changes.md
    expected: "Monitoring changes documented"
    owner: "Development Team"
    status: "pending"
```

---

## Post-Deployment Checklist

### Validation

```yaml
validation:
  - id: "POST-001"
    check: "Metrics flowing"
    description: "Metrics appearing in Prometheus"
    verification: |
      curl -s http://prometheus:9090/api/v1/query?query=up{job="llm-service"}
    expected: "Metrics present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-002"
    check: "Logs aggregating"
    description: "Logs appearing in ELK/Loki"
    verification: |
      # Check log aggregation system
    expected: "Logs present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-003"
    check: "Traces visible"
    description: "Traces appearing in Jaeger"
    verification: |
      # Check Jaeger UI
    expected: "Traces present"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-004"
    check: "Alerts firing"
    description: "Test alerts fire correctly"
    verification: |
      # Trigger test alert
    expected: "Test alert received"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-005"
    check: "Dashboard rendering"
    description: "Dashboards display correctly"
    verification: |
      # Check Grafana dashboards
    expected: "Dashboards render correctly"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-006"
    check: "Performance baseline"
    description: "Performance baseline established"
    verification: |
      # Check baseline metrics
    expected: "Baseline established"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-007"
    check: "Error rate baseline"
    description: "Error rate baseline established"
    verification: |
      # Check error rate metrics
    expected: "Error baseline established"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-008"
    check: "Latency baseline"
    description: "Latency baseline established"
    verification: |
      # Check latency metrics
    expected: "Latency baseline established"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-009"
    check: "Cost baseline"
    description: "Cost baseline established"
    verification: |
      # Check cost metrics
    expected: "Cost baseline established"
    owner: "Finance Team"
    status: "pending"
    
  - id: "POST-010"
    check: "Documentation updated"
    description: "Monitoring documentation updated"
    verification: |
      cat docs/monitoring.md
    expected: "Documentation updated"
    owner: "Development Team"
    status: "pending"
    
  - id: "POST-011"
    check: "Incident response tested"
    description: "Incident response process validated"
    verification: |
      # Check incident response test
    expected: "Incident response tested"
    owner: "SRE Team"
    status: "pending"
    
  - id: "POST-012"
    check: "Rollback plan verified"
    description: "Rollback plan tested"
    verification: |
      # Check rollback test
    expected: "Rollback plan verified"
    owner: "DevOps Team"
    status: "pending"
```

---

## Incident Response Checklist

### During Incident

```yaml
during_incident:
  - id: "INC-001"
    check: "Acknowledge alert"
    description: "Acknowledge alert within SLA"
    verification: |
      # Check alert acknowledgment
    expected: "Alert acknowledged"
    owner: "On-Call Engineer"
    status: "pending"
    
  - id: "INC-002"
    check: "Assess impact"
    description: "Determine incident severity"
    verification: |
      # Check incident severity
    expected: "Severity assessed"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-003"
    check: "Notify stakeholders"
    description: "Notify affected stakeholders"
    verification: |
      # Check notification status
    expected: "Stakeholders notified"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-004"
    check: "Begin investigation"
    description: "Start investigation process"
    verification: |
      # Check investigation status
    expected: "Investigation started"
    owner: "On-Call Engineer"
    status: "pending"
    
  - id: "INC-005"
    check: "Document actions"
    description: "Document all actions taken"
    verification: |
      # Check incident documentation
    expected: "Actions documented"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-006"
    check: "Communicate status"
    description: "Regular status updates"
    verification: |
      # Check status updates
    expected: "Status updates provided"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-007"
    check: "Escalate if needed"
    description: "Escalate to appropriate team"
    verification: |
      # Check escalation
    expected: "Escalation handled"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-008"
    check: "Implement mitigation"
    description: "Implement temporary mitigation"
    verification: |
      # Check mitigation actions
    expected: "Mitigation implemented"
    owner: "On-Call Engineer"
    status: "pending"
```

### Post-Incident

```yaml
post_incident:
  - id: "INC-009"
    check: "Resolve incident"
    description: "Incident resolved and service restored"
    verification: |
      # Check service health
    expected: "Service restored"
    owner: "On-Call Engineer"
    status: "pending"
    
  - id: "INC-010"
    check: "Post-mortem scheduled"
    description: "Post-mortem meeting scheduled"
    verification: |
      # Check calendar
    expected: "Post-mortem scheduled"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-011"
    check: "Root cause identified"
    description: "Root cause identified and documented"
    verification: |
      # Check incident report
    expected: "Root cause documented"
    owner: "Engineering Lead"
    status: "pending"
    
  - id: "INC-012"
    check: "Action items created"
    description: "Preventive action items created"
    verification: |
      # Check issue tracker
    expected: "Action items created"
    owner: "Engineering Lead"
    status: "pending"
    
  - id: "INC-013"
    check: "Monitoring updated"
    description: "Monitoring improved based on incident"
    verification: |
      # Check monitoring changes
    expected: "Monitoring updated"
    owner: "SRE Team"
    status: "pending"
    
  - id: "INC-014"
    check: "Runbooks updated"
    description: "Runbooks updated based on incident"
    verification: |
      # Check runbook updates
    expected: "Runbooks updated"
    owner: "SRE Team"
    status: "pending"
    
  - id: "INC-015"
    check: "Documentation updated"
    description: "Incident documented"
    verification: |
      # Check incident documentation
    expected: "Incident documented"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-016"
    check: "Team debrief"
    description: "Team debrief completed"
    verification: |
      # Check debrief
    expected: "Debrief completed"
    owner: "Incident Commander"
    status: "pending"
    
  - id: "INC-017"
    check: "Metrics tracked"
    description: "Incident metrics tracked"
    verification: |
      # Check incident metrics
    expected: "Metrics tracked"
    owner: "SRE Team"
    status: "pending"
    
  - id: "INC-018"
    check: "Lessons learned"
    description: "Lessons learned documented"
    verification: |
      # Check lessons learned
    expected: "Lessons learned documented"
    owner: "Engineering Lead"
    status: "pending"
```

---

## Review Schedule

### Regular Reviews

```yaml
review_schedule:
  daily:
    - "Review alerts from last 24 hours"
    - "Check error rates and latency"
    - "Review cost metrics"
    owner: "SRE Team"
    frequency: "Every morning"
    
  weekly:
    - "Review alert noise and false positives"
    - "Review dashboard effectiveness"
    - "Review runbook execution"
    owner: "SRE Team"
    frequency: "Every Monday"
    
  monthly:
    - "Review monitoring coverage"
    - "Review alert thresholds"
    - "Review cost optimization opportunities"
    - "Review capacity planning"
    owner: "SRE Team"
    frequency: "First Monday of month"
    
  quarterly:
    - "Review monitoring strategy"
    - "Review tooling effectiveness"
    - "Review documentation"
    - "Review team training needs"
    owner: "SRE Lead"
    frequency: "First month of quarter"
    
  annually:
    - "Comprehensive monitoring audit"
    - "Tooling evaluation"
    - "Budget review"
    - "Strategy alignment"
    owner: "VP Engineering"
    frequency: "Q1"
```

### Review Documentation

```yaml
review_documentation:
  required_documents:
    - "Monitoring Strategy Review"
    - "Alert Effectiveness Report"
    - "Cost Optimization Report"
    - "Capacity Planning Review"
    - "Incident Response Review"
    
  templates:
    - "Weekly Monitoring Review Template"
    - "Monthly Monitoring Report Template"
    - "Quarterly Monitoring Audit Template"
    
  storage:
    location: "docs/monitoring-reviews/"
    format: "Markdown"
    retention: "2 years"
```

---

## References

- SRE Book: https://sre.google/sre-book/table-of-contents/
- OpenTelemetry: https://opentelemetry.io/docs/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/

---

*Last Updated: January 2025*
*Version: 1.0.0*
