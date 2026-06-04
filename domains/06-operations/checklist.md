# Operations Domain - Checklist

## Overview

This checklist verifies operations best practices for LLM/agentic systems.

---

## Priority Guide

- P0: Required for production security and reliability
- P1: Required for maintainable operations
- P2: Recommended for performance and quality

---

## Deployment Checklist

- [ ] P0: Health endpoints implemented
- [ ] P0: Read endpoint separate from health
- [ ] P0: Resource limits configured
- [ ] P0: Readiness and liveness probes configured
- [ ] P0: Container image scanning in CI/CD
- [ ] P1: Deployment automation in place
- [ ] P1: Rollback procedures documented
- [ ] P1: Canary deployment configured
- [ ] P1: Blue-green deployment capability
- [ ] P1: Deployment strategy documented
- [ ] P2: Automated rollback on failure
- [ ] P2: Immutable infrastructure enforced
- [ ] P2: Image promotion from staging to production

---

## Monitoring Checklist

- [ ] P0: Request logging enabled
- [ ] P0: Error logging with context
- [ ] P0: Metrics for latency, errors, and traffic
- [ ] P1: Metrics for key operations
- [ ] P1: Alerting thresholds set
- [ ] P1: Dashboard created
- [ ] P1: SLO tracking configured
- [ ] P1: Anomaly detection enabled
- [ ] P2: Distributed tracing configured
- [ ] P2: Correlation IDs propagated across services
- [ ] P2: Service map visualization available

---

## Scaling Checklist

- [ ] P1: Autoscaling configured
- [ ] P1: Concurrency limits set
- [ ] P1: Queue depth monitoring enabled
- [ ] P2: Load testing performed
- [ ] P2: Resource requests tuned
- [ ] P2: Scaling runbooks maintained
- [ ] P2: Cache hit ratio monitored

---

## Configuration Management Checklist

- [ ] P0: Configuration externalized from code
- [ ] P0: Environment variables used for secrets
- [ ] P0: No hardcoded credentials
- [ ] P1: Centralized config management (e.g., Consul/Vault)
- [ ] P1: Config validation on startup
- [ ] P1: Config version control
- [ ] P1: Hot-reload for non-critical configuration
- [ ] P1: Encryption for sensitive config values
- [ ] P1: Secret rotation schedule maintained
- [ ] P2: Config drift detection enabled
- [ ] P2: Feature flags for gradual rollout

---

## Security Checklist

- [ ] P0: TLS/HTTPS enforced for all endpoints
- [ ] P0: Authentication required for admin endpoints
- [ ] P0: Secrets rotated on schedule
- [ ] P0: Network policies restrict pod communication
- [ ] P0: RBAC for Kubernetes resources
- [ ] P0: Security scanning in CI/CD
- [ ] P1: Container images scanned for vulnerabilities
- [ ] P1: Least privilege principle for service accounts
- [ ] P1: Audit logging for admin actions
- [ ] P1: mTLS for internal service communication
- [ ] P1: OAuth2/JWT tokens with short expiry
- [ ] P1: Rate limiting on all public endpoints
- [ ] P2: Security headers configured (HSTS, CSP)
- [ ] P2: Penetration testing completed

---

## Reliability Checklist

- [ ] P0: Circuit breakers configured for external dependencies
- [ ] P0: Timeouts set for all external calls
- [ ] P0: Retry policies with exponential backoff
- [ ] P1: Bulkhead isolation pattern implemented
- [ ] P1: Graceful degradation for model failures
- [ ] P1: Bulkhead isolation limits concurrent resource usage
- [ ] P1: Dead letter queue for failed messages
- [ ] P1: Health checks with deep probing
- [ ] P1: Graceful shutdown implemented
- [ ] P1: Load balancer health checks validated
- [ ] P1: Connection pooling configured
- [ ] P2: Chaos testing performed regularly
- [ ] P2: Failure injection tests in staging
- [ ] P2: Disaster recovery drills scheduled

---

## Observability Checklist

- [ ] P0: Structured logging in JSON format
- [ ] P0: Metrics collected for all endpoints
- [ ] P0: Distributed tracing configured
- [ ] P0: Correlation IDs propagated across services
- [ ] P1: Dashboards for latency, error rate, traffic
- [ ] P1: Alerting rules defined for key thresholds
- [ ] P1: Log aggregation pipeline operational
- [ ] P1: Service map visualization available
- [ ] P1: Anomaly detection alerts configured
- [ ] P1: SLI/SLO dashboards maintained
- [ ] P2: Trace sampling strategy defined
- [ ] P2: Custom metrics for business logic
- [ ] P2: Log retention policy enforced

---

## Incident Response Checklist

- [ ] P0: On-call rotation established
- [ ] P0: Escalation policy documented
- [ ] P0: Communication plan for incidents
- [ ] P0: Incident severity levels defined
- [ ] P0: Response time targets set for each severity
- [ ] P1: Runbooks for common failure modes
- [ ] P1: Post-mortem process defined
- [ ] P1: Incident tracking in issue tracker
- [ ] P1: War room procedures documented
- [ ] P1: Stakeholder notification templates ready
- [ ] P2: Blameless post-mortem culture enforced
- [ ] P2: Tabletop exercises conducted

---

## Disaster Recovery Checklist

- [ ] P0: RTO (Recovery Time Objective) documented
- [ ] P0: RPO (Recovery Point Objective) documented
- [ ] P0: Database backups automated and tested
- [ ] P0: Backup restoration procedure documented
- [ ] P0: Backup encryption at rest
- [ ] P1: Cross-region replication configured
- [ ] P1: Disaster recovery runbook maintained
- [ ] P1: Recovery drills scheduled quarterly
- [ ] P1: Backup verification automated
- [ ] P1: Point-in-time recovery tested
- [ ] P2: Chaos testing for DR scenarios
- [ ] P2: Multi-region failover automation

---

## Cost Management Checklist

- [ ] P0: Cost monitoring and alerts enabled
- [ ] P0: Budget alerts configured
- [ ] P0: Cost attribution by tenant/service
- [ ] P1: Resource tagging enforced
- [ ] P1: Right-sizing recommendations reviewed monthly
- [ ] P1: Caching strategy to reduce model API costs
- [ ] P1: Idle resource cleanup automation
- [ ] P1: Log and metrics retention cost reviewed
- [ ] P2: Savings plans or reserved capacity evaluated
- [ ] P2: Storage tiering for infrequently accessed data

---

## CI/CD Checklist

- [ ] P0: Automated tests run on every PR
- [ ] P0: Linting and type checking in pipeline
- [ ] P0: Security scanning on every build
- [ ] P0: Artifact signing for releases
- [ ] P1: Integration tests against staging environment
- [ ] P1: Contract tests for API consumers
- [ ] P1: Automated deployment to staging
- [ ] P1: Manual approval gate for production
- [ ] P1: Dependency scanning in pipeline
- [ ] P1: Test coverage reporting
- [ ] P2: Canary deployment in pipeline
- [ ] P2: Automated rollback on health check failure
- [ ] P2: Preview environments for PRs

---

## Lifecycle Management Checklist

- [ ] P0: API versioning strategy in place
- [ ] P0: Deprecation policy documented (90-day minimum)
- [ ] P0: Model versioning and rollback capability
- [ ] P1: Configuration version control
- [ ] P1: Secret rotation schedule maintained
- [ ] P1: Dependency updates tracked and tested
- [ ] P1: Release notes generated automatically
- [ ] P2: SemVer compliance for public APIs
- [ ] P2: Changelog maintained for all releases
- [ ] P2: Technical debt tracked and prioritized

---

## Data Management Checklist

- [ ] P0: Data retention policies defined
- [ ] P0: PII handling compliant with regulations
- [ ] P0: Data encryption at rest and in transit
- [ ] P1: Database connection pooling configured
- [ ] P1: Query performance monitoring enabled
- [ ] P1: Cache invalidation strategy defined
- [ ] P2: Data archival process for old sessions
- [ ] P2: GDPR/CCPA compliance verified
- [ ] P2: Data lineage tracking enabled

---

## Capacity Planning Checklist

- [ ] P1: Load testing performed before release
- [ ] P1: Performance baselines documented
- [ ] P1: Autoscaling limits and thresholds set
- [ ] P1: Capacity forecasting reviewed quarterly
- [ ] P1: Budget for infrastructure growth approved
- [ ] P2: Growth trend analysis documented
- [ ] P2: Cost vs performance trade-off analysis

---

## Testing Checklist

- [ ] P0: Integration tests cover critical paths
- [ ] P0: Model behavior regression tests exist
- [ ] P0: Security tests in CI pipeline
- [ ] P1: Load tests validate scaling limits
- [ ] P1: Contract tests with downstream consumers
- [ ] P1: Failover tests for critical dependencies
- [ ] P1: Synthetic monitoring in production
- [ ] P2: E2E tests for user journeys
- [ ] P2: Chaos engineering experiments scheduled

---

## Documentation Checklist

- [ ] P0: Runbooks for common incidents
- [ ] P0: Architecture diagrams up-to-date
- [ ] P0: Deployment procedures documented
- [ ] P0: Troubleshooting guides maintained
- [ ] P1: API documentation auto-generated
- [ ] P1: Known issues registry maintained
- [ ] P1: Post-mortem templates standardized
- [ ] P2: Developer onboarding guide available
- [ ] P2: Change log maintained per release

---

## Compliance & Governance Checklist

- [ ] P0: Access control list maintained
- [ ] P0: Audit logging enabled for all actions
- [ ] P0: Data encryption verified
- [ ] P0: Compliance training completed by team
- [ ] P1: Data classification policies applied
- [ ] P1: Vendor security assessments completed
- [ ] P1: Vulnerability scanning scheduled (weekly)
- [ ] P1: License compliance verified for all dependencies
- [ ] P2: Privacy impact assessment (PIA) completed
- [ ] P2: Annual security audit scheduled

---

## Vendor & Third-Party Checklist

- [ ] P0: Service level agreements reviewed
- [ ] P0: Fallback mechanisms for critical vendors
- [ ] P0: Vendor contacts and escalation paths documented
- [ ] P1: Vendor security assessment completed
- [ ] P1: API contracts version controlled
- [ ] P1: Integration tests with vendor sandbox
- [ ] P1: Vendor change notification process
- [ ] P1: Vendor performance monitored
- [ ] P2: Vendor deprecation plan in place
- [ ] P2: Multi-vendor strategy where applicable

---

## Container & Infrastructure Checklist

- [ ] P0: Health check probes configured
- [ ] P0: Graceful shutdown implemented
- [ ] P0: Resource limits set (CPU/Memory)
- [ ] P0: Readiness probe implemented
- [ ] P1: Init containers for dependency waits
- [ ] P1: Config via ConfigMap/Secrets (K8s)
- [ ] P1: Pod disruption budgets defined
- [ ] P1: Security context defined for containers
- [ ] P1: Pod security standards enforced
- [ ] P2: Sidecar containers for logging/metrics

---

## Multi-Region & Availability Checklist

- [ ] P1: Multi-region deployment capability
- [ ] P1: Regional failover tested periodically
- [ ] P1: DNS-based geo-routing configured
- [ ] P1: Data residency compliance verified
- [ ] P2: Cross-region cost analyses performed
- [ ] P2: Regional SLO targets defined

---

## Rate Limiting & Quota Management Checklist

- [ ] P0: Rate limiting implemented per endpoint
- [ ] P0: Token budgets enforced for LLM calls
- [ ] P0: Quota alerts configured
- [ ] P0: Request validation and size limits
- [ ] P1: Quota separation by workload type
- [ ] P1: Exponential backoff with jitter implemented
- [ ] P1: Retry budgets defined
- [ ] P1: Fair queuing for priority workloads
- [ ] P2: Request queuing for non-urgent workloads

---

## Change Management Checklist

- [ ] P0: Changes tracked in issue tracker
- [ ] P0: Rollback capability for every change
- [ ] P0: Changes reviewed before production
- [ ] P0: Change freeze periods defined
- [ ] P1: Emergency change procedure defined
- [ ] P1: Change success rate tracked
- [ ] P1: Deployment frequency targets set
- [ ] P1: Deployment lead time monitored
- [ ] P2: Mean time to recover (MTTR) tracked

---

## Network & Connectivity Checklist

- [ ] P1: DNS caching and TTL reviewed
- [ ] P1: TLS certificates monitored for expiration
- [ ] P1: Firewall rules and network policies audited
- [ ] P1: Service mesh health checks validated
- [ ] P1: Ingress controller configured with SSL
- [ ] P2: Outbound internet access restricted
- [ ] P2: Network latency monitoring enabled

---

## Thread Safety & Concurrency Checklist

- [ ] P0: Shared state properly synchronized
- [ ] P0: No blocking calls in async code
- [ ] P0: Race condition tests passed
- [ ] P1: Connection pools sized appropriately
- [ ] P1: Deadlock detection and prevention tested
- [ ] P1: Async resource cleanup verified
- [ ] P2: Concurrency limits documented
- [ ] P2: Stress testing performed

---

## Backup & Restore Checklist

- [ ] P0: Backups automated and verified
- [ ] P0: Retention period defined
- [ ] P0: Restore tested in staging
- [ ] P0: Off-site backup storage configured
- [ ] P1: Backup encryption enabled
- [ ] P1: Point-in-time recovery available
- [ ] P1: Backup schedule documented
- [ ] P1: Backup integrity checks automated
- [ ] P2: Backup storage geographically separated

---

## Team Readiness Checklist

- [ ] P1: On-call coverage 24/7
- [ ] P1: Runbook ownership assigned
- [ ] P1: Post-incident reviews scheduled
- [ ] P1: Training for new team members
- [ ] P1: Contact list for stakeholders maintained
- [ ] P1: Access provisioning process defined
- [ ] P2: Incident response game days conducted
- [ ] P2: Team rotations to prevent burnout

---

## Appendix: MLOps-Specific Checklist

- [ ] P0: Model behavior regression tests
- [ ] P0: Prompt evaluation suite maintained
- [ ] P0: Model endpoint health checks
- [ ] P1: RAG retrieval quality monitored
- [ ] P1: Tool execution success rate tracked
- [ ] P2: Human-in-the-loop flagging available
- [ ] P2: Conversation quality sampled regularly

---

## Appendix: Platform SRE Checklist

- [ ] P0: SLOs defined and tracked in real time
- [ ] P0: Error budget policy enforced
- [ ] P0: Alert noise reduction targets met (<10% false positives)
- [ ] P1: Operational runbooks kept under version control
- [ ] P1: Capacity forecasts reviewed quarterly
- [ ] P1: MTTR tracked and trending down
- [ ] P2: Incident response game days scheduled quarterly
- [ ] P2: Toil reduction goals defined and measured

---

## Appendix: Incident Communication Checklist

- [ ] P0: Communication plan documented
- [ ] P0: Primary, secondary, and escalation contacts defined
- [ ] P0: Status page configured for public services
- [ ] P1: Internal communication channel designated
- [ ] P1: Customer communication templates ready
- [ ] P1: Legal/compliance notified for data incidents
- [ ] P2: Post-incident communication drafted within 24 hours

---

## Appendix: Change Success Metrics Checklist

- [ ] P0: Change failure rate tracked (target <15%)
- [ ] P0: MTTR tracked (target <1 hour for P1)
- [ ] P0: Deployment frequency tracked (target weekly)
- [ ] P1: Lead time for changes measured
- [ ] P1: Rollback rate monitored
- [ ] P2: Change risk categorization applied

---

## Appendix: Resource Optimization Checklist

- [ ] P1: Pod resource requests and limits reviewed monthly
- [ ] P1: Idle namespaces and workloads identified quarterly
- [ ] P1: Spot/preemptible instances used for non-critical workloads
- [ ] P1: Vertical pod autoscaling tested
- [ ] P2: Node auto-provisioning enabled
- [ ] P2: Cluster autoscaler tuned for cost/performance balance
- [ ] P2: Reserved instance coverage evaluated annually

---

## Appendix: Performance & Latency Checklist

- [ ] P0: P50/P95/P99 latency tracked and alerted
- [ ] P0: Cold start latency measured for serverless components
- [ ] P1: Database query performance profiled monthly
- [ ] P1: Frontend Core Web Vitals tracked
- [ ] P1: Model inference latency monitored by endpoint
- [ ] P2: Synthetic tests from key geographic regions
- [ ] P2: Profiling and heap dump analysis after major incidents

---

## Appendix: AI/ML Specific Operations Checklist

- [ ] P0: Model rollback capability verified
- [ ] P0: Model versioning enforced
- [ ] P0: A/B testing framework operational
- [ ] P1: Prompt evaluation suite automated in CI/CD
- [ ] P1: RAG retrieval relevance threshold monitored
- [ ] P1: Tool invocation success rate tracked
- [ ] P1: Guardrails for model outputs validated before release
- [ ] P2: Human-in-the-loop review for high-stakes decisions
- [ ] P2: Model bias and fairness metrics collected
- [ ] P2: Synthetic data generation pipeline tested

---

## Appendix: Data Pipeline Operations Checklist

- [ ] P0: Data pipeline dependencies documented
- [ ] P0: Pipeline failure alerting enabled
- [ ] P0: Data quality checks at pipeline boundaries
- [ ] P1: Pipeline idempotency tested
- [ ] P1: Backfill procedures tested quarterly
- [ ] P1: Data lineage tracking operational
- [ ] P1: Staging and production data separation enforced
- [ ] P2: Real-time pipeline latency monitored
- [ ] P2: Dead letter queue analyzed for data loss

---

## Appendix: Model-Specific Checklist

- [ ] P0: Model registry maintained with versioning
- [ ] P0: Model acceptance criteria defined
- [ ] P0: A/B test sample size calculated before launch
- [ ] P1: Model drift detection enabled
- [ ] P1: Model explainability artifacts generated
- [ ] P1: Model inference cost tracked per request
- [ ] P1: Model shadow deployment tested before promotion
- [ ] P2: Model interpretability tooling integrated

---

## Appendix: Monitoring & Alerting Thresholds Checklist

- [ ] P0: Alert thresholds aligned with SLOs
- [ ] P0: Alert routing defined by service and severity
- [ ] P0: On-call escalation policy tested quarterly
- [ ] P1: Alert fatigue reduction targets set
- [ ] P1: Runbook links embedded in every alert
- [ ] P1: Silencing and grouping rules configured
- [ ] P2: Alert preview tested before promotion to production

---

## Appendix: SRE Automation Checklist

- [ ] P0: Deployment automation covers all environments
- [ ] P1: Remediation playbooks automated where possible
- [ ] P1: Auto-scaling policies validated weekly
- [ ] P1: Certificate renewal automated
- [ ] P2: Chaos engineering experiments automated
- [ ] P2: Cost anomaly detection automated

---

## Appendix: Access Control & Identity Checklist

- [ ] P0: SSO enforced for all production systems
- [ ] P0: Least privilege applied to service accounts
- [ ] P0: Admin access requires MFA
- [ ] P0: Access reviews conducted quarterly
- [ ] P1: Break-glass procedures documented and tested
- [ ] P1: Privileged access logged and audited
- [ ] P1: API key lifecycle management automated
- [ ] P2: Just-in-time access provisioning implemented

---

## Appendix: Business Continuity Checklist

- [ ] P0: Business impact analysis documented
- [ ] P0: Critical services identified and prioritized
- [ ] P0: Communication plan for business stakeholders
- [ ] P1: Alternate processing procedures documented
- [ ] P1: Third-party vendor continuity plans reviewed
- [ ] P2: Annual tabletop exercise conducted

---

## Appendix: Risk Management Checklist

- [ ] P0: Risk register maintained
- [ ] P0: High risks have mitigation plans
- [ ] P1: Risk review cadence defined (monthly)
- [ ] P1: Residual risk accepted by business owners
- [ ] P1: Risk indicators monitored
- [ ] P2: Emerging risks scanned quarterly

---

## Appendix: Test Coverage Checklist

- [ ] P0: Unit test coverage >= 80%
- [ ] P0: Critical paths have integration tests
- [ ] P1: E2E tests for user journeys
- [ ] P1: Contract tests for external APIs
- [ ] P1: Chaos tests for critical services
- [ ] P2: Mutation testing for critical modules
- [ ] P2: Performance regression tests in CI

---

## Appendix: Operational Handoff Checklist

- [ ] P0: Handover checklist completed for each service
- [ ] P0: On-call runbook link in service README
- [ ] P1: Service owner and POC documented
- [ ] P1: Escalation matrix current
- [ ] P1: Monitoring dashboards link in service README
- [ ] P1: Recent post-mortems linked
- [ ] P2: Service architecture diagram in wiki

---

## Appendix: License & Dependency Checklist

- [ ] P1: All dependencies license-compliant (REUSE/SPDX)
- [ ] P1: Dependency tree scanned for vulnerabilities
- [ ] P1: Transitive dependencies reviewed quarterly
- [ ] P1: Policy for EOL dependencies enforced
- [ ] P2: Internal shared libraries versioned
- [ ] P2: Bill of materials (SBOM) generated for releases

---

## Appendix: Audit Readiness Checklist

- [ ] P0: Audit logs retained per policy
- [ ] P0: Log integrity verified (tamper-evident)
- [ ] P0: Access reviews completed quarterly
- [ ] P1: Audit trail for configuration changes enabled
- [ ] P1: Compliance reports generated automatically
- [ ] P1: Data classification labels applied
- [ ] P2: Audit findings tracked to remediation

---

## Appendix: Incident Review Checklist

- [ ] User impact and timeline documented.
- [ ] Failing dependency or behavior identified.
- [ ] Prompt, model, retrieval, and tool versions recorded.
- [ ] Logs reviewed with sensitive data controls.
- [ ] Immediate mitigation applied.
- [ ] Permanent fix assigned.
- [ ] Related checklist or troubleshooting guidance updated.

---

## Appendix: Capability Scoring

```python
class Scoring:
    def score(items: list[dict]) -> float:
        total = len(items)
        if total == 0:
            return 0.0
        done = sum(1 for i in items if i.get("done"))
        return (done / total) * 100

    def classify(score: float) -> str:
        if score >= 90:
            return "production ready"
        elif score >= 70:
            return "needs minor fixes"
        elif score >= 50:
            return "needs significant work"
        return "not production ready"
```

```text
score >= 90  production ready
score >= 70  needs minor fixes
score >= 50  needs significant work
score <  50  not production ready
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)