# AI Evaluation Plan

## System

- Name:
- Owner:
- Risk tier:
- Evaluation owner:

## Evaluation Scope

- User journeys covered:
- Domains covered:
- Model versions:
- Prompt versions:
- Retrieval sources:
- Tools:

## Test Sets

| Test Set | Purpose | Required For |
|----------|---------|--------------|
| Golden paths | Expected normal behavior | All systems |
| Edge cases | Boundary and ambiguous inputs | Medium and high risk |
| Safety cases | Harmful or policy-sensitive inputs | User-facing systems |
| Security cases | Prompt injection and tool misuse | Tool-using systems |
| Privacy cases | Sensitive data handling | Systems processing personal data |
| Regression cases | Previously fixed failures | Production systems |

## Metrics

- Accuracy:
- Refusal quality:
- Grounding quality:
- Tool correctness:
- Latency:
- Cost per request:
- Human review escalation rate:

## Release Thresholds

Define pass/fail criteria and accepted exception handling.

## Evidence Location

Link to evaluation reports, datasets, dashboards, and approvals.
