# Integration Domain - Checklist

## Overview

This checklist verifies integration best practices for LLM/agentic systems.

---

## Priority Guide

- P0: Required for production security and reliability
- P1: Required for maintainable integrations
- P2: Recommended for performance and quality

---

## API Integration Checklist

- [ ] P0: Authentication implemented (API key/JWT/OAuth)
- [ ] P0: Rate limiting configured
- [ ] P0: Input validation on all endpoints
- [ ] P0: Proper error handling with safe messages
- [ ] P1: API versioning implemented
- [ ] P1: Pagination for large result sets
- [ ] P2: Response caching where appropriate

---

## Webhook Checklist

- [ ] P0: Signature verification enabled
- [ ] P0: Retry mechanism with backoff
- [ ] P0: Timeouts on all webhook calls
- [ ] P1: Dead letter queue for failed deliveries
- [ ] P1: Idempotency for duplicate events
- [ ] P2: Webhook health monitoring

---

## Streaming Checklist

- [ ] P0: Backpressure handling implemented
- [ ] P0: Connection timeouts configured
- [ ] P1: Reconnection logic for clients
- [ ] P2: Client-side buffering optimized

---

## Security Checklist

- [ ] P0: No hardcoded secrets
- [ ] P0: HTTPS enforced
- [ ] P1: CORS configured correctly
- [ ] P1: Input sanitization for all data
- [ ] P2: Security headers configured

---

## Operational Excellence Checklist

- [ ] P0: Runbook for common failures documented
- [ ] P0: On-call rotation established
- [ ] P1: Post-mortem process in place
- [ ] P1: Change management process defined
- [ ] P2: Regular incident review meetings scheduled

---

## Deployment & Infrastructure Checklist

- [ ] P0: Container images built with minimal base image
- [ ] P0: Health check endpoints implemented
- [ ] P0: Resource limits (CPU/memory) set
- [ ] P0: Graceful shutdown implemented
- [ ] P1: Configuration via environment variables
- [ ] P1: Secrets managed via vault/KMS
- [ ] P1: Database migrations automated
- [ ] P2: Blue-green or canary deployment strategy
- [ ] P2: Rollback procedure documented

---

## Testing & Quality Assurance Checklist

- [ ] P0: Unit tests for all integration handlers
- [ ] P0: Integration tests for critical paths
- [ ] P0: Contract tests for API consumers
- [ ] P1: Load testing performed before release
- [ ] P1: Chaos engineering tests conducted
- [ ] P1: Security testing (SAST/DAST) in CI
- [ ] P2: End-to-end tests covering user journeys
- [ ] P2: Synthetic monitoring in production

---

## Data Management Checklist

- [ ] P0: Data retention policies defined
- [ ] P0: PII handled according to regulations
- [ ] P1: Data backup strategy implemented
- [ ] P1: Database connection pooling configured
- [ ] P1: Query performance monitored
- [ ] P1: Data encryption at rest enabled
- [ ] P2: Data archival process for old sessions
- [ ] P2: GDPR/CCPA compliance verified

---

## Scalability Checklist

- [ ] P0: Horizontal scaling capability tested
- [ ] P0: Database connection limits configured
- [ ] P0: Cache hit ratio monitored (>80% target)
- [ ] P1: Auto-scaling rules defined
- [ ] P1: Queue depth monitoring implemented
- [ ] P1: Load balancer health checks configured
- [ ] P2: Performance benchmarks established
- [ ] P2: Capacity planning documented

---

## Disaster Recovery Checklist

- [ ] P0: Backup schedule defined and automated
- [ ] P0: Backup restoration tested monthly
- [ ] P0: RTO/RPO targets documented
- [ ] P1: Multi-region deployment strategy
- [ ] P1: Failover procedure documented
- [ ] P1: Data replication verified
- [ ] P2: Recovery drill conducted quarterly
- [ ] P2: Business continuity plan maintained

---

## Compliance & Governance Checklist

- [ ] P0: Access control list maintained
- [ ] P0: Audit logging enabled for all actions
- [ ] P1: Data classification policies applied
- [ ] P1: Third-party integrations reviewed
- [ ] P1: Vulnerability scanning scheduled
- [ ] P1: License compliance verified
- [ ] P2: Privacy impact assessment completed
- [ ] P2: Data processing agreement reviewed

---

## Cost Optimization Checklist

- [ ] P1: Right-sizing recommendations reviewed
- [ ] P1: Idle resource cleanup automated
- [ ] P1: Reserved capacity evaluated for steady workloads
- [ ] P2: Cost alerts configured
- [ ] P2: Resource tagging for chargeback
- [ ] P2: Storage lifecycle policies applied

---

## Vendor & Third-Party Checklist

- [ ] P0: Service level agreements reviewed
- [ ] P0: Fallback mechanisms for critical vendors
- [ ] P1: Vendor security assessment completed
- [ ] P1: API contract documented
- [ ] P1: Integration tests with vendor sandbox
- [ ] P2: Vendor deprecation plan in place

---

## Documentation Checklist

- [ ] P0: API documentation auto-generated
- [ ] P0: Integration runbooks available
- [ ] P0: Architecture diagrams up-to-date
- [ ] P1: Deployment procedures documented
- [ ] P1: Troubleshooting guides maintained
- [ ] P1: Known issues registry maintained
- [ ] P2: Developer onboarding guide available
- [ ] P2: Change log maintained per release

---

## Pre-Production Checklist

- [ ] P0: All checklist items above completed
- [ ] P0: Sign-off from security team
- [ ] P0: Sign-off from platform team
- [ ] P0: Load test results reviewed
- [ ] P1: Staging environment mirrors production
- [ ] P1: Canary deployment tested
- [ ] P1: Rollback plan verified
- [ ] P2: Feature flags configured
- [ ] P2: Monitoring dashboards reviewed

---

## Event-Driven Architecture Checklist

- [ ] P1: Event schema versioning implemented
- [ ] P1: Dead letter queue configured
- [ ] P1: Consumer group scaling tested
- [ ] P2: Event replay mechanism available
- [ ] P2: Schema registry in use
- [ ] P2: Idempotent consumers implemented

---

## Configuration Management Checklist

- [ ] P0: No secrets stored in code or config files
- [ ] P0: Environment-specific configs separated
- [ ] P0: Default values defined for all settings
- [ ] P1: Validation of config values on load
- [ ] P1: Hot-reload of non-critical configs
- [ ] P2: Feature flags for integration variants

---

## Third-Party API Integration Checklist

- [ ] P0: Timeouts configured (connect and read)
- [ ] P0: Retry logic with exponential backoff
- [ ] P0: Circuit breaker for external services
- [ ] P1: API contract tested (contract testing)
- [ ] P1: Fallback behavior documented
- [ ] P2: Rate limit headers respected
- [ ] P2: Response caching with TTL

---

## Security Integration Checklist

- [ ] P0: mTLS for service-to-service communication
- [ ] P0: Secrets rotated regularly (90 days max)
- [ ] P0: API keys scoped to minimum permissions
- [ ] P1: Request signing implemented for critical APIs
- [ ] P1: Audit logs for all integration calls
- [ ] P1: PII redaction in logs
- [ ] P2: Regular penetration testing
- [ ] P2: Secret scanning in CI pipeline

---

## Multi-Tenant Integration Checklist

- [ ] P0: Tenant isolation in database queries
- [ ] P0: Per-tenant rate limiting
- [ ] P0: Tenant-specific API keys
- [ ] P1: Tenant quota enforcement
- [ ] P1: Per-tenant metrics and monitoring
- [ ] P1: Tenant onboarding/offboarding automation
- [ ] P2: Tenant-specific feature flags

---

## Container & Deployment Checklist

- [ ] P0: Health check probes configured
- [ ] P0: Graceful shutdown with SIGTERM handler
- [ ] P0: Resource limits set
- [ ] P1: Init containers for dependency checks
- [ ] P1: Config via ConfigMap/Secrets (Kubernetes)
- [ ] P2: Sidecar containers for logging/metrics
- [ ] P2: Pod disruption budgets defined

---

## Observability & Monitoring Checklist

- [ ] P0: Distributed tracing enabled
- [ ] P0: Structured logging in JSON format
- [ ] P0: Key metrics exported (RED/USE)
- [ ] P1: SLOs defined and tracked
- [ ] P1: Alerting rules configured
- [ ] P1: Log aggregation pipeline
- [ ] P2: Custom dashboards for integration health
- [ ] P2: Trace sampling strategy defined

---

## Streaming Integration Checklist

- [ ] P0: Backpressure handling implemented
- [ ] P0: Connection retry with backoff
- [ ] P0: Stream timeout configured
- [ ] P1: Message acknowledgment semantics
- [ ] P1: Offset/sequence tracking
- [ ] P2: Replay capability for debugging

---

## gRPC Integration Checklist

- [ ] P0: Protobuf schema versioning
- [ ] P0: Deadline/timeout propagation
- [ ] P0: Error status codes standardized
- [ ] P1: Interceptors for auth/metrics/logging
- [ ] P1: Reflection endpoint restricted
- [ ] P2: Load balancing policy configured

---

## WebSocket Integration Checklist

- [ ] P0: Reconnection logic implemented
- [ ] P0: Heartbeat/ping-pong mechanism
- [ ] P0: Message size limits enforced
- [ ] P1: Authentication on upgrade
- [ ] P1: Rate limiting per connection
- [ ] P1: Cleanup on connection close
- [ ] P2: Binary message support

---

## Compliance & Audit Checklist

- [ ] P0: Access logs retained per policy
- [ ] P0: Data encryption in transit verified
- [ ] P1: Data encryption at rest enabled
- [ ] P1: PII handling procedures documented
- [ ] P1: Right to deletion (GDPR) implemented
- [ ] P2: Annual security review conducted

---

## Vendor Lock-In Mitigation Checklist

- [ ] P1: Abstractions for external APIs in place
- [ ] P1: Multiple provider support where possible
- [ ] P1: API contracts version controlled
- [ ] P2: Migration plan documented
- [ ] P2: Open standards preferred over proprietary

---

## Cost Management Checklist

- [ ] P1: Cost attribution by integration
- [ ] P1: Budget alerts configured
- [ ] P1: Request/response size monitoring
- [ ] P2: Efficient serialization formats used
- [ ] P2: Compression enabled where beneficial

---

## Team & Process Checklist

- [ ] P1: Runbooks for integration failures
- [ ] P1: Escalation paths defined
- [ ] P1: On-call coverage established
- [ ] P1: Post-incident review process
- [ ] P2: Developer documentation maintained
- [ ] P2: Integration playground environment

---

## Pre-Deployment Verification

- [ ] P0: All critical tests passing
- [ ] P0: Security scan clean
- [ ] P0: Performance benchmarks met
- [ ] P1: Staging environment tested
- [ ] P1: Rollback procedure verified
- [ ] P1: Monitoring dashboards ready
- [ ] P2: Feature flags configured

---

## Post-Deployment Verification

- [ ] P0: Health checks passing
- [ ] P0: Error rate baseline established
- [ ] P0: Traffic routing verified
- [ ] P1: Canary metrics reviewed
- [ ] P1: Logs clean of errors
- [ ] P2: User feedback collected
- [ ] P2: Capacity metrics reviewed

---

## Appendix: Recommended Configuration Values

```yaml
# Recommended production settings
integration:
  timeout:
    connect: 5s
    read: 30s
    write: 10s
  retry:
    max_attempts: 3
    backoff_multiplier: 2
    initial_delay: 1s
    max_delay: 30s
  circuit_breaker:
    failure_threshold: 5
    recovery_timeout: 60s
    success_threshold: 2
  rate_limit:
    default_rpm: 1000
    burst_size: 100
    cache_ttl: 300s
  connection_pool:
    max_connections: 100
    max_per_host: 20
    connection_timeout: 10s
    idle_timeout: 60s
  logging:
    level: INFO
    format: json
    include_correlation_id: true
  security:
    tls_min_version: 1.2
    signature_algorithm: sha256
    token_refresh_buffer: 300s
```

---

## CI/CD Pipeline Checklist

- [ ] P0: Linting on all changed files
- [ ] P0: Type checking in CI
- [ ] P0: Test suite passes before merge
- [ ] P0: Security scanning (bandit/safety/trivy)
- [ ] P1: Docker image scan for vulnerabilities
- [ ] P1: Integration test stage in pipeline
- [ ] P1: Automated release notes generated
- [ ] P2: Preview deployments for PRs
- [ ] P2: Dependency update bot configured

---

## Disaster Recovery Checklist

- [ ] P0: RTO defined and documented
- [ ] P0: RPO defined and documented
- [ ] P0: Backup verification automated
- [ ] P0: Backup retention policy enforced
- [ ] P1: Cross-region replication enabled
- [ ] P1: Failover drill run quarterly
- [ ] P1: Recovery runbook maintained
- [ ] P2: Chaos engineering experiments scheduled

---

## API Contract Checklist

- [ ] P0: OpenAPI/Swagger spec maintained
- [ ] P0: Breaking changes communicated
- [ ] P1: Consumer-driven contracts tested
- [ ] P1: Schema evolution strategy defined
- [ ] P1: Deprecation notice period enforced (minimum 90 days)
- [ ] P2: API changelog published
- [ ] P2: Developer portal maintained

---

## Multi-Region Checklist

- [ ] P0: Data replication latency < 100ms
- [ ] P0: DNS-based geo-routing configured
- [ ] P1: Regional failover tested
- [ ] P1: Data residency compliance verified
- [ ] P1: Regional WAF rules configured
- [ ] P2: Cost allocation by region

---

## Documentation Checklist

- [ ] P0: API reference documentation auto-generated
- [ ] P0: Architecture diagrams available
- [ ] P0: Deployment runbook maintained
- [ ] P1: Postman collection for endpoints
- [ ] P1: Troubleshooting guide updated
- [ ] P1: SPDX license identifiers for dependencies
- [ ] P2: Developer onboarding checklist

---

## Edge Cases & Edge Services Checklist

- [ ] P1: Timezone handling verified
- [ ] P1: Locale-specific formatting tested
- [ ] P1: Large payload handling tested (>10MB)
- [ ] P1: Unicode edge cases tested
- [ ] P2: Time synchronization with NTP
- [ ] P2: Leap seconds handling verified

---

## Rollback Strategy Checklist

- [ ] P0: Rollback procedure documented
- [ ] P0: Rollback executed < 5 minutes
- [ ] P0: Database migrations reversible
- [ ] P1: Feature flags for gradual rollback
- [ ] P1: Canary phase before full rollout
- [ ] P2: Automated rollback on error thresholds

---

## Cost Governance Checklist

- [ ] P1: Cost anomalies alerting configured
- [ ] P1: Spend by integration visible in dashboards
- [ ] P1: Budget cap enforced per environment
- [ ] P2: Request deduplication where possible
- [ ] P2: Caching strategy reduces LLM cost
- [ ] P2: Batch processing for bulk operations

---

## Regulatory Compliance Checklist

- [ ] P0: GDPR Article 30 records maintained
- [ ] P0: Data processing agreements in place for vendors
- [ ] P0: Right to erasure (deletion) implemented
- [ ] P1: SOC 2 Type II controls adopted
- [ ] P1: HIPAA safeguards where applicable
- [ ] P1: PCI-DSS scope assessed for payment flows
- [ ] P2: Annual accessibility audit scheduled

---

## Integration Lifecycle Checklist

- [ ] P0: Integration owner assigned
- [ ] P0: Business owner identified
- [ ] P1: Onboarding checklist completed
- [ ] P1: Offboarding procedure documented
- [ ] P1: Data retention period defined
- [ ] P2: Knowledge transfer sessions scheduled

---

## Traffic Management Checklist

- [ ] P1: Blue/green deployment capability
- [ ] P1: Weighted traffic shifting tested
- [ ] P1: Sticky sessions for WebSocket
- [ ] P2: Geo-routing rules validated
- [ ] P2: CDN caching headers set correctly

---

## Dependency Management Checklist

- [ ] P1: Software composition analysis (SCA) in CI
- [ ] P1: License compliance checked (REUSE/SPDX)
- [ ] P1: SBOM generated on release
- [ ] P2: Transitive dependency tree reviewed quarterly
- [ ] P2: Vulnerability disclosure process defined

---

## Backup & Restore Checklist

- [ ] P0: Full backup daily
- [ ] P0: Incremental backup every 6 hours
- [ ] P0: Point-in-time recovery capability
- [ ] P0: Backup integrity checks automated
- [ ] P1: Backup encryption enabled
- [ ] P1: Cross-region backup replication
- [ ] P1: Restore drill performed quarterly
- [ ] P2: Backup cost optimized with tiering

---

## Appendix: Severity Definitions

| Severity | Definition | Response Time | Example |
|----------|-----------|---------------|---------|
| P0 | Production broken, data loss, security breach | Immediate | API returning 500 for all requests |
| P1 | Major feature degraded, affects most users | 4 hours | Slow response times affecting user experience |
| P2 | Minor issue, workaround available | Next business day | Suboptimal logging configuration |

---

## Appendix: Common Integration Failure Modes

1. **Thundering Herd**: All clients retry simultaneously after outage, overwhelming services
2. **Cascading Failure**: One service failure causes unrelated services to fail
3. **Split Brain**: Network partition causes cluster inconsistency
4. **Zombie Process**: Orphaned background tasks continue running
5. **Memory Fragmentation**: Long-running process memory grows unbounded
6. **Clock Skew**: Distributed systems with unsynchronized clocks
7. **DNS TTL Mismatch**: Different services caching DNS records differently

---

## Appendix: Integration Maturity Model

### Level 1: Ad Hoc
- Manual integration testing
- No monitoring
- Reactive incident response

### Level 2: Defined
- Standardized integration patterns
- Basic monitoring
- Documented runbooks

### Level 3: Measured
- SLOs tracked
- Automated testing in CI
- Proactive alerting

### Level 4: Optimized
- Chaos engineering practiced
- Automated remediation
- Continuous improvement process

---

## Appendix: Recommended Reading

- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Release It!" by Michael Nygard
- "Site Reliability Engineering" (Google SRE Book)
- "The Phoenix Project" by Gene Kim
- "Building Microservices" by Sam Newman
- "Cloud Native Patterns" by Cornelia Davis

---

## Appendix: Integration Health评分 Scorecard

Compute a simple 0-100 score from checklist coverage.

```python
class IntegrationScorecard:
    def __init__(self):
        self.scores = {}
    
    def score_domain(self, domain: str, items: list[dict]) -> dict:
        total = len(items)
        completed = sum(1 for i in items if i.get("done"))
        pct = (completed / total * 100) if total else 0
        return {"domain": domain, "total": total, "completed": completed, "score": pct}
    
    def overall(self, domains: list[dict]) -> dict:
        by = {d["domain"]: d for d in domains}
        res = []
        total = 0
        done = 0
        for d in by.values():
            res.append(self.score_domain(d["domain"], d["items"]))
            total += d["items"]
            done += sum(1 for i in d["items"] if i.get("done"))
        return {"domains": res, "overall": (done / total * 100) if total else 0}
```

```text
score >= 90 production ready
score >= 70 needs minor fixes
score >= 50 needs significant work
score <  50 not production ready
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Advanced](./advanced.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)