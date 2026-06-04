# Integration Domain - Troubleshooting

## Overview

This document provides comprehensive troubleshooting guidance for integration issues in LLM/agentic systems, covering debugging methodologies, common failure patterns, diagnostic procedures, and resolution strategies.

---

## Table of Contents

1. [Debugging Methodology](#1-debugging-methodology)
2. [API Troubleshooting](#2-api-troubleshooting)
3. [Webhook Troubleshooting](#3-webhook-troubleshooting)
4. [Streaming Issues](#4-streaming-issues)
5. [Authentication Problems](#5-authentication-problems)
6. [Performance Issues](#6-performance-issues)
7. [Data Consistency Errors](#7-data-consistency-errors)
8. [Network & Connectivity](#8-network--connectivity)
9. [Resource Exhaustion](#9-resource-exhaustion)
10. [Deployment Issues](#10-deployment-issues)

---

## 1. Debugging Methodology

### Structured Problem Analysis

```python
class ProblemStatement:
    """Define and track integration problems."""
    
    def __init__(self, description: str, severity: str):
        self.description = description
        self.severity = severity
        self.affected_services = []
        self.error_logs = []
        self.reproduction_steps = []
        self.hypotheses = []
        self.resolution = None
    
    def add_affected_service(self, service_name: str, 
                             error_pattern: str):
        self.affected_services.append({
            "service": service_name,
            "error_pattern": error_pattern
        })
    
    def add_hypothesis(self, hypothesis: str, test: str):
        self.hypotheses.append({
            "hypothesis": hypothesis,
            "test": test,
            "result": "pending"
        })
    
    def mark_resolved(self, resolution: str):
        self.resolution = resolution
        logger.info(f"Problem resolved: {resolution}")

class DebugTrace:
    """Capture complete debug trace for integration calls."""
    
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.span_id = str(uuid.uuid4())[:16]
        self.start_time = time.time()
        self.steps = []
        self.errors = []
    
    def add_step(self, service: str, operation: str, 
                 input_data: Dict = None, output_data: Dict = None):
        step = {
            "timestamp": time.time() - self.start_time,
            "service": service,
            "operation": operation,
            "input": self._sanitize(input_data or {}),
            "output": self._sanitize(output_data or {})
        }
        self.steps.append(step)
        return step
    
    def add_error(self, service: str, error: Exception, 
                  context: Dict = None):
        self.errors.append({
            "timestamp": time.time() - self.start_time,
            "service": service,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        })
    
    def _sanitize(self, data: Dict) -> Dict:
        sensitive_keys = ["password", "token", "secret", "api_key", "authorization"]
        return {
            k: "[REDACTED]" if k.lower() in sensitive_keys else v
            for k, v in data.items()
        }
    
    def to_dict(self):
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "duration_ms": (time.time() - self.start_time) * 1000,
            "steps": self.steps,
            "errors": self.errors,
            "status": "failed" if self.errors else "success"
        }
```

---

## 2. API Troubleshooting

### Issue 4: Schema Validation Failures

**Symptoms:**
- 422 Unprocessable Entity responses
- Missing required fields in requests
- Type coercion errors

**Diagnostics:**
```bash
# Validate request against OpenAPI schema
curl -X POST https://api.example.com/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}' -v

# Check JSON syntax
cat request.json | python -m json.tool

# Verify required fields
jq 'keys' request.json
jq '.prompt | type' request.json
```

**Solutions:**
- Implement Pydantic validators on all request models
- Add middleware to log raw request bodies before validation
- Return detailed validation errors in response
- Document schema in OpenAPI specs

### Issue 5: Slow Response Times

**Symptoms:**
- High p95/p99 latency
- Timeouts under load
- Database query slowness

**Diagnostics:**
```python
class LatencyProfiler:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    @contextmanager
    def profile(self, operation: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.metrics[operation].append(duration)
            logger.info(
                f"Operation {operation} completed",
                extra={"duration_ms": duration * 1000}
            )
    
    def report(self):
        report_data = {}
        for op, times in self.metrics.items():
            report_data[op] = {
                "count": len(times),
                "min_ms": min(times) * 1000,
                "max_ms": max(times) * 1000,
                "avg_ms": sum(times) / len(times) * 1000,
                "p95_ms": sorted(times)[int(len(times) * 0.95)] * 1000
            }
        return report_data

profiler = LatencyProfiler()

# Usage in code
with profiler.profile("database_query"):
    result = await db.fetch(query)
```

**Solutions:**
- Profile each stage of request processing
- Add database query logging with EXPLAIN ANALYZE
- Enable async processing for CPU-bound work
- Check connection pool exhaustion

### Issue 6: Memory Leaks

**Symptoms:**
- Increasing RSS over time
- OOM kills
- GC pressure

**Diagnostics:**
```python
import tracemalloc
import gc

class MemoryDebugger:
    def __init__(self):
        self.snapshots = []
    
    def start_tracing(self):
        tracemalloc.start(25)  # 25 frames deep
    
    def take_snapshot(self, label: str):
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append({
            "label": label,
            "timestamp": time.time(),
            "snapshot": snapshot
        })
    
    def analyze_growth(self, from_label: str, to_label: str):
        from_snap = next(s for s in self.snapshots 
                        if s["label"] == from_label)
        to_snap = next(s for s in self.snapshots 
                       if s["label"] == to_label)
        
        stats = to_snap["snapshot"].compare_to(
            from_snap["snapshot"], "lineno"
        )
        
        for stat in stats[:20]:
            logger.warning(
                f"Memory growth: {stat.traceback} "
                f"allocated {stat.size_diff / 1024:.1f}KB more"
            )
    
    def force_cleanup(self):
        gc.collect()
        self.take_snapshot("after_gc")

debugger = MemoryDebugger()
debugger.start_tracing()
```

**Solutions:**
- Enable circular reference debugging with `gc.set_debug()`
- Check for unclosed connections/sessions
- Review caches for unbounded growth
- Monitor object counts by type

---

## 3. Webhook Troubleshooting

### Issue 7: Silent Webhook Failures

**Symptoms:**
- Events not received
- No error logs
- Empty response logs

**Diagnostics:**
```python
class WebhookDiagnostic:
    def __init__(self, webhook_client):
        self.client = webhook_client
        self.delivery_log = []
    
    async def test_delivery(self, url: str, payload: Dict):
        delivery_id = str(uuid.uuid4())
        start = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers={
                        "X-Delivery-Id": delivery_id,
                        "X-Timestamp": str(start)
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    body = await response.text()
                    record = {
                        "delivery_id": delivery_id,
                        "url": url,
                        "status": response.status,
                        "duration_ms": (time.time() - start) * 1000,
                        "response_body": body,
                        "success": response.status < 400
                    }
                    self.delivery_log.append(record)
                    return record
        except Exception as e:
            record = {
                "delivery_id": delivery_id,
                "url": url,
                "error": str(e),
                "duration_ms": (time.time() - start) * 1000,
                "success": False
            }
            self.delivery_log.append(record)
            return record
    
    def analyze_logs(self):
        failures = [d for d in self.delivery_log if not d["success"]]
        if not failures:
            return {"status": "all_delivered"}
        
        error_patterns = defaultdict(int)
        for failure in failures:
            if "error" in failure:
                error_key = failure["error"].split(":")[0]
                error_patterns[error_key] += 1
        
        return {
            "status": "deliveries_failed",
            "failure_rate": len(failures) / len(self.delivery_log),
            "common_errors": dict(error_patterns)
        }
```

**Solutions:**
- Log every webhook attempt with full details
- Implement retry with exponential backoff (1s, 2s, 4s)
- Add dead letter queue for failed deliveries
- Verify TLS certificates are valid

### Issue 8: Webhook Signature Mismatch

**Symptoms:**
- 401 Unauthorized responses
- "Invalid signature" errors
- Events rejected silently

**Diagnostics:**
```python
import hmac
import hashlib
import base64

def debug_signature(payload: Dict, secret: str, 
                    signature: str) -> Dict:
    raw_payload = json.dumps(payload, sort_keys=True).encode()
    expected_sig = hmac.new(
        secret.encode(), raw_payload, hashlib.sha256
    ).hexdigest()
    
    return {
        "provided_signature": signature,
        "expected_signature": f"sha256={expected_sig}",
        "match": hmac.compare_digest(
            f"sha256={expected_sig}", signature
        ),
        "payload_bytes": len(raw_payload),
        "secret_length": len(secret)
    }

result = debug_signature(webhook_payload, "my_secret", 
                         request_headers.get("X-Signature"))
logger.info("Signature debug info", **result)
```

**Solutions:**
- Ensure consistent JSON serialization (sort keys)
- Use `hmac.compare_digest()` for constant-time comparison
- Verify secret hasn't been rotated
- Check for whitespace in secrets

---

## 4. Streaming Issues

### Issue 9: Stream Interruption

**Symptoms:**
- Client receives truncated responses
- Connection drops mid-stream
- Garbled SSE messages

**Diagnostics:**
```python
class StreamMonitor:
    def __init__(self):
        self.chunk_count = 0
        self.byte_count = 0
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
        self.chunk_count = 0
        self.byte_count = 0
    
    def record_chunk(self, chunk: str):
        self.chunk_count += 1
        self.byte_count += len(chunk.encode())
    
    def end(self):
        duration = time.time() - self.start_time if self.start_time else 0
        return {
            "duration_seconds": duration,
            "chunk_count": self.chunk_count,
            "byte_count": self.byte_count,
            "chunks_per_second": self.chunk_count / duration if duration > 0 else 0
        }
```

**Solutions:**
- Implement heartbeat/ping mechanism
- Add server-side keep-alive headers
- Handle client disconnection gracefully
- Use chunked transfer encoding correctly

### Issue 10: Backpressure Failure

**Symptoms:**
- Memory growth during streaming
- Producer overwhelms consumer
- Event loop lag

**Diagnostics:**
```python
async def monitor_queue(queue: asyncio.Queue):
    while True:
        size = queue.qsize()
        if size > 100:
            logger.warning(f"Queue size high: {size}")
        await asyncio.sleep(1)

async def bounded_stream():
    queue = asyncio.Queue(maxsize=100)
    
    async def producer():
        async for item in source:
            await queue.put(item)
        await queue.put(None)
    
    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            process(item)
            queue.task_done()
```

**Solutions:**
- Set `maxsize` on queues
- Monitor queue depth with alerts
- Implement flow control in streaming protocol
- Add circuit breaker for overwhelmed consumers

---

## 5. Authentication Problems

### Issue 11: Token Expiration

**Symptoms:**
- 401 Unauthorized after period of time
- "Token expired" errors
- Intermittent auth failures

**Diagnostics:**
```python
import jwt
import time

class TokenDebugger:
    def __init__(self, secret: str):
        self.secret = secret
    
    def inspect(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, self.secret, 
                                algorithms=["HS256"], 
                                options={"verify_exp": False})
            now = time.time()
            return {
                "valid": True,
                "exp": payload.get("exp"),
                "iat": payload.get("iat"),
                "expires_in": payload.get("exp", 0) - now if payload.get("exp") else None,
                "claims": payload
            }
        except jwt.ExpiredSignatureError:
            return {"valid": False, "reason": "expired"}
        except jwt.InvalidTokenError as e:
            return {"valid": False, "reason": str(e)}
    
    def is_expiring_soon(self, token: str, 
                         buffer_seconds: int = 300) -> bool:
        info = self.inspect(token)
        if not info.get("valid") and info.get("reason") == "expired":
            return True
        expires_in = info.get("expires_in")
        return expires_in is not None and expires_in < buffer_seconds

debugger = TokenDebugger("your-secret-key")
```

**Solutions:**
- Implement token refresh with expiration buffer
- Log token age on each request
- Configure appropriate token TTL based on use case
- Add graceful degradation during token refresh

### Issue 12: CORS Failures

**Symptoms:**
- Browser CORS errors
- Missing `Access-Control-Allow-Origin` headers
- Preflight requests failing

**Diagnostics:**
```bash
# Check CORS headers
curl -X OPTIONS https://api.example.com/endpoint \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# Expected headers
# Access-Control-Allow-Origin: https://app.example.com
# Access-Control-Allow-Methods: GET, POST, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization
# Access-Control-Max-Age: 3600
```

**Solutions:**
- Verify CORS middleware is applied
- Check wildcard `*` vs specific origins
- Ensure credentials mode is consistent
- Add explicit OPTIONS handler

---

## 6. Performance Issues

### Issue 13: Thread/Connection Pool Exhaustion

**Symptoms:**
- Requests hang indefinitely
- "Connection pool full" errors
- Increasing queue depth

**Diagnostics:**
```python
class PoolMonitor:
    def __init__(self, pool_name: str, pool):
        self.pool_name = pool_name
        self.pool = pool
        self.snapshots = []
    
    def snapshot(self):
        try:
            size = self.pool.size()
            used = self.pool.used()
            free = self.pool.free()
            
            snapshot = {
                "timestamp": time.time(),
                "size": size,
                "used": used,
                "free": free,
                "utilization": used / size if size > 0 else 0
            }
            self.snapshots.append(snapshot)
            return snapshot
        except AttributeError:
            # Handle different pool interfaces
            return {"status": "monitoring_not_supported"}
    
    def get_utilization_trend(self) -> List[float]:
        return [s["utilization"] for s in self.snapshots[-20:]]
    
    def is_exhausted(self) -> bool:
        if not self.snapshots:
            return False
        latest = self.snapshots[-1]
        return latest.get("free", 1) == 0

db_pool_monitor = PoolMonitor("database", db_pool)
http_pool_monitor = PoolMonitor("http", http_client)
```

**Solutions:**
- Log pool utilization periodically
- Alert when utilization exceeds 80%
- Increase pool size if consistently high
- Check for connection leaks (connections not released)

### Issue 14: Rate Limit Thrashing

**Symptoms:**
- Sporadic 429 errors
- Exponential backoff making things worse
- Request queue growing

**Diagnostics:**
```python
class RateLimitTracker:
    def __init__(self):
        self.requests = []
        self.limit = 100
        self.window = 60  # seconds
    
    def record_request(self) -> Dict:
        now = time.time()
        self.requests = [r for r in self.requests 
                        if now - r < self.window]
        current = len(self.requests)
        
        self.requests.append(now)
        
        return {
            "current": current,
            "limit": self.limit,
            "remaining": max(0, self.limit - current),
            "reset_time": self.requests[0] + self.window if len(self.requests) == 1 else min(self.requests) + self.window
        }
    
    def should_throttle(self) -> bool:
        return len(self.requests) >= self.limit * 0.9
```

**Solutions:**
- Implement client-side rate limiting before making requests
- Use adaptive rate limits based on response headers
- Add request queuing with exponential backoff
- Respect `Retry-After` headers

---

## 7. Data Consistency Errors

### Issue 15: Stale Cache Reads

**Symptoms:**
- Old data returned after updates
- Inconsistent views across services
- Cache invalidation failures

**Diagnostics:**
```python
class CacheConsistencyChecker:
    def __init__(self, cache_client, db_client):
        self.cache = cache_client
        self.db = db_client
    
    async def check_key(self, key: str) -> Dict:
        cached = await self.cache.get(key)
        db_value = await self.db.get(key)
        
        match = cached == db_value
        
        if not match:
            logger.warning(
                "Cache inconsistency detected",
                key=key,
                cache_type=type(cached).__name__,
                db_type=type(db_value).__name__
            )
        
        return {
            "key": key,
            "consistent": match,
            "cached": str(cached)[:200],
            "database": str(db_value)[:200]
        }
    
    async def periodic_check(self, keys: List[str], 
                             interval: int = 60):
        while True:
            for key in keys:
                await self.check_key(key)
            await asyncio.sleep(interval)
```

**Solutions:**
- Implement cache invalidation on writes
- Use TTL with reasonable values
- Add cache versioning
- Consider write-through or write-behind strategies

### Issue 16: Orphaned Resources

**Symptoms:**
- Sessions not cleaned up
- Leaked temporary resources
- Growing database tables

**Diagnostics:**
```python
class OrphanDetector:
    def __init__(self, db_client):
        self.db = db_client
    
    async def find_orphaned_sessions(self, 
                                      max_age_hours: int = 24) -> List:
        orphaned = await self.db.fetch("""
            SELECT s.id, s.created_at, COUNT(m.id) as msg_count
            FROM sessions s
            LEFT JOIN messages m ON s.id = m.session_id
            WHERE s.status = 'active'
              AND s.created_at < NOW() - INTERVAL ':age hours'
            GROUP BY s.id
            HAVING COUNT(m.id) = 0 OR MAX(m.created_at) < s.created_at
        """, {"age": max_age_hours})
        
        return [dict(row) for row in orphaned]
    
    async def cleanup_orphans(self):
        orphans = await self.find_orphaned_sessions()
        logger.info(f"Found {len(orphans)} orphaned sessions")
        # Delete or mark as expired
        return orphans
```

**Solutions:**
- Schedule periodic cleanup jobs
- Implement TTL on resources
- Add cleanup on normal request flow
- Monitor resource count metrics

---

## 8. Network & Connectivity

### Issue 17: DNS Resolution Failures

**Symptoms:**
- `getaddrinfo failed` errors
- Intermittent connection failures
- Name resolution timeouts

**Diagnostics:**
```python
import socket
import asyncio

class NetworkDiagnostic:
    @staticmethod
    async def test_dns(hostname: str) -> Dict:
        try:
            loop = asyncio.get_event_loop()
            info = await loop.getaddrinfo(
                hostname, None, 
                family=socket.AF_INET,
                type=socket.SOCK_STREAM
            )
            return {
                "hostname": hostname,
                "resolved": True,
                "addresses": [i[4][0] for i in info]
            }
        except socket.gaierror as e:
            return {
                "hostname": hostname,
                "resolved": False,
                "error": str(e)
            }
    
    @staticmethod
    async def test_connection(host: str, port: int, 
                              timeout: int = 5) -> Dict:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return {
                "host": host,
                "port": port,
                "accessible": True
            }
        except (asyncio.TimeoutError, OSError) as e:
            return {
                "host": host,
                "port": port,
                "accessible": False,
                "error": str(e)
            }
```

**Solutions:**
- Configure DNS caching with TTL
- Use IP addresses as fallback for critical services
- Implement connection retry with backoff
- Monitor DNS resolution latency

### Issue 18: TLS/SSL Issues

**Symptoms:**
- SSL handshake failures
- Certificate verification errors
- Protocol version mismatches

**Diagnostics:**
```bash
# Check SSL certificate
openssl s_client -connect api.example.com:443 -servername api.example.com

# Check certificate chain
openssl s_client -connect api.example.com:443 -showcerts

# Test specific TLS version
openssl s_client -tls1_2 -connect api.example.com:443
```

**Solutions:**
- Pin certificate authorities
- Disable weak cipher suites
- Implement certificate rotation
- Add certificate expiration monitoring

---

## 9. Resource Exhaustion

### Issue 19: File Descriptor Exhaustion

**Symptoms:**
- "Too many open files" errors
- Connection failures
- Process hangs

**Diagnostics:**
```python
import resource

class ResourceMonitor:
    @staticmethod
    def get_fd_count() -> int:
        try:
            import os
            return len(os.listdir(f"/proc/{os.getpid()}/fd"))
        except (FileNotFoundError, PermissionError):
            return -1
    
    @staticmethod
    def get_soft_limit() -> int:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        return soft
    
    @staticmethod
    def get_memory_usage() -> Dict:
        import psutil
        process = psutil.Process()
        mem_info = process.memory_info()
        return {
            "rss_mb": mem_info.rss / (1024 * 1024),
            "vms_mb": mem_info.vms / (1024 * 1024),
            "percent": process.memory_percent()
        }
    
    @staticmethod
    def log_resource_usage():
        logger.info(
            "resource_usage",
            fd_count=ResourceMonitor.get_fd_count(),
            fd_limit=ResourceMonitor.get_soft_limit(),
            **ResourceMonitor.get_memory_usage()
        )
```

**Solutions:**
- Monitor FD count in production
- Set appropriate ulimit values
- Ensure connections/sessions are closed
- Use context managers for resource cleanup

---

## 10. Deployment Issues

### Issue 20: Startup Failures

**Symptoms:**
- Container crashes on startup
- Health check failures
- Dependency errors

**Diagnostics:**
```python
class StartupValidator:
    def __init__(self):
        self.checks = []
        self.failed = []
    
    def add_check(self, name: str, check_fn: Callable, critical: bool = True):
        self.checks.append({
            "name": name,
            "check": check_fn,
            "critical": critical
        })
    
    async def run_all(self) -> Dict:
        results = {}
        for check in self.checks:
            try:
                result = await check["check"]()
                results[check["name"]] = {
                    "status": "pass",
                    "result": result
                }
            except Exception as e:
                results[check["name"]] = {
                    "status": "fail",
                    "error": str(e)
                }
                if check["critical"]:
                    self.failed.append(check["name"])
        
        return {
            "healthy": len(self.failed) == 0,
            "checks": results,
            "failed_critical": self.failed
        }

validator = StartupValidator()

validator.add_check(
    "database_connection",
    lambda: db.execute("SELECT 1"),
    critical=True
)

validator.add_check(
    "redis_connection",
    lambda: redis.ping(),
    critical=True
)

validator.add_check(
    "llm_api_health",
    lambda: llm_client.health_check(),
    critical=False
)

# Run during startup
startup_result = await validator.run_all()
if not startup_result["healthy"]:
    logger.error("Startup checks failed", **startup_result)
    sys.exit(1)
```

**Solutions:**
- Implement comprehensive startup checks
- Add dependency wait logic with timeouts
- Verify configuration before starting
- Log detailed startup errors

---

## Quick Reference

### Diagnostic Commands

```bash
# Network connectivity
ping -c 4 api.example.com
traceroute api.example.com
curl -v https://api.example.com/health

# DNS resolution
nslookup api.example.com
dig api.example.com

# SSL/TLS
openssl s_client -connect api.example.com:443

# System resources
ulimit -n
cat /proc/sys/fs/file-nr

# Docker logs
docker logs --tail 100 container_name
docker logs -f container_name

# Kubernetes debugging
kubectl describe pod <pod_name>
kubectl get events --field-selector reason=Failed
kubectl logs -l app=agent --previous
```

### Monitoring Metrics

```python
KEY_METRICS = {
    "availability": "Uptime percentage target: 99.9%",
    "latency_p99": "P99 latency target: <500ms",
    "error_rate": "Error rate target: <0.1%",
    "throughput": "Requests per second capacity",
    "queue_depth": "Background queue depth",
    "connection_utilization": "DB/HTTP pool utilization",
    "cache_hit_ratio": "Cache effectiveness: >80%",
    "memory_usage": "RSS percentage",
    "fd_utilization": "Open file descriptors / limit"
}

METRIC_ALERTS = {
    "high_latency": "p99 > 1s for 5 minutes",
    "high_error_rate": "error_rate > 1% for 2 minutes",
    "queue_growth": "queue depth > 1000 for 5 minutes",
    "memory_pressure": "memory > 85% for 3 minutes",
    "fd_exhaustion": "fd utilization > 90% for 1 minute"
}
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)