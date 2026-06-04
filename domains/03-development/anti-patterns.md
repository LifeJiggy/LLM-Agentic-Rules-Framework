# Development Domain - Anti-Patterns

## Overview

This document outlines common development mistakes to avoid in LLM/agentic systems. Anti-patterns are proven-bad approaches that introduce maintainability issues, bugs, or security vulnerabilities. Identifying and actively avoiding these patterns is a prerequisite for robust, production-quality agent development.

---

## Table of Contents

1. [God Classes](#1-god-classes)
2. [Magic Numbers](#2-magic-numbers)
3. [Copy-Paste Code](#3-copy-paste-code)
4. [Deep Nesting](#4-deep-nesting)
5. [Inconsistent Error Handling](#5-inconsistent-error-handling)
6. [Hardcoded Secrets](#6-hardcoded-secrets)
7. [Global State](#7-global-state)
8. [Tight Coupling](#8-tight-coupling)
9. [Premature Optimization](#9-premature-optimization)
10. [Exception Swallowing](#10-exception-swallowing)
11. [Insecure Defaults](#11-insecure-defaults)
12. [Missing Input Validation](#12-missing-input-validation)
13. [Blocking on External Calls](#13-blocking-on-external-calls)
14. [No Timeouts](#14-no-timeouts)
15. [Resource Leaks](#15-resource-leaks)
16. [Unbounded Recursion](#16-unbounded-recursion)
17. [Race Conditions](#17-race-conditions)
18. [Information Leakage](#18-information-leakage)

---

## 1. God Classes

### Problem

A single class or module that knows about or does too many things, leading to tight coupling, poor testability, and maintenance nightmare.

### Anti-Pattern

```python
class AgentController:
    def process_prompt(self, prompt): ...
    def validate_input(self, input): ...
    def call_model(self, prompt): ...
    def parse_response(self, response): ...
    def execute_tool(self, tool_name, args): ...
    def send_email(self, recipient, body): ...
    def save_to_database(self, data): ...
    def generate_report(self, data): ...
    def handle_error(self, error): ...
    def log_audit(self, action): ...
```

### Solution

Decompose into focused classes with single responsibilities:

```python
class PromptValidator:
    def validate(self, prompt: str) -> ValidationResult: ...

class ModelClient:
    def generate(self, prompt: str) -> str: ...

class ToolExecutor:
    def execute(self, tool_name: str, args: dict) -> ToolResult: ...

class AuditLogger:
    def log(self, action: str, metadata: dict) -> None: ...
```

---

## 2. Magic Numbers

### Problem

Hardcoded literal values scattered throughout code make maintenance difficult and intent unclear.

### Anti-Pattern

```python
def process_agent_response(response):
    if len(response.tokens) > 4096:
        return response.truncate(4096)
    if response.confidence < 0.7:
        retry(response.prompt, max_retries=3)
    wait(30)
```

### Solution

Define named constants or configuration:

```python
MAX_RESPONSE_TOKENS = 4096
CONFIDENCE_THRESHOLD = 0.7
MAX_TOOL_RETRIES = 3
RETRY_BACKOFF_SECONDS = 30

def process_agent_response(response):
    if len(response.tokens) > MAX_RESPONSE_TOKENS:
        return response.truncate(MAX_RESPONSE_TOKENS)
    if response.confidence < CONFIDENCE_THRESHOLD:
        retry(response.prompt, max_retries=MAX_TOOL_RETRIES)
    wait(RETRY_BACKOFF_SECONDS)
```

---

## 3. Copy-Paste Code

### Problem

Duplicate code leads to bugs when changes must be made in multiple places, and violates DRY principle.

### Anti-Pattern

```python
def get_user_from_cache(user_id):
    user = cache.get(user_id)
    if user is None:
        user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
        if user:
            cache.set(user_id, user, ttl=300)
    return user

def get_order_from_cache(order_id):
    order = cache.get(order_id)
    if order is None:
        order = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))
        if order:
            cache.set(order_id, order, ttl=300)
    return order
```

### Solution

Abstract common logic into reusable functions:

```python
def get_cached_or_fetch(cache_key: str, query: str, params: tuple, cache_ttl: int = 300):
    cached = cache.get(cache_key)
    if cached:
        return cached
    result = db.query(query, params)
    if result:
        cache.set(cache_key, result, ttl=cache_ttl)
    return result

def get_user(user_id):
    return get_cached_or_fetch(
        f"user:{user_id}",
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

def get_order(order_id):
    return get_cached_or_fetch(
        f"order:{order_id}",
        "SELECT * FROM orders WHERE id = ?",
        (order_id,)
    )
```

---

## 4. Deep Nesting

### Problem

Excessive nesting makes code hard to read, test, and maintain.

### Anti-Pattern

```python
def process_agent_request(request):
    if request is not None:
        if request.has_valid_input:
            if request.user_authenticated:
                if request.user_has_permission:
                    if request.rate_limit_ok:
                        if request.prompt_injection_check:
                            result = call_model(request.prompt)
                            if result.success:
                                if result.has_tool_calls:
                                    for tool in result.tool_calls:
                                        if tool.name in allowed_tools:
                                            execute_tool(tool)
                                return result.response
                            else:
                                return error_response("model_failed")
                        else:
                            return error_response("injection_blocked")
                    else:
                        return error_response("rate_limited")
                else:
                    return error_response("unauthorized")
            else:
                return error_response("auth_failed")
        else:
            return error_response("invalid_input")
    else:
        return error_response("missing_request")
```

### Solution

Use early returns and guard clauses:

```python
def process_agent_request(request):
    if request is None:
        return error_response("missing_request")
    if not request.has_valid_input:
        return error_response("invalid_input")
    if not request.user_authenticated:
        return error_response("auth_failed")
    if not request.user_has_permission:
        return error_response("unauthorized")
    if not request.rate_limit_ok:
        return error_response("rate_limited")
    if not request.prompt_injection_check:
        return error_response("injection_blocked")

    result = call_model(request.prompt)
    if not result.success:
        return error_response("model_failed")

    if result.has_tool_calls:
        for tool in result.tool_calls:
            if tool.name in allowed_tools:
                execute_tool(tool)

    return result.response
```

---

## 5. Inconsistent Error Handling

### Problem

Different error handling patterns throughout codebase make debugging difficult and hide issues.

### Anti-Pattern

```python
def fetch_user(user_id):
    try:
        return db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    except:
        return None

def fetch_order(order_id):
    if order_id is None:
        raise ValueError("Order ID required")
    try:
        return db.query("SELECT * FROM orders WHERE id = ?", (order_id,))
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_product(product_id):
    user = db.query("SELECT * FROM products WHERE id = ?", (product_id,))
    if not user:
        return {"error": "Not found"}
    return user
```

### Solution

Establish consistent error handling patterns:

```python
class UserNotFoundError(Exception):
    pass

class DatabaseError(Exception):
    def __init__(self, cause: Exception):
        self.cause = cause
        super().__init__(f"Database error: {cause}")

def fetch_user(user_id: int) -> Dict:
    if user_id is None:
        raise ValueError("User ID required")
    try:
        result = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
        if not result:
            raise UserNotFoundError(user_id)
        return result[0]
    except DatabaseError:
        raise
    except Exception as e:
        raise DatabaseError(e)
```

---

## 6. Hardcoded Secrets

### Problem

Embedding secrets in source code creates security vulnerabilities and deployment issues.

### Anti-Pattern

```python
OPENAI_API_KEY = "sk-abc123..."
DATABASE_URL = "postgresql://admin:password123@prod-db:5432/data"

def get_model_client():
    return OpenAI(api_key=OPENAI_API_KEY)
```

### Solution

Load secrets from secure sources:

```python
import os
from hvac import Client

class SecretManager:
    def __init__(self):
        self._vault = Client(url=os.environ.get("VAULT_ADDR"), token=os.environ.get("VAULT_TOKEN"))
        self._cache = {}

    def get(self, secret_name: str) -> str:
        if secret_name in self._cache:
            return self._cache[secret_name]
        secret = self._vault.secrets.kv.v2.read_secret_version(path=secret_name)
        value = secret["data"]["data"]["value"]
        self._cache[secret_name] = value
        return value

secrets = SecretManager()
OPENAI_API_KEY = secrets.get("openai_api_key")
DATABASE_URL = secrets.get("database_url")
```

---

## 7. Global State

### Problem

Shared mutable global state creates race conditions, testing difficulties, and unpredictable behavior.

### Anti-Pattern

```python
user_sessions = {}
current_user = None

def login(user_id):
    global current_user
    current_user = user_id
    user_sessions[user_id] = {"active": True}

def get_current_user():
    return current_user
```

### Solution

Pass state explicitly and use thread-safe structures:

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class SessionContext:
    user_id: Optional[str]
    session_id: str
    is_active: bool = True

class SessionManager:
    def __init__(self):
        self._sessions = {}
        self._lock = threading.Lock()

    def create_session(self, user_id: str) -> str:
        session_id = secrets.token_urlsafe(32)
        with self._lock:
            self._sessions[session_id] = SessionContext(user_id=user_id, session_id=session_id)
        return session_id

    def get_context(self, session_id: str) -> Optional[SessionContext]:
        with self._lock:
            return self._sessions.get(session_id)
```

---

## 8. Tight Coupling

### Problem

Components depend on concrete implementations rather than abstractions, making testing and refactoring difficult.

### Anti-Pattern

```python
class AgentService:
    def __init__(self):
        self.llm = OpenAI(api_key=os.environ["OPENAI_KEY"])
        self.db = psycopg2.connect(os.environ["DATABASE_URL"])

    def respond(self, prompt):
        response = self.llm.chat.completions.create(...)
        return response.choices[0].message.content
```

### Solution

Depend on abstractions and inject dependencies:

```python
class ModelClient(Protocol):
    def generate(self, prompt: str) -> str: ...

class Repository(Protocol):
    def save(self, entity: Any) -> None: ...

class AgentService:
    def __init__(self, model: ModelClient, repository: Repository):
        self.model = model
        self.repository = repository

    def respond(self, prompt: str) -> str:
        return self.model.generate(prompt)
```

---

## 9. Premature Optimization

### Problem

Optimizing before measuring creates complex, hard-to-maintain code with unclear benefits.

### Anti-Pattern

```python
def process_messages(messages):
    # Overly complex caching strategy before proving it's needed
    cache_keys = [f"msg:{hash(m)}" for m in messages]
    cached_results = {}
    for key in cache_keys:
        cached_results[key] = redis_client.get(key) or {}
    # Complex batch processing logic...
```

### Solution

Start simple and optimize when needed:

```python
def process_messages(messages):
    results = []
    for message in messages:
        result = process_single_message(message)
        results.append(result)
    return results

# Only optimize after profiling shows this is a bottleneck
```

---

## 10. Exception Swallowing

### Problem

Silently catching exceptions hides bugs and makes debugging impossible.

### Anti-Pattern

```python
try:
    result = external_api.call()
    return result
except:
    return None
```

### Solution

Handle specific exceptions appropriately:

```python
try:
    result = external_api.call()
    return result
except APITimeoutError:
    logger.warning("API timeout, using cached value")
    return get_cached_value()
except APIAuthenticationError as e:
    logger.error(f"API auth failed: {e}")
    raise ServiceUnavailable("API authentication failed")
except Exception as e:
    logger.exception("Unexpected error calling API")
    raise
```

---

## 11. Insecure Defaults

### Problem

Default configurations that prioritize convenience over security create vulnerabilities.

### Anti-Pattern

```python
class AgentConfig:
    def __init__(self):
        self.require_auth = False
        self.rate_limit = 0
        self.max_tokens = 1000000
        self.debug_mode = True
        self.log_prompts = True
        self.log_responses = True
```

### Solution

Secure-by-default configurations:

```python
class AgentConfig:
    def __init__(self):
        self.require_auth = True
        self.rate_limit = 60
        self.max_tokens = 4096
        self.debug_mode = False
        self.log_prompts = False
        self.log_responses = False
```

---

## 12. Missing Input Validation

### Problem

Trusting external input leads to injection vulnerabilities and unexpected behavior.

### Anti-Pattern

```python
def process_user_text(user_input):
    prompt = f"You are helpful. User said: {user_input}"
    response = model.generate(prompt)
    return response
```

### Solution

Validate and sanitize all inputs:

```python
def process_user_text(user_input):
    if not isinstance(user_input, str):
        raise TypeError("Input must be string")
    if len(user_input) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input exceeds {MAX_INPUT_LENGTH} characters")
    sanitized = sanitize_input(user_input)
    if detected_injection(sanitized):
        raise SecurityError("Injection detected")
    prompt = f"You are helpful.\nUser input (data only): {sanitized}"
    return model.generate(prompt)
```

---

## 13. Blocking on External Calls

### Problem

Blocking on slow external calls reduces system throughput and creates poor user experience.

### Anti-Pattern

```python
def handle_request(request):
    result = slow_database_call()
    result2 = external_api_call()
    return combine_results(result, result2)
```

### Solution

Use timeouts and async patterns:

```python
async def handle_request(request):
    try:
        result = await asyncio.wait_for(slow_database_call(), timeout=5.0)
    except asyncio.TimeoutError:
        result = None
    try:
        result2 = await asyncio.wait_for(external_api_call(), timeout=10.0)
    except asyncio.TimeoutError:
        result2 = None
    return combine_results(result, result2)
```

---

## 14. No Timeouts

### Problem

Missing timeouts can cause requests to hang indefinitely, exhausting resources.

### Anti-Pattern

```python
response = requests.get("https://api.example.com/data")
data = response.json()
```

### Solution

Always use timeouts:

```python
try:
    response = requests.get("https://api.example.com/data", timeout=30)
    data = response.json()
except requests.Timeout:
    logger.error("Request timed out")
    data = None
```

---

## 15. Resource Leaks

### Problem

Unclosed resources (files, connections, handles) can exhaust system resources.

### Anti-Pattern

```python
def process_file(filename):
    f = open(filename)
    data = json.load(f)
    return process(data)
```

### Solution

Use context managers:

```python
def process_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return process(data)
```

---

## 16. Unbounded Recursion

### Problem

Unlimited recursion can cause stack overflow and crashes.

### Anti-Pattern

```python
def process_context(context):
    response = model.generate(context)
    if "requires more context" in response:
        return process_context(context + more_data)
    return response
```

### Solution

Bound recursion depth:

```python
def process_context(context, depth=0, max_depth=5):
    if depth >= max_depth:
        raise RecursionError("Max context depth exceeded")
    response = model.generate(context)
    if "requires more context" in response:
        return process_context(context + more_data, depth + 1, max_depth)
    return response
```

---

## 17. Race Conditions

### Problem

Unsynchronized access to shared state causes unpredictable behavior.

### Anti-Pattern

```python
session_count = 0

def increment_session():
    global session_count
    session_count += 1
```

### Solution

Use atomic operations or locks:

```python
import threading

class SessionCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._count += 1
            return self._count
```

---

## 18. Information Leakage

### Problem

Returning internal details in error messages or responses compromises security.

### Anti-Pattern

```python
except Exception as e:
    return {"error": str(e), "traceback": traceback.format_exc()}
```

### Solution

Generic error responses with internal logging:

```python
except Exception as e:
    logger.error(f"Internal error: {e}\n{traceback.format_exc()}")
    return {"error": "An internal error occurred. Please try again."}
```

---

## 19. Logging Sensitive Information

### Problem

Logging secrets, PII, or internal state creates security risks and compliance violations.

### Anti-Pattern

```python
def process_user(user):
    logger.info(f"Processing user with password: {user.password}")
    logger.debug(f"Full user record: {user.__dict__}")
```

### Solution

Mask sensitive data in logs:

```python
def process_user(user):
    safe_user = {"id": user.id, "email": mask_email(user.email)}
    logger.info(f"Processing user: {safe_user}")
```

---

## 20. Unbounded Memory Growth

### Problem

Storing unlimited data in memory can cause OOM conditions in long-running agents.

### Anti-Pattern

```python
class AgentMemory:
    def __init__(self):
        self.messages = []

    def add(self, msg):
        self.messages.append(msg)  # Grows unbounded
```

### Solution

Implement bounded memory with LRU eviction:

```python
from collections import deque
MAX_MESSAGES = 1000

class AgentMemory:
    def __init__(self):
        self.messages = deque(maxlen=MAX_MESSAGES)

    def add(self, msg):
        self.messages.append(msg)
```

---

## 21. Silent Failures

### Problem

Failures that don't raise exceptions or log errors are impossible to debug.

### Anti-Pattern

```python
def optional_tool_call(tool_name, args):
    try:
        return execute_tool(tool_name, args)
    except:
        pass  # Silently ignore all failures
    return None
```

### Solution

Explicit error handling with logging:

```python
def optional_tool_call(tool_name, args):
    try:
        return execute_tool(tool_name, args)
    except ToolNotFoundError:
        logger.warning(f"Tool {tool_name} not found")
    except PermissionDenied:
        logger.warning(f"Permission denied for tool {tool_name}")
    except Exception as e:
        logger.error(f"Tool {tool_name} failed: {e}")
    return None
```

---

## 22. Inconsistent API Patterns

### Problem

Mixed API patterns make code harder to use and maintain.

### Anti-Pattern

```python
class ToolRegistry:
    def get_tool(self, name): ...
    def find_tool(self, name): ...  # Different name, same purpose?
    def retrieve_tool(self, id): ...  # Different parameter?
```

### Solution

Consistent naming and parameter patterns:

```python
class ToolRegistry:
    def get(self, tool_id: str) -> Optional[Tool]: ...
    def find_by_name(self, name: str) -> Optional[Tool]: ...
    def list_all(self) -> List[Tool]: ...
```

---

## 23. Overfetching Data

### Problem

Retrieving more data than needed wastes resources and slows responses.

### Anti-Pattern

```python
def get_user_profile(user_id):
    user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    return user  # Returns all columns including sensitive data
```

### Solution

Explicit field selection:

```python
def get_user_profile(user_id):
    user = db.query(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,)
    )
    return user
```

---

## 24. Unhandled Promise States

### Problem

Async operations without proper error handling can silently fail.

### Anti-Pattern

```python
async def process_async():
    result = asyncio.create_task(slow_operation())
    # No await, no error handling
    return "done"
```

### Solution

Proper async/await with error handling:

```python
async def process_async():
    try:
        result = await slow_operation()
        return result
    except asyncio.CancelledError:
        logger.warning("Operation cancelled")
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

---

## 25. Magic Strings

### Problem

Hardcoded string literals scattered in code create maintenance challenges.

### Anti-Pattern

```python
if status == "active":
    process_active()
elif status == "pending":
    process_pending()
```

### Solution

Use enums or constants:

```python
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETE = "complete"

if status == Status.ACTIVE:
    process_active()
```

---

## 26. Inconsistent API Response Formats

### Problem

Mixing response formats makes client code complex and error-prone.

### Anti-Pattern

```python
def get_user():
    return {"data": user, "status": "ok"}  # One format

def get_order():
    return {"result": order}  # Different format

def get_product():
    return product  # Raw object
```

### Solution

Consistent response envelope:

```python
def format_response(data, status="success"):
    return {"data": data, "status": status, "timestamp": now_iso()}

def get_user():
    return format_response(user)
```

---

## 27. Unvalidated Configuration

### Problem

Missing configuration validation causes runtime errors in production.

### Anti-Pattern

```python
class Config:
    def __init__(self):
        self.timeout = os.environ.get("TIMEOUT")  # Could be None or invalid string
```

### Solution

Validate configuration at startup:

```python
from pydantic import BaseSettings, validator

class Config(BaseSettings):
    timeout: int = 30

    @validator("timeout")
    def validate_timeout(cls, v):
        if v < 1 or v > 300:
            raise ValueError("Timeout must be 1-300 seconds")
        return v
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)