# Domain Quick Reference

## Domain Selection Guide

### By System Type

| System Type | Required Domains | Recommended Domains |
|-------------|-----------------|---------------------|
| Customer-facing assistant | Core, Security, Data, Testing, Operations, Compliance | Documentation, Performance |
| Internal agent automation | Core, Development, Integration, Operations, Testing | Documentation |
| High-volume AI API | Core, Integration, Performance, Operations, Testing | Security, Compliance |
| Healthcare AI system | All 10 domains | - |
| Financial AI system | All 10 domains | - |
| Research/prototyping | Core, Testing | Security, Documentation |

### By Risk Tier

| Risk Tier | Minimum Domains | Expected Controls |
|-----------|----------------|-------------------|
| Low | Core, Testing | Basic evaluation, basic monitoring |
| Medium | Core, Security, Data, Testing, Operations | Human review, retention, PII minimization |
| High | All 10 domains | Full control set, audit trail, incident response |

## Domain Dependencies

```
Core <-- Security <-- Data <-- Integration
  |         |           |          |
  v         v           v          v
Testing <-- Operations <-- Performance <-- Compliance
```

## Key Controls by Domain

### Core
- System ownership and purpose
- Risk tier assignment
- Human review for high-impact actions
- Fallback and rollback capability

### Security
- Authentication and authorization
- Secret management
- Threat modeling
- Incident response

### Data
- Data inventory and classification
- Retention and purging
- Legal hold support
- Data subject request handling

### Integration
- Tool registry and permissions
- API versioning
- MCP boundary review
- Vendor and DPA management

### Operations
- Deployment automation
- Rollback procedures
- Monitoring and alerting
- On-call and incident response

### Testing
- Evaluation coverage
- Regression testing
- Safety and fairness testing
- Performance testing

### Documentation
- System registers
- Model cards
- Prompt registers
- Runbooks

### Performance
- Latency SLOs
- Throughput targets
- Cost budgets
- Caching strategy

### Compliance
- Legal basis documentation
- Audit trail
- Exception management
- Training and awareness
