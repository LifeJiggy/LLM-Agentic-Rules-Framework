# Development Domain - Advanced Concepts

## Overview

This document covers advanced development concepts for LLM/agentic systems.

## Advanced Patterns

### 1. Dependency Injection

```python
from typing import Protocol

class Database(Protocol):
    def query(self, sql: str): ...

class UserService:
    def __init__(self, db: Database):
        self.db = db
    
    def get_user(self, user_id: int):
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

### 2. Event-Driven Architecture

```python
from typing import Callable, List

class EventBus:
    def __init__(self):
        self._subscribers: dict = {}
    
    def subscribe(self, event: str, handler: Callable):
        self._subscribers.setdefault(event, []).append(handler)
    
    def publish(self, event: str, data: any):
        for handler in self._subscribers.get(event, []):
            handler(data)
```

### 3. Repository Pattern

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, id): pass
    
    @abstractmethod
    def save(self, entity): pass
    
    @abstractmethod
    def delete(self, id): pass

class UserRepository(Repository):
    def __init__(self, db):
        self.db = db
    
    def get(self, id):
        return self.db.query("SELECT * FROM users WHERE id = ?", (id,))
    
    def save(self, user):
        self.db.execute("INSERT INTO users VALUES (?, ?)", (user.id, user.name))
    
    def delete(self, id):
        self.db.execute("DELETE FROM users WHERE id = ?", (id,))
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
