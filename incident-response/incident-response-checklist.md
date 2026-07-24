# Incident Response Checklists for LLM & Agentic AI Systems

## Table of Contents

1. [Overview](#overview)
2. [P0 Critical Incident Checklist](#p0-checklist)
3. [P1 High Incident Checklist](#p1-checklist)
4. [P2 Medium Incident Checklist](#p2-checklist)
5. [P3 Low Incident Checklist](#p3-checklist)
6. [Phase-Based Checklists](#phase-checklists)
7. [Incident Type Checklists](#incident-type-checklists)
8. [Role-Based Checklists](#role-checklists)
9. [Tool-Assisted Checklists](#tool-checklists)
10. [Post-Incident Checklists](#post-incident-checklists)

---

## Overview

This document provides comprehensive checklists for every phase of incident response in LLM and Agentic AI systems. Checklists are organized by severity level (P0-P3), response phase, incident type, and role.

### Using These Checklists

```yaml
usage_guidelines:
  severity_based:
    - "Use the P0-P3 checklists for severity-specific guidance"
    - "Combine with phase checklists for detailed steps"
  
  phase_based:
    - "Use phase checklists for detailed procedural steps"
    - "Reference role checklists for accountability"
  
  incident_type:
    - "Use incident type checklists for specialized guidance"
    - "Combine with severity checklists for prioritization"
  
  customization:
    - "Adapt checklists to your environment"
    - "Add organization-specific items"
    - "Remove inapplicable items"
```

---

## P0 Critical Incident Checklist

### Initial Response (First 15 Minutes)

```yaml
p0_initial_response:
  detection_verification:
    - [ ] "Incident confirmed (not false positive)"
    - [ ] "Severity verified as P0"
    - [ ] "Impact scope assessed"
    - [ ] "Data exposure evaluated"
  
  immediate_actions:
    - [ ] "Activate incident response team"
    - [ ] "Open war room (Slack channel / bridge)"
    - [ ] "Page incident commander"
    - [ ] "Page technical lead"
    - [ ] "Begin incident timeline"
  
  notification:
    - [ ] "Notify on-call engineer"
    - [ ] "Notify security team"
    - [ ] "Notify engineering leadership"
    - [ ] "Update status page (if user-facing)"
  
  evidence_preservation:
    - [ ] "Preserve application logs"
    - [ ] "Snapshot current metrics"
    - [ ] "Capture system state"
    - [ ] "Document initial observations"
```

### Triage (First 30 Minutes)

```yaml
p0_triage:
  classification:
    - [ ] "Incident type determined"
    - [ ] "Attack vector identified (if security)"
    - [ ] "Affected systems identified"
    - [ ] "Data types affected identified"
  
  impact_assessment:
    - [ ] "Number of affected users estimated"
    - [ ] "Revenue impact assessed"
    - [ ] "SLA impact evaluated"
    - [ ] "Regulatory implications considered"
  
  response_team:
    - [ ] "Incident commander confirmed"
    - [ ] "Technical lead confirmed"
    - [ ] "Communications lead assigned"
    - [ ] "Scribe assigned"
    - [ ] "All roles documented"
  
  response_plan:
    - [ ] "Containment strategy selected"
    - [ ] "Remediation approach outlined"
    - [ ] "Recovery plan drafted"
    - [ ] "Communication timeline established"
```

### Containment (First Hour)

```yaml
p0_containment:
  immediate_containment:
    - [ ] "Malicious traffic blocked"
    - [ ] "Compromised credentials revoked"
    - [ ] "Vulnerable endpoint disabled"
    - [ ] "Affected service isolated"
    - [ ] "Circuit breaker activated (if applicable)"
  
  access_control:
    - [ ] "Unnecessary access revoked"
    - [ ] "API keys rotated"
    - [ ] "Service accounts reviewed"
    - [ ] "Network segmentation verified"
  
  monitoring:
    - [ ] "Enhanced monitoring enabled"
    - [ ] "Alert thresholds adjusted"
    - [ ] "Additional logging enabled"
    - [ ] "Traffic capture enabled"
  
  validation:
    - [ ] "Containment measures verified"
    - [ ] "No unintended side effects"
    - [ ] "Legitimate traffic unaffected"
    - [ ] "Attack cannot continue"
```

### Communication (Ongoing)

```yaml
p0_communication:
  internal:
    - [ ] "Initial stakeholder notification sent"
    - [ ] "Regular updates scheduled (every 30 min)"
    - [ ] "Technical details shared with team"
    - [ ] "Leadership briefed"
  
  external:
    - [ ] "Status page updated"
    - [ ] "Customer support briefed"
    - [ ] "Affected users notified (if required)"
    - [ ] "Legal team engaged (if data breach)"
    - [ ] "Regulatory notification planned (if required)"
  
  documentation:
    - [ ] "All communications logged"
    - [ ] "Decisions documented"
    - [ ] "Timeline maintained"
    - [ ] "Evidence catalogued"
```

### Remediation (Hours 1-4)

```yaml
p0_remediation:
  root_cause:
    - [ ] "Root cause identified"
    - [ ] "Attack vector confirmed"
    - [ ] "Vulnerability documented"
    - [ ] "Impact fully assessed"
  
  immediate_fix:
    - [ ] "Fix implemented"
    - [ ] "Fix tested in staging"
    - [ ] "Fix deployed to production"
    - [ ] "Fix validated"
  
  verification:
    - [ ] "Service restored"
    - [ ] "Metrics normalized"
    - [ ] "No regression"
    - [ ] "Security scan clean"
```

### Recovery (Hours 2-8)

```yaml
p0_recovery:
  service_restoration:
    - [ ] "Full service restored"
    - [ ] "All features operational"
    - [ ] "Performance baseline met"
    - [ ] "Error rates normal"
  
  validation:
    - [ ] "User experience verified"
    - [ ] "Security controls validated"
    - [ ] "Monitoring confirmed working"
    - [ ] "No residual issues"
  
  cleanup:
    - [ ] "Temporary changes reverted"
    - [ ] "Access controls restored"
    - [ ] "Monitoring normalized"
    - [ ] "Status page updated to resolved"
```

### Post-Incident (24-48 Hours)

```yaml
p0_post_incident:
  post_mortem:
    - [ ] "Post-mortem scheduled"
    - [ ] "All participants identified"
    - [ ] "Evidence gathered"
    - [ ] "Timeline reconstructed"
    - [ ] "Post-mortem conducted"
    - [ ] "Document completed"
  
  action_items:
    - [ ] "Action items identified"
    - [ ] "Owners assigned"
    - [ ] "Deadlines set"
    - [ ] "Tracking system updated"
  
  follow_up:
    - [ ] "Regulatory notifications sent (if required)"
    - [ ] "User communications completed"
    - [ ] "Lessons learned shared"
    - [ ] "Process improvements identified"
```

---

## P1 High Incident Checklist

### Initial Response (First 30 Minutes)

```yaml
p1_initial_response:
  detection_verification:
    - [ ] "Incident confirmed (not false positive)"
    - [ ] "Severity verified as P1"
    - [ ] "Impact scope assessed"
  
  immediate_actions:
    - [ ] "Activate incident response team"
    - [ ] "Open war room"
    - [ ] "Page on-call engineer"
    - [ ] "Begin incident timeline"
  
  notification:
    - [ ] "Notify on-call engineer"
    - [ ] "Notify engineering lead"
    - [ ] "Update status page (if user-facing)"
  
  evidence_preservation:
    - [ ] "Preserve application logs"
    - [ ] "Snapshot current metrics"
    - [ ] "Document initial observations"
```

### Triage (First Hour)

```yaml
p1_triage:
  classification:
    - [ ] "Incident type determined"
    - [ ] "Affected systems identified"
    - [ ] "Root cause initial assessment"
  
  impact_assessment:
    - [ ] "Number of affected users estimated"
    - [ ] "Service degradation assessed"
    - [ ] "SLA impact evaluated"
  
  response_team:
    - [ ] "Incident commander assigned"
    - [ ] "Technical lead assigned"
    - [ ] "All roles documented"
  
  response_plan:
    - [ ] "Containment strategy selected"
    - [ ] "Remediation approach outlined"
    - [ ] "Communication timeline established"
```

### Containment (First 2 Hours)

```yaml
p1_containment:
  immediate_containment:
    - [ ] "Issue isolated"
    - [ ] "Affected service identified"
    - [ ] "Traffic rerouted (if applicable)"
    - [ ] "Circuit breaker activated (if applicable)"
  
  monitoring:
    - [ ] "Enhanced monitoring enabled"
    - [ ] "Alert thresholds adjusted"
    - [ ] "Additional logging enabled"
  
  validation:
    - [ ] "Containment measures verified"
    - [ ] "No unintended side effects"
    - [ ] "Service stability confirmed"
```

### Communication (Ongoing)

```yaml
p1_communication:
  internal:
    - [ ] "Initial stakeholder notification sent"
    - [ ] "Regular updates scheduled (every hour)"
    - [ ] "Technical details shared with team"
  
  external:
    - [ ] "Status page updated"
    - [ ] "Customer support briefed"
    - [ ] "Affected users notified (if required)"
  
  documentation:
    - [ ] "All communications logged"
    - [ ] "Decisions documented"
    - [ ] "Timeline maintained"
```

### Remediation (Hours 2-8)

```yaml
p1_remediation:
  root_cause:
    - [ ] "Root cause identified"
    - [ ] "Vulnerability documented"
  
  fix:
    - [ ] "Fix implemented"
    - [ ] "Fix tested"
    - [ ] "Fix deployed"
    - [ ] "Fix validated"
  
  verification:
    - [ ] "Service restored"
    - [ ] "Metrics normalized"
    - [ ] "No regression"
```

### Recovery (Hours 4-24)

```yaml
p1_recovery:
  service_restoration:
    - [ ] "Full service restored"
    - [ ] "Performance baseline met"
    - [ ] "Error rates normal"
  
  validation:
    - [ ] "User experience verified"
    - [ ] "Monitoring confirmed working"
  
  cleanup:
    - [ ] "Temporary changes reverted"
    - [ ] "Status page updated to resolved"
```

### Post-Incident (48-72 Hours)

```yaml
p1_post_incident:
  post_mortem:
    - [ ] "Post-mortem scheduled"
    - [ ] "Post-mortem conducted"
    - [ ] "Document completed"
  
  action_items:
    - [ ] "Action items identified"
    - [ ] "Owners assigned"
    - [ ] "Deadlines set"
  
  follow_up:
    - [ ] "Lessons learned shared"
    - [ ] "Process improvements identified"
```

---

## P2 Medium Incident Checklist

### Initial Response (First 2 Hours)

```yaml
p2_initial_response:
  detection_verification:
    - [ ] "Incident confirmed"
    - [ ] "Severity verified as P2"
  
  immediate_actions:
    - [ ] "On-call engineer notified"
    - [ ] "Incident ticket created"
    - [ ] "Initial investigation started"
  
  evidence_preservation:
    - [ ] "Relevant logs collected"
    - [ ] "Metrics noted"
```

### Triage (First 4 Hours)

```yaml
p2_triage:
  classification:
    - [ ] "Incident type determined"
    - [ ] "Affected systems identified"
  
  impact_assessment:
    - [ ] "User impact assessed"
    - [ ] "Service impact assessed"
  
  response_plan:
    - [ ] "Investigation approach defined"
    - [ ] "Fix timeline estimated"
```

### Investigation (Hours 4-24)

```yaml
p2_investigation:
  root_cause:
    - [ ] "Root cause identified"
    - [ ] "Contributing factors noted"
  
  fix_planning:
    - [ ] "Fix approach defined"
    - [ ] "Fix prioritized"
    - [ ] "Fix scheduled"
```

### Remediation (Hours 24-48)

```yaml
p2_remediation:
  fix:
    - [ ] "Fix implemented"
    - [ ] "Fix tested"
    - [ ] "Fix deployed"
  
  verification:
    - [ ] "Issue resolved"
    - [ ] "No regression"
```

### Post-Incident (1 Week)

```yaml
p2_post_incident:
  documentation:
    - [ ] "Incident documented"
    - [ ] "Lessons learned captured"
  
  improvements:
    - [ ] "Improvement items identified"
    - [ ] "Improvements scheduled"
```

---

## P3 Low Incident Checklist

### Initial Response (First 24 Hours)

```yaml
p3_initial_response:
  detection:
    - [ ] "Issue identified"
    - [ ] "Ticket created"
  
  assignment:
    - [ ] "Assigned to engineer"
    - [ ] "Priority set"
  
  investigation:
    - [ ] "Initial investigation done"
    - [ ] "Impact assessed"
```

### Resolution (1 Week)

```yaml
p3_resolution:
  fix:
    - [ ] "Fix implemented"
    - [ ] "Fix tested"
    - [ ] "Fix deployed"
  
  verification:
    - [ ] "Issue resolved"
    - [ ] "No regression"
```

### Documentation (2 Weeks)

```yaml
p3_documentation:
  documentation:
    - [ ] "Issue documented"
    - [ ] "Resolution noted"
  
  improvements:
    - [ ] "Improvement item logged"
    - [ ] "Improvement scheduled"
```

---

## Phase-Based Checklists

### Detection Phase Checklist

```yaml
detection_checklist:
  automated_detection:
    - [ ] "Monitoring systems operational"
    - [ ] "Alerts configured correctly"
    - [ ] "Alert thresholds appropriate"
    - [ ] "Alert routing working"
    - [ ] "On-call rotation current"
  
  manual_detection:
    - [ ] "User reports reviewed"
    - [ ] "Support tickets analyzed"
    - [ ] "Social media monitored"
    - [ ] "External reports checked"
  
  detection_validation:
    - [ ] "Incident confirmed (not false positive)"
    - [ ] "Severity assessed"
    - [ ] "Scope determined"
    - [ ] "Impact evaluated"
```

### Triage Phase Checklist

```yaml
triage_checklist:
  classification:
    - [ ] "Incident type identified"
    - [ ] "Subtype determined"
    - [ ] "Attack vector identified (if applicable)"
    - [ ] "Affected systems documented"
  
  impact_assessment:
    - [ ] "User impact quantified"
    - [ ] "Service impact assessed"
    - [ ] "Data exposure evaluated"
    - [ ] "Revenue impact estimated"
    - [ ] "SLA impact measured"
  
  response_team:
    - [ ] "Incident commander assigned"
    - [ ] "Technical lead assigned"
    - [ ] "Communications lead assigned"
    - [ ] "Scribe assigned"
    - [ ] "All roles documented"
  
  response_plan:
    - [ ] "Containment strategy selected"
    - [ ] "Remediation approach outlined"
    - [ ] "Recovery plan drafted"
    - [ ] "Communication plan established"
  
  documentation:
    - [ ] "Incident ticket created"
    - [ ] "Timeline started"
    - [ ] "Initial actions documented"
    - [ ] "Decision log started"
```

### Containment Phase Checklist

```yaml
containment_checklist:
  immediate_actions:
    - [ ] "Threat isolated"
    - [ ] "Affected systems contained"
    - [ ] "Traffic managed"
    - [ ] "Access controlled"
  
  access_control:
    - [ ] "Malicious access blocked"
    - [ ] "Credentials rotated"
    - [ ] "API keys invalidated"
    - [ ] "Network segmentation verified"
  
  monitoring:
    - [ ] "Enhanced monitoring enabled"
    - [ ] "Additional logging activated"
    - [ ] "Alert thresholds adjusted"
    - [ ] "Traffic capture enabled"
  
  validation:
    - [ ] "Containment effective"
    - [ ] "No unintended impact"
    - [ ] "Service stability confirmed"
    - [ ] "Attack cannot continue"
  
  evidence:
    - [ ] "Evidence preserved"
    - [ ] "Chain of custody started"
    - [ ] "Forensic data captured"
    - [ ] "System state recorded"
```

### Eradication Phase Checklist

```yaml
eradication_checklist:
  root_cause:
    - [ ] "Root cause identified"
    - [ ] "Vulnerability documented"
    - [ ] "Attack vector confirmed"
    - [ ] "Impact scope finalized"
  
  removal:
    - [ ] "Malicious artifacts removed"
    - [ ] "Backdoors eliminated"
    - [ ] "Persistent access removed"
    - [ ] "Compromised code fixed"
  
  validation:
    - [ ] "System clean"
    - [ ] "No residual compromise"
    - [ ] "Security scan passed"
    - [ ] "Integrity verified"
```

### Recovery Phase Checklist

```yaml
recovery_checklist:
  service_restoration:
    - [ ] "Service restored"
    - [ ] "All features operational"
    - [ ] "Performance baseline met"
    - [ ] "Error rates normal"
    - [ ] "User experience verified"
  
  validation:
    - [ ] "Security controls validated"
    - [ ] "Monitoring confirmed working"
    - [ ] "Alerts tested"
    - [ ] "No regression"
  
  cleanup:
    - [ ] "Temporary changes reverted"
    - [ ] "Access controls restored"
    - [ ] "Monitoring normalized"
    - [ ] "Status page updated"
    - [ ] "Support team briefed"
  
  verification:
    - [ ] "Full functionality confirmed"
    - [ ] "User acceptance verified"
    - [ ] "No lingering issues"
    - [ ] "Incident resolved"
```

### Post-Mortem Phase Checklist

```yaml
post_mortem_checklist:
  preparation:
    - [ ] "Post-mortem scheduled"
    - [ ] "Participants identified"
    - [ ] "Evidence gathered"
    - [ ] "Timeline reconstructed"
    - [ ] "Document drafted"
  
  conduct_meeting:
    - [ ] "Blameless environment established"
    - [ ] "Incident walkthrough completed"
    - [ ] "Root cause analysis conducted"
    - [ ] "What went well discussed"
    - [ ] "What could improve discussed"
    - [ ] "Action items identified"
  
  documentation:
    - [ ] "Post-mortem document completed"
    - [ ] "Timeline documented"
    - [ ] "Root cause documented"
    - [ ] "Impact documented"
    - [ ] "Action items documented"
    - [ ] "Lessons learned captured"
  
  follow_up:
    - [ ] "Action items assigned"
    - [ ] "Deadlines set"
    - [ ] "Tracking system updated"
    - [ ] "Follow-up meetings scheduled"
    - [ ] "Lessons shared with team"
```

---

## Incident Type Checklists

### Prompt Injection Checklist

```yaml
prompt_injection_checklist:
  detection:
    - [ ] "System prompt leaked in output"
    - [ ] "Unauthorized actions performed"
    - [ ] "Safety filters bypassed"
    - [ ] "Suspicious input patterns detected"
    - [ ] "Output contradicts system instructions"
  
  containment:
    - [ ] "Enhanced input filtering enabled"
    - [ ] "Output content moderation activated"
    - [ ] "Affected endpoints rate-limited"
    - [ ] "Suspicious IPs blocked"
    - [ ] "User session terminated (if compromised)"
  
  investigation:
    - [ ] "Attack vector identified"
    - [ ] "Injection pattern documented"
    - [ ] "Successful injections identified"
    - [ ] "Data exposure assessed"
    - [ ] "Actions performed catalogued"
  
  remediation:
    - [ ] "Input validation updated"
    - [ ] "System prompt strengthened"
    - [ ] "Output filtering enhanced"
    - [ ] "Detection rules updated"
    - [ ] "User notification sent (if data exposed)"
  
  prevention:
    - [ ] "Prompt injection testing added"
    - [ ] "Red team exercises scheduled"
    - [ ] "Security training updated"
    - [ ] "Monitoring enhanced"
```

### Data Breach Checklist

```yaml
data_breach_checklist:
  detection:
    - [ ] "Breach confirmed"
    - [ ] "Data types identified"
    - [ ] "Records affected quantified"
    - [ ] "Attack vector identified"
  
  containment:
    - [ ] "Affected systems isolated"
    - [ ] "Compromised credentials revoked"
    - [ ] "Access controls updated"
    - [ ] "Enhanced logging enabled"
    - [ ] "Forensic evidence preserved"
  
  notification:
    - [ ] "Legal team engaged"
    - [ ] "Compliance team notified"
    - [ ] "Regulatory notifications planned"
    - [ ] "User notifications planned"
    - [ ] "Law enforcement notified (if applicable)"
  
  investigation:
    - [ ] "Full scope determined"
    - [ ] "Data types documented"
    - [ ] "Records enumerated"
    - [ ] "Attack timeline reconstructed"
    - [ ] "Vulnerability identified"
  
  remediation:
    - [ ] "Vulnerability patched"
    - [ ] "Access controls updated"
    - [ ] "Monitoring enhanced"
    - [ ] "User passwords reset (if applicable)"
    - [ ] "API keys rotated"
  
  compliance:
    - [ ] "Regulatory notifications sent"
    - [ ] "User notifications sent"
    - [ ] "Documentation completed"
    - [ ] "Audit trail preserved"
    - [ ] "Incident report filed"
```

### Model Failure Checklist

```yaml
model_failure_checklist:
  detection:
    - [ ] "Model failure identified"
    - [ ] "Failure type determined"
    - [ ] "Impact scope assessed"
    - [ ] "Users affected identified"
  
  containment:
    - [ ] "Traffic rerouted to fallback"
    - [ ] "Circuit breaker activated"
    - [ ] "Rate limiting enabled"
    - [ ] "Error responses configured"
  
  investigation:
    - [ ] "Failure root cause identified"
    - [ ] "Model version documented"
    - [ ] "Input patterns analyzed"
    - [ ] "Output patterns analyzed"
    - [ ] "Infrastructure issues ruled out"
  
  remediation:
    - [ ] "Model issue identified"
    - [ ] "Fix approach determined"
    - [ ] "Fix implemented"
    - [ ] "Fix validated"
    - [ ] "Model redeployed"
  
  validation:
    - [ ] "Model performance verified"
    - [ ] "Output quality confirmed"
    - [ ] "No regression"
    - [ ] "Monitoring confirms stability"
```

### Performance Incident Checklist

```yaml
performance_incident_checklist:
  detection:
    - [ ] "Performance degradation detected"
    - [ ] "Metrics reviewed"
    - [ ] "Baseline comparison done"
    - [ ] "Impact scope assessed"
  
  containment:
    - [ ] "Traffic managed"
    - [ ] "Resources scaled"
    - [ ] "Circuit breakers activated"
    - [ ] "Non-essential features disabled"
  
  investigation:
    - [ ] "Bottleneck identified"
    - [ ] "Resource constraints checked"
    - [ ] "Code changes reviewed"
    - [ ] "Infrastructure issues ruled out"
    - [ ] "Traffic patterns analyzed"
  
  remediation:
    - [ ] "Bottleneck addressed"
    - [ ] "Resources optimized"
    - [ ] "Code fixed (if applicable)"
    - [ ] "Configuration updated"
    - [ ] "Scaling adjusted"
  
  validation:
    - [ ] "Performance restored"
    - [ ] "Metrics normalized"
    - [ ] "User experience verified"
    - [ ] "Monitoring confirms stability"
```

---

## Role-Based Checklists

### Incident Commander Checklist

```yaml
incident_commander_checklist:
  initial_response:
    - [ ] "Incident declared"
    - [ ] "Response team assembled"
    - [ ] "War room opened"
    - [ ] "Communication channels established"
    - [ ] "Timeline started"
  
  triage:
    - [ ] "Severity confirmed"
    - [ ] "Impact assessed"
    - [ ] "Response plan developed"
    - [ ] "Roles assigned"
    - [ ] "Next update scheduled"
  
  coordination:
    - [ ] "Technical lead briefed"
    - [ ] "Communications lead briefed"
    - [ ] "Stakeholders notified"
    - [ ] "Resources allocated"
    - [ ] "Blockers removed"
  
  decision_making:
    - [ ] "Containment strategy approved"
    - [ ] "Escalation decisions made"
    - [ ] "Communication approved"
    - [ ] "Trade-offs documented"
  
  resolution:
    - [ ] "Resolution verified"
    - [ ] "Service restored"
    - [ ] "Stakeholders updated"
    - [ ] "Post-mortem scheduled"
    - [ ] "Action items assigned"
```

### Technical Lead Checklist

```yaml
technical_lead_checklist:
  investigation:
    - [ ] "Root cause investigated"
    - [ ] "Evidence collected"
    - [ ] "Hypotheses tested"
    - [ ] "Root cause confirmed"
  
  containment:
    - [ ] "Containment implemented"
    - [ ] "Containment validated"
    - [ ] "No unintended impact"
  
  remediation:
    - [ ] "Fix implemented"
    - [ ] "Fix tested"
    - [ ] "Fix deployed"
    - [ ] "Fix validated"
  
  recovery:
    - [ ] "Service restored"
    - [ ] "Performance verified"
    - [ ] "Monitoring confirmed"
  
  documentation:
    - [ ] "Technical details documented"
    - [ ] "Root cause documented"
    - [ ] "Fix documented"
    - [ ] "Lessons learned captured"
```

### Communications Lead Checklist

```yaml
communications_lead_checklist:
  initial_communication:
    - [ ] "Initial notification sent"
    - [ ] "Status page updated"
    - [ ] "Support team briefed"
    - [ ] "Leadership notified"
  
  ongoing_communication:
    - [ ] "Updates sent on schedule"
    - [ ] "Stakeholders informed"
    - [ ] "Status page maintained"
    - [ ] "Questions answered"
  
  external_communication:
    - [ ] "User notifications prepared"
    - [ ] "Regulatory notifications planned"
    - [ ] "Media statements prepared"
    - [ ] "Legal review completed"
  
  resolution_communication:
    - [ ] "Resolution announced"
    - [ ] "Post-mortem scheduled"
    - [ ] "Follow-up communicated"
    - [ ] "Lessons shared"
```

### Scribe Checklist

```yaml
scribe_checklist:
  documentation:
    - [ ] "Timeline documented"
    - [ ] "Decisions recorded"
    - [ ] "Actions logged"
    - [ ] "Evidence catalogued"
  
  coordination:
    - [ ] "Questions captured"
    - [ ] "Action items tracked"
    - [ ] "Follow-ups scheduled"
  
  post_mortem:
    - [ ] "Timeline reconstructed"
    - [ ] "Evidence organized"
    - [ ] "Draft document prepared"
    - [ ] "Notes distributed"
```

---

## Tool-Assisted Checklists

### Automated Checklist Execution

```python
class AutomatedChecklist:
    """Automate checklist execution and tracking."""
    
    def __init__(self, checklist_type: str, incident: Dict):
        self.checklist_type = checklist_type
        self.incident = incident
        self.items = self._load_checklist()
        self.completed_items = []
        self.pending_items = []
    
    def _load_checklist(self) -> List[Dict]:
        """Load checklist items."""
        # Load from configuration
        return [
            {
                "id": "item_1",
                "description": "Incident confirmed",
                "automated": True,
                "command": "verify_incident",
                "status": "pending"
            },
            {
                "id": "item_2",
                "description": "Severity assigned",
                "automated": False,
                "status": "pending"
            }
        ]
    
    def execute_automated_items(self) -> List[Dict]:
        """Execute automated checklist items."""
        results = []
        
        for item in self.items:
            if item.get("automated") and item["status"] == "pending":
                result = self._execute_item(item)
                results.append({
                    "item_id": item["id"],
                    "result": result
                })
        
        return results
    
    def _execute_item(self, item: Dict) -> Dict:
        """Execute a single checklist item."""
        command = item.get("command")
        
        if command:
            # Execute automated check
            return {"status": "completed", "output": "Automated check passed"}
        
        return {"status": "manual_required"}
    
    def update_status(self, item_id: str, status: str):
        """Update item status."""
        for item in self.items:
            if item["id"] == item_id:
                item["status"] = status
                if status == "completed":
                    self.completed_items.append(item)
                break
    
    def get_progress(self) -> Dict:
        """Get checklist progress."""
        total = len(self.items)
        completed = len([i for i in self.items if i["status"] == "completed"])
        
        return {
            "total": total,
            "completed": completed,
            "percentage": (completed / total * 100) if total > 0 else 0,
            "pending": [i for i in self.items if i["status"] == "pending"]
        }
    
    def generate_report(self) -> Dict:
        """Generate checklist completion report."""
        progress = self.get_progress()
        
        return {
            "checklist_type": self.checklist_type,
            "incident_id": self.incident.get("id"),
            "progress": progress,
            "completed_items": self.completed_items,
            "pending_items": progress["pending"],
            "recommendations": self._generate_recommendations(progress)
        }
    
    def _generate_recommendations(self, progress: Dict) -> List[str]:
        """Generate recommendations based on progress."""
        recommendations = []
        
        if progress["percentage"] < 50:
            recommendations.append("Focus on completing critical items first")
        
        if len(progress["pending"]) > 10:
            recommendations.append("Consider parallelizing checklist execution")
        
        return recommendations
```

### Dashboard Integration

```yaml
checklist_dashboard:
  metrics:
    - name: "Checklist Completion Rate"
      type: "gauge"
      query: "completed_items / total_items * 100"
      thresholds:
        good: 80
        warning: 50
        critical: 20
    
    - name: "Average Time to Complete"
      type: "timer"
      query: "avg(completion_time)"
      unit: "minutes"
    
    - name: "Checklist Items by Status"
      type: "pie_chart"
      query: "group by status"
    
    - name: "Incomplete Critical Items"
      type: "counter"
      query: "count(status='pending' AND priority='critical')"
  
  alerts:
    - name: "Critical Items Incomplete"
      condition: "incomplete_critical > 0"
      severity: "warning"
      notify: ["incident-commander"]
    
    - name: "Checklist Stalled"
      condition: "last_update > 30 minutes"
      severity: "warning"
      notify: ["incident-commander", "technical-lead"]
```

---

## Post-Incident Checklists

### Post-Mortem Preparation Checklist

```yaml
post_mortem_preparation:
  before_meeting:
    - [ ] "Incident summary prepared"
    - [ ] "Timeline reconstructed"
    - [ ] "Evidence gathered"
    - [ ] "Metrics collected"
    - [ ] "Participant list finalized"
    - [ ] "Meeting room/link reserved"
    - [ ] "Ground rules communicated"
  
  documents:
    - [ ] "Incident report draft"
    - [ ] "Timeline document"
    - [ ] "Evidence catalog"
    - [ ] "Metrics dashboard"
    - [ ] "Action item template"
```

### Post-Mortem Meeting Checklist

```yaml
post_mortem_meeting:
  opening:
    - [ ] "Ground rules reviewed"
    - [ ] "Incident summary presented"
    - [ ] "Timeline walkthrough"
  
  discussion:
    - [ ] "Root cause analysis"
    - [ ] "What went well"
    - [ ] "What could improve"
    - [ ] "Action items identified"
  
  closing:
    - [ ] "Action items assigned"
    - [ ] "Deadlines set"
    - [ ] "Follow-up scheduled"
    - [ ] "Next steps documented"
```

### Post-Mortem Follow-Up Checklist

```yaml
post_mortem_follow_up:
  documentation:
    - [ ] "Post-mortem document finalized"
    - [ ] "Document shared with team"
    - [ ] "Document archived"
  
  action_items:
    - [ ] "Action items in tracking system"
    - [ ] "Owners confirmed"
    - [ ] "Deadlines confirmed"
    - [ ] "Follow-up meetings scheduled"
  
  improvements:
    - [ ] "Process improvements implemented"
    - [ ] "Runbooks updated"
    - [ ] "Monitoring enhanced"
    - [ ] "Training scheduled"
  
  communication:
    - [ ] "Lessons learned shared"
    - [ ] "Improvements communicated"
    - [ ] "Success celebrated"
```

### Continuous Improvement Checklist

```yaml
continuous_improvement:
  metrics_tracking:
    - [ ] "Incident metrics tracked"
    - [ ] "Trends analyzed"
    - [ ] "Improvements measured"
    - [ ] "Report generated"
  
  process_review:
    - [ ] "Response process reviewed"
    - [ ] "Gaps identified"
    - [ ] "Improvements planned"
    - [ ] "Changes implemented"
  
  team_development:
    - [ ] "Training needs identified"
    - [ ] "Training scheduled"
    - [ ] "Drills conducted"
    - [ ] "Skills assessed"
  
  tool_improvement:
    - [ ] "Tool effectiveness reviewed"
    - [ ] "Gaps identified"
    - [ ] "New tools evaluated"
    - [ ] "Integrations improved"
```

---

## Customization Guide

### Adding Custom Checklist Items

```yaml
customization_guide:
  adding_items:
    steps:
      - "Identify the gap in current checklists"
      - "Define the checklist item"
      - "Determine if automated or manual"
      - "Add to appropriate checklist"
      - "Test with team"
      - "Update documentation"
  
  example_custom_item:
    id: "custom_1"
    description: "Verify LLM safety filters are active"
    automated: true
    command: "check_safety_filters"
    priority: "critical"
    phase: "containment"
    incident_types: ["prompt_injection", "data_breach"]
```

### Environment-Specific Customization

```yaml
environment_customization:
  development:
    - [ ] "Local testing completed"
    - [ ] "Unit tests passed"
    - [ ] "Code review done"
  
  staging:
    - [ ] "Integration tests passed"
    - [ ] "Performance tests passed"
    - [ ] "Security scan clean"
  
  production:
    - [ ] "Deployment approved"
    - [ ] "Rollback plan ready"
    - [ ] "Monitoring enabled"
    - [ ] "On-call notified"
```

---

## Summary

### Key Checklists by Phase

```yaml
key_checklists:
  detection:
    - "Verify incident is real"
    - "Assess severity"
    - "Document initial observations"
  
  triage:
    - "Classify incident"
    - "Assess impact"
    - "Assign response team"
    - "Develop response plan"
  
  containment:
    - "Isolate threat"
    - "Control access"
    - "Enhance monitoring"
    - "Validate containment"
  
  remediation:
    - "Identify root cause"
    - "Implement fix"
    - "Validate fix"
  
  recovery:
    - "Restore service"
    - "Verify functionality"
    - "Normalize operations"
  
  post_mortem:
    - "Conduct meeting"
    - "Document findings"
    - "Assign action items"
    - "Track improvements"
```

### Quick Reference

```yaml
quick_reference:
  p0:
    response_time: "15 minutes"
    resolution_target: "2 hours"
    key_checklist: "P0 Critical Incident Checklist"
  
  p1:
    response_time: "30 minutes"
    resolution_target: "4 hours"
    key_checklist: "P1 High Incident Checklist"
  
  p2:
    response_time: "2 hours"
    resolution_target: "24 hours"
    key_checklist: "P2 Medium Incident Checklist"
  
  p3:
    response_time: "24 hours"
    resolution_target: "1 week"
    key_checklist: "P3 Low Incident Checklist"
```

---

*Last Updated: 2024*
*Version: 1.0*
*Owner: Engineering & Security Teams*
