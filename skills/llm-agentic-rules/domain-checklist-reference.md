# Domain Checklist Reference

Use this reference for detailed, actionable checklists across all 10 framework domains. Each domain checklist maps directly to the framework's P0/P1/P2/P3 requirements and provides concrete verification steps.

## How to Use This Reference

1. Identify the relevant domain(s) for your task using the domain routing guide.
2. Read the full domain checklist for each applicable domain.
3. For each item, determine if it applies to your system and risk tier.
4. Verify each item with evidence.
5. Document findings and any acceptances or waivers.

## Domain 1: Core (Fundamental AI Requirements)

### P0 - Critical (Blocks Production)

**C0.1: Model Selection Rationale**
- [ ] Model selection is documented with clear rationale.
- [ ] Model capabilities match system requirements.
- [ ] Model limitations are understood and documented.
- [ ] Model version is pinned and tracked.
- [ ] Model fallback strategy exists.

**Verification:**
- Model selection document exists.
- Capability assessment completed.
- Limitations documented in runbook.

**C0.2: Prompt Design and Validation**
- [ ] Prompts are designed with clear objectives.
- [ ] Prompts are validated for clarity and specificity.
- [ ] Prompt injection risks are assessed and mitigated.
- [ ] Prompt templates are version controlled.
- [ ] Prompt performance is evaluated.

**Verification:**
- Prompt design document exists.
- Prompt validation tests pass.
- Injection resistance tests pass.
- Prompt versioning in place.

**C0.3: System Architecture**
- [ ] System architecture is documented.
- [ ] Components and their interactions are defined.
- [ ] Data flow is documented.
- [ ] Scalability considerations are addressed.
- [ ] Failure modes are identified.

**Verification:**
- Architecture diagram exists.
- Data flow diagram exists.
- Failure mode analysis completed.

**C0.4: Context Window Management**
- [ ] Context window limits are defined.
- [ ] Context overflow is handled gracefully.
- [ ] Token counting is implemented and accurate.
- [ ] Context prioritization strategy exists.
- [ ] Context window usage is monitored.

**Verification:**
- Token counting tests pass.
- Context overflow handling tested.
- Context usage metrics collected.

**C0.5: Token Budget Allocation**
- [ ] Token budgets are defined for system components.
- [ ] Token usage is monitored.
- [ ] Token budget exceeded scenarios are handled.
- [ ] Cost implications of token usage are understood.

**Verification:**
- Token budget documentation exists.
- Token usage monitoring configured.
- Cost tracking implemented.

### P1 - High (Requires Acceptance)

**C1.1: Capability Assessment**
- [ ] Model capabilities are formally assessed.
- [ ] Capability gaps are identified.
- [ ] Mitigation strategies for gaps exist.
- [ ] Assessment is documented.

**Verification:**
- Capability assessment document exists.
- Gap analysis completed.

**C1.2: Prompt Template Management**
- [ ] Prompt templates are stored in version control.
- [ ] Template changes are reviewed.
- [ ] Template versioning is implemented.
- [ ] Template testing is automated.

**Verification:**
- Prompt templates in version control.
- Template change process documented.

**C1.3: Model Versioning**
- [ ] Model versions are tracked.
- [ ] Model version compatibility is verified.
- [ ] Model rollback capability exists.
- [ ] Model version migration is tested.

**Verification:**
- Model version registry exists.
- Rollback procedure tested.

### P2 - Medium (Should Address)

**C2.1: Prompt Optimization**
- [ ] Prompts are optimized for clarity and effectiveness.
- [ ] Prompt variants are tested.
- [ ] Prompt performance is monitored.
- [ ] Prompt A/B testing infrastructure exists.

**C2.2: System Design Patterns**
- [ ] Design patterns are documented.
- [ ] Patterns are applied consistently.
- [ ] Pattern alternatives are considered.

### P3 - Low (Nice to Have)

**C3.1: Advanced Prompting Techniques**
- [ ] Chain-of-thought prompting evaluated.
- [ ] Few-shot examples optimized.
- [ ] Prompt chaining implemented where appropriate.

---

## Domain 2: Security (Threat Protection)

### P0 - Critical (Blocks Production)

**S0.1: Authentication**
- [ ] All protected endpoints require authentication.
- [ ] Authentication tokens are validated.
- [ ] Token expiration and refresh is implemented.
- [ ] Authentication failures are logged.
- [ ] Brute force protection is implemented.

**Verification:**
- Authentication tests pass.
- Token validation tests pass.
- Security scan shows no auth bypass.

**S0.2: Authorization**
- [ ] Authorization checks are performed on all protected resources.
- [ ] Authorization logic is centralized and consistent.
- [ ] Privilege escalation is prevented.
- [ ] Role-based access control (RBAC) is implemented if applicable.
- [ ] Authorization failures are logged.

**Verification:**
- Authorization tests pass for all roles.
- Privilege escalation tests pass.

**S0.3: Input Validation and Sanitization**
- [ ] All user inputs are validated.
- [ ] All API inputs are validated against schemas.
- [ ] Input sanitization prevents injection attacks.
- [ ] File uploads are validated for type, size, and content.
- [ ] Input validation errors are logged.

**Verification:**
- Input validation tests pass.
- Fuzz testing shows no injection vulnerabilities.
- Security scan shows no injection flaws.

**S0.4: Output Filtering**
- [ ] Model outputs are filtered for harmful content.
- [ ] Outputs are validated for expected format.
- [ ] Sensitive data is not leaked in outputs.
- [ ] Output filtering is logged.
- [ ] Filter bypass attempts are detected and logged.

**Verification:**
- Output filtering tests pass.
- Red teaming shows no harmful outputs.
- Sensitive data scans show no leaks.

**S0.5: Rate Limiting and Abuse Prevention**
- [ ] Rate limiting is implemented.
- [ ] Rate limits are appropriate for system capacity.
- [ ] Abuse detection is implemented.
- [ ] Rate limit exceeded responses are graceful.
- [ ] Rate limiting metrics are collected.

**Verification:**
- Rate limiting tests pass.
- Load tests verify rate limiting effectiveness.
- Abuse detection tests pass.

**S0.6: API Key and Credential Management**
- [ ] No hardcoded credentials in code.
- [ ] Secrets are managed via secret management system.
- [ ] Credentials are rotated regularly.
- [ ] Credential access is logged.
- [ ] Credential exposure incidents have response plan.

**Verification:**
- Secret scanning shows no hardcoded secrets.
- Secret management system is configured.
- Rotation policy exists and is followed.

### P1 - High (Requires Acceptance)

**S1.1: Prompt Injection Prevention**
- [ ] Prompt injection risks are assessed.
- [ ] Input sanitization prevents injection.
- [ ] Output validation detects injection attempts.
- [ ] Injection attempts are logged and alerted.
- [ ] Red teaming includes prompt injection scenarios.

**Verification:**
- Prompt injection tests pass.
- Red teaming report exists.

**S1.2: Audit Logging**
- [ ] Security events are logged.
- [ ] Logs include actor, action, target, outcome.
- [ ] Logs are tamper-resistant.
- [ ] Log retention meets compliance requirements.
- [ ] Log-based alerting is configured.

**Verification:**
- Audit log samples reviewed.
- Log retention policy documented.
- Log integrity checks implemented.

**S1.3: Dependency Security**
- [ ] Dependencies are scanned for vulnerabilities.
- [ ] Vulnerability scan is part of CI/CD.
- [ ] Critical vulnerabilities are resolved before deployment.
- [ ] Dependency updates are reviewed.
- [ ] License compliance is verified.

**Verification:**
- Dependency scan report shows no critical/high vulnerabilities.
- SCA tool is configured and running.

**S1.4: Data Protection**
- [ ] Sensitive data is encrypted at rest.
- [ ] Sensitive data is encrypted in transit.
- [ ] Data access is logged.
- [ ] Data retention policies are enforced.
- [ ] Data deletion procedures exist.

**Verification:**
- Encryption implementation verified.
- Data access logs reviewed.
- Retention policy documented.

### P2 - Medium (Should Address)

**S2.1: Security Training**
- [ ] Team has security training.
- [ ] Security awareness is maintained.
- [ ] Security incidents are reviewed in retros.

**S2.2: Threat Modeling**
- [ ] Threat model exists.
- [ ] Threat model is updated with changes.
- [ ] Threat model is reviewed periodically.

### P3 - Low (Nice to Have)

**S3.1: Advanced Security Monitoring**
- [ ] Anomaly detection for security events.
- [ ] Security information and event management (SIEM) integration.
- [ ] Automated threat response.

---

## Domain 3: Data (Data Governance and Privacy)

### P0 - Critical (Blocks Production)

**D0.1: Data Sourcing**
- [ ] Data sources are documented.
- [ ] Data sourcing complies with terms of service.
- [ ] Data provenance is tracked.
- [ ] Data quality is assessed.
- [ ] Data licensing is verified.

**Verification:**
- Data source documentation exists.
- Terms of service review completed.
- Data quality report exists.

**D0.2: Data Quality**
- [ ] Data quality metrics are defined.
- [ ] Data quality is monitored.
- [ ] Data quality issues have remediation process.
- [ ] Training data is representative.
- [ ] Test data is representative and separate from training data.

**Verification:**
- Data quality metrics documented.
- Data quality monitoring configured.
- Train/test split validated.

**D0.3: Data Validation**
- [ ] Data is validated at ingestion.
- [ ] Data validation rules are defined.
- [ ] Invalid data is rejected or handled.
- [ ] Data validation is tested.
- [ ] Data validation errors are logged.

**Verification:**
- Data validation tests pass.
- Validation logic reviewed.

**D0.4: Data Storage and Encryption**
- [ ] Data storage is appropriately secured.
- [ ] Sensitive data is encrypted at rest.
- [ ] Data access controls are implemented.
- [ ] Data backup is implemented.
- [ ] Data retention policies are enforced.

**Verification:**
- Encryption implementation verified.
- Access controls tested.
- Backup procedures tested.

**D0.5: Data Privacy**
- [ ] PII/PHI is identified and classified.
- [ ] Privacy impact assessment completed.
- [ ] Data minimization principles applied.
- [ ] User consent is obtained where required.
- [ ] Data subject rights are supported (access, deletion, etc.).

**Verification:**
- PII/PHI inventory exists.
- Privacy impact assessment document exists.
- Consent mechanisms implemented.

### P1 - High (Requires Acceptance)

**D1.1: Data Retention**
- [ ] Data retention policies are defined.
- [ ] Retention policies are enforced.
- [ ] Data deletion procedures exist and are tested.
- [ ] Retention periods comply with regulations.
- [ ] Data archival strategy exists.

**Verification:**
- Retention policy documented.
- Deletion procedures tested.
- Compliance review completed.

**D1.2: Data Lineage**
- [ ] Data lineage is documented.
- [ ] Data transformations are tracked.
- [ ] Data provenance is maintained.
- [ ] Lineage information is accessible.

**Verification:**
- Data lineage documentation exists.
- Lineage tracking implemented.

**D1.3: Data Governance**
- [ ] Data governance policies exist.
- [ ] Data owners are assigned.
- [ ] Data quality ownership is defined.
- [ ] Data governance meetings occur regularly.

**Verification:**
- Governance policy document exists.
- Data owner assignments documented.

### P2 - Medium (Should Address)

**D2.1: Data Catalog**
- [ ] Data catalog exists.
- [ ] Datasets are documented in catalog.
- [ ] Catalog is kept up to date.

**D2.2: Data Quality Metrics**
- [ ] Data quality dashboards exist.
- [ ] Quality trends are monitored.
- [ ] Quality issues are tracked.

### P3 - Low (Nice to Have)

**D3.1: Advanced Data Analytics**
- [ ] Data usage analytics.
- [ ] Data popularity metrics.
- [ ] Data lifecycle automation.

---

## Domain 4: Integration (External System Connectivity)

### P0 - Critical (Blocks Production)

**I0.1: API Contract Definition**
- [ ] API contracts are defined (OpenAPI, GraphQL schema, etc.).
- [ ] Contracts are versioned.
- [ ] Contracts are tested against.
- [ ] Contract changes follow versioning policy.
- [ ] Contract validation is automated.

**Verification:**
- API specification document exists.
- Contract tests pass.
- Contract validation in CI/CD.

**I0.2: Versioning Strategy**
- [ ] API versioning strategy is defined.
- [ ] Version compatibility is tested.
- [ ] Deprecation policy exists.
- [ ] Version migration is tested.
- [ ] Breaking changes are documented.

**Verification:**
- Versioning strategy document exists.
- Compatibility tests pass.

**I0.3: Backward Compatibility**
- [ ] Changes maintain backward compatibility.
- [ ] Breaking changes require major version bump.
- [ ] Deprecation warnings are provided.
- [ ] Migration path is documented.

**Verification:**
- Backward compatibility tests pass.
- No unexpected breaking changes.

**I0.4: Timeout and Retry Configuration**
- [ ] All external calls have timeouts.
- [ ] Retry logic is implemented.
- [ ] Circuit breakers are configured.
- [ ] Fallback behavior is defined.

**Verification:**
- Timeout values documented.
- Retry logic tested.
- Circuit breaker tests pass.

**I0.5: Error Handling and Fallback**
- [ ] All external call errors are handled.
- [ ] Error handling is consistent.
- [ ] Fallback behavior is defined for critical calls.
- [ ] Errors are logged with context.
- [ ] Error responses are user-friendly.

**Verification:**
- Error handling tests pass.
- Fallback behavior tested.
- Error logs reviewed.

### P1 - High (Requires Acceptance)

**I1.1: Integration Testing**
- [ ] Contract tests with external services exist.
- [ ] Integration tests cover main workflows.
- [ ] Test environment mirrors production.
- [ ] Tests are automated and run in CI/CD.

**Verification:**
- Integration test suite exists.
- Tests pass in CI/CD.

**I1.2: Health Monitoring**
- [ ] External service health is monitored.
- [ ] Health check failures trigger alerts.
- [ ] Service degradation is detected.
- [ ] Health status is documented.

**Verification:**
- Monitoring dashboards exist.
- Alert rules configured.

**I1.3: Rate Limiting Compliance**
- [ ] External API rate limits are respected.
- [ ] Rate limit headers are honored.
- [ ] Rate limit exceeded behavior is graceful.
- [ ] Rate limit usage is monitored.

**Verification:**
- Rate limiting tests pass.
- Usage monitoring configured.

### P2 - Medium (Should Address)

**I2.1: Integration Documentation**
- [ ] Integration architecture documented.
- [ ] API usage documented.
- [ ] Troubleshooting guide exists.

**I2.2: Service Level Objectives**
- [ ] SLOs defined for external dependencies.
- [ ] SLO compliance is monitored.
- [ ] SLO violations trigger review.

### P3 - Low (Nice to Have)

**I3.1: Advanced Integration Patterns**
- [ ] Event-driven integration evaluated.
- [ ] Message queue integration where appropriate.
- [ ] API gateway considered.

---

## Domain 5: Development (Code Quality and Engineering)

### P0 - Critical (Blocks Production)

**D0.1: Code Quality Standards**
- [ ] Code follows style guidelines.
- [ ] Linting is configured and passing.
- [ ] Code is well-organized and modular.
- [ ] Functions have single responsibilities.
- [ ] Code duplication is minimized.

**Verification:**
- Linting passes in CI/CD.
- Code review confirms quality.
- Complexity metrics are acceptable.

**D0.2: Error Handling**
- [ ] All error paths are handled.
- [ ] Exceptions are not swallowed silently.
- [ ] Errors are logged with context.
- [ ] Error messages are actionable.
- [ ] Resources are cleaned up on error.

**Verification:**
- Error handling code review passed.
- Error path tests pass.
- Error logs reviewed.

**D0.3: Resource Management**
- [ ] Resources (files, connections, memory) are managed properly.
- [ ] Resources are released after use.
- [ ] Resource leaks are not present.
- [ ] Resource limits are enforced.
- [ ] Resource cleanup is tested.

**Verification:**
- Resource management code review passed.
- Memory leak tests pass.
- Connection pool tests pass.

**D0.4: Security in Code**
- [ ] No hardcoded secrets.
- [ ] No SQL injection vulnerabilities.
- [ ] No command injection vulnerabilities.
- [ ] No path traversal vulnerabilities.
- [ ] No XML external entity (XXE) vulnerabilities.

**Verification:**
- Security scan passed.
- SAST tools show no vulnerabilities.

### P1 - High (Requires Acceptance)

**D1.1: Design Patterns**
- [ ] Appropriate design patterns are used.
- [ ] Patterns are applied consistently.
- [ ] Pattern usage is documented.
- [ ] Anti-patterns are avoided.

**Verification:**
- Architecture review passed.
- Design documentation exists.

**D1.2: Code Review Process**
- [ ] All code is reviewed before merge.
- [ ] Reviews check for security, quality, and correctness.
- [ ] Review comments are addressed.
- [ ] Approval from required reviewers obtained.

**Verification:**
- Pull request audit shows all changes reviewed.
- Review checklist exists and is used.

**D1.3: Technical Debt Management**
- [ ] Technical debt is identified and tracked.
- [ ] Debt is prioritized.
- [ ] Debt remediation is planned.
- [ ] Debt is not accumulating uncontrollably.

**Verification:**
- Technical debt inventory exists.
- Debt reduction plan exists.

### P2 - Medium (Should Address)

**D2.1: Code Documentation**
- [ ] Complex logic has comments.
- [ ] Public APIs have docstrings.
- [ ] README is up to date.
- [ ] Contributing guide exists.

**D2.2: Refactoring**
- [ ] Code smells are identified.
- [ ] Refactoring opportunities are documented.
- [ ] Refactoring is planned.

### P3 - Low (Nice to Have)

**D3.1: Code Quality Metrics**
- [ ] Code quality metrics are tracked.
- [ ] Trends are monitored.
- [ ] Quality gates are defined.

---

## Domain 6: Testing (Validation and Verification)

### P0 - Critical (Blocks Production)

**T0.1: Unit Tests**
- [ ] Unit tests exist for all critical components.
- [ ] Unit tests cover happy paths.
- [ ] Unit tests cover error paths.
- [ ] Unit tests are automated and run in CI/CD.
- [ ] Unit tests are reliable (not flaky).

**Verification:**
- Unit test coverage report shows adequate coverage.
- CI/CD runs unit tests on every commit.
- Flaky test rate is low.

**T0.2: Integration Tests**
- [ ] Integration tests cover main workflows.
- [ ] Integration tests test component interactions.
- [ ] Integration tests are automated.
- [ ] Integration tests run in CI/CD.
- [ ] Test environment is representative.

**Verification:**
- Integration test suite exists and passes.
- Integration tests run in CI/CD.

**T0.3: Test Coverage**
- [ ] Critical paths have > 80% coverage.
- [ ] Coverage is measured and reported.
- [ ] Coverage trends are monitored.
- [ ] Coverage drops trigger alerts.
- [ ] Coverage is enforced in CI/CD.

**Verification:**
- Coverage reports reviewed.
- Coverage gates in CI/CD.

**T0.4: Model Evaluation**
- [ ] Model evaluation framework exists.
- [ ] Evaluation metrics are defined.
- [ ] Baseline performance is established.
- [ ] Evaluation is run before deployment.
- [ ] Evaluation results are documented.

**Verification:**
- Evaluation report exists.
- Metrics meet acceptance criteria.

**T0.5: Red Teaming**
- [ ] Red teaming is performed for safety-critical systems.
- [ ] Red teaming includes adversarial inputs.
- [ ] Red teaming findings are addressed.
- [ ] Red teaming is repeated after significant changes.

**Verification:**
- Red teaming report exists.
- Findings are resolved or accepted.

### P1 - High (Requires Acceptance)

**T1.1: Performance Testing**
- [ ] Performance benchmarks exist.
- [ ] Load testing is performed.
- [ ] Performance regression tests exist.
- [ ] Performance is monitored in production.

**Verification:**
- Performance test results exist.
- Regression tests pass.

**T1.2: Security Testing**
- [ ] Security tests are automated.
- [ ] Penetration testing is performed.
- [ ] Vulnerability scanning is automated.
- [ ] Security test results are reviewed.

**Verification:**
- Security scan reports exist.
- Penetration test report exists (if applicable).

**T1.3: Chaos Testing**
- [ ] Chaos tests are designed.
- [ ] Chaos tests simulate realistic failures.
- [ ] Recovery is validated.
- [ ] Chaos tests are run regularly.

**Verification:**
- Chaos test results exist.
- Recovery procedures validated.

**T1.4: Test Automation**
- [ ] Tests are automated.
- [ ] Tests run in CI/CD.
- [ ] Test execution is reliable.
- [ ] Test results are reported.

### P2 - Medium (Should Address)

**T2.1: Edge Case Testing**
- [ ] Edge cases are identified.
- [ ] Edge cases are tested.
- [ ] Edge case coverage is documented.

**T2.2: Negative Testing**
- [ ] Negative test cases exist.
- [ ] Invalid inputs are tested.
- [ ] Error handling is tested.

### P3 - Low (Nice to Have)

**T3.1: Fuzz Testing**
- [ ] Fuzz testing is performed.
- [ ] Fuzzing coverage is monitored.
- [ ] Fuzzing findings are addressed.

---

## Domain 7: Operations (Production Reliability)

### P0 - Critical (Blocks Production)

**O0.1: Deployment Strategy**
- [ ] Deployment strategy is defined (blue-green, canary, rolling).
- [ ] Deployment is automated.
- [ ] Deployment procedure is documented.
- [ ] Deployment is tested in staging.

**Verification:**
- Deployment runbook exists.
- Staging deployment successful.

**O0.2: Rollback Capability**
- [ ] Rollback procedure is documented.
- [ ] Rollback is tested.
- [ ] Rollback meets RTO.
- [ ] Rollback does not cause data loss.
- [ ] Previous version is available.

**Verification:**
- Rollback tested in staging.
- Rollback time meets RTO.
- Rollback runbook exists.

**O0.3: Monitoring and Alerting**
- [ ] Critical metrics are monitored.
- [ ] Alerts are configured for critical failures.
- [ ] Alert routing is correct.
- [ ] On-call rotation is established.
- [ ] Monitoring dashboards exist.

**Verification:**
- Monitoring dashboards reviewed.
- Alert rules tested.
- On-call rotation documented.

**O0.4: Health Checks**
- [ ] Liveness probes implemented.
- [ ] Readiness probes implemented.
- [ ] Health checks verify dependencies.
- [ ] Health check failures trigger alerts.

**Verification:**
- Health check endpoints tested.
- Health check failure alerts tested.

**O0.5: Incident Response**
- [ ] Incident response plan exists.
- [ ] Escalation procedures are defined.
- [ ] Communication plan exists.
- [ ] Incident response is tested (game days).

**Verification:**
- Incident response plan documented.
- Game day conducted.

### P1 - High (Requires Acceptance)

**O1.1: Logging**
- [ ] Structured logging is implemented.
- [ ] Essential log fields are present.
- [ ] Logs are aggregated.
- [ ] Log-based alerting is configured.

**Verification:**
- Log samples reviewed.
- Log aggregation configured.

**O1.2: Tracing**
- [ ] Distributed tracing is implemented.
- [ ] Trace context is propagated.
- [ ] Traces are stored and searchable.
- [ ] Tracing is tested.

**Verification:**
- Trace samples reviewed.
- Tracing infrastructure operational.

**O1.3: Backup and Recovery**
- [ ] Backup procedures exist.
- [ ] Backups are tested for restoration.
- [ ] Backup retention policy exists.
- [ ] Recovery procedures are documented.

**Verification:**
- Backup restoration tested.
- Recovery time meets RTO.

### P2 - Medium (Should Address)

**O2.1: Capacity Planning**
- [ ] Capacity metrics are monitored.
- [ ] Capacity thresholds are defined.
- [ ] Scaling procedures exist.
- [ ] Capacity planning is performed regularly.

**O2.2: Disaster Recovery**
- [ ] Disaster recovery plan exists.
- [ ] DR procedures are tested.
- [ ] RTO and RPO are defined.
- [ ] DR infrastructure is available.

### P3 - Low (Nice to Have)

**O3.1: Advanced Monitoring**
- [ ] Anomaly detection configured.
- [ ] Predictive alerting implemented.
- [ ] Automated remediation for known issues.

---

## Domain 8: Documentation (Knowledge Management)

### P0 - Critical (Blocks Production)

**Doc0.1: API Documentation**
- [ ] API documentation exists.
- [ ] Documentation is accurate and current.
- [ ] All endpoints are documented.
- [ ] Request/response schemas are documented.
- [ ] Error codes are documented.
- [ ] Examples are provided.

**Verification:**
- API documentation reviewed.
- Documentation matches implementation.

**Doc0.2: Runbooks**
- [ ] Runbooks exist for critical operations.
- [ ] Runbooks are step-by-step and actionable.
- [ ] Runbooks are tested.
- [ ] Runbooks are kept up to date.
- [ ] Runbooks are accessible to operators.

**Verification:**
- Runbook review completed.
- Runbook testing performed.

**Doc0.3: Architecture Documentation**
- [ ] System architecture is documented.
- [ ] Data flow is documented.
- [ ] Component interactions are documented.
- [ ] Architecture decisions are recorded (ADRs).

**Verification:**
- Architecture diagram exists and is current.
- ADRs exist for major decisions.

### P1 - High (Requires Acceptance)

**Doc1.1: User Documentation**
- [ ] User guides exist for user-facing features.
- [ ] Getting started guide exists.
- [ ] Troubleshooting guide exists.
- [ ] FAQ exists.

**Verification:**
- User documentation reviewed.
- User feedback collected.

**Doc1.2: Code Documentation**
- [ ] Complex code has comments.
- [ ] Public APIs have docstrings.
- [ ] README is up to date.
- [ ] Contributing guide exists.

**Verification:**
- Code review checks documentation.
- Documentation coverage measured.

**Doc1.3: Change Documentation**
- [ ] Changelog is maintained.
- [ ] Release notes are written.
- [ ] Migration guides exist for breaking changes.
- [ ] Deprecation notices are provided.

**Verification:**
- Changelog reviewed.
- Release notes published.

### P2 - Medium (Should Address)

**Doc2.1: Internal Documentation**
- [ ] Internal wikis are up to date.
- [ ] Internal APIs are documented.
- [ ] Onboarding documentation exists.

**Doc2.2: Training Materials**
- [ ] Training materials exist.
- [ ] Training is conducted for new team members.

### P3 - Low (Nice to Have)

**Doc3.1: Video Tutorials**
- [ ] Video tutorials for complex features.
- [ ] Video tutorials for common tasks.

**Doc3.2: Interactive Documentation**
- [ ] Interactive API explorer.
- [ ] Live code examples.

---

## Domain 9: Performance (Efficiency and Scalability)

### P0 - Critical (Blocks Production)

**P0.1: Latency Requirements**
- [ ] Latency requirements are defined.
- [ ] Latency is measured and monitored.
- [ ] Latency meets requirements.
- [ ] Latency regression is detected.

**Verification:**
- Latency benchmarks meet targets.
- Latency monitoring configured.
- Regression tests pass.

**P0.2: Throughput Requirements**
- [ ] Throughput requirements are defined.
- [ ] Throughput is measured and monitored.
- [ ] Throughput meets requirements.
- [ ] Throughput regression is detected.

**Verification:**
- Throughput benchmarks meet targets.
- Load testing passed.

**P0.3: Resource Utilization**
- [ ] Resource utilization is monitored.
- [ ] Resource limits are defined.
- [ ] Resource exhaustion is handled.
- [ ] Resource leaks are not present.

**Verification:**
- Resource monitoring configured.
- Resource limit tests pass.
- Memory leak tests pass.

**P0.4: Scalability**
- [ ] System can scale to meet demand.
- [ ] Scaling is automated or documented.
- [ ] Scaling limits are known.
- [ ] Scaling behavior is tested.

**Verification:**
- Load testing at expected scale.
- Scaling procedures tested.

### P1 - High (Requires Acceptance)

**P1.1: Caching Strategy**
- [ ] Caching strategy is defined.
- [ ] Cache invalidation is handled.
- [ ] Cache hit rates are monitored.
- [ ] Cache failures are handled gracefully.

**Verification:**
- Cache configuration reviewed.
- Cache hit rate metrics collected.

**P1.2: Database Performance**
- [ ] Database queries are optimized.
- [ ] Query performance is monitored.
- [ ] Slow queries are identified and addressed.
- [ ] Database connection pooling is configured.

**Verification:**
- Query performance metrics reviewed.
- Slow query log reviewed.

**P1.3: Cost Optimization**
- [ ] Cost implications are understood.
- [ ] Cost monitoring is implemented.
- [ ] Cost optimization opportunities are identified.
- [ ] Cost alerts are configured.

**Verification:**
- Cost monitoring configured.
- Cost analysis completed.

### P2 - Medium (Should Address)

**P2.1: Performance Profiling**
- [ ] Performance profiling is performed.
- [ ] Bottlenecks are identified.
- [ ] Profiling results are documented.

**P2.2: Caching Optimization**
- [ ] Cache hit rates are optimized.
- [ ] Cache invalidation is optimized.
- [ ] Cache warming strategies exist.

### P3 - Low (Nice to Have)

**P3.1: Advanced Optimization**
- [ ] Query optimization performed.
- [ ] Index optimization performed.
- [ ] Algorithm optimization considered.

---

## Domain 10: Compliance (Regulatory and Legal)

### P0 - Critical (Blocks Production)

**C0.1: Regulatory Requirement Identification**
- [ ] Applicable regulations are identified.
- [ ] Regulatory requirements are documented.
- [ ] Compliance status is assessed.
- [ ] Compliance gaps are identified.

**Verification:**
- Regulatory requirement mapping exists.
- Compliance assessment completed.

**C0.2: Audit Trail**
- [ ] Audit logging is implemented.
- [ ] Audit logs capture required events.
- [ ] Audit logs are tamper-resistant.
- [ ] Audit logs are retained for required period.
- [ ] Audit logs are accessible for review.

**Verification:**
- Audit log samples reviewed.
- Retention policy documented.
- Log integrity verified.

**C0.3: Data Governance**
- [ ] Data governance policies exist.
- [ ] Data classification is performed.
- [ ] Data access controls are implemented.
- [ ] Data retention policies are enforced.
- [ ] Data deletion procedures exist.

**Verification:**
- Governance policy document exists.
- Data classification completed.
- Access controls tested.

**C0.4: Privacy Protection**
- [ ] Privacy impact assessment completed.
- [ ] PII/PHI is identified and protected.
- [ ] Data minimization is applied.
- [ ] User consent is obtained where required.
- [ ] Data subject rights are supported.

**Verification:**
- Privacy impact assessment document exists.
- PII/PHI inventory exists.
- Consent mechanisms implemented.

### P1 - High (Requires Acceptance)

**C1.1: Compliance Testing**
- [ ] Compliance tests are automated.
- [ ] Compliance checks run in CI/CD.
- [ ] Compliance violations are detected and alerted.
- [ ] Compliance metrics are reported.

**Verification:**
- Compliance test results reviewed.
- Compliance monitoring configured.

**C1.2: Data Processing Agreements**
- [ ] Data processing agreements are in place.
- [ ] Subprocessor management is documented.
- [ ] Data transfer mechanisms are compliant.

**Verification:**
- DPAs reviewed and current.
- Subprocessor inventory exists.

**C1.3: Regulatory Reporting**
- [ ] Required regulatory reports are defined.
- [ ] Reporting procedures exist.
- [ ] Reports are generated on schedule.
- [ ] Report retention is managed.

**Verification:**
- Reporting schedule documented.
- Sample reports reviewed.

### P2 - Medium (Should Address)

**C2.1: Compliance Training**
- [ ] Team receives compliance training.
- [ ] Training records are maintained.
- [ ] Training is refreshed regularly.

**C2.2: Audit Preparation**
- [ ] Audit procedures are documented.
- [ ] Audit evidence packages are prepared.
- [ ] Audit response procedures exist.

### P3 - Low (Nice to Have)

**C3.1: Advanced Compliance Automation**
- [ ] Automated compliance scanning.
- [ ] Compliance dashboard.
- [ ] Automated evidence collection.

---

## Appendix: Quick Domain Reference

### Domain Quick Reference Table

| Domain | Primary Concern | Key P0 Items | Typical Evidence |
|--------|----------------|--------------|------------------|
| Core | AI system fundamentals | Model selection, prompt design, context management | Model evaluation reports, prompt validation tests |
| Security | Threat protection | Authentication, authorization, input validation, output filtering | Security scans, penetration tests, auth tests |
| Data | Data governance and privacy | Data quality, validation, encryption, retention | Data quality reports, privacy assessments |
| Integration | External connectivity | API contracts, versioning, timeouts, error handling | Integration tests, contract tests, API specs |
| Development | Code quality | Error handling, resource management, no hardcoded secrets | Code reviews, SAST scans, linting results |
| Testing | Validation | Unit tests, integration tests, coverage, evaluation | Test reports, coverage reports, evaluation results |
| Operations | Production reliability | Deployment, rollback, monitoring, incident response | Deployment logs, monitoring dashboards, runbooks |
| Documentation | Knowledge management | API docs, runbooks, architecture docs | Documentation reviews, user feedback |
| Performance | Efficiency | Latency, throughput, resource utilization, scalability | Performance benchmarks, load tests, metrics |
| Compliance | Regulatory | Audit trails, data governance, privacy | Compliance checklists, audit reports, DPAs |

### Checklist Priority Matrix

| Checklist Item | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------------|--------|--------|--------|--------|
| P0 Items | Mandatory | Mandatory | Mandatory | Mandatory |
| P1 Items | Mandatory or Accepted | Accepted | Recommended | Recommended |
| P2 Items | Recommended | Recommended | Optional | Optional |
| P3 Items | Optional | Optional | Optional | Optional |

### Evidence Quick Reference

| Evidence Type | Collection Method | Storage | Retention |
|--------------|-------------------|---------|-----------|
| Test Results | Automated in CI/CD | Artifact repository | 1-3 years |
| Security Scans | Automated in CI/CD | Artifact repository | 3-7 years |
| Performance Tests | Scheduled or on-demand | Artifact repository | 1-2 years |
| Documentation | Manual/automated | Version control | Permanent |
| Audit Logs | Automated | Log aggregation | 2-7 years (regulatory) |
| Configuration | Automated | Version control | Permanent |
| Compliance Reports | Periodic | Document management | 3-7 years (regulatory) |
