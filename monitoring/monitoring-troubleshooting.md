# Monitoring Troubleshooting for AI/LLM Systems

## Common Issues and Solutions

---

## Table of Contents

1. [Missing Metrics](#missing-metrics)
2. [Alert Fatigue Issues](#alert-fatigue-issues)
3. [Trace Gaps](#trace-gaps)
4. [Log Storage Issues](#log-storage-issues)
5. [Dashboard Performance](#dashboard-performance)
6. [Prometheus Issues](#prometheus-issues)
7. [Grafana Issues](#grafana-issues)
8. [Jaeger Issues](#jaeger-issues)
9. [ELK Stack Issues](#elk-stack-issues)
10. [Alertmanager Issues](#alertmanager-issues)
11. [Performance Optimization](#performance-optimization)
12. [Debugging Playbooks](#debugging-playbooks)

---

## Missing Metrics

### Common Symptoms

```yaml
symptoms:
  - "Metrics not appearing in Prometheus"
  - "Grafana dashboards show 'No data'"
  - "Alerts not firing when expected"
  - "Incomplete metric labels"
  - "Metric values are stale"
```

### Diagnosis Steps

```yaml
diagnosis:
  step_1:
    action: "Check service health"
    command: |
      # Check if service is running
      kubectl get pods -l app=llm-service
      
      # Check service endpoint
      curl -f http://llm-service:8080/health
      
    expected: "Service is healthy and responding"
    
  step_2:
    action: "Check metrics endpoint"
    command: |
      # Check if metrics endpoint is exposed
      curl -s http://llm-service:8080/metrics | head -20
      
    expected: "Metrics are being exposed"
    
  step_3:
    action: "Check Prometheus targets"
    command: |
      # Check Prometheus targets
      curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job=="llm-service")'
      
    expected: "Target is up and scraping"
    
  step_4:
    action: "Check Prometheus queries"
    command: |
      # Query specific metric
      curl -s 'http://prometheus:9090/api/v1/query?query=llm_requests_total' | jq '.data.result'
      
    expected: "Metric data exists"
    
  step_5:
    action: "Check metric labels"
    command: |
      # Check available label values
      curl -s 'http://prometheus:9090/api/v1/label/__name__/values' | jq '.data[] | select(startswith("llm_"))'
      
    expected: "Expected metrics exist"
```

### Common Causes and Fixes

```yaml
causes:
  metrics_not_exposed:
    description: "Service doesn't expose /metrics endpoint"
    symptoms:
      - "curl to /metrics returns 404"
      - "No metrics in Prometheus"
    fix: |
      # Add metrics endpoint to service
      from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
      
      @app.get("/metrics")
      def metrics():
          return Response(
              generate_latest(),
              media_type=CONTENT_TYPE_LATEST
          )
      
  prometheus_not_scraping:
    description: "Prometheus not configured to scrape service"
    symptoms:
      - "Target shows as 'down' in Prometheus"
      - "Scrape errors in Prometheus logs"
    fix: |
      # Add scrape config to prometheus.yml
      scrape_configs:
        - job_name: 'llm-service'
          static_configs:
            - targets: ['llm-service:8080']
          scrape_interval: 10s
      
  wrong_port:
    description: "Prometheus scraping wrong port"
    symptoms:
      - "Connection refused errors"
      - "Target down"
    fix: |
      # Verify port in scrape config matches service
      kubectl get svc llm-service -o jsonpath='{.spec.ports[0].port}'
      
  firewall_blocking:
    description: "Firewall blocking Prometheus scraping"
    symptoms:
      - "Scrape timeouts"
      - "Connection refused"
    fix: |
      # Check network policies
      kubectl get networkpolicies
      
      # Add allow rule for Prometheus
      kubectl apply -f - <<EOF
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
        name: allow-prometheus-scrape
      spec:
        podSelector:
          matchLabels:
            app: llm-service
        ingress:
        - from:
          - podSelector:
              matchLabels:
                app: prometheus
          ports:
          - port: 8080
      EOF
      
  metric_cardinality_too_high:
    description: "Too many label combinations"
    symptoms:
      - "Prometheus memory usage high"
      - "Scrape timeouts"
      - "Query performance degraded"
    fix: |
      # Reduce label cardinality
      # Use recording rules for complex queries
      
      # Check current cardinality
      curl -s 'http://prometheus:9090/api/v1/label/__name__/values' | jq 'length'
      
  metric_naming_wrong:
    description: "Metric names don't match queries"
    symptoms:
      - "Queries return no data"
      - "Dashboards show 'No data'"
    fix: |
      # Check metric names
      curl -s 'http://prometheus:9090/api/v1/label/__name__/values' | jq '.data'
      
      # Update queries to match actual metric names
```

### Troubleshooting Script

```python
# troubleshooting/check_metrics.py
import requests
import json
from typing import Dict, List, Any

class MetricsTroubleshooter:
    """Troubleshoot missing metrics"""
    
    def __init__(self, prometheus_url: str, service_url: str):
        self.prometheus_url = prometheus_url
        self.service_url = service_url
        
    def check_service_health(self) -> Dict[str, Any]:
        """Check if service is healthy"""
        try:
            response = requests.get(f"{self.service_url}/health", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                "status": "unreachable",
                "error": str(e)
            }
            
    def check_metrics_endpoint(self) -> Dict[str, Any]:
        """Check if metrics endpoint is accessible"""
        try:
            response = requests.get(f"{self.service_url}/metrics", timeout=5)
            metrics = response.text.split('\n')
            return {
                "accessible": True,
                "metric_count": len([m for m in metrics if not m.startswith('#')]),
                "sample_metrics": metrics[:5]
            }
        except Exception as e:
            return {
                "accessible": False,
                "error": str(e)
            }
            
    def check_prometheus_target(self, job_name: str) -> Dict[str, Any]:
        """Check if Prometheus is scraping the target"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/targets",
                timeout=5
            )
            targets = response.json()["data"]["activeTargets"]
            
            for target in targets:
                if target["labels"].get("job") == job_name:
                    return {
                        "found": True,
                        "health": target["health"],
                        "last_scrape": target["lastScrape"],
                        "scrape_duration": target["lastScrapeDuration"],
                        "error": target.get("lastError", "")
                    }
                    
            return {"found": False}
        except Exception as e:
            return {"error": str(e)}
            
    def check_metric_exists(self, metric_name: str) -> Dict[str, Any]:
        """Check if metric exists in Prometheus"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/query",
                params={"query": metric_name},
                timeout=5
            )
            results = response.json()["data"]["result"]
            return {
                "exists": len(results) > 0,
                "series_count": len(results),
                "sample_values": [r["value"][1] for r in results[:3]]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def run_diagnostics(self, job_name: str, metric_name: str) -> Dict[str, Any]:
        """Run full diagnostics"""
        results = {
            "service_health": self.check_service_health(),
            "metrics_endpoint": self.check_metrics_endpoint(),
            "prometheus_target": self.check_prometheus_target(job_name),
            "metric_exists": self.check_metric_exists(metric_name)
        }
        
        # Add recommendations
        recommendations = []
        
        if results["service_health"]["status"] != "healthy":
            recommendations.append("Service is not healthy - check service logs")
            
        if not results["metrics_endpoint"].get("accessible"):
            recommendations.append("Metrics endpoint not accessible - check service configuration")
            
        if results["prometheus_target"].get("health") != "up":
            recommendations.append("Prometheus target is down - check network and scrape config")
            
        if not results["metric_exists"].get("exists"):
            recommendations.append("Metric not found - check metric naming and instrumentation")
            
        results["recommendations"] = recommendations
        
        return results

# Usage
troubleshooter = MetricsTroubleshooter(
    prometheus_url="http://localhost:9090",
    service_url="http://localhost:8080"
)

results = troubleshooter.run_diagnostics(
    job_name="llm-service",
    metric_name="llm_requests_total"
)

print(json.dumps(results, indent=2))
```

---

## Alert Fatigue Issues

### Common Symptoms

```yaml
symptoms:
  - "Alerts firing too frequently"
  - "Team ignores alerts"
  - "False positives increasing"
  - "Alert response time degrading"
  - "Same alert fires multiple times per day"
```

### Diagnosis Steps

```yaml
diagnosis:
  step_1:
    action: "Analyze alert volume"
    command: |
      # Count alerts by day
      curl -s 'http://prometheus:9090/api/v1/query?query=count(increase(alerts_fired_total[24h]))' | jq '.data.result'
      
    expected: "Understand current alert volume"
    
  step_2:
    action: "Identify noisy alerts"
    command: |
      # Find alerts that fire most frequently
      curl -s 'http://prometheus:9090/api/v1/query?query=topk(10, count by (alertname) (increase(alerts_fired_total[24h])))' | jq '.data.result'
      
    expected: "Identify top 10 most frequent alerts"
    
  step_3:
    action: "Check alert durations"
    command: |
      # Find alerts that fire for long durations
      curl -s 'http://prometheus:9090/api/v1/query?query=topk(10, alert_duration_seconds)' | jq '.data.result'
      
    expected: "Identify long-running alerts"
    
  step_4:
    action: "Review alert thresholds"
    command: |
      # Compare alert thresholds to actual values
      curl -s 'http://prometheus:9090/api/v1/rules' | jq '.data.rules[] | select(.type=="alerting") | {name: .name, query: .query, duration: .duration}'
      
    expected: "Review threshold settings"
    
  step_5:
    action: "Check false positive rate"
    command: |
      # Calculate alert resolution time
      # Fast resolution = likely false positive
      
    expected: "Identify false positives"
```

### Common Causes and Fixes

```yaml
causes:
  threshold_too_sensitive:
    description: "Alert threshold too close to normal variation"
    symptoms:
      - "Alerts fire during normal traffic spikes"
      - "Alerts fire during batch processing"
    fix: |
      # Update alert to use sustained threshold
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(llm_latency_seconds_bucket[5m]))
          >
          2 * llm:latency:p99:baseline
        for: "10m"  # Must be sustained for 10 minutes
        
  no_baselines:
    description: "Static thresholds without understanding normal patterns"
    symptoms:
      - "Alerts fire at different times of day"
      - "Alerts fire on weekends"
    fix: |
      # Create recording rules for baselines
      - record: llm:latency:p99:baseline
        expr: |
          avg_over_time(
            histogram_quantile(0.99, rate(llm_latency_seconds_bucket[5m]))[7d:5m]
          )
          
  too_many_alerts:
    description: "More alerts than humans can process"
    symptoms:
      - "Alert channel has 50+ messages per day"
      - "Team stops checking alerts"
    fix: |
      # Consolidate related alerts
      groups:
        - name: llm_alerts
          rules:
            - alert: LLMServiceIssue
              expr: |
                up{job="llm-service"} == 0
                or
                llm:errors:rate5m > 0.1
                or
                llm:latency:p99:5m > 5
              for: "5m"
              
  no_escalation:
    description: "Alerts without clear response process"
    symptoms:
      - "Alerts acknowledged but not acted on"
      - "No clear owner for alerts"
    fix: |
      # Add escalation and runbook links
      annotations:
        runbook: "https://wiki/runbooks/high-latency"
        escalation: "After 15 minutes, page on-call"
        
  alert_noise:
    description: "Alerts that don't require action"
    symptoms:
      - "Same alert fires multiple times per day"
      - "Team dismisses alerts without investigation"
    fix: |
      # Add inhibition rules
      inhibit_rules:
        - source_match:
            severity: 'critical'
          target_match:
            severity: 'warning'
          equal: ['alertname', 'instance']
```

### Alert Fatigue Reduction Script

```python
# troubleshooting/alert_fatigue_analyzer.py
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class AlertFatigueAnalyzer:
    """Analyze and reduce alert fatigue"""
    
    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url
        
    def get_alert_volume(self, days: int = 7) -> Dict[str, Any]:
        """Get alert volume over time"""
        try:
            # Get all alerts
            response = requests.get(
                f"{self.prometheus_url}/api/v1/alerts",
                timeout=5
            )
            alerts = response.json()["data"]["alerts"]
            
            # Count by alertname
            alert_counts = {}
            for alert in alerts:
                name = alert["labels"].get("alertname", "unknown")
                alert_counts[name] = alert_counts.get(name, 0) + 1
                
            return {
                "total_alerts": len(alerts),
                "by_alertname": alert_counts,
                "top_5": sorted(
                    alert_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def identify_noisy_alerts(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Identify alerts that fire too frequently"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/alerts",
                timeout=5
            )
            alerts = response.json()["data"]["alerts"]
            
            # Count by alertname
            alert_counts = {}
            for alert in alerts:
                name = alert["labels"].get("alertname", "unknown")
                if name not in alert_counts:
                    alert_counts[name] = {
                        "count": 0,
                        "first_seen": alert["activeAt"],
                        "last_seen": alert["activeAt"]
                    }
                alert_counts[name]["count"] += 1
                alert_counts[name]["last_seen"] = max(
                    alert_counts[name]["last_seen"],
                    alert["activeAt"]
                )
                
            # Find noisy alerts
            noisy_alerts = [
                {"name": name, **info}
                for name, info in alert_counts.items()
                if info["count"] >= threshold
            ]
            
            return sorted(noisy_alerts, key=lambda x: x["count"], reverse=True)
        except Exception as e:
            return [{"error": str(e)}]
            
    def analyze_false_positives(self) -> Dict[str, Any]:
        """Analyze potential false positives"""
        try:
            # Get alert rules
            response = requests.get(
                f"{self.prometheus_url}/api/v1/rules",
                timeout=5
            )
            rules = response.json()["data"]["rules"]
            
            # Analyze each rule
            analysis = []
            for rule in rules:
                if rule["type"] == "alerting":
                    # Check how often it fires
                    query = rule["query"]
                    
                    # Get current value
                    value_response = requests.get(
                        f"{self.prometheus_url}/api/v1/query",
                        params={"query": query},
                        timeout=5
                    )
                    current_value = value_response.json()["data"]["result"]
                    
                    analysis.append({
                        "name": rule["name"],
                        "query": query,
                        "duration": rule["duration"],
                        "current_value": current_value,
                        "is_firing": rule["state"] == "firing"
                    })
                    
            return {"rules": analysis}
        except Exception as e:
            return {"error": str(e)}
            
    def recommend_optimizations(self) -> List[Dict[str, Any]]:
        """Recommend alert optimizations"""
        recommendations = []
        
        # Get noisy alerts
        noisy = self.identify_noisy_alerts(threshold=10)
        for alert in noisy:
            recommendations.append({
                "type": "consolidate",
                "alert": alert["name"],
                "reason": f"Fires {alert['count']} times",
                "action": "Consider consolidating with related alerts or increasing duration"
            })
            
        # Check for alerts without duration
        rules = self.analyze_false_positives()
        for rule in rules.get("rules", []):
            if rule["duration"] == "0s":
                recommendations.append({
                    "type": "add_duration",
                    "alert": rule["name"],
                    "reason": "No duration specified",
                    "action": "Add 'for' clause to require sustained threshold"
                })
                
        return recommendations

# Usage
analyzer = AlertFatigueAnalyzer("http://localhost:9090")

# Get alert volume
volume = analyzer.get_alert_volume()
print(f"Total alerts: {volume.get('total_alerts', 0)}")
print(f"Top 5: {volume.get('top_5', [])}")

# Get recommendations
recommendations = analyzer.recommend_optimizations()
for rec in recommendations:
    print(f"{rec['type']}: {rec['alert']} - {rec['action']}")
```

---

## Trace Gaps

### Common Symptoms

```yaml
symptoms:
  - "Incomplete traces in Jaeger"
  - "Missing spans from some services"
  - "Trace context not propagated"
  - "Spans not correlated"
  - "Trace sampling too aggressive"
```

### Diagnosis Steps

```yaml
diagnosis:
  step_1:
    action: "Check Jaeger connectivity"
    command: |
      # Check Jaeger is running
      curl -f http://jaeger:16686/health
      
      # Check Jaeger UI
      curl -s http://jaeger:16686/api/services | jq '.data'
      
    expected: "Jaeger is healthy and has services"
    
  step_2:
    action: "Check trace propagation"
    command: |
      # Check if trace headers are being propagated
      # Look for traceparent header in requests
      
    expected: "Trace context is being propagated"
    
  step_3:
    action: "Check sampling rate"
    command: |
      # Check sampling configuration
      # Verify sampling rate is appropriate
      
    expected: "Sampling rate is configured correctly"
    
  step_4:
    action: "Check span creation"
    command: |
      # Check if spans are being created
      # Look for tracer initialization
      
    expected: "Spans are being created"
    
  step_5:
    action: "Check span export"
    command: |
      # Check if spans are being exported
      # Look for exporter configuration
      
    expected: "Spans are being exported to Jaeger"
```

### Common Causes and Fixes

```yaml
causes:
  trace_context_not_propagated:
    description: "Trace context not passed between services"
    symptoms:
      - "Spans from different services not connected"
      - "Multiple root spans for single request"
    fix: |
      # Ensure W3C Trace Context headers are propagated
      # Check middleware configuration
      
      # Python example
      from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
      
      FastAPIInstrumentor.instrument()
      
      # Node.js example
      const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
      const provider = new NodeTracerProvider();
      provider.register();
      
  sampling_too_aggressive:
    description: "Sampling rate too low"
    symptoms:
      - "Few traces in Jaeger"
      - "Missing traces for some requests"
    fix: |
      # Increase sampling rate
      sampling:
        default_strategy:
          type: probabilistic
          param: 0.5  # Sample 50% of traces
          
  exporter_not_configured:
    description: "Trace exporter not set up"
    symptoms:
      - "No traces in Jaeger"
      - "Spans not appearing"
    fix: |
      # Configure trace exporter
      from opentelemetry.exporter.jaeger.thrift import JaegerExporter
      
      jaeger_exporter = JaegerExporter(
          agent_host_name="localhost",
          agent_port=6831,
      )
      
      provider.add_span_processor(
          BatchSpanProcessor(jaeger_exporter)
      )
      
  service_not_instrumented:
    description: "Service not using OpenTelemetry"
    symptoms:
      - "No spans from specific service"
      - "Service not in Jaeger"
    fix: |
      # Add OpenTelemetry to service
      # Install dependencies
      pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger
      
      # Initialize tracer
      from opentelemetry import trace
      from opentelemetry.sdk.trace import TracerProvider
      
      provider = TracerProvider()
      trace.set_tracer_provider(provider)
      
  span_attributes_missing:
    description: "Spans lack useful attributes"
    symptoms:
      - "Traces not useful for debugging"
      - "Missing context in spans"
    fix: |
      # Add custom attributes to spans
      from opentelemetry import trace
      
      tracer = trace.get_tracer("llm-service")
      
      with tracer.start_as_current_span("llm_request") as span:
          span.set_attribute("llm.model", "gpt-4")
          span.set_attribute("llm.tokens", 500)
```

### Trace Gap Fix Script

```python
# troubleshooting/trace_fixer.py
import requests
from typing import Dict, List, Any
import json

class TraceGapFixer:
    """Diagnose and fix trace gaps"""
    
    def __init__(self, jaeger_url: str, prometheus_url: str):
        self.jaeger_url = jaeger_url
        self.prometheus_url = prometheus_url
        
    def check_jaeger_health(self) -> Dict[str, Any]:
        """Check Jaeger health"""
        try:
            response = requests.get(f"{self.jaeger_url}/health", timeout=5)
            return {"healthy": response.status_code == 200}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
            
    def get_services(self) -> List[str]:
        """Get services with traces"""
        try:
            response = requests.get(
                f"{self.jaeger_url}/api/services",
                timeout=5
            )
            return response.json()["data"]
        except Exception as e:
            return []
            
    def get_traces_for_service(
        self,
        service: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent traces for a service"""
        try:
            response = requests.get(
                f"{self.jaeger_url}/api/traces",
                params={
                    "service": service,
                    "limit": limit
                },
                timeout=5
            )
            return response.json()["data"]
        except Exception as e:
            return []
            
    def analyze_trace_completeness(
        self,
        trace: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze if a trace is complete"""
        spans = trace.get("spans", [])
        
        if not spans:
            return {"complete": False, "reason": "No spans"}
            
        # Check for root span
        root_spans = [s for s in spans if not s.get("references")]
        if not root_spans:
            return {"complete": False, "reason": "No root span"}
            
        # Check for missing services
        services = set(s["process"]["serviceName"] for s in spans)
        
        # Check for broken links
        span_ids = set(s["spanID"] for s in spans)
        missing_refs = []
        for span in spans:
            for ref in span.get("references", []):
                if ref["spanID"] not in span_ids:
                    missing_refs.append(ref["spanID"])
                    
        return {
            "complete": len(missing_refs) == 0,
            "services": list(services),
            "span_count": len(spans),
            "missing_refs": missing_refs
        }
        
    def check_sampling_rate(self) -> Dict[str, Any]:
        """Check sampling configuration"""
        # This would check actual sampling config
        # For now, return placeholder
        return {
            "sampling_rate": "unknown",
            "recommendation": "Check service configuration"
        }
        
    def diagnose_trace_gaps(self, service: str) -> Dict[str, Any]:
        """Diagnose trace gaps for a service"""
        results = {
            "jaeger_health": self.check_jaeger_health(),
            "services": self.get_services(),
            "traces": []
        }
        
        if service in results["services"]:
            traces = self.get_traces_for_service(service)
            for trace in traces:
                analysis = self.analyze_trace_completeness(trace)
                results["traces"].append({
                    "trace_id": trace["traceID"],
                    "analysis": analysis
                })
                
        # Add recommendations
        recommendations = []
        
        if not results["jaeger_health"]["healthy"]:
            recommendations.append("Jaeger is not healthy - check Jaeger deployment")
            
        if service not in results["services"]:
            recommendations.append(f"Service '{service}' not found in Jaeger - check instrumentation")
            
        incomplete_traces = [
            t for t in results["traces"]
            if not t["analysis"]["complete"]
        ]
        if incomplete_traces:
            recommendations.append(
                f"{len(incomplete_traces)} incomplete traces found - check trace propagation"
            )
            
        results["recommendations"] = recommendations
        
        return results

# Usage
fixer = TraceGapFixer(
    jaeger_url="http://localhost:16686",
    prometheus_url="http://localhost:9090"
)

results = fixer.diagnose_trace_gaps("llm-service")
print(json.dumps(results, indent=2))
```

---

## Log Storage Issues

### Common Symptoms

```yaml
symptoms:
  - "Log storage filling up"
  - "Log aggregation system slow"
  - "Logs not being ingested"
  - "Log queries timing out"
  - "Log retention not working"
```

### Diagnosis Steps

```yaml
diagnosis:
  step_1:
    action: "Check storage usage"
    command: |
      # Check disk usage
      df -h /var/log
      
      # Check Elasticsearch storage
      curl -s 'http://elasticsearch:9200/_cat/allocation?v'
      
    expected: "Storage usage within limits"
    
  step_2:
    action: "Check log ingestion"
    command: |
      # Check if logs are being ingested
      curl -s 'http://elasticsearch:9200/_cat/indices?v&s=index'
      
    expected: "Indices are being created and updated"
    
  step_3:
    action: "Check log pipeline"
    command: |
      # Check Logstash/Loki status
      curl -s 'http://logstash:9600/_node/stats' | jq '.pipelines'
      
    expected: "Pipeline is processing logs"
    
  step_4:
    action: "Check retention policy"
    command: |
      # Check ILM policy
      curl -s 'http://elasticsearch:9200/_ilm/policy/llm-logs' | jq '.policy'
      
    expected: "Retention policy is configured"
    
  step_5:
    action: "Check query performance"
    command: |
      # Test a query
      curl -s 'http://elasticsearch:9200/llm-logs-*/_search' -H 'Content-Type: application/json' -d '{"size": 10}' | jq '.took'
      
    expected: "Queries complete in reasonable time"
```

### Common Causes and Fixes

```yaml
causes:
  storage_full:
    description: "Log storage disk full"
    symptoms:
      - "Cannot write new logs"
      - "Services failing"
    fix: |
      # Clean up old indices
      curl -X DELETE 'http://elasticsearch:9200/llm-logs-2024.01.*'
      
      # Update retention policy
      curl -X PUT 'http://elasticsearch:9200/_ilm/policy/llm-logs' -H 'Content-Type: application/json' -d '{
        "policy": {
          "phases": {
            "hot": {
              "actions": {
                "rollover": {
                  "max_size": "50gb",
                  "max_age": "1d"
                }
              }
            },
            "delete": {
              "min_age": "30d",
              "actions": {
                "delete": {}
              }
            }
          }
        }
      }'
      
  ingestion_slow:
    description: "Log ingestion falling behind"
    symptoms:
      - "Logs delayed"
      - "Kibana shows old logs"
    fix: |
      # Increase Logstash workers
      pipeline.workers: 8
      
      # Increase batch size
      pipeline.batch.size: 250
      
      # Check for bottlenecks
      curl -s 'http://logstash:9600/_node/stats' | jq '.pipelines.main.workers'
      
  query_slow:
    description: "Log queries timing out"
    symptoms:
      - "Kibana queries slow"
      - "API timeouts"
    fix: |
      # Optimize mappings
      curl -X PUT 'http://elasticsearch:9200/llm-logs' -H 'Content-Type: application/json' -d '{
        "mappings": {
          "properties": {
            "timestamp": {"type": "date"},
            "level": {"type": "keyword"},
            "message": {"type": "text"}
          }
        }
      }'
      
      # Add index pattern
      curl -X PUT 'http://elasticsearch:9200/llm-logs-*/_settings' -H 'Content-Type: application/json' -d '{
        "index": {
          "refresh_interval": "30s"
        }
      }'
      
  log_volume_too_high:
    description: "Too many logs being generated"
    symptoms:
      - "Storage filling quickly"
      - "Ingestion pipeline overwhelmed"
    fix: |
      # Reduce log verbosity
      # Change log level from DEBUG to INFO
      
      # Sample logs
      # Log only 10% of debug logs
      
      # Filter unnecessary logs
      # Remove health check logs
```

---

## Dashboard Performance

### Common Symptoms

```yaml
symptoms:
  - "Dashboards loading slowly"
  - "Dashboard queries timing out"
  - "Grafana UI unresponsive"
  - "Dashboard panels showing 'No data'"
  - "High memory usage in Grafana"
```

### Diagnosis Steps

```yaml
diagnosis:
  step_1:
    action: "Check Grafana performance"
    command: |
      # Check Grafana metrics
      curl -s 'http://grafana:3000/metrics' | grep "grafana_"
      
    expected: "Grafana metrics within normal range"
    
  step_2:
    action: "Check Prometheus query performance"
    command: |
      # Test query performance
      time curl -s 'http://prometheus:9090/api/v1/query?query=rate(llm_requests_total[5m])' > /dev/null
      
    expected: "Queries complete quickly"
    
  step_3:
    action: "Check dashboard complexity"
    command: |
      # Count panels in dashboard
      # Check number of queries per panel
      
    expected: "Dashboard complexity is manageable"
    
  step_4:
    action: "Check data volume"
    command: |
      # Check metric cardinality
      curl -s 'http://prometheus:9090/api/v1/label/__name__/values' | jq 'length'
      
    expected: "Metric cardinality is controlled"
    
  step_5:
    action: "Check caching"
    command: |
      # Check if caching is configured
      # Check cache hit rate
      
    expected: "Caching is working"
```

### Common Causes and Fixes

```yaml
causes:
  too_many_panels:
    description: "Dashboard has too many panels"
    symptoms:
      - "Dashboard loads slowly"
      - "Browser becomes unresponsive"
    fix: |
      # Reduce panel count
      # Maximum 12 panels per dashboard
      
      # Split into multiple dashboards
      # Create focused dashboards for specific use cases
      
  complex_queries:
    description: "PromQL queries too complex"
    symptoms:
      - "Query timeouts"
      - "High CPU usage"
    fix: |
      # Use recording rules
      - record: llm:requests:rate5m
        expr: sum(rate(llm_requests_total[5m])) by (model)
        
      # Simplify queries
      # Avoid nested aggregations
      
  high_cardinality:
    description: "Too many time series"
    symptoms:
      - "Query performance degraded"
      - "Prometheus memory high"
    fix: |
      # Reduce label cardinality
      # Remove high-cardinality labels
      
      # Use recording rules
      # Pre-aggregate metrics
      
  no_caching:
    description: "Queries not cached"
    symptoms:
      - "Repeated queries slow"
      - "High Prometheus load"
    fix: |
      # Enable query caching
      # Configure cache TTL
      
  refresh_too_frequent:
    description: "Dashboard refreshing too often"
    symptoms:
      - "High load on Prometheus"
      - "Browser performance issues"
    fix: |
      # Increase refresh interval
      # Use 30s or 60s refresh
      
      # Use variable for refresh rate
```

---

## Prometheus Issues

### Common Issues

```yaml
issues:
  out_of_memory:
    symptoms:
      - "Prometheus crashing"
      - "OOM killed"
    causes:
      - "Too many time series"
      - "High cardinality metrics"
      - "Insufficient memory"
    fixes:
      - "Reduce metric cardinality"
      - "Increase memory limits"
      - "Use recording rules"
      - "Configure retention"
      
  scrape_failures:
    symptoms:
      - "Targets showing as down"
      - "Missing metrics"
    causes:
      - "Network issues"
      - "Service down"
      - "Wrong port/path"
    fixes:
      - "Check network connectivity"
      - "Verify service health"
      - "Check scrape configuration"
      
  query_timeout:
    symptoms:
      - "Queries timing out"
      - "Grafana showing 'No data'"
    causes:
      - "Complex queries"
      - "High data volume"
      - "Insufficient resources"
    fixes:
      - "Simplify queries"
      - "Use recording rules"
      - "Increase timeout"
      - "Add resources"
      
  storage_full:
    symptoms:
      - "Prometheus crashing"
      - "Cannot write data"
    causes:
      - "Retention too long"
      - "Disk full"
      - "High write volume"
    fixes:
      - "Reduce retention"
      - "Add disk space"
      - "Reduce scrape frequency"
```

### Prometheus Troubleshooting Script

```python
# troubleshooting/prometheus_troubleshooter.py
import requests
from typing import Dict, List, Any
import json

class PrometheusTroubleshooter:
    """Troubleshoot Prometheus issues"""
    
    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url
        
    def check_health(self) -> Dict[str, Any]:
        """Check Prometheus health"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/-/healthy",
                timeout=5
            )
            return {"healthy": response.status_code == 200}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
            
    def check_targets(self) -> Dict[str, Any]:
        """Check scrape targets"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/targets",
                timeout=5
            )
            targets = response.json()["data"]["activeTargets"]
            
            up = [t for t in targets if t["health"] == "up"]
            down = [t for t in targets if t["health"] == "down"]
            
            return {
                "total": len(targets),
                "up": len(up),
                "down": len(down),
                "down_targets": [
                    {
                        "job": t["labels"]["job"],
                        "instance": t["labels"]["instance"],
                        "error": t.get("lastError", "")
                    }
                    for t in down
                ]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def check_metric_cardinality(self) -> Dict[str, Any]:
        """Check metric cardinality"""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/label/__name__/values",
                timeout=5
            )
            metrics = response.json()["data"]
            
            # Get cardinality for each metric
            cardinality = {}
            for metric in metrics[:100]:  # Check first 100
                series_response = requests.get(
                    f"{self.prometheus_url}/api/v1/series",
                    params={"match[]": metric},
                    timeout=5
                )
                series = series_response.json()["data"]
                cardinality[metric] = len(series)
                
            return {
                "total_metrics": len(metrics),
                "top_10_cardinality": sorted(
                    cardinality.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def check_query_performance(self) -> Dict[str, Any]:
        """Check query performance"""
        try:
            import time
            
            queries = [
                "rate(llm_requests_total[5m])",
                "histogram_quantile(0.99, rate(llm_latency_seconds_bucket[5m]))",
                "sum(rate(llm_requests_total[5m])) by (model)"
            ]
            
            results = []
            for query in queries:
                start = time.time()
                response = requests.get(
                    f"{self.prometheus_url}/api/v1/query",
                    params={"query": query},
                    timeout=10
                )
                duration = time.time() - start
                
                results.append({
                    "query": query,
                    "duration_seconds": duration,
                    "success": response.status_code == 200
                })
                
            return {"query_results": results}
        except Exception as e:
            return {"error": str(e)}
            
    def diagnose(self) -> Dict[str, Any]:
        """Run full diagnosis"""
        results = {
            "health": self.check_health(),
            "targets": self.check_targets(),
            "cardinality": self.check_metric_cardinality(),
            "query_performance": self.check_query_performance()
        }
        
        # Add recommendations
        recommendations = []
        
        if not results["health"]["healthy"]:
            recommendations.append("Prometheus is not healthy - check logs")
            
        if results["targets"].get("down", 0) > 0:
            recommendations.append(
                f"{results['targets']['down']} targets are down - check connectivity"
            )
            
        if results["cardinality"].get("total_metrics", 0) > 10000:
            recommendations.append(
                "High metric cardinality - consider reducing labels"
            )
            
        results["recommendations"] = recommendations
        
        return results

# Usage
troubleshooter = PrometheusTroubleshooter("http://localhost:9090")
results = troubleshooter.diagnose()
print(json.dumps(results, indent=2))
```

---

## Debugging Playbooks

### Playbook: Missing Metrics

```yaml
playbook: missing_metrics
description: "Troubleshoot missing metrics in Prometheus"
steps:
  - step: 1
    action: "Verify service is running"
    command: "kubectl get pods -l app=llm-service"
    expected: "Pods are in Running state"
    
  - step: 2
    action: "Check metrics endpoint"
    command: "curl -s http://llm-service:8080/metrics | head -20"
    expected: "Metrics are being exposed"
    
  - step: 3
    action: "Check Prometheus target"
    command: "curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job==\"llm-service\")'"
    expected: "Target is up and scraping"
    
  - step: 4
    action: "Check metric exists"
    command: "curl -s 'http://prometheus:9090/api/v1/query?query=llm_requests_total'"
    expected: "Metric data exists"
    
  - step: 5
    action: "Check metric labels"
    command: "curl -s 'http://prometheus:9090/api/v1/label/__name__/values' | jq '.data[] | select(startswith(\"llm_\"))'"
    expected: "Expected metrics exist"
    
escalation:
  after_15_minutes: "Page SRE team"
  after_30_minutes: "Page engineering lead"
  
runbook: "https://wiki/runbooks/missing-metrics"
```

### Playbook: Alert Fatigue

```yaml
playbook: alert_fatigue
description: "Reduce alert fatigue"
steps:
  - step: 1
    action: "Analyze alert volume"
    command: "Check alert count over last 24 hours"
    expected: "Understand current alert volume"
    
  - step: 2
    action: "Identify noisy alerts"
    command: "Find alerts that fire most frequently"
    expected: "Identify top noisy alerts"
    
  - step: 3
    action: "Review alert thresholds"
    command: "Compare thresholds to actual values"
    expected: "Identify overly sensitive thresholds"
    
  - step: 4
    action: "Update alert rules"
    command: "Add duration, consolidate related alerts"
    expected: "Reduce alert noise"
    
  - step: 5
    action: "Test changes"
    command: "Verify alerts still fire for real issues"
    expected: "Alerts are effective"
    
escalation:
  after_1_hour: "Page monitoring team lead"
  
runbook: "https://wiki/runbooks/alert-fatigue"
```

### Playbook: Dashboard Slow

```yaml
playbook: dashboard_slow
description: "Fix slow dashboard performance"
steps:
  - step: 1
    action: "Check panel count"
    command: "Count panels in dashboard"
    expected: "Panel count <= 12"
    
  - step: 2
    action: "Check query complexity"
    command: "Review PromQL queries"
    expected: "Queries are optimized"
    
  - step: 3
    action: "Check data volume"
    command: "Check metric cardinality"
    expected: "Cardinality is controlled"
    
  - step: 4
    action: "Enable caching"
    command: "Configure query caching"
    expected: "Caching is working"
    
  - step: 5
    action: "Optimize dashboard"
    command: "Split dashboard, reduce refresh rate"
    expected: "Dashboard loads quickly"
    
escalation:
  after_30_minutes: "Page Grafana admin"
  
runbook: "https://wiki/runbooks/dashboard-slow"
```

---

## References

- Prometheus Troubleshooting: https://prometheus.io/docs/guides/troubleshooting/
- Grafana Troubleshooting: https://grafana.com/docs/grafana/latest/troubleshooting/
- Jaeger Troubleshooting: https://www.jaegertracing.io/docs/latest/troubleshooting/

---

*Last Updated: January 2025*
*Version: 1.0.0*
