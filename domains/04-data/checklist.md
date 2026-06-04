# Data Domain - Checklist

## Overview

This checklist verifies data handling best practices are followed throughout the agent lifecycle, covering storage, retrieval, privacy, security, and operational concerns.

---

## Priority Guide

| Priority | Description |
|----------|-------------|
| P0 | Required for production stability, security, and compliance |
| P1 | Required for maintainable production delivery |
| P2 | Recommended for code quality and performance |
| P3 | Useful refinement for operational excellence |

---

## Pre-Implementation Checklist

### Data Architecture Planning

- [ ] P0: Data flow diagrams created and reviewed
- [ ] P0: Storage requirements identified (structured/unstructured, size, velocity)
- [ ] P0: Privacy and security requirements documented
- [ ] P1: Data retention and deletion policies defined
- [ ] P1: Backup and recovery strategy selected
- [ ] P2: Performance and scaling requirements estimated

---

## Implementation Checklist

### Data Validation

- [ ] P0: All external inputs validated with type and bounds checking
- [ ] P0: Sensitive data identified and marked
- [ ] P1: Schema validation library integrated (pydantic, marshmallow)
- [ ] P1: Input sanitization for prompt injection prevention
- [ ] P2: Validation error messages are informative but safe

### Storage Security

- [ ] P0: All sensitive data encrypted at rest
- [ ] P0: Database connections use TLS
- [ ] P0: No hardcoded credentials in source code
- [ ] P1: Access controls implemented for all data stores
- [ ] P1: Audit logging enabled for data operations
- [ ] P2: Secret management integrated (vault, KMS)

### Data Retrieval

- [ ] P0: Parameterized queries used exclusively
- [ ] P0: No SQL injection vulnerabilities
- [ ] P1: Connection pooling configured
- [ ] P1: Query timeouts set (max 30 seconds)
- [ ] P2: Indexes created for query patterns
- [ ] P2: Caching strategy implemented

---

## Privacy Checklist

### PII Handling

- [ ] P0: PII detection implemented for incoming data
- [ ] P0: PII redacted in logs and error messages
- [ ] P0: PII encrypted or hashed in storage
- [ ] P1: Data retention policies for PII documented
- [ ] P1: Right-to-delete mechanism implemented
- [ ] P2: Privacy impact assessment completed

### Regulatory Compliance

- [ ] P0: GDPR/CCPA requirements identified
- [ ] P0: Data processing records maintained
- [ ] P1: Data subject request handling implemented
- [ ] P2: Privacy by design principles applied

---

## Performance Checklist

### Caching

- [ ] P1: Cache implemented for frequently accessed data
- [ ] P1: Cache TTL defined based on data volatility
- [ ] P1: Cache invalidation on updates
- [ ] P2: Multi-level cache (L1/L2) for scale
- [ ] P2: Cache hit rate monitoring configured

### Query Optimization

- [ ] P1: Database indexes created for primary queries
- [ ] P1: N+1 query problems eliminated
- [ ] P2: Query execution plans reviewed
- [ ] P2: Connection pool sizes validated under load

---

## Operational Checklist

### Backup and Recovery

- [ ] P0: Automated backups configured
- [ ] P0: Restore procedures tested
- [ ] P1: Backup encryption enabled
- [ ] P1: Backup retention meets compliance requirements
- [ ] P2: Point-in-time recovery tested

### Monitoring

- [ ] P1: Data operation latency tracked
- [ ] P1: Data access patterns logged
- [ ] P1: Cache hit/miss ratios monitored
- [ ] P2: Data quality metrics collected

---

## Testing Checklist

### Unit Testing

- [ ] P1: All data access functions have unit tests
- [ ] P1: Validation functions tested with edge cases
- [ ] P1: Cache behavior tested under failure scenarios
- [ ] P2: Data serialization/deserialization tested

### Integration Testing

- [ ] P1: Database queries tested with real data
- [ ] P1: Cache invalidation tested
- [ ] P2: Backup/restore procedures tested

---

## Deployment Checklist

### Pre-Deployment

- [ ] P0: All P0 items verified and documented
- [ ] P1: Data migration scripts tested
- [ ] P1: Backup systems verified before migration
- [ ] P2: Monitoring dashboards updated

### Post-Deployment

- [ ] P1: Backup jobs running successfully
- [ ] P1: Cache warm-up completed if applicable
- [ ] P2: Performance baselines captured

---

## Incident Response Checklist

### Data Loss

- [ ] P0: Backup restoration procedure available
- [ ] P0: Recovery time objective defined and tested
- [ ] P1: Data validation before restore
- [ ] P2: Root cause analysis documented

### Security Incident

- [ ] P0: Compromised data identified and contained
- [ ] P0: Access logs reviewed for unauthorized access
- [ ] P1: Affected data quarantined
- [ ] P2: Compliance notification timeline triggered

---

## Sign-Off

Before marking as complete:

- [ ] All P0 items verified
- [ ] P1 items addressed or documented exceptions
- [ ] Peer review completed
- [ ] Tests passing

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)