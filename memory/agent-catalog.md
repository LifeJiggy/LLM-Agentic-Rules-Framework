# Agent Catalog - Comprehensive Reference

## Overview

The LLM & Agentic Rules Framework defines 12 specialized agents that operate across the AI system lifecycle. Each agent has defined roles, responsibilities, inputs, outputs, and interaction patterns.

## Agent Directory

| Agent | Role | Primary Phase | Key Outputs |
|-------|------|---------------|-------------|
| Rules Architect | Design systems using framework rules | Design | Domain map, ADRs, implementation plan |
| Rules Implementer | Implement system changes | Implementation | Code, prompts, tools, tests |
| Rules Reviewer | Review artifacts against framework | Review | Findings, release recommendation |
| Rules Release Gate | Decide release readiness | Release | Release decision, blocking items |
| Rules Eval | Run and interpret evaluations | Evaluation | Evaluation reports, regression detection |
| Rules Compliance Auditor | Assemble compliance evidence | Compliance | Evidence packages, audit readiness |
| Rules Data Steward | Own data governance | Data Governance | Data policies, inventory, retention |
| Rules Enforcer | Enforce policy rules | Enforcement | Policy enforcement, violation detection |
| Rules Documentation | Maintain documentation | Documentation | System docs, registers, runbooks |
| Rules Tracker | Track metrics and health | Operations | Metrics, dashboards, alerts |
| Rules Orchestrator | Coordinate multi-agent workflows | Coordination | Workflow execution, conflict resolution |
| Rules Security | Define and verify security controls | Security | Security architecture, threat models |

## Agent Details

### Rules Architect Agent

**File**: `agents/rules-architect.md`
**Role**: Design AI, LLM, agentic, RAG, MCP, and coding-agent systems using the framework's domain rules.

**Operating Model**:
- Design-stage advisor
- Does not modify implementations
- Defines what must be built and why
- Output feeds into implementation, compliance, and review

**Scope**:
- Single-turn LLM endpoints
- Multi-turn conversational systems
- Tool-using and agentic workflows
- Retrieval-augmented generation systems
- Multi-provider routing systems
- Coding-agent services
- MCP-integrated components
- Hybrid multi-agent architectures
- Real-time streaming systems
- Batch processing pipelines
- Evaluation and red-teaming infrastructure
- Compliance-as-code systems

**Design Inputs**:
- Business goal or user need
- Target user segment
- Risk sensitivity guide
- Data sources and types
- Deployment environment
- Regulatory context
- Model family preferences
- Budget and performance targets
- Authentication and authorization expectations
- Tool and integration inventory
- Failure tolerance and fallback policy
- Expected query patterns and volume
- Language and localization requirements
- Accessibility requirements
- Monitoring and observability expectations
- Disaster recovery and business continuity requirements

**Design Workflow**:
1. Gather system context and constraints
2. Select applicable framework domains
3. Map user flows and data flows
4. Identify risks and risk tiers
5. Define architecture decisions and rationale
6. Identify control requirements by tier
7. Define release and evidence checklist
8. Record architectural decision records (ADRs)
9. Hand off output to implementation, compliance, and review agents
10. Schedule design review gates

**Outputs**:
- Domain map
- Architecture decision record
- Implementation plan
- Release and evidence checklist
- Design review gate schedule and criteria
- Risk tier assignment with justification
- Control mapping with P0/P1 classification
- Evidence plan with retention requirements
- Exception register for design-phase exceptions
- Coordination plan with other agents and stakeholders

**Interactions**:
- Rules Release Gate Agent: hands off release gates and evidence expectations
- Rules Reviewer Agent: provides review criteria and control descriptions
- Rules Implementer Agent: provides architecture context for implementation
- Rules Eval Agent: provides evaluation requirements and thresholds
- Rules Compliance Auditor: provides compliance obligations and evidence requirements
- Rules Data Steward: provides data governance requirements and flows
- Rules Enforcer Agent: provides policy enforcement requirements
- Rules Documentation Agent: provides documentation requirements
- Rules Tracker Agent: provides metrics and monitoring requirements
- Rules Security Agent: provides security requirements and threat models

---

### Rules Implementer Agent

**File**: `agents/rules-implementer.md`
**Role**: Implement system changes according to architecture decisions, review findings, and framework domain rules.

**Operating Model**:
- Translates approved design decisions into concrete implementation tasks
- Coordinates with code, prompts, tools, tests, and deployment
- Preserves traceability to architecture decisions and compliance requirements

**Scope**:
- Code changes across backend, frontend, and integration layers
- Prompt template creation, update, and versioning
- Tool schema and behavior implementation
- Retrieval index setup and update automation
- Evaluation harness and dataset integration
- Test authoring and CI pipeline updates
- Monitoring and alerting implementation
- Deployment pipeline and configuration management
- Documentation and register maintenance
- Secret and credential setup through approved channels
- Infrastructure as code and environment configuration
- Data pipeline and retention logic implementation
- Audit event emission and telemetry instrumentation
- Exception handling and compensation logic
- Vendor integration and contract enforcement
- Training hook and onboarding flow implementation
- Model and prompt versioning and rollback implementation
- MCP client and server integration and testing
- Circuit breaker and rate limiting implementation
- Feature flagging and progressive rollout implementation
- Human review workflow implementation and routing

**Implementation Inputs**:
- Architecture decision records or design brief
- Framework domains and control requirements
- Implementation plan with component list and acceptance criteria
- Review findings and remediation instructions
- Release gate feedback and follow-up actions
- Evidence expectations and documentation requirements
- Existing system context and constraints
- Security, privacy, and performance guardrails
- Evaluation and testing requirements

**Outputs**:
- Implementation artifacts (code, prompts, configs)
- Test artifacts and coverage reports
- Documentation updates
- Evidence links and artifacts
- Implementation notes and decisions
- Remediation evidence for review findings

---

### Rules Reviewer Agent

**File**: `agents/rules-reviewer.md`
**Role**: Review code, prompts, tools, tests, and documentation against the framework.

**Operating Model**:
- Review-stage control
- Inspects artifacts against framework domain rules
- Produces prioritized findings with remediation guidance

**Review Scope**:
- Implementation code and libraries
- Prompt templates and prompt chains
- Tool definitions, schemas, and routing logic
- Retrieval configuration and indexes
- Evaluation code, datasets, and reports
- Test code, CI configuration, and automation
- Monitoring dashboards and alerting policies
- Runbooks, architecture diagrams, and registers
- Configuration files and secrets handling
- Data flows, pipelines, and retention logic
- APIs, integrations, and MCP boundaries
- Documentation and evidence links
- Vendor contracts, DPA references, and attestations
- Infrastructure as code and deployment manifests
- Logging and observability configuration
- Access control and IAM policies
- Network security groups and firewall rules
- Encryption and key management configuration
- Incident response runbooks and playbooks
- Training materials and onboarding documentation
- Exception register entries and risk acceptance records
- Monitoring and alerting thresholds and routing

**Review Depth Modes**:
- Quick: high-level scan, P0 and P1 gaps only
- Standard: structured review of implementation, tests, docs, evidence
- Deep: comprehensive audit over code, prompts, tools, retrieval, config, compliance, operations

**Finding Severity**:
- P0: blocking issue, must fix before release
- P1: serious issue, must fix within deadline
- P2: improvement, fix recommended but not blocking
- P3: informational, note for future refinement

**Outputs**:
- Findings ordered by severity and domain
- File or workflow references for each finding
- Required remediation with rationale
- Overall release recommendation
- Missing evidence summary
- Exception summary
- Vendor and supply chain gap summary

---

### Rules Release Gate Agent

**File**: `agents/rules-release-gate.md`
**Role**: Decide whether an AI system or agentic feature is ready to release.

**Operating Model**:
- Release-stage control
- Evaluates evidence against checklist and risk tier
- Produces release-ready verdict

**Scope**:
- New feature releases
- Model version upgrades
- Prompt template changes
- Retrieval index updates
- Tool or agent configuration changes
- Data source migrations
- Evaluation suite updates
- Deployment target or region changes
- Rollback or fallback path changes
- Human review workflow changes
- Authentication and authorization changes
- Monitoring and alerting changes
- Infrastructure or network changes
- Security patch releases
- Emergency hotfixes
- Experimental feature releases
- Rollback execution validation
- Canary and phased rollout sign-off
- Post-release compliance verification

**Release Categories**:
- Major: model version upgrade, new tool surface, new regulation rollout
- Minor: prompt change, retrieval update, model router change
- Patch: configuration change, monitoring update
- Emergency: hotfix, security patch, critical regulatory change
- Experimental: feature flag, A/B experiment, limited rollout
- Maintenance: schedule maintenance, dependency upgrade

**Decision Types**:
- Pass: all controls have evidence, release can proceed
- Conditional Pass: minor gaps accepted with follow-ups
- Block: missing or invalid evidence, release must not proceed

**Outputs**:
- Release decision: pass, conditional pass, or block
- Blocking items and required evidence
- Accepted risks and exception register entries
- Evidence links
- Follow-up owners and due dates
- Vendor and supply chain status summary
- Next review recommendation

---

### Rules Eval Agent

**File**: `agents/rules-eval.md`
**Role**: Run, maintain, and interpret evaluation suites for LLM, agentic, RAG, and MCP systems.

**Operating Model**:
- Manages full evaluation lifecycle
- Candidate selection, dataset maintenance, test execution
- Result interpretation, threshold enforcement, regression detection

**Evaluation Suites**:
- Core and capability performance
- Safety and toxicity
- Bias and fairness
- Prompt injection and jailbreak resistance
- Retrieval quality
- Tool use and agent behavior
- Performance and cost
- Regression and comparison
- Red-team and adversarial
- A/B experiment evaluation

**Outputs**:
- Evaluation reports with pass/fail status
- Regression detection and alerts
- Threshold enforcement decisions
- Coverage analysis
- Failure analysis and recommendations
- Evaluation metrics and trends

---

### Rules Compliance Auditor Agent

**File**: `agents/rules-compliance-auditor.md`
**Role**: Assemble, validate, and maintain compliance evidence across all framework domains.

**Operating Model**:
- Evidence and audit control for the framework
- Operates across system lifecycle
- Verifies controls are implemented and evidence collected

**Scope**:
- System design compliance review
- Implementation compliance verification
- Release evidence packaging and validation
- Production compliance monitoring
- Exception register and policy enforcement
- Vendor and supply chain compliance tracking
- Incident response compliance
- Audit trail completeness
- Legal and regulatory obligation mapping
- Training and awareness compliance
- Data governance and privacy compliance
- Retention and legal hold compliance
- Human oversight compliance
- Evidence archival and retention

**Outputs**:
- Compliance evidence packages
- Audit readiness assessments
- Exception register management
- Compliance metrics and reports
- Regulatory filing support
- Training compliance tracking

---

### Rules Data Steward Agent

**File**: `agents/rules-data-steward.md`
**Role**: Own data governance, privacy, quality, retention, legal hold, and data subject rights.

**Operating Model**:
- Data governance authority within the framework
- Defines data policies, validates data controls
- Manages data inventories, oversees retention

**Scope**:
- Data inventory and classification
- Data flow mapping and lineage
- PII minimization and masking
- Sensitive data handling
- Consent and legal basis management
- Retention and purging policies
- Legal hold enforcement
- Data quality checks
- Data subject request fulfillment
- Cross-border transfer controls
- Vendor data access and processing
- Audit logging for data events
- Data security and access controls
- Data breach response planning

**Outputs**:
- Data governance policies
- Data inventory and classification
- Retention schedules
- Legal hold records
- Data subject request tracking
- Data quality reports
- Cross-border transfer assessments

---

### Rules Enforcer Agent

**File**: `agents/rules-enforcer.md`
**Role**: Enforce policy rules, detect violations, and ensure continuous compliance monitoring.

**Operating Model**:
- Runtime control layer
- Monitors system behavior against policies
- Detects deviations, triggers alerts, enforces corrective actions

**Scope**:
- Runtime policy enforcement
- Real-time violation detection
- Automated corrective actions
- Policy rule management
- Violation logging and reporting
- Escalation triggers and workflows
- Compensating control activation
- Guardrail enforcement
- Input/output validation at runtime
- Rate limiting and quota enforcement
- Access control enforcement
- Data handling policy enforcement
- Model behavior boundary enforcement
- Tool permission enforcement
- Prompt injection detection
- Toxicity and safety filtering
- PII detection and masking
- Anomaly detection and alerting

**Outputs**:
- Real-time violation alerts
- Enforcement action logs
- Violation resolution reports
- Policy effectiveness analysis
- Compliance drift reports
- Anomaly detection reports

---

### Rules Documentation Agent

**File**: `agents/rules-documentation.md`
**Role**: Maintain documentation standards, knowledge sharing, and register management.

**Operating Model**:
- Documentation authority within the framework
- Defines documentation standards
- Maintains system registers and produces documentation artifacts

**Scope**:
- System documentation maintenance
- Model card creation and updates
- Prompt register management
- Tool catalog maintenance
- API documentation
- Architecture diagram updates
- Data flow documentation
- Runbook creation and maintenance
- Onboarding documentation
- Training materials
- Knowledge base maintenance
- Documentation review and approval
- Documentation versioning and accessibility

**Outputs**:
- System documentation
- Model cards
- Prompt registers
- Tool catalogs
- API documentation
- Runbooks
- Training materials
- Knowledge base articles

---

### Rules Tracker Agent

**File**: `agents/rules-tracker.md`
**Role**: Track metrics, monitoring, operational health, and performance indicators.

**Operating Model**:
- Observability and metrics authority
- Defines monitoring strategies, collects and analyzes metrics
- Maintains dashboards, generates operational reports

**Scope**:
- Metrics collection and aggregation
- Dashboard design and maintenance
- Alert rule configuration
- Operational health monitoring
- Performance tracking and trending
- Cost monitoring and attribution
- Incident tracking and analysis
- SLA and SLO monitoring
- Compliance metrics tracking
- User experience monitoring
- System behavior baseline
- Anomaly detection and alerting
- Reporting and analytics

**Outputs**:
- Real-time dashboards
- Operational reports
- Trend analysis
- Anomaly detection alerts
- Capacity planning data
- Cost analysis reports
- Compliance metrics
- Performance benchmarks

---

### Rules Orchestrator Agent

**File**: `agents/rules-orchestrator.md`
**Role**: Coordinate multi-agent workflows, manage agent interactions, ensure coherent execution.

**Operating Model**:
- Coordination layer for the agent system
- Manages workflow execution, handles inter-agent communication
- Resolves conflicts, ensures proper sequencing

**Scope**:
- Multi-agent workflow design
- Agent interaction management
- Workflow execution and monitoring
- Conflict resolution between agents
- Task sequencing and dependencies
- Resource allocation across agents
- Status tracking and reporting
- Error handling and recovery
- Workflow optimization
- Agent performance monitoring

**Workflow Types**:
- Design Workflow: Architect → Data Steward → Compliance → Security → Approval
- Implementation Workflow: Implementer → Documentation → Data Steward → Complete
- Review Workflow: Reviewer → Eval → Compliance → Report
- Release Workflow: Release Gate → Eval + Compliance + Tracker → Decision
- Operations Workflow: Tracker → Enforcer → Documentation → Resolution
- Full Lifecycle: Design → Implementation → Review → Release → Operations

**Outputs**:
- Workflow execution plans
- Agent coordination status
- Conflict resolution reports
- Workflow performance metrics
- Resource allocation reports
- Process improvement recommendations

---

### Rules Security Agent

**File**: `agents/rules-security.md`
**Role**: Define, implement, and verify security controls for AI systems.

**Operating Model**:
- Security authority within the framework
- Defines security policies, reviews security architecture
- Verifies security controls, conducts threat modeling

**Scope**:
- Security architecture review
- Threat modeling and risk assessment
- Authentication and authorization review
- Secret management verification
- Network security review
- Data security and encryption review
- Prompt injection defense
- Tool security boundary review
- API security review
- Incident response planning
- Vulnerability management
- Security testing coordination

**Outputs**:
- Threat models and risk assessments
- Security architecture reviews
- Security control recommendations
- Security review reports
- Vulnerability assessments
- Incident response plans
- Security metrics and reports

## Agent Interaction Matrix

| Agent | Architect | Implementer | Reviewer | Release Gate | Eval | Compliance | Data Steward | Enforcer | Documentation | Tracker | Orchestrator | Security |
|-------|-----------|-------------|----------|--------------|------|------------|--------------|----------|---------------|---------|--------------|----------|
| Architect | - | Provides context | Provides criteria | Hands off gates | Provides requirements | Provides obligations | Provides requirements | Provides policies | Provides requirements | Provides metrics | Receives tasks | Provides requirements |
| Implementer | Receives context | - | Receives findings | Receives feedback | Receives eval reqs | Receives compliance reqs | Receives data policies | Receives enforcement reqs | Coordinates updates | Receives metrics | Receives tasks | Receives security reqs |
| Reviewer | Receives criteria | Receives implementation | - | Produces findings | Coordinates eval | Coordinates compliance | Coordinates data | Receives enforcement | Receives documentation | Receives metrics | Receives tasks | Coordinates security |
| Release Gate | Receives gates | Receives implementation | Receives findings | - | Receives eval status | Receives evidence | Receives data evidence | Receives enforcement status | Receives documentation | Receives metrics | Receives tasks | Receives security evidence |
| Eval | Receives requirements | Receives implementation | Coordinates | Receives status | - | Receives compliance | Receives data policies | Receives enforcement | Receives documentation | Receives metrics | Receives tasks | Receives security |
| Compliance | Receives obligations | Receives compliance reqs | Coordinates | Coordinates | Receives compliance | - | Coordinates data | Receives enforcement | Receives documentation | Receives metrics | Receives tasks | Coordinates security |
| Data Steward | Receives requirements | Receives data policies | Coordinates | Receives evidence | Receives data policies | Coordinates | - | Receives enforcement | Receives documentation | Receives metrics | Receives tasks | Coordinates security |
| Enforcer | Receives policies | Receives enforcement reqs | Receives enforcement | Receives status | Receives enforcement | Receives enforcement | Receives enforcement | - | Receives documentation | Receives metrics | Receives tasks | Receives security |
| Documentation | Receives requirements | Coordinates | Receives documentation | Receives documentation | Receives documentation | Receives documentation | Receives documentation | Receives documentation | - | Receives metrics | Receives tasks | Receives documentation |
| Tracker | Receives metrics reqs | Receives metrics | Receives metrics | Receives metrics | Receives metrics | Receives metrics | Receives metrics | Receives metrics | Receives metrics | - | Receives tasks | Receives metrics |
| Orchestrator | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | Receives tasks | - | Receives tasks |
| Security | Receives requirements | Receives security reqs | Coordinates | Receives evidence | Receives security | Coordinates | Coordinates | Receives security | Receives documentation | Receives metrics | Receives tasks | - |

## Lifecycle Coverage

### Design Phase

**Primary Agent**: Rules Architect
**Supporting Agents**: Rules Eval, Rules Compliance Auditor, Rules Data Steward, Rules Security
**Key Activities**:
- System context gathering
- Domain selection and control mapping
- Risk tier assignment
- Architecture decision records
- Implementation planning
- Release and evidence checklist

### Implementation Phase

**Primary Agent**: Rules Implementer
**Supporting Agents**: Rules Documentation, Rules Data Steward
**Key Activities**:
- Code implementation
- Prompt template creation
- Tool integration
- Test authoring
- Documentation updates
- Evidence collection

### Review Phase

**Primary Agent**: Rules Reviewer
**Supporting Agents**: Rules Eval, Rules Compliance Auditor
**Key Activities**:
- Artifact inspection
- Finding documentation
- Remediation guidance
- Release recommendation
- Evidence validation

### Release Phase

**Primary Agent**: Rules Release Gate
**Supporting Agents**: Rules Compliance Auditor, Rules Eval, Rules Tracker
**Key Activities**:
- Evidence validation
- Control assessment
- Release decision
- Exception management
- Post-release scheduling

### Operations Phase

**Primary Agents**: Rules Tracker, Rules Enforcer
**Supporting Agents**: Rules Documentation
**Key Activities**:
- Monitoring and alerting
- Policy enforcement
- Incident response
- Runbook execution
- Metrics collection

### Continuous Improvement

**Primary Agent**: Rules Orchestrator
**Supporting Agents**: All agents
**Key Activities**:
- Workflow optimization
- Process improvement
- Framework updates
- Training and calibration
- Metrics analysis

## Agent Selection Guide

### By System Phase

| Phase | Required Agents | Optional Agents |
|-------|-----------------|-----------------|
| New system design | Architect | Security, Compliance, Data Steward |
| Feature implementation | Implementer | Documentation, Data Steward |
| Pre-release review | Reviewer | Eval, Compliance |
| Release decision | Release Gate | Compliance, Tracker |
| Production operations | Tracker, Enforcer | Documentation |
| Incident response | Tracker, Enforcer | Documentation, Orchestrator |
| Compliance audit | Compliance | All agents as needed |

### By Risk Tier

| Risk Tier | Minimum Agents | Recommended Agents |
|-----------|----------------|-------------------|
| Low | Architect, Implementer, Reviewer | Tracker |
| Medium | Architect, Implementer, Reviewer, Release Gate, Tracker | Compliance, Documentation |
| High | All 12 agents | All 12 agents |

### By System Type

| System Type | Primary Agents | Supporting Agents |
|-------------|----------------|-------------------|
| Customer-facing assistant | All 12 | - |
| Internal agent automation | Architect, Implementer, Reviewer, Tracker | Documentation |
| High-volume AI API | Architect, Implementer, Reviewer, Release Gate, Tracker, Security | Compliance |
| Healthcare AI | All 12 | - |
| Financial AI | All 12 | - |

## Agent Performance Metrics

### Individual Agent Metrics

| Agent | Key Metrics |
|-------|-------------|
| Architect | Design cycle time, ADR quality, control coverage |
| Implementer | Implementation velocity, code quality, test coverage |
| Reviewer | Review cycle time, finding accuracy, remediation rate |
| Release Gate | Decision time, block rate, post-release incidents |
| Eval | Evaluation coverage, threshold adherence, regression detection |
| Compliance | Evidence completeness, audit readiness, exception management |
| Data Steward | Data inventory accuracy, retention compliance, DSAR response time |
| Enforcer | Violation detection rate, false positive rate, response time |
| Documentation | Documentation coverage, currency, accessibility score |
| Tracker | Alert accuracy, dashboard uptime, metric freshness |
| Orchestrator | Workflow completion rate, conflict resolution time |
| Security | Vulnerability count, remediation time, control coverage |

### Team Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Agent utilization | 70-90% | Task tracking |
| Inter-agent communication latency | < 5 minutes | Message tracking |
| Workflow completion rate | > 95% | Workflow tracking |
| Conflict resolution time | < 2 hours | Conflict tracking |
| Error recovery time | < 30 minutes | Error tracking |
| Process improvement rate | > 1 per quarter | Improvement tracking |
