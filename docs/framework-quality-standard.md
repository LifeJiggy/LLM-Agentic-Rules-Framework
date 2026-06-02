# Framework Quality Standard

This standard defines what each framework feature must mean in practice. It converts the README promises into reviewable requirements.

## 1. Standardized Guidelines

Every rule file should use consistent language, priority handling, and evidence expectations.

Minimum standard:

- Each file has a clear title and `Overview`.
- Rules use direct, actionable language.
- P0-P3 priority guidance is present where release or review decisions are made.
- Related files are linked where the topic crosses domains.
- Examples avoid stack-specific assumptions unless the file names the stack.

Review questions:

- Can two teams apply this guidance the same way?
- Does the rule say what to do, why it matters, and how to prove it?
- Is the priority level clear enough for release decisions?

## 2. Domain-Specific Knowledge

Each domain must contain guidance that is specific to its functional area, not generic software advice.

Minimum standard:

- `fundamentals.md` defines the domain's AI-specific concepts.
- `best-practices.md` describes recommended production patterns.
- `anti-patterns.md` names common failures and safer alternatives.
- `checklist.md` supports release, review, or audit use.
- `examples.md` includes practical implementation patterns.
- `troubleshooting.md` supports diagnosis and remediation.
- `advanced.md` covers scale, tradeoffs, or expert-level decisions.

Review questions:

- Would a domain expert recognize this as useful?
- Does it address LLM, agentic, tool, data, or model-specific concerns?
- Does it link to adjacent domains when responsibilities overlap?

## 3. Actionable Checklists

Checklists should be ready to use in PRs, release gates, audits, and incident reviews.

Minimum standard:

- Checklist items begin with a concrete action or verification.
- Items are grouped by workflow stage or control area.
- P0/P1 items are identifiable through priority guidance.
- The checklist avoids vague items such as "performance is good" or "security considered."
- Evidence expectations are clear for high-risk items.

Review questions:

- Can a reviewer mark each item pass/fail?
- Is the owner of the action obvious?
- Does the checklist support both new and existing systems?

## 4. Real-World Examples

Examples should reflect realistic production implementation patterns.

Minimum standard:

- Examples show inputs, outputs, configuration, or review artifacts where possible.
- Examples include failure handling when relevant.
- Examples avoid placeholder-only snippets unless they are templates.
- Security, privacy, and operational risks are not hidden for simplicity.

Review questions:

- Could a team adapt this example without inventing the missing control path?
- Does it show realistic errors, approvals, or monitoring?
- Does it avoid unsafe copy-paste behavior?

## 5. Continuous Evolution

The framework must improve as practices, models, providers, regulations, and incident lessons change.

Minimum standard:

- Changes update `CHANGELOG.md`.
- Roadmap items describe user-facing value.
- Incident or audit lessons produce checklist, troubleshooting, or anti-pattern updates.
- Major structural changes update validators and docs.
- New templates are added to validation when they become part of the supported contract.

Review questions:

- Is there a durable record of why the framework changed?
- Does the change improve adoption, quality, safety, or governance?
- Did validation cover the new expectation?
