# Incident Response Best Practices for LLM & Agentic AI Systems

## Table of Contents

1. [Overview](#overview)
2. [Incident Classification](#incident-classification)
3. [Escalation Matrices](#escalation-matrices)
4. [Runbook Execution](#runbook-execution)
5. [Evidence Preservation](#evidence-preservation)
6. [Stakeholder Communication](#stakeholder-communication)
7. [Post-Mortem Process](#post-mortem-process)
8. [Continuous Improvement](#continuous-improvement)
9. [Tooling and Automation](#tooling-and-automation)
10. [Team Readiness](#team-readiness)
11. [Metrics and KPIs](#metrics-and-kpis)
12. [Integration with Development](#integration-with-development)

---

## Overview

This document outlines best practices for incident response in LLM and Agentic AI systems. These practices are derived from real-world incident management experience and adapted for the unique challenges posed by AI/ML systems.

### Core Best Practice Principles

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BEST PRACTICE PRINCIPLES                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 1. PREPARE BEFORE YOU NEED TO                               │    │
│  │    → Runbooks ready, teams trained, tools configured        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 2. DETECT EARLY, CONTAIN FAST                               │    │
│  │    → Automated detection, rapid containment                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 3. COMMUNICATE CLEARLY AND OFTEN                            │    │
│  │    → Stakeholders informed, no surprises                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 4. DOCUMENT EVERYTHING                                      │    │
│  │    → Timeline, decisions, evidence                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 5. LEARN AND IMPROVE                                        │    │
│  │    → Blameless post-mortems, action item tracking           │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Incident Classification

### Classification Framework

```python
class IncidentClassifier:
    """Automated incident classification for LLM systems."""

    CLASSIFICATION_DIMENSIONS = {
        "type": {
            "security": {
                "subtypes": ["prompt_injection", "data_breach", "unauthorized_access", "model_theft"],
                "base_severity": "P1"
            },
            "performance": {
                "subtypes": ["latency", "throughput", "availability", "resource_exhaustion"],
                "base_severity": "P2"
            },
            "quality": {
                "subtypes": ["hallucination", "bias", "incorrect_output", "formatting"],
                "base_severity": "P2"
            },
            "data": {
                "subtypes": ["pii_exposure", "training_data_leak", "data_poisoning", "data_drift"],
                "base_severity": "P1"
            }
        },
        "impact": {
            "critical": {"threshold": "all_users", "multiplier": 1.5},
            "high": {"threshold": "most_users", "multiplier": 1.2},
            "medium": {"threshold": "some_users", "multiplier": 1.0},
            "low": {"threshold": "few_users", "multiplier": 0.8}
        },
        "urgency": {
            "immediate": {"time_pressure": "active_exploitation", "multiplier": 1.5},
            "high": {"time_pressure": "degrading_service", "multiplier": 1.2},
            "normal": {"time_pressure": "stable", "multiplier": 1.0},
            "low": {"time_pressure": "no_immediate_impact", "multiplier": 0.8}
        }
    }

    def __init__(self):
        self.classification_cache = {}

    def classify_incident(self, incident_data: Dict) -> Dict:
        """Classify an incident based on multiple dimensions."""
        classification = {
            "type": self._classify_type(incident_data),
            "impact": self._classify_impact(incident_data),
            "urgency": self._classify_urgency(incident_data),
            "scope": self._classify_scope(incident_data),
            "risk": self._assess_risk(incident_data)
        }

        # Calculate final severity
        classification["severity"] = self._calculate_severity(classification)

        # Generate classification summary
        classification["summary"] = self._generate_summary(classification)

        return classification

    def _classify_type(self, data: Dict) -> Dict:
        """Classify incident type."""
        indicators = data.get("indicators", [])
        output_content = data.get("output_content", "")
        input_content = data.get("input_content", "")

        # Security indicators
        security_patterns = [
            "ignore previous instructions",
            "you are now",
            "system prompt",
            "override safety"
        ]

        if any(p in input_content.lower() for p in security_patterns):
            return {
                "category": "security",
                "subtype": "prompt_injection",
                "confidence": 0.9
            }

        # Performance indicators
        if data.get("latency_ms", 0) > 5000 or data.get("error_rate", 0) > 0.1:
            return {
                "category": "performance",
                "subtype": "latency" if data.get("latency_ms", 0) > 5000 else "error_rate",
                "confidence": 0.85
            }

        # Quality indicators
        if data.get("safety_score", 1.0) < 0.5 or data.get("hallucination_detected", False):
            return {
                "category": "quality",
                "subtype": "hallucination" if data.get("hallucination_detected") else "safety_violation",
                "confidence": 0.8
            }

        # Data indicators
        import re
        pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{16}\b'               # Credit card
        ]

        for pattern in pii_patterns:
            if re.search(pattern, output_content):
                return {
                    "category": "data",
                    "subtype": "pii_exposure",
                    "confidence": 0.95
                }

        return {
            "category": "unknown",
            "subtype": "unknown",
            "confidence": 0.3
        }

    def _classify_impact(self, data: Dict) -> Dict:
        """Classify incident impact."""
        affected_users = data.get("affected_users", 0)
        total_users = data.get("total_users", 1)
        impact_ratio = affected_users / total_users

        if impact_ratio > 0.8:
            return {"level": "critical", "ratio": impact_ratio}
        elif impact_ratio > 0.5:
            return {"level": "high", "ratio": impact_ratio}
        elif impact_ratio > 0.1:
            return {"level": "medium", "ratio": impact_ratio}
        else:
            return {"level": "low", "ratio": impact_ratio}

    def _classify_urgency(self, data: Dict) -> Dict:
        """Classify incident urgency."""
        if data.get("active_exploitation", False):
            return {"level": "immediate", "reason": "active_exploitation"}
        elif data.get("service_degrading", False):
            return {"level": "high", "reason": "service_degradation"}
        elif data.get("user_impact", False):
            return {"level": "normal", "reason": "user_impact"}
        else:
            return {"level": "low", "reason": "no_immediate_impact"}

    def _classify_scope(self, data: Dict) -> Dict:
        """Classify incident scope."""
        return {
            "system_affected": data.get("system", "unknown"),
            "region_affected": data.get("region", "global"),
            "data_types_affected": data.get("data_types", []),
            "compliance_impact": data.get("compliance_requirements", [])
        }

    def _assess_risk(self, data: Dict) -> Dict:
        """Assess overall risk level."""
        risk_factors = []

        if data.get("data_breach", False):
            risk_factors.append("data_breach")
        if data.get("regulatory_implication", False):
            risk_factors.append("regulatory")
        if data.get("reputational_risk", False):
            risk_factors.append("reputational")
        if data.get("financial_impact", 0) > 100000:
            risk_factors.append("significant_financial")

        risk_score = len(risk_factors) * 25

        return {
            "score": risk_score,
            "factors": risk_factors,
            "level": "critical" if risk_score >= 75 else "high" if risk_score >= 50 else "medium" if risk_score >= 25 else "low"
        }

    def _calculate_severity(self, classification: Dict) -> str:
        """Calculate final severity level."""
        type_severity = self.CLASSIFICATION_DIMENSIONS["type"].get(
            classification["type"]["category"], {}
        ).get("base_severity", "P3")

        impact_multiplier = self.CLASSIFICATION_DIMENSIONS["impact"].get(
            classification["impact"]["level"], {}
        ).get("multiplier", 1.0)

        urgency_multiplier = self.CLASSIFICATION_DIMENSIONS["urgency"].get(
            classification["urgency"]["level"], {}
        ).get("multiplier", 1.0)

        # Convert severity to numeric
        severity_map = {"P0": 4, "P1": 3, "P2": 2, "P3": 1}
        numeric_severity = severity_map.get(type_severity, 1)

        # Apply multipliers
        adjusted_severity = numeric_severity * impact_multiplier * urgency_multiplier

        # Convert back to severity level
        if adjusted_severity >= 4.5:
            return "P0"
        elif adjusted_severity >= 3.5:
            return "P1"
        elif adjusted_severity >= 2.5:
            return "P2"
        else:
            return "P3"

    def _generate_summary(self, classification: Dict) -> str:
        """Generate human-readable classification summary."""
        return (
            f"Incident Type: {classification['type']['category']} - {classification['type']['subtype']}\n"
            f"Impact Level: {classification['impact']['level']}\n"
            f"Urgency: {classification['urgency']['level']}\n"
            f"Scope: {classification['scope']['region_affected']}\n"
            f"Risk Level: {classification['risk']['level']}\n"
            f"Final Severity: {classification['severity']}"
        )
```

### Classification Decision Tree

```yaml
classification_decision_tree:
  step_1:
    question: "Is this a security incident?"
    yes_path:
      question: "Is there active data exfiltration?"
      yes_path:
        severity: "P0"
        type: "security/data_breach"
      no_path:
        question: "Is the system compromised?"
        yes_path:
          severity: "P1"
          type: "security/compromise"
        no_path:
          severity: "P2"
          type: "security/vulnerability"
    no_path:
      next_step: "step_2"

  step_2:
    question: "Is there a service outage or degradation?"
    yes_path:
      question: "Is the outage affecting >50% of users?"
      yes_path:
        severity: "P1"
        type: "performance/outage"
      no_path:
        severity: "P2"
        type: "performance/degradation"
    no_path:
      next_step: "step_3"

  step_3:
    question: "Is the model producing incorrect or harmful outputs?"
    yes_path:
      question: "Are outputs causing harm to users?"
      yes_path:
        severity: "P1"
        type: "quality/harmful_output"
      no_path:
        severity: "P2"
        type: "quality/incorrect_output"
    no_path:
      next_step: "step_4"

  step_4:
    question: "Is there data quality or drift issues?"
    yes_path:
      severity: "P2-P3"
      type: "data/quality"
    no_path:
      severity: "P3"
      type: "minor"
```

---

## Escalation Matrices

### Escalation Framework

```python
class EscalationManager:
    """Manage incident escalation based on rules and conditions."""

    def __init__(self, config: Dict):
        self.config = config
        self.escalation_paths = self._initialize_escalation_paths()
        self.escalation_history = []

    def _initialize_escalation_paths(self) -> Dict:
        return {
            "P0": {
                "immediate": {
                    "time": 0,
                    "recipients": ["on-call-engineer", "incident-commander"],
                    "channels": ["pager", "slack-direct", "phone"]
                },
                "level_1": {
                    "time": 15,  # minutes
                    "recipients": ["engineering-leadership", "security-lead"],
                    "channels": ["slack", "email"]
                },
                "level_2": {
                    "time": 30,
                    "recipients": ["vp-engineering", "ciso", "legal"],
                    "channels": ["slack", "email", "phone"]
                },
                "level_3": {
                    "time": 60,
                    "recipients": ["cto", "ceo"],
                    "channels": ["phone", "email"]
                }
            },
            "P1": {
                "immediate": {
                    "time": 0,
                    "recipients": ["on-call-engineer"],
                    "channels": ["pager", "slack"]
                },
                "level_1": {
                    "time": 30,
                    "recipients": ["incident-commander", "engineering-leadership"],
                    "channels": ["slack", "email"]
                },
                "level_2": {
                    "time": 120,
                    "recipients": ["vp-engineering"],
                    "channels": ["slack", "email"]
                }
            },
            "P2": {
                "immediate": {
                    "time": 0,
                    "recipients": ["on-call-engineer"],
                    "channels": ["slack"]
                },
                "level_1": {
                    "time": 240,  # 4 hours
                    "recipients": ["engineering-leadership"],
                    "channels": ["slack", "email"]
                }
            },
            "P3": {
                "immediate": {
                    "time": 0,
                    "recipients": ["assigned-engineer"],
                    "channels": ["slack"]
                }
            }
        }

    def determine_escalation(self, incident: Dict) -> Dict:
        """Determine escalation path for an incident."""
        severity = incident.get("severity", "P3")
        time_since_detection = self._calculate_time_since_detection(incident)

        escalation_path = self.escalation_paths.get(severity, {})
        current_level = self._determine_current_level(escalation_path, time_since_detection)

        return {
            "severity": severity,
            "current_level": current_level,
            "recipients": escalation_path.get(current_level, {}).get("recipients", []),
            "channels": escalation_path.get(current_level, {}).get("channels", []),
            "next_escalation": self._calculate_next_escalation(escalation_path, current_level)
        }

    def _determine_current_level(self, escalation_path: Dict, time_minutes: int) -> str:
        """Determine the current escalation level based on time."""
        current_level = "immediate"

        for level_name, level_config in escalation_path.items():
            if time_minutes >= level_config["time"]:
                current_level = level_name

        return current_level

    def _calculate_next_escalation(self, escalation_path: Dict, current_level: str) -> Dict:
        """Calculate when the next escalation should occur."""
        levels = list(escalation_path.keys())
        current_index = levels.index(current_level) if current_level in levels else -1

        if current_index < len(levels) - 1:
            next_level = levels[current_index + 1]
            return {
                "level": next_level,
                "time_minutes": escalation_path[next_level]["time"],
                "recipients": escalation_path[next_level]["recipients"]
            }

        return None

    def _calculate_time_since_detection(self, incident: Dict) -> float:
        """Calculate time since incident detection in minutes."""
        from datetime import datetime

        detection_time = incident.get("detection_time")
        if not detection_time:
            return 0

        if isinstance(detection_time, str):
            detection_time = datetime.fromisoformat(detection_time)

        elapsed = datetime.utcnow() - detection_time
        return elapsed.total_seconds() / 60

    def should_escalate(self, incident: Dict) -> bool:
        """Determine if incident should be escalated."""
        escalation = self.determine_escalation(incident)

        # Check if we've already escalated to this level
        last_escalation = self.escalation_history[-1] if self.escalation_history else None

        if last_escalation and last_escalation.get("level") == escalation["current_level"]:
            return False

        return True

    def record_escalation(self, incident_id: str, escalation: Dict):
        """Record an escalation event."""
        self.escalation_history.append({
            "incident_id": incident_id,
            "level": escalation["current_level"],
            "recipients": escalation["recipients"],
            "timestamp": self._get_timestamp()
        })

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Escalation Matrix by Severity

```yaml
escalation_matrix:
  P0:
    immediate:
      time: "0 minutes"
      contacts:
        - role: "On-Call Engineer"
          method: "PagerDuty + Phone"
          response_sla: "5 minutes"
        - role: "Incident Commander"
          method: "Slack DM + Phone"
          response_sla: "10 minutes"
    
    level_1:
      time: "15 minutes"
      contacts:
        - role: "Engineering Leadership"
          method: "Slack + Email"
          response_sla: "15 minutes"
        - role: "Security Lead"
          method: "Slack + Email"
          response_sla: "15 minutes"
    
    level_2:
      time: "30 minutes"
      contacts:
        - role: "VP Engineering"
          method: "Phone"
          response_sla: "30 minutes"
        - role: "CISO"
          method: "Phone"
          response_sla: "30 minutes"
        - role: "Legal"
          method: "Phone"
          response_sla: "30 minutes"
    
    level_3:
      time: "60 minutes"
      contacts:
        - role: "CTO"
          method: "Phone"
          response_sla: "30 minutes"
        - role: "CEO"
          method: "Phone"
          response_sla: "30 minutes"

  P1:
    immediate:
      time: "0 minutes"
      contacts:
        - role: "On-Call Engineer"
          method: "PagerDuty"
          response_sla: "10 minutes"
    
    level_1:
      time: "30 minutes"
      contacts:
        - role: "Incident Commander"
          method: "Slack"
          response_sla: "30 minutes"
        - role: "Engineering Leadership"
          method: "Slack + Email"
          response_sla: "30 minutes"
    
    level_2:
      time: "2 hours"
      contacts:
        - role: "VP Engineering"
          method: "Slack + Email"
          response_sla: "1 hour"

  P2:
    immediate:
      time: "0 minutes"
      contacts:
        - role: "On-Call Engineer"
          method: "Slack"
          response_sla: "30 minutes"
    
    level_1:
      time: "4 hours"
      contacts:
        - role: "Engineering Leadership"
          method: "Slack"
          response_sla: "4 hours"

  P3:
    immediate:
      time: "0 minutes"
      contacts:
        - role: "Assigned Engineer"
          method: "Slack"
          response_sla: "24 hours"
```

---

## Runbook Execution

### Runbook Structure

```yaml
runbook_template:
  metadata:
    name: "string"
    version: "string"
    last_updated: "date"
    owner: "team"
    severity: "P0-P3"
    incident_types: ["list"]
  
  pre_conditions:
    - "Required access level"
    - "Required tools"
    - "Required permissions"
  
  detection:
    signals:
      - "Signal 1: Description"
      - "Signal 2: Description"
    confirmation_steps:
      - "Step to confirm incident"
      - "Step to validate severity"
  
  containment:
    immediate_actions:
      - action: "Action description"
        command: "command to execute"
        expected_result: "What to expect"
        rollback: "How to undo"
    
    verification:
      - "How to verify containment worked"
  
  remediation:
    steps:
      - step: 1
        action: "Description"
        command: "command"
        validation: "How to verify"
      - step: 2
        action: "Description"
        command: "command"
        validation: "How to verify"
  
  recovery:
    steps:
      - "Step to restore service"
      - "Step to validate recovery"
    validation:
      - "How to confirm full recovery"
  
  post_mortem:
    required: true
    template: "link to template"
    deadline: "within 48 hours"
  
  communication:
    internal:
      - "Who to notify"
      - "When to notify"
    external:
      - "If external communication needed"
      - "Template to use"
```

### Runbook Execution Framework

```python
class RunbookExecutor:
    """Execute runbooks with validation and tracking."""

    def __init__(self, runbook: Dict, incident: Dict):
        self.runbook = runbook
        self.incident = incident
        self.execution_log = []
        self.current_step = 0
        self.status = "initialized"

    def execute(self) -> Dict:
        """Execute the runbook with validation."""
        self.status = "executing"

        # Validate pre-conditions
        if not self._validate_preconditions():
            self.status = "blocked"
            return self._create_result("blocked", "Pre-conditions not met")

        # Execute steps
        for i, step in enumerate(self.runbook.get("steps", [])):
            self.current_step = i

            # Log step start
            self._log_step("start", step)

            # Execute step
            result = self._execute_step(step)

            # Log step result
            self._log_step("result", step, result)

            # Validate step
            if not self._validate_step(step, result):
                self.status = "failed"
                return self._create_result("failed", f"Step {i} failed: {result}")

            # Check if we should continue
            if self._should_stop(step, result):
                self.status = "stopped"
                return self._create_result("stopped", "Stopped per runbook conditions")

        self.status = "completed"
        return self._create_result("completed", "Runbook executed successfully")

    def _validate_preconditions(self) -> bool:
        """Validate all pre-conditions are met."""
        preconditions = self.runbook.get("pre_conditions", [])

        for condition in preconditions:
            if not self._check_condition(condition):
                self.execution_log.append({
                    "step": "precondition",
                    "status": "failed",
                    "condition": condition,
                    "timestamp": self._get_timestamp()
                })
                return False

        return True

    def _execute_step(self, step: Dict) -> Dict:
        """Execute a single runbook step."""
        import subprocess
        import time

        result = {
            "step": step.get("name", "unknown"),
            "status": "pending",
            "output": "",
            "error": "",
            "duration_ms": 0
        }

        start_time = time.time()

        try:
            command = step.get("command", "")
            if command:
                # Execute the command
                proc = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=step.get("timeout", 300)
                )

                result["output"] = proc.stdout
                result["error"] = proc.stderr
                result["return_code"] = proc.returncode
                result["status"] = "success" if proc.returncode == 0 else "failed"

            else:
                # Manual step - mark as pending human action
                result["status"] = "pending_manual"
                result["output"] = "Manual step - requires human action"

        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Command timed out"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        result["duration_ms"] = int((time.time() - start_time) * 1000)
        return result

    def _validate_step(self, step: Dict, result: Dict) -> bool:
        """Validate step execution."""
        if result["status"] != "success":
            return False

        # Check expected result if defined
        expected = step.get("expected_result")
        if expected:
            # Simple string match (could be more sophisticated)
            if expected.lower() not in result.get("output", "").lower():
                return False

        return True

    def _should_stop(self, step: Dict, result: Dict) -> bool:
        """Determine if execution should stop."""
        # Stop on failure if configured
        if result["status"] == "failed" and step.get("stop_on_failure", True):
            return True

        # Stop if rollback is needed
        if result["status"] == "failed" and step.get("rollback"):
            self._execute_rollback(step["rollback"])
            return True

        return False

    def _execute_rollback(self, rollback_command: str):
        """Execute rollback command."""
        import subprocess

        try:
            subprocess.run(
                rollback_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
        except Exception as e:
            self.execution_log.append({
                "step": "rollback",
                "status": "failed",
                "error": str(e),
                "timestamp": self._get_timestamp()
            })

    def _log_step(self, event: str, step: Dict, result: Dict = None):
        """Log step execution."""
        log_entry = {
            "event": event,
            "step": step.get("name", "unknown"),
            "timestamp": self._get_timestamp()
        }

        if result:
            log_entry["result"] = result

        self.execution_log.append(log_entry)

    def _check_condition(self, condition: str) -> bool:
        """Check if a pre-condition is met."""
        # Simplified condition checking
        # In production, this would be more sophisticated
        return True

    def _create_result(self, status: str, message: str) -> Dict:
        """Create execution result."""
        return {
            "status": status,
            "message": message,
            "steps_completed": self.current_step + 1,
            "total_steps": len(self.runbook.get("steps", [])),
            "execution_log": self.execution_log
        }

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### LLM-Specific Runbook Examples

```yaml
runbook_prompt_injection:
  name: "Respond to Prompt Injection Attack"
  severity: "P0-P1"
  last_updated: "2024-01-15"
  
  detection:
    signals:
      - "System prompt leaked in output"
      - "Unauthorized actions performed"
      - "Safety filters bypassed"
      - "Suspicious input patterns detected"
  
  containment:
    immediate_actions:
      - action: "Enable enhanced input filtering"
        command: "kubectl set env deployment/llm-service ENHANCED_FILTERING=true"
        expected_result: "environment variable set"
      
      - action: "Rate limit affected endpoints"
        command: "curl -X POST https://api.internal/rate-limit -d '{\"endpoint\": \"/chat\", \"limit\": 10}'"
        expected_result: "rate limit applied"
      
      - action: "Block suspicious IPs"
        command: "iptables -A INPUT -s {SUSPICIOUS_IP} -j DROP"
        expected_result: "IP blocked"
      
      - action: "Enable output content moderation"
        command: "kubectl set env deployment/llm-service OUTPUT_MODERATION=strict"
        expected_result: "moderation enabled"
  
  investigation:
    steps:
      - action: "Review input logs for injection patterns"
        command: "grep -E '(ignore previous|you are now|system prompt)' /var/log/llm/inputs.log | tail -100"
      
      - action: "Check if injection succeeded"
        command: "grep -E '(unauthorized action|safety bypass)' /var/log/llm/outputs.log | tail -50"
      
      - action: "Identify affected users"
        command: "python scripts/identify_affected_users.py --time-range 1h"
  
  remediation:
    steps:
      - step: 1
        action: "Update prompt injection detection rules"
        command: "python scripts/update_injection_rules.py --rules injection_patterns.json"
        validation: "New rules present in config"
      
      - step: 2
        action: "Strengthen system prompt isolation"
        command: "kubectl apply -f k8s/system-prompt-isolation.yaml"
        validation: "Isolation config applied"
      
      - step: 3
        action: "Add output validation layer"
        command: "kubectl apply -f k8s/output-validator.yaml"
        validation: "Validator pod running"
  
  recovery:
    steps:
      - action: "Gradually restore normal traffic"
        command: "kubectl set env deployment/llm-service RATE_LIMIT=normal"
      
      - action: "Monitor for reoccurrence"
        command: "watch -n 5 'curl -s https://api.internal/metrics | jq .injection_attempts'"
  
  communication:
    internal:
      - "Notify security team immediately"
      - "Update engineering leadership within 30 minutes"
    external:
      - "If data exposed, notify affected users within 72 hours"
      - "If regulatory requirement, notify regulators per policy"
```

---

## Evidence Preservation

### Evidence Collection Framework

```python
class EvidenceCollector:
    """Collect and preserve evidence for incident investigation."""

    def __init__(self, incident: Dict):
        self.incident = incident
        self.evidence_items = []
        self.chain_of_custody = []

    def collect_all_evidence(self) -> Dict:
        """Collect all relevant evidence for the incident."""
        evidence = {
            "incident_id": self.incident["id"],
            "collection_time": self._get_timestamp(),
            "items": []
        }

        # Collect different types of evidence
        evidence["items"].extend(self._collect_logs())
        evidence["items"].extend(self._collect_metrics())
        evidence["items"].extend(self._collect_configs())
        evidence["items"].extend(self._collect_traces())
        evidence["items"].extend(self._collect_user_inputs())

        # Create evidence package
        evidence["package"] = self._create_evidence_package(evidence["items"])

        # Generate chain of custody
        evidence["chain_of_custody"] = self._generate_chain_of_custody()

        return evidence

    def _collect_logs(self) -> List[Dict]:
        """Collect relevant log files."""
        log_sources = [
            {
                "name": "llm_application_logs",
                "path": "/var/log/llm/application.log",
                "time_range": "last_24h",
                "collection_method": "file_copy"
            },
            {
                "name": "llm_input_logs",
                "path": "/var/log/llm/inputs.log",
                "time_range": "last_24h",
                "collection_method": "file_copy"
            },
            {
                "name": "llm_output_logs",
                "path": "/var/log/llm/outputs.log",
                "time_range": "last_24h",
                "collection_method": "file_copy"
            },
            {
                "name": "api_access_logs",
                "path": "/var/log/api/access.log",
                "time_range": "last_24h",
                "collection_method": "file_copy"
            },
            {
                "name": "system_logs",
                "path": "/var/log/syslog",
                "time_range": "last_24h",
                "collection_method": "file_copy"
            }
        ]

        collected = []
        for source in log_sources:
            try:
                evidence = self._collect_log_source(source)
                collected.append(evidence)
            except Exception as e:
                self.evidence_items.append({
                    "type": "collection_error",
                    "source": source["name"],
                    "error": str(e)
                })

        return collected

    def _collect_metrics(self) -> List[Dict]:
        """Collect metrics snapshots."""
        import json

        metric_sources = [
            {
                "name": "inference_metrics",
                "query": "rate(llm_inference_duration_seconds_sum[5m])",
                "time_range": "last_6h"
            },
            {
                "name": "error_metrics",
                "query": "rate(llm_errors_total[5m])",
                "time_range": "last_6h"
            },
            {
                "name": "safety_metrics",
                "query": "llm_safety_score_avg",
                "time_range": "last_6h"
            }
        ]

        collected = []
        for source in metric_sources:
            try:
                # Query Prometheus or similar metrics system
                metrics_data = self._query_metrics(source)
                collected.append({
                    "name": source["name"],
                    "data": metrics_data,
                    "collected_at": self._get_timestamp()
                })
            except Exception as e:
                self.evidence_items.append({
                    "type": "collection_error",
                    "source": source["name"],
                    "error": str(e)
                })

        return collected

    def _collect_configs(self) -> List[Dict]:
        """Collect configuration files."""
        config_files = [
            "/etc/llm/config.yaml",
            "/etc/llm/prompts/system.txt",
            "/etc/llm/safety_filters.yaml",
            "/etc/nginx/nginx.conf",
            "/etc/kubernetes/deployments/llm-service.yaml"
        ]

        collected = []
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    collected.append({
                        "name": config_file,
                        "content": content,
                        "hash": self._hash_content(content),
                        "collected_at": self._get_timestamp()
                    })
            except FileNotFoundError:
                pass
            except Exception as e:
                self.evidence_items.append({
                    "type": "collection_error",
                    "source": config_file,
                    "error": str(e)
                })

        return collected

    def _collect_traces(self) -> List[Dict]:
        """Collect distributed traces."""
        # Implementation depends on tracing system (Jaeger, Zipkin, etc.)
        return []

    def _collect_user_inputs(self) -> List[Dict]:
        """Collect relevant user inputs (privacy-compliant)."""
        # Implementation depends on data retention policies
        return []

    def _collect_log_source(self, source: Dict) -> Dict:
        """Collect a specific log source."""
        import subprocess
        import hashlib

        # Determine time range filter
        time_filter = self._get_time_filter(source["time_range"])

        # Collect logs with time filter
        cmd = f"awk '{time_filter}' {source['path']}" if time_filter else f"cat {source['path']}"

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        content = result.stdout
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        return {
            "name": source["name"],
            "path": source["path"],
            "content": content,
            "hash": content_hash,
            "collected_at": self._get_timestamp(),
            "line_count": content.count('\n')
        }

    def _query_metrics(self, source: Dict) -> Dict:
        """Query metrics from monitoring system."""
        # Implementation depends on metrics system
        return {}

    def _get_time_filter(self, time_range: str) -> str:
        """Generate time filter for log collection."""
        from datetime import datetime, timedelta

        if time_range == "last_1h":
            cutoff = datetime.utcnow() - timedelta(hours=1)
        elif time_range == "last_6h":
            cutoff = datetime.utcnow() - timedelta(hours=6)
        elif time_range == "last_24h":
            cutoff = datetime.utcnow() - timedelta(hours=24)
        else:
            return ""

        # Generate awk filter (simplified)
        return f"$0 ~ /{cutoff.strftime('%Y-%m-%d %H')}/"

    def _create_evidence_package(self, items: List[Dict]) -> Dict:
        """Create a packaged evidence archive."""
        import hashlib
        import json

        package_content = json.dumps(items, indent=2)
        package_hash = hashlib.sha256(package_content.encode()).hexdigest()

        return {
            "hash": package_hash,
            "item_count": len(items),
            "total_size_bytes": len(package_content),
            "created_at": self._get_timestamp()
        }

    def _generate_chain_of_custody(self) -> List[Dict]:
        """Generate chain of custody documentation."""
        return [
            {
                "action": "collected",
                "timestamp": self._get_timestamp(),
                "actor": "incident_response_system",
                "description": "Evidence collected automatically"
            }
        ]

    def _hash_content(self, content: str) -> str:
        """Generate hash for content integrity."""
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Evidence Preservation Checklist

```yaml
evidence_preservation:
  immediate_actions:
    - [ ] Preserve all application logs
    - [ ] Snapshot current metrics
    - [ ] Capture configuration state
    - [ ] Record system state
    - [ ] Document initial timeline

  data_to_preserve:
    logs:
      - [ ] Application logs (last 24h)
      - [ ] Access logs (last 24h)
      - [ ] Error logs (last 24h)
      - [ ] Audit logs (last 7 days)
      - [ ] System logs (last 24h)
    
    metrics:
      - [ ] Inference metrics (last 6h)
      - [ ] Error metrics (last 6h)
      - [ ] Safety metrics (last 6h)
      - [ ] Performance metrics (last 6h)
    
    configurations:
      - [ ] Application config
      - [ ] Model config
      - [ ] Safety filters
      - [ ] Rate limits
      - [ ] Network config
    
    user_data:
      - [ ] Affected user sessions (anonymized)
      - [ ] Input/output samples
      - [ ] Error reports

  integrity:
    - [ ] Generate checksums for all evidence
    - [ ] Store in immutable storage
    - [ ] Document chain of custody
    - [ ] Restrict access to evidence
    - [ ] Backup to separate location

  compliance:
    - [ ] PII handling per policy
    - [ ] Data retention requirements
    - [ ] Legal hold if applicable
    - [ ] Regulatory notification timing
```

---

## Stakeholder Communication

### Communication Matrix

```python
class StakeholderCommunicator:
    """Manage stakeholder communications during incidents."""

    def __init__(self, incident: Dict):
        self.incident = incident
        self.stakeholder_groups = self._initialize_stakeholder_groups()
        self.communication_log = []

    def _initialize_stakeholder_groups(self) -> Dict:
        return {
            "executive": {
                "members": ["cto", "ceo", "cfo"],
                "channels": ["email", "phone"],
                "frequency": "every_2h",
                "content_level": "summary",
                "language": "business_impact"
            },
            "engineering": {
                "members": ["vp_engineering", "directors", "team_leads"],
                "channels": ["slack", "email"],
                "frequency": "every_1h",
                "content_level": "detailed",
                "language": "technical"
            },
            "security": {
                "members": ["ciso", "security_team"],
                "channels": ["slack", "pager"],
                "frequency": "immediate",
                "content_level": "detailed",
                "language": "security_focused"
            },
            "legal": {
                "members": ["general_counsel", "legal_team"],
                "channels": ["email", "phone"],
                "frequency": "as_needed",
                "content_level": "risk_focused",
                "language": "legal_implications"
            },
            "customer_facing": {
                "members": ["support_leads", "account_managers"],
                "channels": ["slack", "email"],
                "frequency": "every_2h",
                "content_level": "customer_impact",
                "language": "customer_friendly"
            },
            "external": {
                "members": ["affected_customers", "regulators", "media"],
                "channels": ["email", "status_page"],
                "frequency": "per_policy",
                "content_level": "public_facing",
                "language": "professional"
            }
        }

    def send_initial_notification(self) -> Dict:
        """Send initial incident notification to all stakeholders."""
        notifications = []

        for group_name, group_config in self.stakeholder_groups.items():
            notification = self._create_notification(group_config, "initial")
            notifications.append({
                "group": group_name,
                "notification": notification,
                "sent_at": self._get_timestamp()
            })

            # Send notification
            self._send_notification(group_config, notification)

        return {
            "notifications_sent": len(notifications),
            "details": notifications
        }

    def send_update(self, update_type: str = "status_update") -> Dict:
        """Send update to stakeholders."""
        notifications = []

        for group_name, group_config in self.stakeholder_groups.items():
            if self._should_notify(group_name, update_type):
                notification = self._create_notification(group_config, update_type)
                notifications.append({
                    "group": group_name,
                    "notification": notification,
                    "sent_at": self._get_timestamp()
                })

                self._send_notification(group_config, notification)

        return {
            "notifications_sent": len(notifications),
            "details": notifications
        }

    def _create_notification(self, group_config: Dict, notification_type: str) -> Dict:
        """Create notification tailored to stakeholder group."""
        templates = {
            "executive": {
                "initial": {
                    "subject": f"Incident Declared: {self.incident['title']}",
                    "body": f"""
Executive Summary:
- Incident ID: {self.incident['id']}
- Severity: {self.incident['severity']}
- Business Impact: {self.incident.get('business_impact', 'Under assessment')}
- Current Status: Active investigation
- Next Update: {self._get_next_update_time()}

Actions Being Taken:
1. Incident response team activated
2. Investigation underway
3. Containment measures being implemented
""",
                    "tone": "professional"
                },
                "status_update": {
                    "subject": f"Incident Update: {self.incident['title']}",
                    "body": f"""
Status Update:
- Current Status: {self.incident.get('current_status', 'Ongoing')}
- Impact: {self.incident.get('current_impact', 'Under assessment')}
- Next Steps: {self.incident.get('next_steps', 'Continuing investigation')}
- ETA to Resolution: {self.incident.get('eta', 'Under assessment')}
""",
                    "tone": "professional"
                }
            },
            "engineering": {
                "initial": {
                    "subject": f"[P{self.incident['severity'][-1]}] Incident: {self.incident['title']}",
                    "body": f"""
Technical Summary:
- Incident ID: {self.incident['id']}
- Type: {self.incident.get('type', 'Unknown')}
- Affected Systems: {self.incident.get('affected_systems', 'Under investigation')}
- Initial Assessment: {self.incident.get('initial_assessment', 'Under investigation')}

Response Team:
- Incident Commander: {self.incident.get('commander', 'TBD')}
- Technical Lead: {self.incident.get('tech_lead', 'TBD')}

War Room: {self.incident.get('war_room_link', 'TBD')}
""",
                    "tone": "technical"
                },
                "status_update": {
                    "subject": f"[UPDATE] Incident: {self.incident['title']}",
                    "body": f"""
Technical Update:
- Root Cause: {self.incident.get('root_cause', 'Under investigation')}
- Containment Status: {self.incident.get('containment_status', 'In progress')}
- Actions Taken: {self.incident.get('actions_taken', [])}
- Next Steps: {self.incident.get('next_steps', [])}
""",
                    "tone": "technical"
                }
            }
        }

        group_tone = group_config.get("content_level", "general")
        template = templates.get(group_tone, templates["executive"]).get(
            notification_type,
            {"subject": f"Incident Update: {self.incident['title']}", "body": "Update in progress", "tone": "professional"}
        )

        return template

    def _should_notify(self, group_name: str, update_type: str) -> bool:
        """Determine if a group should be notified."""
        # Simplified logic
        if update_type == "initial":
            return True
        if update_type == "escalation":
            return group_name in ["executive", "security", "legal"]
        if update_type == "resolution":
            return True
        return True

    def _send_notification(self, group_config: Dict, notification: Dict):
        """Send notification via configured channels."""
        for channel in group_config["channels"]:
            if channel == "slack":
                self._send_slack(group_config, notification)
            elif channel == "email":
                self._send_email(group_config, notification)
            elif channel == "phone":
                self._send_phone(group_config, notification)

    def _send_slack(self, group_config: Dict, notification: Dict):
        """Send Slack notification."""
        # Implementation depends on Slack API
        pass

    def _send_email(self, group_config: Dict, notification: Dict):
        """Send email notification."""
        # Implementation depends on email service
        pass

    def _send_phone(self, group_config: Dict, notification: Dict):
        """Send phone notification."""
        # Implementation depends on phone service
        pass

    def _get_next_update_time(self) -> str:
        """Calculate next update time."""
        from datetime import datetime, timedelta
        severity = self.incident.get("severity", "P3")

        intervals = {"P0": "30 minutes", "P1": "1 hour", "P2": "4 hours", "P3": "24 hours"}
        interval = intervals.get(severity, "1 hour")

        return f"{interval} from now"

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Communication Templates

```yaml
communication_templates:
  initial_notification:
    executive: |
      Subject: [P{severity}] Incident: {title}
      
      Executive Summary:
      - Incident ID: {incident_id}
      - Severity: {severity}
      - Business Impact: {business_impact}
      - Current Status: Active investigation
      - Next Update: {next_update_time}
      
      Actions Being Taken:
      1. Incident response team activated
      2. Investigation underway
      3. Containment measures being implemented
      
      Risks:
      - {risk_1}
      - {risk_2}
      
      Questions? Contact: {commander_email}
    
    engineering: |
      Subject: [P{severity}] Incident: {title}
      
      Technical Summary:
      - Incident ID: {incident_id}
      - Type: {incident_type}
      - Affected Systems: {affected_systems}
      - Initial Assessment: {initial_assessment}
      
      Response Team:
      - Incident Commander: {commander}
      - Technical Lead: {tech_lead}
      
      War Room: {war_room_link}
      
      Timeline:
      - {timestamp}: Incident detected
      - {timestamp}: Triage started
      - {timestamp}: Containment initiated
      
      Next Steps:
      1. {next_step_1}
      2. {next_step_2}
  
  status_update: |
    Subject: [UPDATE] Incident: {title}
    
    Status Update:
    - Current Status: {current_status}
    - Root Cause: {root_cause}
    - Impact: {current_impact}
    - Actions Taken: {actions_taken}
    - Next Steps: {next_steps}
    - ETA to Resolution: {eta}
    
    Next Update: {next_update_time}
  
  resolution: |
    Subject: [RESOLVED] Incident: {title}
    
    Resolution Summary:
    - Incident ID: {incident_id}
    - Duration: {duration}
    - Resolution: {resolution_summary}
    - Root Cause: {root_cause}
    
    Impact Summary:
    - Users Affected: {users_affected}
    - Duration of Impact: {impact_duration}
    - Data Exposure: {data_exposure}
    
    Follow-up Actions:
    1. Post-mortem scheduled for {post_mortem_date}
    2. {follow_up_action_1}
    3. {follow_up_action_2}
    
    Post-mortem Link: {post_mortem_link}
```

---

## Post-Mortem Process

### Blameless Post-Mortem Framework

```python
class BlamelessPostMortem:
    """Facilitate blameless post-mortem processes."""

    def __init__(self, incident: Dict):
        self.incident = incident
        self.postmortem_data = {
            "incident_id": incident["id"],
            "created_at": self._get_timestamp(),
            "facilitator": None,
            "attendees": [],
            "timeline": [],
            "root_causes": [],
            "what_went_well": [],
            "what_could_improve": [],
            "action_items": [],
            "lessons_learned": []
        }

    def facilitate_postmortem(self) -> Dict:
        """Facilitate the post-mortem meeting."""
        # Pre-meeting preparation
        self._prepare_meeting()

        # During meeting
        self._facilitate_discussion()

        # Post-meeting
        self._finalize_postmortem()

        return self.postmortem_data

    def _prepare_meeting(self):
        """Prepare for post-mortem meeting."""
        # Gather all incident data
        self.postmortem_data["incident_summary"] = self._gather_incident_summary()
        self.postmortem_data["timeline"] = self._reconstruct_timeline()
        self.postmortem_data["metrics"] = self._gather_metrics()
        self.postmortem_data["evidence"] = self._gather_evidence()

    def _facilitate_discussion(self):
        """Facilitate the post-mortem discussion."""
        # This would be done in a meeting
        # Here we set up the framework for discussion

        discussion_framework = {
            "round_1": {
                "topic": "Incident Walkthrough",
                "duration": "20 minutes",
                "objective": "Everyone understands what happened",
                "questions": [
                    "What was the sequence of events?",
                    "When did things start going wrong?",
                    "What was the impact?"
                ]
            },
            "round_2": {
                "topic": "Root Cause Analysis",
                "duration": "20 minutes",
                "objective": "Identify root causes",
                "questions": [
                    "Why did this happen?",
                    "What factors contributed?",
                    "Why wasn't this prevented?"
                ]
            },
            "round_3": {
                "topic": "What Went Well",
                "duration": "10 minutes",
                "objective": "Identify positive aspects",
                "questions": [
                    "What worked well in the response?",
                    "What should we continue doing?"
                ]
            },
            "round_4": {
                "topic": "What Could Improve",
                "duration": "10 minutes",
                "objective": "Identify improvement opportunities",
                "questions": [
                    "What could we have done better?",
                    "What gaps did we discover?"
                ]
            }
        }

        self.postmortem_data["discussion_framework"] = discussion_framework

    def _finalize_postmortem(self):
        """Finalize post-mortem document."""
        # Generate action items
        self.postmortem_data["action_items"] = self._generate_action_items()

        # Generate recommendations
        self.postmortem_data["recommendations"] = self._generate_recommendations()

        # Calculate metrics
        self.postmortem_data["metrics"] = self._calculate_metrics()

    def _gather_incident_summary(self) -> Dict:
        """Gather incident summary information."""
        return {
            "title": self.incident.get("title"),
            "severity": self.incident.get("severity"),
            "duration": self.incident.get("duration"),
            "impact": self.incident.get("impact"),
            "detection_time": self.incident.get("detection_time"),
            "resolution_time": self.incident.get("resolution_time")
        }

    def _reconstruct_timeline(self) -> List[Dict]:
        """Reconstruct incident timeline."""
        # Would pull from incident logs and documentation
        return []

    def _gather_metrics(self) -> Dict:
        """Gather relevant metrics."""
        return {
            "time_to_detect": self.incident.get("time_to_detect"),
            "time_to_contain": self.incident.get("time_to_contain"),
            "time_to_resolve": self.incident.get("time_to_resolve"),
            "users_affected": self.incident.get("users_affected"),
            "revenue_impact": self.incident.get("revenue_impact")
        }

    def _gather_evidence(self) -> List[Dict]:
        """Gather evidence for post-mortem."""
        return []

    def _generate_action_items(self) -> List[Dict]:
        """Generate action items from post-mortem."""
        action_items = []

        # Convert improvement opportunities to action items
        for improvement in self.postmortem_data.get("what_could_improve", []):
            action_items.append({
                "description": improvement,
                "owner": "TBD",
                "priority": "P2",
                "due_date": self._calculate_due_date(14),  # 2 weeks
                "status": "open"
            })

        return action_items

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations from post-mortem."""
        recommendations = []

        # Based on common patterns
        if self.incident.get("time_to_detect", 0) > 30:
            recommendations.append("Improve monitoring and detection capabilities")

        if self.incident.get("time_to_contain", 0) > 60:
            recommendations.append("Develop better containment runbooks")

        if self.incident.get("users_affected", 0) > 1000:
            recommendations.append("Implement better blast radius controls")

        return recommendations

    def _calculate_metrics(self) -> Dict:
        """Calculate post-mortem metrics."""
        return {
            "mttd": self.incident.get("time_to_detect"),  # Mean Time to Detect
            "mttc": self.incident.get("time_to_contain"),  # Mean Time to Contain
            "mttr": self.incident.get("time_to_resolve"),  # Mean Time to Resolve
            "action_items_count": len(self.postmortem_data.get("action_items", []))
        }

    def _calculate_due_date(self, days: int) -> str:
        """Calculate due date for action items."""
        from datetime import datetime, timedelta
        return (datetime.utcnow() + timedelta(days=days)).isoformat()

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Post-Mortem Quality Checklist

```yaml
post_mortem_quality:
  completeness:
    - [ ] All timeline events documented
    - [ ] Root cause identified and explained
    - [ ] Impact quantified (users, revenue, SLA)
    - [ ] All stakeholders represented
    - [ ] Action items assigned with owners
    - [ ] Due dates set for all action items
  
  blamelessness:
    - [ ] Focus on systems, not individuals
    - [ ] Language avoids blame
    - [ ] Discusses what could be improved systemically
    - [ ] Celebrates what went well
    - [ ] Encourages honest discussion
  
  actionability:
    - [ ] Action items are specific
    - [ ] Action items have clear owners
    - [ ] Action items have realistic deadlines
    - [ ] Action items are prioritized
    - [ ] Follow-up process defined
  
  documentation:
    - [ ] Post-mortem document complete
    - [ ] Supporting evidence linked
    - [ ] Lessons learned captured
    - [ ] Shared with relevant teams
    - [ ] Filed for future reference
```

---

## Continuous Improvement

### Improvement Tracking Framework

```python
class ImprovementTracker:
    """Track and manage continuous improvements from incidents."""

    def __init__(self):
        self.improvements = []
        self.metrics_history = []

    def add_improvement(self, improvement: Dict):
        """Add a new improvement item."""
        improvement["id"] = self._generate_id()
        improvement["created_at"] = self._get_timestamp()
        improvement["status"] = "proposed"
        improvement["priority"] = self._calculate_priority(improvement)

        self.improvements.append(improvement)

    def track_progress(self, improvement_id: str, update: Dict):
        """Track progress on an improvement."""
        improvement = self._find_improvement(improvement_id)
        if improvement:
            improvement["status"] = update.get("status", improvement["status"])
            improvement["progress"] = update.get("progress", improvement.get("progress", 0))
            improvement["last_updated"] = self._get_timestamp()

            # Track metrics
            self._track_metrics(improvement)

    def generate_report(self) -> Dict:
        """Generate improvement report."""
        report = {
            "generated_at": self._get_timestamp(),
            "total_improvements": len(self.improvements),
            "by_status": self._count_by_status(),
            "by_priority": self._count_by_priority(),
            "overdue": self._get_overdue(),
            "recent_completions": self._get_recent_completions(),
            "metrics_trend": self._get_metrics_trend()
        }

        return report

    def _count_by_status(self) -> Dict:
        """Count improvements by status."""
        counts = {}
        for improvement in self.improvements:
            status = improvement.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts

    def _count_by_priority(self) -> Dict:
        """Count improvements by priority."""
        counts = {}
        for improvement in self.improvements:
            priority = improvement.get("priority", "unknown")
            counts[priority] = counts.get(priority, 0) + 1
        return counts

    def _get_overdue(self) -> List[Dict]:
        """Get overdue improvement items."""
        from datetime import datetime

        overdue = []
        for improvement in self.improvements:
            due_date = improvement.get("due_date")
            if due_date and improvement.get("status") != "completed":
                if isinstance(due_date, str):
                    due_date = datetime.fromisoformat(due_date)
                if due_date < datetime.utcnow():
                    overdue.append(improvement)

        return overdue

    def _get_recent_completions(self) -> List[Dict]:
        """Get recently completed improvements."""
        from datetime import datetime, timedelta

        cutoff = datetime.utcnow() - timedelta(days=30)
        completions = []

        for improvement in self.improvements:
            if improvement.get("status") == "completed":
                completed_at = improvement.get("completed_at")
                if completed_at:
                    if isinstance(completed_at, str):
                        completed_at = datetime.fromisoformat(completed_at)
                    if completed_at > cutoff:
                        completions.append(improvement)

        return completions

    def _get_metrics_trend(self) -> Dict:
        """Get metrics trend over time."""
        return {
            "mttd_trend": self._calculate_trend("mttd"),
            "mttc_trend": self._calculate_trend("mttc"),
            "mttr_trend": self._calculate_trend("mttr")
        }

    def _calculate_trend(self, metric: str) -> List[Dict]:
        """Calculate trend for a specific metric."""
        # Would query historical metrics
        return []

    def _track_metrics(self, improvement: Dict):
        """Track metrics related to an improvement."""
        self.metrics_history.append({
            "improvement_id": improvement["id"],
            "timestamp": self._get_timestamp(),
            "metrics": improvement.get("metrics", {})
        })

    def _calculate_priority(self, improvement: Dict) -> str:
        """Calculate priority for an improvement."""
        # Simple priority calculation
        severity = improvement.get("incident_severity", "P3")
        frequency = improvement.get("frequency", 1)

        priority_map = {"P0": 4, "P1": 3, "P2": 2, "P3": 1}
        base_priority = priority_map.get(severity, 1)

        if frequency > 5:
            base_priority += 1

        priority_names = {4: "critical", 3: "high", 2: "medium", 1: "low"}
        return priority_names.get(min(base_priority, 4), "low")

    def _find_improvement(self, improvement_id: str) -> Dict:
        """Find an improvement by ID."""
        for improvement in self.improvements:
            if improvement.get("id") == improvement_id:
                return improvement
        return None

    def _generate_id(self) -> str:
        """Generate unique ID."""
        import uuid
        return str(uuid.uuid4())[:8]

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Continuous Improvement Cycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS IMPROVEMENT CYCLE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                    ┌─────────────────┐                               │
│                    │     INCIDENT    │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │   POST-MORTEM   │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │     LEARN       │                               │
│                    │  (Root Cause,   │                               │
│                    │   Improvements) │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │     PLAN        │                               │
│                    │  (Action Items, │                               │
│                    │   Prevention)   │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │     DO          │                               │
│                    │  (Implement,    │                               │
│                    │   Test)         │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │     CHECK       │                               │
│                    │  (Validate,     │                               │
│                    │   Measure)      │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                    ┌────────▼────────┐                               │
│                    │     ACT         │                               │
│                    │  (Standardize,  │                               │
│                    │   Share)        │                               │
│                    └────────┬────────┘                               │
│                             │                                        │
│                             └───────────────▶ NEXT INCIDENT         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tooling and Automation

### Incident Response Tool Stack

```yaml
incident_response_tools:
  detection:
    monitoring:
      - name: "Prometheus"
        purpose: "Metrics collection and alerting"
        integration: "AlertManager for escalation"
      - name: "Grafana"
        purpose: "Visualization and dashboards"
        integration: "Custom LLM health dashboards"
      - name: "ELK Stack"
        purpose: "Log aggregation and search"
        integration: "Custom log parsers for LLM outputs"
    
    specialized:
      - name: "Custom Safety Monitor"
        purpose: "Monitor for safety violations"
        integration: "Real-time output analysis"
      - name: "Prompt Injection Detector"
        purpose: "Detect injection attempts"
        integration: "Input filtering layer"
  
  response:
    incident_management:
      - name: "PagerDuty"
        purpose: "On-call management and escalation"
        integration: "Slack, email, phone"
      - name: "Jira"
        purpose: "Incident tracking and action items"
        integration: "Custom incident templates"
      - name: "Slack"
        purpose: "Communication and war rooms"
        integration: "Bots for updates"
    
    automation:
      - name: "Runbook Automation"
        purpose: "Automated response actions"
        integration: "Custom scripts and playbooks"
      - name: "ChatOps"
        purpose: "Incident management via chat"
        integration: "Custom bots and commands"
  
  investigation:
    forensics:
      - name: "Evidence Collector"
        purpose: "Automated evidence gathering"
        integration: "S3 for storage"
      - name: "Log Analyzer"
        purpose: "Automated log analysis"
        integration: "ML for anomaly detection"
    
    analysis:
      - name: "Metrics Explorer"
        purpose: "Deep dive into metrics"
        integration: "Prometheus queries"
      - name: "Trace Analyzer"
        purpose: "Distributed trace analysis"
        integration: "Jaeger/Zipkin"
```

### Automation Scripts

```python
class IncidentAutomator:
    """Automate common incident response tasks."""

    def __init__(self, config: Dict):
        self.config = config
        self.automations = self._load_automations()

    def _load_automations(self) -> List[Dict]:
        return [
            {
                "name": "auto_contain_prompt_injection",
                "trigger": "prompt_injection_detected",
                "actions": [
                    {"type": "enable_filter", "filter": "injection_detection"},
                    {"type": "rate_limit", "limit": 10, "window": 60},
                    {"type": "notify", "channel": "security-team"}
                ]
            },
            {
                "name": "auto_contain_data_exfiltration",
                "trigger": "data_exfiltration_detected",
                "actions": [
                    {"type": "block_ip", "ip": "detected_ip"},
                    {"type": "enable_filter", "filter": "pii_detection"},
                    {"type": "notify", "channel": "security-team", "priority": "urgent"},
                    {"type": "create_ticket", "priority": "P0"}
                ]
            },
            {
                "name": "auto_contain_latency_spike",
                "trigger": "latency_spike_detected",
                "actions": [
                    {"type": "scale_up", "replicas": 2},
                    {"type": "enable_circuit_breaker", "threshold": 5},
                    {"type": "notify", "channel": "on-call"}
                ]
            }
        ]

    def execute_automation(self, trigger: str, context: Dict) -> Dict:
        """Execute automation for a given trigger."""
        results = []

        for automation in self.automations:
            if automation["trigger"] == trigger:
                result = self._run_automation(automation, context)
                results.append({
                    "automation": automation["name"],
                    "result": result
                })

        return {"executed": len(results), "results": results}

    def _run_automation(self, automation: Dict, context: Dict) -> Dict:
        """Run a specific automation."""
        action_results = []

        for action in automation["actions"]:
            result = self._execute_action(action, context)
            action_results.append({
                "action": action["type"],
                "result": result
            })

        return {"status": "completed", "actions": action_results}

    def _execute_action(self, action: Dict, context: Dict) -> Dict:
        """Execute a single automation action."""
        action_type = action["type"]

        if action_type == "enable_filter":
            return self._enable_filter(action["filter"])
        elif action_type == "rate_limit":
            return self._set_rate_limit(action["limit"], action["window"])
        elif action_type == "block_ip":
            return self._block_ip(context.get("ip", action.get("ip")))
        elif action_type == "notify":
            return self._send_notification(action["channel"], context)
        elif action_type == "scale_up":
            return self._scale_service(action["replicas"])
        elif action_type == "create_ticket":
            return self._create_ticket(action["priority"], context)
        elif action_type == "enable_circuit_breaker":
            return self._enable_circuit_breaker(action["threshold"])

        return {"status": "unknown_action"}

    def _enable_filter(self, filter_name: str) -> Dict:
        """Enable a content filter."""
        # Implementation depends on filter system
        return {"status": "success", "filter": filter_name}

    def _set_rate_limit(self, limit: int, window: int) -> Dict:
        """Set rate limit."""
        # Implementation depends on rate limiting system
        return {"status": "success", "limit": limit, "window": window}

    def _block_ip(self, ip: str) -> Dict:
        """Block an IP address."""
        # Implementation depends on firewall system
        return {"status": "success", "ip": ip}

    def _send_notification(self, channel: str, context: Dict) -> Dict:
        """Send notification."""
        # Implementation depends on notification system
        return {"status": "success", "channel": channel}

    def _scale_service(self, replicas: int) -> Dict:
        """Scale a service."""
        # Implementation depends on orchestration system
        return {"status": "success", "replicas": replicas}

    def _create_ticket(self, priority: str, context: Dict) -> Dict:
        """Create a ticket."""
        # Implementation depends on ticketing system
        return {"status": "success", "priority": priority}

    def _enable_circuit_breaker(self, threshold: int) -> Dict:
        """Enable circuit breaker."""
        # Implementation depends on circuit breaker system
        return {"status": "success", "threshold": threshold}
```

---

## Team Readiness

### Training Program

```yaml
training_program:
  onboarding:
    - topic: "Incident Response Basics"
      duration: "2 hours"
      format: "self-paced"
      assessment: "quiz"
    
    - topic: "LLM System Architecture"
      duration: "4 hours"
      format: "instructor-led"
      assessment: "quiz"
    
    - topic: "Security Fundamentals for AI"
      duration: "3 hours"
      format: "self-paced"
      assessment: "quiz"
  
  ongoing:
    - topic: "Incident Response Drills"
      frequency: "monthly"
      format: "tabletop exercise"
      participants: "all_engineers"
    
    - topic: "Security Awareness"
      frequency: "quarterly"
      format: "instructor-led"
      participants: "all_employees"
    
    - topic: "Runbook Review"
      frequency: "monthly"
      format: "team_review"
      participants: "on_call_engineers"
  
  specialized:
    - topic: "Incident Commander Training"
      duration: "8 hours"
      format: "workshop"
      participants: "senior_engineers"
      certification: true
    
    - topic: "Forensics for AI Systems"
      duration: "16 hours"
      format: "hands-on_lab"
      participants: "security_team"
      certification: true
```

### On-Call Readiness

```yaml
on_call_readiness:
  prerequisites:
    - "Completed incident response training"
    - "Familiar with runbooks"
    - "Access to all required tools"
    - "Contact information up to date"
  
  responsibilities:
    - "Monitor alerts"
    - "Initial triage"
    - "Escalation as needed"
    - "Runbook execution"
    - "Documentation"
  
  tools_access:
    - "PagerDuty"
    - "Slack"
    - "Grafana"
    - "Kubernetes console"
    - "AWS console"
    - "Log aggregation tools"
  
  support:
    - "Backup on-call engineer"
    - "Escalation contacts"
    - "Runbook links"
    - "War room procedures"
```

---

## Metrics and KPIs

### Incident Response Metrics

```python
class IncidentMetrics:
    """Track and analyze incident response metrics."""

    def __init__(self):
        self.metrics = []

    def record_incident(self, incident: Dict):
        """Record incident metrics."""
        metrics = {
            "incident_id": incident["id"],
            "timestamp": self._get_timestamp(),
            "severity": incident.get("severity"),
            "time_to_detect": incident.get("time_to_detect"),
            "time_to_contain": incident.get("time_to_contain"),
            "time_to_resolve": incident.get("time_to_resolve"),
            "users_affected": incident.get("users_affected", 0),
            "revenue_impact": incident.get("revenue_impact", 0),
            "type": incident.get("type"),
            "root_cause": incident.get("root_cause")
        }

        self.metrics.append(metrics)

    def calculate_kpis(self, time_range: Dict = None) -> Dict:
        """Calculate KPIs for the given time range."""
        filtered = self._filter_by_time_range(time_range)

        if not filtered:
            return self._empty_kpis()

        kpis = {
            "total_incidents": len(filtered),
            "by_severity": self._count_by_severity(filtered),
            "mttd": self._calculate_average(filtered, "time_to_detect"),
            "mttc": self._calculate_average(filtered, "time_to_contain"),
            "mttr": self._calculate_average(filtered, "time_to_resolve"),
            "total_users_affected": sum(i.get("users_affected", 0) for i in filtered),
            "total_revenue_impact": sum(i.get("revenue_impact", 0) for i in filtered),
            "incidents_per_week": self._calculate_rate(filtered, "week"),
            "trend": self._calculate_trend(filtered)
        }

        return kpis

    def _count_by_severity(self, incidents: List[Dict]) -> Dict:
        """Count incidents by severity."""
        counts = {}
        for incident in incidents:
            severity = incident.get("severity", "unknown")
            counts[severity] = counts.get(severity, 0) + 1
        return counts

    def _calculate_average(self, incidents: List[Dict], field: str) -> float:
        """Calculate average for a field."""
        values = [i.get(field, 0) for i in incidents if i.get(field) is not None]
        return sum(values) / len(values) if values else 0

    def _calculate_rate(self, incidents: List[Dict], period: str) -> float:
        """Calculate incidents per time period."""
        if not incidents:
            return 0

        timestamps = [i.get("timestamp") for i in incidents if i.get("timestamp")]
        if not timestamps:
            return 0

        from datetime import datetime
        dates = [datetime.fromisoformat(t) if isinstance(t, str) else t for t in timestamps]

        if period == "week":
            weeks = (max(dates) - min(dates)).days / 7
            return len(incidents) / max(weeks, 1)

        return 0

    def _calculate_trend(self, incidents: List[Dict]) -> Dict:
        """Calculate incident trend."""
        # Simplified trend calculation
        return {
            "direction": "stable",  # up, down, stable
            "change_percent": 0
        }

    def _filter_by_time_range(self, time_range: Dict = None) -> List[Dict]:
        """Filter incidents by time range."""
        if not time_range:
            return self.metrics

        from datetime import datetime, timedelta

        start = time_range.get("start")
        end = time_range.get("end", self._get_timestamp())

        filtered = []
        for m in self.metrics:
            ts = m.get("timestamp")
            if ts:
                if isinstance(ts, str):
                    ts = datetime.fromisoformat(ts)
                if isinstance(start, str):
                    start = datetime.fromisoformat(start)
                if isinstance(end, str):
                    end = datetime.fromisoformat(end)

                if start <= ts <= end:
                    filtered.append(m)

        return filtered

    def _empty_kpis(self) -> Dict:
        """Return empty KPIs."""
        return {
            "total_incidents": 0,
            "by_severity": {},
            "mttd": 0,
            "mttc": 0,
            "mttr": 0,
            "total_users_affected": 0,
            "total_revenue_impact": 0,
            "incidents_per_week": 0,
            "trend": {"direction": "stable", "change_percent": 0}
        }

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### KPI Dashboard

```yaml
kpi_dashboard:
  real_time:
    - name: "Active Incidents"
      type: "counter"
      query: "count(active_incidents)"
      alerts:
        - threshold: 3
          severity: "warning"
        - threshold: 5
          severity: "critical"
    
    - name: "MTTD (Mean Time to Detect)"
      type: "gauge"
      query: "avg(time_to_detect)"
      unit: "minutes"
      thresholds:
        good: 5
        warning: 15
        critical: 30
    
    - name: "MTTR (Mean Time to Resolve)"
      type: "gauge"
      query: "avg(time_to_resolve)"
      unit: "hours"
      thresholds:
        good: 2
        warning: 8
        critical: 24
  
  historical:
    - name: "Incidents by Severity"
      type: "bar_chart"
      query: "group by severity"
      period: "last_30_days"
    
    - name: "Incidents by Type"
      type: "pie_chart"
      query: "group by type"
      period: "last_30_days"
    
    - name: "MTTD Trend"
      type: "line_chart"
      query: "avg(time_to_detect) over time"
      period: "last_90_days"
    
    - name: "MTTR Trend"
      type: "line_chart"
      query: "avg(time_to_resolve) over time"
      period: "last_90_days"
```

---

## Integration with Development

### Incident-Driven Development

```yaml
incident_integration:
  in_development:
    - "Review recent incidents before feature work"
    - "Consider incident patterns in design"
    - "Add monitoring for new features"
    - "Create runbooks for new systems"
  
  in_testing:
    - "Include incident scenarios in testing"
    - "Test containment procedures"
    - "Validate rollback capabilities"
    - "Test communication workflows"
  
  in_deployment:
    - "Check incident action items status"
    - "Verify monitoring is in place"
    - "Confirm runbooks are updated"
    - "Validate escalation paths
  
  in_operations:
    - "Monitor for recurring patterns"
    - "Track action item completion"
    - "Review incident trends"
    - "Update runbooks as needed"
```

### Feedback Loop

```python
class IncidentFeedbackLoop:
    """Create feedback loops between incidents and development."""

    def __init__(self):
        self.feedback_items = []

    def capture_feedback(self, incident: Dict, postmortem: Dict):
        """Capture feedback from incident for development."""
        feedback = {
            "incident_id": incident["id"],
            "feedback_type": self._determine_feedback_type(incident),
            "suggestions": self._generate_suggestions(incident, postmortem),
            "prevention_measures": postmortem.get("action_items", []),
            "monitoring_gaps": self._identify_monitoring_gaps(incident),
            "runbook_gaps": self._identify_runbook_gaps(incident)
        }

        self.feedback_items.append(feedback)
        return feedback

    def _determine_feedback_type(self, incident: Dict) -> str:
        """Determine the type of feedback."""
        severity = incident.get("severity", "P3")
        root_cause = incident.get("root_cause", "")

        if severity in ["P0", "P1"]:
            return "critical"
        elif "monitoring" in root_cause.lower():
            return "monitoring"
        elif "runbook" in root_cause.lower():
            return "process"
        else:
            return "general"

    def _generate_suggestions(self, incident: Dict, postmortem: Dict) -> List[str]:
        """Generate suggestions for development."""
        suggestions = []

        # Based on incident type
        incident_type = incident.get("type", "")
        if "security" in incident_type:
            suggestions.append("Implement additional security controls")
            suggestions.append("Add security testing to CI/CD")
        elif "performance" in incident_type:
            suggestions.append("Add performance testing")
            suggestions.append("Implement auto-scaling")
        elif "quality" in incident_type:
            suggestions.append("Enhance quality monitoring")
            suggestions.append("Add automated quality checks")

        return suggestions

    def _identify_monitoring_gaps(self, incident: Dict) -> List[str]:
        """Identify gaps in monitoring."""
        gaps = []

        # Check if incident was detected by monitoring
        if not incident.get("detected_by_monitoring", True):
            gaps.append("Incident not detected by automated monitoring")

        # Check if metrics were available
        if not incident.get("metrics_available", True):
            gaps.append("Insufficient metrics for investigation")

        return gaps

    def _identify_runbook_gaps(self, incident: Dict) -> List[str]:
        """Identify gaps in runbooks."""
        gaps = []

        if not incident.get("runbook_available", False):
            gaps.append("No runbook for this incident type")
        elif not incident.get("runbook_effective", True):
            gaps.append("Runbook was not effective")

        return gaps

    def generate_development_items(self) -> List[Dict]:
        """Generate development items from feedback."""
        items = []

        for feedback in self.feedback_items:
            for suggestion in feedback.get("suggestions", []):
                items.append({
                    "source": feedback["incident_id"],
                    "type": "improvement",
                    "description": suggestion,
                    "priority": "medium",
                    "status": "proposed"
                })

        return items
```

---

## References

### Internal References

- [Incident Response Runbooks](./runbooks/)
- [Communication Templates](./templates/)
- [Escalation Matrix](./escalation/)
- [Post-Mortem Templates](./post-mortem/)
- [Metrics Dashboard](./metrics/)

### External References

- Google SRE Book - Incident Management
- PagerDuty Incident Response
- Atlassian Incident Management
- MITRE ATT&CK Framework

---

*Last Updated: 2024*
*Version: 1.0*
*Owner: Engineering & Security Teams*
