# Compliance Domain - Examples

> Practical examples for documenting and enforcing compliance controls.

## Overview

These examples provide reusable starting points for compliance records, release reviews, approval rules, and trace redaction patterns. Adapt them to your organization's risk model and legal requirements.

## AI System Register Entry

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
```

## Release Review Template

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

## Tool Approval Rule

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

## Trace Redaction Pattern

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
