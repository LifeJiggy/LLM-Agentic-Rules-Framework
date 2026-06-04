# Audit Findings Reference

Use this reference for common audit findings across all 10 framework domains, including their severity classifications, root causes, and remediation guidance.

## Findings Reference Philosophy

This reference catalogs the most common audit findings organized by domain and severity. Each finding includes:

- **Finding ID**: Unique identifier for tracking
- **Severity**: P0/P1/P2/P3 classification
- **Domain**: Which domain the finding relates to
- **Violated Rule**: Specific framework rule or checklist item
- **Production Risk**: Description of potential impact
- **Root Cause**: Why the issue exists
- **Concrete Fix**: Step-by-step remediation
- **Required Evidence**: What evidence is needed to verify the fix
- **Prevention**: How to prevent this finding in the future

## How to Use This Reference

1. During audit, use this reference to quickly identify and classify findings.
2. Reference the finding ID in audit reports for consistency.
3. Use the concrete fix as a starting point for remediation plans.
4. Use the prevention section to improve processes and prevent recurrence.

## Domain 1: Core (AI System Fundamentals)

### CORE-001: No Model Selection Rationale

**Severity:** P0

**Violated Rule:** Core P0 - Model Selection Rationale

**Production Risk:**
- Inappropriate model for use case leads to poor performance
- Model limitations not understood lead to failures
- No rollback strategy if model underperforms
- Difficulty justifying model choice to stakeholders

**Root Cause:**
- Model selected without formal evaluation
- No documented requirements for model capabilities
- No comparison of alternative models
- No assessment of model limitations

**Concrete Fix:**
1. Document system requirements (latency, accuracy, cost)
2. Evaluate 2-3 candidate models against requirements
3. Document model selection rationale
4. Document model limitations and mitigations
5. Define model fallback strategy
6. Create model evaluation report

**Required Evidence:**
- Model selection document with rationale
- Model evaluation report with metrics
- Model limitation documentation
- Fallback strategy documented

**Prevention:**
- Require model selection document for all new systems
- Include model evaluation in development process
- Review model selection in code review

---

### CORE-002: Prompts Vulnerable to Injection

**Severity:** P0

**Violated Rule:** Core P0 - Prompt Design and Validation, Security P0 - Input Validation

**Production Risk:**
- Attackers manipulate model behavior via prompt injection
- System generates harmful or unauthorized content
- Data exfiltration via prompt injection
- Bypass of safety filters

**Root Cause:**
- Prompts not designed with injection resistance
- No input sanitization for user-provided content
- No output validation for injection attempts
- No testing for prompt injection vulnerabilities

**Concrete Fix:**
1. Review all prompts for injection vulnerabilities
2. Implement input sanitization for user content
3. Add output validation to detect injection
4. Implement prompt injection detection and logging
5. Add prompt injection tests to test suite
6. Conduct red teaming for prompt injection

**Required Evidence:**
- Prompt injection test results
- Red teaming report
- Input sanitization code review
- Output validation tests

**Prevention:**
- Include prompt injection review in code review process
- Add prompt injection tests to CI/CD
- Conduct regular red teaming
- Train developers on prompt injection risks

---

### CORE-003: No Context Window Overflow Handling

**Severity:** P0

**Violated Rule:** Core P0 - Context Window Management

**Production Risk:**
- System crashes when context exceeds model limits
- Truncation of important context leads to poor responses
- Token counting errors lead to unexpected failures
- Poor user experience due to context-related errors

**Root Cause:**
- No context window limits defined
- No overflow handling implemented
- Token counting not implemented or inaccurate
- No context prioritization strategy

**Concrete Fix:**
1. Define context window limits for all components
2. Implement accurate token counting
3. Implement context overflow handling (truncation, summarization, etc.)
4. Define context prioritization strategy
5. Add context overflow tests
6. Monitor context window usage

**Required Evidence:**
- Token counting tests passing
- Context overflow handling tests passing
- Context usage metrics in monitoring
- Documentation of context management strategy

**Prevention:**
- Include context management in design reviews
- Test context overflow scenarios
- Monitor context usage in production

---

### CORE-004: No Model Rollback Capability

**Severity:** P0

**Violated Rule:** Operations P0 - Rollback Capability

**Production Risk:**
- Cannot recover from model failures or regressions
- Extended outages if model causes issues
- Difficulty reverting to previous model version
- Manual rollback process is error-prone

**Root Cause:**
- No model versioning system
- No rollback procedure documented
- No testing of model rollback
- Model deployment not integrated with CI/CD

**Concrete Fix:**
1. Implement model versioning system
2. Document model rollback procedure
3. Test model rollback in staging
4. Automate model rollback where possible
5. Define rollback triggers
6. Measure rollback time

**Required Evidence:**
- Model versioning system implemented
- Rollback runbook documented
- Rollback tested successfully
- Rollback time meets RTO

**Prevention:**
- Require rollback testing before model deployment
- Include model rollback in deployment checklist
- Automate model deployment and rollback

---

## Domain 2: Security (Threat Protection)

### SEC-001: Missing Authentication on API Endpoints

**Severity:** P0

**Violated Rule:** Security P0 - Authentication

**Production Risk:**
- Unauthorized access to system and data
- Data breach and exposure
- Unauthorized data modification or deletion
- Compliance violations (GDPR, HIPAA, etc.)
- Reputation damage

**Root Cause:**
- Authentication not implemented during development
- Authentication bypassed for convenience
- No security review of API endpoints
- Incomplete understanding of security requirements

**Concrete Fix:**
1. Implement authentication middleware (OAuth 2.0, JWT, etc.)
2. Add authentication checks to all protected endpoints
3. Implement token validation
4. Implement token refresh mechanism
5. Add authentication tests
6. Review and fix all unauthenticated endpoints

**Required Evidence:**
- Authentication tests passing
- Security scan showing no auth bypass
- Code review of auth implementation
- Penetration test results (if applicable)

**Prevention:**
- Require authentication in API design
- Include auth checks in code review checklist
- Run security scans in CI/CD
- Conduct regular security reviews

---

### SEC-002: No Input Validation

**Severity:** P0

**Violated Rule:** Security P0 - Input Validation

**Production Risk:**
- Injection attacks (SQL, command, XSS, prompt injection)
- Data corruption
- System compromise
- Data exfiltration
- Service disruption

**Root Cause:**
- Trust in user input without validation
- No input validation framework
- Lack of security awareness
- No security testing

**Concrete Fix:**
1. Implement input validation at all boundaries
2. Use parameterized queries for database access
3. Sanitize user input
4. Validate file uploads (type, size, content)
5. Implement schema validation for API inputs
6. Add validation tests
7. Conduct fuzz testing

**Required Evidence:**
- Input validation tests passing
- Fuzz testing results
- Security scan showing no injection vulnerabilities
- Code review of validation logic

**Prevention:**
- Include input validation in code review checklist
- Add validation tests to CI/CD
- Conduct security training
- Use security linters

---

### SEC-003: Hardcoded Secrets in Code

**Severity:** P0

**Violated Rule:** Security P0 - API Key and Credential Management

**Production Risk:**
- Credential exposure in code repositories
- Unauthorized access to services and data
- Security breach
- Compliance violations
- Difficulty rotating credentials

**Root Cause:**
- Secrets committed during development
- No secret management system
- Lack of secret scanning in CI/CD
- Inadequate security training

**Concrete Fix:**
1. Scan git history for exposed secrets
2. Rotate all exposed credentials
3. Remove secrets from code
4. Implement secret management system (Vault, AWS Secrets Manager, etc.)
5. Configure secret scanning in CI/CD
6. Document secret management procedures
7. Train team on secret management

**Required Evidence:**
- Secret scan showing no hardcoded secrets
- Secret management system configured
- Credential rotation completed
- CI/CD secret scanning configured

**Prevention:**
- Configure secret scanning in CI/CD
- Use pre-commit hooks for secret detection
- Train developers on secret management
- Regular secret scanning audits

---

### SEC-004: No Output Filtering for Harmful Content

**Severity:** P0

**Violated Rule:** Security P0 - Output Filtering

**Production Risk:**
- System generates harmful, offensive, or dangerous content
- Legal liability for harmful outputs
- Reputation damage
- User harm
- Regulatory violations

**Root Cause:**
- No output filtering implemented
- No content moderation
- No testing for harmful outputs
- No red teaming for safety

**Concrete Fix:**
1. Implement output content filtering
2. Define harmful content categories
3. Implement content moderation API
4. Add output filtering tests
5. Conduct red teaming for harmful outputs
6. Implement output validation
7. Log and monitor filtering triggers

**Required Evidence:**
- Output filtering tests passing
- Red teaming report
- Content moderation implementation reviewed
- Monitoring of filtering triggers

**Prevention:**
- Include output filtering in design reviews
- Test for harmful outputs in CI/CD
- Conduct regular red teaming
- Monitor output quality in production

---

### SEC-005: No Rate Limiting

**Severity:** P1

**Violated Rule:** Security P1 - Rate Limiting and Abuse Prevention

**Production Risk:**
- Abuse of system resources
- Denial of service attacks
- Excessive costs from API usage
- Degraded performance for legitimate users
- Service unavailability

**Root Cause:**
- Rate limiting not considered in design
- No abuse detection mechanisms
- No cost controls for API usage
- Lack of load testing

**Concrete Fix:**
1. Define rate limits based on system capacity
2. Implement rate limiting middleware
3. Implement abuse detection
4. Define rate limit exceeded behavior
5. Add rate limiting tests
6. Monitor rate limit metrics
7. Implement cost alerts

**Required Evidence:**
- Rate limiting tests passing
- Load tests showing rate limiting effectiveness
- Rate limit configuration documented
- Monitoring of rate limit metrics

**Prevention:**
- Include rate limiting in design reviews
- Test rate limiting in load tests
- Monitor rate limit metrics in production

---

## Domain 3: Data (Data Governance and Privacy)

### DATA-001: No Data Quality Monitoring

**Severity:** P1

**Violated Rule:** Data P0 - Data Quality

**Production Risk:**
- Poor data quality leads to poor model performance
- Data corruption not detected
- Training data differs from production data
- Silent failures due to bad data

**Root Cause:**
- Data quality not considered in design
- No data validation pipeline
- No monitoring of data quality metrics
- No data quality tests

**Concrete Fix:**
1. Define data quality metrics (completeness, accuracy, consistency, etc.)
2. Implement data validation at ingestion
3. Implement data quality monitoring
4. Set up alerts for data quality degradation
5. Implement data quality tests
6. Create data quality dashboard

**Required Evidence:**
- Data quality metrics defined and documented
- Data quality monitoring configured
- Data quality tests passing
- Data quality dashboard exists

**Prevention:**
- Include data quality in design reviews
- Monitor data quality in production
- Regular data quality audits

---

### DATA-002: Sensitive Data Not Encrypted

**Severity:** P0

**Violated Rule:** Security P0 - Sensitive Data Protected, Data P0 - Data Storage and Encryption

**Production Risk:**
- Data breach and exposure
- Compliance violations (GDPR, HIPAA, PCI)
- Legal liability
- Reputation damage
- Loss of user trust

**Root Cause:**
- Encryption not implemented
- Encryption misconfigured
- Lack of security review
- Inadequate understanding of encryption requirements

**Concrete Fix:**
1. Identify all sensitive data (PII, PHI, credentials, etc.)
2. Implement encryption at rest (database encryption, file encryption)
3. Implement encryption in transit (TLS)
4. Verify encryption is correctly configured
5. Implement key management
6. Test encryption implementation
7. Document encryption strategy

**Required Evidence:**
- Encryption implementation verified
- Security scan showing encryption enabled
- Data classification completed
- Key management system configured

**Prevention:**
- Require encryption in design reviews
- Include encryption in security checklist
- Regular security scans for encryption
- Security training on encryption

---

### DATA-003: No Data Retention Policies

**Severity:** P1

**Violated Rule:** Data P1 - Data Retention

**Production Risk:**
- Data retained longer than required (compliance violation)
- Data deleted too early (business impact)
- Unclear data lifecycle
- Difficulty responding to data subject requests
- Storage cost overruns

**Root Cause:**
- Data retention not considered in design
- No data classification
- No automated retention enforcement
- Lack of compliance awareness

**Concrete Fix:**
1. Classify all data by type and sensitivity
2. Define retention periods for each data type
3. Implement automated retention enforcement
4. Implement data deletion procedures
5. Document retention policies
6. Implement audit logging for data lifecycle
7. Review and update policies regularly

**Required Evidence:**
- Data retention policy documented
- Retention enforcement implemented
- Data deletion procedures tested
- Compliance review completed

**Prevention:**
- Include data retention in design reviews
- Regular data retention audits
- Automated compliance checks

---

### DATA-004: Data Provenance Not Tracked

**Severity:** P2

**Violated Rule:** Data P1 - Data Lineage

**Production Risk:**
- Cannot trace data origins
- Difficulty debugging data issues
- Compliance violations (data governance)
- Difficulty responding to data quality issues
- Poor data governance

**Root Cause:**
- Data lineage not considered in design
- No data lineage tracking system
- Multiple data sources without tracking
- Lack of data governance process

**Concrete Fix:**
1. Document all data sources
2. Implement data lineage tracking
3. Document data transformations
4. Implement data provenance metadata
5. Create data lineage documentation
6. Implement data lineage monitoring

**Required Evidence:**
- Data lineage documentation exists
- Data provenance metadata implemented
- Data lineage diagram exists
- Data governance process documented

**Prevention:**
- Include data lineage in design reviews
- Regular data governance reviews
- Data lineage training

---

## Domain 4: Integration (External System Connectivity)

### INT-001: No Timeout on External API Calls

**Severity:** P1

**Violated Rule:** Integration P0 - Timeout and Retry Configuration

**Production Risk:**
- Hanging operations when external API is slow
- Resource exhaustion (threads, connections)
- Cascading failures across system
- Poor user experience (long waits or timeouts)
- System unavailability

**Root Cause:**
- Timeouts not configured by default
- Lack of awareness of timeout importance
- No timeout standards or guidelines
- No testing of timeout behavior

**Concrete Fix:**
1. Add timeout to all external API calls
2. Document timeout values and rationale
3. Implement timeout handling
4. Add timeout tests
5. Monitor timeout occurrences
6. Review and adjust timeouts based on metrics

**Required Evidence:**
- Code review confirming timeouts on all external calls
- Timeout handling tests passing
- Monitoring showing timeout occurrences
- Timeout values documented

**Prevention:**
- Include timeouts in code review checklist
- Use libraries that enforce timeouts by default
- Monitor timeout metrics
- Regular timeout configuration reviews

---

### INT-002: No Retry Logic for Transient Failures

**Severity:** P1

**Violated Rule:** Integration P0 - Timeout and Retry Configuration

**Production Risk:**
- Transient failures cause permanent errors
- Poor user experience due to avoidable failures
- Increased support burden
- Reduced system reliability

**Root Cause:**
- Retry logic not implemented
- No retry strategy defined
- Fear of retry side effects
- Lack of understanding of transient vs. permanent failures

**Concrete Fix:**
1. Identify external calls that need retry
2. Implement retry with exponential backoff and jitter
3. Define retryable error types
4. Set maximum retry count and total timeout
5. Ensure idempotency or use exactly-once semantics
6. Add retry tests
7. Monitor retry rates

**Required Evidence:**
- Retry logic implemented and tested
- Retry configuration documented
- Monitoring of retry metrics
- Idempotency verified

**Prevention:**
- Include retry logic in design reviews
- Test retry behavior in CI/CD
- Monitor retry metrics in production

---

### INT-003: No Circuit Breaker for External Dependencies

**Severity:** P1

**Violated Rule:** Integration P0 - Error Handling and Fallback

**Production Risk:**
- Cascading failures when external service fails
- Resource exhaustion from failed calls
- System-wide outage from single dependency failure
- Poor user experience during outages

**Root Cause:**
- Circuit breaker pattern not known or considered
- No awareness of cascading failure risk
- Focus on happy path only
- No failure testing

**Concrete Fix:**
1. Identify critical external dependencies
2. Implement circuit breaker for each critical dependency
3. Define circuit breaker thresholds (failure count, timeout)
4. Implement fallback behavior when circuit is open
5. Monitor circuit breaker state
6. Test circuit breaker behavior
7. Document circuit breaker configuration

**Required Evidence:**
- Circuit breaker implementation reviewed
- Circuit breaker tests passing
- Monitoring of circuit breaker state
- Fallback behavior tested

**Prevention:**
- Include circuit breakers in design reviews
- Test circuit breaker behavior
- Monitor circuit breaker metrics
- Chaos testing for dependency failures

---

### INT-004: No Fallback for Critical External Services

**Severity:** P1

**Violated Rule:** Integration P0 - Error Handling and Fallback

**Production Risk:**
- System unavailable when external service is down
- Complete failure from single dependency
- No graceful degradation
- Poor user experience during outages

**Root Cause:**
- Fallback behavior not considered
- Single points of failure in architecture
- No degradation strategy
- Focus on happy path only

**Concrete Fix:**
1. Identify critical external dependencies
2. Define fallback behavior for each (cached data, default values, degraded mode)
3. Implement fallback logic
4. Test fallback behavior
5. Monitor fallback activation
6. Document fallback strategy

**Required Evidence:**
- Fallback behavior documented
- Fallback implementation tested
- Monitoring of fallback activation
- User experience during fallback verified

**Prevention:**
- Include fallback design in architecture reviews
- Test fallback behavior regularly
- Monitor fallback activation in production

---

## Domain 5: Development (Code Quality)

### DEV-001: Missing Error Handling in Critical Paths

**Severity:** P0

**Violated Rule:** Development P0 - Error Handling

**Production Risk:**
- Unhandled exceptions cause system crashes
- Poor error messages for users
- Data loss or corruption
- System unavailability
- Difficult debugging

**Root Cause:**
- Focus on happy path during development
- No error handling guidelines
- Incomplete testing of error paths
- Lack of code review for error handling

**Concrete Fix:**
1. Identify all critical paths
2. Add exception handling to all critical paths
3. Use specific exception types
4. Log errors with context
5. Return appropriate error responses
6. Add error handling tests
7. Review error handling in code review

**Required Evidence:**
- Error handling code review passed
- Error path tests passing
- Error logs reviewed
- Exception handling guidelines documented

**Prevention:**
- Include error handling in code review checklist
- Test error paths in CI/CD
- Use linters to detect bare except clauses
- Error handling training

---

### DEV-002: Hardcoded Configuration Values

**Severity:** P1

**Violated Rule:** Development P0 - Code Quality Standards, Security P0 - Credential Management

**Production Risk:**
- Configuration changes require code changes
- Environment-specific issues
- Secrets exposed in code
- Difficulty managing different environments
- Accidental commitment of secrets

**Root Cause:**
- Configuration not externalized
- Environment variables not used
- No configuration management system
- Development convenience prioritized over best practices

**Concrete Fix:**
1. Externalize all configuration
2. Use environment variables for configuration
3. Use configuration management system
4. Document all configuration options
5. Validate configuration at startup
6. Add configuration validation tests
7. Remove hardcoded values

**Required Evidence:**
- Configuration files reviewed (no hardcoded values)
- Configuration validation tests passing
- Environment variable documentation exists
- Configuration management system configured

**Prevention:**
- Include configuration review in code review
- Use linters to detect hardcoded values
- Configuration management training
- Pre-commit hooks for secret detection

---

### DEV-003: Resource Leaks (Files, Connections)

**Severity:** P1

**Violated Rule:** Development P0 - Resource Management

**Production Risk:**
- File descriptor exhaustion
- Memory leaks
- Connection pool exhaustion
- System slowdown or crash
- Resource starvation for other processes

**Root Cause:**
- Resources not properly released
- No context managers or try-finally
- Exception handling doesn't clean up resources
- No resource leak testing

**Concrete Fix:**
1. Identify all resource acquisitions (files, connections, memory)
2. Use context managers (with statements) for resource management
3. Ensure resources are released in finally blocks
4. Add resource leak detection to tests
5. Use profiling tools to detect leaks
6. Review resource management in code review

**Required Evidence:**
- Resource management code review passed
- Resource leak tests passing
- Memory profiling results (if applicable)
- Connection pool tests passing

**Prevention:**
- Include resource management in code review checklist
- Use static analysis tools to detect resource leaks
- Resource management training
- Regular profiling and leak detection

---

### DEV-004: No Code Review Process

**Severity:** P1

**Violated Rule:** Development P1 - Code Review Process

**Production Risk:**
- Bugs and security vulnerabilities not caught
- Inconsistent code quality
- Knowledge silos
- Technical debt accumulation
- Team morale issues

**Root Cause:**
- No code review process defined
- Time pressure to ship features
- Lack of understanding of code review benefits
- No enforcement of code review

**Concrete Fix:**
1. Define code review process
2. Create code review checklist
3. Require reviews for all changes
4. Define reviewer requirements
5. Set review turnaround time
6. Track code review metrics
7. Train team on effective code review

**Required Evidence:**
- Code review process documented
- Code review checklist exists
- Pull request audit shows reviews happening
- Code review metrics tracked

**Prevention:**
- Enforce code review in CI/CD (require approvals)
- Regular code review process reviews
- Code review training
- Lead by example (senior engineers review)

---

## Domain 6: Testing (Validation and Verification)

### TEST-001: Low Test Coverage

**Severity:** P1

**Violated Rule:** Testing P1 - Comprehensive Test Coverage

**Production Risk:**
- Undetected bugs in uncovered code
- Regressions not caught
- Poor code quality
- Difficult refactoring
- Low confidence in changes

**Root Cause:**
- Testing not prioritized
- Time pressure to ship features
- No coverage requirements
- No coverage monitoring
- Difficult to test (tightly coupled code, no mocking)

**Concrete Fix:**
1. Set coverage target (80% for critical paths)
2. Identify critical paths with low coverage
3. Write tests for uncovered critical paths
4. Configure coverage reporting in CI/CD
5. Set coverage thresholds in CI/CD
6. Improve testability (dependency injection, etc.)
7. Monitor coverage trends

**Required Evidence:**
- Coverage report showing > 80% for critical paths
- Tests passing in CI/CD
- Coverage trend improving
- Test quality review

**Prevention:**
- Include coverage in CI/CD gates
- Review coverage in code review
- Set coverage targets for teams
- Regular coverage reviews

---

### TEST-002: No Integration Tests

**Severity:** P1

**Violated Rule:** Testing P0 - Integration Tests

**Production Risk:**
- Component interactions not tested
- Integration issues not caught until production
- Interface mismatches
- Data flow issues
- Poor system reliability

**Root Cause:**
- Focus on unit tests only
- Integration tests considered too difficult
- No integration test environment
- Lack of integration testing skills

**Concrete Fix:**
1. Identify main workflows to test
2. Set up integration test environment
3. Write integration tests for main workflows
4. Automate integration tests
5. Run integration tests in CI/CD
6. Monitor integration test results

**Required Evidence:**
- Integration test suite exists and passes
- Integration tests run in CI/CD
- Test coverage for main workflows
- Integration test environment documented

**Prevention:**
- Include integration tests in definition of done
- Review integration tests in code review
- Regular integration test reviews
- Integration test training

---

### TEST-003: No Model Evaluation

**Severity:** P0 (for AI systems)

**Violated Rule:** Testing P0 - Model Evaluation

**Production Risk:**
- Model quality not verified
- Model performs poorly in production
- Harmful outputs not detected
- Biases not identified
- Safety issues not caught

**Root Cause:**
- Model evaluation not considered
- No evaluation framework
- No baseline for comparison
- No red teaming for safety

**Concrete Fix:**
1. Define evaluation metrics (accuracy, relevance, safety, etc.)
2. Create evaluation dataset
3. Implement evaluation framework
4. Establish performance baseline
5. Conduct red teaming for safety
6. Run evaluation before deployment
7. Monitor model performance in production

**Required Evidence:**
- Model evaluation report exists
- Evaluation metrics meet acceptance criteria
- Red teaming report exists
- Baseline performance documented

**Prevention:**
- Require model evaluation before deployment
- Include evaluation in CI/CD
- Regular model performance monitoring
- Red teaming on a schedule

---

### TEST-004: No Performance Testing

**Severity:** P1

**Violated Rule:** Testing P1 - Performance Testing

**Production Risk:**
- System unable to handle production load
- Poor performance under stress
- Scaling issues not identified
- Capacity planning based on guesses
- User experience degradation

**Root Cause:**
- Performance testing not prioritized
- No performance benchmarks
- No performance testing environment
- Lack of performance testing skills

**Concrete Fix:**
1. Define performance requirements (latency, throughput)
2. Set up performance testing environment
3. Create performance test suite
4. Run baseline performance tests
5. Run load tests at expected scale
6. Document performance benchmarks
7. Monitor performance in production

**Required Evidence:**
- Performance test results exist
- Performance benchmarks documented
- Load testing passed
- Performance monitoring configured

**Prevention:**
- Include performance testing in CI/CD
- Set performance budgets
- Regular performance reviews
- Performance monitoring in production

---

## Domain 7: Operations (Production Reliability)

### OPS-001: No Monitoring or Alerting

**Severity:** P0

**Violated Rule:** Operations P0 - Monitoring and Alerting

**Production Risk:**
- Failures not detected until users report
- Extended outages
- Slow incident response
- Poor user experience
- Revenue loss

**Root Cause:**
- Monitoring not implemented
- Monitoring considered optional
- No monitoring tools or infrastructure
- Lack of operations expertise

**Concrete Fix:**
1. Define critical metrics to monitor (golden signals: latency, traffic, errors, saturation)
2. Set up monitoring infrastructure (Prometheus, Datadog, etc.)
3. Create monitoring dashboards
4. Configure alerts for critical failures
5. Set up on-call rotation
6. Test alerts
7. Document monitoring setup

**Required Evidence:**
- Monitoring dashboards exist and are populated
- Alert rules configured and tested
- On-call rotation established
- Monitoring coverage documented

**Prevention:**
- Require monitoring in design reviews
- Include monitoring in deployment checklist
- Regular monitoring reviews
- Alert tuning and optimization

---

### OPS-002: No Rollback Capability

**Severity:** P0

**Violated Rule:** Operations P0 - Rollback Capability

**Production Risk:**
- Cannot recover from bad deployments
- Extended outages
- Manual rollback is error-prone
- Data loss during rollback
- Business impact from downtime

**Root Cause:**
- Rollback not considered in deployment design
- No rollback procedure documented
- Rollback never tested
- Manual rollback process

**Concrete Fix:**
1. Document rollback procedure
2. Test rollback in staging
3. Automate rollback where possible
4. Define rollback triggers
5. Ensure previous versions are available
6. Measure rollback time
7. Ensure rollback doesn't cause data loss

**Required Evidence:**
- Rollback runbook documented
- Rollback tested successfully
- Rollback time meets RTO
- Database rollback procedures documented

**Prevention:**
- Test rollback before every deployment
- Include rollback in deployment checklist
- Automate rollback
- Regular rollback drills

---

### OPS-003: No Health Checks

**Severity:** P1

**Violated Rule:** Operations P1 - Health Checks

**Production Risk:**
- Unhealthy instances receive traffic
- Failures not detected by load balancer
- Partial outages not caught
- Poor user experience
- Extended recovery time

**Root Cause:**
- Health checks not implemented
- Health checks not configured in load balancer
- Health checks only check process, not functionality
- No monitoring of health check failures

**Concrete Fix:**
1. Implement liveness probe (is process running?)
2. Implement readiness probe (is service ready for traffic?)
3. Implement health check endpoint
4. Configure health checks in load balancer
5. Alert on health check failures
6. Test health checks
7. Monitor health check metrics

**Required Evidence:**
- Health check endpoints implemented and tested
- Health checks configured in load balancer
- Health check failure alerts configured
- Health check monitoring exists

**Prevention:**
- Include health checks in deployment checklist
- Test health checks in CI/CD
- Monitor health check metrics
- Regular health check reviews

---

### OPS-004: No Incident Response Plan

**Severity:** P1

**Violated Rule:** Operations P1 - Incident Response

**Production Risk:**
- Chaotic response to incidents
- Extended outage duration
- Poor communication during incidents
- Repeat incidents due to lack of learning
- Low team morale

**Root Cause:**
- Incident response not planned
- No incident response team
- No runbooks for common failures
- No incident response training

**Concrete Fix:**
1. Create incident response plan
2. Define escalation procedures
3. Establish on-call rotation
4. Create runbooks for common failures
5. Conduct incident response training
6. Perform regular game days
7. Document incident response procedures

**Required Evidence:**
- Incident response plan documented
- On-call rotation established
- Runbooks exist for critical scenarios
- Game day conducted

**Prevention:**
- Regular incident response training
- Regular game days
- Post-incident reviews
- Continuous improvement of runbooks

---

## Domain 8: Documentation (Knowledge Management)

### DOC-001: No API Documentation

**Severity:** P1

**Violated Rule:** Documentation P0 - API Documentation

**Production Risk:**
- Users cannot integrate with API
- Increased support burden
- Integration errors
- Slow adoption
- Developer frustration

**Root Cause:**
- Documentation not prioritized
- No documentation process
- Documentation out of sync with code
- Lack of documentation tools

**Concrete Fix:**
1. Document all API endpoints
2. Document request/response schemas
3. Document error codes
4. Provide examples
5. Set up API documentation tool (Swagger, OpenAPI)
6. Generate docs from code
7. Keep docs in sync with code

**Required Evidence:**
- API documentation exists and is current
- Documentation matches implementation
- Examples provided
- Documentation review completed

**Prevention:**
- Include documentation in definition of done
- Generate docs from code
- Review documentation in code review
- Regular documentation audits

---

### DOC-002: No Runbooks for Critical Operations

**Severity:** P1

**Violated Rule:** Documentation P0 - Runbooks

**Production Risk:**
- Operators don't know how to handle failures
- Extended outage duration
- Inconsistent response to incidents
- Knowledge loss when team members leave
- Human error during critical operations

**Root Cause:**
- Runbooks not created
- Operational procedures not documented
- No time to document
- Runbooks not kept up to date

**Concrete Fix:**
1. Identify critical operations needing runbooks
2. Create step-by-step runbooks
3. Test runbooks with team
4. Make runbooks easily accessible
5. Keep runbooks up to date
6. Review runbooks regularly

**Required Evidence:**
- Runbooks exist for critical operations
- Runbooks are step-by-step and actionable
- Runbooks are tested
- Runbooks are accessible

**Prevention:**
- Require runbooks before production deployment
- Review runbooks in code review
- Regular runbook updates
- Runbook testing in game days

---

### DOC-003: Architecture Not Documented

**Severity:** P2

**Violated Rule:** Documentation P0 - Architecture Documentation

**Production Risk:**
- New team members struggle to understand system
- Difficult to make architectural decisions
- Architectural knowledge silos
- Technical debt accumulation
- Poor system design over time

**Root Cause:**
- Architecture not documented
- Architecture evolves without documentation
- Documentation not prioritized
- Lack of architecture review process

**Concrete Fix:**
1. Create architecture diagram
2. Document data flows
3. Document component interactions
4. Create ADRs for major decisions
5. Keep documentation up to date
6. Review architecture regularly

**Required Evidence:**
- Architecture diagram exists and is current
- Data flow diagram exists
- ADRs exist for major decisions
- Architecture review completed

**Prevention:**
- Require ADRs for architectural decisions
- Regular architecture reviews
- Keep documentation in version control
- Architecture documentation in onboarding

---

## Domain 9: Performance (Efficiency and Scalability)

### PERF-001: No Performance Baselines

**Severity:** P1

**Violated Rule:** Performance P1 - Performance Baselines

**Production Risk:**
- Performance regressions not detected
- No capacity for performance improvements
- Poor user experience
- Difficulty scaling
- Unexpected costs

**Root Cause:**
- Performance not measured
- No performance testing
- Performance not considered in design
- Lack of performance monitoring

**Concrete Fix:**
1. Define performance requirements (latency, throughput)
2. Run performance benchmarks
3. Document performance baselines
4. Set up performance monitoring
5. Create performance regression tests
6. Monitor performance trends

**Required Evidence:**
- Performance benchmarks documented
- Baseline metrics recorded
- Performance monitoring configured
- Performance regression tests exist

**Prevention:**
- Include performance testing in CI/CD
- Set performance budgets
- Regular performance reviews
- Performance monitoring in production

---

### PERF-002: System Does Not Scale

**Severity:** P1

**Violated Rule:** Performance P0 - Scalability

**Production Risk:**
- System unable to handle growth
- Performance degradation under load
- Service outages during traffic spikes
- Lost business opportunities
- Poor user experience at scale

**Root Cause:**
- Scalability not considered in design
- No load testing
- Single points of failure
- No scaling strategy

**Concrete Fix:**
1. Identify scalability bottlenecks
2. Implement horizontal scaling
3. Implement caching
4. Optimize database queries
5. Implement load balancing
6. Run load testing at expected scale
7. Document scaling procedures

**Required Evidence:**
- Load testing results showing system scales
- Scaling procedures documented
- Caching strategy implemented
- Performance monitoring shows scalability

**Prevention:**
- Include scalability in design reviews
- Regular load testing
- Capacity planning
- Scalability monitoring

---

### PERF-003: No Caching Strategy

**Severity:** P2

**Violated Rule:** Performance P1 - Caching Strategy

**Production Risk:**
- Unnecessary load on backend systems
- Poor performance for repetitive queries
- High costs from API calls
- Slow user experience

**Root Cause:**
- Caching not considered
- No caching requirements identified
- Cache invalidation complexity
- Lack of caching expertise

**Concrete Fix:**
1. Identify cacheable data and operations
2. Define caching strategy (what, when, how long)
3. Implement caching layer
4. Handle cache invalidation
5. Monitor cache hit rates
6. Test cache behavior

**Required Evidence:**
- Caching strategy documented
- Cache implementation reviewed
- Cache hit rate metrics collected
- Cache invalidation tested

**Prevention:**
- Include caching in design reviews
- Monitor cache metrics
- Regular cache optimization reviews

---

## Domain 10: Compliance (Regulatory and Legal)

### COMP-001: No Regulatory Requirement Identification

**Severity:** P0 (for regulated systems)

**Violated Rule:** Compliance P0 - Regulatory Requirement Identification

**Production Risk:**
- Non-compliance with regulations
- Legal penalties and fines
- Loss of certifications
- Business shutdown
- Reputation damage

**Root Cause:**
- Regulations not researched
- No compliance team involvement
- Lack of regulatory awareness
- Assumption that regulations don't apply

**Concrete Fix:**
1. Identify applicable regulations (GDPR, HIPAA, PCI, etc.)
2. Document regulatory requirements
3. Map requirements to system controls
4. Identify compliance gaps
5. Create compliance roadmap
6. Implement missing controls
7. Regular compliance reviews

**Required Evidence:**
- Regulatory requirement mapping exists
- Compliance assessment completed
- Gap analysis documented
- Compliance roadmap created

**Prevention:**
- Involve compliance team early
- Regular compliance reviews
- Compliance training
- Stay updated on regulatory changes

---

### COMP-002: Incomplete Audit Trail

**Severity:** P0 (for regulated systems)

**Violated Rule:** Compliance P0 - Audit Trail

**Production Risk:**
- Cannot demonstrate compliance
- Regulatory penalties
- Difficulty investigating incidents
- Security breaches undetected
- Legal liability

**Root Cause:**
- Audit logging not implemented
- Audit logs incomplete
- Audit logs not retained
- Audit logs not protected

**Concrete Fix:**
1. Identify events to log (authentication, authorization, data access, changes)
2. Implement comprehensive audit logging
3. Ensure logs are tamper-resistant
4. Define log retention period
5. Implement log protection
6. Test log completeness
7. Review logs regularly

**Required Evidence:**
- Audit log samples reviewed
- Log retention policy documented
- Log integrity verified
- Audit trail covers required events

**Prevention:**
- Include audit logging in design reviews
- Regular audit log reviews
- Log retention automation
- Security training on audit logging

---

### COMP-003: No Privacy Impact Assessment

**Severity:** P0 (for systems handling PII/PHI)

**Violated Rule:** Compliance P0 - Privacy Protection

**Production Risk:**
- Privacy violations
- Regulatory penalties (GDPR fines up to 4% of revenue)
- Loss of user trust
- Legal liability
- Reputation damage

**Root Cause:**
- Privacy not considered in design
- No privacy impact assessment process
- Lack of privacy expertise
- No data classification

**Concrete Fix:**
1. Identify all personal data collected and processed
2. Conduct privacy impact assessment
3. Document data flows
4. Implement privacy controls
5. Obtain user consent where required
6. Implement data subject rights (access, deletion, etc.)
7. Document privacy policies

**Required Evidence:**
- Privacy impact assessment document exists
- PII/PHI inventory exists
- Consent mechanisms implemented
- Data subject rights processes documented

**Prevention:**
- Require privacy impact assessment for new systems
- Include privacy in design reviews
- Regular privacy audits
- Privacy training

---

## Appendix: Finding Severity Decision Matrix

Use this matrix to determine finding severity:

| Impact | Likelihood | Detectability | Severity |
|--------|-----------|---------------|----------|
| High | High | Low | P0 |
| High | High | Medium | P0 |
| High | Medium | Low | P0 |
| High | Medium | Medium | P1 |
| High | Low | Any | P1 |
| Medium | High | Low | P0 |
| Medium | High | Medium | P1 |
| Medium | Medium | Low | P1 |
| Medium | Medium | Medium | P2 |
| Medium | Low | Any | P2 |
| Low | High | Low | P1 |
| Low | High | Medium | P2 |
| Low | Medium | Low | P2 |
| Low | Low | Any | P3 |

**Impact Levels:**
- **High**: Data breach, system outage, significant financial loss, user harm
- **Medium**: Degraded performance, limited data exposure, moderate financial impact
- **Low**: Minor inconvenience, cosmetic issues, minimal financial impact

**Likelihood Levels:**
- **High**: Likely to occur in normal operation
- **Medium**: Possible under certain conditions
- **Low**: Unlikely or requires specific conditions

**Detectability Levels:**
- **Low**: Hard to detect, no monitoring
- **Medium**: Detectable with some effort
- **High**: Easy to detect, well-monitored

## Appendix: Finding ID Naming Convention

Use this convention for consistent finding IDs:

**Format:** `{DOMAIN}-{SEQUENCE}`

**Domain Codes:**
- CORE: Core domain
- SEC: Security domain
- DATA: Data domain
- INT: Integration domain
- DEV: Development domain
- TEST: Testing domain
- OPS: Operations domain
- DOC: Documentation domain
- PERF: Performance domain
- COMP: Compliance domain

**Sequence:**
- Three-digit sequential number (001, 002, 003, etc.)
- Reset sequence per domain

**Examples:**
- SEC-001: First security finding
- CORE-042: 42nd core finding
- OPS-015: 15th operations finding

**Severity Suffix** (optional):
- P0 suffix for critical findings
- P1 suffix for high findings

**Examples:**
- SEC-001-P0: Critical security finding
- OPS-015-P1: High operations finding

## Appendix: Finding Tags

Use tags to categorize findings:

**By Type:**
- `security`: Security-related finding
- `reliability`: Reliability-related finding
- `performance`: Performance-related finding
- `maintainability`: Maintainability-related finding
- `compliance`: Compliance-related finding
- `usability`: Usability-related finding

**By Component:**
- `authentication`: Authentication-related
- `authorization`: Authorization-related
- `api`: API-related
- `database`: Database-related
- `frontend`: Frontend-related
- `backend`: Backend-related
- `infrastructure`: Infrastructure-related

**By Trigger:**
- `manual`: Found during manual review
- `automated`: Found by automated tool
- `incident`: Found during incident response
- `complaint`: Found from user complaint

**Example:**
```
Finding ID: SEC-001-P0
Tags: security, authentication, api, automated
```
