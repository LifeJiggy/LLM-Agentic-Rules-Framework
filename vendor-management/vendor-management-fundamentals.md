# Vendor Management Fundamentals for AI/LLM Systems

## Overview

Vendor management for AI and LLM systems requires a structured approach that addresses the unique challenges of managing third-party AI providers, model hosting services, and tool integrations. This guide covers the core concepts, lifecycle management, risk assessment, and compliance requirements specific to AI/LLM vendor relationships.

---

## 1. Vendor Lifecycle Management

### 1.1 Lifecycle Phases

The vendor lifecycle for AI/LLM systems consists of four primary phases, each with distinct activities and governance requirements.

```yaml
vendor_lifecycle:
  phases:
    - name: "Selection"
      duration: "2-8 weeks"
      activities:
        - market_research
        - vendor_identification
        - capability_assessment
        - risk_screening
        - shortlist_creation
        - proof_of_concept
        - final_selection
      governance:
        - procurement_approval
        - legal_review
        - security_review
        - privacy_impact_assessment
      deliverables:
        - vendor_evaluation_report
        - risk_assessment_summary
        - selection_rationale

    - name: "Onboarding"
      duration: "1-4 weeks"
      activities:
        - contract_execution
        - dpa_signing
        - technical_integration
        - access_provisioning
        - team_training
        - baseline_measurement
      governance:
        - security_configuration_review
        - access_control_setup
        - monitoring_enablement
        - incident_response_planning
      deliverables:
        - integration_architecture
        - access_control_matrix
        - monitoring_dashboard

    - name: "Monitoring"
      duration: "Ongoing"
      activities:
        - performance_monitoring
        - security_auditing
        - compliance_verification
        - risk_reassessment
        - relationship_management
        - cost_optimization
      governance:
        - quarterly_reviews
        - annual_audits
        - incident_reporting
        - change_management
      deliverables:
        - performance_reports
        - audit_findings
        - risk_register_updates

    - name: "Offboarding"
      duration: "2-8 weeks"
      activities:
        - transition_planning
        - data_migration
        - access_revocation
        - contract_termination
        - final_auditing
        - knowledge_transfer
      governance:
        - data_return_confirmation
        - destruction_certificate
        - final_reconciliation
        - lessons_learned
      deliverables:
        - migration_completion_report
        - data_destruction_certificate
        - relationship_closure_report
```

### 1.2 Vendor Classification

AI/LLM vendors should be classified based on criticality, data sensitivity, and integration complexity.

```yaml
vendor_classification:
  tiers:
    tier_1_critical:
      description: "Core AI/LLM providers with direct model access"
      examples:
        - "OpenAI (GPT models)"
        - "Anthropic (Claude models)"
        - "Google (Gemini models)"
        - "Azure OpenAI Service"
        - "AWS Bedrock"
      requirements:
        - executive_sponsorship
        - quarterly_business_reviews
        - dedicated_account_management
        - enhanced_sla (99.9%+)
        - comprehensive_dpa
        - regular_penetration_testing
        - business_continuity_planning

    tier_2_important:
      description: "Supporting AI services and tools"
      examples:
        - "Vector databases (Pinecone, Weaviate)"
        - "AI monitoring tools"
        - "Model hosting platforms"
        - "Data labeling services"
        - "Prompt engineering tools"
      requirements:
        - project_sponsorship
        - semi_annual_reviews
        - standard_sla (99.5%+)
        - standard_dpa
        - annual_security_assessment

    tier_3_standard:
      description: "Auxiliary services with limited AI impact"
      examples:
        - "Analytics platforms"
        - "Communication tools"
        - "Project management software"
        - "Documentation platforms"
      requirements:
        - team_sponsorship
        - annual_reviews
        - basic_sla (99.0%+)
        - standard_terms
        - periodic_compliance_check

    tier_4_low:
      description: "Minimal impact services"
      examples:
        - "Development utilities"
        - "Testing tools"
        - "Internal productivity apps"
      requirements:
        - basic_contract
        - minimal_sla
        - standard_terms
```

### 1.3 RACI Matrix for Vendor Management

```yaml
raci_matrix:
  activities:
    vendor_selection:
      responsible: "Procurement Team"
      accountable: "VP of Engineering"
      consulted: "Security Team, Legal, Privacy Officer"
      informed: "Executive Leadership"

    contract_negotiation:
      responsible: "Legal Team"
      accountable: "General Counsel"
      consulted: "Procurement, Security, Privacy Officer"
      informed: "Executive Leadership"

    security_review:
      responsible: "Security Team"
      accountable: "CISO"
      consulted: "Privacy Officer, Legal"
      informed: "Executive Leadership"

    technical_integration:
      responsible: "Engineering Team"
      accountable: "CTO"
      consulted: "Security Team, Architecture"
      informed: "Product Management"

    performance_monitoring:
      responsible: "Operations Team"
      accountable: "VP of Operations"
      consulted: "Engineering, Security"
      informed: "Executive Leadership"

    incident_response:
      responsible: "Security Team"
      accountable: "CISO"
      consulted: "Legal, Communications, Executive"
      informed: "All Stakeholders"

    offboarding:
      responsible: "Procurement Team"
      accountable: "VP of Engineering"
      consulted: "Legal, Security, Engineering"
      informed: "Executive Leadership"
```

---

## 2. Risk Assessment Framework

### 2.1 Risk Categories for AI/LLM Vendors

```yaml
risk_categories:
  operational_risk:
    description: "Risks affecting day-to-day operations"
    factors:
      - service_availability
      - performance_reliability
      - support_quality
      - incident_response
      - business_continuity
    measurement:
      - uptime_percentage
      - mean_time_to_recovery
      - support_response_time
      - incident_frequency
      - disaster_recovery_capability

  security_risk:
    description: "Risks to data confidentiality, integrity, and availability"
    factors:
      - data_protection
      - access_controls
      - encryption_standards
      - vulnerability_management
      - penetration_testing
    measurement:
      - security_audit_frequency
      - vulnerability_remediation_time
      - access_control_effectiveness
      - encryption_coverage
      - security_incident_history

  compliance_risk:
    description: "Risks of regulatory and policy non-compliance"
    factors:
      - data_residency
      - privacy_regulations
      - industry_standards
      - contractual_obligations
      - audit_readiness
    measurement:
      - compliance_framework_coverage
      - audit_findings_count
      - remediation_completion_rate
      - regulatory_change_adaptation

  financial_risk:
    description: "Risks affecting financial stability and costs"
    factors:
      - pricing_stability
      - payment_terms
      - liability_coverage
      - insurance_requirements
      - financial_viability
    measurement:
      - cost_variance
      - payment_term_compliance
      - financial_health_score
      - total_cost_of_ownership

  reputational_risk:
    description: "Risks affecting brand and public perception"
    factors:
      - service_quality
      - ethical_ai_practices
      - data_handling_reputation
      - public_incidents
      - customer_satisfaction
    measurement:
      - customer_satisfaction_score
      - public_sentiment_analysis
      - incident_publicity
      - ethical_compliance_score

  technology_risk:
    description: "Risks related to technology maturity and evolution"
    factors:
      - model_performance
      - technology_roadmap
      - innovation_capability
      - vendor_lock_in
      - technology_obsolescence
    measurement:
      - model_accuracy_metrics
      - roadmap_alignment
      - innovation_index
      - portability_assessment
      - technology_lifecycle_stage
```

### 2.2 Risk Assessment Template

```yaml
risk_assessment_template:
  vendor_name: "{{vendor_name}}"
  assessment_date: "{{assessment_date}}"
  assessor: "{{assessor_name}}"
  
  risk_scores:
    operational_risk:
      score: "1-5"
      weight: "0.25"
      factors:
        - name: "Service Availability"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Performance Reliability"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Support Quality"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
    
    security_risk:
      score: "1-5"
      weight: "0.20"
      factors:
        - name: "Data Protection"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Access Controls"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Encryption Standards"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
    
    compliance_risk:
      score: "1-5"
      weight: "0.20"
      factors:
        - name: "Data Residency"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Privacy Regulations"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Audit Readiness"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
    
    financial_risk:
      score: "1-5"
      weight: "0.15"
      factors:
        - name: "Pricing Stability"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Financial Viability"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
    
    reputational_risk:
      score: "1-5"
      weight: "0.10"
      factors:
        - name: "Public Incidents"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Ethical AI Practices"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
    
    technology_risk:
      score: "1-5"
      weight: "0.10"
      factors:
        - name: "Model Performance"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
        - name: "Vendor Lock-in"
          score: "1-5"
          evidence: "evidence_source"
          notes: "additional_notes"
  
  overall_risk_score: "calculated_weighted_average"
  risk_level: "critical|high|medium|low"
  mitigation_recommendations:
    - priority: "P0"
      action: "action_description"
      owner: "responsible_party"
      deadline: "completion_date"
    - priority: "P1"
      action: "action_description"
      owner: "responsible_party"
      deadline: "completion_date"
  
  approval:
    risk_assessor: "name"
    risk_assessor_date: "date"
    security_approver: "name"
    security_approver_date: "date"
    executive_approver: "name"
    executive_approver_date: "date"
```

### 2.3 Risk Scoring Methodology

```yaml
risk_scoring:
  scoring_scale:
    1: "Very Low Risk - Minimal concerns, standard terms acceptable"
    2: "Low Risk - Minor concerns, standard terms with minor modifications"
    3: "Medium Risk - Moderate concerns, enhanced terms required"
    4: "High Risk - Significant concerns, substantial mitigation required"
    5: "Critical Risk - Severe concerns, executive approval required"
  
  risk_level_thresholds:
    critical: "4.0-5.0"
    high: "3.0-3.9"
    medium: "2.0-2.9"
    low: "1.0-1.9"
  
  risk_level_actions:
    critical:
      - executive_approval_required
      - enhanced_monitoring
      - quarterly_reviews
      - dedicated_risk_mitigation_plan
      - potential_vendor_replacement
    
    high:
      - senior_management_approval
      - increased_monitoring
      - semi_annual_reviews
      - risk_mitigation_plan
      - contingency_planning
    
    medium:
      - management_approval
      - regular_monitoring
      - annual_reviews
      - risk_acceptance_or_mitigation
    
    low:
      - standard_approval
      - routine_monitoring
      - periodic_reviews
      - standard_terms
```

---

## 3. Data Processing Agreements (DPAs)

### 3.1 DPA Requirements for AI/LLM Vendors

```yaml
dpa_requirements:
  mandatory_clauses:
    - name: "Data Processing Purpose"
      description: "Clear definition of data processing purposes"
      requirements:
        - specific_purpose_limitation
        - prohibition_on_secondary_use
        - ai_model_training_prohibition
        - data_mining_prohibition
    
    - name: "Data Subject Rights"
      description: "Support for data subject rights under GDPR/CCPA"
      requirements:
        - right_of_access
        - right_of_rectification
        - right_of_erasure
        - right_to_data_portability
        - right_to_object
        - automated_decision_making_opt_out
    
    - name: "Sub-processor Management"
      description: "Control over sub-processor changes"
      requirements:
        - prior_notification
        - objection_right
        - sub_processor_list
        - binding_obligations
    
    - name: "Data Security"
      description: "Security measures for data protection"
      requirements:
        - encryption_at_rest
        - encryption_in_transit
        - access_controls
        - audit_logging
        - vulnerability_management
        - incident_response
    
    - name: "Data Location"
      description: "Data residency and transfer requirements"
      requirements:
        - processing_location
        - data_residency_compliance
        - cross_border_transfer_safeguards
        - standard_contractual_clauses
    
    - name: "Breach Notification"
      description: "Incident reporting requirements"
      requirements:
        - notification_timeline_72_hours
        - breach_details
        - remediation_measures
        - regulatory_notification_support
    
    - name: "Audit Rights"
      description: "Right to audit vendor's data processing"
      requirements:
        - annual_audit_right
        - audit_notice_period
        - audit_scope
        - audit_cost_allocation
    
    - name: "Data Return and Deletion"
      description: "Data handling upon termination"
      requirements:
        - data_return_timeline
        - data_destruction_timeline
        - destruction_certificate
        - backup_deletion

  ai_specific_clauses:
    - name: "AI Model Training Prohibition"
      description: "Prohibition on using customer data for AI training"
      requirements:
        - explicit_prohibition
        - audit_trail
        - technical_safeguards
        - contractual_penalties
    
    - name: "Model Output Ownership"
      description: "Clarification of AI output ownership"
      requirements:
        - customer_ownership_of_outputs
        - license_grants
        - derivative_work_rights
        - intellectual_property_protection
    
    - name: "AI Bias and Fairness"
      description: "Requirements for AI fairness and bias mitigation"
      requirements:
        - bias_testing
        - fairness_metrics
        - transparency_requirements
        - remediation_obligations
    
    - name: "Model Performance Guarantees"
      description: "Performance guarantees for AI models"
      requirements:
        - accuracy_targets
        - latency_requirements
        - availability_guarantees
        - degradation_protocols
    
    - name: "AI Safety and Ethics"
      description: "AI safety and ethical use requirements"
      requirements:
        - harmful_output_prevention
        - content_moderation
        - safety_testing
        - ethical_ai_framework

  additional_provisions:
    - name: "Intellectual Property"
      description: "IP rights and licensing"
      requirements:
        - pre_existing_ip_rights
        - derivative_work_ownership
        - license_grants
        - ip_infringement_indemnification
    
    - name: "Liability and Indemnification"
      description: "Liability allocation and indemnification"
      requirements:
        - liability_cap
        - indemnification_scope
        - insurance_requirements
        - limitation_of_liability
    
    - name: "Termination"
      description: "Termination and transition provisions"
      requirements:
        - termination_for_convenience
        - termination_for_cause
        - transition_assistance
        - data_return_obligations
    
    - name: "Dispute Resolution"
      description: "Dispute resolution mechanisms"
      requirements:
        - negotiation_period
        - mediation
        - arbitration
        - governing_law
```

### 3.2 DPA Checklist

```yaml
dpa_checklist:
  general_provisions:
    - item: "Scope of processing defined"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Processing purposes limited"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Data categories specified"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Data subjects identified"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Processing duration defined"
      status: "pending|approved|rejected"
      notes: ""
  
  data_subject_rights:
    - item: "Right of access supported"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Right of rectification supported"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Right of erasure supported"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Right to data portability supported"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Right to object supported"
      status: "pending|approved|rejected"
      notes: ""
  
  security_measures:
    - item: "Encryption at rest implemented"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Encryption in transit implemented"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Access controls implemented"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Audit logging enabled"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Vulnerability management program"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Incident response plan"
      status: "pending|approved|rejected"
      notes: ""
  
  sub_processor_management:
    - item: "Sub-processor list provided"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Prior notification for changes"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Objection right established"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Sub-processor obligations defined"
      status: "pending|approved|rejected"
      notes: ""
  
  ai_specific:
    - item: "AI training prohibition"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Model output ownership"
      status: "pending|approved|rejected"
      notes: ""
    - item: "AI bias requirements"
      status: "pending|approved|rejected"
      notes: ""
    - item: "AI safety requirements"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Performance guarantees"
      status: "pending|approved|rejected"
      notes: ""
  
  termination:
    - item: "Data return process defined"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Data destruction timeline"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Destruction certificate"
      status: "pending|approved|rejected"
      notes: ""
    - item: "Transition assistance"
      status: "pending|approved|rejected"
      notes: ""
```

---

## 4. SLA Management

### 4.1 SLA Framework for AI/LLM Vendors

```yaml
sla_framework:
  performance_metrics:
    availability:
      description: "Service availability guarantee"
      target: "99.9%"
      measurement_period: "monthly"
      measurement_method: "uptime_monitoring"
      exclusions:
        - scheduled_maintenance
        - force_majeure
        - customer_caused
      remedies:
        - credit_tier_1: "10% monthly_fee for 99.0-99.9% uptime"
        - credit_tier_2: "25% monthly_fee for 95.0-99.0% uptime"
        - credit_tier_3: "50% monthly_fee for 90.0-95.0% uptime"
        - termination_right: "below 90.0% uptime"
    
    latency:
      description: "Response time guarantee"
      target: "p95 < 500ms"
      measurement_period: "daily"
      measurement_method: "synthetic_monitoring"
      thresholds:
        - tier_1: "p95 < 200ms (excellent)"
        - tier_2: "p95 < 500ms (acceptable)"
        - tier_3: "p95 < 1000ms (degraded)"
        - tier_4: "p95 > 1000ms (unacceptable)"
      remedies:
        - warning: "notification at tier_3"
        - escalation: "remediation_plan at tier_4"
        - credit: "5% monthly_fee for persistent tier_4"
    
    throughput:
      description: "Requests per second guarantee"
      target: "1000 RPS"
      measurement_period: "daily"
      measurement_method: "api_monitoring"
      scaling:
        - auto_scaling: "enabled"
        - burst_capacity: "2000 RPS"
        - scaling_time: "< 5 minutes"
      remedies:
        - notification: "at 80% capacity"
        - scaling_action: "at 90% capacity"
        - credit: "10% monthly_fee for missed targets"
    
    accuracy:
      description: "Model accuracy guarantee"
      target: "95% accuracy"
      measurement_period: "weekly"
      measurement_method: "automated_testing"
      metrics:
        - precision: "0.95"
        - recall: "0.95"
        - f1_score: "0.95"
      remedies:
        - investigation: "within 24 hours"
        - remediation: "within 7 days"
        - credit: "15% monthly_fee for persistent issues"
    
    error_rate:
      description: "Error rate guarantee"
      target: "< 0.1%"
      measurement_period: "daily"
      measurement_method: "api_monitoring"
      error_types:
        - server_errors: "5xx"
        - timeout_errors: "> 30 seconds"
        - rate_limit_errors: "429"
      remedies:
        - notification: "at 0.05% error rate"
        - escalation: "at 0.1% error rate"
        - credit: "10% monthly_fee for persistent issues"

  support_metrics:
    response_time:
      description: "Time to first response"
      targets:
        - critical: "1 hour"
        - high: "4 hours"
        - medium: "8 hours"
        - low: "24 hours"
      measurement_method: "ticket_system"
      remedies:
        - breach_notification: "automatic"
        - escalation: "after 2x target"
        - credit: "5% monthly_fee for persistent breaches"
    
    resolution_time:
      description: "Time to resolve issues"
      targets:
        - critical: "4 hours"
        - high: "24 hours"
        - medium: "72 hours"
        - low: "5 business days"
      measurement_method: "ticket_system"
      remedies:
        - escalation: "at 50% of target"
        - executive_briefing: "at 100% of target"
        - credit: "10% monthly_fee for persistent breaches"
    
    escalation_procedure:
      description: "Escalation path for issues"
      levels:
        - level_1: "Support Team"
        - level_2: "Technical Lead"
        - level_3: "Engineering Manager"
        - level_4: "VP of Engineering"
        - level_5: "CTO"
      timing:
        - level_1_to_2: "30 minutes"
        - level_2_to_3: "1 hour"
        - level_3_to_4: "2 hours"
        - level_4_to_5: "4 hours"

  compliance_metrics:
    audit_completion:
      description: "Completion of required audits"
      target: "100% within 30 days"
      measurement_period: "annual"
      measurement_method: "audit_reports"
      remedies:
        - notification: "at 15 days"
        - escalation: "at 25 days"
        - penalty: "5% annual_fee for non-compliance"
    
    certification_maintenance:
      description: "Maintenance of required certifications"
      target: "100% current"
      measurement_period: "continuous"
      measurement_method: "certification_tracking"
      required_certifications:
        - "SOC 2 Type II"
        - "ISO 27001"
        - "GDPR compliance"
        - "HIPAA compliance (if applicable)"
      remedies:
        - notification: "90 days before expiration"
        - escalation: "30 days before expiration"
        - penalty: "10% monthly_fee for lapsed certifications"
```

### 4.2 SLA Monitoring Dashboard

```yaml
monitoring_dashboard:
  real_time_metrics:
    - name: "Service Availability"
      current_value: "99.95%"
      target: "99.9%"
      status: "healthy"
      trend: "stable"
      alert_threshold: "99.5%"
    
    - name: "API Latency (p95)"
      current_value: "350ms"
      target: "< 500ms"
      status: "healthy"
      trend: "improving"
      alert_threshold: "800ms"
    
    - name: "Error Rate"
      current_value: "0.02%"
      target: "< 0.1%"
      status: "healthy"
      trend: "stable"
      alert_threshold: "0.05%"
    
    - name: "Throughput"
      current_value: "750 RPS"
      target: "1000 RPS"
      status: "healthy"
      trend: "stable"
      alert_threshold: "900 RPS"
    
    - name: "Model Accuracy"
      current_value: "96.2%"
      target: "95%"
      status: "healthy"
      trend: "improving"
      alert_threshold: "94%"

  historical_metrics:
    time_range: "30 days"
    granularity: "daily"
    metrics_tracked:
      - availability_trend
      - latency_trend
      - error_rate_trend
      - throughput_trend
      - accuracy_trend

  alerting_rules:
    - name: "Availability Degradation"
      condition: "availability < 99.5%"
      severity: "warning"
      notification: "email, slack"
      escalation: "after 15 minutes"
    
    - name: "Availability Critical"
      condition: "availability < 99.0%"
      severity: "critical"
      notification: "email, slack, phone"
      escalation: "immediate"
    
    - name: "Latency Degradation"
      condition: "latency_p95 > 800ms"
      severity: "warning"
      notification: "email, slack"
      escalation: "after 30 minutes"
    
    - name: "High Error Rate"
      condition: "error_rate > 0.05%"
      severity: "warning"
      notification: "email, slack"
      escalation: "after 15 minutes"
    
    - name: "Throughput Limit"
      condition: "throughput > 90% capacity"
      severity: "warning"
      notification: "email, slack"
      escalation: "immediate"
```

---

## 5. Compliance Requirements

### 5.1 Regulatory Compliance Matrix

```yaml
compliance_matrix:
  gdpr:
    name: "General Data Protection Regulation"
    applicability: "EU data subjects"
    key_requirements:
      - lawful_basis_for_processing
      - data_subject_rights
      - data_protection_officer
      - data_breach_notification
      - data_protection_impact_assessment
      - international_transfer_safeguards
    vendor_requirements:
      - dpa_with_gdpr_clauses
      - data_processing_records
      - security_measures_documentation
      - sub_processor_management
      - audit_rights
    penalties:
      - up_to_20_million_euros
      - up_to_4_percent_global_revenue

  ccpa:
    name: "California Consumer Privacy Act"
    applicability: "California residents"
    key_requirements:
      - right_to_know
      - right_to_delete
      - right_to_opt_out
      - non_discrimination
      - data_breach_notification
    vendor_requirements:
      - consumer_request_handling
      - data_deletion_capabilities
      - opt_out_mechanisms
      - privacy_policy_disclosure
    penalties:
      - up_to_7500_per_violation
      - actual_damages_for_breach

  hipaa:
    name: "Health Insurance Portability and Accountability Act"
    applicability: "Health information"
    key_requirements:
      - administrative_safeguards
      - physical_safeguards
      - technical_safeguards
      - privacy_rule
      - security_rule
      - breach_notification_rule
    vendor_requirements:
      - business_associate_agreement
      - hipaa_compliance_certification
      - security_assessment
      - audit_rights
      - incident_response_plan
    penalties:
      - up_to_15000_per_violation
      - up_to_15_million_annual_cap

  sox:
    name: "Sarbanes-Oxley Act"
    applicability: "Public companies"
    key_requirements:
      - internal_controls
      - financial_reporting
      - audit_trail
      - data_integrity
    vendor_requirements:
      - sox_compliance_certification
      - audit_rights
      - control_documentation
      - change_management
    penalties:
      - fines
      - imprisonment
      - delisting

  pci_dss:
    name: "Payment Card Industry Data Security Standard"
    applicability: "Payment card data"
    key_requirements:
      - network_security
      - data_protection
      - vulnerability_management
      - access_control
      - monitoring
      - security_policies
    vendor_requirements:
      - pci_dss_certification
      - quarterly_scans
      - annual_assessment
      - incident_response_plan
    penalties:
      - fines_5000_to_100000
      - card_replacement_costs
      - brand_damage
```

### 5.2 AI-Specific Compliance Requirements

```yaml
ai_compliance:
  ai_transparency:
    description: "Requirements for AI system transparency"
    requirements:
      - model_documentation
      - decision_explanation
      - bias_disclosure
      - performance_reporting
    regulations:
      - "EU AI Act"
      - "NIST AI Risk Management Framework"
      - "Algorithmic Accountability Act"
  
  ai_ethics:
    description: "Ethical AI requirements"
    requirements:
      - fairness_metrics
      - bias_testing
      - human_oversight
      - accountability_framework
    standards:
      - "IEEE Ethically Aligned Design"
      - "Asilomar AI Principles"
      - "OECD AI Principles"
  
  ai_safety:
    description: "AI safety requirements"
    requirements:
      - safety_testing
      - failure_mode_analysis
      - human_in_the_loop
      - emergency_shutdown
    standards:
      - "ISO/IEC 42001"
      - "NIST AI RMF"
      - "EU AI Act Risk Categories"
  
  ai_governance:
    description: "AI governance requirements"
    requirements:
      - governance_framework
      - risk_management
      - oversight_committee
      - policy_documentation
    standards:
      - "ISO/IEC 42001"
      - "NIST AI RMF"
      - "EU AI Act"
```

---

## 6. Vendor Selection Criteria

### 6.1 Evaluation Framework

```yaml
evaluation_framework:
  criteria:
    technical_capability:
      weight: "30%"
      factors:
        - name: "Model Performance"
          weight: "10%"
          assessment_method: "benchmark_testing"
          scoring: "1-10"
        - name: "API Reliability"
          weight: "8%"
          assessment_method: "uptime_analysis"
          scoring: "1-10"
        - name: "Scalability"
          weight: "7%"
          assessment_method: "load_testing"
          scoring: "1-10"
        - name: "Integration Ease"
          weight: "5%"
          assessment_method: "technical_evaluation"
          scoring: "1-10"
    
    security_compliance:
      weight: "25%"
      factors:
        - name: "Security Certifications"
          weight: "8%"
          assessment_method: "certification_review"
          scoring: "1-10"
        - name: "Data Protection"
          weight: "7%"
          assessment_method: "security_assessment"
          scoring: "1-10"
        - name: "Compliance Coverage"
          weight: "5%"
          assessment_method: "compliance_audit"
          scoring: "1-10"
        - name: "Incident Response"
          weight: "5%"
          assessment_method: "ir_plan_review"
          scoring: "1-10"
    
    cost_value:
      weight: "20%"
      factors:
        - name: "Pricing Model"
          weight: "8%"
          assessment_method: "cost_analysis"
          scoring: "1-10"
        - name: "Total Cost of Ownership"
          weight: "7%"
          assessment_method: "tco_analysis"
          scoring: "1-10"
        - name: "Value for Money"
          weight: "5%"
          assessment_method: "value_assessment"
          scoring: "1-10"
    
    vendor_reliability:
      weight: "15%"
      factors:
        - name: "Financial Stability"
          weight: "5%"
          assessment_method: "financial_review"
          scoring: "1-10"
        - name: "Market Position"
          weight: "5%"
          assessment_method: "market_analysis"
          scoring: "1-10"
        - name: "Customer References"
          weight: "5%"
          assessment_method: "reference_check"
          scoring: "1-10"
    
    support_service:
      weight: "10%"
      factors:
        - name: "Support Quality"
          weight: "4%"
          assessment_method: "support_evaluation"
          scoring: "1-10"
        - name: "Documentation"
          weight: "3%"
          assessment_method: "docs_review"
          scoring: "1-10"
        - name: "Training"
          weight: "3%"
          assessment_method: "training_assessment"
          scoring: "1-10"
```

### 6.2 Vendor Scorecard

```yaml
vendor_scorecard:
  vendor_name: "{{vendor_name}}"
  evaluation_date: "{{evaluation_date}}"
  evaluator: "{{evaluator_name}}"
  
  scores:
    technical_capability:
      model_performance: 8
      api_reliability: 9
      scalability: 7
      integration_ease: 8
      sub_total: 8.0
    
    security_compliance:
      security_certifications: 9
      data_protection: 8
      compliance_coverage: 7
      incident_response: 8
      sub_total: 8.0
    
    cost_value:
      pricing_model: 7
      total_cost_of_ownership: 7
      value_for_money: 8
      sub_total: 7.3
    
    vendor_reliability:
      financial_stability: 9
      market_position: 8
      customer_references: 8
      sub_total: 8.3
    
    support_service:
      support_quality: 8
      documentation: 7
      training: 7
      sub_total: 7.3
  
  weighted_score: "8.0"
  recommendation: "approve|conditional|reject"
  conditions:
    - "Complete SOC 2 Type II certification within 60 days"
    - "Implement additional data encryption measures"
    - "Provide dedicated account manager"
  
  approval:
    evaluator: "name"
    evaluator_date: "date"
    security_approver: "name"
    security_approver_date: "date"
    executive_approver: "name"
    executive_approver_date: "date"
```

---

## 7. Vendor Onboarding Process

### 7.1 Onboarding Checklist

```yaml
onboarding_checklist:
  phase_1_contractual:
    - item: "Contract execution"
      responsible: "Legal"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "DPA signing"
      responsible: "Legal"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "SLA agreement"
      responsible: "Procurement"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "NDA execution"
      responsible: "Legal"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Insurance verification"
      responsible: "Procurement"
      status: "pending|in_progress|completed"
      notes: ""
  
  phase_2_security:
    - item: "Security assessment"
      responsible: "Security"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Access control setup"
      responsible: "Security"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Encryption configuration"
      responsible: "Security"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Monitoring setup"
      responsible: "Operations"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Incident response planning"
      responsible: "Security"
      status: "pending|in_progress|completed"
      notes: ""
  
  phase_3_technical:
    - item: "API key provisioning"
      responsible: "Engineering"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Integration development"
      responsible: "Engineering"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Testing environment setup"
      responsible: "Engineering"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Performance baseline"
      responsible: "Engineering"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Documentation review"
      responsible: "Engineering"
      status: "pending|in_progress|completed"
      notes: ""
  
  phase_4_operational:
    - item: "Team training"
      responsible: "Operations"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Process documentation"
      responsible: "Operations"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Escalation procedures"
      responsible: "Operations"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Cost tracking setup"
      responsible: "Finance"
      status: "pending|in_progress|completed"
      notes: ""
    - item: "Vendor relationship kickoff"
      responsible: "Procurement"
      status: "pending|in_progress|completed"
      notes: ""
```

---

## Summary

Effective vendor management for AI/LLM systems requires:

1. **Structured Lifecycle Management**: Clear phases from selection to offboarding with defined activities and governance
2. **Comprehensive Risk Assessment**: Multi-dimensional risk evaluation with scoring methodology
3. **Robust DPAs**: AI-specific clauses addressing model training, output ownership, and bias requirements
4. **Detailed SLAs**: Performance, support, and compliance metrics with clear remedies
5. **Regulatory Compliance**: Coverage of GDPR, CCPA, HIPAA, and AI-specific regulations
6. **Rigorous Evaluation**: Weighted criteria and scorecards for vendor selection
7. **Systematic Onboarding**: Multi-phase checklist ensuring all requirements are met

By following these fundamentals, organizations can effectively manage AI/LLM vendor relationships while minimizing risks and ensuring compliance with regulatory and business requirements.
