# Development Domain - Fundamentals

## Overview

This document covers fundamental development principles for LLM/agentic systems, including core design patterns, architectural principles, and foundational concepts that every developer should understand and apply.

---

## Core Principles

### Separation of Concerns

Each component should have a single, well-defined responsibility. This enables easier testing, debugging, and evolution of the system.

### Explicit Dependencies

Dependencies should be explicit and injectable, making it clear what each component needs to function.

### Fail Fast

Validate inputs early and fail with clear error messages rather than propagating invalid state.

### Observability

Build in logging, metrics, and tracing from the start rather than adding them later.

---

## Architectural Patterns

### 1. Layered Architecture

Separate the system into concentric layers:
- Presentation Layer: User interfaces, API endpoints
- Application Layer: Business logic, orchestration
- Domain Layer: Core domain entities and rules
- Infrastructure Layer: External services, databases

### 2. Hexagonal Architecture

The core domain is at the center, surrounded by adapters for external services. This makes the core easily testable without mocks.

### 3. Clean Architecture

Similar to hexagonal, with explicit use cases and interface adapters.

---

## Design Patterns for Agents

### 1. Strategy Pattern for Prompt Processing

Different prompt types may require different processing strategies.

### 2. Observer Pattern for Event Handling

Many components may need to react to agent state changes.

### 3. Command Pattern for Tool Execution

Tool calls can be represented as command objects for queuing and auditing.

---

## Testing Principles

### Unit Tests

Test individual functions in isolation with mocked dependencies.

### Integration Tests

Test interactions between components and external services.

### Property-Based Tests

Use generative testing to find edge cases automatically.

---

## Error Handling Fundamentals

Always handle errors at the appropriate level. Log internally, return generic messages externally.

---

## Configuration Management

Load configuration from environment variables or secure stores. Never hardcode sensitive values.

---

## 5. Design Principles in Depth

### 5.1 Separation of Concerns

Each module, class, or function should have exactly one reason to change. When you find yourself modifying a component for multiple reasons, consider splitting it.

Implementation guidance:
- Keep file sizes small (< 400 lines ideal, < 800 lines maximum)
- Group related functions together in the same module
- Separate concerns vertically (by feature) rather than horizontally (by layer)

### 5.2 Explicit Dependencies

Dependencies should be explicit in type signatures and constructor parameters. This enables:
- Easy testing with mocks or fakes
- Clear understanding of what each component requires
- Compile-time (or type-check-time) verification of wiring

### 5.3 Fail Fast

Validate inputs immediately upon entry to your system. Delaying validation makes debugging harder and can lead to partial state changes that are hard to undo.

Example implementation:
```python
def process_agent_request(request: Dict) -> Response:
    if not request:
        raise ValueError("Request cannot be empty")
    if "prompt" not in request:
        raise ValidationError("Missing required field: prompt")
    if len(request["prompt"]) > MAX_PROMPT_LENGTH:
        raise ValidationError(f"Prompt too long: {len(request['prompt'])} > {MAX_PROMPT_LENGTH}")
    return _do_process(request)
```

### 5.4 Observability

Instrument your code from day one. Key observability signals:

**Logs**: Structured, consistent schema across all components
```python
logger.info("agent.prompt_processed", extra={
    "session_id": session_id,
    "prompt_length": len(prompt),
    "response_length": len(response),
    "model": model_name,
    "duration_ms": duration,
})
```

**Metrics**: Counter, gauge, and histogram for key operations
```python
PROMPT_COUNTER.inc()
RESPONSE_HISTOGRAM.observe(duration)
ACTIVE_SESSIONS_GAUGE.set(active_count)
```

**Traces**: End-to-end request flow through all services
```python
with tracer.start_as_current_span("agent.process") as span:
    span.set_attribute("prompt.length", len(prompt))
    result = agent.process(prompt)
    span.set_attribute("response.length", len(result))
```

---

## 6. Architectural Patterns for Agents

### 6.1 Layered Architecture

The classic three-layer architecture adapted for agent systems:

```
┌─────────────────────────────────────┐
│            Presentation             │
│  (API endpoints, CLI, UI widgets)   │
├─────────────────────────────────────┤
│         Application Layer           │
│    (Agent orchestration, tools)     │
├─────────────────────────────────────┤
│           Domain Layer              │
│   (Business rules, agents, plans)   │
├─────────────────────────────────────┤
│        Infrastructure Layer         │
│ (Models, databases, external APIs)  │
└─────────────────────────────────────┘
```

Implementation considerations:
- Domain layer should be pure Python with no framework dependencies
- Application layer coordinates but contains no business logic
- Infrastructure layer is swappable via dependency injection

### 6.2 Hexagonal Architecture (Ports and Adapters)

The core agent logic sits at the center, surrounded by ports (interfaces) and adapters (implementations).

```python
# Core domain - no external dependencies
class Agent:
    def __init__(self, model_port: ModelPort, tools_port: ToolsPort):
        self.model = model_port
        self.tools = tools_port

    def run(self, user_input: str) -> str:
        validated = self._validate(user_input)
        return self.model.generate(validated)


# Ports (interfaces)
class ModelPort(Protocol):
    def generate(self, prompt: str) -> str: ...


# Adapters (implementations)
class OpenAIModelAdapter(ModelPort):
    def generate(self, prompt: str) -> str:
        return openai_client.chat.completions.create(...)
```

Benefits:
- Core logic is easily tested without mocks
- External services can be swapped without changing core
- Clear boundaries between concerns

### 6.3 Clean Architecture

Robert Martin's Clean Architecture adapted for agents:

```
                    ┌─────────────────────────┐
                    │       Frameworks        │
                    │ (FastAPI, Celery, etc)  │
                    └───────────▲─────────────┘
                              │
                    ┌───────────┴─────────────┐
                    │   Interface Adapters    │
                    │ (REST, JSON, database) │
                    └───────────▲─────────────┘
                              │
                    ┌───────────┴─────────────┐
                    │    Use Case Interactors │
                    │   (Agent workflows)     │
                    └───────────▲─────────────┘
                              │
                    ┌───────────┴─────────────┐
                    │       Entities        │
                    │   (User, Session)   │
                    └───────────▲─────────────┘
                              │
                    ┌───────────┴─────────────┐
                    │     Enterprise Level   │
                    │   (Business rules)    │
                    └─────────────────────────┘
```

---

## 7. Design Patterns for Agent Systems

### 7.1 Observer Pattern for State Changes

Multiple systems may need to react to agent state changes without coupling to the agent.

```python
class AgentStateObserver:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Callable[[str, Any], None]):
        self._observers.append(observer)

    def notify(self, state: str, data: Any):
        for obs in self._observers:
            try:
                obs(state, data)
            except Exception as e:
                logger.exception(f"Observer failed: {e}")
```

Benefits:
- Loose coupling between agent and observers
- Easy to add/remove monitoring systems
- Failure isolation between observers

### 7.2 Strategy Pattern for Decision Making

Different reasoning strategies may be appropriate for different tasks.

```python
class ReasoningStrategy(ABC):
    @abstractmethod
    def decide(self, prompt: str, context: Dict) -> Action: ...


class ChainOfThoughtStrategy(ReasoningStrategy):
    def decide(self, prompt: str, context: Dict) -> Action:
        # Think step by step
        thoughts = self._think(prompt, context)
        return Action(thoughts.final_answer)


class TreeOfThoughtStrategy(ReasoningStrategy):
    def decide(self, prompt: str, context: Dict) -> Action:
        # Explore multiple paths
        tree = self._build_tree(prompt)
        return self._execute_best_path(tree)
```

### 7.3 Command Pattern for Tool Execution

Represent tool calls as objects for queuing, auditing, and replay.

```python
@dataclass
class ToolCommand:
    tool_id: str
    arguments: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any]


class CommandExecutor:
    def execute(self, command: ToolCommand) -> ToolResult:
        # Log, validate, execute
        self._audit(command)
        return self._run(command)
```

---

## 8. Testing Fundamentals

### 8.1 The Testing Pyramid for Agents

```
           ┌──────────────────────────────┐
           │     Manual/Exploratory      │
           │         Testing             │
           └──────────────────────────────┘
                      (5%)
           ┌──────────────────────────────┐
           │         End-to-End           │
           │        Integration           │
           └──────────────────────────────┘
                     (15%)
           ┌──────────────────────────────┐
           │       Integration            │
           └──────────────────────────────┘
                     (20%)
           ┌──────────────────────────────┐
           │         Unit Tests           │
           └──────────────────────────────┘
                     (60%)
```

### 8.2 Property-Based Testing

Use tools like Hypothesis to automatically find edge cases.

```python
@given(st.text(min_size=1, max_size=4000))
def test_prompt_never_crashes(text):
    result = agent.process(text)
    assert result is not None or result is None  # No exception


@given(st.integers(min_value=1, max_value=10000))
def test_rate_limiter_bounded(user_id_int):
    user_id = f"user_{user_id_int}"
    for _ in range(150):
        if not rate_limiter.is_allowed(user_id):
            break
    assert _ < 100  # Should hit limit
```

### 8.3 Mocking Strategy

Create focused test doubles that match your actual interfaces.

```python
class FakeModel:
    def __init__(self, responses: Optional[Dict] = None):
        self.responses = responses or {}
        self.calls = []

    def generate(self, prompt: str, **kwargs) -> str:
        self.calls.append((prompt, kwargs))
        return self.responses.get(prompt, "OK")
```

---

## 9. Error Handling Fundamentals

### 9.1 Exception Hierarchy

Define a clear exception hierarchy for your agent system.

```python
class AgentError(Exception):
    """Base exception for all agent-related errors."""


class ValidationError(AgentError):
    """Input validation failed."""


class AuthenticationError(AgentError):
    """Authentication or authorization failed."""


class ToolError(AgentError):
    """Tool execution failed."""


class RateLimitError(AgentError):
    """Rate limit exceeded."""
```

### 9.2 Error Propagation Strategy

Don't silently catch and ignore exceptions. Either handle them or propagate.

```python
def process_with_handling(prompt: str) -> Result:
    try:
        return agent.process(prompt)
    except ValidationError:
        raise  # Re-raise - caller should handle validation errors
    except ToolError as e:
        logger.error(f"Tool failed: {e}")
        return Result(error="Unable to complete request")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return Result(error="Internal error")
```

---

## 10. Configuration Management

### 10.1 Environment-Specific Configuration

```python
class Config(BaseSettings):
    model_name: str = "gpt-4"
    max_tokens: int = 4096
    temperature: float = 0.7
    rate_limit_rpm: int = 60
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
```

### 10.2 Feature Flags

```python
def should_use_new_planner() -> bool:
    return os.getenv("USE_NEW_PLANNER", "false").lower() == "true"
```

---

## 11. Design Principles Deep Dive

### 11.1 SOLID Principles for Agents

**Single Responsibility Principle (SRP)**
A class should have one reason to change. For agents, this means:
- Separate validation from processing
- Separate tool execution from planning
- Separate memory management from reasoning

**Open-Closed Principle (OCP)**
Software entities should be open for extension, closed for modification. For agents:
- Use plugins for new tools
- Use strategies for different reasoning modes
- Use decorators for cross-cutting concerns

**Liskov Substitution Principle (LSP)**
Subtypes must be substitutable for their base types. For agents:
- Mock models should behave like real models
- Test tools should match production interface
- Error handling should be consistent across implementations

### 11.2 Concurrency Patterns

Thread-safe agent state management:
```python
import threading
from concurrent.futures import ThreadPoolExecutor


class ThreadSafeAgentStore:
    def __init__(self):
        self._sessions = {}
        self._lock = threading.RLock()

    def get_session(self, session_id: str):
        with self._lock:
            return self._sessions.get(session_id)

    def update_session(self, session_id: str, updates: dict):
        with self._lock:
            session = self._sessions.get(session_id, {})
            session.update(updates)
            self._sessions[session_id] = session
```

Async agent with bounded concurrency:
```python
class AsyncAgentPool:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)

    async def process(self, prompt: str) -> str:
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor,
                self._sync_process,
                prompt
            )
```

---

## 12. State Management Fundamentals

### 12.1 Session Isolation

Every user session must be isolated from others:
```python
class SessionContext:
    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.context_messages = []
        self.tool_history = []
        self.created_at = datetime.utcnow()

    def add_message(self, role: str, content: str):
        self.context_messages.append({"role": role, "content": content})

    def get_context_for_prompt(self, max_tokens: int) -> List[dict]:
        # Return trimmed context within token limit
        return self.context_messages[-max_tokens:]
```

### 12.2 Memory Eviction Strategies

Implement bounded memory with eviction:
```python
class BoundedMemory:
    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self._items = collections.OrderedDict()

    def put(self, key: str, value: Any):
        if key in self._items:
            del self._items[key]
        self._items[key] = value
        if len(self._items) > self.max_items:
            self._items.popitem(last=False)

    def get(self, key: str) -> Optional[Any]:
        if key in self._items:
            # Move to end (LRU)
            self._items.move_to_end(key)
            return self._items[key]
        return None
```

---

## 13. Concurrency Patterns for Agents

### 13.1 Thread-Safe Agent State

```python
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor


class ThreadSafeAgentManager:
    def __init__(self):
        self._agents = {}
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=50)

    def get_or_create_agent(self, session_id: str) -> "Agent":
        with self._lock:
            if session_id not in self._agents:
                self._agents[session_id] = Agent()
            return self._agents[session_id]

    def cleanup_session(self, session_id: str):
        with self._lock:
            self._agents.pop(session_id, None)

    async def process_async(self, session_id: str, prompt: str) -> str:
        agent = self.get_or_create_agent(session_id)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            agent.process,
            prompt
        )
```

### 13.2 Async Semaphore for Rate Limiting

```python
class AsyncRateLimiter:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._counts = collections.defaultdict(int)

    async def acquire(self, key: str = "default") -> bool:
        if self._counts[key] >= self.semaphore._value:
            return False
        await self.semaphore.acquire()
        self._counts[key] += 1
        return True

    async def release(self, key: str = "default"):
        self._counts[key] -= 1
        self.semaphore.release()
```

---

## 14. Error Handling Patterns

### 14.1 Exception Hierarchy

```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class ValidationError(AgentError):
    """Input validation failed."""
    pass


class ToolError(AgentError):
    """Tool execution failed."""
    pass


class RateLimitError(AgentError):
    """Rate limit exceeded."""
    pass


class CircuitOpenError(AgentError):
    """Circuit breaker is open."""
    pass
```

### 14.2 Error Recovery Decorator

```python
def with_error_recovery(
    max_retries: int = 3,
    retry_on: tuple = (ConnectionError, TimeoutError, RateLimitError)
):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except retry_on as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
            raise AgentError(f"Failed after {max_retries} attempts") from last_error
        return wrapper
    return decorator
```

---

## 15. Testing Infrastructure Patterns

### 15.1 Test Fixture Management

```python
@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_model(temp_storage):
    responses_file = os.path.join(temp_storage, "responses.json")
    with open(responses_file, "w") as f:
        json.dump({"default": "Mock response"}, f)
    yield MockModel(responses_file)
```

### 15.2 Parameterized Testing

```python
@pytest.mark.parametrize("prompt,expected_tokens", [
    ("Hello", 1),
    ("This is a longer prompt with more words", 9),
    ("A" * 1000, 1000),
])
def test_token_counting(prompt, expected_tokens):
    assert estimate_tokens(prompt) == expected_tokens
```

---

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Checklist](./checklist.md)