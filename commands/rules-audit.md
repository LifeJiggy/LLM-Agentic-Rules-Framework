# /rules-audit

Audit the current project using the LLM & Agentic Rules Framework.

## Prompt

Use the framework in this repository to audit the current project. Start by identifying the system type, risk tier, and relevant domains. Then review the strongest applicable P0/P1 controls from:

- Core
- Security
- Data
- Integration
- Operations
- Testing
- Documentation
- Performance
- Compliance

Return findings ordered by severity. For each finding include:

- affected file or workflow;
- violated rule or checklist area;
- production risk;
- concrete fix;
- required evidence or test.

## Severity Format

Use this output shape:

| Severity | Finding | Evidence Gap | Fix | Owner |

Severity must be one of `P0`, `P1`, `P2`, or `P3`.

---

# Rules Audit Command — Expanded Reference

## Purpose

The `/rules-audit` command provides a systematic, framework-driven audit of any LLM, agentic, or AI system. It applies the 10-domain LLM & Agentic Rules Framework to identify compliance gaps, security vulnerabilities, reliability risks, and operational deficiencies before they reach production.

## When to Use This Command

Use `/rules-audit` when:

- Preparing for a production release
- Conducting periodic compliance reviews
- Responding to an incident or regression
- Onboarding a new system or team
- Performing due diligence for acquisitions or partnerships
- Assessing third-party AI integrations
- Reviewing model or prompt changes
- Validating remediation after a security incident
- Preparing for regulatory audits
- Establishing a baseline for a new project

## Audit Scope and Depth

### Scope Definition

Before beginning an audit, define the scope:

**In Scope**
- Code repositories under review
- Infrastructure components
- Data pipelines and storage
- External integrations
- Deployment configurations
- Monitoring and observability
- Documentation and runbooks

**Out of Scope**
- Systems not in scope (document why)
- Historical versions no longer in use
- Third-party systems without access
- Experimental features not scheduled for production

### Depth Levels

**Quick Audit (1-2 hours)**
- High-level P0/P1 review
- Key domains only (Security, Operations, Core)
- Surface-level findings
- Suitable for: Pre-release checks, quick assessments

**Standard Audit (4-8 hours)**
- Full P0/P1 review
- All applicable domains
- Detailed findings with evidence
- Suitable for: Production releases, quarterly reviews

**Deep Audit (1-3 days)**
- Comprehensive P0/P1/P2/P3 review
- All 10 domains
- Extensive evidence collection
- Suitable for: Regulatory audits, major releases, incident reviews

## Audit Methodology

### Phase 1: Preparation (15-30 minutes)

**Objective**: Understand the system and prepare for the audit.

**Steps:**

1. **Identify System Type**
   - Is this an LLM application, agentic system, RAG pipeline, MCP integration, or hybrid?
   - What is the primary purpose and user base?
   - What are the key workflows and features?

2. **Determine Risk Tier**
   - Assess impact: data loss, security breach, user harm, financial loss, reputation damage
   - Assess reversibility: can changes be rolled back quickly?
   - Assess blast radius: how many users/systems are affected?
   - Assign tier (Tier 1-4) and document rationale

3. **Select Applicable Domains**
   - Use the domain routing guide to identify primary, secondary, and tertiary domains
   - Document why each domain was selected
   - Note any domain interactions or conflicts

4. **Gather Context**
   - Review system documentation
   - Understand recent changes
   - Identify known issues or concerns
   - Review previous audit findings (if applicable)

5. **Prepare Audit Environment**
   - Set up evidence collection workspace
   - Prepare audit tools (scanners, coverage tools, etc.)
   - Schedule stakeholder interviews if needed

**Deliverables:**
- System type and risk tier documented
- Applicable domains identified
- Audit scope defined
- Evidence collection workspace prepared

### Phase 2: Discovery (1-4 hours)

**Objective**: Collect information about the system through automated scanning, manual review, and stakeholder interviews.

**Steps:**

1. **Automated Scanning**
   - Run dependency vulnerability scanners
   - Run static application security testing (SAST)
   - Run code coverage analysis
   - Run linting and style checks
   - Run configuration validation
   - Check for hardcoded secrets
   - Verify health check endpoints
   - Test monitoring and alerting

2. **Code Review**
   - Review authentication and authorization implementation
   - Review input validation and sanitization
   - Review error handling and logging
   - Review external API integrations
   - Review data access patterns
   - Review configuration management
   - Review deployment scripts

3. **Configuration Review**
   - Review environment configurations
   - Review infrastructure as code
   - Review feature flags
   - Review secret management
   - Review network security groups
   - Review access controls

4. **Documentation Review**
   - Review API documentation
   - Review runbooks and procedures
   - Review architecture diagrams
   - Review changelog and release notes
   - Review data governance policies

5. **Infrastructure Review**
   - Review deployment architecture
   - Review monitoring and observability setup
   - Review backup and recovery procedures
   - Review disaster recovery plan
   - Review scaling and capacity planning

6. **Stakeholder Interviews** (if applicable)
   - Interview developers about development practices
   - Interview operators about operational procedures
   - Interview security team about security controls
   - Interview product owners about compliance requirements

**Deliverables:**
- Raw findings from automated scans
- Code review notes
- Configuration review notes
- Documentation gaps identified
- Infrastructure observations

### Phase 3: Analysis (1-2 hours)

**Objective**: Analyze findings, classify by severity, and determine compliance status.

**Steps:**

1. **Classify Findings**
   - Assign severity (P0/P1/P2/P3) to each finding
   - Categorize by domain (Core, Security, Data, etc.)
   - Identify which checklist items are violated
   - Assess production risk for each finding

2. **Assess Compliance**
   - For each applicable checklist item, determine compliance status
   - Document evidence for compliant items
   - Document gaps for non-compliant items
   - Identify trends and patterns

3. **Prioritize Findings**
   - P0: Must be fixed before production
   - P1: Requires explicit acceptance or fix
   - P2: Should be addressed soon
   - P3: Nice to have

4. **Determine Root Causes**
   - For each finding, identify the root cause
   - Determine if finding is isolated or systemic
   - Identify process improvements needed

5. **Assess Interdependencies**
   - Identify findings that are related
   - Identify findings that block other work
   - Identify findings that require coordinated fixes

**Deliverables:**
- Classified findings list
- Compliance status by domain
- Prioritized action items
- Root cause analysis

### Phase 4: Reporting (30 minutes - 1 hour)

**Objective**: Document findings, recommendations, and next steps in a clear, actionable format.

**Steps:**

1. **Generate Audit Report**
   - Executive summary
   - System overview and scope
   - Findings by severity
   - Findings by domain
   - Evidence summary
   - Recommendations
   - Timeline for remediation

2. **Create Action Plan**
   - Prioritized remediation tasks
   - Owners and due dates
   - Dependencies and blockers
   - Resource requirements

3. **Present Findings**
   - Present to stakeholders
   - Answer questions
   - Gather feedback
   - Obtain commitment for remediation

4. **Document Evidence**
   - Link findings to evidence
   - Store evidence in designated location
   - Update evidence index

**Deliverables:**
- Audit report
- Action plan with owners and timelines
- Evidence package
- Presentation materials (if applicable)

### Phase 5: Follow-up (Ongoing)

**Objective**: Ensure findings are addressed and compliance is maintained.

**Steps:**

1. **Track Remediation**
   - Track progress on P0/P1 findings
   - Verify fixes are implemented correctly
   - Re-audit fixed items
   - Update evidence

2. **Validate Fixes**
   - Review fix implementation
   - Test that fixes work
   - Verify no new issues introduced
   - Update documentation

3. **Monitor Compliance**
   - Set up ongoing monitoring for critical items
   - Configure alerts for compliance violations
   - Schedule periodic re-audits

4. **Continuous Improvement**
   - Identify process improvements
   - Update audit procedures based on lessons learned
   - Share findings with team
   - Update training materials

**Deliverables:**
- Remediation tracking dashboard
- Re-audit results
- Updated procedures
- Lessons learned document

## Audit Domains and Focus Areas

### Domain 1: Core (AI System Fundamentals)

**Focus Areas:**
- Model selection and justification
- Prompt design and validation
- System architecture and design patterns
- Context window management
- Token budget allocation
- Model versioning and rollback

**Key Questions:**
- Is the model appropriate for the use case?
- Are prompts designed to prevent injection?
- Is the architecture scalable and maintainable?
- Are context limits handled gracefully?
- Is token usage monitored and optimized?

**Common Findings:**
- No documented rationale for model selection
- Prompts vulnerable to injection attacks
- No context window overflow handling
- No token usage monitoring
- No model rollback capability

### Domain 2: Security (Threat Protection)

**Focus Areas:**
- Authentication and authorization
- Input validation and sanitization
- Output filtering and content moderation
- Rate limiting and abuse prevention
- API key and credential management
- Prompt injection prevention
- Audit logging

**Key Questions:**
- Are all protected endpoints authenticated?
- Is user input validated before processing?
- Are model outputs filtered for harmful content?
- Are rate limits in place to prevent abuse?
- Are secrets managed securely?

**Common Findings:**
- Missing authentication on API endpoints
- No input validation for user-provided data
- No output filtering for harmful content
- Hardcoded API keys or credentials
- No audit logging for security events

### Domain 3: Data (Data Governance and Privacy)

**Focus Areas:**
- Data sourcing and quality
- Data preprocessing and validation
- Data storage and encryption
- Data retention and deletion
- Privacy impact assessment
- Data lineage and provenance

**Key Questions:**
- Is data sourced ethically and legally?
- Is data quality monitored and enforced?
- Is sensitive data encrypted at rest and in transit?
- Are data retention policies defined and enforced?
- Is PII/PHI properly protected?

**Common Findings:**
- No data quality monitoring
- Sensitive data not encrypted
- No data retention policies
- No privacy impact assessment
- Data lineage not documented

### Domain 4: Integration (External System Connectivity)

**Focus Areas:**
- API contract definition and versioning
- Backward compatibility
- Timeout and retry configuration
- Error handling and fallback
- Circuit breakers
- Health monitoring of dependencies

**Key Questions:**
- Are API contracts defined and versioned?
- Are changes backward compatible?
- Do external calls have timeouts and retries?
- Is fallback behavior defined for critical dependencies?
- Are external service health checks implemented?

**Common Findings:**
- No timeout on external API calls
- No retry logic for transient failures
- No circuit breakers for external dependencies
- No fallback for critical external services
- API contracts not documented

### Domain 5: Development (Code Quality and Engineering)

**Focus Areas:**
- Code quality and style
- Error handling completeness
- Resource management
- Security in code (no hardcoded secrets, no injection vulnerabilities)
- Code review process
- Technical debt management

**Key Questions:**
- Does code follow established standards?
- Are all error paths handled?
- Are resources (files, connections, memory) managed properly?
- Are there any hardcoded secrets or injection vulnerabilities?
- Is code reviewed before merge?

**Common Findings:**
- Code does not follow style guidelines
- Missing error handling in secondary paths
- Resource leaks (files, connections not closed)
- Hardcoded secrets in configuration files
- Code merged without review

### Domain 6: Testing (Validation and Verification)

**Focus Areas:**
- Unit test coverage and quality
- Integration test coverage
- Performance and load testing
- Security testing
- Model evaluation
- Chaos testing
- Test automation and CI/CD integration

**Key Questions:**
- Are critical paths covered by unit tests?
- Are integration tests covering main workflows?
- Is test coverage > 80% for critical paths?
- Are performance and security tests performed?
- Is model output evaluated for quality and safety?
- Are tests automated and run in CI/CD?

**Common Findings:**
- Low test coverage (< 50%)
- No integration tests
- No performance testing
- No security testing
- No model evaluation
- Tests not automated or not in CI/CD

### Domain 7: Operations (Production Reliability)

**Focus Areas:**
- Deployment strategy and automation
- Rollback capability and testing
- Monitoring and alerting
- Health checks
- Incident response procedures
- Backup and recovery
- Logging and observability

**Key Questions:**
- Is deployment automated and tested?
- Can the system be rolled back quickly and safely?
- Are critical metrics monitored with appropriate alerts?
- Are health checks implemented and monitored?
- Is there an incident response plan?
- Are backups tested regularly?

**Common Findings:**
- No automated deployment
- Rollback never tested or too slow
- No monitoring for critical workflows
- No health checks
- No incident response plan
- Backups not tested for restoration

### Domain 8: Documentation (Knowledge Management)

**Focus Areas:**
- API documentation
- Runbooks and operational procedures
- Architecture documentation
- User documentation
- Code documentation
- Changelog and release notes

**Key Questions:**
- Is the API documented and current?
- Are runbooks available for critical operations?
- Is the system architecture documented?
- Do users have documentation for features?
- Is code documented with comments and docstrings?
- Is the changelog maintained?

**Common Findings:**
- No API documentation
- No runbooks for common failure scenarios
- Architecture not documented
- No user documentation
- Code lacks comments and docstrings
- Changelog not maintained

### Domain 9: Performance (Efficiency and Scalability)

**Focus Areas:**
- Latency requirements and monitoring
- Throughput requirements and monitoring
- Resource utilization
- Scalability and capacity planning
- Caching strategy
- Database performance
- Cost optimization

**Key Questions:**
- Are latency and throughput requirements defined and met?
- Is resource utilization monitored?
- Can the system scale to meet demand?
- Is caching used effectively?
- Are database queries optimized?
- Is cost monitored and optimized?

**Common Findings:**
- No performance benchmarks
- No latency or throughput monitoring
- System does not scale under load
- No caching strategy
- Database queries not optimized
- Cost not monitored

### Domain 10: Compliance (Regulatory and Legal)

**Focus Areas:**
- Regulatory requirement identification
- Audit trail implementation
- Data governance policies
- Privacy protection
- Compliance testing and monitoring
- Data processing agreements
- Regulatory reporting

**Key Questions:**
- Are applicable regulations identified?
- Is there an audit trail for compliance?
- Are data governance policies in place?
- Is PII/PHI properly protected?
- Is compliance monitored and tested?
- Are data processing agreements in place?

**Common Findings:**
- Applicable regulations not identified
- No audit trail or incomplete audit logging
- No data governance policies
- Privacy impact assessment not completed
- Compliance not monitored
- No data processing agreements

## Audit Findings Classification

### Severity Definitions

**P0 - Critical (Blocks Production)**
- Definition: Issues that could cause system failure, data loss, security breach, or significant user harm.
- Action: Must be fixed before production deployment.
- Exception: Requires CTO/VP Engineering approval with documented risk acceptance.
- Examples:
  - Authentication/authorization bypass
  - Unhandled exceptions in critical paths
  - Data corruption or loss risk
  - Injection vulnerabilities
  - Missing rollback capability
  - No monitoring or alerting for critical workflows
  - PII/PHI exposure in logs or prompts

**P1 - High (Requires Explicit Acceptance)**
- Definition: Issues that degrade reliability, security, or maintainability but don't block production.
- Action: Must be addressed or explicitly accepted by tech lead/architect with documented rationale.
- Examples:
  - Missing retry logic for external calls
  - No circuit breaker for cascading failure protection
  - Incomplete test coverage (< 80% for critical paths)
  - Missing runbook for common failure scenarios
  - No performance baseline established
  - Incomplete error handling in secondary paths
  - Missing timeout configuration

**P2 - Medium (Should Address)**
- Definition: Issues that improve quality but don't significantly impact reliability or security.
- Action: Track in backlog, address in next sprint/iteration.
- Examples:
  - Code style inconsistencies
  - Missing non-critical tests
  - Documentation gaps for internal tools
  - Minor performance optimizations
  - Refactoring opportunities

**P3 - Low (Nice to Have)**
- Definition: Cosmetic issues, minor improvements, future enhancements.
- Action: Address when convenient, no tracking required.
- Examples:
  - UI polish
  - Additional logging verbosity
  - Enhanced reporting features
  - Code comments improvements

### Finding Classification Criteria

When classifying findings, consider:

**Impact**
- User impact: How many users are affected? How severely?
- Data impact: Is there risk of data loss, corruption, or exposure?
- Financial impact: What is the potential financial loss?
- Reputation impact: What is the potential reputational damage?
- Compliance impact: Are there regulatory violations possible?

**Likelihood**
- How likely is this finding to cause a problem?
- Is this a theoretical issue or observed in practice?
- Are there compensating controls in place?
- Has this caused issues in similar systems?

**Detectability**
- How easy is it to detect when this causes a problem?
- Is there monitoring or alerting for this?
- How quickly can this be identified and addressed?

**Risk Calculation**
```
Risk = Impact × Likelihood × (1 / Detectability)
```

Use this formula to help prioritize findings when severity is ambiguous.

## Audit Output Formats

### Standard Audit Table

Use this format for findings:

| Severity | Finding | Affected Component | Violated Rule | Production Risk | Evidence Gap | Concrete Fix | Required Evidence | Owner | Due Date |
|----------|---------|-------------------|---------------|-----------------|--------------|--------------|-------------------|-------|----------|
| P0 | [Brief description] | [File/component] | [Rule violated] | [Risk description] | [What evidence is missing] | [How to fix] | [What evidence is needed] | [Owner] | [Date] |

### Detailed Finding Template

For each finding, provide detailed information:

```
## Finding #[N]: [Title]

**Severity:** P0/P1/P2/P3

**Affected Component:**
- File: [path/to/file]
- Component: [component name]
- Workflow: [workflow description]

**Violated Rule:**
- Domain: [Core/Security/Data/etc.]
- Checklist Item: [Specific checklist item]
- Framework Reference: [Reference to framework documentation]

**Production Risk:**
- Impact: [Description of potential impact]
- Likelihood: [High/Medium/Low]
- Blast Radius: [Number of users/systems affected]
- Current Mitigations: [Any existing mitigations]

**Evidence Gap:**
- Missing: [What evidence is missing]
- Why Important: [Why this evidence matters]
- How to Collect: [How to obtain this evidence]

**Concrete Fix:**
- Description: [Detailed fix description]
- Steps:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- Effort: [Estimated effort: hours/days/weeks]
- Dependencies: [Any dependencies or blockers]

**Required Evidence:**
- Test: [What test is needed]
- Documentation: [What documentation is needed]
- Verification: [How to verify the fix]

**Owner:** [Name/Role]

**Due Date:** [YYYY-MM-DD]

**Status:** [Open/In Progress/Fixed/Accepted/Deferred]
```

### Executive Summary Template

```
## Executive Summary

**System:** [System name and description]
**Audit Date:** [YYYY-MM-DD]
**Auditor:** [Name/Role]
**Risk Tier:** [Tier 1-4]
**Audit Type:** [Quick/Standard/Deep]

### Overall Compliance Status

| Domain | P0 | P1 | P2 | P3 | Status |
|--------|----|----|-----|-----|--------|
| Core   | 0  | 0  | 1   | 0   | PASS   |
| Security | 0 | 1  | 0   | 0   | CONDITIONAL |
| Data   | 0  | 0  | 2   | 1   | PASS   |
| ...    |    |    |     |     |        |

**Overall Status:** [APPROVED / CONDITIONAL / BLOCKED]

### Key Findings Summary

- **P0 (Critical):** [X] findings
  - [Finding 1]: [Brief description]
  - [Finding 2]: [Brief description]
- **P1 (High):** [X] findings
  - [Finding 1]: [Brief description]
  - [Finding 2]: [Brief description]
- **P2 (Medium):** [X] findings
- **P3 (Low):** [X] findings

### Critical Risks

1. **[Risk 1]:** [Description]
   - Impact: [Impact description]
   - Mitigation: [Mitigation strategy]
   - Timeline: [Resolution timeline]

2. **[Risk 2]:** [Description]
   - Impact: [Impact description]
   - Mitigation: [Mitigation strategy]
   - Timeline: [Resolution timeline]

### Recommendations

1. **[Recommendation 1]:** [Description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]

2. **[Recommendation 2]:** [Description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]

### Next Steps

1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]
3. [Action 3]: [Owner] - [Due date]

### Appendix

- Detailed findings: [Link]
- Evidence package: [Link]
- Raw scan results: [Link]
```

## Audit Workflow

### Pre-Audit Checklist

Before starting the audit:

- [ ] System type identified and documented
- [ ] Risk tier assessed and documented
- [ ] Applicable domains selected
- [ ] Audit scope defined
- [ ] Audit depth determined (Quick/Standard/Deep)
- [ ] Evidence collection workspace prepared
- [ ] Audit tools ready (scanners, coverage tools, etc.)
- [ ] Stakeholders notified (if applicable)
- [ ] Previous audit findings reviewed (if applicable)
- [ ] Access to systems and repositories confirmed

### Audit Execution Steps

**Step 1: Automated Scanning**

Run the following automated scans:

1. **Dependency Vulnerability Scan**
   - Tool: [npm audit / pip-audit / Snyk / etc.]
   - Scope: All dependencies including transitive
   - Severity threshold: Critical and High
   - Command example:
     ```bash
     npm audit --audit-level=high
     ```

2. **Secret Scanning**
   - Tool: [gitleaks / truffleHog / git-secrets]
   - Scope: Entire codebase including git history
   - Command example:
     ```bash
     gitleaks detect --source . --report-path secrets-report.json
     ```

3. **Static Code Analysis (SAST)**
   - Tool: [SonarQube / CodeQL / Semgrep]
   - Scope: All code files
   - Focus: Security vulnerabilities, code smells, bugs
   - Command example:
     ```bash
     semgrep --config auto --severity=ERROR .
     ```

4. **Code Coverage Analysis**
   - Tool: [pytest-cov / Istanbul / JaCoCo]
   - Scope: All testable code
   - Target: > 80% coverage for critical paths
   - Command example:
     ```bash
     pytest --cov=src --cov-report=html
     ```

5. **Linting and Style Checks**
   - Tool: [ESLint / pylint / golangci-lint]
   - Scope: All code files
   - Command example:
     ```bash
     pylint src/ --fail-under=8.0
     ```

6. **Configuration Validation**
   - Tool: [jsonschema / yamllint / config-lint]
   - Scope: All configuration files
   - Command example:
     ```bash
     yamllint config/
     ```

7. **Health Check Verification**
   - Method: Manual or automated
   - Scope: All health check endpoints
   - Verify: /health, /health/ready, /health/live
   - Command example:
     ```bash
     curl -f http://localhost:8080/health
     ```

8. **Monitoring and Alerting Verification**
   - Method: Manual review
   - Scope: Monitoring dashboards, alert rules
   - Verify: Critical metrics monitored, alerts configured

**Step 2: Manual Code Review**

Review the following areas manually:

1. **Authentication and Authorization**
   - Review authentication middleware/decorators
   - Review authorization logic for bypasses
   - Verify token validation
   - Check for hardcoded credentials
   - Files to review: Auth modules, API gateways, middleware

2. **Input Validation and Sanitization**
   - Review input validation at all boundaries
   - Check for SQL injection vulnerabilities
   - Check for command injection vulnerabilities
   - Check for path traversal vulnerabilities
   - Check for XSS vulnerabilities
   - Files to review: API endpoints, file upload handlers, database queries

3. **Error Handling and Logging**
   - Review exception handling in critical paths
   - Check for bare except clauses
   - Verify error messages don't leak sensitive information
   - Verify structured logging is implemented
   - Files to review: Error handlers, logging configuration, exception classes

4. **External API Integrations**
   - Review timeout configuration
   - Review retry logic
   - Review circuit breaker implementation
   - Review fallback behavior
   - Review error handling
   - Files to review: API clients, service integrations, HTTP handlers

5. **Data Access Patterns**
   - Review database queries for injection
   - Review data encryption
   - Review access controls
   - Review data validation
   - Files to review: Data access layer, ORM models, database migrations

6. **Configuration Management**
   - Review environment variable usage
   - Check for hardcoded configuration
   - Verify secret management
   - Review configuration validation
   - Files to review: Config files, environment setup, secret management

7. **Deployment and Infrastructure**
   - Review deployment scripts
   - Review infrastructure as code
   - Review rollback procedures
   - Review health checks
   - Files to review: Deployment scripts, Terraform/CloudFormation, Kubernetes manifests

**Step 3: Infrastructure Review**

Review infrastructure and operations:

1. **Deployment Architecture**
   - Review deployment strategy (blue-green, canary, rolling)
   - Review deployment automation
   - Review deployment history
   - Verify deployment testing

2. **Monitoring and Observability**
   - Review monitoring dashboards
   - Review alert rules and thresholds
   - Review log aggregation
   - Review distributed tracing
   - Verify on-call rotation

3. **Backup and Recovery**
   - Review backup procedures
   - Review backup testing
   - Review recovery procedures
   - Verify RTO and RPO are met

4. **Disaster Recovery**
   - Review disaster recovery plan
   - Review DR testing
   - Verify DR infrastructure

5. **Security Configuration**
   - Review network security groups
   - Review firewall rules
   - Review encryption configuration
   - Review access controls

**Step 4: Documentation Review**

Review documentation completeness and quality:

1. **API Documentation**
   - Verify all endpoints are documented
   - Verify request/response schemas are documented
   - Verify error codes are documented
   - Verify examples are provided

2. **Runbooks and Procedures**
   - Verify runbooks exist for critical operations
   - Verify runbooks are step-by-step and actionable
   - Verify runbooks are tested
   - Verify runbooks are accessible

3. **Architecture Documentation**
   - Verify architecture diagrams exist
   - Verify data flow is documented
   - Verify component interactions are documented
   - Verify ADRs exist for major decisions

4. **User Documentation**
   - Verify user guides exist
   - Verify getting started guide exists
   - Verify troubleshooting guide exists

5. **Code Documentation**
   - Verify complex code has comments
   - Verify public APIs have docstrings
   - Verify README is up to date

6. **Change Documentation**
   - Verify changelog is maintained
   - Verify release notes are written
   - Verify migration guides exist for breaking changes

**Step 5: Stakeholder Interviews** (if applicable)

Conduct interviews with key stakeholders:

1. **Developers**
   - Ask about development practices
   - Ask about code review process
   - Ask about testing practices
   - Ask about deployment procedures
   - Ask about known issues

2. **Operators**
   - Ask about operational procedures
   - Ask about incident response
   - Ask about monitoring and alerting
   - Ask about backup and recovery
   - Ask about known operational issues

3. **Security Team**
   - Ask about security controls
   - Ask about vulnerability management
   - Ask about incident response
   - Ask about compliance requirements
   - Ask about security training

4. **Product Owners**
   - Ask about compliance requirements
   - Ask about user impact
   - Ask about business continuity
   - Ask about risk tolerance

**Step 6: Evidence Collection**

Collect evidence for each finding:

1. **Screenshots**
   - Monitoring dashboards
   - Alert configurations
   - Health check results
   - Configuration screenshots

2. **Logs**
   - Application logs
   - System logs
   - Audit logs
   - Error logs

3. **Test Results**
   - Automated test reports
   - Coverage reports
   - Performance test results
   - Security scan results

4. **Configuration Files**
   - Sanitized configuration files
   - Infrastructure as code
   - Deployment manifests

5. **Documentation**
   - Existing documentation
   - Gaps identified

**Step 7: Findings Compilation**

Compile all findings into the audit report:

1. **Deduplicate Findings**
   - Remove duplicate findings
   - Consolidate related findings
   - Merge findings with same root cause

2. **Classify by Severity**
   - Assign P0/P1/P2/P3 to each finding
   - Justify severity assignment

3. **Classify by Domain**
   - Assign domain to each finding
   - Identify cross-domain findings

4. **Assess Production Risk**
   - Describe potential impact
   - Assess likelihood
   - Describe blast radius

5. **Propose Fixes**
   - Provide concrete, actionable fixes
   - Estimate effort
   - Identify dependencies

6. **Identify Evidence Gaps**
   - Note what evidence is missing
   - Explain why evidence is important
   - Describe how to collect evidence

7. **Assign Owners and Due Dates**
   - Assign owner for each finding
   - Set realistic due dates based on severity
   - P0: 24-48 hours
   - P1: 1-2 weeks
   - P2: 1 month
   - P3: Next quarter

## Audit Report Structure

### 1. Executive Summary

**Purpose:** Provide high-level overview for leadership.

**Content:**
- System name and description
- Audit date and auditor
- Risk tier
- Overall compliance status
- Key findings summary
- Critical risks
- Top recommendations
- Next steps

### 2. Audit Scope and Methodology

**Purpose:** Document what was audited and how.

**Content:**
- Systems and components in scope
- Systems and components out of scope
- Audit depth (Quick/Standard/Deep)
- Domains reviewed
- Methods used (automated scanning, manual review, interviews)
- Tools used
- Stakeholders involved
- Limitations and assumptions

### 3. System Overview

**Purpose:** Describe the system for audit context.

**Content:**
- System type and purpose
- Architecture overview
- Key components and workflows
- External dependencies
- User base and impact
- Deployment environment
- Recent changes

### 4. Findings by Severity

**Purpose:** Present all findings ordered by severity.

**Content:**
- P0 findings (Critical)
- P1 findings (High)
- P2 findings (Medium)
- P3 findings (Low)

For each finding:
- Severity
- Finding description
- Affected component
- Violated rule
- Production risk
- Evidence gap
- Concrete fix
- Required evidence
- Owner and due date

### 5. Findings by Domain

**Purpose:** Present findings organized by domain.

**Content:**
- Core findings
- Security findings
- Data findings
- Integration findings
- Development findings
- Testing findings
- Operations findings
- Documentation findings
- Performance findings
- Compliance findings

### 6. Compliance Summary

**Purpose:** Show compliance status by domain and checklist item.

**Content:**
- Compliance matrix (domain × checklist item)
- Pass/Fail/Conditional status
- Evidence collected
- Evidence gaps
- Acceptances or waivers

### 7. Evidence Package

**Purpose:** Link to all collected evidence.

**Content:**
- Index of evidence files
- Links to evidence storage
- Evidence metadata
- Evidence completeness assessment

### 8. Recommendations

**Purpose:** Provide actionable recommendations beyond immediate findings.

**Content:**
- Process improvements
- Tooling improvements
- Training needs
- Architecture improvements
- Policy updates

### 9. Action Plan

**Purpose:** Provide concrete next steps with owners and timelines.

**Content:**
- Prioritized action items
- Owners and due dates
- Dependencies and blockers
- Resource requirements
- Progress tracking

### 10. Appendices

**Purpose:** Provide supporting details.

**Content:**
- Raw scan results
- Detailed technical findings
- Configuration snapshots
- Interview notes
- Glossary
- References to framework documentation

## Audit Evidence Requirements

### Evidence by Finding Severity

**P0 Findings**
- Must have concrete evidence (logs, scan results, screenshots)
- Evidence must be reproducible
- Evidence must be from production or production-like environment
- Evidence must be timestamped
- Evidence must be attributable

**P1 Findings**
- Should have concrete evidence
- Evidence should be reproducible
- Evidence can be from staging or production-like environment

**P2 Findings**
- Evidence is recommended but not required
- Screenshots or descriptions acceptable

**P3 Findings**
- Evidence is optional
- Description is sufficient

### Evidence Collection Best Practices

**Automated Evidence**
- Use tools to automatically collect evidence
- Store evidence in structured format (JSON, XML)
- Include timestamps and metadata
- Verify evidence integrity

**Manual Evidence**
- Take screenshots with timestamps
- Document steps to reproduce
- Include context and environment details
- Verify evidence is clear and readable

**Evidence Linking**
- Link each finding to its evidence
- Use consistent naming conventions
- Maintain evidence index
- Version evidence files

## Audit Quality Assurance

### Self-Review

Before finalizing the audit:

- [ ] All P0/P1 items have evidence or documented rationale
- [ ] All findings are classified with appropriate severity
- [ ] All findings have concrete fixes proposed
- [ ] All findings have owners assigned
- [ ] All evidence is collected and linked
- [ ] Report is reviewed for clarity and completeness
- [ ] Report is reviewed for consistency
- [ ] Report is reviewed for actionable recommendations

### Peer Review

Have another auditor or technical lead review:

- Audit methodology
- Findings classification
- Severity assignments
- Fix proposals
- Evidence completeness

### Stakeholder Review

Share with stakeholders for:

- Factual accuracy
- Completeness
- Acceptance of findings
- Commitment to remediation

## Audit Follow-up

### Remediation Tracking

Track remediation of findings:

1. **Create Remediation Ticket**
   - For each P0/P1 finding
   - Include finding details
   - Include proposed fix
   - Assign owner and due date

2. **Track Progress**
   - Update status regularly
   - Document blockers
   - Escalate if overdue

3. **Verify Fixes**
   - Review fix implementation
   - Test that fix resolves finding
   - Verify no new issues introduced
   - Update evidence

4. **Re-audit**
   - Re-audit fixed findings
   - Verify compliance
   - Update audit report

### Re-audit Criteria

Re-audit when:

- All P0 findings are resolved
- All P1 findings are resolved or accepted
- Significant time has passed (3-6 months)
- Major system changes have occurred
- Regulatory requirements have changed

### Continuous Auditing

Implement continuous auditing:

- Automated scans in CI/CD
- Periodic manual audits
- Real-time compliance monitoring
- Alerting on compliance violations

## Audit Tools and Automation

### Recommended Tools

**Dependency Scanning**
- npm audit, pip-audit, Snyk, Dependabot

**Secret Scanning**
- gitleaks, truffleHog, git-secrets

**SAST**
- SonarQube, CodeQL, Semgrep, ESLint, pylint

**DAST**
- OWASP ZAP, Burp Suite

**Code Coverage**
- pytest-cov, Istanbul, JaCoCo

**Infrastructure Scanning**
- Checkov, tfsec, CloudSploit

**Configuration Validation**
- jsonschema, yamllint, kubeval

**Monitoring and Observability**
- Prometheus, Grafana, Datadog, New Relic

**Evidence Management**
- Git (for code and configs)
- Artifact repositories (for builds and scans)
- Cloud storage (for large files)

### Automated Audit Pipeline

Implement automated auditing in CI/CD:

```yaml
# Example: GitHub Actions workflow
name: Rules Audit
on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Dependency Scan
        run: npm audit --audit-level=high
      
      - name: Secret Scan
        uses: gitleaks/gitleaks-action@v1
      
      - name: SAST Scan
        run: semgrep --config auto --severity=ERROR .
      
      - name: Lint Check
        run: npm run lint
      
      - name: Test Coverage
        run: npm run test:coverage
      
      - name: Generate Report
        run: python scripts/generate-audit-report.py
      
      - name: Upload Evidence
        uses: actions/upload-artifact@v3
        with:
          name: audit-evidence
          path: evidence/
```

## Audit Anti-Patterns

### Anti-Pattern 1: Audit as a One-Time Event

**Problem:** Treating audit as a one-time checkbox exercise.

**Impact:** Compliance degrades over time, issues recur.

**Solution:** Implement continuous auditing with automated scans and periodic manual reviews.

### Anti-Pattern 2: Focusing on Low-Priority Issues

**Problem:** Spending time on P2/P3 issues while P0/P1 issues remain unresolved.

**Impact:** Critical risks remain unaddressed.

**Solution:** Always prioritize P0/P1 findings. Address P2/P3 only after critical issues are resolved.

### Anti-Pattern 3: Ignoring Evidence Gaps

**Problem:** Claiming compliance without evidence or ignoring evidence gaps.

**Impact:** Unsubstantiated claims, audit failures, regulatory violations.

**Solution:** Explicitly document all evidence gaps. Never assume compliance without evidence.

### Anti-Pattern 4: Audit Without Follow-up

**Problem:** Generating audit report but not tracking remediation.

**Impact:** Findings remain unresolved, risks persist.

**Solution:** Create remediation tickets, track progress, verify fixes, re-audit.

### Anti-Pattern 5: Audit Without Stakeholder Buy-in

**Problem:** Conducting audit without stakeholder involvement or commitment.

**Impact:** Findings ignored, no resources for remediation.

**Solution:** Involve stakeholders early, present findings together, obtain commitment for remediation.

### Anti-Pattern 6: Over-Reliance on Automated Tools

**Problem:** Relying solely on automated scans without manual review.

**Impact:** Missing context-dependent findings, false sense of security.

**Solution:** Combine automated scanning with manual code review and stakeholder interviews.

### Anti-Pattern 7: Generic Findings

**Problem:** Reporting vague findings without specific affected files or concrete fixes.

**Impact:** Findings are not actionable, remediation is delayed.

**Solution:** Always provide specific file paths, violated rules, concrete fixes, and evidence requirements.

### Anti-Pattern 8: Severity Inflation or Deflation

**Problem:** Assigning incorrect severity to findings (everything is P0 or everything is P3).

**Impact:** Prioritization breakdown, critical issues ignored or everything is urgent.

**Solution:** Use clear severity definitions and criteria. Calibrate severity assignments with team.

## Audit Checklist

### Pre-Audit Checklist

- [ ] System type identified and documented
- [ ] Risk tier assessed and documented
- [ ] Applicable domains selected
- [ ] Audit scope defined
- [ ] Audit depth determined
- [ ] Evidence collection workspace prepared
- [ ] Audit tools ready
- [ ] Stakeholders notified (if applicable)
- [ ] Previous audit findings reviewed
- [ ] Access to systems and repositories confirmed

### During-Audit Checklist

- [ ] Automated scans completed
- [ ] Code review completed
- [ ] Configuration review completed
- [ ] Documentation review completed
- [ ] Infrastructure review completed
- [ ] Stakeholder interviews completed (if applicable)
- [ ] Evidence collected for all findings
- [ ] Findings classified by severity
- [ ] Findings classified by domain
- [ ] Production risks assessed
- [ ] Concrete fixes proposed
- [ ] Owners assigned
- [ ] Due dates set

### Post-Audit Checklist

- [ ] Audit report generated
- [ ] Executive summary written
- [ ] Findings documented with all required fields
- [ ] Evidence package compiled
- [ ] Action plan created with owners and timelines
- [ ] Report reviewed for quality
- [ ] Peer review completed
- [ ] Stakeholder review completed
- [ ] Findings presented to stakeholders
- [ ] Remediation tickets created for P0/P1 findings
- [ ] Evidence stored in designated location
- [ ] Audit documented in audit log

### Follow-up Checklist

- [ ] Remediation progress tracked
- [ ] Fixes verified
- [ ] Re-audit completed for P0/P1 findings
- [ ] Evidence updated
- [ ] Lessons learned documented
- [ ] Processes updated based on lessons learned
- [ ] Training materials updated (if needed)
- [ ] Next audit scheduled

## Audit Metrics

Track these metrics to improve audit quality:

**Audit Effectiveness**
- Percentage of P0 issues found in audit that were not found in testing
- Percentage of findings that are P0/P1
- Time to resolve findings after audit
- Re-audit pass rate

**Audit Efficiency**
- Time to complete audit
- Findings per hour of audit
- Evidence completeness rate
- Stakeholder satisfaction

**Compliance Metrics**
- Overall compliance rate
- Compliance rate by domain
- Evidence completeness rate
- Trend of compliance over time

**Process Metrics**
- Number of audits per period
- Audit coverage (percentage of systems audited)
- Finding recurrence rate
- Process improvement implementation rate

## Appendix: Audit Templates

### Audit Report Template

```
AUDIT REPORT
============
System: [System name]
Version: [Version]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]
Risk Tier: [Tier 1-4]
Audit Type: [Quick/Standard/Deep]

Executive Summary
-----------------
[High-level summary of audit results]

Overall Status: [APPROVED / CONDITIONAL / BLOCKED]

System Overview
---------------
[Description of system, architecture, purpose]

Audit Scope
-----------
[What was audited, what was not]

Methodology
-----------
[How the audit was conducted]

Findings Summary
----------------
P0 (Critical): [X]
P1 (High): [X]
P2 (Medium): [X]
P3 (Low): [X]

Detailed Findings
-----------------
[Detailed findings with all required fields]

Compliance Summary
------------------
[Compliance status by domain]

Evidence Package
----------------
[Links to evidence]

Recommendations
---------------
[Recommendations for improvements]

Action Plan
-----------
[Prioritized actions with owners and timelines]

Appendices
----------
[Supporting details]

Sign-off: _______________
Date: _______________
```

### Audit Evidence Index Template

```
AUDIT EVIDENCE INDEX
====================
System: [Name]
Audit Date: YYYY-MM-DD
Auditor: [Name]

Evidence Items
--------------
| ID | Description | Type | Location | Checklist Item | Date Collected | Reviewer |
|----|-------------|------|----------|----------------|----------------|----------|
| E1 | [Description] | [Test/Security/Config/etc.] | [Path] | [Checklist item] | [Date] | [Name] |

Evidence Gaps
-------------
| ID | Checklist Item | Why Important | How to Collect | Owner | Due Date |
|----|----------------|---------------|----------------|-------|----------|
| G1 | [Checklist item] | [Why needed] | [How to collect] | [Owner] | [Date] |

Index Complete
--------------
Total Evidence Items: [X]
Total Evidence Gaps: [X]
Evidence Completeness: [X]%

Sign-off: _______________
Date: _______________
```

### Audit Meeting Agenda Template

```
AUDIT FINDINGS PRESENTATION
============================
System: [Name]
Date: YYYY-MM-DD
Attendees: [Names]

Agenda
------
1. Executive Summary (5 min)
   - Audit scope and methodology
   - Overall compliance status
   - Key findings summary

2. P0 Findings (15 min)
   - Critical issues requiring immediate action
   - Production risks
   - Required fixes and timelines

3. P1 Findings (15 min)
   - High-priority issues
   - Acceptance requirements
   - Mitigation plans

4. P2/P3 Findings (5 min)
   - Medium and low priority items
   - Backlog items

5. Recommendations (5 min)
   - Process improvements
   - Tooling improvements
   - Training needs

6. Action Plan (10 min)
   - Prioritized actions
   - Owners and due dates
   - Resource requirements

7. Q&A (10 min)

Action Items
------------
- [Action 1]: [Owner] - [Due date]
- [Action 2]: [Owner] - [Due date]

Next Steps
----------
- [ ] Distribute audit report
- [ ] Create remediation tickets
- [ ] Schedule follow-up meeting
- [ ] Schedule re-audit
```

## Appendix: Common Audit Findings and Fixes

### Finding: No Authentication on API Endpoints

**Severity:** P0

**Violated Rule:** Security - Authentication

**Production Risk:** Unauthorized access to system, data breach, data manipulation

**Concrete Fix:**
1. Implement authentication middleware
2. Add authentication checks to all protected endpoints
3. Use industry-standard authentication (OAuth 2.0, JWT)
4. Implement token validation
5. Add authentication tests

**Required Evidence:**
- Authentication tests passing
- Security scan showing no auth bypass
- Code review of auth implementation

### Finding: No Input Validation

**Severity:** P0

**Violated Rule:** Security - Input Validation

**Production Risk:** Injection attacks (SQL, command, XSS), data corruption

**Concrete Fix:**
1. Implement input validation at all boundaries
2. Use parameterized queries for database access
3. Sanitize user input
4. Validate file uploads
5. Add validation tests

**Required Evidence:**
- Input validation tests passing
- Fuzz testing results
- Security scan showing no injection vulnerabilities

### Finding: No Timeout on External API Calls

**Severity:** P1

**Violated Rule:** Core/Integration - Error Handling

**Production Risk:** Hanging operations, resource exhaustion, cascading failures

**Concrete Fix:**
1. Add timeout configuration to all external API calls
2. Document timeout values
3. Implement timeout handling
4. Add timeout tests

**Required Evidence:**
- Code review confirming timeouts
- Timeout handling tests passing
- Monitoring showing timeout occurrences

### Finding: Low Test Coverage

**Severity:** P1

**Violated Rule:** Testing - Test Coverage

**Production Risk:** Undetected bugs, regressions, quality issues

**Concrete Fix:**
1. Identify critical paths with low coverage
2. Write unit tests for uncovered critical paths
3. Write integration tests for main workflows
4. Set up coverage reporting in CI/CD
5. Enforce coverage thresholds

**Required Evidence:**
- Coverage report showing > 80% for critical paths
- Tests passing in CI/CD
- Test quality review

### Finding: No Monitoring or Alerting

**Severity:** P0

**Violated Rule:** Operations - Monitoring and Alerting

**Production Risk:** Undetected failures, extended outages, slow incident response

**Concrete Fix:**
1. Define critical metrics to monitor
2. Set up monitoring dashboards
3. Configure alerts for critical failures
4. Set up on-call rotation
5. Test alerts

**Required Evidence:**
- Monitoring dashboards screenshot
- Alert configuration documentation
- Alert testing results
- On-call rotation documented

### Finding: Hardcoded Secrets

**Severity:** P0

**Violated Rule:** Security - Credential Management

**Production Risk:** Credential exposure, security breach, unauthorized access

**Concrete Fix:**
1. Remove hardcoded secrets from code
2. Use secret management system (Vault, AWS Secrets Manager, etc.)
3. Rotate exposed credentials
4. Implement secret scanning in CI/CD
5. Document secret management procedures

**Required Evidence:**
- Secret scan showing no hardcoded secrets
- Secret management system configured
- Credential rotation completed
- CI/CD secret scanning configured

### Finding: No Rollback Capability

**Severity:** P0

**Violated Rule:** Operations - Rollback Capability

**Production Risk:** Extended outages, inability to recover from bad deployments

**Concrete Fix:**
1. Document rollback procedure
2. Test rollback in staging
3. Automate rollback where possible
4. Define rollback triggers
5. Measure rollback time

**Required Evidence:**
- Rollback runbook documented
- Rollback tested and successful
- Rollback time meets RTO
- Previous versions available for rollback

## Appendix: Audit Acronyms and Glossary

**Audit Acronyms**

- **P0/P1/P2/P3**: Priority levels (Critical/High/Medium/Low)
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective
- **SAST**: Static Application Security Testing
- **DAST**: Dynamic Application Security Testing
- **SCA**: Software Composition Analysis
- **CI/CD**: Continuous Integration/Continuous Deployment
- **ADR**: Architecture Decision Record
- **RBAC**: Role-Based Access Control
- **PII**: Personally Identifiable Information
- **PHI**: Protected Health Information
- **RAG**: Retrieval-Augmented Generation
- **MCP**: Model Context Protocol
- **API**: Application Programming Interface
- **TLS**: Transport Layer Security
- **SLI**: Service Level Indicator
- **SLO**: Service Level Objective
- **SLA**: Service Level Agreement
- **DR**: Disaster Recovery
- **MTTR**: Mean Time to Recovery
- **MTTD**: Mean Time to Detect

**Audit Terminology**

- **Finding**: A specific issue identified during the audit
- **Evidence**: Proof that a system meets or does not meet a requirement
- **Checklist Item**: A specific requirement from the framework
- **Domain**: A category of requirements (Core, Security, Data, etc.)
- **Severity**: The priority level of a finding (P0-P3)
- **Compliance**: Adherence to framework requirements
- **Gap**: A missing control or requirement
- **Acceptance**: Formal acknowledgment of a finding with documented rationale
- **Remediation**: The process of fixing a finding
- **Re-audit**: A follow-up audit to verify fixes

## Appendix: Audit References

**Framework Documentation**
- `skills/llm-agentic-rules/SKILL.md` - Main framework skill
- `skills/llm-agentic-rules/domain-routing-guide.md` - Domain routing guidance
- `skills/llm-agentic-rules/review-gates-criteria.md` - P0/P1/P2/P3 criteria
- `skills/llm-agentic-rules/compliance-evidence-standards.md` - Evidence standards
- `skills/llm-agentic-rules/domain-checklist-reference.md` - Domain checklists
- `skills/system/SKILL.md` - System reliability hardening
- `skills/system/reliability-checklist.md` - Reliability checklist
- `skills/system/recovery-playbook.md` - Recovery procedures
- `skills/system/timeout-strategy.md` - Timeout configuration
- `skills/system/retry-policy.md` - Retry strategies
- `skills/system/observability-standards.md` - Observability standards
- `skills/system/deployment-safety.md` - Deployment safety

**External Resources**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- SOC 2 Compliance: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html
- ISO 27001: https://www.iso.org/isoiec-27001-information-security.html
- HIPAA Compliance: https://www.hhs.gov/hipaa/
- PCI DSS: https://www.pcisecuritystandards.org/
- GDPR: https://gdpr.eu/
