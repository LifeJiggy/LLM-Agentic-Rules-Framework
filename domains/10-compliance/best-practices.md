# Compliance Domain - Best Practices

## Overview

This document outlines comprehensive compliance best practices for LLM/agentic systems, covering data protection, model change management, evaluation compliance, audit trails, privacy regulations, security controls, and governance.

---

## Table of Contents

1. [Data Protection](#1-data-protection)
2. [Model Change Management](#2-model-change-management)
3. [Evaluation Compliance](#3-evaluation-compliance)
4. [Audit Trails](#4-audit-trails)
5. [Privacy Regulations](#5-privacy-regulations)
6. [Security Controls](#6-security-controls)
7. [Governance](#7-governance)
8. [Incident Response](#8-incident-response)
9. [Vendor Compliance](#9-vendor-compliance)
10. [Documentation](#10-documentation)
11. [Training](#11-training)
12. [Monitoring](#12-monitoring)
13. [Access Control](#13-access-control)
14. [Data Retention](#14-data-retention)
15. [Testing](#15-testing)
16. [Risk Management](#16-risk-management)
17. [International Compliance](#17-international-compliance)
18. [Ethical AI](#18-ethical-ai)
19. [Metrics and Reporting](#19-metrics-and-reporting)
20. [Appendices](#20-appendices)

---

## 1. Data Protection

### Encryption at Rest

```python
class EncryptedDataStore:
    """Store data encrypted at rest."""
    
    def __init__(self, encryption_key: bytes):
        self.key = encryption_key
        self.cipher = AES.new(self.key, AES.MODE_GCM)
    
    def store(self, user_id: str, data: dict) -> str:
        plaintext = json.dumps(data).encode()
        ciphertext, tag = self.cipher.encrypt_and_digest(plaintext)
        return database.save_encrypted(user_id, ciphertext, tag)
    
    def retrieve(self, user_id: str) -> dict:
        ciphertext, tag = database.get_encrypted(user_id)
        plaintext = self.cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(plaintext.decode())
```

### PII Masking

```python
class PIIMasking:
    """Mask PII in processing."""
    
    def mask(self, text):
        return re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[EMAIL]',
            text
        )
    
    def mask_phone(self, text):
        return re.sub(
            r'\+?[\d\s\-\(\)]{10,}',
            '[PHONE]',
            text
        )
    
    def mask_ssn(self, text):
        return re.sub(
            r'\d{3}-\d{2}-\d{4}',
            '[SSN]',
            text
        )
```

### Data Minimization

```python
class DataMinimizer:
    """Enforce data minimization principles."""
    
    ALLOWED_FIELDS = {
        "user_id": True,
        "session_id": True,
        "prompt": True,
        "response": True,
        "timestamp": True
    }
    
    def filter_fields(self, data: dict) -> dict:
        return {
            k: v for k, v in data.items()
            if self.ALLOWED_FIELDS.get(k, False)
        }
```

### Purpose Limitation

```python
class PurposeLimiter:
    def __init__(self):
        self.allowed_purposes = {
            "user_id": ["processing", "billing", "support"],
            "email": ["processing", "support"],
            "phone": ["support"]
        }
    
    def can_use(self, field: str, purpose: str) -> bool:
        return purpose in self.allowed_purposes.get(field, [])
```

---

## 2. Model Change Management

### Model Change Registry

```python
class ModelChangeRegistry:
    """Track model versions and changes."""
    
    def __init__(self):
        self.changes = []
    
    def register_change(self, model_name, version, changes, approval):
        entry = {
            "model": model_name,
            "version": version,
            "changes": changes,
            "approved_by": approval,
            "approved_at": datetime.utcnow()
        }
        self.changes.append(entry)
        return self._archive(entry)
    
    def get_changes(self, model_name, since):
        return [c for c in self.changes 
                if c["model"] == model_name and c["approved_at"] > since]
```

### Change Approval Workflow

```python
class ChangeApprovalWorkflow:
    def __init__(self):
        self.pending = []
        self.approved = []
        self.rejected = []
    
    def submit(self, change: dict, requester: str):
        change["status"] = "pending"
        change["requester"] = requester
        change["submitted_at"] = datetime.utcnow()
        self.pending.append(change)
        return change["id"]
    
    def approve(self, change_id: str, approver: str):
        change = self._find(change_id)
        change["status"] = "approved"
        change["approved_by"] = approver
        change["approved_at"] = datetime.utcnow()
        self.pending.remove(change)
        self.approved.append(change)
    
    def reject(self, change_id: str, reason: str):
        change = self._find(change_id)
        change["status"] = "rejected"
        change["rejection_reason"] = reason
        self.pending.remove(change)
        self.rejected.append(change)
```

### Model Versioning

```python
class ModelVersionManager:
    def __init__(self):
        self.versions = {}
    
    def register(self, name: str, version: str, metadata: dict):
        self.versions[f"{name}:{version}"] = {
            "name": name,
            "version": version,
            "metadata": metadata,
            "registered_at": datetime.utcnow().isoformat()
        }
    
    def get(self, name: str, version: str = None) -> dict:
        if version:
            return self.versions.get(f"{name}:{version}")
        # Return latest
        candidates = [
            v for k, v in self.versions.items() if k.startswith(f"{name}:")
        ]
        return max(candidates, key=lambda x: x["version"]) if candidates else None
```

---

## 3. Evaluation Compliance

### Safety Evaluation

```python
class ComplianceEvaluator:
    """Evaluate model behavior for compliance."""
    
    def __init__(self, evaluation_suite):
        self.suite = evaluation_suite
    
    def evaluate_safety(self, model, dataset):
        """Run safety evaluation."""
        results = self.suite.run_safety_tests(model, dataset)
        
        audit_log.record({
            "evaluation_type": "safety",
            "model_version": model.version,
            "results": results,
            "passed": results.score > 0.95
        })
        
        return results
```

### Fairness Evaluation

```python
class FairnessEvaluator:
    def __init__(self, sensitive_attributes: list):
        self.sensitive_attributes = sensitive_attributes
    
    def evaluate(self, model, test_data) -> dict:
        results = {}
        for attr in self.sensitive_attributes:
            groups = test_data.groupby(attr)
            group_metrics = {}
            for group_name, group_data in groups:
                predictions = model.predict(group_data["input"])
                group_metrics[group_name] = {
                    "accuracy": accuracy_score(group_data["label"], predictions),
                    "false_positive_rate": self._fpr(group_data["label"], predictions)
                }
            results[attr] = group_metrics
        return results
```

### Bias Detection

```python
class BiasDetector:
    def __init__(self):
        self.registry = {}
    
    def register_test(self, name: str, test_fn):
        self.registry[name] = test_fn
    
    def run_all(self, model, dataset) -> dict:
        results = {}
        for name, test_fn in self.registry.items():
            results[name] = test_fn(model, dataset)
        return results
```

---

## 4. Audit Trails

### Comprehensive Audit Logging

```python
class AuditLogger:
    """Immutable audit trail for compliance."""
    
    def __init__(self, storage):
        self.storage = storage
    
    def log(self, actor: str, action: str, resource: str, 
            outcome: str, metadata: dict = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "actor": actor,
            "action": action,
            "resource": resource,
            "outcome": outcome,
            "metadata": metadata or {},
            "source_ip": request.remote_addr if request else None,
            "user_agent": request.headers.get("User-Agent") if request else None
        }
        return self.storage.append("audit", entry)
    
    def query(self, filters: dict) -> list:
        return self.storage.query("audit", filters)
    
    def export(self, start: str, end: str, format: str = "json") -> str:
        records = self.query({"timestamp": {"$gte": start, "$lte": end}})
        if format == "json":
            return json.dumps(records)
        elif format == "csv":
            return self._to_csv(records)
        return records
```

### Tamper-Evident Logging

```python
class TamperEvidentLogger:
    def __init__(self, backend):
        self.backend = backend
        self.previous_hash = None
    
    def log(self, entry: dict):
        entry["hash"] = self._compute_hash(entry)
        if self.previous_hash:
            entry["previous_hash"] = self.previous_hash
        self.previous_hash = entry["hash"]
        self.backend.append(entry)
    
    def _compute_hash(self, entry: dict) -> str:
        content = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def verify_chain(self) -> bool:
        entries = self.backend.get_all()
        for i in range(1, len(entries)):
            if entries[i]["previous_hash"] != entries[i-1]["hash"]:
                return False
        return True
```

### Access Logging

```python
class AccessLogger:
    def __init__(self, storage):
        self.storage = storage
    
    async def log_access(self, user_id: str, resource: str, action: str):
        await self.storage.append("access_log", {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "resource": resource,
            "action": action
        })
    
    async def get_user_activity(self, user_id: str, days: int = 30) -> list:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return await self.storage.query("access_log", {
            "user_id": user_id,
            "timestamp": {"$gte": cutoff.isoformat()}
        })
```

---

## 5. Privacy Regulations

### GDPR Compliance

```python
class GDPRCompliance:
    def __init__(self, storage):
        self.storage = storage
        self.retention_policies = {
            "conversations": timedelta(days=365),
            "logs": timedelta(days=90),
            "audit": timedelta(days=2555)  # 7 years
        }
    
    async def handle_dsar(self, user_id: str) -> dict:
        data = await self.storage.get_all_user_data(user_id)
        return {
            "user_id": user_id,
            "data": data,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    async def handle_erasure(self, user_id: str, verified: bool = False):
        if not verified:
            raise PermissionError("Erasure requires verified identity")
        await self.storage.delete_user_data(user_id)
        await self.audit.log("erasure", user_id=user_id)
    
    async def handle_portability(self, user_id: str, format: str = "json"):
        data = await self.storage.get_all_user_data(user_id)
        if format == "json":
            return json.dumps(data)
        elif format == "csv":
            return self._to_csv(data)
```

### CCPA Compliance

```python
class CCPACompliance:
    def __init__(self):
        self.data_categories = ["personal_info", "sensitive_personal_info"]
    
    def get_privacy_notice(self) -> str:
        return """
# Privacy Notice

## Data Collected
- Personal information: name, email, IP address
- Sensitive personal information: None

## Purpose
- To provide and improve our services.

## Third Parties
- LLM providers (OpenAI, Anthropic)
- Cloud infrastructure (AWS)

## Your Rights
- Know what data is collected
- Request deletion
- Opt out of sale (not applicable)
"""
    
    async def handle_opt_out(self, user_id: str):
        await self.storage.update_preferences(user_id, {"sale_opt_out": True})
        await self.audit.log("ccpa_opt_out", user_id=user_id)
```

### HIPAA Compliance (if applicable)

```python
class HIPAACompliance:
    def __init__(self):
        self.phi_fields = ["name", "dob", "ssn", "medical_record"]
        self.baa_signed = True
    
    def is_phi(self, data: dict) -> bool:
        return any(field in data for field in self.phi_fields)
    
    def sanitize_phi(self, data: dict) -> dict:
        sanitized = data.copy()
        for field in self.phi_fields:
            if field in sanitized:
                sanitized[field] = "[REDACTED]"
        return sanitized
```

---

## 6. Security Controls

### Access Control Lists

```python
class AccessControlList:
    def __init__(self):
        self.policies = {}
    
    def add_policy(self, resource: str, principal: str, actions: list):
        key = f"{resource}:{principal}"
        self.policies[key] = actions
    
    def can(self, principal: str, resource: str, action: str) -> bool:
        key = f"{resource}:{principal}"
        return action in self.policies.get(key, [])
```

### RBAC Implementation

```python
class RBAC:
    def __init__(self):
        self.roles = {
            "admin": ["read", "write", "delete", "manage"],
            "operator": ["read", "write"],
            "viewer": ["read"]
        }
        self.user_roles = {}
    
    def assign_role(self, user_id: str, role: str):
        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}")
        self.user_roles[user_id] = role
    
    def can(self, user_id: str, action: str) -> bool:
        role = self.user_roles.get(user_id, "viewer")
        return action in self.roles.get(role, [])
```

### Secret Rotation

```python
class SecretRotationPolicy:
    def __init__(self):
        self.rotation_intervals = {
            "api_keys": timedelta(days=90),
            "jwt_secrets": timedelta(days=30),
            "database_passwords": timedelta(days=60),
            "tls_certificates": timedelta(days=30)
        }
        self.rotation_history = {}
    
    def is_due(self, secret_type: str, last_rotated: datetime) -> bool:
        interval = self.rotation_intervals.get(secret_type)
        if not interval:
            return False
        return datetime.utcnow() - last_rotated > interval
    
    def rotate(self, secret_type: str, new_value: str):
        self.rotation_history[secret_type] = {
            "rotated_at": datetime.utcnow().isoformat(),
            "new_value": new_value
        }
```

---

## 7. Governance

### Compliance Framework

```python
class ComplianceFramework:
    def __init__(self):
        self.controls = {}
        self.assessments = []
    
    def add_control(self, control_id: str, description: str, owner: str):
        self.controls[control_id] = {
            "description": description,
            "owner": owner,
            "status": "active"
        }
    
    def assess(self, control_id: str) -> dict:
        control = self.controls.get(control_id)
        if not control:
            raise ValueError(f"Unknown control: {control_id}")
        return {
            "control_id": control_id,
            "status": control["status"],
            "owner": control["owner"],
            "assessed_at": datetime.utcnow().isoformat()
        }
```

### Policy Engine

```python
class PolicyEngine:
    def __init__(self):
        self.policies = {}
    
    def add_policy(self, name: str, rule: Callable):
        self.policies[name] = rule
    
    def evaluate(self, context: dict) -> list:
        violations = []
        for name, rule in self.policies.items():
            if not rule(context):
                violations.append(name)
        return violations
```

### Risk Assessment

```python
class RiskAssessment:
    def __init__(self):
        self.risks = []
    
    def add_risk(self, name: str, likelihood: str, impact: str, mitigation: str):
        self.risks.append({
            "name": name,
            "likelihood": likelihood,
            "impact": impact,
            "mitigation": mitigation,
            "score": self._calculate_score(likelihood, impact),
            "identified_at": datetime.utcnow().isoformat()
        })
    
    def _calculate_score(self, likelihood: str, impact: str) -> int:
        scale = {"low": 1, "medium": 2, "high": 3}
        return scale.get(likelihood, 1) * scale.get(impact, 1)
    
    def get_high_risks(self) -> list:
        return [r for r in self.risks if r["score"] >= 6]
```

---

## 8. Incident Response

### Security Incident Response

```python
class SecurityIncidentResponse:
    def __init__(self, notifier, forensics):
        self.notifier = notifier
        self.forensics = forensics
        self.active_incidents = {}
    
    async def create_incident(self, severity: str, description: str):
        incident_id = f"SEC-{uuid.uuid4().hex[:8]}"
        self.active_incidents[incident_id] = {
            "id": incident_id,
            "severity": severity,
            "description": description,
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
        await self.notifier.send({
            "incident_id": incident_id,
            "severity": severity,
            "description": description
        })
        return incident_id
    
    async def contain(self, incident_id: str):
        incident = self.active_incidents.get(incident_id)
        if not incident:
            return
        incident["status"] = "contained"
        incident["contained_at"] = datetime.utcnow().isoformat()
        await self.forensics.collect(incident_id)
    
    async def resolve(self, incident_id: str, resolution: str):
        incident = self.active_incidents.get(incident_id)
        if not incident:
            return
        incident["status"] = "resolved"
        incident["resolved_at"] = datetime.utcnow().isoformat()
        incident["resolution"] = resolution
```

### Breach Notification

```python
class BreachNotification:
    def __init__(self, legal, communications):
        self.legal = legal
        self.communications = communications
    
    async def notify_regulators(self, breach: dict):
        await self.legal.submit({
            "breach_type": breach["type"],
            "affected_records": breach["affected_count"],
            "data_categories": breach["data_categories"],
            "measures_taken": breach["mitigation"]
        })
    
    async def notify_affected_users(self, user_ids: list, breach: dict):
        for user_id in user_ids:
            await self.communications.send_email(
                to=user_id,
                subject="Data Breach Notification",
                body=f"""
We are writing to inform you of a data breach that may have affected your information.
 breach_id: {breach['id']}
 date: {breach['date']}
                """
            )
```

---

## 9. Vendor Compliance

### Vendor Assessment

```python
class VendorAssessment:
    def __init__(self):
        self.assessments = {}
    
    def assess(self, vendor: str, criteria: dict) -> dict:
        score = self._calculate_score(vendor, criteria)
        self.assessments[vendor] = {
            "score": score,
            "criteria": criteria,
            "assessed_at": datetime.utcnow().isoformat()
        }
        return self.assessments[vendor]
    
    def _calculate_score(self, vendor: str, criteria: dict) -> float:
        total = 0
        for criterion, weight in criteria.items():
            total += self._evaluate_criterion(vendor, criterion) * weight
        return total
```

### DPA Management

```python
class DPAManager:
    def __init__(self):
        self.dpas = {}
    
    def register(self, vendor: str, dpa_url: str, signed_date: str):
        self.dpas[vendor] = {
            "url": dpa_url,
            "signed_date": signed_date,
            "status": "active"
        }
    
    def is_compliant(self, vendor: str) -> bool:
        dpa = self.dpas.get(vendor)
        if not dpa:
            return False
        return dpa["status"] == "active"
```

### Subprocessor Tracking

```python
class SubprocessorTracker:
    def __init__(self):
        self.subprocessors = {}
    
    def register(self, name: str, vendor: str, purpose: str, 
                 location: str, safeguards: str):
        self.subprocessors[name] = {
            "vendor": vendor,
            "purpose": purpose,
            "location": location,
            "safeguards": safeguards,
            "added_at": datetime.utcnow().isoformat()
        }
    
    def list_active(self) -> list:
        return list(self.subprocessors.values())
```

---

## 10. Documentation

### Documentation Requirements

```markdown
# Compliance Documentation Requirements

## Privacy Policy
- Data collection purposes
- Data retention periods
- User rights (access, erasure, portability)
- Contact information for DPO

## Data Processing Records (Art. 30 GDPR)
- Controller contact details
- Processor contact details
- Data categories
- Retention periods
- Security measures

## Security Controls Documentation
- Encryption methods
- Access control policies
- Audit logging procedures
- Incident response plan
```

### Evidence Collection

```python
class ComplianceEvidence:
    def __init__(self, storage):
        self.storage = storage
    
    def collect(self, control_id: str, evidence_type: str, 
                evidence_data: dict):
        entry = {
            "control_id": control_id,
            "evidence_type": evidence_type,
            "evidence_data": evidence_data,
            "collected_at": datetime.utcnow().isoformat()
        }
        self.storage.save("compliance_evidence", entry)
    
    def generate_report(self, framework: str) -> dict:
        controls = self.storage.query("compliance_evidence", {"framework": framework})
        return {
            "framework": framework,
            "controls": controls,
            "generated_at": datetime.utcnow().isoformat()
        }
```

### Audit Preparation

```python
class AuditPreparation:
    def __init__(self):
        self.checklist = {}
    
    def prepare(self, audit_type: str) -> dict:
        return {
            "audit_type": audit_type,
            "checklist": self._get_checklist(audit_type),
            "artifacts": self._collect_artifacts(audit_type),
            "contacts": self._get_contacts(audit_type)
        }
    
    def _get_checklist(self, audit_type: str) -> list:
        checklists = {
            "SOC2": ["security", "availability", "processing_integrity", "confidentiality", "privacy"],
            "GDPR": ["data_minimization", "consent", "right_to_erasure", "data_portability"],
            "HIPAA": ["access_controls", "audit_trails", "encryption", "baa"]
        }
        return checklists.get(audit_type, [])
```

---

## 11. Training

### Compliance Training Program

```python
class ComplianceTraining:
    def __init__(self):
        self.courses = {}
        self.completions = {}
    
    def register_course(self, course_id: str, title: str, 
                        content: str, audience: str):
        self.courses[course_id] = {
            "title": title,
            "content": content,
            "audience": audience
        }
    
    def assign(self, user_id: str, course_id: str):
        if course_id not in self.completions:
            self.completions[course_id] = []
        self.completions[course_id].append({
            "user_id": user_id,
            "assigned_at": datetime.utcnow().isoformat(),
            "completed": False
        })
    
    def complete(self, user_id: str, course_id: str):
        for record in self.completions.get(course_id, []):
            if record["user_id"] == user_id:
                record["completed"] = True
                record["completed_at"] = datetime.utcnow().isoformat()
```

### Security Awareness

```markdown
# Security Awareness Training

## Quarterly Training Topics

1. Phishing awareness
2. Password hygiene
3. Incident reporting
4. Data classification

## Completion Tracking

- All employees: annual training
- Engineers: quarterly deep-dive
- Managers: annual leadership module
```

---

## 12. Monitoring

### Compliance Monitoring

```python
class ComplianceMonitor:
    def __init__(self):
        self.metrics = {}
        self.alerts = []
    
    def check_compliance(self, control: str) -> dict:
        result = self._evaluate_control(control)
        if not result["compliant"]:
            self.alerts.append({
                "control": control,
                "timestamp": datetime.utcnow().isoformat(),
                "issue": result["issue"]
            })
        return result
    
    def _evaluate_control(self, control: str) -> dict:
        # Check control implementation
        return {"compliant": True, "evidence": "automated_check"}
```

### Violation Detection

```python
class ViolationDetector:
    def __init__(self, rules: list):
        self.rules = rules
    
    def detect(self, event: dict) -> list:
        violations = []
        for rule in self.rules:
            if rule["condition"](event):
                violations.append({
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "event": event
                })
        return violations
```

---

## 13. Access Control

### Least Privilege

```python
class LeastPrivilegeEnforcer:
    def __init__(self):
        self.roles = {
            "user": ["read_own"],
            "admin": ["read_all", "write", "delete"],
            "auditor": ["read_all"]
        }
    
    def grant(self, user_id: str, role: str):
        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}")
        self.user_roles[user_id] = role
    
    def can(self, user_id: str, action: str, resource: str) -> bool:
        role = self.user_roles.get(user_id, "user")
        permissions = self.roles.get(role, [])
        return f"{action}_{resource}" in permissions
```

### MFA Enforcement

```python
class MFAEnforcer:
    def __init__(self):
        self.enforced_roles = ["admin", "operator"]
    
    def requires_mfa(self, user_id: str) -> bool:
        user_role = self.user_roles.get(user_id)
        return user_role in self.enforced_roles
    
    def verify(self, user_id: str, token: str) -> bool:
        if not self.requires_mfa(user_id):
            return True
        return self._validate_totp(user_id, token)
```

---

## 14. Data Retention

### Retention Policies

```python
class RetentionManager:
    def __init__(self, storage):
        self.storage = storage
        self.policies = {
            "conversations": timedelta(days=365),
            "logs": timedelta(days=90),
            "audit": timedelta(days=2555),
            "metrics": timedelta(days=365)
        }
    
    async def enforce(self):
        for data_type, ttl in self.policies.items():
            cutoff = datetime.utcnow() - ttl
            deleted = await self.storage.delete_older_than(data_type, cutoff)
            logger.info(f"Retention: deleted {deleted} {data_type} records")
    
    async def archive(self, data_type: str, archive_bucket: str):
        cutoff = datetime.utcnow() - self.policies[data_type]
        await self.storage.archive(data_type, archive_bucket, cutoff)
```

### Legal Holds

```python
class LegalHoldManager:
    def __init__(self, storage):
        self.storage = storage
        self.active_holds = set()
    
    def place_hold(self, user_id: str, case_id: str):
        self.active_holds.add(user_id)
        self.storage.set(f"legal_hold:{user_id}", {"case_id": case_id, "active": True})
    
    def release_hold(self, user_id: str):
        self.active_holds.discard(user_id)
        self.storage.delete(f"legal_hold:{user_id}")
    
    def is_on_hold(self, user_id: str) -> bool:
        return user_id in self.active_holds
```

---

## 15. Testing

### Compliance Testing

```python
class ComplianceTester:
    def __init__(self):
        self.test_cases = []
    
    def add_test(self, name: str, test_fn: Callable):
        self.test_cases.append({"name": name, "fn": test_fn})
    
    def run_all(self) -> dict:
        results = {}
        for test in self.test_cases:
            try:
                test["fn"]()
                results[test["name"]] = "pass"
            except AssertionError as e:
                results[test["name"]] = f"fail: {e}"
        return results
```

### Penetration Testing

```python
class PenetrationTest:
    def __init__(self, scope: list):
        self.scope = scope
        self.findings = []
    
    def test(self):
        for target in self.scope:
            # Run security tests
            pass
        return self.findings
```

### Vulnerability Scanning

```python
class VulnerabilityScanner:
    def __init__(self):
        self.scanners = []
    
    def add_scanner(self, scanner: Callable):
        self.scanners.append(scanner)
    
    def scan(self) -> dict:
        findings = []
        for scanner in self.scanners:
            findings.extend(scanner())
        return {"findings": findings, "scan_date": datetime.utcnow().isoformat()}
```

---

## 16. Risk Management

### Risk Assessment

```python
class RiskAssessment:
    def __init__(self):
        self.risks = []
    
    def add_risk(self, name: str, likelihood: str, impact: str, mitigation: str):
        self.risks.append({
            "name": name,
            "likelihood": likelihood,
            "impact": impact,
            "mitigation": mitigation,
            "score": self._calculate_score(likelihood, impact),
            "identified_at": datetime.utcnow().isoformat()
        })
    
    def _calculate_score(self, likelihood: str, impact: str) -> int:
        scale = {"low": 1, "medium": 2, "high": 3}
        return scale.get(likelihood, 1) * scale.get(impact, 1)
```

### Risk Register

```python
class RiskRegister:
    def __init__(self):
        self.risks = {}
    
    def add(self, risk_id: str, description: str, mitigation: str, owner: str):
        self.risks[risk_id] = {
            "description": description,
            "mitigation": mitigation,
            "owner": owner,
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
    
    def update_status(self, risk_id: str, status: str):
        if risk_id in self.risks:
            self.risks[risk_id]["status"] = status
            self.risks[risk_id]["updated_at"] = datetime.utcnow().isoformat()
```

### Mitigation Tracking

```python
class MitigationTracker:
    def __init__(self):
        self.mitigations = {}
    
    def add(self, risk_id: str, action: str, owner: str, due: str):
        self.mitigations[risk_id] = {
            "action": action,
            "owner": owner,
            "due": due,
            "status": "in_progress"
        }
    
    def complete(self, risk_id: str):
        if risk_id in self.mitigations:
            self.mitigations[risk_id]["status"] = "completed"
            self.mitigations[risk_id]["completed_at"] = datetime.utcnow().isoformat()
```

---

## 17. International Compliance

### Data Residency

```python
class DataResidencyManager:
    def __init__(self):
        self.regional_rules = {
            "EU": {"storage": "eu-west-1", "transfer": "intra-EU only"},
            "US": {"storage": "us-east-1", "transfer": "allowed"},
            "UK": {"storage": "eu-west-1", "transfer": "intra-UK only"}
        }
    
    def get_storage_region(self, user_region: str) -> str:
        return self.regional_rules.get(user_region, {}).get("storage", "us-east-1")
    
    def can_transfer(self, from_region: str, to_region: str) -> bool:
        rule = self.regional_rules.get(from_region, {})
        allowed = rule.get("transfer", "")
        return to_region in allowed or "allowed" in allowed
```

### Cross-Border Data Transfer

```python
class CrossBorderTransfer:
    def __init__(self):
        self.sccs = {}  # Standard Contractual Clauses
    
    def validate_transfer(self, from_country: str, to_country: str) -> bool:
        eu_countries = ["DE", "FR", "IT", "ES", "NL"]
        if from_country in eu_countries and to_country not in eu_countries:
            return self._has_sccs(from_country, to_country)
        return True
    
    def _has_sccs(self, from_c: str, to_c: str) -> bool:
        return f"{from_c}:{to_c}" in self.sccs
```

---

## 18. Ethical AI

### Fairness Metrics

```python
class FairnessMetrics:
    def __init__(self):
        self.metrics = {}
    
    def calculate_demographic_parity(self, predictions: list, 
                                     sensitive_attr: list) -> float:
        groups = {}
        for pred, attr in zip(predictions, sensitive_attr):
            groups.setdefault(attr, []).append(pred)
        rates = {g: sum(v)/len(v) for g, v in groups.items()}
        return min(rates.values()) / max(rates.values())
    
    def calculate_equalized_odds(self, y_true: list, y_pred: list, 
                                 sensitive_attr: list) -> float:
        groups = {}
        for true, pred, attr in zip(y_true, y_pred, sensitive_attr):
            groups.setdefault(attr, {"tp": 0, "fp": 0, "fn": 0, "tn": 0})
            if pred == 1 and true == 1:
                groups[attr]["tp"] += 1
            elif pred == 1 and true == 0:
                groups[attr]["fp"] += 1
            elif pred == 0 and true == 1:
                groups[attr]["fn"] += 1
            else:
                groups[attr]["tn"] += 1
        
        tprs = {g: (v["tp"]/(v["tp"]+v["fn"]) if v["tp"]+v["fn"] > 0 else 0) for g, v in groups.items()}
        fprs = {g: (v["fp"]/(v["fp"]+v["tn"]) if v["fp"]+v["tn"] > 0 else 0) for g, v in groups.items()}
        return min(tprs.values()) / max(tprs.values())
```

### Explainability

```python
class ExplainabilityCompliance:
    def __init__(self):
        self.explanations = {}
    
    def generate_explanation(self, model, input_data: dict) -> str:
        explanation = {
            "model_version": model.version,
            "input_features": list(input_data.keys()),
            "decision_factors": self._extract_factors(model, input_data),
            "confidence": model.confidence(input_data),
            "alternatives_considered": model.alternatives(input_data)
        }
        return json.dumps(explanation, indent=2)
```

### Human Oversight

```python
class HumanOversight:
    def __init__(self):
        self.high_stakes_categories = ["medical", "legal", "financial"]
    
    def requires_human_review(self, decision: dict) -> bool:
        category = decision.get("category", "")
        confidence = decision.get("confidence", 1.0)
        return category in self.high_stakes_categories and confidence < 0.9
```

---

## 19. Metrics and Reporting

### Compliance Metrics

```python
class ComplianceMetrics:
    def __init__(self):
        self.metrics = {}
    
    def record(self, name: str, value: float, target: float):
        self.metrics[name] = {
            "value": value,
            "target": target,
            "status": "met" if value >= target else "violated",
            "recorded_at": datetime.utcnow().isoformat()
        }
    
    def generate_dashboard(self) -> dict:
        return {
            "metrics": self.metrics,
            "overall_compliance": self._overall_score(),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _overall_score(self) -> float:
        if not self.metrics:
            return 0.0
        met = sum(1 for m in self.metrics.values() if m["status"] == "met")
        return met / len(self.metrics) * 100
```

### Regulatory Reporting

```python
class RegulatoryReporter:
    def __init__(self, frameworks: list):
        self.frameworks = frameworks
        self.reports = {}
    
    def generate_report(self, framework: str, period: str) -> dict:
        report = {
            "framework": framework,
            "period": period,
            "generated_at": datetime.utcnow().isoformat(),
            "controls": self._assess_controls(framework),
            "violations": self._get_violations(framework, period),
            "remediation_status": self._get_remediation_status(framework)
        }
        self.reports[f"{framework}:{period}"] = report
        return report
```

---

## 20. Appendices

### Compliance Frameworks Matrix

| Framework | Scope | Key Requirements |
|-----------|-------|------------------|
| GDPR | EU personal data | Consent, erasure, portability, DPIA |
| CCPA | California consumers | Right to know, delete, opt-out |
| HIPAA | US healthcare | BAA, access controls, audit trails |
| PCI-DSS | Payment data | Network segmentation, encryption |
| SOC 2 | SaaS trust | Security, availability, confidentiality |
| ISO 27001 | Information security | ISMS, risk assessment, controls |

### Checklist

See [checklist.md](./checklist.md) for compliance verification.

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)