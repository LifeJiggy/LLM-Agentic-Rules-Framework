# LLM & Agentic Rules Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0-blue.svg)](#roadmap)
[![Domains](https://img.shields.io/badge/Domains-10-green.svg)](#domains)
[![Rule Files](https://img.shields.io/badge/Rule%20Files-70%2B-orange.svg)](#rule-categories)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](./CONTRIBUTING.md)

> A production-grade rules framework for building LLM chatbots, agentic systems, and AI-powered applications.

## Table of Contents

- [Overview](#overview)
- [Purpose](#purpose)
- [Target Audience](#target-audience)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Domains](#domains)
- [Domain Structure](#domain-structure)
- [Quick Start](#quick-start)
- [Rule Categories](#rule-categories)
- [Usage Examples](#usage-examples)
- [Integration Guide](#integration-guide)
- [Feature Standards](#feature-standards)
- [Repository Quality Checks](#repository-quality-checks)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [FAQ](#faq)

## Overview

The **LLM & Agentic Rules Framework** is a structured collection of rules, practices, examples, and checklists for teams building robust, secure, maintainable, and auditable AI systems. It is designed as a reference for real delivery work: architecture reviews, implementation, code review, testing, deployment, incident response, and governance.

The framework covers 10 domains with a consistent 7-file structure in each domain. This makes it easy for teams to find the right depth of guidance, from fundamentals through advanced production concerns.

## Purpose

This project helps teams convert broad AI engineering concerns into repeatable operating standards.

| Area | What This Framework Provides |
|------|-------------------------------|
| Standardized rules | Consistent guidance that can be reused across projects and teams |
| Best practices | Recommended patterns for production LLM and agentic systems |
| Anti-patterns | Common failure modes and safer alternatives |
| Checklists | Release, review, onboarding, and audit verification steps |
| Examples | Implementation patterns for prompts, tools, APIs, testing, and operations |
| Troubleshooting | Practical symptoms, causes, and remediation steps |
| Advanced topics | Scaling, governance, performance, safety, and cross-domain tradeoffs |

## Target Audience

This framework is written for:

- AI and ML engineers building LLM-powered applications.
- Software developers integrating AI capabilities into products.
- DevOps and platform engineers deploying AI infrastructure.
- Security professionals reviewing prompt, data, and tool risk.
- Technical leads setting team standards.
- Compliance and governance teams evaluating AI system risk.
- Researchers translating agentic patterns into practical systems.

## Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| 10 comprehensive domains | Covers the major dimensions of LLM and agentic development | Reduces blind spots |
| 7 files per domain | Fundamentals, best practices, anti-patterns, checklist, examples, troubleshooting, advanced | Predictable navigation |
| Production orientation | Focuses on reliability, security, observability, compliance, and operations | Useful beyond prototypes |
| Cross-domain thinking | Connects security, data, testing, performance, and compliance concerns | Better system design |
| Validation tooling | Checks that the repository contract is maintained | Prevents structural drift |
| Contribution guidance | Documents naming, formatting, and review expectations | Easier community input |

## Feature Standards

The README feature promises are backed by concrete project assets:

| Promise | Project Support |
|---------|-----------------|
| Standardized Guidelines | [Framework Quality Standard](./docs/framework-quality-standard.md), [Rule Template](./assets/templates/rule-template.md), validation scripts |
| Domain-Specific Knowledge | [Domain Knowledge Map](./docs/domain-knowledge-map.md), [Domain Index](./docs/domain-index.md), 10 domain folders |
| Actionable Checklists | [Checklist Packs](./docs/checklist-packs.md), domain checklists, checklist export tooling |
| Real-World Examples | [Production Assistant Example](./examples/production-assistant/README.md), [Agentic Automation Example](./examples/agentic-automation/README.md), domain `examples.md` files |
| Continuous Evolution | [Evolution Process](./docs/evolution-process.md), [CHANGELOG.md](./CHANGELOG.md), [ROADMAP.md](./ROADMAP.md) |
| Multi-Agent Distribution | [Agentic CLI Plugin Guide](./docs/agentic-cli-plugin-guide.md), [Adapters](./adapters/README.md), Codex plugin manifest, Claude-style skill and commands |

## Architecture

```text
llm-agentic-rules/
|-- .github/
|   |-- workflows/
|   |   `-- validate-framework.yml
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.md
|   |   |-- feature_request.md
|   |   `-- rule_proposal.md
|   `-- PULL_REQUEST_TEMPLATE.md
|-- .codex-plugin/
|   `-- plugin.json
|-- adapters/
|   |-- README.md
|   |-- manifest.json
|   `-- targets.md
|-- agents/
|   |-- rules-architect.md
|   |-- rules-release-gate.md
|   `-- rules-reviewer.md
|-- commands/
|   |-- rules-audit.md
|   |-- rules-plan.md
|   `-- rules-release.md
|-- assets/
|   `-- templates/
|       |-- architecture-decision-record.md
|       |-- ai-system-register.yml
|       |-- compliance-review.md
|       |-- compliance-evidence-pack.md
|       |-- evaluation-plan.md
|       |-- evaluation-pack-retrieval.md
|       |-- evaluation-pack-safety.md
|       |-- evaluation-pack-tools.md
|       |-- incident-runbook.md
|       |-- model-prompt-change-review.md
|       |-- release-checklist.md
|       `-- rule-template.md
|-- docs/
|   |-- index.md
|   |-- adoption-playbook.md
|   |-- agentic-cli-plugin-guide.md
|   |-- checklist-packs.md
|   |-- getting-started.md
|   |-- advanced-usage.md
|   |-- domain-knowledge-map.md
|   |-- domain-index.md
|   |-- evolution-process.md
|   |-- framework-quality-standard.md
|   |-- glossary.md
|   `-- migration-guide.md
|-- examples/
|   |-- agentic-automation/
|   `-- production-assistant/
|-- domains/
|   |-- 01-core/
|   |-- 02-security/
|   |-- 03-development/
|   |-- 04-data/
|   |-- 05-integration/
|   |-- 06-operations/
|   |-- 07-testing/
|   |-- 08-documentation/
|   |-- 09-performance/
|   `-- 10-compliance/
|-- scripts/
|   |-- check_rules.py
|   |-- install_agent_adapters.py
|   `-- validate-framework.ps1
|-- skills/
|   `-- llm-agentic-rules/
|    -- system/
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- mkdocs.yml
|-- README.md
`-- ROADMAP.md
```

## Domains

| # | Domain | Description | Primary Focus |
|---|--------|-------------|---------------|
| 01 | [Core](./domains/01-core/) | Fundamental rules for all LLM and agentic systems | Architecture, context, tools, state |
| 02 | [Security](./domains/02-security/) | Security-first development and threat prevention | Prompt injection, data protection, access control |
| 03 | [Development](./domains/03-development/) | Software engineering standards for AI systems | Code quality, maintainability, reviews |
| 04 | [Data](./domains/04-data/) | Data handling, retrieval, storage, and governance | Privacy, governance, pipelines |
| 05 | [Integration](./domains/05-integration/) | External services, APIs, tools, and protocols | APIs, webhooks, tool contracts |
| 06 | [Operations](./domains/06-operations/) | Deployment, monitoring, incident response, and reliability | CI/CD, observability, scaling |
| 07 | [Testing](./domains/07-testing/) | Quality assurance and evaluation strategies | Unit, integration, E2E, regression |
| 08 | [Documentation](./domains/08-documentation/) | Documentation standards and knowledge sharing | API docs, runbooks, guides |
| 09 | [Performance](./domains/09-performance/) | Performance, cost, and resource optimization | Latency, throughput, caching |
| 10 | [Compliance](./domains/10-compliance/) | Legal, regulatory, ethical, and audit readiness | Governance, risk controls, review evidence |

## Domain Structure

Each domain contains the same seven rule files:

```text
domain-name/
|-- fundamentals.md
|-- best-practices.md
|-- anti-patterns.md
|-- checklist.md
|-- examples.md
|-- troubleshooting.md
`-- advanced.md
```

| File | Purpose | When To Use |
|------|---------|-------------|
| `fundamentals.md` | Core concepts every practitioner should know | Onboarding and early design |
| `best-practices.md` | Recommended patterns and standards | Design, implementation, review |
| `anti-patterns.md` | Mistakes to avoid and safer alternatives | Risk review and debugging |
| `checklist.md` | Actionable verification steps | PRs, releases, audits |
| `examples.md` | Practical snippets and templates | Implementation and prototyping |
| `troubleshooting.md` | Symptoms, root causes, fixes | Incidents and support |
| `advanced.md` | Complex scenarios and tradeoffs | Scaling and expert review |

## Quick Start

### New Projects

1. Clone the repository.

   ```bash
   git clone https://github.com/Lifejiggy/llm-agentic-rules-framework.git
   cd llm-agentic-rules-framework
   ```

2. Read the core guidance first.

   ```bash
   less domains/01-core/fundamentals.md
   less domains/01-core/checklist.md
   ```

3. Add domains based on your system risk.

   - Production user-facing assistant: core, security, data, testing, operations, compliance.
   - Internal agent automation: core, development, integration, operations, testing.
   - High-volume AI API: core, integration, performance, operations, testing.

4. Copy relevant checklists into your project review process.

### Existing Projects

1. Audit your current implementation against `domains/*/checklist.md`.
2. Start with P0 and P1 security, data, testing, and operations gaps.
3. Use examples and templates to standardize controls.
4. Track exceptions and accepted risks explicitly.

## Rule Categories

| Priority | Meaning | Expected Handling |
|----------|---------|-------------------|
| P0 Critical | Security, safety, compliance, or data-loss risk | Required before production |
| P1 High | Reliability, quality, or maintainability risk | Required unless explicitly accepted |
| P2 Medium | Meaningful quality improvement | Adopt when practical |
| P3 Low | Helpful refinement | Backlog or opportunistic improvement |

## Usage Examples

### CI Structure Check

```yaml
name: Validate Framework
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: ./scripts/validate-framework.ps1
      - run: python scripts/check_rules.py --summary
```

### Project Documentation Reference

```markdown
This project follows the LLM & Agentic Rules Framework:

- Core architecture: domains/01-core/fundamentals.md
- Security controls: domains/02-security/checklist.md
- Evaluation strategy: domains/07-testing/best-practices.md
- Compliance register: assets/templates/ai-system-register.yml
```

### New Team Member Reading Path

```markdown
- [ ] Core fundamentals
- [ ] Security fundamentals
- [ ] Testing checklist
- [ ] Operations troubleshooting
- [ ] Compliance fundamentals
```

## Integration Guide

1. **Assess current state**: identify model, prompt, data, tool, and deployment risks.
2. **Map domains to system scope**: choose the domains that apply to the product.
3. **Adopt checklists gradually**: start with P0 and P1 items.
4. **Add evidence**: keep decisions, evaluations, approvals, and incidents in durable records.
5. **Automate what can be checked**: run repository validation and rule summaries in CI.
6. **Review regularly**: update rules after incidents, model changes, and compliance changes.

## V1 Enhancement Pack

The first enhancement pack adds nine adoption features that make the framework easier to use in real projects:

| # | Feature | Location |
|---|---------|----------|
| 1 | Domain index | [docs/domain-index.md](./docs/domain-index.md) |
| 2 | Glossary | [docs/glossary.md](./docs/glossary.md) |
| 3 | Risk tiering guide | [docs/risk-tiering.md](./docs/risk-tiering.md) |
| 4 | Adoption playbook | [docs/adoption-playbook.md](./docs/adoption-playbook.md) |
| 5 | Release checklist template | [assets/templates/release-checklist.md](./assets/templates/release-checklist.md) |
| 6 | Incident runbook template | [assets/templates/incident-runbook.md](./assets/templates/incident-runbook.md) |
| 7 | Model and prompt change review template | [assets/templates/model-prompt-change-review.md](./assets/templates/model-prompt-change-review.md) |
| 8 | Evaluation plan template | [assets/templates/evaluation-plan.md](./assets/templates/evaluation-plan.md) |
| 9 | Architecture decision record template | [assets/templates/architecture-decision-record.md](./assets/templates/architecture-decision-record.md) |

## Repository Quality Checks

Run the structure validator:

```powershell
./scripts/validate-framework.ps1
```

Run the rule inventory:

```bash
python scripts/check_rules.py --summary
```

Generate roadmap tooling outputs:

```bash
python scripts/check_rules.py \
  --summary \
  --validate-links \
  --json build/rule-report.json \
  --catalog build/rule-catalog.json \
  --coverage build/domain-coverage.md \
  --export-checklists build/checklists.md
```

These checks help confirm that the repository still matches the framework contract: 10 domains, 7 files per domain, supporting docs, templates, automation, catalog output, and checklist exports.

The validators now fail on structural drift that can break adoption in practice: missing files, empty required files, invalid JSON manifests, duplicate framework contract entries, unexpected domain Markdown files, broken local links, broken local anchors, and unsafe report output paths.

## Adapter Installation

Preview all adapter installs:

```bash
python scripts/install_agent_adapters.py --target all --dry-run
```

List supported targets:

```bash
python scripts/install_agent_adapters.py --list-targets
```

Install only one component group:

```bash
python scripts/install_agent_adapters.py --target all --component skill --apply
```

Stage adapters into a review directory:

```bash
python scripts/install_agent_adapters.py --target all --target-root ./adapter-preview --apply
```

Use fail-fast mode for CI or managed rollout:

```bash
python scripts/install_agent_adapters.py --target all --apply --fail-fast
```

The adapter installer validates its source payload, refuses unsafe destination overwrites, skips unchanged files, creates timestamped backups, writes files atomically, counts failures, and returns a non-zero exit code when any copy fails.

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full roadmap.

Current focus:

- Expand production examples for more architectures and stacks.
- Add richer automated validation for quality-standard requirements.
- Keep checklist packs aligned with new domain guidance.
- Use changelog and roadmap updates for continuous evolution.

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting changes.

Useful contribution types:

- new rules for existing domains;
- stronger real-world examples;
- corrections to inaccurate guidance;
- templates for reviews, evaluations, audits, and operations;
- tooling that makes the framework easier to adopt.

## License

This project is licensed under the [MIT License](./LICENSE).

## FAQ

**Q: Which domains should I start with?**  
A: Start with Core. For production systems, add Security, Data, Testing, Operations, and Compliance.

**Q: Can I use only part of the framework?**  
A: Yes. Each domain is designed to be independently useful.

**Q: Are the rules meant to replace engineering judgment?**  
A: No. They create a baseline. Teams should adapt them to system risk, regulation, and business context.

**Q: How should model or prompt changes be handled?**  
A: Treat them as behavior-changing releases. Re-run evaluations, review high-risk workflows, and record the change.
