# Security Domain - Advanced Concepts

## Overview

This document covers advanced security concepts for LLM/agentic systems.

## Advanced Security Patterns

### 1. Circuit Breaker for External APIs

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker pattern for external API calls."""
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker."""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        """Check if should attempt to reset circuit."""
        return (time.time() - self.last_failure_time) > self.recovery_timeout
```

### 2. End-to-End Encryption

```python
from cryptography.fernet import Fernet
from typing import Any
import base64

class SecureMessenger:
    """End-to-end encrypted messaging."""
    
    def __init__(self, master_key: str):
        self.key = base64.urlsafe_b64encode(
            master_key.encode()[:32].ljust(32, b'0')
        )
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: Any) -> str:
        """Encrypt data before sending."""
        import json
        json_data = json.dumps(data)
        encrypted = self.cipher.encrypt(json_data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> Any:
        """Decrypt received data."""
        import json
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return json.loads(decrypted.decode())
```

### 3. Zero Trust Architecture

```python
from typing import Optional
import hashlib
import time

class ZeroTrustValidator:
    """Zero trust validation for requests."""
    
    def __init__(self):
        self.trust_scores = {}
    
    def validate_request(self, request: dict) -> tuple[bool, float]:
        """Validate request and return (is_allowed, trust_score)."""
        
        user_id = request.get("user_id")
        if not user_id:
            return False, 0.0
        
        # Calculate trust score
        trust_score = self._calculate_trust_score(request)
        
        # Check if score meets threshold
        if trust_score >= 0.7:
            return True, trust_score
        
        return False, trust_score
    
    def _calculate_trust_score(self, request: dict) -> float:
        """Calculate trust score based on multiple factors."""
        score = 0.0
        
        # Factor 1: Device fingerprint
        if self._verify_device(request):
            score += 0.3
        
        # Factor 2: Location
        if self._verify_location(request):
            score += 0.2
        
        # Factor 3: Time patterns
        if self._verify_time(request):
            score += 0.2
        
        # Factor 4: Historical behavior
        if self._verify_history(request):
            score += 0.3
        
        return score
    
    def _verify_device(self, request: dict) -> bool:
        """Verify device fingerprint."""
        # Implementation
        return True
    
    def _verify_location(self, request: dict) -> bool:
        """Verify location."""
        # Implementation
        return True
    
    def _verify_time(self, request: dict) -> bool:
        """Verify time patterns."""
        # Implementation
        return True
    
    def _verify_history(self, request: dict) -> bool:
        """Verify historical behavior."""
        # Implementation
        return True
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
