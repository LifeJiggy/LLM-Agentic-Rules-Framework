# Compliance Domain - Anti-Patterns

## Overview

This document outlines compliance anti-patterns to avoid in LLM/agentic systems.

---

## Table of Contents

1. [Untracked Data Processing](#1-untracked-data-processing)
2. [Missing Consent Recording](#2-missing-consent-recording)
3. [Unauditable Decisions](#3-unauditable-decisions)
4. [Overly Broad Permissions](#4-overly-broad-permissions)
5. [No Retention Controls](#5-no-retention-controls)
6. [Ignoring Jurisdiction Rules](#6-ignoring-jurisdiction-rules)
7. [Hardcoded Policy in Prompts](#7-hardcoded-policy-in-prompts)
8. [Unmonitored Production Behavior](#8-unmonitored-production-behavior)
9. [Unbounded Tool Use](#9-unbounded-tool-use)
10. [No Incident Playbook](#10-no-incident-playbook)
11. [Shadow Tooling](#11-shadow-tooling)
12. [Dual-Use Blindness](#12-dual-use-blindness)
13. [Audit Log Gaps](#13-audit-log-gaps)
14. [Noise-Heavy Redaction](#14-noise-heavy-redaction)
15. [Compliance-by-Checklist-Only](#15-compliance-by-checklist-only)
16. [Vendor Naivety](#16-vendor-naivety)
17. [Bad Rollback Hygiene](#17-bad-rollback-hygiene)
18. [Prompt Leakage of Rules](#18-prompt-leakage-of-rules)
19. [Weak Consent Recording](#19-weak-consent-recording)
20. [Retention Drift](#20-retention-drift)
21. [Secret Sprawl](#21-secret-sprawl)
22. [Lagging Exception Management](#22-lagging-exception-management)
23. [Incomplete Vendor Coverage](#23-incomplete-vendor-coverage)
24. [Missing Legal Holds](#24-missing-legal-holds)
25. [Opaque Automation Without Review](#25-opaque-automation-without-review)
26. [Unclear Ownership](#26-unclear-ownership)
27. [Noise-First Monitoring](#27-noise-first-monitoring)
28. [Uncontrolled A/B Testing](#28-uncontrolled-ab-testing)
29. [Appendix](#29-appendix)

---

## 1. Untracked Data Processing

```python
# Bad - No data lineage
def process_user_data(data):
    return model.generate(str(data))  # Where did data come from?

# Good - Tracked processing
def process_user_data(data, purpose="assistant_response"):
    # Log processing event
    audit_log.append({
        "data_source": data.get("source"),
        "purpose": purpose,
        "timestamp": datetime.utcnow()
    })
    return model.generate(str(data))
```

### Symptoms

- Cannot answer "where did this data come from"
- Retraining plans lack evidence pipelines
- Incident response is reactive and incomplete

### Fixes

- Add purpose context before any data enters the prompt
- Store hashes instead of raw records when possible
- Classify rows before any transformation

---

## 2. Missing Consent Recording

```python
# Bad - Assume consent
def collect_data():
    userdata = get_all_user_data()
    return train_model(userdata)

# Good - Explicit consent
def collect_data():
    consent = get_user_consent("train_model")
    if not consent:
        return None
    
    audit_log.record_consent(user_id, "train_model", consent.timestamp)
    return train_model(get_user_data())
```

### Symptoms

- Data subject access requests fail
- Build evidence that contradicts privacy notices
- Rollout blocked without retroactive consent capture

### Fixes

- Record purpose, timestamp, and version of consent receipt
- Tie consent to user identifiers and flows
- Gate data use through a consent manifest

---

## 3. Una auditable Decisions

```python
# Bad - No decision trail
def make_decision(input):
    return model.generate(input)  # Who decided this?

# Good - Auditable
def make_decision(input, session_id):
    decision = model.generate(input)
    audit_log.record({
        "session_id": session_id,
        "input": hash_input(input),
        "decision": decision,
        "model_version": current_model,
        "timestamp": datetime.utcnow()
    })
    return decision
```

### Symptoms

- Regulators cannot trace the decision path
- Model changes create unexplained behavior shifts
- Recurring error patterns go unnoticed

### Fixes

- Emit one audit event per decision
- Hash sensitive fields and attach provenance metadata
- Attach model and prompt versions to every recorded decision

---

## 4. Overly Broad Permissions

### Bad

```python
# Service accounts with wildcard access
ALLOWED_TOOLS = ["*"]
```

### Good

```python
ALLOWED_TOOLS = {
    "support_agent_v1": ["search_help_center", "read_order"],
    "admin_v1": ["search_help_center", "read_order", "update_note"],
}
```

### Symptoms

- Single compromised account enables broad damage
- No separation of duties
- Difficulty demonstrating least privilege in audits

### Fixes

- Use attribute or role-based access for each tool and flow
- Review permission grants quarterly
- Separate test and production permissions

---

## 5. No Retention Controls

### Bad

```python
def save_trace(trace):
    db.traces.insert(trace)  # Never deleted
```

### Good

```python
def save_trace(trace):
    db.traces.insert(trace)
    if should_purge(trace):
        db.traces.delete(trace["id"])
```

### Symptoms

- Blast radius of leaks is larger than necessary
- Discovery costs in litigation explode
- Data residency rules cannot be enforced

### Fixes

- Define retention periods per data class
- Enforce automated purges and archiving
- Implement legal holds where required

---

## 6. Ignoring Jurisdiction Rules

### Bad

```python
def route_request(request):
    return DEFAULT_REGION
```

### Good

```python
def route_request(request):
    jurisdiction = request.user.jurisdiction
    return JURISDICTION_ROUTES[jurisdiction]
```

### Symptoms

- Cross-border transfers happen without safeguards
- Privacy notices do not match local law
- Model outputs omit region-specific disclosures

### Fixes

- Resolve jurisdiction at request boundary
- Keep legal text external to model prompts
- Validate behavior in CI for each jurisdiction

---

## 7. Hardcoded Policy in Prompts

### Bad

```markdown
You are a compliance-aware assistant. Always refuse medical advice.
```

### Good

```python
POLICY_DISCLOSURE = load("compliance_disclosure_{jurisdiction}.txt")

system_prompt = f"""
{POLICY_DISCLOSURE}
"""
```

### Symptoms

- Policy changes require prompt retraining
- Legal text silently drifts from authoritative documents
- Cannot support jurisdiction-specific disclosures

### Fixes

- Use externalized policy snippets
- Keep policy text editable by non-engineers
- Version policy changes independently from model versions

---

## 8. Unmonitored Production Behavior

### Bad

"Evals pass; release it"

### Good

Monitor policy violation rates, output samples, appeals, and tool calls.

### Symptoms

- Behavior regressions reach users before eval reruns
- User complaints are not linked to model versions
- Tool-call volume drops after releases without alerts

### Fixes

- Add monitoring, alerting, and dashboards
- Sampled review of production outputs
- Re-evaluate on any model or prompt change

---

## 9. Unbounded Tool Use

### Bad

```python
def agent_loop(goal):
    while not done:
        tool = choose_tool()
        result = tool()
```

### Good

```python
def agent_loop(goal, max_tool_calls=20):
    calls = 0
    while not done and calls < max_tool_calls:
        tool = choose_tool()
        if tool.requires_approval():
            approval = request_human(goal, tool)
            if not approval:
                break
        result = tool()
        calls += 1
```

### Symptoms

- High-cost credential exhaustion
- Irreversible actions performed without review
- Audit gaps between tool calls

### Fixes

- Cap tool-call depth and breadth
- Require approval or confirmation for high-impact actions
- Log tool call reason, input, output, and actor

---

## 10. No Incident Playbook

### Bad

"We will figure it out if something happens"

### Good

Maintain runbooks and response contacts for each risk tier.

### Symptoms

- Teams react inconsistently under pressure
- Legal and communications are late
- Evidence is lost or tampered with

### Fixes

- Maintain reviewed runbooks
- Rotate on-call and escalation contacts
- Conduct tabletops for model, prompt, and tool changes

---

## 11. Shadow Tooling

### Bad

Custom ad-hoc integrations that bypass internal APIs

### Good

Formal tool registry with policy and audit hooks

### Symptoms

- Data leaks through unsupported channels
- Failures lack predictable handling
- Owners and approval history are missing

### Fixes

- Registry for all tools and integrations
- Policy checks on registration
- Deprecate shadow tools with migration runbooks

---

## 12. Dual-Use Blindness

### Bad

Focus only on intended use cases

### Good

Assess harmful applications and implement guardrails

### Symptoms

- Controls miss attack paths
- Review questions come too late
- Red team scenarios are absent

### Fixes

- Run red-teaming before major releases
- Maintain a dual-use risk register
- Review controls against misuse scenarios

---

## 13. Audit log gaps

### Bad

Audit logs that omit tool calls, approval records, and jurisdiction context

### Good

Immutable audit events with full traceability

### Symptoms

- Reviewers question completeness
- Incident reconstruction fails
- Evidence packages are rejected

### Fixes

- Emit one audit event per high-impact action
- Store event hashes and chain verification
- Include jurisdiction and actor context

---

## 14. Noise-heavy redaction

### Bad

Rules that redact content aggressively, corrupting utility

### Good

Domain-aware redaction with allowlists

### Symptoms

- Meaningful traces become unreadable
- Debugging is impaired
- Reviewers lose trust in redaction tooling

### Fixes

- Build redaction with intended downstream tasks in mind
- Validate against trace quality metrics
- Allow structured exceptions with review

---

## 15. Compliance-by-checklist-only

### Bad

Treating compliance as a periodic checkbox exercise

### Good

Continuous measurement, evidencing, and adaptation

### Symptoms

- Controls atrophy after the audit window
- Evidence is stale
- Actual risk levels diverge from assumed maturity

### Fixes

- Measure compliance continuously
- Retire controls that no longer serve a risk
- Review policy against operational reality quarterly

---

## 16. Vendor naivety

### Bad

Assuming third-party models and tools are compliant by default

### Good

Maintain vendor register, DPA records, and subprocessor list

### Symptoms

- Third-party data flows are unclassified
- Regional restrictions are not enforced
- Contractual obligations drift

### Fixes

- Maintain vendor register, DPA records, and subprocessor list
- Review vendor security attestations at agreed intervals
- Enforce contractual controls in tooling

---

## 17. Bad rollback hygiene

### Bad

No tested rollback or fallback path

### Good

Runbook and automated fallback policy

### Symptoms

- Recovering from incidents takes hours
- Fallback model changes behavior unexpectedly
- Last evaluated version is unknown

### Fixes

- Maintain active fallback versions
- Re-run evals on fallback before relying on it
- Automate where possible with circuit breakers

---

## 18. Prompt leakage of rules

### Bad

Including confidential policy or security rules in prompt text

### Good

Keep policy outside prompts, enforce through tooling

### Symptoms

- Attackers extract rules from outputs
- Legal texts change but prompts remain stale
- Audit identifies policy drift through model outputs

### Fixes

- Externalize policy text
- Restrict who can author prompt templates
- Review outputs for policy leakage in red-teaming

---

## 19. Weak Consent Recording

### Bad

Recording consent as a timestamp only, without purpose or version

### Good

Store structured consent receipts including purpose, timestamp, manifest version, and user ID

### Symptoms

- Cannot prove purpose-specific consent
- Consent disputes are difficult to resolve
- Privacy notices contradict actual practice

### Fixes

- Store consent as structured records
- Include purposeful fields in audit events
- Define a consent receipt schema

---

## 20. Retention Drift

### Bad

Retention policies that exist in documents but are not implemented correctly

### Good

Configuration-backed retention policies with automated enforcement and periodic audits

### Symptoms

- Requests for deletion cannot be satisfied
- Legal hold does not prevent deletion
- Storage costs grow unexpectedly

### Fixes

- Automate retention workers
- Test purge behavior with synthetic data
- Alert when retention backlog grows

---

## 21. Secret Sprawl

### Bad

Storing API keys and credentials in code, prompts, logs, or CI variables without centralized control

### Good

Centralized secret management, scoped credentials, and rotation policies

### Symptoms

- Keys are exposed in logs or versions
- Rotation is unknown or manual
- Scope is broader than needed

### Fixes

- Use a secret manager with fine-grained roles
- Inject secrets at runtime
- Rotate on a calendar or on compromise

---

## 22. Lagging Exception Management

### Bad

Exceptions with no owner, no expiration date, and no risk reconciliation

### Good

Time-bounded exceptions with owner, review date, and compensating controls

### Symptoms

- Controls are permanently weakened
- Regulations cite missing exception management
- Risk posture is unknown

### Fixes

- Require owner, expiry, and rationale per exception
- Create a review cycle for exceptions
- Automate expiration alerts

---

## 23. Incomplete Vendor Coverage

### Bad

Knowledge of some vendors but not all subprocessors or data flows

### Good

Continuous vendor register updates, with DPA and risk assessment for each processor

### Symptoms

- New model provider onboarded without DPA
- Unknown subprocessor handling personal data
- Contractual obligations drift

### Fixes

- Make vendor registration part of onboarding
- Reconcile vendor register quarterly
- Block production releases without vendor compliance artifacts

---

## 24. Missing Legal Holds

### Bad

Deletion occurs while litigation or investigation is pending

### Good

Legal hold mechanisms that suspend deletion for relevant identifiers

### Symptoms

- Evidence is lost during active investigation
- Regulatory penalties for destruction of records
- Inability to respond to discovery requests

### Fixes

- Place legal holds through a dedicated workflow
- Validate hold enforcement before deletion runs
- Review hold log entries at audit time

---

## 25. Opaque Automation Without Review

### Bad

Automation that runs at scale without human review or auditability

### Good

Automated steps that remain auditable and reviewable, with clear handoffs to human oversight

### Symptoms

- Unexplained changes in user experience
- User harm goes undetected
- Compliance coverage does not span automation

### Fixes

- Design for human review at key decision gates
- Capture automation decisions in audit trails
- Sample automated outputs for quality and bias

---

## 26. Unclear Ownership

### Bad

No named owner for models, datasets, tools, or workflows

### Good

Ownership registry with named contacts and up-to-date metadata

### Symptoms

- No one is accountable for decisions or incidents
- Releases proceed without review
- Data subject requests stall

### Fixes

- Require ownership metadata on registration
- Rotate owners proactively
- Include owner contact in system register

---

## 27. Noise-First Monitoring

### Bad

Alerting on every metric movement without tuning

### Good

Tuned policy-violation metrics with severity routing and on-call playbooks

### Symptoms

- Alert fatigue
- Real violations are missed among the noise
- Teams disable or mute alerts

### Fixes

- Prioritize alerts by risk tier and severity
- Conduct regular false-positive reviews
- Automate triage where possible

---

## 28. Uncontrolled A/B Testing

### Bad

Experimentation applied to compliance-relevant outputs without auditing or review

### Good

Experiments with rollback plans, treatment/control monitoring, and evidence collection

### Symptoms

- User harm occurs under a new treatment
- Differential treatment across groups is undetected
- Evidence linking treatment to impact is weak

### Fixes

- Define experiment governance rules by risk tier
- Include compliance metrics as guardrails
- Require signed experiment records

---

## 29. Appendix

## Anti-Pattern Summary Table

| Anti-Pattern | Risk | Signal | Fix |
|--------------|------|--------|-----|
| Untracked processing | Privacy, lineage | Cannot map data to workflow | Emit audit event with source |
| Missing consent | Legal | DSAR impossible | Store purpose-keyed consent receipts |
| Una auditable decisions | Governance | No decision path | Record input hash, model version |
| Overly broad permissions | Security, least privilege | Wildcard grants reviewed | Use role-based tool grants |
| No retention controls | Privacy, cost, discovery | Data never purged | Enforce retention |
| Ignoring jurisdiction rules | Regional law | Cross-border gaps | Route by jurisdiction config |
| Hardcoded policy in prompts | Compliance drift | Prompt-only policy | Externalize policy text |
| Unmonitored production | Regression | User complaints before alerts | Sample production outputs |
| Unbounded tool use | Safety, cost | Infinite tool loops | Cap tool calls and require approval |
| No incident playbook | Resilience | Inconsistent response | Maintain runbooks |
| Shadow tooling | Audit, security | Unknown integrations | Formal tool registry |
| Dual-use blindness | Safety | Controls miss misuse | Run red teamings |
| Audit log gaps | Evidence | Incomplete traces | Emit full audit events |
| Noise-heavy redaction | Utility | Redacted traces unusable | Domain-aware redaction |
| Compliance-by-checklist | Governance | Controls atrophy | Continuous measurement |
| Vendor naivety | Third-party risk | Unknown data flows | Maintain vendor register |
| Bad rollback hygiene | Reliability | Long incident recovery | Tested fallback policy |
| Prompt leakage of rules | Security, compliance | Attackers extract rules | Externalize policy |
| Weak consent recording | Legal | Consent evidence gaps | Structured consent receipts |
| Retention drift | Privacy, legal | Deletion and hold failures | Automated retention |
| Secret sprawl | Security | Exposed credentials | Secret manager |
| Lagging exception management | Governance | Stale exceptions | Time-bounded exceptions |
| Incomplete vendor coverage | Regulatory | Unplanned processors | Vendor register enforcement |
| Missing legal holds | Legal | Evidence loss | Legal hold workflow |
| Opaque automation | Accountability | Unexplained scale harms | Review gates and audit trails |
| Unclear ownership | Governance | No accountability | Ownership registry |
| Noise-first monitoring | Reliability | Alert fatigue | Tuned alerting |
| Uncontrolled A/B testing | Risk | Unaudited experiments | Experiment governance |

```markdown
## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
```

## Operational Impact of Anti-Patterns

Untracked data processing, missing consent recording, unauditable decisions, overly broad permissions, no retention controls, ignoring jurisdiction rules, hardcoded policy in prompts, unmonitored production behavior, unbounded tool use, no incident playbook, shadow tooling, dual-use blindness, audit log gaps, noise-heavy redaction, compliance-by-checklist-only, vendor naivety, bad rollback hygiene, prompt leakage of rules, weak consent recording, retention drift, secret sprawl, lagging exception management, incomplete vendor coverage, missing legal holds, opaque automation without review, unclear ownership, noise-first monitoring, and uncontrolled A/B testing are not just technical failures; they are governance failures.

Each anti-pattern erodes trust, increases legal exposure, and degrades the effectiveness of controls. Removing one anti-pattern often requires changes to tooling, policy, training, and measurement, not just code.

## Remediation Playbook

1. Triage: Identify the most severe anti-pattern in your system.
2. Contain: Add safeguards or gates that minimize further exposure.
3. Assess: Document the risk, affected users, and regulatory exposure.
4. Fix: Implement control improvements.
5. Verify: Run evals, audits, and tests.
6. Evict: Remove compensating controls once the fix is stable.
7. Document: Update runbooks and training.
8. Review: Schedule a post-incident review.

## Anti-Pattern Prioritization Examples

| Rank | Anti-Pattern | Typical Trigger |
|------|--------------|-----------------|
| 1 | Untracked data processing | Audit finding |
| 2 | Missing consent recording | Privacy review |
| 3 | No retention controls | Legal hold violation |
| 4 | Unauditable decisions | Incident investigation |
| 5 | Overly broad permissions | Pen test |
| 6 | Unbounded tool use | Cost anomaly |
| 7 | Ignoring jurisdiction rules | Regional complaint |
| 8 | Hardcoded policy prompts | Legal review |
| 9 | Secret sprawl | Key exposure |
| 10 | No incident playbook | Incident |

## Recommended Training

- Train engineers on data minimization and classification.
- Train reviewers on oversight and override rules.
- Train operators on incident response and runbooks.
- Train procurement on vendor assessment and DPAs.
- Train leadership on exception and risk acceptance criteria.

## Feedback Loop

Use incidents, audits, user complaints, and red-teaming findings as inputs to:

- Tune controls
- Adjust review thresholds
- Update training content
- Refresh exception register
- Revise policies