# Domain Reference - Comprehensive Guide

## Overview

The framework contains 10 domains, each with 7 rule files. This reference provides detailed guidance for each domain including controls, mappings, and selection criteria.

## Domain Selection Guide

### By System Type

| System Type | Required Domains | Recommended Domains | Optional Domains |
|-------------|-----------------|---------------------|------------------|
| Customer-facing assistant | Core, Security, Data, Testing, Operations, Compliance | Documentation, Performance | Development, Integration |
| Internal agent automation | Core, Development, Integration, Operations, Testing | Documentation | Security, Data |
| High-volume AI API | Core, Integration, Performance, Operations, Testing | Security, Compliance | Documentation |
| Healthcare AI system | All 10 domains | - | - |
| Financial AI system | All 10 domains | - | - |
| Research/prototyping | Core, Testing | Security, Documentation | Others as needed |
| Simple chatbot | Core, Testing | Security | Documentation |
| Enterprise platform | All 10 domains | - | - |

### By Risk Tier

| Risk Tier | Minimum Domains | Expected Controls |
|-----------|----------------|-------------------|
| Low | Core, Testing | Basic evaluation, basic monitoring |
| Medium | Core, Security, Data, Testing, Operations | Human review, retention, PII minimization |
| High | All 10 domains | Full control set, audit trail, incident response |

### By Regulatory Requirements

| Regulation | Required Domains | Key Controls |
|------------|-----------------|--------------|
| GDPR | Core, Security, Data, Compliance | Consent, DSAR, DPIA, retention |
| HIPAA | Core, Security, Data, Compliance, Operations | BAA, encryption, audit, breach notification |
| PCI DSS | Core, Security, Data, Compliance | Encryption, access control, testing |
| SOC 2 | Core, Security, Operations, Compliance | Security, availability, confidentiality |
| EU AI Act | All 10 domains | Risk classification, conformity, transparency |

## Domain Dependencies

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

## Domain 01: Core

### Focus
Architecture, context, tools, state

### Description
Fundamental rules for all LLM and agentic systems

### Key Topics
- System architecture and design patterns
- Context window management
- Tool integration and MCP protocol
- State management across turns
- Human-in-the-loop workflows
- Model selection and routing
- Prompt engineering fundamentals
- Response quality controls

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| CORE-001 | P0 | System ownership and purpose documentation |
| CORE-002 | P0 | Risk tier assignment and justification |
| CORE-003 | P0 | Human review for high-impact actions |
| CORE-004 | P0 | Fallback and rollback capability |
| CORE-005 | P1 | Model evaluation and benchmarking |
| CORE-006 | P1 | Prompt version control |
| CORE-007 | P1 | Tool permission boundaries |
| CORE-008 | P1 | Audit logging |
| CORE-009 | P2 | Context window optimization |
| CORE-010 | P2 | Response quality monitoring |

### Key Files

| File | Purpose | Lines |
|------|---------|-------|
| fundamentals.md | Core concepts | 200-500 |
| best-practices.md | Recommended patterns | 300-600 |
| anti-patterns.md | Mistakes to avoid | 200-400 |
| checklist.md | Verification steps | 150-300 |
| examples.md | Practical snippets | 300-600 |
| troubleshooting.md | Symptoms and fixes | 200-400 |
| advanced.md | Complex scenarios | 300-500 |

---

## Domain 02: Security

### Focus
Prompt injection, data protection, access control

### Description
Security-first development and threat prevention

### Key Topics
- Prompt injection attacks and defenses
- Data protection and encryption
- Authentication and authorization
- Secret management
- Network security
- Incident response
- Vulnerability management
- Supply chain security

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| SEC-001 | P0 | Threat modeling |
| SEC-002 | P0 | Input validation and sanitization |
| SEC-003 | P0 | Output filtering |
| SEC-004 | P0 | Secret rotation |
| SEC-005 | P0 | Access control enforcement |
| SEC-006 | P1 | Security monitoring |
| SEC-007 | P1 | Penetration testing |
| SEC-008 | P1 | Security review gates |
| SEC-009 | P2 | Security training |
| SEC-010 | P2 | Security metrics |

### Threat Categories

| Category | Examples | Mitigations |
|----------|----------|-------------|
| Prompt injection | Direct injection, indirect injection | Input validation, content filtering |
| Data exfiltration | API abuse, tool misuse | Access control, monitoring |
| Authentication bypass | Credential stuffing, session hijacking | MFA, session management |
| Privilege escalation | Role manipulation, IDOR | Authorization enforcement |
| Supply chain | Dependency compromise, vendor breach | Vendor assessment, SBOM |

---

## Domain 03: Development

### Focus
Code quality, maintainability, reviews

### Description
Software engineering standards for AI systems

### Key Topics
- Code quality standards
- Version control practices
- Code review processes
- Testing strategies
- Documentation standards
- Refactoring patterns
- Technical debt management
- Development environment setup

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| DEV-001 | P0 | Code review requirements |
| DEV-002 | P1 | Test coverage thresholds |
| DEV-003 | P1 | Documentation completeness |
| DEV-004 | P1 | Linting and formatting |
| DEV-005 | P1 | Static analysis |
| DEV-006 | P2 | Dependency management |
| DEV-007 | P2 | Build automation |
| DEV-008 | P2 | Release management |

### Quality Gates

| Gate | Criteria | Blocking |
|------|----------|----------|
| Code review | At least one approval | Yes |
| Test coverage | > 80% | Yes |
| Linting | No errors | Yes |
| Static analysis | No critical findings | Yes |
| Documentation | Updated for changes | No |

---

## Domain 04: Data

### Focus
Privacy, governance, pipelines

### Description
Data handling, retrieval, storage, and governance

### Key Topics
- Data classification and inventory
- Privacy and PII handling
- Data retention and purging
- Legal hold requirements
- Data quality management
- Data lineage tracking
- Cross-border data transfers
- Data subject requests

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| DATA-001 | P0 | Data inventory maintenance |
| DATA-002 | P0 | Classification labeling |
| DATA-003 | P0 | Retention policy enforcement |
| DATA-004 | P0 | Consent management |
| DATA-005 | P1 | Data minimization |
| DATA-006 | P1 | Encryption at rest and in transit |
| DATA-007 | P1 | Access logging |
| DATA-008 | P2 | Quality validation |
| DATA-009 | P2 | Lineage tracking |
| DATA-010 | P2 | Cross-border assessment |

### Data Classification Levels

| Level | Description | Examples | Controls |
|-------|-------------|----------|----------|
| Public | Freely available | Marketing content | Basic access control |
| Internal | Employee access only | Internal docs | Authentication required |
| Confidential | Restricted access | Customer data | Encryption, access logging |
| Restricted | Highly restricted | PII, PHI | Strong encryption, MFA, audit |

---

## Domain 05: Integration

### Focus
APIs, webhooks, tool contracts

### Description
External services, APIs, tools, and protocols

### Key Topics
- API design and versioning
- Webhook management
- Tool integration patterns
- MCP protocol implementation
- Third-party vendor management
- Contract testing
- Rate limiting and quotas
- Error handling

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| INT-001 | P0 | API versioning strategy |
| INT-002 | P0 | Tool registry maintenance |
| INT-003 | P1 | Credential management |
| INT-004 | P1 | Timeout and retry configuration |
| INT-005 | P1 | Circuit breaker implementation |
| INT-006 | P1 | Contract validation |
| INT-007 | P2 | Vendor assessment |
| INT-008 | P2 | Integration testing |

### Integration Patterns

| Pattern | Use Case | Considerations |
|---------|----------|----------------|
| Synchronous API | Real-time responses | Latency, timeout handling |
| Asynchronous webhook | Event-driven | Idempotency, retry |
| Message queue | Decoupled systems | Ordering, dead letter |
| MCP protocol | Tool integration | Permission, audit |
| GraphQL | Flexible queries | Complexity, caching |

---

## Domain 06: Operations

### Focus
CI/CD, observability, scaling

### Description
Deployment, monitoring, incident response, and reliability

### Key Topics
- Deployment strategies
- Monitoring and alerting
- Incident response
- Disaster recovery
- Capacity planning
- Cost management
- Performance optimization
- SRE practices

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| OPS-001 | P0 | Deployment automation |
| OPS-002 | P0 | Rollback procedures |
| OPS-003 | P0 | Monitoring coverage |
| OPS-004 | P1 | Alert routing |
| OPS-005 | P1 | On-call rotation |
| OPS-006 | P1 | Incident runbooks |
| OPS-007 | P1 | Post-incident reviews |
| OPS-008 | P2 | Capacity forecasting |

### Deployment Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Blue-green | Two identical environments | Zero-downtime deploys |
| Canary | Gradual rollout | Risk mitigation |
| Rolling | Incremental update | Resource efficiency |
| Feature flags | Toggle features | A/B testing, rollback |

---

## Domain 07: Testing

### Focus
Unit, integration, E2E, regression

### Description
Quality assurance and evaluation strategies

### Key Topics
- Evaluation methodology
- Test design patterns
- Regression testing
- Safety and bias testing
- Performance testing
- Chaos engineering
- Test data management
- Test automation

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| TEST-001 | P0 | Evaluation coverage thresholds |
| TEST-002 | P0 | Regression suite maintenance |
| TEST-003 | P0 | Safety test inclusion |
| TEST-004 | P1 | Performance benchmarks |
| TEST-005 | P1 | Test environment parity |
| TEST-006 | P2 | Test data governance |
| TEST-007 | P2 | Test reporting |
| TEST-008 | P2 | Test automation CI/CD |

### Test Types

| Type | Purpose | Frequency |
|------|---------|-----------|
| Unit | Component correctness | Every commit |
| Integration | Component interaction | Every PR |
| E2E | System behavior | Daily |
| Regression | Prevent breaks | Every release |
| Safety | Harm prevention | Every release |
| Performance | SLO compliance | Weekly |
| Chaos | Resilience | Monthly |

---

## Domain 08: Documentation

### Focus
API docs, runbooks, guides

### Description
Documentation standards and knowledge sharing

### Key Topics
- System documentation
- API documentation
- Runbook creation
- Model cards
- Prompt registers
- Architecture diagrams
- Data flow documentation
- Training materials

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| DOC-001 | P1 | Documentation completeness |
| DOC-002 | P1 | Documentation currency |
| DOC-003 | P1 | Accessibility compliance |
| DOC-004 | P2 | Version control |
| DOC-005 | P2 | Review process |
| DOC-006 | P2 | Publication workflow |
| DOC-007 | P3 | Feedback collection |
| DOC-008 | P3 | Archive management |

### Documentation Types

| Type | Audience | Update Frequency |
|------|----------|------------------|
| System overview | All stakeholders | Quarterly |
| API docs | Developers | Per release |
| Runbooks | Operations | Per change |
| Model cards | All stakeholders | Per model change |
| Prompt registers | Developers | Per prompt change |
| Architecture diagrams | Technical staff | Per architecture change |

---

## Domain 09: Performance

### Focus
Latency, throughput, caching

### Description
Performance, cost, and resource optimization

### Key Topics
- Latency optimization
- Throughput management
- Caching strategies
- Cost optimization
- Resource management
- Load testing
- Capacity planning
- Performance monitoring

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| PERF-001 | P1 | SLO definition and tracking |
| PERF-002 | P1 | Performance budgets |
| PERF-003 | P1 | Cache configuration |
| PERF-004 | P1 | Rate limiting |
| PERF-005 | P2 | Resource limits |
| PERF-006 | P2 | Cost attribution |
| PERF-007 | P2 | Performance testing |
| PERF-008 | P3 | Optimization reviews |

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Latency p50 | < 200ms | Request logging |
| Latency p95 | < 500ms | Request logging |
| Latency p99 | < 1000ms | Request logging |
| Throughput | Per capacity plan | Load testing |
| Error rate | < 0.1% | Request logging |
| Cost per request | Within budget | Cost attribution |

---

## Domain 10: Compliance

### Focus
Governance, risk controls, audit

### Description
Legal, regulatory, ethical, and audit readiness

### Key Topics
- Regulatory compliance
- Audit preparation
- Evidence management
- Exception handling
- Policy enforcement
- Training and awareness
- Vendor compliance
- Risk assessment

### Controls

| Control | Priority | Description |
|---------|----------|-------------|
| COMP-001 | P0 | Compliance assessment |
| COMP-002 | P0 | Evidence collection |
| COMP-003 | P0 | Audit trail maintenance |
| COMP-004 | P1 | Exception register |
| COMP-005 | P1 | Policy documentation |
| COMP-006 | P1 | Training tracking |
| COMP-007 | P2 | Vendor management |
| COMP-008 | P2 | Regulatory monitoring |

### Compliance Requirements

| Regulation | Key Requirements | Evidence |
|------------|------------------|----------|
| GDPR | Consent, DSAR, DPIA, retention | Consent records, DSAR logs, DPIA reports |
| HIPAA | BAA, encryption, audit, breach notification | BAAs, encryption verification, audit logs |
| PCI DSS | Encryption, access control, testing | Encryption configs, access logs, test reports |
| SOC 2 | Security, availability, confidentiality | Control evidence, audit reports |
| EU AI Act | Risk classification, conformity, transparency | Risk assessments, conformity docs |

## Control Priority Matrix

| Domain | P0 Count | P1 Count | P2 Count | P3 Count | Total |
|--------|----------|----------|----------|----------|-------|
| Core | 4 | 4 | 2 | 0 | 10 |
| Security | 5 | 3 | 2 | 0 | 10 |
| Development | 1 | 4 | 3 | 0 | 8 |
| Data | 4 | 3 | 3 | 0 | 10 |
| Integration | 2 | 4 | 2 | 0 | 8 |
| Operations | 3 | 4 | 1 | 0 | 8 |
| Testing | 3 | 2 | 3 | 0 | 8 |
| Documentation | 0 | 3 | 3 | 2 | 8 |
| Performance | 0 | 4 | 3 | 1 | 8 |
| Compliance | 3 | 3 | 2 | 0 | 8 |
| **Total** | **25** | **34** | **24** | **3** | **86** |

## Domain Application Checklist

### For New Systems

- [ ] Identify system type and risk tier
- [ ] Select required domains based on system type
- [ ] Map data flows and identify data classification
- [ ] Identify regulatory requirements
- [ ] Select additional domains based on regulations
- [ ] Create domain-specific control mapping
- [ ] Establish evidence collection requirements
- [ ] Define review cadence by domain
- [ ] Document domain-specific acceptance criteria
- [ ] Plan domain-specific training requirements

### For Existing Systems

- [ ] Audit current implementation against domain checklists
- [ ] Identify gaps in P0 and P1 controls
- [ ] Prioritize gaps based on risk and impact
- [ ] Create remediation plan with timeline
- [ ] Establish evidence collection for gaps
- [ ] Update documentation to reflect current state
- [ ] Schedule regular domain reviews
- [ ] Track exceptions and accepted risks
- [ ] Monitor domain-specific metrics
- [ ] Continuous improvement based on findings

## Cross-Domain Control Mapping

| Control | Domains | Priority | Evidence Type |
|---------|---------|----------|---------------|
| Threat modeling | Security, Core | P0 | Document |
| Input validation | Security, Core | P0 | Code, Test |
| Data classification | Data, Security | P0 | Inventory |
| Retention enforcement | Data, Compliance | P0 | Automated |
| Access control | Security, Integration | P0 | Configuration |
| Evaluation coverage | Testing, Core | P0 | Report |
| Deployment automation | Operations, Development | P0 | CI/CD |
| Rollback procedures | Operations, Core | P0 | Runbook |
| Monitoring coverage | Operations, Security | P0 | Dashboard |
| Audit trail | Compliance, Security | P0 | Logs |
| Documentation | Documentation, All | P1 | Documents |
| Performance SLOs | Performance, Operations | P1 | Metrics |
| Training | Compliance, Security | P1 | Records |
| Vendor assessment | Integration, Compliance | P1 | Report |

## Domain-Specific Metrics

### Core Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| System ownership documented | 100% | Documentation audit |
| Risk tier assigned | 100% | System register |
| Human review implemented | 100% for high-risk | Workflow testing |
| Fallback tested | 100% | Test results |

### Security Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Threat model current | 100% | Review records |
| Vulnerabilities remediated | 100% critical, > 90% high | Scan results |
| Security reviews completed | 100% per release | Review records |
| Incident response tested | Quarterly | Drill results |

### Data Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Data inventory current | 100% | Inventory audit |
| Retention enforced | 100% | Automated checks |
| DSAR response time | < 30 days | Request tracking |
| PII detected and handled | 100% | Scan results |

### Testing Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Evaluation coverage | > 80% | Coverage report |
| Regression suite passing | 100% | Test results |
| Safety tests included | 100% per release | Test review |
| Performance benchmarks | Meeting SLOs | Test results |

### Operations Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Deployment automation | 100% | CI/CD config |
| Rollback tested | Monthly | Drill results |
| Monitoring coverage | > 90% | Dashboard audit |
| Incident response time | < 1 hour | Incident tracking |

### Compliance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Evidence completeness | 100% P0, > 90% P1 | Evidence audit |
| Exception register current | 100% | Register audit |
| Training completion | > 95% | Training records |
| Audit findings resolved | 100% critical | Tracking system |

## Domain Interaction Patterns

### Security-Data Interaction

| Pattern | Description | Controls Required |
|---------|-------------|-------------------|
| Data Classification | Security reviews data sensitivity | SEC-001, DATA-002 |
| Access Control | Security enforces data access rules | SEC-005, DATA-007 |
| Encryption | Security defines encryption requirements | SEC-004, DATA-006 |
| Incident Response | Security coordinates data breach response | SEC-006, DATA-009 |

### Testing-Operations Interaction

| Pattern | Description | Controls Required |
|---------|-------------|-------------------|
| Deployment Testing | Testing validates deployment | TEST-004, OPS-001 |
| Rollback Testing | Testing validates rollback procedures | TEST-005, OPS-002 |
| Monitoring Validation | Testing verifies monitoring coverage | TEST-007, OPS-003 |
| Performance Testing | Testing validates performance SLOs | TEST-004, PERF-001 |

### Documentation-Compliance Interaction

| Pattern | Description | Controls Required |
|---------|-------------|-------------------|
| Evidence Documentation | Documentation supports compliance evidence | DOC-001, COMP-002 |
| Audit Trail | Documentation maintains audit records | DOC-002, COMP-003 |
| Policy Documentation | Documentation captures compliance policies | DOC-001, COMP-005 |
| Training Documentation | Documentation supports compliance training | DOC-001, COMP-006 |

### Integration-Security Interaction

| Pattern | Description | Controls Required |
|---------|-------------|-------------------|
| API Security | Security reviews API design | INT-001, SEC-002 |
| Tool Permissions | Security validates tool permissions | INT-002, SEC-005 |
| Vendor Security | Security assesses vendor security | INT-007, SEC-001 |
| Credential Management | Security manages integration credentials | INT-003, SEC-004 |

## Domain Maturity Model

### Level 1: Initial

- Basic controls implemented
- Ad-hoc processes
- Limited documentation
- Reactive approach
- Minimal monitoring

### Level 2: Managed

- P0 controls implemented
- Documented processes
- Basic documentation
- Proactive approach
- Basic monitoring

### Level 3: Defined

- P0 and P1 controls implemented
- Standardized processes
- Complete documentation
- Strategic approach
- Comprehensive monitoring

### Level 4: Quantitatively Managed

- All P0, P1, and P2 controls implemented
- Measured processes
- Metrics-driven documentation
- Data-driven approach
- Advanced monitoring and analytics

### Level 5: Optimizing

- All controls implemented
- Continuously improving processes
- Living documentation
- Predictive approach
- AI-driven monitoring and optimization

## Domain Assessment Framework

### Assessment Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Control Coverage | 25% | Percentage of required controls implemented |
| Evidence Completeness | 20% | Percentage of required evidence collected |
| Process Maturity | 20% | Maturity level of processes |
| Documentation Quality | 15% | Quality and currency of documentation |
| Metrics Coverage | 10% | Percentage of required metrics tracked |
| Improvement Rate | 10% | Rate of continuous improvement |

### Scoring

| Score | Level | Description |
|-------|-------|-------------|
| 90-100 | Excellent | All controls implemented, evidence complete, mature processes |
| 80-89 | Good | Most controls implemented, evidence mostly complete |
| 70-79 | Adequate | Core controls implemented, basic evidence present |
| 60-69 | Below Standard | Some controls missing, evidence gaps |
| Below 60 | Poor | Significant gaps, immediate improvement needed |

## Domain Selection Decision Tree

```
Start
  │
  ├── Is the system user-facing?
  │     ├── Yes → Add Security, Testing
  │     └── No → Continue
  │
  ├── Does the system process personal data?
  │     ├── Yes → Add Data, Compliance
  │     └── No → Continue
  │
  ├── Does the system make automated decisions?
  │     ├── Yes → Add Testing, Compliance
  │     └── No → Continue
  │
  ├── Is the system high-availability?
  │     ├── Yes → Add Operations, Performance
  │     └── No → Continue
  │
  ├── Is the system in a regulated industry?
  │     ├── Yes → Add Compliance, Documentation
  │     └── No → Continue
  │
  └── Always include Core domain
```
