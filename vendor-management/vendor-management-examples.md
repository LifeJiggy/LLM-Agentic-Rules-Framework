# Vendor Management Examples for AI/LLM Systems

## Overview

This guide provides practical examples of vendor assessment templates, DPA checklists, SLA monitoring, and vendor scorecards with YAML/JSON configurations. These examples can be adapted for your organization's specific needs.

---

## 1. Vendor Assessment Templates

### 1.1 Vendor Evaluation Scorecard (YAML)

```yaml
vendor_evaluation_scorecard:
  metadata:
    vendor_name: "OpenAI"
    evaluation_date: "2026-07-24"
    evaluator: "AI Platform Team"
    evaluation_type: "Annual Review"
  
  dimensions:
    - name: "Technical Capability"
      weight: 0.30
      criteria:
        - name: "Model Performance"
          weight: 0.10
          score: 9
          max_score: 10
          evidence: "GPT-4 benchmark results exceed requirements"
          notes: "Consistent performance across test cases"
        
        - name: "API Reliability"
          weight: 0.08
          score: 8
          max_score: 10
          evidence: "99.95% uptime in last 12 months"
          notes: "Minor incidents handled well"
        
        - name: "Scalability"
          weight: 0.07
          score: 8
          max_score: 10
          evidence: "Successfully handles 10x load spikes"
          notes: "Auto-scaling works as expected"
        
        - name: "Integration Ease"
          weight: 0.05
          score: 9
          max_score: 10
          evidence: "Excellent SDK and documentation"
          notes: "Quick integration timeline"
      
      sub_score: 8.5
      sub_weighted_score: 2.55
    
    - name: "Security & Compliance"
      weight: 0.25
      criteria:
        - name: "Certifications"
          weight: 0.08
          score: 9
          max_score: 10
          evidence: "SOC 2 Type II, ISO 27001 certified"
          notes: "Certifications current and valid"
        
        - name: "Data Protection"
          weight: 0.07
          score: 8
          max_score: 10
          evidence: "Strong encryption and access controls"
          notes: "DPA terms acceptable"
        
        - name: "Compliance Coverage"
          weight: 0.05
          score: 8
          max_score: 10
          evidence: "GDPR, CCPA compliant"
          notes: "HIPAA available with BAA"
        
        - name: "Incident Response"
          weight: 0.05
          score: 8
          max_score: 10
          evidence: "Clear incident response procedures"
          notes: "72-hour breach notification"
      
      sub_score: 8.25
      sub_weighted_score: 2.06
    
    - name: "Cost & Value"
      weight: 0.20
      criteria:
        - name: "Pricing Model"
          weight: 0.08
          score: 7
          max_score: 10
          evidence: "Usage-based pricing, competitive rates"
          notes: "Volume discounts available"
        
        - name: "Total Cost of Ownership"
          weight: 0.07
          score: 7
          max_score: 10
          evidence: "Moderate integration costs"
          notes: "Ongoing optimization opportunities"
        
        - name: "Value for Money"
          weight: 0.05
          score: 8
          max_score: 10
          evidence: "Strong ROI demonstrated"
          notes: "Value exceeds cost"
      
      sub_score: 7.33
      sub_weighted_score: 1.47
    
    - name: "Vendor Reliability"
      weight: 0.15
      criteria:
        - name: "Financial Stability"
          weight: 0.05
          score: 9
          max_score: 10
          evidence: "Strong funding and revenue growth"
          notes: "Market leader position"
        
        - name: "Market Position"
          weight: 0.05
          score: 9
          max_score: 10
          evidence: "Industry leader in AI/LLM"
          notes: "Strong competitive position"
        
        - name: "Customer References"
          weight: 0.05
          score: 8
          max_score: 10
          evidence: "Strong reference customers"
          notes: "Positive customer feedback"
      
      sub_score: 8.67
      sub_weighted_score: 1.30
    
    - name: "Support & Service"
      weight: 0.10
      criteria:
        - name: "Support Quality"
          weight: 0.04
          score: 8
          max_score: 10
          evidence: "24/7 support available"
          notes: "Responsive and knowledgeable"
        
        - name: "Documentation"
          weight: 0.03
          score: 9
          max_score: 10
          evidence: "Comprehensive API documentation"
          notes: "Regular updates"
        
        - name: "Training"
          weight: 0.03
          score: 7
          max_score: 10
          evidence: "Online resources and webinars"
          notes: "Could improve hands-on training"
      
      sub_score: 8.00
      sub_weighted_score: 0.80
  
  overall:
    total_weighted_score: 8.18
    rating: "Excellent"
    recommendation: "Approve continued partnership"
    
    strengths:
      - "Industry-leading model performance"
      - "Strong security and compliance posture"
      - "Excellent documentation and support"
      - "Reliable service delivery"
    
    areas_for_improvement:
      - "Pricing optimization opportunities"
      - "Enhanced training programs"
      - "More flexible contract terms"
    
    action_items:
      - action: "Negotiate volume discount"
        owner: "Procurement"
        deadline: "2026-08-15"
        priority: "High"
      
      - action: "Schedule technical deep-dive"
        owner: "Engineering"
        deadline: "2026-08-01"
        priority: "Medium"
      
      - action: "Review DPA terms"
        owner: "Legal"
        deadline: "2026-07-31"
        priority: "High"
  
  approval:
    evaluator: "Jane Smith"
    evaluator_date: "2026-07-24"
    security_approver: "John Doe"
    security_approver_date: "2026-07-25"
    executive_approver: "Sarah Johnson"
    executive_approver_date: "2026-07-26"
```

### 1.2 Vendor Assessment Questionnaire (JSON)

```json
{
  "vendor_assessment_questionnaire": {
    "metadata": {
      "vendor_name": "Anthropic",
      "assessment_date": "2026-07-24",
      "assessor": "Security Team",
      "assessment_type": "Initial Evaluation"
    },
    "sections": {
      "company_information": {
        "questions": [
          {
            "id": "CI-001",
            "question": "What is your company's founding date?",
            "answer": "2021",
            "rating": "acceptable",
            "notes": "Young but well-funded company"
          },
          {
            "id": "CI-002",
            "question": "How many employees do you have?",
            "answer": "500+",
            "rating": "good",
            "notes": "Adequate size for support"
          },
          {
            "id": "CI-003",
            "question": "What is your funding status?",
            "answer": "Series C, $2B+ raised",
            "rating": "excellent",
            "notes": "Strong financial backing"
          }
        ]
      },
      "technical_capabilities": {
        "questions": [
          {
            "id": "TC-001",
            "question": "What AI models do you offer?",
            "answer": "Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku",
            "rating": "excellent",
            "notes": "Multiple model tiers for different use cases"
          },
          {
            "id": "TC-002",
            "question": "What is your API rate limit?",
            "answer": "Varies by model, up to 10,000 RPM",
            "rating": "good",
            "notes": "Adequate for most use cases"
          },
          {
            "id": "TC-003",
            "question": "Do you offer fine-tuning capabilities?",
            "answer": "Yes, with enterprise plan",
            "rating": "good",
            "notes": "Available for custom use cases"
          }
        ]
      },
      "security_compliance": {
        "questions": [
          {
            "id": "SC-001",
            "question": "What security certifications do you hold?",
            "answer": "SOC 2 Type II, ISO 27001",
            "rating": "excellent",
            "notes": "Industry-standard certifications"
          },
          {
            "id": "SC-002",
            "question": "Do you conduct regular penetration testing?",
            "answer": "Yes, quarterly by third parties",
            "rating": "excellent",
            "notes": "Regular testing documented"
          },
          {
            "id": "SC-003",
            "question": "How do you handle data encryption?",
            "answer": "AES-256 at rest, TLS 1.3 in transit",
            "rating": "excellent",
            "notes": "Strong encryption standards"
          }
        ]
      },
      "data_protection": {
        "questions": [
          {
            "id": "DP-001",
            "question": "Do you offer a Data Processing Agreement?",
            "answer": "Yes, comprehensive DPA available",
            "rating": "excellent",
            "notes": "GDPR-compliant DPA"
          },
          {
            "id": "DP-002",
            "question": "Where is data processed and stored?",
            "answer": "US and EU data centers",
            "rating": "good",
            "notes": "Data residency options available"
          },
          {
            "id": "DP-003",
            "question": "Do you use customer data for model training?",
            "answer": "No, with enterprise agreement",
            "rating": "excellent",
            "notes": "Clear training prohibition"
          }
        ]
      },
      "support_service": {
        "questions": [
          {
            "id": "SS-001",
            "question": "What support options do you offer?",
            "answer": "24/7 email, chat, and phone support",
            "rating": "good",
            "notes": "Multiple support channels"
          },
          {
            "id": "SS-002",
            "question": "What is your average response time?",
            "answer": "< 1 hour for critical issues",
            "rating": "good",
            "notes": "Meets our requirements"
          },
          {
            "id": "SS-003",
            "question": "Do you offer dedicated account management?",
            "answer": "Yes, for enterprise customers",
            "rating": "good",
            "notes": "Available at our tier"
          }
        ]
      }
    },
    "overall_assessment": {
      "total_score": 8.5,
      "rating": "Excellent",
      "recommendation": "Approve with conditions",
      "conditions": [
        "Execute DPA before data sharing",
        "Verify SOC 2 report within 30 days",
        "Establish dedicated account manager"
      ]
    }
  }
}
```

---

## 2. DPA Checklists

### 2.1 DPA Compliance Checklist (YAML)

```yaml
dpa_compliance_checklist:
  metadata:
    vendor_name: "Google Cloud AI Platform"
    dpa_version: "2026-01"
    review_date: "2026-07-24"
    reviewer: "Legal Team"
  
  general_provisions:
    - id: "GP-001"
      clause: "Scope of Processing"
      requirement: "Clear definition of processing scope"
      status: "Compliant"
      evidence: "Section 2.1 defines processing scope"
      notes: "Scope matches our requirements"
    
    - id: "GP-002"
      clause: "Processing Purpose"
      requirement: "Limited to specified purposes"
      status: "Compliant"
      evidence: "Section 2.2 limits purposes"
      notes: "No secondary use permitted"
    
    - id: "GP-003"
      clause: "Data Categories"
      requirement: "Specific data categories defined"
      status: "Compliant"
      evidence: "Section 2.3 lists data categories"
      notes: "Categories clearly defined"
    
    - id: "GP-004"
      clause: "Data Subjects"
      requirement: "Data subjects identified"
      status: "Compliant"
      evidence: "Section 2.4 identifies data subjects"
      notes: "Categories clearly defined"
  
  data_subject_rights:
    - id: "DSR-001"
      clause: "Right of Access"
      requirement: "Support for data subject access requests"
      status: "Compliant"
      evidence: "Section 4.1 supports access requests"
      notes: "Clear process defined"
    
    - id: "DSR-002"
      clause: "Right of Rectification"
      requirement: "Support for data correction"
      status: "Compliant"
      evidence: "Section 4.2 supports rectification"
      notes: "Process documented"
    
    - id: "DSR-003"
      clause: "Right of Erasure"
      requirement: "Support for data deletion"
      status: "Compliant"
      evidence: "Section 4.3 supports erasure"
      notes: "Deletion process defined"
    
    - id: "DSR-004"
      clause: "Right to Data Portability"
      requirement: "Support for data export"
      status: "Compliant"
      evidence: "Section 4.4 supports portability"
      notes: "Export formats available"
    
    - id: "DSR-005"
      clause: "Right to Object"
      requirement: "Support for processing objection"
      status: "Compliant"
      evidence: "Section 4.5 supports objection"
      notes: "Objection process defined"
  
  security_measures:
    - id: "SM-001"
      clause: "Encryption at Rest"
      requirement: "Data encrypted at rest"
      status: "Compliant"
      evidence: "Section 5.1 AES-256 encryption"
      notes: "Industry-standard encryption"
    
    - id: "SM-002"
      clause: "Encryption in Transit"
      requirement: "Data encrypted in transit"
      status: "Compliant"
      evidence: "Section 5.2 TLS 1.3"
      notes: "Strong transit encryption"
    
    - id: "SM-003"
      clause: "Access Controls"
      requirement: "Role-based access controls"
      status: "Compliant"
      evidence: "Section 5.3 RBAC implemented"
      notes: "Granular access controls"
    
    - id: "SM-004"
      clause: "Audit Logging"
      requirement: "Comprehensive audit logging"
      status: "Compliant"
      evidence: "Section 5.4 audit logs enabled"
      notes: "Logs retained for 12 months"
    
    - id: "SM-005"
      clause: "Vulnerability Management"
      requirement: "Regular vulnerability scanning"
      status: "Compliant"
      evidence: "Section 5.5 quarterly scanning"
      notes: "Vulnerabilities remediated timely"
    
    - id: "SM-006"
      clause: "Incident Response"
      requirement: "Incident response plan"
      status: "Compliant"
      evidence: "Section 5.6 IR plan documented"
      notes: "Plan tested annually"
  
  sub_processor_management:
    - id: "SP-001"
      clause: "Sub-processor List"
      requirement: "List of sub-processors provided"
      status: "Compliant"
      evidence: "Appendix A lists sub-processors"
      notes: "List updated quarterly"
    
    - id: "SP-002"
      clause: "Prior Notification"
      requirement: "Notification before sub-processor changes"
      status: "Compliant"
      evidence: "Section 6.1 30-day notice"
      notes: "Email notification required"
    
    - id: "SP-003"
      clause: "Objection Right"
      requirement: "Right to object to sub-processors"
      status: "Compliant"
      evidence: "Section 6.2 objection process"
      notes: "30-day objection window"
    
    - id: "SP-004"
      clause: "Sub-processor Obligations"
      requirement: "Binding obligations on sub-processors"
      status: "Compliant"
      evidence: "Section 6.3 contractual obligations"
      notes: "Same DPA terms apply"
  
  ai_specific:
    - id: "AI-001"
      clause: "AI Training Prohibition"
      requirement: "Prohibition on using customer data for training"
      status: "Compliant"
      evidence: "Section 7.1 explicit prohibition"
      notes: "Enterprise agreement required"
    
    - id: "AI-002"
      clause: "Model Output Ownership"
      requirement: "Clarification of AI output ownership"
      status: "Compliant"
      evidence: "Section 7.2 customer owns outputs"
      notes: "Clear ownership terms"
    
    - id: "AI-003"
      clause: "AI Bias Requirements"
      requirement: "Bias testing and fairness requirements"
      status: "Partially Compliant"
      evidence: "Section 7.3 bias testing available"
      notes: "Requires additional requirements"
    
    - id: "AI-004"
      clause: "AI Safety Requirements"
      requirement: "Safety testing and content filtering"
      status: "Compliant"
      evidence: "Section 7.4 safety measures implemented"
      notes: "Content filtering active"
  
  audit_rights:
    - id: "AR-001"
      clause: "Audit Frequency"
      requirement: "Annual audit right"
      status: "Compliant"
      evidence: "Section 8.1 annual audits permitted"
      notes: "30-day notice required"
    
    - id: "AR-002"
      clause: "Audit Scope"
      requirement: "Comprehensive audit scope"
      status: "Compliant"
      evidence: "Section 8.2 scope defined"
      notes: "Includes security and compliance"
    
    - id: "AR-003"
      clause: "Audit Cost"
      requirement: "Clear cost allocation"
      status: "Compliant"
      evidence: "Section 8.3 cost allocation"
      notes: "Shared cost model"
  
  data_return_deletion:
    - id: "DR-001"
      clause: "Data Return"
      requirement: "Data return upon termination"
      status: "Compliant"
      evidence: "Section 9.1 data return process"
      notes: "30-day return window"
    
    - id: "DR-002"
      clause: "Data Deletion"
      requirement: "Data deletion upon termination"
      status: "Compliant"
      evidence: "Section 9.2 deletion process"
      notes: "60-day deletion timeline"
    
    - id: "DR-003"
      clause: "Destruction Certificate"
      requirement: "Certificate of destruction"
      status: "Compliant"
      evidence: "Section 9.3 destruction certificate"
      notes: "Written confirmation provided"
  
  breach_notification:
    - id: "BN-001"
      clause: "Notification Timeline"
      requirement: "72-hour breach notification"
      status: "Compliant"
      evidence: "Section 10.1 72-hour notification"
      notes: "Email notification required"
    
    - id: "BN-002"
      clause: "Breach Details"
      requirement: "Comprehensive breach information"
      status: "Compliant"
      evidence: "Section 10.2 details specified"
      notes: "Includes impact assessment"
    
    - id: "BN-003"
      clause: "Remediation"
      requirement: "Remediation measures"
      status: "Compliant"
      evidence: "Section 10.3 remediation plan"
      notes: "Corrective actions documented"
  
  overall_assessment:
    compliance_score: 95
    status: "Compliant"
    gaps: []
    recommendations: [
      "Enhance AI bias testing requirements",
      "Add specific performance metrics",
      "Include more detailed incident response procedures"
    ]
  
  approval:
    reviewer: "Legal Team"
    review_date: "2026-07-24"
    approval_status: "Approved"
    next_review_date: "2027-07-24"
```

---

## 3. SLA Monitoring Examples

### 3.1 SLA Monitoring Dashboard (YAML)

```yaml
sla_monitoring_dashboard:
  metadata:
    vendor_name: "Azure OpenAI Service"
    monitoring_period: "2026-06-01 to 2026-06-30"
    report_date: "2026-07-01"
    owner: "Operations Team"
  
  performance_metrics:
    availability:
      target: 99.9
      actual: 99.97
      status: "Met"
      measurement_method: "Synthetic monitoring"
      downtime_minutes: 13.2
      incidents: 2
      details:
        - date: "2026-06-15"
          duration: "8 minutes"
          cause: "Scheduled maintenance"
          impact: "Minimal"
        - date: "2026-06-22"
          duration: "5.2 minutes"
          cause: "Network issue"
          impact: "Minimal"
    
    latency:
      target_p95: 500
      actual_p95: 387
      status: "Met"
      measurement_method: "API monitoring"
      p50: 245
      p99: 892
      trend: "Stable"
    
    throughput:
      target_rps: 1000
      actual_rps: 1250
      status: "Met"
      measurement_method: "API monitoring"
      peak_rps: 1850
      average_rps: 980
    
    error_rate:
      target: 0.1
      actual: 0.03
      status: "Met"
      measurement_method: "API monitoring"
      error_types:
        server_errors: 0.01
        timeout_errors: 0.01
        rate_limit_errors: 0.01
    
    accuracy:
      target: 95
      actual: 96.8
      status: "Met"
      measurement_method: "Automated testing"
      test_cases: 10000
      passed: 9680
      failed: 320
  
  support_metrics:
    response_time:
      target_critical: 60
      actual_critical: 45
      target_high: 240
      actual_high: 180
      target_medium: 480
      actual_medium: 420
      status: "Met"
    
    resolution_time:
      target_critical: 240
      actual_critical: 180
      target_high: 1440
      actual_high: 1200
      target_medium: 4320
      actual_medium: 3600
      status: "Met"
    
    tickets:
      total: 24
      critical: 2
      high: 8
      medium: 14
      satisfaction_rating: 4.6
  
  compliance_metrics:
    audit_completion:
      target: 100
      actual: 100
      status: "Met"
    
    certification_maintenance:
      soc2_type2: "Current"
      iso27001: "Current"
      gdpr: "Compliant"
      hipaa: "N/A"
      status: "Met"
  
  cost_metrics:
    budget: 50000
    actual: 47500
    variance: -5
    status: "Under Budget"
    cost_per_request: 0.0038
    optimization_opportunities:
      - "Implement caching to reduce API calls"
      - "Optimize prompt engineering"
      - "Right-size model selection"
  
  sla_compliance_summary:
    overall_compliance: 100
    metrics_met: 15
    metrics_total: 15
    breaches: 0
    credits_earned: 0
  
  alerts_and_incidents:
    alerts:
      - date: "2026-06-15"
        type: "Scheduled Maintenance"
        severity: "Low"
        status: "Resolved"
        impact: "Minimal"
      - date: "2026-06-22"
        type: "Network Issue"
        severity: "Low"
        status: "Resolved"
        impact: "Minimal"
    
    incidents:
      - date: "2026-06-15"
        type: "Service Degradation"
        duration: "8 minutes"
        impact: "Minimal"
        root_cause: "Scheduled maintenance"
        resolution: "Completed as planned"
        prevention: "N/A"
  
  recommendations:
    - "Continue current performance level"
      priority: "Low"
      owner: "Operations Team"
      deadline: "Ongoing"
    
    - "Implement caching optimization"
      priority: "Medium"
      owner: "Engineering Team"
      deadline: "2026-08-01"
    
    - "Schedule quarterly performance review"
      priority: "Low"
      owner: "Operations Team"
      deadline: "2026-10-01"
  
  approval:
    report_owner: "Operations Team"
    report_date: "2026-07-01"
    review_status: "Approved"
    next_review_date: "2026-08-01"
```

### 3.2 SLA Breach Report (JSON)

```json
{
  "sla_breach_report": {
    "metadata": {
      "vendor_name": "AI Vendor X",
      "breach_date": "2026-06-22",
      "report_date": "2026-06-23",
      "severity": "High",
      "owner": "Operations Team"
    },
    "breach_details": {
      "metric": "Availability",
      "target": 99.9,
      "actual": 98.5,
      "breach_duration": "45 minutes",
      "impact": "Service unavailable for 45 minutes"
    },
    "timeline": {
      "detection": "2026-06-22 14:30 UTC",
      "notification": "2026-06-22 14:35 UTC",
      "investigation": "2026-06-22 14:40 UTC",
      "resolution": "2026-06-22 15:15 UTC",
      "post_mortem": "2026-06-24 10:00 UTC"
    },
    "root_cause": {
      "description": "Database connection pool exhaustion",
      "contributing_factors": [
        "Unexpected traffic spike",
        "Connection pool size insufficient",
        "Health check not detecting issue"
      ]
    },
    "impact_assessment": {
      "affected_users": 500,
      "affected_requests": 15000,
      "revenue_impact": 5000,
      "reputation_impact": "Moderate"
    },
    "remediation": {
      "immediate": [
        "Increased connection pool size",
        "Implemented circuit breaker"
      ],
      "long_term": [
        "Auto-scaling for connection pools",
        "Enhanced monitoring",
        "Load testing with traffic spikes"
      ]
    },
    "sla_credit": {
      "eligible": true,
      "amount": 2500,
      "percentage": 5,
      "period": "2026-06"
    },
    "lessons_learned": [
      "Improve traffic spike detection",
      "Enhance connection pool monitoring",
      "Implement better health checks"
    ],
    "prevention_actions": [
      {
        "action": "Implement auto-scaling",
        "owner": "Engineering Team",
        "deadline": "2026-07-15",
        "status": "In Progress"
      },
      {
        "action": "Enhance monitoring",
        "owner": "Operations Team",
        "deadline": "2026-07-10",
        "status": "Completed"
      }
    ]
  }
}
```

---

## 4. Vendor Scorecards

### 4.1 Quarterly Business Review Scorecard (YAML)

```yaml
quarterly_business_review_scorecard:
  metadata:
    vendor_name: "Anthropic"
    review_period: "Q2 2026"
    review_date: "2026-07-15"
    participants:
      - "Vendor: Account Manager"
      - "Customer: VP Engineering, AI Lead"
  
  executive_summary:
    overall_relationship: "Strong"
    key_achievements:
      - "Successfully launched new AI feature"
      - "Exceeded performance targets"
      - "Strong partnership development"
    key_concerns:
      - "Pricing increases expected"
      - "Need for more customization options"
    strategic_alignment: "High"
  
  performance_review:
    sla_compliance:
      availability: 99.98
      latency: 99.5
      throughput: 100
      accuracy: 98.5
      support_response: 100
      overall: 99.6
    
    business_value:
      revenue_impact: "Positive"
      cost_savings: "15% reduction in development costs"
      time_to_market: "30% faster feature delivery"
      competitive_advantage: "Strong differentiation"
    
    innovation:
      new_features: 5
      roadmap_alignment: "High"
      technical_leadership: "Strong"
      partnership_value: "Growing"
  
  cost_analysis:
    budget_vs_actual:
      budget: 200000
      actual: 185000
      variance: -7.5
      status: "Under Budget"
    
    cost_optimization:
      savings_identified: 15000
      savings_realized: 15000
      optimization_areas:
        - "Implemented caching"
        - "Optimized prompts"
        - "Right-sized models"
    
    forecast:
      next_quarter: 190000
      next_year: 750000
      assumptions: [
        "10% usage growth",
        "New feature launch",
        "Price stability"
      ]
  
  relationship_assessment:
    communication:
      score: 9
      feedback: "Excellent communication and transparency"
      improvements: "Continue regular check-ins"
    
    support:
      score: 8
      feedback: "Responsive and knowledgeable support"
      improvements: "Faster escalation for critical issues"
    
    partnership:
      score: 9
      feedback: "Strong strategic alignment"
      improvements: "More joint innovation initiatives"
    
    trust:
      score: 9
      feedback: "High trust and reliability"
      improvements: "Maintain transparency"
  
  risk_assessment:
    risks:
      - name: "Pricing Increase"
        likelihood: "High"
        impact: "Medium"
        mitigation: "Negotiate long-term contract"
      
      - name: "Service Disruption"
        likelihood: "Low"
        impact: "High"
        mitigation: "Maintain fallback options"
      
      - name: "Regulatory Changes"
        likelihood: "Medium"
        impact: "Medium"
        mitigation: "Monitor compliance requirements"
    
    overall_risk: "Low"
    risk_trend: "Stable"
  
  strategic_alignment:
    business_goals_alignment: "High"
    technology_roadmap_alignment: "High"
    innovation_partnership: "Strong"
    market_position: "Leader"
  
  action_items:
    - action: "Negotiate volume discount"
      owner: "Procurement"
      deadline: "2026-08-15"
      priority: "High"
      status: "In Progress"
    
    - action: "Joint innovation workshop"
      owner: "AI Team"
      deadline: "2026-08-01"
      priority: "Medium"
      status: "Planned"
    
    - action: "Review contract terms"
      owner: "Legal"
      deadline: "2026-08-30"
      priority: "High"
      status: "Planned"
    
    - action: "Performance optimization"
      owner: "Engineering"
      deadline: "2026-07-31"
      priority: "Medium"
      status: "In Progress"
  
  next_steps:
    - "Schedule follow-up meeting"
    - "Execute action items"
    - "Review progress monthly"
    - "Plan Q3 review"
  
  approval:
    reviewer: "VP Engineering"
    review_date: "2026-07-15"
    approval_status: "Approved"
    next_review_date: "2026-10-15"
```

### 4.2 Vendor Comparison Scorecard (JSON)

```json
{
  "vendor_comparison_scorecard": {
    "metadata": {
      "comparison_date": "2026-07-24",
      "purpose": "AI Platform Selection",
      "evaluator": "AI Team"
    },
    "vendors": [
      {
        "name": "OpenAI",
        "scores": {
          "technical_capability": 9.0,
          "security_compliance": 8.5,
          "cost_value": 7.5,
          "vendor_reliability": 9.0,
          "support_service": 8.0
        },
        "overall_score": 8.5,
        "recommendation": "Strong Candidate"
      },
      {
        "name": "Anthropic",
        "scores": {
          "technical_capability": 8.5,
          "security_compliance": 9.0,
          "cost_value": 7.0,
          "vendor_reliability": 8.0,
          "support_service": 8.5
        },
        "overall_score": 8.3,
        "recommendation": "Strong Candidate"
      },
      {
        "name": "Google Cloud AI",
        "scores": {
          "technical_capability": 8.0,
          "security_compliance": 9.0,
          "cost_value": 8.0,
          "vendor_reliability": 9.0,
          "support_service": 7.5
        },
        "overall_score": 8.2,
        "recommendation": "Good Candidate"
      }
    ],
    "comparison_matrix": {
      "dimensions": [
        {
          "name": "Technical Capability",
          "weight": 0.30,
          "criteria": [
            "Model Performance",
            "API Reliability",
            "Scalability",
            "Integration Ease"
          ]
        },
        {
          "name": "Security & Compliance",
          "weight": 0.25,
          "criteria": [
            "Certifications",
            "Data Protection",
            "Compliance Coverage"
          ]
        },
        {
          "name": "Cost & Value",
          "weight": 0.20,
          "criteria": [
            "Pricing Model",
            "Total Cost of Ownership"
          ]
        },
        {
          "name": "Vendor Reliability",
          "weight": 0.15,
          "criteria": [
            "Financial Stability",
            "Market Position"
          ]
        },
        {
          "name": "Support & Service",
          "weight": 0.10,
          "criteria": [
            "Support Quality",
            "Documentation"
          ]
        }
      ]
    },
    "recommendation": {
      "primary_choice": "OpenAI",
      "secondary_choice": "Anthropic",
      "rationale": "OpenAI leads in technical capability and reliability; Anthropic excels in security and support",
      "conditions": [
        "Negotiate volume discounts",
        "Establish dedicated support",
        "Execute comprehensive DPA"
      ]
    }
  }
}
```

---

## 5. Vendor Risk Register

### 5.1 Risk Register (YAML)

```yaml
vendor_risk_register:
  metadata:
    vendor_name: "AI Platform Vendor"
    last_updated: "2026-07-24"
    owner: "Risk Management Team"
  
  risks:
    - id: "VR-001"
      name: "Service Disruption"
      category: "Operational"
      description: "Vendor experiences significant service outage"
      likelihood: "Low"
      impact: "High"
      risk_score: "Medium"
      mitigation:
        - "Maintain fallback vendor"
        - "Implement circuit breakers"
        - "Regular disaster recovery testing"
      owner: "Operations Team"
      status: "Active"
      last_reviewed: "2026-07-24"
    
    - id: "VR-002"
      name: "Data Breach"
      category: "Security"
      description: "Vendor experiences data breach affecting our data"
      likelihood: "Low"
      impact: "Critical"
      risk_score: "High"
      mitigation:
        - "Encryption at rest and in transit"
        - "Regular security audits"
        - "Incident response plan"
      owner: "Security Team"
      status: "Active"
      last_reviewed: "2026-07-24"
    
    - id: "VR-003"
      name: "Pricing Increase"
      category: "Financial"
      description: "Vendor significantly increases pricing"
      likelihood: "High"
      impact: "Medium"
      risk_score: "Medium"
      mitigation:
        - "Long-term contract negotiation"
        - "Volume discount agreements"
        - "Alternative vendor evaluation"
      owner: "Procurement Team"
      status: "Active"
      last_reviewed: "2026-07-24"
    
    - id: "VR-004"
      name: "Regulatory Non-Compliance"
      category: "Compliance"
      description: "Vendor fails to meet regulatory requirements"
      likelihood: "Low"
      impact: "High"
      risk_score: "Medium"
      mitigation:
        - "Regular compliance audits"
        - "Contractual compliance requirements"
        - "Monitoring regulatory changes"
      owner: "Legal Team"
      status: "Active"
      last_reviewed: "2026-07-24"
    
    - id: "VR-005"
      name: "Vendor Acquisition"
      category: "Strategic"
      description: "Vendor acquired by another company"
      likelihood: "Medium"
      impact: "Medium"
      risk_score: "Medium"
      mitigation:
        - "Monitor vendor financial health"
        - "Maintain alternative vendors"
        - "Contractual change provisions"
      owner: "Strategic Planning"
      status: "Active"
      last_reviewed: "2026-07-24"
    
    - id: "VR-006"
      name: "Model Performance Degradation"
      category: "Technical"
      description: "AI model performance degrades significantly"
      likelihood: "Medium"
      impact: "Medium"
      risk_score: "Medium"
      mitigation:
        - "Continuous performance monitoring"
        - "A/B testing capabilities"
        - "Fallback model options"
      owner: "AI Team"
      status: "Active"
      last_reviewed: "2026-07-24"
  
  risk_summary:
    total_risks: 6
    critical: 0
    high: 1
    medium: 5
    low: 0
    overall_risk_level: "Medium"
    risk_trend: "Stable"
  
  review_schedule:
    frequency: "Monthly"
    next_review: "2026-08-24"
    review_owner: "Risk Management Team"
```

---

## 6. Vendor Onboarding Checklist

### 6.1 Onboarding Checklist Template (YAML)

```yaml
vendor_onboarding_checklist:
  metadata:
    vendor_name: "{{vendor_name}}"
    onboarding_date: "{{date}}"
    onboarding_owner: "{{owner_name}}"
    target_completion: "{{target_date}}"
  
  phase_1_contractual:
    - id: "ONB-001"
      task: "Execute Master Service Agreement"
      responsible: "Legal"
      status: "pending"
      due_date: "{{date}}"
      dependencies: []
      notes: ""
    
    - id: "ONB-002"
      task: "Sign Data Processing Agreement"
      responsible: "Legal"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001"]
      notes: ""
    
    - id: "ONB-003"
      task: "Execute Service Level Agreement"
      responsible: "Procurement"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001"]
      notes: ""
    
    - id: "ONB-004"
      task: "Sign Non-Disclosure Agreement"
      responsible: "Legal"
      status: "pending"
      due_date: "{{date}}"
      dependencies: []
      notes: ""
    
    - id: "ONB-005"
      task: "Verify Insurance Coverage"
      responsible: "Procurement"
      status: "pending"
      due_date: "{{date}}"
      dependencies: []
      notes: ""
  
  phase_2_security:
    - id: "ONB-006"
      task: "Complete Security Assessment"
      responsible: "Security"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001"]
      notes: ""
    
    - id: "ONB-007"
      task: "Implement Access Controls"
      responsible: "Security"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-006"]
      notes: ""
    
    - id: "ONB-008"
      task: "Configure Encryption"
      responsible: "Security"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-006"]
      notes: ""
    
    - id: "ONB-009"
      task: "Enable Monitoring"
      responsible: "Operations"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-007"]
      notes: ""
    
    - id: "ONB-010"
      task: "Establish Incident Response Plan"
      responsible: "Security"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-006"]
      notes: ""
  
  phase_3_technical:
    - id: "ONB-011"
      task: "Provision API Credentials"
      responsible: "Engineering"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001", "ONB-006"]
      notes: ""
    
    - id: "ONB-012"
      task: "Define Integration Architecture"
      responsible: "Engineering"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-011"]
      notes: ""
    
    - id: "ONB-013"
      task: "Configure Testing Environment"
      responsible: "Engineering"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-011"]
      notes: ""
    
    - id: "ONB-014"
      task: "Establish Performance Baseline"
      responsible: "Engineering"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-013"]
      notes: ""
    
    - id: "ONB-015"
      task: "Review Documentation"
      responsible: "Engineering"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-011"]
      notes: ""
  
  phase_4_operational:
    - id: "ONB-016"
      task: "Complete Team Training"
      responsible: "Operations"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-012"]
      notes: ""
    
    - id: "ONB-017"
      task: "Document Processes"
      responsible: "Operations"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-016"]
      notes: ""
    
    - id: "ONB-018"
      task: "Define Escalation Procedures"
      responsible: "Operations"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-010"]
      notes: ""
    
    - id: "ONB-019"
      task: "Set Up Cost Tracking"
      responsible: "Finance"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001"]
      notes: ""
    
    - id: "ONB-020"
      task: "Conduct Kickoff Meeting"
      responsible: "Procurement"
      status: "pending"
      due_date: "{{date}}"
      dependencies: ["ONB-001", "ONB-006"]
      notes: ""
  
  completion_status:
    total_tasks: 20
    completed: 0
    in_progress: 0
    pending: 20
    completion_percentage: 0
  
  approval:
    onboarding_owner: "{{name}}"
    date: "{{date}}"
    security_approver: "{{name}}"
    date: "{{date}}"
    executive_approver: "{{name}}"
    date: "{{date}}"
```

---

## 7. Vendor Performance Dashboard

### 7.1 Performance Dashboard Configuration (YAML)

```yaml
vendor_performance_dashboard:
  dashboard_name: "AI Vendor Performance Dashboard"
  refresh_frequency: "Real-time"
  data_sources:
    - "vendor_api_monitoring"
    - "internal_monitoring"
    - "user_feedback"
    - "financial_systems"
  
  widgets:
    - name: "Service Availability"
      type: "gauge"
      metric: "availability_percentage"
      target: 99.9
      thresholds:
        green: 99.9
        yellow: 99.5
        red: 99.0
      time_range: "30 days"
    
    - name: "API Latency"
      type: "line_chart"
      metric: "p95_latency_ms"
      target: 500
      thresholds:
        green: 500
        yellow: 800
        red: 1000
      time_range: "7 days"
    
    - name: "Error Rate"
      type: "line_chart"
      metric: "error_rate_percentage"
      target: 0.1
      thresholds:
        green: 0.1
        yellow: 0.5
        red: 1.0
      time_range: "7 days"
    
    - name: "Throughput"
      type: "line_chart"
      metric: "requests_per_second"
      target: 1000
      thresholds:
        green: 1000
        yellow: 500
        red: 100
      time_range: "7 days"
    
    - name: "Cost Tracking"
      type: "bar_chart"
      metric: "daily_cost"
      target: 1667
      thresholds:
        green: 1667
        yellow: 2000
        red: 2500
      time_range: "30 days"
    
    - name: "SLA Compliance"
      type: "pie_chart"
      metric: "sla_compliance_percentage"
      target: 100
      thresholds:
        green: 100
        yellow: 99
        red: 95
      time_range: "Current Month"
    
    - name: "Incident Summary"
      type: "table"
      metrics:
        - "incident_count"
        - "mean_time_to_resolution"
        - "customer_impact"
      time_range: "30 days"
    
    - name: "Vendor Scorecard"
      type: "scorecard"
      dimensions:
        - "Technical Performance"
        - "Support Quality"
        - "Cost Efficiency"
        - "Innovation"
        - "Partnership"
      time_range: "Quarterly"
  
  alerting:
    channels:
      - "email"
      - "slack"
      - "sms"
    rules:
      - name: "Availability Alert"
        condition: "availability < 99.9%"
        severity: "warning"
        recipients: ["ops-team@company.com"]
      
      - name: "Critical Alert"
        condition: "availability < 99.0%"
        severity: "critical"
        recipients: ["ops-team@company.com", "exec-team@company.com"]
      
      - name: "Cost Alert"
        condition: "daily_cost > 2500"
        severity: "warning"
        recipients: ["finance@company.com"]
  
  reporting:
    daily:
      - "availability_summary"
      - "performance_summary"
      - "cost_summary"
    
    weekly:
      - "detailed_performance_report"
      - "trend_analysis"
      - "incident_summary"
    
    monthly:
      - "comprehensive_performance_report"
      - "sla_compliance_report"
      - "cost_optimization_report"
    
    quarterly:
      - "executive_summary"
      - "vendor_scorecard"
      - "strategic_recommendations"
```

---

## Summary

These examples provide practical templates for:

1. **Vendor Assessment**: Comprehensive scorecards and questionnaires
2. **DPA Compliance**: Detailed checklists for data protection
3. **SLA Monitoring**: Dashboards and breach reports
4. **Vendor Scorecards**: Performance and comparison scorecards
5. **Risk Management**: Vendor risk registers
6. **Onboarding**: Comprehensive onboarding checklists
7. **Performance Dashboards**: Real-time monitoring configurations

Use these templates as starting points and customize them for your organization's specific requirements and vendor relationships.
