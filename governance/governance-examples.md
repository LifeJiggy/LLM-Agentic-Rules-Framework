# Governance Examples - LLM & Agentic Rules Framework

## Overview

This document provides practical implementation examples for governance in LLM and agentic systems.

## Example 1: Policy Template

### Context

**When to Use**: Creating new governance policies

**Goal**: Document policies for AI system governance

### Implementation

```yaml
policy_template:
  policy_id: "POL-001"
  title: "AI System Governance Policy"
  version: "1.0"
  effective_date: "2026-01-01"
  owner: "Chief Ethics Officer"
  approved_by: "Board of Directors"
  
  purpose: "Establish governance framework for AI systems"
  
  scope: "All AI systems developed or deployed by the organization"
  
  policy_statements:
    - statement: "All AI systems must have documented purpose and intended use"
      rationale: "Ensures systems are developed with clear objectives"
      compliance: "mandatory"
    
    - statement: "All AI systems must undergo risk assessment"
      rationale: "Identifies and mitigates potential harms"
      compliance: "mandatory"
    
    - statement: "All AI systems must have human oversight for high-risk decisions"
      rationale: "Ensures accountability and safety"
      compliance: "mandatory"
    
    - statement: "All AI systems must be monitored for performance and fairness"
      rationale: "Ensures ongoing quality and equity"
      compliance: "mandatory"
    
    - statement: "All AI systems must have incident response procedures"
      rationale: "Enables rapid response to issues"
      compliance: "mandatory"
  
  responsibilities:
    - role: "System Owner"
      responsibilities:
        - "Document system purpose and intended use"
        - "Conduct risk assessment"
        - "Implement monitoring"
        - "Respond to incidents"
    
    - role: "Ethics Officer"
      responsibilities:
        - "Review high-risk systems"
        - "Approve policy exceptions"
        - "Conduct audits"
        - "Report to board"
    
    - role: "Engineering Team"
      responsibilities:
        - "Implement controls"
        - "Conduct testing"
        - "Monitor performance"
        - "Respond to incidents"
  
  enforcement:
    - "Policy compliance is mandatory"
    - "Violations may result in disciplinary action"
    - "Exceptions require approval from Ethics Officer"
    - "Audits conducted annually"
  
  review:
    frequency: "annually"
    reviewers: ["Ethics Officer", "Legal", "Engineering"]
    approval_required: true
```

## Example 2: Exception Register

### Context

**When to Use**: Tracking policy exceptions

**Goal**: Manage exceptions to governance policies

### Implementation

```yaml
exception_register:
  system_id: "support-assistant-001"
  last_updated: "2026-06-04"
  owner: "Compliance Team"
  
  exceptions:
    - exception_id: "EXC-001"
      policy_id: "POL-001"
      policy_requirement: "Human review for all high-risk decisions"
      exception_reason: "Automated approval for low-risk decisions under $100"
      compensating_controls:
        - "Daily audit of all automated decisions"
        - "Weekly sample review by compliance"
        - "Alert on anomalous patterns"
      owner: "Product Manager"
      approver: "Ethics Officer"
      expiry_date: "2026-12-31"
      status: "active"
      review_history:
        - date: "2026-06-04"
          decision: "approved"
          rationale: "Low risk, good compensating controls"
    
    - exception_id: "EXC-002"
      policy_id: "POL-002"
      policy_requirement: "Data retention max 90 days"
      exception_reason: "Legal hold requires 7-year retention for audit"
      compensating_controls:
        - "Legal hold review quarterly"
        - "Access restricted to legal team"
        - "Encryption at rest and in transit"
      owner: "Legal Team"
      approver: "Ethics Officer"
      expiry_date: "2027-06-04"
      status: "active"
      review_history:
        - date: "2026-06-04"
          decision: "approved"
          rationale: "Legal requirement, appropriate controls"
  
  metrics:
    total_exceptions: 2
    active_exceptions: 2
    expired_exceptions: 0
    pending_review: 0
```

## Example 3: Audit Evidence Package

### Context

**When to Use**: Preparing for compliance audits

**Goal**: Organize evidence for audit readiness

### Implementation

```yaml
audit_evidence_package:
  audit_id: "AUDIT-2026-Q2"
  system_id: "support-assistant-001"
  audit_date: "2026-06-04"
  
  sections:
    - section: "system_documentation"
      evidence:
        - evidence_id: "DOC-001"
          type: "document"
          name: "System Purpose Document"
          location: "docs/system-purpose.md"
          last_updated: "2026-01-15"
        
        - evidence_id: "DOC-002"
          type: "document"
          name: "Risk Assessment"
          location: "docs/risk-assessment.md"
          last_updated: "2026-03-01"
        
        - evidence_id: "DOC-003"
          type: "document"
          name: "Architecture Decision Records"
          location: "docs/adr/"
          last_updated: "2026-05-15"
    
    - section: "control_evidence"
      evidence:
        - evidence_id: "CTRL-001"
          type: "configuration"
          name: "Access Control Configuration"
          location: "config/access-control.yaml"
          last_updated: "2026-04-01"
        
        - evidence_id: "CTRL-002"
          type: "report"
          name: "Security Scan Results"
          location: "reports/security-scan-2026-06.pdf"
          last_updated: "2026-06-01"
        
        - evidence_id: "CTRL-003"
          type: "report"
          name: "Penetration Test Report"
          location: "reports/pentest-2026-Q1.pdf"
          last_updated: "2026-03-31"
    
    - section: "operational_evidence"
      evidence:
        - evidence_id: "OPS-001"
          type: "log"
          name: "Incident Log"
          location: "logs/incidents/"
          last_updated: "2026-06-01"
        
        - evidence_id: "OPS-002"
          type: "report"
          name: "Post-Mortem Reports"
          location: "reports/post-mortems/"
          last_updated: "2026-05-15"
        
        - evidence_id: "OPS-003"
          type: "report"
          name: "Monitoring Dashboard"
          location: "dashboards/production"
          last_updated: "real_time"
    
    - section: "compliance_evidence"
      evidence:
        - evidence_id: "COMP-001"
          type: "document"
          name: "Exception Register"
          location: "compliance/exception-register.yaml"
          last_updated: "2026-06-04"
        
        - evidence_id: "COMP-002"
          type: "report"
          name: "Training Completion Records"
          location: "compliance/training/"
          last_updated: "2026-05-31"
        
        - evidence_id: "COMP-003"
          type: "document"
          name: "Vendor DPA Records"
          location: "compliance/vendor-dpas/"
          last_updated: "2026-04-15"
  
  validation:
    completeness: "95%"
    accuracy: "verified"
    currency: "current"
    integrity: "hash_chain"
  
  sign_off:
    auditor: "External Audit Firm"
    date: "2026-06-15"
    status: "approved"
    findings: "None"
```

## Model Governance Policy Template

```yaml
model_governance_policy:
  metadata:
    policy_id: "MGP-001"
    policy_name: "AI Model Governance Policy"
    version: "1.0"
    effective_date: "2025-01-01"
    review_date: "2026-01-01"
    owner: "AI Ethics Board"
    approved_by: "Chief Technology Officer"
    classification: "Internal"
  
  purpose: |
    This policy establishes requirements for the development, validation,
    deployment, and monitoring of AI models. It ensures models are
    developed responsibly, operate effectively, and maintain compliance.
  
  scope: |
    This policy applies to all AI models developed, deployed, or used
    by the organization, including:
    - Machine learning models
    - Large language models
    - Recommendation systems
    - Decision support systems
    - Automated decision-making systems
  
  model_lifecycle:
    development:
      requirements:
        - "Use version control for all artifacts"
        - "Follow coding standards"
        - "Document data sources"
        - "Record hyperparameters"
        - "Maintain development logs"
      standards:
        - "Code review required"
        - "Documentation required"
        - "Testing required"
        - "Security review required"
        - "Ethics review required"
    
    validation:
      requirements:
        - "Performance testing"
        - "Bias testing"
        - "Security testing"
        - "Robustness testing"
        - "Fairness evaluation"
      criteria:
        - "Performance benchmarks met"
        - "Bias thresholds not exceeded"
        - "Security vulnerabilities addressed"
        - "Robustness requirements met"
        - "Fairness criteria satisfied"
    
    deployment:
      requirements:
        - "Approval gates passed"
        - "Documentation complete"
        - "Monitoring configured"
        - "Rollback plan documented"
        - "Stakeholders notified"
      criteria:
        - "All validation passed"
        - "All approvals obtained"
        - "All documentation complete"
        - "All monitoring active"
        - "All stakeholders informed"
    
    monitoring:
      requirements:
        - "Performance monitoring"
        - "Quality monitoring"
        - "Safety monitoring"
        - "Drift detection"
        - "Incident detection"
      criteria:
        - "Monitoring active and alerting"
        - "Metrics within thresholds"
        - "No safety issues detected"
        - "No drift detected"
        - "No incidents unaddressed`
  
  model_card_requirements:
    required_fields:
      - "Model name and version"
      - "Model owner"
      - "Model purpose"
      - "Training data description"
      - "Performance metrics"
      - "Bias metrics"
      - "Known limitations"
      - "Intended use"
      - "Not intended use"
      - "Ethical considerations`
    optional_fields:
      - "Architecture details"
      - "Training process"
      - "Evaluation methodology"
      - "Comparison to baselines"
      - "Future improvements`
  
  approval_gates:
    development_approval:
      authority: "Team Lead"
      criteria:
        - "Code review complete"
        - "Documentation complete"
        - "Tests passing"
      turnaround: "1 business day"
    
    validation_approval:
      authority: "Validation Team"
      criteria:
        - "All validation tests passed"
        - "Bias testing complete"
        - "Security testing complete"
      turnaround: "3 business days"
    
    deployment_approval:
      authority: "Director"
      criteria:
        - "All approvals obtained"
        - "All documentation complete"
        - "All monitoring configured"
      turnaround: "2 business days"
    
    high_risk_approval:
      authority: "VP/CISO"
      criteria:
        - "All standard approvals"
        - "Enhanced documentation"
        - "Additional testing"
        - "Executive briefing`
      turnaround: "5 business days`
```

## Incident Response Policy Template

```yaml
incident_response_policy:
  metadata:
    policy_id: "IRP-001"
    policy_name: "AI Incident Response Policy"
    version: "1.0"
    effective_date: "2025-01-01"
    review_date: "2026-01-01"
    owner: "Security Team"
    approved_by: "Chief Information Security Officer"
    classification: "Internal"
  
  purpose: |
    This policy defines how to respond to incidents involving AI systems,
    including model failures, security breaches, ethical violations,
    and regulatory non-compliance.
  
  scope: |
    This policy applies to all incidents involving AI systems, including:
    - Model performance degradation
    - Security incidents
    - Ethical violations
    - Data privacy breaches
    - Regulatory non-compliance
    - System outages
  
  severity_levels:
    - level: "P0 - Critical"
      description: "System-wide failure or safety issue"
      response_time: "15 minutes"
      resolution_time: "4 hours"
      escalation: "Immediate executive notification"
      examples:
        - "Complete system failure"
        - "Safety incident"
        - "Data breach"
        - "Regulatory violation`
    
    - level: "P1 - High"
      description: "Significant degradation or security issue"
      response_time: "1 hour"
      resolution_time: "24 hours"
      escalation: "Management notification within 1 hour"
      examples:
        - "Major performance degradation"
        - "Security vulnerability exploited"
        - "Bias detected in production"
        - "Service disruption`
    
    - level: "P2 - Medium"
      description: "Partial degradation or minor security issue"
      response_time: "4 hours"
      resolution_time: "72 hours"
      escalation: "Team lead notification within 4 hours"
      examples:
        - "Minor performance degradation"
        - "Minor security issue"
        - "Minor bias concern"
        - "Partial service disruption`
    
    - level: "P3 - Low"
      description: "Minor issue with workaround"
      response_time: "24 hours"
      resolution_time: "1 week"
      escalation: "Standard process"
      examples:
        - "Minor bug"
        - "Minor documentation issue"
        - "Minor performance concern`
  
  response_phases:
    detection:
      activities:
        - "Identify the incident`
        - "Classify severity`
        - "Assign incident ID`
        - "Notify incident commander`
        - "Begin documentation`
      responsible: "Incident Commander`
      timeline: "Immediate`
    
    containment:
      activities:
        - "Contain the incident`
        - "Preserve evidence`
        - "Assess impact`
        - "Implement short-term fix`
        - "Communicate status`
      responsible: "Technical Lead`
      timeline: "Within response time SLA`
    
    investigation:
      activities:
        - "Conduct root cause analysis`
        - "Identify contributing factors`
        - "Document findings`
        - "Develop remediation plan`
        - "Communicate findings`
      responsible: "Investigation Team`
      timeline: "Within resolution time SLA`
    
    remediation:
      activities:
        - "Implement remediation`
        - "Verify remediation`
        - "Document remediation`
        - "Update documentation`
        - "Communicate completion`
      responsible: "Remediation Team`
      timeline: "Per remediation plan`
    
    recovery:
      activities:
        - "Restore service`
        - "Verify operation`
        - "Monitor for recurrence`
        - "Update monitoring`
        - "Communicate recovery`
      responsible: "Operations Team`
      timeline: "Immediately after remediation`
    
    post_incident:
      activities:
        - "Conduct post-incident review`
        - "Document lessons learned`
        - "Identify improvements`
        - "Implement improvements`
        - "Share learnings`
      responsible: "Incident Commander`
      timeline: "Within 1 week of resolution`
  
  communication:
    internal:
      channels:
        - "Incident management platform`
        - "Email`
        - "Phone`
        - "Slack`
      audiences:
        - "Incident response team`
        - "Management`
        - "Executive team`
        - "All employees (if needed)`
      frequency:
        - "Initial notification: Immediate`
        - "Status updates: Every 2 hours for P0/P1`
        - "Resolution notification: Immediate`
    
    external:
      channels:
        - "Email`
        - "Phone`
        - "Public statement (if needed)`
      audiences:
        - "Affected users`
        - "Regulators (if required)`
        - "Media (if required)`
        - "Partners (if required)`
      requirements:
        - "Legal review required`
        - "Executive approval required`
        - "Consistent messaging`
        - "Documentation required`
  
  evidence_preservation:
    requirements:
      - "Preserve all relevant logs`
      - "Preserve system state`
      - "Preserve communications`
      - "Preserve forensic evidence`
      - "Chain of custody documentation`
    procedures:
      - "Isolate affected systems`
      - "Copy relevant logs`
      - "Document system state`
      - "Secure evidence storage`
      - "Access control on evidence`
  
  roles_and_responsibilities:
    - role: "Incident Commander"
      responsibilities:
        - "Overall incident management`
        - "Coordination of response`
        - "Communication management`
        - "Decision making`
        - "Post-incident review`
    
    - role: "Technical Lead"
      responsibilities:
        - "Technical investigation`
        - "Remediation implementation`
        - "Recovery execution`
        - "Technical communication`
        - "Documentation`
    
    - role: "Communications Lead"
      responsibilities:
        - "Internal communication`
        - "External communication`
        - "Stakeholder management`
        - "Message development`
        - "Media management`
    
    - role: "Legal Counsel"
      responsibilities:
        - "Legal assessment`
        - "Regulatory notification`
        - "Liability assessment`
        - "Evidence preservation`
        - "Legal communication`
```

## Training Program Template

```yaml
training_program_template:
  metadata:
    program_id: "TP-001"
    program_name: "AI Governance Training Program"
    version: "1.0"
    effective_date: "2025-01-01"
    review_date: "2026-01-01"
    owner: "Training Coordinator"
    approved_by: "Chief Compliance Officer"
    classification: "Internal"
  
  purpose: |
    This program ensures all stakeholders understand AI governance
    requirements, policies, and procedures. It builds capability
    to comply with governance requirements.
  
  target_audiences:
    - audience: "All Employees"
      training_required:
        - "AI Governance Fundamentals"
        - "Acceptable Use Policy"
        - "Data Privacy Basics"
        - "Incident Reporting"
      frequency: "Annual"
      duration: "2 hours"
      format: "Online self-paced`
    
    - audience: "Technical Teams"
      training_required:
        - "Advanced AI Governance"
        - "Model Development Standards"
        - "Security Requirements"
        - "Monitoring and Alerting`
      frequency: "Annual`
      duration: "4 hours`
      format: "Instructor-led`
    
    - audience: "Management"
      training_required:
        - "Governance Leadership`
        - "Risk Management`
        - "Compliance Oversight`
        - "Incident Management`
      frequency: "Annual`
      duration: "3 hours`
      format: "Workshop`
    
    - audience: "Compliance Team"
      training_required:
        - "Audit Procedures`
        - "Evidence Collection`
        - "Reporting Requirements`
        - "Regulatory Updates`
      frequency: "Quarterly`
      duration: "2 hours`
      format: "Instructor-led`
  
  training_modules:
    - module: "AI Governance Fundamentals"
      description: "Introduction to AI governance concepts`
      duration: "45 minutes`
      content:
        - "What is AI governance`
        - "Why governance matters`
        - "Governance framework overview`
        - "Roles and responsibilities`
        - "Compliance requirements`
      assessment:
        type: "Multiple choice`
        questions: 20
        passing_score: "80%`
      delivery:
        format: "Online self-paced`
        platform: "Learning Management System`
        completion_tracking: "Automatic`
    
    - module: "Acceptable Use Policy"
      description: "Understanding acceptable use of AI systems`
      duration: "30 minutes`
      content:
        - "Permitted uses`
        - "Prohibited uses`
        - "Conditional uses`
        - "Reporting violations`
        - "Consequences`
      assessment:
        type: "Scenario-based`
        questions: 10
        passing_score: "80%`
      delivery:
        format: "Online self-paced`
        platform: "Learning Management System`
        completion_tracking: "Automatic`
    
    - module: "Data Privacy Basics"
      description: "Understanding data privacy requirements`
      duration: "30 minutes`
      content:
        - "What is personal data`
        - "Data privacy principles`
        - "Data handling requirements`
        - "Privacy controls`
        - "Reporting breaches`
      assessment:
        type: "Multiple choice`
        questions: 15
        passing_score: "80%`
      delivery:
        format: "Online self-paced`
        platform: "Learning Management System`
        completion_tracking: "Automatic`
    
    - module: "Model Development Standards"
      description: "Standards for developing AI models`
      duration: "60 minutes`
      content:
        - "Development process`
        - "Documentation requirements`
        - "Testing requirements`
        - "Validation requirements`
        - "Deployment requirements`
      assessment:
        type: "Practical exercise`
        scenarios: 3
        passing_score: "80%`
      delivery:
        format: "Instructor-led`
        platform: "Training room`
        completion_tracking: "Manual`
    
    - module: "Security Requirements"
      description: "Security requirements for AI systems`
      duration: "45 minutes`
      content:
        - "Access controls`
        - "Data protection`
        - "Threat protection`
        - "Incident response`
        - "Security monitoring`
      assessment:
        type: "Multiple choice`
        questions: 20
        passing_score: "80%`
      delivery:
        format: "Online self-paced`
        platform: "Learning Management System`
        completion_tracking: "Automatic`
  
  tracking_and_reporting:
    tracking_system:
      platform: "Learning Management System`
      features:
        - "Course enrollment`
        - "Completion tracking`
        - "Assessment scoring`
        - "Certificate generation`
        - "Reporting`
    
    metrics:
      - metric: "Completion Rate"
        target: "100%"
        measurement: "Completed / Enrolled`
        frequency: "Monthly`
      
      - metric: "Assessment Pass Rate"
        target: "> 90%"
        measurement: "Passed / Attempted`
        frequency: "Monthly`
      
      - metric: "Average Score"
        target: "> 85%"
        measurement: "Average of all scores`
        frequency: "Monthly`
      
      - metric: "Time to Complete"
        target: "< 30 days`
        measurement: "Completion date - Assignment date`
        frequency: "Monthly`
    
    reporting:
      - report: "Monthly Training Report"
        audience: "Management`
        frequency: "Monthly`
        content:
          - "Completion rates`
          - "Assessment results`
          - "Trend analysis`
          - "Issues and recommendations`
      
      - report: "Quarterly Training Summary"
        audience: "Executive team`
        frequency: "Quarterly`
        content:
          - "Overall training effectiveness`
          - "Compliance status`
          - "Improvement opportunities`
          - "Resource requirements`
  
  remediation:
    non_completion:
      process:
        - "Identify non-completions`
        - "Send reminders`
        - "Escalate to manager`
        - "Restrict access (if needed)`
        - "Report to compliance`
      timeline:
        - "Initial reminder: 7 days before deadline`
        - "Second reminder: 3 days before deadline`
        - "Manager escalation: 1 day after deadline`
        - "Access restriction: 7 days after deadline`
        - "Compliance report: 14 days after deadline`
    
    assessment_failure:
      process:
        - "Provide feedback`
        - "Offer additional training`
        - "Allow retake`
        - "Escalate if repeated failure`
        - "Document remediation`
      attempts:
        max: 3
        cooldown: "24 hours between attempts`
        escalation: "After 3 failures`
  
  maintenance:
    content_review:
      frequency: "Annual`
      activities:
        - "Review training content`
        - "Update for regulatory changes`
        - "Incorporate feedback`
        - "Update examples`
        - "Refresh delivery methods`
    
    effectiveness_review:
      frequency: "Quarterly`
      activities:
        - "Analyze metrics`
        - "Gather feedback`
        - "Identify improvements`
        - "Implement changes`
        - "Measure impact`
    
    technology_maintenance:
      frequency: "Monthly`
      activities:
        - "Update LMS"
        - "Maintain content"
        - "Fix issues`
        - "Optimize performance`
        - "Ensure security`
```

## Compliance Dashboard Template

```yaml
compliance_dashboard_template:
  metadata:
    dashboard_id: "CD-001"
    dashboard_name: "Governance Compliance Dashboard"
    version: "1.0"
    last_updated: "2025-07-24"
    owner: "Compliance Team"
    classification: "Internal"
  
  overview_section:
    title: "Governance Overview"
    metrics:
      - metric: "Overall Compliance Score"
        value: "98%"
        target: "95%"
        status: "Green"
        trend: "Improving"
      
      - metric: "Active Exceptions"
        value: "5"
        target: "< 10"
        status: "Green"
        trend: "Stable"
      
      - metric: "Open Audit Findings"
        value: "2"
        target: "0"
        status: "Yellow"
        trend: "Decreasing"
      
      - metric: "Training Completion"
        value: "95%"
        target: "100%"
        status: "Yellow"
        trend: "Improving"
      
      - metric: "Incidents (MTD)"
        value: "3"
        target: "< 5"
        status: "Green"
        trend: "Stable"
  
  compliance_section:
    title: "Compliance by Category"
    categories:
      - category: "Policy Compliance"
        score: "100%"
        status: "Green"
        details: "All policies current and enforced`
      
      - category: "Access Controls"
        score: "98%"
        status: "Green"
        details: "2 minor issues remediated`
      
      - category: "Data Governance"
        score: "97%"
        status: "Green"
        details: "Data quality on target`
      
      - category: "Security Controls"
        score: "100%"
        status: "Green"
        details: "All controls operating`
      
      - category: "Model Governance"
        score: "96%"
        status: "Green"
        details: "All models documented`
      
      - category: "Incident Management"
        score: "100%"
        status: "Green"
        details: "All incidents handled`
  
  exceptions_section:
    title: "Exception Summary"
    metrics:
      - metric: "Total Active Exceptions"
        value: "5"
        breakdown:
          low_risk: 3
          medium_risk: 2
          high_risk: 0
          critical: 0
      
      - metric: "Exceptions Pending Review"
        value: "2"
        oldest_age: "15 days`
      
      - metric: "Exceptions Expiring Soon"
        value: "1"
        expiry_date: "2025-08-15`
      
      - metric: "Overdue Reviews"
        value: "0"
        status: "Green"
  
  audit_section:
    title: "Audit Status"
    metrics:
      - metric: "Internal Audits"
        completed_ytd: 2
        planned_next_quarter: 1
        findings_open: 2
        findings_closed: 8
      
      - metric: "External Audits"
        last_audit: "2025-03-15"
        next_audit: "2025-09-15"
        certification: "ISO 42001"
        status: "Certified`
      
      - metric: "Self-Assessments"
        completed_ytd: 4
        next_scheduled: "2025-07-31"
        average_score: "95%"
  
  training_section:
    title: "Training Status"
    metrics:
      - metric: "Overall Completion"
        value: "95%"
        target: "100%"
        trend: "Improving"
      
      - metric: "New Hire Training"
        completion_rate: "100%"
        average_time_to_complete: "5 days"
      
      - metric: "Annual Refresher"
        completion_rate: "92%"
        deadline: "2025-12-31"
        days_remaining: "160"
      
      - metric: "Assessment Scores"
        average: "87%"
        passing_rate: "95%"
  
  incidents_section:
    title: "Incident Summary"
    metrics:
      - metric: "Incidents (MTD)"
        total: 3
        by_severity:
          p0: 0
          p1: 1
          p2: 2
          p3: 0
      
      - metric: "Mean Time to Resolve"
        current: "3.5 hours"
        target: "< 4 hours"
        status: "Green"
      
      - metric: "Incident Trend"
        current_month: 3
        previous_month: 4
        trend: "Decreasing"
  
  risk_section:
    title: "Risk Summary"
    metrics:
      - metric: "Overall Risk Score"
        value: "Low"
        trend: "Stable"
      
      - metric: "High-Risk Items"
        value: "2"
        items:
          - "EU AI Act compliance`
          - "Resource constraints`
      
      - metric: "Risk Mitigations"
        active: 8
        completed_ytd: 5
        effectiveness: "90%"
  
  trends_section:
    title: "Trends (6 Months)"
    charts:
      - chart: "Compliance Score Trend"
        data:
          - month: "2025-01"
            value: "92%"
          - month: "2025-02"
            value: "94%"
          - month: "2025-03"
            value: "95%"
          - month: "2025-04"
            value: "97%"
          - month: "2025-05"
            value: "98%"
          - month: "2025-06"
            value: "98%"
      
      - chart: "Exception Count Trend"
        data:
          - month: "2025-01"
            value: 8
          - month: "2025-02"
            value: 7
          - month: "2025-03"
            value: 6
          - month: "2025-04"
            value: 6
          - month: "2025-05"
            value: 5
          - month: "2025-06"
            value: 5
      
      - chart: "Training Completion Trend"
        data:
          - month: "2025-01"
            value: "85%"
          - month: "2025-02"
            value: "88%"
          - month: "2025-03"
            value: "90%"
          - month: "2025-04"
            value: "92%"
          - month: "2025-05"
            value: "94%"
          - month: "2025-06"
            value: "95%"
  
  actions_section:
    title: "Action Items"
    items:
      - action: "Complete marketing team training"
        owner: "Training Coordinator"
        due: "2025-07-15"
        priority: "High"
        status: "In Progress"
      
      - action: "Close medium-risk exceptions"
        owner: "Compliance Officer"
        due: "2025-07-31"
        priority: "Medium"
        status: "In Progress"
      
      - action: "Prepare for EU AI Act"
        owner: "Legal Team"
        due: "2025-08-31"
        priority: "High"
        status: "Planning"
      
      - action: "Remediate audit findings"
        owner: "Technical Lead"
        due: "2025-07-31"
        priority: "High"
        status: "In Progress"
```

## Example Summary

| Example | Complexity | Time Required | Key Components |
|---------|------------|---------------|----------------|
| Policy Template | Medium | 2 hours | Policy statements, responsibilities |
| Exception Register | Low | 1 hour | Exception tracking, review history |
| Audit Evidence | High | 4 hours | Evidence collection, validation |
| Model Governance | Medium | 3 hours | Lifecycle, approval gates, documentation |
| Incident Response | Medium | 2 hours | Severity levels, response phases, communication |
| Training Program | High | 4 hours | Modules, assessment, tracking, remediation |
| Compliance Dashboard | High | 6 hours | Metrics, trends, actions, visualization |
