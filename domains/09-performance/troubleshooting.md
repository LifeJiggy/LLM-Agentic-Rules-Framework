# Performance Domain - Troubleshooting

> Common performance issues in LLM and agentic systems, with diagnosis and remediation steps.

## Overview

When an AI system is slow or expensive, the bottleneck may be the model, prompt size, retrieval, database access, external tools, queueing, retries, or agent loop design. Troubleshooting should isolate each stage before changing architecture.

## Slow End-To-End Responses

**Symptoms:**

- User-facing responses exceed latency targets.
- P95 or P99 latency increases while average latency appears acceptable.
- Long tasks time out before the agent finishes.

**Likely causes:**

- Prompt context has grown over time.
- Retrieval or tool calls are serialized unnecessarily.
- Model provider latency changed.
- Agent loop iterations are unbounded.

**Resolution:**

1. Break traces into application, retrieval, model, and tool segments.
2. Compare prompt and completion token counts against previous releases.
3. Cap agent loop iterations and tool retries.
4. Parallelize independent read-only tool calls where safe.
5. Add streaming or partial progress updates for long responses.

## Token Cost Spikes

**Symptoms:**

- Cost per request increases.
- High-volume workflows consume budget faster than expected.
- Batch jobs cause unexpected provider charges.

**Likely causes:**

- More retrieved chunks are inserted into prompts.
- Conversation history is not summarized or pruned.
- A larger model is used for simple routing or extraction.
- Retries repeat expensive prompts.

**Resolution:**

1. Track prompt tokens, completion tokens, and retry counts.
2. Set token budgets per workflow.
3. Move simple tasks to smaller models where quality allows.
4. Cache stable intermediate results.
5. Stop retrying deterministic validation failures.

## Retrieval Latency

**Symptoms:**

- Model calls are fast, but total response time is slow.
- Vector search or database queries dominate traces.
- Retrieval returns too many weakly relevant chunks.

**Likely causes:**

- Missing database indexes.
- Poor chunking strategy.
- Search parameters are too broad.
- Reranking is expensive or applied too often.

**Resolution:**

1. Profile vector search, metadata filters, and reranking separately.
2. Add indexes for common metadata filters.
3. Reduce top-k before reranking.
4. Cache frequent retrieval results when data freshness allows.
5. Revisit chunk size and overlap.

## Tool Bottlenecks

**Symptoms:**

- Agent reasoning is quick, but external actions are slow.
- Tool calls queue or time out under load.
- Retried tool calls amplify downstream load.

**Likely causes:**

- External API rate limits.
- Serial calls that could be batched.
- Missing timeout boundaries.
- Unbounded retries during downstream degradation.

**Resolution:**

1. Add per-tool latency and error metrics.
2. Batch or coalesce repeated reads.
3. Use backoff with jitter.
4. Queue long-running work.
5. Add circuit breakers for degraded dependencies.

## Cache Regressions

**Symptoms:**

- Latency increases after a release that changed prompts, models, or retrieval.
- Cache hit rate drops sharply.
- Users receive stale or inconsistent responses.

**Likely causes:**

- Cache keys changed unintentionally.
- Cache invalidation rules are incomplete.
- Policy or prompt versions are missing from cache keys.
- Sensitive or user-specific data is cached too broadly.

**Resolution:**

1. Compare cache hit rate before and after release.
2. Inspect cache key components.
3. Include model, prompt, policy, and retrieval versions where relevant.
4. Add tests for stale and cross-user cache behavior.
5. Purge unsafe cache entries immediately.

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Operations Troubleshooting](../06-operations/troubleshooting.md)
