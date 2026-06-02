# Operations Domain - Troubleshooting

> Common operational issues for LLM and agentic systems, with diagnosis and remediation steps.

## Overview

LLM systems fail differently from conventional services because they depend on model providers, token budgets, prompt behavior, tool availability, retrieval quality, and user input distribution. Operational troubleshooting should separate infrastructure failures from model behavior failures so teams can choose the right fix quickly.

## Latency Spikes

**Symptoms:**

- P95 or P99 response time increases.
- Requests spend more time waiting on model or retrieval calls.
- User-facing agents time out during multi-step tasks.

**Likely causes:**

- Model provider latency or rate limiting.
- Larger prompts after context growth.
- Slow retrieval, database, or tool calls.
- Agent loops performing too many iterations.

**Resolution:**

1. Break down latency by model call, retrieval, tool call, and application processing.
2. Check prompt token counts and conversation history size.
3. Add or tune timeouts for each external dependency.
4. Cap agent loop iterations and tool retries.
5. Add fallback responses for degraded dependencies.

## Rate Limits And Quota Exhaustion

**Symptoms:**

- Model API returns rate-limit or quota errors.
- Batch jobs block interactive traffic.
- Retries increase load instead of recovering service.

**Likely causes:**

- No request shaping across workloads.
- Retry policy lacks jitter or backoff.
- Token-heavy requests consume quota faster than expected.

**Resolution:**

1. Separate quotas for interactive, batch, and evaluation workloads.
2. Use exponential backoff with jitter.
3. Queue non-urgent work.
4. Add token budgeting before model calls.
5. Alert before quota exhaustion, not only after failure.

## Tool Failures

**Symptoms:**

- Agent plans correctly but cannot complete actions.
- Tool calls fail with authorization, timeout, or schema errors.
- The agent retries unsafe or impossible actions.

**Likely causes:**

- Tool credentials changed or expired.
- Tool schema no longer matches implementation.
- The agent lacks clear failure handling instructions.
- External service is degraded.

**Resolution:**

1. Confirm tool health outside the agent.
2. Validate tool schemas against real requests.
3. Rotate or repair credentials.
4. Return structured tool errors to the agent.
5. Block repeated unsafe retries with retry limits and escalation.

## Context Window Overflow

**Symptoms:**

- Model requests fail due to token limits.
- Important instructions disappear from context.
- Responses become inconsistent in long sessions.

**Likely causes:**

- Conversation history is appended without pruning.
- Retrieval returns too many chunks.
- Prompts include duplicated instructions.

**Resolution:**

1. Measure tokens per request.
2. Keep system and policy instructions pinned.
3. Summarize or prune old conversation turns.
4. Limit retrieval results by relevance and token budget.
5. Add tests for long-session behavior.

## Output Quality Regression

**Symptoms:**

- The system still runs but responses become less accurate or less aligned.
- Users report more escalations or corrections.
- Evaluation pass rate drops after a release.

**Likely causes:**

- Prompt, retrieval, model, or tool changes affected behavior.
- Evaluation coverage missed a workflow.
- Production input distribution shifted.

**Resolution:**

1. Compare recent prompt, model, retrieval, and tool changes.
2. Re-run regression evaluations.
3. Sample production traces with privacy controls.
4. Roll back the smallest behavior-changing component if needed.
5. Add new failing cases to the evaluation suite.

## Incident Review Checklist

- [ ] User impact and timeline documented.
- [ ] Failing dependency or behavior identified.
- [ ] Prompt, model, retrieval, and tool versions recorded.
- [ ] Logs reviewed with sensitive data controls.
- [ ] Immediate mitigation applied.
- [ ] Permanent fix assigned.
- [ ] Related checklist or troubleshooting guidance updated.

## Related Rules

- [Operations Fundamentals](./fundamentals.md)
- [Operations Best Practices](./best-practices.md)
- [Operations Checklist](./checklist.md)
- [Testing Checklist](../07-testing/checklist.md)
- [Performance Troubleshooting](../09-performance/troubleshooting.md)
