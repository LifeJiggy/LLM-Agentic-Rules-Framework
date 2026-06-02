# Compliance Domain - Fundamentals

> Foundational compliance concepts for LLM and agentic systems that handle users, data, decisions, regulated workflows, or externally visible outputs.

## Overview

Compliance for AI systems is the practice of proving that the system operates within legal, contractual, ethical, and organizational requirements. For LLM and agentic systems, compliance must cover both traditional software controls and model-specific risks such as opaque reasoning, generated content, tool use, data leakage, autonomy, and evaluation drift.

## Core Principles

### Accountability

Every production AI workflow needs a named owner, a documented purpose, and a decision path for approving high-risk behavior.

- Assign ownership for each model, agent, tool, and data source.
- Define who can approve deployments and policy exceptions.
- Keep a review trail for material changes.

### Lawful and Fair Processing

Collect, process, and retain data only when there is a valid business and legal basis.

- Document the purpose for each data category.
- Minimize personal and sensitive data.
- Avoid using production user data in prompts, logs, or evaluations unless approved.

### Transparency

Users and operators should understand when AI is involved and what the system can and cannot do.

- Disclose AI assistance where required.
- Document known limitations.
- Provide escalation paths for contested outcomes.

### Human Oversight

Use human review for workflows that can materially affect rights, safety, finances, employment, healthcare, legal status, or access to critical services.

- Define review thresholds.
- Preserve context needed for review.
- Make overrides auditable.

## Compliance Scope

| Area | What To Document |
|------|------------------|
| System purpose | Intended use, prohibited use, target users |
| Data processing | Sources, retention, consent or legal basis |
| Model behavior | Capabilities, limitations, evaluation results |
| Tool access | Permissions, side effects, approval requirements |
| Human oversight | Review points, escalation paths, override rules |
| Audit trail | Logs, approvals, incidents, model/version changes |

## Risk Tiers

| Tier | Description | Minimum Control |
|------|-------------|-----------------|
| Low | Internal productivity or low-impact assistance | Basic logging and documented owner |
| Medium | Customer-facing guidance or workflow automation | Evaluation, monitoring, privacy review |
| High | Decisions with financial, legal, safety, or rights impact | Human review, formal risk assessment, audit trail |
| Prohibited | Uses banned by law, policy, or contract | Block at design and access-control layers |

## Related Rules

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)
