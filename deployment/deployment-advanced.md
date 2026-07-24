# Advanced Deployment Topics for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Canary Analysis](#canary-analysis)
   - [Metrics and Thresholds](#metrics-and-thresholds)
   - [Automated Analysis](#automated-analysis)
   - [Manual Analysis](#manual-analysis)
3. [A/B Testing](#ab-testing)
   - [Experiment Design](#experiment-design)
   - [Statistical Significance](#statistical-significance)
   - [Implementation](#implementation)
4. [Multi-Region Deployment](#multi-region-deployment)
   - [Architecture](#architecture)
   - [Data Replication](#data-replication)
   - [Traffic Management](#traffic-management)
5. [Disaster Recovery](#disaster-recovery)
   - [Backup Strategies](#backup-strategies)
   - [Recovery Procedures](#recovery-procedures)
   - [Testing DR Plans](#testing-dr-plans)
6. [Deployment Automation](#deployment-automation)
   - [GitOps](#gitops)
   - [Progressive Delivery](#progressive-delivery)
   - [Self-Healing Systems](#self-healing-systems)
7. [Advanced Monitoring](#advanced-monitoring)
   - [Observability Stack](#observability-stack)
   - [Custom Metrics](#custom-metrics)
   - [Alerting Strategies](#alerting-strategies)
8. [Security Considerations](#security-considerations)
   - [Supply Chain Security](#supply-chain-security)
   - [Runtime Security](#runtime-security)
   - [Compliance](#compliance)
9. [Summary](#summary)

---

## Overview

Advanced deployment topics cover sophisticated techniques for deploying AI/LLM systems with high reliability, scalability, and security. These practices are essential for production systems that require high availability and minimal risk.

### Key Principles

- **Automation First**: Automate repetitive tasks and decision-making
- **Observability**: Monitor everything and alert on anomalies
- **Gradual Rollout**: Never expose all users to untested changes
- **Fail Fast**: Detect issues early and recover quickly
- **Security by Design**: Embed security in every deployment stage

---

## Canary Analysis

### Metrics and Thresholds

```yaml
# canary-analysis-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: canary-analysis-config
data:
  metrics.yaml: |
    metrics:
      - name: request-success-rate
        description: "Percentage of successful requests"
        query: |
          sum(rate(http_requests_total{status!~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) * 100
        threshold:
          min: 99.0
        weight: 30
      
      - name: request-duration-p99
        description: "99th percentile request duration"
        query: |
          histogram_quantile(0.99, 
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          )
        threshold:
          max: 2.0
        weight: 25
      
      - name: error-rate
        description: "Percentage of 5xx errors"
        query: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) * 100
        threshold:
          max: 1.0
        weight: 25
      
      - name: llm-inference-latency
        description: "LLM inference latency"
        query: |
          histogram_quantile(0.95, 
            sum(rate(llm_inference_duration_seconds_bucket[5m])) by (le)
          )
        threshold:
          max: 5.0
        weight: 20
      
      - name: memory-usage
        description: "Memory utilization"
        query: |
          sum(container_memory_usage_bytes{container="llm-api"}) /
          sum(container_spec_memory_limit_bytes{container="llm-api"}) * 100
        threshold:
          max: 85.0
        weight: 10
      
      - name: gpu-utilization
        description: "GPU utilization"
        query: |
          avg(nvidia_gpu_utilization)
        threshold:
          min: 30.0
          max: 95.0
        weight: 10
```

### Automated Analysis

```yaml
# canary-analysis-automation.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: llm-api-canary
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  progressDeadlineSeconds: 600
  service:
    port: 8080
    targetPort: 8080
    gateways:
      - llm-api-gateway
    hosts:
      - llm-api.example.com
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
      - name: llm-inference-latency-p99
        thresholdRange:
          max: 2000
        interval: 30s
      - name: llm-error-rate
        thresholdRange:
          max: 1
        interval: 1m
      - name: memory-usage
        thresholdRange:
          max: 85
        interval: 1m
    webhooks:
      loadtest:
        name: load-test
        url: http://flagger-loadtester.flagger-system/
        timeout: 15s
        metadata:
          type: bash
          cmd: "curl -sd 'test' http://llm-api-canary.test.svc.cluster.local:8080/api/v1/completions"
      alert:
        name: slack-alert
        url: http://webhook-worker.flagger-system/got webhook/alert/flagger
        timeout: 5s
        metadata:
          type: text
          text: |
            {{ if eq .CanaryWeight "0" }}
            Canary promotion: {{ .ObjectRef.Name }} canary analysis passed
            {{ else }}
            Canary weight: {{ .CanaryWeight }}%
            {{ end }}
```

### Manual Analysis

```python
# canary_analysis.py
import requests
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CanaryMetric:
    name: str
    query: str
    threshold_min: float
    threshold_max: float
    weight: int

class CanaryAnalyzer:
    def __init__(self, prometheus_url: str, canary_version: str):
        self.prometheus_url = prometheus_url
        self.canary_version = canary_version
        self.metrics: List[CanaryMetric] = []
    
    def add_metric(self, metric: CanaryMetric):
        self.metrics.append(metric)
    
    def query_prometheus(self, query: str, start: datetime, end: datetime) -> float:
        """Query Prometheus for metric value."""
        response = requests.get(
            f"{self.prometheus_url}/api/v1/query_range",
            params={
                "query": query,
                "start": start.isoformat(),
                "end": end.isoformat(),
                "step": "60s"
            }
        )
        data = response.json()
        
        if data["status"] == "success" and data["data"]["result"]:
            values = [float(v[1]) for v in data["data"]["result"][0]["values"]]
            return sum(values) / len(values)
        
        return 0.0
    
    def analyze_canary(self, duration_minutes: int = 5) -> Dict:
        """Analyze canary deployment metrics."""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=duration_minutes)
        
        results = {}
        all_passed = True
        
        for metric in self.metrics:
            value = self.query_prometheus(metric.query, start_time, end_time)
            
            passed = True
            if metric.threshold_min and value < metric.threshold_min:
                passed = False
            if metric.threshold_max and value > metric.threshold_max:
                passed = False
            
            results[metric.name] = {
                "value": value,
                "threshold_min": metric.threshold_min,
                "threshold_max": metric.threshold_max,
                "passed": passed,
                "weight": metric.weight
            }
            
            if not passed:
                all_passed = False
        
        # Calculate weighted score
        total_weight = sum(m.weight for m in self.metrics)
        passed_weight = sum(
            m.weight for m in self.metrics 
            if results[m.name]["passed"]
        )
        score = (passed_weight / total_weight) * 100
        
        return {
            "all_passed": all_passed,
            "score": score,
            "metrics": results,
            "timestamp": end_time.isoformat(),
            "canary_version": self.canary_version
        }
    
    def should_promote(self, analysis_result: Dict, threshold: float = 90.0) -> bool:
        """Determine if canary should be promoted."""
        return analysis_result["score"] >= threshold
    
    def should_rollback(self, analysis_result: Dict, failure_threshold: int = 3) -> bool:
        """Determine if canary should be rolled back."""
        failed_metrics = sum(
            1 for m in analysis_result["metrics"].values()
            if not m["passed"]
        )
        return failed_metrics >= failure_threshold

# Usage example
analyzer = CanaryAnalyzer(
    prometheus_url="http://prometheus:9090",
    canary_version="1.3.0"
)

analyzer.add_metric(CanaryMetric(
    name="request-success-rate",
    query='sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100',
    threshold_min=99.0,
    threshold_max=None,
    weight=30
))

analyzer.add_metric(CanaryMetric(
    name="request-duration-p99",
    query='histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))',
    threshold_min=None,
    threshold_max=2.0,
    weight=25
))

result = analyzer.analyze_canary(duration_minutes=5)

if analyzer.should_promote(result):
    print("Promoting canary to production")
elif analyzer.should_rollback(result):
    print("Rolling back canary")
else:
    print("Canary analysis inconclusive, continuing monitoring")
```

---

## A/B Testing

### Experiment Design

```yaml
# ab-test-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ab-test-config
data:
  experiments.yaml: |
    experiments:
      - name: "new-embedding-model"
        description: "Test new sentence-transformers embedding model"
        status: active
        traffic_split:
          control:
            percentage: 50
            variant: "text-embedding-ada-002"
          treatment:
            percentage: 50
            variant: "sentence-transformers/all-mpnet-base-v2"
        metrics:
          - name: "embedding_quality"
            description: "Cosine similarity score"
            target: higher
          - name: "inference_latency"
            description: "Embedding generation time"
            target: lower
          - name: "user_satisfaction"
            description: "User rating of search results"
            target: higher
        duration_days: 14
        min_sample_size: 1000
      
      - name: "new-llm-prompt"
        description: "Test new prompt template for completions"
        status: active
        traffic_split:
          control:
            percentage: 70
            variant: "prompt-v1"
          treatment:
            percentage: 30
            variant: "prompt-v2"
        metrics:
          - name: "response_quality"
            description: "Human evaluation score"
            target: higher
          - name: "token_usage"
            description: "Average tokens per response"
            target: lower
          - name: "user_engagement"
            description: "Click-through rate on responses"
            target: higher
        duration_days: 7
        min_sample_size: 5000
```

### Statistical Significance

```python
# ab_test_analysis.py
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class ABTestMetric:
    name: str
    control_values: List[float]
    treatment_values: List[float]
    target: str  # "higher" or "lower"

class ABTestAnalyzer:
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
    
    def calculate_sample_size(
        self, 
        baseline_rate: float, 
        minimum_detectable_effect: float,
        power: float = 0.8
    ) -> int:
        """Calculate required sample size for experiment."""
        z_alpha = stats.norm.ppf(1 - self.alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)
        
        n = (
            (z_alpha * np.sqrt(2 * p1 * (1 - p1)) + 
             z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 /
            (p2 - p1) ** 2
        )
        
        return int(np.ceil(n))
    
    def analyze_metric(self, metric: ABTestMetric) -> Dict:
        """Analyze a single metric for statistical significance."""
        control = np.array(metric.control_values)
        treatment = np.array(metric.treatment_values)
        
        # Calculate basic statistics
        control_mean = np.mean(control)
        treatment_mean = np.mean(treatment)
        control_std = np.std(control)
        treatment_std = np.std(treatment)
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(control, treatment)
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(
            (control_std ** 2 + treatment_std ** 2) / 2
        )
        cohens_d = (treatment_mean - control_mean) / pooled_std if pooled_std > 0 else 0
        
        # Determine if statistically significant
        is_significant = p_value < self.alpha
        
        # Determine if practically significant
        if metric.target == "higher":
            is_practically_significant = treatment_mean > control_mean
        else:
            is_practically_significant = treatment_mean < control_mean
        
        # Calculate confidence interval for difference
        se = np.sqrt(control_std ** 2 / len(control) + treatment_std ** 2 / len(treatment))
        z_crit = stats.norm.ppf(1 - self.alpha / 2)
        diff = treatment_mean - control_mean
        ci_lower = diff - z_crit * se
        ci_upper = diff + z_crit * se
        
        return {
            "metric": metric.name,
            "control_mean": control_mean,
            "treatment_mean": treatment_mean,
            "difference": diff,
            "relative_difference": (diff / control_mean * 100) if control_mean != 0 else 0,
            "p_value": p_value,
            "is_significant": is_significant,
            "is_practically_significant": is_practically_significant,
            "effect_size": cohens_d,
            "confidence_interval": {
                "lower": ci_lower,
                "upper": ci_upper
            },
            "sample_size": {
                "control": len(control),
                "treatment": len(treatment)
            }
        }
    
    def analyze_experiment(
        self, 
        metrics: List[ABTestMetric],
        min_sample_size: int = 1000
    ) -> Dict:
        """Analyze entire experiment with multiple metrics."""
        results = {
            "metrics": [],
            "overall_significant": True,
            "recommendation": "continue"
        }
        
        for metric in metrics:
            result = self.analyze_metric(metric)
            results["metrics"].append(result)
            
            if not result["is_significant"]:
                results["overall_significant"] = False
        
        # Determine recommendation
        significant_metrics = sum(
            1 for r in results["metrics"] 
            if r["is_significant"]
        )
        
        min_samples_met = all(
            r["sample_size"]["control"] >= min_sample_size and
            r["sample_size"]["treatment"] >= min_sample_size
            for r in results["metrics"]
        )
        
        if significant_metrics == len(results["metrics"]) and min_samples_met:
            # Check if all significant results favor treatment
            all_favor_treatment = all(
                r["is_practically_significant"] 
                for r in results["metrics"]
            )
            
            if all_favor_treatment:
                results["recommendation"] = "promote_treatment"
            else:
                results["recommendation"] = "keep_control"
        elif not min_samples_met:
            results["recommendation"] = "continue_collecting_data"
        else:
            results["recommendation"] = "continue"
        
        return results

# Usage example
analyzer = ABTestAnalyzer(confidence_level=0.95)

# Simulate data
np.random.seed(42)
control_latency = np.random.normal(1.5, 0.3, 1000)
treatment_latency = np.random.normal(1.3, 0.3, 1000)

control_quality = np.random.normal(0.8, 0.1, 1000)
treatment_quality = np.random.normal(0.85, 0.1, 1000)

metrics = [
    ABTestMetric(
        name="inference_latency",
        control_values=control_latency.tolist(),
        treatment_values=treatment_latency.tolist(),
        target="lower"
    ),
    ABTestMetric(
        name="response_quality",
        control_values=control_quality.tolist(),
        treatment_values=treatment_quality.tolist(),
        target="higher"
    )
]

results = analyzer.analyze_experiment(metrics)
print(json.dumps(results, indent=2))
```

---

## Multi-Region Deployment

### Architecture

```yaml
# multi-region-architecture.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: multi-region-config
data:
  regions.yaml: |
    regions:
      - name: us-east-1
        type: primary
        endpoint: https://us-east-1.llm-api.example.com
        weight: 40
        features:
          - completions
          - embeddings
          - fine-tuning
      
      - name: us-west-2
        type: secondary
        endpoint: https://us-west-2.llm-api.example.com
        weight: 30
        features:
          - completions
          - embeddings
      
      - name: eu-west-1
        type: secondary
        endpoint: https://eu-west-1.llm-api.example.com
        weight: 20
        features:
          - completions
          - embeddings
      
      - name: ap-southeast-1
        type: secondary
        endpoint: https://ap-southeast-1.llm-api.example.com
        weight: 10
        features:
          - completions
          - embeddings
    
    routing:
      strategy: "latency-based"
      failover:
        enabled: true
        health_check_interval: 30s
        failure_threshold: 3
        recovery_threshold: 2
      
      load_balancing:
        algorithm: "weighted-round-robin"
        sticky_sessions: false
        circuit_breaker:
          enabled: true
          threshold: 5
          timeout: 30s
```

### Data Replication

```yaml
# data-replication.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-replication-config
data:
  replication.yaml: |
    databases:
      - name: llm-api-postgres
        type: postgresql
        primary_region: us-east-1
        replica_regions:
          - us-west-2
          - eu-west-1
          - ap-southeast-1
        replication_mode: "async"
        replication_lag_threshold: 1000  # milliseconds
        backup:
          enabled: true
          interval: "1h"
          retention: "30d"
          cross_region: true
    
    caches:
      - name: llm-api-redis
        type: redis
        primary_region: us-east-1
        replica_regions:
          - us-west-2
          - eu-west-1
        replication_mode: "sync"
        cluster_mode: true
    
    object_storage:
      - name: llm-models
        type: s3
        primary_region: us-east-1
        replica_regions:
          - us-west-2
          - eu-west-1
        cross_region_replication: true
```

### Traffic Management

```yaml
# multi-region-traffic.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: llm-api-global
spec:
  hosts:
    - llm-api.example.com
  http:
    - route:
        - destination:
            host: llm-api.us-east-1
            port:
              number: 8080
          weight: 40
        - destination:
            host: llm-api.us-west-2
            port:
              number: 8080
          weight: 30
        - destination:
            host: llm-api.eu-west-1
            port:
              number: 8080
          weight: 20
        - destination:
            host: llm-api.ap-southeast-1
            port:
              number: 8080
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx
      timeout: 10s
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: llm-api-global
spec:
  host: llm-api.example.com
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1000
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 1000
        http2MaxRequests: 1000
        maxRequestsPerConnection: 100
        maxRetries: 3
    loadBalancer:
      simple: LEAST_CONN
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

---

## Disaster Recovery

### Backup Strategies

```yaml
# disaster-recovery.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: disaster-recovery-config
data:
  backup-strategy.yaml: |
    backup_strategies:
      - name: "database-backup"
        type: "postgresql"
        schedule: "0 2 * * *"  # Daily at 2 AM
        retention:
          daily: 30
          weekly: 12
          monthly: 12
        storage:
          primary: "s3://llm-api-backups/database/"
          secondary: "gs://llm-api-backups-drc/database/"
        verification:
          enabled: true
          schedule: "0 4 * * 0"  # Weekly on Sunday at 4 AM
          test_restore: true
      
      - name: "model-backup"
        type: "filesystem"
        schedule: "0 3 * * *"  # Daily at 3 AM
        paths:
          - "/models"
        retention:
          daily: 7
          weekly: 4
        storage:
          primary: "s3://llm-api-backups/models/"
          secondary: "gs://llm-api-backups-drc/models/"
      
      - name: "config-backup"
        type: "kubernetes"
        schedule: "*/30 * * * *"  # Every 30 minutes
        resources:
          - "configmaps"
          - "secrets"
          - "deployments"
          - "services"
        retention:
          hourly: 24
          daily: 7
        storage:
          primary: "s3://llm-api-backups/config/"
    
    recovery_objectives:
      rto: "4h"  # Recovery Time Objective
      rpo: "1h"  # Recovery Point Objective
      
      scenarios:
        - name: "single-region-failure"
          rto: "30m"
          rpo: "5m"
          procedures:
            - "failover-to-secondary-region"
            - "verify-data-consistency"
            - "update-dns-records"
        
        - name: "database-corruption"
          rto: "2h"
          rpo: "1h"
          procedures:
            - "stop-application"
            - "restore-database-from-backup"
            - "verify-data-integrity"
            - "restart-application"
        
        - name: "complete-outage"
          rto: "4h"
          rpo: "1h"
          procedures:
            - "activate-drc-region"
            - "restore-from-backups"
            - "verify-system-integrity"
            - "redirect-traffic"
```

### Recovery Procedures

```bash
#!/bin/bash
# disaster-recovery.sh - Disaster Recovery Script

set -e

# Configuration
PRIMARY_REGION="us-east-1"
SECONDARY_REGION="us-west-2"
BACKUP_BUCKET="s3://llm-api-backups"
DATABASE_NAME="llm-api"

echo "=== Disaster Recovery Procedure ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Step 1: Assess the situation
echo "Step 1: Assessing situation..."
kubectl get nodes -l topology.kubernetes.io/region=$PRIMARY_REGION || echo "Primary region unavailable"

# Step 2: Stop traffic to affected region
echo "Step 2: Updating traffic routing..."
kubectl patch virtualservice llm-api-global \
  --type merge \
  -p '{"spec":{"http":[{"route":[{"destination":{"host":"llm-api.us-east-1","port":{"number":8080}},"weight":0},{"destination":{"host":"llm-api.us-west-2","port":{"number":8080}},"weight":100}]}]}}'

# Step 3: Verify secondary region is healthy
echo "Step 3: Verifying secondary region..."
kubectl get pods -n production --context=us-west-2

# Step 4: Restore database if needed
echo "Step 4: Checking database status..."
LATEST_BACKUP=$(aws s3 ls s3://llm-api-backups/database/ --recursive | sort | tail -n 1 | awk '{print $4}')
echo "Latest backup: $LATEST_BACKUP"

# Step 5: Restore from backup if needed
echo "Step 5: Restoring from backup..."
aws s3 cp $BACKUP_BUCKET/database/$LATEST_BACKUP /tmp/restore.sql
psql -h postgres-secondary -U admin -d $DATABASE_NAME < /tmp/restore.sql

# Step 6: Verify data consistency
echo "Step 6: Verifying data consistency..."
psql -h postgres-secondary -U admin -d $DATABASE_NAME -c "SELECT COUNT(*) FROM completions;"

# Step 7: Update DNS
echo "Step 7: Updating DNS records..."
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "llm-api.example.com",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "SECONDARY_IP"}]
      }
    }]
  }'

# Step 8: Verify recovery
echo "Step 8: Verifying recovery..."
curl -f https://llm-api.example.com/health/ready

echo "=== Disaster Recovery Complete ==="
```

### Testing DR Plans

```yaml
# dr-test-config.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dr-test
  namespace: disaster-recovery
spec:
  schedule: "0 0 1 * *"  # Monthly on 1st at midnight
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: dr-test
              image: dr-test:latest
              env:
                - name: PRIMARY_REGION
                  value: "us-east-1"
                - name: SECONDARY_REGION
                  value: "us-west-2"
                - name: TEST_MODE
                  value: "true"
              command: ["/bin/bash", "/scripts/dr-test.sh"]
          restartPolicy: Never
      backoffLimit: 1
```

---

## Deployment Automation

### GitOps

```yaml
# gitops-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gitops-config
data:
  argocd-application.yaml: |
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: llm-api
      namespace: argocd
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/llm-api-deployments.git
        targetRevision: HEAD
        path: environments/production
      destination:
        server: https://kubernetes.default.svc
        namespace: production
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
        retry:
          limit: 5
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 3m0s
  
  flux-config.yaml: |
    apiVersion: kustomize.toolkit.fluxcd.io/v1
    kind: Kustomization
    metadata:
      name: llm-api
      namespace: flux-system
    spec:
      interval: 5m
      path: ./environments/production
      prune: true
      sourceRef:
        kind: GitRepository
        name: llm-api-deployments
      healthChecks:
        - apiVersion: apps/v1
          kind: Deployment
          name: llm-api
          namespace: production
      timeout: 3m
```

### Progressive Delivery

```yaml
# progressive-delivery.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: llm-api
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  progressDeadlineSeconds: 600
  service:
    port: 8080
    targetPort: 8080
    gateways:
      - llm-api-gateway
    hosts:
      - llm-api.example.com
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
    webhooks:
      loadtest:
        name: load-test
        url: http://flagger-loadtester.flagger-system/
        timeout: 15s
        metadata:
          type: bash
          cmd: "curl -sd 'test' http://llm-api-canary.test.svc.cluster.local:8080/api/v1/completions"
      alert:
        name: slack-alert
        url: http://webhook-worker.flagger-system/got webhook/alert/flagger
        timeout: 5s
        metadata:
          type: text
          text: |
            Canary weight: {{ .CanaryWeight }}%
            Status: {{ .CanaryStatus }}
```

### Self-Healing Systems

```yaml
# self-healing-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: self-healing-config
data:
  auto-remediation.yaml: |
    remediation_rules:
      - name: "high-error-rate"
        condition:
          metric: "http_requests_total{status=~'5..'}"
          threshold: 0.05
          duration: "5m"
        actions:
          - type: "rollback"
            deployment: "llm-api"
            namespace: "production"
          - type: "alert"
            channel: "slack"
            message: "Auto-rollback triggered due to high error rate"
      
      - name: "high-latency"
        condition:
          metric: "http_request_duration_seconds{quantile='0.99'}"
          threshold: 2.0
          duration: "5m"
        actions:
          - type: "scale-up"
            deployment: "llm-api"
            namespace: "production"
            replicas: 5
          - type: "alert"
            channel: "slack"
            message: "Auto-scaling triggered due to high latency"
      
      - name: "pod-crash-loop"
        condition:
          metric: "kube_pod_container_status_restarts_total"
          threshold: 5
          duration: "10m"
        actions:
          - type: "restart"
            deployment: "llm-api"
            namespace: "production"
          - type: "alert"
            channel: "slack"
            message: "Auto-restart triggered due to crash loop"
```

---

## Advanced Monitoring

### Observability Stack

```yaml
# observability-stack.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: observability-stack
data:
  stack.yaml: |
    components:
      metrics:
        prometheus:
          enabled: true
          retention: "30d"
          storage: "50Gi"
        thanos:
          enabled: true
          bucket: "s3://llm-api-metrics/"
      
      logging:
        loki:
          enabled: true
          retention: "30d"
          storage: "100Gi"
        promtail:
          enabled: true
      
      tracing:
        tempo:
          enabled: true
          retention: "7d"
          storage: "20Gi"
      
      visualization:
        grafana:
          enabled: true
          dashboards:
            - "llm-api-overview"
            - "llm-api-performance"
            - "llm-api-errors"
            - "llm-api-business"
    
    alerts:
      slack:
        enabled: true
        channel: "#llm-api-alerts"
        webhook: "https://hooks.slack.com/services/xxx"
      
      pagerduty:
        enabled: true
        service_key: "xxx"
```

### Custom Metrics

```yaml
# custom-metrics.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-metrics
data:
  metrics.yaml: |
    metrics:
      - name: "llm_completions_total"
        type: "counter"
        description: "Total number of LLM completions"
        labels:
          - "model"
          - "status"
          - "user_segment"
      
      - name: "llm_completion_tokens_total"
        type: "counter"
        description: "Total tokens generated"
        labels:
          - "model"
          - "user_segment"
      
      - name: "llm_completion_duration_seconds"
        type: "histogram"
        description: "LLM completion duration"
        buckets: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        labels:
          - "model"
          - "prompt_length"
      
      - name: "llm_embedding_duration_seconds"
        type: "histogram"
        description: "Embedding generation duration"
        buckets: [0.01, 0.05, 0.1, 0.5, 1.0]
        labels:
          - "model"
          - "input_length"
      
      - name: "llm_model_loading_duration_seconds"
        type: "histogram"
        description: "Model loading duration"
        buckets: [1.0, 5.0, 10.0, 30.0, 60.0]
        labels:
          - "model"
          - "load_type"
      
      - name: "llm_gpu_memory_usage_bytes"
        type: "gauge"
        description: "GPU memory usage"
        labels:
          - "gpu_id"
          - "model"
```

### Alerting Strategies

```yaml
# alerting-strategies.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: llm-api-alerts
  namespace: monitoring
spec:
  groups:
    - name: llm-api.rules
      rules:
        - alert: HighErrorRate
          expr: |
            sum(rate(http_requests_total{status=~"5.."}[5m])) /
            sum(rate(http_requests_total[5m])) > 0.05
          for: 5m
          labels:
            severity: critical
            team: ml-platform
          annotations:
            summary: "High error rate detected"
            description: "Error rate is {{ $value | humanizePercentage }}"
            runbook_url: "https://runbooks.example.com/high-error-rate"
        
        - alert: HighLatency
          expr: |
            histogram_quantile(0.99, 
              sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
            ) > 2
          for: 5m
          labels:
            severity: warning
            team: ml-platform
          annotations:
            summary: "High latency detected"
            description: "99th percentile latency is {{ $value }}s"
            runbook_url: "https://runbooks.example.com/high-latency"
        
        - alert: ModelLoadingSlow
          expr: |
            histogram_quantile(0.95, 
              sum(rate(llm_model_loading_duration_seconds_bucket[5m])) by (le)
            ) > 30
          for: 5m
          labels:
            severity: warning
            team: ml-platform
          annotations:
            summary: "Model loading is slow"
            description: "Model loading 95th percentile is {{ $value }}s"
            runbook_url: "https://runbooks.example.com/slow-model-loading"
```

---

## Security Considerations

### Supply Chain Security

```yaml
# supply-chain-security.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: supply-chain-security
data:
  security.yaml: |
    image_scanning:
      enabled: true
      scanner: "trivy"
      severity_threshold: "HIGH"
      auto_scan: true
    
    image_signing:
      enabled: true
      signer: "cosign"
      keyless: true
    
    dependency_scanning:
      enabled: true
      tools:
        - "safety"
        - "snyk"
        - "owasp-dependency-check"
    
    sbom_generation:
      enabled: true
      format: "spdx"
      tool: "syft"
    
    policy_enforcement:
      enabled: true
      policy_engine: "opa"
      policies:
        - "no-privileged-containers"
        - "no-root-user"
        - "resource-limits-required"
        - "image-registry-restricted"
```

### Runtime Security

```yaml
# runtime-security.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: runtime-security
data:
  security.yaml: |
    pod_security:
      run_as_non_root: true
      read_only_root_filesystem: true
      allow_privilege_escalation: false
      capabilities:
        drop:
          - ALL
    
    network_policies:
      enabled: true
      default_action: "deny"
      allow_rules:
        - name: "allow-ingress"
          from:
            - namespaceSelector:
                matchLabels:
                  name: ingress-nginx
          to:
            - port: 8080
        
        - name: "allow-database"
          from:
            - podSelector:
                matchLabels:
                  app: llm-api
          to:
            - podSelector:
                matchLabels:
                  app: postgres
              port: 5432
    
    secret_management:
      enabled: true
      provider: "vault"
      rotation:
        enabled: true
        interval: "24h"
```

### Compliance

```yaml
# compliance-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: compliance-config
data:
  compliance.yaml: |
    frameworks:
      - name: "SOC2"
        controls:
          - "CC6.1"
          - "CC6.6"
          - "CC7.1"
          - "CC7.2"
          - "CC8.1"
      
      - name: "GDPR"
        controls:
          - "Article.5"
          - "Article.25"
          - "Article.32"
      
      - name: "HIPAA"
        controls:
          - "§164.308"
          - "§164.310"
          - "§164.312"
    
    audit_logging:
      enabled: true
      events:
        - "authentication"
        - "authorization"
        - "data_access"
        - "configuration_change"
      retention: "1 year"
    
    data_classification:
      enabled: true
      levels:
        - "public"
        - "internal"
        - "confidential"
        - "restricted"
```

---

## Summary

Advanced deployment topics for AI/LLM systems include:

1. **Canary Analysis**: Automated and manual analysis of canary deployments
2. **A/B Testing**: Statistical analysis of experiments with multiple metrics
3. **Multi-Region Deployment**: Architecture, data replication, and traffic management
4. **Disaster Recovery**: Backup strategies, recovery procedures, and DR testing
5. **Deployment Automation**: GitOps, progressive delivery, and self-healing systems
6. **Advanced Monitoring**: Observability stack, custom metrics, and alerting
7. **Security Considerations**: Supply chain security, runtime security, and compliance

By mastering these advanced topics, teams can deploy AI/LLM systems with high reliability, scalability, and security in production environments.

### Key Takeaways

- **Automate everything possible** - Manual processes are error-prone
- **Monitor comprehensively** - Detect issues before users do
- **Test in production safely** - Use canary and A/B testing
- **Plan for disaster** - Have tested recovery procedures
- **Secure the supply chain** - Protect against threats at every stage
- **Use GitOps** - Infrastructure as code enables reproducibility
- **Implement self-healing** - Systems should recover automatically
