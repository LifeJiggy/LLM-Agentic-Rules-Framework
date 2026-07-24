# Loop Best Practices - LLM & Agentic Rules Framework

## Overview

This document provides recommended patterns, standards, and approaches for implementing agent loops in LLM and agentic systems.

## Best Practice 1: Define Clear Stopping Conditions

### Pattern

Always define explicit conditions for when the loop should stop.

**Stopping Conditions**:

| Condition | Description | Priority |
|-----------|-------------|----------|
| Goal achieved | Task completed successfully | High |
| Max iterations | Maximum attempts reached | High |
| Timeout | Time limit exceeded | High |
| Resource exhausted | Budget or quota exceeded | High |
| Error threshold | Too many consecutive errors | Medium |
| User intervention | User requests stop | High |
| Safety concern | Potential safety issue detected | High |

**Implementation**:

```yaml
stopping_conditions:
  goal_achieved:
    description: "Stop when primary goal is achieved"
    check: "evaluate_goal_completion()"
    priority: "high"
    action: "return_success"
  
  max_iterations:
    description: "Stop when maximum iterations reached"
    check: "iteration >= max_iterations"
    max_iterations: 10
    priority: "high"
    action: "return_max_iterations_exceeded"
  
  timeout:
    description: "Stop when timeout reached"
    check: "elapsed_time >= timeout"
    timeout: "5 minutes"
    priority: "high"
    action: "return_timeout"
  
  resource_exhausted:
    description: "Stop when resources exhausted"
    checks:
      - "tokens_used >= token_budget"
      - "api_calls >= api_call_limit"
      - "cost >= cost_budget"
    priority: "high"
    action: "return_resource_exhausted"
  
  error_threshold:
    description: "Stop when too many errors"
    check: "consecutive_errors >= error_threshold"
    error_threshold: 3
    priority: "medium"
    action: "return_error_threshold"
  
  user_intervention:
    description: "Stop when user requests"
    check: "user_stop_requested()"
    priority: "high"
    action: "return_user_stop"
  
  safety_concern:
    description: "Stop when safety issue detected"
    check: "safety_check_failed()"
    priority: "high"
    action: "return_safety_concern"
```

## Best Practice 2: Implement Progressive Backoff

### Pattern

When retrying failed actions, use progressive backoff to avoid overwhelming the system.

**Backoff Strategy**:

```yaml
backoff_strategy:
  initial_delay: "100ms"
  max_delay: "30 seconds"
  multiplier: 2
  jitter: true
  max_retries: 3
  
  retry_conditions:
    - "rate_limit_exceeded"
    - "temporary_server_error"
    - "network_timeout"
    - "resource_unavailable"
  
  no_retry_conditions:
    - "authentication_failed"
    - "authorization_failed"
    - "invalid_input"
    - "permanent_error"
```

**Implementation**:

```python
import time
import random

def retry_with_backoff(func, max_retries=3, initial_delay=0.1, max_delay=30, multiplier=2):
    """Retry function with exponential backoff."""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise
            
            # Add jitter
            jitter = random.uniform(0, delay * 0.1)
            sleep_time = min(delay + jitter, max_delay)
            
            time.sleep(sleep_time)
            delay *= multiplier
```

## Best Practice 3: Maintain Loop State

### Pattern

Maintain comprehensive loop state for debugging, recovery, and optimization.

**State Structure**:

```yaml
loop_state:
  metadata:
    loop_id: "unique_identifier"
    started_at: "timestamp"
    last_updated: "timestamp"
    status: "running | completed | failed | stopped"
  
  iteration:
    current: "iteration_number"
    max: "maximum_iterations"
    history: "list_of_previous_iterations"
  
  context:
    goal: "current_goal"
    observations: "current_observations"
    environment: "environment_state"
  
  progress:
    completed_steps: "list_of_completed_steps"
    pending_steps: "list_of_pending_steps"
    failed_steps: "list_of_failed_steps"
  
  resources:
    tokens_used: "number"
    tokens_remaining: "number"
    api_calls: "number"
    cost: "number"
  
  errors:
    consecutive_errors: "number"
    total_errors: "number"
    error_history: "list_of_errors"
```

**State Persistence**:

```yaml
state_persistence:
  enabled: true
  frequency: "every_iteration"
  storage: "redis | database | file"
  backup: "enabled"
  recovery: "resume_from_last_checkpoint"
  
  considerations:
    - "State size limits"
    - "Persistence latency"
    - "Recovery time"
    - "Cost implications"
```

## Best Practice 4: Implement Progress Tracking

### Pattern

Track progress to detect stalls, measure efficiency, and optimize performance.

**Progress Metrics**:

```yaml
progress_metrics:
  - metric: "iteration_progress"
    description: "Progress through iterations"
    formula: "current_iteration / max_iterations"
    alert: "stuck_at_same_iteration"
  
  - metric: "goal_progress"
    description: "Progress towards goal"
    formula: "completed_subgoals / total_subgoals"
    alert: "no_progress_for_3_iterations"
  
  - metric: "resource_efficiency"
    description: "Resources used per progress"
    formula: "tokens_used / progress_made"
    alert: "efficiency_decreasing"
  
  - metric: "time_efficiency"
    description: "Time per progress"
    formula: "elapsed_time / progress_made"
    alert: "slowing_down"
```

**Stall Detection**:

```yaml
stall_detection:
  enabled: true
  criteria:
    - "no_progress_for_3_iterations"
    - "same_action_repeated_3_times"
    - "error_rate_increasing"
    - "resource_usage_increasing_without_progress"
  
  actions:
    - "log_stall_detection"
    - "attempt_alternative_strategy"
    - "reduce_scope"
    - "escalate_to_human"
```

## Best Practice 5: Implement Graceful Degradation

### Pattern

When resources are limited or errors occur, degrade gracefully rather than failing completely.

**Degradation Levels**:

```yaml
degradation_levels:
  level_1:
    name: "full_functionality"
    description: "All features available"
    conditions: "resources_available"
  
  level_2:
    name: "reduced_functionality"
    description: "Non-essential features disabled"
    conditions: "resources_low"
    actions:
      - "disable_caching"
      - "reduce_logging"
      - "simplify_responses"
  
  level_3:
    name: "minimal_functionality"
    description: "Only essential features"
    conditions: "resources_critical"
    actions:
      - "use_cached_responses"
      - "simplify_reasoning"
      - "reduce_output_quality"
  
  level_4:
    name: "emergency_mode"
    description: "Basic response only"
    conditions: "resources_exhausted"
    actions:
      - "return_cached_response"
      - "return_error_message"
      - "escalate_to_human"
```

## Best Practice 6: Implement Safety Mechanisms

### Pattern

Implement safety mechanisms to prevent harmful actions and ensure system integrity.

**Safety Mechanisms**:

```yaml
safety_mechanisms:
  action_validation:
    description: "Validate actions before execution"
    checks:
      - "action_within_scope"
      - "action_allowed_by_policy"
      - "action_not_harmful"
      - "action_reversible"
    on_failure: "reject_action"
  
  human_approval:
    description: "Require human approval for high-risk actions"
    criteria:
      - "irreversible_action"
      - "high_impact_action"
      - "sensitive_data_action"
      - "external_system_action"
    timeout: "5_minutes"
    on_timeout: "reject_action"
  
  audit_logging:
    description: "Log all actions for audit"
    fields:
      - "action_type"
      - "action_details"
      - "action_result"
      - "timestamp"
      - "user_context"
    retention: "1_year"
  
  rollback_capability:
    description: "Ability to undo actions"
    requirements:
      - "action_is_reversible"
      - "state_is_saved"
      - "rollback_procedure_defined"
    on_failure: "escalate_to_human"
```

## Best Practice 7: Optimize Token Usage

### Pattern

Optimize token usage to reduce cost and stay within context window limits.

**Optimization Strategies**:

```yaml
token_optimization:
  strategies:
    - strategy: "context_summarization"
      description: "Summarize context to reduce tokens"
      implementation: "summarize_every_n_iterations(n=5)"
      savings: "30-50%"
    
    - strategy: "selective_context"
      description: "Only include relevant context"
      implementation: "filter_context_by_relevance()"
      savings: "20-40%"
    
    - strategy: "efficient_prompts"
      description: "Use concise prompts"
      implementation: "optimize_prompt_structure()"
      savings: "10-30%"
    
    - strategy: "caching"
      description: "Cache repeated computations"
      implementation: "cache_tool_results()"
      savings: "40-60%"
  
  monitoring:
    - metric: "tokens_per_iteration"
      target: "< 1000"
      alert: "increasing_trend"
    
    - metric: "total_tokens_per_task"
      target: "< 5000"
      alert: "exceeds_budget"
    
    - metric: "token_efficiency"
      description: "Progress per token"
      target: "increasing"
      alert: "decreasing_trend"
```

## Best Practice Documentation

### Loop Configuration Template

```yaml
loop_configuration:
  loop_id: string
  loop_type: simple | retry | adaptive | multi_goal
  description: string
  
  stopping_conditions:
    goal_achieved: boolean
    max_iterations: integer
    timeout: string
    resource_limits: object
  
  error_handling:
    max_retries: integer
    backoff_strategy: object
    fallback_behavior: string
  
  state_management:
    persistence: boolean
    checkpoint_frequency: string
    recovery_strategy: string
  
  monitoring:
    metrics: [list]
    alerts: [list]
    logging: object
```

### Loop Execution Report Template

```yaml
loop_execution_report:
  loop_id: string
  execution_id: string
  started_at: string
  completed_at: string
  status: success | failed | stopped
  
  summary:
    total_iterations: integer
    goal_achieved: boolean
    duration: string
    tokens_used: integer
    cost: number
  
  iterations:
    - iteration: integer
      action: string
      result: string
      duration: string
      tokens_used: integer
  
  errors:
    - error_type: string
      message: string
      iteration: integer
      recovered: boolean
  
  recommendations:
    - category: string
      recommendation: string
      priority: string
```

## References

- Loop fundamentals: `loop-fundamentals.md`
- Loop anti-patterns: `loop-anti-patterns.md`
- Loop checklist: `loop-checklist.md`
- Loop examples: `loop-examples.md`
- Loop troubleshooting: `loop-troubleshooting.md`
- Loop advanced: `loop-advanced.md`
