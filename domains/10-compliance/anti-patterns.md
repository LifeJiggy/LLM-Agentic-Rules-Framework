# Compliance Domain - Anti-Patterns

> Common compliance failures in LLM and agentic systems, with safer alternatives.

## Overview

These anti-patterns describe governance failures that make AI systems hard to audit, unsafe to operate, or difficult to defend during review. Use them during design reviews and incident retrospectives.

## Shipping Without A Stated Purpose

**Problem:** The system is deployed before its intended use and prohibited use are documented.

**Why it fails:** Reviewers cannot judge whether data, tools, and outputs are appropriate.

**Better approach:** Write a short system purpose, approved user group, risk tier, and prohibited-use list before production access.

## Logging Everything Forever

**Problem:** Prompts, completions, files, and tool traces are retained indefinitely.

**Why it fails:** AI logs can contain personal data, secrets, customer records, and sensitive business information.

**Better approach:** Apply data minimization, redaction, access controls, and retention schedules to AI traces.

## Treating Prompts As Informal Notes

**Problem:** Critical policy behavior exists only inside prompts and changes without review.

**Why it fails:** Prompt changes can materially alter system behavior without code review or audit evidence.

**Better approach:** Version prompts, review high-risk changes, and connect prompts to tests or evaluations.

## No Human Escalation Path

**Problem:** The system handles contested or high-impact outcomes without a clear human review route.

**Why it fails:** Users and operators cannot correct errors, appeal decisions, or stop harmful automation.

**Better approach:** Define escalation triggers, reviewer responsibilities, and override logging.

## Vendor Assumptions Without Evidence

**Problem:** Teams assume a model provider's default settings satisfy privacy, retention, residency, and training requirements.

**Why it fails:** Defaults vary across providers, products, regions, and account configurations.

**Better approach:** Record vendor settings, data processing terms, and approved model configurations.

## Evaluating Only Happy Paths

**Problem:** Compliance review uses normal examples but skips abuse, edge cases, protected classes, and refusal behavior.

**Why it fails:** Real-world risk appears in adversarial and ambiguous cases.

**Better approach:** Include red-team prompts, sensitive-data cases, bias probes, and tool-misuse tests.
