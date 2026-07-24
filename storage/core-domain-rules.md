# Core Domain Rules - Complete Reference

## Overview

The Core domain contains the fundamental rules that every LLM and agentic system must follow regardless of risk tier or domain selection. These rules establish the foundation for all other domains.

## CORE-001: System Ownership and Purpose

### Rule Statement

Every AI system must have a documented owner, clear purpose statement, and defined intended use cases before production deployment.

### Detailed Requirements

**System Owner Requirements**:
- Named individual responsible for system behavior
- Contact information (email, phone, slack)
- Role and responsibilities documented
- Escalation path when owner unavailable
- Ownership transfer process defined

**Purpose Statement Requirements**:
- Clear description of what the system does
- Target user segments defined
- Intended use cases with specific boundaries
- Success metrics and thresholds
- Limitations and constraints documented

**Intended Use Documentation**:
- Specific tasks the system performs
- Domains and topics the system covers
- Languages and locales supported
- Input types accepted
- Output types generated
- Integration points

**Prohibited Use Documentation**:
- Explicit list of prohibited uses
- Regulatory restrictions
- Policy restrictions
- Safety restrictions
- Ethical restrictions

### Implementation Guidance

**Step 1: Identify System Owner**
```yaml
system_owner:
  name: "Jane Smith"
  role: "ML Engineering Lead"
  email: "jane.smith@company.com"
  phone: "+1-555-0123"
  slack: "@jane.smith"
  team: "AI Platform"
  manager: "John Doe"
```

**Step 2: Document Purpose**
```yaml
system_purpose:
  description: "Customer support assistant that helps users resolve technical issues"
  target_users: ["Customer support agents", "End users with technical issues"]
  intended_uses:
    - "Answer frequently asked questions"
    - "Guide users through troubleshooting steps"
    - "Escalate complex issues to human agents"
  success_metrics:
    - metric: "resolution_rate"
      target: 0.80
    - metric: "user_satisfaction"
      target: 4.0
  limitations:
    - "Cannot make account changes"
    - "Cannot access billing information"
    - "Cannot override security controls"
```

**Step 3: Document Prohibited Uses**
```yaml
prohibited_uses:
  - "Making financial decisions"
  - "Providing legal advice"
  - "Making medical diagnoses"
  - "Generating harmful content"
  - "Circumventing security controls"
  - "Accessing unauthorized data"
```

### Verification Checklist

- [ ] System owner named with contact information
- [ ] Purpose statement documented
- [ ] Intended use cases defined
- [ ] Prohibited uses documented
- [ ] Target user segments identified
- [ ] Success metrics defined
- [ ] Limitations documented
- [ ] Owner acknowledgment obtained

### Evidence Requirements

| Evidence | Type | Location | Retention |
|----------|------|----------|-----------|
| System register | Document | System registry | Life of system |
| Owner assignment | Record | System registry | Life of system |
| Purpose statement | Document | System documentation | Life of system |
| Use case documentation | Document | System documentation | Life of system |

---

## CORE-002: Risk Tier Assignment

### Rule Statement

Every AI system must have a risk tier assigned based on intended use, data sensitivity, and potential for harm, documented with justification.

### Risk Tier Definitions

**Low Risk**:
- Internal productivity or assistance
- No direct user impact
- No sensitive data processing
- No automated decisions affecting rights
- Examples: Internal code assistant, internal documentation chatbot

**Medium Risk**:
- Customer-facing guidance or workflow automation
- Limited rights impact
- Some sensitive data processing
- Human review available
- Examples: Customer support assistant, content generation for review

**High Risk**:
- Decisions affecting rights, safety, finance, healthcare, legal status
- Access to critical services
- Significant sensitive data processing
- Automated decisions with real-world impact
- Examples: Medical triage assistant, loan approval advisor, hiring evaluation tool

**Prohibited Risk**:
- Uses banned by law, policy, or contract
- Social scoring systems
- Unauthorized surveillance
- Deepfake generation for fraud
- Examples: Social scoring, unauthorized surveillance, fraud tools

### Risk Assessment Methodology

**Step 1: Identify Impact Dimensions**
```yaml
impact_dimensions:
  user_harm:
    description: "Potential harm to users"
    levels:
      - minimal: "No impact or minimal discomfort"
      - temporary: "Temporary disruption or inconvenience"
      - lasting: "Lasting impact on user"
      - critical: "Life-threatening or irreversible harm"
  
  data_exposure:
    description: "Potential data exposure"
    levels:
      - public: "Only public data at risk"
      - internal: "Internal data could be exposed"
      - confidential: "Confidential data could be exposed"
      - restricted: "Restricted or sensitive data could be exposed"
  
  financial_impact:
    description: "Potential financial impact"
    levels:
      - minimal: "Less than $10K"
      - moderate: "$10K to $100K"
      - significant: "$100K to $1M"
      - severe: "Greater than $1M"
  
  legal_exposure:
    description: "Potential legal exposure"
    levels:
      - minimal: "Contractual risk only"
      - moderate: "Regulatory warning possible"
      - significant: "Regulatory fine possible"
      - severe: "Criminal liability possible"
```

**Step 2: Score Each Dimension**
```yaml
scoring:
  user_harm:
    minimal: 1
    temporary: 2
    lasting: 3
    critical: 4
  
  data_exposure:
    public: 1
    internal: 2
    confidential: 3
    restricted: 4
  
  financial_impact:
    minimal: 1
    moderate: 2
    significant: 3
    severe: 4
  
  legal_exposure:
    minimal: 1
    moderate: 2
    significant: 3
    severe: 4
```

**Step 3: Calculate Risk Score**
```yaml
risk_calculation:
  formula: "Sum of all dimension scores"
  ranges:
    low: "1-8 points"
    medium: "9-16 points"
    high: "17-24 points"
    critical: "25+ points"
```

**Step 4: Assign Risk Tier**
```yaml
risk_tier_assignment:
  low:
    required_controls: "P0 basic controls"
    review_cadence: "Annually"
    evidence_requirements: "Basic documentation"
  
  medium:
    required_controls: "P0 + P1 controls"
    review_cadence: "Semi-annually"
    evidence_requirements: "Standard evidence package"
  
  high:
    required_controls: "P0 + P1 + P2 controls"
    review_cadence: "Quarterly"
    evidence_requirements: "Full evidence package"
  
  prohibited:
    required_controls: "System blocked from deployment"
    review_cadence: "N/A"
    evidence_requirements: "N/A"
```

### Risk Assessment Example

```yaml
risk_assessment:
  system_id: "support-assistant-001"
  assessment_date: "2026-06-04"
  assessor: "Jane Smith"
  
  impact_scores:
    user_harm: 2  # Temporary disruption
    data_exposure: 3  # Customer PII exposed
    financial_impact: 1  # Less than $10K
    legal_exposure: 2  # GDPR applicable
  
  total_score: 14
  risk_tier: medium
  
  justification: |
    Customer support assistant handles PII (customer names, emails, issue descriptions).
    Errors could cause temporary disruption but no lasting harm.
    Financial impact limited to support costs.
    GDPR applies due to EU customer data.
    Human review available for complex issues.
  
  required_domains:
    - core
    - security
    - data
    - testing
    - operations
    - compliance
  
  required_controls:
    - P0: All Core, Security, Data controls
    - P1: Testing, Operations controls
    - P2: Performance, Documentation controls
```

### Verification Checklist

- [ ] Risk assessment conducted using standardized methodology
- [ ] All impact dimensions evaluated
- [ ] Risk score calculated and documented
- [ ] Risk tier assigned with justification
- [ ] Required domains identified
- [ ] Required controls identified
- [ ] Assessment reviewed by appropriate authority
- [ ] Assessment date documented
- [ ] Review date scheduled

---

## CORE-003: Human Review for High-Impact Actions

### Rule Statement

Systems making high-impact decisions must include human review before actions are executed, with documented review process and audit trail.

### High-Impact Action Categories

**Financial Actions**:
- Transactions above defined thresholds
- Account changes
- Payment processing
- Refund processing
- Credit decisions

**Healthcare Actions**:
- Medical recommendations
- Triage decisions
- Treatment suggestions
- Diagnosis support
- Medication recommendations

**Legal Actions**:
- Legal advice
- Compliance decisions
- Contract review
- Regulatory interpretations
- Audit decisions

**Employment Actions**:
- Hiring decisions
- Performance evaluations
- Termination recommendations
- Compensation decisions
- Promotion recommendations

**Access Control Actions**:
- Privilege changes
- Permission grants
- Access revocations
- Security policy changes
- User role changes

**Data Actions**:
- Data deletion
- Data modification
- Data export
- Data sharing
- Retention changes

### Human Review Implementation

**Review Workflow**:
```yaml
review_workflow:
  trigger: "High-impact action requested"
  steps:
    - step: 1
      action: "Validate request"
      description: "Verify request is authorized and complete"
      timeout: "5 minutes"
    
    - step: 2
      action: "Route to reviewer"
      description: "Send to appropriate human reviewer"
      timeout: "15 minutes"
    
    - step: 3
      action: "Review decision"
      description: "Reviewer examines action and context"
      timeout: "1 hour"
    
    - step: 4
      action: "Approve or reject"
      description: "Reviewer makes decision with rationale"
      timeout: "15 minutes"
    
    - step: 5
      action: "Execute or notify"
      description: "Execute approved action or notify requester of rejection"
      timeout: "5 minutes"
```

**Review SLAs**:
```yaml
review_slas:
  critical:
    response_time: "15 minutes"
    resolution_time: "1 hour"
    escalation: "Immediate to manager"
  
  high:
    response_time: "1 hour"
    resolution_time: "4 hours"
    escalation: "After 2 hours"
  
  medium:
    response_time: "4 hours"
    resolution_time: "24 hours"
    escalation: "After 8 hours"
  
  low:
    response_time: "24 hours"
    resolution_time: "72 hours"
    escalation: "After 48 hours"
```

### Audit Trail Requirements

**Audit Log Fields**:
```yaml
audit_fields:
  - field: "action_id"
    description: "Unique identifier for the action"
    type: "uuid"
  
  - field: "timestamp"
    description: "When the action was requested"
    type: "iso8601"
  
  - field: "requester"
    description: "Who requested the action"
    type: "string"
  
  - field: "action_type"
    description: "Type of action requested"
    type: "string"
  
  - field: "action_details"
    description: "Details of the action"
    type: "object"
  
  - field: "reviewer"
    description: "Who reviewed the action"
    type: "string"
  
  - field: "review_timestamp"
    description: "When the review occurred"
    type: "iso8601"
  
  - field: "decision"
    description: "Approved or rejected"
    type: "enum"
  
  - field: "rationale"
    description: "Reason for the decision"
    type: "string"
  
  - field: "execution_timestamp"
    description: "When the action was executed"
    type: "iso8601"
```

### Verification Checklist

- [ ] High-impact actions identified in system design
- [ ] Human review workflow implemented
- [ ] Review SLAs defined and documented
- [ ] Review routing configured
- [ ] Audit trail implemented
- [ ] Reviewer training completed
- [ ] Escalation paths defined
- [ ] Review metrics tracked

---

## CORE-004: Fallback and Rollback Capability

### Rule Statement

Every AI system must have tested fallback mechanisms and documented rollback procedures, with regular testing to ensure effectiveness.

### Fallback Types

**Model Fallback**:
```yaml
model_fallback:
  primary:
    provider: "openai"
    model: "gpt-4"
    timeout: "30 seconds"
  
  fallback_1:
    provider: "anthropic"
    model: "claude-3-opus"
    trigger: "primary_timeout_or_error"
    timeout: "30 seconds"
  
  fallback_2:
    provider: "cached_response"
    trigger: "all_providers_failed"
    max_age: "1 hour"
  
  fallback_3:
    type: "graceful_degradation"
    trigger: "all_fallbacks_failed"
    response: "I'm unable to process your request right now. Please try again later."
```

**Tool Fallback**:
```yaml
tool_fallback:
  primary_tool:
    name: "database_query"
    timeout: "10 seconds"
    retry: 3
  
  fallback_tool:
    name: "cached_data"
    trigger: "primary_timeout_or_error"
    max_age: "1 hour"
  
  no_tool_response:
    trigger: "all_tools_failed"
    response: "I don't have access to that information right now."
```

**Service Fallback**:
```yaml
service_fallback:
  primary_service:
    name: "payment_service"
    timeout: "30 seconds"
    circuit_breaker:
      failure_threshold: 5
      reset_timeout: "60 seconds"
  
  fallback_service:
    name: "queued_payment"
    trigger: "circuit_breaker_open"
    queue_timeout: "5 minutes"
```

### Rollback Procedures

**Rollback Trigger Criteria**:
```yaml
rollback_triggers:
  - trigger: "evaluation_failure"
    severity: "critical"
    action: "immediate_rollback"
    notification: ["engineering", "product"]
  
  - trigger: "security_incident"
    severity: "critical"
    action: "immediate_rollback"
    notification: ["security", "engineering", "executive"]
  
  - trigger: "performance_degradation"
    severity: "high"
    action: "scheduled_rollback"
    threshold: "p95_latency > 2000ms for 5 minutes"
    notification: ["engineering", "operations"]
  
  - trigger: "error_rate_spike"
    severity: "high"
    action: "scheduled_rollback"
    threshold: "error_rate > 5% for 5 minutes"
    notification: ["engineering", "operations"]
```

**Rollback Procedure**:
```yaml
rollback_procedure:
  steps:
    - step: 1
      action: "Initiate rollback"
      command: "deploy-rollback --version <previous_version>"
      timeout: "5 minutes"
    
    - step: 2
      action: "Verify rollback"
      command: "health-check --full"
      timeout: "5 minutes"
    
    - step: 3
      action: "Monitor stability"
      duration: "15 minutes"
      metrics: ["error_rate", "latency", "availability"]
    
    - step: 4
      action: "Communicate status"
      template: "rollback_complete"
      recipients: ["stakeholders"]
    
    - step: 5
      action: "Document rollback"
      template: "rollback_report"
      fields: ["reason", "version", "timeline", "impact"]
```

### Verification Checklist

- [ ] Fallback mechanisms defined for each failure mode
- [ ] Fallback configuration documented
- [ ] Fallback tested in staging
- [ ] Fallback tested in production (canary)
- [ ] Rollback procedure documented
- [ ] Rollback tested in staging
- [ ] Rollback triggers defined
- [ ] Rollback decision authority assigned
- [ ] Rollback communication plan defined
- [ ] Rollback metrics tracked

---

## CORE-005: Model Evaluation and Benchmarking

### Rule Statement

AI systems must have evaluation suites that measure performance, safety, and quality against defined thresholds, with results documented and reviewed.

### Evaluation Suite Structure

```yaml
evaluation_suite:
  system_id: "support-assistant-001"
  version: "1.2.0"
  last_updated: "2026-06-04"
  
  suites:
    - suite_id: "safety"
      name: "Safety Evaluation"
      description: "Verify system prevents harmful outputs"
      priority: "P0"
      threshold: 0.95
      datasets:
        - name: "harmful_content"
          version: "1.0"
          samples: 1000
        - name: "prompt_injection"
          version: "1.0"
          samples: 500
    
    - suite_id: "quality"
      name: "Quality Evaluation"
      description: "Verify system produces accurate outputs"
      priority: "P0"
      threshold: 0.85
      datasets:
        - name: "task_performance"
          version: "1.0"
          samples: 2000
        - name: "instruction_following"
          version: "1.0"
          samples: 1000
    
    - suite_id: "performance"
      name: "Performance Evaluation"
      description: "Verify system meets performance SLOs"
      priority: "P1"
      thresholds:
        latency_p95: 500
        throughput: 100
        error_rate: 0.01
    
    - suite_id: "regression"
      name: "Regression Evaluation"
      description: "Verify no regressions from baseline"
      priority: "P0"
      baseline: "1.1.0"
      regression_threshold: 0.03
```

### Evaluation Results Template

```yaml
evaluation_results:
  evaluation_id: "eval-2026-06-04-001"
  system_id: "support-assistant-001"
  version: "1.2.0"
  executed_at: "2026-06-04T10:00:00Z"
  duration: "45 minutes"
  status: "pass"
  
  suite_results:
    - suite_id: "safety"
      status: "pass"
      score: 0.97
      threshold: 0.95
      tests:
        - test_id: "harmful_content_001"
          status: "pass"
          score: 0.99
        - test_id: "prompt_injection_001"
          status: "pass"
          score: 0.95
    
    - suite_id: "quality"
      status: "pass"
      score: 0.88
      threshold: 0.85
      tests:
        - test_id: "task_performance_001"
          status: "pass"
          score: 0.90
        - test_id: "instruction_following_001"
          status: "pass"
          score: 0.86
    
    - suite_id: "performance"
      status: "pass"
      metrics:
        latency_p95: 450
        throughput: 120
        error_rate: 0.005
    
    - suite_id: "regression"
      status: "pass"
      regressions: 0
      improvements: 2
  
  summary:
    total_tests: 5000
    passed: 4950
    failed: 50
    pass_rate: 0.99
    overall_status: "pass"
  
  recommendation: "Release approved"
  reviewer: "Jane Smith"
  review_date: "2026-06-04"
```

### Verification Checklist

- [ ] Evaluation policy defined
- [ ] Evaluation suites configured
- [ ] Evaluation datasets maintained
- [ ] Evaluation thresholds defined
- [ ] Evaluation automation implemented
- [ ] Evaluation reporting configured
- [ ] Evaluation results archived
- [ ] Evaluation review process defined

---

## CORE-006: Prompt Version Control

### Rule Statement

All prompts used in production must be version-controlled with change history, review process, and rollback capability.

### Prompt Register Structure

```yaml
prompt_register:
  system_id: "support-assistant-001"
  prompts:
    - prompt_id: "system_prompt_001"
      name: "Main System Prompt"
      description: "Primary system prompt for customer support"
      versions:
        - version: "1.0.0"
          created_at: "2026-01-15"
          created_by: "Jane Smith"
          status: "deprecated"
          changelog: "Initial version"
        
        - version: "1.1.0"
          created_at: "2026-03-01"
          created_by: "Jane Smith"
          status: "deprecated"
          changelog: "Added escalation instructions"
        
        - version: "1.2.0"
          created_at: "2026-06-01"
          created_by: "John Doe"
          status: "active"
          changelog: "Improved safety guardrails"
          evaluation_results:
            safety_score: 0.97
            quality_score: 0.88
      
      current_version: "1.2.0"
      owner: "Jane Smith"
      review_required: true
      rollback_available: true
```

### Prompt Change Process

```yaml
prompt_change_process:
  steps:
    - step: 1
      action: "Create change request"
      description: "Document proposed change with rationale"
      required_fields:
        - "Change description"
        - "Rationale"
        - "Expected impact"
        - "Risk assessment"
    
    - step: 2
      action: "Review change"
      description: "Review by prompt owner and security"
      reviewers:
        - "Prompt owner"
        - "Security team"
        - "Product team"
      timeout: "48 hours"
    
    - step: 3
      action: "Test change"
      description: "Run evaluation suite on new prompt"
      required_evaluations:
        - "Safety evaluation"
        - "Quality evaluation"
        - "Regression evaluation"
      pass_criteria:
        safety_score: ">= 0.95"
        quality_score: ">= 0.85"
        regressions: 0
    
    - step: 4
      action: "Deploy change"
      description: "Deploy new prompt version"
      deployment_strategy: "canary"
      canary_percentage: 10
      canary_duration: "24 hours"
    
    - step: 5
      action: "Monitor change"
      description: "Monitor for issues after deployment"
      monitoring_duration: "72 hours"
      metrics:
        - "Error rate"
        - "User feedback"
        - "Safety incidents"
    
    - step: 6
      action: "Complete rollout"
      description: "Roll out to all users if stable"
      requires_approval: true
```

### Verification Checklist

- [ ] Prompt register created and maintained
- [ ] All prompts version-controlled
- [ ] Change process documented
- [ ] Review process defined
- [ ] Evaluation required for changes
- [ ] Rollback capability tested
- [ ] Change history maintained
- [ ] Owner assigned for each prompt

---

## CORE-007: Tool Permission Boundaries

### Rule Statement

All tools available to AI systems must have defined permission boundaries with least-privilege enforcement and audit logging.

### Tool Registry Structure

```yaml
tool_registry:
  system_id: "support-assistant-001"
  tools:
    - tool_id: "database_query"
      name: "Database Query"
      description: "Query customer database"
      permissions:
        - "read:customers"
        - "read:tickets"
      restrictions:
        - "No write operations"
        - "No PII export"
        - "Rate limit: 100 requests/hour"
      human_approval: false
      audit_required: true
    
    - tool_id: "send_email"
      name: "Send Email"
      description: "Send email to customer"
      permissions:
        - "send:email"
      restrictions:
        - "Only to verified customer email"
        - "No attachments"
        - "Rate limit: 10 emails/hour"
      human_approval: true
      approval_threshold: "high_risk_content"
      audit_required: true
    
    - tool_id: "account_update"
      name: "Account Update"
      description: "Update customer account"
      permissions:
        - "write:account"
      restrictions:
        - "Only specific fields"
        - "Requires customer verification"
        - "Rate limit: 5 updates/hour"
      human_approval: true
      approval_threshold: "always"
      audit_required: true
```

### Tool Invocation Audit

```yaml
tool_audit:
  required_fields:
    - "tool_id"
    - "timestamp"
    - "user_id"
    - "input_parameters"
    - "output_result"
    - "success"
    - "duration_ms"
    - "approval_status"
    - "approver"
  
  retention: "1 year"
  alert_rules:
    - condition: "rate_limit_exceeded"
      action: "alert_security_team"
    - condition: "approval_bypass"
      action: "alert_security_team"
    - condition: "unusual_pattern"
      action: "alert_operations_team"
```

### Verification Checklist

- [ ] Tool registry created and maintained
- [ ] Permissions defined for each tool
- [ ] Restrictions documented
- [ ] Human approval requirements defined
- [ ] Audit logging implemented
- [ ] Rate limiting configured
- [ ] Tool testing completed
- [ ] Tool monitoring configured

---

## CORE-008: Audit Logging

### Rule Statement

All significant system actions must be logged with sufficient detail for forensic analysis, incident investigation, and compliance.

### Audit Log Schema

```yaml
audit_log_schema:
  required_fields:
    - field: "event_id"
      type: "uuid"
      description: "Unique event identifier"
    
    - field: "timestamp"
      type: "iso8601"
      description: "Event timestamp in UTC"
    
    - field: "event_type"
      type: "string"
      description: "Type of event"
      values:
        - "authentication"
        - "authorization"
        - "data_access"
        - "tool_invocation"
        - "configuration_change"
        - "release_decision"
        - "incident"
        - "policy_violation"
    
    - field: "user_id"
      type: "string"
      description: "User performing the action"
    
    - field: "source_ip"
      type: "string"
      description: "IP address of the source"
    
    - field: "action"
      type: "string"
      description: "Action performed"
    
    - field: "resource"
      type: "string"
      description: "Resource affected"
    
    - field: "result"
      type: "enum"
      values: ["success", "failure", "error"]
    
    - field: "correlation_id"
      type: "uuid"
      description: "Correlation ID for request tracing"
    
    - field: "details"
      type: "object"
      description: "Additional event details"
  
  optional_fields:
    - field: "session_id"
      type: "string"
    
    - field: "request_id"
      type: "string"
    
    - field: "duration_ms"
      type: "integer"
    
    - field: "error_message"
      type: "string"
```

### Log Retention Requirements

```yaml
log_retention:
  authentication_logs:
    retention: "1 year"
    storage: "immutable_store"
    access: "security_team"
  
  authorization_logs:
    retention: "1 year"
    storage: "immutable_store"
    access: "security_team"
  
  data_access_logs:
    retention: "7 years"
    storage: "immutable_store"
    access: "compliance_team"
  
  tool_invocation_logs:
    retention: "1 year"
    storage: "immutable_store"
    access: "security_team"
  
  configuration_change_logs:
    retention: "3 years"
    storage: "immutable_store"
    access: "operations_team"
  
  incident_logs:
    retention: "7 years"
    storage: "immutable_store"
    access: "security_team"
```

### Verification Checklist

- [ ] Audit logging implemented
- [ ] All required fields captured
- [ ] Log integrity protected
- [ ] Log retention configured
- [ ] Log access controlled
- [ ] Log monitoring configured
- [ ] Log alert rules configured
- [ ] Log backup configured

---

## CORE-009: Context Window Optimization

### Rule Statement

Systems should optimize context window usage to balance response quality with cost and latency, with monitoring and optimization.

### Optimization Techniques

**Prompt Optimization**:
```yaml
prompt_optimization:
  techniques:
    - technique: "remove_redundancy"
      description: "Remove duplicate or redundant information"
      impact: "10-20% token reduction"
    
    - technique: "summarize_history"
      description: "Summarize conversation history"
      impact: "30-50% token reduction"
    
    - technique: "prioritize_information"
      description: "Prioritize most relevant information"
      impact: "10-30% token reduction"
    
    - technique: "use_templates"
      description: "Use efficient prompt templates"
      impact: "10-20% token reduction"
```

**Context Management**:
```yaml
context_management:
  strategies:
    - strategy: "sliding_window"
      description: "Keep most recent N messages"
      window_size: 10
    
    - strategy: "importance_ranking"
      description: "Rank messages by importance"
      keep_top_k: 20
    
    - strategy: "summarization"
      description: "Summarize older messages"
      summarize_threshold: "older than 1 hour"
    
    - strategy: "retrieval"
      description: "Retrieve relevant context as needed"
      retrieval_threshold: "relevance > 0.7"
```

### Context Metrics

```yaml
context_metrics:
  - metric: "average_context_utilization"
    target: "> 70%"
    measurement: "tokens_used / max_tokens"
  
  - metric: "context_overflow_rate"
    target: "< 1%"
    measurement: "overflow_events / total_requests"
  
  - metric: "context_cost_per_request"
    target: "< $0.01"
    measurement: "total_cost / total_requests"
```

### Verification Checklist

- [ ] Context utilization monitored
- [ ] Optimization techniques implemented
- [ ] Cost tracking configured
- [ ] Performance impact assessed
- [ ] Optimization rules documented
- [ ] Metrics tracked over time

---

## CORE-010: Response Quality Monitoring

### Rule Statement

Systems should monitor response quality metrics to detect degradation and guide improvements, with alerting and trending.

### Quality Metrics

```yaml
quality_metrics:
  - metric: "accuracy"
    description: "Factual accuracy of responses"
    target: "> 0.90"
    measurement: "sampled_evaluation"
    frequency: "daily"
  
  - metric: "relevance"
    description: "Relevance to user query"
    target: "> 0.85"
    measurement: "sampled_evaluation"
    frequency: "daily"
  
  - metric: "coherence"
    description: "Coherence and fluency"
    target: "> 0.90"
    measurement: "sampled_evaluation"
    frequency: "daily"
  
  - metric: "safety"
    description: "Safety score"
    target: "> 0.95"
    measurement: "automated_checks"
    frequency: "continuous"
  
  - metric: "user_satisfaction"
    description: "User feedback score"
    target: "> 4.0"
    measurement: "user_feedback"
    frequency: "continuous"
```

### Quality Monitoring Configuration

```yaml
quality_monitoring:
  sampling:
    rate: 0.1  # 10% of requests
    strategy: "random"
  
  evaluation:
    method: "automated_with_human_review"
    automated_metrics: ["accuracy", "relevance", "coherence", "safety"]
    human_review_rate: 0.01  # 1% of sampled requests
  
  alerting:
    rules:
      - condition: "accuracy < 0.85"
        severity: "high"
        action: "alert_ml_team"
      
      - condition: "safety < 0.90"
        severity: "critical"
        action: "alert_security_team"
      
      - condition: "user_satisfaction < 3.5"
        severity: "medium"
        action: "alert_product_team"
  
  trending:
    period: "7d"
    comparison: "previous_7d"
    report: "weekly_quality_report"
```

### Verification Checklist

- [ ] Quality metrics defined
- [ ] Quality monitoring configured
- [ ] Sampling strategy implemented
- [ ] Alerting configured
- [ ] Trending configured
- [ ] Reporting configured
- [ ] Improvement process defined
- [ ] Metrics tracked over time
