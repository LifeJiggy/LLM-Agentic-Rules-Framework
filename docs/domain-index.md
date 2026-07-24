# Domain Index

## Overview

This index helps teams find the right rule file for a specific task.

## By Work Type

| Work Type | Start Here | Supporting Domains |
|-----------|------------|--------------------|
| New AI product design | `01-core/fundamentals.md` | Security, Data, Testing, Compliance |
| Prompt or agent change | `01-core/best-practices.md` | Testing, Security, Compliance |
| Tool integration | `05-integration/fundamentals.md` | Security, Operations, Testing |
| RAG pipeline | `04-data/fundamentals.md` | Security, Testing, Performance |
| Production release | `06-operations/checklist.md` | Testing, Security, Compliance |
| Latency or cost review | `09-performance/checklist.md` | Operations, Data, Integration |
| Compliance review | `10-compliance/checklist.md` | Security, Data, Documentation |
| Incident response | `incident-response/incident-response-fundamentals.md` | Operations, Security, Testing |
| Deployment | `deployment/deployment-fundamentals.md` | Operations, Testing, Monitoring |
| Monitoring | `monitoring/monitoring-fundamentals.md` | Operations, Performance |
| Cost optimization | `cost-management/cost-management-fundamentals.md` | Performance, Operations |
| Vendor assessment | `vendor-management/vendor-management-fundamentals.md` | Security, Compliance |
| Governance | `governance/governance-fundamentals.md` | Compliance, Security |
| Evaluation | `evaluation/evaluation-fundamentals.md` | Testing, Security |
| Agent loops | `loop/loop-fundamentals.md` | Core, Tools |
| Tool integration | `tools/tools-fundamentals.md` | Integration, Security |

## By Reader

| Reader | Most Useful Files |
|--------|-------------------|
| AI/ML engineer | Core fundamentals, Evaluation best practices, Loop patterns |
| Software engineer | Development best practices, Tools examples, Testing checklist |
| DevOps engineer | Deployment checklist, Monitoring setup, Operations troubleshooting |
| Security reviewer | Security checklist, Security anti-patterns, Incident response |
| Technical lead | Core advanced, Architecture templates, Governance checklist |
| Compliance reviewer | Compliance fundamentals, Governance checklist, Evidence templates |
| Product manager | Evaluation workflows, Cost management, Vendor assessment |
| Data engineer | Data fundamentals, Data steward rules, Monitoring setup |

## By System Type

### Production User-Facing Assistant

```mermaid
flowchart LR
    A[Start] --> B[Core Fundamentals]
    B --> C[Security Checklist]
    C --> D[Data Checklist]
    D --> E[Testing Checklist]
    E --> F[Operations Checklist]
    F --> G[Compliance Checklist]
    G --> H[Ready for Production]
```

1. `domains/01-core/fundamentals.md`
2. `domains/02-security/checklist.md`
3. `domains/04-data/checklist.md`
4. `domains/07-testing/checklist.md`
5. `domains/06-operations/checklist.md`
6. `domains/10-compliance/checklist.md`
7. `evaluation/evaluation-checklist.md`
8. `incident-response/incident-response-checklist.md`

### Internal Agentic Automation

```mermaid
flowchart LR
    A[Start] --> B[Core Fundamentals]
    B --> C[Integration Best Practices]
    C --> D[Security Best Practices]
    D --> E[Operations Troubleshooting]
    E --> F[Testing Best Practices]
    F --> G[Ready for Use]
```

1. `domains/01-core/fundamentals.md`
2. `domains/05-integration/best-practices.md`
3. `domains/02-security/best-practices.md`
4. `domains/06-operations/troubleshooting.md`
5. `domains/07-testing/best-practices.md`
6. `loop/loop-fundamentals.md`
7. `tools/tools-fundamentals.md`

### High-Volume AI API

```mermaid
flowchart LR
    A[Start] --> B[Core Best Practices]
    B --> C[Integration Checklist]
    C --> D[Performance Checklist]
    D --> E[Operations Checklist]
    E --> F[Testing Advanced]
    F --> G[Ready for Scale]
```

1. `domains/01-core/best-practices.md`
2. `domains/05-integration/checklist.md`
3. `domains/09-performance/checklist.md`
4. `domains/06-operations/checklist.md`
5. `domains/07-testing/advanced.md`
6. `cost-management/cost-management-checklist.md`
7. `monitoring/monitoring-checklist.md`

### Enterprise AI Platform

```mermaid
flowchart LR
    A[Start] --> B[All Domains]
    B --> C[All Modules]
    C --> D[All Agents]
    D --> E[Ready for Enterprise]
```

1. All 10 core domains
2. All 9 operational modules
3. All 12 agent definitions
4. Governance framework
5. Vendor management
6. Compliance evidence

## Baseline Reading Paths

### Quick Start (1 hour)

1. `domains/01-core/fundamentals.md` - Core concepts
2. `evaluation/evaluation-fundamentals.md` - Evaluation basics
3. `incident-response/incident-response-fundamentals.md` - Incident response

### Comprehensive (1 day)

1. All core domain fundamentals (10 files)
2. All module fundamentals (9 files)
3. Agent overview (12 files)

### Expert (1 week)

1. All domain files (70 files)
2. All module files (63 files)
3. All agent files (12 files)
4. All skill files (9 files)
5. Memory and storage resources (20 files)
