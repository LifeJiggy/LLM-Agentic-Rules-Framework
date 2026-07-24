# Loop Troubleshooting - LLM & Agentic Rules Framework

## Overview

This document provides practical solutions for common issues encountered when implementing agent loops.

## Issue 1: Loop Runs Indefinitely

### Symptoms

- Loop never completes
- No stopping condition triggered
- Resources continuously consumed
- User complains about hanging

### Root Cause

- Missing or incorrect stopping conditions
- Goal check never returns true
- Timeout not configured
- Iteration limit not set

### Resolution

#### Step 1: Debug Stopping Conditions

```python
def debug_stopping_conditions(loop_state):
    """Debug why stopping conditions are not met."""
    issues = []
    
    # Check iteration limit
    if loop_state.iteration >= loop_state.max_iterations:
        issues.append("iteration_limit_reached")
    
    # Check timeout
    elapsed = datetime.now() - loop_state.start_time
    if elapsed >= loop_state.timeout:
        issues.append("timeout_reached")
    
    # Check goal achievement
    if not loop_state.goal_achieved:
        issues.append("goal_not_achieved")
    
    # Check for infinite loop indicators
    if loop_state.iteration > 100:
        issues.append("possible_infinite_loop")
    
    return issues
```

#### Step 2: Add Debug Logging

```python
def add_debug_logging(loop):
    """Add debug logging to loop."""
    original_should_continue = loop.should_continue
    
    def debug_should_continue():
        result = original_should_continue()
        print(f"Should continue: {result}")
        print(f"Iteration: {loop.state.iteration}/{loop.state.max_iterations}")
        print(f"Elapsed: {datetime.now() - loop.state.start_time}")
        print(f"Goal achieved: {loop.state.goal_achieved}")
        return result
    
    loop.should_continue = debug_should_continue
```

#### Step 3: Fix Stopping Conditions

```yaml
stopping_conditions_fix:
  checks:
    - check: "max_iterations"
      fix: "set_max_iterations(limit=10)"
    
    - check: "timeout"
      fix: "set_timeout(minutes=5)"
    
    - check: "goal_achievement"
      fix: "verify_goal_check_function()"
    
    - check: "resource_limits"
      fix: "set_resource_limits(tokens=10000)"
  
  validation:
    - "test_with_known_completion"
    - "test_with_timeout"
    - "test_with_iteration_limit"
```

### Prevention

- Always define explicit stopping conditions
- Test stopping conditions thoroughly
- Add debug logging during development
- Monitor loop execution in production

## Issue 2: High Token Usage

### Symptoms

- Token budget exceeded
- Cost higher than expected
- Context window overflow
- Performance degradation

### Root Cause

- Unbounded context growth
- Redundant information in prompts
- Inefficient token usage
- No summarization

### Resolution

#### Step 1: Analyze Token Usage

```python
def analyze_token_usage(loop_history):
    """Analyze token usage patterns."""
    token_usage = []
    
    for entry in loop_history:
        tokens = entry.get("tokens_used", 0)
        token_usage.append(tokens)
    
    return {
        "total_tokens": sum(token_usage),
        "average_tokens": sum(token_usage) / len(token_usage) if token_usage else 0,
        "max_tokens": max(token_usage) if token_usage else 0,
        "tokens_per_iteration": token_usage
    }
```

#### Step 2: Optimize Token Usage

```yaml
token_optimization:
  strategies:
    - strategy: "context_summarization"
      description: "Summarize old context"
      implementation: "summarize_context_every_n_iterations(n=5)"
      expected_savings: "30-50%"
    
    - strategy: "selective_context"
      description: "Only include relevant context"
      implementation: "filter_context_by_relevance()"
      expected_savings: "20-40%"
    
    - strategy: "efficient_prompts"
      description: "Use concise prompts"
      implementation: "optimize_prompt_structure()"
      expected_savings: "10-30%"
    
    - strategy: "caching"
      description: "Cache repeated computations"
      implementation: "cache_tool_results()"
      expected_savings: "40-60%"
  
  monitoring:
    - metric: "tokens_per_iteration"
      target: "< 1000"
      alert: "increasing_trend"
    
    - metric: "total_tokens_per_task"
      target: "< 5000"
      alert: "exceeds_budget"
```

#### Step 3: Implement Token Limits

```python
class TokenAwareLoop:
    def __init__(self, token_budget: int):
        self.token_budget = token_budget
        self.tokens_used = 0
    
    def check_token_budget(self, tokens_needed: int) -> bool:
        """Check if token budget allows action."""
        return self.tokens_used + tokens_needed <= self.token_budget
    
    def use_tokens(self, tokens: int):
        """Record token usage."""
        self.tokens_used += tokens
        
        # Check if approaching budget
        if self.tokens_used > self.token_budget * 0.8:
            print(f"Warning: Token usage at {self.tokens_used}/{self.token_budget}")
```

### Prevention

- Set token budgets
- Monitor token usage
- Implement summarization
- Use efficient prompts
- Cache repeated computations

## Issue 3: Loop Stalls

### Symptoms

- Loop makes no progress
- Same actions repeated
- No goal advancement
- Time passes without results

### Root Cause

- Strategy not adapting
- Goal check too strict
- Resources exhausted
- Error recovery failing

### Resolution

#### Step 1: Detect Stall

```python
def detect_stall(history: list, window_size: int = 3) -> bool:
    """Detect if loop is stalling."""
    if len(history) < window_size:
        return False
    
    recent_actions = [h.get("action") for h in history[-window_size:]]
    
    # Check for repeated actions
    if len(set(recent_actions)) == 1:
        return True
    
    # Check for no progress
    recent_progress = [h.get("progress", 0) for h in history[-window_size:]]
    if len(set(recent_progress)) == 1:
        return True
    
    return False
```

#### Step 2: Recover from Stall

```yaml
stall_recovery:
  strategies:
    - strategy: "change_approach"
      description: "Try different approach"
      implementation: "switch_strategy()"
    
    - strategy: "reduce_scope"
      description: "Simplify the task"
      implementation: "simplify_goal()"
    
    - strategy: "gather更多信息"
      description: "Get more information"
      implementation: "gather_more_context()"
    
    - strategy: "escalate"
      description: "Escalate to human"
      implementation: "escalate_to_human()"
  
  triggers:
    - "same_action_3_times"
    - "no_progress_3_iterations"
    - "error_rate_increasing"
```

#### Step 3: Prevent Stalls

```python
class StallResistantLoop:
    def __init__(self):
        self.action_history = []
        self.progress_history = []
    
    def check_for_stall(self) -> bool:
        """Check for stall conditions."""
        # Check repeated actions
        if len(self.action_history) >= 3:
            if len(set(self.action_history[-3:])) == 1:
                return True
        
        # Check no progress
        if len(self.progress_history) >= 3:
            if len(set(self.progress_history[-3:])) == 1:
                return True
        
        return False
    
    def recover_from_stall(self):
        """Recover from stall."""
        # Change strategy
        self.current_strategy = self.get_alternative_strategy()
        
        # Reset history
        self.action_history = []
        self.progress_history = []
```

### Prevention

- Implement stall detection
- Have alternative strategies
- Monitor progress regularly
- Set progress thresholds

## Issue 4: Error Recovery Fails

### Symptoms

- Errors not recovered
- Loop crashes on errors
- No retry for transient errors
- Persistent errors cause failure

### Root Cause

- No error handling
- Wrong error classification
- Retry logic incorrect
- Fallback not implemented

### Resolution

#### Step 1: Analyze Error Patterns

```python
def analyze_errors(error_history: list) -> dict:
    """Analyze error patterns."""
    error_counts = {}
    error_types = {}
    
    for error in error_history:
        error_type = error.get("type", "unknown")
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        if error_type not in error_types:
            error_types[error_type] = []
        error_types[error_type].append(error)
    
    return {
        "total_errors": len(error_history),
        "error_counts": error_counts,
        "error_types": error_types,
        "most_common_error": max(error_counts, key=error_counts.get) if error_counts else None
    }
```

#### Step 2: Implement Proper Error Handling

```yaml
error_handling_fix:
  classification:
    - type: "transient"
      examples: ["timeout", "temporary_error", "rate_limit"]
      action: "retry_with_backoff"
    
    - type: "persistent"
      examples: ["authentication_error", "invalid_input"]
      action: "stop_and_report"
    
    - type: "recoverable"
      examples: ["data_validation_error", "format_error"]
      action: "fix_and_retry"
  
  retry_strategy:
    max_retries: 3
    backoff: "exponential"
    initial_delay: 0.1
    max_delay: 30
  
  fallback:
    strategy: "graceful_degradation"
    levels:
      - "full_functionality"
      - "reduced_functionality"
      - "minimal_functionality"
      - "error_message"
```

#### Step 3: Test Error Recovery

```python
def test_error_recovery():
    """Test error recovery mechanisms."""
    test_cases = [
        {"error": "timeout", "expected": "retry"},
        {"error": "rate_limit", "expected": "retry"},
        {"error": "auth_error", "expected": "stop"},
        {"error": "invalid_input", "expected": "stop"},
    ]
    
    for test in test_cases:
        result = handle_error(test["error"])
        assert result == test["expected"], f"Failed for {test['error']}"
```

### Prevention

- Classify errors properly
- Implement retry logic
- Add fallback behavior
- Test error scenarios

## Issue 5: State Corruption

### Symptoms

- State inconsistent
- Recovery fails
- Data loss
- Loop behaves unexpectedly

### Root Cause

- State not persisted
- Partial updates
- Concurrent access
- Memory corruption

### Resolution

#### Step 1: Validate State

```python
def validate_state(state: dict) -> bool:
    """Validate state integrity."""
    required_fields = ["iteration", "status", "history"]
    
    for field in required_fields:
        if field not in state:
            return False
    
    # Validate types
    if not isinstance(state["iteration"], int):
        return False
    
    if state["status"] not in ["running", "completed", "failed"]:
        return False
    
    if not isinstance(state["history"], list):
        return False
    
    return True
```

#### Step 2: Implement State Recovery

```yaml
state_recovery:
  persistence:
    frequency: "every_iteration"
    storage: "database"
    backup: "enabled"
  
  recovery:
    strategy: "resume_from_last_checkpoint"
    validation: "validate_state_integrity"
    fallback: "restart_from_beginning"
  
  integrity:
    checksum: "enabled"
    validation: "on_load"
    repair: "automatic_if_possible"
```

#### Step 3: Prevent State Issues

```python
class StateManager:
    def __init__(self):
        self.state = {}
        self.checksum = None
    
    def update_state(self, updates: dict):
        """Update state with validation."""
        # Validate updates
        if not self.validate_updates(updates):
            raise ValueError("Invalid state updates")
        
        # Apply updates
        self.state.update(updates)
        
        # Update checksum
        self.checksum = self.calculate_checksum()
    
    def save_state(self):
        """Save state with checksum."""
        state_with_checksum = {
            "state": self.state,
            "checksum": self.checksum
        }
        # Save to persistent storage
        self.persist_state(state_with_checksum)
    
    def load_state(self) -> dict:
        """Load state with validation."""
        state_with_checksum = self.load_from_storage()
        
        # Validate checksum
        if state_with_checksum["checksum"] != self.calculate_checksum():
            raise ValueError("State corrupted")
        
        return state_with_checksum["state"]
```

### Prevention

- Persist state regularly
- Validate state integrity
- Implement checksums
- Test recovery scenarios

## Diagnostic Commands

| Purpose | Command | Expected Output |
|---------|---------|-----------------|
| Check loop status | `loop --status` | Current loop state |
| View loop history | `loop --history` | Loop execution history |
| Check token usage | `loop --tokens` | Token usage statistics |
| Validate state | `loop --validate-state` | State validation results |
| Check stopping conditions | `loop --check-stopping` | Stopping condition status |

## Escalation Criteria

| Condition | Action | Contact |
|-----------|--------|---------|
| Loop runs > 1 hour | Investigate immediately | Engineering Lead |
| Token budget exceeded | Stop and optimize | ML Team |
| State corruption detected | Stop and recover | Operations Team |
| Error rate > 50% | Investigate root cause | Engineering Lead |
| Security concern | Stop immediately | Security Team |

## References

- Loop fundamentals: `loop-fundamentals.md`
- Loop best practices: `loop-best-practices.md`
- Loop anti-patterns: `loop-anti-patterns.md`
- Loop checklist: `loop-checklist.md`
- Loop examples: `loop-examples.md`
- Loop advanced: `loop-advanced.md`
