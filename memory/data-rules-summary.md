# Data Rules Summary - LLM & Agentic Rules Framework

## Overview

This document summarizes the data rules for LLM and agentic systems. The Data domain establishes requirements for data handling, privacy, governance, and quality throughout the AI system lifecycle.

## P0 Critical Rules

### DATA-001: Data Inventory Maintenance

**Rule**: Every AI system must maintain a current inventory of all data sources, types, and classifications.

**Why It Matters**: Without data inventory, organizations cannot assess data risks, enforce policies, or respond to data subject requests. Inventory is the foundation of data governance.

**Implementation Requirements**:
- Identify all data sources (databases, APIs, files, streams)
- Document data types and formats
- Classify data by sensitivity (public, internal, confidential, restricted)
- Assign data owners and stewards
- Document data flows and transformations
- Update inventory when data sources change
- Review inventory quarterly

**Data Inventory Fields**:
- Data source name and location
- Data type and format
- Sensitivity classification
- Data owner
- Data steward
- Retention period
- Legal basis for processing
- Cross-border transfers
- Third-party access

**Evidence Required**:
- Data inventory document
- Classification labels
- Owner assignments
- Review history

### DATA-002: Classification Labeling

**Rule**: All data processed by AI systems must be classified by sensitivity and labeled accordingly.

**Why It Matters**: Classification drives security controls, access policies, and handling requirements. Without classification, data may be over-protected (wasting resources) or under-protected (creating risk).

**Classification Levels**:
- Public: Freely available, no access restrictions
- Internal: Employee access only, basic controls
- Confidential: Restricted access, encryption, logging
- Highly Restricted: Strong encryption, MFA, audit, legal review

**Implementation Requirements**:
- Define classification schema
- Apply labels to all data sources
- Implement label-based access controls
- Monitor classification compliance
- Review classifications periodically
- Handle classification changes

**Evidence Required**:
- Classification schema
- Labeling records
- Access control configuration
- Compliance monitoring results

### DATA-003: Retention Policy Enforcement

**Rule**: Data retention policies must be defined and enforced for all data processed by AI systems.

**Why It Matters**: Retaining data longer than necessary increases risk and cost. Failing to retain data long enough violates legal requirements. Automated enforcement ensures consistency.

**Implementation Requirements**:
- Define retention periods by data type and regulation
- Implement automated retention enforcement
- Support legal hold to suspend deletion
- Document retention exceptions
- Audit retention compliance
- Handle cross-border retention requirements

**Retention Periods by Regulation**:
- GDPR: Purpose limitation, delete when no longer needed
- HIPAA: 6 years from creation or last effective date
- PCI DSS: 1 year for audit logs, 3 years for other records
- SOC 2: 7 years for audit evidence
- CCPA: Delete on request unless exception applies

**Evidence Required**:
- Retention policy document
- Retention configuration
- Legal hold records
- Retention audit results

### DATA-004: Consent Management

**Rule**: Systems processing personal data must implement consent management where required by regulation.

**Why It Matters**: Many regulations require consent for personal data processing. Without consent management, organizations cannot demonstrate lawful basis for processing.

**Implementation Requirements**:
- Identify consent requirements by jurisdiction
- Implement consent collection and recording
- Support consent withdrawal
- Respect consent preferences in processing
- Document consent evidence
- Handle consent renewal

**Consent Requirements by Regulation**:
- GDPR: Consent must be freely given, specific, informed, unambiguous
- CCPA: Right to opt-out of sale of personal information
- HIPAA: Authorization for uses beyond treatment, payment, healthcare operations
- COPPA: Verifiable parental consent for children under 13

**Evidence Required**:
- Consent collection mechanism
- Consent records
- Withdrawal handling
- Consent evidence for audits

## P1 High Priority Rules

### DATA-005: Data Minimization

**Rule**: AI systems must collect and process only the minimum data necessary for their intended purpose.

**Why It Matters**: Excessive data collection increases risk, cost, and compliance burden. Data minimization reduces attack surface and regulatory exposure.

**Implementation Requirements**:
- Define data requirements for each purpose
- Collect only required data fields
- Process only required data attributes
- Delete data when no longer needed
- Avoid secondary use without authorization
- Document data minimization decisions

**Evidence Required**:
- Data requirements documentation
- Minimization decisions
- Data flow diagrams showing minimization

### DATA-006: Encryption at Rest and in Transit

**Rule**: Confidential and restricted data must be encrypted at rest and in transit.

**Why It Matters**: Encryption protects data from unauthorized access even if other controls fail. It is a fundamental control for data protection.

**Implementation Requirements**:
- Encrypt data at rest using AES-256 or equivalent
- Encrypt data in transit using TLS 1.2+
- Manage encryption keys securely
- Rotate encryption keys regularly
- Implement key access controls
- Document encryption configuration

**Encryption Standards**:
- At rest: AES-256-GCM
- In transit: TLS 1.2 or higher
- Key management: HSM or equivalent
- Key rotation: At least annually

**Evidence Required**:
- Encryption configuration
- Key management procedures
- Key rotation records
- Encryption verification tests

### DATA-007: Access Logging

**Rule**: All access to confidential and restricted data must be logged with sufficient detail for audit.

**Why It Matters**: Access logs provide evidence of data handling, enable incident investigation, and support compliance requirements.

**Implementation Requirements**:
- Log all data access events
- Include user identity, timestamp, action, and data accessed
- Protect log integrity
- Retain logs per compliance requirements
- Monitor access patterns for anomalies
- Review access logs regularly

**Access Log Fields**:
- User identity (who)
- Timestamp (when)
- Action (what)
- Data accessed (which data)
- Source (where from)
- Result (success/failure)

**Evidence Required**:
- Access logging configuration
- Sample access logs
- Log retention policy
- Access pattern monitoring

## P2 Medium Priority Rules

### DATA-008: Data Quality Validation

**Rule**: Data used for AI system training and operation must be validated for quality.

**Why It Matters**: Poor data quality leads to poor model performance, biased outputs, and unreliable results. Quality validation ensures data fitness for purpose.

**Implementation Requirements**:
- Define data quality metrics
- Implement quality validation checks
- Monitor data quality over time
- Alert on quality degradation
- Document quality issues and remediation
- Track quality improvements

**Data Quality Dimensions**:
- Accuracy: Data correctly represents reality
- Completeness: All required data is present
- Consistency: Data is consistent across sources
- Timeliness: Data is current and up-to-date
- Validity: Data conforms to defined formats

**Evidence Required**:
- Quality metrics definition
- Quality validation configuration
- Quality monitoring results
- Quality improvement actions

### DATA-009: Cross-Border Transfer Assessment

**Rule**: Data transfers across borders must be assessed for regulatory compliance.

**Why It Matters**: Many regulations restrict cross-border data transfers. Non-compliance can result in fines and legal action.

**Implementation Requirements**:
- Identify cross-border data flows
- Assess regulatory requirements for each jurisdiction
- Implement transfer mechanisms (SCCs, adequacy decisions)
- Document transfer assessments
- Monitor transfer compliance
- Handle regulatory changes

**Transfer Mechanisms**:
- Standard Contractual Clauses (SCCs)
- Binding Corporate Rules (BCRs)
- Adequacy decisions
- Explicit consent
- Contractual necessity

**Evidence Required**:
- Transfer assessment documentation
- Transfer mechanism implementation
- Compliance monitoring results

### DATA-010: Data Lineage Tracking

**Rule**: Data transformations and lineage should be tracked to support audit and debugging.

**Why It Matters**: Data lineage provides visibility into how data flows through the system. It supports debugging, audit, and compliance requirements.

**Implementation Requirements**:
- Document data transformations
- Track data lineage through the system
- Maintain transformation history
- Support lineage queries
- Document lineage for audit
- Handle lineage for derived data

**Evidence Required**:
- Lineage documentation
- Transformation logs
- Lineage query capability

## Data Governance Framework

### Data Governance Roles

| Role | Responsibilities |
|------|------------------|
| Data Owner | Accountable for data quality, access, and compliance |
| Data Steward | Responsible for data management and policy enforcement |
| Data Custodian | Technical implementation of data controls |
| DPO | Oversight of data protection compliance |
| Legal | Legal basis and regulatory guidance |

### Data Governance Processes

| Process | Description | Frequency |
|---------|-------------|-----------|
| Data inventory review | Verify and update data inventory | Quarterly |
| Classification review | Verify data classification accuracy | Quarterly |
| Retention review | Verify retention enforcement | Monthly |
| Access review | Review data access permissions | Quarterly |
| Quality review | Review data quality metrics | Monthly |
| Transfer review | Review cross-border transfers | Quarterly |

## Data Anti-Patterns

### Excessive Data Collection

**Anti-Pattern**: Collecting more data than necessary for the intended purpose.

**Why It Fails**: Increases risk, cost, and compliance burden. Violates data minimization principle.

**Correct Approach**: Define data requirements for each purpose. Collect only required fields. Review collection practices regularly.

### Missing Data Classification

**Anti-Pattern**: Processing data without classification or with incorrect classification.

**Why It Fails**: Without classification, appropriate controls cannot be applied. Data may be over-protected or under-protected.

**Correct Approach**: Classify all data by sensitivity. Apply labels consistently. Implement label-based controls.

### Ungoverned Data Retention

**Anti-Pattern**: Retaining data indefinitely without policy or enforcement.

**Why It Fails**: Increases risk and cost. May violate regulations requiring deletion. Makes data subject requests difficult.

**Correct Approach**: Define retention periods by data type and regulation. Implement automated enforcement. Support legal hold.

### Missing Consent Records

**Anti-Pattern**: Processing personal data without consent records or with inadequate consent.

**Why It Fails**: Violates consent requirements. Cannot demonstrate lawful basis. May result in fines and legal action.

**Correct Approach**: Implement consent collection and recording. Support consent withdrawal. Document consent evidence.

## Data Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Data inventory completeness | 100% | Inventory audit |
| Classification accuracy | > 95% | Classification audit |
| Retention compliance | 100% | Automated checks |
| Access logging coverage | 100% for confidential+ | Log audit |
| Encryption coverage | 100% for confidential+ | Configuration audit |
| Quality score | > 0.90 | Quality metrics |
| Transfer assessment completion | 100% | Assessment audit |
| Data subject request response time | < 30 days | Request tracking |

## Cross-Domain Dependencies

The Data domain interacts with other domains:

| Domain | Data Dependency | Interaction |
|--------|-----------------|-------------|
| Core | DATA-001, DATA-002 | Inventory and classification inform core design |
| Security | DATA-004, DATA-006 | Consent and encryption require security controls |
| Integration | DATA-009 | Cross-border transfers affect integrations |
| Operations | DATA-003, DATA-007 | Retention and logging are operational |
| Testing | DATA-008 | Quality validation is a testing activity |
| Documentation | DATA-001, DATA-002 | Inventory and classification require documentation |
| Performance | DATA-008 | Quality affects performance |
| Compliance | DATA-001, DATA-003, DATA-004 | Inventory, retention, and consent support compliance |

## References

- Data domain fundamentals: `domains/04-data/fundamentals.md`
- Data domain best practices: `domains/04-data/best-practices.md`
- Data domain anti-patterns: `domains/04-data/anti-patterns.md`
- Data domain checklist: `domains/04-data/checklist.md`
- Data domain examples: `domains/04-data/examples.md`
- Data domain troubleshooting: `domains/04-data/troubleshooting.md`
- Data domain advanced: `domains/04-data/advanced.md`
