# Reliability Checklist

Use this checklist for code, adapters, rules, validators, plugins, and agentic workflows.

## Error Handling

- [ ] Input paths, config values, and target names are validated before side effects.
- [ ] Missing files and unreadable files produce actionable errors.
- [ ] Invalid JSON, YAML, Markdown, or manifest data fails early.
- [ ] Errors preserve enough context to identify the failing file, target, or operation.
- [ ] Expected errors do not hide unexpected exceptions.

## Runtime Reliability

- [ ] External calls define timeout behavior.
- [ ] Retries are bounded and do not multiply side effects.
- [ ] Fallback behavior is explicit and tested.
- [ ] Partial work is skipped, resumed, or rolled back safely.
- [ ] Final summaries include success, skip, warning, and failure counts.

## Safe Writes

- [ ] Writes avoid replacing directories or symlink targets unexpectedly.
- [ ] Existing files are backed up or versioned before overwrite.
- [ ] Changed files are written atomically where practical.
- [ ] Output paths reject unsafe destinations.
- [ ] Dry-run and apply modes report consistent planned operations.

## Release Readiness

- [ ] P0 failures block release.
- [ ] P1 failures require owner, due date, and accepted risk.
- [ ] Monitoring or logs expose the failure modes users care about.
- [ ] Rollback or disablement steps are documented.
- [ ] Verification commands have been run after the hardening change.

