# Agent Catalog

## Overview

The framework defines specialized agents that operate across the AI system lifecycle.

## Core Agents

### Rules Architect Agent
- **Role**: Design AI, LLM, agentic, RAG, MCP, and coding-agent systems
- **Phase**: Design
- **Outputs**: Domain map, ADRs, implementation plan, release checklist

### Rules Implementer Agent
- **Role**: Implement system changes according to architecture decisions
- **Phase**: Implementation
- **Outputs**: Code, prompts, tools, tests, documentation

### Rules Reviewer Agent
- **Role**: Review code, prompts, tools, tests, and documentation
- **Phase**: Review
- **Outputs**: Findings, release recommendation, remediation guidance

### Rules Release Gate Agent
- **Role**: Decide whether system is ready to release
- **Phase**: Release
- **Outputs**: Release decision, blocking items, exception tracking

### Rules Eval Agent
- **Role**: Run and interpret evaluation suites
- **Phase**: Evaluation
- **Outputs**: Evaluation reports, regression detection, threshold enforcement

### Rules Compliance Auditor Agent
- **Role**: Assemble and validate compliance evidence
- **Phase**: Compliance
- **Outputs**: Evidence packages, audit readiness, exception management

### Rules Data Steward Agent
- **Role**: Own data governance, privacy, quality, retention
- **Phase**: Data Governance
- **Outputs**: Data policies, inventory, retention enforcement

### Rules Enforcer Agent
- **Role**: Enforce policy rules and detect violations
- **Phase**: Enforcement
- **Outputs**: Policy enforcement, violation detection, compliance monitoring

### Rules Documentation Agent
- **Role**: Maintain documentation standards and knowledge sharing
- **Phase**: Documentation
- **Outputs**: System docs, model cards, runbooks, registers

### Rules Tracker Agent
- **Role**: Track metrics, monitoring, and operational health
- **Phase**: Operations
- **Outputs**: Metrics, dashboards, alerts, operational reports

## Agent Interaction Flow

```
Rules Architect -> Rules Implementer -> Rules Reviewer -> Rules Release Gate
       |                    |                  |                  |
       v                    v                  v                  v
  Rules Eval        Rules Data Steward   Rules Compliance    Rules Tracker
                                              Auditor
```

## Lifecycle Coverage

| Phase | Primary Agent | Supporting Agents |
|-------|---------------|-------------------|
| Design | Architect | Eval, Compliance, Data Steward |
| Implement | Implementer | Documentation, Data Steward |
| Review | Reviewer | Eval, Compliance |
| Release | Release Gate | Compliance, Tracker |
| Operate | Tracker | Enforcer, Documentation |
