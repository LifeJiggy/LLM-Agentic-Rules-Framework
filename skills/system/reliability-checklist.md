# Reliability Checklist

Use this checklist for code, adapters, rules, validators, plugins, and agentic workflows.

## Error Handling

### Input Validation

- [ ] Input paths, config values, and target names are validated before side effects.
- [ ] All external input is validated against expected schemas.
- [ ] Null and undefined values are handled explicitly.
- [ ] Empty strings and collections are validated appropriately.
- [ ] Numeric ranges are enforced (min, max, precision).
- [ ] String length limits are enforced.
- [ ] Enumeration values are validated against allowed options.
- [ ] Date and time formats are validated.
- [ ] Email, URL, and other format-specific validations are performed.
- [ ] Custom validation rules are applied for domain-specific constraints.

### Error Detection and Reporting

- [ ] Missing files and unreadable files produce actionable errors.
- [ ] File permissions are checked before access attempts.
- [ ] File existence is verified before operations.
- [ ] File size limits are enforced for reads and writes.
- [ ] Directory traversal attacks are prevented.
- [ ] Symlink following is controlled and audited.
- [ ] Invalid JSON, YAML, Markdown, or manifest data fails early.
- [ ] Parse errors include line and column information.
- [ ] Schema validation errors are descriptive and actionable.
- [ ] Encoding issues are detected and reported.
- [ ] Malformed data is rejected before processing.
- [ ] Type mismatches are detected at boundaries.
- [ ] Errors preserve enough context to identify the failing file, target, or operation.
- [ ] Error messages include operation context.
- [ ] Error messages include relevant parameter values (sanitized).
- [ ] Error messages include suggestions for resolution when possible.
- [ ] Expected errors do not hide unexpected exceptions.
- [ ] Specific exception types are used for expected errors.
- [ ] Generic exception handlers catch only truly unexpected errors.
- [ ] Exception handlers re-raise when they cannot handle the error.
- [ ] Multiple exception handlers are ordered from specific to general.

### Error Handling Patterns

- [ ] Try-catch blocks are used appropriately around risky operations.
- [ ] Finally blocks are used for cleanup operations.
- [ ] Context managers are used for resource management.
- [ ] Resource cleanup happens in all code paths.
- [ ] Error handlers do not swallow exceptions silently.
- [ ] Error handlers log errors before recovery or re-raising.
- [ ] Error handling does not introduce new failure modes.
- [ ] Nested error handling is minimized.
- [ ] Error propagation is consistent across layers.

## Runtime Reliability

### External Call Management

- [ ] External calls define timeout behavior.
- [ ] Timeout values are appropriate for the operation.
- [ ] Timeouts are configured at multiple levels (connection, request, total).
- [ ] Timeout values are documented and justified.
- [ ] Timeouts are tested under various network conditions.
- [ ] Timeout exceptions are handled appropriately.
- [ ] Retries are bounded and do not multiply side effects.
- [ ] Maximum retry count is defined and enforced.
- [ ] Retry limits are configurable.
- [ ] Total retry time is bounded.
- [ ] Retry attempts are tracked and limited.
- [ ] Retry budgets prevent excessive retry attempts.
- [ ] Idempotency is ensured for retried operations.
- [ ] Side effects are not repeated on retry.
- [ ] Retry metadata is included in logs and metrics.

### Retry Implementation

- [ ] Retry strategy is appropriate for the failure type.
- [ ] Exponential backoff is used for rate limiting.
- [ ] Linear retry is used for consistent failure rates.
- [ ] Jitter is added to prevent thundering herd.
- [ ] Circuit breaker is implemented for sustained failures.
- [ ] Retry is disabled for non-retryable errors.
- [ ] Retry conditions are clearly documented.
- [ ] Retry behavior is observable through metrics.

### Fallback Behavior

- [ ] Fallback behavior is explicit and tested.
- [ ] Fallback triggers are clearly defined.
- [ ] Fallback behavior is documented.
- [ ] Fallback responses are validated.
- [ ] Fallback activation is logged and monitored.
- [ ] Fallback recovery is automatic when primary recovers.
- [ ] Multiple fallback levels are defined for critical services.
- [ ] Fallback data freshness is tracked.
- [ ] Fallback limitations are communicated to users.

### Cancellation and Timeout

- [ ] Cancellation tokens are used for long-running operations.
- [ ] Cancellation is checked at safe points.
- [ ] Resources are cleaned up on cancellation.
- [ ] Partial results are returned when appropriate.
- [ ] Timeout exceptions are propagated correctly.
- [ ] Operation deadlines are enforced.
- [ ] Concurrent operations are limited appropriately.
- [ ] Backpressure is implemented for high-load scenarios.
- [ ] Bulkhead pattern isolates critical resources.
- [ ] Rate limiting prevents resource exhaustion.

### Partial Work Management

- [ ] Partial work is skipped, resumed, or rolled back safely.
- [ ] Transaction boundaries are clearly defined.
- [ ] Atomic operations are used where appropriate.
- [ ] Partial state is detected and handled.
- [ ] Recovery from partial state is automated where possible.
- [ ] Partial work is logged for debugging.
- [ ] Idempotent operations enable safe retry.
- [ ] Compensation transactions undo partial work.
- [ ] State snapshots enable recovery.
- [ ] Checkpoints are created for long-running operations.

### Summaries and Reporting

- [ ] Final summaries include success, skip, warning, and failure counts.
- [ ] Summary statistics are accurate and complete.
- [ ] Summary generation is reliable and doesn't fail.
- [ ] Summary includes timing information.
- [ ] Summary includes resource utilization.
- [ ] Summary identifies items requiring attention.
- [ ] Summary is formatted for human readability.
- [ ] Summary is available in structured format for automation.

## Safe Writes

### Write Safety Principles

- [ ] Writes avoid replacing directories or symlink targets unexpectedly.
- [ ] Destination paths are validated before writing.
- [ ] File type is verified before writing.
- [ ] Symlink targets are resolved and validated.
- [ ] Directory permissions are checked before creation.
- [ ] Existing files are backed up or versioned before overwrite.
- [ ] Backup files are created before modification.
- [ ] Backup files are stored separately from originals.
- [ ] Backup naming includes version or timestamp.
- [ ] Backup retention policy is defined and enforced.
- [ ] Changed files are written atomically where practical.
- [ ] Temporary files are used for writes.
- [ ] Atomic rename operations are used.
- [ ] Write validation occurs before finalization.
- [ ] Partial writes are detected and cleaned up.
- [ ] Output paths reject unsafe destinations.
- [ ] Path traversal attacks are prevented.
- [ ] Absolute paths are used or validated.
- [ ] Path normalization is performed.
- [ ] Dangerous paths (system directories) are rejected.
- [ ] Dry-run and apply modes report consistent planned operations.
- [ ] Dry-run accurately predicts apply behavior.
- [ ] Dry-run and apply use same logic for operations.
- [ ] Differences between dry-run and apply are documented.

### Write Atomicity

- [ ] Critical writes use atomic operations.
- [ ] File system transactions are used where available.
- [ ] Write operations are isolated from readers.
- [ ] Concurrent write conflicts are detected and handled.
- [ ] Write locks are used for exclusive access.
- [ ] Write ordering is preserved when required.
- [ ] Write dependencies are tracked.
- [ ] Rollback is possible for failed atomic writes.

### Write Validation

- [ ] Written content is validated before completion.
- [ ] File integrity is verified after write.
- [ ] File permissions are verified after creation.
- [ ] File existence is confirmed after write.
- [ ] File readability is verified.
- [ ] Content checksums are verified.
- [ ] File size matches expected size.
- [ ] Write errors are reported with context.

## Release Readiness

### Failure Classification and Response

- [ ] P0 failures block release.
- [ ] P0 failure criteria are clearly defined.
- [ ] P0 failures require immediate escalation.
- [ ] P0 failure detection is automated.
- [ ] P1 failures require owner, due date, and accepted risk.
- [ ] P1 failure severity is assessed.
- [ ] P1 failure owners are assigned.
- [ ] P1 failure due dates are realistic.
- [ ] Accepted risks are documented.
- [ ] Risk acceptance criteria are defined.
- [ ] P2 failures are tracked but don't block release.
- [ ] P3 failures are logged for future improvement.
- [ ] Failure severity levels are clearly defined.
- [ ] Failure classification is consistent across teams.

### Monitoring and Observability

- [ ] Monitoring or logs expose the failure modes users care about.
- [ ] Critical failure paths are instrumented.
- [ ] Error rates are tracked by type.
- [ ] Error context is sufficient for debugging.
- [ ] Alerts are configured for critical failures.
- [ ] Alert thresholds are appropriate.
- [ ] Alert fatigue is prevented.
- [ ] Dashboard displays key reliability metrics.
- [ ] Log aggregation is configured.
- [ ] Log retention meets requirements.

### Rollback and Disablement

- [ ] Rollback or disablement steps are documented.
- [ ] Rollback procedures are tested regularly.
- [ ] Rollback time is within acceptable limits.
- [ ] Rollback scripts are version controlled.
- [ ] Rollback triggers are defined.
- [ ] Feature flags enable gradual disablement.
- [ ] Emergency disablement procedures exist.
- [ ] Disablement communication plan exists.
- [ ] Rollback evidence is collected.

### Verification and Testing

- [ ] Verification commands have been run after the hardening change.
- [ ] All verification tests pass.
- [ ] Performance benchmarks are met.
- [ ] Security scans are clean.
- [ ] Manual testing is completed.
- [ ] Regression tests pass.
- [ ] Integration tests pass.
- [ ] End-to-end tests pass.
- [ ] Load testing is performed for high-traffic features.
- [ ] Chaos testing validates resilience.

### Documentation

- [ ] Changes are documented in release notes.
- [ ] Architecture diagrams are updated.
- [ ] Runbooks are updated.
- [ ] Operational procedures are documented.
- [ ] Recovery procedures are documented.
- [ ] Known limitations are documented.
- [ ] Troubleshooting guides are available.
- [ ] Contact information for escalation is current.

## Domain-Specific Reliability

### LLM and AI Systems

- [ ] Model inference timeouts are configured.
- [ ] Model fallback behavior is defined.
- [ ] Prompt validation prevents injection attacks.
- [ ] Response validation ensures expected format.
- [ ] Token limits are enforced.
- [ ] Context window overflow is handled.
- [ ] Model versioning is tracked.
- [ ] A/B testing infrastructure is reliable.
- [ ] Model degradation is detected.
- [ ] Fallback models are available.

### Agentic Systems

- [ ] Tool call failures are handled gracefully.
- [ ] Tool output validation is performed.
- [ ] Agent state is persisted appropriately.
- [ ] Multi-step workflow failures are recoverable.
- [ ] Agent memory limits are enforced.
- [ ] Tool invocation timeouts are configured.
- [ ] Agent decision logic is validated.
- [ ] Human oversight triggers are implemented.
- [ ] Agent actions are auditable.
- [ ] Agent recovery procedures are defined.

### Adapter and Integration Systems

- [ ] Adapter failures don't crash main system.
- [ ] Adapter timeouts are configured.
- [ ] Adapter fallback behavior is defined.
- [ ] Adapter version compatibility is validated.
- [ ] Adapter configuration is validated.
- [ ] Adapter health checks are implemented.
- [ ] Adapter failures are logged and monitored.
- [ ] Adapter recovery is automatic when possible.
- [ ] Adapter isolation prevents cascading failures.
- [ ] Adapter metrics are collected.

### CLI and IDE Tools

- [ ] Command execution failures are handled.
- [ ] User input validation is performed.
- [ ] File system operations are safe.
- [ ] Configuration errors are reported clearly.
- [ ] Help text is accurate and complete.
- [ ] Error messages suggest solutions.
- [ ] Exit codes follow conventions.
- [ ] Progress indicators are accurate.
- [ ] Interrupt signals are handled gracefully.
- [ ] Temporary files are cleaned up.

### Plugin Systems

- [ ] Plugin loading failures are handled gracefully.
- [ ] Plugin isolation prevents crashes.
- [ ] Plugin API versioning is managed.
- [ ] Plugin dependencies are validated.
- [ ] Plugin timeouts prevent hangs.
- [ ] Plugin failures don't affect core system.
- [ ] Plugin updates are atomic.
- [ ] Plugin rollback is possible.
- [ ] Plugin metrics are collected.
- [ ] Plugin security is validated.

### Validation Systems

- [ ] Validation errors are clear and actionable.
- [ ] Validation performance is acceptable.
- [ ] Validation rules are version controlled.
- [ ] Validation results are reproducible.
- [ ] Validation failures don't corrupt data.
- [ ] Validation can be skipped when appropriate.
- [ ] Validation caching improves performance.
- [ ] Validation metrics are collected.
- [ ] Validation rules are tested.
- [ ] Validation errors include fix suggestions.

## Testing Requirements

### Unit Testing

- [ ] Error paths are tested.
- [ ] Timeout behavior is tested.
- [ ] Retry behavior is tested.
- [ ] Circuit breaker behavior is tested.
- [ ] Fallback behavior is tested.
- [ ] Partial write recovery is tested.
- [ ] Rollback procedures are tested.
- [ ] Edge cases are covered.
- [ ] Error handling is tested.
- [ ] Resource cleanup is tested.

### Integration Testing

- [ ] End-to-end workflows are tested.
- [ ] External service failures are simulated.
- [ ] Network failures are simulated.
- [ ] Database failures are simulated.
- [ ] Partial failures are tested.
- [ ] Recovery scenarios are tested.
- [ ] Performance under load is tested.
- [ ] Concurrent operations are tested.
- [ ] Data consistency is verified.
- [ ] System integration is validated.

### Chaos Testing

- [ ] Service failures are injected.
- [ ] Network latency is simulated.
- [ ] Resource exhaustion is tested.
- [ ] Dependency failures are tested.
- [ ] Cascading failures are prevented.
- [ ] Recovery is automatic where designed.
- [ ] Monitoring detects injected failures.
- [ ] Alerts fire appropriately.
- [ ] System degrades gracefully.
- [ ] Rollback procedures work under stress.

### Performance Testing

- [ ] Load testing meets performance targets.
- [ ] Stress testing identifies breaking points.
- [ ] Soak testing detects memory leaks.
- [ ] Spike testing handles traffic bursts.
- [ ] Endurance testing validates long-running stability.
- [ ] Performance baselines are established.
- [ ] Performance regressions are detected.
- [ ] Bottlenecks are identified and addressed.

## Operational Procedures

### Deployment Procedures

- [ ] Deployment checklist is followed.
- [ ] Pre-deployment verification passes.
- [ ] Deployment is staged appropriately.
- [ ] Rollback plan is ready.
- [ ] Monitoring is active during deployment.
- [ ] Post-deployment verification passes.
- [ ] Deployment documentation is complete.
- [ ] Deployment metrics are collected.

### Incident Response

- [ ] Incident response plan exists.
- [ ] On-call rotation is established.
- [ ] Escalation paths are defined.
- [ ] Communication plan is documented.
- [ ] Incident documentation template exists.
- [ ] Post-incident review process exists.
- [ ] Root cause analysis is performed.
- [ ] Remediation actions are tracked.
- [ ] Lessons learned are documented.
- [ ] Incident metrics are collected.

### Maintenance Procedures

- [ ] Regular maintenance windows are scheduled.
- [ ] Maintenance procedures are documented.
- [ ] Maintenance notifications are sent.
- [ ] Maintenance rollback plan exists.
- [ ] Post-maintenance verification is performed.
- [ ] Maintenance metrics are collected.
- [ ] Maintenance history is maintained.

## Security Considerations

### Security Reliability

- [ ] Authentication failures are handled securely.
- [ ] Authorization failures are logged and monitored.
- [ ] Rate limiting prevents abuse.
- [ ] Input validation prevents injection attacks.
- [ ] Output encoding prevents injection attacks.
- [ ] Sensitive data is not logged.
- [ ] Encryption is used for sensitive data.
- [ ] Security patches are applied promptly.
- [ ] Vulnerability scanning is performed regularly.
- [ ] Security incidents are handled appropriately.

### Data Protection

- [ ] Data backup procedures are defined.
- [ ] Backup integrity is verified.
- [ ] Backup restoration is tested.
- [ ] Data retention policies are enforced.
- [ ] Data deletion is secure.
- [ ] Data encryption is implemented.
- [ ] Data access is audited.
- [ ] Data breaches are handled appropriately.
- [ ] Privacy regulations are complied with.
- [ ] Data classification is performed.

## Compliance and Audit

### Audit Trail

- [ ] All changes are logged.
- [ ] Configuration changes are tracked.
- [ ] Deployment history is maintained.
- [ ] Access logs are retained.
- [ ] Audit logs are protected from tampering.
- [ ] Audit logs are retained for required period.
- [ ] Audit reports are generated regularly.
- [ ] Audit findings are addressed.

### Compliance Requirements

- [ ] Regulatory requirements are identified.
- [ ] Compliance controls are implemented.
- [ ] Compliance evidence is collected.
- [ ] Compliance reports are generated.
- [ ] Compliance gaps are addressed.
- [ ] Compliance training is provided.
- [ ] Compliance audits are passed.
- [ ] Compliance metrics are monitored.

## Continuous Improvement

### Metrics and Feedback

- [ ] Key reliability metrics are defined.
- [ ] Metrics are collected and monitored.
- [ ] Metrics dashboards are available.
- [ ] Metrics trends are analyzed.
- [ ] Improvement opportunities are identified.
- [ ] Changes are measured for impact.
- [ ] Feedback loops are established.
- [ ] Learning from incidents is institutionalized.

### Process Improvement

- [ ] Reliability processes are documented.
- [ ] Process adherence is monitored.
- [ ] Process improvements are implemented.
- [ ] Best practices are shared.
- [ ] Training is provided.
- [ ] Tools and automation are improved.
- [ ] Technical debt is managed.
- [ ] Architecture evolves for better reliability.

## Quick Reference

### Critical Checks (Must Pass)

1. P0 failures block release.
2. Error handling covers all error paths.
3. Timeouts are configured for all external calls.
4. Retries are bounded and safe.
5. Observability is implemented.
6. Rollback procedures exist and are tested.
7. Safe write patterns are used.
8. Partial failure recovery is handled.

### High Priority Checks (Should Pass)

1. Circuit breakers are implemented.
2. Fallback behavior is defined and tested.
3. Monitoring and alerting are configured.
4. Documentation is complete.
5. Testing covers error paths.
6. Performance benchmarks are met.
7. Security review is completed.

### Medium Priority Checks (Nice to Have)

1. Chaos testing is performed.
2. Advanced resilience patterns are used.
3. Comprehensive metrics are collected.
4. Runbooks are detailed.
5. Training materials are available.

### Low Priority Checks (Backlog)

1. Advanced monitoring dashboards.
2. Predictive failure analysis.
3. Automated remediation.
4. Self-healing systems.
5. Advanced observability tools.

## Appendix: Common Failure Modes

### Network Failures

- Connection timeout
- DNS resolution failure
- TLS handshake failure
- Packet loss
- Network partition
- Load balancer failure

### Service Failures

- Service crash
- Service overload
- Service unresponsive
- Service returning errors
- Service version mismatch
- Service configuration error

### Data Failures

- Database connection failure
- Database deadlock
- Database corruption
- Data validation failure
- Data migration failure
- Data serialization failure

### Infrastructure Failures

- Server failure
- Disk full
- Memory exhaustion
- CPU saturation
- Network interface failure
- Power outage

### Application Failures

- Unhandled exception
- Memory leak
- Thread deadlock
- Resource exhaustion
- Configuration error
- Deployment failure

### Human Errors

- Configuration mistake
- Deployment error
- Data entry error
- Procedure violation
- Communication failure
- Decision error

## Appendix: Recovery Time Objectives

### Critical Systems (RTO < 5 minutes)

- Automated rollback
- Automated failover
- Hot standby systems
- Instant recovery procedures

### Important Systems (RTO < 30 minutes)

- Warm standby systems
- Scripted rollback procedures
- Pre-staged recovery resources

### Standard Systems (RTO < 4 hours)

- Documented recovery procedures
- Available recovery resources
- Trained personnel

### Low Priority Systems (RTO < 24 hours)

- Documented recovery procedures
- Scheduled recovery windows
- Standard recovery resources
