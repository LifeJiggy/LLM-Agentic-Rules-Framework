# Agents Domain

## Overview

The Agents domain contains specialized agents for implementing the LLM & Agentic Rules Framework.

## Architecture

```mermaid
flowchart TD
    A[Agents] --> B[Design Phase]
    A --> C[Implementation Phase]
    A --> D[Review Phase]
    A --> E[Release Phase]
    A --> F[Operations Phase]
    A --> G[Governance Phase]
    
    B --> B1[Rules Architect]
    
    C --> C1[Rules Implementer]
    C --> C2[Rules Data Steward]
    
    D --> D1[Rules Reviewer]
    D --> D2[Rules Eval]
    D --> D3[Rules Security]
    
    E --> E1[Rules Release Gate]
    
    F --> F1[Rules Tracker]
    F --> F2[Rules Enforcer]
    F --> F3[Rules Documentation]
    
    G --> G1[Rules Compliance Auditor]
    G --> G2[Rules Orchestrator]
```

## Agent Interactions

```mermaid
flowchart LR
    A[Rules Architect] -->|Design Context| B[Rules Implementer]
    B -->|Implementation| C[Rules Reviewer]
    C -->|Review Findings| D[Rules Release Gate]
    D -->|Release Decision| E[Rules Tracker]
    
    A -->|Security Requirements| F[Rules Security]
    F -->|Security Review| C
    
    A -->|Data Requirements| G[Rules Data Steward]
    G -->|Data Governance| C
    
    C -->|Evaluation Requirements| H[Rules Eval]
    H -->|Evaluation Results| D
    
    D -->|Compliance Evidence| I[Rules Compliance Auditor]
    I -->|Compliance Status| D
    
    E -->|Metrics| J[Rules Tracker]
    J -->|Monitoring| K[Rules Enforcer]
    
    L[Rules Orchestrator] -->|Coordinates| A
    L -->|Coordinates| B
    L -->|Coordinates| C
    L -->|Coordinates| D
```

## Files

| File | Purpose |
|------|---------|
| rules-architect.md | System design and architecture |
| rules-implementer.md | System implementation |
| rules-reviewer.md | Code and artifact review |
| rules-release-gate.md | Release decisions |
| rules-eval.md | Evaluation execution |
| rules-compliance-auditor.md | Compliance evidence |
| rules-data-steward.md | Data governance |
| rules-enforcer.md | Policy enforcement |
| rules-documentation.md | Documentation standards |
| rules-tracker.md | Metrics and monitoring |
| rules-orchestrator.md | Multi-agent coordination |
| rules-security.md | Security controls |

## Quick Start

1. Start with `rules-architect.md` for system design
2. Use `rules-implementer.md` for implementation
3. Reference `rules-reviewer.md` for review process
4. Use `rules-release-gate.md` for release decisions
