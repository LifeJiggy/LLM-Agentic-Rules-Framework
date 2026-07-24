# Loop Fundamentals - LLM & Agentic Rules Framework

## Overview

This document establishes the fundamental concepts, principles, and requirements for agent loops in LLM and agentic systems. Agent loops enable systems to iteratively process, decide, and act until goals are achieved or constraints are met.

## What is an Agent Loop?

An agent loop is a cyclical process where an AI system:

1. **Observes** its environment and current state
2. **Thinks** about what to do next
3. **Acts** by taking an action
4. **Evaluates** the result of the action
5. **Decides** whether to continue or stop

This cycle repeats until:
- The goal is achieved
- A stopping condition is met
- A resource limit is reached
- An error occurs that cannot be recovered

## Why Agent Loops Matter

### Without Agent Loops

- Systems can only handle single-turn interactions
- Complex tasks require multiple user prompts
- Systems cannot self-correct errors
- Systems cannot adapt to changing conditions
- Systems cannot work autonomously

### With Agent Loops

- Systems can handle multi-step tasks
- Systems can work towards goals autonomously
- Systems can self-correct based on feedback
- Systems can adapt to changing conditions
- Systems can chain multiple actions together

## Agent Loop Components

### 1. Observation

**Purpose**: Gather information about current state and environment

**Components**:
- User input and context
- System state and history
- External data and tools
- Environmental signals

**Requirements**:
- Complete and accurate observation
- Relevant information filtering
- Context window management
- History maintenance

### 2. Thinking

**Purpose**: Process observations and decide what to do next

**Components**:
- Reasoning about current state
- Planning next actions
- Evaluating options
- Selecting best approach

**Requirements**:
- Clear reasoning process
- Goal-oriented planning
- Risk assessment
- Resource awareness

### 3. Action

**Purpose**: Execute the decided action

**Components**:
- Tool invocations
- API calls
- Data transformations
- External interactions

**Requirements**:
- Safe execution
- Error handling
- Audit logging
- Rollback capability

### 4. Evaluation

**Purpose**: Assess the result of the action

**Components**:
- Result validation
- Success criteria checking
- Error detection
- Impact assessment

**Requirements**:
- Objective evaluation
- Clear success criteria
- Failure detection
- Impact measurement

### 5. Decision

**Purpose**: Determine whether to continue or stop

**Components**:
- Goal achievement check
- Stopping condition evaluation
- Resource limit check
- Risk assessment

**Requirements**:
- Clear stopping criteria
- Resource awareness
- Risk management
- Graceful termination

## Agent Loop Types

### Simple Loop

```
while not done:
    observe()
    think()
    act()
    evaluate()
```

**Use Case**: Simple task completion

**Characteristics**:
- Linear progression
- Single goal
- Simple stopping criteria
- Low complexity

### Retry Loop

```
attempts = 0
while not done and attempts < max_attempts:
    observe()
    think()
    act()
    if success:
        done = True
    else:
        attempts += 1
```

**Use Case**: Tasks that may fail initially

**Characteristics**:
- Retry on failure
- Maximum attempt limit
- Error handling
- Backoff strategy

### Adaptive Loop

```
strategy = initial_strategy
while not done:
    observe()
    think(strategy)
    act()
    result = evaluate()
    strategy = adapt(strategy, result)
```

**Use Case**: Tasks requiring strategy adjustment

**Characteristics**:
- Strategy adaptation
- Learning from results
- Dynamic approach
- Optimization

### Multi-Goal Loop

```
goals = [goal1, goal2, goal3]
current_goal = goals[0]
while goals_remaining:
    observe()
    think(current_goal)
    act()
    if goal_achieved(current_goal):
        goals.remove(current_goal)
        current_goal = goals[0] if goals else None
```

**Use Case**: Tasks with multiple objectives

**Characteristics**:
- Multiple goals
- Goal prioritization
- Progress tracking
- Flexible completion

## Loop Control Parameters

### Maximum Iterations

```yaml
max_iterations:
  description: "Maximum number of loop iterations"
  default: 10
  range: [1, 100]
  considerations:
    - "Task complexity"
    - "Resource constraints"
    - "Time limits"
    - "User patience"
```

### Timeout

```yaml
timeout:
  description: "Maximum time for loop execution"
  default: "5 minutes"
  range: ["10 seconds", "1 hour"]
  considerations:
    - "User experience"
    - "Resource availability"
    - "Cost limits"
    - "SLA requirements"
```

### Resource Limits

```yaml
resource_limits:
  token_budget:
    description: "Maximum tokens to consume"
    default: 10000
    range: [100, 100000]
  
  api_calls:
    description: "Maximum API calls"
    default: 20
    range: [1, 100]
  
  cost_budget:
    description: "Maximum cost"
    default: "$0.10"
    range: ["$0.01", "$10.00"]
```

### Stopping Conditions

```yaml
stopping_conditions:
  goal_achieved:
    description: "Stop when goal is achieved"
    priority: "high"
  
  max_iterations_reached:
    description: "Stop when max iterations reached"
    priority: "high"
  
  timeout_reached:
    description: "Stop when timeout reached"
    priority: "high"
  
  resource_exhausted:
    description: "Stop when resources exhausted"
    priority: "high"
  
  error_occurred:
    description: "Stop when unrecoverable error occurs"
    priority: "medium"
  
  user_intervention:
    description: "Stop when user requests stop"
    priority: "high"
```

## Loop State Management

### State Components

```yaml
loop_state:
  iteration: "current iteration number"
  history: "list of previous actions and results"
  context: "current context and observations"
  goals: "current goals and progress"
  resources: "remaining resources"
  metadata: "loop metadata and timestamps"
```

### State Persistence

```yaml
state_persistence:
  required: true
  storage: "in-memory or database"
  checkpoint_frequency: "every_iteration"
  recovery: "resume_from_last_checkpoint"
  
  considerations:
    - "State size limits"
    - "Persistence latency"
    - "Recovery complexity"
    - "Cost implications"
```

## Loop Error Handling

### Error Types

| Type | Description | Handling |
|------|-------------|----------|
| Transient | Temporary failures | Retry with backoff |
| Persistent | Permanent failures | Stop and report |
| Recoverable | Can be fixed | Attempt recovery |
| Unrecoverable | Cannot be fixed | Stop and escalate |

### Error Recovery Strategies

```yaml
error_recovery:
  retry:
    description: "Retry the failed action"
    max_retries: 3
    backoff: "exponential"
  
  alternative:
    description: "Try alternative approach"
    conditions: ["transient_error", "alternative_available"]
  
  skip:
    description: "Skip failed action and continue"
    conditions: ["non_critical_action", "can_proceed_without"]
  
  rollback:
    description: "Undo previous actions and retry"
    conditions: ["partial_failure", "state_corrupted"]
  
  escalate:
    description: "Escalate to human or higher-level agent"
    conditions: ["unrecoverable_error", "safety_concern"]
```

## Loop Monitoring and Observability

### Metrics

```yaml
loop_metrics:
  performance:
    - metric: "iterations_per_task"
      description: "Average iterations to complete task"
      target: "< 10"
    
    - metric: "completion_rate"
      description: "Percentage of tasks completed"
      target: "> 90%"
    
    - metric: "average_duration"
      description: "Average loop duration"
      target: "< 5 minutes"
  
  quality:
    - metric: "goal_achievement_rate"
      description: "Percentage of goals achieved"
      target: "> 85%"
    
    - metric: "error_rate"
      description: "Percentage of iterations with errors"
      target: "< 5%"
    
    - metric: "user_satisfaction"
      description: "User satisfaction with loop performance"
      target: "> 4.0"
  
  resources:
    - metric: "token_usage"
      description: "Average tokens per task"
      target: "< 5000"
    
    - metric: "cost_per_task"
      description: "Average cost per task"
      target: "< $0.05"
```

### Logging

```yaml
loop_logging:
  required_fields:
    - "loop_id"
    - "iteration"
    - "action"
    - "result"
    - "timestamp"
    - "duration"
    - "tokens_used"
  
  optional_fields:
    - "error_message"
    - "retry_count"
    - "strategy_used"
    - "confidence_score"
  
  retention: "30_days"
  storage: "structured_logs"
```

## Loop Anti-Patterns

### Infinite Loop

**Anti-Pattern**: Loop without proper stopping conditions

**Why It Fails**: Consumes resources indefinitely, never completes

**Correct Approach**: Define clear stopping conditions and resource limits

### No Error Handling

**Anti-Pattern**: Loop without error handling or recovery

**Why It Fails**: Transient errors cause immediate failure

**Correct Approach**: Implement retry logic and error recovery

### Unbounded Growth

**Anti-Pattern**: Loop state grows without bounds

**Why It Fails**: Memory and context window limits exceeded

**Correct Approach**: Implement state pruning and summarization

### No Progress Tracking

**Anti-Pattern**: Loop without progress measurement

**Why It Fails**: Cannot detect stalls or measure efficiency

**Correct Approach**: Track progress metrics and detect stalls

## Loop Checklist

### Design Phase

- [ ] Loop type selected
- [ ] Stopping conditions defined
- [ ] Resource limits set
- [ ] Error handling designed
- [ ] State management planned

### Implementation Phase

- [ ] Loop logic implemented
- [ ] Stopping conditions implemented
- [ ] Resource limits enforced
- [ ] Error handling implemented
- [ ] State management implemented
- [ ] Logging implemented
- [ ] Monitoring configured

### Testing Phase

- [ ] Normal execution tested
- [ ] Error scenarios tested
- [ ] Resource limits tested
- [ ] Stopping conditions tested
- [ ] Performance tested

### Production Phase

- [ ] Monitoring active
- [ ] Alerting configured
- [ ] Logging working
- [ ] Metrics collected
- [ ] Optimization ongoing

## References

- Loop best practices: `loop-best-practices.md`
- Loop anti-patterns: `loop-anti-patterns.md`
- Loop checklist: `loop-checklist.md`
- Loop examples: `loop-examples.md`
- Loop troubleshooting: `loop-troubleshooting.md`
- Loop advanced: `loop-advanced.md`
