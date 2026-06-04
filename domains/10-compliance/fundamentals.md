# Compliance Domain - Fundamentals

> Foundational compliance concepts for LLM and agentic systems that handle users, data, decisions, regulated workflows, or externally visible outputs.

## Overview

Compliance for AI systems is the practice of proving that the system operates within legal, contractual, ethical, and organizational requirements. For LLM and agentic systems, compliance must cover both traditional software controls and model-specific risks such as opaque reasoning, generated content, tool use, data leakage, autonomy, and evaluation drift.

---

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Accountability](#2-accountability)
3. [Lawful and Fair Processing](#3-lawful-and-fair-processing)
4. [Transparency](#4-transparency)
5. [Human Oversight](#5-human-oversight)
6. [Compliance Scope](#6-compliance-scope)
7. [Risk Tiers](#7-risk-tiers)
8. [Data Governance](#8-data-governance)
9. [Model Behavior](#9-model-behavior)
10. [Tool Access](#10-tool-access)
11. [Audit Trail](#11-audit-trail)
12. [Privacy Basics](#12-privacy-basics)
13. [Security Basics](#13-security-basics)
14. [Governance Basics](#14-governance-basics)
15. [Monitoring Basics](#15-monitoring-basics)
16. [Vendor Basics](#16-vendor-basics)
17. [Incident Response Basics](#17-incident-response-basics)
18. [International Compliance Basics](#18-international-compliance-basics)
19. [Ethical AI Basics](#19-ethical-ai-basics)
20. [Technical Controls Overview](#20-technical-controls-overview)
21. [Mental Model for Compliance](#21-mental-model-for-compliance)
22. [Appendix](#22-appendix)

---

## 1. Core Principles

These principles are the foundation for every compliance decision in an AI system:

- Accountability: named ownership and decision paths
- Lawfulness: valid legal basis for processing
- Fairness: unbiased treatment and outcomes where possible
- Transparency: clear disclosure and auditability
- Safety: minimization of harm and misuse
- Security: protection against unauthorized access or disclosure
- Human Oversight: review and control for high-impact decisions
- Documentation: durable records and evidence

## 2. Accountability

Every production AI workflow needs a named owner, a documented purpose, and a decision path for approving high-risk behavior.

- Assign ownership for each model, agent, tool, and data source.
- Define who can approve deployments and policy exceptions.
- Keep a review trail for material changes.

## Owner Documentation

```python
class OwnerRegistry:
    def __init__(self):
        self.owners = {}

    def register(self, component: str, owner: str, contact: str):
        self.owners[component] = {
            "owner": owner,
            "contact": contact,
        }

    def get_owner(self, component: str) -> dict:
        return self.owners.get(component, {})
```

## Change Approval Requirement

```python
CHANGE_APPROVAL_REQUIRED = {
    "model_version": True,
    "system_prompt": True,
    "tool_permissions": True,
    "data_retention_policy": True,
}
```

## Material Change Criteria Examples

```python
MATERIAL_CHANGES = [
    "model_version",
    "retrieval_source",
    "tool",
    "fine_tuning_job",
    "system_prompt",
    "data_processing_purpose",
    "jurisdiction_coverage",
    "retention_policy",
]
```

## 3. Lawful and Fair Processing

Collect, process, and retain data only when there is a valid business and legal basis.

- Document the purpose for each data category.
- Minimize personal and sensitive data.
- Avoid using production user data in prompts, logs, or evaluations unless approved.

## Legal Basis Catalog

| Legal Basis | Typical Use |
|-------------|-------------|
| Consent | User-driven services with optional data use |
| Contract | Data necessary to perform the service |
| Legal obligation | Data required for reporting or compliance |
| Vital interests | Emergency response data |
| Public task | Government service operation |
| Legitimate interest | Balanced business need with user rights |

## Purpose Limitation Enforcement

```python
class PurposeLimiter:
    def __init__(self):
        self.purpose_registry = {
            "user_id": ["processing", "billing"],
            "email": ["processing", "support", "marketing"],
            "messages": ["processing"],
        }

    def can_process(self, field: str, purpose: str) -> bool:
        return purpose in self.purpose_registry.get(field, [])

    def filter_purposes(self, record: dict, allowed: list) -> dict:
        allowed_fields = set()
        for field, purposes in self.purpose_registry.items():
            if any(p in allowed for p in purposes):
                allowed_fields.add(field)
        return {k: v for k, v in record.items() if k in allowed_fields}
```

## 4. Transparency

Users and operators should understand when AI is involved and what the system can and cannot do.

- Disclose AI assistance where required.
- Document known limitations.
- Provide escalation paths for contested outcomes.

## Disclosure Requirements

- When a user is interacting with an AI system.
- When AI-generated content is presented as authoritative.
- When decisions made by AI affect user rights, finances, or access.
- How to request human review.
- How to file complaints or appeals.

## Limitations Documentation Template

```markdown
System Limitations
1. May produce incorrect factual claims.
2. Should not be relied on for medical, legal, or financial advice.
3. May reflect historical biases present in training data.
4. Confidence scores are not calibrated guarantees.
```

## Escalation Path Documentation

```python
ESCALATION_PATH = {
    "technical_issue": "support@example.com",
    "harms_complaint": "trust_and_safety@example.com",
    "privacy_request": "privacy@example.com",
    "data_subject_request": "privacy@example.com",
}
```

## 5. Human Oversight

Use human review for workflows that can materially affect rights, safety, finances, employment, healthcare, legal status, or access to critical services.

- Define review thresholds.
- Preserve context needed for review.
- Make overrides auditable.

## Review Threshold Definition

```python
REVIEW_THRESHOLDS = {
    "high_stakes": True,
    "low_confidence": 0.8,
    "sensitive_action": True,
    "contentious_category": ["legal", "medical", "financial"],
    "first_interaction_with_vulnerable_user": True,
}
```

## Override Auditing

```python
class HumanOverrideAuditor:
    def __init__(self, audit_log):
        self.audit_log = audit_log

    def record(self, session_id: str, reviewer: str, reason: str):
        self.audit_log.append({
            "session_id": session_id,
            "reviewer": reviewer,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        })
```

## Review Context Packaging

```python
def package_review_context(session) -> dict:
    return {
        "session_id": session.id,
        "user_message": session.user_message,
        "assistant_reply": session.assistant_reply,
        "tools_called": session.tools_called,
        "model_version": session.model_version,
        "timestamp": session.timestamp,
        "risk_tier": session.risk_tier,
        "jurisdiction": session.jurisdiction,
    }
```

## 6. Compliance Scope

| Area | What To Document |
|------|------------------|
| System purpose | Intended use, prohibited use, target users |
| Data processing | Sources, retention, consent or legal basis |
| Model behavior | Capabilities, limitations, evaluation results |
| Tool access | Permissions, side effects, approval requirements |
| Human oversight | Review points, escalation paths, override rules |
| Audit trail | Logs, approvals, incidents, model/version changes |
| Security controls | Authentication, authorization, network topology |
| Privacy controls | Minimization, retention, consent, data-subject rights |
| Incident response | Runbooks, contacts, escalation |
| Vendor governance | DPA, subprocessors, attestations |

## 7. Risk Tiers

| Tier | Description | Minimum Control |
|------|-------------|-----------------|
| Low | Internal productivity or low-impact assistance | Basic logging and documented owner |
| Medium | Customer-facing guidance or workflow automation | Evaluation, monitoring, privacy review |
| High | Decisions with financial, legal, safety, or rights impact | Human review, formal risk assessment, audit trail |
| Prohibited | Uses banned by law, policy, or contract | Block at design and access-control layers |

## Risk Tier Assignment Criteria

```python
def assign_risk_tier(system_profile: dict) -> str:
    if system_profile.get("affects_legal_rights") or system_profile.get("affects_safety"):
        return "high"
    if system_profile.get("customer_facing") and system_profile.get("processes_personal_data"):
        return "medium"
    if system_profile.get("internal_only") and not system_profile.get("uses_real_user_data"):
        return "low"
    return "medium"
```

## 8. Data Governance

## Data Inventory

```python
class DataInventory:
    def __init__(self):
        self.assets = {}

    def register(self, asset_id: str, description: str, owner: str, classification: str):
        self.assets[asset_id] = {
            "description": description,
            "owner": owner,
            "classification": classification,
            "registered_at": datetime.utcnow().isoformat(),
        }

    def list_by_owner(self, owner: str) -> list:
        return [a for a in self.assets.values() if a["owner"] == owner]
```

## Sensitivity Classification

| Classification | Examples | Handling |
|----------------|----------|----------|
| Public | Published marketing content | Standard controls |
| Internal | Internal wiki, employee handbook | Access restricted to employees |
| Confidential | Customer data, business plans | Encryption required |
| Restricted | Health data, payment data | Strong access control and audit |

## Data Quality Checks

```python
class DataQualityChecker:
    def __init__(self):
        self.checks = []

    def check_completeness(self, record: dict, required_fields: list) -> bool:
        return all(field in record for field in required_fields)

    def check_freshness(self, timestamp: str, max_age_days: int = 30) -> bool:
        dt = datetime.fromisoformat(timestamp)
        return (datetime.utcnow() - dt).days <= max_age_days
```

## 9. Model Behavior

## Capability Documentation

- Prompting strengths and weaknesses.
- Languages and cultures represented.
- Context window and token limits.
- Known failure modes.
- Intended task scope.

## Evaluation Coverage

- Safety and toxicity.
- Fairness/disparate impact.
- Accuracy on representative inputs.
- Robustness to formatting drift.
- Tool use safety.

## Evaluation Result Template

```markdown
Evaluation Result
- Date:
- Model version:
- Dataset:
- Overall score:
- Failure cases:
- Disparate impacts:
- Review outcome:
```

## 10. Tool Access

- Inventories tool names, versions, and owners.
- Maps tools to permissions.
- Distinguishes read vs write actions.
- Defines fallback behavior.
- Documents side effects.

## Tool Permission Matrix

```python
TOOL_PERMISSIONS = {
    "read_order_status": ["agent", "support"],
    "update_order_note": ["support"],
    "send_email": ["support", "admin"],
    "issue_refund": ["admin"],
}
```

## Side Effect Documentation

```markdown
Tool: send_email
Side effects: Sends externally visible email
Reversibility: Irreversible
Mitigations: Human review required before send
Owner: support-lead
```

## 11. Audit Trail

## Minimum Audit Event Fields

- Event ID
- Timestamp
- Actor
- Action
- Resource
- Outcome
- Session or request ID
- Jurisdiction
- Classification
- Metadata hash or linked artifacts

## Audit Log Schema Example

```python
AUDIT_LOG_SCHEMA = {
    "event_id": "uuid",
    "timestamp": "iso8601",
    "actor": "string",
    "actor_type": "user|service|model",
    "action": "string",
    "resource": "string",
    "outcome": "success|failure|denied",
    "session_id": "string",
    "jurisdiction": "string",
    "classification": "string",
    "metadata": "dict",
}
```

## Log Integrity Mechanisms

```python
class IntegrityChain:
    def __init__(self):
        self.chain = []

    def append(self, event: dict):
        event = dict(event)
        event["hash"] = self._hash(event)
        if self.chain:
            event["previous_hash"] = self.chain[-1]["hash"]
        else:
            event["previous_hash"] = None
        self.chain.append(event)

    def verify(self) -> bool:
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr["previous_hash"] != prev["hash"]:
                return False
        return True

    def _hash(self, event: dict) -> str:
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()
```

## 12. Privacy Basics

## PII Identification

- Direct identifiers: names, emails, phone numbers, addresses.
- Indirect identifiers: IP addresses, device IDs, user IDs.
- Sensitive attributes: race, health, religion, biometrics.
- Contextual sensitivity: query history, session behavior.

## Minimization Tactics

- Limit collection fields.
- Redact before logging.
- Use hashing or tokenization.
- Apply purpose restrictions.
- Limit retention through lifecycle automation.

## 13. Security Basics

## Authentication Requirements

- Unique identity per actor.
- Strong authentication for privileged roles.
- Session hygiene for interactive agents.

## Authorization Principles

- Deny by default.
- Grant minimum needed.
- Evaluate authorization on each action.
- Audit both granted and denied actions.

## Secret Management

- Store API keys, credentials, and tokens in a secret manager.
- Rotate secrets on schedule.
- Audit secret access.
- Avoid secrets in prompts and logs.

## Threat Model Basics

- Identify assets and trust boundaries.
- Catalog threats relevant to AI systems (jailbreaks, data leakage, model theft, misuse).
- Define mitigations in control terms.

## 14. Governance Basics

## Policy Controls

- Published, reviewed, and versioned.
- Tied to risk tier and jurisdiction.
- Mapped to technical enforcement where possible.

## Exception Management

Exceptions should have:

- Owner and expiration date.
- Documented rationale.
- Mitigating controls in place.
- A review date.

```python
class ExceptionRegister:
    def __init__(self):
        self.exceptions = {}

    def add(self, exception_id: str, owner: str, expires_on: str, rationale: str):
        self.exceptions[exception_id] = {
            "owner": owner,
            "expires_on": expires_on,
            "rationale": rationale,
            "active": True,
        }

    def expire(self):
        now = datetime.utcnow().date().isoformat()
        for exc in self.exceptions.values():
            if exc["expires_on"] < now:
                exc["active"] = False
```

## 15. Monitoring Basics

What to monitor:

- Policy violation rates.
- User appeals and complaints.
- Output sampling results.
- Tool call volumes and failures.
- Model version-level metrics.

Qualitative monitoring:

- Review sampled outputs for quality, bias, and leakage.
- Track reviewer agreement on oversight decisions.

## 16. Vendor Basics

- Maintain vendor register and DPA records.
- Track subprocessors and data flows.
- Review security attestations.
- Confirm contractual controls are reflected in tooling.

## 17. Incident Response Basics

Incident response basics:

- Detect, classify, contain, recover, and review.
- Maintain runbooks per high-impact workflow.
- Define notification timeline and contacts.

## Incident Severity Levels

| Severity | Criteria | Response SLA |
|----------|----------|--------------|
| Critical | Data breach, safety event, regulatory exposure | 1 hour |
| High | Significant user harm, large-scale service degradation | 4 hours |
| Medium | Localized impact, manageable user confusion | 24 hours |
| Low | Cosmetic or minimal impact | 72 hours |

## 18. International Compliance Basics

## Multi-Jurisdiction Considerations

- GDPR (EU, EEA, UK)
- CCPA/CPRA (California)
- HIPAA (US healthcare)
- LGPD (Brazil)
- AI Act (EU)
- Local equivalents for Asia, Middle East, Africa

## Jurisdiction Mapping Example

```python
class JurisdictionMapper:
    def __init__(self):
        self.region_to_law = {
            "EU": "GDPR",
            "UK": "UK_GDPR",
            "CA": "CCPA",
            "US": "state_specific",
            "BR": "LGPD",
        }

    def applicable_law(self, jurisdiction_code: str) -> str:
        return self.region_to_law.get(jurisdiction_code, "general")
```

## 19. Ethical AI Basics

- Do no harm.
- Prevent unfair discrimination.
- Respect access to redress.
- Design for inclusion.
- Engage stakeholders.
- Conduct broad impact assessments.

## Ethics Evaluation Examples

```python
class EthicsEvaluator:
    def evaluate_transparency(self, system: dict) -> dict:
        return {
            "disclosure_complete": True,
            "limitations_documented": True,
            "user_contact_provided": True,
        }

    def evaluate_fairness(self, predictions, groups) -> dict:
        # placeholder
        return {
            "demographic_parity_ratio": 1.0,
            "equalized_odds": 1.0,
        }
```

## 20. Technical Controls Overview

## Controls by Layer

| Layer | Controls |
|-------|----------|
| Prompt and model | Prompt injection mitigation, output filtering, model selection |
| Retrieval | Source control, citation, freshness |
| Tool layer | Permission checks, approval gates, audit hooks |
| Storage | Encryption, access controls, retention, legal holds |
| Network | TLS, WAF, segmentation |
| Identity | MFA, RBAC, least privilege |
| Monitoring | Metrics, alerts, sampled output reviews |

## 21. Mental Model for Compliance

1. Claim: What law, policy, or contract obligation are we satisfying?
2. Control: Which technical, administrative, or physical control addresses it?
3. Evidence: What artifacts demonstrate that the control is implemented and effective?
4. Review: Who checks the evidence and how often?
5. Adaptation: When controls change as a result of audits, incidents, or regulations.

## 22. Appendix

## Why This Domain Matters

Compliance is not optional once AI systems touch users, regulated data, or externally visible automated decisions. compliance for AI systems is the practice of proving that the system operates within legal, contractual, ethical, and organizational requirements. For LLM and agentic systems, compliance must cover both traditional software controls and model-specific risks such as opaque reasoning, generated content, tool use, data leakage, autonomy, and evaluation drift.

## Glossary

| Term | Meaning |
|------|---------|
| PII | Personally identifiable information |
| DPIA | Data protection impact assessment |
| BAA | Business associate agreement |
| DPO | Data protection officer |
| SCC | Standard contractual clauses |
| DSR | Data subject request |
| PET | Privacy-enhancing technology |
| LLM | Large language model |

## Controls Catalog

- Identity and access controls
- Encryption key management
- Logging and audit controls
- Model evaluation controls
- Tool authorization controls
- Retention and legal hold controls
- Prompt and output filtering
- Human review and approval controls
- Vendor and supply chain controls
- Monitoring and response controls

## Claim, Control, Evidence Model

Use this model for every compliance artifact:

- Claim: A statement of obligation.
- Control: A method that addresses the obligation.
- Evidence: A supporting artifact that the control operates as intended.

## Governance Meeting Cadences

- Weekly: release and exception review
- Monthly: control owner catch-up
- Quarterly: evidence refresh, training updates
- Annually: policy review and risk assessment

## Evidence Durability Guidelines

- Store evidence in a durable, auditable datastore.
- Version evidence with system version and release ID.
- Apply retention at least as long as the longest applicable regulatory requirement.
- Include integrity checks (hash chain or digital signature) where needed.

## Long Tail of Ongoing Obligation

Compliance does not stop at release. Onboarding, retraining, incident response, model updates, vendor changes, and policy revisions all require review and evidence.

## Assurance Cycle

1. Assess
2. Design controls
3. Implement controls
4. Collect evidence
5. Review and improve
6. Repeat

## Compliance Relationship to Related Domains

- Security: protects confidentiality, integrity, and availability
- Privacy: lawful, fair, and transparent processing
- Testing: evaluates whether outputs behave as intended
- Operations: monitors and responds to behavior and failure
- Documentation: records claims, controls, evidence, and decisions

## Checklist for Fundamental Readiness

- Ownership is assigned
- Data inventory is active
- Threat model is current
- Evaluation coverage is documented
- Access controls are enforced
- Logging is configured
- Release gates include compliance review
- Runbooks exist for incidents and changes
- Training is assigned and tracked
- Vendor register is current

## Regulatory Expectations Summary

| Priority | Control Area | Expectation |
|----------|--------------|-------------|
| P0 | Data protection | Minimize, record legal basis, manage consent |
| P0 | Audit and evidence | Immutable or tamper-evident logs with integrity checks |
| P0 | Access control | Least privilege, MFA, temporary elevation only |
| P1 | Model governance | Versioning, evaluation, human oversight for high-impact decisions |
| P1 | Incident response | Plan, contacts, runbooks, postmortems |
| P1 | Vendor management | DPA, subprocessor list, attestation refresh |
| P1 | Human review | Required and documented for decisions affecting rights |
| P2 | Monitoring | Continuous visibility into violations and anomalies |
| P2 | Documentation | System, model, prompt, tool registers and runbooks |
| P2 | Testing | Regression and red-team coverage |

## Compliance Artifacts to Maintain

- System register
- Model card and model risk file
- Prompt register
- Audit log schema and sample events
- Retention policy and legal-hold runbook
- Release evidence packet
- Incident response runbook
- Exception register

## Escalation Rules

- High-severity violations escalate immediately to compliance, CISO, and legal.
- Medium-severity violations escalate within one business day.
- Low-severity reviews are scheduled monthly.
- Events affecting EU data subjects also notify the DPO.

## Exception Queue Rules

- Each exception has an owner, expiration date, and compensating control.
- Exceptions go through review before approval.
- Expired exceptions require renewal or control implementation.

## Review Schedule

- Review after every material model, prompt, tool, or data change.
- Review after every audit or incident.
- Review quarterly for all other systems.

## Further Reading

- NIST AI Risk Management Framework
- GDPR recitals and guidance
- EU AI Act documentation
- ISO/IEC 23894 and ISO/IEC 38507
- OWASP Top 10 for large language models
- Vendor documentation and certifications

## Documents and Contracts

- Privacy policy
- Data processing agreement
- Data retention and legal hold policy
- Incident response plan
- Vendor management policy
- Access control policy
- Model risk and policy policies
- Change management policy

## Trust Models

- Red teaming to identify harmful or risky behaviors
- Harm categorization and severity scales
- Control catalog mapped to evidence
- Governance meeting cadences
- Evidence retention and access
- Incident response and breach notification

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)

## Compliance Maturity Model

1. No documented ownership or logging
2. Ownership documented; ad-hoc review
3. Evaluation and monitoring in place
4. Continuous compliance measurement
5. Adaptive policy and automated remediation

## System Examples

- Low risk: internal chatbot with logging and owner
- Medium risk: customer support assistant with evaluation and monitoring
- High risk: medical or financial advice tool with human review and formal risk assessment
- Prohibited: use banned by law, policy, or contract

## Key Takeaways

- Compliance is continuous, not a one-time check.
- Every AI system needs an owner, purpose, and review cadence.
- Data minimization, audit logging, and human oversight are foundational.
- Model and prompt changes require re-evaluation.
- Legal and contractual requirements vary by jurisdiction.
- Vendor data flows must be controlled.
- Incident response and runbooks are essential.

## Further Reading

- NIST AI Risk Management Framework
- GDPR recitals and guidance
- EU AI Act documentation
- ISO/IEC 23894 and ISO/IEC 38507
- OWASP Top 10 for large language models
- Vendor documentation and certifications