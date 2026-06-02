# Domain Knowledge Map

This map clarifies the expertise each domain is expected to contain and where teams should look for cross-domain concerns.

| Domain | Core Expertise | Adjacent Domains | Evidence To Maintain |
|--------|----------------|------------------|----------------------|
| Core | Agent architecture, context, tools, state, error handling | Security, Testing, Operations | Architecture notes, agent design records |
| Security | Prompt injection, secrets, access control, tool abuse, data exposure | Data, Integration, Compliance | Threat model, security review, access review |
| Development | Code quality, maintainability, review process, dependency hygiene | Testing, Documentation, Operations | PR review, coding standards, dependency audit |
| Data | Data classification, retention, retrieval, storage, governance | Security, Compliance, Performance | Data inventory, retention policy, retrieval evaluation |
| Integration | API contracts, tool schemas, webhooks, retries, idempotency | Security, Operations, Testing | Tool registry, integration tests, API contracts |
| Operations | Deployment, monitoring, incident response, rollback, reliability | Performance, Security, Documentation | Runbooks, dashboards, incident reports |
| Testing | Behavior tests, evals, regression, red-team cases, E2E workflows | Security, Data, Compliance | Evaluation reports, test datasets, regression records |
| Documentation | User docs, API docs, runbooks, ADRs, knowledge management | Operations, Compliance, Development | Published docs, ADRs, changelog |
| Performance | Latency, throughput, cost, caching, capacity | Operations, Data, Integration | Benchmarks, traces, capacity plans |
| Compliance | Governance, audit evidence, risk tiering, human oversight | Security, Data, Documentation | System register, approvals, evidence pack |

## Cross-Domain Review Rules

- Security and Data should both review systems that process personal or sensitive data.
- Integration and Security should both review tools that can write, send, delete, buy, approve, or change status.
- Testing and Compliance should both review high-impact workflows.
- Operations and Performance should both review high-volume or user-facing systems.
- Documentation and Operations should both review incident runbooks and release procedures.

## Domain Owner Responsibilities

Domain owners should:

- keep terminology aligned with the glossary;
- update examples when production patterns change;
- add anti-patterns after incidents or repeated review failures;
- keep checklist items actionable;
- ensure related domain links stay valid.
