# Agentic Automation Example

This example shows how to apply the framework to an internal agent that triages engineering tickets.

## Scenario

The agent reads new bug reports, classifies severity, searches internal docs, suggests owners, and drafts a triage summary. It cannot close tickets or change priority without human approval.

## Domain Pack

Use the Internal Agentic Automation pack from `docs/checklist-packs.md`.

Required domains:

- Core
- Development
- Integration
- Security
- Operations
- Testing

## Controls

| Control | Implementation |
|---------|----------------|
| Tool permissions | Read-only issue tracker and docs search by default. |
| Human approval | Priority changes require reviewer approval. |
| Retry behavior | Tool retries use backoff and stop after bounded attempts. |
| Evaluation | Test cases cover classification, routing, tool failures, and prompt injection. |
| Observability | Traces include task ID, tool calls, and decision summary. |
| Rollback | Feature flag disables the agent without affecting the issue tracker. |

## Example Review Questions

- Does the agent clearly separate suggestions from actions?
- Are write tools gated behind approval?
- Can malicious ticket text override tool-use instructions?
- Are failed tool calls surfaced to reviewers?
- Is there a fallback path when internal docs search is unavailable?
