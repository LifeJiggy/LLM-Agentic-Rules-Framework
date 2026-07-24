# Incident Response Examples for LLM & Agentic AI Systems

## Table of Contents

1. [Overview](#overview)
2. [Security Incident Response](#security-incident)
3. [Data Breach Response](#data-breach)
4. [Model Failure Response](#model-failure)
5. [Performance Incident Response](#performance-incident)
6. [Prompt Injection Response](#prompt-injection)
7. [Hallucination Cascade Response](#hallucination)
8. [API Abuse Response](#api-abuse)
9. [Configuration Incident Response](#configuration-incident)
10. [Integration Failure Response](#integration-failure)

---

## Overview

This document provides practical, real-world examples of incident response for various types of incidents in LLM and Agentic AI systems. Each example includes detection, triage, containment, remediation, recovery, and post-mortem phases.

---

## Security Incident Response

### Example 1: Unauthorized Model Access

#### Scenario

```yaml
scenario:
  title: "Unauthorized Access to LLM Inference Endpoint"
  detection_time: "2024-01-15 02:30 UTC"
  severity: "P0"
  description: |
    Anomalous API access pattern detected - single API key making 
    10,000+ requests per minute to the inference endpoint from 
    multiple geographic locations. Key belongs to a test account 
    that should have minimal usage.
```

#### Detection

```python
class UnauthorizedAccessDetector:
    """Detect unauthorized access to LLM endpoints."""
    
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    def detect_anomaly(self, api_key: str) -> Dict:
        """Detect anomalous access patterns."""
        # Get recent usage for this API key
        usage = self.metrics.query(
            f'rate(llm_requests_total{{api_key="{api_key}"}}[5m])'
        )
        
        # Compare to baseline
        baseline = self.metrics.query(
            f'avg_over_time(llm_requests_total{{api_key="{api_key}"}}[7d])'
        )
        
        anomaly_score = usage / max(baseline, 1)
        
        if anomaly_score > 10:  # 10x normal usage
            return {
                "detected": True,
                "severity": "P0",
                "api_key": api_key,
                "current_rate": usage,
                "baseline_rate": baseline,
                "anomaly_score": anomaly_score
            }
        
        return {"detected": False}
```

#### Triage

```yaml
triage:
  classification:
    type: "security"
    subtype: "unauthorized_access"
    attack_vector: "compromised_api_key"
    affected_systems:
      - "llm-inference-endpoint"
      - "api-gateway"
  
  impact_assessment:
    users_affected: 0  # API key is test account
    data_exposure: "unknown"
    revenue_impact: "potential"
    sla_impact: "none"
  
  response_team:
    incident_commander: "security-lead"
    technical_lead: "platform-engineer"
    communications_lead: "engineering-manager"
    scribe: "security-analyst"
```

#### Containment

```python
class ContainmentActions:
    """Execute containment actions."""
    
    def __init__(self, config):
        self.config = config
    
    def execute_containment(self, api_key: str) -> Dict:
        """Execute containment actions."""
        actions = []
        
        # Action 1: Revoke compromised API key
        self._revoke_api_key(api_key)
        actions.append({"action": "revoke_api_key", "status": "completed"})
        
        # Action 2: Enable enhanced rate limiting
        self._enable_rate_limiting()
        actions.append({"action": "enable_rate_limiting", "status": "completed"})
        
        # Action 3: Block suspicious IPs
        suspicious_ips = self._get_suspicious_ips(api_key)
        self._block_ips(suspicious_ips)
        actions.append({"action": "block_ips", "count": len(suspicious_ips)})
        
        # Action 4: Enable enhanced logging
        self._enable_enhanced_logging()
        actions.append({"action": "enable_logging", "status": "completed"})
        
        # Action 5: Notify affected parties
        self._notify_parties()
        actions.append({"action": "notify_parties", "status": "completed"})
        
        return {"actions": actions}
    
    def _revoke_api_key(self, api_key: str):
        """Revoke the compromised API key."""
        # Implementation: API call to revoke key
        pass
    
    def _enable_rate_limiting(self):
        """Enable enhanced rate limiting."""
        # Implementation: Update rate limit config
        pass
    
    def _get_suspicious_ips(self, api_key: str) -> List[str]:
        """Get IPs associated with suspicious activity."""
        # Implementation: Query access logs
        return []
    
    def _block_ips(self, ips: List[str]):
        """Block suspicious IP addresses."""
        # Implementation: Update firewall rules
        pass
    
    def _enable_enhanced_logging(self):
        """Enable enhanced logging for investigation."""
        # Implementation: Update logging config
        pass
    
    def _notify_parties(self):
        """Notify relevant parties."""
        # Implementation: Send notifications
        pass
```

#### Investigation

```yaml
investigation:
  findings:
    - "API key was exposed in a public GitHub repository"
    - "Key was used to access inference endpoint from 15 countries"
    - "Approximately 500,000 requests made over 48 hours"
    - "No sensitive data exposed through inference responses"
    - "Attacker attempted to extract model information"
  
  timeline:
    - time: "2024-01-13 10:00"
      event: "API key pushed to public repository"
    - time: "2024-01-13 14:00"
      event: "First unauthorized access detected"
    - time: "2024-01-15 02:30"
      event: "Anomaly detected by monitoring"
    - time: "2024-01-15 02:35"
      event: "Incident declared, containment initiated"
    - time: "2024-01-15 02:45"
      event: "API key revoked, IPs blocked"
```

#### Remediation

```python
class RemediationPlan:
    """Implement remediation measures."""
    
    def __init__(self, incident: Dict):
        self.incident = incident
    
    def execute_remediation(self) -> Dict:
        """Execute remediation plan."""
        remediation = {
            "immediate": [
                "Rotate all API keys for affected service",
                "Implement automated secret scanning in CI/CD",
                "Enable API key expiration policy"
            ],
            "short_term": [
                "Implement API key usage monitoring",
                "Add geographic restrictions to API keys",
                "Implement request signing"
            ],
            "long_term": [
                "Migrate to OAuth 2.0 authentication",
                "Implement zero-trust architecture",
                "Add anomaly detection for API usage"
            ]
        }
        
        return remediation
```

#### Post-Mortem

```yaml
post_mortem:
  summary:
    title: "Unauthorized API Key Access"
    severity: "P0"
    duration: "48 hours"
    impact: "API key compromised, no data breach"
  
  root_cause:
    primary: "API key exposed in public GitHub repository"
    contributing:
      - "No automated secret scanning"
      - "No API key expiration policy"
      - "Insufficient access monitoring"
  
  what_went_well:
    - "Anomaly detection caught the issue"
    - "Containment was swift"
    - "No data breach occurred"
  
  what_could_improve:
    - "Implement automated secret scanning"
    - "Add API key expiration"
    - "Enhance access monitoring"
  
  action_items:
    - description: "Implement automated secret scanning"
      owner: "security-team"
      priority: "P1"
      due_date: "2024-02-01"
    
    - description: "Implement API key expiration"
      owner: "platform-team"
      priority: "P1"
      due_date: "2024-02-15"
    
    - description: "Enhance API usage monitoring"
      owner: "sre-team"
      priority: "P2"
      due_date: "2024-03-01"
```

---

## Data Breach Response

### Example 2: Training Data Exposure

#### Scenario

```yaml
scenario:
  title: "Training Data Exposure Through LLM Outputs"
  detection_time: "2024-02-01 14:20 UTC"
  severity: "P0"
  description: |
    Users reported receiving outputs containing what appears to be
    personal information (emails, phone numbers) from training data.
    Investigation reveals model memorizing and regurgitating training data.
```

#### Detection

```python
class TrainingDataLeakDetector:
    """Detect training data leakage in LLM outputs."""
    
    def __init__(self):
        self.pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b'
        }
    
    def analyze_output(self, output: str) -> Dict:
        """Analyze output for PII patterns."""
        import re
        
        findings = []
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, output)
            if matches:
                findings.append({
                    "type": pii_type,
                    "count": len(matches),
                    "samples": matches[:3]  # First 3 for investigation
                })
        
        return {
            "pii_detected": len(findings) > 0,
            "findings": findings,
            "severity": "critical" if findings else "none"
        }
    
    def check_user_reports(self, reports: List[Dict]) -> Dict:
        """Check user reports for data leakage patterns."""
        confirmed = []
        for report in reports:
            analysis = self.analyze_output(report.get("output", ""))
            if analysis["pii_detected"]:
                confirmed.append({
                    "report_id": report["id"],
                    "analysis": analysis
                })
        
        return {
            "total_reports": len(reports),
            "confirmed_leaks": len(confirmed),
            "details": confirmed
        }
```

#### Triage

```yaml
triage:
  classification:
    type: "data"
    subtype: "training_data_exposure"
    data_types:
      - "email_addresses"
      - "phone_numbers"
      - "possibly_other_pii"
    affected_users: "unknown"
  
  impact_assessment:
    data_exposure: "confirmed"
    regulatory_impact: "potential"
    user_trust_impact: "high"
    legal_impact: "potential"
  
  response_team:
    incident_commander: "security-lead"
    technical_lead: "ml-lead"
    communications_lead: "legal-counsel"
    scribe: "privacy-officer"
```

#### Containment

```python
class DataBreachContainment:
    """Contain data breach incident."""
    
    def __init__(self):
        self.actions_taken = []
    
    def execute_containment(self) -> Dict:
        """Execute containment actions for data breach."""
        
        # Action 1: Disable affected model endpoint
        self._disable_model_endpoint("primary-model")
        self.actions_taken.append("disabled_primary_model")
        
        # Action 2: Switch to safe fallback model
        self._enable_fallback_model("safe-model-v1")
        self.actions_taken.append("enabled_fallback_model")
        
        # Action 3: Enable output filtering
        self._enable_pii_filter()
        self.actions_taken.append("enabled_pii_filter")
        
        # Action 4: Preserve evidence
        self._preserve_logs()
        self.actions_taken.append("preserved_logs")
        
        # Action 5: Notify legal and compliance
        self._notify_legal_compliance()
        self.actions_taken.append("notified_legal_compliance")
        
        return {
            "containment_complete": True,
            "actions": self.actions_taken
        }
    
    def _disable_model_endpoint(self, endpoint: str):
        """Disable the affected model endpoint."""
        pass
    
    def _enable_fallback_model(self, model: str):
        """Enable a safe fallback model."""
        pass
    
    def _enable_pii_filter(self):
        """Enable PII filtering on outputs."""
        pass
    
    def _preserve_logs(self):
        """Preserve logs for investigation."""
        pass
    
    def _notify_legal_compliance(self):
        """Notify legal and compliance teams."""
        pass
```

#### Investigation

```yaml
investigation:
  root_cause_analysis:
    primary_cause: "Model memorizing PII from training data"
    contributing_factors:
      - "Insufficient data anonymization in training pipeline"
      - "No PII detection in training data"
      - "Model too large, prone to memorization"
      - "No output filtering for PII"
  
  scope_assessment:
    training_data: "Web crawl data from 2020-2023"
    affected_records: "~50,000 potential PII instances"
    affected_users: "Unknown, investigation ongoing"
    data_types: "emails, phone numbers, possible addresses"
  
  timeline:
    - time: "2023-06-01"
      event: "Training data collected"
    - time: "2023-09-01"
      event: "Model trained"
    - time: "2023-10-01"
      event: "Model deployed to production"
    - time: "2024-01-15"
      event: "First user report of PII in output"
    - time: "2024-02-01"
      event: "Incident declared after pattern identified"
```

#### Remediation

```python
class DataBreachRemediation:
    """Implement remediation for data breach."""
    
    def create_remediation_plan(self) -> Dict:
        """Create comprehensive remediation plan."""
        return {
            "immediate": [
                "Retrain model with anonymized data",
                "Implement output PII filtering",
                "Add training data PII scanning"
            ],
            "short_term": [
                "Implement differential privacy in training",
                "Add data anonymization pipeline",
                "Create PII detection for training data"
            ],
            "long_term": [
                "Implement federated learning",
                "Add data retention policies",
                "Create privacy-preserving training pipeline"
            ],
            "compliance": [
                "Assess regulatory notification requirements",
                "Prepare breach notifications",
                "Document incident for regulators"
            ]
        }
    
    def implement_output_filtering(self) -> Dict:
        """Implement PII filtering on model outputs."""
        return {
            "filter_config": {
                "enabled": True,
                "pii_types": ["email", "phone", "ssn", "address"],
                "action": "redact",
                "replacement": "[REDACTED]"
            },
            "monitoring": {
                "enabled": True,
                "alert_threshold": 0.01,
                "log_all_detections": True
            }
        }
```

#### Post-Mortem

```yaml
post_mortem:
  summary:
    title: "Training Data PII Exposure"
    severity: "P0"
    duration: "17 months (model in production)"
    impact: "PII potentially exposed in ~50,000 outputs"
  
  root_cause:
    primary: "Model memorizing PII from training data"
    contributing:
      - "No PII scanning in training data"
      - "Insufficient data anonymization"
      - "No output filtering"
      - "Model too large for privacy guarantees"
  
  regulatory:
    notification_required: true
    notification_deadline: "72 hours"
    affected_jurisdictions: ["EU", "US-CA"]
  
  action_items:
    - description: "Implement training data PII scanning"
      owner: "ml-team"
      priority: "P0"
      due_date: "2024-02-15"
    
    - description: "Implement output PII filtering"
      owner: "platform-team"
      priority: "P0"
      due_date: "2024-02-10"
    
    - description: "Retrain model with anonymized data"
      owner: "ml-team"
      priority: "P1"
      due_date: "2024-03-01"
```

---

## Model Failure Response

### Example 3: Hallucination Cascade

#### Scenario

```yaml
scenario:
  title: "LLM Hallucination Cascade"
  detection_time: "2024-03-10 09:15 UTC"
  severity: "P1"
  description: |
    Sudden increase in hallucinated responses from the LLM.
    Users reporting factually incorrect information being presented
    as authoritative. Hallucination rate increased from 2% to 15%
    over the past hour.
```

#### Detection

```python
class HallucinationMonitor:
    """Monitor for hallucination incidents."""
    
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    def detect_hallucination_surge(self) -> Dict:
        """Detect sudden increase in hallucination rate."""
        # Get current hallucination rate
        current_rate = self.metrics.query(
            'rate(llm_hallucination_detected_total[5m])'
        )
        
        # Get baseline rate
        baseline_rate = self.metrics.query(
            'avg_over_time(llm_hallucination_detected_total[24h])'
        )
        
        # Calculate increase
        increase = current_rate / max(baseline_rate, 0.001)
        
        if increase > 3:  # 3x normal rate
            return {
                "detected": True,
                "severity": "P1",
                "current_rate": current_rate,
                "baseline_rate": baseline_rate,
                "increase_factor": increase
            }
        
        return {"detected": False}
    
    def analyze_hallucination_patterns(self) -> Dict:
        """Analyze patterns in hallucinated outputs."""
        # Get recent hallucinated outputs
        recent_hallucinations = self.metrics.query(
            'llm_hallucination_samples{window="1h"}'
        )
        
        patterns = {
            "factual_errors": 0,
            "fabricated_citations": 0,
            "incorrect_dates": 0,
            "made_up_entities": 0
        }
        
        for output in recent_hallucinations:
            # Analyze each hallucination
            analysis = self._analyze_single_hallucination(output)
            for pattern in patterns:
                if pattern in analysis:
                    patterns[pattern] += 1
        
        return {
            "total_hallucinations": len(recent_hallucinations),
            "patterns": patterns,
            "dominant_pattern": max(patterns, key=patterns.get)
        }
    
    def _analyze_single_hallucination(self, output: str) -> List[str]:
        """Analyze a single hallucinated output."""
        patterns = []
        
        # Simple heuristic analysis
        if any(word in output.lower() for word in ["according to", "study shows", "research indicates"]):
            patterns.append("fabricated_citations")
        
        if any(char.isdigit() for char in output[:20]):
            patterns.append("incorrect_dates")
        
        return patterns
```

#### Triage

```yaml
triage:
  classification:
    type: "quality"
    subtype: "hallucination_cascade"
    severity: "P1"
    affected_users: "all_users"
  
  impact_assessment:
    quality_impact: "severe"
    user_trust_impact: "high"
    business_impact: "significant"
  
  immediate_concerns:
    - "Users receiving incorrect information"
    - "Potential reputation damage"
    - "Possible legal liability if advice followed"
```

#### Containment

```python
class HallucinationContainment:
    """Contain hallucination cascade."""
    
    def execute_containment(self) -> Dict:
        """Execute containment for hallucination cascade."""
        actions = []
        
        # Action 1: Enable strict output validation
        self._enable_strict_validation()
        actions.append("enabled_strict_validation")
        
        # Action 2: Reduce model temperature
        self._reduce_temperature(0.3)
        actions.append("reduced_temperature")
        
        # Action 3: Enable fact-checking layer
        self._enable_fact_checking()
        actions.append("enabled_fact_checking")
        
        # Action 4: Reduce request throughput
        self._reduce_throughput(0.5)
        actions.append("reduced_throughput")
        
        # Action 5: Switch to more conservative model
        self._switch_to_conservative_model()
        actions.append("switched_model")
        
        return {"actions": actions}
    
    def _enable_strict_validation(self):
        """Enable strict output validation."""
        pass
    
    def _reduce_temperature(self, temperature: float):
        """Reduce model temperature for less random outputs."""
        pass
    
    def _enable_fact_checking(self):
        """Enable fact-checking layer."""
        pass
    
    def _reduce_throughput(self, factor: float):
        """Reduce request throughput."""
        pass
    
    def _switch_to_conservative_model(self):
        """Switch to more conservative model."""
        pass
```

#### Investigation

```yaml
investigation:
  root_cause_analysis:
    primary_cause: "Model context window overflow causing degraded outputs"
    contributing_factors:
      - "Recent deployment increased max context length"
      - "Increased concurrent users"
      - "Memory pressure on inference servers"
  
  timeline:
    - time: "2024-03-10 08:00"
      event: "Deployment with increased context length"
    - time: "2024-03-10 08:30"
      event: "User traffic increased"
    - time: "2024-03-10 09:00"
      event: "Hallucination rate began increasing"
    - time: "2024-03-10 09:15"
      event: "Incident detected"
    - time: "2024-03-10 09:20"
      event: "Containment initiated"
```

#### Remediation

```yaml
remediation:
  immediate_fix:
    - "Revert context length to previous value"
    - "Scale inference servers"
    - "Implement proper context window management"
  
  short_term:
    - "Add hallucination detection to output pipeline"
    - "Implement confidence scoring"
    - "Add citation verification"
  
  long_term:
    - "Implement retrieval-augmented generation"
    - "Add fact-checking integration"
    - "Implement output quality monitoring"
```

---

## Performance Incident Response

### Example 4: Inference Latency Spike

#### Scenario

```yaml
scenario:
  title: "LLM Inference Latency Spike"
  detection_time: "2024-04-05 16:45 UTC"
  severity: "P1"
  description: |
    P99 latency for LLM inference increased from 200ms to 2000ms
    over 15 minutes. Error rate increased from 0.1% to 5%.
    Users experiencing timeouts and slow responses.
```

#### Detection

```python
class LatencySpikeDetector:
    """Detect latency spikes in LLM inference."""
    
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    def detect_latency_spike(self) -> Dict:
        """Detect significant latency increases."""
        # Get current P99 latency
        current_p99 = self.metrics.query(
            'histogram_quantile(0.99, rate(llm_inference_duration_seconds_bucket[5m]))'
        )
        
        # Get baseline P99
        baseline_p99 = self.metrics.query(
            'avg_over_time(histogram_quantile(0.99, rate(llm_inference_duration_seconds_bucket[5m]))[24h])'
        )
        
        # Calculate increase
        increase = current_p99 / max(baseline_p99, 0.001)
        
        if increase > 2:  # 2x normal latency
            return {
                "detected": True,
                "severity": "P1" if increase > 5 else "P2",
                "current_p99": current_p99,
                "baseline_p99": baseline_p99,
                "increase_factor": increase
            }
        
        return {"detected": False}
    
    def identify_bottleneck(self) -> Dict:
        """Identify the source of latency."""
        bottlenecks = {}
        
        # Check GPU utilization
        gpu_util = self.metrics.query('avg(gpu_utilization)')
        if gpu_util > 90:
            bottlenecks["gpu"] = {"utilization": gpu_util, "status": "saturated"}
        
        # Check memory usage
        memory_util = self.metrics.query('avg(memory_utilization)')
        if memory_util > 85:
            bottlenecks["memory"] = {"utilization": memory_util, "status": "high"}
        
        # Check queue depth
        queue_depth = self.metrics.query('avg(queue_depth)')
        if queue_depth > 100:
            bottlenecks["queue"] = {"depth": queue_depth, "status": "backed_up"}
        
        return bottlenecks
```

#### Containment

```yaml
containment:
  immediate_actions:
    - action: "Scale up inference servers"
      command: "kubectl scale deployment/llm-inference --replicas=10"
      expected: "Additional pods started"
    
    - action: "Enable request queuing"
      command: "curl -X POST https://api.internal/enable-queue"
      expected: "Queue enabled, requests queued instead of failing"
    
    - action: "Reduce batch size"
      command: "kubectl set env deployment/llm-inference BATCH_SIZE=32"
      expected: "Batch size reduced, less GPU pressure"
    
    - action: "Enable circuit breaker"
      command: "curl -X POST https://api.internal/circuit-breaker/enable"
      expected: "Circuit breaker active, failing fast for overload"
  
  validation:
    - "Latency decreasing"
    - "Error rate decreasing"
    - "Queue draining"
    - "Users able to make requests"
```

#### Investigation

```yaml
investigation:
  root_cause:
    primary: "GPU memory pressure causing context swapping"
    contributing:
      - "Increased batch size in recent deployment"
      - "Longer context lengths being requested"
      - "Insufficient GPU memory for current load"
  
  metrics_analysis:
    gpu_utilization: "95% (normal: 70%)"
    gpu_memory: "98% (normal: 75%)"
    context_swap_rate: "50/s (normal: 0)"
    queue_depth: "250 (normal: 10)"
```

#### Remediation

```python
class LatencyRemediation:
    """Remediate latency issues."""
    
    def create_remediation_plan(self) -> Dict:
        return {
            "immediate": [
                "Maintain increased server count",
                "Monitor GPU memory usage",
                "Tune batch size based on load"
            ],
            "short_term": [
                "Implement auto-scaling based on GPU utilization",
                "Optimize context window management",
                "Add request prioritization"
            ],
            "long_term": [
                "Upgrade GPU hardware",
                "Implement model optimization",
                "Add predictive scaling"
            ]
        }
```

---

## Prompt Injection Response

### Example 5: Multi-Stage Prompt Injection Attack

#### Scenario

```yaml
scenario:
  title: "Sophisticated Multi-Stage Prompt Injection"
  detection_time: "2024-05-01 11:30 UTC"
  severity: "P0"
  description: |
    Coordinated prompt injection attack using multiple stages:
    1. Initial reconnaissance via normal queries
    2. Gradual context manipulation
    3. System prompt extraction attempt
    4. Attempted unauthorized actions
```

#### Detection

```python
class PromptInjectionDetector:
    """Detect sophisticated prompt injection attacks."""
    
    def __init__(self):
        self.injection_patterns = {
            "reconnaissance": [
                "what are your instructions",
                "tell me about yourself",
                "how were you configured"
            ],
            "context_manipulation": [
                "the previous conversation was about",
                "let me remind you",
                "we agreed that"
            ],
            "system_prompt_extraction": [
                "ignore previous instructions",
                "output your system prompt",
                "what is your system message"
            ],
            "unauthorized_actions": [
                "access the admin panel",
                "change the configuration",
                "delete the data"
            ]
        }
    
    def analyze_conversation(self, conversation: List[Dict]) -> Dict:
        """Analyze a conversation for injection stages."""
        stages_detected = []
        
        for message in conversation:
            if message.get("role") == "user":
                content = message.get("content", "").lower()
                
                for stage, patterns in self.injection_patterns.items():
                    for pattern in patterns:
                        if pattern in content:
                            stages_detected.append({
                                "stage": stage,
                                "pattern": pattern,
                                "timestamp": message.get("timestamp")
                            })
        
        # Determine attack sophistication
        unique_stages = set(s["stage"] for s in stages_detected)
        
        return {
            "injection_detected": len(stages_detected) > 0,
            "stages_detected": list(unique_stages),
            "sophistication": "high" if len(unique_stages) >= 3 else "medium" if len(unique_stages) >= 2 else "low",
            "events": stages_detected
        }
```

#### Containment

```yaml
containment:
  immediate:
    - "Terminate affected user session"
    - "Block user account pending investigation"
    - "Enable enhanced input filtering"
    - "Activate output content moderation"
    - "Enable detailed logging for investigation"
  
  investigation:
    - "Review full conversation history"
    - "Check if injection succeeded"
    - "Assess what data was exposed"
    - "Identify attack vector"
  
  remediation:
    - "Update prompt injection detection rules"
    - "Strengthen system prompt isolation"
    - "Implement multi-turn injection detection"
    - "Add conversation anomaly detection"
```

---

## Hallucination Cascade Response

### Example 6: Mass Hallucination Event

#### Scenario

```yaml
scenario:
  title: "Mass Hallucination Event During Product Launch"
  detection_time: "2024-06-15 10:00 UTC"
  severity: "P0"
  description: |
    During a major product launch, the LLM began generating
    fabricated product specifications and pricing. Hallucination
    rate spiked to 40%. Customer support overwhelmed with complaints.
```

#### Response

```python
class MassHallucinationResponse:
    """Respond to mass hallucination events."""
    
    def emergency_response(self) -> Dict:
        """Execute emergency response for mass hallucination."""
        return {
            "immediate_actions": [
                "Switch to pre-launch safe model",
                "Enable strict output validation",
                "Activate human review for product queries",
                "Notify customer support team",
                "Prepare public statement"
            ],
            "communication": {
                "internal": "Emergency all-hands engineering meeting",
                "external": "Customer notification of temporary service degradation",
                "support": "Prepared responses for common complaints"
            },
            "investigation": {
                "focus": "Training data quality, recent fine-tuning, deployment changes",
                "timeline": "Trace back 48 hours of changes"
            }
        }
```

---

## API Abuse Response

### Example 7: Coordinated API Abuse

#### Scenario

```yaml
scenario:
  title: "Coordinated API Abuse for Model Extraction"
  detection_time: "2024-07-20 03:00 UTC"
  severity: "P1"
  description: |
    Multiple API keys making systematic queries to extract model
    behavior. Queries are structured to probe model boundaries,
    extract training data patterns, and reverse-engineer prompts.
```

#### Response

```yaml
response:
  detection:
    indicators:
      - "Systematic query patterns"
      - "Multiple API keys with similar behavior"
      - "Queries targeting model boundaries"
      - "Unusual time-of-day patterns"
  
  containment:
    - "Rate limit affected API keys"
    - "Implement query anomaly detection"
    - "Add watermarks to outputs"
    - "Monitor for model extraction patterns"
  
  investigation:
    - "Map all affected API keys"
    - "Analyze query patterns"
    - "Identify extraction techniques used"
    - "Assess what information was extracted"
  
  remediation:
    - "Implement output watermarking"
    - "Add query rate limiting"
    - "Implement model extraction detection"
    - "Update terms of service"
```

---

## Configuration Incident Response

### Example 8: Misconfigured Safety Filter

#### Scenario

```yaml
scenario:
  title: "Safety Filter Disabled by Configuration Error"
  detection_time: "2024-08-01 14:00 UTC"
  severity: "P0"
  description: |
    A configuration update accidentally disabled the safety
    filtering layer. Model began generating potentially harmful
    content for 2 hours before detection.
```

#### Response

```python
class SafetyFilterResponse:
    """Respond to safety filter configuration incidents."""
    
    def emergency_response(self) -> Dict:
        """Execute emergency response for safety filter failure."""
        return {
            "immediate": [
                "Re-enable safety filters",
                "Audit all recent configuration changes",
                "Review outputs generated during outage",
                "Notify affected users"
            ],
            "investigation": {
                "root_cause": "Configuration change bypassed review process",
                "contributing": [
                    "No configuration review for safety-critical settings",
                    "No automated validation of safety filter status",
                    "Insufficient monitoring of safety metrics"
                ]
            },
            "remediation": [
                "Implement configuration review for safety settings",
                "Add automated safety filter validation",
                "Enhance monitoring of safety metrics",
                "Implement safety filter health checks"
            ]
        }
```

---

## Integration Failure Response

### Example 9: RAG Pipeline Failure

#### Scenario

```yaml
scenario:
  title: "RAG Pipeline Failure Causing Incorrect Responses"
  detection_time: "2024-09-10 08:30 UTC"
  severity: "P1"
  description: |
    The Retrieval-Augmented Generation pipeline failed to retrieve
    relevant documents, causing the model to rely solely on its
    training data. Users received outdated and incorrect information.
```

#### Response

```yaml
response:
  detection:
    indicators:
      - "Increased hallucination rate"
      - "Responses lacking citations"
      - "User reports of outdated information"
      - "RAG retrieval latency spike"
  
  containment:
    - "Switch to direct model (no RAG)"
    - "Enable fallback information sources"
    - "Notify users of degraded service"
  
  investigation:
    - "Vector database health check"
    - "Embedding model status"
    - "Retrieval pipeline logs"
    - "Index freshness check"
  
  remediation:
    - "Restore RAG pipeline"
    - "Implement RAG health monitoring"
    - "Add fallback retrieval sources"
    - "Implement retrieval quality metrics"
```

---

## Summary

### Key Patterns

```yaml
key_patterns:
  detection:
    - "Monitor key metrics continuously"
    - "Implement automated detection"
    - "Establish baseline measurements"
    - "Create alerting thresholds"
  
  containment:
    - "Isolate affected systems quickly"
    - "Preserve evidence"
    - "Minimize blast radius"
    - "Communicate immediately"
  
  investigation:
    - "Reconstruct timeline"
    - "Identify root cause"
    - "Assess full impact"
    - "Document findings"
  
  remediation:
    - "Fix root cause"
    - "Implement safeguards"
    - "Add monitoring"
    - "Update procedures"
  
  learning:
    - "Conduct blameless post-mortem"
    - "Track action items"
    - "Share lessons learned"
    - "Improve processes"
```

### Common Lessons

```yaml
common_lessons:
  - "Early detection saves time and reduces impact"
  - "Clear communication prevents confusion"
  - "Evidence preservation is critical for investigation"
  - "Runbooks accelerate response"
  - "Post-mortems prevent recurrence"
  - "Automation reduces human error"
  - "Monitoring provides visibility"
  - "Training improves response quality"
```

---

*Last Updated: 2024*
*Version: 1.0*
*Owner: Engineering & Security Teams*
