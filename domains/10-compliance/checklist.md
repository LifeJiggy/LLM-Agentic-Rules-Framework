# Compliance Domain - Checklist

> Verification checklist for releasing or reviewing LLM and agentic systems.

## Overview

Use this checklist before releasing medium-risk or high-risk AI systems, and when reviewing production systems after material model, prompt, data, or tool changes.

## Priority Guide

- P0: Required for legal, regulatory, safety, rights-impacting, or audit-blocking controls.
- P1: Required for medium-risk and high-risk production systems unless explicitly accepted.
- P2: Recommended for governance maturity and review efficiency.
- P3: Useful refinement for evidence quality.

---

## Table of Contents

1. [System Definition](#1-system-definition)
2. [Data Governance](#2-data-governance)
3. [Model And Prompt Governance](#3-model-and-prompt-governance)
4. [Tool And Agent Controls](#4-tool-and-agent-controls)
5. [Evaluation And Monitoring](#5-evaluation-and-monitoring)
6. [Release Decision](#6-release-decision)
7. [Security Controls](#7-security-controls)
8. [Privacy Controls](#8-privacy-controls)
9. [Access Control](#9-access-control)
10. [Audit and Evidence](#10-audit-and-evidence)
11. [Incident Response](#11-incident-response)
12. [Vendor Management](#12-vendor-management)
13. [International Deployment](#13-international-deployment)
14. [Retention and Disposal](#14-retention-and-disposal)
15. [Human Oversight](#15-human-oversight)
16. [Policy and Governance](#16-policy-and-governance)
17. [Monitoring and Alerting](#17-monitoring-and-alerting)
18. [Tools and Change Management](#18-tools-and-change-management)
19. [Testing and Validation](#19-testing-and-validation)
20. [Post-Release](#20-post-release)
21. [Evidence Packaging](#21-evidence-packaging)
22. [Appendix](#22-appendix)

---

## 1. System Definition

- [ ] System owner is documented.
- [ ] Intended use is documented.
- [ ] Prohibited uses are documented.
- [ ] User groups are documented.
- [ ] Risk tier is assigned.
- [ ] Review cadence is defined.
- [ ] System purpose is aligned with business objectives.
- [ ] Scope is clearly bounded (inputs, outputs, dependencies).
- [ ] Exclusions are explicitly stated.
- [ ] Success criteria are defined.
- [ ] Failure modes are documented.
- [ ] Escalation path is known.
- [ ] Legal basis for processing is established.
- [ ] Jurisdiction coverage is defined.

## 2. Data Governance

- [ ] Data sources are documented.
- [ ] Personal and sensitive data categories are identified.
- [ ] Legal basis or business justification is documented.
- [ ] Data minimization has been applied.
- [ ] Retention period is defined for prompts, completions, traces, and logs.
- [ ] Access to AI logs is restricted.
- [ ] Data inventory is maintained and current.
- [ ] Data classification is applied to all inputs and outputs.
- [ ] Consent records are captured where required.
- [ ] Purpose limitation is enforced.
- [ ] Data retention and purging schedules exist.
- [ ] Legal holds are supported.
- [ ] Third-party data transfers are reviewed.
- [ ] Data location and residency are documented.

## 3. Model And Prompt Governance

- [ ] Model provider and model version are recorded.
- [ ] Prompt templates are versioned.
- [ ] High-risk prompt changes require review.
- [ ] Model upgrades trigger regression evaluation.
- [ ] Known limitations are documented.
- [ ] Model cards are maintained.
- [ ] Prompt templates are stored in version control and reviewed.
- [ ] System prompt included review and approval.
- [ ] Fine-tuned models are differentiated from base models.
- [ ] Evaluation results are saved per version.
- [ ] Prompt injection mitigations are tested.
- [ ] Retraining or fine-tuning data sources are reviewed.
- [ ] Performance drift thresholds are defined.
- [ ] Rollback procedures for model/prompt changes are documented.

## 4. Tool And Agent Controls

- [ ] Agent tools are inventoried.
- [ ] Tool permissions follow least privilege.
- [ ] Irreversible or high-impact actions require confirmation or review.
- [ ] Tool calls are logged with enough context for audit.
- [ ] Failure modes and rollback paths are documented.
- [ ] Tool APIs are scoped by capability, not broad access.
- [ ] Tool credentials are stored in a secret manager.
- [ ] Tool output is validated before consumption.
- [ ] Tool retry and timeout behavior is defined.
- [ ] Rate limiting is configured.

## 5. Evaluation And Monitoring

- [ ] Compliance-relevant test cases exist.
- [ ] Harmful, biased, misleading, and privacy-risk outputs are tested.
- [ ] Production monitoring covers policy violations.
- [ ] Incident response path is documented.
- [ ] Exceptions and accepted risks are approved.
- [ ] Safety and toxicity tests cover representative language and cultural contexts.
- [ ] Fairness and bias metrics are baselined.
- [ ] Regression suite is run on every candidate before promotion.
- [ ] Alerting policies are defined for policy violation thresholds.
- [ ] Dashboarding captures core compliance KPIs.

## 6. Release Decision

- [ ] Security review completed where required.
- [ ] Privacy review completed where required.
- [ ] Legal or compliance review completed for high-impact workflows.
- [ ] Human oversight requirements are implemented.
- [ ] Audit evidence is stored in a durable location.
- [ ] Rollback plan is confirmed.
- [ ] Communication plan is ready.
- [ ] Required metrics are inspected before release approval.
- [ ] Exception log is empty or closed.
- [ ] Change log and release notes are captured.

## 7. Security Controls

- [ ] Secrets are not stored in prompts, logs, or checkpoints.
- [ ] TLS is enforced for data in transit.
- [ ] Authentication and authorization are enforced for admin interfaces.
- [ ] Penetration testing is scheduled periodically.
- [ ] Threat model is documented.
- [ ] Vulnerability scanning covers dependencies.
- [ ] Network segmentation isolates sensitive data access.
- [ ] Security headers or WAF rules are applied.
- [ ] Secrets are rotated on the defined schedule.
- [ ] Suspicious access patterns are alerted on.

## 8. Privacy Controls

- [ ] PII minimization is applied to data entering the system.
- [ ] Redaction rules are tested and not too noisy.
- [ ] Consent is collected and stored where needed.
- [ ] Data subject request handling procedures are documented.
- [ ] Privacy notices match deployed capabilities.
- [ ] Cross-border transfer mechanisms are documented.
- [ ] DPIA or privacy risk assessment is completed.
- [ ] Retention rules are enforced programmatically.
- [ ] Users can access and export their data.
- [ ] Users can request deletion when legally allowed.

## 9. Access Control

- [ ] Roles are defined and mapped to permissions.
- [ ] Separation of duties is applied where required.
- [ ] Privileged operations require additional authentication.
- [ ] MFA is enforced for sensitive roles.
- [ ] Access reviews are performed periodically.
- [ ] Temporary access expires automatically.
- [ ] Service accounts follow least privilege naming and scoping.
- [ ] Superuser usage is monitored.
- [ ] Authorization failures are audited.

## 10. Audit and Evidence

- [ ] Audit events are generated and stored.
- [ ] Audit events include actor, action, timestamp, and outcome.
- [ ] Audit records are tamper evident or tamper protected.
- [ ] Evidence is linked to each control claim.
- [ ] Evidence retention aligns with policy and legal requirements.
- [ ] Exported evidence passes validation.
- [ ]Archiving rules are defined for audit data.
- [ ]Audit log schema is documented.

## 11. Incident Response

- [ ] Incident response plan exists.
- [ ] Contacts on duty are documented.
- [ ] Runbooks exist for common failure modes.
- [ ] Post-incident reviews are scheduled.
- [ ] Notifications to affected users are possible.
- [ ] Breach notification steps are documented.
- [ ] Legal and CISO are looped automatically for high-severity events.

## 12. Vendor Management

- [ ] List of subprocessors and data processors is current.
- [ ] DPAs are in place where required.
- [ ] Vendor security questionnaires are reviewed.
- [ ] Vendor risk assessments are refreshed periodically.
- [ ] Service-level and security obligations are contractually enforced.
- [ ] Vendor access is limited to required scope.
- [ ] Vendor certifications are tracked.
- [ ] Offboarding runbooks exist for vendor changes.

## 13. International Deployment

- [ ] Jurisdiction-specific disclosure text is maintained.
- [ ] Data residency requirements are mapped to infrastructure.
- [ ] Cross-border transfer restrictions are reviewed.
- [ ] Local language support is available where required.
- [ ] Regulatory regimes are documented for each operating region.

## 14. Retention and Disposal

- [ ] Retention schedules are defined and enforced.
- [ ] Archival location and format are documented.
- [ ] Legal holds are supported.
- [ ] Deletion validation is performed.
- [ ] Secure disposal of keys and backups is documented.

## 15. Human Oversight

- [ ] Human review points are defined in workflows.
- [ ] Override and escalation behavior is documented.
- [ ] Reviewers receive training and context packs.
- [ ] Override decisions are audited.
- [ ] High-stakes outputs are routed to human review.
- [ ] Review surfaces preserve source input and evidence.

## 16. Policy and Governance

- [ ] Compliance policy is current and published.
- [ ] Exception handling process is documented.
- [ ] Policy review calendar is defined.
- [ ] Control owners are assigned and aware.
- [ ] Risk appetite is documented.
- [ ] Governance meetings are scheduled.

## 17. Monitoring and Alerting

- [ ] Policy violation dashboards are available.
- [ ] Alerts have clear severity and routing.
- [ ] False positive tuning is scheduled.
- [ ] On-call response playbook is current.

## 18. Tools and Change Management

- [ ] Tool registry is up to date.
- [ ] Tool permissions are reviewed on change.
- [ ] Candidate tool changes pass policy review.
- [ ] Deprecated tools are migrated off.

## 19. Testing and Validation

- [ ] Regression tests cover compliance invariants.
- [ ] Red team or adversarial tests run on a schedule.
- [ ] Model updates pass safety and fairness gates.
- [ ] Privacy unit tests verify redaction behavior.
- [ ] Data retention worker tests verify purge behavior.
- [ ] Emergency rollback is rehearsed annually.

## 20. Post-Release

- [ ] First 72-hour review is scheduled.
- [ ] Production metrics are reviewed.
- [ ] User feedback incidents are tracked.
- [ ] Exceptions are reconciled before next release.
- [ ] Evidence archive is updated with release artifacts.

## 21. Evidence Packaging

- [ ] Control mapping documents are updated.
- [ ] Evidence location for each control is known.
- [ ] Audit packages are exported before audits.
- [ ] Evidence integrity checks pass.

## 22. Appendix

## Release Gate Reference

| Gate | Owner | Evidence |
|------|-------|----------|
| P0 | Compliance | Legal sign-off, risk register update |
| P1 | Engineering | Evaluation report, test evidence |
| P2 | Product | Documentation updates, training content |

## Glossary
- P0: Required for legal, regulatory, safety, rights-impacting, or audit-blocking controls.
- P1: Required for medium-risk and high-risk production systems unless explicitly accepted.
- P2: Recommended for governance maturity and review efficiency.
- P3: Useful refinement for evidence quality.

## Reference Standards
- SOC 2
- ISO/IEC 27001
- NIST SP 800-53
- GDPR
- CCPA
- HIPAA
- PCI DSS
- CSA CCM
- MITRE ATLAS
- OWASP Top 10 for LLMs
- EU AI Act
- LGPD
- India DPDP Act
- China PIPL
- Singapore PDPA

## Compliance Domains
### Data Governance
- [ ] Data inventory exists.
- [ ] PII is classified.
- [ ] Sensitive attributes are tagged.
- [ ] Data lineage is documented.
- [ ] Data quality metrics are defined.
- [ ] Data catalog is current.
- [ ] Retention schedule is published and enforced.
- [ ] Deletion workflows are tested.
- [ ] Archival strategy is defined.
- [ ] Legal hold process is documented.
- [ ] Data sharing agreements are recorded.
- [ ] Third-party data access is limited.

### Model Governance
- [ ] Model cards exist for every production system.
- [ ] Prompt templates are versioned and reviewed.
- [ ] Fine-tuning datasets are documented.
- [ ] Evaluation suite covers safety, fairness, and capability.
- [ ] Drift metrics are tracked.
- [ ] Fallback model is defined and tested.
- [ ] Rollback runbook exists.
- [ ] Material changes require re-evaluation.

### Access Control
- [ ] Identity provider integrated.
- [ ] RBAC policies are defined and approved.
- [ ] Separation of duties is enforced.
- [ ] MFA is required for privileged users.
- [ ] Session timeouts are defined.
- [ ] Access reviews are completed quarterly.
- [ ] Deactivated accounts are disabled immediately.
- [ ] Service accounts follow least privilege.
- [ ] API keys are short-lived when possible.
- [ ] Privileged operations are audited.
- [ ] Authorization failures are logged.
- [ ] Emergency access is time-bounded and reviewed.

### Audit and Logging
- [ ] Centralized logging is configured.
- [ ] Audit events include actor, action, outcome, and timestamp.
- [ ] Logs are immutable or tamper-evident.
- [ ] Log rotation is configured.
- [ ] Logs are retained per policy.
- [ ] Audit log schema is documented.
- [ ] Missing log events are investigated.
- [ ] Log access is restricted.
- [ ] Log forwarding is encrypted.
- [ ] User activity is auditable.
- [ ] Model inference is logged.
- [ ] Tool invocations are logged.

### Encryption and Key Management
- [ ] Encryption standards are documented.
- [ ] TLS is enforced for external and internal traffic.
- [ ] Data at rest is encrypted.
- [ ] Key storage uses a dedicated key management system.
- [ ] Key rotation schedule is documented and enforced.
- [ ] Key access is limited.
- [ ] Key compromise procedures are defined.
- [ ] Hardware security modules are used where required.
- [ ] Certificate lifecycle is managed.
- [ ] Encryption algorithm choices are reviewed for currency.

### Change Management
- [ ] All changes are reviewed.
- [ ] Model changes trigger evaluation.
- [ ] Prompt changes are reviewed for compliance impact.
- [ ] Data source changes are reviewed with the DPO.
- [ ] Tool changes require sign-off from security and compliance.
- [ ] Infrastructure changes are tracked.
- [ ] Emergency change process is documented.
- [ ] Release evidence is recorded.
- [ ] Rollback plan is defined and tested.
- [ ] Change communication plan exists.
- [ ] Deployment windows are defined.
- [ ] Feature flags have owners and review dates.

### Testing and Validation
- [ ] Unit tests cover compliance controls.
- [ ] Integration tests verify policy enforcement.
- [ ] System prompt tests validate policy wording.
- [ ] Redact tests validate PII handling.
- [ ] Retrieval tests verify source quality.
- [ ] Tool limit tests verify authorization boundaries.
- [ ] Failure mode tests verify fallback behavior.
- [ ] Regression suite runs in CI.
- [ ] Bias tests are included in pre-release checks.
- [ ] Accessibility tests are included.
- [ ] Localization tests are included.
- [ ] Performance tests include budget and latency checks.
- [ ] Chaos tests verify resilience.
- [ ] Penetration tests are scheduled.

### Monitoring and Alerting
- [ ] Compliance dashboards are available.
- [ ] Policy violation alerts are routed.
- [ ] Alert severity definitions are documented.
- [ ] On-call rotation is defined.
- [ ] MTTR targets are set and reviewed.
- [ ] False positive tuning is scheduled.
- [ ] Incident reviews are conducted.
- [ ] Change in metrics triggers investigation.
- [ ] Anomaly detection covers compliance events.
- [ ] Sampling strategy is defined for manual review.
- [ ] Incident postmortems include compliance review.

### Incident Response
- [ ] Incident response plan exists.
- [ ] Roles and contacts are documented.
- [ ] Severity definitions are agreed.
- [ ] Containment playbooks exist.
- [ ] Communication plans exist.
- [ ] Breach notification SLA is defined.
- [ ] Evidence collection procedures are documented.
- [ ] Legal and privacy are looped for incidents.
- [ ] Lessons learned are tracked to remediation.
- [ ] Tabletop exercises are scheduled.
- [ ] Runbooks are tested.
- [ ] Recovery metrics are tracked.

### Training and Awareness
- [ ] Engineers receive compliance training.
- [ ] Reviewers receive specific training.
- [ ] Training status is tracked.
- [ ] Refresher training is timely.
- [ ] New hire onboarding includes compliance.
- [ ] Compliance guidance is accessible.
- [ ] Escalation paths are known.
- [ ] User awareness materials are available.
- [ ] Incident training is included.
- [ ] Data handling training is refreshed.

### Documentation
- [ ] System register is current.
- [ ] Model cards exist.
- [ ] Prompt register is available.
- [ ] Tool catalog is maintained.
- [ ] Runbooks are documented.
- [ ] Architecture diagrams are current.
- [ ] Data flow diagrams are current.
- [ ] Threat model is documented.
- [ ] Privacy notice is published.
- [ ] Terms of service are published.
- [ ] Data processing agreements are archived.
- [ ] Evidence packages are organized.

### Human Oversight
- [ ] Review points are defined in workflow.
- [ ] High-impact actions require human approval.
- [ ] Reviewers receive context and instructions.
- [ ] Override reasons are required.
- [ ] Override metrics are tracked.
- [ ] Escalation paths are documented.
- [ ] Review latency is monitored.
- [ ] Reviewer agreement is measured.
- [ ] Difficult cases are escalated.
- [ ] Policy updates are communicated to reviewers.
- [ ] Review tooling supports audit.

### Privacy
- [ ] PII minimization is enforced.
- [ ] Consent receipts are recorded.
- [ ] Data subject requests are fulfilled within SLA.
- [ ] Privacy notices match actual practice.
- [ ] Data minimization tests are automated.
- [ ] Retention and purging are programmatic.
- [ ] Legal holds are enforced.
- [ ] Cross-border transfers are controlled.
- [ ] PII leakage tests are in CI.
- [ ] Data subject access workflow is documented.
- [ ] DPO contact is published.
- [ ] DPIA is current.

### Ethical AI
- [ ] Fairness metrics are baselined.
- [ ] Bias mitigation strategies are selected.
- [ ] Disparate impact is monitored.
- [ ] Explainability features are available.
- [ ] Contestability pathways exist.
- [ ] Purpose limitation is enforced.
- [ ] Harms assessment is conducted.
- [ ] Stakeholder consultation is documented.
- [ ] High-risk uses undergo formal review.
- [ ] Red-team exercises are scheduled.
- [ ] Remediation plans for ethical findings exist.

### Vendor Management
- [ ] Vendor register is current.
- [ ] DPA inventory exists.
- [ ] Subprocessor list is maintained.
- [ ] Vendor questionnaires are completed.
- [ ] Security attestations are evidence-backed.
- [ ] Service-level obligations are reviewed.
- [ ] Vendor access is restricted and audited.
- [ ] Incident escalation procedures include vendors.
- [ ] Offboarding procedures preserve data control.
- [ ] Vendor roadmap is tracked for compliance changes.

### Supply Chain
- [ ] Dependencies are inventoried.
- [ ] Vulnerability scanning is scheduled.
- [ ] License compliance is reviewed.
- [ ] Third-party components are approved.
- [ ] SBOM is produced and current.
- [ ] Patch management policy exists.
- [ ] Supply chain risk is reviewed.
- [ ] Software integrity is verified.
- [ ] Artifact provenance is recorded.
- [ ] Build environment is hardened.

### Transparency
- [ ] AI involvement is disclosed to users.
- [ ] Limits of capability are stated.
- [ ] Accountabilities are documented.
- [ ] Model and prompt versions are tracked.
- [ ] Errors and mistakes are surfaced.
- [ ] Feedback channels are available.
- [ ] Explanations are provided where needed.
- [ ] Appeal and dispute processes are available.
- [ ] Performance metrics are disclosed.
- [ ] Breach notifications are timely.

### Accessibility and Inclusivity
- [ ] Accessibility testing is performed.
- [ ] Localization is reviewed.
- [ ] Inclusive language guidelines are applied.
- [ ] Feedback from diverse users is incorporated.
- [ ] Multilingual support is confirmed.
- [ ] Assistive technology compatibility is tested.
- [ ] Ethnographic testing surfaces gaps.
- [ ] Disability accommodations are supported.
- [ ] Cultural context is considered.

### Cost and Performance Compliance
- [ ] Cost models are reviewed.
- [ ] Performance baselines are set.
- [ ] Token budgets are enforced.
- [ ] Latency budgets are defined and monitored.
- [ ] Fallback triggers are tested.
- [ ] Request volume limits are enforced.
- [ ] Rate limiting policies are configured.
- [ ] Budget alerts are routed.
- [ ] Cost attribution is available.
- [ ] Optimization opportunities are reviewed periodically.

```markdown
## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
```

## Additional Checklist Items

### Enterprise Controls
- [ ] Third-party audits are scheduled.
- [ ] Penetration testing covers AI components.
- [ ] Architecture review is current.
- [ ] Data flow diagrams are current.
- [ ] Ownership is documented in system register.
- [ ] Runbook access is restricted and audited.
- [ ] Backup and restore is tested.

### Data Governance Controls
- [ ] Data inventory is current.
- [ ] Data classification is defined and applied.
- [ ] Sensitive attributes are labeled.
- [ ] Data quality checks are performed.
- [ ] Data provenance is tracked.
- [ ] Data sharing agreements are documented.
- [ ] Data retention schedule is published.
- [ ] Legal hold workflow is tested.
- [ ] Data disposal is validated.
- [ ] Cross-border data flows are reviewed.
- [ ] Data catalog is updated.

### Model Governance Controls
- [ ] Model cards are maintained and reviewed.
- [ ] Prompt templates are versioned and reviewed.
- [ ] Prompt injection mitigations are tested.
- [ ] Model evaluation results are stored.
- [ ] Drift detection is enabled.
- [ ] Fallback model is defined and tested.
- [ ] Rollback runbook is current.
- [ ] Model-risk file is reviewed.
- [ ] Evaluation suite covers safety, fairness, and capability.
- [ ] Performance tests include latency and cost.

### Tool and Agent Controls
- [ ] Tool inventory is current.
- [ ] Tools are scoped by capability.
- [ ] Credentials are stored in a secret manager.
- [ ] Audit hooks are implemented.
- [ ] Human approval is required for irreversible actions.
- [ ] Tool calls are logged and auditable.
- [ ] Retry and timeout behavior is defined.
- [ ] Rate limiting is configured.
- [ ] Tool failure modes are documented.
- [ ] Tool permissions are reviewed on change.

### Human Oversight Controls
- [ ] Review points are documented.
- [ ] Override reasons are required.
- [ ] Reviewers receive training.
- [ ] High-impact outputs are routed to review.
- [ ] Review surfaces preserve evidence.
- [ ] Review latency is monitored.
- [ ] Reviewer agreement is measured.
- [ ] Difficult cases are escalated.
- [ ] Policy updates are communicated.
- [ ] Audit trail includes reviewer identity.

### Incident Response Controls
- [ ] Incident response plan exists.
- [ ] Contacts are documented and current.
- [ ] Severity definitions are agreed.
- [ ] Containment playbooks exist.
- [ ] Communication plans exist.
- [ ] Breach notification SLA is defined.
- [ ] Evidence collection is documented.
- [ ] Legal and privacy are looped.
- [ ] Lessons learned are tracked.
- [ ] Tabletop exercises are scheduled.
- [ ] Runbooks are tested.
- [ ] Recovery metrics are tracked.

### Vendor Management Controls
- [ ] Vendor register is current.
- [ ] DPA inventory exists.
- [ ] Subprocessor list is maintained.
- [ ] Vendor questionnaires are completed.
- [ ] Security attestations are backed.
- [ ] Service-level obligations are reviewed.
- [ ] Vendor access is restricted.
- [ ] Incident escalation includes vendors.
- [ ] Offboarding preserves data control.
- [ ] Vendor roadmap is tracked.

### Privacy Controls
- [ ] PII minimization is enforced.
- [ ] Consent receipts are recorded.
- [ ] DSRs are fulfilled within SLA.
- [ ] Privacy notices match practice.
- [ ] Data minimization tests are automated.
- [ ] Retention and purging are programmatic.
- [ ] Legal holds are enforced.
- [ ] Cross-border transfers are controlled.
- [ ] PII leakage tests are in CI.
- [ ] DPO contact is published.
- [ ] DPIA is current.

### Access Control Controls
- [ ] Identity provider integrated.
- [ ] RBAC policies are defined.
- [ ] Separation of duties enforced.
- [ ] MFA required for privileged users.
- [ ] Session timeouts defined.
- [ ] Access reviews completed quarterly.
- [ ] Deactivated accounts disabled.
- [ ] Service accounts follow least privilege.
- [ ] API keys are short-lived.
- [ ] Privileged operations audited.
- [ ] Authorization failures logged.
- [ ] Emergency access time-bounded.

### Audit and Evidence Controls
- [ ] Centralized logging is configured.
- [ ] Audit events include actor, action, outcome, and timestamp.
- [ ] Logs are immutable or tamper-evident.
- [ ] Log rotation is configured.
- [ ] Logs are retained per policy.
- [ ] Audit log schema is documented.
- [ ] Missing log events are investigated.
- [ ] Log access is restricted.
- [ ] Log forwarding is encrypted.
- [ ] User activity is auditable.
- [ ] Model inference is logged.
- [ ] Tool invocations are logged.

### Encryption and Key Management Controls
- [ ] Encryption standards are documented.
- [ ] TLS is enforced for external and internal traffic.
- [ ] Data at rest is encrypted.
- [ ] Key storage uses a dedicated key management system.
- [ ] Key rotation schedule is documented and enforced.
- [ ] Key access is limited.
- [ ] Key compromise procedures are defined.
- [ ] Hardware security modules are used where required.
- [ ] Certificate lifecycle is managed.
- [ ] Encryption algorithm choices are reviewed for currency.

### Change Management Controls
- [ ] All changes are reviewed.
- [ ] Model changes trigger evaluation.
- [ ] Prompt changes are reviewed for compliance impact.
- [ ] Data source changes are reviewed with DPO.
- [ ] Tool changes require compliance sign-off.
- [ ] Infrastructure changes are tracked.
- [ ] Emergency change process is documented.
- [ ] Release evidence is recorded.
- [ ] Rollback plan is defined and tested.
- [ ] Change communication plan exists.
- [ ] Deployment windows are defined.
- [ ] Feature flags have owners.

### Testing and Validation Controls
- [ ] Unit tests cover compliance controls.
- [ ] Integration tests verify policy enforcement.
- [ ] System prompt tests validate policy wording.
- [ ] Redact tests validate PII handling.
- [ ] Retrieval tests verify source quality.
- [ ] Tool limit tests verify authorization boundaries.
- [ ] Failure mode tests verify fallback behavior.
- [ ] Regression suite runs in CI.
- [ ] Bias tests are included pre-release.
- [ ] Accessibility tests are included.
- [ ] Localization tests are included.
- [ ] Performance tests include budget and latency.
- [ ] Chaos tests verify resilience.
- [ ] Penetration tests are scheduled.

### Monitoring and Alerting Controls
- [ ] Compliance dashboards are available.
- [ ] Policy violation alerts are routed.
- [ ] Alert severity definitions are documented.
- [ ] On-call rotation is defined.
- [ ] MTTR targets are set and reviewed.
- [ ] False positive tuning is scheduled.
- [ ] Incident reviews are conducted.
- [ ] Change in metrics triggers investigation.
- [ ] Anomaly detection covers compliance events.
- [ ] Sampling strategy is defined for manual review.
- [ ] Incident postmortems include compliance review.

### Documentation Controls
- [ ] System register is current.
- [ ] Model cards exist.
- [ ] Prompt register is available.
- [ ] Tool catalog is maintained.
- [ ] Runbooks are documented.
- [ ] Architecture diagrams are current.
- [ ] Data flow diagrams are current.
- [ ] Threat model is documented.
- [ ] Privacy notice is published.
- [ ] Terms of service are published.
- [ ] Data processing agreements are archived.
- [ ] Evidence packages are organized.

## Appendix

## Release Gate Reference

| Gate | Owner | Evidence |
|------|-------|----------|
| P0 | Compliance | Legal sign-off, risk register update |
| P1 | Engineering | Evaluation report, test evidence |
| P2 | Product | Documentation updates, training content |

## Glossary
- P0: Required for legal, regulatory, safety, rights-impacting, or audit-blocking controls.
- P1: Required for medium-risk and high-risk production systems unless explicitly accepted.
- P2: Recommended for governance maturity and review efficiency.
- P3: Useful refinement for evidence quality.

## Reference Standards
- SOC 2
- ISO/IEC 27001
- NIST SP 800-53
- GDPR
- CCPA
- HIPAA
- PCI DSS
- CSA CCM
- MITRE ATLAS
- OWASP Top 10 for LLMs
- EU AI Act
- LGPD
- India DPDP Act
- China PIPL
- Singapore PDPA