# Evaluation Troubleshooting - LLM & Agentic Rules Framework

## Overview

This document provides practical solutions for common issues encountered during evaluation of LLM and agentic systems.

## Issue 1: Flaky Evaluation Results

### Symptoms

- Evaluation passes sometimes and fails sometimes
- Same test produces different results on different runs
- No code changes between passing and failing runs
- Results vary between environments

### Root Cause

- Non-deterministic model outputs
- Network latency variations
- Resource contention
- Time-dependent behavior
- Random sampling in evaluation

### Resolution

#### Step 1: Identify Flaky Tests

```python
# Track test results over time
test_history = []

def run_test(test_id, test_func):
    result = test_func()
    test_history.append({
        'test_id': test_id,
        'result': result,
        'timestamp': datetime.now()
    })
    
    # Check for flakiness
    recent_results = [h for h in test_history if h['test_id'] == test_id][-10:]
    if len(recent_results) >= 10:
        pass_rate = sum(1 for r in recent_results if r['result']) / len(recent_results)
        if 0.1 < pass_rate < 0.9:
            print(f"Flaky test detected: {test_id} (pass rate: {pass_rate:.2%})")
```

#### Step 2: Fix Non-Determinism

```yaml
non_determinism_fixes:
  - fix: "set_temperature_zero"
    description: "Set temperature to 0 for deterministic outputs"
    implementation: "model_config.temperature = 0"
  
  - fix: "set_seed"
    description: "Set random seed for reproducibility"
    implementation: "random.seed(42); torch.manual_seed(42)"
  
  - fix: "use_golden_dataset"
    description: "Use fixed golden dataset for evaluation"
    implementation: "load_fixed_dataset('golden_dataset_v1')"
  
  - fix: "mock_external_services"
    description: "Mock external services for consistency"
    implementation: "mock_api_responses()"
```

#### Step 3: Add Retry Logic

```python
def run_test_with_retry(test_func, max_retries=3, pass_threshold=0.8):
    """Run test with retry logic for flaky tests."""
    results = []
    
    for i in range(max_retries):
        result = test_func()
        results.append(result)
        
        # Check if we have enough confidence
        if len(results) >= 3:
            pass_rate = sum(results) / len(results)
            if pass_rate >= pass_threshold:
                return True
            elif pass_rate < (1 - pass_threshold):
                return False
    
    # Final decision based on all retries
    return sum(results) / len(results) >= pass_threshold
```

### Prevention

- Set temperature to 0 for evaluation
- Use deterministic evaluation datasets
- Mock external dependencies
- Add retry logic for critical tests
- Track flaky test metrics

## Issue 2: Slow Evaluation Execution

### Symptoms

- Evaluation takes too long to complete
- CI/CD pipeline times out
- Evaluation blocks release process
- Developers skip evaluation due to time

### Root Cause

- Large test datasets
- Sequential test execution
- Inefficient test implementation
- Resource bottlenecks
- Network latency

### Resolution

#### Step 1: Optimize Test Execution

```yaml
optimization_strategies:
  - strategy: "parallel_execution"
    description: "Run tests in parallel"
    implementation: "pytest -n auto"
    expected_improvement: "50-70% faster"
  
  - strategy: "test_caching"
    description: "Cache test results for unchanged code"
    implementation: "pytest-cache"
    expected_improvement: "30-50% faster"
  
  - strategy: "dataset_sampling"
    description: "Use representative samples for quick evaluation"
    implementation: "sample_dataset(size=100)"
    expected_improvement: "60-80% faster"
  
  - strategy: "incremental_evaluation"
    description: "Only re-run affected tests"
    implementation: "detect_changed_components()"
    expected_improvement: "40-60% faster"
```

#### Step 2: Implement Parallel Evaluation

```python
import concurrent.futures
from typing import List, Callable

def run_parallel_evaluation(tests: List[Callable], max_workers: int = 4):
    """Run evaluation tests in parallel."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test): test for test in tests}
        results = {}
        
        for future in concurrent.futures.as_completed(futures):
            test = futures[future]
            try:
                result = future.result()
                results[test.__name__] = result
            except Exception as e:
                results[test.__name__] = {'error': str(e)}
    
    return results
```

#### Step 3: Optimize Dataset Size

```yaml
dataset_optimization:
  full_dataset:
    size: 10000
    use_case: "release_evaluation"
    execution_time: "30 minutes"
  
  sample_dataset:
    size: 1000
    use_case: "ci_evaluation"
    execution_time: "5 minutes"
  
  quick_dataset:
    size: 100
    use_case: "pre_commit_evaluation"
    execution_time: "30 seconds"
  
  selection_strategy:
    - "stratified_sampling"
    - "cover_all_categories"
    - "include_edge_cases"
    - "maintain_distribution"
```

### Prevention

- Use parallel execution
- Implement test caching
- Use appropriate dataset sizes
- Optimize test implementations
- Monitor execution times

## Issue 3: False Positives in Safety Evaluation

### Symptoms

- Safety evaluation flags legitimate responses as harmful
- High false positive rate in safety checks
- Legitimate content is blocked
- User complaints about over-filtering

### Root Cause

- Overly aggressive safety filters
- Poorly calibrated thresholds
- Missing context in safety checks
- Bias in safety detection models
- Insufficient training data

### Resolution

#### Step 1: Analyze False Positives

```python
def analyze_false_positives(results):
    """Analyze false positives in safety evaluation."""
    false_positives = []
    
    for result in results:
        if result['expected_safe'] and not result['detected_safe']:
            false_positives.append({
                'input': result['input'],
                'response': result['response'],
                'expected': result['expected_safe'],
                'detected': result['detected_safe'],
                'reason': result.get('detection_reason', 'unknown')
            })
    
    # Categorize false positives
    categories = {}
    for fp in false_positives:
        category = categorize_false_positive(fp)
        if category not in categories:
            categories[category] = []
        categories[category].append(fp)
    
    return categories
```

#### Step 2: Calibrate Safety Thresholds

```yaml
threshold_calibration:
  process:
    - step: "collect_labeled_data"
      description: "Collect labeled data for calibration"
      size: "1000_samples"
    
    - step: "analyze_thresholds"
      description: "Analyze different threshold values"
      thresholds: [0.8, 0.85, 0.9, 0.95, 0.99]
    
    - step: "select_optimal_threshold"
      description: "Select threshold balancing precision and recall"
      criteria: "maximize_f1_score"
    
    - step: "validate_threshold"
      description: "Validate threshold on held-out data"
      validation_size: "200_samples"
  
  metrics:
    - metric: "precision"
      description: "True positives / (True positives + False positives)"
      target: "> 0.95"
    
    - metric: "recall"
      description: "True positives / (True positives + False negatives)"
      target: "> 0.90"
    
    - metric: "f1_score"
      description: "Harmonic mean of precision and recall"
      target: "> 0.92"
```

#### Step 3: Improve Safety Detection

```yaml
improvement_strategies:
  - strategy: "context_aware_detection"
    description: "Consider context when making safety decisions"
    implementation: "analyze_conversation_context()"
  
  - strategy: "multi_model_ensemble"
    description: "Use multiple safety detection models"
    implementation: "ensemble投票()"
  
  - strategy: "human_review_for_edge_cases"
    description: "Route edge cases to human reviewers"
    implementation: "if confidence < 0.8: route_to_human()"
  
  - strategy: "continuous_learning"
    description: "Learn from false positive feedback"
    implementation: "update_model_with_feedback()"
```

### Prevention

- Calibrate thresholds regularly
- Use context-aware detection
- Implement human review for edge cases
- Monitor false positive rates
- Collect feedback on false positives

## Issue 4: Evaluation Dataset Drift

### Symptoms

- Evaluation results improve but production quality degrades
- Test data no longer represents production
- New edge cases not covered
- Historical test data becomes irrelevant

### Root Cause

- Production data distribution changes
- New use cases emerge
- Model behavior changes
- User behavior evolves
- Test data not refreshed

### Resolution

#### Step 1: Detect Dataset Drift

```python
def detect_dataset_drift(production_data, test_data, threshold=0.1):
    """Detect drift between production and test data."""
    # Calculate distribution differences
    production_stats = calculate_statistics(production_data)
    test_stats = calculate_statistics(test_data)
    
    drift_scores = {}
    for metric in production_stats:
        if metric in test_stats:
            drift = abs(production_stats[metric] - test_stats[metric])
            drift_scores[metric] = drift
    
    # Identify drifted metrics
    drifted_metrics = [m for m, d in drift_scores.items() if d > threshold]
    
    return {
        'drift_scores': drift_scores,
        'drifted_metrics': drifted_metrics,
        'has_drift': len(drifted_metrics) > 0
    }
```

#### Step 2: Refresh Test Data

```yaml
data_refresh_strategy:
  triggers:
    - trigger: "drift_detected"
      action: "refresh_dataset"
      priority: "high"
    
    - trigger: "new_use_case"
      action: "add_test_cases"
      priority: "medium"
    
    - trigger: "scheduled"
      action: "refresh_dataset"
      frequency: "monthly"
  
  refresh_process:
    - step: "sample_production_data"
      description: "Sample from production traffic"
      sample_size: "1000_requests"
      anonymization: "required"
    
    - step: "validate_samples"
      description: "Validate sample quality"
      checks:
        - "no_harmful_content"
        - "representative_distribution"
        - "properly_labeled"
    
    - step: "merge_with_existing"
      description: "Merge new samples with existing dataset"
      strategy: "replace_oldest_30%"
    
    - step: "version_dataset"
      description: "Create new dataset version"
      versioning: "semantic"
    
    - step: "validate_dataset"
      description: "Validate merged dataset"
      checks:
        - "coverage_complete"
        - "no_duplicates"
        - "quality_metrics_met"
```

#### Step 3: Monitor Dataset Quality

```yaml
dataset_monitoring:
  metrics:
    - metric: "dataset_freshness"
      description: "Age of oldest samples"
      threshold: "90_days"
      alert: "dataset_stale"
    
    - metric: "coverage_completeness"
      description: "Percentage of use cases covered"
      threshold: "90%"
      alert: "coverage_gap"
    
    - metric: "distribution_match"
      description: "Match between test and production distribution"
      threshold: "0.9"
      alert: "distribution_drift"
  
  monitoring_frequency: "weekly"
  reporting: "monthly"
```

### Prevention

- Monitor dataset drift regularly
- Refresh test data monthly
- Add new test cases for new use cases
- Version control test data
- Validate dataset quality

## Issue 5: Inconsistent Evaluation Across Environments

### Symptoms

- Evaluation passes in development but fails in CI
- Different results in staging vs production
- Environment-specific failures
- Local vs CI differences

### Root Cause

- Different model versions
- Different configurations
- Different data sources
- Different resource availability
- Network differences

### Resolution

#### Step 1: Standardize Environments

```yaml
environment_standardization:
  requirements:
    - requirement: "identical_model_version"
      description: "Use same model version across environments"
      implementation: "pin_model_version()"
    
    - requirement: "identical_configuration"
      description: "Use same configuration across environments"
      implementation: "use_configuration_management()"
    
    - requirement: "identical_test_data"
      description: "Use same test data across environments"
      implementation: "use_versioned_datasets()"
    
    - requirement: "similar_resources"
      description: "Ensure similar resource availability"
      implementation: "match_resource_specs()"
```

#### Step 2: Containerize Evaluation

```dockerfile
# Dockerfile.evaluation
FROM python:3.9-slim

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy evaluation code
COPY evaluation/ /app/evaluation/

# Copy test data
COPY test_data/ /app/test_data/

# Set environment variables
ENV MODEL_VERSION=1.2.0
ENV EVALUATION_CONFIG=/app/evaluation/config.yaml

# Run evaluation
CMD ["python", "/app/evaluation/run_evaluation.py"]
```

#### Step 3: Validate Environment Parity

```python
def validate_environment_parity():
    """Validate that evaluation environment matches expected configuration."""
    checks = []
    
    # Check model version
    model_version = get_model_version()
    checks.append({
        'check': 'model_version',
        'expected': os.environ.get('EXPECTED_MODEL_VERSION'),
        'actual': model_version,
        'passed': model_version == os.environ.get('EXPECTED_MODEL_VERSION')
    })
    
    # Check configuration
    config_hash = get_config_hash()
    checks.append({
        'check': 'configuration',
        'expected': os.environ.get('EXPECTED_CONFIG_HASH'),
        'actual': config_hash,
        'passed': config_hash == os.environ.get('EXPECTED_CONFIG_HASH')
    })
    
    # Check test data version
    test_data_version = get_test_data_version()
    checks.append({
        'check': 'test_data_version',
        'expected': os.environ.get('EXPECTED_TEST_DATA_VERSION'),
        'actual': test_data_version,
        'passed': test_data_version == os.environ.get('EXPECTED_TEST_DATA_VERSION')
    })
    
    return all(check['passed'] for check in checks)
```

### Prevention

- Standardize evaluation environments
- Containerize evaluation
- Version control all components
- Validate environment parity
- Document environment requirements

## Issue 6: Evaluation Not Catching Production Issues

### Symptoms

- Evaluation passes but production has issues
- Users report problems not detected by evaluation
- Quality degrades without evaluation noticing
- Evaluation metrics don't correlate with user experience

### Root Cause

- Evaluation coverage gaps
- Unrealistic test scenarios
- Missing edge cases
- Outdated test data
- Wrong metrics being evaluated

### Resolution

#### Step 1: Analyze Production Issues

```python
def analyze_production_issues(issues, evaluation_results):
    """Analyze why evaluation didn't catch production issues."""
    missed_issues = []
    
    for issue in issues:
        # Check if issue was covered by evaluation
        covered = check_evaluation_coverage(issue, evaluation_results)
        
        if not covered:
            missed_issues.append({
                'issue': issue,
                'reason': 'not_covered_by_evaluation',
                'recommendation': 'add_test_case'
            })
        else:
            # Check why evaluation passed
            analysis = analyze_false_negative(issue, evaluation_results)
            missed_issues.append({
                'issue': issue,
                'reason': analysis['reason'],
                'recommendation': analysis['recommendation']
            })
    
    return missed_issues
```

#### Step 2: Improve Evaluation Coverage

```yaml
coverage_improvement:
  process:
    - step: "gap_analysis"
      description: "Identify gaps in evaluation coverage"
      methods:
        - "production_issue_analysis"
        - "user_feedback_analysis"
        - "competitor_analysis"
    
    - step: "add_test_cases"
      description: "Add test cases for identified gaps"
      priority: "based on_impact"
    
    - step: "expand_datasets"
      description: "Expand test datasets"
      focus: "edge_cases"
    
    - step: "add_metrics"
      description: "Add metrics for identified gaps"
      focus: "user_experience"
  
  coverage_targets:
    - target: "100% of production issues"
      description: "All production issues should be covered"
    
    - target: "90% of user complaints"
      description: "Most user complaints should be caught"
    
    - target: "100% of critical paths"
      description: "All critical paths should be tested"
```

#### Step 3: Add Production Monitoring

```yaml
production_monitoring:
  metrics:
    - metric: "user_satisfaction"
      source: "feedback_surveys"
      frequency: "daily"
      alert: "score < 3.5"
    
    - metric: "error_rate"
      source: "application_logs"
      frequency: "real_time"
      alert: "rate > 1%"
    
    - metric: "response_quality"
      source: "sampled_evaluation"
      frequency: "hourly"
      alert: "score < 0.8"
  
  correlation:
    - correlation: "evaluation_vs_production"
      description: "Correlate evaluation results with production metrics"
      frequency: "weekly"
      action: "adjust_evaluation_if_correlation_low"
```

### Prevention

- Analyze production issues regularly
- Improve evaluation coverage
- Add production monitoring
- Correlate evaluation with production
- Update test cases based on findings

## Issue 7: Evaluation Cost Too High

### Symptoms

- Evaluation costs exceed budget
- API costs for evaluation are high
- Compute resources for evaluation are expensive
- Evaluation is not cost-effective

### Root Cause

- Large test datasets
- Frequent evaluation runs
- Expensive model calls
- Inefficient evaluation code
- Over-provisioned resources

### Resolution

#### Step 1: Analyze Cost Drivers

```python
def analyze_evaluation_costs(evaluation_runs):
    """Analyze cost drivers in evaluation."""
    cost_breakdown = {
        'api_calls': 0,
        'compute': 0,
        'storage': 0,
        'network': 0
    }
    
    for run in evaluation_runs:
        cost_breakdown['api_calls'] += run.get('api_cost', 0)
        cost_breakdown['compute'] += run.get('compute_cost', 0)
        cost_breakdown['storage'] += run.get('storage_cost', 0)
        cost_breakdown['network'] += run.get('network_cost', 0)
    
    # Identify top cost drivers
    sorted_costs = sorted(cost_breakdown.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total_cost': sum(cost_breakdown.values()),
        'breakdown': cost_breakdown,
        'top_drivers': sorted_costs[:3]
    }
```

#### Step 2: Optimize Evaluation Costs

```yaml
cost_optimization:
  strategies:
    - strategy: "reduce_dataset_size"
      description: "Use smaller, representative datasets"
      implementation: "stratified_sampling(size=1000)"
      expected_savings: "50-70%"
    
    - strategy: "cache_results"
      description: "Cache evaluation results for unchanged components"
      implementation: "cache_evaluation_results()"
      expected_savings: "30-50%"
    
    - strategy: "use_smaller_models"
      description: "Use smaller models for evaluation where appropriate"
      implementation: "use_evaluation_model()"
      expected_savings: "40-60%"
    
    - strategy: "optimize_code"
      description: "Optimize evaluation code for efficiency"
      implementation: "profile_and_optimize()"
      expected_savings: "20-40%"
    
    - strategy: "scheduled_evaluation"
      description: "Run evaluation only when needed"
      implementation: "conditional_evaluation()"
      expected_savings: "30-50%"
```

#### Step 3: Set Cost Budgets

```yaml
cost_budgets:
  monthly_budget: 1000
  alerts:
    - threshold: 80%
      action: "alert_ml_team"
    - threshold: 100%
      action: "block_evaluation"
  
  cost_tracking:
    - metric: "cost_per_evaluation"
      target: "< $10"
    
    - metric: "monthly_total_cost"
      target: "< $1000"
    
    - metric: "cost_per_test"
      target: "< $0.01"
```

### Prevention

- Set cost budgets
- Monitor costs regularly
- Optimize evaluation efficiency
- Use appropriate dataset sizes
- Cache evaluation results

## Diagnostic Commands

| Purpose | Command | Expected Output |
|---------|---------|-----------------|
| Check evaluation status | `evaluate --status` | Current evaluation state |
| View evaluation logs | `evaluate --logs` | Evaluation execution logs |
| Check dataset version | `evaluate --dataset-version` | Current dataset version |
| Validate environment | `evaluate --validate-env` | Environment validation results |
| Check cost usage | `evaluate --costs` | Cost breakdown report |

## Escalation Criteria

| Condition | Action | Contact |
|-----------|--------|---------|
| Evaluation fails for > 24 hours | Escalate to ML Lead | ML Lead |
| Safety evaluation fails | Immediate escalation | Security Team |
| Cost exceeds budget by > 50% | Escalate to Finance | Finance Team |
| Dataset drift detected | Escalate to Data Team | Data Team |
| Environment inconsistency | Escalate to Operations | Operations Team |

## References

- Evaluation fundamentals: `evaluation-fundamentals.md`
- Evaluation best practices: `evaluation-best-practices.md`
- Evaluation anti-patterns: `evaluation-anti-patterns.md`
- Evaluation checklist: `evaluation-checklist.md`
- Evaluation examples: `evaluation-examples.md`
- Evaluation advanced: `evaluation-advanced.md`
