---
name: llm-agentic-rules
description: Apply the LLM & Agentic Rules Framework to coding-agent work. Use when reviewing, building, testing, documenting, deploying, or governing LLM apps, agentic systems, AI tools, RAG, MCP integrations, model changes, prompt changes, or coding-agent workflows.
---

# LLM & Agentic Rules

Use this skill to apply the repository's 10-domain framework inside agentic coding assistants.

## Operating Model

1. Identify the system type and risk tier.
2. Select the relevant domain checklist pack.
3. Read the matching domain files before proposing or editing code.
4. Apply P0/P1 rules before release.
5. Record evidence using the templates in `assets/templates/`.
6. Update docs, tests, and changelog when the change affects behavior.

## Domain Routing

| User Task | Load These Domains |
|-----------|--------------------|
| New AI app or agent | Core, Security, Data, Testing, Operations, Compliance |
| Tool or MCP integration | Core, Integration, Security, Operations, Testing |
| RAG or knowledge system | Core, Data, Security, Testing, Performance |
| Production release | Operations, Testing, Security, Compliance, Performance |
| Code review | Development, Security, Testing, Documentation |
| Incident or regression | Operations, Troubleshooting, Testing, Performance |
| Regulated workflow | Compliance, Data, Security, Documentation, Testing |

## Required Review Gates

- P0 items block production unless there is a documented exception.
- P1 items require explicit acceptance if not completed.
- Model, prompt, retrieval, and tool changes count as behavior changes.
- Human oversight is required for high-impact workflows.
- Sensitive data in prompts, traces, or logs requires privacy and security review.
- Reliability reviews must include error paths, rollback, observability, and operator recovery steps.
- Agentic tool changes must define expected failure modes before implementation is accepted.

## Response Format

When asked to audit, plan, or release-gate a project, respond with:

1. System type and assumed risk tier.
2. Selected framework domains.
3. P0/P1 findings or controls.
4. Required tests and evidence.
5. Release decision or next action.

If evidence is missing, state exactly what evidence is missing instead of assuming compliance.

## Cross-Agent Portability Rules

- Avoid tool-specific commands unless the user names a target tool.
- Prefer repository-relative file references.
- Keep generated prompts usable in CLI and IDE assistants.
- Do not require network access to apply the framework.
- Treat adapters as instruction packs unless a target has a native plugin format.

## Useful Repository Files

- `docs/domain-index.md`
- `docs/checklist-packs.md`
- `docs/risk-tiering.md`
- `docs/framework-quality-standard.md`
- `assets/templates/release-checklist.md`
- `assets/templates/model-prompt-change-review.md`
- `assets/templates/evaluation-plan.md`
- `scripts/check_rules.py`

## Default Agent Behavior

When using this skill:

- Read the relevant local domain files before making recommendations.
- Prefer checklist-backed decisions over generic advice.
- Surface missing tests, missing evidence, and missing ownership.
- Surface missing error handling, timeout handling, retry limits, and rollback plans.
- Keep recommendations scoped to the user's system type and risk tier.
- Do not invent compliance status; state evidence gaps clearly.
