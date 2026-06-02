# Risk Tiering Guide

Use this guide to decide how much review, testing, monitoring, and evidence an AI system needs.

## Risk Tiers

| Tier | Description | Minimum Controls |
|------|-------------|------------------|
| Low | Internal assistance with no sensitive data and no autonomous side effects | Owner, purpose, basic logs, core checklist |
| Medium | Customer-facing content, business data, retrieval, or reversible tools | Security review, evaluations, monitoring, rollback plan |
| High | Financial, legal, safety, employment, healthcare, access, or rights impact | Formal risk review, human oversight, audit evidence, incident plan |
| Prohibited | Uses banned by law, policy, contract, or organization values | Block design, deployment, and access paths |

## Tiering Questions

- Can the system affect a user's rights, money, safety, employment, healthcare, or access to services?
- Does it process personal, sensitive, confidential, or regulated data?
- Can it call tools that write, delete, send, purchase, approve, or change status?
- Is the output shown directly to customers or third parties?
- Would a wrong answer create legal, financial, reputational, or safety harm?
- Does it operate without human review?

## Control Matrix

| Control | Low | Medium | High |
|---------|-----|--------|------|
| System owner | Required | Required | Required |
| Intended use | Required | Required | Required |
| Security review | Recommended | Required | Required |
| Privacy review | If personal data | Required if personal data | Required |
| Evaluation suite | Basic | Required | Required with edge cases |
| Human oversight | Optional | Conditional | Required |
| Audit evidence | Lightweight | Release evidence | Formal evidence pack |
| Monitoring | Basic | Required | Required with alerts |
| Incident runbook | Recommended | Required | Required |

## Review Cadence

| Tier | Suggested Cadence |
|------|-------------------|
| Low | Every major release |
| Medium | Every release or monthly |
| High | Every material change and quarterly |
