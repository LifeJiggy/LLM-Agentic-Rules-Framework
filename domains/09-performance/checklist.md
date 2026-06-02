# Performance Domain - Checklist

> Release and review checklist for latency, throughput, cost, and resource efficiency in LLM and agentic systems.

## Overview

Performance checks for AI systems must cover more than application CPU and database queries. Teams also need to inspect prompt size, model latency, retrieval quality, tool-call fanout, streaming behavior, queue depth, token cost, cache hit rate, and degradation behavior.

## Priority Guide

- P0: Required when performance failure can cause outages, unsafe retries, or excessive cost.
- P1: Required for user-facing latency and capacity targets unless explicitly accepted.
- P2: Recommended for cost control and resource efficiency.
- P3: Useful refinement for optimization maturity.

## Measurement

- [ ] Key user journeys have latency targets.
- [ ] P50, P95, and P99 latency are measured separately.
- [ ] Model latency is separated from application, retrieval, and tool latency.
- [ ] Token counts are tracked for prompts and completions.
- [ ] Cost per request is measured for high-volume workflows.
- [ ] Evaluation and batch jobs are measured separately from interactive traffic.

## Prompt And Context Efficiency

- [ ] System prompts are deduplicated.
- [ ] Conversation history is pruned, summarized, or windowed.
- [ ] Retrieval results have a token budget.
- [ ] Large documents are chunked and ranked before model calls.
- [ ] Prompt templates avoid unused instructions and verbose boilerplate.
- [ ] Long-context requests have explicit justification.

## Model And Inference

- [ ] Model choice matches the task complexity.
- [ ] Small or fast models are used for classification, routing, and extraction where appropriate.
- [ ] Streaming is enabled for long user-facing responses when useful.
- [ ] Timeouts are set for each model call.
- [ ] Retries use exponential backoff with jitter.
- [ ] Fallback behavior exists for provider latency or outage.

## Retrieval And Data Access

- [ ] Retrieval latency is measured independently.
- [ ] Embedding and vector search parameters are tuned.
- [ ] Database queries have appropriate indexes.
- [ ] N+1 API or database calls are avoided.
- [ ] Cacheable reference data is cached with invalidation rules.
- [ ] Slow retrieval results are visible in traces.

## Agent And Tool Execution

- [ ] Maximum agent loop iterations are enforced.
- [ ] Tool-call fanout is bounded.
- [ ] Parallel tool calls are used only where safe.
- [ ] Irreversible tool calls are not retried blindly.
- [ ] Tool latency and error rates are monitored.
- [ ] Long-running tools are queued or made asynchronous.

## Caching

- [ ] Cache candidates are identified by stability and risk.
- [ ] Cache keys include relevant model, prompt, policy, and retrieval versions.
- [ ] Sensitive data is not cached in unsafe locations.
- [ ] Cache hit rate is monitored.
- [ ] Cache invalidation rules are documented.
- [ ] Stale-cache behavior is tested.

## Load And Capacity

- [ ] Expected peak traffic is documented.
- [ ] Load tests cover realistic prompt and tool patterns.
- [ ] Rate limits are understood for model and external tool providers.
- [ ] Batch workloads cannot starve interactive requests.
- [ ] Queue depth and worker saturation are monitored.
- [ ] Autoscaling signals reflect real bottlenecks.

## Release Decision

- [ ] Performance regression tests pass.
- [ ] New latency or cost risks are documented.
- [ ] Dashboards and alerts are updated.
- [ ] Rollback plan exists for performance regressions.
- [ ] Accepted performance exceptions have owners and expiration dates.

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Troubleshooting](./troubleshooting.md)
- [Operations Checklist](../06-operations/checklist.md)
