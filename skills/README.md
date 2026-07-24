# Skills Domain

## Overview

The Skills domain contains specialized skills for implementing LLM and agentic system patterns.

## Architecture

```mermaid
flowchart TD
    A[Skills] --> B[LLM Agentic Rules]
    A --> C[System]
    
    B --> B1[Evaluation Workflows]
    B --> B2[Loop Patterns]
    B --> B3[Domain Routing]
    B --> B4[Review Gates]
    B --> B5[Compliance Evidence]
    
    C --> C1[Tool Integration]
    C --> C2[Performance Optimization]
    C --> C3[Deployment Safety]
    C --> C4[Observability]
    C --> C5[Recovery]
```

## Skills Overview

```mermaid
flowchart LR
    A[Skills] --> B[LLM Agentic Rules]
    A --> C[System]
    
    B --> B1[Domain-Specific Skills]
    B --> B2[Workflow Skills]
    B --> B3[Pattern Skills]
    
    C --> C1[Integration Skills]
    C --> C2[Operations Skills]
    C --> C3[Performance Skills]
```

## Folders

| Folder | Purpose |
|--------|---------|
| llm-agentic-rules/ | Domain-specific skills for LLM and agentic systems |
| system/ | System-level skills for operations and performance |

## Quick Start

1. Browse `llm-agentic-rules/` for domain-specific guidance
2. Browse `system/` for operational guidance
3. Reference individual skill files for detailed patterns
