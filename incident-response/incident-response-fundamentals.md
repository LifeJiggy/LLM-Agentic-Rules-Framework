# Incident Response Fundamentals for LLM & Agentic AI Systems

## Table of Contents

1. [Overview](#overview)
2. [Incident Types in AI/LLM Systems](#incident-types)
3. [Severity Classification](#severity-classification)
4. [Response Lifecycle](#response-lifecycle)
5. [Roles and Responsibilities](#roles-and-responsibilities)
6. [Communication Protocols](#communication-protocols)
7. [Incident Detection](#incident-detection)
8. [Triage Process](#triage-process)
9. [Containment Strategies](#containment-strategies)
10. [Remediation Framework](#remediation-framework)
11. [Post-Mortem Process](#post-mortem-process)
12. [Incident Response for LLM-Specific Threats](#llm-specific-threats)
13. [Checklists](#checklists)
14. [References](#references)

---

## Overview

Incident response for LLM and Agentic AI systems requires specialized procedures that account for the unique characteristics of these technologies: probabilistic outputs, model degradation over time, prompt injection vulnerabilities, and the autonomous nature of agentic systems. This document establishes the foundational concepts, processes, and frameworks necessary for effective incident management.

### Core Principles

```
┌─────────────────────────────────────────────────────────────┐
│                  INCIDENT RESPONSE PRINCIPLES                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SPEED        → Minimize time to detection & response    │
│  2. CONTAINMENT  → Stop the bleeding before it spreads      │
│  3. TRANSPARENCY → Communicate openly with stakeholders     │
│  4. LEARNING     → Every incident is a learning opportunity │
│  5. PREPAREDNESS → Assume incidents will happen             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why AI/LLM Incident Response Differs

Traditional software incidents follow deterministic patterns. AI/LLM incidents are fundamentally different:

| Characteristic | Traditional Software | AI/LLM Systems |
|---|---|---|
| Root cause | Code bug, config error | Data drift, prompt injection, model hallucination |
| Predictability | Deterministic failures | Probabilistic failures |
| Detection | Error logs, exceptions | Behavioral anomalies, output quality metrics |
| Fix | Patch code, rollback | Retrain model, update prompts, filter inputs |
| Time to resolve | Minutes to hours | Hours to days (retraining) |
| Blast radius | Specific feature | All users, all conversations |

---

## Incident Types

### 1. Security Incidents

#### Prompt Injection Attacks

```yaml
incident_type: prompt_injection
description: "Attacker manipulates LLM inputs to override system instructions"
severity_range: P1-P0
detection_signals:
  - System prompt revealed in output
  - Unauthorized actions performed
  - Bypass of safety filters
  - Unexpected tool/API calls
examples:
  - Direct injection: "Ignore previous instructions and..."
  - Indirect injection: Malicious content in retrieved documents
  - Multi-turn injection: Gradual context manipulation
```

**Detection Indicators:**
- User input patterns matching known injection techniques
- System prompt leakage detected in outputs
- Unauthorized tool invocations
- Output content contradicting system instructions

#### Data Exfiltration via LLM

```python
# Detection pattern for data exfiltration attempts
class ExfiltrationDetector:
    """Monitor for patterns indicating data exfiltration through LLM outputs."""

    SENSITIVE_PATTERNS = [
        r'\b\d{3}-\d{2}-\d{4}\b',          # SSN pattern
        r'\b\d{16}\b',                       # Credit card pattern
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'(?i)(password|secret|api.?key|token)\s*[:=]\s*\S+',  # Secrets
    ]

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.alert_threshold = 0.85

    def detect_exfiltration(self, user_input: str, llm_output: str) -> dict:
        """Check for potential data exfiltration in LLM interactions."""
        import re

        results = {
            "input_risk_score": 0.0,
            "output_risk_score": 0.0,
            "alerts": []
        }

        # Analyze output for sensitive data patterns
        for pattern in self.SENSITIVE_PATTERNS:
            matches = re.findall(pattern, llm_output)
            if matches:
                results["output_risk_score"] += 0.2 * len(matches)
                results["alerts"].append({
                    "type": "sensitive_data_in_output",
                    "pattern": pattern,
                    "count": len(matches)
                })

        # Check for prompt injection indicators
        injection_indicators = [
            "ignore previous",
            "forget your instructions",
            "you are now",
            "new system prompt",
            "override safety"
        ]

        for indicator in injection_indicators:
            if indicator.lower() in user_input.lower():
                results["input_risk_score"] += 0.3
                results["alerts"].append({
                    "type": "prompt_injection",
                    "indicator": indicator
                })

        return results
```

#### Model Theft or Unauthorized Access

```yaml
incident_type: model_access
description: "Unauthorized access to model weights, training data, or inference endpoints"
severity: P0
detection_signals:
  - Unexpected API access patterns
  - Large data transfers from model storage
  - Authentication anomalies
  - Model endpoint accessed from unknown IPs
immediate_actions:
  - Revoke API keys
  - Enable IP allowlisting
  - Audit access logs
  - Notify security team
```

### 2. Performance Incidents

#### Model Degradation

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics

class ModelDegradationMonitor:
    """Monitor model performance metrics for degradation signals."""

    def __init__(self, baseline_window_days: int = 30, alert_threshold: float = 0.15):
        self.baseline_window = baseline_window_days
        self.alert_threshold = alert_threshold
        self.metrics_history: List[Dict] = []

    def record_metric(self, metric_name: str, value: float, timestamp: Optional[datetime] = None):
        """Record a performance metric data point."""
        self.metrics_history.append({
            "metric": metric_name,
            "value": value,
            "timestamp": timestamp or datetime.utcnow()
        })

    def calculate_baseline(self, metric_name: str) -> Dict:
        """Calculate baseline statistics for a metric."""
        cutoff = datetime.utcnow() - timedelta(days=self.baseline_window)
        values = [
            m["value"] for m in self.metrics_history
            if m["metric"] == metric_name and m["timestamp"] > cutoff
        ]

        if not values:
            return {"mean": 0, "std": 0, "samples": 0}

        return {
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "samples": len(values)
        }

    def check_degradation(self, metric_name: str, current_value: float) -> Dict:
        """Check if current metric indicates degradation."""
        baseline = self.calculate_baseline(metric_name)

        if baseline["samples"] < 10:
            return {"degraded": False, "reason": "insufficient_baseline_data"}

        deviation = abs(current_value - baseline["mean"]) / max(baseline["std"], 0.001)

        is_degraded = deviation > 2.0  # More than 2 standard deviations

        return {
            "degraded": is_degraded,
            "metric": metric_name,
            "current": current_value,
            "baseline_mean": baseline["mean"],
            "baseline_std": baseline["std"],
            "deviation_sigma": deviation,
            "severity": self._classify_severity(deviation)
        }

    def _classify_severity(self, deviation: float) -> str:
        if deviation > 4.0:
            return "P0"
        elif deviation > 3.0:
            return "P1"
        elif deviation > 2.5:
            return "P2"
        return "P3"

    def detect_drift(self, metric_name: str, window_hours: int = 1) -> Dict:
        """Detect metric drift within a time window."""
        cutoff = datetime.utcnow() - timedelta(hours=window_hours)
        recent = [
            m["value"] for m in self.metrics_history
            if m["metric"] == metric_name and m["timestamp"] > cutoff
        ]

        if len(recent) < 5:
            return {"drift_detected": False, "reason": "insufficient_recent_data"}

        baseline = self.calculate_baseline(metric_name)
        recent_mean = statistics.mean(recent)

        if baseline["std"] == 0:
            return {"drift_detected": False, "reason": "zero_baseline_variance"}

        drift = (recent_mean - baseline["mean"]) / baseline["std"]

        return {
            "drift_detected": abs(drift) > 2.0,
            "drift_direction": "negative" if drift < 0 else "positive",
            "drift_magnitude": drift,
            "recent_mean": recent_mean,
            "baseline_mean": baseline["mean"],
            "window_hours": window_hours
        }
```

#### Latency Spikes

```yaml
incident_type: latency_spike
description: "Sudden increase in LLM inference response time"
severity_range: P2-P0
metrics_to_monitor:
  - p50_latency_ms
  - p95_latency_ms
  - p99_latency_ms
  - time_to_first_token_ms
  - tokens_per_second
thresholds:
  p95_degradation_percent: 50    # Alert if p95 > 1.5x baseline
  p99_degradation_percent: 100   # Alert if p99 > 2x baseline
  max_acceptable_latency_ms: 10000  # Hard limit
common_causes:
  - GPU memory pressure
  - Batch size conflicts
  - Network latency to model serving
  - Context window overflow
  - Token generation bottlenecks
```

### 3. Data Breach Incidents

#### Training Data Exposure

```python
class TrainingDataBreachDetector:
    """Detect potential training data exposure through LLM outputs."""

    def __init__(self):
        self.known_breach_patterns = [
            "training data contains",
            "memorized from",
            "I remember seeing",
            "from the dataset",
            "in the training corpus"
        ]

    def analyze_output_for_data_leakage(self, output: str, context: str = "") -> Dict:
        """Analyze LLM output for signs of training data leakage."""
        results = {
            "potential_leakage": False,
            "confidence": 0.0,
            "indicators": []
        }

        # Check for memorized content indicators
        for pattern in self.known_breach_patterns:
            if pattern.lower() in output.lower():
                results["potential_leakage"] = True
                results["confidence"] = min(results["confidence"] + 0.25, 1.0)
                results["indicators"].append(pattern)

        # Check for PII patterns that shouldn't be in outputs
        import re
        pii_patterns = {
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "address": r'\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b'
        }

        for pii_type, pattern in pii_patterns.items():
            if re.search(pattern, output):
                results["potential_leakage"] = True
                results["confidence"] = min(results["confidence"] + 0.3, 1.0)
                results["indicators"].append(f"pii_{pii_type}")

        return results

    def check_training_data_access(self, access_logs: List[Dict]) -> Dict:
        """Audit training data access logs for anomalies."""
        suspicious = []

        for log in access_logs:
            risk_score = 0

            # Unusual access time
            if self._is_off_hours(log.get("timestamp")):
                risk_score += 2

            # Large download
            if log.get("bytes_transferred", 0) > 1_000_000_000:  # > 1GB
                risk_score += 3

            # Access from new IP
            if log.get("is_new_ip", False):
                risk_score += 2

            # Multiple rapid access
            if log.get("requests_per_minute", 0) > 100:
                risk_score += 4

            if risk_score >= 5:
                suspicious.append({
                    "log": log,
                    "risk_score": risk_score,
                    "reasons": self._explain_risk(log)
                })

        return {
            "total_accesses": len(access_logs),
            "suspicious_accesses": len(suspicious),
            "details": suspicious
        }
```

### 4. Model Failure Incidents

#### Hallucination Cascades

```python
class HallucinationDetector:
    """Detect and categorize hallucination incidents."""

    def __init__(self, fact_check_client=None):
        self.fact_check_client = fact_check_client
        self.hallucination_patterns = {
            "factual": [
                "incorrect facts",
                "fabricated information",
                "false claims"
            ],
            "citation": [
                "non-existent papers",
                "fake references",
                "invented sources"
            ],
            "temporal": [
                "future events as past",
                "incorrect dates",
                "timeline confusion"
            ],
            "attribution": [
                "wrong authorship",
                "misattributed quotes",
                "false credentials"
            ]
        }

    def analyze_hallucination(self, text: str, context: Dict = None) -> Dict:
        """Analyze text for hallucination indicators."""
        analysis = {
            "hallucination_score": 0.0,
            "categories": [],
            "severity": "low",
            "recommended_actions": []
        }

        # Pattern-based detection
        hallucination_indicators = [
            (r'\bsource\b.*\bhttps?://\S+\b', 0.3),  # Suspicious URLs
            (r'\baccording to\b.*\b(?:study|research)\b', 0.2),  # Unverified citations
            (r'\bin\s+\d{4}\b.*\b(?:discovered|invented)\b', 0.25),  # Historical claims
        ]

        for pattern, weight in hallucination_indicators:
            import re
            if re.search(pattern, text, re.IGNORECASE):
                analysis["hallucination_score"] += weight

        # Severity classification
        if analysis["hallucination_score"] > 0.7:
            analysis["severity"] = "critical"
            analysis["recommended_actions"] = [
                "immediate_output_retraction",
                "user_notification",
                "model_review"
            ]
        elif analysis["hallucination_score"] > 0.4:
            analysis["severity"] = "high"
            analysis["recommended_actions"] = [
                "add_disclaimer",
                "request_human_review",
                "log_for_analysis"
            ]
        elif analysis["hallucination_score"] > 0.2:
            analysis["severity"] = "medium"
            analysis["recommended_actions"] = [
                "flag_output",
                "monitor_pattern"
            ]

        return analysis

    def create_incident_report(self, hallucination_analysis: Dict, user_id: str, timestamp: str) -> Dict:
        """Create a structured incident report for hallucination events."""
        return {
            "incident_type": "hallucination",
            "severity": hallucination_analysis["severity"],
            "user_id": user_id,
            "timestamp": timestamp,
            "hallucination_score": hallucination_analysis["hallucination_score"],
            "categories": hallucination_analysis["categories"],
            "recommended_actions": hallucination_analysis["recommended_actions"],
            "escalation_required": hallucination_analysis["severity"] in ["critical", "high"],
            "auto_remediate": hallucination_analysis["severity"] == "critical"
        }
```

---

## Severity Classification

### P0 - Critical

```yaml
severity: P0
name: Critical
response_time: 15 minutes
resolution_target: 2 hours
notification:
  - immediate: ["on-call-engineer", "incident-commander", "security-team"]
  - within_1hr: ["engineering-leadership", "ciso", "legal"]
  - within_4hr: ["executive-team", "board-notification-if-required"]
characteristics:
  - Active data breach in progress
  - Model completely unavailable
  - Security compromise with data exfiltration
  - Systematic harmful outputs to users
  - Legal/regulatory violation in progress
impact:
  - All users affected
  - Revenue impact > $10K/hour
  - Reputational damage
  - Potential legal liability
examples:
  - Training data being exfiltrated
  - Model generating harmful content at scale
  - Complete inference service outage
  - Unauthorized model access confirmed
```

### P1 - High

```yaml
severity: P1
name: High
response_time: 30 minutes
resolution_target: 4 hours
notification:
  - immediate: ["on-call-engineer", "incident-commander"]
  - within_1hr: ["engineering-leadership", "security-team"]
  - within_4hr: ["product-leadership"]
characteristics:
  - Significant service degradation
  - Partial data breach (limited scope)
  - Security vulnerability being exploited
  - Model generating incorrect outputs consistently
  - Authentication system failures
impact:
  - >50% users affected
  - Revenue impact > $1K/hour
  - Data integrity concerns
  - Service level agreement breaches
examples:
  - API latency >5x normal for >30 minutes
  - Prompt injection affecting subset of users
  - Model returning sensitive information
  - Authentication service degraded
```

### P2 - Medium

```yaml
severity: P2
name: Medium
response_time: 2 hours
resolution_target: 24 hours
notification:
  - immediate: ["on-call-engineer"]
  - within_4hr: ["engineering-leadership"]
  - within_24hr: ["product-leadership"]
characteristics:
  - Minor service degradation
  - Non-sensitive data exposure
  - Model quality regression
  - Performance below SLA but functional
impact:
  - <50% users affected
  - Minor revenue impact
  - User experience degradation
  - Increased support tickets
examples:
  - Increased hallucination rate
  - Latency spike <2x normal
  - Intermittent API errors
  - Model output quality decline
```

### P3 - Low

```yaml
severity: P3
name: Low
response_time: 24 hours
resolution_target: 1 week
notification:
  - immediate: ["assigned-engineer"]
  - within_1week: ["engineering-leadership"]
characteristics:
  - Minor issues with workarounds
  - Cosmetic output problems
  - Non-urgent optimization needs
  - Edge case model failures
impact:
  - Minimal user impact
  - No revenue impact
  - Workaround available
examples:
  - Occasional odd responses
  - Minor formatting issues
  - Slow but successful operations
  - Edge case handling
```

### Severity Matrix

```
                    IMPACT
                    Low         Medium       High         Critical
LIKELIHOOD  ┌──────────┬──────────┬──────────┬──────────┐
High        │   P2     │   P1     │   P0     │   P0     │
            ├──────────┼──────────┼──────────┼──────────┤
Medium      │   P3     │   P2     │   P1     │   P0     │
            ├──────────┼──────────┼──────────┼──────────┤
Low         │   P3     │   P3     │   P2     │   P1     │
            ├──────────┼──────────┼──────────┼──────────┤
Rare        │   P3     │   P3     │   P3     │   P2     │
            └──────────┴──────────┴──────────┴──────────┘
```

---

## Response Lifecycle

### Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     INCIDENT RESPONSE LIFECYCLE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │
│   │ DETECT   │───▶│  TRIAGE  │───▶│ CONTAIN  │───▶│ERADICATE │    │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘    │
│        │              │               │               │            │
│        ▼              ▼               ▼               ▼            │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │
│   │ MONITOR  │◀───│  DECIDE  │◀───│ ASSESS   │◀───│ RECOVER  │    │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘    │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐                                                   │
│   │POST-MORTEM│                                                  │
│   └──────────┘                                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Detection

```python
class IncidentDetection:
    """Automated incident detection for LLM systems."""

    def __init__(self, config: Dict):
        self.config = config
        self.detection_rules = self._load_detection_rules()

    def _load_detection_rules(self) -> List[Dict]:
        return [
            {
                "name": "safety_violation",
                "condition": "output_safety_score < 0.3",
                "severity": "P0",
                "auto_escalate": True
            },
            {
                "name": "latency_spike",
                "condition": "p99_latency > baseline * 2",
                "severity": "P1",
                "auto_escalate": False
            },
            {
                "name": "error_rate_spike",
                "condition": "error_rate > 0.05",
                "severity": "P1",
                "auto_escalate": True
            },
            {
                "name": "hallucination_surge",
                "condition": "hallucination_rate > baseline * 3",
                "severity": "P2",
                "auto_escalate": False
            },
            {
                "name": "data_exfiltration_attempt",
                "condition": "exfiltration_score > 0.8",
                "severity": "P0",
                "auto_escalate": True
            }
        ]

    def evaluate_metrics(self, metrics: Dict) -> List[Dict]:
        """Evaluate current metrics against detection rules."""
        triggered = []

        for rule in self.detection_rules:
            if self._check_condition(rule["condition"], metrics):
                triggered.append({
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "auto_escalate": rule["auto_escalate"],
                    "metrics": metrics,
                    "timestamp": self._get_timestamp()
                })

        return triggered

    def _check_condition(self, condition: str, metrics: Dict) -> bool:
        """Evaluate a detection condition against current metrics."""
        # Simplified condition evaluation
        try:
            # In production, use a proper expression evaluator
            parts = condition.split()
            metric_name = parts[0]
            operator = parts[1]
            threshold = float(parts[2].replace("baseline", "").strip("* ") if "baseline" in parts[2] else parts[2])

            actual = metrics.get(metric_name, 0)
            baseline = metrics.get(f"baseline_{metric_name}", 1)

            if "baseline" in condition:
                threshold = baseline * threshold

            if operator == ">":
                return actual > threshold
            elif operator == "<":
                return actual < threshold
            elif operator == ">=":
                return actual >= threshold
            elif operator == "<=":
                return actual <= threshold

        except Exception:
            return False

        return False
```

### Phase 2: Triage

```yaml
triage_process:
  step_1_initial_assessment:
    duration: "5 minutes"
    actions:
      - Verify incident is real (not false positive)
      - Determine severity level
      - Check if known issue
      - Assess blast radius

  step_2_classification:
    duration: "10 minutes"
    categories:
      - security: "Prompt injection, data breach, unauthorized access"
      - performance: "Latency, throughput, availability"
      - quality: "Hallucination, bias, output degradation"
      - data: "Training data issues, PII exposure, data drift"

  step_3_assignment:
    duration: "5 minutes"
    roles:
      incident_commander: "Owns the incident, coordinates response"
      technical_lead: "Leads technical investigation"
      communications: "Manages stakeholder updates"
      scribe: "Documents timeline and decisions"

  step_4_response_plan:
    duration: "10 minutes"
    actions:
      - Identify containment strategy
      - Determine if rollback needed
      - Assess data exposure
      - Plan communication timeline
```

### Phase 3: Containment

```python
class ContainmentStrategy:
    """Containment strategies for different incident types."""

    @staticmethod
    def contain_prompt_injection(config: Dict) -> Dict:
        """Contain prompt injection incidents."""
        return {
            "immediate": [
                "Enable enhanced input filtering",
                "Activate output content moderation",
                "Rate limit affected endpoints",
                "Block suspicious IP ranges"
            ],
            "short_term": [
                "Update prompt injection detection rules",
                "Strengthen system prompt isolation",
                "Add output validation layers",
                "Review and rotate API keys"
            ],
            "validation": [
                "Test containment measures",
                "Verify no legitimate traffic blocked",
                "Monitor for attack adaptation"
            ]
        }

    @staticmethod
    def contain_data_breach(config: Dict) -> Dict:
        """Contain data breach incidents."""
        return {
            "immediate": [
                "Isolate affected systems",
                "Revoke compromised credentials",
                "Enable enhanced logging",
                "Notify security team",
                "Preserve forensic evidence"
            ],
            "short_term": [
                "Reset affected user sessions",
                "Update access controls",
                "Review data exposure scope",
                "Engage legal counsel"
            ],
            "regulatory": [
                "Assess notification requirements",
                "Prepare breach notifications",
                "Document timeline for regulators"
            ]
        }

    @staticmethod
    def contain_model_failure(config: Dict) -> Dict:
        """Contain model failure incidents."""
        return {
            "immediate": [
                "Route traffic to fallback model",
                "Enable circuit breaker",
                "Reduce request throughput",
                "Increase monitoring granularity"
            ],
            "short_term": [
                "Identify failure root cause",
                "Rollback to previous model version",
                "Update model serving configuration",
                "Review model deployment pipeline"
            ],
            "recovery": [
                "Validate model performance",
                "Gradually restore traffic",
                "Monitor for regression"
            ]
        }
```

### Phase 4: Eradication

```yaml
eradication_checklist:
  security_incidents:
    - Remove compromised access
    - Patch vulnerability
    - Update security controls
    - Validate no persistence mechanisms
    - Conduct security scan

  model_incidents:
    - Identify and fix model issue
    - Retrain if necessary
    - Validate model performance
    - Test edge cases
    - Deploy updated model

  data_incidents:
    - Identify data source
    - Remove exposed data
    - Update data handling
    - Validate data integrity
    - Review access controls
```

### Phase 5: Recovery

```python
class RecoveryPlan:
    """Structured recovery planning for incident response."""

    def __init__(self, incident: Dict):
        self.incident = incident
        self.recovery_steps = []

    def create_recovery_plan(self) -> Dict:
        """Create a comprehensive recovery plan."""
        plan = {
            "incident_id": self.incident["id"],
            "created_at": self._get_timestamp(),
            "recovery_phases": []
        }

        # Phase 1: System Recovery
        plan["recovery_phases"].append({
            "phase": "system_recovery",
            "steps": [
                "Verify system health",
                "Restore from backup if needed",
                "Validate data integrity",
                "Test core functionality"
            ],
            "success_criteria": [
                "All systems operational",
                "Data integrity verified",
                "No residual vulnerabilities"
            ]
        })

        # Phase 2: Service Restoration
        plan["recovery_phases"].append({
            "phase": "service_restoration",
            "steps": [
                "Enable service gradually",
                "Monitor key metrics",
                "Validate user experience",
                "Confirm performance baseline"
            ],
            "success_criteria": [
                "Service handling traffic",
                "Metrics within normal range",
                "No user complaints"
            ]
        })

        # Phase 3: Validation
        plan["recovery_phases"].append({
            "phase": "validation",
            "steps": [
                "Conduct security review",
                "Validate incident fully resolved",
                "Verify prevention measures",
                "Document lessons learned"
            ],
            "success_criteria": [
                "Security review passed",
                "Incident confirmed resolved",
                "Prevention measures active"
            ]
        })

        return plan

    def validate_recovery(self, metrics: Dict) -> Dict:
        """Validate that recovery is complete and successful."""
        validation = {
            "complete": True,
            "checks": []
        }

        # Check 1: System health
        health_check = metrics.get("system_health", {})
        validation["checks"].append({
            "name": "system_health",
            "passed": health_check.get("status") == "healthy",
            "details": health_check
        })

        # Check 2: Performance baseline
        perf_check = metrics.get("performance", {})
        validation["checks"].append({
            "name": "performance_baseline",
            "passed": perf_check.get("latency_p99", 0) < perf_check.get("baseline_p99", float("inf")) * 1.2,
            "details": perf_check
        })

        # Check 3: Security controls
        security_check = metrics.get("security", {})
        validation["checks"].append({
            "name": "security_controls",
            "passed": security_check.get("vulnerabilities", 999) == 0,
            "details": security_check
        })

        validation["complete"] = all(c["passed"] for c in validation["checks"])
        return validation
```

### Phase 6: Post-Mortem

```yaml
post_mortem_template:
  incident_summary:
    - Incident ID
    - Date and time
    - Duration
    - Severity
    - Impact summary

  timeline:
    - Detection time
    - Triage start
    - Containment start
    - Eradication start
    - Recovery start
    - Resolution time

  root_cause_analysis:
    - Primary cause
    - Contributing factors
    - Why detection was delayed (if applicable)
    - Why containment took as long as it did

  lessons_learned:
    - What went well
    - What could be improved
    - Action items with owners and deadlines

  prevention_measures:
    - Technical improvements
    - Process improvements
    - Monitoring enhancements
    - Training needs
```

---

## Roles and Responsibilities

### Incident Commander

```yaml
role: Incident Commander
responsibilities:
  - Own the incident from detection to resolution
  - Make escalation decisions
  - Coordinate cross-functional response
  - Ensure clear communication
  - Drive post-mortem process

authority:
  - Can declare incidents
  - Can escalate to any level
  - Can authorize emergency changes
  - Can freeze deployments

skills_required:
  - Technical understanding of LLM systems
  - Leadership under pressure
  - Communication skills
  - Decision-making ability
  - Calm demeanor
```

### Technical Lead

```yaml
role: Technical Lead
responsibilities:
  - Lead technical investigation
  - Implement containment measures
  - Coordinate remediation efforts
  - Validate fixes
  - Document technical findings

authority:
  - Can modify system configuration
  - Can deploy hotfixes
  - Can access diagnostic tools
  - Can request additional resources

skills_required:
  - Deep LLM system knowledge
  - Debugging expertise
  - Security understanding
  - System architecture knowledge
```

### Communications Lead

```yaml
role: Communications Lead
responsibilities:
  - Manage internal communications
  - Draft external communications
  - Coordinate with legal/regulatory
  - Update stakeholders
  - Manage support team messaging

authority:
  - Can approve external communications
  - Can coordinate with legal
  - Can update status pages
  - Can notify affected parties

skills_required:
  - Clear writing skills
  - Stakeholder management
  - Crisis communication
  - Legal awareness
```

### Scribe

```yaml
role: Scribe
responsibilities:
  - Document incident timeline
  - Record decisions made
  - Track action items
  - Capture technical details
  - Prepare post-mortem draft

authority:
  - Can request information from responders
  - Can access incident channels
  - Can create documentation

skills_required:
  - Attention to detail
  - Fast documentation
  - Technical understanding
  - Organization
```

---

## Communication Protocols

### Internal Communication

```python
class IncidentCommunicator:
    """Handles all incident-related communications."""

    def __init__(self, config: Dict):
        self.config = config
        self.channels = {
            "slack": config.get("slack_channel"),
            "email": config.get("email_distribution"),
            "pager": config.get("pager_service"),
            "status_page": config.get("status_page_url")
        }

    def notify_initial(self, incident: Dict):
        """Send initial incident notification."""
        message = self._format_initial_notification(incident)

        # Immediate notification to response team
        self._send_slack(self.channels["slack"]["response"], message)
        self._send_pager(self.config["on_call"], message)

        # Log notification
        self._log_notification("initial", incident, message)

    def notify_escalation(self, incident: Dict, new_severity: str):
        """Send escalation notification."""
        message = self._format_escalation(incident, new_severity)

        # Notify leadership
        self._send_email(self.channels["email"]["leadership"], message)
        self._send_slack(self.channels["slack"]["leadership"], message)

        self._log_notification("escalation", incident, message)

    def update_status_page(self, incident: Dict, status: str):
        """Update public status page."""
        update = {
            "incident_id": incident["id"],
            "status": status,
            "impact": incident["impact"],
            "updates": self._get_latest_updates(incident)
        }

        self._send_status_page_update(update)
        self._log_notification("status_page", incident, update)

    def send_resolution(self, incident: Dict):
        """Send incident resolution notification."""
        message = self._format_resolution(incident)

        # Notify all stakeholders
        self._send_email(self.channels["email"]["all"], message)
        self._send_slack(self.channels["slack"]["general"], message)
        self._update_status_page(incident, "resolved")

        self._log_notification("resolution", incident, message)

    def _format_initial_notification(self, incident: Dict) -> Dict:
        return {
            "title": f"🚨 Incident Declared: {incident['title']}",
            "severity": incident["severity"],
            "summary": incident["summary"],
            "impact": incident["impact"],
            "commander": incident["commander"],
            "war_room": incident["war_room_link"],
            "next_update": "In 30 minutes or upon significant change"
        }

    def _format_escalation(self, incident: Dict, new_severity: str) -> Dict:
        return {
            "title": f"⚠️ Incident Escalated to {new_severity}",
            "incident_id": incident["id"],
            "previous_severity": incident["severity"],
            "new_severity": new_severity,
            "reason": incident.get("escalation_reason", "Unknown"),
            "current_impact": incident["impact"],
            "actions_taken": incident.get("actions_taken", [])
        }

    def _format_resolution(self, incident: Dict) -> Dict:
        return {
            "title": f"✅ Incident Resolved: {incident['title']}",
            "incident_id": incident["id"],
            "duration": incident.get("duration", "Unknown"),
            "resolution": incident["resolution"],
            "post_mortem_link": incident.get("post_mortem_link"),
            "follow_up_items": incident.get("follow_up_items", [])
        }

    def _send_slack(self, channel: str, message: Dict):
        """Send Slack notification."""
        # Implementation depends on Slack API client
        pass

    def _send_email(self, recipients: str, message: Dict):
        """Send email notification."""
        # Implementation depends on email service
        pass

    def _send_pager(self, target: str, message: Dict):
        """Send pager notification."""
        # Implementation depends on pager service
        pass

    def _send_status_page_update(self, update: Dict):
        """Send status page update."""
        # Implementation depends on status page service
        pass

    def _log_notification(self, notification_type: str, incident: Dict, content: Dict):
        """Log notification for audit trail."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "type": notification_type,
            "incident_id": incident["id"],
            "content": content
        }
        # Store in audit log
        pass

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### External Communication Templates

```yaml
user_notification:
  template: |
    We're currently experiencing issues with [SERVICE].
    
    What's happening: [BRIEF_DESCRIPTION]
    Impact: [USER_IMPACT]
    Current status: [STATUS]
    Expected resolution: [ETA]
    
    We'll provide updates every [INTERVAL] or sooner if status changes.
    
    For questions, please contact [SUPPORT_CHANNEL].

regulatory_notification:
  template: |
    Date of incident: [DATE]
    Date of discovery: [DISCOVERY_DATE]
    Description: [DESCRIPTION]
    Data affected: [DATA_TYPES]
    Individuals affected: [AFFECT_COUNT]
    Measures taken: [ACTIONS]
    Contact: [DPO_CONTACT]
    
    Per [REGULATION] requirements, we are notifying you of this incident.

media_statement:
  template: |
    We are aware of [INCIDENT_DESCRIPTION] and are taking immediate action
    to address it. Our security and engineering teams are working to resolve
    the issue. We will provide updates as we learn more.
    
    [COMPANY] takes the security and privacy of our users' data very
    seriously. We are conducting a thorough investigation and will share
    findings as appropriate.
```

---

## Incident Detection

### Monitoring Stack for LLM Systems

```yaml
monitoring_configuration:
  metrics:
    inference:
      - latency_p50
      - latency_p95
      - latency_p99
      - throughput_rps
      - error_rate
      - timeout_rate
    
    model:
      - hallucination_rate
      - safety_score_avg
      - output_quality_score
      - token_usage_avg
      - context_window_utilization
    
    system:
      - cpu_utilization
      - memory_utilization
      - gpu_utilization
      - gpu_memory_used
      - network_io
    
    business:
      - active_users
      - request_count
      - conversion_rate
      - user_satisfaction_score

  alerts:
    - name: "high_latency"
      metric: "latency_p99"
      condition: "> 5000"
      duration: "5m"
      severity: "P2"
      notify: ["on-call"]
    
    - name: "error_spike"
      metric: "error_rate"
      condition: "> 0.05"
      duration: "2m"
      severity: "P1"
      notify: ["on-call", "engineering-lead"]
    
    - name: "safety_violation"
      metric: "safety_score_avg"
      condition: "< 0.5"
      duration: "1m"
      severity: "P0"
      notify: ["on-call", "engineering-lead", "security"]
    
    - name: "hallucination_surge"
      metric: "hallucination_rate"
      condition: "> 0.1"
      duration: "10m"
      severity: "P1"
      notify: ["on-call", "ml-team"]

  dashboards:
    - name: "llm_health_overview"
      panels:
        - title: "Inference Latency"
          type: "timeseries"
          metrics: ["latency_p50", "latency_p95", "latency_p99"]
        
        - title: "Error Rate"
          type: "gauge"
          metrics: ["error_rate"]
          thresholds: [0.01, 0.05, 0.1]
        
        - title: "Safety Score"
          type: "timeseries"
          metrics: ["safety_score_avg"]
          alerts: ["safety_violation"]
        
        - title: "Hallucination Rate"
          type: "timeseries"
          metrics: ["hallucination_rate"]
          alerts: ["hallucination_surge"]
```

### Automated Detection Rules

```python
class AutomatedDetector:
    """Automated incident detection with alerting."""

    def __init__(self, alerting_client, metrics_client):
        self.alerting = alerting_client
        self.metrics = metrics_client
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Dict]:
        return [
            {
                "name": "anomalous_output_pattern",
                "description": "Detect unusual output patterns that may indicate model compromise",
                "check": self._check_output_anomaly,
                "severity": "P1",
                "cooldown_minutes": 30
            },
            {
                "name": "prompt_injection_attempt",
                "description": "Detect potential prompt injection in user inputs",
                "check": self._check_injection_pattern,
                "severity": "P0",
                "cooldown_minutes": 5
            },
            {
                "name": "data_exfiltration_signal",
                "description": "Detect patterns suggesting data exfiltration",
                "check": self._check_exfiltration_signal,
                "severity": "P0",
                "cooldown_minutes": 10
            },
            {
                "name": "model_degradation",
                "description": "Detect model performance degradation",
                "check": self._check_model_degradation,
                "severity": "P2",
                "cooldown_minutes": 60
            }
        ]

    def run_detection_cycle(self) -> List[Dict]:
        """Run all detection rules and return triggered alerts."""
        triggered = []

        for rule in self.rules:
            try:
                result = rule["check"]()
                if result["triggered"]:
                    # Check cooldown
                    if not self._in_cooldown(rule["name"], rule["cooldown_minutes"]):
                        alert = {
                            "rule": rule["name"],
                            "description": rule["description"],
                            "severity": rule["severity"],
                            "details": result["details"],
                            "timestamp": self._get_timestamp()
                        }
                        triggered.append(alert)
                        self.alerting.send_alert(alert)
                        self._update_cooldown(rule["name"])

            except Exception as e:
                # Detection failure is itself an incident
                self.alerting.send_alert({
                    "rule": f"{rule['name']}_failure",
                    "severity": "P2",
                    "details": {"error": str(e)},
                    "timestamp": self._get_timestamp()
                })

        return triggered

    def _check_output_anomaly(self) -> Dict:
        """Check for anomalous output patterns."""
        recent_outputs = self.metrics.get_recent("output_samples", count=100)

        if len(recent_outputs) < 10:
            return {"triggered": False, "reason": "insufficient_data"}

        # Check for unusual patterns
        safety_scores = [o.get("safety_score", 1.0) for o in recent_outputs]
        avg_safety = sum(safety_scores) / len(safety_scores)

        low_safety_count = sum(1 for s in safety_scores if s < 0.5)
        low_safety_rate = low_safety_count / len(safety_scores)

        return {
            "triggered": low_safety_rate > 0.1,
            "details": {
                "avg_safety_score": avg_safety,
                "low_safety_rate": low_safety_rate,
                "sample_count": len(recent_outputs)
            }
        }

    def _check_injection_pattern(self) -> Dict:
        """Check for prompt injection patterns."""
        recent_inputs = self.metrics.get_recent("input_samples", count=100)

        injection_patterns = [
            "ignore previous instructions",
            "you are now",
            "forget everything",
            "new system prompt",
            "override",
            "bypass"
        ]

        detected = 0
        for input_sample in recent_inputs:
            text = input_sample.get("text", "").lower()
            for pattern in injection_patterns:
                if pattern in text:
                    detected += 1
                    break

        detection_rate = detected / max(len(recent_inputs), 1)

        return {
            "triggered": detection_rate > 0.05,  # > 5% injection attempts
            "details": {
                "detection_rate": detection_rate,
                "detected_count": detected,
                "sample_count": len(recent_inputs)
            }
        }

    def _check_exfiltration_signal(self) -> Dict:
        """Check for data exfiltration signals."""
        recent_outputs = self.metrics.get_recent("output_samples", count=100)

        import re
        pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{16}\b',              # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
        ]

        pii_count = 0
        for output in recent_outputs:
            text = output.get("text", "")
            for pattern in pii_patterns:
                if re.search(pattern, text):
                    pii_count += 1
                    break

        pii_rate = pii_count / max(len(recent_outputs), 1)

        return {
            "triggered": pii_rate > 0.01,  # > 1% outputs contain PII
            "details": {
                "pii_rate": pii_rate,
                "pii_count": pii_count,
                "sample_count": len(recent_outputs)
            }
        }

    def _check_model_degradation(self) -> Dict:
        """Check for model performance degradation."""
        current_metrics = self.metrics.get_current()
        baseline = self.metrics.get_baseline("1h")

        degradation_signals = []

        # Check latency
        if current_metrics.get("latency_p99", 0) > baseline.get("latency_p99", 0) * 1.5:
            degradation_signals.append("latency")

        # Check error rate
        if current_metrics.get("error_rate", 0) > baseline.get("error_rate", 0) * 2:
            degradation_signals.append("error_rate")

        # Check quality
        if current_metrics.get("quality_score", 1) < baseline.get("quality_score", 1) * 0.9:
            degradation_signals.append("quality")

        return {
            "triggered": len(degradation_signals) >= 2,
            "details": {
                "degradation_signals": degradation_signals,
                "current": current_metrics,
                "baseline": baseline
            }
        }

    def _in_cooldown(self, rule_name: str, cooldown_minutes: int) -> bool:
        """Check if rule is in cooldown period."""
        # Implementation depends on storage backend
        return False

    def _update_cooldown(self, rule_name: str):
        """Update cooldown timestamp for a rule."""
        # Implementation depends on storage backend
        pass

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

---

## Triage Process

### Triage Decision Tree

```
                    ┌─────────────────┐
                    │  INCIDENT        │
                    │  DETECTED        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Is it a        │
                    │  security       │
                    │  incident?      │
                    └────────┬────────┘
                      ┌──────┴──────┐
                      │             │
                    Yes            No
                      │             │
              ┌───────▼───────┐    │
              │ Is data        │    │
              │ exfiltrated?   │    │
              └───────┬───────┘    │
                ┌─────┴─────┐      │
                │           │      │
              Yes          No      │
                │           │      │
        ┌───────▼───┐  ┌───▼───┐  │
        │   P0      │  │  P1   │  │
        │  BREACH   │  │ ATTACK│  │
        └───────────┘  └───────┘  │
                                  │
                    ┌─────────────▼─────────────┐
                    │  Is the service            │
                    │  degraded or down?         │
                    └─────────────┬─────────────┘
                      ┌───────────┴───────────┐
                      │                       │
                    Yes                       No
                      │                       │
              ┌───────▼───────┐       ┌───────▼───────┐
              │ >50% users    │       │  Is model     │
              │ affected?     │       │  output       │
              └───────┬───────┘       │  degraded?    │
                ┌─────┴─────┐         └───────┬───────┘
                │           │           ┌─────┴─────┐
              Yes          No          Yes          No
                │           │           │           │
        ┌───────▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐
        │   P1      │  │  P2   │  │  P2   │  │  P3   │
        │  OUTAGE   │  │ DEGRAD│  │QUALITY│  │ MINOR │
        └───────────┘  └───────┘  └───────┘  └───────┘
```

### Triage Checklist

```yaml
triage_checklist:
  initial_assessment:
    - [ ] Incident is verified (not false positive)
    - [ ] Initial severity assigned
    - [ ] Incident commander assigned
    - [ ] War room created
    - [ ] Initial stakeholders notified

  classification:
    - [ ] Incident type determined
    - [ ] Blast radius assessed
    - [ ] Data exposure evaluated
    - [ ] User impact quantified
    - [ ] Revenue impact estimated

  response_plan:
    - [ ] Containment strategy selected
    - [ ] Technical lead assigned
    - [ ] Communications lead assigned
    - [ ] Scribe assigned
    - [ ] Next update time set

  documentation:
    - [ ] Incident ticket created
    - [ ] Timeline started
    - [ ] Initial actions documented
    - [ ] Decisions recorded
    - [ ] Communication log started
```

---

## Containment Strategies

### Immediate Containment

```python
class ImmediateContainment:
    """Quick containment actions for various incident types."""

    @staticmethod
    def rate_limit_by_pattern(pattern: str, limit: int, window: int):
        """Implement rate limiting based on request patterns."""
        return {
            "action": "rate_limit",
            "pattern": pattern,
            "limit": f"{limit} requests per {window} seconds",
            "scope": "affected_endpoints",
            "duration": "until incident resolved"
        }

    @staticmethod
    def block_malicious_ips(ip_ranges: List[str]):
        """Block identified malicious IP ranges."""
        return {
            "action": "block_ips",
            "ranges": ip_ranges,
            "scope": "all_endpoints",
            "duration": "until incident resolved",
            "review": "24 hours"
        }

    @staticmethod
    def enable_enhanced_filtering():
        """Enable additional input/output filtering."""
        return {
            "action": "enable_filtering",
            "filters": [
                "injection_detection",
                "pii_detection",
                "safety_scoring"
            ],
            "scope": "all_endpoints",
            "duration": "until incident resolved"
        }

    @staticmethod
    def switch_to_fallback_model():
        """Switch to fallback model during incident."""
        return {
            "action": "model_switch",
            "from": "primary_model",
            "to": "fallback_model",
            "reason": "primary model incident",
            "duration": "until primary validated",
            "validation_required": True
        }

    @staticmethod
    def enable_circuit_breaker(failure_threshold: int = 5, recovery_timeout: int = 60):
        """Enable circuit breaker for affected endpoints."""
        return {
            "action": "circuit_breaker",
            "failure_threshold": failure_threshold,
            "recovery_timeout": recovery_timeout,
            "scope": "affected_endpoints",
            "fallback_response": "service_temporarily_unavailable"
        }
```

### Containment Validation

```yaml
containment_validation:
  security_incidents:
    - [ ] Malicious traffic blocked
    - [ ] Compromised credentials revoked
    - [ ] Vulnerable endpoint disabled
    - [ ] Enhanced monitoring active
    - [ ] Forensic evidence preserved

  model_incidents:
    - [ ] Traffic rerouted successfully
    - [ ] Fallback model operational
    - [ ] Performance acceptable
    - [ ] No data loss
    - [ ] Users notified if affected

  data_incidents:
    - [ ] Data source isolated
    - [ ] Access controls updated
    - [ ] Affected data identified
    - [ ] Legal team notified
    - [ ] Regulatory timeline documented
```

---

## Remediation Framework

### Remediation Planning

```python
class RemediationPlanner:
    """Create structured remediation plans for incidents."""

    def __init__(self, incident: Dict):
        self.incident = incident

    def create_remediation_plan(self) -> Dict:
        """Generate a comprehensive remediation plan."""
        plan = {
            "incident_id": self.incident["id"],
            "remediation_items": []
        }

        # Root cause remediation
        plan["remediation_items"].append({
            "category": "root_cause",
            "description": "Address the root cause of the incident",
            "actions": self._get_root_cause_actions(),
            "priority": "high",
            "deadline": self._calculate_deadline("root_cause")
        })

        # Prevention measures
        plan["remediation_items"].append({
            "category": "prevention",
            "description": "Implement measures to prevent recurrence",
            "actions": self._get_prevention_actions(),
            "priority": "medium",
            "deadline": self._calculate_deadline("prevention")
        })

        # Detection improvements
        plan["remediation_items"].append({
            "category": "detection",
            "description": "Improve detection capabilities",
            "actions": self._get_detection_improvements(),
            "priority": "medium",
            "deadline": self._calculate_deadline("detection")
        })

        # Process improvements
        plan["remediation_items"].append({
            "category": "process",
            "description": "Improve incident response processes",
            "actions": self._get_process_improvements(),
            "priority": "low",
            "deadline": self._calculate_deadline("process")
        })

        return plan

    def _get_root_cause_actions(self) -> List[Dict]:
        """Get actions based on incident type."""
        incident_type = self.incident.get("type", "unknown")

        actions_map = {
            "prompt_injection": [
                {"action": "Update input validation", "owner": "security_team"},
                {"action": "Strengthen system prompt isolation", "owner": "ml_team"},
                {"action": "Add output content filtering", "owner": "ml_team"}
            ],
            "data_breach": [
                {"action": "Patch vulnerability", "owner": "security_team"},
                {"action": "Rotate compromised credentials", "owner": "security_team"},
                {"action": "Update access controls", "owner": "platform_team"}
            ],
            "model_failure": [
                {"action": "Identify model issue", "owner": "ml_team"},
                {"action": "Retrain model if needed", "owner": "ml_team"},
                {"action": "Update model validation", "owner": "ml_team"}
            ],
            "performance": [
                {"action": "Optimize inference pipeline", "owner": "platform_team"},
                {"action": "Scale infrastructure", "owner": "infrastructure_team"},
                {"action": "Update capacity planning", "owner": "platform_team"}
            ]
        }

        return actions_map.get(incident_type, [
            {"action": "Investigate root cause", "owner": "engineering"},
            {"action": "Implement fix", "owner": "engineering"}
        ])

    def _get_prevention_actions(self) -> List[Dict]:
        return [
            {"action": "Add monitoring for this failure mode", "owner": "sre_team"},
            {"action": "Update runbooks", "owner": "engineering"},
            {"action": "Conduct security review", "owner": "security_team"},
            {"action": "Update training data", "owner": "ml_team"}
        ]

    def _get_detection_improvements(self) -> List[Dict]:
        return [
            {"action": "Add automated detection rule", "owner": "sre_team"},
            {"action": "Update alert thresholds", "owner": "sre_team"},
            {"action": "Add dashboard panel", "owner": "sre_team"}
        ]

    def _get_process_improvements(self) -> List[Dict]:
        return [
            {"action": "Update incident response playbook", "owner": "engineering"},
            {"action": "Conduct tabletop exercise", "owner": "security_team"},
            {"action": "Update communication templates", "owner": "comms_team"}
        ]

    def _calculate_deadline(self, category: str) -> str:
        """Calculate deadline based on category and severity."""
        from datetime import datetime, timedelta

        severity = self.incident.get("severity", "P3")

        deadlines = {
            "root_cause": {"P0": 1, "P1": 7, "P2": 14, "P3": 30},
            "prevention": {"P0": 7, "P1": 14, "P2": 30, "P3": 60},
            "detection": {"P0": 14, "P1": 30, "P2": 60, "P3": 90},
            "process": {"P0": 30, "P1": 60, "P2": 90, "P3": 180}
        }

        days = deadlines.get(category, {}).get(severity, 30)
        deadline = datetime.utcnow() + timedelta(days=days)
        return deadline.isoformat()
```

---

## Post-Mortem Process

### Post-Mortem Template

```markdown
# Incident Post-Mortem: [INCIDENT_TITLE]

## Summary

| Field | Value |
|-------|-------|
| Incident ID | [ID] |
| Date | [DATE] |
| Duration | [DURATION] |
| Severity | [P0-P3] |
| Commander | [NAME] |
| Status | Resolved |

## Impact

- **Users affected:** [NUMBER] ([PERCENTAGE] of total)
- **Duration of impact:** [TIME]
- **Revenue impact:** [AMOUNT] (estimated)
- **Data exposure:** [YES/NO, DETAILS IF YES]
- **SLA impact:** [YES/NO, DETAILS IF YES]

## Timeline (UTC)

| Time | Event | Actor |
|------|-------|-------|
| HH:MM | Incident detected | [SYSTEM/PERSON] |
| HH:MM | Triage started | [PERSON] |
| HH:MM | Containment initiated | [PERSON] |
| HH:MM | Root cause identified | [PERSON] |
| HH:MM | Fix deployed | [PERSON] |
| HH:MM | Incident resolved | [PERSON] |

## Root Cause

[Detailed description of what caused the incident]

## What Went Well

- [LIST OF THINGS THAT WENT WELL]

## What Could Be Improved

- [LIST OF IMPROVEMENT OPPORTUNITIES]

## Action Items

| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| [ACTION] | [OWNER] | [P0-P3] | [DATE] | Open |

## Lessons Learned

[KEY TAKEAWAYS FROM THIS INCIDENT]

## Supporting Data

- [LINKS TO LOGS, GRAPHS, EVIDENCE]
```

### Post-Mortem Meeting Agenda

```yaml
post_mortem_meeting:
  duration: "60 minutes"
  attendees:
    - Incident Commander
    - Technical Lead
    - Communications Lead
    - Scribe
    - Engineering Leadership
    - Affected Team Members

  agenda:
    - time: "0-5 min"
      topic: "Review incident summary"
      owner: "Incident Commander"
    
    - time: "5-20 min"
      topic: "Walk through timeline"
      owner: "Scribe"
    
    - time: "20-35 min"
      topic: "Discuss root cause"
      owner: "Technical Lead"
    
    - time: "35-45 min"
      topic: "Review action items"
      owner: "Incident Commander"
    
    - time: "45-55 min"
      topic: "Discuss prevention measures"
      owner: "All"
    
    - time: "55-60 min"
      topic: "Next steps and follow-up"
      owner: "Incident Commander"

  rules:
    - Focus on systems, not individuals
    - Blameless environment
    - Action items must have owners and deadlines
    - Document everything
    - Follow up on action items
```

---

## LLM-Specific Threats

### Threat Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LLM THREAT MATRIX                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT THREATS              │  OUTPUT THREATS                        │
│  ─────────────              │  ──────────────                        │
│  • Prompt Injection         │  • Hallucination                       │
│  • Indirect Injection       │  • Data Leakage                        │
│  • Jailbreak Attempts       │  • Harmful Content                     │
│  • Token Overflow           │  • Misinformation                      │
│  • Context Manipulation     │  • Bias Amplification                  │
│                             │                                        │
│  SYSTEM THREATS             │  DATA THREATS                          │
│  ─────────────              │  ────────────                          │
│  • Model Theft              │  • Training Data Exposure              │
│  • API Abuse                │  • PII in Outputs                      │
│  • Resource Exhaustion      │  • Model Inversion                     │
│  • Side-Channel Attacks     │  • Membership Inference                │
│  • Supply Chain Attacks     │  • Data Poisoning                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Incident Response for Prompt Injection

```python
class PromptInjectionResponse:
    """Specialized response procedures for prompt injection incidents."""

    def __init__(self, incident: Dict):
        self.incident = incident

    def detect_injection_type(self, input_text: str) -> Dict:
        """Classify the type of prompt injection."""
        types = {
            "direct_injection": {
                "patterns": [
                    "ignore previous",
                    "you are now",
                    "forget instructions",
                    "new system prompt"
                ],
                "severity": "high"
            },
            "indirect_injection": {
                "patterns": [
                    "from the document",
                    "according to the text",
                    "as mentioned in"
                ],
                "severity": "medium"
            },
            "jailbreak": {
                "patterns": [
                    "do anything now",
                    "developer mode",
                    " DAN",
                    "jailbreak"
                ],
                "severity": "high"
            },
            "context_manipulation": {
                "patterns": [
                    "the previous conversation was",
                    "let me remind you",
                    "we agreed that"
                ],
                "severity": "medium"
            }
        }

        detected_types = []
        input_lower = input_text.lower()

        for injection_type, config in types.items():
            for pattern in config["patterns"]:
                if pattern.lower() in input_lower:
                    detected_types.append({
                        "type": injection_type,
                        "severity": config["severity"],
                        "matched_pattern": pattern
                    })
                    break

        return {
            "input": input_text[:200] + "..." if len(input_text) > 200 else input_text,
            "injection_types": detected_types,
            "overall_severity": self._calculate_overall_severity(detected_types)
        }

    def _calculate_overall_severity(self, detected_types: List[Dict]) -> str:
        if not detected_types:
            return "none"

        severity_map = {"high": 3, "medium": 2, "low": 1}
        max_severity = max(severity_map.get(t["severity"], 0) for t in detected_types)

        for sev, val in severity_map.items():
            if val == max_severity:
                return sev

        return "low"

    def create_response_plan(self) -> Dict:
        """Create a response plan for the injection incident."""
        return {
            "incident_id": self.incident["id"],
            "response_type": "prompt_injection",
            "immediate_actions": [
                "Log full input and context for analysis",
                "Block the attacking user/session",
                "Review system prompt for weaknesses",
                "Check if injection succeeded"
            ],
            "investigation": [
                "Analyze attack vector",
                "Check for similar patterns in recent traffic",
                "Review system prompt isolation",
                "Assess what data/actions were exposed"
            ],
            "remediation": [
                "Update input validation",
                "Strengthen system prompt",
                "Add output filtering",
                "Update detection rules"
            ],
            "prevention": [
                "Implement input sanitization layer",
                "Add prompt injection detection",
                "Regular prompt security audits",
                "Red team testing"
            ]
        }
```

---

## Checklists

### P0 Incident Checklist

```yaml
p0_checklist:
  detection:
    - [ ] Incident confirmed (not false positive)
    - [ ] Severity verified as P0
    - [ ] Incident ticket created
    - [ ] War room initiated

  response:
    - [ ] Incident commander assigned
    - [ ] Technical lead assigned
    - [ ] Communications lead assigned
    - [ ] Scribe assigned
    - [ ] Initial notifications sent

  containment:
    - [ ] Containment strategy selected
    - [ ] Immediate actions executed
    - [ ] Containment validated
    - [ ] Evidence preserved

  communication:
    - [ ] Initial stakeholder notification
    - [ ] Status page updated
    - [ ] Regular updates scheduled
    - [ ] External communications prepared (if needed)

  resolution:
    - [ ] Root cause identified
    - [ ] Fix implemented
    - [ ] Service restored
    - [ ] Validation complete

  post_mortem:
    - [ ] Post-mortem scheduled
    - [ ] Timeline documented
    - [ ] Action items assigned
    - [ ] Follow-up plan created
```

### P1 Incident Checklist

```yaml
p1_checklist:
  detection:
    - [ ] Incident confirmed
    - [ ] Severity verified as P1
    - [ ] Incident ticket created

  response:
    - [ ] Incident commander assigned
    - [ ] Technical lead assigned
    - [ ] Initial notifications sent

  containment:
    - [ ] Containment strategy selected
    - [ ] Immediate actions executed
    - [ ] Containment validated

  communication:
    - [ ] Stakeholder notification
    - [ ] Regular updates scheduled

  resolution:
    - [ ] Root cause identified
    - [ ] Fix implemented
    - [ ] Service restored

  post_mortem:
    - [ ] Post-mortem scheduled
    - [ ] Action items assigned
```

---

## References

### Internal References

- [Incident Response Runbooks](./runbooks/)
- [Communication Templates](./templates/)
- [Escalation Matrix](./escalation/)
- [Post-Mortem Templates](./post-mortem/)

### External References

- NIST Computer Security Incident Handling Guide (SP 800-61)
- SANS Incident Response Process
- MITRE ATT&CK Framework
- OWASP AI Security Guide

---

*Last Updated: 2024*
*Version: 1.0*
*Owner: Security & Engineering Team*
