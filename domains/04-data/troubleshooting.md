# Data Domain - Troubleshooting

## Overview

This document covers common data handling issues and solutions for LLM/agentic systems, providing guidance for debugging, performance optimization, and resolving typical problems.

---

## Common Issues and Solutions

### Issue 1: Slow Data Retrieval

**Symptoms:**
- High latency in agent responses
- Timeouts on data queries
- User experiencing delays

**Solutions:**
- Add indexes on queried columns
- Implement connection pooling
- Add caching layer
- Review query execution plans
- Consider read replicas

### Issue 2: Cache Misses Causing Performance Degradation

**Symptoms:**
- Repeated identical queries
- Higher database load
- Inconsistent response times

**Solutions:**
- Review cache key strategy
- Increase cache TTL for stable data
- Pre-warm cache for known patterns
- Monitor cache hit rates

### Issue 3: Context Window Overflow

**Symptoms:**
- Truncated responses
- Poor quality answers
- Token limit errors

**Solutions:**
- Implement context summarization
- Reduce context retention
- Prioritize recent messages
- Monitor token usage

### Issue 4: Data Privacy Violations

**Symptoms:**
- PII in logs
- Unencrypted sensitive data
- Privacy complaints

**Solutions:**
- Enable data sanitization
- Configure log filtering
- Implement encryption at rest
- Review access controls

---

## Diagnostic Procedures

### Procedure 1: Investigate Slow Queries

Step by step investigation:

```bash
# 1. Check query performance
EXPLAIN QUERY PLAN SELECT * FROM conversations WHERE user_id = ?

# 2. Review connection pool stats
redis-cli info stats | grep instantaneous_ops_per_sec

# 3. Analyze slow query logs
grep "slow" /var/log/mysql/slow.log
```

```python
# 4. Profile data access
import time

def timed_query(query_fn, *args):
    start = time.perf_counter()
    result = query_fn(*args)
    duration = time.perf_counter() - start
    logger.info(f"Query took {duration:.3f}s")
    return result
```

### Procedure 2: Debug Cache Issues

Investigation checklist:

- [ ] Check cache hit rate metrics
- [ ] Verify cache key generation
- [ ] Review TTL settings for data
- [ ] Check cache server health
- [ ] Examine cache eviction patterns

```python
# Debug cache behavior
class CacheDebugger:
    def __init__(self, cache):
        self.cache = cache
        self.hits = 0
        self.misses = 0
    
    async def get(self, key):
        value = await self.cache.get(key)
        if value is not None:
            self.hits += 1
        else:
            self.misses += 1
        return value
    
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
```

---

## Performance Optimization

### 1. Connection Pool Tuning

```python
# Monitor pool usage
class PoolMonitor:
    def __init__(self, pool):
        self.pool = pool
        self.checkouts = 0
        self.timeouts = 0
    
    async def get_connection(self, timeout=5):
        try:
            conn = await asyncio.wait_for(
                self.pool.acquire(), timeout=timeout
            )
            self.checkouts += 1
            return conn
        except asyncio.TimeoutError:
            self.timeouts += 1
            raise
```

### 2. Query Optimization

```python
# Optimal index creation
CREATE INDEX idx_conversation_user_created ON conversations(user_id, created_at DESC);
CREATE INDEX idx_conversation_expires ON conversations(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX idx_conversation_session ON conversations(session_id);
```

### 3. Pagination for Large Results

```python
class PaginatedDataFetcher:
    def __init__(self, page_size: int = 50):
        self.page_size = page_size
    
    async def fetch_all(self, query: str) -> List[Any]:
        results = []
        page_token = None
        
        while True:
            page = await self.fetch_page(query, page_token, self.page_size)
            results.extend(page["items"])
            
            if not page.get("next_page_token"):
                break
            
            page_token = page["next_page_token"]
        
        return results
```

---

## Recovery Procedures

### Procedure 1: Restore from Backup

1. Identify most recent clean backup
2. Validate backup integrity
3. Create restore target (new table/database)
4. Execute restore operation
5. Verify restored data quality
6. Update application configuration

```bash
# Restore example
mysql -u user -p database < backup_2024_01_15.sql
```

### Procedure 2: Handle Corrupted Cache

1. Flush cache cluster
2. Identify affected data sets
3. Rebuild cache from primary store
4. Validate rebuilt cache entries
5. Resume normal operations

```python
async def rebuild_cache(cache: AgentDataCache, data_source):
    keys = await data_source.list_all_keys()
    for key in keys:
        data = await data_source.get(key)
        cache.set(key, data, ttl=3600)
```

---

## Monitoring Queries

### Query 1: Cache Effectiveness

```
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
```

### Query 2: Database Query Performance

```
histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))
```

### Query 3: Data Access Patterns

```
sum by(conversation_id) (rate(conversation_queries_total[1h]))
```

---

## Common Error Messages

### Error: "Connection pool exhausted"

Likely causes:
- Too many concurrent connections
- Leaked connections (not returned to pool)
- Pool size too small for workload

### Error: "Context length exceeded"

Likely causes:
- Too much conversation history retained
- Large document contexts not summarized
- Missing token counting in pipeline

### Error: "No valid data found"

Likely causes:
- Incorrect query parameters
- Data retention cleaned up relevant records
- Access control blocking query

---

## Production Checklist

### Daily Checks

- [ ] Check error dashboard for data-related spikes
- [ ] Verify cache hit rates above 80%
- [ ] Review slow query logs
- [ ] Check disk space on data stores
- [ ] Verify backups completed

### Weekly Checks

- [ ] Review data quality metrics
- [ ] Update database statistics
- [ ] Check index fragmentation
- [ ] Review retention policies
- [ ] Test restore procedures

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)