# Deployment Checklist for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [P0 - Critical Checks](#p0---critical-checks)
3. [P1 - High Priority Checks](#p1---high-priority-checks)
4. [P2 - Medium Priority Checks](#p2---medium-priority-checks)
5. [P3 - Low Priority Checks](#p3---low-priority-checks)
6. [Pre-Deployment Phase](#pre-deployment-phase)
7. [Deployment Phase](#deployment-phase)
8. [Post-Deployment Phase](#post-deployment-phase)
9. [Rollback Checklist](#rollback-checklist)
10. [LLM-Specific Checks](#llm-specific-checks)
11. [Infrastructure Checks](#infrastructure-checks)
12. [Security Checks](#security-checks)
13. [Performance Checks](#performance-checks)
14. [Communication Checklist](#communication-checklist)
15. [Summary](#summary)

---

## Overview

This checklist ensures all critical aspects of deployment are covered before, during, and after releasing AI/LLM systems to production. Use this checklist to minimize risk and ensure reliable deployments.

### Priority Levels

- **P0**: Critical - Must pass before deployment can proceed
- **P1**: High - Should be completed but may have workarounds
- **P2**: Medium - Important but not blocking
- **P3**: Low - Nice to have, can be addressed post-deployment

### Checklist Usage Guidelines

```
Before Deployment:
  1. Complete all P0 checks
  2. Complete as many P1 checks as possible
  3. Note any P2/P3 items for post-deployment

During Deployment:
  1. Follow deployment phase checklist
  2. Monitor metrics continuously
  3. Be ready to execute rollback checklist

After Deployment:
  1. Complete post-deployment verification
  2. Monitor for 24 hours
  3. Document any issues encountered
```

---

## P0 - Critical Checks

### Code Quality

- [ ] All unit tests pass (`pytest tests/unit/ -v`)
- [ ] Code coverage meets minimum threshold (≥80%)
- [ ] No critical or high-severity security vulnerabilities (`trivy image --severity HIGH,CRITICAL`)
- [ ] Code has been reviewed and approved by at least one team member
- [ ] No merge conflicts with main branch
- [ ] No TODO/FIXME comments in critical paths
- [ ] No debug code or console.log statements in production code
- [ ] All type hints are correct (if using typed language)
- [ ] No hardcoded values that should be configurable
- [ ] Code follows team style guidelines

### Build Verification

- [ ] Docker image builds successfully
- [ ] Docker image size is within acceptable limits (<2GB)
- [ ] All dependencies are correctly installed
- [ ] No deprecated or vulnerable dependencies
- [ ] Build artifacts are pushed to registry
- [ ] Image tags are correct and follow naming convention
- [ ] Multi-stage build is optimized
- [ ] No secrets embedded in image layers
- [ ] Base image is from trusted source
- [ ] Image metadata is correct (labels, annotations)

### Configuration

- [ ] All environment variables are configured correctly
- [ ] Secrets are properly managed (not hardcoded)
- [ ] Configuration matches target environment requirements
- [ ] Database migrations are backward compatible
- [ ] Feature flags are configured as intended
- [ ] ConfigMaps are updated with latest configuration
- [ ] Secrets are rotated if needed
- [ ] Environment-specific overrides are correct
- [ ] Configuration validation passes
- [ ] No configuration drift from previous deployment

### Health Checks

- [ ] Liveness probe endpoint responds correctly
- [ ] Readiness probe endpoint responds correctly
- [ ] Startup probe endpoint responds correctly
- [ ] Health check timeout is appropriate
- [ ] Health check interval is appropriate
- [ ] Health checks validate all critical dependencies
- [ ] Health check response includes version information
- [ ] Health check logs are informative
- [ ] Health check metrics are exposed
- [ ] Health check alerts are configured

---

## P1 - High Priority Checks

### Testing

- [ ] Integration tests pass
- [ ] API contract tests pass
- [ ] Load tests meet performance requirements
- [ ] Smoke tests pass in staging environment
- [ ] End-to-end tests pass
- [ ] Regression tests pass
- [ ] Security tests pass
- [ ] Chaos tests pass (if applicable)
- [ ] Data migration tests pass
- [ ] Failover tests pass

### Monitoring

- [ ] Monitoring dashboards are updated
- [ ] Alert rules are configured and tested
- [ ] Log aggregation is working correctly
- [ ] Tracing is configured and working
- [ ] Metrics collection is enabled
- [ ] Alert notifications are sent to correct channels
- [ ] Runbooks are linked to alerts
- [ ] Dashboard panels are not broken
- [ ] Metrics retention is configured
- [ ] Log retention is configured

### Security

- [ ] SSL/TLS certificates are valid and not expiring soon
- [ ] API keys and tokens are rotated if needed
- [ ] Access controls are properly configured
- [ ] Audit logging is enabled
- [ ] Security scanning has been performed
- [ ] Network policies are configured
- [ ] Pod security policies are in place
- [ ] RBAC roles are correctly assigned
- [ ] Secrets are encrypted at rest
- [ ] Secrets are encrypted in transit

### Infrastructure

- [ ] Required infrastructure resources are provisioned
- [ ] Resource limits are set appropriately
- [ ] Network policies are configured
- [ ] Storage volumes are mounted correctly
- [ ] GPU resources are available (if required)
- [ ] Load balancers are configured correctly
- [ ] DNS records are updated (if needed)
- [ ] CDN configuration is correct (if applicable)
- [ ] Auto-scaling is configured
- [ ] Pod disruption budgets are set

---

## P2 - Medium Priority Checks

### Documentation

- [ ] Deployment runbook is updated
- [ ] API documentation is current
- [ ] Change log is updated
- [ ] Architecture diagram is updated
- [ ] Known issues are documented
- [ ] Rollback procedures are documented
- [ ] Contact information is current
- [ ] Escalation paths are documented
- [ ] Post-mortem template is ready
- [ ] Lessons learned are captured

### Performance

- [ ] Response time meets SLA requirements
- [ ] Throughput meets expected load
- [ ] Memory usage is within acceptable limits
- [ ] CPU usage is within acceptable limits
- [ ] GPU utilization is optimized
- [ ] Database connection pools are sized correctly
- [ ] Cache hit rates are acceptable
- [ ] Query performance is optimized
- [ ] Network latency is acceptable
- [ ] Disk I/O is within limits

### Backup

- [ ] Database backups are configured
- [ ] Backup restoration has been tested
- [ ] Backup retention policy is configured
- [ ] Off-site backup is enabled (if required)
- [ ] Backup monitoring is in place
- [ ] Backup encryption is enabled
- [ ] Backup verification is automated
- [ ] Point-in-time recovery is tested
- [ ] Cross-region backup is configured (if needed)
- [ ] Backup alerts are configured

---

## P3 - Low Priority Checks

### Optimization

- [ ] Code profiling has been performed
- [ ] Bottlenecks have been identified
- [ ] Caching strategies are optimized
- [ ] Database queries are optimized
- [ ] API responses are compressed
- [ ] Image layers are optimized
- [ ] Startup time is minimized
- [ ] Memory footprint is reduced
- [ ] CPU utilization is optimized
- [ ] Network traffic is minimized

### Accessibility

- [ ] API endpoints are documented
- [ ] Error messages are user-friendly
- [ ] Rate limiting is configured
- [ ] API versioning is implemented
- [ ] Deprecation notices are in place
- [ ] SDKs are updated (if applicable)
- [ ] Client libraries are compatible
- [ ] Migration guides are provided
- [ ] Backward compatibility is maintained
- [ ] Forward compatibility is considered

### Cleanup

- [ ] Temporary files are cleaned up
- [ ] Unused dependencies are removed
- [ ] Debug code is removed
- [ ] Console logs are removed
- [ ] TODO comments are addressed
- [ ] Old Docker images are pruned
- [ ] Unused ConfigMaps are removed
- [ ] Unused Secrets are removed
- [ ] Old Deployments are cleaned up
- [ ] Namespace is tidy

---

## Pre-Deployment Phase

### Code Freeze

- [ ] Code freeze has been announced
- [ ] All feature branches are merged
- [ ] No pending pull requests
- [ ] Release branch is created (if applicable)
- [ ] Version number is updated
- [ ] Changelog is updated
- [ ] Release notes are drafted
- [ ] Stakeholders are notified of freeze
- [ ] CI/CD pipeline is clear
- [ ] No conflicting deployments scheduled

### Build and Test

- [ ] Build is triggered and successful
- [ ] All automated tests pass
- [ ] Manual testing is completed (if required)
- [ ] Performance benchmarks are met
- [ ] Security scan is clean
- [ ] Dependency scan is clean
- [ ] License compliance is verified
- [ ] Container scan is clean
- [ ] Infrastructure scan is clean
- [ ] Code quality metrics are acceptable

### Staging Deployment

- [ ] Staging environment is clean
- [ ] Staging deployment is successful
- [ ] Smoke tests pass in staging
- [ ] Integration tests pass in staging
- [ ] Load tests pass in staging
- [ ] Staging configuration matches production
- [ ] Staging data is representative
- [ ] Staging monitoring is active
- [ ] Staging alerts are configured
- [ ] Staging access is available for team

### Approval

- [ ] Technical lead approval received
- [ ] Product owner approval received (if required)
- [ ] Security team approval received (if required)
- [ ] Change management approval received (if required)
- [ ] Deployment window is confirmed
- [ ] On-call engineer is notified
- [ ] Support team is notified
- [ ] Customer success is notified (if applicable)
- [ ] Leadership is informed (for major releases)
- [ ] All approvers are available during deployment

---

## Deployment Phase

### Pre-Deployment

- [ ] Notify team of deployment start
- [ ] Verify no conflicting deployments
- [ ] Verify infrastructure is healthy
- [ ] Verify monitoring is active
- [ ] Verify rollback plan is ready
- [ ] Verify database backups are current
- [ ] Verify feature flags are configured
- [ ] Verify secrets are available
- [ ] Verify network connectivity
- [ ] Verify DNS is correct

### Deployment Execution

- [ ] Deploy to canary (5% traffic)
- [ ] Monitor canary metrics for 5 minutes
- [ ] Deploy to 20% traffic
- [ ] Monitor metrics for 10 minutes
- [ ] Deploy to 50% traffic
- [ ] Monitor metrics for 15 minutes
- [ ] Deploy to 100% traffic
- [ ] Verify all pods are running
- [ ] Verify health checks are passing
- [ ] Verify no error spikes

### Post-Deployment Verification

- [ ] All pods are running and healthy
- [ ] Health checks are passing
- [ ] No error spikes in logs
- [ ] Response times are within SLA
- [ ] Throughput meets expected load
- [ ] Database connections are stable
- [ ] Cache is warming up
- [ ] Metrics are flowing correctly
- [ ] Alerts are not firing
- [ ] User feedback is positive

---

## Post-Deployment Phase

### Immediate Verification (0-15 minutes)

- [ ] All services are responding
- [ ] No error alerts have fired
- [ ] Key metrics are stable
- [ ] User feedback is positive
- [ ] No support tickets related to deployment
- [ ] Database queries are performing well
- [ ] Cache hit rates are acceptable
- [ ] Memory usage is stable
- [ ] CPU usage is stable
- [ ] Network traffic is normal

### Short-term Verification (15-60 minutes)

- [ ] Performance metrics are stable
- [ ] Error rates are within acceptable limits
- [ ] Resource utilization is normal
- [ ] No memory leaks detected
- [ ] No connection pool exhaustion
- [ ] Database replication is healthy
- [ ] Cache invalidation is working
- [ ] Background jobs are processing
- [ ] Scheduled tasks are running
- [ ] Monitoring dashboards are accurate

### Long-term Verification (1-24 hours)

- [ ] System stability is maintained
- [ ] No delayed errors or issues
- [ ] User satisfaction is maintained
- [ ] Cost metrics are within budget
- [ ] Compliance requirements are met
- [ ] No security incidents
- [ ] No data integrity issues
- [ ] No performance degradation
- [ ] No unexpected behavior
- [ ] All SLAs are met

### Communication

- [ ] Deployment success announced to team
- [ ] Release notes are published
- [ ] Stakeholders are notified
- [ ] Documentation is updated
- [ ] Lessons learned are captured
- [ ] Customer success is informed
- [ ] Support team is updated
- [ ] Leadership is informed (for major releases)
- [ ] Blog post is published (if applicable)
- [ ] Social media is updated (if applicable)

---

## Rollback Checklist

### Rollback Triggers

- [ ] Error rate exceeds 5% for more than 5 minutes
- [ ] Response time exceeds SLA for more than 5 minutes
- [ ] Critical functionality is broken
- [ ] Security vulnerability is detected
- [ ] Data integrity issues are detected
- [ ] Health checks are failing
- [ ] Resource exhaustion is detected
- [ ] Dependency failures are detected
- [ ] User complaints exceed threshold
- [ ] Business metrics are impacted

### Rollback Execution

- [ ] Rollback decision is made
- [ ] Rollback command is executed
- [ ] Rollback is verified
- [ ] Traffic is routed to previous version
- [ ] Monitoring confirms rollback success
- [ ] Database changes are reverted (if needed)
- [ ] Feature flags are toggled (if applicable)
- [ ] Cache is invalidated (if needed)
- [ ] DNS is updated (if needed)
- [ ] CDN is purged (if needed)

### Post-Rollback

- [ ] Root cause is identified
- [ ] Fix is developed and tested
- [ ] Deployment is retried with fix
- [ ] Documentation is updated
- [ ] Team is debriefed
- [ ] Post-mortem is scheduled
- [ ] Action items are assigned
- [ ] Follow-up deployment is planned
- [ ] Stakeholders are informed
- [ ] Lessons learned are captured

---

## LLM-Specific Checks

### Model Verification

- [ ] Model version is correct
- [ ] Model is loaded successfully
- [ ] Model inference is working
- [ ] Model performance meets requirements
- [ ] Model memory usage is acceptable
- [ ] Model latency is acceptable
- [ ] Model accuracy is verified
- [ ] Model fallback is configured
- [ ] Model caching is working
- [ ] Model updates are rolling out correctly

### GPU Resources

- [ ] GPU is available on nodes
- [ ] GPU drivers are correct version
- [ ] CUDA version is compatible
- [ ] GPU memory is sufficient
- [ ] GPU utilization is monitored
- [ ] GPU errors are logged
- [ ] GPU alerts are configured
- [ ] GPU failover is tested
- [ ] GPU scaling is configured
- [ ] GPU costs are tracked

### Inference Pipeline

- [ ] Tokenizer is working correctly
- [ ] Prompt template is correct
- [ ] Response format is correct
- [ ] Error handling is robust
- [ ] Rate limiting is configured
- [ ] Timeout is configured
- [ ] Retry logic is implemented
- [ ] Circuit breaker is configured
- [ ] Fallback responses are ready
- [ ] Logging is comprehensive

---

## Infrastructure Checks

### Kubernetes

- [ ] Cluster is healthy
- [ ] Nodes are ready
- [ ] Pods are scheduled correctly
- [ ] Services are reachable
- [ ] Ingress is configured
- [ ] Certificates are valid
- [ ] Network policies are in place
- [ ] Resource quotas are set
- [ ] Limit ranges are configured
- [ ] RBAC is correct

### Database

- [ ] Database is accessible
- [ ] Migrations are applied
- [ ] Connections are pooling correctly
- [ ] Replication is healthy
- [ ] Backups are current
- [ ] Monitoring is active
- [ ] Alerts are configured
- [ ] Performance is acceptable
- [ ] Storage is sufficient
- [ ] Security is configured

### Cache

- [ ] Redis is accessible
- [ ] Memory is sufficient
- [ ] Persistence is configured
- [ ] Replication is healthy
- [ ] Eviction policy is correct
- [ ] Monitoring is active
- [ ] Alerts are configured
- [ ] Security is configured
- [ ] Backup is configured
- [ ] Failover is tested

---

## Security Checks

### Authentication

- [ ] API keys are valid
- [ ] Tokens are not expired
- [ ] OAuth flows are working
- [ ] SSO is configured correctly
- [ ] MFA is enforced (if required)
- [ ] Session management is correct
- [ ] Password policies are enforced
- [ ] Account lockout is configured
- [ ] Audit logging is enabled
- [ ] Security alerts are configured

### Authorization

- [ ] RBAC roles are correct
- [ ] Permissions are least-privilege
- [ ] Service accounts are restricted
- [ ] Network policies are in place
- [ ] Pod security policies are correct
- [ ] Secret access is limited
- [ ] API access is restricted
- [ ] Admin access is protected
- [ ] Audit logging is enabled
- [ ] Compliance requirements are met

### Data Protection

- [ ] Data is encrypted at rest
- [ ] Data is encrypted in transit
- [ ] PII is handled correctly
- [ ] Data retention is configured
- [ ] Data deletion is implemented
- [ ] Data masking is in place
- [ ] Backup encryption is enabled
- [ ] Key rotation is scheduled
- [ ] Secrets are managed securely
- [ ] Compliance requirements are met

---

## Performance Checks

### Latency

- [ ] Response time meets SLA
- [ ] P95 latency is acceptable
- [ ] P99 latency is acceptable
- [ ] Inference latency is acceptable
- [ ] Database query latency is acceptable
- [ ] Cache latency is acceptable
- [ ] Network latency is acceptable
- [ ] Cold start time is acceptable
- [ ] Timeout values are appropriate
- [ ] Retry delays are appropriate

### Throughput

- [ ] Requests per second meets requirements
- [ ] Concurrent connections are sufficient
- [ ] Queue depth is manageable
- [ ] Background job throughput is acceptable
- [ ] Database throughput is acceptable
- [ ] Cache throughput is acceptable
- [ ] Network throughput is acceptable
- [ ] GPU throughput is acceptable
- [ ] Batch processing is efficient
- [ ] Streaming is working correctly

### Resource Utilization

- [ ] CPU usage is within limits
- [ ] Memory usage is within limits
- [ ] GPU usage is within limits
- [ ] Disk usage is within limits
- [ ] Network usage is within limits
- [ ] Connection pools are sized correctly
- [ ] Thread pools are sized correctly
- [ ] Queue sizes are manageable
- [ ] Cache sizes are appropriate
- [ ] Buffer sizes are appropriate

---

## Communication Checklist

### Pre-Deployment Communication

- [ ] Team notified of deployment schedule
- [ ] Stakeholders informed of changes
- [ ] Support team briefed on changes
- [ ] Customer success informed (if applicable)
- [ ] On-call engineer confirmed
- [ ] Deployment window confirmed
- [ ] Rollback plan communicated
- [ ] Emergency contacts listed
- [ ] Communication channels confirmed
- [ ] Status page updated (if applicable)

### During Deployment Communication

- [ ] Deployment status updates posted
- [ ] Issues communicated immediately
- [ ] Rollback decisions communicated
- [ ] Metrics updates provided
- [ ] Stakeholders kept informed
- [ ] Support team updated
- [ ] Customer success updated (if applicable)
- [ ] Leadership informed (if needed)
- [ ] Documentation updated
- [ ] Status page updated (if applicable)

### Post-Deployment Communication

- [ ] Deployment success announced
- [ ] Release notes published
- [ ] Changes documented
- [ ] Known issues documented
- [ ] Follow-up items listed
- [ ] Team debriefed
- [ ] Stakeholders informed
- [ ] Customers informed (if applicable)
- [ ] Blog post published (if applicable)
- [ ] Social media updated (if applicable)

---

## Summary

This deployment checklist provides a comprehensive framework for ensuring reliable deployments of AI/LLM systems. By following these checks at each phase, teams can minimize risk, catch issues early, and maintain high availability.

### Key Points

1. **P0 checks are mandatory** - Never skip critical checks
2. **Test thoroughly** - Multiple layers of testing are essential
3. **Monitor actively** - Real-time monitoring catches issues early
4. **Communicate clearly** - Keep stakeholders informed throughout
5. **Have a rollback plan** - Always be prepared to revert changes
6. **Document everything** - Knowledge sharing reduces future risks
7. **LLM-specific checks matter** - AI systems have unique requirements
8. **Security is non-negotiable** - Protect data and systems
9. **Performance monitoring is critical** - Catch degradation early
10. **Continuous improvement** - Learn from each deployment

### Checklist Maintenance

- Review and update checklist quarterly
- Add new checks based on lessons learned
- Remove obsolete checks
- Customize for your organization
- Train team on checklist usage
- Automate checks where possible
- Track checklist compliance
- Measure deployment success rates

### Deployment Metrics to Track

- Deployment frequency (how often you deploy)
- Lead time for changes (commit to production)
- Change failure rate (percentage of failed deployments)
- Mean time to recovery (time to recover from failure)
- Time to restore service (time to restore after incident)
- Deployment success rate (percentage of successful deployments)
- Rollback rate (percentage of deployments requiring rollback)
- Average deployment duration (time from start to completion)

### Common Checklist Mistakes to Avoid

- Skipping P0 checks due to time pressure
- Not updating checklist after incidents
- Over-complicating the checklist
- Not automating repetitive checks
- Ignoring post-deployment verification
- Not involving the whole team in checklist creation
- Treating checklist as optional
- Not learning from failed deployments

---

## Deployment Gates Checklist

### Gate 1: Build Verification

- [ ] Code compiles without errors
- [ ] Unit tests pass (100% of critical path tests)
- [ ] Code coverage meets minimum threshold (≥80%)
- [ ] No critical or high-severity security vulnerabilities
- [ ] Code has been reviewed and approved
- [ ] No merge conflicts with main branch
- [ ] Build artifacts are created successfully
- [ ] Docker image builds without errors
- [ ] Image size is within acceptable limits
- [ ] No secrets embedded in image

### Gate 2: Integration Verification

- [ ] Integration tests pass
- [ ] API contract tests pass
- [ ] Database migrations are backward compatible
- [ ] External service integrations work correctly
- [ ] Message queue integrations work correctly
- [ ] Cache integrations work correctly
- [ ] Authentication/authorization work correctly
- [ ] Rate limiting works correctly
- [ ] Error handling works correctly
- [ ] Logging works correctly

### Gate 3: Staging Verification

- [ ] Staging deployment is successful
- [ ] Smoke tests pass in staging
- [ ] Load tests meet performance requirements
- [ ] Security scan is clean
- [ ] Configuration matches production
- [ ] Data is representative
- [ ] Monitoring is active
- [ ] Alerts are configured
- [ ] Access is available for team
- [ ] No blocking issues identified

### Gate 4: Production Approval

- [ ] Technical lead approval received
- [ ] Product owner approval received (if required)
- [ ] Security team approval received (if required)
- [ ] Change management approval received (if required)
- [ ] Deployment window is confirmed
- [ ] On-call engineer is notified
- [ ] Support team is notified
- [ ] Rollback plan is documented
- [ ] All approvers are available
- [ ] No conflicting deployments scheduled

---

## Feature Flag Checklist

### Pre-Deployment

- [ ] Feature flag is created
- [ ] Flag key follows naming convention
- [ ] Flag description is clear
- [ ] Flag variations are defined
- [ ] Flag rules are configured
- [ ] Flag targeting is correct
- [ ] Flag fallback is configured
- [ ] Flag metrics are defined
- [ ] Flag alerts are configured
- [ ] Flag documentation is complete

### During Deployment

- [ ] Flag is disabled in production
- [ ] Flag is enabled for internal users
- [ ] Flag is enabled for beta users
- [ ] Metrics are being collected
- [ ] Alerts are not firing
- [ ] No errors in logs
- [ ] Performance is acceptable
- [ ] User feedback is positive
- [ ] Flag is ready for gradual rollout
- [ ] Rollback plan is ready

### Post-Deployment

- [ ] Flag is enabled for 10% of users
- [ ] Metrics are stable
- [ ] Flag is enabled for 50% of users
- [ ] Metrics are stable
- [ ] Flag is enabled for 100% of users
- [ ] Metrics are stable
- [ ] Flag is marked as permanent
- [ ] Flag cleanup is scheduled
- [ ] Documentation is updated
- [ ] Team is informed

---

## Database Migration Checklist

### Pre-Migration

- [ ] Migration script is tested
- [ ] Migration is backward compatible
- [ ] Migration can be rolled back
- [ ] Database backup is current
- [ ] Migration window is scheduled
- [ ] Team is notified
- [ ] Rollback plan is documented
- [ ] Dependencies are identified
- [ ] Impact is assessed
- [ ] Approval is received

### During Migration

- [ ] Migration script is executed
- [ ] Migration is monitored
- [ ] Errors are logged
- [ ] Performance is acceptable
- [ ] Data integrity is verified
- [ ] Application is tested
- [ ] Rollback is ready
- [ ] Communication is maintained
- [ ] Timeline is tracked
- [ ] Issues are documented

### Post-Migration

- [ ] Migration is verified
- [ ] Application is working correctly
- [ ] Performance is acceptable
- [ ] Data integrity is verified
- [ ] Monitoring is active
- [ ] Alerts are configured
- [ ] Documentation is updated
- [ ] Team is informed
- [ ] Old code is cleaned up
- [ ] Lessons learned are captured

---

## API Versioning Checklist

### Pre-Deployment

- [ ] API version is incremented
- [ ] Breaking changes are documented
- [ ] Deprecation notices are added
- [ ] Migration guide is created
- [ ] SDK is updated
- [ ] Client libraries are updated
- [ ] Backward compatibility is maintained
- [ ] Forward compatibility is considered
- [ ] Versioning strategy is followed
- [ ] Approval is received

### During Deployment

- [ ] Old version is still available
- [ ] New version is deployed
- [ ] Both versions are working
- [ ] Deprecation warnings are logged
- [ ] Metrics are collected
- [ ] Alerts are configured
- [ ] Monitoring is active
- [ ] Communication is maintained
- [ ] Timeline is tracked
- [ ] Issues are documented

### Post-Deployment

- [ ] Both versions are working
- [ ] Deprecation notices are visible
- [ ] Migration guide is accessible
- [ ] SDK is updated
- [ ] Client libraries are updated
- [ ] Documentation is updated
- [ ] Team is informed
- [ ] Old version removal is scheduled
- [ ] Cleanup is planned
- [ ] Lessons learned are captured
