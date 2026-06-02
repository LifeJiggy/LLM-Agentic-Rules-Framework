---
name: system
description: Apply system-level hardening, reliability, and error-handling checks for LLM, agentic, adapter, CLI, IDE, plugin, validation, and release workflows. Use when work involves failure modes, retries, timeouts, rollback, observability, safe writes, install safety, or production readiness.
---

# System Reliability Hardening

Use this skill when a change can fail at runtime, during install, during validation, or during agentic execution.

## Workflow

1. Identify the user-facing or operator-facing failure modes.
2. Classify each failure as blocking, recoverable, degraded, or informational.
3. Check timeout, retry, cancellation, and fallback behavior.
4. Check that partial writes, partial installs, and partial state transitions are recoverable.
5. Confirm errors are observable through logs, summaries, reports, or release evidence.
6. Require rollback or disablement steps for production-impacting changes.

## Required References

- Read `reliability-checklist.md` before reviewing implementation or release readiness.
- Read `recovery-playbook.md` when the task involves install, migration, rollout, rollback, or partial failure.

## Default Output

When asked to harden a system, return:

1. Critical failure modes.
2. Missing error handling.
3. Reliability improvements made or recommended.
4. Verification commands and results.
5. Remaining risk, if any.

