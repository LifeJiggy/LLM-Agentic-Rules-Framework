# Core Rules Summary - LLM & Agentic Rules Framework

## Overview

This document summarizes the core rules for all LLM and agentic systems. The Core domain establishes foundational requirements that every AI system must meet regardless of risk tier or domain selection.

## Rule Priority Levels

| Priority | Meaning | Expected Handling |
|----------|---------|-------------------|
| P0 Critical | Security, safety, compliance, or data-loss risk | Required before production |
| P1 High | Reliability, quality, or maintainability risk | Required unless explicitly accepted |
| P2 Medium | Meaningful quality improvement | Adopt when practical |
| P3 Low | Helpful refinement | Backlog or opportunistic improvement |

## P0 Critical Rules

### CORE-001: System Ownership and Purpose

**Rule**: Every AI system must have a documented owner, clear purpose statement, and defined intended use cases.

**Why It Matters**: Without clear ownership, accountability for system behavior, incidents, and compliance is undefined. Without purpose documentation, scope creep and misuse become unmanageable.

**Implementation Requirements**:
- Document system owner with contact information
- Define intended use cases with specific boundaries
- Document prohibited use cases explicitly
- Define target user segments
- Identify regulatory jurisdictions
- Update documentation when system scope changes

**Evidence Required**:
- System register entry with owner and purpose
- Intended use documentation
- Prohibited use documentation
- Review date confirming currency

**Verification Method**:
- Check system register for completeness
- Verify documentation exists and is current
- Confirm owner acknowledgment of responsibilities

### CORE-002: Risk Tier Assignment

**Rule**: Every AI system must have a risk tier assigned based on intended use, data sensitivity, and potential for harm.

**Why It Matters**: Risk tier determines the level of controls, evidence, and review required. Without proper risk assessment, systems may be over-controlled (wasting resources) or under-controlled (creating unacceptable risk).

**Risk Tier Criteria**:
- Low: Internal productivity or assistance without user impact
- Medium: Customer-facing guidance or workflow automation with limited rights impact
- High: Decisions affecting rights, safety, finance, healthcare, legal status, or access to critical services
- Prohibited: Uses banned by law, policy, or contract

**Implementation Requirements**:
- Conduct risk assessment using standardized methodology
- Document risk tier with justification
- Review risk tier when system scope changes
- Review risk tier at least annually for high-risk systems
- Assign risk tier before production deployment

**Evidence Required**:
- Risk assessment document
- Risk tier assignment with justification
- Review history showing currency

### CORE-003: Human Review for High-Impact Actions

**Rule**: Systems making high-impact decisions must include human review before actions are executed.

**Why It Matters**: Automated decisions affecting rights, safety, or significant business impact require human oversight to prevent harm, ensure fairness, and maintain accountability.

**High-Impact Actions Include**:
- Financial transactions above defined thresholds
- Healthcare recommendations or triage
- Hiring or evaluation decisions
- Legal or compliance decisions
- Access control changes
- Data deletion or modification
- Public-facing content publication

**Implementation Requirements**:
- Identify all high-impact actions in system design
- Implement human review gates before execution
- Define review SLAs based on urgency
- Maintain audit trail of review decisions
- Handle reviewer unavailability with escalation paths

**Evidence Required**:
- Human review workflow configuration
- Review SLA documentation
- Audit trail of review decisions
- Escalation procedure documentation

### CORE-004: Fallback and Rollback Capability

**Rule**: Every AI system must have tested fallback mechanisms and documented rollback procedures.

**Why It Matters**: AI systems can fail in unpredictable ways. Without fallbacks, failures cause complete service disruption. Without rollback capability, problematic deployments cannot be quickly reversed.

**Implementation Requirements**:
- Define fallback behavior for each failure mode
- Implement automated fallback triggers
- Test fallback mechanisms regularly
- Document rollback procedures
- Test rollback in staging before production
- Define rollback triggers and decision authority
- Maintain rollback time estimates

**Evidence Required**:
- Fallback configuration documentation
- Rollback runbook
- Rollback test results
- Fallback activation logs

## P1 High Priority Rules

### CORE-005: Model Evaluation and Benchmarking

**Rule**: AI systems must have evaluation suites that measure performance, safety, and quality against defined thresholds.

**Why It Matters**: Without evaluation, system quality is unknown. Evaluation provides objective evidence of system capabilities and limitations, enabling informed release decisions.

**Implementation Requirements**:
- Define evaluation policy with suite selection
- Maintain evaluation datasets with versioning
- Run evaluation suite before each release
- Compare results against baselines and thresholds
- Document evaluation results and decisions
- Track evaluation metrics over time

**Evidence Required**:
- Evaluation policy document
- Evaluation dataset documentation
- Evaluation results with pass/fail status
- Threshold compliance evidence

### CORE-006: Prompt Version Control

**Rule**: All prompts used in production must be version-controlled with change history and review.

**Why It Matters**: Prompts define system behavior. Without version control, changes cannot be tracked, audited, or rolled back. Uncontrolled prompt changes can cause unexpected behavior or policy violations.

**Implementation Requirements**:
- Store prompts in version control system
- Document prompt purpose and context
- Review prompt changes before deployment
- Maintain change history with rationale
- Test prompt changes against evaluation suite
- Enable prompt rollback

**Evidence Required**:
- Prompt register with versions
- Change history with approvals
- Evaluation results for prompt changes

### CORE-007: Tool Permission Boundaries

**Rule**: All tools available to AI systems must have defined permission boundaries with least-privilege enforcement.

**Why It Matters**: Tools extend system capabilities but also extend attack surface. Without permission boundaries, tools can be misused for unauthorized actions, data exfiltration, or privilege escalation.

**Implementation Requirements**:
- Register all tools in tool catalog
- Define permission scope for each tool
- Implement least-privilege principle
- Require human approval for high-impact tools
- Audit all tool invocations
- Implement tool rate limiting

**Evidence Required**:
- Tool catalog with permission definitions
- Tool permission configuration
- Audit logs of tool invocations
- Human approval records for high-impact tools

### CORE-008: Audit Logging

**Rule**: All significant system actions must be logged with sufficient detail for forensic analysis and compliance.

**Why It Matters**: Audit logs provide evidence of system behavior, enable incident investigation, support compliance requirements, and deter misuse.

**Implementation Requirements**:
- Log all user interactions
- Log all model invocations
- Log all tool executions
- Log all access control decisions
- Log all configuration changes
- Include correlation IDs for request tracing
- Retain logs per compliance requirements
- Protect log integrity

**Evidence Required**:
- Logging configuration
- Log retention policy
- Sample logs showing required fields
- Log integrity verification

## P2 Medium Priority Rules

### CORE-009: Context Window Optimization

**Rule**: Systems should optimize context window usage to balance response quality with cost and latency.

**Why It Matters**: Context window limitations affect response quality. Inefficient context usage wastes tokens (increasing cost and latency) or omits important information (reducing quality).

**Implementation Requirements**:
- Monitor context window utilization
- Implement context prioritization
- Use retrieval augmentation where appropriate
- Optimize prompt structure for efficiency
- Track token usage metrics
- Balance context completeness with cost

**Evidence Required**:
- Context utilization metrics
- Optimization documentation
- Cost impact analysis

### CORE-010: Response Quality Monitoring

**Rule**: Systems should monitor response quality metrics to detect degradation and guide improvements.

**Why It Matters**: AI system quality can degrade over time due to model updates, data changes, or usage pattern shifts. Monitoring enables early detection and proactive improvement.

**Implementation Requirements**:
- Define quality metrics (accuracy, relevance, coherence)
- Implement quality sampling and scoring
- Track quality trends over time
- Alert on quality degradation
- Use quality data to guide improvements
- Report quality metrics to stakeholders

**Evidence Required**:
- Quality metrics definition
- Quality monitoring configuration
- Quality trend reports
- Improvement actions based on quality data

## Rule Implementation Checklist

### For New Systems

- [ ] CORE-001: Document system owner and purpose
- [ ] CORE-002: Assign risk tier with justification
- [ ] CORE-003: Implement human review for high-impact actions
- [ ] CORE-004: Implement fallback and rollback capability
- [ ] CORE-005: Set up evaluation suite
- [ ] CORE-006: Implement prompt version control
- [ ] CORE-007: Define tool permission boundaries
- [ ] CORE-008: Implement audit logging
- [ ] CORE-009: Optimize context window usage
- [ ] CORE-010: Set up response quality monitoring

### For Existing Systems

- [ ] Verify system ownership is documented
- [ ] Verify risk tier is assigned and current
- [ ] Verify human review is implemented for high-impact actions
- [ ] Verify fallback and rollback are tested
- [ ] Verify evaluation suite is running
- [ ] Verify prompts are version-controlled
- [ ] Verify tool permissions are defined
- [ ] Verify audit logging is comprehensive
- [ ] Verify context optimization is in place
- [ ] Verify quality monitoring is active

## Core Domain Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| System documentation complete | 100% | Documentation audit |
| Risk tier assigned | 100% | System register |
| Human review for high-risk | 100% | Workflow testing |
| Fallback tested | 100% | Test results |
| Evaluation suite passing | 100% | Evaluation reports |
| Prompts version controlled | 100% | Version control audit |
| Tool permissions defined | 100% | Tool catalog |
| Audit logging comprehensive | 100% | Log review |
| Context optimization active | > 80% utilization | Metrics |
| Quality monitoring active | 100% | Monitoring dashboard |

## Cross-Domain Dependencies

The Core domain provides foundational rules that impact all other domains:

| Domain | Core Dependency | Impact |
|--------|-----------------|--------|
| Security | CORE-001, CORE-002 | Ownership and risk tier inform security controls |
| Data | CORE-002, CORE-008 | Risk tier and audit logging support data governance |
| Integration | CORE-007 | Tool permissions inform integration security |
| Operations | CORE-004, CORE-008 | Fallback and logging support operations |
| Testing | CORE-005 | Evaluation requirements inform testing strategy |
| Documentation | CORE-001, CORE-006 | Ownership and prompts require documentation |
| Performance | CORE-009 | Context optimization impacts performance |
| Compliance | CORE-001, CORE-002, CORE-008 | Ownership, risk, and logging support compliance |

## Common Anti-Patterns

### Missing System Ownership

**Anti-Pattern**: System deployed without documented owner or contact information.

**Why It Fails**: No one is accountable for system behavior, incidents, or compliance. Issues go unresolved because responsibility is unclear.

**Correct Approach**: Document owner with contact information before deployment. Require owner acknowledgment of responsibilities.

### Undefined Risk Tier

**Anti-Pattern**: System deployed without risk tier assessment or with risk tier assigned after deployment.

**Why It Fails**: Without risk tier, appropriate controls cannot be determined. System may lack required controls or implement unnecessary ones.

**Correct Approach**: Conduct risk assessment during design phase. Assign risk tier before production deployment. Review when scope changes.

### Missing Human Review

**Anti-Pattern**: High-impact actions executed automatically without human oversight.

**Why It Fails**: Automated decisions can cause harm, bias, or legal liability without human judgment. Errors propagate without correction opportunity.

**Correct Approach**: Identify high-impact actions during design. Implement human review gates. Define review SLAs. Maintain audit trail.

### Untested Fallback

**Anti-Pattern**: Fallback mechanisms documented but never tested in realistic conditions.

**Why It Fails**: Untested fallbacks may not work when needed. Fallback activation during incidents may cause additional failures.

**Correct Approach**: Test fallback mechanisms regularly. Include fallback testing in evaluation suite. Verify fallback behavior under load.

### Uncontrolled Prompts

**Anti-Prompt**: Prompts modified directly in production without version control or review.

**Why It Fails**: Uncontrolled changes can cause unexpected behavior, policy violations, or quality degradation. Changes cannot be tracked or rolled back.

**Correct Approach**: Store prompts in version control. Review changes before deployment. Test against evaluation suite. Maintain change history.

## References

- Core domain fundamentals: `domains/01-core/fundamentals.md`
- Core domain best practices: `domains/01-core/best-practices.md`
- Core domain anti-patterns: `domains/01-core/anti-patterns.md`
- Core domain checklist: `domains/01-core/checklist.md`
- Core domain examples: `domains/01-core/examples.md`
- Core domain troubleshooting: `domains/01-core/troubleshooting.md`
- Core domain advanced: `domains/01-core/advanced.md`
