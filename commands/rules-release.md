# /rules-release

Run a release readiness review using the framework.

## Prompt

Review the current change as a release candidate. Use the release checklist, model/prompt change review template, evaluation plan, operations checklist, and compliance checklist where applicable.

Return:

- release decision: pass, conditional pass, or block;
- blocking P0/P1 gaps;
- required tests and evidence;
- rollback or disablement plan;
- owner for each unresolved item.
- reliability verdict for failure handling, retries, timeouts, observability, rollback, and operator recovery.

## Release Decision Rules

- `block`: any unresolved P0 item or missing high-risk human oversight.
- `conditional pass`: unresolved P1 item with owner, due date, and accepted risk.
- `pass`: required controls, tests, evidence, monitoring, and rollback are present.

## Reliability Gate

- Block release when a known high-impact failure mode has no containment or rollback path.
- Require explicit timeout, retry, and fallback behavior for external tools and model calls.
- Require observable error signals for production workflows.
- Require a manual recovery path when automation can leave partial state.
