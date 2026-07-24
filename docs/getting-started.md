# Getting Started

## Overview

This guide helps you get started with the LLM & Agentic Rules Framework.

## Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/Lifejiggy/llm-agentic-rules-framework.git
cd llm-agentic-rules-framework
```

### Step 2: Read Core Fundamentals

```bash
less domains/01-core/fundamentals.md
less domains/01-core/checklist.md
```

### Step 3: Select Domains Based on Risk

| System Type | Required Domains | Recommended Domains |
|-------------|-----------------|---------------------|
| Production user-facing assistant | Core, Security, Data, Testing, Operations, Compliance | Documentation, Performance |
| Internal agent automation | Core, Development, Integration, Operations, Testing | Documentation |
| High-volume AI API | Core, Integration, Performance, Operations, Testing | Security, Compliance |
| Healthcare AI system | All 10 domains | - |
| Financial AI system | All 10 domains | - |

### Step 4: Copy Checklists

Copy relevant checklists into your project review process.

## Framework Architecture

```mermaid
flowchart TD
    A[Framework] --> B[10 Core Domains]
    A --> C[9 Operational Modules]
    A --> D[12 Agents]
    A --> E[9 Skills]
    A --> F[20 Memory/Storage Files]
    
    B --> B1[70 Rule Files]
    C --> C2[63 Module Files]
    D --> D3[12 Agent Definitions]
    E --> E4[9 Skill Files]
    F --> F5[20 Reference Files]
```

## Domain Selection

```mermaid
flowchart TD
    A[System Assessment] --> B{Risk Tier?}
    B -->|Low| C[Core + Testing]
    B -->|Medium| D[Core + Security + Data + Testing + Operations]
    B -->|High| E[All 10 Domains]
    B -->|Critical| F[All Domains + All Modules]
    
    C --> G[Basic controls]
    D --> H[Standard controls]
    E --> I[Enhanced controls]
    F --> J[Maximum controls]
```

## Module Selection

```mermaid
flowchart TD
    A[System Needs] --> B{What do you need?}
    B -->|AI Evaluation| C[Evaluation Module]
    B -->|Agent Loops| D[Loop Module]
    B -->|Tool Integration| E[Tools Module]
    B -->|Incident Handling| F[Incident Response Module]
    B -->|Deployment| G[Deployment Module]
    B -->|Monitoring| H[Monitoring Module]
    B -->|Cost Control| I[Cost Management Module]
    B -->|Vendor Risk| J[Vendor Management Module]
    B -->|Governance| K[Governance Module]
```

## Agent Selection

```mermaid
flowchart TD
    A[Workflow Phase] --> B{Which phase?}
    B -->|Design| C[Rules Architect]
    B -->|Implement| D[Rules Implementer]
    B -->|Review| E[Rules Reviewer]
    B -->|Release| F[Rules Release Gate]
    B -->|Evaluate| G[Rules Eval]
    B -->|Monitor| H[Rules Tracker]
    B -->|Enforce| I[Rules Enforcer]
    B -->|Govern| J[Rules Compliance Auditor]
```

## Reading Paths

### Quick Start (1 hour)

1. Core fundamentals
2. Evaluation fundamentals
3. Incident response fundamentals

### Comprehensive (1 day)

1. All core domain fundamentals
2. All module fundamentals
3. Agent overview

### Expert (1 week)

1. All domain files
2. All module files
3. All agent files
4. All skill files

## Next Steps

1. Read the [Domain Index](./domain-index.md) for specific guidance
2. Review the [Domain Knowledge Map](./domain-knowledge-map.md) for visual overview
3. Explore the [Adoption Playbook](./adoption-playbook.md) for implementation steps
4. Check the [Glossary](./glossary.md) for key terms
