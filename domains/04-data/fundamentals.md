# Data Domain - Fundamentals

## Overview

This document covers fundamental data handling principles for LLM/agentic systems, including data lifecycle, validation, serialization, caching, privacy, and retrieval patterns that every developer should understand and apply.

---

## Core Data Principles for LLM Systems

### 1. Data Validation

All input data must be validated before processing to prevent injection attacks, ensure quality, and maintain system integrity.

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, validator
import re

class AgentDataContext(BaseModel):
    """Validated context for agent operations."""
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, str]] = []
    metadata: Dict[str, Any] = {}
    
    @validator("user_id")
    def validate_user_id(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]{1,64}$", v):
            raise ValueError("Invalid user ID format")
        return v
    
    @validator("session_id")
    def validate_session_id(cls, v):
        if not re.match(r"^[a-f0-9]{32}$", v):
            raise ValueError("Invalid session ID format")
        return v

def validate_user_data(data: Dict[str, Any], max_length: int = 10000) -> List[str]:
    """Validate incoming user data with detailed error reporting."""
    errors = []
    
    if not isinstance(data, dict):
        errors.append("Data must be a dictionary")
        return errors
    
    for key, value in data.items():
        if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
            errors.append(f"Invalid type for key '{key}': {type(value).__name__}")
        
        if isinstance(value, str) and len(value) > max_length:
            errors.append(f"Value for '{key}' exceeds {max_length} characters")
    
    return errors
```

### 2. Data Serialization

```python
import json
from typing import Any, Union
from datetime import datetime

class AgentDataSerializer:
    """Safe serialization for agent data structures."""
    
    @staticmethod
    def serialize(data: Any) -> str:
        """Serialize data to JSON with error handling."""
        try:
            return json.dumps(data, default=str, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise SerializationError(f"Failed to serialize: {e}")
    
    @staticmethod
    def deserialize(data: str, expected_type: type = None) -> Any:
        """Deserialize data with validation."""
        try:
            result = json.loads(data)
            if expected_type and not isinstance(result, expected_type):
                raise TypeError(f"Expected {expected_type}, got {type(result)}")
            return result
        except (json.JSONDecodeError, TypeError) as e:
            raise DeserializationError(f"Failed to deserialize: {e}")

class SerializationError(Exception):
    """Raised when serialization fails."""
    pass

class DeserializationError(Exception):
    """Raised when deserialization fails."""
    pass
```

### 3. Data Caching

```python
from functools import lru_cache
import time
import threading
from typing import Dict, Any, Optional, Callable

class AgentDataCache:
    """Production-ready cache for agent data."""
    
    def __init__(self, default_ttl: int = 300, max_size: int = 1000):
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: Dict[str, tuple] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        with self._lock:
            if key not in self._cache:
                return None
            
            value, expiry = self._cache[key]
            if time.time() > expiry:
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Cache value with TTL."""
        expiry = time.time() + (ttl or self.default_ttl)
        
        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_oldest()
            self._cache[key] = (value, expiry)
    
    def _evict_oldest(self):
        """Evict oldest entries."""
        oldest = min(self._cache.items(), key=lambda x: x[1][1])
        del self._cache[oldest[0]]

class CachedDataLoader:
    """Data loader with automatic caching."""
    
    def __init__(self, loader_fn: Callable, cache: AgentDataCache):
        self.loader = loader_fn
        self.cache = cache
    
    async def load(self, key: str) -> Any:
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        
        data = await self.loader(key)
        self.cache.set(key, data)
        return data
```

---

## Data Types for LLM Systems

### 1. Vector Embeddings

```python
import numpy as np
from typing import List, Optional

class EmbeddingStore:
    """Storage and retrieval for vector embeddings."""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self._embeddings: Dict[str, np.ndarray] = {}
    
    def store(self, key: str, embedding: np.ndarray) -> None:
        if embedding.shape != (self.dimension,):
            raise ValueError(f"Expected dimension {self.dimension}")
        self._embeddings[key] = embedding
    
    def get(self, key: str) -> Optional[np.ndarray]:
        return self._embeddings.get(key)
    
    def similarity(self, key1: str, key2: str) -> float:
        """Compute cosine similarity between embeddings."""
        emb1 = self._embeddings.get(key1)
        emb2 = self._embeddings.get(key2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))

class EmbeddingGenerator:
    """Generate embeddings from text."""
    
    def __init__(self, model_client, batch_size: int = 100):
        self.model = model_client
        self.batch_size = batch_size
    
    async def embed(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for text batch."""
        if len(texts) <= self.batch_size:
            return await self._batch_embed(texts)
        
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            results.extend(await self._batch_embed(batch))
        
        return results
    
    async def _batch_embed(self, texts: List[str]) -> List[np.ndarray]:
        # Implementation depends on chosen embedding model
        pass
```

### 2. Conversation Data

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Conversation:
    session_id: str
    user_id: str
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_message(self, role: str, content: str, **metadata) -> Message:
        msg = Message(role=role, content=content, metadata=metadata)
        self.messages.append(msg)
        self.updated_at = datetime.utcnow()
        return msg
    
    def get_context(self, max_tokens: int = 4000) -> List[Dict[str, str]]:
        """Get context within token limit."""
        context = []
        total_tokens = 0
        
        for msg in reversed(self.messages):
            msg_tokens = self._estimate_tokens(msg.content)
            if total_tokens + msg_tokens > max_tokens:
                break
            context.insert(0, {"role": msg.role, "content": msg.content})
            total_tokens += msg_tokens
        
        return context
    
    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return len(text) // 4
```

---

## Data Retrieval Patterns

### 1. Basic Retrieval

```python
class DataRetriever:
    """Retrieve data for agent context."""
    
    def __init__(self, data_sources: Dict[str, Any]):
        self.sources = data_sources
    
    async def retrieve(self, query: str, source: str = None, 
                      limit: int = 10) -> List[Any]:
        """Retrieve relevant data."""
        if source:
            return await self._retrieve_from_source(source, query, limit)
        
        all_results = []
        for src_name, src_client in self.sources.items():
            results = await self._retrieve_from_source(src_name, query, limit)
            all_results.extend(results)
        
        return all_results[:limit]
    
    async def _retrieve_from_source(self, source: str, query: str, 
                                   limit: int) -> List[Any]:
        if source == "memory":
            return await self._retrieve_from_memory(query, limit)
        elif source == "database":
            return await self._retrieve_from_database(query, limit)
        elif source == "api":
            return await self._retrieve_from_api(query, limit)
        return []
    
    async def _retrieve_from_memory(self, query: str, limit: int) -> List[Any]:
        # Retrieve from in-memory store
        pass
    
    async def _retrieve_from_database(self, query: str, limit: int) -> List[Any]:
        # Retrieve from database with query sanitization
        pass
    
    async def _retrieve_from_api(self, query: str, limit: int) -> List[Any]:
        # Retrieve from external API
        pass
```

---

## Data Lifecycle Management

### 1. Retention Policies

```python
from enum import Enum

class RetentionPolicy(Enum):
    SHORT_TERM = 3600  # 1 hour
    MEDIUM_TERM = 86400  # 1 day
    LONG_TERM = 2592000  # 30 days
    PERMANENT = -1  # Never expire

class DataLifecycleManager:
    """Manage data retention and cleanup."""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.retention_policies: Dict[str, RetentionPolicy] = {}
    
    def set_retention(self, data_type: str, policy: RetentionPolicy) -> None:
        self.retention_policies[data_type] = policy
    
    def should_retain(self, data_type: str, age_seconds: float) -> bool:
        policy = self.retention_policies.get(data_type, RetentionPolicy.MEDIUM_TERM)
        if policy == RetentionPolicy.PERMANENT:
            return True
        return age_seconds < policy.value
    
    async def cleanup_expired(self) -> int:
        """Remove expired data."""
        expired = await self.storage.find_expired()
        removed = 0
        
        for data in expired:
            if not self.should_retain(data.type, data.age_seconds):
                await self.storage.delete(data.id)
                removed += 1
        
        return removed
```

---

## Data Privacy Fundamentals

### 1. PII Detection and Redaction

```python
import re
from typing import List, Tuple

class PIIDetector:
    """Detect personally identifiable information."""
    
    PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?[1-9]\d{1,14}",
        "ssn": r"\d{3}-\d{2}-\d{4}",
        "credit_card": r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}",
    }
    
    def detect(self, text: str) -> List[Tuple[str, str, Tuple[int, int]]]:
        findings = []
        for pii_type, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                findings.append((pii_type, match.group(), match.span()))
        return findings

class DataSanitizer:
    """Sanitize data for safe processing."""
    
    def __init__(self, detector: PIIDetector):
        self.detector = detector
    
    def sanitize(self, text: str) -> str:
        findings = self.detector.detect(text)
        sanitized = text
        
        offsets = 0
        for pii_type, value, (start, end) in findings:
            sanitized = sanitized[:start + offsets] + "[REDACTED]" + sanitized[end + offsets:]
            offsets += len("[REDACTED]") - (end - start)
        
        return sanitized
```

---

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)