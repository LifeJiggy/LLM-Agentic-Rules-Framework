# Audit Report Templates

Use these templates to generate consistent, comprehensive, and actionable audit reports for the LLM & Agentic Rules Framework.

## Template Philosophy

Good audit reports are:

- **Clear**: Easy to understand for both technical and non-technical stakeholders
- **Actionable**: Findings include concrete fixes with owners and timelines
- **Evidence-Based**: Every finding is backed by evidence
- **Structured**: Consistent format makes reports easy to navigate and compare
- **Comprehensive**: Cover all applicable domains and severity levels
- **Timely**: Delivered promptly after audit completion

## Report Types

### 1. Executive Summary Report

**Purpose:** High-level overview for leadership and stakeholders.

**Length:** 2-5 pages

**Audience:** Executives, product owners, project managers

**Content:**
- Overall compliance status
- Key findings summary
- Critical risks
- Top recommendations
- Next steps

### 2. Standard Audit Report

**Purpose:** Comprehensive audit findings for technical teams.

**Length:** 10-30 pages

**Audience:** Tech leads, engineers, security team, operations team

**Content:**
- Executive summary
- Detailed findings
- Evidence package
- Action plan
- Appendices with technical details

### 3. Compliance Audit Report

**Purpose:** Regulatory compliance assessment.

**Length:** 20-50 pages

**Audience:** Compliance officers, auditors, regulators

**Content:**
- Regulatory requirement mapping
- Compliance status by requirement
- Evidence of compliance
- Gap analysis
- Remediation plan

### 4. Quick Audit Report

**Purpose:** Rapid assessment for pre-release checks.

**Length:** 2-5 pages

**Audience:** Development team, tech lead

**Content:**
- Findings summary
- Blocking issues
- Recommendations

## Template 1: Executive Summary Report

```
AUDIT EXECUTIVE SUMMARY
=======================

System: [System name and description]
Version: [Version]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]
Risk Tier: [Tier 1-4]
Audit Type: [Quick/Standard/Deep]

EXECUTIVE SUMMARY
-----------------
[2-3 paragraph summary of audit results, key findings, and recommendations]

OVERALL COMPLIANCE STATUS
--------------------------
[ ] APPROVED - All P0 and P1 gates passed, system is ready for production
[ ] CONDITIONAL - P0 passed, P1 findings accepted with documented rationale
[ ] BLOCKED - P0 or P1 findings unresolved, production deployment not recommended

FINDINGS SUMMARY
----------------
| Severity | Count | Status |
|----------|-------|--------|
| P0 (Critical) | [X] | [Resolved/Open/Blocking] |
| P1 (High) | [X] | [Resolved/Open/Accepted] |
| P2 (Medium) | [X] | [Open/Backlog] |
| P3 (Low) | [X] | [Open/Future] |

CRITICAL RISKS
--------------
1. **[Risk 1]:** [Brief description]
   - Impact: [High/Medium/Low]
   - Likelihood: [High/Medium/Low]
   - Mitigation: [Brief mitigation strategy]
   - Timeline: [Resolution timeline]

2. **[Risk 2]:** [Brief description]
   - Impact: [High/Medium/Low]
   - Likelihood: [High/Medium/Low]
   - Mitigation: [Brief mitigation strategy]
   - Timeline: [Resolution timeline]

TOP RECOMMENDATIONS
-------------------
1. **[Recommendation 1]:** [Brief description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]

2. **[Recommendation 2]:** [Brief description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]

NEXT STEPS
----------
1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]
3. [Action 3]: [Owner] - [Due date]

COMPLIANCE BY DOMAIN
--------------------
| Domain | P0 | P1 | P2 | Status |
|--------|----|----|-----|--------|
| Core | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Security | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Data | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Integration | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Development | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Testing | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Operations | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Documentation | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Performance | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |
| Compliance | [X] | [X] | [X] | [PASS/CONDITIONAL/FAIL] |

EVIDENCE SUMMARY
----------------
- Test results: [Available/Missing]
- Security scans: [Available/Missing]
- Performance benchmarks: [Available/Missing]
- Documentation: [Available/Missing]

APPENDIX
--------
- Full audit report: [Link]
- Evidence package: [Link]
- Raw scan results: [Link]

Report Prepared By: [Name]
Date: YYYY-MM-DD
Next Audit Date: YYYY-MM-DD
```

## Template 2: Standard Audit Report

```
STANDARD AUDIT REPORT
=====================

System Information
------------------
System Name: [System name]
System Description: [Brief description]
Version: [Version]
Environment: [Production/Staging/Development]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]
Audit Type: [Quick/Standard/Deep]
Risk Tier: [Tier 1-4]

EXECUTIVE SUMMARY
-----------------
[Comprehensive summary of audit results, including overall compliance status, key findings, critical risks, and top recommendations. 3-5 paragraphs.]

AUDIT SCOPE AND METHODOLOGY
----------------------------
Scope:
- [Component/system 1]
- [Component/system 2]
- [Component/system 3]

Out of Scope:
- [Excluded item 1]: [Rationale]
- [Excluded item 2]: [Rationale]

Methodology:
- Automated scanning (dependency check, secret scanning, SAST, linting, coverage)
- Manual code review
- Configuration review
- Infrastructure review
- Documentation review
- Stakeholder interviews (if applicable)

Domains Reviewed:
- [Domain 1]
- [Domain 2]
- ...

Tools Used:
- [Tool 1]: [Version]
- [Tool 2]: [Version]

SYSTEM OVERVIEW
---------------
[Description of the system, its purpose, architecture, key components, external dependencies, user base, deployment environment, and recent changes. Include architecture diagram if available.]

FINDINGS BY SEVERITY
---------------------

### P0 - Critical Findings (Block Production)

#### Finding P0.1: [Title]
- **Severity:** P0
- **Affected Component:** [File/component/workflow]
- **Domain:** [Domain name]
- **Violated Rule:** [Specific checklist item]
- **Production Risk:**
  - Impact: [Description of potential impact]
  - Likelihood: [High/Medium/Low]
  - Blast Radius: [Number of users/systems affected]
- **Evidence Gap:** [What evidence is missing]
- **Concrete Fix:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Required Evidence:** [What evidence is needed to verify fix]
- **Owner:** [Name/Role]
- **Due Date:** YYYY-MM-DD
- **Status:** [Open/In Progress/Fixed/Accepted/Deferred]

#### Finding P0.2: [Title]
[Same format as P0.1]

### P1 - High Findings (Requires Acceptance)

#### Finding P1.1: [Title]
[Same format as P0.1]

#### Finding P1.2: [Title]
[Same format as P0.1]

### P2 - Medium Findings (Should Address)

#### Finding P2.1: [Title]
[Same format as P0.1]

### P3 - Low Findings (Nice to Have)

#### Finding P3.1: [Title]
[Same format as P0.1]

FINDINGS BY DOMAIN
-------------------

### Core Domain
- P0: [X] findings
- P1: [X] findings
- P2: [X] findings
- P3: [X] findings
- Status: [PASS/CONDITIONAL/FAIL]

[Summary of core findings]

### Security Domain
[Same format as Core]

### Data Domain
[Same format as Core]

### Integration Domain
[Same format as Core]

### Development Domain
[Same format as Core]

### Testing Domain
[Same format as Core]

### Operations Domain
[Same format as Core]

### Documentation Domain
[Same format as Core]

### Performance Domain
[Same format as Core]

### Compliance Domain
[Same format as Core]

COMPLIANCE MATRIX
-----------------
| Domain | Checklist Item | Status | Evidence | Notes |
|--------|---------------|--------|----------|-------|
| Core | Model selection rationale | [PASS/FAIL/N/A] | [Available/Missing] | [Notes] |
| Core | Prompt design and validation | [PASS/FAIL/N/A] | [Available/Missing] | [Notes] |
| ... | ... | ... | ... | ... |

EVIDENCE PACKAGE
----------------
| Evidence ID | Description | Type | Location | Checklist Item | Date | Status |
|-------------|-------------|------|----------|----------------|------|--------|
| E001 | [Description] | [Test/Security/Config] | [Path] | [Checklist item] | [Date] | [Collected/Reviewed] |

EVIDENCE GAPS
-------------
| Gap ID | Checklist Item | Why Important | How to Collect | Owner | Due Date |
|--------|----------------|---------------|----------------|-------|----------|
| G001 | [Checklist item] | [Why needed] | [How to collect] | [Owner] | [Date] |

RECOMMENDATIONS
---------------
### Process Improvements
1. **[Recommendation]:** [Description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]
   - Owner: [Name]

### Tooling Improvements
1. **[Recommendation]:** [Description]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Expected Impact: [Impact description]
   - Owner: [Name]

### Training Needs
1. **[Training Need]:** [Description]
   - Priority: [High/Medium/Low]
   - Target Audience: [Team/Role]
   - Suggested Format: [Workshop/Documentation/Online course]

ACTION PLAN
-----------
| Priority | Action | Owner | Due Date | Dependencies | Status |
|----------|--------|-------|----------|--------------|--------|
| P0 | [Action 1] | [Owner] | [Date] | [Dependencies] | [Open/In Progress/Complete] |
| P1 | [Action 2] | [Owner] | [Date] | [Dependencies] | [Open/In Progress/Complete] |
| P2 | [Action 3] | [Owner] | [Date] | [Dependencies] | [Open/In Progress/Complete] |

APPENDICES
----------

### Appendix A: Raw Scan Results
[Links to or summaries of raw scan results]

### Appendix B: Configuration Snapshots
[Links to or summaries of configuration files]

### Appendix C: Interview Notes
[Summary of stakeholder interviews]

### Appendix D: Technical Details
[Additional technical details, diagrams, etc.]

### Appendix E: Glossary
- **P0:** Critical finding that blocks production
- **P1:** High finding requiring explicit acceptance
- **P2:** Medium finding that should be addressed
- **P3:** Low finding that is nice to have
- [Other terms as needed]

Report Approved By: [Name/Role]
Date: YYYY-MM-DD
Distribution: [List of recipients]
Next Audit Date: YYYY-MM-DD
```

## Template 3: Compliance Audit Report

```
COMPLIANCE AUDIT REPORT
=======================

Regulatory Framework: [GDPR/HIPAA/PCI/SOX/etc.]
System: [System name]
Version: [Version]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]
Compliance Officer: [Name/Role]

EXECUTIVE SUMMARY
-----------------
[Summary of compliance status, key findings, and recommendations]

COMPLIANCE STATUS
-----------------
Overall Status: [COMPLIANT / NON-COMPLIANT / CONDITIONALLY COMPLIANT]

| Regulation | Requirement | Status | Evidence | Gap | Remediation |
|-----------|-------------|--------|----------|-----|-------------|
| [Reg 1] | [Requirement 1] | [Compliant/Non-compliant] | [Evidence] | [Gap description] | [Remediation plan] |
| [Reg 1] | [Requirement 2] | [Compliant/Non-compliant] | [Evidence] | [Gap description] | [Remediation plan] |

REGULATORY REQUIREMENT MAPPING
------------------------------

### [Regulation 1]: [Name]

**Applicability:**
[Description of why this regulation applies]

**Requirements:**
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

**Compliance Status:**
[Compliant/Non-compliant/Conditionally compliant]

**Evidence:**
- [Evidence 1]
- [Evidence 2]

**Gaps:**
- [Gap 1]: [Description, impact, remediation]
- [Gap 2]: [Description, impact, remediation]

### [Regulation 2]: [Name]
[Same format as Regulation 1]

COMPLIANCE FINDINGS
-------------------

### Finding C-001: [Title]
- **Severity:** P0/P1/P2/P3
- **Regulation:** [Applicable regulation]
- **Requirement:** [Specific requirement]
- **Finding:** [Description of non-compliance]
- **Evidence:** [Evidence of non-compliance]
- **Risk:** [Regulatory and business risk]
- **Remediation:**
  1. [Step 1]
  2. [Step 2]
- **Owner:** [Name]
- **Due Date:** [Date]
- **Status:** [Open/In Progress/Complete]

EVIDENCE OF COMPLIANCE
----------------------

### Authentication and Access Control
- [Evidence item 1]
- [Evidence item 2]

### Data Protection
- [Evidence item 1]
- [Evidence item 2]

### Audit Trail
- [Evidence item 1]
- [Evidence item 2]

### Data Retention
- [Evidence item 1]
- [Evidence item 2]

### Privacy Protection
- [Evidence item 1]
- [Evidence item 2]

REMEDIATION PLAN
----------------

### Immediate Actions (P0)
1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]

### Short-term Actions (P1)
1. [Action 1]: [Owner] - [Due date]
2. [Action 2]: [Owner] - [Due date]

### Long-term Actions (P2/P3)
1. [Action 1]: [Owner] - [Due date]

COMPLIANCE ATTESTATION
----------------------

We attest that the findings in this report are accurate and complete to the best of our knowledge.

Auditor: [Name]
Date: YYYY-MM-DD

Compliance Officer: [Name]
Date: YYYY-MM-DD

Technical Lead: [Name]
Date: YYYY-MM-DD

Report Distribution:
- [Recipient 1]
- [Recipient 2]
- [Recipient 3]

Next Compliance Audit: YYYY-MM-DD
```

## Template 4: Quick Audit Report

```
QUICK AUDIT REPORT
==================
System: [System name]
Audit Date: YYYY-MM-DD
Auditor: [Name/Role]

OVERALL STATUS: [PASS / CONDITIONAL / FAIL]

BLOCKING ISSUES (P0)
--------------------
| # | Finding | Location | Fix | Owner |
|---|---------|----------|-----|-------|
| 1 | [Finding] | [Location] | [Fix] | [Owner] |
| 2 | [Finding] | [Location] | [Fix] | [Owner] |

HIGH PRIORITY ISSUES (P1)
--------------------------
| # | Finding | Location | Fix | Owner |
|---|---------|----------|-----|-------|
| 1 | [Finding] | [Location] | [Fix] | [Owner] |
| 2 | [Finding] | [Location] | [Fix] | [Owner] |

RECOMMENDATIONS
---------------
1. [Recommendation 1]
2. [Recommendation 2]

NEXT STEPS
----------
1. [Next step 1]: [Owner] - [Due date]
2. [Next step 2]: [Owner] - [Due date]

Auditor: [Name]
Date: YYYY-MM-DD
```

## Template 5: Detailed Finding Report

```
DETAILED FINDING REPORT
=======================

Finding ID: [FIND-001]
Date Identified: YYYY-MM-DD
Auditor: [Name]

FINDING DETAILS
---------------
Title: [Descriptive title]
Severity: [P0/P1/P2/P3]
Domain: [Core/Security/Data/etc.]
Checklist Item: [Specific checklist item]

AFFECTED COMPONENT
------------------
File(s): [File paths]
Component(s): [Component names]
Workflow(s): [Workflow descriptions]
Line Numbers: [If applicable]

VIOLATED RULE
-------------
Rule: [Rule name or description]
Framework Reference: [Link to framework documentation]
Checklist Reference: [Link to checklist item]

PRODUCTION RISK
---------------
Impact:
- User Impact: [Description]
- Data Impact: [Description]
- Financial Impact: [Description]
- Reputation Impact: [Description]
- Compliance Impact: [Description]

Likelihood: [High/Medium/Low]
Blast Radius: [Description of scope]
Current Mitigations: [Any existing mitigations]

EVIDENCE
--------
| Evidence ID | Description | Type | Location | Date Collected |
|-------------|-------------|------|----------|----------------|
| E001 | [Description] | [Screenshot/Log/Scan/etc.] | [Path] | [Date] |

Evidence Details:
[Detailed description of evidence]

EVIDENCE GAP
------------
Missing Evidence: [What evidence is missing]
Why Important: [Why this evidence matters]
How to Collect: [How to obtain this evidence]

ROOT CAUSE ANALYSIS
-------------------
Immediate Cause: [What directly caused this finding]
Root Cause: [Why the immediate cause exists]
Contributing Factors: [Other factors that contributed]
Systemic Issues: [Is this a one-time issue or systemic?]

CONCRETE FIX
------------
Description: [Detailed description of the fix]

Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Effort Estimate: [Hours/Days/Weeks]
Dependencies: [Any dependencies or blockers]
Risks: [Risks associated with the fix]

REQUIRED EVIDENCE
-----------------
Test: [What test is needed to verify the fix]
Documentation: [What documentation needs to be updated]
Verification: [How to verify the fix is complete]

REMEDIATION TRACKING
--------------------
Owner: [Name/Role]
Due Date: YYYY-MM-DD
Status: [Open/In Progress/Fixed/Accepted/Deferred]
Actual Completion Date: [Date if completed]

Notes:
[Any additional notes or updates]

RE-AUDIT
--------
Re-audit Date: YYYY-MM-DD
Re-audit Auditor: [Name]
Re-audit Result: [PASS/FAIL]
Re-audit Notes: [Notes from re-audit]

APPENDIX
--------
[Additional details, screenshots, logs, etc.]
```

## Template 6: Remediation Tracking Report

```
REMEDIATION TRACKING REPORT
============================
System: [System name]
Audit Date: YYYY-MM-DD
Report Date: YYYY-MM-DD
Report Prepared By: [Name]

REMEDIATION SUMMARY
-------------------
Total Findings: [X]
- P0 (Critical): [X] total, [X] resolved, [X] open
- P1 (High): [X] total, [X] resolved, [X] open
- P2 (Medium): [X] total, [X] resolved, [X] open
- P3 (Low): [X] total, [X] resolved, [X] open

Overall Progress: [X]% complete

REMEDIATION BY FINDING
----------------------

### P0 Findings

| Finding ID | Title | Owner | Due Date | Status | Notes |
|------------|-------|-------|----------|--------|-------|
| FIND-001 | [Title] | [Owner] | [Date] | [Status] | [Notes] |
| FIND-002 | [Title] | [Owner] | [Date] | [Status] | [Notes] |

### P1 Findings
[Same format as P0]

### P2 Findings
[Same format as P0]

### P3 Findings
[Same format as P0]

OVERDUE ITEMS
-------------
| Finding ID | Title | Owner | Due Date | Days Overdue | Status |
|------------|-------|-------|----------|--------------|--------|
| [ID] | [Title] | [Owner] | [Date] | [X] | [Status] |

BLOCKED ITEMS
-------------
| Finding ID | Title | Owner | Blocker | Expected Resolution |
|------------|-------|-------|---------|---------------------|
| [ID] | [Title] | [Owner] | [Blocker description] | [Date] |

RECENTLY COMPLETED
------------------
| Finding ID | Title | Owner | Completion Date | Verification |
|------------|-------|-------|-----------------|--------------|
| [ID] | [Title] | [Owner] | [Date] | [Verification status] |

UPCOMING DEADLINES
------------------
| Finding ID | Title | Owner | Due Date | Days Remaining |
|------------|-------|-------|----------|----------------|
| [ID] | [Title] | [Owner] | [Date] | [X] |

RISKS AND ISSUES
----------------
| Risk/Issue | Description | Impact | Mitigation | Owner |
|------------|-------------|--------|------------|-------|
| [Risk 1] | [Description] | [Impact] | [Mitigation] | [Owner] |

RECOMMENDATIONS
---------------
1. [Recommendation 1]
2. [Recommendation 2]

NEXT REPORT DATE: YYYY-MM-DD
Report Prepared By: [Name]
Approved By: [Name]
```

## Template 7: Audit Presentation Slides

```
SLIDE 1: Title Slide
====================
AUDIT RESULTS: [System Name]
[Date]

Auditor: [Name]
Risk Tier: [Tier 1-4]

SLIDE 2: Agenda
===============
1. Audit Overview
2. System Summary
3. Findings Summary
4. Critical Risks
5. Recommendations
6. Action Plan
7. Q&A

SLIDE 3: Audit Overview
=======================
- System: [Name]
- Audit Period: [Dates]
- Audit Type: [Quick/Standard/Deep]
- Domains Reviewed: [List]
- Overall Status: [APPROVED/CONDITIONAL/BLOCKED]

SLIDE 4: System Overview
========================
- System Type: [Type]
- Purpose: [Description]
- User Base: [Description]
- Architecture: [High-level diagram]
- Recent Changes: [Summary]

SLIDE 5: Findings Summary
=========================
| Severity | Count | Status |
|----------|-------|--------|
| P0 (Critical) | [X] | [Status] |
| P1 (High) | [X] | [Status] |
| P2 (Medium) | [X] | [Status] |
| P3 (Low) | [X] | [Status] |

SLIDE 6: P0 Findings
====================
- [Finding 1]: [Brief description]
  - Impact: [Impact description]
  - Fix: [Brief fix description]
  - Timeline: [Resolution timeline]

- [Finding 2]: [Brief description]
  - Impact: [Impact description]
  - Fix: [Brief fix description]
  - Timeline: [Resolution timeline]

SLIDE 7: P1 Findings
====================
- [Finding 1]: [Brief description]
  - Impact: [Impact description]
  - Fix: [Brief fix description]
  - Timeline: [Resolution timeline]

- [Finding 2]: [Brief description]
  - Impact: [Impact description]
  - Fix: [Brief fix description]
  - Timeline: [Resolution timeline]

SLIDE 8: Compliance by Domain
=============================
| Domain | Status |
|--------|--------|
| Core | [PASS/CONDITIONAL/FAIL] |
| Security | [PASS/CONDITIONAL/FAIL] |
| Data | [PASS/CONDITIONAL/FAIL] |
| Integration | [PASS/CONDITIONAL/FAIL] |
| Development | [PASS/CONDITIONAL/FAIL] |
| Testing | [PASS/CONDITIONAL/FAIL] |
| Operations | [PASS/CONDITIONAL/FAIL] |
| Documentation | [PASS/CONDITIONAL/FAIL] |
| Performance | [PASS/CONDITIONAL/FAIL] |
| Compliance | [PASS/CONDITIONAL/FAIL] |

SLIDE 9: Critical Risks
=======================
1. [Risk 1]
   - Impact: [Description]
   - Mitigation: [Strategy]
   - Timeline: [Timeline]

2. [Risk 2]
   - Impact: [Description]
   - Mitigation: [Strategy]
   - Timeline: [Timeline]

SLIDE 10: Recommendations
=========================
1. [Recommendation 1]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Impact: [Impact description]

2. [Recommendation 2]
   - Priority: [High/Medium/Low]
   - Effort: [Estimated effort]
   - Impact: [Impact description]

SLIDE 11: Action Plan
=====================
| Priority | Action | Owner | Due Date |
|----------|--------|-------|----------|
| P0 | [Action 1] | [Owner] | [Date] |
| P1 | [Action 2] | [Owner] | [Date] |
| P2 | [Action 3] | [Owner] | [Date] |

SLIDE 12: Next Steps
====================
1. [Next step 1]
2. [Next step 2]
3. [Next step 3]

SLIDE 13: Q&A
=============
Questions?

Contact: [Contact information]

SLIDE 14: Appendix
==================
- Full Report: [Link]
- Evidence Package: [Link]
- Raw Scans: [Link]
```

## Report Writing Guidelines

### Writing Principles

**Be Clear and Concise**
- Use simple, direct language
- Avoid jargon unless necessary and defined
- Use bullet points instead of paragraphs
- Keep sentences short

**Be Specific**
- Include specific file paths, line numbers, and code examples
- Use exact terminology from the framework
- Provide concrete numbers and metrics
- Avoid vague language ("some issues", "a few problems")

**Be Actionable**
- Every finding must have a concrete fix
- Every fix must have an owner and due date
- Every recommendation must have expected impact
- Provide step-by-step instructions for fixes

**Be Evidence-Based**
- Every finding must have evidence
- Reference specific evidence for each finding
- Include evidence in the report or as appendices
- Don't make claims without evidence

**Be Organized**
- Use consistent structure throughout
- Group related findings together
- Use headings, subheadings, and bullet points
- Include table of contents for long reports

### Writing Style

**Active Voice**
- Instead of: "It was observed that authentication was missing"
- Use: "Authentication is missing on API endpoints"

**Present Tense**
- Instead of: "There was no timeout on the API call"
- Use: "The API call has no timeout"

**Specific Language**
- Instead of: "The system has security issues"
- Use: "SQL injection vulnerability in user.php line 45"

**Objective Tone**
- Instead of: "The developers did a poor job"
- Use: "Error handling is incomplete in critical paths"

### Report Structure Best Practices

**Start with the Most Important Information**
- Put executive summary at the beginning
- Order findings by severity (P0 first)
- Put critical risks at the top

**Use Visual Hierarchy**
- Use headings and subheadings
- Use bullet points for lists
- Use tables for structured data
- Use bold for emphasis

**Include Context**
- Explain why each finding matters
- Describe the production risk
- Provide background information

**Provide Examples**
- Include code snippets for code-related findings
- Include screenshots for UI or configuration findings
- Include log excerpts for runtime findings

## Report Review and Approval

### Self-Review Checklist

Before finalizing the report:

- [ ] All P0/P1 findings have evidence
- [ ] All findings have concrete fixes
- [ ] All findings have owners assigned
- [ ] All evidence is linked to findings
- [ ] Report is free of typos and errors
- [ ] Report is consistent in formatting
- [ ] Report is appropriate for the audience
- [ ] Report is actionable

### Peer Review Checklist

Have a peer review the report:

- [ ] Findings are accurate and complete
- [ ] Severity assignments are appropriate
- [ ] Fixes are concrete and actionable
- [ ] Evidence supports findings
- [ ] Report is clear and well-organized
- [ ] No sensitive information exposed

### Stakeholder Review Checklist

Share with stakeholders for review:

- [ ] Technical findings are accurate
- [ ] Business impact is correctly assessed
- [ ] Recommendations are acceptable
- [ ] Action plan is realistic
- [ ] Owners and timelines are agreed upon

## Report Distribution

### Distribution List

**Executive Summary:**
- Executives (CTO, VP Engineering)
- Product owners
- Project managers

**Standard Audit Report:**
- Tech leads
- Engineering managers
- Security team
- Operations team
- Developers

**Compliance Audit Report:**
- Compliance officers
- Legal team
- Auditors
- Regulators (if required)

**Quick Audit Report:**
- Development team
- Tech lead
- Project manager

### Distribution Method

- Secure file sharing (encrypted if necessary)
- Version control repository
- Audit management system
- Email (for non-sensitive reports)

## Report Retention

### Retention Policy

- Executive summaries: 3 years
- Standard audit reports: 3 years
- Compliance audit reports: 7 years (or as required by regulation)
- Quick audit reports: 1 year

### Storage

- Store in secure, backed-up location
- Use consistent naming convention
- Include metadata (date, system, auditor)
- Maintain index of all reports

### Access Control

- Limit access to authorized personnel
- Protect sensitive findings
- Use encryption for sensitive reports
- Maintain audit trail of access
