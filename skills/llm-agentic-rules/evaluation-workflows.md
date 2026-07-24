# Evaluation Workflows Skill

## Purpose

This skill provides standardized workflows for evaluating LLM and agentic systems across safety, quality, performance, and compliance dimensions.

## Workflow 1: Pre-Release Evaluation

### Trigger

System is ready for production release.

### Steps

```mermaid
flowchart TD
    A[Release Request] --> B[Load Evaluation Policy]
    B --> C[Select Evaluation Suites]
    C --> D[Execute Safety Evaluation]
    D --> E{Safety Pass?}
    E -->|No| F[Block Release]
    E -->|Yes| G[Execute Quality Evaluation]
    G --> H{Quality Pass?}
    H -->|No| I[Block Release]
    H -->|Yes| J[Execute Performance Evaluation]
    J --> K{Performance Pass?}
    K -->|No| L[Block Release]
    K -->|Yes| M[Execute Regression Evaluation]
    M --> N{Regression Pass?}
    N -->|No| O[Block Release]
    N -->|Yes| P[Generate Evaluation Report]
    P --> Q[Release Decision]
```

### Checklist

- [ ] Evaluation policy loaded
- [ ] Evaluation suites selected
- [ ] Safety evaluation executed
- [ ] Quality evaluation executed
- [ ] Performance evaluation executed
- [ ] Regression evaluation executed
- [ ] Report generated
- [ ] Release decision made

## Workflow 2: Continuous Monitoring

### Trigger

System is in production.

### Steps

```mermaid
flowchart TD
    A[Production Traffic] --> B[Sample Requests]
    B --> C[Safety Monitoring]
    B --> D[Quality Monitoring]
    B --> E[Performance Monitoring]
    C --> F{Safety Issue?}
    F -->|Yes| G[Alert Security Team]
    F -->|No| H[Log Results]
    D --> I{Quality Issue?}
    I -->|Yes| J[Alert ML Team]
    I -->|No| K[Log Results]
    E --> L{Performance Issue?}
    L -->|Yes| M[Alert Operations]
    L -->|No| N[Log Results]
    G --> O[Investigate and Fix]
    J --> O
    M --> O
    H --> P[Update Metrics]
    K --> P
    N --> P
```

### Checklist

- [ ] Sampling configured
- [ ] Safety monitoring active
- [ ] Quality monitoring active
- [ ] Performance monitoring active
- [ ] Alerting configured
- [ ] Metrics collection active
- [ ] Reporting configured

## Workflow 3: Incident Response Evaluation

### Trigger

Production incident detected.

### Steps

```mermaid
flowchart TD
    A[Incident Detected] --> B[Assess Severity]
    B --> C{Safety Incident?}
    C -->|Yes| D[Immediate Safety Evaluation]
    C -->|No| E[Standard Evaluation]
    D --> F[Identify Root Cause]
    E --> F
    F --> G[Implement Fix]
    G --> H[Verify Fix]
    H --> I[Run Regression Evaluation]
    I --> J{Regression Pass?}
    J -->|No| K[Revert Fix]
    J -->|Yes| L[Deploy Fix]
    K --> M[Investigate Further]
    L --> N[Monitor Post-Fix]
    M --> F
```

### Checklist

- [ ] Incident severity assessed
- [ ] Evaluation type selected
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Fix verified
- [ ] Regression evaluated
- [ ] Fix deployed
- [ ] Post-fix monitoring active

## Workflow 4: Model Update Evaluation

### Trigger

Model version updated.

### Steps

```mermaid
flowchart TD
    A[Model Update] --> B[Compare Versions]
    B --> C[Execute Safety Comparison]
    C --> D[Execute Quality Comparison]
    D --> E[Execute Performance Comparison]
    E --> F[Generate Comparison Report]
    F --> G{Degradation Detected?}
    G -->|Yes| H[Block Update]
    G -->|No| I[Approve Update]
    H --> J[Investigate Degradation]
    I --> K[Deploy Update]
    J --> L[Rollback or Fix]
```

### Checklist

- [ ] Model versions documented
- [ ] Comparison baseline established
- [ ] Safety comparison executed
- [ ] Quality comparison executed
- [ ] Performance comparison executed
- [ ] Comparison report generated
- [ ] Update decision made

## Workflow 5: Compliance Evaluation

### Trigger

Compliance audit or regulatory requirement.

### Steps

```mermaid
flowchart TD
    A[Compliance Requirement] --> B[Identify Regulations]
    B --> C[Map to Controls]
    C --> D[Execute Compliance Evaluation]
    D --> E[Generate Evidence]
    E --> F[Validate Evidence]
    F --> G{Compliance Met?}
    G -->|No| H[Remediate Gaps]
    G -->|Yes| I[Archive Evidence]
    H --> J[Re-evaluate]
    J --> G
    I --> K[Update Compliance Register]
```

### Checklist

- [ ] Regulations identified
- [ ] Controls mapped
- [ ] Evaluation executed
- [ ] Evidence generated
- [ ] Evidence validated
- [ ] Compliance status determined
- [ ] Gaps remediated
- [ ] Evidence archived
