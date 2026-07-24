# Checklist Templates - Comprehensive Collection

## Overview

This document provides complete checklist templates for all domains, release processes, and operational activities.

## Release Checklist

### Pre-Release Checklist

#### P0 Critical Controls

- [ ] System register entry complete and current
- [ ] Risk tier assigned and justified
- [ ] All P0 controls have complete evidence
- [ ] Human review implemented for high-risk workflows
- [ ] Fallback and rollback plan tested
- [ ] Security review completed and signed
- [ ] Privacy review completed
- [ ] Threat model current for security-relevant changes
- [ ] Data inventory current for data source changes
- [ ] Evaluation suite passing for candidate version
- [ ] No outstanding critical incidents affecting the system
- [ ] Exception register reviewed for expired or ownerless entries

#### P1 High Priority Controls

- [ ] All P1 controls have evidence or documented exceptions
- [ ] Architecture decision records current for material changes
- [ ] Vulnerability scan current
- [ ] Penetration test current if required by risk tier
- [ ] Secret management verified
- [ ] Network controls reviewed
- [ ] Monitoring and alerting configured
- [ ] Rollback procedure tested in staging
- [ ] Runbooks updated
- [ ] Training assignments current
- [ ] Vendor and DPA records current
- [ ] Post-release review scheduled for high-risk releases

#### P2 Medium Priority Controls

- [ ] Documentation updated
- [ ] Model card current
- [ ] Prompt register updated
- [ ] Tool catalog updated
- [ ] Architecture diagrams updated
- [ ] Data flow diagrams updated if applicable
- [ ] API documentation current
- [ ] Change log maintained
- [ ] Performance benchmarks passing
- [ ] Cost impact acceptable

### Evidence Package Checklist

- [ ] Evaluation report for candidate version
- [ ] Security review record
- [ ] Privacy review record
- [ ] Threat model review record
- [ ] Vulnerability scan results
- [ ] Penetration test summary if required
- [ ] Data inventory and classification
- [ ] Data flow diagram if required
- [ ] Retention schedule and purge evidence
- [ ] Legal hold validation if required
- [ ] Consent or legal basis documentation
- [ ] Tool inventory and permission review
- [ ] API versioning and compatibility review
- [ ] MCP boundary review if applicable
- [ ] Vendor contracts and DPAs current
- [ ] Deployment runbook
- [ ] Rollback runbook
- [ ] Monitoring and alerting configuration
- [ ] On-call and escalation contacts
- [ ] Incident response plan
- [ ] Training completion records
- [ ] Exception register current
- [ ] Compliance risk assessment updated

### Release Decision Checklist

- [ ] Evidence package validated
- [ ] All P0 evidence present and valid
- [ ] All P1 evidence addressed
- [ ] Evidence links resolve and are versioned
- [ ] Evaluation thresholds aligned with risk tier
- [ ] Exception register reviewed for expiration
- [ ] Post-release review scheduled
- [ ] Communication plan defined
- [ ] Rollback decision owner identified
- [ ] Decision rationale documented
- [ ] Stakeholder notification sent

### Post-Release Checklist

#### 24-Hour Review

- [ ] Evaluation metrics stable
- [ ] No policy violations detected
- [ ] No security incidents detected
- [ ] Performance within SLO
- [ ] Cost within budget
- [ ] User feedback normal
- [ ] No unexpected tool invocations
- [ ] Audit logging functioning

#### 72-Hour Review

- [ ] Evaluation metrics trend acceptable
- [ ] Exception conditions monitored
- [ ] Post-release testing results reviewed
- [ ] User feedback assessed
- [ ] Incident review conducted if applicable
- [ ] Training completion verified
- [ ] Vendor performance within SLA
- [ ] Evidence package complete

#### 30-Day Review

- [ ] Full evaluation re-run completed or scheduled
- [ ] Compliance metrics reviewed
- [ ] Exception status reviewed
- [ ] Post-release incidents reviewed
- [ ] Lessons learned documented
- [ ] Control improvements identified
- [ ] Follow-up actions closed or rescheduled
- [ ] Metrics reported to stakeholders

## Security Review Checklist

### Architecture Review

- [ ] Threat model complete and current
- [ ] Security architecture documented
- [ ] Trust boundaries defined
- [ ] Data flow security reviewed
- [ ] Component security boundaries defined
- [ ] Third-party integration security reviewed
- [ ] Authentication mechanism appropriate for risk tier
- [ ] Authorization model defined and documented
- [ ] Least privilege enforced
- [ ] Secret management implemented

### Authentication Review

- [ ] Authentication mechanism appropriate for risk tier
- [ ] Multi-factor authentication implemented where required
- [ ] Session management secure
- [ ] Token validation implemented
- [ ] Password policy enforced
- [ ] API key management implemented
- [ ] OAuth/OIDC implementation reviewed
- [ ] SSO integration security verified

### Authorization Review

- [ ] Authorization model defined and documented
- [ ] Least privilege enforced
- [ ] Role and permission management implemented
- [ ] Access control boundaries verified
- [ ] Administrative access secured
- [ ] Tool permissions scoped appropriately
- [ ] Data access control verified
- [ ] Cross-service authorization reviewed

### Secret Management Review

- [ ] Secrets stored securely
- [ ] Secret rotation implemented
- [ ] Secret access controlled
- [ ] Secret encryption verified
- [ ] Secret audit logging configured
- [ ] Emergency revocation procedure documented
- [ ] Secret lifecycle management implemented
- [ ] Secret transmission security verified

### Network Security Review

- [ ] Network segmentation implemented
- [ ] TLS enforced for all communications
- [ ] Certificate management configured
- [ ] Firewall rules reviewed
- [ ] API gateway configured
- [ ] DDoS protection enabled
- [ ] DNS security configured
- [ ] Network monitoring implemented

### Data Security Review

- [ ] Encryption at rest implemented
- [ ] Encryption in transit verified
- [ ] Key management configured
- [ ] Data masking implemented where required
- [ ] PII protection verified
- [ ] Data retention enforced
- [ ] Backup security verified
- [ ] Data disposal procedures documented

### Application Security Review

- [ ] Input validation implemented
- [ ] Output encoding implemented
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection implemented
- [ ] Security headers configured
- [ ] Error handling secure
- [ ] Logging secure and complete

### Prompt Security Review

- [ ] Prompt injection defenses implemented
- [ ] Content filtering configured
- [ ] Output safety validation implemented
- [ ] System prompt isolation verified
- [ ] Jailbreak detection configured
- [ ] Safety guardrails tested
- [ ] Prompt version control implemented
- [ ] Prompt audit logging configured

### Tool Security Review

- [ ] Tool permissions scoped appropriately
- [ ] Tool credentials isolated
- [ ] Tool call auditing configured
- [ ] Tool rate limiting implemented
- [ ] Tool timeout configured
- [ ] Tool fallback behavior defined
- [ ] Tool input validation implemented
- [ ] Tool output handling secure

### Monitoring Security Review

- [ ] Security logging configured
- [ ] Audit trail complete
- [ ] Anomaly detection configured
- [ ] Alert routing configured
- [ ] Incident response procedures documented
- [ ] Forensics capability available
- [ ] Security monitoring dashboards configured
- [ ] Security metrics tracked

## Data Governance Checklist

### Data Inventory

- [ ] Data sources identified and documented
- [ ] Data types classified
- [ ] Data sensitivity labeled
- [ ] Data owners assigned
- [ ] Data processors identified
- [ ] Data flows documented
- [ ] Cross-border transfers identified
- [ ] Retention requirements defined

### Privacy and PII

- [ ] PII elements identified
- [ ] PII detection scanning implemented
- [ ] PII minimization implemented
- [ ] Consent management implemented
- [ ] Purpose limitation enforced
- [ ] Data subject request handling ready
- [ ] Privacy notice updated
- [ ] DPIA completed if required

### Retention and Legal Hold

- [ ] Retention schedule defined
- [ ] Retention enforcement implemented
- [ ] Legal hold support verified
- [ ] Purge procedures documented
- [ ] Archive procedures documented
- [ ] Retention monitoring configured
- [ ] Retention exceptions documented
- [ ] Retention audit trail maintained

### Data Quality

- [ ] Data quality rules defined
- [ ] Data validation implemented
- [ ] Data quality monitoring configured
- [ ] Data quality alerts configured
- [ ] Data quality remediation procedures documented
- [ ] Data quality metrics tracked
- [ ] Data quality reporting implemented
- [ ] Data quality improvement process defined

### Data Access

- [ ] Access control implemented
- [ ] Access logging configured
- [ ] Access reviews scheduled
- [ ] Access recertification process defined
- [ ] Privileged access monitored
- [ ] Access anomalies detected
- [ ] Access incident response defined
- [ ] Access metrics tracked

## Testing Checklist

### Evaluation Coverage

- [ ] Evaluation policy defined
- [ ] Evaluation datasets maintained
- [ ] Evaluation harness configured
- [ ] Evaluation thresholds defined
- [ ] Evaluation automation implemented
- [ ] Evaluation reporting configured
- [ ] Evaluation regression detection implemented
- [ ] Evaluation results archived

### Test Types

- [ ] Unit tests implemented
- [ ] Integration tests implemented
- [ ] End-to-end tests implemented
- [ ] Regression tests implemented
- [ ] Safety tests implemented
- [ ] Bias tests implemented
- [ ] Performance tests implemented
- [ ] Chaos tests implemented

### Test Quality

- [ ] Test coverage meets threshold
- [ ] Test data management implemented
- [ ] Test environment parity verified
- [ ] Test automation CI/CD integrated
- [ ] Test reporting configured
- [ ] Test maintenance process defined
- [ ] Test metrics tracked
- [ ] Test improvement process defined

### Evaluation Types

- [ ] Safety evaluation included
- [ ] Quality evaluation included
- [ ] Performance evaluation included
- [ ] Cost evaluation included
- [ ] Regression evaluation included
- [ ] Red-team evaluation included
- [ ] Human evaluation included
- [ ] A/B experiment evaluation included

## Operations Checklist

### Deployment

- [ ] Deployment automation implemented
- [ ] Deployment pipeline tested
- [ ] Deployment runbook updated
- [ ] Deployment rollback tested
- [ ] Deployment verification implemented
- [ ] Deployment monitoring configured
- [ ] Deployment communication plan defined
- [ ] Deployment approval process defined

### Monitoring and Alerting

- [ ] Monitoring dashboards configured
- [ ] Alert rules configured
- [ ] Alert routing configured
- [ ] On-call rotation current
- [ ] Escalation paths documented
- [ ] Monitoring coverage verified
- [ ] Alert accuracy validated
- [ ] Monitoring metrics tracked

### Incident Response

- [ ] Incident response plan current
- [ ] Incident runbooks updated
- [ ] Incident response team trained
- [ ] Incident communication plan defined
- [ ] Incident escalation paths documented
- [ ] Incident post-mortem process defined
- [ ] Incident metrics tracked
- [ ] Incident improvement process defined

### Backup and Recovery

- [ ] Backup procedures documented
- [ ] Backup testing performed
- [ ] Recovery procedures documented
- [ ] Recovery testing performed
- [ ] Disaster recovery plan current
- [ ] Business continuity plan current
- [ ] RTO and RPO defined
- [ ] Recovery metrics tracked

## Documentation Checklist

### System Documentation

- [ ] System overview documented
- [ ] Architecture documented
- [ ] Data flows documented
- [ ] Security architecture documented
- [ ] Deployment topology documented
- [ ] API documentation current
- [ ] Configuration documentation current
- [ ] Troubleshooting guide current

### Model Documentation

- [ ] Model card created
- [ ] Model capabilities documented
- [ ] Model limitations documented
- [ ] Evaluation results documented
- [ ] Training data documented
- [ ] Known biases documented
- [ ] Intended use cases documented
- [ ] Prohibited use cases documented

### Prompt Documentation

- [ ] Prompt register maintained
- [ ] Prompt purposes documented
- [ ] Prompt templates documented
- [ ] Prompt version history maintained
- [ ] Prompt evaluation results documented
- [ ] Prompt known issues documented
- [ ] Prompt usage guidelines documented
- [ ] Prompt rollback procedures documented

### Runbook Documentation

- [ ] Incident response runbooks current
- [ ] Deployment runbooks current
- [ ] Rollback runbooks current
- [ ] Recovery runbooks current
- [ ] Escalation runbooks current
- [ ] Maintenance runbooks current
- [ ] Troubleshooting runbooks current
- [ ] Runbook testing documented

## Performance Checklist

### SLO Definition

- [ ] Latency SLOs defined
- [ ] Throughput SLOs defined
- [ ] Availability SLOs defined
- [ ] Error rate SLOs defined
- [ ] Cost SLOs defined
- [ ] SLO measurement implemented
- [ ] SLO alerting configured
- [ ] SLO reporting configured

### Performance Testing

- [ ] Performance test suite defined
- [ ] Performance benchmarks established
- [ ] Performance baseline documented
- [ ] Performance regression detection implemented
- [ ] Performance profiling implemented
- [ ] Performance optimization process defined
- [ ] Performance metrics tracked
- [ ] Performance improvement process defined

### Cost Management

- [ ] Cost budgets defined
- [ ] Cost attribution implemented
- [ ] Cost monitoring configured
- [ ] Cost alerting configured
- [ ] Cost optimization process defined
- [ ] Cost reporting configured
- [ ] Cost metrics tracked
- [ ] Cost improvement process defined

### Capacity Planning

- [ ] Capacity requirements documented
- [ ] Capacity monitoring configured
- [ ] Capacity forecasting implemented
- [ ] Capacity scaling procedures documented
- [ ] Capacity testing performed
- [ ] Capacity metrics tracked
- [ ] Capacity improvement process defined
- [ ] Capacity budget approved

## Compliance Checklist

### Compliance Assessment

- [ ] Regulatory applicability assessed
- [ ] Compliance requirements documented
- [ ] Compliance controls defined
- [ ] Compliance evidence requirements defined
- [ ] Compliance monitoring configured
- [ ] Compliance reporting configured
- [ ] Compliance metrics tracked
- [ ] Compliance improvement process defined

### Audit Preparation

- [ ] Audit scope defined
- [ ] Audit evidence collected
- [ ] Audit evidence validated
- [ ] Audit findings addressed
- [ ] Audit report documented
- [ ] Audit follow-up actions tracked
- [ ] Audit metrics tracked
- [ ] Audit improvement process defined

### Exception Management

- [ ] Exception register maintained
- [ ] Exception approval process defined
- [ ] Exception monitoring configured
- [ ] Exception renewal process defined
- [ ] Exception closure process defined
- [ ] Exception metrics tracked
- [ ] Exception reporting configured
- [ ] Exception improvement process defined

### Training and Awareness

- [ ] Training requirements defined
- [ ] Training assignments tracked
- [ ] Training completion monitored
- [ ] Training effectiveness measured
- [ ] Training records maintained
- [ ] Training metrics tracked
- [ ] Training reporting configured
- [ ] Training improvement process defined

## Agent-Specific Checklists

### Rules Architect Checklist

- [ ] System context gathered
- [ ] Risk tier assigned
- [ ] Domains selected
- [ ] Control requirements defined
- [ ] Architecture decisions documented
- [ ] Implementation plan created
- [ ] Release checklist defined
- [ ] Design review gates scheduled

### Rules Implementer Checklist

- [ ] Implementation tasks defined
- [ ] Code implemented
- [ ] Tests implemented
- [ ] Documentation updated
- [ ] Evidence collected
- [ ] Code review completed
- [ ] Build successful
- [ ] Deployment ready

### Rules Reviewer Checklist

- [ ] Review scope defined
- [ ] Artifacts inspected
- [ ] Findings documented
- [ ] Remediation guidance provided
- [ ] Evidence validated
- [ ] Release recommendation made
- [ ] Report generated
- [ ] Follow-up tracked

### Rules Release Gate Checklist

- [ ] Release request validated
- [ ] Evidence package received
- [ ] Evidence validated
- [ ] Controls assessed
- [ ] Decision made
- [ ] Decision communicated
- [ ] Post-release review scheduled
- [ ] Decision archived

### Rules Eval Checklist

- [ ] Evaluation request received
- [ ] Evaluation suites selected
- [ ] Datasets prepared
- [ ] Evaluation executed
- [ ] Results analyzed
- [ ] Thresholds checked
- [ ] Report generated
- [ ] Results archived

### Rules Compliance Auditor Checklist

- [ ] Evidence requirements defined
- [ ] Evidence collected
- [ ] Evidence validated
- [ ] Compliance verified
- [ ] Gaps identified
- [ ] Remediation tracked
- [ ] Report generated
- [ ] Archive updated

### Rules Data Steward Checklist

- [ ] Data inventory current
- [ ] Classification applied
- [ ] Retention enforced
- [ ] Legal hold verified
- [ ] Consent managed
- [ ] Quality validated
- [ ] Access controlled
- [ ] Metrics tracked

### Rules Enforcer Checklist

- [ ] Policy rules defined
- [ ] Enforcement configured
- [ ] Violation detection active
- [ ] Alerting configured
- [ ] Escalation paths defined
- [ ] Logging configured
- [ ] Metrics tracked
- [ ] Improvement process defined

### Rules Documentation Checklist

- [ ] Documentation requirements defined
- [ ] Documentation created
- [ ] Documentation reviewed
- [ ] Documentation published
- [ ] Documentation versioned
- [ ] Documentation feedback collected
- [ ] Documentation metrics tracked
- [ ] Documentation improvement process defined

### Rules Tracker Checklist

- [ ] Metrics defined
- [ ] Collection configured
- [ ] Dashboards created
- [ ] Alerting configured
- [ ] Reporting configured
- [ ] Metrics validated
- [ ] Metrics tracked
- [ ] Improvement process defined

### Rules Orchestrator Checklist

- [ ] Workflows defined
- [ ] Agent interactions configured
- [ ] Conflict resolution defined
- [ ] Monitoring configured
- [ ] Reporting configured
- [ ] Metrics tracked
- [ ] Improvement process defined
- [ ] Documentation maintained

### Rules Security Checklist

- [ ] Threat model complete
- [ ] Security controls defined
- [ ] Security review completed
- [ ] Vulnerability assessment complete
- [ ] Penetration test complete if required
- [ ] Security monitoring configured
- [ ] Incident response ready
- [ ] Metrics tracked

## Vendor and Supply Chain Checklist

### Vendor Assessment

- [ ] Vendor identified and documented
- [ ] Vendor risk assessment completed
- [ ] Vendor security review completed
- [ ] Vendor compliance status verified
- [ ] Vendor DPA executed if required
- [ ] Vendor SLA defined and agreed
- [ ] Vendor incident response procedures defined
- [ ] Vendor exit strategy documented

### Supply Chain Security

- [ ] Dependency inventory complete
- [ ] Dependency vulnerability scan current
- [ ] Dependency license compliance verified
- [ ] SBOM generated and maintained
- [ ] Dependency pinning implemented
- [ ] Dependency update process defined
- [ ] Supply chain attack mitigation implemented
- [ ] Vendor access controls implemented

### Vendor Monitoring

- [ ] Vendor performance monitoring configured
- [ ] Vendor security monitoring configured
- [ ] Vendor compliance monitoring configured
- [ ] Vendor incident notification configured
- [ ] Vendor review schedule defined
- [ ] Vendor renewal tracking configured
- [ ] Vendor risk register maintained
- [ ] Vendor escalation paths defined

## Human Oversight Checklist

### Human Review Requirements

- [ ] High-risk outputs require human review
- [ ] Human review workflow defined
- [ ] Human review SLA defined
- [ ] Human review escalation defined
- [ ] Human review training completed
- [ ] Human review metrics tracked
- [ ] Human review quality verified
- [ ] Human review audit trail maintained

### Escalation Procedures

- [ ] Escalation paths documented
- [ ] Escalation contacts current
- [ ] Escalation SLAs defined
- [ ] Escalation training completed
- [ ] Escalation testing performed
- [ ] Escalation metrics tracked
- [ ] Escalation improvement process defined
- [ ] Escalation documentation maintained

### Feedback Mechanisms

- [ ] User feedback channels defined
- [ ] User feedback collection implemented
- [ ] User feedback analysis performed
- [ ] User feedback response process defined
- [ ] User feedback metrics tracked
- [ ] User feedback improvement process defined
- [ ] User feedback documentation maintained
- [ ] User feedback communication defined

## Audit Preparation Checklist

### Pre-Audit Preparation

- [ ] Audit scope defined
- [ ] Audit timeline agreed
- [ ] Audit team identified
- [ ] Audit materials prepared
- [ ] Audit evidence collected
- [ ] Audit evidence validated
- [ ] Audit documentation current
- [ ] Audit contacts identified

### During Audit

- [ ] Audit facilitation provided
- [ ] Audit evidence presented
- [ ] Audit questions answered
- [ ] Audit findings documented
- [ ] Audit clarifications provided
- [ ] Audit recommendations noted
- [ ] Audit timeline followed
- [ ] Audit communication maintained

### Post-Audit

- [ ] Audit report reviewed
- [ ] Audit findings addressed
- [ ] Audit recommendations implemented
- [ ] Audit follow-up tracked
- [ ] Audit lessons learned documented
- [ ] Audit improvements implemented
- [ ] Audit evidence archived
- [ ] Audit metrics tracked

## Continuous Improvement Checklist

### Process Improvement

- [ ] Improvement opportunities identified
- [ ] Improvement priorities set
- [ ] Improvement actions defined
- [ ] Improvement actions assigned
- [ ] Improvement actions tracked
- [ ] Improvement actions verified
- [ ] Improvement metrics tracked
- [ ] Improvement documentation maintained

### Framework Updates

- [ ] Framework changes reviewed
- [ ] Framework changes tested
- [ ] Framework changes documented
- [ ] Framework changes communicated
- [ ] Framework changes implemented
- [ ] Framework changes verified
- [ ] Framework metrics tracked
- [ ] Framework documentation updated

### Training and Development

- [ ] Training needs identified
- [ ] Training plan created
- [ ] Training delivered
- [ ] Training effectiveness measured
- [ ] Training records maintained
- [ ] Training improvement process defined
- [ ] Training metrics tracked
- [ ] Training documentation maintained
