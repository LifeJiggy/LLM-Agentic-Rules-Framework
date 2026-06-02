# Core Domain - Fundamentals

> Foundational principles and core concepts that every LLM/agentic system developer must understand. These fundamentals apply across all domains and serve as the foundation for all other rules.

## Overview

The core domain defines baseline engineering principles for LLM and agentic systems. Use it before specialized domain guidance so architecture, context handling, tools, state, evaluation, safety, and operations share a consistent foundation.

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [LLM Fundamentals](#llm-fundamentals)
4. [Agent Architecture Fundamentals](#agent-architecture-fundamentals)
5. [Agent Loop Fundamentals](#agent-loop-fundamentals)
6. [Context Management](#context-management)
7. [Tool Fundamentals](#tool-fundamentals)
8. [Priority Hierarchy](#priority-hierarchy)
9. [State Management Fundamentals](#state-management-fundamentals)
10. [Communication Patterns](#communication-patterns)
11. [Error Handling Fundamentals](#error-handling-fundamentals)
12. [Quality Attributes](#quality-attributes)
13. [Token Economics](#token-economics)
14. [Temperature and Sampling](#temperature-and-sampling)
15. [Prompt Structure](#prompt-structure)
16. [Agent Types](#agent-types)
17. [Memory Fundamentals](#memory-fundamentals)
18. [Tool Selection Logic](#tool-selection-logic)
19. [Evaluation Fundamentals](#evaluation-fundamentals)
20. [Security Fundamentals](#security-fundamentals)
21. [Performance Fundamentals](#performance-fundamentals)

---

## Core Principles

### 1. Single Responsibility Principle (SRP)

Every component, function, or agent should have one primary responsibility. This principle is even more critical in LLM systems where unclear boundaries lead to unpredictable behavior.

```python
# Bad: God agent
class OmnipotentAgent:
    def chat(self): ...
    def analyze(self): ...
    def execute(self): ...
    def deploy(self): ...

# Good: Specialized agents
class ChatAgent:
    def chat(self): ...
    def get_history(self): ...

class AnalysisAgent:
    def analyze(self): ...
    def generate_report(self): ...

class ExecutionAgent:
    def execute(self): ...
    def validate(self): ...
```

### 2. Don't Repeat Yourself (DRY)

Extract common patterns and reuse them across prompts, tools, and agent configurations.

```python
from string import Template

class PromptTemplate:
    CODE_GENERATION = Template("""
    You are an expert $language developer.
    Task: $task
    Requirements:
    - Write clean, idiomatic $language code
    - Include type hints where applicable
    - Add docstrings for public functions
    - Handle edge cases gracefully
    Output only the code, no explanations.
    """)
    
    @classmethod
    def render(cls, template_name, **kwargs):
        template = getattr(cls, template_name.upper(), None)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")
        return template.safe_substitute(**kwargs)
```

### 3. Keep It Simple, Stupid (KISS)

Prefer simple solutions over complex ones. Start with the simplest working solution and add complexity only when needed.

```python
# Good: Simple prompt
def summarize(text: str) -> str:
    return f"Summarize the following text in 3 bullet points:\n\n{text}"

# Bad: Over-engineered
def summarize(
    text: str,
    style: str,
    audience: str,
    tone: str,
    format: str,
    max_words: int,
    include_examples: bool,
    ...
):
    return f"""
    You are an expert summarizer with 20 years of experience...
    [100 lines of complex instructions]
    """
```

### 4. You Aren't Gonna Need It (YAGNI)

Don't build features until they're actually needed. In LLM systems, adding capabilities increases complexity and cost.

```python
class MinimalAgent:
    def __init__(self):
        self.core_tools = [ReadTool(), WriteTool()]
    
    def add_tool_if_needed(self, tool, usage_count_threshold: int = 10):
        if self._tool_request_count(tool.name) >= usage_count_threshold:
            self.core_tools.append(tool)
```

### 5. Boy Scout Rule

Always leave the code/documentation better than you found it. In LLM systems, this includes prompt refinements and agent improvements.

```python
class AgentMaintenance:
    def improve_after_failure(self, task: str, failure: Exception):
        self.failure_log.append({
            "task": task,
            "error": str(failure),
            "timestamp": datetime.now()
        })
        
        if self._similar_failures_count(task) >= 3:
            self._refine_prompt_for_task_type(task)
```

---

## LLM Fundamentals

### What Are Language Models?

Language models are probabilistic systems that predict the next token based on context. Understanding this fundamental nature is crucial for building effective applications.

**Key Properties:**

| Property | Description | Implication |
|----------|-------------|-------------|
| Probabilistic | Outputs vary with same input | Use temperature and seeds for control |
| Context-limited | Fixed token window | Manage context carefully |
| Training-dependent | Knowledge bounded by training data | May need external tools for current info |
| Pattern-matching | Recognizes and extends patterns | Use few-shot examples effectively |
| Instruction-following | Responds to directives | Write clear, specific instructions |

### How LLMs Work

```python
class LLMUnderstanding:
    """Conceptual model of how LLMs operate."""
    
    @staticmethod
    def next_token_prediction(context: str) -> str:
        """
        LLMs predict the next token given a context.
        This is fundamentally a pattern completion system.
        """
        # The model assigns probabilities to all possible next tokens
        # Top-p (nucleus) sampling selects from the most likely tokens
        # Temperature controls how deterministic the selection is
        pass
    
    @staticmethod
    def attention_mechanism():
        """
        Attention allows the model to focus on relevant parts of the input
        when generating each part of the output.
        """
        pass
```

### Model Capabilities and Limitations

```python
class ModelCapabilities:
    """Understand what models can and cannot do."""
    
    STRENGTHS = [
        "Text generation and completion",
        "Summarization and extraction",
        "Translation",
        "Question answering (from training data)",
        "Code generation",
        "Reasoning over provided context"
    ]
    
    LIMITATIONS = [
        "No real-time information without retrieval",
        "Can generate plausible but incorrect information",
        "No persistent memory across conversations",
        "Mathematical reasoning can be unreliable",
        "Long contexts may show attention degradation",
        "Biases from training data persist"
    ]
    
    @staticmethod
    def when_to_use_llm(task: str) -> bool:
        llm_tasks = ["generate", "summarize", "translate", "classify", "extract"]
        return any(keyword in task.lower() for keyword in llm_tasks)
    
    @staticmethod
    def when_to_use_code(task: str) -> bool:
        code_tasks = ["calculate", "sort", "filter", "aggregate", "validate"]
        return any(keyword in task.lower() for keyword in code_tasks)
```

---

## Agent Architecture Fundamentals

### What Is an Agent?

An agent is an autonomous system that can perceive its environment, make decisions, and take actions to achieve goals.

**Core Components:**

1. **Perception**: How the agent receives input
2. **Reasoning**: How the agent processes information
3. **Action**: How the agent affects the world
4. **Memory**: How the agent retains information
5. **Learning**: How the agent improves

### Basic Agent Structure

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.tools: List[Tool] = []
        self.memory: Optional[Memory] = None
    
    @abstractmethod
    def perceive(self, input_data: Any) -> Dict:
        """Process incoming information."""
        pass
    
    @abstractmethod
    def reason(self, perception: Dict) -> Dict:
        """Make decisions based on perception."""
        pass
    
    @abstractmethod
    def act(self, decision: Dict) -> Any:
        """Execute actions based on reasoning."""
        pass
    
    def execute(self, task: str, context: Optional[Dict] = None) -> Any:
        perception = self.perceive({"task": task, "context": context})
        decision = self.reason(perception)
        return self.act(decision)
```

### Agent Types

| Type | Description | Use Case |
|------|-------------|----------|
| Reactive | Responds to current input only | Simple chatbots |
| Deliberative | Plans before acting | Complex task execution |
| Hybrid | Combines reactive and deliberative | Most production systems |
| Learning | Improves from experience | Personalized systems |

### Agent Communication

```python
class AgentCommunication:
    """Communication patterns between agents."""
    REQUEST_RESPONSE = "request_response"
    PUBLISH_SUBSCRIBE = "publish_subscribe"
    PIPELINE = "pipeline"
    ORCHESTRATION = "orchestration"
```

---

## Agent Loop Fundamentals

The core agent loop is the fundamental execution pattern for all agentic systems.

### Standard Agent Loop

```
1. Think: Understand the task and requirements
2. Plan: Break down into actionable steps
3. Act: Execute the planned actions
4. Observe: Gather results and feedback
5. Reflect: Evaluate progress toward goal
6. Iterate: Improve if needed
```

### Loop Implementation

```python
class AgentLoop:
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.iteration_count = 0
    
    async def run(self, task: str) -> Result:
        state = InitialState(task=task)
        
        while not self._is_complete(state) and self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            
            thought = await self._think(state)
            plan = await self._plan(thought)
            action_result = await self._act(plan)
            observation = await self._observe(action_result)
            reflection = await self._reflect(observation)
            
            state = self._update_state(state, reflection)
        
        return self._finalize(state)
```

### Convergence Criteria

```python
class ConvergenceChecker:
    def __init__(self, threshold: float = 0.95, max_iterations: int = 10):
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.history: List[float] = []
    
    def is_converged(self, result: Dict) -> bool:
        score = result.get("confidence", 0.0)
        self.history.append(score)
        
        if len(self.history) >= 2:
            improvement = score - self.history[-2]
            if improvement < 0.01:
                return True
        
        return score >= self.threshold or len(self.history) >= self.max_iterations
```

---

## Context Management

### Reading Before Acting

**MANDATORY RULE:** Always read project files and understand the context before implementing any changes.

```python
class ContextAwareAgent:
    async def execute(self, task: str) -> Dict:
        context = await self._gather_context(task)
        understanding = await self._understand_requirements(task, context)
        plan = await self._create_plan(understanding)
        result = await self._execute_plan(plan)
        return await self._verify(result)
    
    async def _gather_context(self, task: str) -> Dict:
        return {
            "project_structure": await self._read_project_structure(),
            "relevant_files": await self._find_relevant_files(task),
            "dependencies": await self._analyze_dependencies(),
            "existing_patterns": await self._identify_patterns()
        }
```

### Context Window Management

```python
class ContextWindowManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.priority_weights = {
            "system_prompt": 1.0,
            "task_description": 0.9,
            "recent_history": 0.8,
            "relevant_context": 0.6,
            "background_info": 0.3
        }
    
    def build_context(self, components: Dict[str, str]) -> str:
        sorted_components = sorted(
            components.items(),
            key=lambda x: self.priority_weights.get(x[0], 0.5),
            reverse=True
        )
        
        context = ""
        current_tokens = 0
        
        for name, content in sorted_components:
            content_tokens = self._count_tokens(content)
            if current_tokens + content_tokens <= self.max_tokens:
                context += content + "\n"
                current_tokens += content_tokens
            elif self.priority_weights.get(name, 0) >= 0.8:
                truncated = self._truncate_to_fit(content, self.max_tokens - current_tokens)
                context += truncated + "\n"
                break
        
        return context
```

### Context Types

| Type | Description | Retention |
|------|-------------|-----------|
| System | Role and behavior definition | Always retained |
| Episodic | Conversation history | Trimmed by relevance |
| Semantic | Knowledge and facts | Retrieved as needed |
| Working | Current task context | Session-scoped |

---

## Tool Fundamentals

### Tool Definition

Tools are interfaces that allow agents to interact with external systems.

```python
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: List[ToolParameter]
    execute: Callable
    timeout: int = 30
    retries: int = 3
```

### Tool Categories

| Category | Examples | Use Case |
|----------|----------|----------|
| File Operations | Read, Write, Search | Code manipulation |
| Web Access | HTTP, Webhook | External API calls |
| Database | Query, Insert, Update | Data operations |
| Computation | Execute, Calculate | Processing tasks |
| Communication | Email, Slack, Discord | Notifications |

### Tool Selection Logic

```python
class ToolSelector:
    def __init__(self, tools: List[ToolDefinition]):
        self.tools = {tool.name: tool for tool in tools}
        self.usage_history: Dict[str, int] = {}
    
    def select_tools(self, task: str) -> List[ToolDefinition]:
        task_keywords = self._extract_keywords(task)
        scores = {}
        
        for name, tool in self.tools.items():
            tool_keywords = self._extract_keywords(tool.description)
            overlap = len(task_keywords & tool_keywords)
            scores[name] = overlap
        
        selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        return [self.tools[name] for name, score in selected if score > 0]
```

---

## Priority Hierarchy

Rules and decisions follow a clear priority hierarchy:

```
System Rules > Domain Rules > Task Rules > User Preferences
```

### Rule Priority Levels

| Level | Code | Description |
|-------|------|-------------|
| Critical | P0 | Must implement, security/safety implications |
| High | P1 | Should implement, significant impact |
| Medium | P2 | Recommended, improves quality |
| Low | P3 | Nice to have, incremental improvement |

### Conflict Resolution

```python
class RulePriorityResolver:
    def resolve(self, conflicting_rules: List[Rule]) -> Rule:
        sorted_rules = sorted(
            conflicting_rules,
            key=lambda r: (
                r.source_priority,
                r.level_priority,
                r.specificity
            ),
            reverse=True
        )
        return sorted_rules[0]
```

---

## State Management Fundamentals

### State Types

```python
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

class StateType(Enum):
    TRANSIENT = "transient"
    PERSISTENT = "persistent"
    SESSION = "session"
    GLOBAL = "global"

@dataclass
class AgentState:
    state_type: StateType
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    
    def update(self, key: str, value: Any) -> 'AgentState':
        new_data = {**self.data, key: value}
        return AgentState(
            state_type=self.state_type,
            data=new_data,
            created_at=self.created_at,
            updated_at=datetime.now(),
            version=self.version + 1
        )
```

### State Isolation

```python
class IsolatedState:
    def __init__(self):
        self._sessions: Dict[str, AgentState] = {}
    
    def create_session(self, session_id: str) -> AgentState:
        if session_id in self._sessions:
            raise SessionExistsError(session_id)
        self._sessions[session_id] = AgentState(StateType.SESSION)
        return self._sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[AgentState]:
        return self._sessions.get(session_id)
    
    def destroy_session(self, session_id: str):
        self._sessions.pop(session_id, None)
```

---

## Communication Patterns

### Request-Response Pattern

```python
class RequestResponsePattern:
    async def execute(self, request: Dict) -> Dict:
        response = await self.agent.process(request)
        return {"status": "success", "data": response}
```

### Pipeline Pattern

```python
class PipelinePattern:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
    
    async def execute(self, input_data: Any) -> Any:
        current_data = input_data
        for agent in self.agents:
            current_data = await agent.execute(current_data)
        return current_data
```

### Orchestration Pattern

```python
class OrchestratorPattern:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
    
    async def execute(self, task: str) -> Any:
        plan = await self._decompose(task)
        results = await asyncio.gather(*[
            self.agents[subtask.agent].execute(subtask.task)
            for subtask in plan.subtasks
        ], return_exceptions=True)
        return await self._compose(results)
```

---

## Error Handling Fundamentals

### Error Categories

| Category | Examples | Handling Strategy |
|----------|----------|-------------------|
| Transient | Rate limits, timeouts | Retry with backoff |
| Input | Invalid prompts, missing data | Validate and inform user |
| Resource | Memory limits, file access | Queue and process later |
| Model | Context overflow, refusal | Adjust and retry |
| System | Infrastructure failures | Fallback to alternatives |

### Error Handling Pattern

```python
class ErrorHandler:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    async def handle_with_retry(self, operation: Callable, *args) -> Any:
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return await operation(*args)
            except RateLimitError as e:
                await asyncio.sleep(2 ** attempt)
                last_error = e
            except ValidationError as e:
                raise UserInputError(str(e))
            except Exception as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    raise
        
        raise last_error
```

---

## Quality Attributes

### Key Quality Attributes for LLM Systems

| Attribute | Description | Measurement |
|-----------|-------------|-------------|
| Accuracy | Correctness of outputs | Human evaluation, test cases |
| Consistency | Reproducibility of results | Same input, same output |
| Latency | Response time | P50, P95, P99 percentiles |
| Throughput | Requests per time unit | Requests/second |
| Cost | Resource efficiency | Tokens used, API calls |
| Reliability | Uptime and availability | Error rate, uptime % |
| Scalability | Handling increased load | Performance under load |

### Quality Metrics

```python
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    accuracy: float
    consistency: float
    latency_p50: float
    latency_p95: float
    latency_p99: float
    throughput: float
    error_rate: float
    cost_per_request: float
    
    def meets_thresholds(self, thresholds: Dict[str, float]) -> bool:
        return all(
            getattr(self, metric) >= threshold
            for metric, threshold in thresholds.items()
        )
```

---

## Token Economics

### Token Approximations

- 1 token ≈ 4 characters (English)
- 1 token ≈ 0.75 words (English)
- Code typically uses more tokens per character

### Token Budget Strategy

```python
class TokenBudget:
    def __init__(self, total_budget: int):
        self.total = total_budget
        self.system_prompt_allocation = int(total_budget * 0.1)
        self.context_allocation = int(total_budget * 0.3)
        self.conversation_allocation = int(total_budget * 0.4)
        self.response_allocation = int(total_budget * 0.2)
    
    def can_add_context(self, tokens: int) -> bool:
        return tokens <= self.context_allocation - self.used_context
```

---

## Temperature and Sampling

Temperature controls output randomness.

| Temperature | Use Case | Characteristics |
|-------------|----------|-----------------|
| 0.0 | Code generation, factual tasks | Deterministic, consistent |
| 0.3 - 0.5 | Balanced tasks | Some variation, mostly consistent |
| 0.7 - 1.0 | Creative writing, brainstorming | More variation, creative |
| 1.0+ | Highly experimental | Maximum variation |

```python
class LLMConfiguration:
    DETERMINISTIC = {"temperature": 0.0, "top_p": 1.0}
    BALANCED = {"temperature": 0.5, "top_p": 0.9}
    CREATIVE = {"temperature": 0.8, "top_p": 0.95}
```

---

## Memory Fundamentals

### Memory Types

```python
class MemoryType(Enum):
    EPISODIC = "episodic"      # Specific experiences
    SEMANTIC = "semantic"      # General knowledge
    WORKING = "working"        # Current context
    PROCEDURAL = "procedural"  # How-to knowledge
```

### Memory Operations

```python
class MemorySystem:
    def store(self, content, memory_type, importance=0.5):
        """Store new memory."""
        pass
    
    def retrieve(self, query, memory_type=None, top_k=5):
        """Retrieve relevant memories."""
        pass
    
    def consolidate(self):
        """Merge and compress old memories."""
        pass
```

---

## Evaluation Fundamentals

### Evaluation Types

| Type | Description | Use Case |
|------|-------------|----------|
| Exact Match | String equality | Factual queries, JSON output |
| Semantic Similarity | Meaning similarity | Open-ended generation |
| F1 Score | Token overlap | Classification, extraction |
| Human Evaluation | Human judgment | Quality, safety, alignment |

### Evaluation Pipeline

```python
class EvaluationPipeline:
    def __init__(self, metrics):
        self.metrics = metrics
    
    def evaluate(self, predictions, references):
        results = {}
        for metric in self.metrics:
            results[metric] = self.metrics[metric](predictions, references)
        return results
```

---

## Security Fundamentals

### Prompt Injection Defense

```python
class PromptInjectionDefense:
    def __init__(self):
        self.patterns = [
            r"ignore (previous|all) instructions",
            r"you are now (dan|evil|unlimited)",
            r"system:",
            r"\[INST\]",
            r"override.*safety",
        ]
    
    def detect(self, text: str) -> bool:
        return any(re.search(p, text, re.I) for p in self.patterns)
```

### Output Filtering

```python
class OutputFilter:
    def filter(self, output: str) -> str:
        # Check for harmful content
        # Redact PII
        # Enforce length limits
        pass
```

---

## Performance Fundamentals

### Latency Budgets

```python
class LatencyBudget:
    def __init__(self):
        self.budgets = {
            "time_to_first_token": 500,  # ms
            "completion": 5000,  # ms
            "tool_call": 1000,  # ms
        }
    
    def check(self, component: str, actual_ms: float) -> bool:
        return actual_ms <= self.budgets.get(component, float('inf'))
```

### Throughput Considerations

- Use async/await for I/O-bound operations
- Batch requests where possible
- Implement connection pooling
- Cache frequent queries

---

## Related Rules

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-15 | Initial comprehensive version |
| 1.1.0 | 2024-02-01 | Added quality attributes section |
| 1.2.0 | 2024-02-15 | Enhanced tool fundamentals |
