# Compliance Domain - Advanced

> Advanced compliance patterns for complex, high-impact, or multi-jurisdiction LLM and agentic systems.

## Overview

Advanced compliance work focuses on mapping controls to evidence, managing model risk, supporting jurisdiction-specific requirements, governing autonomous tool use, and maintaining continuous assurance over time.

## Table of Contents

1. [Control Mapping](#1-control-mapping)
2. [Model Risk Management](#2-model-risk-management)
3. [Jurisdiction-Aware Deployment](#3-jurisdiction-aware-deployment)
4. [Agentic Action Governance](#4-agentic-action-governance)
5. [Continuous Compliance](#5-continuous-compliance)
6. [Advanced Encryption](#6-advanced-encryption)
7. [Token Budgeting](#7-token-budgeting)
8. [Audit Architecture](#8-audit-architecture)
9. [Privacy-Enhancing Technologies](#9-privacy-enhancing-technologies)
10. [Compliance Testing Frameworks](#10-compliance-testing-frameworks)
11. [Metrics and Validation](#11-metrics-and-validation)
12. [Code Review Workflows](#12-code-review-workflows)
13. [Debugging and Observability](#13-debugging-and-observability)
14. [Dependency and Change Management](#14-dependency-and-change-management)
15. [Appendix](#15-appendix)

---

## 1. Control Mapping

Map each AI control to the policies, contracts, and regulations it supports. This avoids duplicating work across audits.

| Control | Evidence | Example Requirement |
|---------|----------|---------------------|
| Data minimization | Data inventory, prompt redaction tests | Privacy and confidentiality |
| Human oversight | Approval logs, reviewer workflow | High-impact decision governance |
| Model evaluation | Regression reports, red-team results | Safety and quality assurance |
| Access control | IAM policy, permission review | Least privilege |
| Incident response | Runbook, post-incident report | Operational resilience |
| Consent management | Consent receipts, purpose registry | Lawful basis for processing |
| Retention enforcement | Automated purge jobs, legal hold records | Records management policy |
| Vendor governance | DPA inventory, subprocessor register | Third-party risk and privacy law |

## Control Mapping Workflow

```python
class ControlMapper:
    def __init__(self, registry):
        self.registry = registry
        self.mappings = {}

    def map_control(self, control_id, regulation, requirement, evidence_fn):
        self.mappings[control_id] = {
            "control_id": control_id,
            "regulation": regulation,
            "requirement": requirement,
            "evidence_fn": evidence_fn,
            "last_verified": None,
            "next_review": None,
        }

    def verify(self, control_id):
        mapping = self.mappings[control_id]
        evidence = mapping["evidence_fn"]()
        mapping["last_verified"] = datetime.utcnow().isoformat()
        return evidence
```

## Evidence Packaging

```python
class EvidencePackage:
    def __init__(self, framework, controls, optics):
        self.framework = framework
        self.controls = controls
        self.optics = optics

    def render(self, fmt="markdown"):
        if fmt == "json":
            return json.dumps(self._to_json(), indent=2)
        return self._to_markdown()
```

## Audit Readiness Checklist

```python
class AuditReadinessChecker:
    def __init__(self):
        self.checks = [
            "ownership_documented",
            "evidence_linked",
            "controls_current",
            "runbook_tested",
            "vendor_register_current",
        ]

    def score(self):
        passed = sum(1 for c in self.checks if self._check(c))
        return passed / len(self.checks)
```

---

## 2. Model Risk Management

For high-impact systems, maintain a model risk file.

- Approved use cases.
- Known limitations.
- Evaluation scope and gaps.
- Monitoring plan.
- Fallback or rollback plan.
- Material-change criteria.
- Residual risks and accepted exceptions.

## Model Risk File

```python
class ModelRiskFile:
    def __init__(self, model_name, owner):
        self.model_name = model_name
        self.owner = owner
        self.use_cases = []
        self.limitations = []
        self.evaluation_scope = []
        self.monitoring_plan = None
        self.fallback = None
        self.material_change_criteria = []
        self.residual_risks = []

    def add_use_case(self, use_case):
        self.use_cases.append(use_case)

    def add_limitation(self, limitation):
        self.limitations.append(limitation)
```

## Change Gate Process

```python
class ModelChangeGate:
    def __init__(self):
        self.pending = []
        self.approved = []

    def submit(self, change):
        change["status"] = "pending"
        change["submitted_at"] = datetime.utcnow().isoformat()
        self.pending.append(change)
        return change["id"]

    def approve(self, change_id, approver, rationale):
        change = next(c for c in self.pending if c["id"] == change_id)
        change["status"] = "approved"
        change["approver"] = approver
        change["rationale"] = rationale
        change["approved_at"] = datetime.utcnow().isoformat()
        self.pending.remove(change)
        self.approved.append(change)
        return change
```

## Material Change Definition

```python
MATERIAL_CHANGE_CRITERIA = {
    "model_version_change": True,
    "prompt_template_change": True,
    "retrieval_source_change": True,
    "tool_permission_change": True,
    "fine_tuning_run": True,
    "rag_index_rebuild": True,
    "fallback_model_change": True,
    "logging_or_monitoring_disabled": True,
}
```

---

## 3. Jurisdiction-Aware Deployment

Different regions can require different data handling, disclosure, retention, and review controls.

Recommended pattern:

1. Classify users and data by jurisdiction.
2. Keep policy decisions outside prompts where possible.
3. Use configuration-driven controls for retention, routing, and disclosure text.
4. Test jurisdiction-specific behavior in CI or release evaluation.

## Jurisdiction Registry

```python
class JurisdictionRegistry:
    def __init__(self):
        self.rules = {
            "EU": {"law": "GDPR", "retention_days": 365, "disclosure": "eu_disclosure.txt"},
            "UK": {"law": "UK_GDPR", "retention_days": 365, "disclosure": "uk_disclosure.txt"},
            "CA": {"law": "CCPA", "retention_days": 365, "disclosure": "ca_disclosure.txt"},
            "US": {"law": "state_specific", "retention_days": 365, "disclosure": "us_disclosure.txt"},
        }

    def get_rules(self, jurisdiction_code):
        return self.rules.get(jurisdiction_code, self.rules["US"])
```

## Region-Aware Data Router

```python
class RegionAwareRouter:
    def __init__(self, registry):
        self.registry = registry

    def route(self, user_context):
        jurisdiction = user_context.get("jurisdiction")
        rules = self.registry.get_rules(jurisdiction)
        return {
            "storage_region": rules["storage_region"],
            "disclosure": open(rules["disclosure"]).read(),
            "retention_days": rules["retention_days"],
        }
```

## Disclosure and Consent Enforcement

```python
class ConsentEnforcer:
    def __init__(self):
        self.consent_records = {}

    def ensure_consent(self, user_id, purpose):
        rec = self.consent_records.get(user_id, {})
        if rec.get(purpose) is not True:
            raise ConsentRequired(f"User {user_id} missing consent for {purpose}")
        return rec[purpose]
```

## Multi-Jurisdiction Testing

```python
def test_jurisdiction_templates():
    cases = [
        ("EU", "eu_disclosure.txt"),
        ("UK", "uk_disclosure.txt"),
        ("CA", "ca_disclosure.txt"),
    ]
    for jurisdiction, file in cases:
        disclosure = open(file).read()
        assert jurisdiction in disclosure or "your region" in disclosure
```

---

## 4. Agentic Action Governance

Autonomous systems need stronger controls because they can chain decisions and external actions.

- Separate read tools from write tools.
- Require scoped credentials per tool.
- Add policy checks before each tool call.
- Log the reason, input, output, and actor for high-impact actions.
- Require human approval for irreversible actions.

## Permissioned Tool Registry

```python
class PermissionedToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, policy, credential_scope):
        self.tools[name] = {
            "name": name,
            "policy": policy,
            "credential_scope": credential_scope,
        }

    def can_call(self, actor, tool_name, payload):
        tool = self.tools[tool_name]
        return tool["policy"](actor, payload)
```

## Action Gate

```python
class ActionGate:
    def __init__(self, policy_engine, auditor):
        self.policy_engine = policy_engine
        self.auditor = auditor

    def evaluate(self, actor, tool_name, payload):
        allowed = self.policy_engine.evaluate(actor, tool_name, payload)
        self.auditor.log_tool_call(actor, tool_name, payload, allowed)
        if not allowed:
            raise ActionDenied(f"Policy denied {tool_name}")
```

## Human Approval Gate

```python
class HumanApprovalGate:
    def __init__(self):
        self.requires_approval = {
            "send_email": True,
            "update_account": True,
            "close_ticket": False,
        }

    def needs_human_approval(self, tool_name):
        return self.requires_approval.get(tool_name, False)

    def record_approval(self, action_id, approver):
        return {"action_id": action_id, "approver": approver, "ts": datetime.utcnow().isoformat()}
```

## Tool Call Trace Schema

```python
TOOL_CALL_TRACE_SCHEMA = {
    "trace_id": str,
    "actor": str,
    "tool_name": str,
    "payload": dict,
    "decision": str,
    "approver": str,
    "input_refs": list,
    "output_refs": list,
    "timestamp": str,
}
```

---

## 5. Continuous Compliance

Compliance should be monitored after release.

- Track policy-violation rates.
- Sample production outputs.
- Review user complaints and appeals.
- Re-run evaluations on model, prompt, retrieval, and tool changes.
- Retire systems that no longer have a valid owner or business purpose.

## Compliance Telemetry

```python
class ComplianceTelemetry:
    def __init__(self, metrics_backend):
        self.metrics = metrics_backend

    def record_violation(self, control, severity, context):
        self.metrics.increment("compliance.violation", tags={
            "control": control,
            "severity": severity,
        })

    def record_policy_check(self, policy, result):
        self.metrics.increment("compliance.policy_check", tags={
            "policy": policy,
            "result": result,
        })
```

## Production Sampling Job

```python
class ProductionSampler:
    def __init__(self, store, sampler):
        self.store = store
        self.sampler = sampler

    def sample(self, limit=200):
        candidates = self.store.recent_traces(limit)
        return self.sampler.filter(candidates)
```

## Model Change Trigger

```python
class ModelChangeTrigger:
    def __init__(self, evaluator, deployer):
        self.evaluator = evaluator
        self.deployer = deployer

    def on_model_change(self, model_version):
        required = self.evaluator.required_suite(model_version)
        if not required["passed"]:
            self.deployer.block_release(model_version, required["reason"])
```

## Retirement Policy

```python
RETIREMENT_CRITERIA = {
    "owner_missing_days": 90,
    "last_review_days": 180,
    "violation_rate_threshold": 0.05,
}
```

---

## 6. Advanced Encryption

Use defense-in-depth for sensitive prompts, retrieved context, and tool payloads.

## Encryption-at-Rest Patterns

```python
class EncryptionAtRest:
    def __init__(self, key_provider):
        self.key_provider = key_provider

    def encrypt(self, plaintext):
        key = self.key_provider.current_key()
        iv = os.urandom(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.b64encode(iv + tag + ciphertext).decode()

    def decrypt(self, payload):
        raw = base64.b64decode(payload.encode())
        iv, tag, ciphertext = raw[:12], raw[12:28], raw[28:]
        cipher = AES.new(self.key_provider.current_key(), AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
```

## Key Rotation Policy

```python
class KeyRotationPolicy:
    def __init__(self, key_store):
        self.key_store = key_store
        self.rotation_interval_days = 90

    def rotate_if_due(self):
        current = self.key_store.active_key()
        created = datetime.fromisoformat(current["created_at"])
        if datetime.utcnow() - created > timedelta(days=self.rotation_interval_days):
            new_key = self._generate_key()
            self.key_store.activate(new_key)
            self.key_store.archive(current)
```

## Secret Handling

```python
class SecretManager:
    def __init__(self, backend):
        self.backend = backend

    def get(self, name):
        return self.backend.fetch_secret(name)

    def inject(self, env):
        for name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
            env[name] = self.get(name)
```

---

## 7. Token Budgeting

Control cost, leakage risk, and output stability with token budgets and routing rules.

```python
class TokenBudget:
    def __init__(self, limits):
        self.limits = limits

    def remaining(self, user_tier, context):
        used = context.get("tokens_used", 0)
        limit = self.limits[user_tier]
        return max(0, limit - used)

    def enforce(self, user_tier, incoming_tokens):
        if incoming_tokens > self.limits[user_tier]:
            raise TokenBudgetExceeded()
```

## Request Routing

```python
class RequestRouter:
    def __init__(self, models, fallback):
        self.models = models
        self.fallback = fallback

    def route(self, request):
        if request.tokens > self.models["small"]["max_tokens"]:
            return self.models["large"]
        if self.models["small"]["available"]:
            return self.models["small"]
        return self.fallback
```

## Telemetry and Alerts

```python
class UsageTelemetry:
    def __init__(self):
        self.errors = defaultdict(int)

    def record_fallback(self, reason):
        self.errors[reason] += 1

    def should_page(self):
        return any(v > 100 for v in self.errors.values())
```

## Error-Tolerant Recovery

```python
class RetryPolicy:
    def __init__(self, max_retries=2, backoff=1):
        self.max_retries = max_retries
        self.backoff = backoff

    def execute(self, fn, *args, **kwargs):
        last = None
        for attempt in range(self.max_retries):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last = e
                time.sleep(self.backoff ** attempt)
        raise last
```

---

## 8. Audit Architecture

## Distributed Audit Event Schema

```python
AUDIT_EVENT_SCHEMA = {
    "event_id": str,
    "event_type": str,
    "timestamp": str,
    "actor": str,
    "actor_type": str,
    "resource": str,
    "action": str,
    "outcome": str,
    "session_id": str,
    "request_id": str,
    "jurisdiction": str,
    "classification": str,
    "source_service": str,
    "target_service": str,
    "metadata": dict,
}
```

## Audit Bus

```python
class AuditBus:
    def __init__(self):
        self.handlers = []

    def publish(self, event):
        for handler in self.handlers:
            handler(event)

    def subscribe(self, handler):
        self.handlers.append(handler)
```

## Log Integrity Service

```python
class LogIntegrityService:
    def __init__(self, store):
        self.store = store

    def verify(self, start, end):
        events = self.store.query(start, end)
        for i in range(1, len(events)):
            prev = events[i - 1]
            curr = events[i]
            if curr.get("previous_hash") != prev["hash"]:
                return False
        return True
```

## Logging Library

```python
class AuditLogger:
    def __init__(self, audit_bus):
        self.bus = audit_bus

    def log(self, event_type, actor, resource, action, outcome, metadata=None):
        event = {
            "event_id": uuid.uuid4().hex,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "actor": actor,
            "resource": resource,
            "action": action,
            "outcome": outcome,
            "metadata": metadata or {},
        }
        self.bus.publish(event)
```

## Storage and Retention

```python
class AuditStore:
    def __init__(self, db):
        self.db = db

    def append(self, event):
        self.db.insert("audit_events", event)

    def query(self, start, end, filters=None):
        return self.db.query("audit_events", {
            "timestamp": {"$gte": start, "$lte": end},
            **(filters or {}),
        })
```

## Search and Indexing

```python
class AuditIndex:
    def __init__(self, store):
        self.store = store

    def search(self, query):
        return self.store.query("audit_events", {"$text": {"$search": query}})
```

## Privacy Filters

```python
class AuditPrivacyFilter:
    SENSITIVE = [
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"(?i)(password|api_key|token)\s*[:=]\s*\S+"),
    ]

    def filter_event(self, event):
        event = copy.deepcopy(event)
        for key in ["input", "output", "metadata"]:
            if isinstance(event.get(key), str):
                event[key] = self.redact(event[key])
        return event

    def redact(self, text):
        for pattern in self.SENSITIVE:
            text = pattern.sub("[REDACTED]", text)
        return text
```

## Export and Reporting

```python
class AuditExporter:
    def __init__(self, store, privacy_filter):
        self.store = store
        self.privacy_filter = privacy_filter

    def export_csv(self, start, end):
        events = self.store.query(start, end)
        rows = []
        for event in events:
            event = self.privacy_filter.filter_event(event)
            rows.append([event.get(k, "") for k in AUDIT_EVENT_SCHEMA])
        return "\n".join([",".join(row) for row in rows])
```

---

## 9. Privacy-Enhancing Technologies

Techniques that reduce exposure while preserving utility.

```python
class DifferentialPrivacy:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def apply(self, counts):
        noise = np.random.laplace(0, 1 / self.epsilon, size=len(counts))
        return np.maximum(0, np.array(counts) + noise).tolist()
```

## Synthetic Data Generation

```python
class SyntheticDataGenerator:
    def __init__(self, base_dataset):
        self.base = base_dataset

    def generate(self, n=1000):
        samples = []
        for _ in range(n):
            row = self._sample_row(self.base)
            samples.append(row)
        return samples
```

## Data Masking

```python
class DataMasking:
    def __init__(self):
        self.strategies = {
            "email": lambda x: re.sub(r".+@", "***@", x),
            "phone": lambda x: re.sub(r"\d", "*", x[-4:]).join([x[:-4], "****"]),
            "ssn": lambda x: "***-**-****",
        }

    def mask(self, record):
        masked = dict(record)
        for field, fn in self.strategies.items():
            if field in masked:
                masked[field] = fn(masked[field])
        return masked
```

## Federated Learning Patterns

```python
class FederatedClient:
    def __init__(self, client_id, local_data):
        self.client_id = client_id
        self.local_data = local_data

    def compute_update(self, global_model):
        local_grad = self._train_local(global_model)
        return {
            "client_id": self.client_id,
            "gradient": local_grad,
            "samples": len(self.local_data),
        }
```

---

## 10. Compliance Testing Frameworks

## Regression Evaluation Harness

```python
class ComplianceRegressionHarness:
    def __init__(self, baseline, suite):
        self.baseline = baseline
        self.suite = suite

    def run(self, candidate):
        candidate_results = self.suite.run(candidate)
        baseline_results = self.suite.run(self.baseline)
        return self._compare(candidate_results, baseline_results)
```

## Red-Teaming Templates

```python
class RedTeamTemplateRegistry:
    def __init__(self):
        self.templates = [
            "medical_advice_edge_cases",
            "legal_advice_edge_cases",
            "financial_advice_edge_cases",
            "pii_extraction_attacks",
            "prompt_injection_suite",
            "jailbreak_candidates",
        ]

    def all(self):
        return self.templates
```

## A/B Compliance Gates

```python
class ComplianceABGate:
    def __init__(self, metrics):
        self.metrics = metrics

    def gate(self, variant_a, variant_b):
        for metric in self.metrics:
            a = self._measure(variant_a, metric)
            b = self._measure(variant_b, metric)
            if not self._within_tolerance(a, b):
                return False, metric
        return True, None
```

---

## 11. Metrics and Validation

## Compliance Metrics Model

```python
class ComplianceMetricsModel:
    def __init__(self):
        self.gates = []

    def add_gate(self, name, evaluator, threshold):
        self.gates.append({
            "name": name,
            "evaluator": evaluator,
            "threshold": threshold,
        })

    def evaluate(self, candidate):
        results = {}
        for gate in self.gates:
            value = gate["evaluator"](candidate)
            results[gate["name"]] = {
                "value": value,
                "threshold": gate["threshold"],
                "passed": value >= gate["threshold"],
            }
        return results
```

## Release Readiness Criteria

```python
RELEASE_READINESS_CRITERIA = [
    ("safety_score", ">=", 0.95),
    ("fairness_delta", "<=", 0.02),
    ("pii_leakage_rate", "<=", 0.001),
    ("tool_policy_violation_rate", "<=", 0.0),
    ("human_review_coverage", ">=", 0.99),
]
```

## Bias and Fairness Metrics

```python
class BiasFairnessMetrics:
    def __init__(self):
        self.metrics = {}

    def assess(self, predictions, labels, groups):
        self.metrics["demographic_parity"] = self._demographic_parity(predictions, groups)
        self.metrics["equalized_odds"] = self._equalized_odds(predictions, labels, groups)
        return self.metrics
```

---

## 12. Code Review Workflows

## PR Compliance Checklist

```markdown
- [ ] Owner approved
- [ ] Risk tier remains valid
- [ ] Tools added/removed reviewed
- [ ] Route configuration reviewed
- [ ] Data handling reviewed
- [ ] Logging reviewed
- [ ] Fallback or rollout plan included
- [ ] Release record updated
```

## Automated PR Hooks

```python
class CompliancePRHook:
    def __init__(self, checks):
        self.checks = checks

    def run(self, pr):
        results = []
        for check in self.checks:
            results.append({
                "check": check.name,
                "passed": check.run(pr),
            })
        return results
```

## Review Assignment

```python
class ReviewAssignment:
    def __init__(self):
        self.routing = {
            "security": ["security-reviewer"],
            "privacy": ["dpo", "legal"],
            "model": ["ml-owner", "platform-lead"],
        }

    def assign(self, pr):
        reviewers = set()
        for label, pool in self.routing.items():
            if label in pr.labels:
                reviewers.update(pool)
        return list(reviewers)
```

---

## 13. Debugging and Observability

## Trace Inspection Pattern

```python
class TraceInspector:
    def __init__(self, trace_store):
        self.trace_store = trace_store

    def inspect(self, trace_id):
        trace = self.trace_store.get(trace_id)
        redacted = AuditPrivacyFilter().filter_event(trace)
        return redacted
```

## Policy Violation Debugger

```python
class PolicyViolationDebugger:
    def __init__(self, policy_store):
        self.policy_store = policy_store

    def explain(self, actor, tool, payload):
        matching = self.policy_store.matching(actor, tool)
        return {
            "matching_rules": matching,
            "denials": [m for m in matching if not m["allow"]],
        }
```

## Latency and Budget Debugging

```python
class LatencyDebugger:
    def __init__(self):
        self.samples = []

    def record(self, span):
        self.samples.append({
            "span": span.name,
            "duration_ms": span.duration_ms,
        })

    def slow_spans(self, threshold_ms=200):
        return [s for s in self.samples if s["duration_ms"] >= threshold_ms]
```

## Drift Alerts

```python
class DriftAlerter:
    def __init__(self, thresholds):
        self.thresholds = thresholds

    def check(self, metric, value):
        threshold = self.thresholds.get(metric)
        if threshold and value > threshold:
            return {"metric": metric, "value": value, "threshold": threshold}
        return None
```

## Failure Modes

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Key unavailable | health check | key rotation + cached backup |
| Policy store stale | checksum mismatch | reload and re-evaluate |
| Trace overflow | queue depth alarm | sampling and tiering |
| Audit bus lag | consumer lag monitor | provision additional consumers |
|

---

## 14. Dependency and Change Management

## Dependency Inventory

```python
class DependencyInventory:
    def __init__(self):
        self.inventory = {}

    def register(self, name, version, source, risk):
        self.inventory[name] = {
            "version": version,
            "source": source,
            "risk": risk,
            "added_at": datetime.utcnow().isoformat(),
        }
```

## Change Approval Workflow

```python
class ChangeApprovalWorkflow:
    def __init__(self):
        self.pending = []
        self.approved = []
        self.rejected = []

    def submit(self, change: dict, requester: str):
        change["status"] = "pending"
        change["requester"] = requester
        change["submitted_at"] = datetime.utcnow().isoformat()
        self.pending.append(change)
        return change["id"]

    def approve(self, change_id: str, approver: str):
        change = self._find(change_id)
        change["status"] = "approved"
        change["approved_by"] = approver
        change["approved_at"] = datetime.utcnow().isoformat()
        self.pending.remove(change)
        self.approved.append(change)

    def reject(self, change_id: str, reason: str):
        change = self._find(change_id)
        change["status"] = "rejected"
        change["rejection_reason"] = reason
        self.pending.remove(change)
        self.rejected.append(change)

    def _find(self, change_id):
        for c in self.pending:
            if c["id"] == change_id:
                return c
        raise KeyError(change_id)
```

## Model Version Registry

```python
class ModelVersionRegistry:
    def __init__(self):
        self.versions = {}

    def register(self, name: str, version: str, metadata: dict):
        self.versions[f"{name}:{version}"] = {
            "name": name,
            "version": version,
            "metadata": metadata,
            "registered_at": datetime.utcnow().isoformat(),
        }

    def get(self, name: str, version: str = None) -> dict:
        if version:
            return self.versions.get(f"{name}:{version}")
        candidates = [
            v for k, v in self.versions.items() if k.startswith(f"{name}:")
        ]
        return max(candidates, key=lambda x: x["version"]) if candidates else None
```

## Rollback Runbook

```python
class RollbackRunbook:
    def __init__(self, deployer, evaluator):
        self.deployer = deployer
        self.evaluator = evaluator

    def rollback(self, model_name, target_version):
        self.deployer.set_active(model_name, target_version)
        result = self.evaluator.evaluate_safety(model_name, target_version)
        if not result["passed"]:
            raise RollbackVerificationError(result)
        return {"status": "rolled_back", "model": model_name, "version": target_version}
```

## Impact Analysis

```python
class ImpactAnalysis:
    def __init__(self, evaluator, policy):
        self.evaluator = evaluator
        self.policy = policy

    def analyze(self, candidate):
        eval_results = self.evaluator.run(candidate)
        policy_results = []
        for rule in self.policy.rules():
            policy_results.append({
                "rule": rule.name,
                "result": rule.apply(candidate),
            })
        return {"evaluations": eval_results, "policy": policy_results}
```

## Configuration State Management

```python
class ConfigStateManager:
    def __init__(self, backend):
        self.backend = backend

    def snapshot(self):
        return self.backend.current_state()

    def revert(self, snapshot_id):
        self.backend.restore(snapshot_id)
```

## Change Communication Plan

```python
class ChangeCommunicationPlan:
    def __init__(self):
        self.plan = {
            "notification_recipients": ["platform-team", "security", "support"],
            "channels": ["email", "slack", "status-page"],
            "rollout_schedule": "2026-06-04T00:00:00Z",
        }

    def notify(self, change):
        for recipient in self.plan["notification_recipients"]:
            send(recipient, change)
```

## Backup Policy

```python
class BackupPolicy:
    def __init__(self, backup_store):
        self.backup_store = backup_store
        self.retention_days = 90

    def backup(self, source):
        snapshot = self._snapshot(source)
        self.backup_store.save(snapshot)

    def restore(self, snapshot_id):
        return self.backup_store.load(snapshot_id)

    def expire(self):
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        self.backup_store.delete_before(cutoff)
```

## Disaster Recovery Runbook

```python
class DisasterRecoveryRunbook:
    def __init__(self, backup_policy, deployer):
        self.backup_policy = backup_policy
        self.deployer = deployer

    def recover(self, snapshot_id):
        data = self.backup_policy.restore(snapshot_id)
        return self.deployer.deploy(data)
```

---

## 15. Appendix

## Regulatory References

| Regulation | Scope | Key Obligations |
|------------|-------|-----------------|
| GDPR | EU personal data | Consent, DPIAs, breach notification |
| CCPA/CPRA | California consumers | Right to know, delete, opt-out |
| HIPAA | US healthcare | BAA, safeguards, breach notification |
| PCI-DSS | Payment card data | Segmentation, encryption, monitoring |
| SOC 2 | SaaS trust services | Security, availability, confidentiality |
| ISO 27001 | Information security | ISMS, risk treatment, controls |
| EU AI Act | AI systems | Risk classes, conformity assessment |
| Brazil LGPD | Brazil personal data | Consent, DPO, data subject rights |

## Compliance Maturity Model

| Level | Capability |
|-------|------------|
| 1 | No documented ownership or logging |
| 2 | Ownership documented; ad-hoc review |
| 3 | Evaluation and monitoring in place |
| 4 | Continuous compliance measurement |
| 5 | Adaptive policy and automated remediation |

## Domain Glossary

| Term | Meaning |
|------|---------|
| DPIA | Data protection impact assessment |
| BAA | Business associate agreement |
| DPO | Data protection officer |
| SCC | Standard contractual clauses |
| PET | Privacy-enhancing technology |
| LLM | Large language model |

```markdown
## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
```