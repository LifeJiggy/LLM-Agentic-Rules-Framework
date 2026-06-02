# Data Domain - Advanced Concepts

## Overview

This document covers advanced data concepts for LLM/agentic systems.

## Advanced Patterns

### 1. CQRS Pattern

```python
class CommandHandler:
    def execute(self, command):
        # Write operations
        self.db.save(command)

class QueryHandler:
    def execute(self, query):
        # Read from optimized read store
        return self.read_db.query(query)
```

### 2. Event Sourcing

```python
class EventStore:
    def append(self, event):
        self.events.append(event)
    
    def get_events(self, aggregate_id):
        return [e for e in self.events if e.aggregate_id == aggregate_id]
```

### 3. Data Sharding

```python
class ShardManager:
    def __init__(self, num_shards):
        self.num_shards = num_shards
    
    def get_shard(self, key):
        return hash(key) % self.num_shards
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
