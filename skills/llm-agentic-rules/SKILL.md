---
name: llm-agentic-rules
description: Apply the LLM & Agentic Rules Framework to coding-agent work. Use when reviewing, building, testing, documenting, deploying, or governing LLM apps, agentic systems, AI tools, RAG, MCP integrations, model changes, prompt changes, or coding-agent workflows.
---

# LLM & Agentic Rules

Use this skill to apply the repository's 10-domain framework inside agentic coding assistants.

## Operating Model

1. Identify the system type and risk tier.
2. Select the relevant domain checklist pack.
3. Read the matching domain files before proposing or editing code.
4. Apply P0/P1 rules before release.
5. Record evidence using the templates in `assets/templates/`.
6. Update docs, tests, and changelog when the change affects behavior.

### Operating Model Deep Dive

**Step 1: System Identification**
- Determine if the system is an LLM application, agentic system, RAG pipeline, MCP integration, or hybrid.
- Assess the deployment context: internal tool, customer-facing product, regulated workflow, or experimental.
- Identify key stakeholders: end users, operators, compliance teams, security teams.
- Document the system's purpose, data flows, and external dependencies.

**Step 2: Risk Tier Assessment**
- Evaluate potential impact of failures: data loss, security breach, user harm, financial loss, reputation damage.
- Assess reversibility: can changes be rolled back quickly? Is data recoverable?
- Consider blast radius: how many users or systems are affected by a failure?
- Review regulatory requirements: does the system handle PHI, PII, financial data, or other regulated information?
- Assign a risk tier (see `risk-tiering.md`) and document the rationale.

**Step 3: Domain Selection**
- Match the system type and task to the appropriate domain checklist packs.
- Consider both primary domains (directly related to the task) and secondary domains (indirectly affected).
- Load all relevant domain files before making recommendations.
- Note any domain interactions or conflicts.

**Step 4: Rule Application**
- Read the matching domain files in full before proposing changes.
- Apply P0 rules first—these are non-negotiable and must be satisfied.
- Apply P1 rules next—these require explicit acceptance if not completed.
- Document which rules apply and which are satisfied or waived.
- Flag any rules that require human review or approval.

**Step 5: Evidence Collection**
- Use the templates in `assets/templates/` for consistent evidence documentation.
- Collect evidence during development, not just at the end.
- Evidence should be reproducible and verifiable by others.
- Include screenshots, logs, test outputs, and configuration snapshots as appropriate.
- Link evidence to specific rules and checklist items.

**Step 6: Documentation and Changelog**
- Update user-facing documentation for behavior changes.
- Update API documentation for interface changes.
- Update runbooks for operational changes.
- Update the changelog with a clear description of changes, rationale, and migration steps.
- Ensure documentation is accessible to all stakeholders.

## Domain Routing

| User Task | Load These Domains |
|-----------|--------------------|
| New AI app or agent | Core, Security, Data, Testing, Operations, Compliance |
| Tool or MCP integration | Core, Integration, Security, Operations, Testing |
| RAG or knowledge system | Core, Data, Security, Testing, Performance |
| Production release | Operations, Testing, Security, Compliance, Performance |
| Code review | Development, Security, Testing, Documentation |
| Incident or regression | Operations, Troubleshooting, Testing, Performance |
| Regulated workflow | Compliance, Data, Security, Documentation, Testing |

### Domain Routing Deep Dive

**New AI Application**
- Core: Fundamental AI system requirements, model selection, prompt engineering
- Security: Authentication, authorization, input validation, output filtering
- Data: Data sourcing, preprocessing, storage, privacy, retention
- Testing: Unit tests, integration tests, evaluation frameworks, red teaming
- Operations: Deployment, monitoring, scaling, incident response
- Compliance: Regulatory requirements, audit trails, data governance

**Tool or MCP Integration**
- Core: Tool interface design, capability negotiation, error handling
- Integration: API contracts, versioning, backward compatibility, timeout handling
- Security: Tool access controls, sandboxing, input sanitization, audit logging
- Operations: Tool health monitoring, fallback strategies, rate limiting
- Testing: Contract tests, integration tests, failure simulation

**RAG or Knowledge System**
- Core: Retrieval architecture, chunking strategy, embedding selection
- Data: Knowledge base construction, data quality, freshness, indexing
- Security: Data access controls, query filtering, injection prevention
- Testing: Retrieval accuracy, relevance scoring, hallucination detection
- Performance: Query latency, throughput, caching strategies, scalability

**Production Release**
- Operations: Deployment strategy, rollback plan, monitoring, alerting
- Testing: Regression tests, performance tests, chaos tests, canary analysis
- Security: Security review, vulnerability scanning, penetration testing
- Compliance: Regulatory checks, audit evidence, privacy impact assessment
- Performance: Load testing, capacity planning, bottleneck identification

**Code Review**
- Development: Code quality, design patterns, architecture compliance
- Security: Security vulnerabilities, injection risks, access control
- Testing: Test coverage, test quality, edge cases
- Documentation: Code comments, API docs, architecture diagrams

**Incident or Regression**
- Operations: Incident response, root cause analysis, recovery procedures
- Troubleshooting: Debug procedures, log analysis, metric correlation
- Testing: Regression tests, reproduction steps, fix validation
- Performance: Performance impact, resource utilization, scalability

**Regulated Workflow**
- Compliance: Regulatory requirements, audit trails, data governance
- Data: Data classification, retention, deletion, privacy
- Security: Access controls, encryption, audit logging, incident response
- Documentation: Process documentation, training materials, audit evidence
- Testing: Validation tests, compliance checks, acceptance criteria

## Required Review Gates

- P0 items block production unless there is a documented exception.
- P1 items require explicit acceptance if not completed.
- Model, prompt, retrieval, and tool changes count as behavior changes.
- Human oversight is required for high-impact workflows.
- Sensitive data in prompts, traces, or logs requires privacy and security review.
- Reliability reviews must include error paths, rollback, observability, and operator recovery steps.
- Agentic tool changes must define expected failure modes before implementation is accepted.

### Review Gates Deep Dive

**P0 - Critical (Blocks Production)**
- Definition: Issues that could cause system failure, data loss, security breach, or significant user harm.
- Examples:
  - Authentication/authorization bypass
  - Unhandled exceptions in critical paths
  - Data corruption or loss risk
  - Injection vulnerabilities (prompt injection, SQL injection, command injection)
  - Missing rollback capability for production changes
  - No monitoring or alerting for critical workflows
  - PII/PHI exposure in logs or prompts
- Resolution: Must be fixed before production deployment.
- Exception process: Requires CTO/VP Engineering approval, documented risk acceptance, and compensating controls.

**P1 - High (Requires Explicit Acceptance)**
- Definition: Issues that degrade reliability, security, or maintainability but don't block production.
- Examples:
  - Missing retry logic for external calls
  - No circuit breaker for cascading failure protection
  - Incomplete test coverage (< 80% for critical paths)
  - Missing runbook for common failure scenarios
  - No performance baseline established
  - Incomplete error handling in secondary paths
  - Missing timeout configuration
- Resolution: Must be addressed or explicitly accepted by tech lead/architect with documented rationale.
- Acceptance criteria: Risk acknowledged, mitigation plan in place, timeline for resolution defined.

**P2 - Medium (Should Address)**
- Definition: Issues that improve quality but don't significantly impact reliability or security.
- Examples:
  - Code style inconsistencies
  - Missing non-critical tests
  - Documentation gaps for internal tools
  - Minor performance optimizations
  - Refactoring opportunities
- Resolution: Track in backlog, address in next sprint/iteration.

**P3 - Low (Nice to Have)**
- Definition: Cosmetic issues, minor improvements, future enhancements.
- Examples:
  - UI polish
  - Additional logging verbosity
  - Enhanced reporting features
  - Code comments improvements
- Resolution: Address when convenient, no tracking required.

## Response Format

When asked to audit, plan, or release-gate a project, respond with:

1. System type and assumed risk tier.
2. Selected framework domains.
3. P0/P1 findings or controls.
4. Required tests and evidence.
5. Release decision or next action.

If evidence is missing, state exactly what evidence is missing instead of assuming compliance.

### Response Format Templates

**Audit Response Template**
```
## Audit Results

**System Type:** [AI Application / Agentic System / RAG Pipeline / MCP Integration / Hybrid]
**Risk Tier:** [Tier 1 - Critical / Tier 2 - High / Tier 3 - Medium / Tier 4 - Low]
**Assessed By:** [Agent/Engineer name]
**Date:** [YYYY-MM-DD]

### Domains Assessed
1. [Domain 1]: [Status]
2. [Domain 2]: [Status]
...

### P0 Findings (Blocking)
- [Finding 1]: [Description, location, impact, remediation]
- [Finding 2]: ...

### P1 Findings (Requires Acceptance)
- [Finding 1]: [Description, location, impact, accepted/rejected, rationale]
- [Finding 2]: ...

### P2/P3 Findings (Informational)
- [Finding 1]: ...
- [Finding 2]: ...

### Required Tests and Evidence
- [Test/Evidence 1]: [Status - Collected/Missing]
- [Test/Evidence 2]: [Status - Collected/Missing]

### Missing Evidence
- [Evidence item 1]: [Why needed, where to find/create]
- [Evidence item 2]: ...

### Release Decision
[ ] APPROVED - All P0 items resolved, P1 items accepted
[ ] CONDITIONAL - P0 items resolved, P1 items require acceptance before release
[ ] BLOCKED - P0 items remain unresolved
[ ] INSUFFICIENT EVIDENCE - Cannot make determination without additional evidence

### Next Actions
1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]
```

**Plan Response Template**
```
## Implementation Plan

**System Type:** [Description]
**Risk Tier:** [Tier 1-4]
**Proposed Changes:** [Summary]

### Phase 1: Foundation
- [Task 1]: [Description, domain, priority]
- [Task 2]: ...

### Phase 2: Core Implementation
- [Task 1]: ...
- [Task 2]: ...

### Phase 3: Testing and Validation
- [Task 1]: ...
- [Task 2]: ...

### Phase 4: Deployment Preparation
- [Task 1]: ...
- [Task 2]: ...

### Domain Checklist References
- [Domain 1]: [Specific checklist items to verify]
- [Domain 2]: ...

### Evidence to Collect
- [Evidence 1]: [How to collect, when]
- [Evidence 2]: ...

### Risks and Mitigations
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: ...

### Timeline Estimate
- Phase 1: [Duration]
- Phase 2: [Duration]
- Phase 3: [Duration]
- Phase 4: [Duration]
- Total: [Duration]
```

**Release Gate Response Template**
```
## Release Gate Assessment

**Release Candidate:** [Version/Commit]
**System Type:** [Description]
**Risk Tier:** [Tier 1-4]
**Assessment Date:** [YYYY-MM-DD]

### Pre-Release Checklist
- [ ] All P0 items resolved
- [ ] All P1 items accepted with documented rationale
- [ ] Required tests executed and passing
- [ ] Evidence collected and verified
- [ ] Documentation updated
- [ ] Rollback plan tested
- [ ] Monitoring configured
- [ ] Stakeholders notified

### Domain Compliance Summary
| Domain | P0 | P1 | P2 | Status |
|--------|----|----|-----|--------|
| Core   | 0  | 0  | 1   | PASS   |
| Security | 0 | 1  | 0   | CONDITIONAL |
| ...    |    |    |     |        |

### Evidence Summary
- Test results: [Link/Summary]
- Security scan: [Link/Summary]
- Performance benchmark: [Link/Summary]
- Documentation: [Link/Summary]

### Outstanding Items
- [Item 1]: [Owner, due date, impact]
- [Item 2]: ...

### Release Decision
[ ] APPROVED FOR RELEASE
[ ] APPROVED WITH CONDITIONS - [Conditions]
[ ] BLOCKED - [Reasons]

### Post-Release Actions
- [Action 1]: [When, owner]
- [Action 2]: ...
```

## Cross-Agent Portability Rules

- Avoid tool-specific commands unless the user names a target tool.
- Prefer repository-relative file references.
- Keep generated prompts usable in CLI and IDE assistants.
- Do not require network access to apply the framework.
- Treat adapters as instruction packs unless a target has a native plugin format.

### Cross-Agent Portability Deep Dive

**Tool Agnosticism**
- Generate instructions that work across different agent environments (CLI, IDE, web, API).
- Avoid assumptions about available tools or commands.
- When tool-specific commands are necessary, clearly label them and provide alternatives.
- Use abstract descriptions of operations rather than specific tool invocations.

**Repository-Relative References**
- Always use paths relative to the repository root.
- Example: `docs/domain-index.md` instead of `/home/user/project/docs/domain-index.md`.
- Avoid absolute paths unless explicitly required.
- Use forward slashes for cross-platform compatibility.

**CLI and IDE Compatibility**
- Generate prompts that are clear and actionable in text-based interfaces.
- Avoid relying on GUI-specific features or visual cues.
- Structure responses for easy parsing by both humans and machines.
- Use markdown formatting for readability in terminals.

**Offline Operation**
- All framework application should be possible without network access.
- Avoid requiring external API calls for framework enforcement.
- Cache or embed necessary reference materials locally.
- Design workflows that work in air-gapped environments.

**Adapter Design**
- Adapters are instruction packs that translate the framework to specific tools.
- Unless a target has a native plugin format, use instruction-based adapters.
- Adapters should be thin translation layers, not logic-heavy components.
- Adapters should preserve the semantics of the original framework instructions.

## Useful Repository Files

- `docs/domain-index.md`
- `docs/checklist-packs.md`
- `docs/risk-tiering.md`
- `docs/framework-quality-standard.md`
- `assets/templates/release-checklist.md`
- `assets/templates/model-prompt-change-review.md`
- `assets/templates/evaluation-plan.md`
- `scripts/check_rules.py`

### Useful Repository Files Deep Dive

**Core Documentation**
- `docs/domain-index.md`: Overview of all 10 domains, their purposes, and relationships.
- `docs/checklist-packs.md`: Pre-assembled checklist combinations for common task types.
- `docs/risk-tiering.md`: Detailed risk tier definitions, assessment criteria, and examples.
- `docs/framework-quality-standard.md`: Quality metrics, maturity levels, and compliance criteria.

**Templates**
- `assets/templates/release-checklist.md`: Comprehensive release checklist with domain-specific items.
- `assets/templates/model-prompt-change-review.md`: Template for reviewing model and prompt changes.
- `assets/templates/evaluation-plan.md`: Template for planning model and system evaluations.

**Scripts**
- `scripts/check_rules.py`: Automated rule checker that validates compliance with framework requirements.
- `scripts/validate_evidence.py`: Validates that collected evidence meets framework standards.
- `scripts/generate_report.py`: Generates compliance and audit reports from collected evidence.

**Domain Files**
- `domains/01-core/fundamentals.md`: Core AI system requirements and principles.
- `domains/02-security/threat-model.md`: Security threat modeling and controls.
- `domains/03-data/governance.md`: Data governance, privacy, and retention policies.
- `domains/04-integration/compatibility.md`: Integration patterns and compatibility requirements.
- `domains/05-development/quality.md`: Development practices and code quality standards.
- `domains/06-testing/strategy.md`: Testing strategies, coverage requirements, and test types.
- `domains/07-operations/reliability.md`: Operational reliability, monitoring, and incident response.
- `domains/08-documentation/standards.md`: Documentation standards and requirements.
- `domains/09-performance/efficiency.md`: Performance optimization and scalability.
- `domains/10-compliance/audit.md`: Compliance requirements and audit procedures.

**Additional Resources**
- `examples/`: Example implementations and case studies.
- `templates/`: Additional templates for specific scenarios.
- `reference/`: Reference materials, standards, and external links.
- `tools/`: Supporting tools and utilities.

## Default Agent Behavior

When using this skill:

- Read the relevant local domain files before making recommendations.
- Prefer checklist-backed decisions over generic advice.
- Surface missing tests, missing evidence, and missing ownership.
- Surface missing error handling, timeout handling, retry limits, and rollback plans.
- Keep recommendations scoped to the user's system type and risk tier.
- Do not invent compliance status; state evidence gaps clearly.

### Default Agent Behavior Deep Dive

**Pre-Recommendation Protocol**
1. Read all relevant domain files for the task at hand.
2. Check the checklist for the specific task type.
3. Identify any P0/P1 items that apply.
4. Verify that evidence exists for compliance claims.
5. Formulate recommendations based on framework rules, not generic best practices.

**Decision-Making Principles**
- **Evidence-Based**: Every recommendation must reference a specific framework rule or checklist item.
- **Risk-Appropriate**: Recommendations should match the system's risk tier.
- **Actionable**: Recommendations should be specific, concrete, and implementable.
- **Prioritized**: P0 items first, then P1, then P2/P3.
- **Transparent**: Clearly state assumptions, uncertainties, and evidence gaps.

**Communication Standards**
- Use clear, concise language.
- Avoid jargon unless necessary and defined.
- Provide context for recommendations.
- Explain the "why" behind each recommendation.
- Offer alternatives when appropriate.
- Flag trade-offs explicitly.

**Quality Assurance**
- Verify recommendations against the framework before presenting.
- Check for consistency with previous recommendations.
- Validate that recommendations don't conflict with each other.
- Ensure recommendations are complete for the task scope.
- Test recommendations against the checklist.

**Escalation Triggers**
- P0 findings that cannot be resolved within the current context.
- Conflicts between framework requirements and user constraints.
- Ambiguous system type or risk tier.
- Missing critical evidence that cannot be obtained.
- Recommendations that require expertise outside the agent's knowledge.

## Risk Tier Framework

### Tier Definitions

**Tier 1 - Critical (Highest Risk)**
- Systems handling financial transactions, healthcare data, or critical infrastructure.
- Failures can cause significant financial loss, physical harm, or widespread service disruption.
- Examples: Payment processing, medical diagnosis support, air traffic control, emergency services.
- Requirements: All P0 and P1 rules must be satisfied. Extensive testing required. Human oversight mandatory.

**Tier 2 - High Risk**
- Customer-facing systems with significant user base or business impact.
- Failures cause user frustration, data loss, or security incidents.
- Examples: E-commerce platforms, social media, enterprise SaaS, communication tools.
- Requirements: All P0 rules must be satisfied. P1 rules must be addressed or accepted. Comprehensive testing required.

**Tier 3 - Medium Risk**
- Internal tools or systems with limited user base.
- Failures cause work disruption but limited external impact.
- Examples: Internal dashboards, development tools, internal APIs.
- Requirements: P0 rules must be satisfied. P1 rules should be addressed. Standard testing required.

**Tier 4 - Low Risk**
- Experimental systems, prototypes, or non-critical tools.
- Failures have minimal impact and are easily recoverable.
- Examples: Proof of concepts, research projects, personal tools.
- Requirements: Critical P0 rules must be satisfied. Basic testing recommended.

### Risk Tier Assessment Criteria

**Impact Assessment**
- User impact: How many users are affected? How severely?
- Data impact: Is there risk of data loss, corruption, or exposure?
- Financial impact: What is the potential financial loss?
- Reputation impact: What is the potential reputational damage?
- Compliance impact: Are there regulatory violations possible?

**Reversibility Assessment**
- Can changes be rolled back quickly? (Minutes/Hours/Days)
- Is data recoverable? (Yes/No/Partially)
- Can the system be restored to a known good state?
- What is the recovery time objective (RTO)?

**Blast Radius Assessment**
- Number of users affected
- Number of systems dependent
- Geographic distribution of impact
- Cross-service dependencies

## Evidence Standards

### Evidence Categories

**Test Evidence**
- Automated test execution results (pass/fail, coverage reports)
- Manual test results and sign-offs
- Performance benchmark results
- Load test results
- Chaos test results
- Security scan results

**Documentation Evidence**
- Updated documentation
- Architecture diagrams
- Runbooks and procedures
- API documentation
- User guides

**Configuration Evidence**
- Configuration files (sanitized)
- Environment variable documentation
- Feature flag configurations
- Deployment manifests
- Infrastructure as code

**Observability Evidence**
- Monitoring dashboard screenshots
- Alert configuration documentation
- Log aggregation setup
- Metric collection verification
- Tracing configuration

**Compliance Evidence**
- Regulatory checklists
- Audit trail samples
- Privacy impact assessments
- Security assessment reports
- Data flow diagrams

### Evidence Quality Standards

**Completeness**
- Evidence must cover all applicable checklist items.
- Evidence must be sufficient to verify compliance.
- Evidence must be reproducible.

**Authenticity**
- Evidence must be from the actual system, not hypothetical.
- Evidence must be timestamped.
- Evidence must be attributable to a specific version/state.

**Clarity**
- Evidence must be clearly labeled and organized.
- Evidence must include context for interpretation.
- Evidence must be accessible to reviewers.

**Retention**
- Evidence must be retained for the required period.
- Evidence must be stored in a stable, accessible location.
- Evidence must be backed up.

## Audit Trail Requirements

### Audit Log Content

Every significant action must be logged with:
- Timestamp (ISO 8601 with timezone)
- Actor (user, service, agent)
- Action performed
- Target of the action (file, component, system)
- Outcome (success, failure, partial)
- Context (relevant parameters, state)
- Correlation ID for tracing

### Audit Events to Log

**Development Events**
- Code commits
- Pull request creation and merge
- Code review approvals
- Configuration changes
- Dependency updates

**Deployment Events**
- Deployment initiation
- Deployment success/failure
- Rollback initiation and completion
- Configuration changes in production
- Infrastructure changes

**Operational Events**
- Service restarts
- Configuration reloads
- Scaling events
- Health check failures
- Incident creation and resolution

**Security Events**
- Authentication attempts (success/failure)
- Authorization checks
- Access control changes
- Security scan executions
- Vulnerability discoveries

### Audit Retention

- Development audit logs: 1 year
- Deployment audit logs: 3 years
- Operational audit logs: 2 years
- Security audit logs: 7 years (or as required by regulation)
- Compliance audit logs: As required by applicable regulations

## Continuous Compliance

### Ongoing Compliance Activities

**Regular Reviews**
- Weekly: Review new changes for compliance
- Monthly: Comprehensive compliance review
- Quarterly: External audit preparation
- Annually: Full compliance assessment

**Continuous Monitoring**
- Automated compliance checks in CI/CD
- Real-time alerting for compliance violations
- Regular security scans
- Dependency vulnerability monitoring

**Improvement Cycle**
- Collect compliance metrics
- Identify gaps and trends
- Implement improvements
- Verify effectiveness
- Document changes

## Framework Evolution

### Version Management

- Framework versions are tagged and released.
- Changes to the framework follow the same review process as system changes.
- Migration guides are provided for major version changes.
- Backward compatibility is maintained when possible.

### Feedback Integration

- Collect feedback from framework users.
- Review feedback in regular framework meetings.
- Prioritize improvements based on impact and feasibility.
- Communicate changes to all users.
- Update documentation and training materials.

## Appendix: Quick Reference

### Task to Domain Mapping

| Task | Primary Domains | Secondary Domains |
|------|----------------|-------------------|
| New LLM feature | Core, Security, Testing | Data, Operations |
| Model upgrade | Core, Testing, Performance | Security, Operations |
| Prompt change | Core, Security, Testing | Documentation |
| RAG improvement | Core, Data, Testing | Security, Performance |
| Tool integration | Integration, Security, Testing | Core, Operations |
| Production deploy | Operations, Security | Testing, Compliance |
| Incident response | Operations, Troubleshooting | Testing, Performance |
| Compliance audit | Compliance, Security | Documentation, Data |
| Code review | Development, Security | Testing, Documentation |
| Performance tuning | Performance, Operations | Testing, Core |

### P0 Rule Quick Reference

- No unhandled exceptions in critical paths
- All external inputs validated
- Authentication and authorization enforced
- Sensitive data protected in transit and at rest
- Rollback capability exists and is tested
- Monitoring and alerting configured
- Error handling includes timeout, retry, and fallback
- No hardcoded secrets or credentials
- Dependencies scanned for vulnerabilities
- Data validation at all boundaries

### P1 Rule Quick Reference

- Retry logic with bounded retries
- Circuit breakers for external dependencies
- Timeout configuration for all external calls
- Comprehensive test coverage (> 80% critical paths)
- Runbooks for common failure scenarios
- Performance baselines established
- Structured logging implemented
- Health checks implemented
- Graceful degradation defined
- Documentation complete for user-facing features
