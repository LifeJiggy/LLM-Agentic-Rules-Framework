# Performance Domain - Troubleshooting

## Overview

Common performance issues in LLM and agentic systems, with diagnosis and remediation steps.

## Table of Contents

1. [Slow End-To-End Responses](#1-slow-end-to-end-responses)
2. [Token Cost Spikes](#2-token-cost-spikes)
3. [Retrieval Latency](#3-retrieval-latency)
4. [Tool Bottlenecks](#4-tool-bottlenecks)
5. [Cache Regressions](#5-cache-regressions)
6. [Out-of-Memory and Resource Exhaustion](#6-out-of-memory-and-resource-exhaustion)
7. [Provider Rate Limiting and Throttling](#7-provider-rate-limiting-and-throttling)
8. [Connection and Socket Exhaustion](#8-connection-and-socket-exhaustion)
9. [Latency Degradation on Long Conversations](#9-latency-degradation-on-long-conversations)
10. [Streaming UX Issues](#10-streaming-ux-issues)
11. [Duplicate or Redundant Tool Calls](#11-duplicate-or-redundant-tool-calls)
12. [Model Selection Mismatches](#12-model-selection-mismatches)
13. [Cache Stampede](#13-cache-stampede)
14. [Circuit Breaker Stuck Open](#14-circuit-breaker-stuck-open)
15. [Memory Leaks in Long-Running Agents](#15-memory-leaks-in-long-running-agents)
16. [Load Test Failures](#16-load-test-failures)
17. [Cost Anomalies](#17-cost-anomalies)
18. [Observability Gaps](#18-observability-gaps)
19. [Agent Loop Unbounded Iteration](#19-agent-loop-unbounded-iteration)
20. [Context Drift and Stale History](#20-context-drift-and-stale-history)
21. [Scheduler and Queue Backpressure](#21-scheduler-and-queue-backpressure)
22. [Disk and Model Weight Loading](#22-disk-and-model-weight-loading)
23. [Tokenizer and Output Format Overhead](#23-tokenizer-and-output-format-overhead)
24. [Multimodal and Attachment Bloat](#24-multimodal-and-attachment-bloat)
25. [Dependency Cascade Failures](#25-dependency-cascade-failures)
26. [Configuration Drift](#26-configuration-drift)
27. [Cold Start Performance](#27-cold-start-performance)
28. [Garbage Collection Pauses](#28-garbage-collection-pauses)
29. [DNS Resolution Delays](#29-dns-resolution-delays)
30. [TLS Handshake Overhead](#30-tls-handshake-overhead)

---

## 1. Slow End-To-End Responses

**Symptoms:**

- User-facing responses exceed latency targets.
- P95 or P99 latency increases while average latency appears acceptable.
- Long tasks time out before the agent finishes.

**Likely causes:**

- Prompt context has grown over time.
- Retrieval or tool calls are serialized unnecessarily.
- Model provider latency changed.
- Agent loop iterations are unbounded.

**Diagnostic steps:**

1. Break traces into application, retrieval, model, and tool segments.
2. Compare prompt and completion token counts against previous releases.
3. Cap agent loop iterations and tool retries.
4. Parallelize independent read-only tool calls where safe.
5. Add streaming or partial progress updates for long responses.

### Investigation Snippet

```python
class SegmentedTimer:
    def __init__(self, prompt: str):
        self.segments = {}
        self.overall_start = time.perf_counter()
    
    async def measure(self, name: str, coro):
        start = time.perf_counter()
        result = await coro
        self.segments[name] = time.perf_counter() - start
        return result
    
    def report(self):
        total = time.perf_counter() - self.overall_start
        print(f"Total: {total:.3f}s")
        for name, duration in self.segments.items():
            print(f"  {name}: {duration:.3f}s ({duration/total:.0%})")
```

### Resolution Checklist

- [ ] Add segment tracing.
- [ ] Compare p95 by model and by route.
- [ ] Reduce prompt tokens via summarization.
- [ ] Parallelize tool calls.
- [ ] Add streaming.

---

## 2. Token Cost Spikes

**Symptoms:**

- Cost per request increases.
- High-volume workflows consume budget faster than expected.
- Batch jobs cause unexpected provider charges.

**Likely causes:**

- More retrieved chunks are inserted into prompts.
- Conversation history is not summarized or pruned.
- A larger model is used for simple routing or extraction.
- Retries repeat expensive prompts.

**Diagnostic steps:**

1. Track prompt tokens, completion tokens, and retry counts.
2. Set token budgets per workflow.
3. Move simple tasks to smaller models where quality allows.
4. Cache stable intermediate results.
5. Stop retrying deterministic validation failures.

### Investigation Snippet

```python
class CostInvestigator:
    def __init__(self, pricing):
        self.pricing = pricing
        self.requests = []
    
    def record(self, model: str, prompt_tokens: int, completion_tokens: int, retries: int = 0):
        cost = self.pricing.cost(model, prompt_tokens, completion_tokens) * (1 + retries)
        self.requests.append({
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "retries": retries,
            "cost": cost,
        })
    
    def total_cost(self) -> float:
        return sum(r["cost"] for r in self.requests)
    
    def by_model(self) -> dict:
        from collections import defaultdict
        buckets = defaultdict(float)
        for r in self.requests:
            buckets[r["model"]] += r["cost"]
        return dict(buckets)
```

### Resolution Checklist

- [ ] Verify token distribution per request type.
- [ ] Add token budgets.
- [ ] Review model routing choices.
- [ ] Enable caching.

---

## 3. Retrieval Latency

**Symptoms:**

- Model calls are fast, but total response time is slow.
- Vector search or database queries dominate traces.
- Retrieval returns too many weakly relevant chunks.

**Likely causes:**

- Missing database indexes.
- Poor chunking strategy.
- Search parameters are too broad.
- Reranking is expensive or applied too often.

**Diagnostic steps:**

1. Profile vector search, metadata filters, and reranking separately.
2. Add indexes for common metadata filters.
3. Reduce top-k before reranking.
4. Cache frequent retrieval results when data freshness allows.
5. Revisit chunk size and overlap.

### Resolution Checklist

- [ ] Profile each sub-step of retrieval.
- [ ] Add missing indexes.
- [ ] Cache retrieval results where possible.
- [ ] Reduce top-k to the minimum acceptable.

---

## 4. Tool Bottlenecks

**Symptoms:**

- Agent reasoning is quick, but external actions are slow.
- Tool calls queue or time out under load.
- Retried tool calls amplify downstream load.

**Likely causes:**

- External API rate limits.
- Serial calls that could be batched.
- Missing timeout boundaries.
- Unbounded retries during downstream degradation.

**Diagnostic steps:**

1. Add per-tool latency and error metrics.
2. Batch or coalesce repeated reads.
3. Use backoff with jitter.
4. Queue long-running work.
5. Add circuit breakers for degraded dependencies.

### Resolution Checklist

- [ ] Add timeout to every tool call.
- [ ] Group identical reads.
- [ ] Add circuit breakers.
- [ ] Use event queues for long jobs.

---

## 5. Cache Regressions

**Symptoms:**

- Latency increases after a release that changed prompts, models, or retrieval.
- Cache hit rate drops sharply.
- Users receive stale or inconsistent responses.

**Likely causes:**

- Cache keys changed unintentionally.
- Cache invalidation rules are incomplete.
- Policy or prompt versions are missing from cache keys.
- Sensitive or user-specific data is cached too broadly.

**Diagnostic steps:**

1. Compare cache hit rate before and after release.
2. Inspect cache key components.
3. Include model, prompt, policy, and retrieval versions where relevant.
4. Add tests for stale and cross-user cache behavior.
5. Purge unsafe cache entries immediately.

### Resolution Checklist

- [ ] Add cache key version components.
- [ ] Review invalidation rules.
- [ ] Add tests for stale data.

---

## 6. Out-of-Memory and Resource Exhaustion

**Symptoms:**

- Worker process RSS grows continuously.
- OOM killer terminates services.
- Latency spikes before crashes.

**Likely causes:**

- Session state grows without bound.
- Unclosed file handles or database cursors.
- Large retrieval outputs retained in memory.
- Memory-heavy libraries (tokenizers, embeddings) loaded repeatedly.

**Diagnostic steps:**

1. Inspect RSS and swap usage over time.
2. Profile object allocations.
3. Review session lifecycle and cleanup.

### Resolution Checklist

- [ ] Cap session size.
- [ ] Ensure cleanup on session end.
- [ ] Use streaming for large outputs.
- [ ] Monitor memory in production.

---

## 7. Provider Rate Limiting and Throttling

**Symptoms:**

- HTTP 429 responses increase.
- Downstream services see retry storms.
- Latency is highly variable.

**Likely causes:**

- Concurrency exceeds provider limits.
- Missing or ignored `Retry-After` headers.
- Single point of failure for provider calls.

**Diagnostic steps:**

1. Inspect provider metrics and error codes.
2. Review retry configuration.
3. Verify concurrency limits match provider quota.

### Resolution Checklist

- [ ] Respect provider concurrency limits.
- [ ] Honor `Retry-After` headers.
- [ ] Run load tests under quota constraints.

---

## 8. Connection and Socket Exhaustion

**Symptoms:**

- `OSError: [Errno 24] Too many open files`.
- New requests stall or hang.
- TLS handshakes consume CPU.

**Likely causes:**

- HTTP client session created per request.
- Connector limits too high or too low.
- Missing cleanup on process shutdown.

**Diagnostic steps:**

1. Inspect open socket count.
2. Review HTTP client initialization.
3. Verify session cleanup.

### Resolution Checklist

- [ ] Switch to session reuse.
- [ ] Set connector limits.
- [ ] Close sessions on shutdown.

---

## 9. Latency Degradation on Long Conversations

**Symptoms:**

- Initial turns are fast; later turns are slow.
- Token input grows with conversation length.
- Summarization triggers cause noticeable pauses.

**Likely causes:**

- Unbounded conversation history growth.
- Summarization is synchronous and blocks the event loop.
- No sliding window mechanism.

**Diagnostic steps:**

1. Plot token input by conversation turn.
2. Review summarization behavior.

### Resolution Checklist

- [ ] Add sliding window.
- [ ] Summarize asynchronously.
- [ ] Cap total token input.

---

## 10. Streaming UX Issues

**Symptoms:**

- Users see blank pages for several seconds before output begins.
- Output arrives in large, irregular bursts.
- Mobile connections experience stutter.

**Likely causes:**

- Buffering too large or too small.
- Backpressure propagation not implemented.
- Frameworks delay rendering until first chunk.

**Resolution:**

Tune buffer sizes. Send heartbeats to prevent intermediate proxies from timing out.

---

## 11. Duplicate or Redundant Tool Calls

**Symptoms:**

- Same tool called repeatedly with identical parameters.
- Tool latency dominates agent time.
- External service sees duplicate requests.

**Diagnostic steps:**

1. Inspect tool call trace.
2. Verify deduplication logic.
3. Review agent loop for unnecessary re-invocation.

### Resolution Checklist

- [ ] Cache tool calls by canonicalized parameters.
- [ ] Deduplicate within a single step.
- [ ] Log tool call hits and misses.

---

## 12. Model Selection Mismatches

**Symptoms:**

- Simple tasks run on expensive, slow models.
- Quality is fine, but cost and latency are excessive.

**Diagnostic steps:**

1. Classify tasks by complexity.
2. Review routing table.

### Resolution Checklist

- [ ] Add complexity classifier.
- [ ] Add direct routes for simple tasks.
- [ ] Validate quality after routing changes.

---

## 13. Cache Stampede

**Symptoms:**

- Latency spikes when a popular key expires.
- Multiple replicas hit the backing store simultaneously.

**Resolution:**

Use probabilistic early expiration plus request coalescing.

```python
async def get_with_jitter(cache, key: str, fetch_fn, base_ttl: int = 300):
    cached = await cache.get(key)
    if cached:
        return json.loads(cached)
    lock_key = f"lock:{key}"
    acquired = await cache.set(lock_key, "1", ex=5, nx=True)
    if not acquired:
        await asyncio.sleep(0.1)
        return await get_with_jitter(cache, key, fetch_fn, base_ttl)
    try:
        value = await fetch_fn()
        jitter = base_ttl * 0.1
        ttl = base_ttl + random.randint(-int(jitter), int(jitter))
        await cache.setex(key, ttl, json.dumps(value))
        await cache.delete(lock_key)
        return value
    except Exception:
        await cache.delete(lock_key)
        raise
```

---

## 14. Circuit Breaker Stuck Open

**Symptoms:**

- Failure rate falls, but requests are still rejected.
- Half-open probes never succeed.

**Diagnostic steps:**

1. Inspect circuit breaker state and counters.
2. Verify recovery timeout is reasonable.
3. Check that `_success` is called on successful probe.

### Resolution Checklist

- [ ] Verify half-open semantics.
- [ ] Set reasonable recovery timeout.
- [ ] Add metrics to observe transitions.

---

## 15. Memory Leaks in Long-Running Agents

**Symptoms:**

- RSS increases over hours or days.
- Performance degrades gradually.
- Eventually OOM-crashes.

**Diagnostic steps:**

1. Take heap snapshots before and after test run.
2. Search for retained session state.
3. Check for circular references in caches.

### Resolution Checklist

- [ ] Cap session and cache sizes.
- [ ] Remove strong references to closed sessions.
- [ ] Use weakrefs for caches.

---

## 16. Load Test Failures

**Symptoms:**

- Tests fail at concurrency > 1.
- Latency increases linearly with concurrency.
- Errors increase under load.

**Diagnostic steps:**

1. Inspect thread or event loop saturation.
2. Check for lock contention.
3. Review connection pool configuration.

---

## 17. Cost Anomalies

**Symptoms:**

- Monthly bill exceeds forecast.
- Certain users or workflows dominate spend.
- New release triggered unexpected charges.

**Diagnostic steps:**

1. Break down cost by model, endpoint, and user.
2. Compare per-request cost against baseline.
3. Check for runaway retries.

### Resolution Checklist

- [ ] Alerts for budget overruns.
- [ ] Review user and endpoint cost splits.
- [ ] Audit retry behavior.

---

## 18. Observability Gaps

**Symptoms:**

- Issue discovered by user report after impact.
- Unknown downstream failures.
- Blind spots in distributed trace.

**Diagnostic steps:**

1. Review alert coverage.
2. Inject synthetic requests that cover full path.
3. Check trace completeness and sampled rate.

### Resolution Checklist

- [ ] Instrument all external calls.
- [ ] Ensure tags/model IDs are present.
- [ ] Review alert rules quarterly.

---

## 19. Agent Loop Unbounded Iteration

**Symptoms:**

- Agent runs for minutes or hours without returning.
- Token cost shows repeated model/tool cycles.
- Users cancel the operation.

**Likely causes:**

- Loop termination condition missing.
- Tool failures do not break the loop.
- Refinement loop continues even after satisfactory output.

**Resolution:**

1. Hard cap loop iterations per request.
2. Add early-exit conditions for repeated identical tool calls.
3. Review loop termination criteria.

---

## 20. Context Drift and Stale History

**Symptoms:**

- Agent mentions facts from early conversation that are contradicted later.
- Token budget is dominated by outdated retrieval or tool outputs.

**Resolution:**

1. Use sliding window plus summary.
2. Summarize retrieval results before insertion.
3. Drop repeated tool outputs.

---

## 21. Scheduler and Queue Backpressure

**Symptoms:**

- Queue depth grows without bound.
- Workers fall behind during traffic spikes.
- Request latency grows with queue wait time.

**Likely causes:**

- Consumer lag.
- Backpressure not propagated.
- No depth threshold to trigger scaling.

**Resolution:**

1. Add queue-depth alerting.
2. Apply autoscaling based on queue depth.
3. Reject requests early when queue is near capacity.

---

## 22. Disk and Model Weight Loading

**Symptoms:**

- First request after deploy is much slower than subsequent requests.
- Workers restart frequently in rolling-update deployments.

**Likely causes:**

- Cold cache for model weights.
- Disk I/O contention during weight loading.

**Resolution:**

1. Pre-warm workers before serving traffic.
2. Pin models to fast storage (volume type, locality).
3. Share read-only model cache across workers.

---

## 23. Tokenizer and Output Format Overhead

**Symptoms:**

- Request-level latency varies unexpectedly.
- High CPU utilization around tokenizer boundaries.

**Resolution:**

1. Cache tokenizer instances.
2. Avoid tokenizing large documents in the hot path.
3. Pre-truncate inputs to maximum token limit.

---

## 24. Multimodal and Attachment Bloat

**Symptoms:**

- Responses with images or PDFs take much longer.
- Cost per request increases with attachment count.

**Likely causes:**

- Full attachments passed every turn.
- Uncompressed images dominate token count.

**Resolution:**

1. Compress images before embedding.
2. Store attachments externally and pass references.
3. Separate attachment loading from prompt construction.

---

## 25. Dependency Cascade Failures

**Symptoms:**

- Upstream database failure causes agent latency spike.
- Cascading timeouts block shutdown.

**Likely causes:**

- Missing graceful timeout in database client.
- Unhandled exceptions propagate.

**Resolution:**

1. Add timeouts to all database or search calls.
2. Add graceful degradation paths.
3. Ensure exceptions do not leak as raw traces.

---

## 26. Configuration Drift

**Symptoms:**

- Performance degrades over time without code changes.
- Different environments have different performance characteristics.
- Rollback does not restore original latency.

**Diagnostic steps:**

1. Compare configuration across environments.
2. Review change history for config changes.
3. Validate configuration in CI.

### Resolution Checklist

- [ ] Pin configuration versions.
- [ ] Test configuration changes in staging.
- [ ] Automate configuration validation.

---

## 27. Cold Start Performance

**Symptoms:**

- First requests after deploy are slower.
- Workers take time to reach steady state.
- Cache warmup affects initial latency.

**Diagnostic steps:**

1. Measure cold start vs warm latency.
2. Review initialization sequence.
3. Check for lazy loading issues.

### Resolution Checklist

- [ ] Pre-warm worker processes.
- [ ] Preload model weights.
- [ ] Initialize caches at startup.

---

## 28. Garbage Collection Pauses

**Symptoms:**

- Sporadic latency spikes with no apparent cause.
- GC logs show frequent full collections.
- Heap usage grows and shrinks periodically.

**Diagnostic steps:**

1. Enable GC logging.
2. Review heap snapshots.
3. Check for object churn.

### Resolution Checklist

- [ ] Tune GC parameters.
- [ ] Reduce object allocations.
- [ ] Use object pools for hot paths.

---

## 29. DNS Resolution Delays

**Symptoms:**

- Intermittent latency spikes.
- Errors correlate with DNS timeouts.
- Latency improves with DNS caching.

**Diagnostic steps:**

1. Profile DNS resolution time.
2. Check DNS cache TTL.
3. Review DNS provider performance.

### Resolution Checklist

- [ ] Increase DNS cache TTL.
- [ ] Use local DNS cache.
- [ ] Consider DNS prefetching.

---

## 30. TLS Handshake Overhead

**Symptoms:**

- First request to new host is slow.
- TLS renegotiation visible in traces.
- High CPU on connection establishment.

**Diagnostic steps:**

1. Profile TLS handshake time.
2. Check session resumption configuration.
3. Review cipher suite performance.

### Resolution Checklist

- [ ] Enable TLS session resumption.
- [ ] Use session tickets.
- [ ] Optimize cipher suites.

---

## Diagnostic Decision Tree

```
Latency high?
  ├── Yes -> Segment trace
  │         ├── Model slow? -> Check provider latency or select smaller model.
  │         ├── Retrieval slow? -> Check indexes and top-k.
  │         ├── Tool slow? -> Check timeouts and rate limits.
  │         └── Network? -> Reuse connection pool.
  └── No -> Cost high?
            ├── Yes -> Inspect token counts and model routing.
            └── No -> Resilience issue?
                      ├── Errors up? -> Check retries and circuit breakers.
                      └── Memory up? -> Look for leaks and unbounded state.
```

---

## Quick Fixes

| Symptom            | Quick Fix                                      | Risk  |
|--------------------|-------------------------------------------------|-------|
| High latency       | Reduce prompt size or use smaller model          | Low   |
| High cost          | Enable caching for repeated prompts              | Low   |
| Rate limiting      | Reduce concurrency, add backoff                 | Low   |
| Memory growth      | Add TTL or maxlen to queues and caches           | Low   |
| Stale cache        | Shorten TTL or add invalidation hook             | Low   |
| OOM                | Close sessions, cap session size                 | Low   |
| Streaming blank    | Reduce initial buffer size                       | Low   |
| Tool storms        | Add deduplication and circuit breakers           | Low   |
| Context bloat      | Add summarization and sliding window             | Low   |
| DNS delays         | Increase cache TTL                               | Low   |
| TLS overhead       | Enable session resumption                        | Low   |
| GC pauses          | Tune GC or use object pools                      | Low   |
| Config drift       | Pin configs, validate in CI                      | Low   |
| Cold starts        | Pre-warm workers and caches                      | Low   |

---

## Escalation Procedures

### When to Escalate

- **P0 - Page immediately**: Complete outage, data loss, security breach
- **P1 - Page within 15 min**: Significant degradation, rising errors, SLO breach
- **P2 - Respond within 1 hour**: Minor degradation, warnings, cost anomalies
- **P3 - Respond within 4 hours**: Optimization opportunities, feature requests

### Escalation Contacts

| Role | Contact | Escalation Condition |
|------|---------|---------------------|
| On-Call Engineer | @oncall | All P0/P1 incidents |
| Team Lead | @lead | P0 incidents or after 30 min |
| Engineering Manager | @manager | P0 incidents or after 1 hour |
| VP Engineering | @vp | P0 incidents or after 2 hours |

### Communication Templates

#### Initial Alert

```
[P0] Performance Incident
Component: [agent/router/cache/etc]
Start Time: [ISO timestamp]
Symptoms: [brief description]
Current Impact: [users affected, SLO breach status]
Next Steps: [triage actions]
```

#### Status Update

```
[P0] Update: [Incident Name]
Status: [Investigating/Identified/Mitigating/Resolved]
Current: [brief status]
ETA: [if available]
```

#### Resolution

```
[P0] Resolved: [Incident Name]
Root Cause: [brief description]
Duration: [start to resolution]
Impact: [final impact assessment]
Follow-up: [action items]
```

---

## Post-Incident Review Template

### Incident Summary

- **Incident ID**: [unique identifier]
- **Date/Time**: [when it occurred]
- **Duration**: [how long it lasted]
- **Severity**: [P0/P1/P2/P3]
- **Components Affected**: [list components]

### Timeline

| Time | Event |
|------|-------|
| HH:MM | [first indicator] |
| HH:MM | [detection] |
| HH:MM | [escalation] |
| HH:MM | [mitigation] |
| HH:MM | [resolution] |

### Root Cause Analysis

**What happened?**

[Description of the failure mode]

**Why did it happen?**

1. [Technical cause]
2. [Process cause]
3. [Organizational cause]

### Impact Assessment

- **Users Affected**: [number or percentage]
- **Duration**: [minutes/hours]
- **Financial Impact**: [estimated cost]
- **Reputation Impact**: [if applicable]

### Remediation Steps

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [action 1] | [team/person] | [date] | [pending/in progress/done] |
| [action 2] | [team/person] | [date] | [pending/in progress/done] |

### Lessons Learned

1. [What went well]
2. [What could be improved]
3. [Where we got lucky]

### Action Items

- [ ] [Preventive action 1]
- [ ] [Preventive action 2]
- [ ] [Detective action 1]
- [ ] [Detective action 2]

---

## Common Debugging Commands

### Linux/macOS

```bash
# Check process resource usage
ps aux | grep agent
top -p <pid>
htop

# Check open files
lsof -p <pid> | wc -l
lsof -p <pid>

# Check network connections
ss -tulpn | grep <port>
netstat -an | grep <port>

# Check memory
free -h
cat /proc/<pid>/status | grep Vm

# Profile CPU
perf top -p <pid>
py-spy top --pid <pid>

# Trace system calls
strace -p <pid>
dtrace -p <pid>
```

### Windows

```powershell
# Check process
Get-Process -Name agent

# Check memory
Get-Process -Name agent | Select-Object WorkingSet

# Check network
netstat -ano | findstr <port>

# Profile
wpr -start CPU -record
# ... reproduce issue ...
wpr -stop profile.etl
```

### Kubernetes

```bash
# Get pod details
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# Check resource usage
kubectl top pod <pod-name>
kubectl top node <node-name>

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

---

## Performance Regression Checklist

### Detection

- [ ] Automated load test in CI/CD pipeline
- [ ] p95 latency regression detection
- [ ] Cost per request regression detection
- [ ] Error rate regression detection

### Analysis

- [ ] Identify changed code in regression window
- [ ] Profile new vs old version
- [ ] Compare metrics side-by-side
- [ ] Review deployment changes

### Remediation

- [ ] Rollback to previous version
- [ ] Fix regression in feature branch
- [ ] Add regression test to prevent recurrence
- [ ] Update performance budgets if appropriate

---

## Capacity Planning Guide

### Metrics to Track

- Current request rate (RPS)
- Peak request rate (RPS)
- Average latency (p50, p95, p99)
- Error rate
- Resource utilization (CPU, memory, network, disk)
- Queue depth
- Connection pool saturation

### Scaling Triggers

| Metric | Trigger | Action |
|--------|---------|--------|
| CPU | > 70% | Add replicas |
| Memory | > 80% | Increase memory or add replicas |
| Queue depth | > target | Add workers |
| p95 latency | > SLO | Scale out or optimize |
| Error rate | > threshold | Investigate and scale |

### Forecasting

- Track weekly/monthly growth trends
- Plan 3-6 months ahead
- Maintain 30% headroom
- Review quarterly

---

## Cost Optimization Guide

### Immediate Actions

1. Enable caching for repeated queries
2. Route simple tasks to cheaper models
3. Set token budgets
4. Reduce unnecessary tool calls

### Medium-term Actions

1. Implement semantic caching
2. Add request deduplication
3. Optimize batch sizes
4. Review and eliminate unused features

### Long-term Actions

1. Evaluate custom models
2. Consider self-hosting for high volume
3. Implement intelligent scaling
4. Negotiate volume discounts

---

## Security and Performance

### Secure by Default

- Never disable TLS for performance
- Use TLS session resumption
- Implement proper certificate validation
- Use secrets management (not environment variables)

### Performance-Security Tradeoffs

| Practice | Security Benefit | Performance Cost | Recommendation |
|----------|------------------|------------------|----------------|
| TLS 1.3 | Encryption | ~5% latency | Always use |
| Certificate rotation | Prevents compromise | Brief latency spike | Use automated rotation |
| Request signing | Prevents tampering | ~2% latency | Use for sensitive operations |
| Rate limiting | Prevents abuse | Minimal overhead | Always implement |

---

## Disaster Recovery

### Recovery Time Objectives (RTO)

| Component | RTO | Strategy |
|-----------|-----|----------|
| Stateless API | 5 minutes | Scale up/out |
| Database | 30 minutes | Failover replica |
| Cache | 1 minute | Switch to DB fallback |
| Message Queue | 10 minutes | Restore from backup |

### Recovery Point Objectives (RPO)

| Data Type | RPO | Strategy |
|-----------|-----|----------|
| Session state | 1 minute | Frequent cache writes |
| User data | 15 minutes | Database replication |
| Logs | 1 hour | Centralized logging |
| Metrics | 5 minutes | Time-series database |

---

## Compliance and Performance

### GDPR Considerations

- Right to erasure affects caching strategies
- Data locality affects latency
- Consent management affects personalization
- Data portability affects API design

### Performance Implications

| Requirement | Performance Impact | Mitigation |
|-------------|-------------------|------------|
| Data residency | Increased latency for cross-region | Use edge caching |
| Right to deletion | Cache invalidation complexity | Implement key naming scheme |
| Consent management | Conditional data processing | Pre-process with consent |
| Audit logging | Additional I/O | Async log shipping |

---

## SRE Practices

### Error Budgets

```
Error Budget = 1 - SLO
Example: 99.9% SLO = 0.1% error budget (43.2 min downtime/month)
```

### Burn Rate

```
Burn Rate = Actual Error Rate / Allowed Error Rate
Example: 2% actual / 0.1% allowed = 20x burn rate
```

### Alerting on Burn Rate

- High burn rate triggers immediate action
- Fast burn: 14.4x (outage in 3 days)
- Slow burn: 6x (outage in 14 days)

### SLO Tiers

| Tier | SLO | Error Budget | Burn Rate Alert |
|------|-----|--------------|-----------------|
| Tier 1 | 99.9% | 43.2 min/month | > 6x |
| Tier 2 | 99.5% | 3.6 hours/month | > 12x |
| Tier 3 | 99.0% | 7.2 hours/month | > 24x |

---

## Performance Debt Management

### Identifying Technical Debt

- Latency > SLO on critical paths
- Cache hit rate < target
- Unbounded resource growth
- Missing timeouts or retries
- No observability

### Debt Prioritization

| Debt Item | Impact | Effort | Priority |
|-----------|--------|--------|----------|
| Missing timeouts | High | Low | P0 |
| No caching | High | Medium | P0 |
| Unbounded memory | High | Low | P0 |
| No monitoring | High | Medium | P0 |
| Suboptimal queries | Medium | Medium | P1 |

### Debt Reduction Sprint

1. **Week 1**: Critical items (P0)
2. **Week 2**: High impact items
3. **Week 3**: Medium impact items
4. **Week 4**: Refactoring and cleanup

---

## Capacity Testing

### Load Test Scenarios

1. **Baseline**: Single user, measure baseline latency
2. **Normal Load**: Expected peak traffic
3. **Peak Load**: 150% of expected peak
4. **Stress Test**: Find breaking point
5. **Soak Test**: 24-48 hour sustained load
6. **Spike Test**: Sudden traffic increase

### Success Criteria

- [ ] p95 latency within SLO at all load levels
- [ ] p99 latency within 2x SLO
- [ ] Error rate < 0.1% at peak
- [ ] No memory leaks in 24h soak
- [ ] Graceful degradation under stress

### Load Test Automation

```python
class LoadTestRunner:
    def __init__(self, target_rps: int, duration: int):
        self.target_rps = target_rps
        self.duration = duration
        self.completed = 0
        self.failed = 0
    
    async def run(self, test_fn):
        start = time.time()
        while time.time() - start < self.duration:
            tasks = [test_fn() for _ in range(self.target_rps)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            self.completed += sum(1 for r in results if not isinstance(r, Exception))
            self.failed += sum(1 for r in results if isinstance(r, Exception))
            await asyncio.sleep(1)
    
    def report(self):
        total = self.completed + self.failed
        print(f"Completed: {self.completed}/{total}")
        print(f"Failed: {self.failed}")
        print(f"Error rate: {self.failed / total * 100:.2f}%")
```

---

## Continuous Optimization

### Weekly Review

- Review latency trends
- Check cache hit rates
- Audit cost per request
- Identify new bottlenecks

### Monthly Review

- Full performance audit
- Update performance budgets
- Review model routing effectiveness
- Plan optimization sprints

### Quarterly Review

- Capacity planning
- Infrastructure review
- Technology evaluation
- Team training

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
