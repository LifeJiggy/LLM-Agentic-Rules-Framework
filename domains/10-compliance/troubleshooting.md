# Compliance Domain - Troubleshooting

> Common compliance issues in LLM and agentic systems and how to resolve them.

## Overview

Use this file during audits, incident reviews, or release blockers where the issue is missing evidence, unclear ownership, sensitive data exposure, or unmanaged policy exceptions.

---

## Table of Contents

1. [Missing Approval Evidence](#1-missing-approval-evidence)
2. [Sensitive Data Appears In Logs](#2-sensitive-data-appears-in-logs)
3. [Model Upgrade Changes Regulated Output](#3-model-upgrade-changes-regulated-output)
4. [Unclear Human Review Requirements](#4-unclear-human-review-requirements)
5. [Policy Exceptions Accumulate](#5-policy-exceptions-accumulate)
6. [Consent Records Are Missing or Incomplete](#6-consent-records-are-missing-or-incomplete)
7. [Data Subject Request Cannot Be Fulfilled](#7-data-subject-request-cannot-be-fulfilled)
8. [Audit Logs Are Incomplete or Inconsistent](#8-audit-logs-are-incomplete-or-inconsistent)
9. [Retention Policies Are Not Enforced](#9-retention-policies-are-not-enforced)
10. [Jurisdiction Rules Are Not Applied](#10-jurisdiction-rules-are-not-applied)
11. [Vendor Compliance Lapses](#11-vendor-compliance-lapses)
12. [Excessive False Positives in Policy Checks](#12-excessive-false-positives-in-policy-checks)
13. [Tool Call Audit Gaps](#13-tool-call-audit-gaps)
14. [Human Override Not Audited](#14-human-override-not-audited)
15. [Redaction Breaks Valid Traces](#15-redaction-breaks-valid-traces)
16. [Model Risk File Is Stale](#16-model-risk-file-is-stale)
17. [Release Evidence Is Missing Links](#17-release-evidence-is-missing-links)
18. [Incident Response Is Sluggish](#18-incident-response-is-sluggish)
19. [Appendix](#19-appendix)

---

## 1. Missing Approval Evidence

**Symptom:** A reviewer asks why a system was approved, but the team can only point to chat messages or informal notes.

**Likely cause:** The release process lacks a durable evidence location.

**Resolution:**

1. Create a release review record.
2. Attach evaluation, privacy, security, and risk review evidence.
3. Link the record from the system register.
4. Require the same record for future releases.

**Preventive controls:**

- Pre-populate release templates from the system register.
- Automate attachment of evaluation metrics.
- Assign a release evidence owner.

---

## 2. Sensitive Data Appears In Logs

**Symptom:** Prompt or completion traces contain secrets, personal data, or regulated records.

**Likely cause:** Logging was designed for debugging without data classification.

**Resolution:**

1. Restrict access to affected logs.
2. Redact or purge records according to policy.
3. Add redaction before persistence.
4. Reduce trace retention.
5. Add a regression test for the leakage pattern.

```python
# Example redaction hook
def before_persist(trace):
    return AuditPrivacyFilter().filter_event(trace)
```

**Preventive controls:**

- Define classification rules for prompts and outputs.
- Block secrets at the tokenizer or logging layer.
- Sample redacted logs for leakage in CI.

---

## 3. Model Upgrade Changes Regulated Output

**Symptom:** A model upgrade changes refusals, advice, tone, or classification decisions.

**Likely cause:** Model versions are not treated as behavior-affecting dependencies.

**Resolution:**

1. Roll back if user impact is unacceptable.
2. Run the approved evaluation suite against both versions.
3. Review changed cases with the system owner.
4. Update the model register and release evidence.

**Preventive controls:**

- Treat model versions as locked dependencies.
- Gate model changes behind evaluation and review.
- Maintain a model risk file with rollout criteria.

---

## 4. Unclear Human Review Requirements

**Symptom:** Operators disagree about when AI output can be sent or acted on.

**Likely cause:** Oversight rules are implicit or only described in training.

**Resolution:**

1. Define review thresholds in documentation.
2. Add product controls that enforce review where possible.
3. Log approvals and overrides.
4. Train reviewers with examples of borderline cases.

**Preventive controls:**

- Encode review thresholds in routing code.
- Publish operator guidance.
- Retrain reviewers when rules change.

---

## 5. Policy Exceptions Accumulate

**Symptom:** Many releases rely on temporary exceptions that are never revisited.

**Likely cause:** Exceptions have no owner, expiration, or remediation plan.

**Resolution:**

1. Assign each exception an owner.
2. Add an expiration date.
3. Document the accepted risk.
4. Track remediation to closure.

**Preventive controls:**

- Expire exceptions automatically unless renewed.
- Require a quarterly exception report.
- Review exceptions in governance meetings.

---

## 6. Consent Records Are Missing or Incomplete

**Symptom:** Data subject requests require evidence of consent, but records are split between systems or missing.

**Likely cause:** Consent was collected outside the AI system context or not recorded.

**Resolution:**

1. Map consent points to data flows.
2. Store consent records with identifiable user IDs and timestamps.
3. Reconcile records between frontend and backend systems.
4. Implement retroactive consent capture where feasible.

**Preventive controls:**

- Design consent collection into the onboarding flow.
- Use a single consent registry.
- Include consent IDs in audit trails.

---

## 7. Data Subject Request Cannot Be Fulfilled

**Symptom:** A user’s access or deletion request cannot be completed because of fragmented data, missing retention labels, or legal holds.

**Likely cause:** Data management is not organized around data subject rights.

**Resolution:**

1. Map user data to identifiers and storage locations.
2. Apply retention labels consistently.
3. Implement legal-hold awareness in deletion workflows.
4. Test DSAR and erasure flows in staging.

**Preventive controls:**

- Maintain a user data inventory.
- Automate export and deletion jobs.
- Alert on incomplete fulfillment after N days.

---

## 8. Audit Logs Are Incomplete or Inconsistent

**Symptom:** Reviewers cannot reconstruct an incident because event fields vary, timestamps are missing, or context is insufficient.

**Likely cause:** Multiple teams or services emit audit events without a common schema.

**Resolution:**

1. Publish a canonical audit event schema.
2. Update emitters to include required fields.
3. Backfill critical events from existing logs.
4. Add schema validation in the logging pipeline.

**Preventive controls:**

- Enforce schema via logging library or middleware.
- Run automated integrity checks on audit trails.
- Review schema changes in compliance governance.

---

## 9. Retention Policies Are Not Enforced

**Symptom:** Old prompts and traces persist longer than policy allows, increasing legal and privacy risk.

**Likely cause:** Retention is manual or applies only to some data stores.

**Resolution:**

1. Audit all data stores holding AI artifacts.
2. Write retention rules for each data class.
3. Implement automated purge and archive jobs.
4. Validate via tests and alert on backlog.

**Preventive controls:**

- Enforce retention in infrastructure (TTL indexes, lifecycle policies).
- Monitor retention job successes and failures.
- Review data map and retention rules quarterly.

---

## 10. Jurisdiction Rules Are Not Applied

**Symptom:** Users receive disclosures or retention treatment that does not match their region.

**Likely cause:** Jurisdiction is detected after policy decisions or not at all.

**Resolution:**

1. Detect jurisdiction at request entry.
2. Store jurisdiction in session or request context.
3. Apply region-specific policies programmatically.
4. Test each jurisdiction in automated tests.

**Preventive controls:**

- Use a jurisdiction registry.
- Reject ambiguous jurisdiction unless fallback is acceptable.
- Update tests when new jurisdictions are added.

---

## 11. Vendor Compliance Lapses

**Symptom:** Model providers or tool vendors do not meet required certifications or DPA terms.

**Likely cause:** Vendor register is incomplete or not reviewed regularly.

**Resolution:**

1. Map all vendors touching user data or regulated outputs.
2. Collect attestations and DPAs.
3. Escalate expired or missing documents.
4. Document compensating controls for gaps.

**Preventive controls:**

- Maintain a tracked vendor inventory.
- Schedule annual reviews.
- Block vendor onboarding without compliance artifacts.

---

## 12. Excessive False Positives in Policy Checks

**Symptom:** Policy checks block legitimate workflows, causing user frustration and workarounds.

**Likely cause:** Rules are too broad or lack context awareness.

**Resolution:**

1. Analyze blocked-action logs.
2. Narrow rule scope with additional context.
3. Add exception paths with approval.
4. Track false-positive rate in monitoring.

**Preventive controls:**

- Co-design policies with affected teams.
- Provide override mechanisms with audit logging.
- Adjust thresholds based on operational feedback.

---

## 13. Tool Call Audit Gaps

**Symptom:** High-impact tool calls are missing from audit logs, or logs lack inputs/outputs.

**Likely cause:** Ad-hoc tool integrations bypass the central audit bus.

**Resolution:**

1. Require all tools to use the shared audit client.
2. Add test coverage that asserts audit events are emitted.
3. Review tool onboarding checklist to include audit requirements.

**Preventive controls:**

- Central tool registry with mandatory audit policy.
- API gateway enforcement for internal tool calls.

---

## 14. Human Override Not Audited

**Symptom:** Reviewers override AI recommendations, but the reason and context are not captured.

**Likely cause:** Override action does not emit an audit event.

**Resolution:**

1. Log every override with reviewer identity, timestamp, reason, and decision context.
2. Surface overrides in monitoring dashboards.
3. Analyze override patterns for training needs.

**Preventive controls:**

- Require a reason field in override UI.
- Alert when override rates spike.

---

## 15. Redaction Breaks Valid Traces

**Symptom:** After adding redaction rules, traces become unreadable or fail compliance tests.

**Likely cause:** Redaction patterns are too broad or tokenization is naive.

**Resolution:**

1. Collect representative trace samples.
2. Tune regex patterns or switch to structured data masking.
3. Add quality checks for redacted output.
4. Allow allowlists for known safe content.

**Preventive controls:**

- Add redaction tests in CI.
- Review redacted trace samples quarterly.
- Use token-level masking when regex is insufficient.

---

## 16. Model Risk File Is Stale

**Symptom:** Decision makers rely on outdated use cases, limitations, or fallback plans.

**Likely cause:** No review cadence or ownership is unclear.

**Resolution:**

1. Assign a current owner.
2. Review and revalidate quarterly.
3. Link to release evidence automatically.

**Preventive controls:**

- Set expiration reminders for risk file entries.
- Require a current risk file before any material change.

---

## 17. Release Evidence Is Missing Links

**Symptom:** Reviewers cannot navigate from the system register to evaluation results, security reviews, or privacy reviews.

**Likely cause:** Links are copied manually and drift over time.

**Resolution:**

1. Use structured artifact storage with stable IDs.
2. Populate release templates via automation.
3. Add a validation step that checks link freshness.

**Preventive controls:**

- Automate release evidence generation.
- Alert when evidence expires before the next review.

---

## 18. Incident Response Is Sluggish

**Symptom:** Compliance incidents take too long to triage, contain, and resolve.

**Likely cause:** Runbooks are generic, roles are unclear, or alerting is insufficient.

**Resolution:**

1. Update runbooks with system-specific steps.
2. Define on-call roles and escalation paths.
3. Conduct tabletops for model, prompt, and tool incidents.
4. Measure and track MTTR.

**Preventive controls:**

- Automate containment where possible (rollout, feature flag, circuit breaker).
- Rotate on-call contacts and validate reachability.
- Review incident response after every compliance event.

---

## 19. Appendix

## Common Root Causes

| Symptom | Likely Cause | Preventive Control |
|---------|--------------|--------------------|
| Untracked processing | No audit event emitted | Mandatory audit hook |
| Missing consent | Consent collected outside registry | Centralized consent capture |
| Model upgrade breakage | Model not treated as dependency | Version lock, eval gate |
| Logging gaps | Ad-hoc integrations bypass audit | Central tool registry |
| Retention lapses | Manual purge only | Automated TTL and tests |
| Jurisdiction mismatch | Late region detection | Early classification |
| Exceptions never expire | Manual tracking only | Automated expiry alerts |
| Audit schema drift | No standard contract | Canonical schema enforcement |

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)

## Decision Trees

Use decision trees for high-frequency issues:

1. Sensitive data in logs
  - Yes: activate redaction tests and retention controls
  - No: proceed
2. Model upgrade failure
  - Yes: activate rollback and evaluation
  - No: proceed
3. Human review gap
  - Yes: review workflow and reviewer coverage
  - No: proceed

## Example Runbook Summary

- Summary of step, owner, and estimated time for each troubleshooting block.
- Ensure each resolution includes preventive control.

## Periodic Review Schedule

- Weekly: review new incidents and exceptions.
- Monthly: review audit logs, False positive alerts, and retention metrics.
- Quarterly: policy review, control owner catch-up, and evidence refresh.
- Annually: risk assessment and training refresh.

## Metrics to Track

- Policy violation rate
- Retention compliance rate
- Audit completeness rate
- Human review coverage
- Data subject request fulfillment time
- Exception backlog
- Model risk review age

## Continuous Improvement Loop

1. Collect issue signals from audits, incidents, and user feedback
2. Classify root cause
3. Assign owner
4. Implement control fix
5. Update checklist
6. Re-run tests
7. Communicate change
8. Schedule verification

## Closing Notes

Troubleshooting is most effective when controls, training, and monitoring are mature. Repeat issues often indicate that preventive controls are missing.

## Resolution Techniques by Tier

| Issue Tier | Typical Resolution | Tooling Support |
|------------|-------------------|------------------|
| P0 | Policy enforcement, feature flags, rollback | Automated gates + human review |
| P1 | UI remediation, training, alert tuning | Product update + comms |
| P2 | Runbook refresh, documentation | Documentation tooling |
| P3 | Monitoring tuning | Dashboard and alert config |

## Common Escalation Paths

- Compliance -> Legal -> Executive for regulatory exposure
- Compliance -> Security -> Engineering for technical control gaps
- Compliance -> Product -> Engineering for user-facing mitigations

## Release Block Handling

If a compliance issue blocks a release:

1. Document the blocking issue and risk accepted or not accepted.
2. Define a remediation plan with deadline and owner.
3. Require sign-off from compliance and legal before proceeding.
4. Schedule follow-up review.

## Reference Standards

- SOC 2 for audit and evidence
- ISO/IEC 27001 for security controls
- NIST SP 800-53 for control baselines
- GDPR for EU privacy requirements
- CCPA for California privacy requirements
- HIPAA for healthcare data handling
- PCI DSS for card data handling
- CSA CCM for cloud controls
- MITRE ATLAS for adversarial threats
- OWASP Top 10 for LLMs for prompt injection and abuse
- EU AI Act for high-risk classification and conformity
- LGPD for Brazil privacy requirements
- India DPDP Act for India data
- China PIPL for China data
- Singapore PDPA for Singapore data