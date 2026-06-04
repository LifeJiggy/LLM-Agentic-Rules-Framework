# Data Domain - Examples

## Overview

This document provides concrete code examples for implementing data handling best practices in LLM/agentic systems, including vector databases, conversation storage, caching, privacy, and pipeline patterns.

---

## Example 1: Conversation History Manager

```python
from collections import deque
from typing import Dict, Any, List, Optional
import json
import time

class ConversationHistoryManager:
    """Production-ready conversation history with token management."""
    
    def __init__(self, max_messages: int = 100, max_tokens: int = 4000):
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.histories: Dict[str, deque] = {}
        self._lock = threading.Lock()
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add message to conversation history."""
        with self._lock:
            if session_id not in self.histories:
                self.histories[session_id] = deque(maxlen=self.max_messages)
            self.histories[session_id].append({
                "role": role,
                "content": content,
                "timestamp": time.time()
            })
    
    def get_context(self, session_id: str, token_limit: int = None) -> List[Dict]:
        """Get conversation context within token limit."""
        history = self.histories.get(session_id, deque())
        limit = token_limit or self.max_tokens
        
        context = []
        total_tokens = 0
        
        for msg in reversed(history):
            msg_tokens = self._estimate_tokens(msg["content"])
            if total_tokens + msg_tokens > limit:
                break
            context.insert(0, {
                "role": msg["role"],
                "content": msg["content"]
            })
            total_tokens += msg_tokens
        
        return context
    
    def clear_session(self, session_id: str) -> None:
        with self._lock:
            self.histories.pop(session_id, None)
    
    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

# Usage
history = ConversationHistoryManager()
history.add_message("session_123", "user", "What is the weather?")
context = history.get_context("session_123")
```

---

## Example 2: Vector Database Integration

```python
import numpy as np
from typing import List, Optional, Dict
import asyncio

class VectorDatabaseAdapter:
    """Abstract vector database operations."""
    
    def __init__(self, client, dimension: int = 1536, metric: str = "cosine"):
        self.client = client
        self.dimension = dimension
        self.metric = metric
        self.collection = None
    
    async def initialize(self, collection_name: str) -> None:
        """Initialize collection with schema."""
        self.collection = await self.client.create_collection(
            name=collection_name,
            dimension=self.dimension,
            metric=self.metric,
            if_exists="reuse"
        )
    
    async def upsert(self, doc_id: str, embedding: np.ndarray, 
                     metadata: Dict = None) -> None:
        """Store or update embedding."""
        if embedding.shape[0] != self.dimension:
            raise ValueError(f"Expected {self.dimension} dimensions")
        
        await self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding.tolist()],
            metadatas=[metadata] if metadata else None
        )
    
    async def search(self, query_embedding: np.ndarray, 
                     top_k: int = 10, 
                     filters: Dict = None) -> List[Dict]:
        """Search for similar vectors."""
        results = await self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=filters
        )
        
        return self._format_results(results)
    
    def _format_results(self, raw_results) -> List[Dict]:
        formatted = []
        for i, (ids, distances, metadatas) in enumerate(zip(
            raw_results["ids"], raw_results["distances"], raw_results["metadatas"]
        )):
            for doc_id, distance, metadata in zip(ids, distances, metadatas):
                formatted.append({
                    "id": doc_id,
                    "score": 1 - distance,  # Convert distance to similarity
                    "metadata": metadata or {}
                })
        return formatted

# Usage
db = VectorDatabaseAdapter(chroma_client, dimension=1536)
await db.initialize("conversations")
```

---

## Example 3: Secure Data Caching

```python
import redis.asyncio as redis
from typing import Optional, Any, Dict
import json
import time

class SecureCacheManager:
    """Encrypted, time-limited cache for sensitive data."""
    
    def __init__(self, redis_client, encryption_key: bytes, default_ttl: int = 300):
        self.redis = redis_client
        self.cipher = Fernet(encryption_key)
        self.default_ttl = default_ttl
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        encrypted = await self.redis.get(key)
        if not encrypted:
            return None
        
        try:
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted)
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Cache value with encryption."""
        serialized = json.dumps(value)
        encrypted = self.cipher.encrypt(serialized.encode())
        await self.redis.setex(key, ttl or self.default_ttl, encrypted)
    
    async def invalidate(self, key: str) -> None:
        """Remove cached value."""
        await self.redis.delete(key)

class CacheWithCircuitBreaker:
    """Cache that fails gracefully."""
    
    def __init__(self, cache: SecureCacheManager, fallback_ttl: int = 60):
        self.cache = cache
        self.fallback_ttl = fallback_ttl
        self.fallback_data: Dict[str, Any] = {}
    
    async def get(self, key: str, loader_fn) -> Any:
        try:
            value = await self.cache.get(key)
            if value is not None:
                return value
        except Exception:
            # Cache error, use fallback
            pass
        
        value = await loader_fn()
        self.fallback_data[key] = {
            "value": value,
            "expires": time.time() + self.fallback_ttl
        }
        
        try:
            await self.cache.set(key, value)
        except Exception:
            pass  # Log but don't fail
        
        return value
```

---

## Example 4: Data Pipeline for Agents

```python
import asyncio
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PipelineResult:
    data: Any
    source: str
    confidence: float
    metadata: Dict[str, Any]

class DataPipeline:
    """Pipeline for fetching and processing agent data."""
    
    def __init__(self, sources: Dict[str, Any]):
        self.sources = sources
        self._metrics = {}
    
    async def fetch(self, query: str, context: Dict = None) -> List[PipelineResult]:
        """Fetch data from multiple sources in parallel."""
        tasks = [
            self._fetch_from_source(source_name, source, query, context)
            for source_name, source in self.sources.items()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten and filter errors
        all_results = []
        for result in results:
            if isinstance(result, Exception):
                continue
            all_results.extend(result)
        
        return self._rank_and_filter(all_results)
    
    async def _fetch_from_source(self, name: str, source: Any, 
                                  query: str, context: Dict) -> List[PipelineResult]:
        try:
            raw_data = await source.query(query, context)
            
            processed = []
            for item in raw_data:
                processed.append(PipelineResult(
                    data=item.get("content"),
                    source=name,
                    confidence=item.get("score", 0.5),
                    metadata=item.get("metadata", {})
                ))
            
            return processed
        except Exception as e:
            logger.warning(f"Source {name} error: {e}")
            return []
    
    def _rank_and_filter(self, results: List[PipelineResult]) -> List[PipelineResult]:
        results.sort(key=lambda x: x.confidence, reverse=True)
        return [r for r in results if r.confidence > 0.3][:20]

# Usage
pipeline = DataPipeline({
    "vector_store": VectorDB(),
    "knowledge_base": KnowledgeBase(),
    "api": ExternalAPI()
})

results = await pipeline.fetch("What is our return policy?", context={"user_id": "123"})
```

---

## Example 5: Data Sanitization for Safety

```python
import re
from typing import List, Tuple

class DataSanitizer:
    """Sanitize data for safe agent processing."""
    
    PATTERNS_TO_REDACT = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),
    ]
    
    def sanitize_for_context(self, text: str) -> str:
        """Sanitize text before adding to context."""
        sanitized = text
        for pattern, replacement in self.PATTERNS_TO_REDACT:
            sanitized = re.sub(pattern, replacement, sanitized)
        return sanitized
    
    def sanitize_for_storage(self, data: Dict) -> Dict:
        """Sanitize data before storage."""
        sanitized = {}
        pii_fields = {"ssn", "credit_card", "email", "phone"}
        
        for key, value in data.items():
            if key in pii_fields:
                sanitized[key] = self._hash_pii(str(value))
            elif isinstance(value, str):
                sanitized[key] = self.sanitize_for_context(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _hash_pii(self, value: str) -> str:
        import hashlib
        return f"hashed_{hashlib.sha256(value.encode()).hexdigest()[:16]}"

# Usage
sanitizer = DataSanitizer()
safe_context = sanitizer.sanitize_for_context(user_input)
safe_storage = sanitizer.sanitize_for_storage(user_data)
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)