# Decision Matrix - Comprehensive Reference

## Overview

This document provides decision matrices for various scenarios including risk assessment, control selection, agent selection, domain selection, and prioritization decisions.

## Risk Assessment Matrix

### Risk Scoring

| Impact Dimension | Low (1) | Medium (2) | High (3) | Critical (4) |
|------------------|---------|------------|----------|--------------|
| User harm | Minimal discomfort | Temporary disruption | Lasting impact | Life-threatening |
| Data exposure | Public data only | Internal data disclosed | Confidential data disclosed | Restricted or sensitive data exposed |
| Financial impact | < $10K | $10K - $100K | $100K - $1M | > $1M |
| Reputational impact | Minor internal issue | Customer complaint | Media coverage | Regulatory investigation |
| Legal exposure | Contractual risk | Regulatory warning | Regulatory fine | Criminal liability |
| Operational impact | No impact | Minor degradation | Significant degradation | Complete outage |
| Safety impact | No impact | Minor risk | Significant risk | Critical risk |
| Compliance impact | No impact | Warning | Fine | License revocation |

### Risk Score Calculation

```
Risk Score = Sum of all dimension scores

Score Ranges:
- Low Risk: 1-8 points
- Medium Risk: 9-16 points
- High Risk: 17-24 points
- Critical Risk: 25+ points
```

### Risk Tier Assignment

| Risk Score | Risk Tier | Required Controls | Review Cadence |
|------------|-----------|-------------------|----------------|
| 1-8 | Low | Basic P0 controls | Annually |
| 9-16 | Medium | P0 + P1 controls | Semi-annually |
| 17-24 | High | All P0 + P1 + P2 controls | Quarterly |
| 25+ | Critical | All controls + enhanced | Monthly |

### Risk Assessment Example

```
System: Customer Support Assistant

Impact Assessment:
- User harm: Medium (2) - Temporary disruption possible
- Data exposure: High (3) - Customer PII exposed
- Financial impact: Low (1) - <$10K impact
- Reputational impact: Medium (2) - Customer complaints possible
- Legal exposure: Medium (2) - GDPR applicable
- Operational impact: Low (1) - No critical operations
- Safety impact: Low (1) - No physical safety
- Compliance impact: Medium (2) - GDPR fines possible

Total Score: 14
Risk Tier: Medium
Required Controls: P0 + P1
Review Cadence: Semi-annually
```

## Domain Selection Matrix

### By System Type

| System Type | Core | Security | Development | Data | Integration | Operations | Testing | Documentation | Performance | Compliance |
|-------------|------|----------|-------------|------|-------------|------------|---------|---------------|-------------|------------|
| Customer-facing assistant | ✓ | ✓ | ○ | ✓ | ○ | ✓ | ✓ | ○ | ○ | ✓ |
| Internal agent automation | ✓ | ○ | ✓ | ○ | ✓ | ✓ | ✓ | ○ | ○ | ○ |
| High-volume AI API | ✓ | ✓ | ○ | ○ | ✓ | ✓ | ✓ | ○ | ✓ | ✓ |
| Healthcare AI system | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Financial AI system | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Research/prototyping | ✓ | ○ | ○ | ○ | ○ | ○ | ✓ | ○ | ○ | ○ |
| Simple chatbot | ✓ | ○ | ○ | ○ | ○ | ○ | ✓ | ○ | ○ | ○ |
| Enterprise platform | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

✓ = Required, ○ = Recommended

### By Risk Tier

| Risk Tier | Core | Security | Development | Data | Integration | Operations | Testing | Documentation | Performance | Compliance |
|-----------|------|----------|-------------|------|-------------|------------|---------|---------------|-------------|------------|
| Low | ✓ | ○ | ○ | ○ | ○ | ○ | ✓ | ○ | ○ | ○ |
| Medium | ✓ | ✓ | ○ | ✓ | ○ | ✓ | ✓ | ○ | ○ | ✓ |
| High | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Critical | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### By Regulatory Requirements

| Regulation | Core | Security | Development | Data | Integration | Operations | Testing | Documentation | Performance | Compliance |
|------------|------|----------|-------------|------|-------------|------------|---------|---------------|-------------|------------|
| GDPR | ✓ | ✓ | ○ | ✓ | ○ | ○ | ○ | ✓ | ○ | ✓ |
| HIPAA | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ○ | ✓ |
| PCI DSS | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ○ | ✓ |
| SOC 2 | ✓ | ✓ | ○ | ○ | ○ | ✓ | ✓ | ✓ | ○ | ✓ |
| EU AI Act | ✓ | ✓ | ○ | ✓ | ○ | ○ | ✓ | ✓ | ○ | ✓ |
| CCPA/CPRA | ✓ | ✓ | ○ | ✓ | ○ | ○ | ○ | ✓ | ○ | ✓ |

## Agent Selection Matrix

### By Activity

| Activity | Primary Agent | Supporting Agents |
|----------|---------------|-------------------|
| System design | Architect | Security, Compliance, Data Steward |
| Feature implementation | Implementer | Documentation, Data Steward |
| Code review | Reviewer | Eval, Compliance |
| Security review | Security | Compliance |
| Data governance | Data Steward | Compliance |
| Evaluation execution | Eval | - |
| Release decision | Release Gate | Compliance, Tracker |
| Monitoring setup | Tracker | - |
| Policy enforcement | Enforcer | Tracker |
| Documentation | Documentation | - |
| Incident response | Enforcer, Tracker | Documentation |
| Compliance audit | Compliance | All agents as needed |
| Workflow coordination | Orchestrator | All agents |

### By System Phase

| Phase | Required Agents | Optional Agents |
|-------|-----------------|-----------------|
| Design | Architect | Security, Compliance, Data Steward |
| Implementation | Implementer | Documentation, Data Steward |
| Review | Reviewer | Eval, Compliance, Security |
| Release | Release Gate | Compliance, Tracker |
| Operations | Tracker, Enforcer | Documentation |
| Incident Response | Enforcer, Tracker | Documentation, Orchestrator |

### By Risk Tier

| Risk Tier | Minimum Agents | Full Agent Set |
|-----------|----------------|----------------|
| Low | Architect, Implementer, Reviewer | Architect, Implementer, Reviewer, Tracker |
| Medium | Architect, Implementer, Reviewer, Release Gate, Tracker | All except Orchestrator, Security |
| High | All 12 agents | All 12 agents |

## Control Priority Matrix

### By Domain and Priority

| Domain | P0 Controls | P1 Controls | P2 Controls | P3 Controls |
|--------|-------------|-------------|-------------|-------------|
| Core | CORE-001 to CORE-004 | CORE-005 to CORE-008 | CORE-009 to CORE-010 | - |
| Security | SEC-001 to SEC-005 | SEC-006 to SEC-008 | SEC-009 to SEC-010 | - |
| Development | DEV-001 | DEV-002 to DEV-005 | DEV-006 to DEV-008 | - |
| Data | DATA-001 to DATA-004 | DATA-005 to DATA-007 | DATA-008 to DATA-010 | - |
| Integration | INT-001 to INT-002 | INT-003 to INT-006 | INT-007 to INT-008 | - |
| Operations | OPS-001 to OPS-003 | OPS-004 to OPS-007 | OPS-008 | - |
| Testing | TEST-001 to TEST-003 | TEST-004 to TEST-005 | TEST-006 to TEST-008 | - |
| Documentation | - | DOC-001 to DOC-003 | DOC-004 to DOC-006 | DOC-007 to DOC-008 |
| Performance | - | PERF-001 to PERF-004 | PERF-005 to PERF-007 | PERF-008 |
| Compliance | COMP-001 to COMP-003 | COMP-004 to COMP-006 | COMP-007 to COMP-008 | - |

### By Control Type

| Control Type | P0 Count | P1 Count | P2 Count | P3 Count |
|--------------|----------|----------|----------|----------|
| Preventive | 15 | 12 | 8 | 1 |
| Detective | 8 | 10 | 10 | 2 |
| Corrective | 2 | 12 | 6 | 0 |
| **Total** | **25** | **34** | **24** | **3** |

### By Implementation Effort

| Effort Level | P0 Controls | P1 Controls | P2 Controls | P3 Controls |
|--------------|-------------|-------------|-------------|-------------|
| Low (< 1 day) | 5 | 8 | 10 | 2 |
| Medium (1-5 days) | 10 | 15 | 10 | 1 |
| High (5-20 days) | 8 | 10 | 4 | 0 |
| Very High (> 20 days) | 2 | 1 | 0 | 0 |

## Finding Severity Matrix

### Severity Classification

| Severity | Description | Response Time | Resolution Time | Escalation |
|----------|-------------|---------------|-----------------|------------|
| P0 | Blocking issue, must fix before release | Immediate | Before release | Release Gate → CISO |
| P1 | Serious issue, must fix within deadline | 24 hours | 7 days | Reviewer → System Owner |
| P2 | Improvement, fix recommended | 1 week | 30 days | Reviewer → System Owner |
| P3 | Informational, note for future | Next sprint | Backlog | Reviewer → Documentation |

### Severity by Domain

| Domain | Common P0 | Common P1 | Common P2 |
|--------|-----------|-----------|-----------|
| Core | Missing human review for high-risk | Risk tier not justified | Scope not clearly documented |
| Security | Missing authentication | Weak secret rotation | Incomplete security headers |
| Data | PII leakage | Incomplete classification | Missing data quality checks |
| Integration | Tool boundary violation | Missing timeout configuration | Documentation gap |
| Operations | Missing rollback | Alerting not configured | Runbook missing detail |
| Testing | Evaluation failure | Missing prompt injection test | Test coverage below 80% |
| Documentation | Missing model card | Outdated architecture diagram | Missing runbook |
| Performance | Latency exceeds SLO | Cost exceeds budget | Missing performance test |
| Compliance | Missing exception register | Outdated vendor register | Missing evidence |

### Finding Impact Assessment

| Impact | User Impact | Data Impact | Business Impact | Technical Impact |
|--------|-------------|-------------|-----------------|------------------|
| Critical | Service outage for all users | Data breach with PII | Revenue loss > $100K | System compromise |
| High | Service degradation for users | Data exposure internal | Revenue loss $10K-100K | Significant technical debt |
| Medium | Feature unavailable | Data quality issues | Revenue loss < $10K | Maintainability issues |
| Low | Minor inconvenience | No data impact | No revenue impact | Code quality issues |

## Evidence Type Matrix

### By Evidence Source

| Source | Type | Automation | Reliability | Cost |
|--------|------|------------|-------------|------|
| CI/CD pipeline | Automated | Full | High | Low |
| Evaluation harness | Automated | Full | High | Low |
| Security scanner | Automated | Full | High | Low |
| Monitoring system | Automated | Full | High | Medium |
| Manual review | Manual | None | High | High |
| Audit assessment | Manual | None | High | Very High |
| Penetration test | Manual | None | High | Very High |
| Training records | Semi-automated | Partial | Medium | Medium |
| Vendor attestation | Manual | None | Medium | Medium |
| Legal review | Manual | None | High | Very High |

### By Evidence Retention

| Evidence Type | Minimum Retention | Storage | Access |
|---------------|-------------------|---------|--------|
| Security review | 12 months | Evidence store | Security team |
| Penetration test | 12 months | Evidence store | Security team |
| Vulnerability scan | 30 days | CI/CD artifacts | Engineering team |
| Evaluation report | Per release | Evidence store | Release team |
| Privacy review | 12 months | Evidence store | Compliance team |
| Threat model | 12 months | Evidence store | Security team |
| DPA | Per vendor contract | Compliance store | Legal team |
| Training completion | 12 months | HR/LMS system | HR team |
| Audit report | 7 years | Compliance store | Compliance team |
| Incident report | 7 years | Evidence store | Security team |

### By Evidence Validation

| Validation Method | Frequency | Responsible | Criteria |
|-------------------|-----------|-------------|----------|
| Link resolution | Daily | Automated | Link resolves to valid resource |
| Content freshness | Weekly | Automated | Content within policy window |
| Signature verification | Daily | Automated | Digital signature valid |
| Completeness check | Per release | Compliance Auditor | All required evidence present |
| Accuracy verification | Quarterly | Subject matter expert | Content accurate and current |
| Accessibility check | Quarterly | Documentation Agent | Meets accessibility standards |

## Release Decision Matrix

### Decision Criteria

| Criterion | Pass | Conditional Pass | Block |
|-----------|------|------------------|-------|
| P0 controls | All have evidence | - | Any missing |
| P1 controls | All have evidence | Minor gaps with mitigations | Major gaps |
| Evidence links | All resolve | Minor broken links | Major broken links |
| Evaluation suite | Passing | Minor failures with mitigation | Major failures |
| Security review | Complete | Minor findings with plan | Critical findings |
| Privacy review | Complete | Minor findings with plan | Critical findings |
| Rollback plan | Tested | Tested in staging | Not tested |
| Monitoring | Configured | Partially configured | Not configured |
| Exception register | Current | Minor exceptions | Expired/ownerless exceptions |
| Vendor DPA | Current | Pending renewal | Expired/missing |

### Decision Process

```
Release Request Received
    │
    ▼
Evidence Validation
    │
    ├── All P0 evidence present ──── Continue
    │
    └── P0 evidence missing ──────── Block
    │
    ▼
P1 Control Assessment
    │
    ├── All P1 evidence present ──── Continue
    │
    ├── Minor P1 gaps ───────────── Conditional Pass
    │
    └── Major P1 gaps ───────────── Block
    │
    ▼
Evaluation Status
    │
    ├── Evaluation passing ───────── Continue
    │
    ├── Minor failures ──────────── Conditional Pass
    │
    └── Major failures ──────────── Block
    │
    ▼
Final Assessment
    │
    ├── All criteria met ─────────── Pass
    │
    ├── Minor gaps with mitigations ─ Conditional Pass
    │
    └── Any blocking item ─────────── Block
```

## Exception Management Matrix

### Exception Types

| Type | Description | Max Duration | Approval Required |
|------|-------------|--------------|-------------------|
| Technical limitation | Cannot implement control due to technical constraint | 90 days | Domain owner |
| Resource constraint | Cannot allocate resources for control | 90 days | Domain owner |
| Vendor dependency | Control depends on vendor capability | 180 days | Compliance |
| Regulatory ambiguity | Unclear regulatory requirement | 180 days | Legal |
| Experimental design | Testing new approach | 30 days | Architect |
| Legacy system | Existing system cannot support control | 365 days | CISO |

### Exception Risk Matrix

| Residual Risk | P0 Control | P1 Control | P2 Control |
|---------------|------------|------------|------------|
| Low | Requires CISO approval + compensating controls | Requires domain owner approval | Requires documentation |
| Medium | Requires CISO approval + enhanced monitoring | Requires compliance approval | Requires domain owner approval |
| High | Not permitted | Requires CISO approval | Requires compliance approval |
| Critical | Not permitted | Not permitted | Requires CISO approval |

### Exception Lifecycle

```
Exception Requested
    │
    ▼
Risk Assessment
    │
    ├── Residual Risk Low ────────── Approve with conditions
    │
    ├── Residual Risk Medium ──────── Approve with enhanced controls
    │
    ├── Residual Risk High ────────── Escalate to CISO
    │
    └── Residual Risk Critical ────── Reject
    │
    ▼
Exception Granted
    │
    ├── Monitor compliance ────────── Monthly review
    │
    ├── Track expiration ──────────── 30-day reminder
    │
    └── Renewal decision ──────────── Before expiration
```

## Escalation Matrix

### By Issue Type

| Issue Type | First Contact | Second Contact | Final Escalation | SLA |
|------------|---------------|----------------|------------------|-----|
| ADR disagreement | Engineering lead | Architecture review board | Governance committee | 48 hours |
| Exception approval | Domain owner | Compliance officer | CISO | 24 hours |
| Control gap in high-risk | Compliance | CISO | CEO / Board | 4 hours |
| Test failure blocking release | Engineering lead | Release Gate Agent | Product owner | 24 hours |
| Budget overrun for controls | Engineering lead | Finance | CFO approval | 1 week |
| Security incident | Security team | CISO | Executive team | Immediate |
| Compliance violation | Compliance | Legal | Regulatory notification | 24 hours |
| Data breach | Data Steward | DPO | Legal, Executive | Immediate |

### By Severity

| Severity | First Response | Escalation Path | Resolution Target |
|----------|----------------|-----------------|-------------------|
| Critical | Immediate | On-call → Manager → Executive | 4 hours |
| High | 15 minutes | On-call → Manager | 24 hours |
| Medium | 1 hour | On-call | 72 hours |
| Low | 4 hours | Team lead | 1 week |
| Informational | Next business day | Team | Next sprint |

## Prioritization Matrix

### Effort vs Impact

| | Low Effort | Medium Effort | High Effort |
|---|------------|---------------|-------------|
| **High Impact** | Do First | Schedule | Plan Carefully |
| **Medium Impact** | Do Next | Evaluate | Consider |
| **Low Impact** | Do When Ready | Defer | Don't Do |

### Urgency vs Importance

| | Not Urgent | Urgent |
|---|------------|--------|
| **Important** | Schedule | Do First |
| **Not Important** | Delegate | Do If Time |

### Risk vs Cost

| | Low Cost | High Cost |
|---|----------|-----------|
| **High Risk** | Implement Immediately | Plan Implementation |
| **Low Risk** | Implement When Ready | Accept Risk |

## Resource Allocation Matrix

### By Agent Type

| Agent | Primary Resources | Secondary Resources | Budget Impact |
|-------|-------------------|---------------------|---------------|
| Architect | Design tools, documentation | Collaboration platforms | Low |
| Implementer | Development environment, CI/CD | Testing infrastructure | Medium |
| Reviewer | Review tools, testing environment | Documentation platforms | Low |
| Release Gate | Decision support tools | Monitoring dashboards | Low |
| Eval | Evaluation harness, datasets | Compute resources | Medium |
| Compliance | Evidence management, audit tools | Legal review | Medium |
| Data Steward | Data governance tools | Privacy review | Low |
| Enforcer | Monitoring tools, alerting | Incident response | Medium |
| Documentation | Documentation platforms | Diagramming tools | Low |
| Tracker | Monitoring tools, dashboards | Analytics platforms | Medium |
| Orchestrator | Workflow tools | Coordination platforms | Low |
| Security | Security tools, scanning | Penetration testing | High |

### By System Phase

| Phase | Resource Allocation | Duration | Team Size |
|-------|---------------------|----------|-----------|
| Design | Architecture, security, compliance review | 1-4 weeks | 3-5 people |
| Implementation | Development, testing, documentation | 2-8 weeks | 3-10 people |
| Review | Code review, evaluation, security review | 1-2 weeks | 2-5 people |
| Release | Evidence validation, decision support | 1-3 days | 2-4 people |
| Operations | Monitoring, incident response | Ongoing | 2-4 people |

## Quality Gate Matrix

### By Gate Type

| Gate | Criteria | Blocking | Evidence Required |
|------|----------|----------|-------------------|
| Design Gate | Architecture approved, risk tier assigned | Yes | ADR, risk assessment |
| Implementation Gate | Code complete, tests passing | Yes | Code, test results |
| Review Gate | All findings addressed, no P0/P1 | Yes | Review report |
| Release Gate | All controls have evidence | Yes | Evidence package |
| Deployment Gate | Deployment successful, monitoring active | Yes | Deployment log |
| Post-Release Gate | 24-hour metrics stable | No | Metrics report |

### Gate Progression

```
Design Gate
    │
    ├── Approved ──── Implementation
    │
    └── Rejected ──── Redesign
    │
    ▼
Implementation Gate
    │
    ├── Passed ────── Review
    │
    └── Failed ────── Fix Issues
    │
    ▼
Review Gate
    │
    ├── Pass ──────── Release
    │
    ├── Conditional ── Release with Monitoring
    │
    └── Block ──────── Remediation
    │
    ▼
Release Gate
    │
    ├── Pass ──────── Deploy
    │
    ├── Conditional ── Deploy with Monitoring
    │
    └── Block ──────── Remediation
    │
    ▼
Deployment Gate
    │
    ├── Success ────── Production
    │
    └── Failure ────── Rollback
    │
    ▼
Post-Release Gate
    │
    ├── Stable ────── Closure
    │
    └── Issues ────── Investigation
```

## Trade-off Matrix

### Security vs Usability

| Security Level | Usability Impact | Use Case |
|----------------|------------------|----------|
| Maximum | High friction | Financial, healthcare |
| High | Moderate friction | Customer-facing, enterprise |
| Medium | Low friction | Internal tools, automation |
| Low | Minimal friction | Research, prototyping |

### Performance vs Cost

| Performance Level | Cost Impact | Use Case |
|-------------------|-------------|----------|
| Maximum | Very high | Real-time, latency-critical |
| High | High | Customer-facing, interactive |
| Medium | Moderate | Internal tools, batch processing |
| Low | Low | Background tasks, non-urgent |

### Automation vs Control

| Automation Level | Control Impact | Use Case |
|------------------|----------------|----------|
| Full automation | Less human oversight | Low-risk, high-volume |
| Semi-automation | Human review for edge cases | Medium-risk, moderate-volume |
| Manual with automation | Human decision, automated support | High-risk, low-volume |
| Full manual | Complete human control | Critical, regulatory |

### Speed vs Quality

| Speed Priority | Quality Impact | Use Case |
|----------------|----------------|----------|
| Maximum speed | Accept technical debt | Emergency, hotfix |
| Fast | Managed technical debt | Feature development, iteration |
| Balanced | Controlled quality | Standard development |
| Maximum quality | Slower delivery | Compliance, security-critical |

## Technology Selection Matrix

### Model Provider Selection

| Criterion | Weight | OpenAI | Anthropic | Google | Open Source |
|-----------|--------|--------|-----------|--------|-------------|
| Quality | 25% | High | High | High | Variable |
| Cost | 20% | Medium | Medium | Medium | Low |
| Latency | 15% | Low | Low | Low | Variable |
| Security | 15% | High | High | High | Variable |
| Compliance | 15% | High | High | High | Variable |
| Support | 10% | High | High | Medium | Low |

### Vector Database Selection

| Criterion | Weight | Pinecone | Weaviate | Chroma | pgvector |
|-----------|--------|----------|----------|--------|----------|
| Scalability | 25% | High | High | Medium | Medium |
| Performance | 25% | High | High | Medium | Medium |
| Cost | 20% | Medium | Medium | Low | Low |
| Features | 15% | High | High | Medium | Medium |
| Operations | 15% | Managed | Self-hosted | Self-hosted | Self-hosted |

### Monitoring Tool Selection

| Criterion | Weight | Datadog | Grafana | Prometheus | Custom |
|-----------|--------|---------|---------|------------|--------|
| Features | 25% | High | High | Medium | Variable |
| Cost | 25% | High | Low | Low | Low |
| Ease of Use | 20% | High | Medium | Low | Low |
| Scalability | 15% | High | High | High | Variable |
| Integration | 15% | High | High | High | Variable |

## Process Selection Matrix

### Incident Response Process

| Incident Type | Response Time | Team Size | Escalation | Documentation |
|---------------|---------------|-----------|------------|---------------|
| Critical Security | Immediate | 5+ | CISO, Executive | Full post-mortem |
| High Security | 15 minutes | 3-5 | Security Lead | Post-mortem |
| Medium Availability | 1 hour | 2-3 | On-call Lead | Incident report |
| Low Performance | 4 hours | 1-2 | Team Lead | Ticket |

### Release Process

| Release Type | Approval Required | Testing Level | Documentation | Rollback Plan |
|--------------|-------------------|---------------|---------------|---------------|
| Major | Full review | Complete | Full | Required |
| Minor | Technical review | Standard | Updated | Required |
| Patch | Automated | Minimal | Changelog | Required |
| Emergency | Expedited | Critical | Post-release | Required |

### Review Process

| Review Type | Reviewers | Duration | Depth | Blocking |
|-------------|-----------|----------|-------|----------|
| Architecture | Architect, Security, Compliance | 1-2 weeks | Deep | Yes |
| Code | 2+ engineers | 1-2 days | Standard | Yes |
| Security | Security team | 3-5 days | Deep | Yes |
| Compliance | Compliance team | 1-2 weeks | Standard | Yes |

## Resource Allocation Matrix

### Team Size by System Complexity

| Complexity | Design | Implementation | Review | Operations |
|------------|--------|----------------|--------|------------|
| Simple | 1-2 | 2-3 | 1-2 | 1 |
| Medium | 2-3 | 3-5 | 2-3 | 2 |
| Complex | 3-5 | 5-10 | 3-5 | 3-5 |
| Enterprise | 5+ | 10+ | 5+ | 5+ |

### Budget Allocation by Phase

| Phase | Percentage | Activities |
|-------|------------|------------|
| Design | 15% | Architecture, planning, reviews |
| Implementation | 40% | Development, testing, documentation |
| Review | 15% | Code review, security review, compliance |
| Operations | 20% | Monitoring, incident response, maintenance |
| Improvement | 10% | Training, optimization, framework updates |

## Success Criteria Matrix

### System Success Criteria

| Criterion | Measurement | Target | Frequency |
|-----------|-------------|--------|-----------|
| Availability | Uptime monitoring | 99.9% | Continuous |
| Performance | Latency monitoring | p95 < 500ms | Continuous |
| Quality | Evaluation scores | > 0.85 | Per release |
| Security | Vulnerability count | 0 critical | Daily |
| Compliance | Audit findings | 0 critical | Quarterly |
| Cost | Budget utilization | < 100% | Monthly |
| User Satisfaction | Feedback scores | > 4.0/5.0 | Monthly |

### Project Success Criteria

| Criterion | Measurement | Target | Frequency |
|-----------|-------------|--------|-----------|
| On Time | Delivery date vs planned | Within 10% | Per milestone |
| On Budget | Actual vs planned cost | Within 10% | Monthly |
| Quality | Defect rate | < 5 per release | Per release |
| Adoption | User adoption rate | > 80% target | Monthly |
| Satisfaction | Stakeholder satisfaction | > 4.0/5.0 | Quarterly |

## Risk Response Matrix

### Risk Response Strategies

| Risk Level | Strategy | Actions |
|------------|----------|---------|
| Critical | Avoid | Eliminate the risk activity |
| High | Mitigate | Implement controls to reduce risk |
| Medium | Transfer | Shift risk to third party (insurance, vendor) |
| Low | Accept | Accept the risk with monitoring |

### Risk Response by Category

| Risk Category | Avoid | Mitigate | Transfer | Accept |
|---------------|-------|----------|----------|--------|
| Security | Stop feature | Implement controls | Cyber insurance | Low-risk only |
| Compliance | Exit market | Implement controls | Legal counsel | De minimis |
| Performance | Reduce scope | Optimize | CDN guarantee | Within tolerance |
| Cost | Reduce features | Optimize | Fixed-price contract | Within budget |
| Quality | Reduce scope | Improve testing | Warranty | Within tolerance |

## Decision Documentation Matrix

### Documentation Requirements by Decision Type

| Decision Type | Required Documents | Review Required | Approval Required |
|---------------|-------------------|-----------------|-------------------|
| Architecture | ADR, Design Doc | Yes | Yes |
| Security | Threat Model, Security Review | Yes | Yes |
| Compliance | Compliance Assessment, Evidence | Yes | Yes |
| Technology | Evaluation Report, Selection Rationale | Yes | Yes |
| Process | Process Document, Training Materials | Yes | No |
| Configuration | Configuration Doc, Change Log | No | No |

### Documentation Retention by Type

| Document Type | Retention Period | Storage | Access |
|---------------|------------------|---------|--------|
| ADR | Life of system | Version control | Team |
| Threat Model | 12 months or until change | Evidence store | Security |
| Compliance Evidence | 7 years | Compliance store | Compliance |
| Incident Reports | 7 years | Evidence store | Security |
| Evaluation Reports | Per release | Evidence store | Team |
| Training Records | 12 months | HR/LMS | HR |
| Design Documents | Life of system | Version control | Team |
| Review Reports | 3 years | Evidence store | Team |
| Vendor Assessments | Duration of contract + 1 year | Compliance store | Compliance |
| Audit Reports | 7 years | Compliance store | Compliance |

## Quick Reference Summary

### Most Common Decisions

| Decision | Primary Matrix | Supporting Matrices |
|----------|----------------|---------------------|
| Risk tier assignment | Risk Assessment Matrix | Domain Selection Matrix |
| Domain selection | Domain Selection Matrix | Risk Assessment Matrix |
| Agent selection | Agent Selection Matrix | Domain Selection Matrix |
| Control priority | Control Priority Matrix | Risk Assessment Matrix |
| Finding severity | Finding Severity Matrix | Escalation Matrix |
| Release decision | Release Decision Matrix | Exception Management Matrix |
| Exception approval | Exception Management Matrix | Risk Assessment Matrix |
| Escalation | Escalation Matrix | Severity Matrix |

### Decision Workflow

```
Identify Decision Need
    │
    ├── Select Appropriate Matrix
    │
    ├── Gather Required Information
    │
    ├── Apply Matrix Criteria
    │
    ├── Document Decision
    │
    ├── Get Required Approvals
    │
    └── Implement and Monitor
```
