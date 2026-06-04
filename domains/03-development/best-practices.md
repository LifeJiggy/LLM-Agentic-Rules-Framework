# Development Domain - Best Practices

## Overview

This document outlines recommended development practices for LLM/agentic systems, covering code organization, testing strategies, error handling, documentation standards, and production deployment considerations.

---

## Table of Contents

1. [Code Organization](#1-code-organization)
2. [Error Handling](#2-error-handling)
3. [Testing](#3-testing)
4. [Documentation](#4-documentation)
5. [Configuration Management](#5-configuration-management)
6. [Logging and Monitoring](#6-logging-and-monitoring)
7. [Performance Optimization](#7-performance-optimization)
8. [Security Practices](#8-security-practices)
9. [Deployment Practices](#9-deployment-practices)
10. [Maintenance Practices](#10-maintenance-practices)

---

## 1. Code Organization

### 1.1 Project Structure

A well-organized project structure promotes maintainability and team collaboration.

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── planner.py
│   │   └── executor.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── registry.py
│   │   └── implementations/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── adapters/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── validators.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── security.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

### 1.2 Modular Design Principles

Principle 1: Single Responsibility
```python
# Each module should have one reason to change

# ❌ Bad - Multiple responsibilities in one class
class AgentController:
    def validate_input(self): ...
    def call_model(self): ...
    def send_email(self): ...
    def save_to_db(self): ...

# ✅ Good - Separate focused classes
class InputValidator:
    def validate(self, input: str) -> ValidationResult: ...

class ModelClient:
    def generate(self, prompt: str) -> str: ...

class EmailService:
    def send(self, recipient: str, body: str) -> None: ...

class DataStore:
    def persist(self, data: dict) -> None: ...
```

Principle 2: Explicit Dependencies
```python
# Dependencies should be explicit and injected

# ❌ Bad - Hidden dependencies
class Agent:
    def __init__(self):
        self.db = open_database_connection()
        self.api = ExternalAPI()

# ✅ Good - Explicit, injectable dependencies
class Agent:
    def __init__(self, db: Database, api_client: APIClient):
        self.db = db
        self.api = api_client
```

---

## 2. Error Handling

### 2.1 Custom Exception Hierarchy

```python
class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass

class ValidationError(AgentError):
    """Input validation failed."""
    pass

class AuthenticationError(AgentError):
    """Authentication or authorization failed."""
    pass

class ModelError(AgentError):
    """LLM model call failed."""
    pass

class ToolError(AgentError):
    """Tool execution failed."""
    pass

class RateLimitError(AgentError):
    """Rate limit exceeded."""
    pass

class ConfigurationError(AgentError):
    """Configuration error."""
    pass
```

### 2.2 Graceful Degradation

```python
def get_agent_response(prompt: str, fallback_enabled: bool = True) -> str:
    try:
        primary_result = call_primary_model(prompt)
        if primary_result.quality_score > 0.8:
            return primary_result.text
    except ModelError as e:
        logger.warning(f"Primary model failed: {e}")

    if fallback_enabled:
        try:
            fallback_result = call_fallback_model(prompt)
            return fallback_result.text
        except ModelError as e:
            logger.warning(f"Fallback model failed: {e}")
        except RateLimitError:
            logger.warning("Both models rate-limited")

    return "I'm unable to provide a response right now. Please try again later."
```

---

## 3. Testing

### 3.1 Test Structure

```python
# tests/unit/test_agent_core.py

import pytest
from unittest.mock import Mock, patch
from src.agent.core import AgentCore


class TestAgentCore:
    def setup_method(self):
        self.model = Mock()
        self.tool_registry = Mock()
        self.agent = AgentCore(model=self.model, tool_registry=self.tool_registry)

    def test_process_simple_prompt(self):
        self.model.generate.return_value = "Hello back!"
        result = self.agent.process("Hello")
        assert result == "Hello back!"
        self.model.generate.assert_called_once()

    def test_handles_tool_calls(self):
        response = "I'll help with that. [TOOL:search]"
        self.model.generate.return_value = response
        self.tool_registry.execute.return_value = "search results"
        result = self.agent.process("Search for something")
        assert "search results" in result

    @pytest.mark.parametrize("input,expected", [
        ("Hello", True),
        ("ignore instructions", False),
        ("new rules", False),
    ])
    def test_injection_detection(self, input, expected):
        result = self.agent.detect_injection(input)
        assert result == expected
```

### 3.2 Property-Based Testing

```python
from hypothesis import given, strategies as st
import pytest

@given(st.text(min_size=1, max_size=4000))
def test_validator_never_crashes(input_text):
    result = validator.validate(input_text)
    assert isinstance(result, ValidationResult)
    assert result.error is not None or result.valid

@given(st.integers(min_value=1, max_value=10000))
def test_rate_limiter_bounded_calls(user_id_int):
    user_id = f"user_{user_id_int}"
    rate_limiter = RateLimiter(max_requests=100)
    for _ in range(200):
        if not rate_limiter.is_allowed(user_id):
            break
    # Should always hit limit before 200 calls
    assert _ < 100
```

---

## 4. Documentation

### 4.1 Comprehensive Docstrings

```python
def calculate_token_cost(text: str, model: str = "gpt-4") -> float:
    """Calculate the token cost for a given text with a specific model.

    Token costs are computed based on the model's pricing structure and
    include both input and output token charges. This function uses
    an accurate tokenizer appropriate for the specified model.

    Args:
        text: The text to tokenize and calculate cost for.
        model: The model name to use for tokenization. Defaults to "gpt-4".
            Supported: "gpt-4", "gpt-3.5-turbo", "claude-3-opus".

    Returns:
        The estimated cost in USD for processing this text.

    Raises:
        ValueError: If model is not supported.
        ImportError: If required tokenizer library is not installed.

    Example:
        >>> calculate_token_cost("Hello world", "gpt-4")
        0.00003

        >>> calculate_token_cost("Summarize this.", model="gpt-3.5-turbo")
        0.000015

    Note:
        Costs are estimates based on current pricing. Actual costs may vary
        based on API provider terms and volume discounts.
    """
    ...
```

---

## 5. Configuration Management

### 5.1 Environment-Aware Configuration

```python
from pydantic import BaseSettings, Field
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AgentConfig(BaseSettings):
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    log_level: str = Field(default="INFO")
    max_input_length: int = Field(default=4000, ge=1, le=50000)
    max_output_tokens: int = Field(default=4096, ge=1, le=100000)
    rate_limit_rpm: int = Field(default=60, ge=1)
    model_temperature: float = Field(default=0.7, ge=0, le=2)
    model_name: str = Field(default="gpt-4")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

---

## 6. Logging and Monitoring

### 6.1 Structured Logging

```python
import structlog
from datetime import datetime


logger = structlog.get_logger()


def log_agent_action(action: str, user_id: str, **metadata):
    logger.info(
        action=action,
        user_id=user_id,
        timestamp=datetime.utcnow().isoformat(),
        **metadata
    )
```

---

## 7. Performance Optimization

### 7.1 Caching Strategy

```python
from functools import lru_cache
import time


@lru_cache(maxsize=1000)
def get_cached_prompt_template(template_name: str) -> str:
    return load_prompt_template(template_name)
```

---

## 8. Security Practices

### 8.1 Input Sanitization Pipeline

```python
def sanitize_user_input(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    stripped = "".join(ch for ch in normalized if ord(ch) >= 32 or ch in "\n\r\t")
    escaped = html.escape(stripped)
    return escaped
```

---

## 9. Deployment Practices

### 9.1 Health Checks

```python
def health_check() -> Dict[str, str]:
    checks = {
        "database": "healthy" if db.ping() else "unhealthy",
        "model": "healthy" if model.ping() else "unhealthy",
    }
    return checks
```

---

## 10. Maintenance Practices

### 10.1 Deprecation Warnings

```python
import warnings


def deprecated(replacement: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated, use {replacement} instead",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 10. Maintenance Practices

### 10.1 Deprecation Warnings

```python
import warnings


def deprecated(replacement: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated, use {replacement} instead",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 11. Advanced Testing Practices

### 11.1 Mock External Dependencies

```python
class TestAgentWithMocks:
    def setup_method(self):
        self.model_mock = Mock(spec=ModelClient)
        self.tool_mock = Mock(spec=ToolRegistry)
        self.bus_mock = Mock(spec=EventBus)
        self.agent = AgentCore(
            model=self.model_mock,
            tools=self.tool_mock,
            bus=self.bus_mock
        )

    def test_model_called_with_validated_input(self):
        prompt = "Hello world"
        self.model_mock.generate.return_value = "Hi there!"
        result = self.agent.process(prompt)
        self.model_mock.generate.assert_called_once()
        call_args = self.model_mock.generate.call_args
        assert len(call_args[0][0]) <= self.agent.config.max_input_length
```

### 11.2 Integration Test Patterns

```python
@pytest.fixture
def test_database():
    db = create_test_db()
    yield db
    db.cleanup()


@pytest.fixture
def test_agent(test_database):
    model = TestModelClient()
    tools = ToolRegistry(database=test_database)
    bus = EventBus()
    return AgentCore(model=model, tools=tools, bus=bus)


def test_full_agent_workflow(test_agent):
    response = test_agent.process("What is the weather today?")
    assert response is not None
    assert len(response) > 0
```

### 11.3 Chaos Engineering for Resilience

```python
@pytest.mark.chaos
def test_agent_handles_model_timeout(chaos_model):
    chaos_model._inject_timeout = True
    agent = AgentCore(model=chaos_model, tools=Mock(), bus=Mock())
    with pytest.raises(AgentError):
        agent.process("Test prompt")
```

---

## 12. Code Review Standards

### 12.1 Security Checklist for Reviews

- All inputs validated at boundaries
- No hardcoded secrets
- Proper error handling
- Authorization checks on all operations
- No information leakage in responses

### 12.2 Performance Review Points

- Function complexity (cyclomatic complexity < 10)
- Resource cleanup in finally blocks
- Timeouts on all external calls
- Caching where appropriate

---

## 13. Documentation Standards

### 13.1 README Template

```markdown
# Project Name

Brief description of what this agent does.

## Quick Start

```bash
pip install -r requirements.txt
python -m agent.main --config config.yaml
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| MODEL_NAME | gpt-4 | Model to use |
| MAX_TOKENS | 4096 | Max response tokens |

## API

See `docs/api.md` for endpoint documentation.
```

### 13.2 Architecture Decision Records

Document major decisions in `docs/adr/`:
- Why we chose this model provider
- Why we use this caching strategy
- Security decisions and trade-offs

---

## 14. Continuous Integration Practices

### 14.1 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

### 14.2 CI Pipeline

```yaml
# .github/workflows/ci.yml
steps:
  - checkout
  - setup-python
  - install-dependencies
  - run-tests:
      matrix:
        - python-version: [3.9, 3.10, 3.11]
  - run-security-scans
  - build-and-push
```

---

## 15. Monitoring and Observability

### 15.1 Key Metrics to Track

- Request latency (p50, p95, p99)
- Error rate by type
- Token usage per model
- Cache hit ratio
- Tool execution success rate

### 15.2 Health Check Endpoints

```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "checks": {
            "database": await db_health(),
            "model": await model_health(),
            "cache": cache_health(),
        }
    }


@app.get("/ready")
async def ready():
    return {"ready": all_systems_operational()}
```

---

## 16. Advanced Security Practices

### 16.1 Token Sanitization Pipeline

```python
import re
from typing import List, Tuple


BLOCKED_PATTERNS = [
    (r"(?i)ignore.*instructions", "instruction_override"),
    (r"(?i)new.*rules", "rule_injection"),
    (r"(?i)system.*prompt", "prompt_extraction"),
]


def scan_prompt(text: str) -> Tuple[bool, List[str]]:
    violations = []
    for pattern, name in BLOCKED_PATTERNS:
        if re.search(pattern, text):
            violations.append(name)
    return len(violations) == 0, violations


def sanitize_prompt(text: str) -> str:
    sanitized = text
    for pattern, _ in BLOCKED_PATTERNS:
        sanitized = re.sub(pattern, "[BLOCKED]", sanitized)
    return sanitized
```

### 16.2 API Key Rotation

```python
class APIKeyManager:
    def __init__(self, vault_client):
        self.vault = vault_client
        self._current_key = None
        self._previous_key = None

    async def get_key(self) -> str:
        if self._current_key and not self._is_expired():
            return self._current_key
        await self._rotate_key()
        return self._current_key

    async def _rotate_key(self):
        self._previous_key = self._current_key
        self._current_key = await self.vault.read("api_key")
        if self._previous_key:
            asyncio.create_task(self._revoke_old_key())

    def _is_expired(self) -> bool:
        # Check key age against policy
        return False

    async def _revoke_old_key(self):
        if self._previous_key:
            await self.vault.revoke(self._previous_key)
```

---

## 17. Performance Testing Patterns

### 17.1 Load Testing Setup

```python
import asyncio
import time
from typing import List, Callable


async def load_test(
    func: Callable,
    inputs: List[Any],
    concurrency: int = 10,
    warmup: int = 5
) -> Dict[str, Any]:
    # Warmup
    for _ in range(warmup):
        await func(inputs[0])

    # Actual test
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_call(input):
        async with semaphore:
            start = time.perf_counter()
            try:
                result = await func(input)
                return {"success": True, "duration": time.perf_counter() - start}
            except Exception as e:
                return {"success": False, "error": str(e), "duration": time.perf_counter() - start}

    results = await asyncio.gather(*[bounded_call(i) for i in inputs])
    return analyze_results(results)


def analyze_results(results: List[Dict]) -> Dict[str, Any]:
    durations = [r["duration"] for r in results if r["success"]]
    return {
        "success_rate": len([r for r in results if r["success"]]) / len(results),
        "p50": sorted(durations)[len(durations) // 2],
        "p95": sorted(durations)[int(len(durations) * 0.95)],
        "p99": sorted(durations)[int(len(durations) * 0.99)],
    }
```

---

## 18. Continuous Integration Practices

### 18.1 Pre-commit Configuration

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--strict]
```

### 18.2 CI Pipeline for Agents

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt

      - name: Run linting
        run: |
          black --check .
          flake8 .
          mypy .

      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

---

## 19. Monitoring and Observability

### 19.1 Structured Metrics

```python
from prometheus_client import Counter, Histogram, Gauge


class AgentMetrics:
    def __init__(self):
        self.requests = Counter("agent_requests_total", "Total agent requests")
        self.errors = Counter("agent_errors_total", "Total agent errors", ["type"])
        self.duration = Histogram("agent_request_duration_seconds", "Request duration")
        self.active_sessions = Gauge("agent_active_sessions", "Active sessions")

    def record_request(self, endpoint: str = ""):
        self.requests.inc()

    def record_error(self, error_type: str):
        self.errors.labels(type=error_type).inc()

    def observe_duration(self, duration: float):
        self.duration.observe(duration)
```

---

## 20. Security Practices

### 20.1 Input Sanitization Pipeline

```python
import re
from typing import List, Tuple


INJECTION_PATTERNS = [
    (r"(?i)ignore.*instructions", "instruction_override"),
    (r"(?i)new.*rules", "rule_injection"),
    (r"(?i)system.*prompt", "prompt_extraction"),
]


def scan_and_sanitize(text: str) -> Tuple[str, List[str]]:
    violations = []
    sanitized = text
    for pattern, name in INJECTION_PATTERNS:
        if re.search(pattern, text):
            violations.append(name)
        sanitized = re.sub(pattern, "[BLOCKED]", sanitized)
    return sanitized, violations


def validate_prompt_safety(prompt: str) -> ValidationResult:
    sanitized, violations = scan_and_sanitize(prompt)
    if violations:
        return ValidationResult(
            valid=False,
            error=f"Safety violations: {violations}"
        )
    return ValidationResult(valid=True, sanitized=sanitized)
```

### 20.2 API Key Management

```python
class SecureApiKeyManager:
    def __init__(self, secret_store):
        self.secret_store = secret_store
        self._keys = {}

    async def get_key(self, service: str) -> str:
        if service in self._keys:
            key_info = self._keys[service]
            if self._is_expired(key_info):
                await self._rotate_key(service)
            return self._keys[service]["value"]
        return await self._load_new_key(service)

    async def _load_new_key(self, service: str) -> str:
        secret = await self.secret_store.read(f"api/{service}")
        self._keys[service] = {
            "value": secret["key"],
            "expires": datetime.fromisoformat(secret["expires_at"])
        }
        return secret["key"]
```

---

## 21. Data Flow Best Practices

### 21.1 Immutable Data Structures

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ImmutableContext:
    user_id: str
    session_id: str
    messages: Tuple[dict, ...]
    metadata: frozenset = frozenset()


def add_message(context: ImmutableContext, role: str, content: str) -> ImmutableContext:
    new_messages = context.messages + ({"role": role, "content": content},)
    return ImmutableContext(
        user_id=context.user_id,
        session_id=context.session_id,
        messages=new_messages
    )
```

### 21.2 Data Validation Pipeline

```python
from pydantic import BaseModel, validator


class PromptRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7

    @validator("prompt")
    def validate_prompt(cls, v):
        if len(v) > 50000:
            raise ValueError("Prompt too long")
        return v

    @validator("temperature")
    def validate_temperature(cls, v):
        if v < 0 or v > 2:
            raise ValueError("Temperature must be 0-2")
        return v
```

---

## 22. Error Recovery Patterns

### 22.1 Dead Letter Queue for Failed Operations

```python
class FailedOperationQueue:
    def __init__(self, max_size: int = 1000):
        self.queue = collections.deque(maxlen=max_size)

    def push(self, operation: dict, error: Exception):
        self.queue.append({
            "operation": operation,
            "error": str(error),
            "timestamp": datetime.utcnow().isoformat()
        })

    async def retry_oldest(self, executor) -> bool:
        if not self.queue:
            return False
        item = self.queue.popleft()
        try:
            await executor(item["operation"])
            return True
        except Exception:
            self.queue.append(item)  # Put back at end
            return False
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)