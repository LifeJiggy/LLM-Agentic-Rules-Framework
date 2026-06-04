# Domain Routing Guide

Use this guide to systematically select and apply the correct domain checklist packs for any LLM, agentic, or AI system task.

## Domain Routing Philosophy

Domain routing is the process of matching a task, system type, or change to the appropriate checklist domains. Proper routing ensures that all relevant quality gates are applied without wasting effort on irrelevant checks.

### Routing Principles

**Completeness**
- All applicable domains must be considered.
- Don't skip domains that seem "obvious" or "already covered."
- Consider indirect impacts across domains.

**Precision**
- Select the minimum set of domains that fully cover the task.
- Avoid loading unnecessary domains that add overhead.
- Balance thoroughness with efficiency.

**Context-Awareness**
- Consider the system's risk tier when selecting domains.
- Adjust domain depth based on criticality.
- Prioritize P0/P1 checks for high-risk systems.

**Traceability**
- Document why each domain was selected.
- Record which checklist items were applied.
- Maintain audit trail of domain routing decisions.

## The 10 Domains

### Overview

The LLM & Agentic Rules Framework consists of 10 domains, each covering a specific aspect of AI system quality:

| # | Domain | Focus | Primary Concern |
|---|--------|-------|-----------------|
| 1 | Core | Fundamental AI system requirements | Model selection, prompt engineering, system architecture |
| 2 | Security | Threat protection and access control | Authentication, authorization, injection prevention |
| 3 | Data | Data governance and privacy | Quality, sourcing, storage, retention, compliance |
| 4 | Integration | External system connectivity | APIs, protocols, compatibility, contracts |
| 5 | Development | Code quality and engineering practices | Design patterns, testing, code review |
| 6 | Testing | Validation and verification | Coverage, evaluation, red teaming, performance testing |
| 7 | Operations | Production reliability | Deployment, monitoring, incident response |
| 8 | Documentation | Knowledge management | API docs, runbooks, user guides |
| 9 | Performance | Efficiency and scalability | Latency, throughput, resource utilization |
| 10 | Compliance | Regulatory and legal requirements | Audit trails, data governance, privacy |

### Domain Dependencies

Domains are not independent—they interact and influence each other:

```
Core → Security (AI systems need security)
Core → Testing (AI systems need testing)
Core → Data (AI systems need data)
Security → Compliance (security enables compliance)
Data → Compliance (data governance enables compliance)
Operations → Testing (operations need testing)
Performance → Operations (performance affects operations)
All → Documentation (everything needs documentation)
```

## Routing Decision Tree

### Step 1: Identify System Type

**Questions to Ask:**
- Is this a new AI application or agent? → Core, Security, Data, Testing, Operations, Compliance
- Is this an integration with an external tool or service? → Core, Integration, Security, Operations, Testing
- Is this a RAG or knowledge-based system? → Core, Data, Security, Testing, Performance
- Is this a production release of any AI system? → Operations, Testing, Security, Compliance, Performance
- Is this a code review? → Development, Security, Testing, Documentation
- Is this an incident response or regression fix? → Operations, Troubleshooting, Testing, Performance
- Is this a regulated workflow (healthcare, finance, legal)? → Compliance, Data, Security, Documentation, Testing

### Step 2: Identify Change Type

**Questions to Ask:**
- Is this a model change (new model, model upgrade, fine-tuning)? → Core, Testing, Performance, Security
- Is this a prompt change (new prompt, prompt optimization, prompt template)? → Core, Security, Testing
- Is this a retrieval change (new data source, chunking strategy, embedding model)? → Core, Data, Testing, Performance
- Is this a tool change (new tool, tool modification, tool removal)? → Integration, Security, Testing, Operations
- Is this an infrastructure change (deployment, scaling, networking)? → Operations, Security, Performance
- Is this a data change (new dataset, data pipeline, data migration)? → Data, Security, Testing, Compliance

### Step 3: Identify Risk Tier

**Questions to Ask:**
- What is the potential impact of failure? (Data loss, security breach, user harm, financial loss)
- How many users are affected? (1, 10, 1,000, 1,000,000+)
- Is the system customer-facing or internal?
- Does the system handle regulated data (PHI, PII, financial)?
- What is the recovery time objective? (Minutes, hours, days)
- What is the blast radius? (Single user, team, organization, public)

**Risk Tier Assignment:**
- Tier 1 (Critical): Financial, healthcare, critical infrastructure
- Tier 2 (High): Customer-facing, high business impact
- Tier 3 (Medium): Internal tools, limited user base
- Tier 4 (Low): Experimental, prototypes, personal tools

### Step 4: Select Domains

Based on the answers above, select the appropriate domains:

**Primary Domains (Must Apply)**
- Domains directly related to the system type and change type.
- These are non-negotiable and must be fully applied.

**Secondary Domains (Should Apply)**
- Domains that are indirectly affected by the change.
- These should be reviewed but may not require full checklist application.

**Tertiary Domains (Consider)**
- Domains that might be relevant depending on implementation details.
- Review at a high level, apply specific checklist items if relevant.

## Routing by System Type

### New AI Application

**System Characteristics:**
- Greenfield development of an LLM-powered application
- No existing production deployment
- Multiple components: model, prompts, data, API, UI

**Primary Domains:**
1. **Core** (P0/P1)
   - Model selection and justification
   - Prompt design and validation
   - System architecture and design patterns
   - Context window management
   - Token budget allocation

2. **Security** (P0/P1)
   - Authentication and authorization
   - Input validation and sanitization
   - Output filtering and content moderation
   - Rate limiting and abuse prevention
   - API key and credential management

3. **Data** (P0/P1)
   - Data sourcing and quality
   - Data preprocessing and validation
   - Data storage and encryption
   - Data retention and deletion policies
   - Privacy impact assessment

4. **Testing** (P0/P1)
   - Unit tests for components
   - Integration tests for workflows
   - Evaluation framework for model outputs
   - Red teaming for safety
   - Performance and load testing

5. **Operations** (P0/P1)
   - Deployment strategy
   - Monitoring and observability
   - Health checks
   - Incident response procedures
   - Rollback capability

6. **Compliance** (P0/P1/P2)
   - Regulatory requirements assessment
   - Audit trail implementation
   - Data governance policies
   - Privacy policy alignment
   - Terms of service compliance

**Secondary Domains:**
- **Integration**: If integrating with external APIs or services
- **Performance**: If performance is a key requirement
- **Documentation**: If extensive user-facing documentation is needed

### Tool or MCP Integration

**System Characteristics:**
- Integrating external tools or services with an AI agent
- Tool invocation, parameter passing, result parsing
- Tool availability and reliability concerns

**Primary Domains:**
1. **Core** (P0/P1)
   - Tool interface design
   - Capability negotiation
   - Tool selection logic
   - Parameter validation
   - Result interpretation

2. **Integration** (P0/P1)
   - API contract definition
   - Versioning strategy
   - Backward compatibility
   - Timeout and retry configuration
   - Error handling and fallback

3. **Security** (P0/P1)
   - Tool access controls
   - Input sanitization
   - Output validation
   - Audit logging of tool calls
   - Sandboxing or isolation

4. **Operations** (P0/P1)
   - Tool health monitoring
   - Fallback strategies
   - Rate limiting
   - Circuit breakers
   - Alerting on tool failures

5. **Testing** (P0/P1)
   - Contract tests with tool providers
   - Integration tests for tool workflows
   - Failure simulation (tool unavailable, slow response, invalid output)
   - Chaos testing for tool resilience

**Secondary Domains:**
- **Core**: Prompt engineering for tool use
- **Security**: Prompt injection prevention via tool outputs
- **Data**: Data flow through tools
- **Performance**: Tool call latency optimization

### RAG or Knowledge System

**System Characteristics:**
- Retrieval-augmented generation system
- Knowledge base with documents, embeddings, vector store
- Retrieval, ranking, and generation pipeline

**Primary Domains:**
1. **Core** (P0/P1)
   - Retrieval architecture design
   - Chunking strategy
   - Embedding model selection
   - Ranking and filtering logic
   - Context window management
   - Generation prompt design

2. **Data** (P0/P1)
   - Knowledge base construction
   - Data quality and curation
   - Data freshness and update strategy
   - Indexing and storage
   - Data lineage and provenance
   - Privacy and access controls

3. **Security** (P0/P1)
   - Data access controls
   - Query filtering and sanitization
   - Injection prevention (retrieval-based attacks)
   - Sensitive data detection and filtering
   - Audit logging of retrievals

4. **Testing** (P0/P1)
   - Retrieval accuracy metrics
   - Relevance scoring validation
   - Hallucination detection
   - End-to-end evaluation
   - Adversarial testing

5. **Performance** (P0/P1)
   - Query latency optimization
   - Throughput scaling
   - Caching strategies
   - Index optimization
   - Embedding model performance

**Secondary Domains:**
- **Integration**: Vector database integration
- **Operations**: Monitoring retrieval quality
- **Compliance**: Data governance for knowledge base

### Production Release

**System Characteristics:**
- Deploying an AI system to production
- Can be any of the above system types
- Focus on safe, reliable deployment

**Primary Domains:**
1. **Operations** (P0/P1)
   - Deployment strategy (blue-green, canary, rolling)
   - Rollback plan and testing
   - Health checks and readiness probes
   - Monitoring and alerting
   - Incident response procedures
   - Change management process

2. **Testing** (P0/P1)
   - Regression test suite
   - Performance benchmarks
   - Load testing
   - Chaos testing
   - Canary analysis
   - Smoke tests

3. **Security** (P0/P1)
   - Security review
   - Vulnerability scanning
   - Penetration testing
   - Authentication and authorization verification
   - Data protection validation

4. **Compliance** (P0/P1/P2)
   - Regulatory requirements check
   - Audit evidence collection
   - Privacy impact assessment
   - Data retention compliance
   - Licensing compliance

5. **Performance** (P0/P1)
   - Performance benchmarks met
   - Load testing results
   - Capacity planning
   - Bottleneck analysis
   - Resource utilization optimization

**Secondary Domains:**
- **Core**: Final model validation
- **Data**: Data pipeline verification
- **Documentation**: Release notes and user communication

### Code Review

**System Characteristics:**
- Reviewing code changes for AI systems
- Can be any component: model code, prompt templates, data pipelines, etc.
- Focus on quality, security, and maintainability

**Primary Domains:**
1. **Development** (P0/P1)
   - Code quality and style
   - Design patterns and architecture
   - Code organization and modularity
   - Error handling completeness
   - Resource management

2. **Security** (P0/P1)
   - Security vulnerabilities
   - Injection risks (prompt, SQL, command)
   - Access control implementation
   - Sensitive data handling
   - Dependency vulnerabilities

3. **Testing** (P0/P1)
   - Test coverage
   - Test quality and relevance
   - Edge case coverage
   - Mock usage and realism
   - Test maintainability

4. **Documentation** (P0/P1/P2)
   - Code comments and docstrings
   - API documentation
   - Architecture diagrams
   - README and usage guides
   - Changelog updates

**Secondary Domains:**
- **Core**: AI-specific concerns (prompt design, model usage)
- **Operations**: Deployment and operational concerns
- **Performance**: Performance implications

### Incident or Regression

**System Characteristics:**
- Responding to production incidents or regressions
- Diagnosing and fixing issues
- Preventing recurrence

**Primary Domains:**
1. **Operations** (P0/P1)
   - Incident response procedures
   - Root cause analysis
   - Recovery procedures
   - Post-incident review
   - Runbook updates

2. **Troubleshooting** (P0/P1)
   - Debug procedures
   - Log analysis techniques
   - Metric correlation methods
   - Reproduction steps
   - Isolation of failure domains

3. **Testing** (P0/P1)
   - Regression test development
   - Reproduction test cases
   - Fix validation tests
   - Chaos testing for similar scenarios

4. **Performance** (P0/P1)
   - Performance impact assessment
   - Resource utilization analysis
   - Scalability implications
   - Bottleneck identification

**Secondary Domains:**
- **Security**: Security implications of the incident
- **Documentation**: Incident documentation and lessons learned
- **Core**: Model or prompt issues

### Regulated Workflow

**System Characteristics:**
- Systems subject to regulatory requirements
- Healthcare (HIPAA), finance (PCI/SOX), legal, government
- Strict audit and compliance requirements

**Primary Domains:**
1. **Compliance** (P0/P1)
   - Regulatory requirement mapping
   - Compliance control implementation
   - Audit trail completeness
   - Privacy impact assessment
   - Data governance policies

2. **Data** (P0/P1)
   - Data classification
   - Data retention policies
   - Data deletion procedures
   - Data encryption
   - Access logging and auditing

3. **Security** (P0/P1)
   - Access controls and authentication
   - Encryption (at rest and in transit)
   - Audit logging
   - Incident response for data breaches
   - Vulnerability management

4. **Documentation** (P0/P1)
   - Process documentation
   - Training materials
   - Audit evidence packages
   - Standard operating procedures
   - Change management records

5. **Testing** (P0/P1)
   - Validation testing
   - Compliance testing
   - Acceptance criteria
   - Audit test execution

**Secondary Domains:**
- **Core**: AI system functionality
- **Operations**: Operational procedures
- **Development**: Code quality and security

## Routing by Change Type

### Model Changes

**Change Types:**
- New model deployment
- Model upgrade (e.g., GPT-3.5 → GPT-4)
- Fine-tuning or custom model
- Model configuration changes

**Applicable Domains:**
- **Core** (P0): Model selection rationale, capability assessment, prompt compatibility
- **Testing** (P0): Model evaluation, regression testing, safety testing
- **Performance** (P1): Latency, throughput, cost analysis
- **Security** (P1): Prompt injection resistance, output safety
- **Operations** (P1): Model deployment, rollback, monitoring

### Prompt Changes

**Change Types:**
- New prompt template
- Prompt optimization
- System message changes
- Few-shot example updates

**Applicable Domains:**
- **Core** (P0): Prompt design principles, clarity, specificity
- **Security** (P0): Prompt injection prevention, jailbreak resistance
- **Testing** (P0): Prompt effectiveness evaluation, A/B testing
- **Documentation** (P1): Prompt documentation, versioning

### Retrieval Changes

**Change Types:**
- New data source
- Chunking strategy modification
- Embedding model change
- Vector database migration
- Ranking algorithm update

**Applicable Domains:**
- **Core** (P0): Retrieval architecture, chunking strategy
- **Data** (P0): Data quality, sourcing, indexing
- **Testing** (P0): Retrieval accuracy, relevance metrics
- **Performance** (P1): Query latency, throughput
- **Security** (P1): Data access controls, query filtering

### Tool Changes

**Change Types:**
- New tool integration
- Tool parameter modification
- Tool removal
- Tool fallback logic changes

**Applicable Domains:**
- **Integration** (P0): API contracts, versioning, compatibility
- **Security** (P0): Access controls, input sanitization, audit logging
- **Testing** (P0): Contract tests, integration tests, failure simulation
- **Operations** (P1): Health monitoring, circuit breakers, fallback strategies
- **Core** (P1): Tool selection logic, parameter validation

### Infrastructure Changes

**Change Types:**
- Deployment environment changes
- Scaling configuration
- Networking changes
- Database migrations
- Cache configuration

**Applicable Domains:**
- **Operations** (P0): Deployment strategy, rollback plan, monitoring
- **Security** (P0): Network security, access controls, encryption
- **Performance** (P1): Performance impact, capacity planning
- **Testing** (P1): Infrastructure testing, chaos testing

### Data Changes

**Change Types:**
- New dataset integration
- Data pipeline modification
- Data migration
- Data retention policy changes

**Applicable Domains:**
- **Data** (P0): Data quality, sourcing, governance
- **Security** (P0): Data encryption, access controls
- **Testing** (P0): Data validation, pipeline testing
- **Compliance** (P1): Regulatory compliance, privacy impact
- **Operations** (P1): Data pipeline monitoring

## Advanced Routing Scenarios

### Multi-Domain Interactions

**Scenario: Model Upgrade with New Features**
- **Core**: Model capability assessment, prompt migration
- **Testing**: Comprehensive regression testing, new feature testing
- **Security**: New attack surface analysis
- **Performance**: Latency and cost comparison
- **Operations**: Deployment strategy, rollback plan
- **Documentation**: Update all user-facing documentation

**Scenario: RAG System with New Data Source**
- **Data**: Data quality assessment, sourcing, indexing
- **Core**: Retrieval architecture, chunking strategy
- **Testing**: Retrieval accuracy, relevance metrics
- **Performance**: Query latency impact
- **Security**: Data access controls, injection prevention
- **Compliance**: Data governance, privacy impact

**Scenario: Agent with New Tool Integration**
- **Integration**: API contract, versioning, compatibility
- **Security**: Tool access controls, input sanitization
- **Testing**: Contract tests, integration tests, failure simulation
- **Operations**: Tool health monitoring, circuit breakers
- **Core**: Tool selection logic, parameter validation

## Routing Checklist

### Pre-Routing Checklist

- [ ] System type clearly identified
- [ ] Change type clearly identified
- [ ] Risk tier assessed and documented
- [ ] All stakeholders identified
- [ ] Regulatory requirements identified

### Routing Checklist

- [ ] Primary domains selected based on system type
- [ ] Secondary domains selected based on change type
- [ ] Tertiary domains considered
- [ ] Domain interactions identified
- [ ] Routing rationale documented

### Post-Routing Checklist

- [ ] All selected domain files loaded
- [ ] P0/P1 items identified for each domain
- [ ] Evidence requirements identified
- [ ] Test requirements identified
- [ ] Routing decision reviewed and approved

## Routing Documentation Template

```
DOMAIN ROUTING RECORD
=====================
Task: [Task description]
System Type: [AI App / Agent / RAG / Integration / Other]
Change Type: [Model / Prompt / Retrieval / Tool / Infrastructure / Data]
Risk Tier: [Tier 1-4]
Date: YYYY-MM-DD
Routed By: [Name/Role]

Primary Domains
---------------
1. [Domain]: [Rationale for inclusion]
2. [Domain]: [Rationale for inclusion]

Secondary Domains
-----------------
1. [Domain]: [Rationale for inclusion]
2. [Domain]: [Rationale for inclusion]

Tertiary Domains (Considered but Not Fully Applied)
---------------------------------------------------
1. [Domain]: [Rationale for exclusion or limited application]

P0/P1 Items Identified
-----------------------
- [Domain] P0: [Item description]
- [Domain] P1: [Item description]

Evidence Required
-----------------
- [Evidence 1]: [Domain, how to collect]
- [Evidence 2]: [Domain, how to collect]

Tests Required
--------------
- [Test 1]: [Domain, test type]
- [Test 2]: [Domain, test type]

Review Status
-------------
- [ ] Routing reviewed by tech lead
- [ ] Routing approved
- [ ] Any deviations documented

Sign-off: _______________
Date: _______________
```

## Routing Common Mistakes

### Mistake 1: Incomplete Domain Coverage

**Problem**: Missing relevant domains, leading to gaps in quality assurance.

**Example**: Deploying a RAG system without considering Data or Security domains.

**Solution**: Use the routing decision tree systematically. Don't skip domains that seem "obvious."

### Mistake 2: Over-Application

**Problem**: Applying all domains to every task, creating unnecessary overhead.

**Example**: Applying Compliance domain to an internal experimental prototype.

**Solution**: Consider risk tier and system type. Low-risk experimental systems need fewer domains.

### Mistake 3: Ignoring Domain Interactions

**Problem**: Treating domains as independent, missing cross-cutting concerns.

**Example**: Focusing on Core (model selection) without considering Security (prompt injection risks).

**Solution**: Map domain dependencies and ensure cross-cutting concerns are addressed.

### Mistake 4: Not Documenting Routing Decisions

**Problem**: Cannot explain why certain domains were selected or skipped.

**Example**: During audit, unable to justify why Security domain was not fully applied.

**Solution**: Always document routing decisions with rationale.

### Mistake 5: Static Routing

**Problem**: Using the same domain routing for all instances of a task type.

**Example**: Always applying the same domains for "model changes" without considering the specific change.

**Solution**: Re-evaluate routing for each specific task. Consider the change scope and impact.

## Routing Tools and Automation

### Automated Routing Suggestions

**Input-Based Routing**
```python
def suggest_domains(system_type, change_type, risk_tier):
    routing_matrix = {
        ('ai_app', 'model_change'): ['Core', 'Testing', 'Performance', 'Security'],
        ('ai_app', 'prompt_change'): ['Core', 'Security', 'Testing'],
        ('rag', 'data_change'): ['Core', 'Data', 'Testing', 'Performance'],
        ('integration', 'tool_change'): ['Integration', 'Security', 'Testing', 'Operations'],
        ('any', 'production_release'): ['Operations', 'Testing', 'Security', 'Compliance', 'Performance'],
        ('any', 'code_review'): ['Development', 'Security', 'Testing', 'Documentation'],
        ('any', 'incident'): ['Operations', 'Troubleshooting', 'Testing', 'Performance'],
        ('regulated', 'any'): ['Compliance', 'Data', 'Security', 'Documentation', 'Testing'],
    }
    
    # Get base domains
    domains = routing_matrix.get((system_type, change_type), [])
    
    # Adjust based on risk tier
    if risk_tier == 'Tier 1':
        domains = list(set(domains + ['Compliance', 'Security', 'Operations']))
    elif risk_tier == 'Tier 2':
        domains = list(set(domains + ['Security', 'Operations']))
    
    return domains
```

### Routing Validation

**Validation Checks**
- Verify all primary domains are included
- Verify no critical domains are missing
- Verify domain depth matches risk tier
- Verify routing is documented

### Routing Metrics

Track routing effectiveness:
- Domains applied per task type
- P0/P1 items found per domain
- Evidence completeness per domain
- Time spent per domain
- Missed issues (post-release bugs that should have been caught by a domain)

## Appendix: Routing Quick Reference

### Task Type to Domain Mapping

| Task Type | Core | Security | Data | Integration | Development | Testing | Operations | Documentation | Performance | Compliance |
|-----------|------|----------|------|-------------|-------------|---------|------------|---------------|-------------|------------|
| New AI App | P0 | P0 | P0 | - | - | P0 | P0 | P1 | P1 | P1 |
| Tool Integration | P0 | P0 | - | P0 | - | P0 | P1 | P1 | - | - |
| RAG System | P0 | P0 | P0 | P1 | - | P0 | P1 | P1 | P0 | P1 |
| Production Release | P1 | P0 | P1 | P1 | - | P0 | P0 | P1 | P0 | P0 |
| Code Review | P1 | P0 | - | - | P0 | P0 | - | P1 | - | - |
| Incident Response | P1 | P1 | - | - | - | P0 | P0 | P1 | P0 | - |
| Regulated Workflow | P0 | P0 | P0 | - | - | P0 | P1 | P0 | - | P0 |

### Change Type to Domain Mapping

| Change Type | Core | Security | Data | Integration | Development | Testing | Operations | Documentation | Performance | Compliance |
|-------------|------|----------|------|-------------|-------------|---------|------------|---------------|-------------|------------|
| Model Change | P0 | P1 | - | - | - | P0 | P1 | P1 | P1 | - |
| Prompt Change | P0 | P0 | - | - | - | P0 | - | P1 | - | - |
| Retrieval Change | P0 | P1 | P0 | - | - | P0 | - | P1 | P1 | - |
| Tool Change | P1 | P0 | - | P0 | - | P0 | P1 | P1 | - | - |
| Infrastructure Change | - | P0 | - | P1 | - | P1 | P0 | P1 | P1 | - |
| Data Change | P1 | P0 | P0 | - | - | P0 | P1 | P1 | P1 | P1 |

### Risk Tier to Domain Depth Mapping

| Risk Tier | Core | Security | Data | Integration | Development | Testing | Operations | Documentation | Performance | Compliance |
|-----------|------|----------|------|-------------|-------------|---------|------------|---------------|-------------|------------|
| Tier 1 | Full | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| Tier 2 | Full | Full | Full | Standard | Standard | Full | Full | Standard | Full | Full |
| Tier 3 | Standard | Standard | Standard | Minimal | Minimal | Standard | Standard | Minimal | Standard | Standard |
| Tier 4 | Minimal | Minimal | Minimal | - | Minimal | Minimal | Minimal | - | Minimal | Minimal |

**Depth Definitions:**
- **Full**: All P0, P1, P2, P3 items apply. Comprehensive review required.
- **Standard**: All P0, P1 items apply. P2 items as time permits.
- **Minimal**: P0 items only. P1 items only if critical.
- **Dash (-)**: Domain not applicable to this risk tier.
