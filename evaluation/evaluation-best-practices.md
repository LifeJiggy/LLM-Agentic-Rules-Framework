# Evaluation Best Practices - LLM & Agentic Rules Framework

## Overview

This document provides recommended patterns, standards, and approaches for evaluating LLM and agentic systems.

## Best Practice 1: Layered Evaluation Strategy

### Pattern

Implement evaluation at multiple layers, from unit tests to full system evaluation.

**Layers**:

| Layer | Scope | Frequency | Duration |
|-------|-------|-----------|----------|
| Unit | Individual components | Every commit | < 5 min |
| Integration | Component interactions | Every PR | < 15 min |
| System | Full system behavior | Every release | < 30 min |
| Production | Live system monitoring | Continuous | Real-time |

**Benefits**:
- Early detection of issues
- Fast feedback for developers
- Comprehensive coverage
- Cost-effective testing

**Implementation**:

```yaml
layered_evaluation:
  unit:
    trigger: "commit"
    tests:
      - "prompt_template_tests"
      - "tool_function_tests"
      - "validation_logic_tests"
    timeout: "5 minutes"
  
  integration:
    trigger: "pull_request"
    tests:
      - "api_endpoint_tests"
      - "database_query_tests"
      - "external_service_tests"
    timeout: "15 minutes"
    requires: ["unit"]
  
  system:
    trigger: "release_request"
    tests:
      - "safety_evaluation"
      - "quality_evaluation"
      - "performance_evaluation"
    timeout: "30 minutes"
    requires: ["integration"]
  
  production:
    trigger: "continuous"
    tests:
      - "real_user_monitoring"
      - "anomaly_detection"
      - "feedback_collection"
    timeout: "real_time"
    requires: ["system"]
```

## Best Practice 2: Evaluation Data Management

### Pattern

Maintain versioned, realistic test datasets that represent production conditions.

**Data Categories**:

| Category | Description | Size | Update Frequency |
|----------|-------------|------|------------------|
| Golden Dataset | High-quality labeled examples | 1000+ | Quarterly |
| Edge Cases | Unusual or boundary inputs | 500+ | Monthly |
| Adversarial | Attack and injection attempts | 200+ | Monthly |
| Regression | Previously failing cases | Growing | Continuous |
| Production Sample | Sampled from real traffic | 1000+ | Daily |

**Data Quality Requirements**:
- Realistic: Represents actual user inputs
- Diverse: Covers all use cases and edge cases
- Labeled: Has expected outputs or behavior
- Versioned: Tracked with metadata
- Validated: Quality checked regularly

**Implementation**:

```yaml
evaluation_data:
  golden_dataset:
    name: "golden_dataset"
    version: "2.1"
    location: "s3://eval-data/golden/"
    samples: 1500
    categories:
      - "frequently_asked_questions"
      - "technical_support"
      - "account_management"
      - "billing_inquiries"
    labels:
      - "expected_response_category"
      - "expected_sentiment"
      - "expected_action"
    quality:
      accuracy: "> 0.95"
      coverage: "all_use_cases"
      freshness: "< 90_days"
  
  adversarial_dataset:
    name: "adversarial_dataset"
    version: "1.3"
    location: "s3://eval-data/adversarial/"
    samples: 300
    categories:
      - "prompt_injection"
      - "jailbreak_attempts"
      - "data_exfiltration"
      - "harmful_content"
    labels:
      - "attack_type"
      - "expected_defense"
      - "severity"
    quality:
      coverage: "all_known_attacks"
      freshness: "< 30_days"
  
  regression_dataset:
    name: "regression_dataset"
    version: "1.0"
    location: "s3://eval-data/regression/"
    samples: "growing"
    source: "previous_failures"
    labels:
      - "failure_id"
      - "failure_date"
      - "root_cause"
      - "fix_version"
    quality:
      completeness: "all_fixed_failures"
      accuracy: "validated_fixes"
```

## Best Practice 3: Automated Evaluation Pipeline

### Pattern

Automate evaluation execution, analysis, and reporting in CI/CD pipeline.

**Pipeline Stages**:

| Stage | Activities | Output |
|-------|------------|--------|
| Prepare | Load test data, configure environment | Ready state |
| Execute | Run evaluation suites | Raw results |
| Analyze | Process results, identify failures | Analysis |
| Report | Generate reports, distribute | Reports |
| Decide | Make release decision | Decision |

**Implementation**:

```yaml
evaluation_pipeline:
  stages:
    - stage: "prepare"
      steps:
        - step: "load_test_data"
          action: "download_dataset"
          parameters:
            dataset: "evaluation_dataset"
            version: "latest"
        
        - step: "configure_environment"
          action: "setup_environment"
          parameters:
            model: "current_version"
            config: "evaluation_config"
        
        - step: "validate_setup"
          action: "verify_configuration"
          timeout: "5 minutes"
    
    - stage: "execute"
      parallel: true
      steps:
        - step: "safety_evaluation"
          action: "run_evaluation_suite"
          parameters:
            suite: "safety"
            timeout: "15 minutes"
        
        - step: "quality_evaluation"
          action: "run_evaluation_suite"
          parameters:
            suite: "quality"
            timeout: "15 minutes"
        
        - step: "performance_evaluation"
          action: "run_benchmark"
          parameters:
            benchmark: "performance"
            timeout: "10 minutes"
    
    - stage: "analyze"
      steps:
        - step: "process_results"
          action: "analyze_evaluation_results"
          inputs: ["safety_results", "quality_results", "performance_results"]
        
        - step: "identify_failures"
          action: "categorize_failures"
          inputs: ["analysis"]
        
        - step: "compare_baseline"
          action: "compare_with_baseline"
          inputs: ["analysis"]
          parameters:
            baseline: "previous_release"
    
    - stage: "report"
      steps:
        - step: "generate_report"
          action: "create_evaluation_report"
          inputs: ["analysis", "failures", "comparison"]
        
        - step: "distribute_report"
          action: "send_notification"
          inputs: ["report"]
          parameters:
            channels: ["slack", "email"]
            recipients: ["ml_team", "product"]
    
    - stage: "decide"
      steps:
        - step: "check_thresholds"
          action: "evaluate_thresholds"
          inputs: ["analysis"]
        
        - step: "make_decision"
          action: "release_decision"
          inputs: ["threshold_check", "failures"]
          parameters:
            policy: "evaluation_policy"
```

## Best Practice 4: Threshold Management

### Pattern

Define, track, and refine evaluation thresholds based on system maturity and risk.

**Threshold Strategy**:

| Maturity Level | Threshold Approach | Refinement Frequency |
|----------------|-------------------|----------------------|
| Initial | Conservative (high thresholds) | Monthly |
| Growing | Balanced (industry benchmarks) | Quarterly |
| Mature | Optimized (data-driven) | Semi-annually |

**Threshold Types**:

| Type | Description | Example |
|------|-------------|---------|
| Absolute | Fixed value | Safety score > 0.95 |
| Relative | Compared to baseline | No regression from baseline |
| Statistical | Statistical significance | p-value < 0.05 |
| Business | Business-defined | User satisfaction > 4.0 |

**Implementation**:

```yaml
threshold_management:
  thresholds:
    safety:
      absolute:
        overall_score: 0.95
        harmful_content_refusal: 0.99
        prompt_injection_resistance: 0.95
      
      relative:
        vs_baseline: "no_regression"
        regression_threshold: 0.02
    
    quality:
      absolute:
        overall_score: 0.85
        task_performance: 0.85
        coherence: 0.80
      
      relative:
        vs_baseline: "no_regression"
        regression_threshold: 0.03
    
    performance:
      absolute:
        latency_p95: 500
        throughput: 100
        error_rate: 0.01
    
    business:
      user_satisfaction: 4.0
      resolution_rate: 0.80
  
  refinement:
    frequency: "quarterly"
    process:
      - "Analyze threshold performance"
      - "Identify false positives/negatives"
      - "Review industry benchmarks"
      - "Adjust thresholds"
      - "Document changes"
```

## Best Practice 5: Failure Analysis and Remediation

### Pattern

Systematically analyze evaluation failures and track remediation to completion.

**Failure Categories**:

| Category | Description | Priority |
|----------|-------------|----------|
| Safety | Harmful content, injection, jailbreak | P0 |
| Quality | Incorrect, irrelevant, incoherent output | P1 |
| Performance | Latency, throughput, error rate | P1 |
| Regression | Degradation from baseline | P1 |
| Edge Case | Unusual input handling | P2 |

**Remediation Process**:

```yaml
failure_remediation:
  process:
    - step: "classify_failure"
      description: "Categorize and prioritize failure"
      criteria:
        - "safety_impact"
        - "user_impact"
        - "frequency"
        - "severity"
    
    - step: "investigate_root_cause"
      description: "Determine why the failure occurred"
      methods:
        - "log_analysis"
        - "input_inspection"
        - "prompt_review"
        - "model_behavior_analysis"
    
    - step: "determine_fix"
      description: "Identify appropriate fix"
      options:
        - "prompt_update"
        - "model_fine_tuning"
        - "safety_filter_update"
        - "tool_permission_change"
        - "configuration_update"
    
    - step: "implement_fix"
      description: "Implement the fix"
      requirements:
        - "code_review"
        - "testing"
        - "documentation"
    
    - step: "verify_fix"
      description: "Verify fix resolves failure"
      methods:
        - "re_run_failing_test"
        - "run_full_evaluation"
        - "regression_testing"
    
    - step: "document_resolution"
      description: "Document the failure and resolution"
      artifacts:
        - "failure_report"
        - "root_cause_analysis"
        - "fix_description"
        - "verification_results"
```

## Best Practice 6: Evaluation Monitoring and Alerting

### Pattern

Monitor evaluation metrics in production and alert on anomalies.

**Monitoring Strategy**:

| Metric | Alert Threshold | Response |
|--------|-----------------|----------|
| Safety score drop | > 5% decrease | Immediate investigation |
| Quality score drop | > 10% decrease | Investigation within 24 hours |
| Error rate spike | > 2x baseline | Immediate investigation |
| Latency increase | > 50% increase | Investigation within 24 hours |

**Implementation**:

```yaml
evaluation_monitoring:
  metrics:
    - metric: "safety_score"
      source: "automated_safety_checks"
      frequency: "hourly"
      alerts:
        - condition: "drop > 5%"
          severity: "critical"
          action: "page_security_team"
        - condition: "drop > 10%"
          severity: "critical"
          action: "page_ciso"
    
    - metric: "quality_score"
      source: "user_feedback_sampling"
      frequency: "daily"
      alerts:
        - condition: "drop > 10%"
          severity: "high"
          action: "alert_ml_team"
    
    - metric: "error_rate"
      source: "application_logs"
      frequency: "real_time"
      alerts:
        - condition: "rate > 1%"
          severity: "high"
          action: "alert_operations"
        - condition: "rate > 5%"
          severity: "critical"
          action: "page_on_call"
    
    - metric: "user_satisfaction"
      source: "feedback_surveys"
      frequency: "weekly"
      alerts:
        - condition: "score < 3.5"
          severity: "medium"
          action: "alert_product_team"
  
  dashboards:
    - name: "Evaluation Overview"
      metrics: ["safety_score", "quality_score", "error_rate"]
      refresh: "hourly"
    
    - name: "Production Health"
      metrics: ["latency", "throughput", "error_rate"]
      refresh: "real_time"
    
    - name: "User Experience"
      metrics: ["user_satisfaction", "resolution_rate"]
      refresh: "daily"
```

## Best Practice 7: Evaluation Governance

### Pattern

Establish governance for evaluation processes, including review, approval, and audit.

**Governance Structure**:

| Role | Responsibility | Authority |
|------|----------------|-----------|
| Evaluation Owner | Maintain evaluation suite | Approve test cases |
| ML Lead | Review evaluation results | Approve thresholds |
| Security Lead | Review safety evaluation | Approve safety thresholds |
| Release Manager | Make release decisions | Approve releases |
| Compliance | Audit evaluation process | Require improvements |

**Governance Process**:

```yaml
evaluation_governance:
  reviews:
    - review: "evaluation_policy_review"
      frequency: "quarterly"
      participants: ["evaluation_owner", "ml_lead", "security_lead"]
      criteria:
        - "policy currency"
        - "threshold appropriateness"
        - "coverage completeness"
        - "automation effectiveness"
    
    - review: "evaluation_results_review"
      frequency: "per_release"
      participants: ["ml_lead", "product", "release_manager"]
      criteria:
        - "threshold compliance"
        - "failure analysis"
        - "regression assessment"
        - "release recommendation"
    
    - review: "evaluation_process_audit"
      frequency: "annually"
      participants: ["compliance", "evaluation_owner"]
      criteria:
        - "process adherence"
        - "documentation completeness"
        - "evidence retention"
        - "improvement tracking"
  
  approvals:
    - approval: "threshold_change"
      approver: "ml_lead"
      criteria:
        - "justified by data"
        - "risk assessed"
        - "stakeholders informed"
    
    - approval: "test_case_addition"
      approver: "evaluation_owner"
      criteria:
        - "coverage gap addressed"
        - "test case validated"
        - "expected output defined"
    
    - approval: "evaluation_exception"
      approver: "ml_lead"
      criteria:
        - "exception justified"
        - "compensating controls defined"
        - "time-limited"
```

## Best Practice Documentation

### Evaluation Policy Template

```yaml
evaluation_policy:
  policy_id: string
  system_id: string
  version: string
  effective_date: string
  owner: string
  
  purpose: string
  scope: string
  
  requirements:
    pre_release: [list]
    continuous: [list]
  
  thresholds: object
  
  roles: object
  
  process: object
  
  governance: object
  
  exceptions: object
```

### Evaluation Report Template

```yaml
evaluation_report:
  report_id: string
  system_id: string
  version: string
  executed_at: string
  
  summary: object
  suite_results: [list]
  failures: [list]
  recommendations: [list]
  
  sign_off:
    evaluator: string
    date: string
    recommendation: string
```

## References

- Evaluation fundamentals: `evaluation-fundamentals.md`
- Evaluation anti-patterns: `evaluation-anti-patterns.md`
- Evaluation checklist: `evaluation-checklist.md`
- Evaluation examples: `evaluation-examples.md`
- Evaluation troubleshooting: `evaluation-troubleshooting.md`
- Evaluation advanced: `evaluation-advanced.md`
