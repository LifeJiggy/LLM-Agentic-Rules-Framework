# Framework Context - Comprehensive Reference

## Overview

The LLM & Agentic Rules Framework is a production-grade rules framework for building LLM chatbots, agentic systems, and AI-powered applications. Version 1.1.0 with 10 domains and 70+ rule files.

## Project Structure

```
llm-agentic-rules/
├── .github/
│   ├── workflows/
│   │   └── validate-framework.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── rule_proposal.md
│   └── PULL_REQUEST_TEMPLATE.md
├── .codex-plugin/
│   └── plugin.json
├── adapters/
│   ├── README.md
│   ├── manifest.json
│   └── targets.md
├── agents/
│   ├── rules-architect.md
│   ├── rules-compliance-auditor.md
│   ├── rules-data-steward.md
│   ├── rules-enforcer.md
│   ├── rules-documentation.md
│   ├── rules-eval.md
│   ├── rules-implementer.md
│   ├── rules-orchestrator.md
│   ├── rules-release-gate.md
│   ├── rules-reviewer.md
│   ├── rules-security.md
│   └── rules-tracker.md
├── commands/
│   ├── rules-audit.md
│   ├── rules-plan.md
│   └── rules-release.md
├── assets/
│   └── templates/
│       ├── architecture-decision-record.md
│       ├── ai-system-register.yml
│       ├── compliance-review.md
│       ├── compliance-evidence-pack.md
│       ├── evaluation-plan.md
│       ├── evaluation-pack-retrieval.md
│       ├── evaluation-pack-safety.md
│       ├── evaluation-pack-tools.md
│       ├── incident-runbook.md
│       ├── model-prompt-change-review.md
│       ├── release-checklist.md
│       └── rule-template.md
├── docs/
│   ├── index.md
│   ├── adoption-playbook.md
│   ├── agentic-cli-plugin-guide.md
│   ├── checklist-packs.md
│   ├── getting-started.md
│   ├── advanced-usage.md
│   ├── domain-knowledge-map.md
│   ├── domain-index.md
│   ├── evolution-process.md
│   ├── framework-quality-standard.md
│   ├── glossary.md
│   └── migration-guide.md
├── examples/
│   ├── agentic-automation/
│   └── production-assistant/
├── domains/
│   ├── 01-core/
│   ├── 02-security/
│   ├── 03-development/
│   ├── 04-data/
│   ├── 05-integration/
│   ├── 06-operations/
│   ├── 07-testing/
│   ├── 08-documentation/
│   ├── 09-performance/
│   └── 10-compliance/
├── memory/
│   ├── framework-context.md
│   ├── agent-catalog.md
│   ├── domain-reference.md
│   ├── integration-patterns.md
│   └── decision-matrix.md
├── scripts/
│   ├── check_rules.py
│   ├── install_agent_adapters.py
│   └── validate-framework.ps1
├── skills/
│   └── llm-agentic-rules/
│       └── system/
├── storage/
│   ├── rule-templates.md
│   ├── checklist-templates.md
│   ├── evaluation-templates.md
│   ├── incident-templates.md
│   └── architecture-templates.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── mkdocs.yml
├── README.md
└── ROADMAP.md
```

## Domain Structure

Each domain contains exactly 7 files with consistent structure:

| File | Purpose | When To Use | Lines Expected |
|------|---------|-------------|----------------|
| fundamentals.md | Core concepts every practitioner should know | Onboarding and early design | 200-500 |
| best-practices.md | Recommended patterns and standards | Design, implementation, review | 300-600 |
| anti-patterns.md | Mistakes to avoid and safer alternatives | Risk review and debugging | 200-400 |
| checklist.md | Actionable verification steps | PRs, releases, audits | 150-300 |
| examples.md | Practical snippets and templates | Implementation and prototyping | 300-600 |
| troubleshooting.md | Symptoms, root causes, fixes | Incidents and support | 200-400 |
| advanced.md | Complex scenarios and tradeoffs | Scaling and expert review | 300-500 |

## Domains Detail

### Domain 01: Core

**Focus**: Architecture, context, tools, state
**Description**: Fundamental rules for all LLM and agentic systems
**Key Topics**:
- System architecture and design patterns
- Context window management
- Tool integration and MCP protocol
- State management across turns
- Human-in-the-loop workflows
- Model selection and routing
- Prompt engineering fundamentals
- Response quality controls

**Controls**:
- System ownership and purpose documentation
- Risk tier assignment
- Human review for high-impact actions
- Fallback and rollback capability
- Model evaluation and benchmarking
- Prompt version control
- Tool permission boundaries
- Audit logging

### Domain 02: Security

**Focus**: Prompt injection, data protection, access control
**Description**: Security-first development and threat prevention
**Key Topics**:
- Prompt injection attacks and defenses
- Data protection and encryption
- Authentication and authorization
- Secret management
- Network security
- Incident response
- Vulnerability management
- Supply chain security

**Controls**:
- Threat modeling
- Input validation and sanitization
- Output filtering
- Secret rotation
- Access control enforcement
- Security monitoring
- Penetration testing
- Security review gates

### Domain 03: Development

**Focus**: Code quality, maintainability, reviews
**Description**: Software engineering standards for AI systems
**Key Topics**:
- Code quality standards
- Version control practices
- Code review processes
- Testing strategies
- Documentation standards
- Refactoring patterns
- Technical debt management
- Development environment setup

**Controls**:
- Code review requirements
- Test coverage thresholds
- Documentation completeness
- Linting and formatting
- Static analysis
- Dependency management
- Build automation
- Release management

### Domain 04: Data

**Focus**: Privacy, governance, pipelines
**Description**: Data handling, retrieval, storage, and governance
**Key Topics**:
- Data classification and inventory
- Privacy and PII handling
- Data retention and purging
- Legal hold requirements
- Data quality management
- Data lineage tracking
- Cross-border data transfers
- Data subject requests

**Controls**:
- Data inventory maintenance
- Classification labeling
- Retention policy enforcement
- Consent management
- Data minimization
- Encryption at rest and in transit
- Access logging
- Quality validation

### Domain 05: Integration

**Focus**: APIs, webhooks, tool contracts
**Description**: External services, APIs, tools, and protocols
**Key Topics**:
- API design and versioning
- Webhook management
- Tool integration patterns
- MCP protocol implementation
- Third-party vendor management
- Contract testing
- Rate limiting and quotas
- Error handling

**Controls**:
- API versioning strategy
- Tool registry maintenance
- Credential management
- Timeout and retry configuration
- Circuit breaker implementation
- Contract validation
- Vendor assessment
- Integration testing

### Domain 06: Operations

**Focus**: CI/CD, observability, scaling
**Description**: Deployment, monitoring, incident response, and reliability
**Key Topics**:
- Deployment strategies
- Monitoring and alerting
- Incident response
- Disaster recovery
- Capacity planning
- Cost management
- Performance optimization
- SRE practices

**Controls**:
- Deployment automation
- Rollback procedures
- Monitoring coverage
- Alert routing
- On-call rotation
- Incident runbooks
- Post-incident reviews
- Capacity forecasting

### Domain 07: Testing

**Focus**: Unit, integration, E2E, regression
**Description**: Quality assurance and evaluation strategies
**Key Topics**:
- Evaluation methodology
- Test design patterns
- Regression testing
- Safety and bias testing
- Performance testing
- Chaos engineering
- Test data management
- Test automation

**Controls**:
- Evaluation coverage thresholds
- Regression suite maintenance
- Safety test inclusion
- Performance benchmarks
- Test environment parity
- Test data governance
- Test reporting
- Test automation CI/CD

### Domain 08: Documentation

**Focus**: API docs, runbooks, guides
**Description**: Documentation standards and knowledge sharing
**Key Topics**:
- System documentation
- API documentation
- Runbook creation
- Model cards
- Prompt registers
- Architecture diagrams
- Data flow documentation
- Training materials

**Controls**:
- Documentation completeness
- Documentation currency
- Accessibility compliance
- Version control
- Review process
- Publication workflow
- Feedback collection
- Archive management

### Domain 09: Performance

**Focus**: Latency, throughput, caching
**Description**: Performance, cost, and resource optimization
**Key Topics**:
- Latency optimization
- Throughput management
- Caching strategies
- Cost optimization
- Resource management
- Load testing
- Capacity planning
- Performance monitoring

**Controls**:
- SLO definition and tracking
- Performance budgets
- Cache configuration
- Rate limiting
- Resource limits
- Cost attribution
- Performance testing
- Optimization reviews

### Domain 10: Compliance

**Focus**: Governance, risk controls, audit
**Description**: Legal, regulatory, ethical, and audit readiness
**Key Topics**:
- Regulatory compliance
- Audit preparation
- Evidence management
- Exception handling
- Policy enforcement
- Training and awareness
- Vendor compliance
- Risk assessment

**Controls**:
- Compliance assessment
- Evidence collection
- Audit trail maintenance
- Exception register
- Policy documentation
- Training tracking
- Vendor management
- Regulatory monitoring

## Priority Levels

| Priority | Meaning | Expected Handling | Timeline |
|----------|---------|-------------------|----------|
| P0 Critical | Security, safety, compliance, or data-loss risk | Required before production | Immediate |
| P1 High | Reliability, quality, or maintainability risk | Required unless explicitly accepted | Before release |
| P2 Medium | Meaningful quality improvement | Adopt when practical | Current quarter |
| P3 Low | Helpful refinement | Backlog or opportunistic | Future planning |

## Target Audience

| Role | Primary Use | Key Domains |
|------|-------------|-------------|
| AI/ML Engineers | Building LLM applications | Core, Testing, Performance |
| Software Developers | Integrating AI capabilities | Core, Development, Integration |
| DevOps/Platform Engineers | Deploying AI infrastructure | Operations, Performance, Security |
| Security Professionals | Reviewing prompt, data, tool risk | Security, Compliance, Data |
| Technical Leads | Setting team standards | All domains |
| Compliance/Governance | Evaluating AI system risk | Compliance, Data, Security |
| Researchers | Translating patterns into systems | Core, Testing, Documentation |

## Quality Standards

| Promise | Project Support |
|---------|-----------------|
| Standardized Guidelines | Framework Quality Standard, Rule Template, validation scripts |
| Domain-Specific Knowledge | Domain Knowledge Map, Domain Index, 10 domain folders |
| Actionable Checklists | Checklist Packs, domain checklists, checklist export tooling |
| Real-World Examples | Production Assistant Example, Agentic Automation Example, domain examples |
| Continuous Evolution | Evolution Process, CHANGELOG.md, ROADMAP.md |
| Multi-Agent Distribution | Agentic CLI Plugin Guide, Adapters, plugin manifests |

## Repository Quality Checks

### Structure Validation

```powershell
./scripts/validate-framework.ps1
```

Checks:
- 10 domains exist with correct naming
- 7 files per domain with correct naming
- Required docs, templates, and automation present
- No structural drift from framework contract

### Rule Inventory

```bash
python scripts/check_rules.py --summary
```

Outputs:
- Rule count by domain and priority
- Coverage analysis
- Gap identification
- Quality metrics

### Full Validation

```bash
python scripts/check_rules.py \
  --summary \
  --validate-links \
  --json build/rule-report.json \
  --catalog build/rule-catalog.json \
  --coverage build/domain-coverage.md \
  --export-checklists build/checklists.md
```

## Integration Points

### CI/CD Integration

```yaml
name: Validate Framework
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: ./scripts/validate-framework.ps1
      - run: python scripts/check_rules.py --summary
```

### Documentation Reference

```markdown
This project follows the LLM & Agentic Rules Framework:
- Core architecture: domains/01-core/fundamentals.md
- Security controls: domains/02-security/checklist.md
- Evaluation strategy: domains/07-testing/best-practices.md
- Compliance register: assets/templates/ai-system-register.yml
```

### Team Onboarding Path

```markdown
- [ ] Core fundamentals
- [ ] Security fundamentals
- [ ] Testing checklist
- [ ] Operations troubleshooting
- [ ] Compliance fundamentals
```

## Adapter System

### Preview Installs

```bash
python scripts/install_agent_adapters.py --target all --dry-run
```

### List Targets

```bash
python scripts/install_agent_adapters.py --list-targets
```

### Install Components

```bash
python scripts/install_agent_adapters.py --target all --component skill --apply
```

### Stage for Review

```bash
python scripts/install_agent_adapters.py --target all --target-root ./adapter-preview --apply
```

### CI/Managed Rollout

```bash
python scripts/install_agent_adapters.py --target all --apply --fail-fast
```

## Framework Evolution

### Current Focus

- Expand production examples for more architectures and stacks
- Add richer automated validation for quality-standard requirements
- Keep checklist packs aligned with new domain guidance
- Use changelog and roadmap updates for continuous evolution

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-01 | Initial release with 10 domains |
| 1.1.0 | 2026-06-01 | Added agent system, adapter system, enhanced validation |

## Usage Patterns

### New Project Adoption

1. Clone the repository
2. Read core fundamentals and checklist
3. Add domains based on system risk
4. Copy relevant checklists into project review process

### Existing Project Audit

1. Audit current implementation against domain checklists
2. Start with P0 and P1 security, data, testing, and operations gaps
3. Use examples and templates to standardize controls
4. Track exceptions and accepted risks explicitly

### Risk-Based Domain Selection

| System Type | Required Domains | Optional Domains |
|-------------|-----------------|------------------|
| Customer-facing assistant | Core, Security, Data, Testing, Operations, Compliance | Documentation, Performance |
| Internal agent automation | Core, Development, Integration, Operations, Testing | Documentation |
| High-volume AI API | Core, Integration, Performance, Operations, Testing | Security, Compliance |
| Healthcare AI system | All 10 domains | - |
| Financial AI system | All 10 domains | - |

## Cross-Domain Dependencies

```
Core ←→ Security ←→ Data ←→ Integration
  ↑         ↑         ↑         ↑
  ↓         ↓         ↓         ↓
Testing ←→ Operations ←→ Performance ←→ Compliance
```

| Domain | Depends On | Impacts |
|--------|-----------|---------|
| Core | Security, Compliance | All domains |
| Security | Core, Data, Integration | Operations, Compliance |
| Data | Core, Security | Integration, Testing, Compliance |
| Integration | Core, Security, Data | Operations, Testing |
| Operations | Security, Integration | Testing, Documentation |
| Testing | Core, Security, Data | Operations, Release Gate |
| Documentation | All domains | Compliance, Operations |
| Performance | Core, Integration | Operations, Testing |
| Compliance | Security, Data, Testing | Release Gate, Documentation |

## Key Terminology

| Term | Definition |
|------|------------|
| ADR | Architecture Decision Record |
| P0/P1/P2/P3 | Priority levels for controls and findings |
| RAG | Retrieval-augmented generation |
| MCP | Model Context Protocol |
| DSAR | Data Subject Access Request |
| DPIA | Data Protection Impact Assessment |
| DPO | Data Protection Officer |
| DPA | Data Processing Agreement |
| SLA | Service Level Agreement |
| SLO | Service Level Objective |
| MTTR | Mean Time To Recovery |
| TTL | Time To Live |
| CI/CD | Continuous Integration / Continuous Deployment |
| RBAC | Role-Based Access Control |
| ABAC | Attribute-Based Access Control |
| PBAC | Policy-Based Access Control |

## Governance Model

### Review Cadence

| Review Type | Frequency | Participants |
|-------------|-----------|--------------|
| Design review | Per project | Architect, Security, Compliance |
| Code review | Per PR | Developers, Reviewer |
| Security review | Per release | Security, Compliance |
| Compliance review | Quarterly | Compliance, Legal, DPO |
| Architecture review | Semi-annually | Architect, Engineering, Product |
| Framework review | Annually | All stakeholders |

### Escalation Paths

| Issue Type | First Escalation | Second Escalation | Final Escalation |
|------------|------------------|-------------------|------------------|
| ADR disagreement | Engineering lead | Architecture review board | Governance committee |
| Exception approval | Domain owner | Compliance officer | Chief Risk Officer |
| Control gap in high-risk | Compliance | CISO | CEO / Board |
| Test failure blocking release | Engineering lead | Release Gate Agent | Product owner |
| Budget overrun for controls | Engineering lead | Finance | CFO approval |

## Evidence Management

### Evidence Types

| Type | Description | Generation |
|------|-------------|------------|
| Automated | Generated by CI/CD, evaluation, monitoring | Automated |
| Manual | Produced by human review, audit, assessment | Manual |
| Hybrid | Automated collection with human validation | Semi-automated |

### Retention Requirements

| Evidence Type | Minimum Retention | Storage |
|---------------|-------------------|---------|
| Security review | 12 months or until architecture change | Evidence store |
| Penetration test | 12 months | Evidence store |
| Vulnerability scan | 30 days | CI/CD artifacts |
| Evaluation report | Per release | Evidence store |
| Privacy review | 12 months or until data handling changes | Evidence store |
| Threat model | 12 months or until architecture changes | Evidence store |
| DPA | Per vendor contract | Compliance store |
| Training completion | 12 months | HR/LMS system |

### Integrity Requirements

- Hash chain or digital signature for evidence
- Timestamp and signatory on all evidence
- Retrievable by system, release, and control
- Versioned and immutable once published
- Access controlled and audit logged

## Common Anti-Patterns

### Architecture Anti-Patterns

| Anti-Pattern | Risk | Mitigation |
|--------------|------|------------|
| Single point of failure | Total system failure | Multi-provider router with fallback |
| Scope creep in prompts | Unauthorized actions | Explicit scope boundaries, prompt register |
| Missing human review | Harmful actions executed | Human review gates for high-impact |
| Unbounded tool access | Data exfiltration | Permissioned tool registry, least privilege |
| Ignored data residency | Regulatory violations | Jurisdiction tagging, transfer assessment |
| No model fallback | Service disruption | Fallback model, graceful degradation |
| Untested rollback | Extended outage | Regular rollback drills, tested automation |
| Missing exception management | Control gaps | Formal exception register with review |

### Implementation Anti-Patterns

| Anti-Pattern | Risk | Mitigation |
|--------------|------|------------|
| Hardcoded secrets | Credential leakage | Secret management, rotation |
| Missing input validation | Injection attacks | Input sanitization, schema validation |
| No rate limiting | Resource exhaustion | Rate limiting, quota management |
| Missing audit logging | No forensic capability | Comprehensive audit trail |
| Inadequate error handling | Unpredictable behavior | Structured error handling |
| Skipping tests | Quality regression | Test coverage requirements |
| Documentation debt | Knowledge loss | Documentation standards |
| Configuration drift | Security gaps | Configuration management |

## Metrics and KPIs

### System Health Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | Uptime monitoring |
| Error rate | < 0.1% | Request logging |
| Latency p95 | < 500ms | Performance monitoring |
| Throughput | Per capacity plan | Load testing |
| Cost per request | Within budget | Cost attribution |

### Process Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Review cycle time | < 48 hours | Review tracking |
| Deployment frequency | Per capacity plan | CI/CD metrics |
| Mean time to detect | < 5 minutes | Incident tracking |
| Mean time to resolve | < 1 hour | Incident tracking |
| Post-release incident rate | < 2% | Incident tracking |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Evaluation score | > 0.85 | Evaluation suite |
| Safety score | > 0.95 | Safety evaluation |
| User satisfaction | > 4.0/5.0 | User feedback |
| Documentation coverage | 100% | Documentation audit |
| Test coverage | > 80% | Code coverage |

## Regulatory Reference

| Regulation | Scope | Key Obligations | Framework Domain |
|------------|-------|-----------------|------------------|
| GDPR | EU personal data | Lawful basis, consent, DSAR, DPIA | Data, Compliance |
| HIPAA | US health data | Safeguards, breach notification, BAA | Security, Data, Compliance |
| PCI DSS | Payment data | Encryption, access control, testing | Security, Data, Compliance |
| SOC 2 | Service organizations | Security, availability, confidentiality | Security, Operations, Compliance |
| EU AI Act | AI systems in EU | Risk classification, conformity, transparency | Core, Compliance, Testing |
| NIST AI RMF | AI governance | Govern, map, measure, manage | All domains |
| CCPA/CPRA | California consumer data | Consumer rights, disclosure, deletion | Data, Compliance |
| GLBA | Financial data | Safeguards, privacy notices, access controls | Security, Data, Compliance |
| ISO 27001 | Information security | ISMS, risk assessment, controls | Security, Compliance |

## Framework Design Principles

### Privacy by Design

- Data minimization in all data flows
- Purpose limitation enforcement
- Consent management at collection points
- Right to erasure support
- Privacy impact assessments for new features

### Security by Design

- Authentication and authorization at boundaries
- Encryption for data at rest and in transit
- Secret management with rotation
- Audit logging for all sensitive operations
- Security review gates in development

### Resilience by Design

- Graceful degradation on failures
- Circuit breakers for external dependencies
- Fallback mechanisms for critical paths
- Recovery procedures tested regularly
- Chaos engineering for validation

### Observability by Design

- Structured logging with correlation IDs
- Metrics collection at key points
- Distributed tracing across services
- Dashboard visibility for operations
- Alert routing to appropriate teams

### Testability by Design

- Evaluation harness integrated in CI/CD
- Test data management and governance
- Regression test suite maintenance
- Safety and fairness testing included
- Performance testing in staging

### Compliance by Design

- Evidence generation automated where possible
- Audit trail for all significant actions
- Exception management with tracking
- Training requirements enforced
- Vendor compliance verified

### Maintainability by Design

- Modular architecture with clear boundaries
- Documentation maintained with code
- Code review for all changes
- Technical debt tracked and managed
- Refactoring opportunities identified

### Scalability by Design

- Load handling validated
- Resource management automated
- Caching strategies implemented
- Capacity planning performed
- Cost optimization reviewed
