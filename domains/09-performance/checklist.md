# Performance Domain - Checklist

## Overview

Performance verification checklist for LLM/agentic systems.

## Priority Guide

- P0: Critical for user experience
- P1: Important for cost control
- P2: Helpful for optimization

---

## Caching Checklist

- [ ] P0: Cache hit rate > 80%
- [ ] P0: Cache TTL appropriate for data volatility
- [ ] P1: Cache invalidation on updates
- [ ] P1: Multi-level cache implemented
- [ ] P2: Cache warm-up for peak hours

### Verification Steps

1. Inspect cache hit rate in production metrics.
2. Confirm TTL aligns with data update frequency.
3. Verify invalidation triggers on writes.
4. Check L1 hit rate and L2 hit rate separately.
5. Preload hot keys during deployment.

### Cache Key Hygiene

- [ ] P0: Cache keys include model version and policy
- [ ] P0: Cache keys are deterministic for same inputs
- [ ] P1: Cache keys exclude user-specific identifiers unless required
- [ ] P1: Cache keys handle whitespace normalization
- [ ] P2: Cache keys use consistent hashing for collision resistance

### Cache Monitoring

- [ ] P0: Cache hit rate tracked per prefix
- [ ] P0: Cache miss latency tracked
- [ ] P1: Cache eviction rate tracked
- [ ] P1: Cache memory usage tracked
- [ ] P2: Cache key space growth monitored

---

## Latency Checklist

- [ ] P0: Time to first token < 500ms (p95)
- [ ] P0: Response completion < 5s (p95)
- [ ] P1: Token budget enforcement
- [ ] P1: Timeout on all external calls
- [ ] P2: Parallel processing where safe

### Verification Steps

1. Run synthetic traces for p95 and p99.
2. Confirm streaming is enabled for long responses.
3. Verify API timeouts are set.
4. Test parallel tool calls in staging.
5. Run chaos experiments to validate latency under failure.

### Latency Budget Allocation

- [ ] P0: Define latency budget per component
- [ ] P0: Allocate 50% to model inference
- [ ] P1: Allocate 20% to retrieval
- [ ] P1: Allocate 15% to tool execution
- [ ] P2: Allocate 15% to overhead

### Latency Segments

- [ ] P0: Trace includes all external calls
- [ ] P0: Trace includes model calls
- [ ] P1: Trace includes retrieval queries
- [ ] P1: Trace includes tool executions
- [ ] P2: Trace includes serialization/deserialization

---

## Resource Checklist

- [ ] P0: Memory usage bounded
- [ ] P1: Connection pool configured
- [ ] P1: Context size managed
- [ ] P2: Resource cleanup guaranteed

### Verification Steps

1. Monitor RSS in production.
2. Verify pool limits under load.
3. Confirm context size does not exceed budget.
4. Ensure sessions close on shutdown.

### Memory Management

- [ ] P0: Memory usage monitored in production
- [ ] P0: Max RSS limit configured
- [ ] P1: Memory leak detection enabled
- [ ] P1: Object pooling for hot paths
- [ ] P2: Periodic heap snapshots in staging

### Connection Management

- [ ] P0: Connection pool limits set
- [ ] P0: Connection timeout configured
- [ ] P1: Keepalive enabled
- [ ] P1: DNS cache TTL optimized
- [ ] P2: Connection metrics monitored

---

## Token Optimization Checklist

- [ ] P0: Prompt tokens measured and limited
- [ ] P0: Completion tokens measured
- [ ] P1: Conversation summarization implemented
- [ ] P1: Tool outputs compressed before insertion
- [ ] P2: Model routing by complexity active

### Verification Steps

1. Inspect token counts in traces.
2. Review summarization quality manually.
3. Check tool output size before insertion.
4. Verify routing decisions in logs.

### Token Counting

- [ ] P0: Tokenizer accurate for chosen models
- [ ] P0: Token counts validated against provider
- [ ] P1: Token budget enforced per request
- [ ] P1: Token usage trended over time
- [ ] P2: Token cost per user tracked

---

## Resilience Checklist

- [ ] P0: Retries use exponential backoff with jitter
- [ ] P0: Timeouts configured for all outbound calls
- [ ] P1: Circuit breakers on external dependencies
- [ ] P1: Bulkhead pattern applied
- [ ] P2: Graceful degradation on model failures

### Verification Steps

1. Review retry policy in code.
2. Confirm timeout values.
3. Test circuit breaker transitions.
4. Simulate downstream failures.

### Circuit Breaker Configuration

- [ ] P0: Circuit breaker on all external APIs
- [ ] P0: Failure threshold defined per dependency
- [ ] P1: Recovery timeout appropriate for SLA
- [ ] P1: Half-open probe behavior tested
- [ ] P2: Circuit breaker metrics exposed

---

## Observability Checklist

- [ ] P0: p50, p95, p99 latency tracked
- [ ] P0: Error rate tracked per endpoint
- [ ] P1: Token usage and cost tracked
- [ ] P1: Cache hit rate tracked
- [ ] P2: Performance dashboards published

### Verification Steps

1. Verify metrics in Grafana or equivalent.
2. Confirm alerts cover warning and critical thresholds.
3. Check that dashboards are shared and up to date.

### Tracing

- [ ] P0: Distributed traces for all requests
- [ ] P0: Trace sampling rate configured
- [ ] P1: Trace includes cache, model, and tool spans
- [ ] P1: Trace errors captured with context
- [ ] P2: Trace data retention policy defined

### Logging

- [ ] P0: Structured log format used
- [ ] P0: Request IDs propagated
- [ ] P1: PII redacted from logs
- [ ] P1: Log levels appropriate for environment
- [ ] P2: Log aggregation configured

---

## Cost Checklist

- [ ] P0: Budget alerts configured
- [ ] P0: Model routing by complexity enabled
- [ ] P1: Cost per request monitored
- [ ] P1: Anomaly detection on spend
- [ ] P2: Monthly cost projections published

### Verification Steps

1. Verify alerting policies.
2. Review routing logs.
3. Inspect spend dashboard.

### Cost Allocation

- [ ] P0: Costs allocated by user or team
- [ ] P0: Cost per model tracked
- [ ] P1: Cost per feature tracked
- [ ] P1: Cost trends analyzed weekly
- [ ] P2: Cost optimization opportunities identified monthly

---

## Security and Privacy Checklist

- [ ] P0: PII redacted from traces
- [ ] P0: TLS enabled for all outbound traffic
- [ ] P1: Secrets not logged
- [ ] P1: Least privilege for service accounts
- [ ] P2: Audit logs retained and reviewed

### Verification Steps

1. Sample traces for PII.
2. Confirm cipher suites.
3. Verify no secrets in logs.

### Data Protection

- [ ] P0: Encryption at rest enabled
- [ ] P0: Data retention policies enforced
- [ ] P1: Data anonymization for analytics
- [ ] P1: Access control lists reviewed
- [ ] P2: Data classification completed

---

## Deployment Checklist

- [ ] P0: Load test passes at 1.5x peak traffic
- [ ] P0: Performance SLOs documented
- [ ] P1: Rollback plan for performance regressions
- [ ] P1: Feature flag for new caching behavior
- [ ] P2: Rollout staged by percentage

### Verification Steps

1. Review load test report.
2. Confirm SLO definitions.
3. Validate feature flag control.

### Canary Deployment

- [ ] P0: Traffic percentage starts at 5%
- [ ] P0: Automatic rollback on error rate increase
- [ ] P1: Performance metrics monitored during rollout
- [ ] P1: Rollback trigger thresholds defined
- [ ] P2: Post-rollout review scheduled

---

## Operational Checklist

- [ ] P0: Alerts routed to on-call
- [ ] P0: Incident runbook for latency spikes
- [ ] P1: Weekly review of performance metrics
- [ ] P1: Monthly capacity planning
- [ ] P2: Quarterly performance regression test suite updated

### Verification Steps

1. Verify alert recipients.
2. Review runbook against recent incidents.
3. Update capacity forecast.

### On-Call Readiness

- [ ] P0: On-call rotation documented
- [ ] P0: Escalation policy defined
- [ ] P1: On-call handbook available
- [ ] P1: war rooms defined for critical incidents
- [ ] P2: Post-incident reviews scheduled

---

## Pre-Deployment Checklist

- [ ] P0: Unit tests pass
- [ ] P0: Integration tests pass
- [ ] P1: Load test passes
- [ ] P1: Security scan passes
- [ ] P2: Documentation updated

### Code Review

- [ ] P0: Performance implications reviewed
- [ ] P0: Timeouts added for external calls
- [ ] P1: Caching strategy appropriate
- [ ] P1: Token usage considered
- [ ] P2: Architecture diagram updated

---

## Post-Deployment Checklist

- [ ] P0: Latency within SLO
- [ ] P0: Error rate within threshold
- [ ] P1: Cache hit rate monitored
- [ ] P1: Cost within budget
- [ ] P2: No memory leaks detected

### Monitoring Validation

- [ ] P0: Metrics appearing in dashboards
- [ ] P0: Alerts firing correctly
- [ ] P1: Trace data complete
- [ ] P1: Log aggregation working
- [ ] P2: Cost tracking accurate

---

## Incident Response Checklist

- [ ] P0: Identify affected users
- [ ] P0: Determine root cause
- [ ] P1: Implement fix
- [ ] P1: Deploy fix with monitoring
- [ ] P2: Conduct post-incident review

### Incident Triage

- [ ] P0: Severity assessed within 15 minutes
- [ ] P0: Communication initiated within 30 minutes
- [ ] P1: Status page updated
- [ ] P1: War room opened if P0
- [ ] P2: Stakeholder updates provided

### Post-Incident

- [ ] P0: Root cause identified
- [ ] P0: Remediation steps documented
- [ ] P1: Follow-up actions assigned
- [ ] P1: Timeline documented
- [ ] P2: Lessons learned shared

---

## Monitoring Setup Checklist

- [ ] P0: Latency metrics collected
- [ ] P0: Error rate metrics collected
- [ ] P1: Token usage metrics collected
- [ ] P1: Cache metrics collected
- [ ] P2: Cost metrics collected

### Metric Definitions

- [ ] P0: Each metric has clear definition
- [ ] P0: Alert thresholds defined
- [ ] P1: Metric owners assigned
- [ ] P1: Metric refresh intervals defined
- [ ] P2: Metric retention policies set

---

## Alert Configuration Checklist

- [ ] P0: Latency alert configured
- [ ] P0: Error rate alert configured
- [ ] P1: Cache hit rate alert configured
- [ ] P1: Cost alert configured
- [ ] P2: Memory usage alert configured

### Alert Routing

- [ ] P0: Alerts routed to correct on-call
- [ ] P0: Escalation paths defined
- [ ] P1: Alert grouping configured
- [ ] P1: Maintenance windows defined
- [ ] P2: Alert suppression rules created

---

## Runbook Checklist

- [ ] P0: Latency spike runbook exists
- [ ] P0: Error rate spike runbook exists
- [ ] P1: Cache failure runbook exists
- [ ] P1: Cost anomaly runbook exists
- [ ] P2: Memory leak investigation runbook exists

### Runbook Quality

- [ ] P0: Runbooks tested quarterly
- [ ] P0: Runbooks include escalation contacts
- [ ] P1: Runbooks include diagnostic steps
- [ ] P1: Runbooks include rollback procedures
- [ ] P2: Runbooks link to relevant dashboards

---

## Capacity Planning Checklist

- [ ] P0: Peak traffic forecasted
- [ ] P0: Resource requirements calculated
- [ ] P1: Scaling policies defined
- [ ] P1: Cost projections updated
- [ ] P2: Infrastructure roadmap reviewed

### Capacity Metrics

- [ ] P0: CPU utilization trends reviewed
- [ ] P0: Memory utilization trends reviewed
- [ ] P1: Network throughput trends reviewed
- [ ] P1: Storage utilization trends reviewed
- [ ] P2: Database connection pool usage reviewed

---

## Vendor Management Checklist

- [ ] P0: Provider contracts reviewed
- [ ] P0: Rate limits documented
- [ ] P1: Fallback providers identified
- [ ] P1: Cost optimization reviewed
- [ ] P2: Multi-cloud strategy evaluated

### Provider Health

- [ ] P0: Provider status page monitored
- [ ] P0: Provider SLAs documented
- [ ] P1: Provider latency tracked
- [ ] P1: Provider error rates tracked
- [ ] P2: Provider incident history reviewed

---

## Documentation Checklist

- [ ] P0: SLOs documented
- [ ] P0: Architecture diagrams updated
- [ ] P1: Runbooks updated
- [ ] P1: API docs updated
- [ ] P2: Performance best practices documented

### Documentation Maintenance

- [ ] P0: Documentation reviewed quarterly
- [ ] P0: Documentation linked from README
- [ ] P1: Documentation versioned with code
- [ ] P1: Documentation feedback channel open
- [ ] P2: Documentation metrics tracked

---

## Training Checklist

- [ ] P0: Team trained on SLOs
- [ ] P0: Team trained on runbooks
- [ ] P1: Team trained on monitoring tools
- [ ] P1: Team trained on incident response
- [ ] P2: Team trained on cost optimization

### Training Program

- [ ] P0: New hire onboarding includes performance basics
- [ ] P0: Quarterly refresher training scheduled
- [ ] P1: Incident simulation exercises quarterly
- [ ] P1: Cross-training on critical components
- [ ] P2: Performance certification program

---

## Tooling Checklist

- [ ] P0: Profiling tools available
- [ ] P0: Tracing tools available
- [ ] P1: Load testing tools available
- [ ] P1: Chaos engineering tools available
- [ ] P2: Cost tracking tools available

### Tool Evaluation

- [ ] P0: Tools evaluated annually
- [ ] P0: Tool licenses maintained
- [ ] P1: Tool integration tested
- [ ] P1: Tool training provided
- [ ] P2: Tool ROI measured

---

## Compliance Checklist

- [ ] P0: PII handling documented
- [ ] P0: Data retention policies defined
- [ ] P1: Audit logging configured
- [ ] P1: Access controls reviewed
- [ ] P2: Security policies updated

### Compliance Monitoring

- [ ] P0: Compliance dashboard created
- [ ] P0: Compliance metrics collected
- [ ] P1: Compliance alerts configured
- [ ] P1: Compliance reports generated monthly
- [ ] P2: Compliance audits conducted quarterly

---

## Backup and Recovery Checklist

- [ ] P0: Backup schedule defined
- [ ] P0: Recovery procedures tested
- [ ] P1: Failure scenarios documented
- [ ] P1: Recovery time objectives defined
- [ ] P2: Disaster recovery plan updated

### Backup Verification

- [ ] P0: Backups verified daily
- [ ] P0: Recovery tested quarterly
- [ ] P1: Backup encryption enabled
- [ ] P1: Backup retention policy enforced
- [ ] P2: Backup cost optimized

---

## Testing Checklist

- [ ] P0: Unit tests pass
- [ ] P0: Integration tests pass
- [ ] P1: Performance tests pass
- [ ] P1: Chaos tests pass
- [ ] P2: Penetration tests pass

### Test Coverage

- [ ] P0: Critical paths covered
- [ ] P0: Error handling tested
- [ ] P1: Edge cases covered
- [ ] P1: Performance regressions tested
- [ ] P2: Security tests included

---

## Release Checklist

- [ ] P0: Code review completed
- [ ] P0: Tests passing
- [ ] P1: Staging validated
- [ ] P1: Rollback plan documented
- [ ] P2: Change management approved

### Release Readiness

- [ ] P0: Performance impact assessed
- [ ] P0: Monitoring validated
- [ ] P1: Rollback tested
- [ ] P1: Communication plan ready
- [ ] P2: Post-release review scheduled

---

## Communication Checklist

- [ ] P0: Stakeholders informed
- [ ] P0: Customers notified of changes
- [ ] P1: Internal teams briefed
- [ ] P1: Status page updated
- [ ] P2: Post-release summary published

### Stakeholder Communication

- [ ] P0: Executive summary prepared
- [ ] P0: Timeline communicated
- [ ] P1: Risk assessment shared
- [ ] P1: Success criteria defined
- [ ] P2: Feedback collected

---

## Budget Checklist

- [ ] P0: Monthly budget reviewed
- [ ] P0: Cost variances explained
- [ ] P1: Cost optimization opportunities identified
- [ ] P1: Vendor contracts reviewed
- [ ] P2: Annual budget forecast updated

### Financial Planning

- [ ] P0: Quarterly forecasts updated
- [ ] P0: Actual vs planned reviewed
- [ ] P1: Cost attribution refined
- [ ] P1: Optimization ROI calculated
- [ ] P2: Budget scenarios planned

---

## Team Checklist

- [ ] P0: Roles and responsibilities defined
- [ ] P0: On-call rotation established
- [ ] P1: Team training scheduled
- [ ] P1: Knowledge base maintained
- [ ] P2: Team feedback collected

### Team Development

- [ ] P0: Skills matrix updated
- [ ] P0: Mentorship program active
- [ ] P1: Career development plans
- [ ] P1: Performance reviews conducted
- [ ] P2: Team satisfaction surveyed

---

## Risk Management Checklist

- [ ] P0: Risks identified
- [ ] P0: Mitigation strategies defined
- [ ] P1: Risk owners assigned
- [ ] P1: Risk reviews scheduled
- [ ] P2: Risk register maintained

### Risk Assessment

- [ ] P0: Technical risks reviewed
- [ ] P0: Operational risks reviewed
- [ ] P1: Compliance risks reviewed
- [ ] P1: Business risks reviewed
- [ ] P2: Emerging risks identified

---

## Performance Budget Checklist

- [ ] P0: Performance budgets defined
- [ ] P0: Budget thresholds documented
- [ ] P1: Budget tracking implemented
- [ ] P1: Budget alerts configured
- [ ] P2: Budget reviews scheduled

### Budget Enforcement

- [ ] P0: SLOs enforced in CI/CD
- [ ] P0: Budget gates in deployment pipeline
- [ ] P1: Performance budgets in RFCs
- [ ] P1: Budget variance alerts
- [ ] P2: Budget optimization targets set

---

## Load Testing Checklist

- [ ] P0: Load test environment ready
- [ ] P0: Load test scenarios defined
- [ ] P1: Load test executed
- [ ] P1: Load test results documented
- [ ] P2: Load test reports generated

### Test Execution

- [ ] P0: Baseline performance established
- [ ] P0: Load test covers peak traffic
- [ ] P1: Stress test identifies breaking points
- [ ] P1: Soak test runs for 24 hours
- [ ] P2: Spike test simulates traffic surges

---

## Chaos Engineering Checklist

- [ ] P0: Chaos experiments defined
- [ ] P0: Chaos experiments executed
- [ ] P1: Chaos experiment results documented
- [ ] P1: Improvements identified
- [ ] P2: Chaos engineering process established

### Experiment Design

- [ ] P0: Blast radius controlled
- [ ] P0: Rollback plan defined
- [ ] P1: Success criteria defined
- [ ] P1: Monitoring validated
- [ ] P2: Experiment automation enabled

---

## Reliability Checklist

- [ ] P0: SLOs defined and documented
- [ ] P0: SLO monitoring implemented
- [ ] P1: Error budgets defined
- [ ] P1: Error budget alerts configured
- [ ] P2: Reliability reviews scheduled

### SLO Management

- [ ] P0: SLOs aligned with business needs
- [ ] P0: SLO burn rate monitored
- [ ] P1: SLO reviews monthly
- [ ] P1: SLO adjustments documented
- [ ] P2: SLO training for all teams

---

## Scalability Checklist

- [ ] P0: Scalability requirements defined
- [ ] P0: Scalability tests executed
- [ ] P1: Scaling policies implemented
- [ ] P1: Autoscaling configured
- [ ] P2: Scalability roadmap established

### Scaling Strategy

- [ ] P0: Horizontal scaling preferred
- [ ] P0: Stateless design enforced
- [ ] P1: Database scaling planned
- [ ] P1: Cache scaling planned
- [ ] P2: Global distribution considered

---

## Capacity Planning Checklist

- [ ] P0: Current capacity assessed
- [ ] P0: Future capacity projected
- [ ] P1: Capacity gaps identified
- [ ] P1: Capacity improvements planned
- [ ] P2: Capacity reviews scheduled

### Forecasting

- [ ] P0: Growth trends analyzed
- [ ] P0: Seasonal patterns considered
- [ ] P1: Capacity headroom maintained
- [ ] P1: Procurement timeline planned
- [ ] P2: Cost projections shared

---

## Performance Tuning Checklist

- [ ] P0: Performance metrics collected
- [ ] P0: Performance bottlenecks identified
- [ ] P1: Performance improvements implemented
- [ ] P1: Performance improvements tested
- [ ] P2: Performance tuning process established

### Tuning Process

- [ ] P0: Profile before optimizing
- [ ] P0: One change at a time
- [ ] P1: Impact measured after each change
- [ ] P1: Benchmarks updated
- [ ] P2: Performance debt tracked

---

## Query Optimization Checklist

- [ ] P0: Query performance analyzed
- [ ] P0: Slow queries identified
- [ ] P1: Query optimizations implemented
- [ ] P1: Query performance monitored
- [ ] P2: Query optimization process established

### Database Performance

- [ ] P0: Indexes on frequent queries
- [ ] P0: Query plans reviewed
- [ ] P1: Query caching enabled
- [ ] P1: Connection pooling configured
- [ ] P2: Database sharding evaluated

---

## Index Optimization Checklist

- [ ] P0: Index usage analyzed
- [ ] P0: Missing indexes identified
- [ ] P1: Index optimizations implemented
- [ ] P1: Index performance monitored
- [ ] P2: Index optimization process established

### Index Maintenance

- [ ] P0: Index fragmentation monitored
- [ ] P0: Index rebuilds scheduled
- [ ] P1: Index statistics updated
- [ ] P1: Index usage tracked
- [ ] P2: Index consolidation evaluated

---

## Database Optimization Checklist

- [ ] P0: Database performance analyzed
- [ ] P0: Database bottlenecks identified
- [ ] P1: Database optimizations implemented
- [ ] P1: Database performance monitored
- [ ] P2: Database optimization process established

### Database Configuration

- [ ] P0: Memory allocation optimized
- [ ] P0: Disk I/O optimized
- [ ] P1: Connection limits tuned
- [ ] P1: Query cache configured
- [ ] P2: Read replicas considered

---

## Connection Management Checklist

- [ ] P0: Connection pools configured
- [ ] P0: Connection limits set
- [ ] P1: Connection monitoring implemented
- [ ] P1: Connection optimizations applied
- [ ] P2: Connection management reviewed

### Connection Health

- [ ] P0: Connection timeout configured
- [ ] P0: Connection retry policy defined
- [ ] P1: Connection leak detection enabled
- [ ] P1: Connection metrics collected
- [ ] P2: Connection pooling library updated

---

## Thread Management Checklist

- [ ] P0: Thread pools configured
- [ ] P0: Thread limits set
- [ ] P1: Thread monitoring implemented
- [ ] P1: Thread optimizations applied
- [ ] P2: Thread management reviewed

### Thread Safety

- [ ] P0: Shared resources protected
- [ ] P0: Deadlock prevention implemented
- [ ] P1: Thread contention monitored
- [ ] P1: Lock-free algorithms considered
- [ ] P2: Thread profiling enabled

---

## Memory Management Checklist

- [ ] P0: Memory usage monitored
- [ ] P0: Memory limits configured
- [ ] P1: Memory optimizations implemented
- [ ] P1: Memory leaks identified and fixed
- [ ] P2: Memory management reviewed

### Memory Optimization

- [ ] P0: Garbage collection tuned
- [ ] P0: Object pooling implemented
- [ ] P1: Memory profiling enabled
- [ ] P1: Large object handling optimized
- [ ] P2: Memory allocation patterns analyzed

---

## CPU Management Checklist

- [ ] P0: CPU usage monitored
- [ ] P0: CPU limits set
- [ ] P1: CPU optimizations implemented
- [ ] P1: CPU-intensive tasks optimized
- [ ] P2: CPU management reviewed

### CPU Optimization

- [ ] P0: CPU profiling enabled
- [ ] P0: Hot paths identified
- [ ] P1: Algorithm optimization applied
- [ ] P1: Parallelization opportunities found
- [ ] P2: CPU affinity configured

---

## Network Optimization Checklist

- [ ] P0: Network usage monitored
- [ ] P0: Network optimizations applied
- [ ] P1: Network bottlenecks identified
- [ ] P1: Network improvements implemented
- [ ] P2: Network management reviewed

### Network Performance

- [ ] P0: Latency optimized
- [ ] P0: Throughput maximized
- [ ] P1: Packet loss monitored
- [ ] P1: Bandwidth utilization tracked
- [ ] P2: CDN configuration optimized

---

## API Optimization Checklist

- [ ] P0: API performance analyzed
- [ ] P0: API bottlenecks identified
- [ ] P1: API optimizations implemented
- [ ] P1: API performance monitored
- [ ] P2: API optimization process established

### API Best Practices

- [ ] P0: Response size limited
- [ ] P0: Pagination implemented
- [ ] P1: Compression enabled
- [ ] P1: Caching headers set
- [ ] P2: API versioning strategy

---

## Service Mesh Optimization Checklist

- [ ] P0: Service mesh configuration reviewed
- [ ] P0: Service mesh performance analyzed
- [ ] P1: Service mesh optimizations applied
- [ ] P1: Service mesh monitoring implemented
- [ ] P2: Service mesh optimization process established

### Mesh Configuration

- [ ] P0: Sidecar proxies sized correctly
- [ ] P0: Traffic splitting configured
- [ ] P1: Circuit breakers in mesh
- [ ] P1: Retries configured in mesh
- [ ] P2: Mesh telemetry optimized

---

## Container Optimization Checklist

- [ ] P0: Container configuration reviewed
- [ ] P0: Container resource limits set
- [ ] P1: Container optimizations implemented
- [ ] P1: Container performance monitored
- [ ] P2: Container optimization process established

### Container Best Practices

- [ ] P0: Base image size minimized
- [ ] P0: Multi-stage builds used
- [ ] P1: Resource limits enforced
- [ ] P1: Health checks configured
- [ ] P2: Image vulnerability scanning

---

## Orchestration Optimization Checklist

- [ ] P0: Orchestration configuration reviewed
- [ ] P0: Orchestration performance analyzed
- [ ] P1: Orchestration optimizations applied
- [ ] P1: Orchestration monitoring implemented
- [ ] P2: Orchestration optimization process established

### Kubernetes Optimization

- [ ] P0: Node pools sized correctly
- [ ] P0: Pod disruption budgets set
- [ ] P1: HPA configured
- [ ] P1: VPA enabled if appropriate
- [ ] P2: Cluster autoscaling enabled

---

## Infrastructure Optimization Checklist

- [ ] P0: Infrastructure configuration reviewed
- [ ] P0: Infrastructure performance analyzed
- [ ] P1: Infrastructure optimizations applied
- [ ] P1: Infrastructure monitoring implemented
- [ ] P2: Infrastructure optimization process established

### Cloud Optimization

- [ ] P0: Right-sizing applied
- [ ] P0: Reserved instances purchased
- [ ] P1: Spot instances for non-critical
- [ ] P1: Auto-scaling configured
- [ ] P2: Cost allocation tags applied

---

## Cloud Optimization Checklist

- [ ] P0: Cloud configuration reviewed
- [ ] P0: Cloud costs analyzed
- [ ] P1: Cloud optimizations applied
- [ ] P1: Cloud cost monitoring implemented
- [ ] P2: Cloud optimization process established

### Cost Management

- [ ] P0: Budgets and alerts set
- [ ] P0: Unused resources identified
- [ ] P1: Savings plans evaluated
- [ ] P1: Resource tagging enforced
- [ ] P2: Multi-cloud strategy reviewed

---

## Edge Computing Optimization Checklist

- [ ] P0: Edge configuration reviewed
- [ ] P0: Edge performance analyzed
- [ ] P1: Edge optimizations applied
- [ ] P1: Edge monitoring implemented
- [ ] P2: Edge optimization process established

### Edge Architecture

- [ ] P0: Edge locations selected
- [ ] P0: Cache invalidation strategy
- [ ] P1: Edge computing logic defined
- [ ] P1: Edge failure handling
- [ ] P2: Edge cost analysis

---

## CDN Optimization Checklist

- [ ] P0: CDN configuration reviewed
- [ ] P0: CDN performance analyzed
- [ ] P1: CDN optimizations applied
- [ ] P1: CDN monitoring implemented
- [ ] P2: CDN optimization process established

### CDN Configuration

- [ ] P0: Cache headers configured
- [ ] P0: TTL values optimized
- [ ] P1: Compression enabled
- [ ] P1: Image optimization applied
- [ ] P2: CDN purge automation

---

## Load Balancer Optimization Checklist

- [ ] P0: Load balancer configuration reviewed
- [ ] P0: Load balancer performance analyzed
- [ ] P1: Load balancer optimizations applied
- [ ] P1: Load balancer monitoring implemented
- [ ] P2: Load balancer optimization process established

### Load Balancing

- [ ] P0: Algorithm selected for use case
- [ ] P0: Health checks configured
- [ ] P1: Session affinity if needed
- [ ] P1: SSL termination optimized
- [ ] P2: Global load balancing considered

---

## Security Optimization Checklist

- [ ] P0: Security configuration reviewed
- [ ] P0: Security performance analyzed
- [ ] P1: Security optimizations applied
- [ ] P1: Security monitoring implemented
- [ ] P2: Security optimization process established

### Security Best Practices

- [ ] P0: TLS 1.3 enabled
- [ ] P0: Cipher suites hardened
- [ ] P1: Certificate rotation automated
- [ ] P1: DDoS protection enabled
- [ ] P2: Security scanning automated

---

## Compliance Checklist

- [ ] P0: Compliance requirements documented
- [ ] P0: Compliance audits conducted
- [ ] P1: Compliance improvements implemented
- [ ] P1: Compliance monitoring configured
- [ ] P2: Compliance reviews scheduled

### Regulatory Compliance

- [ ] P0: GDPR requirements met
- [ ] P0: Data residency enforced
- [ ] P1: Right to deletion implemented
- [ ] P1: Consent management in place
- [ ] P2: Privacy impact assessment

---

## Disaster Recovery Checklist

- [ ] P0: Disaster recovery plan documented
- [ ] P0: Disaster recovery tests conducted
- [ ] P1: Disaster recovery improvements implemented
- [ ] P1: Disaster recovery monitoring configured
- [ ] P2: Disaster recovery reviews scheduled

### DR Testing

- [ ] P0: Failover tested quarterly
- [ ] P0: Recovery time measured
- [ ] P1: Recovery point objective defined
- [ ] P1: Backup restoration tested
- [ ] P2: Disaster simulation exercises

---

## Backup Checklist

- [ ] P0: Backup schedule defined
- [ ] P0: Recovery procedures tested
- [ ] P1: Failure scenarios documented
- [ ] P1: Recovery time objectives defined
- [ ] P2: Disaster recovery plan updated

### Backup Strategy

- [ ] P0: 3-2-1 backup rule followed
- [ ] P0: Backup encryption enabled
- [ ] P1: Incremental backups implemented
- [ ] P1: Cross-region replication
- [ ] P2: Backup verification automated

---

## Data Management Checklist

- [ ] P0: Data storage reviewed
- [ ] P0: Data lifecycle managed
- [ ] P1: Data optimization applied
- [ ] P1: Data monitoring implemented
- [ ] P2: Data management reviewed

### Data Governance

- [ ] P0: Data catalog maintained
- [ ] P0: Data quality monitored
- [ ] P1: Data lineage tracked
- [ ] P1: Data retention enforced
- [ ] P2: Data mesh architecture considered

---

## API Gateway Checklist

- [ ] P0: API gateway configuration reviewed
- [ ] P0: API gateway performance analyzed
- [ ] P1: API gateway optimizations applied
- [ ] P1: API gateway monitoring implemented
- [ ] P2: API gateway optimization process established

### Gateway Features

- [ ] P0: Rate limiting configured
- [ ] P0: Authentication enforced
- [ ] P1: Request/response transformation
- [ ] P1: API versioning supported
- [ ] P2: Developer portal enabled

---

## Service Discovery Checklist

- [ ] P0: Service discovery configuration reviewed
- [ ] P0: Service discovery performance analyzed
- [ ] P1: Service discovery optimizations applied
- [ ] P1: Service discovery monitoring implemented
- [ ] P2: Service discovery optimization process established

### Discovery Health

- [ ] P0: Service registry healthy
- [ ] P0: Health checks passing
- [ ] P1: Service mesh integrated
- [ ] P1: DNS caching optimized
- [ ] P2: Service dependency mapping

---

## Message Queue Optimization Checklist

- [ ] P0: Message queue configuration reviewed
- [ ] P0: Message queue performance analyzed
- [ ] P1: Message queue optimizations applied
- [ ] P1: Message queue monitoring implemented
- [ ] P2: Message queue optimization process established

### Queue Configuration

- [ ] P0: Queue depth monitored
- [ ] P0: Consumer lag tracked
- [ ] P1: Partition count optimized
- [ ] P1: Batch size tuned
- [ ] P2: Dead letter queues configured

---

## Event Streaming Checklist

- [ ] P0: Event streaming configuration reviewed
- [ ] P0: Event streaming performance analyzed
- [ ] P1: Event streaming optimizations applied
- [ ] P1: Event streaming monitoring implemented
- [ ] P2: Event streaming optimization process established

### Streaming Best Practices

- [ ] P0: Topic partitioning strategy
- [ ] P0: Retention policies defined
- [ ] P1: Consumer groups optimized
- [ ] P1: Exactly-once semantics if needed
- [ ] P2: Schema registry used

---

## Logging Optimization Checklist

- [ ] P0: Logging configuration reviewed
- [ ] P0: Logging performance analyzed
- [ ] P1: Logging optimizations applied
- [ ] P1: Logging monitoring implemented
- [ ] P2: Logging optimization process established

### Log Management

- [ ] P0: Log levels appropriate
- [ ] P0: Structured logging used
- [ ] P1: Log sampling for high volume
- [ ] P1: Log aggregation configured
- [ ] P2: Log retention policies enforced

---

## Metrics Collection Checklist

- [ ] P0: Metrics configuration reviewed
- [ ] P0: Metrics performance analyzed
- [ ] P1: Metrics optimizations applied
- [ ] P1: Metrics monitoring implemented
- [ ] P2: Metrics optimization process established

### Metrics Strategy

- [ ] P0: RED metrics collected
- [ ] P0: USE metrics collected
- [ ] P1: Custom business metrics defined
- [ ] P1: Metric cardinality limits enforced
- [ ] P2: Metric correlation enabled

---

## Tracing Optimization Checklist

- [ ] P0: Tracing configuration reviewed
- [ ] P0: Tracing performance analyzed
- [ ] P1: Tracing optimizations applied
- [ ] P1: Tracing monitoring implemented
- [ ] P2: Tracing optimization process established

### Trace Quality

- [ ] P0: 100% of errors traced
- [ ] P0: Sample rate configured for load
- [ ] P1: Baggage propagation enabled
- [ ] P1: Trace context injected
- [ ] P2: Trace analysis automated

---

## Alerting Optimization Checklist

- [ ] P0: Alert configuration reviewed
- [ ] P0: Alert performance analyzed
- [ ] P1: Alert optimizations applied
- [ ] P1: Alert monitoring implemented
- [ ] P2: Alert optimization process established

### Alert Quality

- [ ] P0: Actionable alerts only
- [ ] P0: Alert severity levels defined
- [ ] P1: Alert noise reduced
- [ ] P1: Alert correlation enabled
- [ ] P2: Alert fatigue monitored

---

## Dashboard Optimization Checklist

- [ ] P0: Dashboard configuration reviewed
- [ ] P0: Dashboard performance analyzed
- [ ] P1: Dashboard optimizations applied
- [ ] P1: Dashboard monitoring implemented
- [ ] P2: Dashboard optimization process established

### Dashboard Design

- [ ] P0: Key metrics visible in 5 seconds
- [ ] P0: Drill-down paths defined
- [ ] P1: Real-time updates configured
- [ ] P1: Dashboard sharing enabled
- [ ] P2: Mobile-responsive design

---

## Documentation Review Checklist

- [ ] P0: Documentation current
- [ ] P0: Documentation linked
- [ ] P1: Documentation accurate
- [ ] P1: Examples working
- [ ] P2: Feedback incorporated

### Documentation Standards

- [ ] P0: README present and complete
- [ ] P0: API docs generated
- [ ] P1: Architecture diagrams current
- [ ] P1: Runbooks tested
- [ ] P2: Glossary maintained

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
