# Integration Domain - Examples

## Overview

This document provides integration examples for LLM/agentic systems.

## Example: REST Client

```python
import requests
from typing import Optional

class APIClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
```

## Example: Webhook Handler

```python
import hmac
import hashlib

class WebhookHandler:
    def __init__(self, secret: str):
        self.secret = secret
    
    def verify(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(
            self.secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
