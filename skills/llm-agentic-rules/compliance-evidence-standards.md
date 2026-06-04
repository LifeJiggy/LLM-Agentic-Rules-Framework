# Compliance and Evidence Standards

Use this guide when collecting, documenting, and maintaining evidence for LLM, agentic, and AI system compliance with the framework.

## Evidence Philosophy

Evidence is the proof that a system meets the framework's requirements. Without evidence, compliance claims are unsubstantiated. Evidence must be collected systematically, stored securely, and maintained throughout the system's lifecycle.

### Evidence Principles

**Authenticity**
- Evidence must come from the actual system, not from assumptions or plans.
- Evidence must be timestamped and attributable.
- Evidence must be reproducible by independent reviewers.

**Completeness**
- Evidence must cover all applicable checklist items.
- Evidence must be sufficient to verify compliance.
- Evidence gaps must be explicitly documented.

**Clarity**
- Evidence must be clearly labeled and organized.
- Evidence must include context for interpretation.
- Evidence must be accessible to reviewers.

**Retention**
- Evidence must be retained for the required period.
- Evidence must be stored in a stable, accessible location.
- Evidence must be protected from tampering or loss.

## Evidence Categories

### Test Evidence

Test evidence demonstrates that the system functions correctly and meets requirements.

**Automated Test Results**
- Test execution reports (pass/fail status)
- Code coverage reports (line, branch, function coverage)
- Test execution time and trends
- Flaky test identification and resolution

**Manual Test Results**
- Manual test execution records
- Tester name and date
- Test environment details
- Pass/fail status with notes
- Screenshots or recordings for UI tests

**Performance Test Results**
- Load test results (requests per second, latency, error rate)
- Stress test results (breaking points, failure modes)
- Soak test results (memory leaks, degradation over time)
- Spike test results (recovery from traffic spikes)

**Security Test Results**
- Vulnerability scan reports
- Penetration test results
- Security audit findings
- Dependency vulnerability reports

**Evaluation Results**
- Model evaluation metrics (accuracy, precision, recall, F1)
- LLM-as-judge evaluation results
- Human evaluation results
- A/B test results
- Red teaming results

**Chaos Test Results**
- Failure injection results
- Recovery time measurements
- System behavior under failure
- Monitoring and alerting validation

### Documentation Evidence

Documentation evidence shows that the system is properly documented and maintainable.

**Code Documentation**
- Code comments and docstrings
- API documentation (OpenAPI, GraphQL schema)
- Architecture diagrams
- Data flow diagrams
- Sequence diagrams for complex workflows

**User Documentation**
- User guides and manuals
- API reference documentation
- Getting started guides
- Tutorials and examples
- FAQ and troubleshooting guides

**Operational Documentation**
- Runbooks for common operations
- Incident response procedures
- Deployment guides
- Configuration guides
- Backup and recovery procedures

**Change Documentation**
- Changelog entries
- Release notes
- Migration guides
- Deprecation notices
- API versioning documentation

### Configuration Evidence

Configuration evidence demonstrates that the system is configured correctly and securely.

**Application Configuration**
- Configuration files (sanitized, no secrets)
- Environment variable documentation
- Feature flag configurations
- Model parameters and settings
- Prompt templates (if applicable)

**Infrastructure Configuration**
- Infrastructure as code (Terraform, CloudFormation, etc.)
- Network configuration
- Security group rules
- Load balancer configuration
- CDN configuration

**Deployment Configuration**
- Deployment manifests (Kubernetes, Docker Compose, etc.)
- CI/CD pipeline configuration
- Environment promotion procedures
- Rollback configuration

**Security Configuration**
- Authentication configuration
- Authorization configuration
- Encryption settings
- Certificate configuration
- Secret management configuration

### Observability Evidence

Observability evidence shows that the system can be monitored and debugged in production.

**Logging Configuration**
- Log format specification
- Log aggregation setup
- Log retention policy
- Log-based alerting rules
- Sample logs demonstrating structure and content

**Metrics Configuration**
- Metrics collection setup
- Metric naming conventions
- Dashboard configurations
- Alert rules and thresholds
- Sample metric queries

**Tracing Configuration**
- Distributed tracing setup
- Trace sampling configuration
- Trace storage and retention
- Trace visualization setup
- Sample traces demonstrating end-to-end visibility

**Monitoring Configuration**
- Health check endpoints
- Monitoring coverage documentation
- On-call rotation
- Escalation procedures
- Monitoring tool configuration

### Compliance Evidence

Compliance evidence demonstrates adherence to regulatory and legal requirements.

**Regulatory Compliance**
- Regulatory requirement mapping
- Compliance checklist completion
- Regulatory audit reports
- Privacy impact assessments
- Data protection impact assessments

**Audit Evidence**
- Audit trail samples
- Access logs
- Change logs
- Configuration change records
- Deployment records

**Data Governance**
- Data classification documentation
- Data flow diagrams
- Data retention policies
- Data deletion procedures
- Data access controls

**Legal Compliance**
- Terms of service
- Privacy policy
- User consent records
- Data processing agreements
- Licensing compliance

## Evidence Collection Process

### During Development

**Continuous Collection**
- Collect evidence as you work, not at the end.
- Take screenshots of important configuration steps.
- Save test output and logs.
- Document decisions and rationale.
- Link evidence to specific checklist items.

**Evidence Artifacts to Collect During Development**
- Test execution logs
- Code review comments and approvals
- Design decision documents
- Configuration snapshots
- Performance benchmark results
- Security scan results

### During Testing

**Test Evidence Collection**
- Automated test reports (JUnit, pytest, etc.)
- Manual test sign-offs
- Performance benchmark results
- Security scan results
- Evaluation results (model outputs, human evaluations)
- Chaos test results

**Evidence Quality Checks**
- Tests are passing (or failures are documented and accepted).
- Test coverage meets requirements.
- Test results are reproducible.
- Test environment is documented.
- Test data is representative.

### During Deployment

**Deployment Evidence Collection**
- Deployment logs
- Health check results
- Smoke test results
- Rollback test results
- Monitoring configuration screenshots
- Alert configuration documentation

**Deployment Validation**
- All pre-deployment checks passed.
- Post-deployment health checks passed.
- Monitoring is active and collecting data.
- Alerts are configured and tested.
- Rollback procedure is documented and tested.

### During Operations

**Operational Evidence Collection**
- Monitoring dashboards (screenshots or exports)
- Incident reports
- Change logs
- Performance metrics over time
- Audit logs

**Ongoing Maintenance**
- Regularly review evidence for completeness.
- Update evidence when system changes.
- Archive evidence according to retention policy.
- Verify evidence is accessible and readable.

## Evidence Storage and Management

### Storage Principles

**Organization**
- Store evidence in a structured, hierarchical manner.
- Use consistent naming conventions.
- Group evidence by domain, checklist item, and date.
- Include README files explaining evidence organization.

**Accessibility**
- Evidence must be accessible to authorized reviewers.
- Evidence must be searchable.
- Evidence must be retrievable within reasonable time.
- Evidence must be readable (format compatibility).

**Security**
- Evidence must be protected from unauthorized modification.
- Evidence must be backed up.
- Evidence must be retained for required periods.
- Sensitive evidence must be encrypted.

**Retention**
- Define retention periods based on regulatory requirements and business needs.
- Automate evidence retention where possible.
- Archive old evidence according to policy.
- Ensure archived evidence remains accessible.

### Storage Locations

**Recommended Storage Structure**
```
evidence/
├── by-release/
│   ├── v1.0.0/
│   │   ├── test-results/
│   │   ├── security-scans/
│   │   ├── performance-benchmarks/
│   │   ├── deployment-logs/
│   │   └── release-checklist.md
│   └── v1.1.0/
├── by-domain/
│   ├── core/
│   ├── security/
│   ├── data/
│   └── ...
├── by-type/
│   ├── test-results/
│   ├── security-scans/
│   ├── performance-benchmarks/
│   └── ...
└── templates/
    ├── test-result-template.md
    ├── security-scan-template.md
    └── ...
```

**Storage Options**
- Version control (Git) for code-related evidence
- Artifact repositories (Artifactory, Nexus) for build artifacts
- Cloud storage (S3, GCS) for large files and backups
- Database for structured evidence (audit logs, metrics)
- Document management systems for compliance documentation

### Evidence Metadata

Every piece of evidence should include metadata:

**Required Metadata**
- **Title**: Descriptive name of the evidence
- **Date**: When the evidence was collected
- **Collector**: Who collected the evidence
- **System**: Which system/version the evidence applies to
- **Checklist Item**: Which framework checklist item this evidence supports
- **Format**: File format and tool used
- **Location**: Where the evidence is stored
- **Retention**: How long to retain the evidence

**Optional Metadata**
- Environment (dev/staging/production)
- Test configuration
- Tool versions
- Related evidence items
- Review status

**Metadata Template**
```yaml
---
title: "API Endpoint Load Test Results"
date: "2026-06-04"
collector: "Jane Smith (QA Engineer)"
system: "LLM-Agent v2.1.0"
checklist_item: "Operations P0 - Performance testing"
format: "k6 HTML report"
location: "evidence/by-release/v2.1.0/performance/api-load-test.html"
retention: "3 years"
environment: "staging"
tool_version: "k6 v0.45.0"
test_configuration: "1000 concurrent users, 10 minutes"
related_evidence:
  - "evidence/by-release/v2.1.0/performance/baseline-metrics.md"
review_status: "approved"
reviewed_by: "John Doe (Tech Lead)"
review_date: "2026-06-05"
---
```

## Evidence Templates

### Test Result Template

```
TEST RESULT REPORT
==================
Test Suite: [Name]
Test Type: [Unit/Integration/Performance/Security/etc.]
Date: YYYY-MM-DD
Tester: [Name/Role]
System: [System name and version]
Environment: [Dev/Staging/Production]

Test Configuration
------------------
- Tool: [Testing tool name and version]
- Configuration: [Relevant configuration details]
- Test data: [Description of test data used]

Results Summary
---------------
Total Tests: [X]
Passed: [X] ([X]%)
Failed: [X] ([X]%)
Skipped: [X] ([X]%)
Flaky: [X] ([X]%)

Coverage
--------
Line Coverage: [X]%
Branch Coverage: [X]%
Function Coverage: [X]%

Failed Tests
------------
1. [Test name]: [Failure description]
   - Error: [Error message]
   - Stack trace: [If applicable]
   - Status: [Fixed/Deferred/Accepted]

Performance Metrics (if applicable)
------------------------------------
- P50 Latency: [X]ms
- P95 Latency: [X]ms
- P99 Latency: [X]ms
- Throughput: [X] requests/second
- Error Rate: [X]%

Observations
------------
[Any notable observations, issues, or anomalies]

Recommendations
---------------
[Recommendations for improvements]

Sign-off: _______________
Date: _______________
```

### Security Scan Template

```
SECURITY SCAN REPORT
====================
Scan Type: [Vulnerability/SAST/DAST/IAST/Dependency]
Scanner: [Tool name and version]
Date: YYYY-MM-DD
Scanned By: [Name/Role]
System: [System name and version]
Environment: [Dev/Staging/Production]

Scan Configuration
------------------
- Targets: [What was scanned]
- Scope: [In-scope and out-of-scope items]
- Scan depth: [Quick/Standard/Deep]
- Credentials used: [Yes/No, type if yes]

Results Summary
---------------
Total Findings: [X]
Critical: [X]
High: [X]
Medium: [X]
Low: [X]
Informational: [X]

Critical Findings
-----------------
1. [Finding title]
   - Severity: Critical
   - Location: [File/URL/Component]
   - Description: [Detailed description]
   - Impact: [Potential impact]
   - Remediation: [How to fix]
   - Status: [Open/Fixed/Accepted/Deferred]
   - Owner: [Name]
   - Due Date: [Date]

High Findings
--------------
[Same format as Critical]

Medium Findings
---------------
[Same format as Critical]

Low/Informational Findings
---------------------------
[List or reference to detailed report]

Compliance Status
-----------------
[ ] All critical findings resolved
[ ] All high findings resolved or accepted
[ ] Medium findings tracked
[ ] Scan meets compliance requirements

Next Steps
----------
- [ ] Fix critical findings by [date]
- [ ] Fix high findings by [date]
- [ ] Track medium findings in backlog
- [ ] Re-scan after fixes

Sign-off: _______________
Date: _______________
```

### Performance Benchmark Template

```
PERFORMANCE BENCHMARK REPORT
=============================
Benchmark Suite: [Name]
Date: YYYY-MM-DD
Benchmarked By: [Name/Role]
System: [System name and version]
Environment: [Staging/Production-like]

Benchmark Configuration
------------------------
- Tool: [Benchmarking tool and version]
- Load profile: [Description of load pattern]
- Duration: [How long the test ran]
- Warm-up period: [Duration before measurements]
- Metrics collected: [List of metrics]

System Configuration
--------------------
- Instance type: [e.g., AWS m5.large]
- Database: [Type and size]
- Cache: [Configuration]
- Network: [Bandwidth, latency]

Results
-------
Throughput: [X] requests/second
P50 Latency: [X]ms
P95 Latency: [X]ms
P99 Latency: [X]ms
Max Latency: [X]ms
Error Rate: [X]%
Concurrent Users: [X]

Resource Utilization
--------------------
CPU: [X]%
Memory: [X]%
Disk I/O: [X]
Network I/O: [X]

Baseline Comparison
-------------------
Baseline Throughput: [X] req/s
Baseline P95 Latency: [X]ms
Change in Throughput: [+/-X]%
Change in P95 Latency: [+/-X]%

Performance Assessment
----------------------
[ ] Meets performance targets
[ ] Exceeds performance targets
[ ] Below performance targets
[ ] Regression detected

Regression Analysis (if applicable)
------------------------------------
- Regression magnitude: [X]%
- Suspected cause: [Analysis]
- Remediation plan: [Steps to fix]

Recommendations
---------------
[Recommendations for performance improvements]

Sign-off: _______________
Date: _______________
```

### Audit Trail Template

```
AUDIT TRAIL ENTRY
=================
Entry ID: [Unique identifier]
Timestamp: YYYY-MM-DD HH:MM:SS TZ
Actor: [User/Service/Agent ID]
Action: [What was done]
Target: [What was acted upon]
Outcome: [Success/Failure/Partial]
Context: [Relevant parameters, state, environment]
Correlation ID: [Request/operation ID for tracing]

Details
-------
[Detailed description of the action]

Before State
------------
[State of the system before the action]

After State
-----------
[State of the system after the action]

Impact
------
[Impact of the action on the system, users, data]

Sign-off: _______________
Date: _______________
```

## Evidence Review Process

### Review Frequency

**Continuous Review**
- Review evidence as it is collected.
- Verify evidence quality and completeness.
- Identify gaps early.

**Pre-Release Review**
- Comprehensive evidence review before production deployment.
- Verify all P0/P1 evidence is collected.
- Verify evidence quality and authenticity.
- Sign off on evidence package.

**Periodic Review**
- Monthly: Review evidence completeness for recent changes.
- Quarterly: Comprehensive evidence audit.
- Annually: Full compliance audit.

### Review Checklist

**Authenticity Review**
- [ ] Evidence comes from actual system (not plans or assumptions).
- [ ] Evidence is timestamped.
- [ ] Evidence source is identifiable.
- [ ] Evidence is reproducible.

**Completeness Review**
- [ ] All P0 items have evidence.
- [ ] All P1 items have evidence or documented acceptance.
- [ ] Evidence is sufficient to verify compliance.
- [ ] Evidence gaps are documented.

**Quality Review**
- [ ] Evidence is clear and understandable.
- [ ] Evidence includes necessary context.
- [ ] Evidence is in a supported format.
- [ ] Evidence is not corrupted or incomplete.

**Retention Review**
- [ ] Evidence is stored in the correct location.
- [ ] Evidence metadata is complete.
- [ ] Evidence retention period is defined.
- [ ] Evidence backup is configured.

## Evidence Maintenance

### Lifecycle

**Creation**
- Evidence is created during development, testing, and deployment.
- Evidence is collected systematically.
- Evidence is linked to checklist items.

**Review**
- Evidence is reviewed for quality and completeness.
- Evidence is verified for authenticity.
- Evidence gaps are identified and addressed.

**Storage**
- Evidence is stored in the designated location.
- Evidence is organized and indexed.
- Evidence metadata is recorded.

**Retention**
- Evidence is retained for the required period.
- Evidence is protected from loss or tampering.
- Evidence is archived according to policy.

**Disposal**
- Evidence is disposed of after retention period.
- Disposal is documented.
- Disposal is secure (especially for sensitive evidence).

### Updates

**When to Update Evidence**
- System changes that affect compliance.
- Test results change (new test runs).
- Configuration changes.
- Incident responses.
- Audit findings.

**How to Update Evidence**
- Version evidence files when updated.
- Link new evidence to old evidence.
- Document what changed and why.
- Retain old evidence for historical context.

## Evidence for Audits

### Audit Preparation

**Pre-Audit Checklist**
- [ ] All evidence is collected and organized.
- [ ] Evidence covers all applicable checklist items.
- [ ] Evidence is current (from recent system state).
- [ ] Evidence is authentic and verifiable.
- [ ] Evidence gaps are documented with rationale.
- [ ] Evidence retention policy is followed.
- [ ] Evidence is accessible to auditors.

**Audit Package**
- Executive summary of compliance status.
- System overview and architecture.
- Evidence index (mapping checklist items to evidence).
- Evidence artifacts (test results, scan reports, etc.).
- Gap analysis and remediation plans.
- Historical compliance trends.

### Audit Evidence Standards

**External Audit Requirements**
- Evidence must be independently verifiable.
- Evidence must be tamper-evident.
- Evidence must be retained for regulatory periods.
- Evidence chain of custody must be maintained.
- Evidence must be available on demand.

**Internal Audit Requirements**
- Evidence must be accessible to internal auditors.
- Evidence must be current and relevant.
- Evidence must be organized for efficient review.
- Evidence gaps must be documented.

## Evidence Automation

### Automated Evidence Collection

**CI/CD Integration**
- Automatically collect test results.
- Automatically collect coverage reports.
- Automatically collect security scan results.
- Automatically collect build artifacts.
- Automatically publish evidence to repository.

**Monitoring Integration**
- Automatically collect metrics.
- Automatically collect logs.
- Automatically collect traces.
- Automatically generate reports.

**Scheduled Collection**
- Daily: Collect operational metrics.
- Weekly: Collect performance benchmarks.
- Monthly: Collect security scan results.
- Quarterly: Collect compliance reports.

### Evidence Validation

**Automated Validation**
- Verify evidence files are not corrupted.
- Verify evidence metadata is complete.
- Verify evidence is in expected format.
- Verify evidence is recent enough.
- Alert on missing evidence.

**Manual Validation**
- Review evidence for completeness.
- Verify evidence authenticity.
- Verify evidence relevance.
- Verify evidence quality.

## Evidence Metrics

### Metrics to Track

**Evidence Completeness**
- Percentage of checklist items with evidence.
- Evidence gaps by domain.
- Evidence gaps by priority (P0/P1/P2/P3).
- Trend of evidence completeness over time.

**Evidence Quality**
- Evidence authenticity issues.
- Evidence format issues.
- Evidence clarity issues.
- Reviewer satisfaction with evidence.

**Evidence Timeliness**
- Time from system change to evidence collection.
- Time from evidence collection to review.
- Time from gap identification to evidence collection.
- Time from audit request to evidence delivery.

### Reporting

**Weekly Evidence Report**
- Evidence collected this week.
- Evidence gaps identified.
- Evidence quality issues.
- Upcoming evidence needs.

**Monthly Evidence Report**
- Evidence completeness by domain.
- Evidence quality trends.
- Evidence retention compliance.
- Evidence process improvements.

**Quarterly Evidence Report**
- Comprehensive evidence audit.
- Compliance status.
- Evidence gaps and remediation.
- Process improvements.
- Training needs.

## Common Evidence Mistakes

### Mistake 1: Collecting Evidence at the End

**Problem**: Waiting until the end of a project to collect evidence leads to incomplete or missing evidence.

**Impact**: Cannot demonstrate compliance, audit failures, release delays.

**Solution**: Collect evidence continuously during development.

### Mistake 2: Evidence Without Context

**Problem**: Evidence files without metadata or context are meaningless.

**Impact**: Reviewers cannot understand or verify evidence.

**Solution**: Always include metadata and context with evidence.

### Mistake 3: Assuming Compliance Without Evidence

**Problem**: Stating that something is compliant without providing evidence.

**Impact**: Unsubstantiated claims, audit failures, trust issues.

**Solution**: Always provide evidence for compliance claims.

### Mistake 4: Not Documenting Evidence Gaps

**Problem**: Ignoring evidence gaps instead of documenting them.

**Impact**: Surprises during audits, last-minute scrambles.

**Solution**: Explicitly document evidence gaps with rationale and remediation plan.

### Mistake 5: Poor Evidence Organization

**Problem**: Evidence scattered across locations, inconsistent naming, no index.

**Impact**: Difficult to find evidence, time-consuming audits.

**Solution**: Use consistent structure and naming conventions. Maintain evidence index.

### Mistake 6: Not Retaining Evidence

**Problem**: Deleting old evidence, not following retention policy.

**Impact**: Cannot demonstrate historical compliance, regulatory violations.

**Solution**: Follow retention policy. Automate evidence archival.

## Appendix: Evidence Checklist Templates

### Evidence Collection Checklist

```
EVIDENCE COLLECTION CHECKLIST
==============================
System: [Name]
Version: [Version]
Date: YYYY-MM-DD
Collector: [Name]

Core Domain
-----------
[ ] Model selection rationale documented
[ ] Prompt design documented
[ ] Architecture diagrams current
[ ] System requirements documented

Security Domain
---------------
[ ] Authentication implementation verified
[ ] Authorization implementation verified
[ ] Input validation implemented
[ ] Output filtering implemented
[ ] Security scan results collected
[ ] Penetration test results (if applicable)

Data Domain
-----------
[ ] Data sourcing documented
[ ] Data quality verified
[ ] Data retention policy documented
[ ] Data encryption implemented
[ ] Privacy impact assessment completed

Testing Domain
--------------
[ ] Unit test results collected
[ ] Integration test results collected
[ ] Performance test results collected
[ ] Security test results collected
[ ] Evaluation results collected (if applicable)
[ ] Test coverage report generated

Operations Domain
-----------------
[ ] Deployment procedure documented
[ ] Rollback procedure documented and tested
[ ] Monitoring configuration documented
[ ] Health checks implemented and tested
[ ] Incident response procedure documented

Compliance Domain
-----------------
[ ] Regulatory requirements identified
[ ] Compliance checklist completed
[ ] Audit trail samples collected
[ ] Data governance policy documented
[ ] Privacy policy aligned

Evidence Storage
----------------
[ ] Evidence stored in designated location
[ ] Evidence indexed and organized
[ ] Evidence metadata complete
[ ] Evidence backed up

Sign-off: _______________
Date: _______________
```

### Evidence Audit Checklist

```
EVIDENCE AUDIT CHECKLIST
========================
Auditor: [Name]
Date: YYYY-MM-DD
System: [Name]
Version: [Version]

Completeness Check
------------------
[ ] All P0 checklist items have evidence
[ ] All P1 checklist items have evidence or acceptance
[ ] Evidence gaps are documented
[ ] Evidence covers all applicable domains

Quality Check
-------------
[ ] Evidence is authentic (from actual system)
[ ] Evidence is timestamped
[ ] Evidence is attributable
[ ] Evidence is reproducible
[ ] Evidence is clear and understandable
[ ] Evidence includes necessary context

Organization Check
------------------
[ ] Evidence is stored in correct location
[ ] Evidence is properly indexed
[ ] Evidence naming is consistent
[ ] Evidence metadata is complete
[ ] Evidence is accessible to reviewers

Retention Check
---------------
[ ] Evidence retention policy is defined
[ ] Evidence retention periods are appropriate
[ ] Evidence is backed up
[ ] Old evidence is archived according to policy
[ ] Evidence disposal is documented

Compliance Check
----------------
[ ] Evidence meets regulatory requirements
[ ] Evidence chain of custody is maintained
[ ] Evidence is tamper-evident
[ ] Evidence is available on demand for auditors

Audit Findings
--------------
[ ] No findings - Evidence compliance is satisfactory
[ ] Minor findings - [List findings]
[ ] Major findings - [List findings]
[ ] Critical findings - [List findings]

Recommendations
---------------
[Recommendation 1]
[Recommendation 2]

Next Audit Date: [Date]
Sign-off: _______________
Date: _______________
```
