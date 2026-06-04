# Data Domain - Best Practices

## Overview

This document outlines data best practices for LLM/agentic systems, covering data management, privacy, retrieval, and operational excellence. All practices are production-oriented with specific guidance for AI system contexts.

---

## Table of Contents

1. [Data Storage Best Practices](#1-data-storage-best-practices)
2. [Data Retrieval Best Practices](#2-data-retrieval-best-practices)
3. [Privacy and Security Best Practices](#3-privacy-and-security-best-practices)
4. [Caching Best Practices](#4-caching-best-practices)
5. [Data Quality Best Practices](#5-data-quality-best-practices)
6. [Backup and Recovery Best Practices](#6-backup-and-recovery-best-practices)
7. [Monitoring and Observability](#7-monitoring-and-observability)
8. [Performance Optimization](#8-performance-optimization)

---

## 1. Data Storage Best Practices

### 1.1 Schema Design

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class AgentDataContext(BaseModel):
    """Well-structured context for agent operations."""
    user_id: str = Field(..., min_length=1, max_length=64)
    session_id: str = Field(..., min_length=32, max_length=64)
    conversation_round: int = Field(default=0, ge=0)
    created_at: float = Field(default_factory=time.time)
    data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = True
        extra = "forbid"

class ConversationSchema(BaseModel):
    """Optimized schema for conversation storage."""
    session_id: str
    user_id: str
    messages: List[Dict[str, str]]
    token_count: int
    expires_at: Optional[float]
    
    @validator("token_count")
    def validate_token_budget(cls, v):
        if v > 32000:
            raise ValueError("Token count exceeds maximum context window")
        return v
```

### 1.2 Connection Management

```python
import asyncio
from contextlib import asynccontextmanager

class ConnectionPool:
    """Managed connection pool for data stores."""
    
    def __init__(self, min_connections: int = 5, max_connections: int = 20):
        self.min_connections = min_connections
        self.max_connections = max_connections
        self._pool = asyncio.Queue()
        self._in_use = set()
    
    async def initialize(self):
        for _ in range(self.min_connections):
            conn = await self._create_connection()
            await self._pool.put(conn)
    
    @asynccontextmanager
    async def get_connection(self):
        if not self._pool.empty():
            conn = await self._pool.get()
        else:
            if len(self._in_use) >= self.max_connections:
                raise RuntimeError("Connection pool exhausted")
            conn = await self._create_connection()
        
        self._in_use.add(conn)
        try:
            yield conn
        finally:
            self._in_use.discard(conn)
            if not self._pool.full():
                await self._pool.put(conn)
    
    async def _create_connection(self):
        # Implementation depends on data store
        pass
```

---

## 2. Data Retrieval Best Practices

### 2.1 Query Optimization

```python
class OptimizedRetriever:
    """Retrieval with automatic optimization."""
    
    def __init__(self, vector_db, keyword_db):
        self.vector_db = vector_db
        self.keyword_db = keyword_db
        self.query_cache = AgentDataCache(ttl=60)
    
    async def retrieve(self, query: str, filters: Dict = None) -> List[SearchResult]:
        cache_key = f"{query}:{json.dumps(filters)}"
        cached = self.query_cache.get(cache_key)
        if cached:
            return cached
        
        results = await self._hybrid_search(query, filters)
        self.query_cache.set(cache_key, results)
        return results
    
    async def _hybrid_search(self, query: str, filters: Dict) -> List[SearchResult]:
        # Optimize based on query characteristics
        if len(query) < 50:
            return await self._keyword_priority_search(query, filters)
        else:
            return await self._semantic_priority_search(query, filters)
```

### 2.2 Pagination and Batching

```python
class PaginatedRetriever:
    """Handle large result sets efficiently."""
    
    async def retrieve_paginated(self, query: str, 
                                 page_size: int = 100,
                                 page_token: str = None) -> Dict:
        """Retrieve results with pagination."""
        results, total_count, next_token = await self._retrieve_page(
            query, page_size, page_token
        )
        
        return {
            "results": results,
            "total_count": total_count,
            "page_size": page_size,
            "page_token": next_token,
            "has_more": next_token is not None
        }
    
    async def _retrieve_page(self, query: str, page_size: int, 
                             page_token: str) -> tuple:
        # Implementation with cursor-based pagination
        pass
```

---

## 3. Privacy and Security Best Practices

### 3.1 Data Encryption

```python
from cryptography.fernet import Fernet
import os

class SecureDataStorage:
    """Encrypt data at rest."""
    
    def __init__(self):
        self.key = os.environ.get("DATA_ENCRYPTION_KEY")
        if not self.key:
            raise ConfigurationError("DATA_ENCRYPTION_KEY not set")
        self.cipher = Fernet(self.key.encode())
    
    def encrypt(self, data: Any) -> bytes:
        serialized = json.dumps(data).encode()
        return self.cipher.encrypt(serialized)
    
    def decrypt(self, encrypted_data: bytes) -> Any:
        decrypted = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
```

### 3.2 Access Control

```python
class DataAccessControl:
    """Enforce data access permissions."""
    
    def __init__(self, permission_store):
        self.permissions = permission_store
    
    def can_access(self, user_id: str, data_id: str, action: str) -> bool:
        required_permission = f"{data_id}:{action}"
        user_permissions = self.permissions.get(user_id, [])
        return required_permission in user_permissions or "admin" in user_permissions
```

---

## 4. Caching Best Practices

### 4.1 Multi-Level Cache

```python
class MultiLevelCache:
    """L1 (memory) + L2 (Redis) cache strategy."""
    
    def __init__(self, l1_cache, l2_cache):
        self.l1 = l1_cache
        self.l2 = l2_cache
    
    async def get(self, key: str) -> Optional[Any]:
        value = self.l1.get(key)
        if value is not None:
            return value
        
        value = await self.l2.get(key)
        if value is not None:
            self.l1.set(key, value)
        
        return value
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        self.l1.set(key, value)
        await self.l2.set(key, value, ttl=ttl)
```

---

## 5. Data Quality Best Practices

### 5.1 Schema Validation

```python
class DataSchemaValidator:
    """Validate data against schemas."""
    
    def __init__(self, schemas: Dict[str, BaseModel]):
        self.schemas = schemas
    
    def validate(self, data: Any, schema_name: str) -> tuple:
        schema = self.schemas.get(schema_name)
        if not schema:
            raise ValueError(f"Unknown schema: {schema_name}")
        
        try:
            validated = schema(**data)
            return validated.dict(), []
        except Exception as e:
            return None, self._extract_errors(e)
    
    def _extract_errors(self, error) -> List[str]:
        if hasattr(error, "errors"):
            return [f"{e['loc'][0]}: {e['msg']}" for e in error.errors()]
        return [str(error)]
```

---

## 6. Backup and Recovery Best Practices

### 6.1 Automated Backups

```python
class DataBackupManager:
    """Manage data backups with retention."""
    
    def __init__(self, backup_destination, retention_days: int = 30):
        self.destination = backup_destination
        self.retention_days = retention_days
    
    async def backup(self, data: Any, backup_id: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{backup_id}_{timestamp}.json"
        
        serialized = json.dumps(data) if not isinstance(data, str) else data
        await self.destination.save(filename, serialized)
        
        return filename
    
    async def restore(self, backup_id: str) -> Any:
        latest = await self._find_latest_backup(backup_id)
        data = await self.destination.load(latest)
        return json.loads(data) if data else None
    
    async def cleanup_old_backups(self) -> int:
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        old_backups = await self.destination.list_older_than(cutoff)
        
        for backup in old_backups:
            await self.destination.delete(backup)
        
        return len(old_backups)
```

---

## 7. Monitoring and Observability

### 7.1 Data Pipeline Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

class DataPipelineMetrics:
    """Metrics for data operations."""
    
    OPERATIONS = Counter("data_operations_total", "Total data operations", 
                         ["operation", "success"])
    LATENCY = Histogram("data_operation_duration_seconds", "Operation latency",
                        ["operation"])
    CACHE_HIT_RATE = Gauge("data_cache_hit_rate", "Cache hit ratio")
    QUEUE_DEPTH = Gauge("data_queue_depth", "Number of pending operations")
    
    @classmethod
    def record_operation(cls, operation: str, success: bool, duration: float):
        cls.OPERATIONS.labels(operation=operation, success=str(success)).inc()
        cls.LATENCY.labels(operation=operation).observe(duration)
```

---

## 8. Performance Optimization

### 8.1 Index Optimization

```python
class IndexOptimizer:
    """Optimize database indexes for agent queries."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def create_optimal_indexes(self, tables: List[str]) -> None:
        for table in tables:
            await self._create_agent_indexes(table)
    
    async def _create_agent_indexes(self, table: str) -> None:
        indexes = [
            f"CREATE INDEX idx_{table}_session ON {table}(session_id)",
            f"CREATE INDEX idx_{table}_user_created ON {table}(user_id, created_at DESC)",
            f"CREATE INDEX idx_{table}_expires ON {table}(expires_at) WHERE expires_at IS NOT NULL"
        ]
        
        for sql in indexes:
            try:
                await self.db.execute(sql)
            except Exception as e:
                logger.warning(f"Index creation warning: {e}")
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)