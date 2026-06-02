# Advanced Usage

Use this guide when applying the framework across multiple teams, services, or regulated workflows.

## Domain Mapping

Create a domain map for each AI system.

| Question | Domain |
|----------|--------|
| What is the agent allowed to do? | Core, Integration, Security |
| What data can it see? | Data, Security, Compliance |
| How do we know it works? | Testing, Performance |
| How do we operate it? | Operations, Documentation |
| How do we prove it is controlled? | Compliance, Security, Documentation |

## Risk-Based Adoption

### Low Risk

- Internal-only usage.
- No sensitive data.
- No autonomous write actions.
- Basic owner, purpose, and logging are enough.

### Medium Risk

- Customer-facing content.
- Retrieval over business data.
- Tool use with reversible actions.
- Requires evaluation, monitoring, and privacy review.

### High Risk

- Financial, legal, safety, employment, healthcare, eligibility, or access impact.
- Requires human oversight, formal risk assessment, auditable evidence, and incident playbooks.

## Operating Model

For larger organizations, assign owners:

| Role | Responsibility |
|------|----------------|
| Domain owner | Maintains a domain's rule files |
| System owner | Applies rules to a specific AI system |
| Reviewer | Checks releases against selected checklists |
| Compliance owner | Maintains governance evidence |
| Platform owner | Automates validation and reporting |

## Change Management

Treat these as behavior-changing releases:

- model upgrades;
- prompt changes;
- retrieval source changes;
- embedding model changes;
- tool permission changes;
- safety policy changes;
- evaluation threshold changes.

Each release should record what changed, what was tested, what risks remain, and who approved it.

## Evidence Pack

A strong production evidence pack contains:

- AI system register;
- data inventory;
- model and prompt change log;
- evaluation report;
- security review;
- privacy review;
- compliance review;
- incident response plan;
- rollback plan.
