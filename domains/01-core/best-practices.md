# Core Domain - Best Practices

## Overview

This document outlines the recommended approaches and best practices for building robust LLM/agentic systems. Each section includes production-ready patterns, code examples, and practical guidance.

## Table of Contents

1. [Prompt Engineering Best Practices](#prompt-engineering-best-practices)
2. [Agent Design Best Practices](#agent-design-best-practices)
3. [Tool Usage Best Practices](#tool-usage-best-practices)
4. [Context Management Best Practices](#context-management-best-practices)
5. [Quality Assurance Best Practices](#quality-assurance-best-practices)
6. [Error Handling Best Practices](#error-handling-best-practices)
7. [Testing Best Practices](#testing-best-practices)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Security Best Practices](#security-best-practices)
10. [Performance Best Practices](#performance-best-practices)
11. [Deployment Best Practices](#deployment-best-practices)
12. [Cost Management Best Practices](#cost-management-best-practices)
13. [Data Management Best Practices](#data-management-best-practices)
14. [Integration Best Practices](#integration-best-practices)
15. [Documentation Best Practices](#documentation-best-practices)

---

## Prompt Engineering Best Practices

### 1. Clear and Specific Prompts

Always write clear, unambiguous prompts that precisely describe the desired outcome.

```python
# Bad - Vague
prompt = "Write something about AI"

# Good - Specific with constraints
prompt = """
Write a 200-word introduction to transformer-based language models.
Include:
1. The key innovation (self-attention)
2. How they differ from RNNs
3. One real-world application
Write for an audience with basic programming knowledge.
"""
```

### 2. Structured Prompt Templates

Use consistent, structured formats for prompts.

```python
from string import Template
from typing import Dict, Any

class PromptTemplate:
    """Type-safe prompt template system."""
    
    TEMPLATES = {
        "code_review": Template("""
        You are reviewing $language code.
        
        Code:
        ```$language
        $code
        ```
        
        Provide feedback on:
        1. Correctness (bugs, edge cases)
        2. Style (idiomatic $language)
        3. Performance (optimizations)
        4. Security (vulnerabilities)
        
        Format as JSON: {"issues": [...], "suggestions": [...], "score": 1-10}
        """),
        
        "summarize": Template("""
        Summarize the following text in $num_bullets bullet points.
        Style: $style
        Focus on: $focus
        
        Text:
        $text
        
        Summary:
        """)
    }
    
    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        template = cls.TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")
        return template.safe_substitute(**kwargs)

# Usage
prompt = PromptTemplate.render(
    "code_review",
    language="Python",
    code="def add(a, b): return a + b"
)
```

### 3. Include Relevant Context

Provide necessary context without overwhelming the model.

```python
def build_context_aware_prompt(task: str, context: Dict) -> str:
    """Build prompt with just enough relevant context."""
    prompt = f"""
    Task: {task}
    
    """
    
    if "file_content" in context:
        prompt += f"File content:\n```\n{context['file_content'][:2000]}\n```\n\n"
    
    if "error_message" in context:
        prompt += f"Error to fix:\n{context['error_message']}\n\n"
    
    if "constraints" in context:
        prompt += "Constraints:\n"
        for constraint in context["constraints"]:
            prompt += f"- {constraint}\n"
    
    return prompt
```

### 4. Use Few-Shot Learning Effectively

```python
class FewShotPromptBuilder:
    """Build effective few-shot prompts."""
    
    def __init__(self, examples: List[Dict], max_examples: int = 3):
        self.examples = examples
        self.max_examples = max_examples
    
    def build(self, task: str) -> str:
        selected = self._select_examples(task)
        
        prompt = "Complete the following tasks in the same style as the examples.\n\n"
        
        for i, ex in enumerate(selected, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Input: {ex['input']}\n"
            prompt += f"Output: {ex['output']}\n\n"
        
        prompt += f"Now complete:\nInput: {task}\nOutput:"
        return prompt
    
    def _select_examples(self, task: str) -> List[Dict]:
        if len(self.examples) <= self.max_examples:
            return self.examples
        # Select diverse, relevant examples
        return self.examples[:self.max_examples]
```

### 5. Prompt Versioning

Track prompt changes and enable rollback.

```python
class PromptRegistry:
    """Version and manage prompts."""
    
    def __init__(self):
        self.versions: Dict[str, Dict[str, str]] = {}
    
    def register(self, name: str, template: str, version: str, metadata: Dict = None):
        if name not in self.versions:
            self.versions[name] = {}
        self.versions[name][version] = {
            "template": template,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
    
    def get(self, name: str, version: str = "latest") -> str:
        versions = self.versions.get(name, {})
        if version == "latest":
            version = max(versions.keys())
        return versions.get(version, {}).get("template")
    
    def compare(self, name: str, v1: str, v2: str) -> Dict:
        t1 = self.versions.get(name, {}).get(v1, {})
        t2 = self.versions.get(name, {}).get(v2, {})
        return {
            "v1": v1,
            "v2": v2,
            "changed": t1.get("template") != t2.get("template")
        }
```

---

## Agent Design Best Practices

### 1. Define Clear Agent Roles

Each agent should have a specific, well-defined responsibility.

```python
from abc import ABC, abstractmethod

class AgentRole:
    """Define clear boundaries for agent responsibilities."""
    role: str = "undefined"
    responsibilities: List[str] = []
    boundaries: List[str] = []

class CodeReviewAgent(AgentRole):
    role = "Code Reviewer"
    responsibilities = [
        "Identify bugs and potential issues",
        "Check code style and conventions",
        "Suggest performance improvements",
        "Verify test coverage"
    ]
    boundaries = [
        "Cannot modify code directly",
        "Cannot merge pull requests",
        "Cannot access production databases"
    ]

class BaseAgent(ABC):
    def __init__(self, role: AgentRole):
        self.role = role
        self.validate_capabilities()
    
    def validate_capabilities(self):
        """Ensure agent operates within defined boundaries."""
        pass
    
    @abstractmethod
    def execute(self, task: str) -> Dict:
        pass
```

### 2. Implement Comprehensive Error Handling

```python
class ResilientAgent:
    """Agent with comprehensive error handling."""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.error_handler = ErrorHandler(max_retries)
    
    async def execute(self, task: str) -> Dict:
        try:
            return await self.error_handler.handle_with_retry(
                self._execute_internal, task
            )
        except TransientError as e:
            return {
                "status": "error",
                "error": str(e),
                "recoverable": True,
                "suggestion": "Retry in a few minutes"
            }
        except ValidationError as e:
            return {
                "status": "error",
                "error": str(e),
                "recoverable": False,
                "suggestion": "Check input parameters"
            }
        except Exception as e:
            logger.exception("Unexpected agent error")
            return {
                "status": "error",
                "error": "Internal agent error",
                "recoverable": False
            }
```

### 3. Use Structured Output Schemas

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum

class TaskStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    TIMEOUT = "timeout"

class AgentOutput(BaseModel):
    """Structured output schema for agent responses."""
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: Optional[int] = None
    
    @validator('result')
    def validate_result_for_status(cls, v, values):
        if values.get('status') == 'error' and v is not None:
            raise ValueError("Result must be None when status is error")
        return v
```

### 4. Implement Health Checks

```python
class AgentHealthCheck:
    """Health check for agent systems."""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def check(self) -> Dict[str, Any]:
        checks = {
            "llm_connectivity": await self._check_llm(),
            "tools_available": self._check_tools(),
            "memory_status": self._check_memory(),
            "rate_limits": self._check_rate_limits()
        }
        
        all_healthy = all(
            check["healthy"] for check in checks.values()
        )
        
        return {
            "healthy": all_healthy,
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _check_llm(self) -> Dict:
        try:
            start = time.time()
            await self.agent.llm.complete("Health check", max_tokens=5)
            latency = time.time() - start
            return {"healthy": True, "latency_ms": latency * 1000}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
```

---

## Tool Usage Best Practices

### 1. Validate Tool Arguments

Always validate arguments before calling tools.

```python
from pydantic import BaseModel, ValidationError

class SearchToolInput(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: Optional[Dict[str, Any]] = None

class SearchTool:
    def invoke(self, arguments: Dict) -> Dict:
        try:
            validated = SearchToolInput(**arguments)
        except ValidationError as e:
            return {
                "error": f"Invalid arguments: {e}",
                "code": "VALIDATION_ERROR"
            }
        
        return self._search(validated.query, validated.top_k, validated.filters)
```

### 2. Implement Tool Timeouts

```python
import asyncio

class ToolWithTimeout:
    def __init__(self, tool, timeout_seconds: int = 30):
        self.tool = tool
        self.timeout = timeout_seconds
    
    async def invoke(self, **kwargs) -> Dict:
        try:
            return await asyncio.wait_for(
                self.tool.invoke(**kwargs),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            return {
                "error": f"Tool timed out after {self.timeout}s",
                "code": "TIMEOUT"
            }
```

### 3. Tool Result Caching

```python
from functools import lru_cache
import hashlib

class CachedTool:
    def __init__(self, tool, cache_ttl: int = 3600):
        self.tool = tool
        self.cache_ttl = cache_ttl
        self.cache: Dict[str, Tuple[Any, float]] = {}
    
    async def invoke(self, **kwargs) -> Dict:
        cache_key = self._compute_cache_key(kwargs)
        
        if cache_key in self.cache:
            result, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return result
        
        result = await self.tool.invoke(**kwargs)
        self.cache[cache_key] = (result, time.time())
        return result
    
    def _compute_cache_key(self, kwargs: Dict) -> str:
        return hashlib.md5(
            json.dumps(kwargs, sort_keys=True).encode()
        ).hexdigest()
```

---

## Context Management Best Practices

### 1. Token-Aware Context Building

```python
class TokenAwareContextBuilder:
    def __init__(self, max_tokens: int, tokenizer):
        self.max_tokens = max_tokens
        self.tokenizer = tokenizer
        self.priority_weights = {
            "system_prompt": 1.0,
            "task": 0.9,
            "recent_history": 0.8,
            "relevant_context": 0.6,
            "background": 0.3
        }
    
    def build(self, components: Dict[str, str]) -> str:
        sorted_items = sorted(
            components.items(),
            key=lambda x: self.priority_weights.get(x[0], 0.5),
            reverse=True
        )
        
        context = ""
        tokens_used = 0
        
        for name, content in sorted_items:
            content_tokens = self.tokenizer.count(content)
            
            if tokens_used + content_tokens <= self.max_tokens:
                context += f"\n## {name}\n{content}\n"
                tokens_used += content_tokens
            elif self.priority_weights.get(name, 0) >= 0.8:
                # Truncate but include high-priority content
                available = self.max_tokens - tokens_used
                truncated = self.tokenizer.truncate(content, available)
                context += f"\n## {name} (truncated)\n{truncated}\n"
                break
        
        return context
```

### 2. Conversation History Management

```python
class ConversationManager:
    def __init__(self, max_history: int = 20, max_tokens: int = 4000):
        self.max_history = max_history
        self.max_tokens = max_tokens
        self.history: List[Dict] = []
        self.tokenizer = get_tokenizer()
    
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self._trim()
    
    def _trim(self):
        while len(self.history) > self.max_history:
            self.history.pop(0)
        
        total_tokens = sum(self.tokenizer.count(m["content"]) for m in self.history)
        while total_tokens > self.max_tokens and len(self.history) > 2:
            removed = self.history.pop(1 if self.history[0]["role"] == "system" else 0)
            total_tokens -= self.tokenizer.count(removed["content"])
    
    def get_messages(self) -> List[Dict]:
        return self.history.copy()
```

---

## Quality Assurance Best Practices

### 1. Output Validation

```python
class OutputValidator:
    def __init__(self, schema: Dict):
        self.schema = schema
    
    def validate(self, output: str) -> ValidationResult:
        try:
            data = json.loads(output)
            validated = self._validate_against_schema(data)
            return ValidationResult(valid=True, data=validated)
        except json.JSONDecodeError:
            return ValidationResult(valid=False, error="Invalid JSON")
        except ValidationError as e:
            return ValidationResult(valid=False, error=str(e))
    
    def _validate_against_schema(self, data: Dict) -> Dict:
        # Implement schema validation
        return data
```

### 2. Retry Logic with Exponential Backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=60)
)
async def execute_with_retry(agent, task: str) -> Dict:
    return await agent.execute(task)
```

---

## Error Handling Best Practices

### 1. Categorize Errors

```python
class ErrorCategory(Enum):
    TRANSIENT = "transient"  # Retry: rate limits, timeouts
    INPUT = "input"          # Fix input: validation errors
    MODEL = "model"          # Adjust: context overflow, refusals
    SYSTEM = "system"        # Fallback: infrastructure failures

class CategorizedErrorHandler:
    def handle(self, error: Exception) -> Dict:
        category = self._categorize(error)
        
        if category == ErrorCategory.TRANSIENT:
            return self._handle_retry(error)
        elif category == ErrorCategory.INPUT:
            return self._handle_input_error(error)
        elif category == ErrorCategory.MODEL:
            return self._handle_model_error(error)
        else:
            return self._handle_system_error(error)
```

### 2. Graceful Degradation

```python
class GracefulDegradation:
    def __init__(self):
        self.levels = ["full", "reduced", "minimal", "emergency"]
    
    async def execute(self, task: str, mode: str = "full") -> Dict:
        if mode == "full":
            return await self._full_execution(task)
        elif mode == "reduced":
            return await self._reduced_execution(task)
        elif mode == "minimal":
            return await self._minimal_execution(task)
        else:
            return {"error": "System in emergency mode", "retry_later": True}
```

---

## Monitoring and Observability

### 1. Structured Logging

```python
import structlog

logger = structlog.get_logger()

class MonitoredAgent:
    async def execute(self, task: str) -> Dict:
        logger.info(
            "agent.execute.start",
            agent=self.name,
            task_preview=task[:100],
            session_id=get_session_id()
        )
        
        start = time.time()
        try:
            result = await self._execute(task)
            logger.info(
                "agent.execute.success",
                duration_ms=(time.time() - start) * 1000,
                tokens_used=result.get("tokens_used")
            )
            return result
        except Exception as e:
            logger.error(
                "agent.execute.error",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=(time.time() - start) * 1000
            )
            raise
```

### 2. Metrics Collection

```python
class AgentMetrics:
    def __init__(self):
        self.requests = 0
        self.successes = 0
        self.failures = 0
        self.latencies: List[float] = []
    
    def record_request(self, latency: float, success: bool):
        self.requests += 1
        self.latencies.append(latency)
        if success:
            self.successes += 1
        else:
            self.failures += 1
    
    def summary(self) -> Dict:
        if not self.latencies:
            return {}
        
        return {
            "total_requests": self.requests,
            "success_rate": self.successes / self.requests,
            "error_rate": self.failures / self.requests,
            "avg_latency_ms": sum(self.latencies) / len(self.latencies),
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)]
        }
```

---

## Security Best Practices

### 1. Input Sanitization

```python
import re

class InputSanitizer:
    def __init__(self):
        self.injection_patterns = [
            r"ignore (previous|all) instructions",
            r"you are now (dan|evil)",
            r"system:",
            r"\[INST\]",
        ]
        self.compiled = [re.compile(p, re.I) for p in self.injection_patterns]
    
    def sanitize(self, user_input: str) -> str:
        for pattern in self.compiled:
            if pattern.search(user_input):
                logger.warning(f"Potential injection: {user_input[:100]}")
                raise SecurityError("Suspicious input detected")
        return user_input
```

### 2. Rate Limiting

```python
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = time()
        cutoff = now - self.window
        
        self.requests[user_id] = [
            t for t in self.requests[user_id] if t > cutoff
        ]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(now)
        return True
```

---

## Performance Best Practices

### 1. Request Batching

```python
class BatchProcessor:
    def __init__(self, batch_size: int = 10, max_wait_ms: int = 100):
        self.batch_size = batch_size
        self.max_wait = max_wait_ms / 1000
        self.queue: List[Dict] = []
    
    async def add(self, item: Dict) -> Any:
        future = asyncio.Future()
        self.queue.append({"item": item, "future": future})
        
        if len(self.queue) >= self.batch_size:
            await self._process_batch()
        
        return await future
    
    async def _process_batch(self):
        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]
        
        results = await self._process_items([b["item"] for b in batch])
        
        for item, result in zip(batch, results):
            item["future"].set_result(result)
```

### 2. Connection Pooling

```python
class ConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.pool = asyncio.Queue(maxsize=max_connections)
        for _ in range(max_connections):
            self.pool.put_nowait(self._create_connection())
    
    async def acquire(self):
        return await self.pool.get()
    
    def release(self, conn):
        self.pool.put_nowait(conn)
```

---

## Deployment Best Practices

### 1. Canary Deployments

```python
class CanaryDeployment:
    def __init__(self, old_model: str, new_model: str, traffic_split: float):
        self.old_model = old_model
        self.new_model = new_model
        self.traffic_split = traffic_split
    
    def route(self, user_id: str) -> str:
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return self.new_model if (hash_val % 100) < (self.traffic_split * 100) else self.old_model
```

### 2. Feature Flags

```python
class FeatureFlags:
    def __init__(self):
        self.flags: Dict[str, Dict] = {}
    
    def register(self, name: str, default: bool = False, rollout: float = 0.0):
        self.flags[name] = {"enabled": default, "rollout": rollout}
    
    def is_enabled(self, name: str, user_id: str = None) -> bool:
        flag = self.flags.get(name, {})
        if not flag.get("enabled"):
            return False
        
        if user_id and flag.get("rollout", 0) < 1.0:
            hash_val = int(hashlib.md5(f"{name}:{user_id}".encode()).hexdigest(), 16)
            return (hash_val % 100) < (flag["rollout"] * 100)
        
        return True
```

---

## Cost Management Best Practices

### 1. Token Budget Tracking

```python
class TokenBudget:
    def __init__(self, daily_limit: int):
        self.daily_limit = daily_limit
        self.used = 0
    
    def check(self, estimated_tokens: int) -> bool:
        if self.used + estimated_tokens > self.daily_limit:
            logger.warning(f"Token budget exceeded: {self.used + estimated_tokens}/{self.daily_limit}")
            return False
        return True
    
    def consume(self, tokens: int):
        self.used += tokens
```

### 2. Model Routing

```python
class ModelRouter:
    def __init__(self):
        self.models = {
            "fast": {"model": "gpt-3.5-turbo", "cost": 0.002},
            "standard": {"model": "gpt-4", "cost": 0.03},
            "advanced": {"model": "gpt-4-turbo", "cost": 0.06}
        }
        self.routing_rules = [
            (lambda t: len(t) < 100, "fast"),
            (lambda t: "complex" in t.lower(), "advanced"),
            (lambda t: True, "standard")
        ]
    
    def route(self, task: str, budget: float = None) -> str:
        for condition, tier in self.routing_rules:
            if condition(task):
                model = self.models[tier]
                if budget and model["cost"] > budget:
                    return self.models["fast"]["model"]
                return model["model"]
        return self.models["standard"]["model"]
```

---

## Documentation Best Practices

### 1. Prompt Documentation

```python
class DocumentedPrompt:
    """Prompt with embedded documentation."""
    
    name: str = "code_review"
    version: str = "1.0.0"
    description: str = "Reviews code for bugs, style, and security"
    author: str = "Team Name"
    
    input_variables = ["language", "code"]
    output_format = "JSON with issues, suggestions, score"
    
    template = """
    [Template here]
    """
    
    examples = [
        {
            "input": {"language": "python", "code": "..."},
            "output": {"issues": [...], "score": 7}
        }
    ]
    
    known_limitations = [
        "May miss subtle race conditions",
        "Security checks are basic"
    ]
```

### 2. API Documentation

```python
from fastapi import FastAPI, Doc

app = FastAPI()

@app.post("/agents/{agent_id}/execute", response_model=AgentOutput)
async def execute_agent(
    agent_id: str,
    request: ExecutionRequest,
    background_tasks: BackgroundTasks
) -> AgentOutput:
    """
    Execute an agent task.
    
    - **agent_id**: Unique agent identifier
    - **request**: Task input and parameters
    
    Returns structured output with status, result, and metadata.
    """
    result = await agent_executor.execute(agent_id, request)
    
    background_tasks.add_task(
        log_execution, agent_id, request, result
    )
    
    return result
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)
