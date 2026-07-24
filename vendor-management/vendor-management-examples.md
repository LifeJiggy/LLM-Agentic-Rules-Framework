# Vendor Management Examples - LLM & Agentic Rules Framework

## Overview

This document provides practical implementation examples for vendor management in LLM and agentic systems.

## Example 1: Vendor Assessment Template

### Context

**When to Use**: Evaluating new vendors before engagement

**Goal**: Assess vendor risk and compliance

### Implementation

```yaml
vendor_assessment:
  vendor: "AI Model Provider"
  assessment_date: "2026-06-04"
  assessor: "Security Team"
  
  sections:
    - section: "company_information"
      fields:
        - field: "company_name"
          value: "AI Provider Inc."
        - field: "headquarters"
          value: "San Francisco, CA"
        - field: "employees"
          value: "500-1000"
        - field: "founded"
          value: "2018"
        - field: "funding_stage"
          value: "Series C"
    
    - section: "security_assessment"
      criteria:
        - criterion: "SOC2_certification"
          status: "pass"
          evidence: "SOC2 Type II report dated 2026-01-15"
        
        - criterion: "encryption_at_rest"
          status: "pass"
          evidence: "AES-256 encryption documented"
        
        - criterion: "encryption_in_transit"
          status: "pass"
          evidence: "TLS 1.3 enforced"
        
        - criterion: "access_controls"
          status: "pass"
          evidence: "RBAC implemented"
        
        - criterion: "incident_response"
          status: "pass"
          evidence: "IR plan documented"
        
        - criterion: "penetration_testing"
          status: "pass"
          evidence: "Annual pentest completed"
    
    - section: "compliance_assessment"
      criteria:
        - criterion: "gdpr_compliance"
          status: "pass"
          evidence: "DPA available, SCCs implemented"
        
        - criterion: "ccpa_compliance"
          status: "pass"
          evidence: "Privacy notice updated"
        
        - criterion: "hipaa_compliance"
          status: "conditional"
          evidence: "BAA required"
        
        - criterion: "soc2_compliance"
          status: "pass"
          evidence: "SOC2 Type II report"
    
    - section: "operational_assessment"
      criteria:
        - criterion: "sla_guarantee"
          status: "pass"
          evidence: "99.9% uptime SLA"
        
        - criterion: "support_availability"
          status: "pass"
          evidence: "24/7 support available"
        
        - criterion: "documentation_quality"
          status: "pass"
          evidence: "Comprehensive documentation"
        
        - criterion: "api_quality"
          status: "pass"
          evidence: "RESTful API with OpenAPI spec"
    
    - section: "financial_assessment"
      criteria:
        - criterion: "financial_stability"
          status: "pass"
          evidence: "Well-funded, positive cash flow"
        
        - criterion: "pricing_transparency"
          status: "pass"
          evidence: "Clear pricing structure"
        
        - criterion: "contract_terms"
          status: "pass"
          evidence: "Standard terms, negotiable"
  
  overall_assessment:
    status: "approved"
    risk_level: "medium"
    conditions:
      - "Execute DPA before engagement"
      - "Quarterly security reviews required"
      - "Annual SOC2 report required"
  
  recommendation: "Proceed with engagement"
  next_review: "2027-06-04"
```

## Example 2: Vendor Scorecard

### Context

**When to Use**: Monitoring vendor performance over time

**Goal**: Track vendor performance against SLAs and requirements

### Implementation

```yaml
vendor_scorecard:
  vendor: "AI Model Provider"
  period: "Q2 2026"
  last_updated: "2026-06-04"
  
  metrics:
    - metric: "uptime"
      target: "99.9%"
      actual: "99.95%"
      status: "pass"
      trend: "stable"
    
    - metric: "latency_p95"
      target: "< 200ms"
      actual: "150ms"
      status: "pass"
      trend: "improving"
    
    - metric: "error_rate"
      target: "< 0.1%"
      actual: "0.05%"
      status: "pass"
      trend: "stable"
    
    - metric: "support_response_time"
      target: "< 4 hours"
      actual: "2 hours"
      status: "pass"
      trend: "improving"
    
    - metric: "security_incidents"
      target: "0"
      actual: "0"
      status: "pass"
      trend: "stable"
    
    - metric: "compliance_status"
      target: "compliant"
      actual: "compliant"
      status: "pass"
      trend: "stable"
  
  overall_score: 95
  rating: "excellent"
  
  issues:
    - issue: "Minor latency spike on 2026-05-15"
      severity: "low"
      resolution: "Resolved within 2 hours"
      impact: "Minimal"
  
  recommendations:
    - "Continue current engagement"
    - "Request quarterly security reviews"
    - "Negotiate volume discount"
  
  next_review: "2026-09-04"
```

## Example 3: DPA Checklist

### Context

**When to Use**: Ensuring DPA requirements are met

**Goal**: Verify Data Processing Agreement compliance

### Implementation

```yaml
dpa_checklist:
  vendor: "AI Model Provider"
  dpa_date: "2026-01-01"
  review_date: "2026-06-04"
  
  requirements:
    - requirement: "data_processing_purpose"
      status: "met"
      evidence: "Section 2.1 of DPA"
    
    - requirement: "data_categories"
      status: "met"
      evidence: "Section 2.2 of DPA"
    
    - requirement: "data_subjects"
      status: "met"
      evidence: "Section 2.3 of DPA"
    
    - requirement: "processing_duration"
      status: "met"
      evidence: "Section 2.4 of DPA"
    
    - requirement: "subprocessor_approval"
      status: "met"
      evidence: "Section 3.1 of DPA"
    
    - requirement: "security_measures"
      status: "met"
      evidence: "Section 4.1 of DPA"
    
    - requirement: "data_subject_rights"
      status: "met"
      evidence: "Section 5.1 of DPA"
    
    - requirement: "breach_notification"
      status: "met"
      evidence: "Section 6.1 of DPA - 72 hours"
    
    - requirement: "data_return_deletion"
      status: "met"
      evidence: "Section 7.1 of DPA"
    
    - requirement: "audit_rights"
      status: "met"
      evidence: "Section 8.1 of DPA"
  
  overall_status: "compliant"
  next_review: "2027-01-01"
```

## Example Summary

| Example | Complexity | Time Required | Key Components |
|---------|------------|---------------|----------------|
| Vendor Assessment | High | 4 hours | Security, compliance, operations |
| Vendor Scorecard | Medium | 2 hours | Metrics, trends, recommendations |
| DPA Checklist | Low | 1 hour | Requirements, evidence, status |
