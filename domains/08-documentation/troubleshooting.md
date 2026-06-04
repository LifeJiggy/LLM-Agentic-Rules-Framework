# Documentation Domain - Troubleshooting

## Overview

This document covers common documentation issues and their solutions for LLM/agentic systems. It is organized by symptom and root cause to help documentation authors, reviewers, and platform operators quickly resolve problems.

---

## Table of Contents

1. [Documentation Drift](#1-documentation-drift)
2. [Missing or Incomplete API Docs](#2-missing-or-incomplete-api-docs)
3. [No Prompt Documentation](#3-no-prompt-documentation)
4. [Missing Examples](#4-missing-examples)
5. [Outdated Runbooks](#5-outdated-runbooks)
6. [Monolithic Documentation Structure](#6-monolithic-documentation-structure)
7. [No Troubleshooting Sections](#7-no-troubleshooting-sections)
8. [Missing Limitations](#8-missing-limitations)
9. [Inconsistent Terminology](#9-inconsistent-terminology)
10. [No Security Documentation](#10-no-security-documentation)
11. [Poor Error Code Documentation](#11-poor-error-code-documentation)
12. [No Index or Search](#12-no-index-or-search)
13. [Code and Docs Out of Sync](#13-code-and-docs-out-of-sync)
14. [No Feedback Mechanism](#14-no-feedback-mechanism)
15. [No Maintenance Schedule](#15-no-maintenance-schedule)
16. [Undocumented Assumptions](#16-undocumented-assumptions)
17. [No Quick-Start Guide](#17-no-quick-start-guide)
18. [Missing Change Log](#18-missing-change-log)
19. [Unassigned Ownership](#19-unassigned-ownership)
20. [Accessibility Issues](#20-accessibility-issues)
21. [Broken Internal Links](#21-broken-internal-links)
22. [Outdated Diagrams](#22-outdated-diagrams)
23. [Compliance Documentation Gaps](#23-compliance-documentation-gaps)
24. [Performance Documentation Gaps](#24-performance-documentation-gaps)
25. [Diagram Rendering Failures](#25-diagram-rendering-failures)
26. [Search Optimization Issues](#26-search-optimization-issues)
27. [Localization and Translation Gaps](#27-localization-and-translation-gaps)
28. [Onboarding Documentation Gaps](#28-onboarding-documentation-gaps)
29. [Appendix: Troubleshooting Toolkit](#29-appendix-troubleshooting-toolkit)

---

## 1. Documentation Drift

### Symptom

Users report that the documentation does not match actual agent behavior. Examples:
- Docs say `POST /agent/process`, but code has `POST /agent/execute`.
- Documentation lists parameter `prompt`, but the API now requires `task`.
- Documentation says temperature default is 0.7, but code uses 0.3.

### Root Causes

- Code changed without updating docs.
- Prompt templates updated without updating prompt cards.
- API responses changed schema without updating examples.
- Renamed endpoints without updating cross-references.

### Solutions

#### Immediate Fix

1. Audit current code/docs for mismatches.
2. Update documentation to match implementation.
3. Add version tracking to prompts and schemas.
4. Update related cross-references.

#### Long-term Prevention

- **Generate docs from code**: Use OpenAPI, docstring scrapers, or DSL-to-doc generators.
- **CI check**: Add a pre-merge check that compares API schema to OpenAPI spec.
- **Prompt sync**: Store prompts in version control with metadata. Read doc cards from the same source.

```python
# Generate API docs from source
class APIDocGenerator:
    def generate_from_route(self, route):
        return f"""## {route.method} {route.path}

{route.summary}

### Request

{json.dumps(route.request_schema, indent=2)}

### Response

{json.dumps(route.response_schema, indent=2)}
"""
```

#### Verification

After update, verify with a tester:
```bash
# Compare documented parameters vs actual
curl -s https://api.example.com/openapi.json | jq .paths
diff <(curl -s https://docs.example.com/api.md) <(generated_docs)
```

---

## 2. Missing or Incomplete API Docs

### Symptom

Developer asks "What parameters does this endpoint accept?" and the docs are:
- Missing entirely.
- List endpoint path but no parameters.
- Missing response schema.
- No authentication instructions.

### Root Causes

- API was prototyped quickly without documentation.
- Docs were an afterthought.
- No owner assigned to API docs.
- API changed but docs were not updated.

### Solutions

#### Immediate Fix

1. Document every endpoint with at minimum:
   - HTTP method and path.
   - Request body schema (all required and optional fields).
   - Response schema (including error responses).
   - Authentication requirements.
   - Rate limits.

2. Create an OpenAPI spec even if not integrated into a portal yet.
3. Add one example request and one example response per endpoint.

#### Long-term Prevention

- **Doc-driven development**: Write OpenAPI spec before implementation.
- **PR requirement**: API changes require doc changes in the same PR.
- **Automated generation**: Generate docs from code annotations.

```yaml
# Minimum OpenAPI entry for each endpoint
paths:
  /agent/execute:
    post:
      summary: Execute agent task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AgentRequest'
      responses:
        '200':
          description: Successful execution
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
```

---

## 3. No Prompt Documentation

### Symptom

Prompts exist in code but have no documentation. Questions arise:
- What prompt is in production?
- What model and temperature is it using?
- When was it last changed?
- What are the known failure modes?

### Root Causes

- Prompts stored as strings in code without metadata.
- No prompt inventory or registry.
- Prompt changes happen in code commits without doc updates.

### Solutions

#### Immediate Fix

1. Create a prompt card for every production prompt.
2. Document: model, temperature, max tokens, version, author, date, examples.
3. Link prompt cards from operational runbooks and architecture docs.

#### Template

```markdown
# Prompt Card: [Name]

## Metadata
| Field | Value |
|-------|-------|
| Version | X.Y.Z |
| Model | gpt-4-turbo |
| Temperature | 0.3 |
| Author | @username |
| Date | YYYY-MM-DD |

## System Prompt
```
[Full prompt text]
```

## Tools Available
- tool_name(description)

## Examples
[Input/output pairs]

## Constraints
- [List]

## Performance
- Accuracy: X%
```

#### Long-term Prevention

- **Prompt registry**: Store prompts in a database with versioning.
- **CI check**: Deployments that change prompt files require prompt card updates.
- **Evaluation pipeline**: Automated evals run on every prompt change with results appearing in the prompt card.

```python
class PromptCardEnforcer:
    def validate(self, prompt_file: Path) -> bool:
        card_path = prompt_file.with_suffix(".md")
        if not card_path.exists():
            raise MissingPromptCardError(prompt_file)
        # Validate card has required sections
        card = card_path.read_text()
        required = ["## Metadata", "## System Prompt", "## Examples"]
        for section in required:
            if section not in card:
                raise IncompletePromptCardError(card_path, section)
        return True
```

---

## 4. Missing Examples

### Symptom

API endpoint exists but has no example request/response. Developer asks "How do I call this?" and gets no answer from docs.

### Root Causes

- Examples not prioritized during writing.
- Copy-paste from different contexts that broke formatting.
- Examples not tested after code changes.

### Solutions

#### Immediate Fix

1. Add at least one example request for each endpoint.
2. Add at least one example response (success and error).
3. Add one runnable code example per SDK/language.

#### Long-term Prevention

- **Example testing**: Run examples as part of CI. If example output doesn't match actual output, fail the build.
- **Example gallery**: Maintain a gallery of runnable examples sorted by complexity.
- **Snippet validation**: Test that all JSON examples are valid JSON.

```python
# Test that examples in docs are valid
class ExampleValidator:
    def test_json_examples(self, doc_path: Path):
        content = doc_path.read_text()
        json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
        for block in json_blocks:
            json.loads(block)  # Raises if invalid
```

---

## 5. Outdated Runbooks

### Symptom

During an incident, the on-call engineer follows a runbook and finds:
- Commands no longer work (CLI renamed, flags changed).
- Service names have changed.
- Contact info is outdated.
- Diagnostic steps reference old dashboards.

### Root Causes

- Infra or tooling changed without updating runbooks.
- Runbooks written once and never reviewed.
- Ownership is unclear.
- No testing of runbook accuracy.

### Solutions

#### Immediate Fix

1. Assign ownership of each runbook to a team.
2. Review all runbooks quarterly.
3. Test runbook commands in a staging environment.
4. Update contact info, dashboard URLs, and service names.

#### Runbook Format

```markdown
# Runbook: [Name]

## Last Updated
YYYY-MM-DD by @username

## Owner
@team-name

## Detection
- Alert: AlertName
- Dashboard: URL
- Threshold: value

## Diagnosis
1. Step-by-step diagnostic commands.
2. What to look for in each output.

## Remediation
1. Step-by-step remediation commands.
2. Rollback procedure.
3. Verification steps.

## Escalation
- Contact: @person or #channel
- When to escalate.

## Verification
- How to confirm the issue is resolved.
```

#### Long-term Prevention

- **Runbook CI**: Verify that URLs in runbooks return 200. Verify that commands in runbooks don't have obvious syntax errors.
- **Post-incident updates**: Always update runbook as part of post-mortem ticket.
- **Alert-to-doc links**: Every PagerDuty alert links to its runbook.

```python
class RunbookChecker:
    def check_urls(self, runbook_path: Path):
        content = runbook_path.read_text()
        urls = re.findall(r'https?://\S+', content)
        for url in urls:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            if resp.status_code >= 400:
                print(f"BROKEN: {url} in {runbook_path}")
```

---

## 6. Monolithic Documentation Structure

### Symptom

Single `README.md` or `docs.md` file contains everything. It is 5000+ lines long. Developers complain they cannot find information.

### Root Causes

- No documentation structure defined.
- Team did not agree on organization.
- Everything written to the first available file.

### Solutions

#### Immediate Fix

1. Split monolithic docs into logical sections by audience and topic.
2. Create an index.md or README.md that links to sections.
3. Move files into appropriate directories.

#### Recommended Structure

```
docs/
├── README.md
├── api/
│   ├── agents.md
│   ├── tools.md
│   └── openapi.yaml
├── guides/
│   ├── getting-started.md
│   ├── deployment.md
│   └── troubleshooting.md
├── operations/
│   ├── runbooks/
│   │   ├── high-error-rate.md
│   │   └── model-failure.md
│   └── slo.md
├── prompts/
│   └── customer-support.md
├── architecture/
│   ├── overview.md
│   ├── data-flow.md
│   └── adr/
└── compliance/
    └── gdpr.md
```

---

## 7. No Troubleshooting Sections

### Symptom

Deployment guide says "Run `kubectl apply`." When it fails, users have no guidance.

### Root Causes

- Author assumed deployment would always work.
- Troubleshooting was deprioritized.
- Team did not think about failure modes.

### Solutions

#### Immediate Fix

1. Add a Troubleshooting section to every operational guide.
2. Document common failure modes with symptoms, causes, and fixes.
3. Include diagnostic commands.

#### Template

```markdown
## Troubleshooting

### Pod not starting

**Symptoms:** `CrashLoopBackOff`

**Diagnosis:**
```bash
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>
```

**Common causes:**
- Image pull failure: check registry credentials.
- Crash in application: check logs for stack trace.
- Resource limits too low: increase memory/CPU in deployment yaml.

**Fix:**
```bash
kubectl set resources deployment/agent --limits=memory=2Gi
```

### Health check failing

**Symptoms:** `Readiness probe failed`

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
kubectl exec <pod-name> -- curl -f http://localhost:8000/health
```
```

---

## 8. Missing Limitations

### Symptom

Documentation over-promises. Example: "This agent can answer questions about any topic." Users are frustrated when it hallucinates or lacks knowledge.

### Root Causes

- Marketing language mixed with technical docs.
- No review of actual capabilities.
- Team did not document constraints.

### Solutions

#### Immediate Fix

1. Add a Limitations section to every agent/prompt card.
2. Be explicit about what the agent cannot do.
3. Include data cutoffs, geographic restrictions, rate limits.

#### Template

```markdown
## Limitations

- Knowledge cutoff: YYYY-MM-DD
- Maximum context: 128K tokens
- Supported languages: English, Spanish, French
- Not available 24/7: maintenance window daily 02:00-04:00 UTC
- Cannot access external databases (uses only search tool)
- Maximum 100 requests per session per day
```

---

## 9. Inconsistent Terminology

### Symptom

Same concept has different names in different docs:
- `agent.execute()`, `agent.run()`, `agent.invoke()`, `agent.process()`
- "Prompt", "instruction", "system message" used interchangeably without definition.

### Root Causes

- No glossary or style guide.
- Multiple authors with different backgrounds.
- Refactoring changed code names but docs were not updated.

### Solutions

#### Immediate Fix

1. Create a glossary with canonical terms.
2. Audit docs for inconsistent use of key terms.
3. Update all references to use canonical terms.

#### Long-term Prevention

- **Style guide**: Define preferred terms.
- **Linting**: Use Vale or custom linter to flag inconsistent terminology.
- **Review checklist**: Include "consistent terminology" in PR review.

```python
# Terminology linter example
TERMINOLOGY = {
    "execute": ["invoke", "process"],
    "prompt": ["instruction", "system message"],
    "tool": ["function", "action"],
}

class TerminologyChecker:
    def check(self, content: str) -> list:
        violations = []
        for canonical, aliases in TERMINOLOGY.items():
            for alias in aliases:
                if alias in content.lower():
                    violations.append(f"Use '{canonical}' instead of '{alias}'")
        return violations
```

---

## 10. No Security Documentation

### Symptom

Security-critical information is missing:
- No authentication instructions.
- No mention of encryption.
- Secret management unexplained.
- No security incident contact.

### Root Causes

- Security was not a documentation priority.
- Docs focused on functionality, not security posture.
- Legal/compliance review was not part of doc process.

### Solutions

#### Immediate Fix

1. Add a Security section to every affected document.
2. Document authentication, authorization, encryption, and incident reporting.
3. Link to security policy and runbook.

#### Template

```markdown
## Security

### Authentication

All API requests require a Bearer token:
```
Authorization: Bearer <token>
```

Tokens expire after 1 hour. Refresh via `POST /auth/refresh`.

### Authorization

Users can only access their own sessions. Admin endpoints require `admin` scope.

### Encryption

- Data in transit: TLS 1.3
- Data at rest: AES-256

### Secret Management

- Store API keys in environment variables or secrets manager.
- Never commit secrets to version control.
- Rotate keys every 90 days.

### Reporting Vulnerabilities

Email security@example.com. Do not open public issues.
```

---

## 11. Poor Error Code Documentation

### Symptom

Users see error codes in API responses but docs say nothing about them or give unhelpful descriptions like "Error" or "Something went wrong."

### Root Causes

- Error handling was not documented during development.
- Error codes were added as needed without updating docs.
- Generic error messages used.

### Solutions

#### Immediate Fix

1. Create an error code reference table.
2. Document each code with:
   - HTTP status.
   - Meaning.
   - Resolution steps.
   - Example.

#### Template

```markdown
## Error Codes

| Code | HTTP | Meaning | Resolution |
|------|------|---------|------------|
| E001 | 400 | Invalid request body | Check JSON schema, ensure required fields present |
| E002 | 401 | Authentication required | Verify API key and token expiry |
| E003 | 403 | Insufficient permissions | Check user scopes, contact admin |
| E004 | 404 | Resource not found | Verify ID or path exists |
| E005 | 429 | Rate limit exceeded | Implement exponential backoff, respect Retry-After header |
| E006 | 500 | LLM provider unavailable | Enable fallback model via MODEL_FALLBACK=true |
| E007 | 503 | Service temporarily unavailable | Retry after 30 seconds, check status page |
```

#### Long-term Prevention

- **Error code registry**: Maintain a single source of truth for error codes.
- **Auto-generated error reference**: Generate error docs from code raise statements.

```python
class ErrorRegistry:
    errors = {
        "E001": {"http": 400, "message": "Invalid request body", "resolution": "Check schema"},
        "E002": {"http": 401, "message": "Authentication required", "resolution": "Verify API key"},
    }

    def generate_table(self) -> str:
        lines = ["| Code | HTTP | Meaning | Resolution |", "|------|------|---------|------------|"]
        for code, info in sorted(self.errors.items()):
            lines.append(f"| {code} | {info['http']} | {info['message']} | {info['resolution']} |")
        return "\n".join(lines)
```

---

## 12. No Index or Search

### Symptom

Documentation is hundreds of pages with no navigation. Users cannot find what they need.

### Root Causes

- No table of contents in long documents.
- No sidebar navigation in docs site.
- No search functionality implemented.
- Related content not linked.

### Solutions

#### Immediate Fix

1. Add a table of contents to every document over 500 lines.
2. Create an index page with topics and use cases.
3. Implement full-text search in the docs site.
4. Add "Related" sections to each page.

#### Index Template

```markdown
# Documentation Index

## By Topic

- [LLM Integration](./concepts/llm.md)
- [Tool Use](./concepts/tools.md)
- [Memory](./concepts/memory.md)
- [Streaming](./concepts/streaming.md)
- [Authentication](./api/auth.md)

## By Use Case

- [Getting Started](./getting-started.md)
- [Deploy to Production](./guides/deployment.md)
- [Monitoring and Alerts](./operations/monitoring.md)
- [Troubleshooting](./operations/troubleshooting.md)

## By Audience

- [For Developers](./audience/developers.md)
- [For Operators](./audience/operators.md)
- [For End Users](./audience/users.md)
```

#### Long-term Prevention

- **MkDocs/Docusaurus navigation**: Configure sidebar automatically from directory structure.
- **Search index**: Maintain a search index updated on every doc build.
- **Related content**: Auto-suggest related pages based on tags.

---

## 13. Code and Docs Out of Sync

### Symptom

- Documentation says: `POST /agent/process`
- Code has: `POST /agent/execute`
- Documentation says: `session_id` is optional
- Code raises `ValueError` if `session_id` is missing

### Root Causes

- No single source of truth.
- Docs and code maintained separately.
- No automation to sync them.

### Solutions

#### Immediate Fix

1. Reconcile all mismatches.
2. Decide on a source of truth (code should drive API docs).
3. Update all cross-references.

#### Long-term Prevention

- **Docs from code**: Generate API reference from source code using decorators, docstrings, or OpenAPI annotations.
- **Doc tests**: Run tests that verify doc examples against actual API behavior.
- **Code review gate**: Require doc updates in same PR as code changes.

```python
# Auto-generate endpoint docs from Flask routes
class FlaskDocGenerator:
    def generate(self, app):
        docs = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue
            docs.append(f"## {rule.methods} {rule.rule}")
            docs.append(rule.doc or "No description.")
        return "\n".join(docs)
```

---

## 14. No Feedback Mechanism

### Symptom

Documentation authors have no idea if docs are helpful. Users silently struggle or work around poor docs.

### Root Causes

- No feedback collection built into docs site.
- No channel for doc issues.
- Feedback not acted upon.

### Solutions

#### Immediate Fix

1. Add feedback widget to every doc page.
2. Create a Slack channel or issue tracker for doc feedback.
3. Acknowledge and act on feedback within a week.

#### Feedback Widget

```markdown
## Was this page helpful?

- [Yes] [No] [Submit feedback]

Feedback goes to #docs-feedback on Slack.
```

#### Feedback Collection API

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/doc-feedback")
async def doc_feedback(request: Request):
    data = await request.json()
    store_feedback(data["path"], data["rating"], data["comment"])
    return {"status": "ok"}
```

#### Long-term Prevention

- **Feedback review cadence**: Review feedback weekly, prioritize fixes.
- **Doc issue template**: Use GitHub issue template for doc problems.
- **Metrics**: Track feedback volume and sentiment over time.

---

## 15. No Maintenance Schedule

### Symptom

Documentation written once and never updated. After a year it is completely wrong.

### Root Causes

- No review schedule defined.
- No ownership assigned.
- No process for update triggers (e.g., after incidents, releases).

### Solutions

#### Immediate Fix

1. Assign an owner to every document.
2. Create a review calendar.
3. Set calendar reminders for reviews.

#### Review Calendar

| Document Type | Review Interval | Trigger |
|---------------|-----------------|---------|
| API Reference | Every release | New version |
| Runbooks | Quarterly | Calendar |
| Architecture | Semi-annually | Calendar |
| Prompt Cards | Per change | PR merge |
| Getting Started | Annually | Calendar |
| Compliance | Annually | Audit |

#### Long-term Prevention

- **Last verified date**: Include `Last Verified: YYYY-MM-DD` in every doc.
- **Stale doc alerts**: Automated alerts for docs not reviewed in 90 days.
- **Post-change updates**: Deployment scripts include doc update checklist.

```python
class DocMaintenanceSchedule:
    def __init__(self):
        self.intervals = {
            "api_reference": timedelta(days=30),
            "runbook": timedelta(days=90),
            "architecture": timedelta(days=180),
            "getting_started": timedelta(days=365),
            "compliance": timedelta(days=365),
        }

    def get_next_review(self, doc_type: str, last_reviewed: str) -> str:
        last = datetime.fromisoformat(last_reviewed)
        interval = self.intervals.get(doc_type, timedelta(days=90))
        return (last + interval).date().isoformat()

    def is_due(self, doc_type: str, last_reviewed: str) -> bool:
        return datetime.now().date() >= datetime.fromisoformat(
            self.get_next_review(doc_type, last_reviewed)
        ).date()
```

---

## 16. Undocumented Assumptions

### Symptom

Code or documentation makes assumptions that are not stated. Users hit unexpected behavior:
- Code assumes US locale for date formatting.
- Function assumes model is always available.
- Doc says "fast" but does not quantify what fast means.

### Root Causes

- Assumptions made during design and forgotten.
- Author assumed audience would share context.
- No review by someone outside the immediate team.

### Solutions

#### Immediate Fix

1. Identify assumptions in docs and code.
2. Document each assumption explicitly.
3. Use a standard Assumptions section in templates.

#### Template

```markdown
## Assumptions

- User is in US Eastern timezone.
- Database is PostgreSQL 14+ with pgvector extension.
- Model `gpt-4-turbo` is available in the deployment region.
- Session IDs are UUID v4 format.
- API key has `agent:execute` scope.
```

#### Long-term Prevention

- **Code review checklist**: Include "are all assumptions documented?" in review.
- **Doc template**: Mandatory Assumptions section.
- **Testing**: Test from perspective of users who do not share assumptions.

---

## 17. No Quick-Start Guide

### Symptom

Documentation jumps straight into advanced topics. New users must read 50 pages before running anything.

### Root Causes

- Team assumed users were already familiar.
- Quick start was deprioritized.
- "Comprehensive docs" prioritized over progressive disclosure.

### Solutions

#### Immediate Fix

1. Create a 5-minute quick start guide.
2. Ensure it is the first thing users see in the README.
3. Link to detailed docs from the quick start.

#### Quick Start Template

```markdown
# Quick Start

Get an agent running in 5 minutes.

## Prerequisites

- Python 3.11+
- pip

## Step 1: Install

```bash
pip install agent-framework
```

## Step 2: Run

```python
from agent import Agent

agent = Agent()
response = agent.run("What is 2+2?")
print(response)
```

## Step 3: Next Steps

- [Full Tutorial](./tutorials/full.md)
- [API Reference](./api/overview.md)
- [Deployment Guide](./guides/deployment.md)
```

---

## 18. Missing Change Log

### Symptom

Users discover breaking changes only after upgrading. They have no idea what changed or why.

### Root Causes

- No changelog maintained.
- Changes merged without documentation updates.
- No culture of documenting changes.

### Solutions

#### Immediate Fix

1. Start a CHANGELOG.md following Keep a Changelog format.
2. Document the most recent release.
3. Backfill major changes from previous versions.

#### Template

```markdown
# Changelog

All notable changes are documented here.

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Fixed
- Fix description

## [1.2.0] - 2024-01-15

### Added
- Feature 1

### Changed
- Change 1

### Fixed
- Fix 1

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
```

#### Long-term Prevention

- **Release drafter**: GitHub action to auto-generate changelog from PR labels.
- **Semantic release**: Auto-version and release based on conventional commits.
- **PR requirement**: Changes without CHANGELOG entries are blocked.

---

## 19. Unassigned Ownership

### Symptom

No one is responsible for keeping documentation accurate. Docs drift, and no one fixes them.

### Root Causes

- Docs owned by "the team" - i.e., no one.
- Ownership not established when docs were created.
- No accountability mechanism.

### Solutions

#### Immediate Fix

1. Assign a primary owner to every document.
2. Create a registry of doc owners.
3. Set review intervals.

#### Owner Registry

```markdown
# Documentation Ownership Registry

| Document | Owner | Review Date | Next Review |
|----------|-------|-------------|-------------|
| API Reference | @team-api | 2024-01-15 | 2024-04-15 |
| Runbooks | @team-ops | 2024-01-15 | 2024-04-15 |
| Architecture | @team-arch | 2024-01-15 | 2024-07-15 |
| Getting Started | @team-docs | 2024-01-15 | 2025-01-15 |
```

#### Long-term Prevention

- **Ownership check**: PRs touching docs without owner tag are flagged.
- **Review reminders**: Automated reminders 2 weeks before review date.
- **Stale doc alerts**: Alerts when docs exceed review interval without update.

```python
class DocOwnershipRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, path: str, owner: str, review_days: int = 90):
        self.registry[path] = {
            "owner": owner,
            "review_days": review_days,
            "last_reviewed": datetime.utcnow().isoformat()
        }

    def get_owner(self, path: str) -> str:
        return self.registry.get(path, {}).get("owner", "unassigned")

    def get_stale(self, threshold_days: int = 90) -> list:
        stale = []
        cutoff = datetime.utcnow() - timedelta(days=threshold_days)
        for path, meta in self.registry.items():
            last = datetime.fromisoformat(meta["last_reviewed"])
            if last < cutoff:
                stale.append(path)
        return stale
```

---

## 20. Accessibility Issues

### Symptom

Documentation is difficult or impossible to use for people with disabilities:
- Images lack alt text.
- Color contrast is too low.
- Documents are not navigable via keyboard.
- Heading hierarchy is broken.

### Root Causes

- Accessibility was not a requirement.
- No accessibility testing performed.
- Authors focused on content only.

### Solutions

#### Immediate Fix

1. Add alt text to all images.
2. Fix heading hierarchy (no skipped levels).
3. Ensure color contrast meets WCAG AA (4.5:1 for text).

#### Automated Checks

```bash
# Use axe-cli or pa11y
pa11y https://docs.example.com

# Use WAVE
https://wave.webaim.org/
```

#### Alt Text Template

```markdown
<!-- Good -->
![Agent sequence diagram showing user request flowing through API
to agent orchestrator, then to LLM and tool service before returning 
a response to the user.](./diagrams/agent-flow.png)

<!-- Bad -->
![Agent flow](./diagrams/agent-flow.png)
```

---

## 21. Broken Internal Links

### Symptom

Users click links in documentation and get 404 errors.

### Root Causes

- Documents moved or renamed without updating links.
- Typos in relative paths.
- Files deleted but links remain.

### Solutions

#### Immediate Fix

1. Run a link checker across all documentation.
2. Fix or redirect broken links.
3. Add 404 handling to docs site.

#### Automated Link Checking

```bash
# Using markdown-link-check
npx markdown-link-check docs/**/*.md

# Using Python
python scripts/check_links.py docs/
```

```python
import requests
from pathlib import Path
import re

class LinkChecker:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)

    def check(self) -> list:
        broken = []
        for md in self.docs_dir.rglob("*.md"):
            content = md.read_text()
            for match in re.finditer(r'\[.*?\]\((.*?)\)', content):
                url = match.group(1)
                if url.startswith("http"):
                    try:
                        resp = requests.head(url, timeout=5, allow_redirects=True)
                        if resp.status_code >= 400:
                            broken.append((str(md), url, resp.status_code))
                    except Exception as e:
                        broken.append((str(md), url, str(e)))
                else:
                    target = (md.parent / url).resolve()
                    if not target.exists():
                        broken.append((str(md), url, "file not found"))
        return broken
```

#### Long-term Prevention

- **CI integration**: Fail build if broken links are found.
- **Redirect map**: Maintain redirects for moved documents.
- **Link naming convention**: Use stable link slugs (kebab-case).

---

## 22. Outdated Diagrams

### Symptom

Diagrams in documentation do not match current architecture:
- Services shown that no longer exist.
- Missing new services.
- Data flow paths are wrong.

### Root Causes

- Architecture changed but diagrams not updated.
- Diagram source files not in version control.
- No review process for diagrams.

### Solutions

#### Immediate Fix

1. Update diagrams to reflect current architecture.
2. Store diagram source (Mermaid, PlantUML, DOT) in version control.
3. Add diagrams to review checklist.

#### Long-term Prevention

- **Render in CI**: Validate that all diagram source files render without errors.
- **Architecture review**: Update diagrams as part of architectural change process.
- **Diagram standards**: Define style guide for colors, naming, layout.

```bash
# Verify Mermaid diagrams
npx @mermaid-js/mermaid-cli docs/**/*.mmd

# Verify PlantUML
java -jar plantuml.jar docs/diagrams/*.puml
```

---

## 23. Compliance Documentation Gaps

### Symptom

During an audit, required documentation is missing or outdated:
- No data processing agreement.
- No audit evidence.
- No privacy notice.

### Root Causes

- Compliance not prioritized by engineering team.
- Legal/compliance not looped into doc process.
- Compliance docs treated as separate from product docs.

### Solutions

#### Immediate Fix

1. Identify all compliance requirements (SOC2, GDPR, HIPAA, PCI-DSS).
2. Create or update compliance documentation.
3. Schedule regular compliance reviews.

#### Compliance Checklist

```markdown
# Compliance Documentation Audit

## SOC 2
- [ ] System description documented
- [ ] Control objectives listed
- [ ] Control activities described
- [ ] Evidence collection automated

## GDPR
- [ ] Data processing records (Art. 30)
- [ ] Data protection impact assessment
- [ ] Privacy notices for users
- [ ] Data retention policies

## HIPAA
- [ ] BAA signed with all PHI processors
- [ ] Access controls documented
- [ ] Audit trail for ePHI access
```

---

## 24. Performance Documentation Gaps

### Symptom

Users do not know what performance to expect:
- No latency targets documented.
- No throughput limits mentioned.
- No SLOs defined.

### Root Causes

- Performance not measured or tracked.
- Performance targets not agreed upon.
- Performance docs omitted during writing.

### Solutions

#### Immediate Fix

1. Document performance characteristics for all API endpoints.
2. Define SLOs for availability, latency, and error rate.
3. Link to performance dashboards.

#### Performance Section Template

```markdown
## Performance

### Latency

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| POST /agent/execute | 1.2s | 3.5s | 8.1s |
| GET /sessions/{id} | 50ms | 100ms | 200ms |

### Throughput

- Requests per second: 100 (standard tier), 1000 (enterprise tier)
- Tokens per minute: 100K (standard tier), 1M (enterprise tier)

### SLOs

- Availability: 99.9% over 30 days
- Error rate: <0.1%
- Latency p99: <10s
```

---

## 25. Diagram Rendering Failures

### Symptom

Diagrams appear as raw code blocks instead of rendered graphics:
- Mermaid shows ` ```mermaid ` text.
- PlantUML images are broken.
- Image paths are incorrect.

### Root Causes

- Docs site not configured for diagrams.
- Mermaid/PlantUML plugins missing.
- Image paths relative to wrong directory.
- Diagrams use unsupported syntax.

### Solutions

#### Immediate Fix

1. Verify docs site configuration for renderers.
2. Fix image paths (use relative paths from markdown file).
3. Validate diagram syntax against renderer version.

#### MkDocs Configuration

```yaml
# mkdocs.yml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.details

plugins:
  - mermaid2
```

#### Docusaurus Configuration

```javascript
// docusaurus.config.js
module.exports = {
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};
```

---

## 26. Search Optimization Issues

### Symptom

Users cannot find information using the docs search:
- Search returns no results for common terms.
- Search results are not ranked by relevance.
- Search does not index all docs.

### Root Causes

- Search index not built or not updated.
- Search does not stem words or handle synonyms.
- Search only indexes titles, not content.

### Solutions

#### Immediate Fix

1. Rebuild search index.
2. Include content in search index, not just titles.
3. Test common queries to verify results.

#### Long-term Prevention

- **Reindex on build**: Search index rebuilt every time docs are deployed.
- **Analytics**: Track search queries and no-result queries.
- **Synonyms**: Add synonyms for domain-specific terms.

```python
class DocSearch:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.index = self._build_index()

    def _build_index(self) -> dict:
        index = {}
        for md in self.docs_dir.rglob("*.md"):
            content = md.read_text().lower()
            words = re.findall(r'\b[a-z0-9]+\b', content)
            for word in words:
                if len(word) > 2:
                    index.setdefault(word, set()).add(str(md))
        return index

    def search(self, query: str, limit: int = 10) -> list:
        words = set(re.findall(r'\b[a-z0-9]+\b', query.lower()))
        scores = defaultdict(int)
        for word in words:
            for doc in self.index.get(word, []):
                scores[doc] += 1
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
```

---

## 27. Localization and Translation Gaps

### Symptom

Documentation is only in English. International users cannot use it. Translated docs are incomplete or inconsistent.

### Root Causes

- Localization not prioritized.
- Translation process not defined.
- No budget for professional translation.

### Solutions

#### Immediate Fix

1. Identify priority docs for translation.
2. Use machine translation for initial pass with human review.
3. Flag English-only docs with a banner.

#### Long-term Prevention

- **i18n framework**: Use gettext or similar for docs.
- **Translation workflow**: PO files, review process, CI validation.
- **Locale routing**: Serve docs at `/docs/en/`, `/docs/es/`, etc.

```po
# translations/docs/locale/es/LC_MESSAGES/messages.po
msgid "Getting Started"
msgstr "Primeros Pasos"

msgid "API Reference"
msgstr "Referencia de API"

msgid "Documentation"
msgstr "Documentación"
```

---

## 28. Onboarding Documentation Gaps

### Symptom

New team members take weeks to become productive because documentation is:
- Missing setup instructions.
- Not structured for progressive learning.
- Lacking hands-on exercises.

### Root Causes

- No onboarding doc process.
- Existing team members forgot what it was like to be new.
- Onboarding not prioritized.

### Solutions

#### Immediate Fix

1. Create a getting started path for day 1, week 1, month 1.
2. Include hands-on exercises with expected outcomes.
3. Assign a mentor to review onboarding docs quarterly.

#### Onboarding Path Template

```markdown
# Onboarding: New Engineer

## Day 1

1. Read [Architecture Overview](../architecture/overview.md).
2. Set up local environment per [Setup](./setup.md).
3. Run first agent per [Quickstart](./quickstart.md).
4. Join #agent-platform Slack channel.

## Week 1

- Read [API Reference](../api/overview.md).
- Shadow on-call engineer.
- Submit first documentation PR.
- Attend architecture review.

## Month 1

- Own one runbook improvement.
- Write one prompt card.
- Present architecture overview.
```

---

## 29. Appendix: Troubleshooting Toolkit

### Quick Diagnostic Commands

```bash
# Check docs build
mkdocs build --strict

# Check markdown
markdownlint docs/**/*.md

# Check links
markdown-link-check docs/**/*.md

# Check spelling
codespell docs/

# Check accessibility
axe-cli https://docs.example.com

# Generate doc coverage
python scripts/doc_coverage.py

# Verify examples
python scripts/test_examples.py

# Check Mermaid diagrams
mmdc -i docs/**/*.mmd -o /dev/null

# Check PlantUML
java -jar plantuml.jar docs/**/*.puml -failfast2

# Rebuild search index
python scripts/build_search_index.py docs/
```

### Common Issues Quick Reference

| Issue | Symptom | Fix |
|-------|---------|-----|
| Docs site won't build | Build fails | Check markdown syntax, run `mkdocs build --strict` |
| Diagrams not rendering | Raw code blocks visible | Install mermaid/plantuml plugin |
| Search not working | No results | Rebuild search index, check configuration |
| Links broken | 404 errors | Run link checker, update paths |
| Stale content | Users complain | Assign owner, set review schedule |
| No examples | Users confused | Add at least one example per major feature |
| Runbooks outdated | Commands fail | Test commands in staging quarterly |
| Missing prompt docs | Prompts in code only | Create prompt card template, enforce in PR |
| API docs incomplete | Missing parameters | Generate from code, add to OpenAPI spec |
| Compliance gaps | Audit findings | Create compliance checklist, assign owner |

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Checklist](./checklist.md)
