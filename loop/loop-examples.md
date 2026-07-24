# Loop Examples - LLM & Agentic Rules Framework

## Overview

This document provides practical implementation examples for agent loops in LLM and agentic systems.

## Example 1: Simple Task Completion Loop

### Context

**When to Use**: Completing a single task with clear success criteria

**Goal**: Complete a specific task and return result

### Implementation

```python
from typing import Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class LoopState:
    iteration: int
    max_iterations: int
    start_time: datetime
    timeout: timedelta
    goal: str
    history: list
    status: str

class SimpleTaskLoop:
    def __init__(
        self,
        task_func: Callable,
        goal_check: Callable,
        max_iterations: int = 10,
        timeout_minutes: int = 5
    ):
        self.task_func = task_func
        self.goal_check = goal_check
        self.max_iterations = max_iterations
        self.timeout = timedelta(minutes=timeout_minutes)
        self.state = None
    
    def execute(self, goal: str) -> dict:
        """Execute the simple task loop."""
        self.state = LoopState(
            iteration=0,
            max_iterations=self.max_iterations,
            start_time=datetime.now(),
            timeout=self.timeout,
            goal=goal,
            history=[],
            status="running"
        )
        
        while self.should_continue():
            self.state.iteration += 1
            
            try:
                # Execute task
                result = self.task_func(goal, self.state.history)
                
                # Record in history
                self.state.history.append({
                    "iteration": self.state.iteration,
                    "action": "task_execution",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Check if goal achieved
                if self.goal_check(result, goal):
                    self.state.status = "completed"
                    return {
                        "status": "completed",
                        "iterations": self.state.iteration,
                        "result": result,
                        "history": self.state.history
                    }
                
            except Exception as e:
                # Record error
                self.state.history.append({
                    "iteration": self.state.iteration,
                    "action": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Loop ended without achieving goal
        self.state.status = "max_iterations_exceeded"
        return {
            "status": "max_iterations_exceeded",
            "iterations": self.state.iteration,
            "result": None,
            "history": self.state.history
        }
    
    def should_continue(self) -> bool:
        """Check if loop should continue."""
        # Check iteration limit
        if self.state.iteration >= self.state.max_iterations:
            return False
        
        # Check timeout
        elapsed = datetime.now() - self.state.start_time
        if elapsed >= self.state.timeout:
            return False
        
        # Check status
        if self.state.status != "running":
            return False
        
        return True

# Example usage
def task_function(goal: str, history: list) -> dict:
    """Example task function."""
    return {"success": True, "data": f"Completed: {goal}"}

def goal_check(result: dict, goal: str) -> bool:
    """Check if goal is achieved."""
    return result.get("success", False)

# Run the loop
loop = SimpleTaskLoop(
    task_func=task_function,
    goal_check=goal_check,
    max_iterations=5,
    timeout_minutes=2
)

result = loop.execute("Complete the analysis")
print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
```

### Expected Outcome

- Loop executes task repeatedly
- Goal check determines completion
- Returns result and history
- Handles timeout and iteration limits

### Verification

- [ ] Loop executes correctly
- [ ] Goal check works
- [ ] Timeout enforced
- [ ] Iteration limit enforced
- [ ] History recorded
- [ ] Status reported correctly

## Example 2: Retry Loop with Backoff

### Context

**When to Use**: Tasks that may fail initially but can succeed with retries

**Goal**: Complete task despite transient failures

### Implementation

```python
import time
import random
from typing import Any, Callable, List
from dataclasses import dataclass
from enum import Enum

class ErrorType(Enum):
    TRANSIENT = "transient"
    PERSISTENT = "persistent"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"

@dataclass
class RetryConfig:
    max_retries: int
    initial_delay: float
    max_delay: float
    multiplier: float
    retryable_errors: List[ErrorType]

class RetryLoop:
    def __init__(self, retry_config: RetryConfig):
        self.config = retry_config
        self.retry_count = 0
        self.history = []
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> dict:
        """Execute function with retry logic."""
        last_error = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Record success
                self.history.append({
                    "attempt": attempt + 1,
                    "status": "success",
                    "result": result
                })
                
                return {
                    "status": "success",
                    "result": result,
                    "attempts": attempt + 1,
                    "history": self.history
                }
                
            except Exception as e:
                last_error = e
                error_type = self.classify_error(e)
                
                # Record error
                self.history.append({
                    "attempt": attempt + 1,
                    "status": "error",
                    "error_type": error_type.value,
                    "error_message": str(e)
                })
                
                # Check if retryable
                if error_type not in self.config.retryable_errors:
                    break
                
                # Check if we have retries left
                if attempt == self.config.max_retries:
                    break
                
                # Calculate delay with exponential backoff
                delay = self.calculate_delay(attempt)
                time.sleep(delay)
        
        # All retries failed
        return {
            "status": "failed",
            "error": str(last_error),
            "attempts": self.config.max_retries + 1,
            "history": self.history
        }
    
    def classify_error(self, error: Exception) -> ErrorType:
        """Classify error type."""
        error_message = str(error).lower()
        
        if "rate limit" in error_message:
            return ErrorType.RATE_LIMIT
        elif "timeout" in error_message:
            return ErrorType.TIMEOUT
        elif "temporary" in error_message:
            return ErrorType.TRANSIENT
        else:
            return ErrorType.PERSISTENT
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = self.config.initial_delay * (self.config.multiplier ** attempt)
        delay = min(delay, self.config.max_delay)
        
        # Add jitter
        jitter = random.uniform(0, delay * 0.1)
        return delay + jitter

# Example usage
retry_config = RetryConfig(
    max_retries=3,
    initial_delay=0.1,
    max_delay=30,
    multiplier=2,
    retryable_errors=[ErrorType.TRANSIENT, ErrorType.RATE_LIMIT, ErrorType.TIMEOUT]
)

def unreliable_function():
    """Example function that may fail."""
    if random.random() < 0.5:
        raise Exception("Temporary error")
    return {"success": True}

retry_loop = RetryLoop(retry_config)
result = retry_loop.execute_with_retry(unreliable_function)
print(f"Status: {result['status']}")
print(f"Attempts: {result['attempts']}")
```

### Expected Outcome

- Function retried on transient errors
- Exponential backoff with jitter
- Different handling for error types
- History of all attempts

### Verification

- [ ] Retry logic works correctly
- [ ] Backoff calculation correct
- [ ] Error classification works
- [ ] Max retries enforced
- [ ] History recorded
- [ ] Success/failure reported

## Example 3: Adaptive Strategy Loop

### Context

**When to Use**: Tasks requiring strategy adjustment based on results

**Goal**: Optimize approach through adaptation

### Implementation

```python
from typing import Any, Callable, Dict, List
from dataclasses import dataclass
from enum import Enum

class Strategy(Enum):
    DIRECT = "direct"
    ALTERNATIVE = "alternative"
    SIMPLIFIED = "simplified"
    ESCALATION = "escalation"

@dataclass
class AdaptiveConfig:
    strategies: List[Strategy]
    adaptation_threshold: float
    max_consecutive_failures: int

class AdaptiveLoop:
    def __init__(self, config: AdaptiveConfig):
        self.config = config
        self.current_strategy = Strategy.DIRECT
        self.consecutive_failures = 0
        self.history = []
        self.strategy_performance = {s: {"success": 0, "failure": 0} for s in Strategy}
    
    def execute(self, task_func: Callable, goal_check: Callable, goal: Any) -> dict:
        """Execute with adaptive strategy."""
        iteration = 0
        max_iterations = 10
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                # Execute with current strategy
                result = task_func(goal, self.current_strategy)
                
                # Check if goal achieved
                if goal_check(result, goal):
                    return {
                        "status": "completed",
                        "strategy": self.current_strategy.value,
                        "iterations": iteration,
                        "result": result,
                        "history": self.history
                    }
                
                # Record failure
                self.record_failure()
                
                # Adapt strategy if needed
                if self.should_adapt():
                    self.adapt_strategy()
                
            except Exception as e:
                # Record error
                self.history.append({
                    "iteration": iteration,
                    "strategy": self.current_strategy.value,
                    "status": "error",
                    "error": str(e)
                })
                
                # Adapt strategy
                self.record_failure()
                if self.should_adapt():
                    self.adapt_strategy()
        
        return {
            "status": "max_iterations_exceeded",
            "iterations": iteration,
            "strategy_history": self.history
        }
    
    def should_adapt(self) -> bool:
        """Check if strategy should be adapted."""
        return self.consecutive_failures >= self.config.max_consecutive_failures
    
    def adapt_strategy(self):
        """Adapt strategy based on performance."""
        # Get next strategy
        strategy_index = self.config.strategies.index(self.current_strategy)
        if strategy_index < len(self.config.strategies) - 1:
            self.current_strategy = self.config.strategies[strategy_index + 1]
        else:
            self.current_strategy = Strategy.ESCALATION
        
        # Reset failure count
        self.consecutive_failures = 0
        
        # Record adaptation
        self.history.append({
            "action": "strategy_adaptation",
            "new_strategy": self.current_strategy.value,
            "reason": "consecutive_failures"
        })
    
    def record_failure(self):
        """Record failure and update performance."""
        self.consecutive_failures += 1
        self.strategy_performance[self.current_strategy]["failure"] += 1

# Example usage
adaptive_config = AdaptiveConfig(
    strategies=[Strategy.DIRECT, Strategy.ALTERNATIVE, Strategy.SIMPLIFIED, Strategy.ESCALATION],
    adaptation_threshold=0.3,
    max_consecutive_failures=3
)

def task_with_strategy(goal: Any, strategy: Strategy) -> dict:
    """Example task that varies by strategy."""
    return {"success": False, "strategy": strategy.value}

def check_goal(result: dict, goal: Any) -> bool:
    """Check if goal is achieved."""
    return result.get("success", False)

adaptive_loop = AdaptiveLoop(adaptive_config)
result = adaptive_loop.execute(task_with_strategy, check_goal, "complete_task")
print(f"Status: {result['status']}")
print(f"Strategy: {result.get('strategy_history', [])}")
```

### Expected Outcome

- Strategy adapts based on failures
- Performance tracked per strategy
- Escalation when all strategies fail
- History of adaptations

### Verification

- [ ] Strategy adaptation works
- [ ] Performance tracking correct
- [ ] Escalation logic works
- [ ] History recorded
- [ ] Goal check works
- [ ] Max iterations enforced

## Example Summary

| Example | Complexity | Time Required | Key Concepts |
|---------|------------|---------------|--------------|
| Simple Task Loop | Low | 30 minutes | Stopping conditions, state management, progress tracking |
| Retry Loop | Medium | 45 minutes | Backoff strategy, error classification, retry logic |
| Adaptive Loop | High | 1 hour | Strategy selection, performance tracking, adaptation |

## References

- Loop fundamentals: `loop-fundamentals.md`
- Loop best practices: `loop-best-practices.md`
- Loop anti-patterns: `loop-anti-patterns.md`
- Loop checklist: `loop-checklist.md`
- Loop troubleshooting: `loop-troubleshooting.md`
- Loop advanced: `loop-advanced.md`
