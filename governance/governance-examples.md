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

## Example Summary

| Example | Complexity | Time Required | Key Components |
|---------|------------|---------------|----------------|
| Policy Template | Medium | 2 hours | Policy statements, responsibilities |
| Exception Register | Low | 1 hour | Exception tracking, review history |
| Audit Evidence | High | 4 hours | Evidence collection, validation |
