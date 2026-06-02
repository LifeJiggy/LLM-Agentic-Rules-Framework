# Compliance Domain - Advanced

> Advanced compliance patterns for complex, high-impact, or multi-jurisdiction LLM and agentic systems.

## Overview

Advanced compliance work focuses on mapping controls to evidence, managing model risk, supporting jurisdiction-specific requirements, and governing autonomous tool use over time.

## Control Mapping

Map each AI control to the policies, contracts, and regulations it supports. This avoids duplicating work across audits.

| Control | Evidence | Example Requirement |
|---------|----------|---------------------|
| Data minimization | Data inventory, prompt redaction tests | Privacy and confidentiality |
| Human oversight | Approval logs, reviewer workflow | High-impact decision governance |
| Model evaluation | Regression reports, red-team results | Safety and quality assurance |
| Access control | IAM policy, permission review | Least privilege |
| Incident response | Runbook, post-incident report | Operational resilience |

## Model Risk Management

For high-impact systems, maintain a model risk file.

- Approved use cases.
- Known limitations.
- Evaluation scope and gaps.
- Monitoring plan.
- Fallback or rollback plan.
- Material-change criteria.
- Residual risks and accepted exceptions.

## Jurisdiction-Aware Deployment

Different regions can require different data handling, disclosure, retention, and review controls.

Recommended pattern:

1. Classify users and data by jurisdiction.
2. Keep policy decisions outside prompts where possible.
3. Use configuration-driven controls for retention, routing, and disclosure text.
4. Test jurisdiction-specific behavior in CI or release evaluation.

## Agentic Action Governance

Autonomous systems need stronger controls because they can chain decisions and external actions.

- Separate read tools from write tools.
- Require scoped credentials per tool.
- Add policy checks before each tool call.
- Log the reason, input, output, and actor for high-impact actions.
- Require human approval for irreversible actions.

## Continuous Compliance

Compliance should be monitored after release.

- Track policy-violation rates.
- Sample production outputs.
- Review user complaints and appeals.
- Re-run evaluations on model, prompt, retrieval, and tool changes.
- Retire systems that no longer have a valid owner or business purpose.
