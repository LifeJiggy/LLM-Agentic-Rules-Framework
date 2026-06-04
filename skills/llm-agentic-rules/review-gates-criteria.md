# Review Gates Criteria

Use this guide to understand and apply the P0/P1/P2/P3 review gates for LLM, agentic, and AI systems.

## Review Gates Overview

Review gates are quality checkpoints that must be satisfied before a system can progress to the next stage (development → testing → staging → production). The gates are organized by severity:

- **P0 (Critical)**: Blocks production. Must be resolved before deployment.
- **P1 (High)**: Requires explicit acceptance. Must be addressed or formally accepted with documented rationale.
- **P2 (Medium)**: Should be addressed. Tracked in backlog.
- **P3 (Low)**: Nice to have. Addressed when convenient.

### Gate Philosophy

**P0 - Non-Negotiable**
- These are the minimum requirements for a safe, secure, functional system.
- P0 failures indicate fundamental flaws that could cause harm.
- No exceptions without CTO/VP Engineering approval.
- Must be resolved before any production deployment.

**P1 - Requires Accountability**
- These are important quality and reliability requirements.
- P1 failures don't block production but indicate elevated risk.
- Require explicit acceptance with documented rationale.
- Must have a mitigation plan and timeline.

**P2 - Quality Standards**
- These are best practices that improve maintainability and reliability.
- P2 failures don't block production but should be tracked.
- Address in next sprint/iteration.
- No formal acceptance required.

**P3 - Continuous Improvement**
- These are enhancements and polish items.
- P3 failures have minimal impact.
- Address when convenient.
- No tracking required unless desired.

## P0 Review Gates (Critical - Blocks Production)

### P0.1: No Unhandled Exceptions in Critical Paths

**Criteria:**
- All code paths in user-facing workflows have exception handling.
- No bare `except:` clauses that swallow exceptions.
- All exceptions are logged with sufficient context.
- Critical operations have try-catch or equivalent error handling.
- Exceptions are not silently ignored.

**Verification:**
- Code review confirms exception handling in all critical paths.
- Static analysis tools configured to flag unhandled exceptions.
- Test coverage includes error paths.
- Production monitoring shows no unhandled exceptions in critical flows.

**Common Violations:**
- Missing try-catch around external API calls
- Bare except clauses
- Exceptions logged but not handled
- Error paths not tested

### P0.2: All External Inputs Validated

**Criteria:**
- All user inputs are validated before processing.
- All API inputs are validated against schemas.
- All file inputs are validated for format, size, and content.
- All database inputs are parameterized (no SQL injection).
- All external API inputs are sanitized.

**Verification:**
- Input validation code present at all boundaries.
- Schema validation for structured inputs (JSON, YAML, etc.).
- Negative test cases for invalid inputs.
- Fuzz testing for input validation robustness.

**Common Violations:**
- Direct use of user input in database queries
- Missing validation for API parameters
- No file type or size validation
- Trusting external data without verification

### P0.3: Authentication and Authorization Enforced

**Criteria:**
- All protected endpoints require authentication.
- Authorization checks are performed for each request.
- Authentication tokens are validated and not trusted blindly.
- Authorization logic is consistent and not bypassable.
- Privilege escalation is prevented.

**Verification:**
- Authentication middleware or decorators present.
- Authorization logic reviewed for bypasses.
- Test cases for authenticated and unauthenticated access.
- Test cases for different permission levels.
- Security scan shows no authentication bypass vulnerabilities.

**Common Violations:**
- Missing authentication on API endpoints
- Authorization checks only on frontend (not backend)
- Trusting client-provided user IDs
- Hardcoded admin credentials

### P0.4: Sensitive Data Protected

**Criteria:**
- Passwords, API keys, tokens are never logged.
- PII/PHI is encrypted at rest and in transit.
- Sensitive data is not exposed in error messages.
- Sensitive data is not exposed in API responses.
- Data masking is applied where appropriate.

**Verification:**
- Log review confirms no sensitive data in logs.
- Encryption is implemented for data at rest.
- TLS is enforced for data in transit.
- Error messages are sanitized.
- Data classification is documented.

**Common Violations:**
- Logging API keys or passwords
- Returning full user objects with sensitive fields
- Sending passwords in email
- Storing credit card numbers unencrypted

### P0.5: Rollback Capability Exists and is Tested

**Criteria:**
- Rollback procedure is documented.
- Rollback has been tested in staging.
- Rollback can be executed within defined RTO.
- Previous version is available for rollback.
- Rollback does not cause data loss.

**Verification:**
- Rollback runbook exists and is current.
- Rollback was tested in last deployment.
- Rollback time meets RTO requirements.
- Rollback does not require manual file edits.
- Database rollback procedures documented.

**Common Violations:**
- No rollback procedure documented
- Rollback never tested
- Rollback requires manual steps that are error-prone
- Rollback causes data loss
- No previous version available for rollback

### P0.6: Monitoring and Alerting Configured

**Criteria:**
- Critical metrics are monitored (error rate, latency, availability).
- Alerts are configured for critical failures.
- Alert thresholds are appropriate.
- Alerts route to on-call personnel.
- Monitoring covers all critical user workflows.

**Verification:**
- Monitoring dashboards exist and are populated.
- Alert rules are configured and tested.
- On-call rotation is established.
- Alert routing is correct.
- Monitoring coverage is documented.

**Common Violations:**
- No monitoring for critical workflows
- Alerts configured but never tested
- Alert thresholds too aggressive or too lenient
- Alerts routed to wrong people
- No monitoring for external dependencies

### P0.7: Error Handling Includes Timeout, Retry, and Fallback

**Criteria:**
- All external calls have timeouts configured.
- Retry logic is implemented for transient failures.
- Fallback behavior is defined for critical operations.
- Circuit breakers prevent cascading failures.
- Error handling is tested.

**Verification:**
- Timeout values are documented and justified.
- Retry logic is bounded (max retries, max time).
- Fallback paths are tested.
- Circuit breakers are configured with appropriate thresholds.
- Error handling tests cover timeout, retry exhaustion, and fallback activation.

**Common Violations:**
- No timeout on external API calls
- Infinite retry loops
- No fallback for critical external dependencies
- Circuit breakers not implemented
- Error handling not tested

### P0.8: No Hardcoded Secrets or Credentials

**Criteria:**
- No API keys, passwords, or tokens in code.
- No credentials in configuration files in version control.
- Secrets are managed via secret management system.
- Environment variables are used for configuration.
- Credentials are rotated regularly.

**Verification:**
- Secret scanning tools run on codebase.
- No secrets in git history.
- Secret management system is configured.
- Environment variable documentation exists.
- Credential rotation policy exists.

**Common Violations:**
- API keys hardcoded in source code
- Passwords in configuration files
- AWS keys in git repository
- Database credentials in code
- No secret management system

### P0.9: Dependencies Scanned for Vulnerabilities

**Criteria:**
- Dependency vulnerability scanning is automated.
- Critical vulnerabilities are resolved before deployment.
- Dependency updates are reviewed.
- License compliance is verified.
- Transitive dependencies are scanned.

**Verification:**
- Vulnerability scan reports show no critical/high vulnerabilities.
- Dependency scanning is part of CI/CD pipeline.
- Dependency update policy exists.
- License compatibility is verified.
- Software composition analysis (SCA) tool is used.

**Common Violations:**
- No vulnerability scanning
- Critical vulnerabilities ignored
- Outdated dependencies with known exploits
- License violations (GPL in proprietary software)
- Transitive dependencies not scanned

### P0.10: Data Validation at All Boundaries

**Criteria:**
- Input data is validated at system boundaries.
- Output data is validated before sending.
- Data transformations are validated.
- Data integrity checks are implemented.
- Corrupt data is rejected or handled gracefully.

**Verification:**
- Validation logic exists at all input/output boundaries.
- Validation rules are documented.
- Test cases include invalid data scenarios.
- Data quality metrics are monitored.
- Data validation errors are logged.

**Common Violations:**
- Trusting external data without validation
- No validation on database writes
- Missing data type checks
- No handling for corrupt or malformed data
- Data transformations not validated

## P1 Review Gates (High - Requires Explicit Acceptance)

### P1.1: Retry Logic with Bounded Retries

**Criteria:**
- Retry logic is implemented for transient failures.
- Maximum retry count is defined and enforced.
- Total retry time is bounded.
- Retry is disabled for non-retryable errors.
- Retry does not cause side effects (idempotency).

**Acceptance Criteria:**
- If not implemented: Document rationale, define timeline for implementation, implement monitoring for retry-related failures.
- If implemented: Verify bounds are reasonable, verify idempotency, verify non-retryable errors are excluded.

**Verification:**
- Code review confirms retry bounds.
- Tests verify retry behavior and bounds.
- Monitoring tracks retry rates.
- Retry configuration is documented.

**Common Violations:**
- Infinite retry loops
- No maximum retry count
- Retrying non-retryable errors
- Retry causing duplicate side effects

### P1.2: Circuit Breakers for External Dependencies

**Criteria:**
- Circuit breakers are implemented for external service calls.
- Circuit breaker thresholds are defined.
- Circuit breaker state is monitored.
- Fallback behavior is defined when circuit is open.
- Circuit breaker recovery is automatic.

**Acceptance Criteria:**
- If not implemented: Document rationale, assess risk of cascading failures, define timeline.
- If implemented: Verify thresholds are appropriate, verify fallback works, verify monitoring.

**Verification:**
- Circuit breaker implementation reviewed.
- Tests simulate sustained failures.
- Monitoring shows circuit breaker state changes.
- Fallback behavior is tested.

**Common Violations:**
- No circuit breakers for external calls
- Circuit breaker thresholds too high or too low
- No fallback when circuit is open
- Circuit breaker state not monitored

### P1.3: Timeout Configuration for All External Calls

**Criteria:**
- All external API calls have timeouts.
- All database queries have timeouts.
- All file operations have timeouts.
- Timeout values are appropriate for the operation.
- Timeouts are documented.

**Acceptance Criteria:**
- If not implemented: Document rationale, assess risk of hanging operations, define timeline.
- If implemented: Verify timeouts are reasonable, verify timeout handling, verify no overly aggressive timeouts.

**Verification:**
- Code review confirms timeouts on all external calls.
- Timeout values are documented and justified.
- Timeout handling is tested.
- Monitoring tracks timeout occurrences.

**Common Violations:**
- No timeout on external API calls
- Timeout values too aggressive (causing false failures)
- Timeout values too lenient (allowing hanging operations)
- Timeout not handled (crashes on timeout)

### P1.4: Comprehensive Test Coverage

**Criteria:**
- Critical paths have > 80% test coverage.
- Error paths are tested.
- Edge cases are tested.
- Integration tests cover main workflows.
- Tests are automated and run in CI/CD.

**Acceptance Criteria:**
- If coverage < 80%: Document gaps, assess risk, define timeline to improve.
- If coverage >= 80%: Verify test quality, verify edge cases covered, verify tests are maintained.

**Verification:**
- Coverage reports generated and reviewed.
- Test suite runs in CI/CD.
- Tests are not flaky.
- Test quality is reviewed (not just quantity).

**Common Violations:**
- No automated tests
- Tests only cover happy path
- Flaky tests that are ignored
- No integration tests
- Tests not run in CI/CD

### P1.5: Runbooks for Common Failure Scenarios

**Criteria:**
- Runbooks exist for common failure modes.
- Runbooks include step-by-step recovery procedures.
- Runbooks are tested and current.
- Runbooks are accessible to on-call personnel.
- Runbooks include escalation paths.

**Acceptance Criteria:**
- If not created: Document rationale, identify critical failure scenarios, define timeline.
- If created: Verify completeness, verify accuracy, verify accessibility.

**Verification:**
- Runbook documentation exists.
- Runbooks are reviewed by operations team.
- Runbooks are tested in game days.
- Runbooks are kept up to date.

**Common Violations:**
- No runbooks
- Runbooks are outdated or inaccurate
- Runbooks not tested
- Runbooks not accessible
- Runbooks don't include escalation paths

### P1.6: Performance Baselines Established

**Criteria:**
- Performance benchmarks are documented.
- Baseline metrics are collected in production-like environment.
- Performance regression tests exist.
- Performance is monitored in production.
- Performance targets are defined.

**Acceptance Criteria:**
- If not established: Document rationale, define timeline to establish baselines.
- If established: Verify baselines are realistic, verify monitoring, verify regression tests.

**Verification:**
- Performance benchmark results exist.
- Baseline metrics are documented.
- Performance monitoring is configured.
- Regression tests catch performance degradation.

**Common Violations:**
- No performance benchmarks
- Baselines not measured in production-like environment
- No performance monitoring
- No performance regression tests
- Performance targets not defined

### P1.7: Structured Logging Implemented

**Criteria:**
- Logs use structured format (JSON).
- Essential fields are included (timestamp, level, service, operation, request_id).
- Sensitive data is not logged.
- Log levels are used appropriately.
- Logs are aggregated and searchable.

**Acceptance Criteria:**
- If not implemented: Document rationale, assess debugging impact, define timeline.
- If implemented: Verify structured format, verify essential fields, verify no sensitive data.

**Verification:**
- Log samples reviewed for structure and content.
- Log aggregation is configured.
- Log search and querying is available.
- No sensitive data in logs (verified via log scanning).

**Common Violations:**
- Unstructured logs (plain text)
- Missing essential fields
- Sensitive data in logs
- Inappropriate log levels
- Logs not aggregated

### P1.8: Health Checks Implemented

**Criteria:**
- Liveness probes implemented.
- Readiness probes implemented.
- Health checks verify critical dependencies.
- Health check endpoints are secured.
- Health checks are monitored.

**Acceptance Criteria:**
- If not implemented: Document rationale, assess operational impact, define timeline.
- If implemented: Verify coverage, verify accuracy, verify monitoring.

**Verification:**
- Health check endpoints exist and respond.
- Health checks verify critical dependencies.
- Health check failures trigger alerts.
- Health checks are included in monitoring.

**Common Violations:**
- No health checks
- Health checks only verify process is running (not functionality)
- Health checks not monitored
- Health check endpoints not secured

### P1.9: Graceful Degradation Defined

**Criteria:**
- System behavior is defined for degraded states.
- Non-essential features can be disabled.
- System remains functional with reduced functionality.
- Degradation is automatic or easily triggered.
- Degradation state is monitored.

**Acceptance Criteria:**
- If not defined: Document rationale, assess user impact, define timeline.
- If defined: Verify degradation paths, verify testing, verify monitoring.

**Verification:**
- Degradation scenarios documented.
- Degradation is tested.
- Monitoring detects degradation.
- Recovery from degradation is automated or documented.

**Common Violations:**
- No graceful degradation (system crashes on dependency failure)
- Degradation not tested
- Degradation not monitored
- No recovery from degraded state

### P1.10: Documentation Complete for User-Facing Features

**Criteria:**
- User-facing features are documented.
- API documentation is current.
- Error messages are clear and actionable.
- Configuration options are documented.
- Known limitations are documented.

**Acceptance Criteria:**
- If incomplete: Document gaps, assess user impact, define timeline.
- If complete: Verify accuracy, verify accessibility, verify completeness.

**Verification:**
- Documentation review completed.
- Documentation is accessible to users.
- Documentation is kept up to date.
- User feedback on documentation is positive.

**Common Violations:**
- No documentation
- Documentation is outdated
- Documentation is incomplete
- Documentation is not accessible
- Error messages are cryptic

## P2 Review Gates (Medium - Should Address)

### P2.1: Code Quality and Style

**Criteria:**
- Code follows established style guidelines.
- Code is well-organized and modular.
- Functions and classes have single responsibilities.
- Code duplication is minimized.
- Code is readable and maintainable.

**Verification:**
- Linting tools pass.
- Code review confirms quality.
- Code complexity metrics are acceptable.
- No significant code duplication.

### P2.2: Non-Critical Test Coverage

**Criteria:**
- Non-critical paths have reasonable test coverage.
- Edge cases for non-critical paths are tested.
- Negative test cases exist.
- Test maintenance is sustainable.

**Verification:**
- Coverage reports reviewed.
- Test quality assessed.
- Test maintenance burden is acceptable.

### P2.3: Internal Tool Documentation

**Criteria:**
- Internal tools have documentation.
- Internal APIs are documented.
- Configuration options are documented.
- Troubleshooting guides exist.

**Verification:**
- Documentation review completed.
- Internal users can find and use documentation.

### P2.4: Minor Performance Optimizations

**Criteria:**
- Obvious performance issues are addressed.
- Performance opportunities are documented.
- Performance monitoring is in place.

**Verification:**
- Performance profiling completed.
- No obvious bottlenecks.
- Performance is acceptable for current scale.

### P2.5: Refactoring Opportunities

**Criteria:**
- Technical debt is documented.
- Refactoring opportunities are identified.
- Refactoring does not change behavior.
- Refactoring is tested.

**Verification:**
- Technical debt inventory maintained.
- Refactoring is planned and tracked.

## P3 Review Gates (Low - Nice to Have)

### P3.1: UI Polish

**Criteria:**
- UI is visually appealing.
- UI is consistent with design system.
- UI is responsive.

**Verification:**
- UI review completed.
- Design review passed.

### P3.2: Enhanced Logging Verbosity

**Criteria:**
- Additional debug logging where useful.
- Log verbosity is configurable.

**Verification:**
- Debug logging is available but not enabled by default in production.

### P3.3: Additional Reporting Features

**Criteria:**
- Enhanced reporting capabilities.
- Additional metrics and dashboards.

**Verification:**
- Reporting features meet user needs.

### P3.4: Code Comment Improvements

**Criteria:**
- Complex logic has explanatory comments.
- Public APIs have comprehensive docstrings.

**Verification:**
- Code review confirms documentation quality.

## Gate Enforcement by Risk Tier

### Tier 1 (Critical)

**Enforcement:**
- All P0 gates must pass.
- All P1 gates must pass or be formally accepted.
- P2 gates should be addressed before release.
- P3 gates addressed as time permits.
- No exceptions without CTO/VP Engineering approval.

**Review Process:**
- Mandatory security review.
- Mandatory code review by senior engineer.
- Mandatory testing by QA team.
- Mandatory sign-off from all stakeholders.

### Tier 2 (High)

**Enforcement:**
- All P0 gates must pass.
- P1 gates must pass or be formally accepted by tech lead.
- P2 gates should be addressed.
- P3 gates addressed as time permits.
- Exceptions require tech lead and architect approval.

**Review Process:**
- Security review for security-related changes.
- Code review by senior engineer.
- Testing by development team.
- Sign-off from tech lead.

### Tier 3 (Medium)

**Enforcement:**
- All P0 gates must pass.
- P1 gates should be addressed.
- P2 gates addressed as time permits.
- P3 gates optional.
- Exceptions require team lead approval.

**Review Process:**
- Code review by peer.
- Testing by development team.
- Sign-off from team lead.

### Tier 4 (Low)

**Enforcement:**
- Critical P0 gates must pass (security, data protection).
- Other P0 gates strongly recommended.
- P1 gates recommended.
- P2/P3 gates optional.
- Exceptions require developer and reviewer approval.

**Review Process:**
- Code review by peer (if available).
- Testing by developer.
- Self-sign-off acceptable.

## Gate Bypass Process

### When Bypass is Necessary

Bypassing a gate may be necessary in emergency situations. The bypass process ensures that risks are acknowledged and mitigated.

### Bypass Approval Matrix

| Gate | Tier 1 Approval | Tier 2 Approval | Tier 3 Approval | Tier 4 Approval |
|------|----------------|----------------|----------------|----------------|
| P0   | CTO/VP Eng + CISO | Tech Lead + Architect | Team Lead | Developer + Reviewer |
| P1   | Tech Lead + Architect | Tech Lead | Team Lead | Developer |
| P2   | Not allowed | Not allowed | Team Lead | Developer |
| P3   | Not allowed | Not allowed | Not allowed | Developer |

### Bypass Documentation Requirements

**For P0 Bypass:**
- Detailed description of the emergency.
- Risk assessment of bypassing the gate.
- Mitigation plan to address the gate later.
- Compensating controls to reduce risk.
- Timeline for gate implementation.
- Approval from required stakeholders.
- Post-bypass review scheduled.

**For P1 Bypass:**
- Description of why gate cannot be met.
- Risk assessment.
- Mitigation plan.
- Timeline for gate implementation.
- Approval from required stakeholders.

**For P2/P3 Bypass:**
- Brief description of why not addressed.
- Timeline for future addressal (optional).

### Bypass Template

```
GATE BYPASS REQUEST
===================
Requested By: [Name/Role]
Date: YYYY-MM-DD
System: [System name and version]
Change: [Description of change]

Gate Bypassed: [P0/P1/P2/P3] - [Gate description]

Reason for Bypass
-----------------
[Detailed explanation of why gate cannot be met]

Risk Assessment
---------------
[Description of risks introduced by bypass]

Mitigation Plan
---------------
[How risks will be mitigated]

Compensating Controls
---------------------
[Additional controls to reduce risk]

Timeline for Gate Implementation
--------------------------------
[When gate will be fully satisfied]

Approvals
---------
- [ ] Tech Lead: [Name, Date]
- [ ] Architect: [Name, Date]
- [ ] Security: [Name, Date]
- [ ] CTO/VP Eng: [Name, Date] (required for Tier 1 P0)

Post-Bypass Review
------------------
Scheduled: [Date]
Reviewer: [Name]
```

## Gate Metrics and Reporting

### Metrics to Track

**Gate Compliance Metrics**
- P0 gate pass rate (target: 100%)
- P1 gate pass rate (target: > 90%)
- P2 gate pass rate (target: > 70%)
- P3 gate pass rate (target: > 50%)
- Gate bypass rate (target: < 5%)
- Time to resolve P0/P1 findings
- Evidence completeness rate

**Quality Metrics**
- Production incident rate
- Security incident rate
- Bug escape rate to production
- Mean time to detect (MTTD)
- Mean time to resolve (MTTR)
- Customer satisfaction scores

**Process Metrics**
- Average review cycle time
- Gate review meeting frequency
- Evidence collection completeness
- Documentation update rate

### Reporting

**Weekly Report**
- Gates passed/failed this week
- P0/P1 findings and resolution status
- Evidence completeness
- Upcoming releases and gate status

**Monthly Report**
- Gate compliance trends
- Quality metrics trends
- Process improvement opportunities
- Training needs

**Quarterly Report**
- Comprehensive gate compliance review
- Framework effectiveness assessment
- Process improvements implemented
- Goals for next quarter

## Gate Training

### Training Requirements

**All Team Members**
- Framework overview
- Gate definitions and criteria
- Evidence collection standards
- Routing process

**Tech Leads**
- Gate enforcement
- Bypass approval process
- Risk tier assessment
- Escalation procedures

**Security Team**
- Security gate criteria
- Threat modeling
- Vulnerability assessment
- Security review process

**Operations Team**
- Operational gate criteria
- Runbook development
- Incident response
- Monitoring and alerting

### Training Materials

- Framework presentation
- Gate criteria cheat sheet
- Evidence collection guide
- Routing decision tree
- Bypass process guide
- Case studies and examples
- Video tutorials
- Hands-on exercises

## Gate Continuous Improvement

### Feedback Collection

- Collect feedback on gate criteria clarity.
- Collect feedback on gate enforcement consistency.
- Collect feedback on evidence burden.
- Collect feedback on process efficiency.

### Improvement Process

1. Review feedback quarterly.
2. Identify patterns and common issues.
3. Propose gate criteria updates.
4. Update documentation and training.
5. Communicate changes to team.
6. Monitor impact of changes.

### Gate Criteria Updates

- Update criteria based on lessons learned.
- Update criteria based on new threats or technologies.
- Update criteria based on regulatory changes.
- Update criteria based on team feedback.

## Appendix: Gate Checklist Templates

### Pre-Release Gate Checklist

```
PRE-RELEASE GATE CHECKLIST
===========================
Release: [Version/Name]
Date: YYYY-MM-DD
Reviewer: [Name]

P0 Gates (All Must Pass)
-------------------------
[ ] No unhandled exceptions in critical paths
[ ] All external inputs validated
[ ] Authentication and authorization enforced
[ ] Sensitive data protected
[ ] Rollback capability exists and is tested
[ ] Monitoring and alerting configured
[ ] Error handling includes timeout, retry, fallback
[ ] No hardcoded secrets or credentials
[ ] Dependencies scanned for vulnerabilities
[ ] Data validation at all boundaries

P1 Gates (All Must Pass or Be Accepted)
----------------------------------------
[ ] Retry logic with bounded retries
[ ] Circuit breakers for external dependencies
[ ] Timeout configuration for all external calls
[ ] Comprehensive test coverage (> 80%)
[ ] Runbooks for common failure scenarios
[ ] Performance baselines established
[ ] Structured logging implemented
[ ] Health checks implemented
[ ] Graceful degradation defined
[ ] Documentation complete for user-facing features

P2 Gates (Should Pass)
-----------------------
[ ] Code quality and style
[ ] Non-critical test coverage
[ ] Internal tool documentation
[ ] Minor performance optimizations
[ ] Refactoring opportunities addressed

P3 Gates (Nice to Have)
-----------------------
[ ] UI polish
[ ] Enhanced logging verbosity
[ ] Additional reporting features
[ ] Code comment improvements

Evidence Collected
------------------
[ ] Test results: [Link]
[ ] Security scan: [Link]
[ ] Performance benchmarks: [Link]
[ ] Documentation: [Link]
[ ] Monitoring configuration: [Link]

Gate Decision
-------------
[ ] APPROVED - All P0 and P1 gates passed
[ ] CONDITIONAL - P0 passed, P1 accepted with rationale
[ ] BLOCKED - P0 or P1 not satisfied

Sign-off: _______________
Date: _______________
```

### Gate Review Meeting Agenda

```
GATE REVIEW MEETING
===================
Release: [Version/Name]
Date: YYYY-MM-DD
Attendees: [Names]

Agenda
------
1. Review P0 gate status (15 min)
   - Any failures?
   - Any bypass requests?
   - Resolution timeline

2. Review P1 gate status (15 min)
   - Any failures?
   - Acceptance requests?
   - Mitigation plans

3. Review P2/P3 gate status (10 min)
   - Status update
   - deferral decisions

4. Evidence review (10 min)
   - Evidence completeness
   - Evidence quality

5. Release decision (10 min)
   - Go/No-go decision
   - Conditions for release
   - Timeline

Action Items
------------
- [Action 1]: [Owner] - [Due date]
- [Action 2]: [Owner] - [Due date]
```

### Daily Gate Standup Template

```
DAILY GATE STANDUP
==================
Date: YYYY-MM-DD
Release: [Version/Name]

P0 Status
---------
Total: [X]
Passed: [X]
Failed: [X]
Blockers: [List]

P1 Status
---------
Total: [X]
Passed: [X]
Accepted: [X]
Failed: [X]
Blockers: [List]

P2 Status
---------
Total: [X]
Completed: [X]
Remaining: [X]

P3 Status
---------
Total: [X]
Completed: [X]
Remaining: [X]

Evidence Status
---------------
Collected: [X]%
Missing: [List]

Risks and Blockers
------------------
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

Next Steps
----------
- [Next step 1]: [Owner] - [Due date]
- [Next step 2]: [Owner] - [Due date]
```

## Appendix: Gate Failure Recovery

### P0 Failure Recovery

**Immediate Actions:**
1. Stop all related development work.
2. Notify tech lead and security team (if security-related).
3. Assess impact and scope.
4. Develop fix plan.
5. Implement and test fix.
6. Re-run gate review.
7. Document failure and resolution.

**Recovery Time Objective:**
- Tier 1: 4 hours
- Tier 2: 8 hours
- Tier 3: 24 hours
- Tier 4: 48 hours

### P1 Failure Recovery

**Immediate Actions:**
1. Document the failure.
2. Assess risk and impact.
3. Propose mitigation or acceptance.
4. Get approval from tech lead/architect.
5. Implement mitigation or document acceptance.
6. Update evidence.
7. Continue with conditional approval.

**Recovery Time Objective:**
- Tier 1: 24 hours
- Tier 2: 48 hours
- Tier 3: 1 week
- Tier 4: 2 weeks

### P2/P3 Failure Recovery

**Actions:**
1. Document in backlog.
2. Prioritize for future sprint.
3. No blocking action required.
4. Continue with release.
