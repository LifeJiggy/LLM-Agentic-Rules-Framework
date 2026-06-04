# Data Domain - Anti-Patterns

## Overview

This document outlines data anti-patterns to avoid in LLM/agentic systems. Anti-patterns are proven-bad approaches that introduce security vulnerabilities, performance issues, and maintenance challenges. Identifying and actively avoiding these patterns is essential for production-quality data handling.

---

## Table of Contents

1. [Unencrypted Sensitive Data](#1-unencrypted-sensitive-data)
2. [SQL Injection Vulnerabilities](#2-sql-injection-vulnerabilities)
3. [No Connection Pooling](#3-no-connection-pooling)
4. [Missing Data Validation](#4-missing-data-validation)
5. [Unbounded Context Growth](#5-unbounded-context-growth)
6. [No Caching Strategy](#6-no-caching-strategy)
7. [Missing Rate Limiting](#7-missing-rate-limiting)
8. [No Backup Strategy](#8-no-backup-strategy)
9. [Insecure Default Permissions](#9-insecure-default-permissions)
10. [No PII Handling](#10-no-pii-handling)

---

## 1. Unencrypted Sensitive Data

### Problem
Storing sensitive data without encryption exposes it to breaches and compliance violations.

### Anti-Pattern
```python
# Bad - Plain text storage
class UserData:
    def save(self, user_id, email, phone):
        query = f"""
        INSERT INTO users (user_id, email, phone)
        VALUES ('{user_id}', '{email}', '{phone}')
        """
        db.execute(query)
```

### Solution
```python
# Good - Encrypted storage
class SecureUserData:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
    
    def save(self, user_id, email, phone):
        encrypted_email = self.cipher.encrypt(email.encode())
        encrypted_phone = self.cipher.encrypt(phone.encode())
        
        query = "INSERT INTO users (user_id, email, phone) VALUES (?, ?, ?)"
        db.execute(query, (user_id, encrypted_email, encrypted_phone))
```

---

## 2. SQL Injection Vulnerabilities

### Problem
Direct string interpolation in SQL queries allows attackers to execute arbitrary commands.

### Anti-Pattern
```python
# Bad - Vulnerable to injection
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    return db.execute(query)
```

### Solution
```python
# Good - Parameterized queries
def get_user_data(user_id):
    if not isinstance(user_id, str) or len(user_id) > 64:
        raise ValidationError("Invalid user_id")
    
    query = "SELECT * FROM users WHERE user_id = ?"
    return db.execute(query, (user_id,))
```

---

## 3. No Connection Pooling

### Problem
Creating connections per request exhausts database resources and creates latency.

### Anti-Pattern
```python
# Bad - New connection every time
def get_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
```

### Solution
```python
# Good - Connection pooling
class UserRepository:
    def __init__(self, pool):
        self.pool = pool
    
    def get_user(self, user_id):
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone()
```

---

## 4. Missing Data Validation

### Problem
Accepting untrusted data leads to downstream errors and security issues.

### Anti-Pattern
```python
# Bad - No validation
def process_conversation(data):
    return {
        "user_id": data["user_id"],
        "messages": data["messages"],
        "timestamp": data["timestamp"]
    }
```

### Solution
```python
# Good - Full validation
from pydantic import BaseModel, validator

class ConversationInput(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    messages: List[Dict] = Field(..., max_items=1000)
    timestamp: float = Field(..., gt=0)
    
    @validator("user_id")
    def sanitize_user_id(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Invalid user ID format")
        return v

def process_conversation(data: ConversationInput):
    return data.dict()
```

---

## 5. Unbounded Context Growth

### Problem
Unlimited conversation history exhausts memory and LLM context windows.

### Anti-Pattern
```python
# Bad - Unlimited growth
class ConversationHistory:
    def __init__(self):
        self.messages = []
    
    def add_message(self, msg):
        self.messages.append(msg)  # Grows unbounded
```

### Solution
```python
# Good - Bounded with summarization
class BoundedHistory:
    def __init__(self, max_messages: int = 100, max_tokens: int = 4000):
        self.messages = deque(max_messages=max_messages)
        self.max_tokens = max_tokens
    
    def add_message(self, msg):
        self.messages.append(msg)
        if self._token_count() > self.max_tokens:
            self._summarize_oldest()
    
    def _token_count(self) -> int:
        return sum(len(m.get("content", "").split()) for m in self.messages)
```

---

## 6. No Caching Strategy

### Problem
Repeated identical queries waste time and resources.

### Anti-Pattern
```python
# Bad - Always hits database
def get_user_preferences(user_id):
    return db.query("SELECT * FROM preferences WHERE user_id = ?", (user_id,))
```

### Solution
```python
# Good - Caching with TTL
class PreferencesCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = TTLCache(maxsize=10000, ttl=ttl_seconds)
    
    def get(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        
        prefs = db.query("SELECT * FROM preferences WHERE user_id = ?", (user_id,))
        self.cache[user_id] = prefs
        return prefs
```

---

## 7. Missing Rate Limiting

### Problem
Unbounded data access creates DoS vulnerabilities and cost explosions.

### Anti-Pattern
```python
# Bad - No limits
def fetch_usage_data(user_id):
    return db.query("SELECT * FROM usage WHERE user_id = ?", (user_id,))
```

### Solution
```python
# Good - Rate limited
class RateLimitedDataFetcher:
    def __init__(self, limiter):
        self.limiter = limiter
    
    async def fetch_usage_data(self, user_id):
        if not self.limiter.allow(f"data:{user_id}"):
            raise RateLimitError("Too many requests")
        return db.query("SELECT * FROM usage WHERE user_id = ?", (user_id,))
```

---

## 8. No Backup Strategy

### Problem
No backups mean permanent data loss on system failure.

### Anti-Pattern
```python
# Bad - No backup
def save_critical_data(data):
    db.execute("INSERT INTO critical VALUES (?)", (data,))
```

### Solution
```python
# Good - Backup before save
class BackupedDataStore:
    async def save_critical_data(self, data):
        await self.backup_manager.create_snapshot("critical_table")
        await db.execute("INSERT INTO critical VALUES (?)", (data,))
```

---

## 9. Insecure Default Permissions

### Problem
Default-permissive settings allow unauthorized data access.

### Anti-Pattern
```python
# Bad - Open by default
class DataService:
    def __init__(self):
        self.permitted_users = ["*"]  # Anyone can access
```

### Solution
```python
# Good - Explicit deny
class SecureDataService:
    def __init__(self):
        self.permitted_users: Set[str] = set()
    
    def allow_access(self, user_id):
        self.permitted_users.add(user_id)
    
    def can_access(self, user_id) -> bool:
        return user_id in self.permitted_users
```

---

## 10. No PII Handling

### Problem
Processing PII without safeguards violates privacy regulations.

### Anti-Pattern
```python
# Bad - Raw PII in logs
def log_user_interaction(user_data):
    logger.info(f"User {user_data['email']} did something")  # PII leak
```

### Solution
```python
# Good - Sanitized logging
def log_user_interaction(user_data, pii_detector):
    safe_email = pii_detector.redact(user_data["email"])
    logger.info(f"User {safe_email} did something")
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Checklist](./checklist.md)