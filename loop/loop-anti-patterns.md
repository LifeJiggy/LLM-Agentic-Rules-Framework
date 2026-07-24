# Loop Anti-Patterns - LLM & Agentic Rules Framework

## Overview

This document describes common mistakes, failure modes, and dangerous approaches to avoid when implementing agent loops.

## Anti-Pattern 1: Infinite Loop

### Description

Loop without proper stopping conditions that runs indefinitely.

### Why It Fails

- Consumes resources indefinitely
- Never completes the task
- Blocks other operations
- Causes system instability

### Warning Signs

- No maximum iteration limit
- No timeout configured
- No goal completion check
- Loop runs for extended periods

### Correct Approach

```yaml
loop_with_stopping:
  stopping_conditions:
    - "goal_achieved"
    - "max_iterations_reached"
    - "timeout_reached"
    - "resource_exhausted"
    - "user_stop_requested"
  
  max_iterations: 10
  timeout: "5 minutes"
  
  validation:
    - "check_stopping_conditions_every_iteration"
    - "log_iteration_count"
    - "alert_on_high_iteration_count"
```

## Anti-Pattern 2: No Error Handling

### Description

Loop without error handling or recovery mechanisms.

### Why It Fails

- Transient errors cause immediate failure
- No retry for temporary issues
- System crashes on errors
- No graceful degradation

### Warning Signs

- No try-catch blocks
- No retry logic
- No error logging
- No fallback behavior

### Correct Approach

```yaml
error_handling:
  retry:
    max_retries: 3
    backoff: "exponential"
    initial_delay: "100ms"
    max_delay: "30 seconds"
  
  fallback:
    strategy: "graceful_degradation"
    levels:
      - "full_functionality"
      - "reduced_functionality"
      - "minimal_functionality"
      - "emergency_mode"
  
  escalation:
    conditions:
      - "unrecoverable_error"
      - "safety_concern"
      - "resource_exhausted"
    action: "escalate_to_human"
  
  logging:
    enabled: true
    fields: ["error_type", "message", "iteration", "timestamp"]
```

## Anti-Pattern 3: Unbounded Growth

### Description

Loop state grows without bounds, exceeding memory or context limits.

### Why It Fails

- Memory exhaustion
- Context window overflow
- Performance degradation
- System crashes

### Warning Signs

- History grows indefinitely
- No state pruning
- No summarization
- Memory usage increasing

### Correct Approach

```yaml
state_management:
  history:
    max_size: 100
    pruning_strategy: "keep_last_n"
    summarization: "enabled"
  
  context:
    max_tokens: 4000
    summarization_threshold: 3000
    summarization_strategy: "sliding_window"
  
  state:
    persistence: "checkpoint_every_5_iterations"
    compression: "enabled"
    archival: "move_old_state_to_archive"
  
  monitoring:
    - metric: "state_size"
      alert: "state_size > 80% of limit"
    - metric: "memory_usage"
      alert: "memory > 80% of available"
```

## Anti-Pattern 4: No Progress Tracking

### Description

Loop without progress measurement or stall detection.

### Why It Fails

- Cannot detect stalls
- Cannot measure efficiency
- Cannot optimize performance
- Cannot provide user feedback

### Warning Signs

- No progress metrics
- No stall detection
- No efficiency measurement
- No user feedback

### Correct Approach

```yaml
progress_tracking:
  metrics:
    - metric: "iteration_progress"
      formula: "current_iteration / max_iterations"
    
    - metric: "goal_progress"
      formula: "completed_subgoals / total_subgoals"
    
    - metric: "resource_efficiency"
      formula: "tokens_used / progress_made"
    
    - metric: "time_efficiency"
      formula: "elapsed_time / progress_made"
  
  stall_detection:
    enabled: true
    criteria:
      - "no_progress_for_3_iterations"
      - "same_action_repeated_3_times"
      - "error_rate_increasing"
    actions:
      - "log_stall"
      - "attempt_alternative"
      - "escalate_if_persistent"
  
  user_feedback:
    frequency: "every_3_iterations"
    content:
      - "current_progress"
      - "estimated_completion"
      - "resources_used"
```

## Anti-Pattern 5: Rigid Strategy

### Description

Loop that doesn't adapt strategy based on results or conditions.

### Why It Fails

- Cannot handle changing conditions
- Cannot learn from failures
- Cannot optimize performance
- Stuck in suboptimal approaches

### Warning Signs

- Same approach regardless of results
- No strategy adaptation
- No learning from failures
- No optimization

### Correct Approach

```yaml
adaptive_strategy:
  enabled: true
  
  adaptation_triggers:
    - trigger: "failure_threshold_reached"
      action: "switch_strategy"
    
    - trigger: "progress_stalled"
      action: "try_alternative"
    
    - trigger: "resource_usage_high"
      action: "optimize_approach"
    
    - trigger: "success_rate_low"
      action: "revise_strategy"
  
  strategies:
    - strategy: "direct_approach"
      conditions: ["initial_strategy", "progress_good"]
    
    - strategy: "alternative_approach"
      conditions: ["direct_failed", "alternative_available"]
    
    - strategy: "simplified_approach"
      conditions: ["resources_low", "complexity_high"]
    
    - strategy: "escalation"
      conditions: ["all_strategies_failed", "safety_concern"]
```

## Anti-Pattern 6: Ignoring Resource Limits

### Description

Loop that doesn't respect resource constraints (tokens, API calls, cost).

### Why It Fails

- Exceeds budget
- Hits rate limits
- Consumes excessive resources
- Causes cost overruns

### Warning Signs

- No token tracking
- No API call counting
- No cost monitoring
- No budget alerts

### Correct Approach

```yaml
resource_management:
  token_budget:
    total: 10000
    per_iteration: 1000
    alert_threshold: 80%
    action_on_exceed: "graceful_degradation"
  
  api_calls:
    total: 20
    per_minute: 10
    alert_threshold: 80%
    action_on_exceed: "wait_or_degrade"
  
  cost_budget:
    total: "$0.10"
    per_task: "$0.05"
    alert_threshold: 80%
    action_on_exceed: "reduce_quality"
  
  monitoring:
    frequency: "every_iteration"
    metrics:
      - "tokens_used"
      - "api_calls_made"
      - "cost_incurred"
    alerts:
      - "approaching_limit"
      - "limit_exceeded"
```

## Anti-Pattern 7: No User Communication

### Description

Loop without feedback or communication to the user.

### Why It Fails

- User has no visibility into progress
- User cannot provide guidance
- User satisfaction decreases
- User may interrupt unnecessarily

### Warning Signs

- No progress updates
- No status messages
- No estimated completion
- No option for user input

### Correct Approach

```yaml
user_communication:
  progress_updates:
    frequency: "every_3_iterations"
    content:
      - "current_progress"
      - "estimated_completion"
      - "resources_used"
      - "next_steps"
  
  status_messages:
    events:
      - "loop_started"
      - "strategy_changed"
      - "error_occurred"
      - "loop_completed"
    format: "concise_human_readable"
  
  user_input:
    enabled: true
    events:
      - "user_feedback_received"
      - "user_stop_requested"
      - "user_guidance_provided"
    handling: "integrate_into_loop"
```

## Anti-Pattern 8: Hardcoded Logic

### Description

Loop with hardcoded logic that cannot be configured or modified.

### Why It Fails

- Cannot adapt to different scenarios
- Cannot be tuned or optimized
- Cannot be maintained easily
- Cannot be extended

### Warning Signs

- Configuration values in code
- No external configuration
- No feature flags
- No tuning parameters

### Correct Approach

```yaml
configurable_logic:
  configuration:
    source: "external_config_file"
    reload: "on_change"
    validation: "required"
  
  parameters:
    - parameter: "max_iterations"
      default: 10
      range: [1, 100]
      description: "Maximum number of iterations"
    
    - parameter: "timeout"
      default: "5 minutes"
      range: ["10 seconds", "1 hour"]
      description: "Maximum loop duration"
    
    - parameter: "error_threshold"
      default: 3
      range: [1, 10]
      description: "Consecutive errors before stopping"
  
  feature_flags:
    - flag: "enable_adaptive_strategy"
      default: true
      description: "Enable strategy adaptation"
    
    - flag: "enable_progress_tracking"
      default: true
      description: "Enable progress tracking"
    
    - flag: "enable_user_communication"
      default: true
      description: "Enable user feedback"
```

## Anti-Pattern Summary Table

| Anti-Pattern | Risk Level | Impact | Detection Difficulty | Remediation Effort |
|--------------|------------|--------|---------------------|-------------------|
| Infinite loop | Critical | Resource exhaustion, system crash | Easy | Low |
| No error handling | High | Immediate failure on errors | Easy | Low |
| Unbounded growth | High | Memory exhaustion, context overflow | Medium | Medium |
| No progress tracking | Medium | Cannot detect stalls or optimize | Easy | Low |
| Rigid strategy | Medium | Cannot adapt to changing conditions | Medium | Medium |
| Ignoring resource limits | High | Cost overruns, rate limit hits | Easy | Low |
| No user communication | Medium | User dissatisfaction, unnecessary interruptions | Easy | Low |
| Hardcoded logic | Medium | Cannot tune or maintain | Easy | Medium |

## Prevention Strategies

### Code Review Checklist

```yaml
code_review:
  loop_review:
    - "stopping_conditions_defined"
    - "error_handling_implemented"
    - "resource_limits_enforced"
    - "progress_tracking_enabled"
    - "user_communication_implemented"
    - "configuration_externalized"
    - "logging_implemented"
    - "monitoring_configured"
```

### Automated Detection

```yaml
anti_pattern_detection:
  rules:
    - rule: "detect_infinite_loop"
      condition: "no_stopping_conditions"
      action: "block_deployment"
    
    - rule: "detect_no_error_handling"
      condition: "no_try_catch_in_loop"
      action: "alert_developer"
    
    - rule: "detect_unbounded_growth"
      condition: "state_grows_without_limit"
      action: "alert_developer"
    
    - rule: "detect_no_progress_tracking"
      condition: "no_progress_metrics"
      action: "alert_developer"
    
    - rule: "detect_hardcoded_logic"
      condition: "config_values_in_code"
      action: "alert_developer"
```

## References

- Loop fundamentals: `loop-fundamentals.md`
- Loop best practices: `loop-best-practices.md`
- Loop checklist: `loop-checklist.md`
- Loop examples: `loop-examples.md`
- Loop troubleshooting: `loop-troubleshooting.md`
- Loop advanced: `loop-advanced.md`
