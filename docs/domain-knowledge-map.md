# Domain Knowledge Map

## Overview

This document provides a visual map of how all framework components connect.

## Framework Overview

```mermaid
flowchart TD
    A[LLM & Agentic Rules Framework] --> B[Core Domains]
    A --> C[Operational Modules]
    A --> D[Agents]
    A --> E[Skills]
    A --> F[Memory & Storage]
    
    B --> B1[01-Core]
    B --> B2[02-Security]
    B --> B3[03-Development]
    B --> B4[04-Data]
    B --> B5[05-Integration]
    B --> B6[06-Operations]
    B --> B7[07-Testing]
    B --> B8[08-Documentation]
    B --> B9[09-Performance]
    B --> B10[10-Compliance]
    
    C --> C1[Evaluation]
    C --> C2[Loop]
    C --> C3[Tools]
    C --> C4[Incident Response]
    C --> C5[Deployment]
    C --> C6[Monitoring]
    C --> C7[Cost Management]
    C --> C8[Vendor Management]
    C --> C9[Governance]
```

## Domain Dependencies

```mermaid
flowchart TD
    A[Core] --> B[Security]
    A --> C[Data]
    A --> D[Integration]
    
    B --> E[Operations]
    C --> E
    D --> E
    
    E --> F[Testing]
    E --> G[Performance]
    
    F --> H[Compliance]
    G --> H
    
    H --> I[Documentation]
    
    J[Evaluation] --> F
    K[Incident Response] --> E
    L[Deployment] --> E
    M[Monitoring] --> E
    N[Governance] --> H
```

## Agent Lifecycle

```mermaid
flowchart LR
    A[Design] --> B[Implement]
    B --> C[Review]
    C --> D[Release]
    D --> E[Operate]
    E --> F[Govern]
    F --> A
    
    A -->|Architect| G[Rules Architect]
    B -->|Implementer| H[Rules Implementer]
    C -->|Reviewer| I[Rules Reviewer]
    D -->|Release Gate| J[Rules Release Gate]
    E -->|Tracker| K[Rules Tracker]
    F -->|Compliance| L[Rules Compliance Auditor]
```

## Cross-Domain Connections

```mermaid
flowchart TD
    subgraph Security
        S1[Prompt Injection]
        S2[Data Protection]
        S3[Access Control]
    end
    
    subgraph Data
        D1[Privacy]
        D2[Governance]
        D3[Quality]
    end
    
    subgraph Testing
        T1[Safety Testing]
        T2[Quality Testing]
        T3[Performance Testing]
    end
    
    subgraph Operations
        O1[Deployment]
        O2[Monitoring]
        O3[Incident Response]
    end
    
    S1 --> T1
    S2 --> D1
    S3 --> O1
    D1 --> T2
    D2 --> O2
    T1 --> O3
    T3 --> O2
```

## Module Integration

```mermaid
flowchart LR
    A[Evaluation] --> B[Testing Domain]
    C[Loop] --> D[Core Domain]
    E[Tools] --> F[Integration Domain]
    G[Incident Response] --> H[Operations Domain]
    I[Deployment] --> J[Operations Domain]
    K[Monitoring] --> L[Operations Domain]
    M[Cost Management] --> N[Performance Domain]
    O[Vendor Management] --> P[Compliance Domain]
    Q[Governance] --> R[Compliance Domain]
```

## Skill Integration

```mermaid
flowchart TD
    A[LLM Agentic Rules Skills] --> B[Evaluation Workflows]
    A --> C[Loop Patterns]
    A --> D[Domain Routing]
    A --> E[Review Gates]
    A --> F[Compliance Evidence]
    
    G[System Skills] --> H[Tool Integration]
    G --> I[Performance Optimization]
    G --> J[Deployment Safety]
    G --> K[Observability]
    G --> L[Recovery]
    
    B --> M[Evaluation Module]
    C --> N[Loop Module]
    D --> O[Core Domains]
    E --> P[Review Process]
    F --> Q[Compliance Module]
    H --> R[Tools Module]
    I --> S[Performance Domain]
    J --> T[Deployment Module]
    K --> U[Monitoring Module]
    L --> V[Incident Response Module]
```

## Risk Assessment Flow

```mermaid
flowchart TD
    A[System Assessment] --> B{Risk Tier?}
    B -->|Low| C[Basic Controls]
    B -->|Medium| D[Standard Controls]
    B -->|High| E[Enhanced Controls]
    B -->|Critical| F[Maximum Controls]
    
    C --> G[Core + Testing]
    D --> G + H[Security + Data + Operations]
    E --> G + H + I[All Domains]
    F --> G + H + I + J[All Domains + Governance]
```

## Compliance Mapping

```mermaid
flowchart TD
    A[Regulatory Requirements] --> B{Regulation?}
    B -->|GDPR| C[Data + Compliance]
    B -->|HIPAA| D[Security + Data + Compliance]
    B -->|SOC 2| E[Security + Operations + Compliance]
    B -->|EU AI Act| F[Core + Compliance + Testing]
    B -->|PCI DSS| G[Security + Data + Compliance]
    
    C --> H[Data Inventory]
    C --> I[Consent Management]
    C --> J[Retention Policies]
    
    D --> K[Encryption]
    D --> L[Audit Logging]
    D --> M[Access Control]
    
    E --> N[Security Controls]
    E --> O[Availability Monitoring]
    E --> P[Confidentiality Measures]
```
