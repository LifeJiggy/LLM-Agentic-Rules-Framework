# Production Assistant Example

This example shows how a team can apply the framework to a user-facing support assistant.

## Scenario

The assistant drafts support replies from approved help-center articles and order metadata. A support agent reviews each reply before it is sent to the customer.

## Domain Pack

Use the Production User-Facing Assistant pack from `docs/checklist-packs.md`.

Required domains:

- Core
- Security
- Data
- Testing
- Operations
- Performance
- Compliance

## Controls

| Control | Implementation |
|---------|----------------|
| Retrieval grounding | Only approved help-center articles are retrieved. |
| Human oversight | Drafts require agent approval before sending. |
| Tool access | The assistant can read order status but cannot issue refunds. |
| Logging | Prompts and completions are retained for 30 days with redaction. |
| Evaluation | Regression set includes normal, ambiguous, sensitive, and policy cases. |
| Incident response | Unsafe draft reports disable the assistant workflow until review. |

## Release Evidence

- `assets/templates/ai-system-register.yml`
- `assets/templates/evaluation-plan.md`
- `assets/templates/release-checklist.md`
- `assets/templates/compliance-review.md`
- `assets/templates/incident-runbook.md`

## Example Review Questions

- Does the assistant ever answer outside approved sources?
- Are sensitive customer fields redacted from traces?
- Can the assistant perform irreversible actions?
- Are model and prompt versions recorded for each release?
- Are failing evaluation cases added to the regression set?
