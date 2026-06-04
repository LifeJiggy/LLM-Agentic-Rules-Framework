# Audit Preparation Guide

Use this guide to prepare for a rules audit using the LLM & Agentic Rules Framework.

## Preparation Philosophy

Proper preparation is essential for an effective audit. Rushed or incomplete preparation leads to incomplete findings, missed issues, and wasted time. This guide ensures that audits are thorough, efficient, and produce actionable results.

### Preparation Principles

**Understand Before Judging**
- Learn the system before auditing it.
- Understand the business context and constraints.
- Recognize trade-offs and rationale for past decisions.

**Be Systematic**
- Follow a structured approach.
- Use checklists to ensure completeness.
- Document everything.

**Be Objective**
- Base findings on evidence, not opinions.
- Apply standards consistently.
- Avoid bias toward or against specific technologies or approaches.

**Be Constructive**
- Focus on improvement, not blame.
- Provide actionable recommendations.
- Recognize what is working well.

## Pre-Audit Phase

### Step 1: Understand the Audit Request

**Questions to Answer:**
- Why is this audit being conducted?
- What are the audit goals and objectives?
- Who are the stakeholders?
- What are the success criteria?
- What is the timeline?
- What is the scope?

**Deliverables:**
- Audit charter or brief
- Stakeholder map
- Success criteria defined
- Timeline agreed upon

### Step 2: Identify System Type and Risk Tier

**System Type Identification**

Determine the system type:

| System Type | Characteristics | Primary Domains |
|-------------|----------------|-----------------|
| AI Application | LLM-powered app, chatbot, assistant | Core, Security, Data, Testing, Operations, Compliance |
| Agentic System | Multi-step agent with tools | Core, Integration, Security, Operations, Testing |
| RAG System | Retrieval-augmented generation | Core, Data, Security, Testing, Performance |
| MCP Integration | Model Context Protocol integration | Core, Integration, Security, Operations, Testing |
| Model Service | API serving ML models | Core, Security, Operations, Performance, Testing |
| Data Pipeline | ETL/ELT for AI training data | Data, Security, Operations, Testing |
| Prompt Management | Prompt engineering and versioning | Core, Security, Documentation, Testing |

**Risk Tier Assessment**

Assess the risk tier based on:

**Tier 1 - Critical**
- Financial transactions or healthcare data
- Critical infrastructure
- High user impact (100k+ users)
- Regulatory requirements (HIPAA, PCI, SOX)
- Examples: Payment processing, medical diagnosis, critical infrastructure

**Tier 2 - High**
- Customer-facing systems
- Significant business impact
- Sensitive data handling
- Examples: E-commerce, SaaS platforms, communication tools

**Tier 3 - Medium**
- Internal tools
- Limited user base
- Non-sensitive data
- Examples: Internal dashboards, development tools, internal APIs

**Tier 4 - Low**
- Experimental systems
- Prototypes
- Non-critical tools
- Examples: POCs, research projects, personal tools

**Deliverables:**
- System type documented
- Risk tier assigned with rationale
- Risk assessment document

### Step 3: Select Applicable Domains

Use the domain routing guide to select applicable domains:

**Primary Domains (Must Apply)**
- Domains directly related to system type
- Domains directly related to audit objectives

**Secondary Domains (Should Apply)**
- Domains indirectly affected
- Domains with known concerns

**Tertiary Domains (Consider)**
- Domains that might be relevant
- Review at a high level

**Deliverables:**
- Domain selection documented
- Routing rationale documented
- Domain checklist items identified

### Step 4: Define Audit Scope

**Scope Definition**

**In Scope:**
- [ ] Code repositories
- [ ] Infrastructure components
- [ ] Data pipelines
- [ ] External integrations
- [ ] Deployment configurations
- [ ] Monitoring and observability
- [ ] Documentation
- [ ] Security controls
- [ ] Compliance requirements

**Out of Scope:**
- [ ] Third-party systems without access
- [ ] Historical versions no longer in use
- [ ] Experimental features not scheduled for production
- [ ] [Other exclusions with rationale]

**Deliverables:**
- Scope document
- Exclusions documented with rationale

### Step 5: Determine Audit Depth

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

**Deliverables:**
- Audit depth determined
- Time estimate provided
- Resource requirements identified

## Tool Preparation

### Required Tools

**Dependency Scanning**
- [ ] npm audit / pip-audit / Snyk / Dependabot
- [ ] Installed and configured
- [ ] Scope defined (all dependencies or key dependencies only)

**Secret Scanning**
- [ ] gitleaks / truffleHog / git-secrets
- [ ] Installed and configured
- [ ] Scope defined (entire repo or recent changes only)

**Static Code Analysis (SAST)**
- [ ] SonarQube / CodeQL / Semgrep / ESLint / pylint
- [ ] Installed and configured
- [ ] Ruleset defined

**Code Coverage**
- [ ] pytest-cov / Istanbul / JaCoCo
- [ ] Installed and configured
- [ ] Coverage threshold defined

**Infrastructure Scanning**
- [ ] Checkov / tfsec / CloudSploit
- [ ] Installed and configured
- [ ] Scope defined

**Configuration Validation**
- [ ] jsonschema / yamllint / kubeval
- [ ] Installed and configured
- [ ] Schemas defined

### Tool Configuration

For each tool, configure:

1. **Scope**: What to scan (entire repo, specific directories, etc.)
2. **Severity Threshold**: What to report (Critical, High, Medium, Low)
3. **Exclusions**: What to exclude (test files, generated code, etc.)
4. **Output Format**: How to capture results (JSON, HTML, etc.)
5. **Baseline**: Whether to compare against previous results

### Automated Scan Setup

Set up automated scanning if not already in place:

```yaml
# Example: Pre-audit scan script
name: Pre-Audit Scan
steps:
  - name: Dependency Scan
    run: npm audit --audit-level=high --json > audit/dependency-scan.json
  
  - name: Secret Scan
    run: gitleaks detect --source . --report-path audit/secret-scan.json
  
  - name: SAST Scan
    run: semgrep --config auto --severity=ERROR --json -o audit/sast-scan.json .
  
  - name: Lint Check
    run: npm run lint > audit/lint-report.txt 2>&1
  
  - name: Test Coverage
    run: npm run test:coverage -- --json > audit/coverage-report.json
```

## Evidence Collection Preparation

### Evidence Workspace Setup

Create a structured evidence workspace:

```
audit-evidence/
├── scans/
│   ├── dependency/
│   ├── secrets/
│   ├── sast/
│   ├── lint/
│   └── coverage/
├── configs/
│   ├── application/
│   ├── infrastructure/
│   └── deployment/
├── docs/
│   ├── architecture/
│   ├── runbooks/
│   ├── api/
│   └── changelog/
├── logs/
│   ├── application/
│   ├── system/
│   └── audit/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── performance/
│   └── security/
├── screenshots/
│   ├── monitoring/
│   ├── dashboards/
│   └── configurations/
└── metadata/
    ├── scan-metadata.json
    ├── config-snapshots.json
    └── evidence-index.json
```

### Evidence Metadata Template

For each evidence item, create metadata:

```json
{
  "id": "E001",
  "title": "Dependency Vulnerability Scan",
  "type": "security-scan",
  "tool": "npm audit",
  "date": "2026-06-04",
  "collector": "Auditor Name",
  "system": "System Name v1.0.0",
  "checklist_item": "Development P0 - Dependency Scanning",
  "format": "JSON",
  "location": "audit-evidence/scans/dependency/npm-audit.json",
  "retention": "3 years",
  "environment": "staging",
  "tool_version": "npm audit 8.0.0",
  "configuration": "audit-level=high, include=dev",
  "related_evidence": [],
  "review_status": "collected",
  "reviewed_by": null,
  "review_date": null
}
```

## Stakeholder Communication

### Stakeholder Identification

Identify all stakeholders:

| Stakeholder | Role | Contact | Involvement Level |
|-------------|------|---------|-------------------|
| Tech Lead | Technical decision maker | [email] | High |
| Security Team | Security controls | [email] | High |
| DevOps/Operations | Infrastructure and deployment | [email] | Medium |
| Product Owner | Business requirements | [email] | Medium |
| Compliance Officer | Regulatory requirements | [email] | Medium |
| Development Team | Implementation details | [email] | Medium |

### Communication Plan

**Pre-Audit Communication**
- Notify stakeholders of upcoming audit
- Request access to systems and documentation
- Schedule interviews or meetings
- Provide timeline and scope

**During-Audit Communication**
- Provide regular status updates
- Request additional information as needed
- Clarify findings with stakeholders

**Post-Audit Communication**
- Present findings to stakeholders
- Discuss remediation plans
- Obtain commitment for fixes
- Schedule follow-up

## Access and Permissions

### Required Access

**Code Repository**
- [ ] Read access to all code repositories
- [ ] Access to git history
- [ ] Access to pull requests and code reviews

**Infrastructure**
- [ ] Read access to infrastructure as code (Terraform, CloudFormation, etc.)
- [ ] Access to deployment configurations
- [ ] Access to monitoring dashboards (read-only)

**Documentation**
- [ ] Access to all documentation repositories
- [ ] Access to runbooks and procedures
- [ ] Access to architecture diagrams

**Testing**
- [ ] Access to test repositories
- [ ] Access to test results and reports
- [ ] Access to test environments

**Security**
- [ ] Access to security scan results
- [ ] Access to vulnerability reports
- [ ] Access to security policies

### Access Request Template

```
ACCESS REQUEST FOR AUDIT
=========================
Requester: [Auditor Name]
Date: YYYY-MM-DD
System: [System Name]

Required Access
---------------
1. Repository: [repo-name]
   - URL: [repository URL]
   - Access level: Read
   - Reason: Code review for audit

2. Infrastructure: [infra-repo-name]
   - URL: [repository URL]
   - Access level: Read
   - Reason: Infrastructure review for audit

3. Monitoring: [monitoring-tool]
   - URL: [dashboard URL]
   - Access level: Read-only
   - Reason: Review monitoring configuration

4. Documentation: [wiki/docs-repo]
   - URL: [URL]
   - Access level: Read
   - Reason: Review documentation

Timeline
--------
Start Date: YYYY-MM-DD
End Date: YYYY-MM-DD

Approval
--------
- [ ] Tech Lead: [Name] - [Date]
- [ ] Security Team: [Name] - [Date]
- [ ] Operations: [Name] - [Date]
```

## Audit Checklist Preparation

### Domain Checklist Preparation

For each selected domain, prepare the checklist:

**Core Domain**
- [ ] Model selection rationale documented
- [ ] Prompt design and validation performed
- [ ] System architecture documented
- [ ] Context window management implemented
- [ ] Token budget allocation defined

**Security Domain**
- [ ] Authentication implemented and tested
- [ ] Authorization implemented and tested
- [ ] Input validation implemented
- [ ] Output filtering implemented
- [ ] Rate limiting implemented
- [ ] Secret management implemented
- [ ] Audit logging implemented

**Data Domain**
- [ ] Data sourcing documented
- [ ] Data quality monitored
- [ ] Data validation implemented
- [ ] Data encryption implemented
- [ ] Data retention policies defined
- [ ] Privacy impact assessment completed

**Integration Domain**
- [ ] API contracts defined and versioned
- [ ] Backward compatibility maintained
- [ ] Timeouts configured
- [ ] Retry logic implemented
- [ ] Circuit breakers implemented
- [ ] Fallback behavior defined

**Development Domain**
- [ ] Code quality standards defined
- [ ] Error handling implemented
- [ ] Resource management implemented
- [ ] Code review process followed
- [ ] Technical debt managed

**Testing Domain**
- [ ] Unit tests implemented
- [ ] Integration tests implemented
- [ ] Test coverage > 80% for critical paths
- [ ] Performance tests performed
- [ ] Security tests performed
- [ ] Model evaluation performed (if applicable)

**Operations Domain**
- [ ] Deployment strategy defined
- [ ] Rollback capability tested
- [ ] Monitoring and alerting configured
- [ ] Health checks implemented
- [ ] Incident response plan exists
- [ ] Backup and recovery tested

**Documentation Domain**
- [ ] API documentation complete
- [ ] Runbooks exist for critical operations
- [ ] Architecture documentation exists
- [ ] User documentation complete
- [ ] Code documentation complete
- [ ] Changelog maintained

**Performance Domain**
- [ ] Latency requirements defined and met
- [ ] Throughput requirements defined and met
- [ ] Resource utilization monitored
- [ ] Scalability tested
- [ ] Caching strategy defined
- [ ] Cost monitoring implemented

**Compliance Domain**
- [ ] Regulatory requirements identified
- [ ] Audit trail implemented
- [ ] Data governance policies exist
- [ ] Privacy protection implemented
- [ ] Compliance testing performed

## Interview Preparation

### Stakeholder Interview Questions

**Developers**
- What is the development process?
- How is code review conducted?
- What testing practices are followed?
- How are deployments performed?
- What are the known technical challenges?
- What is the technical debt situation?
- How is security handled in the development process?

**Operators**
- What is the deployment process?
- How is monitoring and alerting configured?
- What is the incident response process?
- How are backups performed and tested?
- What is the disaster recovery plan?
- What are the common operational issues?
- How is capacity planning handled?

**Security Team**
- What security controls are in place?
- How are vulnerabilities managed?
- What is the incident response process?
- What compliance requirements apply?
- How is access control managed?
- How is security training handled?
- What are the current security concerns?

**Product Owners**
- What are the business requirements?
- What is the user impact?
- What are the compliance requirements?
- What is the risk tolerance?
- What are the business continuity requirements?
- What are the data handling requirements?

## Risk Assessment Preparation

### Risk Identification

Identify potential risks before the audit:

**Technical Risks**
- Outdated dependencies
- Unpatched systems
- Technical debt
- Single points of failure
- Lack of monitoring

**Security Risks**
- Authentication/authorization bypass
- Injection vulnerabilities
- Data exposure
- Credential exposure
- Insufficient logging

**Operational Risks**
- No rollback capability
- No incident response plan
- Untested backups
- Lack of monitoring
- Manual deployment processes

**Compliance Risks**
- Missing audit trails
- Incomplete documentation
- Privacy violations
- Data retention issues
- Regulatory non-compliance

### Risk Mitigation Planning

For each identified risk:

1. **Describe the risk**
2. **Assess likelihood and impact**
3. **Identify current mitigations**
4. **Identify additional mitigations needed**
5. **Assign owner and timeline**

## Final Preparation Checklist

### One Week Before Audit

- [ ] System type and risk tier documented
- [ ] Applicable domains selected
- [ ] Audit scope defined
- [ ] Audit depth determined
- [ ] Audit tools installed and configured
- [ ] Evidence workspace created
- [ ] Stakeholders notified
- [ ] Access requests submitted
- [ ] Previous audit findings reviewed
- [ ] Audit schedule confirmed

### One Day Before Audit

- [ ] All tools tested and working
- [ ] Access confirmed
- [ ] Evidence workspace ready
- [ ] Checklist prepared
- [ ] Interview schedule confirmed
- [ ] Audit plan reviewed
- [ ] Team briefed (if applicable)

### Day of Audit

- [ ] All tools accessible
- [ ] Evidence workspace accessible
- [ ] Checklist printed/available
- [ ] Interview schedule confirmed
- [ ] Note-taking tools ready
- [ ] Recording equipment ready (if permitted)
- [ ] Stakeholder contacts available

## Audit Best Practices

### During Preparation

1. **Start Early**: Begin preparation well in advance of the audit.
2. **Be Thorough**: Don't skip preparation steps.
3. **Document Everything**: Keep detailed notes of preparation activities.
4. **Verify Access**: Confirm all access is working before the audit.
5. **Test Tools**: Ensure all tools are working correctly.
6. **Communicate**: Keep stakeholders informed throughout preparation.

### During Audit

1. **Be Objective**: Base findings on evidence, not opinions.
2. **Be Systematic**: Follow the methodology consistently.
3. **Be Thorough**: Don't rush. Complete all steps.
4. **Be Constructive**: Frame findings as opportunities for improvement.
5. **Document Evidence**: Collect evidence for every finding.
6. **Ask Questions**: Clarify ambiguities with stakeholders.
7. **Take Notes**: Document everything during the audit.

### After Audit

1. **Review Thoroughly**: Review findings for accuracy and completeness.
2. **Get Feedback**: Share findings with stakeholders for validation.
3. **Present Clearly**: Present findings in a clear, actionable format.
4. **Follow Up**: Track remediation and verify fixes.
5. **Improve Process**: Learn from each audit and improve the process.

## Common Preparation Mistakes

### Mistake 1: Insufficient System Understanding

**Problem:** Starting the audit without understanding the system.

**Impact:** Missed findings, incorrect assumptions, wasted time.

**Solution:** Spend time understanding the system before auditing. Read documentation, talk to stakeholders, review architecture.

### Mistake 2: Incomplete Tool Setup

**Problem:** Tools not configured or not working properly.

**Impact:** Delays, incomplete scans, missed findings.

**Solution:** Test all tools before the audit. Verify configurations and outputs.

### Mistake 3: No Access to Systems

**Problem:** Cannot access necessary systems or data.

**Impact:** Incomplete audit, inability to verify findings.

**Solution:** Request access well in advance. Verify access before the audit.

### Mistake 4: Undefined Scope

**Problem:** Unclear what is in scope and out of scope.

**Impact:** Scope creep, missed areas, wasted effort.

**Solution:** Define scope clearly before starting. Document exclusions with rationale.

### Mistake 5: No Stakeholder Buy-in

**Problem:** Stakeholders not aware of or committed to the audit.

**Impact:** Lack of cooperation, findings ignored, no remediation.

**Solution:** Involve stakeholders early. Communicate the value of the audit. Obtain commitment for remediation.

## Preparation Templates

### Audit Plan Template

```
AUDIT PLAN
==========
System: [System Name]
Version: [Version]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]
Risk Tier: [Tier 1-4]
Audit Depth: [Quick/Standard/Deep]

System Type
-----------
[Description of system type and purpose]

Audit Objectives
----------------
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

Applicable Domains
------------------
1. [Domain]: [Rationale]
2. [Domain]: [Rationale]

Audit Scope
-----------
In Scope:
- [Item 1]
- [Item 2]

Out of Scope:
- [Item 1]: [Rationale]

Audit Methodology
-----------------
1. [Step 1]
2. [Step 2]
3. [Step 3]

Tools and Resources
-------------------
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

Stakeholders
------------
- [Stakeholder 1]: [Role, contact]
- [Stakeholder 2]: [Role, contact]

Timeline
--------
- [Date]: [Activity]
- [Date]: [Activity]

Deliverables
------------
- [Deliverable 1]
- [Deliverable 2]

Success Criteria
----------------
- [Criterion 1]
- [Criterion 2]

Risks and Mitigations
---------------------
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

Approval
--------
- [ ] Tech Lead: [Name, Date]
- [ ] Security: [Name, Date]
- [ ] Operations: [Name, Date]
```

### Access Request Template

```
ACCESS REQUEST
==============
System: [System Name]
Audit Period: [Start Date] - [End Date]
Requester: [Auditor Name]

Required Access
---------------
| System | Access Level | Purpose | Owner |
|--------|--------------|---------|-------|
| [System 1] | [Read/Write/Admin] | [Purpose] | [Owner] |
| [System 2] | [Read/Write/Admin] | [Purpose] | [Owner] |

Justification
-------------
[Why this access is needed for the audit]

Data Handling
-------------
- Sensitive data will be handled according to [policy]
- Access will be limited to audit period
- Access will be revoked after audit
- All data will be stored securely

Approvals
---------
- [ ] System Owner: [Name, Date]
- [ ] Security Team: [Name, Date]
- [ ] Data Protection Officer: [Name, Date] (if applicable)
```

### Stakeholder Communication Template

```
AUDIT NOTIFICATION
==================
To: [Stakeholders]
From: [Auditor Name]
Date: YYYY-MM-DD
Subject: Upcoming Audit of [System Name]

Overview
--------
We will be conducting an audit of [System Name] using the LLM & Agentic Rules Framework.

Audit Details
-------------
System: [System Name]
Audit Period: [Start Date] - [End Date]
Auditor: [Name]
Risk Tier: [Tier 1-4]

Scope
-----
[Brief description of audit scope]

Objectives
----------
- [Objective 1]
- [Objective 2]

Required Cooperation
--------------------
- Access to systems and documentation
- Availability for interviews
- Review of findings

Expected Outcomes
-----------------
- Identification of compliance gaps
- Recommendations for improvements
- Action plan for remediation

Contact
-------
Questions: [Contact information]

Timeline
--------
- [Date]: Audit begins
- [Date]: Interviews scheduled
- [Date]: Draft findings shared
- [Date]: Final report delivered
```
