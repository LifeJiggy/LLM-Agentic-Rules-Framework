# Security Domain - Best Practices

## Overview

This document outlines recommended security practices for LLM/agentic systems.

## Input Validation Best Practices

### 1. Validate All Inputs

```python
from pydantic import BaseModel, validator

class UserQuery(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Query cannot be empty")
        if len(v) > 1000:
            raise ValueError("Query too long")
        return v.strip()
```

### 2. Use Allowlists Over Blocklists

```python
# Bad - Blocklist approach
BLOCKED_PATTERNS = ["DROP TABLE", "rm -rf"]

def is_safe(command):
    for pattern in BLOCKED_PATTERNS:
        if pattern in command:
            return False
    return True

# Good - Allowlist approach
ALLOWED_COMMANDS = {"read", "list", "search"}

def is_safe(command):
    return command.split()[0] in ALLOWED_COMMANDS
```

### 3. Parameterized Queries

```python
# Bad - SQL injection vulnerable
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# Good - Parameterized
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

## Secret Management

### Environment Variables

```python
import os
from typing import Optional

class SecretManager:
    """Manage secrets securely."""
    
    @staticmethod
    def get_api_key() -> str:
        key = os.environ.get("API_KEY")
        if not key:
            raise ValueError("API_KEY not configured")
        return key
    
    @staticmethod
    def get_database_url() -> Optional[str]:
        return os.environ.get("DATABASE_URL")
```

### Secrets Rotation

```python
class SecretRotator:
    """Rotate secrets periodically."""
    
    def __init__(self, vault_client):
        self.vault = vault_client
    
    async def rotate_if_needed(self, secret_name: str):
        """Rotate secret if past rotation period."""
        metadata = await self.vault.get_metadata(secret_name)
        
        if self._should_rotate(metadata):
            await self.vault.rotate(secret_name)
    
    def _should_rotate(self, metadata) -> bool:
        """Check if rotation is needed."""
        last_rotated = metadata.get("last_rotated")
        if not last_rotated:
            return True
        
        days_since = (datetime.now() - last_rotated).days
        return days_since >= 90
```

## Output Filtering

### Sensitive Data Detection

```python
import re

SENSITIVE_PATTERNS = {
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    "api_key": r'(?i)(api[_-]?key|secret)[=:]\s*[\w-]{20,}',
    "password": r'(?i)password[=:]\s*\S+',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
}

class OutputFilter:
    """Filter sensitive data from outputs."""
    
    def __init__(self):
        self.patterns = SENSITIVE_PATTERNS
    
    def filter(self, text: str) -> str:
        """Redact sensitive information."""
        for label, pattern in self.patterns.items():
            text = re.sub(pattern, f"[{label.upper()}_REDACTED]", text)
        return text
```

## Rate Limiting Best Practices

### Token Bucket Algorithm

```python
import time

class TokenBucket:
    """Token bucket rate limiter."""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def allow_request(self) -> bool:
        """Check if request is allowed."""
        self._refill()
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
    
    def _refill(self):
        """Refill tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
```

## Audit Logging

### Security Event Logging

```python
import logging
from datetime import datetime
from typing import Dict, Any

class SecurityLogger:
    """Log security-relevant events."""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def log_authentication(self, user_id: str, success: bool, ip: str):
        """Log authentication attempt."""
        self.logger.info({
            "event": "authentication",
            "user_id": user_id,
            "success": success,
            "ip": ip,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_permission_denied(self, user_id: str, resource: str):
        """Log permission denial."""
        self.logger.warning({
            "event": "permission_denied",
            "user_id": user_id,
            "resource": resource,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_sensitive_operation(self, user_id: str, operation: str):
        """Log sensitive operations."""
        self.logger.info({
            "event": "sensitive_operation",
            "user_id": user_id,
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat()
        })
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
