# Compliance Domain - Best Practices

> Recommended practices for making LLM and agentic systems reviewable, governable, and audit-ready.

## Overview

Use these practices when designing, releasing, or reviewing AI systems that require governance evidence. They focus on ownership, approvals, data minimization, human oversight, and change control.

## Build A Compliance Register

Maintain a lightweight register for each AI system.

| Field | Description |
|-------|-------------|
| System name | Human-readable service or agent name |
| Owner | Responsible person or team |
| Purpose | Approved intended use |
| Users | Internal users, customers, or third parties |
| Data classes | Public, internal, confidential, personal, sensitive |
| Models | Provider, model name, version or release channel |
| Tools | External systems the agent can call |
| Risk tier | Low, medium, high, or prohibited |
| Review cadence | Monthly, quarterly, or release-based |

## Use Policy Gates

Add explicit gates before production release:

- privacy review for personal or sensitive data;
- security review for tool use or external integrations;
- legal review for regulated or high-impact workflows;
- evaluation review for harmful, biased, or misleading outputs;
- operations review for logging, monitoring, and incident response.

## Keep Auditable Evidence

Store evidence in locations that survive personnel changes.

- Architecture decision records.
- Model and prompt change logs.
- Evaluation reports.
- Red-team findings and remediation notes.
- User-impact assessments.
- Incident reports and corrective actions.

## Minimize Data Exposure

Treat prompts, completions, traces, embeddings, screenshots, files, and tool outputs as possible regulated records.

- Redact secrets and sensitive data before logging.
- Apply retention limits to AI traces.
- Separate production data from evaluation data.
- Restrict access to logs and replay tools.

## Document Human Review

For high-impact systems, document when human review is required.

- Before irreversible tool execution.
- Before sending regulated advice.
- Before changing customer status, access, pricing, eligibility, or benefits.
- After confidence drops below the approved threshold.

## Verify Vendor And Model Changes

Do not treat model upgrades as invisible infrastructure changes.

- Re-run regression evaluations.
- Review updated provider terms.
- Check data retention and training settings.
- Record the change in the system register.
