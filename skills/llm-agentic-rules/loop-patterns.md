# Loop Patterns Skill

## Purpose

This skill provides standardized patterns for implementing agent loops in LLM and agentic systems.

## Pattern 1: Simple Task Loop

### Use Case

Completing a single task with clear success criteria.

### Diagram

```mermaid
flowchart TD
    A[Start] --> B[Initialize State]
    B --> C{Should Continue?}
    C -->|No| D[Return Result]
    C -->|Yes| E[Observe]
    E --> F[Think]
    F --> G[Act]
    G --> H[Evaluate]
    H --> I{Goal Achieved?}
    I -->|Yes| J[Return Success]
    I -->|No| K{Max Iterations?}
    K -->|Yes| L[Return Max Iterations]
    K -->|No| M[Update State]
    M --> C
```

### Configuration

```yaml
simple_loop:
  max_iterations: 10
  timeout: "5 minutes"
  stopping_conditions:
    - "goal_achieved"
    - "max_iterations_reached"
    - "timeout_reached"
```

## Pattern 2: Retry Loop

### Use Case

Tasks that may fail initially but can succeed with retries.

### Diagram

```mermaid
flowchart TD
    A[Start] --> B[Initialize Retry Counter]
    B --> C{Retry Count < Max?}
    C -->|No| D[Return Failure]
    C -->|Yes| E[Execute Task]
    E --> F{Success?}
    F -->|Yes| G[Return Success]
    F -->|No| H[Check Error Type]
    H --> I{Retryable?}
    I -->|No| J[Return Error]
    I -->|Yes| K[Wait with Backoff]
    K --> L[Increment Retry Count]
    L --> C
```

### Configuration

```yaml
retry_loop:
  max_retries: 3
  backoff:
    initial_delay: "100ms"
    max_delay: "30 seconds"
    multiplier: 2
    jitter: true
  retryable_errors:
    - "timeout"
    - "rate_limit"
    - "temporary_server_error"
```

## Pattern 3: Adaptive Loop

### Use Case

Tasks requiring strategy adjustment based on results.

### Diagram

```mermaid
flowchart TD
    A[Start] --> B[Select Initial Strategy]
    B --> C[Execute with Strategy]
    C --> D[Evaluate Result]
    D --> E{Goal Achieved?}
    E -->|Yes| F[Return Success]
    E -->|No| G[Analyze Failure]
    G --> H{Adapt Strategy?}
    H -->|Yes| I[Select New Strategy]
    H -->|No| J[Continue with Current]
    I --> K[Update State]
    J --> K
    K --> L{Max Iterations?}
    L -->|Yes| M[Return Max Iterations]
    L -->|No| C
```

### Configuration

```yaml
adaptive_loop:
  strategies:
    - "direct_approach"
    - "alternative_approach"
    - "simplified_approach"
    - "escalation"
  adaptation_threshold: 3
  max_iterations: 10
```

## Pattern 4: Multi-Goal Loop

### Use Case

Tasks with multiple objectives to complete.

### Diagram

```mermaid
flowchart TD
    A[Start] --> B[Initialize Goals]
    B --> C{Goals Remaining?}
    C -->|No| D[Return Success]
    C -->|Yes| E[Select Next Goal]
    E --> F[Execute for Goal]
    F --> G{Goal Achieved?}
    G -->|Yes| H[Mark Goal Complete]
    G -->|No| I{Max Attempts?}
    I -->|Yes| J[Mark Goal Failed]
    I -->|No| K[Retry Goal]
    H --> L[Update Progress]
    J --> L
    K --> F
    L --> C
```

### Configuration

```yaml
multi_goal_loop:
  goals:
    - name: "gather_information"
      priority: 1
      max_attempts: 3
    - name: "analyze_data"
      priority: 2
      max_attempts: 3
    - name: "generate_report"
      priority: 3
      max_attempts: 3
  completion_strategy: "all_goals"
```

## Pattern 5: Pipeline Loop

### Use Case

Sequential processing through multiple stages.

### Diagram

```mermaid
flowchart LR
    A[Input] --> B[Stage 1: Validate]
    B --> C[Stage 2: Transform]
    C --> D[Stage 3: Enrich]
    D --> E[Stage 4: Validate]
    E --> F[Stage 5: Output]
    
    B -->|Error| G[Handle Error]
    C -->|Error| G
    D -->|Error| G
    E -->|Error| G
    G --> H{Recoverable?}
    H -->|Yes| I[Retry Stage]
    H -->|No| J[Return Error]
    I --> B
```

### Configuration

```yaml
pipeline_loop:
  stages:
    - name: "validate"
      tool: "input_validator"
      timeout: "5 seconds"
    - name: "transform"
      tool: "data_transformer"
      timeout: "10 seconds"
    - name: "enrich"
      tool: "data_enricher"
      timeout: "15 seconds"
    - name: "validate_output"
      tool: "output_validator"
      timeout: "5 seconds"
    - name: "output"
      tool: "result_generator"
      timeout: "10 seconds"
  error_handling: "stage_retry"
  max_retries_per_stage: 3
```

## Pattern Selection Guide

| Pattern | Use Case | Complexity | When to Use |
|---------|----------|------------|-------------|
| Simple | Single task | Low | Clear success criteria |
| Retry | Fault-tolerant tasks | Low | Transient failures expected |
| Adaptive | Complex tasks | Medium | Strategy adjustment needed |
| Multi-goal | Multiple objectives | Medium | Multiple outcomes required |
| Pipeline | Sequential processing | Medium | Multi-stage workflows |

## Implementation Checklist

- [ ] Pattern selected based on requirements
- [ ] Stopping conditions defined
- [ ] Error handling implemented
- [ ] State management implemented
- [ ] Progress tracking implemented
- [ ] Monitoring configured
- [ ] Testing completed
- [ ] Documentation updated
