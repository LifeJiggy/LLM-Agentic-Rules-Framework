# Development Domain - Advanced Concepts

## Overview

This document covers advanced development concepts for LLM/agentic systems, including architectural patterns, design principles, testing strategies, and production-grade implementation guidance. All concepts are presented with production considerations, security implications, and integration examples.

---

## Table of Contents

1. [Dependency Injection](#1-dependency-injection)
2. [Event-Driven Architecture](#2-event-driven-architecture)
3. [Repository Pattern](#3-repository-pattern)
4. [Strategy Pattern](#4-strategy-pattern)
5. [Observer Pattern](#5-observer-pattern)
6. [State Machine Pattern](#6-state-machine-pattern)
7. [Factory Pattern](#7-factory-pattern)
8. [Decorator Pattern](#8-decorator-pattern)
9. [Command Pattern](#9-command-pattern)
10. [Mediator Pattern](#10-mediator-pattern)
11. [Chain of Responsibility](#11-chain-of-responsibility)
12. [Adapter Pattern](#12-adapter-pattern)
13. [Facade Pattern](#13-facade-pattern)
14. [Builder Pattern](#14-builder-pattern)
15. [Template Method Pattern](#15-template-method-pattern)
16. [Abstract Factory Pattern](#16-abstract-factory-pattern)
17. [Flyweight Pattern](#17-flyweight-pattern)
18. [Proxy Pattern](#18-proxy-pattern)
19. [Composite Pattern](#19-composite-pattern)
20. [Bridge Pattern](#20-bridge-pattern)

---

## 1. Dependency Injection

Dependency Injection (DI) is a design pattern that allows components to receive their dependencies from external sources rather than creating them internally. This promotes loose coupling, testability, and flexibility in agentic systems.

### 1.1 Dependency Injection Container

```python
from typing import Protocol, Type, TypeVar, Generic, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod
import inspect


T = TypeVar('T')


class Provider(Protocol):
    def get(self) -> Any: ...


class Container:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._locks: Dict[str, threading.Lock] = {}

    def register(self, name: str, service: Any, singleton: bool = False) -> None:
        if singleton:
            self._singletons[name] = service
        else:
            self._services[name] = service

    def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
        self._factories[name] = factory

    def resolve(self, name: str) -> Any:
        if name in self._singletons:
            return self._singletons[name]
        if name in self._services:
            return self._services[name]
        if name in self._factories:
            return self._factories[name]()
        raise KeyError(f"Service '{name}' not registered")

    def resolve_all(self, name: str) -> Any:
        service = self.resolve(name)
        if hasattr(service, '__iter__') and not isinstance(service, (str, bytes)):
            return list(service)
        return [service]


class Database(ABC):
    @abstractmethod
    def query(self, sql: str, params: tuple = ()) -> list: ...

    @abstractmethod
    def execute(self, sql: str, params: tuple = ()) -> int: ...


class PostgresDatabase(Database):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._pool: Optional[Any] = None

    def query(self, sql: str, params: tuple = ()) -> list:
        if not self._pool:
            self._pool = self._create_pool()
        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def execute(self, sql: str, params: tuple = ()) -> int:
        if not self._pool:
            self._pool = self._create_pool()
        with self._pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.rowcount

    def _create_pool(self):
        import psycopg2.pool
        return psycopg2.pool.ThreadedConnectionPool(
            minconn=5, maxconn=20,
            dsn=self.connection_string
        )


class UserService:
    def __init__(self, db: Database, cache: Optional[Any] = None):
        self.db = db
        self.cache = cache

    def get_user(self, user_id: int) -> Optional[Dict]:
        if self.cache:
            cached = self.cache.get(f"user:{user_id}")
            if cached:
                return cached

        result = self.db.query(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,)
        )
        user = result[0] if result else None

        if user and self.cache:
            self.cache.set(f"user:{user_id}", user, ttl=300)

        return user


class SecureDatabase(Database):
    def __init__(self, inner: Database, audit_logger: Callable):
        self.inner = inner
        self.audit_logger = audit_logger

    def query(self, sql: str, params: tuple = ()) -> list:
        self.audit_logger(f"QUERY: {sql} - params masked")
        return self.inner.query(sql, params)

    def execute(self, sql: str, params: tuple = ()) -> int:
        self.audit_logger(f"EXECUTE: {sql} - params masked")
        return self.inner.execute(sql, params)


def create_container() -> Container:
    container = Container()
    container.register_factory('db', lambda: PostgresDatabase(os.environ.get('DATABASE_URL')))
    container.register_factory('audit', lambda: lambda msg: print(f"[AUDIT] {msg}"))
    container.register('secure_db', SecureDatabase(container.resolve('db'), container.resolve('audit')))
    container.register('user_service', UserService(container.resolve('secure_db')))
    return container
```

### 1.2 Agent-Scoped Dependency Injection

```python
class AgentExecutionContext:
    def __init__(self, user_id: str, session_id: str, container: Container):
        self.user_id = user_id
        self.session_id = session_id
        self.container = container
        self.scoped_services: Dict[str, Any] = {}

    def get_service(self, name: str) -> Any:
        if name in self.scoped_services:
            return self.scoped_services[name]
        service = self.container.resolve(name)
        if hasattr(service, 'set_context'):
            service.set_context(self.user_id, self.session_id)
        return service

    def set_scoped_service(self, name: str, service: Any) -> None:
        self.scoped_services[name] = service


class ContextAwareService:
    def set_context(self, user_id: str, session_id: str) -> None:
        self.context_user_id = user_id
        self.context_session_id = session_id

    def get_context(self) -> tuple:
        return getattr(self, 'context_user_id', None), getattr(self, 'context_session_id', None)


class UserScopedStorageService(ContextAwareService):
    def __init__(self, base_storage: Any):
        self.base_storage = base_storage

    def get_user_data(self, key: str) -> Any:
        user_id, session_id = self.get_context()
        scoped_key = f"user:{user_id}:{session_id}:{key}"
        return self.base_storage.get(scoped_key)

    def set_user_data(self, key: str, value: Any) -> None:
        user_id, session_id = self.get_context()
        scoped_key = f"user:{user_id}:{session_id}:{key}"
        self.base_storage.set(scoped_key, value)
```

---

## 2. Event-Driven Architecture

Event-driven architecture enables loose coupling between components and supports asynchronous processing in agent systems.

### 2.1 Event Bus with Priority and Filtering

```python
import asyncio
import logging
from typing import Callable, Dict, List, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class EventPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    name: str
    data: Any
    priority: EventPriority = EventPriority.NORMAL
    source: str = "unknown"
    timestamp: str = ""
    event_id: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._priority_handlers: Dict[str, Dict[EventPriority, List[Callable]]] = {}
        self._filters: Dict[str, List[Callable[[Event], bool]]] = {}
        self._logger = logging.getLogger(__name__)
        self._stats: Dict[str, int] = {}

    def subscribe(self, event: str, handler: Callable[[Event], None], priority: EventPriority = EventPriority.NORMAL) -> None:
        if event not in self._priority_handlers:
            self._priority_handlers[event] = {}

        priority_handlers = self._priority_handlers[event]
        if priority not in priority_handlers:
            priority_handlers[priority] = []

        priority_handlers[priority].append(handler)
        self._subscribers.setdefault(event, []).append(handler)

    def add_filter(self, event: str, filter_fn: Callable[[Event], bool]) -> None:
        self._filters.setdefault(event, []).append(filter_fn)

    async def publish(self, event: Event) -> List[Any]:
        handlers = self._priority_handlers.get(event.name, {})
        ordered_priorities = sorted(handlers.keys(), key=lambda p: p.value, reverse=True)

        results = []
        for priority in ordered_priorities:
            for handler in handlers[priority]:
                if self._passes_filters(event):
                    try:
                        result = handler(event)
                        if asyncio.iscoroutine(result):
                            result = await result
                        results.append(result)
                        self._stats[event.name] = self._stats.get(event.name, 0) + 1
                    except Exception as e:
                        self._logger.error(f"Handler failed for {event.name}: {e}")

        return results

    def _passes_filters(self, event: Event) -> bool:
        filters = self._filters.get(event.name, [])
        return all(f(event) for f in filters)

    def get_stats(self) -> Dict[str, int]:
        return self._stats.copy()


class AgentEventManager:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self._register_handlers()

    def _register_handlers(self):
        self.bus.subscribe('user_action', self._handle_user_action, EventPriority.HIGH)
        self.bus.subscribe('tool_result', self._handle_tool_result, EventPriority.NORMAL)
        self.bus.subscribe('error', self._handle_error, EventPriority.CRITICAL)
        self.bus.add_filter('user_action', lambda e: e.data.get('user_id') is not None)

    async def _handle_user_action(self, event: Event):
        await self._log_action(event)
        await self._update_context(event)

    async def _handle_tool_result(self, event: Event):
        result = event.data.get('result')
        if result and result.get('error'):
            await self.bus.publish(Event(
                name='tool_error',
                data=event.data,
                priority=EventPriority.HIGH,
                source=event.source
            ))

    async def _handle_error(self, event: Event):
        self._logger.critical(f"CRITICAL ERROR: {event.data}")
        await self._alert_operators(event)

    async def _log_action(self, event: Event):
        pass

    async def _update_context(self, event: Event):
        pass

    async def _alert_operators(self, event: Event):
        pass
```

---

## 3. Repository Pattern

The repository pattern abstracts data access, providing a collection-like interface for domain objects.

### 3.1 Generic Repository with Transaction Support

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Generic, TypeVar
from contextlib import contextmanager


T = TypeVar('T', bound='Entity')


@dataclass
class Entity:
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Repository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> Optional[T]: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, entity: T) -> None: ...

    @abstractmethod
    def find(self, **criteria) -> List[T]: ...


class TransactionManager:
    def __init__(self):
        self._active_transactions: Dict[str, Any] = {}

    @contextmanager
    def transaction(self, tx_id: Optional[str] = None):
        transaction_id = tx_id or str(uuid.uuid4())
        self._active_transactions[transaction_id] = True
        try:
            yield transaction_id
            self._active_transactions.pop(transaction_id, None)
        except Exception:
            self._active_transactions.pop(transaction_id, None)
            raise


class DatabaseBackedRepository(Repository[T]):
    def __init__(self, db: Database, transaction_manager: Optional[TransactionManager] = None):
        self.db = db
        self.tx_manager = transaction_manager

    def get(self, id: int) -> Optional[T]:
        result = self.db.query(f"SELECT * FROM {self._table} WHERE id = %s", (id,))
        if not result:
            return None
        return self._from_row(result[0])

    def save(self, entity: T) -> T:
        if entity.id is None:
            entity.id = self._insert(entity)
            entity.created_at = datetime.utcnow()
        else:
            self._update(entity)
            entity.updated_at = datetime.utcnow()
        return entity

    def delete(self, entity: T) -> None:
        self.db.execute(f"DELETE FROM {self._table} WHERE id = %s", (entity.id,))

    def find(self, **criteria) -> List[T]:
        where_clause = " AND ".join(f"{k} = %s" for k in criteria.keys())
        query = f"SELECT * FROM {self._table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        result = self.db.query(query, tuple(criteria.values()))
        return [self._from_row(row) for row in result]

    @abstractmethod
    def _table(self) -> str: ...

    @abstractmethod
    def _from_row(self, row: tuple) -> T: ...

    @abstractmethod
    def _insert(self, entity: T) -> int: ...

    @abstractmethod
    def _update(self, entity: T) -> None: ...


class UserRepository(DatabaseBackedRepository[Entity]):
    @property
    def _table(self) -> str:
        return "users"

    def _from_row(self, row: tuple) -> Entity:
        return Entity(id=row[0], created_at=row[1], updated_at=row[2])

    def _insert(self, entity: Entity) -> int:
        return self.db.execute(
            f"INSERT INTO {self._table} (created_at) VALUES (%s) RETURNING id",
            (entity.created_at,)
        )

    def _update(self, entity: Entity) -> None:
        self.db.execute(
            f"UPDATE {self._table} SET updated_at = %s WHERE id = %s",
            (entity.updated_at, entity.id)
        )
```

---

## 4. Strategy Pattern

The strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

### 4.1 Prompt Processing Strategy

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import nltk


class PromptStrategy(ABC):
    @abstractmethod
    def process(self, prompt: str, context: Dict[str, Any]) -> str: ...

    @abstractmethod
    def can_handle(self, prompt: str, context: Dict[str, Any]) -> bool: ...


class SummarizeStrategy(PromptStrategy):
    def process(self, prompt: str, context: Dict[str, Any]) -> str:
        return f"Summarize the following content:\n\n{prompt}\n\nSummary:"

    def can_handle(self, prompt: str, context: Dict[str, Any]) -> bool:
        return "summarize" in prompt.lower() or "summary" in prompt.lower()


class TranslateStrategy(PromptStrategy):
    def __init__(self, target_language: str):
        self.target_language = target_language

    def process(self, prompt: str, context: Dict[str, Any]) -> str:
        return f"Translate to {self.target_language}:\n\n{prompt}\n\nTranslation:"

    def can_handle(self, prompt: str, context: Dict[str, Any]) -> str:
        return "translate" in prompt.lower()


class PromptStrategySelector:
    def __init__(self, strategies: Optional[List[PromptStrategy]] = None):
        self.strategies = strategies or [
            SummarizeStrategy(),
            TranslateStrategy("English"),
        ]

    def select(self, prompt: str, context: Dict[str, Any]) -> Optional[PromptStrategy]:
        for strategy in self.strategies:
            if strategy.can_handle(prompt, context):
                return strategy
        return None

    def process(self, prompt: str, context: Dict[str, Any]) -> Optional[str]:
        strategy = self.select(prompt, context)
        if strategy:
            return strategy.process(prompt, context)
        return None
```

---

## 5. Observer Pattern

The observer pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

### 5.1 Agent State Observer

```python
from typing import Callable, Dict, List, Any
from enum import Enum


class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING_TOOL = "executing_tool"
    WAITING = "waiting"
    COMPLETE = "complete"
    ERROR = "error"


class AgentStateObserver:
    def __init__(self):
        self._observers: Dict[AgentState, List[Callable]] = {}
        self._current_state: Optional[AgentState] = None

    def register(self, state: AgentState, callback: Callable[[Any], None]) -> None:
        self._observers.setdefault(state, []).append(callback)

    def notify(self, state: AgentState, data: Any = None) -> None:
        self._current_state = state
        callbacks = self._observers.get(state, [])
        for callback in callbacks:
            callback(data)

    def get_current_state(self) -> Optional[AgentState]:
        return self._current_state


class ObservableAgent:
    def __init__(self):
        self._state_observer = AgentStateObserver()
        self._register_default_observers()

    def _register_default_observers(self):
        self._state_observer.register(AgentState.THINKING, lambda d: self._log_thinking(d))
        self._state_observer.register(AgentState.EXECUTING_TOOL, lambda d: self._log_tool(d))
        self._state_observer.register(AgentState.ERROR, lambda d: self._handle_error(d))

    def _transition_to(self, state: AgentState, data: Any = None):
        self._state_observer.notify(state, data)

    def _log_thinking(self, data):
        pass

    def _log_tool(self, data):
        pass

    def _handle_error(self, data):
        pass
```

---

## 6. State Machine Pattern

The state machine pattern allows an object to alter its behavior when its internal state changes.

### 6.1 Agent Execution State Machine

```python
from enum import Enum, auto
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass


class ExecutionState(Enum):
    INITIAL = auto()
    VALIDATING_INPUT = auto()
    BUILDING_PROMPT = auto()
    CALLING_MODEL = auto()
    PROCESSING_RESPONSE = auto()
    EXECUTING_TOOL = auto()
    WAITING_FOR_CONFIRMATION = auto()
    COMPLETE = auto()
    ERROR = auto()


@dataclass
class StateTransition:
    from_state: ExecutionState
    to_state: ExecutionState
    handler: Optional[Callable] = None


class AgentStateMachine:
    def __init__(self):
        self.current_state = ExecutionState.INITIAL
        self._transitions: List[StateTransition] = []
        self._context: Dict[str, Any] = {}
        self._register_transitions()

    def _register_transitions(self):
        transitions = [
            (ExecutionState.INITIAL, ExecutionState.VALIDATING_INPUT),
            (ExecutionState.VALIDATING_INPUT, ExecutionState.BUILDING_PROMPT),
            (ExecutionState.BUILDING_PROMPT, ExecutionState.CALLING_MODEL),
            (ExecutionState.CALLING_MODEL, ExecutionState.PROCESSING_RESPONSE),
            (ExecutionState.PROCESSING_RESPONSE, ExecutionState.EXECUTING_TOOL),
            (ExecutionState.EXECUTING_TOOL, ExecutionState.COMPLETE),
            (ExecutionState.EXECUTING_TOOL, ExecutionState.WAITING_FOR_CONFIRMATION),
        ]
        for from_s, to_s in transitions:
            self._transitions.append(StateTransition(from_s, to_s))

    def transition_to(self, new_state: ExecutionState, context: Optional[Dict] = None) -> None:
        if context:
            self._context.update(context)

        valid_transition = any(
            t.from_state == self.current_state and t.to_state == new_state
            for t in self._transitions
        )

        if not valid_transition:
            raise ValueError(f"Invalid state transition: {self.current_state} -> {new_state}")

        self.current_state = new_state

    def can_transition_to(self, state: ExecutionState) -> bool:
        return any(
            t.from_state == self.current_state and t.to_state == state
            for t in self._transitions
        )
```

---

## 7. Factory Pattern

The factory pattern provides an interface for creating objects in a superclass, but allows subclasses to alter the types of objects that will be created.

### 7.1 Tool Factory for Agent Systems

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Tool(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> Any: ...

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_description(self) -> str: ...


class FileReadTool(Tool):
    def execute(self, path: str) -> str:
        with open(path) as f:
            return f.read()

    def get_name(self) -> str:
        return "file_read"

    def get_description(self) -> str:
        return "Read file contents"


class DatabaseQueryTool(Tool):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def execute(self, query: str) -> list:
        pass

    def get_name(self) -> str:
        return "database_query"

    def get_description(self) -> str:
        return "Execute database query"


class ToolFactory:
    def __init__(self):
        self._tool_configs: Dict[str, Dict] = {}

    def register_tool(self, name: str, config: Dict) -> None:
        self._tool_configs[name] = config

    def create_tool(self, name: str, **kwargs) -> Tool:
        if name == "file_read":
            return FileReadTool()
        elif name == "database_query":
            connection_string = kwargs.get('connection_string') or self._tool_configs[name].get('connection_string')
            return DatabaseQueryTool(connection_string)
        raise ValueError(f"Unknown tool: {name}")

    def create_from_spec(self, spec: Dict) -> Tool:
        return self.create_tool(spec['name'], **spec.get('config', {}))
```

---

## 8. Decorator Pattern

The decorator pattern allows behavior to be added to individual objects, either statically or dynamically, without affecting the behavior of other objects from the same class.

### 8.1 Tool Execution Decorator

```python
import functools
import time
from typing import Callable, Any, Optional
from datetime import datetime


def with_retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator


def with_circuit_breaker(circuit_breaker: Any):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return circuit_breaker.call(lambda: func(*args, **kwargs))
        return wrapper
    return decorator


def with_timeout(seconds: int):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import signal
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator
```

---

## 9. Command Pattern

The command pattern encapsulates a request as an object, thereby allowing for parameterization of clients with queues, requests, and operations.

### 9.1 Agent Command Queue

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import uuid


class Command(ABC):
    def __init__(self, command_id: Optional[str] = None):
        self.command_id = command_id or str(uuid.uuid4())
        self.created_at = datetime.utcnow()

    @abstractmethod
    def execute(self) -> Any: ...

    @abstractmethod
    def undo(self) -> None: ...


class ToolCommand(Command):
    def __init__(self, tool_name: str, tool_args: Dict, command_id: Optional[str] = None):
        super().__init__(command_id)
        self.tool_name = tool_name
        self.tool_args = tool_args
        self._result = None

    def execute(self) -> Any:
        tool = ToolFactory().create_tool(self.tool_name)
        self._result = tool.execute(**self.tool_args)
        return self._result

    def undo(self) -> None:
        if self.tool_name == "file_write":
            import os
            path = self.tool_args.get('path')
            if path and os.path.exists(path):
                os.remove(path)


class CommandQueue:
    def __init__(self):
        self._queue: list = []
        self._executed: list = []
        self._undone: list = []

    def enqueue(self, command: Command) -> str:
        self._queue.append(command)
        return command.command_id

    def execute_next(self) -> Any:
        if not self._queue:
            return None
        command = self._queue.pop(0)
        result = command.execute()
        self._executed.append(command)
        return result

    def undo_last(self) -> None:
        if not self._executed:
            return
        command = self._executed.pop()
        command.undo()
        self._undone.append(command)
```

---

## 10. Mediator Pattern

The mediator pattern defines an object that encapsulates how a set of objects interact, promoting loose coupling.

### 10.1 Agent Component Mediator

```python
from typing import Any, Dict, Optional


class ComponentMediator:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._handlers: Dict[str, Callable] = {}

    def register(self, name: str, component: Any) -> None:
        self._components[name] = component

    def send(self, sender: str, message: str, data: Any) -> Any:
        handler = self._handlers.get(message)
        if handler:
            return handler(sender, data)
        raise ValueError(f"No handler for message: {message}")

    def register_handler(self, message: str, handler: Callable) -> None:
        self._handlers[message] = handler


class PromptBuildingMediator(ComponentMediator):
    def __init__(self):
        super().__init__()
        self._register_handlers()

    def _register_handlers(self):
        self.register_handler('build_prompt', self._build_prompt)
        self.register_handler('validate_input', self._validate_input)

    def _build_prompt(self, sender: str, data: Dict) -> str:
        if 'prompt_builder' not in self._components:
            return ""
        return self._components['prompt_builder'].build(data['prompt'], data.get('context', {}))

    def _validate_input(self, sender: str, data: Dict) -> bool:
        if 'validator' not in self._components:
            return True
        return self._components['validator'].validate(data['input'])
```

---

## 11. Chain of Responsibility

The chain of responsibility pattern passes a request along a chain of handlers, allowing multiple objects to handle the request without coupling the sender to the receiver.

### 11.1 Security Validation Chain

```python
from typing import Any, Optional, List


class Handler:
    def __init__(self, next_handler: Optional['Handler'] = None):
        self.next_handler = next_handler

    def handle(self, request: Any) -> Any:
        if self.next_handler:
            return self.next_handler.handle(request)
        return request


class InputValidationHandler(Handler):
    def handle(self, request: Any) -> Any:
        if not isinstance(request, dict):
            raise TypeError("Request must be a dictionary")
        if 'prompt' not in request:
            raise ValueError("Missing required 'prompt' field")
        return super().handle(request)


class InjectionDetectionHandler(Handler):
    def handle(self, request: Any) -> Any:
        prompt = request.get('prompt', '')
        if self._detect_injection(prompt):
            raise ValueError("Potential prompt injection detected")
        return super().handle(request)

    def _detect_injection(self, prompt: str) -> bool:
        patterns = [
            r"ignore.*instructions",
            r"new.*rules",
            r"system.*prompt",
        ]
        import re
        return any(re.search(p, prompt, re.IGNORECASE) for p in patterns)


class RateLimitHandler(Handler):
    def __init__(self, next_handler: Optional[Handler] = None, limit: int = 60):
        super().__init__(next_handler)
        self.limit = limit
        self._counts: Dict[str, int] = {}
        self._window_start: Dict[str, float] = {}

    def handle(self, request: Any) -> Any:
        user_id = request.get('user_id', 'anonymous')
        now = time.time()

        if user_id not in self._counts or now - self._window_start.get(user_id, now) > 60:
            self._counts[user_id] = 0
            self._window_start[user_id] = now

        if self._counts[user_id] >= self.limit:
            raise RuntimeError("Rate limit exceeded")

        self._counts[user_id] += 1
        return super().handle(request)


def create_security_chain() -> Handler:
    return RateLimitHandler(
        InjectionDetectionHandler(
            InputValidationHandler()
        )
    )
```

---

## 12. Adapter Pattern

The adapter pattern allows incompatible interfaces to work together by wrapping one interface with another.

### 12.1 Model API Adapter

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ModelAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str: ...

    @abstractmethod
    def count_tokens(self, text: str) -> int: ...

    @abstractmethod
    def get_model_info(self) -> Dict: ...


class OpenAIAdapter(ModelAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def generate(self, prompt: str, **kwargs) -> str:
        if not self._client:
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

    def count_tokens(self, text: str) -> int:
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except Exception:
            return len(text) // 4

    def get_model_info(self) -> Dict:
        return {"provider": "openai", "model": self.model}


class AnthropicAdapter(ModelAdapter):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 4096),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def count_tokens(self, text: str) -> int:
        return len(text) // 4

    def get_model_info(self) -> Dict:
        return {"provider": "anthropic", "model": self.model}
```

---

## 13. Facade Pattern

The facade pattern provides a simplified interface to a complex subsystem.

### 13.1 Agent Development Facade

```python
from typing import Any, Dict, Optional


class AgentDevelopmentFacade:
    def __init__(self, container: Container):
        self.container = container

    def build_agent(self, config: Dict) -> Any:
        validator = self._get_validator(config)
        db = self._get_database(config)
        event_bus = self._get_event_bus()
        return self._assemble_agent(validator, db, event_bus, config)

    def _get_validator(self, config: Dict) -> Any:
        return self.container.resolve('validator')

    def _get_database(self, config: Dict) -> Any:
        return self.container.resolve('database')

    def _get_event_bus(self) -> Any:
        return self.container.resolve('event_bus')

    def _assemble_agent(self, validator: Any, db: Any, event_bus: Any, config: Dict) -> Any:
        return {
            'validator': validator,
            'database': db,
            'event_bus': event_bus,
            'config': config,
        }


class AgentBuilderFacade:
    @staticmethod
    def create_from_config(config_path: str) -> Any:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        container = create_container()
        return AgentDevelopmentFacade(container).build_agent(config)
```

---

## 14. Builder Pattern

The builder pattern separates the construction of a complex object from its representation.

### 14.1 Prompt Builder

```python
from typing import List, Optional, Dict


class PromptBuilder:
    def __init__(self):
        self._system_prompt: str = ""
        self._context: List[str] = []
        self._user_prompt: str = ""
        self._temperature: float = 0.7
        self._max_tokens: int = 4096
        self._stop_sequences: List[str] = []

    def set_system_prompt(self, prompt: str) -> 'PromptBuilder':
        self._system_prompt = prompt
        return self

    def add_context(self, context: str) -> 'PromptBuilder':
        self._context.append(context)
        return self

    def set_user_prompt(self, prompt: str) -> 'PromptBuilder':
        self._user_prompt = prompt
        return self

    def set_temperature(self, temp: float) -> 'PromptBuilder':
        self._temperature = max(0, min(2, temp))
        return self

    def set_max_tokens(self, max_tokens: int) -> 'PromptBuilder':
        self._max_tokens = min(max_tokens, 100000)
        return self

    def add_stop_sequence(self, sequence: str) -> 'PromptBuilder':
        self._stop_sequences.append(sequence)
        return self

    def build(self) -> Dict:
        return {
            'messages': [
                {"role": "system", "content": self._system_prompt},
                *[{"role": "user", "content": ctx} for ctx in self._context if ctx],
                {"role": "user", "content": self._user_prompt},
            ],
            'temperature': self._temperature,
            'max_tokens': self._max_tokens,
            'stop': self._stop_sequences,
        }


class SecurePromptBuilder(PromptBuilder):
    def __init__(self):
        super().__init__()
        self._injection_detected = False

    def set_user_prompt(self, prompt: str) -> 'SecurePromptBuilder':
        sanitized = self._sanitize(prompt)
        self._user_prompt = sanitized
        return self

    def _sanitize(self, prompt: str) -> str:
        import re
        dangerous = [
            r"ignore.*instructions",
            r"new.*rules",
            r"system.*prompt",
        ]
        for pattern in dangerous:
            if re.search(pattern, prompt, re.IGNORECASE):
                self._injection_detected = True
                prompt = re.sub(pattern, "[BLOCKED]", prompt, flags=re.IGNORECASE)
        return prompt
```

---

## 15. Template Method Pattern

The template method pattern defines the skeleton of an algorithm in an operation, deferring some steps to subclasses.

### 15.1 Agent Processing Template

```python
from abc import ABC, abstractmethod
from typing import Any, Dict


class AgentProcessor(ABC):
    def process(self, input: str) -> str:
        validated = self.validate(input)
        structured = self.structure(validated)
        result = self.execute(structured)
        return self.format(result)

    def validate(self, input: str) -> str:
        if not input:
            raise ValueError("Input cannot be empty")
        return self._additional_validation(input)

    @abstractmethod
    def _additional_validation(self, input: str) -> str: ...

    @abstractmethod
    def structure(self, input: str) -> Dict: ...

    @abstractmethod
    def execute(self, structured_input: Dict) -> Any: ...

    def format(self, result: Any) -> str:
        return str(result) if result else "No result"


class TextAnalysisAgent(AgentProcessor):
    def _additional_validation(self, input: str) -> str:
        if len(input) > 10000:
            raise ValueError("Input too long")
        return input

    def structure(self, input: str) -> Dict:
        return {"text": input, "analysis_type": "summary"}

    def execute(self, structured_input: Dict) -> Any:
        text = structured_input["text"]
        return {"word_count": len(text.split()), "char_count": len(text)}
```

---

## 16. Abstract Factory Pattern

The abstract factory pattern provides an interface for creating families of related or dependent objects.

### 16.1 Model Provider Abstract Factory

```python
from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def create_adapter(self) -> ModelAdapter: ...

    @abstractmethod
    def create_tokenizer(self) -> TokenizerAdapter: ...

    @abstractmethod
    def get_embedding_model(self) -> str: ...


class OpenAIProvider(ModelProvider):
    def create_adapter(self) -> ModelAdapter:
        return OpenAIAdapter(os.environ.get("OPENAI_API_KEY"))

    def create_tokenizer(self) -> TokenizerAdapter:
        return OpenAITokenizer()

    def get_embedding_model(self) -> str:
        return "text-embedding-3-large"


class AnthropicProvider(ModelProvider):
    def create_adapter(self) -> ModelAdapter:
        return AnthropicAdapter(os.environ.get("ANTHROPIC_API_KEY"))

    def create_tokenizer(self) -> TokenizerAdapter:
        return AnthropicTokenizer()

    def get_embedding_model(self) -> str:
        return "text-embedding-3"


class ProviderFactory:
    def __init__(self):
        self._providers: Dict[str, ModelProvider] = {}

    def register(self, name: str, provider: ModelProvider) -> None:
        self._providers[name] = provider

    def create(self, name: str) -> ModelProvider:
        if name not in self._providers:
            raise KeyError(f"Provider '{name}' not registered")
        return self._providers[name]
```

---

## 17. Flyweight Pattern

The flyweight pattern minimizes memory usage by sharing as much data as possible with similar objects.

### 17.1 Prompt Template Flyweight

```python
from typing import Dict, Any, Optional


class PromptTemplateFlyweight:
    def __init__(self):
        self._templates: Dict[str, Dict] = {}
        self._instances: Dict[str, PromptTemplate] = {}

    def get_template(self, template_name: str) -> PromptTemplate:
        if template_name not in self._instances:
            self._instances[template_name] = PromptTemplate(template_name, shared_data=self._templates.get(template_name, {}))
        return self._instances[template_name]

    def register_template(self, name: str, template: Dict) -> None:
        self._templates[name] = template


class PromptTemplate:
    def __init__(self, name: str, shared_data: Dict):
        self.name = name
        self.shared_data = shared_data

    def render(self, context: Dict) -> str:
        template = self.shared_data.get('template', '')
        return template.format(**context)


flyweight = PromptTemplateFlyweight()
flyweight.register_template("summarize", {"template": "Summarize: {content}"})
template = flyweight.get_template("summarize")
```

---

## 18. Proxy Pattern

The proxy pattern provides a surrogate or placeholder for another object to control access to it.

### 18.1 Rate-Limited Model Proxy

```python
import time
from typing import Any


class ModelProxy:
    def __init__(self, real_model: ModelAdapter, rate_limiter: Any):
        self.real_model = real_model
        self.rate_limiter = rate_limiter

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.rate_limiter.allow_request():
            raise RuntimeError("Rate limit exceeded")
        return self.real_model.generate(prompt, **kwargs)

    def count_tokens(self, text: str) -> int:
        return self.real_model.count_tokens(text)


class CachingModelProxy:
    def __init__(self, real_model: ModelAdapter):
        self.real_model = real_model
        self._cache: Dict[str, str] = {}

    def generate(self, prompt: str, **kwargs) -> str:
        cache_key = f"{prompt}:{kwargs}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        result = self.real_model.generate(prompt, **kwargs)
        self._cache[cache_key] = result
        return result
```

---

## 19. Composite Pattern

The composite pattern composes objects into tree structures to represent part-whole hierarchies.

### 19.1 Tool Composite

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ToolComponent(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> Any: ...


class LeafTool(ToolComponent):
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

    def execute(self, **kwargs) -> Any:
        return self.func(**kwargs)


class CompositeTool(ToolComponent):
    def __init__(self, name: str):
        self.name = name
        self._children: List[ToolComponent] = []

    def add(self, tool: ToolComponent) -> None:
        self._children.append(tool)

    def execute(self, **kwargs) -> Any:
        results = []
        for child in self._children:
            results.append(child.execute(**kwargs))
        return results
```

---

## 20. Bridge Pattern

The bridge pattern decouples an abstraction from its implementation so the two can vary independently.

### 20.1 Agent Bridge

```python
from abc import ABC, abstractmethod


class AgentImplementation(ABC):
    @abstractmethod
    def process_request(self, request: str) -> str: ...


class LLMAgent(AgentImplementation):
    def __init__(self, model_adapter: ModelAdapter):
        self.model = model_adapter

    def process_request(self, request: str) -> str:
        return self.model.generate(request)


class RuleBasedAgent(AgentImplementation):
    def process_request(self, request: str) -> str:
        return "Rule-based response"


class AgentAbstraction:
    def __init__(self, implementation: AgentImplementation):
        self.impl = implementation

    def handle(self, request: str) -> str:
        return self.impl.process_request(request)
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)