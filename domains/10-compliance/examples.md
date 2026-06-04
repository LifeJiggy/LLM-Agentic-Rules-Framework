# Compliance Domain - Examples

> Practical examples for documenting and enforcing compliance controls.

## Overview

These examples provide reusable starting points for compliance records, release reviews, approval rules, and trace redaction patterns. Adapt them to your organization's risk model and legal requirements.

---

## Table of Contents

1. [AI System Register Entry](#1-ai-system-register-entry)
2. [Release Review Template](#2-release-review-template)
3. [Tool Approval Rule](#3-tool-approval-rule)
4. [Trace Redaction Pattern](#4-trace-redaction-pattern)
5. [Consent Record Schema](#5-consent-record-schema)
6. [Incident Report Template](#6-incident-report-template)
7. [Audit Event Examples](#7-audit-event-examples)
8. [Data Processing Purpose Registry](#8-data-processing-purpose-registry)
9. [Model Risk File Example](#9-model-risk-file-example)
10. [Vendor Assessment Questionnaire](#10-vendor-assessment-questionnaire)
11. [DPA Record Example](#11-dpa-record-example)
12. [Jurisdiction Disclosure Snippets](#12-jurisdiction-disclosure-snippets)
13. [Release Evidence Packet](#13-release-evidence-packet)
14. [Retention Policy Config](#14-retention-policy-config)
15. [Legal Hold Record](#15-legal-hold-record)
16. [Appendix](#16-appendix)

---

## 1. AI System Register Entry

```yaml
system: support-response-assistant
owner: customer-platform
purpose: Draft customer support replies for human review
risk_tier: medium
users:
  - support agents
data_classes:
  - customer messages
  - order metadata
models:
  - provider: example-provider
    model: example-model
    version: pinned-release
tools:
  - read_order_status
  - search_help_center
human_oversight:
  required_before_customer_send: true
retention:
  prompts: 30 days
  completions: 30 days
  evaluation_records: 1 year
jurisdiction: US
review_cadence: quarterly
success_criteria:
  - human_review_rate >= 0.95
  - pii_leak_rate < 0.001
  - mean_time_to_human_review < 120 seconds
```

## 2. Release Review Template

```markdown
## AI Compliance Review

System:
Owner:
Risk tier:
Release:

### Changes
- Model:
- Prompts:
- Tools:
- Data sources:

### Evidence
- Evaluation report:
- Security review:
- Privacy review:
- Incident rollback plan:

### Decision
- [ ] Approved
- [ ] Approved with conditions
- [ ] Rejected
```

```json
{
  "release": {
    "system": "support-response-assistant",
    "version": "1.2.0",
    "timestamp": "2026-06-04T13:30:00Z",
    "changes": {
      "model": "example-provider/example-model@2026-06-04",
      "prompts": ["prompts/v4/order_lookup.md"],
      "tools": [],
      "data_sources": []
    },
    "evidence": {
      "evaluation": "https://...",
      "security": "https://...",
      "privacy": "https://...",
      "rollback_plan": "https://..."
    },
    "decision": "Approved with conditions",
    "approver": "compliance@example.com"
  }
}
```

## 3. Tool Approval Rule

```python
def requires_human_approval(tool_name: str, payload: dict) -> bool:
    high_impact_tools = {
        "send_customer_email",
        "issue_refund",
        "change_account_status",
        "submit_regulatory_filing",
    }

    if tool_name in high_impact_tools:
        return True

    if payload.get("contains_sensitive_data"):
        return True

    return False
```

## 4. Trace Redaction Pattern

```python
import re

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*\S+"),
]

def redact_trace(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
```

## 5. Consent Record Schema

```json
{
  "user_id": "user_123",
  "purpose": "assistant_training",
  "granted": true,
  "timestamp": "2026-06-04T13:30:00Z",
  "source": "settings_page",
  "version": "consent_manifest_v2",
  "expires_at": null
}
```

## 6. Incident Report Template

```markdown
## AI Compliance Incident Report

Incident Identifier:
Severity:
Time Detected:
System:
Owning Team:
Reporter:

### Timeline
- ...

### Impact
- Affected users:
- Data involved:
- Compliance frameworks impacted:

### Remediation Steps
1. ...
2. ...

### Verification
- [ ] Root cause identified
- [ ] Follow-up actions assigned

### Notification
- Regulators:
- Users:
- Internal stakeholders:
```

## 7. Audit Event Examples

```python
import uuid
from datetime import datetime
from typing import Optional

class AuditEventBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.event = {
            "event_id": str(uuid.uuid4()),
            "event_type": "tool_call",
            "timestamp": datetime.utcnow().isoformat(),
            "actor": None,
            "actor_type": None,
            "resource": None,
            "action": None,
            "outcome": None,
            "session_id": None,
            "request_id": None,
            "jurisdiction": None,
            "classification": None,
            "source_service": None,
            "target_service": None,
            "metadata": {},
        }

    def set_actor(self, actor: str, actor_type: str = "user"):
        self.event["actor"] = actor
        self.event["actor_type"] = actor_type
        return self

    def set_resource(self, resource: str):
        self.event["resource"] = resource
        return self

    def set_action(self, action: str):
        self.event["action"] = action
        return self

    def set_outcome(self, outcome: str):
        self.event["outcome"] = outcome
        return self

    def set_session(self, session_id: Optional[str]):
        self.event["session_id"] = session_id
        return self

    def set_request(self, request_id: Optional[str]):
        self.event["request_id"] = request_id
        return self

    def set_jurisdiction(self, jurisdiction: Optional[str]):
        self.event["jurisdiction"] = jurisdiction
        return self

    def set_classification(self, classification: str):
        self.event["classification"] = classification
        return self

    def set_services(self, source: str, target: str):
        self.event["source_service"] = source
        self.event["target_service"] = target
        return self

    def add_metadata(self, key: str, value):
        self.event["metadata"][key] = value
        return self

    def build(self) -> dict:
        event = self.event
        self.reset()
        return event
```

## 8. Data Processing Purpose Registry

```python
from typing import Dict, List, Optional
from datetime import datetime

class ProcessingPurposeRegistry:
    def __init__(self):
        self.purposes: Dict[str, dict] = {}
        self.user_consents: Dict[str, dict] = {}

    def register_purpose(
        self,
        purpose_id: str,
        description: str,
        legal_basis: str,
        data_categories: List[str],
        retention_days: int,
        owner: str,
    ):
        self.purposes[purpose_id] = {
            "description": description,
            "legal_basis": legal_basis,
            "data_categories": data_categories,
            "retention_days": retention_days,
            "owner": owner,
            "registered_at": datetime.utcnow().isoformat(),
        }

    def record_consent(self, user_id: str, purpose_id: str, granted: bool, source: str = "ui"):
        if purpose_id not in self.purposes:
            raise ValueError(f"Unknown purpose: {purpose_id}")
        self.user_consents[(user_id, purpose_id)] = {
            "granted": granted,
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }

    def can_process(self, user_id: str, purpose_id: str) -> bool:
        record = self.user_consents.get((user_id, purpose_id))
        if not record:
            return False
        return record["granted"]
```

## 9. Model Risk File Example

```python
from typing import List, Dict, Optional
from datetime import datetime

class ModelRiskFile:
    def __init__(self, system_name: str, owner: str):
        self.system_name = system_name
        self.owner = owner
        self.approved_use_cases: List[str] = []
        self.known_limitations: List[str] = []
        self.evaluation_coverage: List[dict] = []
        self.monitoring_plan: Optional[str] = None
        self.fallback_model: Optional[str] = None
        self.material_change_criteria: List[str] = []
        self.accepted_risks: List[dict] = []

    def add_approved_use_case(self, use_case: str):
        self.approved_use_cases.append(use_case)

    def add_limitation(self, limitation: str):
        self.known_limitations.append(limitation)

    def add_evaluation(self, name: str, passed: bool, evaluator: str):
        self.evaluation_coverage.append({
            "name": name,
            "passed": passed,
            "evaluator": evaluator,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def register_accepted_risk(self, name: str, rationale: str, review_date: str):
        self.accepted_risks.append({
            "name": name,
            "rationale": rationale,
            "owner": self.owner,
            "review_date": review_date,
            "status": "accepted",
            "registered_at": datetime.utcnow().isoformat(),
        })
```

## 10. Vendor Assessment Questionnaire

```markdown
## Vendor Security and Compliance Assessment

### Company Information
- Name:
- Contact:
- DPO or privacy contact:

### Certifications
- SOC 2 Type II:
- ISO 27001:
- Other:

### Data Processing
- Subprocessors:
- Data residency:
- Encryption in transit and at rest:

## Contractual
- DPA available:
- Data return/deletion terms:
- Incident notification SLA:
```

## 11. DPA Record Example

```json
{
  "vendor": "example-vendor",
  "dpa_url": "https://example.com/dpa",
  "signed_date": "2026-01-01",
  "expiration_date": "2028-01-01",
  "data_categories": ["personal_data"],
  "purpose": "model_hosting",
  "subprocessors": ["infra_provider_x"],
  "status": "active",
  "owner": "legal@example.com"
}
```

## 12. Jurisdiction Disclosure Snippets

```markdown
EU Disclosure:
This service uses automated assistance. You have the right to opt out of automated decision-making. To exercise your rights, contact privacy@example.com.

UK Disclosure:
Some outputs are generated by an AI assistant. You may request human review of decisions that affect you materially.

California Disclosure:
This service does not sell personal information. You may request disclosure and deletion of your personal information.
```

## 13. Release Evidence Packet

```python
from typing import List, Dict

class ReleaseEvidencePacket:
    def __init__(self, system_id: str, release_id: str):
        self.system_id = system_id
        self.release_id = release_id
        self.evidence: Dict[str, object] = {}

    def add(self, key: str, value):
        self.evidence[key] = value

    def render(self, fmt: str = "json") -> str:
        if fmt == "json":
            return json.dumps({
                "system_id": self.system_id,
                "release_id": self.release_id,
                "evidence": {k: str(v) for k, v in self.evidence.items()},
            }, indent=2)
        lines = [
            f"# Release Evidence: {self.release_id}",
            "",
        ]
        for key, value in self.evidence.items():
            lines.append(f"## {key}")
            lines.append(str(value))
            lines.append("")
        return "\n".join(lines)
```

## 14. Retention Policy Config

```python
from typing import Dict
from datetime import timedelta

RETENTION_POLICIES = {
    "prompts": timedelta(days=30),
    "completions": timedelta(days=30),
    "tool_traces": timedelta(days=30),
    "audit_events": timedelta(days=2555),
    "evaluation_records": timedelta(days=365),
}

class RetentionPolicyStore:
    def __init__(self, policies: Dict[str, timedelta]):
        self.policies = policies

    def ttl(self, data_class: str) -> timedelta:
        return self.policies.get(data_class, timedelta(days=30))
```

## 15. Legal Hold Record

```python
class LegalHoldManager:
    def __init__(self, evidence_store):
        self.evidence_store = evidence_store
        self.active_holds: Dict[str, dict] = {}

    def place_hold(self, user_id: str, case_id: str, legal_basis: str):
        self.active_holds[user_id] = {
            "case_id": case_id,
            "legal_basis": legal_basis,
            "active": True,
            "placed_at": datetime.utcnow().isoformat(),
        }
        self.evidence_store.record_legal_hold(user_id, self.active_holds[user_id])

    def release_hold(self, user_id: str):
        hold = self.active_holds.get(user_id)
        if not hold:
            return
        hold["active"] = False
        hold["released_at"] = datetime.utcnow().isoformat()
        self.evidence_store.record_legal_hold_release(user_id, hold)

    def is_on_hold(self, user_id: str) -> bool:
        hold = self.active_holds.get(user_id)
        return hold is not None and hold.get("active", False)
```

## 16. Appendix

## Additional Examples

### Data Subject Request Fulfillment

```python
class DataSubjectRequestHandler:
    def __init__(self, store):
        self.store = store

    def export(self, user_id: str) -> dict:
        return {
            "user_id": user_id,
            "prompts": self.store.get_prompts(user_id),
            "completions": self.store.get_completions(user_id),
            "tool_calls": self.store.get_tool_calls(user_id),
            "audit_events": self.store.get_audit_events(user_id),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def delete(self, user_id: str):
        self.store.delete_user_data(user_id)
        self.store.append_audit_event({"action": "dsr_deletion", "user_id": user_id})
```

### Legal Hold Implementation

```python
class LegalHoldEnforcer:
    def __init__(self, store):
        self.store = store
        self.holds = {}

    def place_hold(self, user_id: str, case_id: str):
        self.holds[user_id] = {"case_id": case_id, "active": True}

    def can_delete(self, user_id: str) -> bool:
        return not self.holds.get(user_id, {}).get("active", False)
```

### Audit Event Normalizer

```python
class AuditNormalizer:
    REQUIRED_FIELDS = ["event_id", "timestamp", "actor", "action", "outcome"]

    def normalize(self, event: dict) -> dict:
        normalized = {k: event.get(k) for k in self.REQUIRED_FIELDS}
        normalized["metadata"] = event.get("metadata", {})
        return normalized
```

### Model Risk File Generator

```python
class ModelRiskFileGenerator:
    def generate(self, model_profile: dict) -> dict:
        return {
            "model_name": model_profile["model_name"],
            "owner": model_profile["owner"],
            "approved_use_cases": model_profile.get("use_cases", []),
            "known_limitations": model_profile.get("limitations", []),
            "fallback_strategy": model_profile.get("fallback"),
            "monitoring_plan": model_profile.get("monitoring_plan"),
            "created_at": datetime.utcnow().isoformat(),
        }
```

### Vendor Register Entry

```json
{
  "vendor_name": "example-vendor",
  "services": ["model_hosting"],
  "dpa_signed": true,
  "dpa_url": "https://example.com/dpa",
  "subprocessors": ["example-subprocessor"],
  "data_categories": ["personal_data"],
  "retention_days": 30,
  "encryption_in_transit": "TLS 1.3",
  "encryption_at_rest": true,
  "certifications": ["SOC 2", "ISO 27001"],
  "owner": "legal@example.com",
  "review_due": "2027-01-01"
}
```

### Exception Record Schema

```json
{
  "exception_id": "exception_001",
  "control": "retention_policy",
  "justification": "Artificial extension for litigation support.",
  "owner": "legal@example.com",
  "review_date": "2027-06-04",
  "status": "active",
  "created_at": "2026-06-04T13:30:00Z"
}
```

### Compliance Metric Example

```python
COMPLIANCE_METRICS = {
    "retention_compliance_rate": {
        "target": 1.0,
        "unit": "ratio",
        "owner": "platform",
    },
    "evaluation_pass_rate": {
        "target": 0.99,
        "unit": "ratio",
        "owner": "ml-platform",
    },
    "review_latency_p95": {
        "target": 300,
        "unit": "seconds",
        "owner": "trust_and_safety",
    },
}
```

### Permission Matrix

```python
class ToolPermissionMatrix:
    def __init__(self):
        self.matrix = {
            "search_help_center": ["support", "admin"],
            "issue_refund": ["admin"],
            "send_email": ["support", "admin"],
        }

    def allowed_for(self, tool: str, role: str) -> bool:
        return role in self.matrix.get(tool, [])

    def allowed_roles(self, tool: str) -> list:
        return self.matrix.get(tool, [])
```

### Consent Verification

```python
class ConsentVerifier:
    def __init__(self, registry):
        self.registry = registry

    def verify(self, user_id: str, purpose: str) -> bool:
        return self.registry.can_process(user_id, purpose)
```

### Packaging Release Evidence

```python
def package_release_evidence(system_id, release_id) -> dict:
    return {
        "system_id": system_id,
        "release_id": release_id,
        "date": datetime.utcnow().isoformat(),
        "evaluation_link": "https://example.com/evaluations/{system_id}/{release_id}".format(system_id=system_id, release_id=release_id),
        "security_review_link": "https://example.com/security/{system_id}/{release_id}".format(system_id=system_id, release_id=release_id),
        "privacy_review_link": "https://example.com/privacy/{system_id}/{release_id}".format(system_id=system_id, release_id=release_id),
        "rollback_plan_link": "https://example.com/runbooks/{system_id}".format(system_id=system_id),
        "status": "ready_for_review",
    }
```

### Release Evidence Packet

```python
from typing import List, Dict

class ReleaseEvidencePacket:
    def __init__(self, system_id: str, release_id: str):
        self.system_id = system_id
        self.release_id = release_id
        self.evidence: Dict[str, object] = {}

    def add(self, key: str, value):
        self.evidence[key] = value

    def render(self, fmt: str = "json") -> str:
        if fmt == "json":
            return json.dumps({
                "system_id": self.system_id,
                "release_id": self.release_id,
                "evidence": {k: str(v) for k, v in self.evidence.items()},
            }, indent=2)
        lines = [
            f"# Release Evidence: {self.release_id}",
            "",
        ]
        for key, value in self.evidence.items():
            lines.append(f"## {key}")
            lines.append(str(value))
            lines.append("")
        return "\n".join(lines)
```

### Retention Policy Config

```python
from typing import Dict
from datetime import timedelta

RETENTION_POLICIES = {
    "prompts": timedelta(days=30),
    "completions": timedelta(days=30),
    "tool_traces": timedelta(days=30),
    "audit_events": timedelta(days=2555),
    "evaluation_records": timedelta(days=365),
}

class RetentionPolicyStore:
    def __init__(self, policies: Dict[str, timedelta]):
        self.policies = policies

    def ttl(self, data_class: str) -> timedelta:
        return self.policies.get(data_class, timedelta(days=30))
```

### Legal Hold Record

```python
class LegalHoldManager:
    def __init__(self, evidence_store):
        self.evidence_store = evidence_store
        self.active_holds: Dict[str, dict] = {}

    def place_hold(self, user_id: str, case_id: str, legal_basis: str):
        self.active_holds[user_id] = {
            "case_id": case_id,
            "legal_basis": legal_basis,
            "active": True,
            "placed_at": datetime.utcnow().isoformat(),
        }
        self.evidence_store.record_legal_hold(user_id, self.active_holds[user_id])

    def release_hold(self, user_id: str):
        hold = self.active_holds.get(user_id)
        if not hold:
            return
        hold["active"] = False
        hold["released_at"] = datetime.utcnow().isoformat()
        self.evidence_store.record_legal_hold_release(user_id, hold)

    def is_on_hold(self, user_id: str) -> bool:
        hold = self.active_holds.get(user_id)
        return hold is not None and hold.get("active", False)
```

### Exception Record Handle

```python
class ComplianceException:
    def __init__(self, exception_id, control, owner, review_date, justification):
        self.exception_id = exception_id
        self.control = control
        self.owner = owner
        self.review_date = review_date
        self.justification = justification
        self.status = "active"

    def is_expired(self):
        return datetime.utcnow().date() > datetime.fromisoformat(self.review_date).date()

    def renew(self, new_review_date):
        self.review_date = new_review_date
        self.status = "renewed"
```

### Activity Summary Example

```python
class UserActivitySummary:
    def __init__(self, audit_store):
        self.audit_store = audit_store

    def summarize(self, user_id: str, days: int = 30) -> dict:
        cutoff = datetime.utcnow() - timedelta(days=days)
        events = self.audit_store.query_events({
            "actor": user_id,
            "timestamp": {"$gte": cutoff.isoformat()},
        })
        return {
            "user_id": user_id,
            "event_count": len(events),
            "first_event": events[0]["timestamp"] if events else None,
            "last_event": events[-1]["timestamp"] if events else None,
            "actions": [e["action"] for e in events],
        }
```

### Compliance Heatmap Example

```python
COMPLIANCE_HEATMAP = {
    "data_minimization": {"status": "green", "last_review": "2026-03-04"},
    "prompt_injection": {"status": "yellow", "last_review": "2026-01-04"},
    "vendor_due_diligence": {"status": "red", "last_review": "2025-09-04"},
    "retention": {"status": "green", "last_review": "2026-04-04"},
    "review_coverage": {"status": "yellow", "last_review": "2025-12-04"},
}
```

## Additional Usage

```markdown
## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
```

## Runbook Template

```markdown
System:
Owner:
Risk Tier:

## Incident: 
Timeline:
- 
Impact:
- Affected users:
- Data involved:

## Remediation Steps
1. 
2. 
3. 

## Verification
- [ ] Root cause identified
- [ ] Follow-up actions assigned

## Notification
- Regulators:
- Users:
- Internal stakeholders:
```

## Sample Audit Event

```json
{
  "event_id": "abc123",
  "event_type": "tool_call",
  "timestamp": "2026-06-04T13:30:00Z",
  "actor": "admin_1",
  "actor_type": "user",
  "resource": "tool/order/update",
  "action": "call",
  "outcome": "success",
  "session_id": "session_456",
  "request_id": "req_789",
  "jurisdiction": "US",
  "classification": "internal",
  "source_service": "gateway",
  "target_service": "order-service",
  "metadata": {"tool": "order/update"}
}
```

## Compliance Heatmap Example

```python
COMPLIANCE_HEATMAP = {
    "data_minimization": {"status": "green", "last_review": "2026-03-04"},
    "prompt_injection": {"status": "yellow", "last_review": "2026-01-04"},
    "vendor_due_diligence": {"status": "red", "last_review": "2025-09-04"},
    "retention": {"status": "green", "last_review": "2026-04-04"},
    "review_coverage": {"status": "yellow", "last_review": "2025-12-04"},
}
```

## Additional Example Patterns

- Add example event payloads
- Add example policy rules
- Add example runbook snippets

## Usage Guidance

Use the above examples as templates; adapt them to your registry, release workflow, and policy definitions.