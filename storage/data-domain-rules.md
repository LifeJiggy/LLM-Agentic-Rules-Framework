# Data Domain Rules - Complete Reference

## Overview

The Data domain contains rules for data handling, privacy, governance, and quality throughout the AI system lifecycle.

## DATA-001: Data Inventory Maintenance

### Rule Statement

Every AI system must maintain a current inventory of all data sources, types, and classifications.

### Data Inventory Schema

```yaml
data_inventory:
  system_id: "support-assistant-001"
  last_updated: "2026-06-04"
  owner: "Data Team"
  
  data_sources:
    - source_id: "customer_database"
      name: "Customer Database"
      type: "database"
      technology: "PostgreSQL"
      location: "AWS RDS us-east-1"
      description: "Primary customer data store"
      
      data_types:
        - type: "customer_profiles"
          classification: "confidential"
          fields: ["customer_id", "name", "email", "phone", "address"]
          pii: true
          owner: "customer_success"
        
        - type: "support_tickets"
          classification: "confidential"
          fields: ["ticket_id", "customer_id", "subject", "description", "status"]
          pii: true
          owner: "customer_success"
        
        - type: "interaction_history"
          classification: "internal"
          fields: ["interaction_id", "customer_id", "timestamp", "channel", "summary"]
          pii: false
          owner: "customer_success"
      
      retention:
        customer_profiles: "7 years"
        support_tickets: "3 years"
        interaction_history: "1 year"
      
      access:
        read: ["customer_success", "support_agents", "ml_platform"]
        write: ["customer_success", "support_agents"]
        admin: ["database_admins"]
      
      encryption:
        at_rest: "AES-256"
        in_transit: "TLS 1.2"
        key_management: "AWS KMS"
    
    - source_id: "knowledge_base"
      name: "Knowledge Base"
      type: "vector_store"
      technology: "Pinecone"
      location: "Pinecone Cloud"
      description: "Document embeddings for retrieval"
      
      data_types:
        - type: "document_embeddings"
          classification: "internal"
          fields: ["document_id", "embedding", "metadata"]
          pii: false
          owner: "content_team"
        
        - type: "document_content"
          classification: "internal"
          fields: ["document_id", "title", "content", "version"]
          pii: false
          owner: "content_team"
      
      retention:
        document_embeddings: "until_document_deleted"
        document_content: "until_document_deleted"
      
      access:
        read: ["ml_platform", "support_agents"]
        write: ["content_team", "ml_platform"]
        admin: ["ml_platform_admins"]
    
    - source_id: "user_feedback"
      name: "User Feedback"
      type: "api"
      technology: "REST API"
      location: "internal API"
      description: "User feedback and ratings"
      
      data_types:
        - type: "feedback_ratings"
          classification: "internal"
          fields: ["feedback_id", "user_id", "rating", "timestamp"]
          pii: false
          owner: "product_team"
        
        - type: "feedback_comments"
          classification: "confidential"
          fields: ["feedback_id", "user_id", "comment", "timestamp"]
          pii: true
          owner: "product_team"
      
      retention:
        feedback_ratings: "2 years"
        feedback_comments: "1 year"
      
      access:
        read: ["product_team", "ml_platform"]
        write: ["support_agents", "ml_platform"]
        admin: ["product_admins"]
  
  data_flows:
    - flow_id: "flow_001"
      name: "Customer Query Flow"
      source: "customer_database"
      destination: "ml_platform"
      data_types: ["customer_profiles", "support_tickets"]
      transformations: ["anonymization", "summarization"]
      controls: ["encryption", "access_control", "audit_logging"]
    
    - flow_id: "flow_002"
      name: "Knowledge Retrieval Flow"
      source: "knowledge_base"
      destination: "ml_platform"
      data_types: ["document_embeddings", "document_content"]
      transformations: ["retrieval", "ranking"]
      controls: ["access_control", "audit_logging"]
    
    - flow_id: "flow_003"
      name: "Feedback Collection Flow"
      source: "ml_platform"
      destination: "user_feedback"
      data_types: ["feedback_ratings", "feedback_comments"]
      transformations: ["validation", "storage"]
      controls: ["encryption", "access_control", "audit_logging"]
```

### Verification Checklist

- [ ] Data inventory created
- [ ] All data sources documented
- [ ] Data types classified
- [ ] Data owners assigned
- [ ] Retention periods defined
- [ ] Access controls documented
- [ ] Data flows mapped
- [ ] Inventory reviewed quarterly

---

## DATA-002: Classification Labeling

### Rule Statement

All data processed by AI systems must be classified by sensitivity and labeled accordingly.

### Classification Schema

```yaml
classification_schema:
  levels:
    - level: "public"
      description: "Freely available, no access restrictions"
      controls:
        - "basic_access_control"
        - "integrity_protection"
      examples:
        - "Marketing content"
        - "Public documentation"
        - "Open source code"
    
    - level: "internal"
      description: "Employee access only, basic controls"
      controls:
        - "authentication_required"
        - "access_logging"
        - "integrity_protection"
      examples:
        - "Internal documentation"
        - "Non-sensitive business data"
        - "Internal communications"
    
    - level: "confidential"
      description: "Restricted access, encryption, logging"
      controls:
        - "authentication_required"
        - "authorization_required"
        - "encryption_at_rest"
        - "encryption_in_transit"
        - "access_logging"
        - "audit_trail"
      examples:
        - "Customer PII"
        - "Business secrets"
        - "Financial data"
        - "Employee data"
    
    - level: "restricted"
      description: "Highly restricted, strong encryption, MFA, audit"
      controls:
        - "mfa_required"
        - "strong_encryption"
        - "access_logging"
        - "audit_trail"
        - "real_time_monitoring"
        - "legal_review"
      examples:
        - "Payment card data"
        - "Health records"
        - "Legal privileged information"
        - "Authentication credentials"
  
  labeling:
    method: "metadata_tagging"
    fields:
      - field: "classification_level"
        type: "enum"
        values: ["public", "internal", "confidential", "restricted"]
      
      - field: "classification_date"
        type: "date"
      
      - field: "classified_by"
        type: "string"
      
      - field: "review_date"
        type: "date"
      
      - field: "data_owner"
        type: "string"
    
    enforcement:
      - "All data sources must have classification labels"
      - "Classification must be reviewed annually"
      - "Classification changes require approval"
      - "Higher classification requires justification"
```

### Verification Checklist

- [ ] Classification schema defined
- [ ] Labels applied to all data
- [ ] Classification documented
- [ ] Classification reviewed annually
- [ ] Label enforcement implemented
- [ ] Classification training completed

---

## DATA-003: Retention Policy Enforcement

### Rule Statement

Data retention policies must be defined and enforced for all data processed by AI systems.

### Retention Policy

```yaml
retention_policy:
  general_rules:
    - rule: "purpose_limitation"
      description: "Delete data when no longer needed for purpose"
      enforcement: "automated"
    
    - rule: "legal_hold_override"
      description: "Retention suspended during legal hold"
      enforcement: "manual_with_automation"
    
    - rule: "regulatory_minimum"
      description: "Retain for minimum required by regulation"
      enforcement: "automated"
  
  retention_periods:
    - data_type: "customer_pii"
      period: "7 years"
      regulation: "GDPR, CCPA"
      enforcement: "automated_purge"
      legal_hold: "supported"
    
    - data_type: "support_tickets"
      period: "3 years"
      regulation: "business_requirement"
      enforcement: "automated_purge"
      legal_hold: "supported"
    
    - data_type: "interaction_history"
      period: "1 year"
      regulation: "business_requirement"
      enforcement: "automated_purge"
      legal_hold: "supported"
    
    - data_type: "audit_logs"
      period: "7 years"
      regulation: "SOC 2, ISO 27001"
      enforcement: "automated_archive"
      legal_hold: "supported"
    
    - data_type: "evaluation_results"
      period: "3 years"
      regulation: "business_requirement"
      enforcement: "automated_purge"
      legal_hold: "supported"
    
    - data_type: "user_feedback"
      period: "2 years"
      regulation: "business_requirement"
      enforcement: "automated_purge"
      legal_hold: "supported"
  
  enforcement:
    automated_purge:
      schedule: "daily"
      method: "soft_delete_then_purge"
      soft_delete_period: "30 days"
      notification: "data_owner_before_purge"
    
    legal_hold:
      trigger: "legal_team_request"
      process:
        - "Suspend automated purge"
        - "Flag affected records"
        - "Notify data owner"
        - "Document hold reason"
        - "Review hold quarterly"
      release: "legal_team_approval"
```

### Verification Checklist

- [ ] Retention policy defined
- [ ] Retention periods documented
- [ ] Automated enforcement configured
- [ ] Legal hold process documented
- [ ] Retention monitoring configured
- [ ] Retention audit performed quarterly

---

## DATA-004: Consent Management

### Rule Statement

Systems processing personal data must implement consent management where required by regulation.

### Consent Management Architecture

```yaml
consent_management:
  requirements:
    - regulation: "GDPR"
      consent_types:
        - type: "data_processing"
          description: "Consent for data processing"
          required: true
          granular: true
          withdrawable: true
        
        - type: "marketing"
          description: "Consent for marketing communications"
          required: false
          granular: true
          withdrawable: true
        
        - type: "third_party_sharing"
          description: "Consent for sharing with third parties"
          required: true
          granular: true
          withdrawable: true
    
    - regulation: "CCPA"
      consent_types:
        - type: "data_sale_opt_out"
          description: "Opt-out of data sale"
          required: false
          granular: false
          withdrawable: true
  
  implementation:
    collection:
      method: "explicit_opt_in"
      ui_requirements:
        - "Clear and conspicuous"
        - "Separate from terms and conditions"
        - "No pre-checked boxes"
        - "Easy to withdraw"
      documentation:
        - "What data is collected"
        - "Why it is collected"
        - "How it is used"
        - "Who it is shared with"
        - "How to withdraw"
    
    storage:
      schema:
        - field: "consent_id"
          type: "uuid"
        - field: "user_id"
          type: "string"
        - field: "consent_type"
          type: "string"
        - field: "granted"
          type: "boolean"
        - field: "timestamp"
          type: "iso8601"
        - field: "version"
          type: "string"
        - field: "method"
          type: "string"
        - field: "ip_address"
          type: "string"
      retention: "duration_of_relationship_plus_3_years"
      integrity: "immutable_audit_log"
    
    withdrawal:
      method: "same_as_collection"
      ui_requirements:
        - "As easy to withdraw as to grant"
        - "Confirmation of withdrawal"
        - "Effective immediately"
      processing:
        - "Stop processing for withdrawn purpose"
        - "Delete data if no other legal basis"
        - "Notify third parties of withdrawal"
        - "Document withdrawal"
    
    verification:
      frequency: "on_each_processing"
      method: "check_consent_record"
      action_on_no_consent: "stop_processing"
```

### Verification Checklist

- [ ] Consent requirements identified
- [ ] Consent collection implemented
- [ ] Consent storage configured
- [ ] Withdrawal process implemented
- [ ] Verification process implemented
- [ ] Consent records maintained
- [ ] Consent audit trail maintained

---

## DATA-005: Data Minimization

### Rule Statement

AI systems must collect and process only the minimum data necessary for their intended purpose.

### Minimization Implementation

```yaml
data_minimization:
  principles:
    - principle: "purpose_limitation"
      description: "Collect only data needed for stated purpose"
      implementation: "data_requirements_definition"
    
    - principle: "data_reduction"
      description: "Reduce data to minimum necessary fields"
      implementation: "field_selection_and_masking"
    
    - principle: "retention_limitation"
      description: "Keep data only as long as needed"
      implementation: "automated_retention_enforcement"
    
    - principle: "access_limitation"
      description: "Access only data needed for task"
      implementation: "role_based_access_control"
  
  implementation:
    - area: "collection"
      techniques:
        - "Collect only required fields"
        - "Make optional fields truly optional"
        - "Validate collection necessity"
      verification: "data_collection_audit"
    
    - area: "processing"
      techniques:
        - "Process only required attributes"
        - "Filter unnecessary data before processing"
        - "Aggregate where individual data not needed"
      verification: "data_processing_audit"
    
    - area: "storage"
      techniques:
        - "Store only necessary data"
        - "Archive or delete when no longer needed"
        - "Compress where possible"
      verification: "data_storage_audit"
    
    - area: "sharing"
      techniques:
        - "Share only necessary data"
        - "Anonymize or pseudonymize where possible"
        - "Document sharing necessity"
      verification: "data_sharing_audit"
```

### Verification Checklist

- [ ] Data requirements defined
- [ ] Collection minimized
- [ ] Processing minimized
- [ ] Storage minimized
- [ ] Sharing minimized
- [ ] Minimization reviewed quarterly

---

## DATA-006: Encryption at Rest and in Transit

### Rule Statement

Confidential and restricted data must be encrypted at rest and in transit.

### Encryption Standards

```yaml
encryption_standards:
  at_rest:
    algorithm: "AES-256-GCM"
    key_management: "AWS KMS or HashiCorp Vault"
    key_rotation: "annually"
    scope: "all_confidential_and_restricted_data"
    implementation:
      - "Database encryption"
      - "File system encryption"
      - "Backup encryption"
      - "Log encryption"
  
  in_transit:
    protocol: "TLS 1.2 or higher"
    certificate_management: "AWS Certificate Manager or Let's Encrypt"
    certificate_rotation: "before_expiry"
    scope: "all_data_transmission"
    implementation:
      - "API communication"
      - "Database connections"
      - "Inter-service communication"
      - "External integrations"
  
  key_management:
    provider: "AWS KMS or HashiCorp Vault"
    configuration:
      - "Keys stored in HSM"
      - "Access controlled via IAM"
      - "Key usage logged"
      - "Key rotation automated"
    access:
      - "Application service accounts"
      - "Operations team (break-glass)"
      - "Security team (audit)"
```

### Verification Checklist

- [ ] Encryption at rest implemented
- [ ] Encryption in transit implemented
- [ ] Key management configured
- [ ] Key rotation configured
- [ ] Certificate management configured
- [ ] Encryption verified regularly

---

## DATA-007: Access Logging

### Rule Statement

All access to confidential and restricted data must be logged with sufficient detail for audit.

### Access Logging Schema

```yaml
access_logging:
  schema:
    required_fields:
      - field: "access_id"
        type: "uuid"
        description: "Unique access event identifier"
      
      - field: "timestamp"
        type: "iso8601"
        description: "Access timestamp in UTC"
      
      - field: "user_id"
        type: "string"
        description: "User performing access"
      
      - field: "user_role"
        type: "string"
        description: "Role of user"
      
      - field: "action"
        type: "enum"
        values: ["read", "write", "delete", "export"]
        description: "Action performed"
      
      - field: "resource_type"
        type: "string"
        description: "Type of resource accessed"
      
      - field: "resource_id"
        type: "string"
        description: "Identifier of resource"
      
      - field: "data_classification"
        type: "enum"
        values: ["public", "internal", "confidential", "restricted"]
        description: "Classification of data accessed"
      
      - field: "source_ip"
        type: "string"
        description: "IP address of access"
      
      - field: "result"
        type: "enum"
        values: ["success", "failure", "denied"]
        description: "Result of access attempt"
      
      - field: "justification"
        type: "string"
        description: "Justification for access (required for restricted)"
    
    optional_fields:
      - field: "session_id"
        type: "string"
      
      - field: "request_id"
        type: "string"
      
      - field: "data_fields"
        type: "array"
        description: "Specific fields accessed"
      
      - field: "export_format"
        type: "string"
        description: "Format if data exported"
  
  retention:
    confidential_logs: "7 years"
    restricted_logs: "7 years"
    internal_logs: "1 year"
  
  storage:
    primary: "immutable_log_store"
    backup: "encrypted_backup"
    integrity: "hash_chain"
  
  monitoring:
    real_time_alerts:
      - condition: "restricted_data_access_from_unknown_ip"
        severity: "critical"
        action: "alert_security_team"
      
      - condition: "bulk_data_export"
        severity: "high"
        action: "alert_security_team"
      
      - condition: "access_outside_business_hours"
        severity: "medium"
        action: "log_for_review"
    
    periodic_reviews:
      - review: "weekly_access_summary"
        scope: "all_confidential_and_restricted"
        reviewer: "data_owner"
      
      - review: "monthly_anomaly_analysis"
        scope: "all_data_access"
        reviewer: "security_team"
```

### Verification Checklist

- [ ] Access logging implemented
- [ ] All required fields captured
- [ ] Log integrity protected
- [ ] Log retention configured
- [ ] Monitoring configured
- [ ] Reviews scheduled

---

## DATA-008: Data Quality Validation

### Rule Statement

Data used for AI system training and operation must be validated for quality.

### Quality Dimensions

```yaml
quality_dimensions:
  accuracy:
    description: "Data correctly represents reality"
    metrics:
      - "error_rate"
      - "correctness_score"
    threshold: "> 0.95"
    measurement: "automated_validation"
  
  completeness:
    description: "All required data is present"
    metrics:
      - "null_rate"
      - "missing_value_rate"
    threshold: "< 0.05"
    measurement: "automated_validation"
  
  consistency:
    description: "Data is consistent across sources"
    metrics:
      - "consistency_score"
      - "conflict_rate"
    threshold: "> 0.98"
    measurement: "cross_source_validation"
  
  timeliness:
    description: "Data is current and up-to-date"
    metrics:
      - "freshness_score"
      - "staleness_rate"
    threshold: "> 0.90"
    measurement: "timestamp_analysis"
  
  validity:
    description: "Data conforms to defined formats"
    metrics:
      - "format_compliance_rate"
      - "schema_violation_rate"
    threshold: "> 0.99"
    measurement: "schema_validation"
```

### Quality Validation Implementation

```yaml
quality_validation:
  automated_checks:
    - check: "null_check"
      description: "Check for null values in required fields"
      frequency: "on_ingestion"
      action: "reject_or_flag"
    
    - check: "format_check"
      description: "Validate data format"
      frequency: "on_ingestion"
      action: "reject_or_flag"
    
    - check: "range_check"
      description: "Validate values are within expected range"
      frequency: "on_ingestion"
      action: "reject_or_flag"
    
    - check: "duplicate_check"
      description: "Check for duplicate records"
      frequency: "daily"
      action: "flag_for_review"
    
    - check: "freshness_check"
      description: "Check data freshness"
      frequency: "hourly"
      action: "alert_if_stale"
  
  quality_metrics:
    - metric: "overall_quality_score"
      formula: "weighted_average(accuracy, completeness, consistency, timeliness, validity)"
      target: "> 0.90"
    
    - metric: "ingestion_error_rate"
      formula: "errors / total_records"
      target: "< 0.01"
    
    - metric: "data_freshness"
      formula: "1 - (current_time - last_update) / expected_interval"
      target: "> 0.90"
  
  quality_reporting:
    frequency: "daily"
    distribution: ["data_team", "ml_team", "product_team"]
    dashboard: "data_quality_dashboard"
  
  quality_improvement:
    process:
      - "Identify quality issues"
      - "Root cause analysis"
      - "Implement fixes"
      - "Verify fixes"
      - "Update validation rules"
    tracking: "quality_issue_tracker"
```

### Verification Checklist

- [ ] Quality dimensions defined
- [ ] Quality metrics configured
- [ ] Automated checks implemented
- [ ] Quality reporting configured
- [ ] Quality improvement process defined
- [ ] Quality reviewed monthly

---

## DATA-009: Cross-Border Transfer Assessment

### Rule Statement

Data transfers across borders must be assessed for regulatory compliance.

### Transfer Assessment Framework

```yaml
cross_border_transfers:
  assessment:
    - transfer_id: "transfer_001"
      name: "EU to US data transfer"
      source_jurisdiction: "EU"
      destination_jurisdiction: "US"
      data_types: ["customer_pii", "support_tickets"]
      volume: "10000_records_per_day"
      
      regulatory_requirements:
        - regulation: "GDPR"
          requirement: "Adequate safeguards required"
          mechanism: "Standard Contractual Clauses (SCCs)"
          status: "implemented"
        
        - regulation: "EU AI Act"
          requirement: "Transparency about transfers"
          mechanism: "Privacy notice"
          status: "implemented"
      
      risk_assessment:
        risk_level: "medium"
        factors:
          - "Different legal frameworks"
          - "Government access risks"
          - "Enforcement challenges"
        mitigations:
          - "SCCs in place"
          - "Encryption in transit and at rest"
          - "Access controls"
          - "Regular audits"
      
      documentation:
        - "Transfer impact assessment"
        - "SCCs agreement"
        - "Technical measures documentation"
        - "Audit results"
    
    - transfer_id: "transfer_002"
      name: "US to EU data transfer"
      source_jurisdiction: "US"
      destination_jurisdiction: "EU"
      data_types: ["usage_analytics"]
      volume: "100000_records_per_day"
      
      regulatory_requirements:
        - regulation: "CCPA"
          requirement: "Disclosure of transfers"
          mechanism: "Privacy notice"
          status: "implemented"
      
      risk_assessment:
        risk_level: "low"
        factors:
          - "EU has adequate protection"
          - "Non-sensitive data"
        mitigations:
          - "Encryption in transit"
          - "Access controls"
      
      documentation:
        - "Transfer assessment"
        - "Privacy notice"
```

### Verification Checklist

- [ ] Transfers identified
- [ ] Assessments completed
- [ ] Mechanisms implemented
- [ ] Documentation maintained
- [ ] Monitoring configured
- [ ] Reviews scheduled

---

## DATA-010: Data Lineage Tracking

### Rule Statement

Data transformations and lineage should be tracked to support audit and debugging.

### Lineage Tracking Implementation

```yaml
data_lineage:
  tracking:
    enabled: true
    granularity: "field_level"
    
    metadata:
      - field: "source_system"
        description: "System where data originated"
      
      - field: "extraction_timestamp"
        description: "When data was extracted"
      
      - field: "transformations"
        description: "List of transformations applied"
      
      - field: "destination_system"
        description: "System where data was loaded"
      
      - field: "loading_timestamp"
        description: "When data was loaded"
      
      - field: "pipeline_id"
        description: "Identifier of data pipeline"
      
      - field: "pipeline_version"
        description: "Version of pipeline code"
  
  transformations:
    - transformation_id: "transform_001"
      name: "PII Anonymization"
      description: "Anonymize PII fields"
      input_fields: ["name", "email", "phone"]
      output_fields: ["anonymous_id"]
      method: "hashing"
      reversibility: "irreversible"
    
    - transformation_id: "transform_002"
      name: "Data Aggregation"
      description: "Aggregate daily metrics"
      input_fields: ["interaction_records"]
      output_fields: ["daily_metrics"]
      method: "summarization"
      reversibility: "irreversible"
    
    - transformation_id: "transform_003"
      name: "Feature Engineering"
      description: "Create ML features"
      input_fields: ["customer_data", "interaction_data"]
      output_fields: ["feature_vector"]
      method: "transformation"
      reversibility: "reversible_with_metadata"
  
  lineage_queries:
    - query: "upstream"
      description: "Find all sources of a data element"
      example: "Where did this customer_id come from?"
    
    - query: "downstream"
      description: "Find all uses of a data element"
      example: "What systems use this customer_id?"
    
    - query: "impact_analysis"
      description: "Assess impact of changing a data element"
      example: "What breaks if we change this field?"
    
    - query: "audit_trail"
      description: "Trace data through all transformations"
      example: "Show me the full history of this record"
  
  verification:
    frequency: "daily"
    method: "lineage_completeness_check"
    coverage_target: "> 95%"
```

### Verification Checklist

- [ ] Lineage tracking implemented
- [ ] Transformations documented
- [ ] Metadata captured
- [ ] Queries supported
- [ ] Verification configured
- [ ] Coverage monitored
