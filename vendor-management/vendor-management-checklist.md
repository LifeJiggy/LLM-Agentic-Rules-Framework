# Vendor Management Checklist for AI/LLM Systems

## Overview

This checklist provides comprehensive P0-P3 verification checks for vendor selection, onboarding, monitoring, and offboarding phases. Use this checklist to ensure all critical requirements are addressed.

---

## 1. Vendor Selection Phase

### 1.1 P0 - Critical Requirements (Must Pass)

```yaml
selection_p0:
  business_alignment:
    - id: "SEL-001"
      requirement: "Vendor aligns with business objectives"
      verification_method: "executive_review"
      evidence: "business_alignment_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-002"
      requirement: "Vendor meets core use case requirements"
      verification_method: "requirements_validation"
      evidence: "requirements_mapping"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-003"
      requirement: "Vendor supports required AI/LLM capabilities"
      verification_method: "technical_evaluation"
      evidence: "capability_assessment"
      status: "pending|pass|fail"
      notes: ""

  security_compliance:
    - id: "SEL-004"
      requirement: "Vendor holds required security certifications"
      verification_method: "certification_verification"
      evidence: "soc2_type2_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-005"
      requirement: "Vendor complies with data protection regulations"
      verification_method: "compliance_audit"
      evidence: "gdpr_compliance_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-006"
      requirement: "Vendor implements encryption at rest and in transit"
      verification_method: "security_assessment"
      evidence: "encryption_configuration_review"
      status: "pending|pass|fail"
      notes: ""

  financial_viability:
    - id: "SEL-007"
      requirement: "Vendor demonstrates financial stability"
      verification_method: "financial_assessment"
      evidence: "financial_health_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-008"
      requirement: "Vendor pricing is within budget constraints"
      verification_method: "cost_analysis"
      evidence: "budget_approval"
      status: "pending|pass|fail"
      notes: ""

  legal_compliance:
    - id: "SEL-009"
      requirement: "Vendor accepts DPA requirements"
      verification_method: "legal_review"
      evidence: "dpa_acceptance_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-010"
      requirement: "Vendor agrees to audit rights"
      verification_method: "legal_review"
      evidence: "audit_rights_confirmation"
      status: "pending|pass|fail"
      notes: ""
```

### 1.2 P1 - High Priority (Should Pass)

```yaml
selection_p1:
  technical_evaluation:
    - id: "SEL-011"
      requirement: "Vendor passes technical proof of concept"
      verification_method: "poc_execution"
      evidence: "poc_results_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-012"
      requirement: "Vendor meets performance requirements"
      verification_method: "benchmark_testing"
      evidence: "performance_benchmark_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-013"
      requirement: "Vendor demonstrates scalability"
      verification_method: "load_testing"
      evidence: "scalability_test_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-014"
      requirement: "Vendor provides adequate API documentation"
      verification_method: "documentation_review"
      evidence: "api_documentation_assessment"
      status: "pending|pass|fail"
      notes: ""

  reference_verification:
    - id: "SEL-015"
      requirement: "Vendor provides positive customer references"
      verification_method: "reference_check"
      evidence: "reference_verification_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-016"
      requirement: "Vendor has relevant industry experience"
      verification_method: "market_analysis"
      evidence: "industry_experience_assessment"
      status: "pending|pass|fail"
      notes: ""

  support_evaluation:
    - id: "SEL-017"
      requirement: "Vendor provides adequate support options"
      verification_method: "support_evaluation"
      evidence: "support_plan_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-018"
      requirement: "Vendor support meets response time requirements"
      verification_method: "sla_analysis"
      evidence: "support_sla_review"
      status: "pending|pass|fail"
      notes: ""
```

### 1.3 P2 - Medium Priority (Nice to Have)

```yaml
selection_p2:
  innovation_assessment:
    - id: "SEL-019"
      requirement: "Vendor demonstrates innovation capabilities"
      verification_method: "roadmap_review"
      evidence: "innovation_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-020"
      requirement: "Vendor has strong AI research capabilities"
      verification_method: "research_evaluation"
      evidence: "research_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-021"
      requirement: "Vendor offers customization options"
      verification_method: "feature_analysis"
      evidence: "customization_assessment"
      status: "pending|pass|fail"
      notes: ""

  partnership_potential:
    - id: "SEL-022"
      requirement: "Vendor demonstrates partnership mindset"
      verification_method: "relationship_assessment"
      evidence: "partnership_evaluation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-023"
      requirement: "Vendor offers strategic value"
      verification_method: "strategic_analysis"
      evidence: "strategic_value_assessment"
      status: "pending|pass|fail"
      notes: ""
```

### 1.4 P3 - Low Priority (Optional)

```yaml
selection_p3:
  additional_features:
    - id: "SEL-024"
      requirement: "Vendor provides training programs"
      verification_method: "training_evaluation"
      evidence: "training_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-025"
      requirement: "Vendor has community ecosystem"
      verification_method: "ecosystem_analysis"
      evidence: "ecosystem_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "SEL-026"
      requirement: "Vendor offers professional services"
      verification_method: "services_evaluation"
      evidence: "services_assessment"
      status: "pending|pass|fail"
      notes: ""
```

---

## 2. Vendor Onboarding Phase

### 2.1 P0 - Critical Requirements (Must Pass)

```yaml
onboarding_p0:
  contractual:
    - id: "ONB-001"
      requirement: "Master service agreement executed"
      verification_method: "legal_review"
      evidence: "executed_msa"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-002"
      requirement: "Data processing agreement signed"
      verification_method: "legal_review"
      evidence: "executed_dpa"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-003"
      requirement: "Service level agreement defined"
      verification_method: "sla_review"
      evidence: "executed_sla"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-004"
      requirement: "Confidentiality agreement in place"
      verification_method: "legal_review"
      evidence: "executed_nda"
      status: "pending|pass|fail"
      notes: ""

  security_setup:
    - id: "ONB-005"
      requirement: "Security assessment completed"
      verification_method: "security_review"
      evidence: "security_assessment_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-006"
      requirement: "Access controls implemented"
      verification_method: "access_review"
      evidence: "access_control_matrix"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-007"
      requirement: "Encryption configured"
      verification_method: "security_review"
      evidence: "encryption_configuration"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-008"
      requirement: "Monitoring enabled"
      verification_method: "operations_review"
      evidence: "monitoring_setup_confirmation"
      status: "pending|pass|fail"
      notes: ""

  legal_compliance:
    - id: "ONB-009"
      requirement: "Insurance verification completed"
      verification_method: "legal_review"
      evidence: "insurance_certificate"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-010"
      requirement: "Compliance documentation collected"
      verification_method: "compliance_review"
      evidence: "compliance_documentation_package"
      status: "pending|pass|fail"
      notes: ""
```

### 2.2 P1 - High Priority (Should Pass)

```yaml
onboarding_p1:
  technical_integration:
    - id: "ONB-011"
      requirement: "API credentials provisioned"
      verification_method: "technical_review"
      evidence: "api_credentials_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-012"
      requirement: "Integration architecture defined"
      verification_method: "architecture_review"
      evidence: "integration_architecture_document"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-013"
      requirement: "Testing environment configured"
      verification_method: "technical_review"
      evidence: "testing_environment_setup"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-014"
      requirement: "Performance baseline established"
      verification_method: "performance_testing"
      evidence: "performance_baseline_report"
      status: "pending|pass|fail"
      notes: ""

  operational_setup:
    - id: "ONB-015"
      requirement: "Escalation procedures defined"
      verification_method: "process_review"
      evidence: "escalation_procedure_document"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-016"
      requirement: "Incident response plan established"
      verification_method: "security_review"
      evidence: "incident_response_plan"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-017"
      requirement: "Communication channels established"
      verification_method: "relationship_review"
      evidence: "communication_plan"
      status: "pending|pass|fail"
      notes: ""
```

### 2.3 P2 - Medium Priority (Nice to Have)

```yaml
onboarding_p2:
  team_enablement:
    - id: "ONB-018"
      requirement: "Team training completed"
      verification_method: "training_verification"
      evidence: "training_completion_records"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-019"
      requirement: "Documentation reviewed"
      verification_method: "documentation_review"
      evidence: "documentation_review_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-020"
      requirement: "Knowledge transfer completed"
      verification_method: "knowledge_review"
      evidence: "knowledge_transfer_confirmation"
      status: "pending|pass|fail"
      notes: ""

  process_setup:
    - id: "ONB-021"
      requirement: "Change management process defined"
      verification_method: "process_review"
      evidence: "change_management_procedure"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-022"
      requirement: "Cost tracking configured"
      verification_method: "finance_review"
      evidence: "cost_tracking_setup"
      status: "pending|pass|fail"
      notes: ""
```

### 2.4 P3 - Low Priority (Optional)

```yaml
onboarding_p3:
  optimization:
    - id: "ONB-023"
      requirement: "Performance optimization planned"
      verification_method: "optimization_review"
      evidence: "optimization_plan"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "ONB-024"
      requirement: "Innovation roadmap aligned"
      verification_method: "strategic_review"
      evidence: "innovation_alignment_plan"
      status: "pending|pass|fail"
      notes: ""
```

---

## 3. Vendor Monitoring Phase

### 3.1 P0 - Critical Requirements (Must Pass)

```yaml
monitoring_p0:
  performance_monitoring:
    - id: "MON-001"
      requirement: "Availability monitoring active"
      verification_method: "monitoring_review"
      evidence: "availability_monitoring_dashboard"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-002"
      requirement: "Performance metrics tracked"
      verification_method: "metrics_review"
      evidence: "performance_metrics_dashboard"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-003"
      requirement: "Error rates monitored"
      verification_method: "monitoring_review"
      evidence: "error_rate_monitoring"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-004"
      requirement: "SLA compliance tracked"
      verification_method: "sla_review"
      evidence: "sla_compliance_report"
      status: "pending|pass|fail"
      notes: ""

  security_monitoring:
    - id: "MON-005"
      requirement: "Security incidents tracked"
      verification_method: "security_review"
      evidence: "security_incident_log"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-006"
      requirement: "Access patterns monitored"
      verification_method: "security_review"
      evidence: "access_monitoring_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-007"
      requirement: "Compliance status tracked"
      verification_method: "compliance_review"
      evidence: "compliance_monitoring_report"
      status: "pending|pass|fail"
      notes: ""

  cost_monitoring:
    - id: "MON-008"
      requirement: "Costs tracked and reported"
      verification_method: "finance_review"
      evidence: "cost_tracking_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-009"
      requirement: "Budget variance monitored"
      verification_method: "finance_review"
      evidence: "budget_variance_report"
      status: "pending|pass|fail"
      notes: ""
```

### 3.2 P1 - High Priority (Should Pass)

```yaml
monitoring_p1:
  quality_monitoring:
    - id: "MON-010"
      requirement: "Quality metrics tracked"
      verification_method: "quality_review"
      evidence: "quality_metrics_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-011"
      requirement: "User feedback collected"
      verification_method: "feedback_review"
      evidence: "user_feedback_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-012"
      requirement: "Continuous improvement tracked"
      verification_method: "improvement_review"
      evidence: "improvement_tracking_report"
      status: "pending|pass|fail"
      notes: ""

  relationship_monitoring:
    - id: "MON-013"
      requirement: "Regular reviews conducted"
      verification_method: "relationship_review"
      evidence: "review_meeting_minutes"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-014"
      requirement: "Communication effectiveness assessed"
      verification_method: "communication_review"
      evidence: "communication_assessment"
      status: "pending|pass|fail"
      notes: ""
```

### 3.3 P2 - Medium Priority (Nice to Have)

```yaml
monitoring_p2:
  risk_monitoring:
    - id: "MON-015"
      requirement: "Risk register maintained"
      verification_method: "risk_review"
      evidence: "risk_register"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-016"
      requirement: "Vendor financial health monitored"
      verification_method: "financial_review"
      evidence: "vendor_financial_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-017"
      requirement: "Market position tracked"
      verification_method: "market_review"
      evidence: "market_position_assessment"
      status: "pending|pass|fail"
      notes: ""

  innovation_monitoring:
    - id: "MON-018"
      requirement: "Vendor roadmap tracked"
      verification_method: "roadmap_review"
      evidence: "vendor_roadmap_assessment"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-019"
      requirement: "New features evaluated"
      verification_method: "feature_review"
      evidence: "feature_evaluation_report"
      status: "pending|pass|fail"
      notes: ""
```

### 3.4 P3 - Low Priority (Optional)

```yaml
monitoring_p3:
  optimization_monitoring:
    - id: "MON-020"
      requirement: "Optimization opportunities identified"
      verification_method: "optimization_review"
      evidence: "optimization_opportunities_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "MON-021"
      requirement: "Best practices implemented"
      verification_method: "best_practices_review"
      evidence: "best_practices_implementation_report"
      status: "pending|pass|fail"
      notes: ""
```

---

## 4. Vendor Offboarding Phase

### 4.1 P0 - Critical Requirements (Must Pass)

```yaml
offboarding_p0:
  data_management:
    - id: "OFF-001"
      requirement: "Data inventory completed"
      verification_method: "data_review"
      evidence: "data_inventory_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-002"
      requirement: "Data export executed"
      verification_method: "data_review"
      evidence: "data_export_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-003"
      requirement: "Data validation completed"
      verification_method: "data_review"
      evidence: "data_validation_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-004"
      requirement: "Data destruction confirmed"
      verification_method: "security_review"
      evidence: "data_destruction_certificate"
      status: "pending|pass|fail"
      notes: ""

  access_revocation:
    - id: "OFF-005"
      requirement: "API access revoked"
      verification_method: "security_review"
      evidence: "access_revocation_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-006"
      requirement: "User accounts deactivated"
      verification_method: "security_review"
      evidence: "account_deactivation_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-007"
      requirement: "Credentials rotated"
      verification_method: "security_review"
      evidence: "credential_rotation_confirmation"
      status: "pending|pass|fail"
      notes: ""

  legal_closure:
    - id: "OFF-008"
      requirement: "Contract termination executed"
      verification_method: "legal_review"
      evidence: "contract_termination_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-009"
      requirement: "Final reconciliation completed"
      verification_method: "finance_review"
      evidence: "final_reconciliation_report"
      status: "pending|pass|fail"
      notes: ""
```

### 4.2 P1 - High Priority (Should Pass)

```yaml
offboarding_p1:
  transition_management:
    - id: "OFF-010"
      requirement: "Alternative vendor selected"
      verification_method: "procurement_review"
      evidence: "alternative_vendor_selection"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-011"
      requirement: "Migration plan executed"
      verification_method: "migration_review"
      evidence: "migration_completion_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-012"
      requirement: "New system validated"
      verification_method: "validation_review"
      evidence: "validation_test_report"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-013"
      requirement: "User communication completed"
      verification_method: "communication_review"
      evidence: "user_communication_confirmation"
      status: "pending|pass|fail"
      notes: ""

  knowledge_transfer:
    - id: "OFF-014"
      requirement: "Documentation transferred"
      verification_method: "knowledge_review"
      evidence: "documentation_transfer_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-015"
      requirement: "Processes documented"
      verification_method: "process_review"
      evidence: "process_documentation"
      status: "pending|pass|fail"
      notes: ""
```

### 4.3 P2 - Medium Priority (Nice to Have)

```yaml
offboarding_p2:
  relationship_closure:
    - id: "OFF-016"
      requirement: "Vendor feedback provided"
      verification_method: "relationship_review"
      evidence: "vendor_feedback_documentation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-017"
      requirement: "Lessons learned documented"
      verification_method: "review_meeting"
      evidence: "lessons_learned_document"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-018"
      requirement: "Future engagement considered"
      verification_method: "strategic_review"
      evidence: "future_engagement_assessment"
      status: "pending|pass|fail"
      notes: ""

  process_improvement:
    - id: "OFF-019"
      requirement: "Process improvements identified"
      verification_method: "process_review"
      evidence: "process_improvement_recommendations"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-020"
      requirement: "Vendor management updates planned"
      verification_method: "review_meeting"
      evidence: "vendor_management_update_plan"
      status: "pending|pass|fail"
      notes: ""
```

### 4.4 P3 - Low Priority (Optional)

```yaml
offboarding_p3:
  optimization:
    - id: "OFF-021"
      requirement: "Knowledge base updated"
      verification_method: "knowledge_review"
      evidence: "knowledge_base_update_confirmation"
      status: "pending|pass|fail"
      notes: ""
    
    - id: "OFF-022"
      requirement: "Templates updated"
      verification_method: "template_review"
      evidence: "template_update_confirmation"
      status: "pending|pass|fail"
      notes: ""
```

---

## 5. Checklist Usage Guidelines

### 5.1 Usage Instructions

```yaml
usage_instructions:
  when_to_use:
    - vendor_selection
    - vendor_onboarding
    - vendor_monitoring
    - vendor_offboarding
    - periodic_reviews
    - audit_preparation
  
  how_to_use:
    - assign_responsibilities
    - set_deadlines
    - track_progress
    - document_evidence
    - conduct_reviews
    - update_status
  
  roles:
    checklist_owner:
      responsibilities:
        - maintain_checklist
        - assign_items
        - track_progress
        - conduct_reviews
        - report_status
    
    item_owner:
      responsibilities:
        - complete_assigned_items
        - provide_evidence
        - update_status
        - report_progress
        - escalate_issues
    
    reviewer:
      responsibilities:
        - review_completions
        - verify_evidence
        - approve_items
        - provide_feedback
        - conduct_audits

  frequency:
    selection: "during_vendor_selection_process"
    onboarding: "during_vendor_onboarding"
    monitoring: "monthly|quarterly|annual"
    offboarding: "during_vendor_offboarding"
```

### 5.2 Evidence Requirements

```yaml
evidence_requirements:
  documentation:
    - "Written_confirmation"
    - "Signed_documents"
    - "Audit_reports"
    - "Test_results"
    - "Meeting_minutes"
  
  verification:
    - "Independent_verification"
    - "Third_party_confirmation"
    - "System_screenshots"
    - "Log_files"
    - "Certifications"
  
  retention:
    - "Store_evidence_securely"
    - "Maintain_for_audit_period"
    - "Version_control"
    - "Access_control"
    - "Backup_regularly"
  
  quality:
    - "Complete_and_accurate"
    - "Timely_collection"
    - "Proper_formatting"
    - "Clear_attribution"
    - "Accessible_storage"
```

### 5.3 Escalation Procedures

```yaml
escalation_procedures:
  level_1:
    trigger: "item_overdue_by_7_days"
    action: "notify_item_owner"
    escalation_to: "team_lead"
    timeframe: "24_hours"
  
  level_2:
    trigger: "item_overdue_by_14_days"
    action: "escalate_to_management"
    escalation_to: "department_head"
    timeframe: "48_hours"
  
  level_3:
    trigger: "item_overdue_by_30_days"
    action: "escalate_to_executive"
    escalation_to: "vp_or_c_level"
    timeframe: "72_hours"
  
  critical:
    trigger: "p0_item_failing"
    action: "immediate_escalation"
    escalation_to: "executive_sponsor"
    timeframe: "immediate"
```

---

## 6. Checklist Templates

### 6.1 Vendor Selection Checklist Template

```yaml
selection_checklist_template:
  vendor_name: "{{vendor_name}}"
  evaluation_date: "{{date}}"
  evaluator: "{{evaluator_name}}"
  
  p0_critical:
    business_alignment:
      - requirement: "Aligns with business objectives"
        status: "pending"
        evidence: ""
        notes: ""
    
    security_compliance:
      - requirement: "Required certifications held"
        status: "pending"
        evidence: ""
        notes: ""
    
    financial_viability:
      - requirement: "Financially stable"
        status: "pending"
        evidence: ""
        notes: ""
    
    legal_compliance:
      - requirement: "DPA requirements accepted"
        status: "pending"
        evidence: ""
        notes: ""
  
  p1_high:
    technical_evaluation:
      - requirement: "Passes technical POC"
        status: "pending"
        evidence: ""
        notes: ""
    
    reference_verification:
      - requirement: "Positive references provided"
        status: "pending"
        evidence: ""
        notes: ""
  
  p2_medium:
    innovation_assessment:
      - requirement: "Demonstrates innovation"
        status: "pending"
        evidence: ""
        notes: ""
  
  p3_low:
    additional_features:
      - requirement: "Training programs offered"
        status: "pending"
        evidence: ""
        notes: ""
  
  overall_assessment:
    score: "{{score}}"
    recommendation: "{{recommendation}}"
    conditions: ["{{condition}}"]
  
  approval:
    evaluator: "{{name}}"
    date: "{{date}}"
    security_approver: "{{name}}"
    date: "{{date}}"
    executive_approver: "{{name}}"
    date: "{{date}}"
```

### 6.2 Vendor Onboarding Checklist Template

```yaml
onboarding_checklist_template:
  vendor_name: "{{vendor_name}}"
  onboarding_date: "{{date}}"
  onboarding_owner: "{{owner_name}}"
  
  p0_critical:
    contractual:
      - requirement: "MSA executed"
        status: "pending"
        evidence: ""
        notes: ""
    
    security_setup:
      - requirement: "Security assessment completed"
        status: "pending"
        evidence: ""
        notes: ""
    
    legal_compliance:
      - requirement: "Insurance verified"
        status: "pending"
        evidence: ""
        notes: ""
  
  p1_high:
    technical_integration:
      - requirement: "API credentials provisioned"
        status: "pending"
        evidence: ""
        notes: ""
    
    operational_setup:
      - requirement: "Escalation procedures defined"
        status: "pending"
        evidence: ""
        notes: ""
  
  p2_medium:
    team_enablement:
      - requirement: "Team training completed"
        status: "pending"
        evidence: ""
        notes: ""
  
  p3_low:
    optimization:
      - requirement: "Performance optimization planned"
        status: "pending"
        evidence: ""
        notes: ""
  
  overall_assessment:
    completion_percentage: "{{percentage}}"
    issues: ["{{issue}}"]
    next_steps: ["{{next_step}}"]
  
  approval:
    onboarding_owner: "{{name}}"
    date: "{{date}}"
    security_approver: "{{name}}"
    date: "{{date}}"
    executive_approver: "{{name}}"
    date: "{{date}}"
```

---

## Summary

This checklist provides comprehensive verification checks for all phases of vendor management:

1. **Selection Phase**: Evaluate vendors against critical requirements
2. **Onboarding Phase**: Ensure proper setup and integration
3. **Monitoring Phase**: Track performance and compliance
4. **Offboarding Phase**: Manage transitions effectively

Use this checklist to:
- Ensure all critical requirements are addressed
- Track progress and completion
- Document evidence for audits
- Escalate issues appropriately
- Maintain compliance with regulations

By following this checklist, organizations can systematically manage vendor relationships while minimizing risks and ensuring compliance.
