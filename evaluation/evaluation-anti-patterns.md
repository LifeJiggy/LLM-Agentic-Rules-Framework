# Evaluation Anti-Patterns - LLM & Agentic Rules Framework

## Overview

This document describes common mistakes, failure modes, and dangerous approaches to avoid when evaluating LLM and agentic systems.

## Anti-Pattern 1: Evaluating Too Late

### Description

Running evaluation only at release time, after all development is complete.

### Why It Fails

- Issues discovered late are expensive to fix
- Release deadlines are missed
- Developers lose context for fixing issues
- Quality becomes a bottleneck

### Warning Signs

- Evaluation takes longer than development
- Frequent release delays due to evaluation failures
- Developers avoid running evaluation locally
- Evaluation is seen as a gate, not a process

### Correct Approach

```yaml
evaluation_timing:
  wrong: "evaluate_only_at_release"
  right: "continuous_evaluation"
  
  continuous_evaluation:
    - trigger: "commit"
      evaluation: "unit_tests"
      feedback_time: "< 5 minutes"
    
    - trigger: "pull_request"
      evaluation: "integration_tests"
      feedback_time: "< 15 minutes"
    
    - trigger: "merge_to_main"
      evaluation: "full_evaluation"
      feedback_time: "< 30 minutes"
    
    - trigger: "release_request"
      evaluation: "release_evaluation"
      feedback_time: "< 1 hour"
```

## Anti-Pattern 2: Skipping Safety Evaluation

### Description

Skipping safety evaluation due to time pressure or assuming safety is handled.

### Why It Fails

- Safety issues cause harm in production
- Legal and regulatory liability
- Reputational damage
- Loss of user trust

### Warning Signs

- Safety evaluation is "optional" in CI/CD
- Safety failures are logged but not investigated
- Safety thresholds are set very low
- Safety is not part of release criteria

### Correct Approach

```yaml
safety_evaluation:
  mandatory: true
  blocking: true
  exceptions:
    - exception: "emergency_release"
      process:
        - "run_minimal_safety_suite"
        - "document_exception"
        - "complete_full_evaluation_post_release"
        - "review_in_next_governance_meeting"
  
  no_skip_policy:
    rule: "safety_evaluation_must_pass"
    escalation: "if_safety_fails_block_release"
    override: "ciso_approval_required"
```

## Anti-Pattern 3: Using Unrealistic Test Data

### Description

Using synthetic test data that doesn't represent production conditions.

### Why It Fails

- Tests pass in development but fail in production
- Edge cases are not covered
- Real user behavior is not tested
- Quality metrics are misleading

### Warning Signs

- Test data is manually created
- Test data is months old
- Test data doesn't include edge cases
- Test data doesn't match production distribution

### Correct Approach

```yaml
test_data_strategy:
  data_sources:
    - source: "production_sample"
      description: "Sampled from real production traffic"
      refresh: "daily"
      anonymization: "required"
      size: "1000_requests_per_day"
    
    - source: "synthetic_augmentation"
      description: "Generated to fill coverage gaps"
      refresh: "monthly"
      validation: "required"
      size: "as_needed"
    
    - source: "adversarial_collection"
      description: "Attack and injection attempts"
      refresh: "monthly"
      sources:
        - "security_research"
        - "red_team_findings"
        - "incident_analysis"
      size: "200+_patterns"
  
  quality_requirements:
    - "must represent production distribution"
    - "must include edge cases"
    - "must be regularly refreshed"
    - "must be validated for accuracy"
    - "must be version controlled"
```

## Anti-Pattern 4: Ignoring Flaky Tests

### Description

Ignoring intermittently failing tests and treating them as expected.

### Why It Fails

- Flaky tests erode confidence in evaluation
- Real failures are masked by flaky test noise
- Test suite becomes unreliable
- Developers stop trusting evaluation results

### Warning Signs

- Tests sometimes pass, sometimes fail
- "Flaky" tests are disabled or ignored
- Test results vary between runs
- Developers re-run tests hoping for pass

### Correct Approach

```yaml
flaky_test_management:
  detection:
    method: "track_test_results"
    threshold: "test_fails_in_10%_of_runs"
    tracking_period: "30_days"
  
  quarantine:
    process:
      - "detect_flaky_test"
      - "move_to_quarantine_suite"
      - "create_investigation_ticket"
      - "fix_or_remove_within_30_days"
    
    quarantine_rules:
      - "do_not_block_release"
      - "track_quarantine_count"
      - "alert_when_count_increases"
  
  resolution:
    options:
      - "fix_test_instability"
      - "remove_flaky_test"
      - "replace_with_stable_test"
    
    priority: "high"
    sla: "30_days"
```

## Anti-Pattern 5: Not Tracking Trends

### Description

Looking at evaluation results in isolation without tracking trends over time.

### Why It Fails

- Gradual degradation goes undetected
- Improvements are not recognized
- Patterns are not identified
- Historical context is lost

### Warning Signs

- No historical evaluation data
- No trend analysis
- No comparison to previous versions
- No long-term metrics tracking

### Correct Approach

```yaml
trend_tracking:
  metrics:
    - metric: "safety_score"
      tracking: "per_release"
      visualization: "trend_chart"
      alerts:
        - "declining_trend"
        - "sudden_drop"
    
    - metric: "quality_score"
      tracking: "per_release"
      visualization: "trend_chart"
      alerts:
        - "declining_trend"
        - "sudden_drop"
    
    - metric: "error_rate"
      tracking: "continuous"
      visualization: "time_series"
      alerts:
        - "increasing_trend"
        - "spike"
  
  reporting:
    frequency: "weekly"
    content:
      - "trend_analysis"
      - "comparison_to_baseline"
      - "improvement_areas"
      - "regression_areas"
```

## Anti-Pattern 6: Threshold Gaming

### Description

Setting thresholds based on current performance rather than requirements.

### Why It Fails

- Thresholds become meaningless
- Quality bar is lowered instead of improved
- System degrades over time
- Compliance is not achieved

### Warning Signs

- Thresholds are frequently lowered
- Thresholds are set just above current performance
- No external benchmark comparison
- Thresholds are not reviewed

### Correct Approach

```yaml
threshold_setting:
  principles:
    - "thresholds_based_on_requirements"
    - "thresholds_not_based_on_current_performance"
    - "thresholds_reviewed_quarterly"
    - "thresholds_compared_to_industry"
  
  process:
    - step: "define_requirements"
      description: "Define quality requirements from business needs"
    
    - step: "research_benchmarks"
      description: "Research industry benchmarks"
    
    - step: "set_thresholds"
      description: "Set thresholds based on requirements and benchmarks"
    
    - step: "validate_thresholds"
      description: "Validate thresholds are achievable but challenging"
    
    - step: "document_rationale"
      description: "Document why each threshold was set"
  
  governance:
    review: "quarterly"
    approver: "ml_lead"
    criteria:
      - "justified_by_requirements"
      - "aligned_with_benchmarks"
      - "achievable_with_effort"
```

## Anti-Pattern 7: Evaluating the Wrong Things

### Description

Focusing evaluation on metrics that don't matter for the system's purpose.

### Why It Fails

- Effort is wasted on irrelevant metrics
- Important aspects are not evaluated
- Quality is misleading
- Resources are misallocated

### Warning Signs

- Evaluation focuses on easy-to-measure metrics
- Important metrics are not tracked
- Evaluation doesn't match system purpose
- Stakeholders don't trust evaluation results

### Correct Approach

```yaml
metric_selection:
  process:
    - step: "identify_stakeholder_needs"
      description: "Understand what stakeholders care about"
    
    - step: "map_to_metrics"
      description: "Map stakeholder needs to measurable metrics"
    
    - step: "prioritize_metrics"
      description: "Prioritize metrics by importance"
    
    - step: "define_collection"
      description: "Define how to collect each metric"
    
    - step: "validate_relevance"
      description: "Validate metrics are relevant and actionable"
  
  example_mapping:
    stakeholder_need: "users_get_correct_answers"
    metric: "task_performance_accuracy"
    measurement: "evaluation_on_labeled_dataset"
    target: "> 0.85"
```

## Anti-Pattern 8: One-Shot Evaluation

### Description

Running evaluation once and assuming results are permanent.

### Why It Fails

- System behavior changes over time
- Model updates affect quality
- Data drift affects performance
- New attack vectors emerge

### Warning Signs

- Evaluation run once at launch
- No continuous monitoring
- No periodic re-evaluation
- Evaluation not run after changes

### Correct Approach

```yaml
continuous_evaluation:
  triggers:
    - trigger: "code_change"
      evaluation: "regression_suite"
    
    - trigger: "prompt_change"
      evaluation: "full_evaluation_suite"
    
    - trigger: "model_update"
      evaluation: "full_evaluation_suite"
    
    - trigger: "scheduled"
      evaluation: "monitoring_evaluation"
      frequency: "daily"
    
    - trigger: "incident"
      evaluation: "targeted_evaluation"
```

## Anti-Pattern 9: No Human Evaluation

### Description

Relying solely on automated evaluation without human judgment.

### Why It Fails

- Automated metrics miss nuances
- Subjective quality is not measured
- Edge cases are not caught
- User experience is not evaluated

### Warning Signs

- All evaluation is automated
- No human review of outputs
- User feedback is not collected
- Quality is measured only by metrics

### Correct Approach

```yaml
human_evaluation:
  roles:
    - role: "quality_reviewer"
      responsibilities:
        - "review_sampled_outputs"
        - "rate_quality"
        - "identify_issues"
      frequency: "weekly"
      sample_size: "100_outputs"
    
    - role: "safety_reviewer"
      responsibilities:
        - "review_safety_failures"
        - "assess_severity"
        - "recommend_fixes"
      frequency: "per_safety_failure"
      sample_size: "all_failures"
    
    - role: "user_researcher"
      responsibilities:
        - "collect_user_feedback"
        - "conduct_user_testing"
        - "analyze_satisfaction"
      frequency: "monthly"
      sample_size: "50_users"
  
  integration:
    - "human_evaluation_informs_automated_metrics"
    - "human_feedback_validates_automated_results"
    - "human_judgment_overrides_automation_when_needed"
```

## Anti-Pattern 10: Evaluation Without Action

### Description

Running evaluation but not acting on the results.

### Why It Fails

- Evaluation becomes a waste of resources
- Issues are not fixed
- Quality does not improve
- Stakeholders lose trust

### Warning Signs

- Evaluation results are not reviewed
- Failures are not investigated
- Improvements are not implemented
- No follow-up on action items

### Correct Approach

```yaml
actionable_evaluation:
  process:
    - step: "generate_results"
      action: "create_evaluation_report"
    
    - step: "review_results"
      action: "stakeholder_review_meeting"
      frequency: "per_release"
    
    - step: "create_action_items"
      action: "document_required_actions"
    
    - step: "assign_ownership"
      action: "assign_action_items_to_individuals"
    
    - step: "track_completion"
      action: "track_action_item_status"
    
    - step: "verify_improvement"
      action: "re_evaluate_after_fixes"
  
  accountability:
    - "each_action_item_has_owner"
    - "each_action_item_has_deadline"
    - "status_tracked_weekly"
    - "overdue_items_escalated"
```

## Anti-Pattern Summary Table

| Anti-Pattern | Risk Level | Impact | Detection Difficulty | Remediation Effort |
|--------------|------------|--------|---------------------|-------------------|
| Evaluating too late | High | Release delays, expensive fixes | Easy | Medium |
| Skipping safety | Critical | Harm, liability, reputation damage | Easy | Low (just don't skip) |
| Unrealistic test data | High | False confidence, production failures | Medium | Medium |
| Ignoring flaky tests | Medium | Eroded confidence, masked failures | Easy | Low |
| Not tracking trends | Medium | Gradual degradation undetected | Medium | Low |
| Threshold gaming | High | Lowering quality bar over time | Medium | Medium |
| Evaluating wrong things | Medium | Wasted effort, missed issues | Medium | Medium |
| One-shot evaluation | High | Changes not caught | Easy | Low |
| No human evaluation | Medium | Missed nuances, poor UX | Medium | Medium |
| Evaluation without action | High | No improvement, wasted resources | Easy | Low |

## Prevention Strategies

### Automated Detection

```yaml
anti_pattern_detection:
  rules:
    - rule: "detect_late_evaluation"
      condition: "evaluation_run_after_release"
      action: "alert_evaluation_owner"
    
    - rule: "detect_skipped_safety"
      condition: "release_without_safety_evaluation"
      action: "block_release"
    
    - rule: "detect_stale_data"
      condition: "test_data_older_than_90_days"
      action: "alert_data_owner"
    
    - rule: "detect_flaky_tests"
      condition: "test_fails_in_10%_of_runs"
      action: "quarantine_test"
    
    - rule: "detect_no_trend_tracking"
      condition: "evaluation_results_not_stored"
      action: "alert_evaluation_owner"
```

### Review Checklists

```yaml
anti_pattern_review:
  pre_release:
    - "evaluation_run_before_release"
    - "safety_evaluation_not_skipped"
    - "test_data_current"
    - "flaky_tests_quarantined"
    - "trends_tracked"
    - "thresholds_not_gamed"
    - "relevant_metrics_evaluated"
    - "continuous_evaluation_configured"
    - "human_evaluation_included"
    - "action_items_created"
```

## References

- Evaluation fundamentals: `evaluation-fundamentals.md`
- Evaluation best practices: `evaluation-best-practices.md`
- Evaluation checklist: `evaluation-checklist.md`
- Evaluation examples: `evaluation-examples.md`
- Evaluation troubleshooting: `evaluation-troubleshooting.md`
- Evaluation advanced: `evaluation-advanced.md`
