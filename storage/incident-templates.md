# Incident Templates - Comprehensive Collection

## Overview

This document provides complete templates for incident response, runbooks, and post-incident reviews.

## Incident Report Template

```yaml
incident_report:
  incident_id: string
  title: string
  severity: critical | high | medium | low
  status: detected | investigating | contained | resolved | closed
  
  timeline:
    detected_at: string
    reported_at: string
    acknowledged_at: string
    contained_at: string | null
    resolved_at: string | null
    closed_at: string | null
    detection_source: monitoring | user_report | internal_report | external_report
  
  impact:
    affected_systems: [list]
    affected_users: integer
    affected_data_types: [list]
    business_impact: string
    financial_impact: string
    reputation_impact: string
    compliance_impact: string
  
  classification:
    category: security | data_breach | availability | performance | compliance | other
    subcategory: string
    attack_vector: string | null
    threat_actor: internal | external | unknown
    motivation: financial | espionage | sabotage | accidental | unknown
  
  investigation:
    root_cause: string
    contributing_factors: [list]
    attack_timeline: [list]
    evidence_collected: [list]
    forensic_analysis: string | null
  
  response:
    containment_actions: [list]
    eradication_actions: [list]
    recovery_actions: [list]
    communication_actions: [list]
  
  resolution:
    resolution_summary: string
    lessons_learned: [list]
    improvements_identified: [list]
    follow_up_actions: [list]
  
  team:
    incident_commander: string
    technical_lead: string
    communications_lead: string
    team_members: [list]
    external_partners: [list]
  
  evidence:
    - evidence_id: string
      type: log | screenshot | configuration | code | communication
      description: string
      location: string
      collected_by: string
      collected_at: string
      integrity_hash: string
  
  communication:
    internal_updates: [list]
    external_notifications: [list]
    regulatory_notifications: [list]
  
  post_incident:
    post_mortem_date: string
    post_mortem_attendees: [list]
    root_cause_analysis: string
    action_items: [list]
    timeline_reconstruction: string
```

## Incident Response Runbook Template

```yaml
runbook:
  runbook_id: string
  title: string
  version: string
  last_updated: string
  owner: string
  status: active | draft | archived
  
  scope:
    description: string
    applicable_incidents: [list]
    prerequisites: [list]
  
  roles:
    - role: Incident Commander
      responsibilities: [list]
      contact: string
    - role: Technical Lead
      responsibilities: [list]
      contact: string
    - role: Communications Lead
      responsibilities: [list]
      contact: string
  
  detection:
    sources:
      - source: monitoring
        alerts: [list]
        dashboards: [list]
      - source: user_report
        channels: [list]
        escalation: string
      - source: internal_report
        channels: [list]
        escalation: string
    
    initial_assessment:
      - question: "What is the affected system?"
        purpose: Identify scope
      - question: "What is the user impact?"
        purpose: Determine severity
      - question: "Is data exposed?"
        purpose: Assess data breach
      - question: "Is the issue ongoing?"
        purpose: Determine urgency
  
  response_procedures:
    phase_1_containment:
      name: Containment
      duration: 15_minutes
      steps:
        - step: 1
          action: "Isolate affected system"
          command: "[isolation command]"
          verification: "[verification command]"
          timeout: 5_minutes
          failure_action: "Escalate to technical lead"
        
        - step: 2
          action: "Disable compromised accounts"
          command: "[disable command]"
          verification: "[verification command]"
          timeout: 5_minutes
          failure_action: "Escalate to security lead"
        
        - step: 3
          action: "Block malicious IPs"
          command: "[block command]"
          verification: "[verification command]"
          timeout: 5_minutes
          failure_action: "Escalate to operations"
    
    phase_2_eradication:
      name: Eradication
      duration: 60_minutes
      steps:
        - step: 1
          action: "Identify root cause"
          commands:
            - "[diagnostic command 1]"
            - "[diagnostic command 2]"
          verification: "[verification command]"
          timeout: 30_minutes
          failure_action: "Escalate to engineering"
        
        - step: 2
          action: "Remove malicious artifacts"
          command: "[removal command]"
          verification: "[verification command]"
          timeout: 15_minutes
          failure_action: "Escalate to security"
        
        - step: 3
          action: "Patch vulnerability"
          command: "[patch command]"
          verification: "[verification command]"
          timeout: 15_minutes
          failure_action: "Escalate to engineering"
    
    phase_3_recovery:
      name: Recovery
      duration: 60_minutes
      steps:
        - step: 1
          action: "Restore from clean backup"
          command: "[restore command]"
          verification: "[verification command]"
          timeout: 30_minutes
          failure_action: "Escalate to operations"
        
        - step: 2
          action: "Verify system integrity"
          command: "[verification command]"
          verification: "[verification command]"
          timeout: 15_minutes
          failure_action: "Escalate to security"
        
        - step: 3
          action: "Gradually restore service"
          command: "[restore command]"
          verification: "[verification command]"
          timeout: 15_minutes
          failure_action: "Escalate to operations"
    
    phase_4_communication:
      name: Communication
      duration: ongoing
      steps:
        - step: 1
          action: "Notify internal stakeholders"
          template: "[internal notification template]"
          recipients: [list]
          timeout: 15_minutes
        
        - step: 2
          action: "Notify affected users"
          template: "[user notification template]"
          recipients: [list]
          timeout: 1_hour
        
        - step: 3
          action: "Notify regulators if required"
          template: "[regulatory notification template]"
          recipients: [list]
          timeout: 72_hours
          conditions: [list]
  
  escalation:
    triggers:
      - trigger: "Incident not contained within 30 minutes"
        action: "Escalate to CISO"
      - trigger: "Data breach confirmed"
        action: "Activate breach response team"
      - trigger: "Regulatory notification required"
        action: "Engage legal counsel"
    
    contacts:
      - level: 1
        role: On-call Engineer
        contact: "[on-call contact]"
        response_time: 15_minutes
      - level: 2
        role: Technical Lead
        contact: "[lead contact]"
        response_time: 30_minutes
      - level: 3
        role: Security Lead
        contact: "[security contact]"
        response_time: 1_hour
      - level: 4
        role: CISO
        contact: "[ciso contact]"
        response_time: 2_hours
      - level: 5
        role: Executive Team
        contact: "[executive contact]"
        response_time: 4_hours
  
  verification:
    post_recovery_checks:
      - check: "System health verified"
        command: "[health check command]"
        expected: "[expected output]"
      - check: "Monitoring functional"
        command: "[monitoring check]"
        expected: "[expected output]"
      - check: "Security controls active"
        command: "[security check]"
        expected: "[expected output]"
      - check: "No ongoing attacks"
        command: "[attack check]"
        expected: "[expected output]"
  
  documentation:
    required_artifacts:
      - "Incident timeline"
      - "Root cause analysis"
      - "Impact assessment"
      - "Evidence collected"
      - "Actions taken"
      - "Lessons learned"
      - "Follow-up actions"
    
    templates:
      - name: "Incident Report"
        location: "[template location]"
      - name: "Post-Incident Review"
        location: "[template location]"
      - name: "Executive Summary"
        location: "[template location]"
```

## Post-Incident Review Template

```yaml
post_incident_review:
  review_id: string
  incident_id: string
  title: string
  review_date: string
  status: scheduled | in_progress | completed
  
  attendees:
    - name: string
      role: string
      department: string
  
  timeline_reconstruction:
    - timestamp: string
      event: string
      actor: string
      details: string
      evidence: [list]
  
  root_cause_analysis:
    primary_cause: string
    contributing_factors: [list]
    why_questions:
      - question: "Why did the incident occur?"
        answer: string
      - question: "Why was the root cause not prevented?"
        answer: string
      - question: "Why was the incident not detected earlier?"
        answer: string
      - question: "Why was the response delayed?"
        answer: string
  
  impact_summary:
    duration: string
    affected_users: integer
    affected_systems: [list]
    data_exposure: string | null
    financial_impact: string
    reputation_impact: string
    compliance_impact: string
  
  what_went_well:
    - item: string
      details: string
    - item: string
      details: string
  
  what_could_improve:
    - item: string
      details: string
      priority: high | medium | low
    - item: string
      details: string
      priority: high | medium | low
  
  action_items:
    - id: string
      action: string
      owner: string
      due_date: string
      status: open | in_progress | completed
      priority: high | medium | low
      category: prevention | detection | response | recovery
  
  metrics:
    time_to_detect: string
    time_to_contain: string
    time_to_eradicate: string
    time_to_recover: string
    total_duration: string
  
  lessons_learned:
    - lesson: string
      category: process | technology | people
      recommendation: string
  
  follow_up:
    next_review_date: string
    progress_review_frequency: string
    reporting_channel: string
```

## Emergency Response Template

```yaml
emergency_response:
  emergency_id: string
  title: string
  type: security_breach | data_breach | system_compromise | regulatory_emergency
  severity: critical
  declared_at: string
  declared_by: string
  
  activation:
    criteria:
      - "Active data breach with PII exposure"
      - "System compromise with ongoing attack"
      - "Regulatory notification deadline within 24 hours"
      - "Critical system outage affecting all users"
    
    procedures:
      - step: 1
        action: "Declare emergency"
        command: "[emergency declaration command]"
        notification: [list]
        timeout: immediate
      
      - step: 2
        action: "Activate emergency team"
        command: "[activation command]"
        notification: [list]
        timeout: 15_minutes
      
      - step: 3
        action: "Establish command center"
        command: "[command center setup]"
        notification: [list]
        timeout: 30_minutes
  
  emergency_team:
    - role: Emergency Commander
      name: string
      contact: string
      responsibilities: [list]
    - role: Technical Lead
      name: string
      contact: string
      responsibilities: [list]
    - role: Legal Counsel
      name: string
      contact: string
      responsibilities: [list]
    - role: Communications Lead
      name: string
      contact: string
      responsibilities: [list]
    - role: External Forensics
      name: string
      contact: string
      responsibilities: [list]
  
  immediate_actions:
    - action: "Isolate affected systems"
      commands: [list]
      timeout: 15_minutes
      success_criteria: string
    - action: "Preserve evidence"
      commands: [list]
      timeout: 30_minutes
      success_criteria: string
    - action: "Assess scope"
      commands: [list]
      timeout: 1_hour
      success_criteria: string
    - action: "Notify regulators if required"
      templates: [list]
      timeout: 72_hours
      success_criteria: string
  
  communication_plan:
    internal:
      - audience: Executive Team
        channel: "[channel]"
        frequency: "Every 2 hours"
        template: "[template]"
      - audience: All Employees
        channel: "[channel]"
        frequency: "As needed"
        template: "[template]"
    
    external:
      - audience: Affected Users
        channel: "[channel]"
        frequency: "Within 24 hours"
        template: "[template]"
        legal_review: required
      - audience: Regulators
        channel: "[channel]"
        frequency: "Within 72 hours"
        template: "[template]"
        legal_review: required
      - audience: Media
        channel: "[channel]"
        frequency: "As needed"
        template: "[template]"
        legal_review: required
  
  recovery_criteria:
    - criteria: "All affected systems restored"
      verification: "[verification method]"
      owner: string
    - criteria: "Security controls verified"
      verification: "[verification method]"
      owner: string
    - criteria: "Monitoring restored"
      verification: "[verification method]"
      owner: string
    - criteria: "All evidence preserved"
      verification: "[verification method]"
      owner: string
  
  post_emergency:
    - action: "Conduct emergency post-mortem"
      timeline: "Within 48 hours"
      attendees: [list]
    - action: "File regulatory notifications"
      timeline: "Per regulatory requirements"
      owner: string
    - action: "Notify affected individuals"
      timeline: "Within 72 hours"
      owner: string
    - action: "Implement immediate fixes"
      timeline: "Within 1 week"
      owner: string
```

## Data Breach Response Template

```yaml
data_breach_response:
  breach_id: string
  title: string
  discovered_at: string
  reported_at: string
  status: detected | assessing | containing | notifying | resolved
  
  breach_details:
    data_types_affected: [list]
    records_affected: integer
    data_subjects_affected: integer
    jurisdictions: [list]
    breach_cause: external_attack | internal_error | system_failure | unauthorized_access
    attack_vector: string | null
  
  assessment:
    risk_to_individuals: high | medium | low
    likelihood_of_harm: high | medium | low
    sensitivity_of_data: high | medium | low
    ease_of_identification: high | medium | low
    mitigation_possible: high | medium | low
    overall_risk: high | medium | low
  
  containment:
    immediate_actions: [list]
    evidence_preserved: boolean
    systems_isolated: [list]
    access_revoked: [list]
  
  notification:
    regulatory:
      - jurisdiction: string
        authority: string
        deadline: string
        submitted: boolean
        submission_date: string | null
        reference_number: string | null
    data_subjects:
      deadline: string
      method: email | mail | website | other
      template: string
      sent: boolean
      sent_date: string | null
    other:
      - party: string
        reason: string
        deadline: string
        notified: boolean
  
  remediation:
    immediate: [list]
    short_term: [list]
    long_term: [list]
  
  documentation:
    - document: "Breach Assessment Report"
      location: string
      status: complete | in_progress
    - document: "Evidence Package"
      location: string
      status: complete | in_progress
    - document: "Notification Records"
      location: string
      status: complete | in_progress
    - document: "Remediation Plan"
      location: string
      status: complete | in_progress
```

## Security Incident Checklist

### Detection and Assessment

- [ ] Incident detected and reported
- [ ] Initial assessment completed
- [ ] Severity classified
- [ ] Incident commander assigned
- [ ] Response team activated
- [ ] Communication channel established
- [ ] Timeline started

### Containment

- [ ] Affected systems isolated
- [ ] Malicious activity stopped
- [ ] Evidence preserved
- [ ] Access credentials rotated
- [ ] Network segmentation verified
- [ ] Monitoring enhanced

### Investigation

- [ ] Root cause identified
- [ ] Attack vector determined
- [ ] Scope of compromise assessed
- [ ] Data exposure identified
- [ ] Forensic analysis completed
- [ ] Evidence cataloged

### Eradication

- [ ] Malicious artifacts removed
- [ ] Vulnerabilities patched
- [ ] Backdoors identified and removed
- [ ] System integrity verified
- [ ] Security controls validated
- [ ] Clean state confirmed

### Recovery

- [ ] Systems restored from clean backups
- [ ] Services gradually restored
- [ ] Monitoring verified functional
- [ ] Security controls re-enabled
- [ ] User access restored
- [ ] Normal operations resumed

### Notification

- [ ] Internal stakeholders notified
- [ ] Affected users notified
- [ ] Regulators notified if required
- [ ] Law enforcement notified if required
- [ ] Partners notified if required
- [ ] Media statement prepared if needed

### Post-Incident

- [ ] Post-incident review scheduled
- [ ] Lessons learned documented
- [ ] Action items assigned
- [ ] Security improvements identified
- [ ] Process improvements identified
- [ ] Training needs identified

## Incident Severity Matrix

| Severity | Response Time | Escalation | Communication | Review |
|----------|---------------|------------|---------------|--------|
| Critical | Immediate | CISO, Executive | All stakeholders | 24 hours |
| High | 15 minutes | Security Lead | Management | 48 hours |
| Medium | 1 hour | On-call Lead | Team | 1 week |
| Low | 4 hours | Team Lead | Team | 2 weeks |

## Incident Communication Templates

### Internal Status Update

```markdown
# Incident Status Update - [Incident ID]

**Time**: [timestamp]
**Status**: [status]
**Severity**: [severity]

## Current Situation
[Description of current state]

## Impact
[Description of impact]

## Actions Taken
- [Action 1]
- [Action 2]

## Next Steps
- [Next step 1]
- [Next step 2]

## ETA to Resolution
[Estimate]

## Contact
[Incident commander contact]
```

### External User Notification

```markdown
# Security Incident Notification

**Date**: [date]
**Incident**: [brief description]

## What Happened
[Clear, concise description]

## What Information Was Involved
[Types of data affected]

## What We Are Doing
[Actions being taken]

## What You Can Do
[Recommended actions for users]

## For More Information
[Contact information]
```

### Regulatory Notification

```markdown
# Data Breach Notification

**Organization**: [name]
**Contact**: [name, title, phone, email]
**Date of Breach**: [date]
**Date of Discovery**: [date]
**Number of Individuals Affected**: [number]
**Types of Information Compromised**: [list]
**Description of Breach**: [detailed description]
**Measures Taken**: [actions taken]
**Measures Proposed**: [planned actions]
```

## Incident Metrics Template

```yaml
incident_metrics:
  period: string
  total_incidents: integer
  
  by_severity:
    critical: integer
    high: integer
    medium: integer
    low: integer
  
  by_category:
    security: integer
    data_breach: integer
    availability: integer
    performance: integer
    compliance: integer
  
  by_status:
    detected: integer
    investigating: integer
    contained: integer
    resolved: integer
    closed: integer
  
  performance:
    mean_time_to_detect: string
    mean_time_to_contain: string
    mean_time_to_resolve: string
    mean_time_to_close: string
  
  trends:
    - metric: incidents_per_month
      current: number
      previous: number
      trend: increasing | stable | decreasing
    - metric: mean_time_to_detect
      current: string
      previous: string
      trend: improving | stable | degrading
    - metric: mean_time_to_resolve
      current: string
      previous: string
      trend: improving | stable | degrading
  
  targets:
    mean_time_to_detect: string
    mean_time_to_contain: string
    mean_time_to_resolve: string
    incident_rate_per_month: number
  
  comparison:
    vs_target:
      mean_time_to_detect: meeting | not_meeting
      mean_time_to_contain: meeting | not_meeting
      mean_time_to_resolve: meeting | not_meeting
      incident_rate: meeting | not_meeting
    vs_previous_period:
      incidents: improved | same | degraded
      response_time: improved | same | degraded
      resolution_time: improved | same | degraded
```
