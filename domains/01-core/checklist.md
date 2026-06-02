# Core Domain - Checklist

## Overview

This checklist verifies that core principles and best practices are followed for all LLM/agentic system implementations.

## Table of Contents

1. [Pre-Implementation Checklist](#pre-implementation-checklist)
2. [Prompt Engineering Checklist](#prompt-engineering-checklist)
3. [Agent Design Checklist](#agent-design-checklist)
4. [Tool Integration Checklist](#tool-integration-checklist)
5. [Context Management Checklist](#context-management-checklist)
6. [Memory System Checklist](#memory-system-checklist)
7. [Error Handling Checklist](#error-handling-checklist)
8. [Security Checklist](#security-checklist)
9. [Performance Checklist](#performance-checklist)
10. [Testing Checklist](#testing-checklist)
11. [Monitoring Checklist](#monitoring-checklist)
12. [Deployment Checklist](#deployment-checklist)
13. [Documentation Checklist](#documentation-checklist)
14. [Cost Management Checklist](#cost-management-checklist)
15. [Sign-Off Checklist](#sign-off-checklist)

---

## Pre-Implementation Checklist

### Requirements Analysis
- [ ] User requirements documented and validated
- [ ] Success criteria defined (quantitative where possible)
- [ ] Scope boundaries established (what the system will NOT do)
- [ ] Stakeholder alignment achieved
- [ ] Risk assessment completed

### Architecture Planning
- [ ] Agent roles and responsibilities defined
- [ ] System architecture diagram created
- [ ] Data flow documented
- [ ] Integration points identified
- [ ] Scalability requirements established
- [ ] Failure modes identified

### Resource Planning
- [ ] Model selection justified (capability vs cost)
- [ ] Token budget estimated
- [ ] Tool inventory defined
- [ ] Infrastructure requirements specified
- [ ] Team skills gap analysis completed

---

## Prompt Engineering Checklist

### Design
- [ ] Prompt is specific and unambiguous
- [ ] Task scope is clearly bounded
- [ ] Constraints are explicitly stated
- [ ] Desired output format is defined
- [ ] Few-shot examples are provided (where applicable)
- [ ] Context window requirements calculated

### Structure
- [ ] Uses consistent formatting
- [ ] Separates instruction from context from examples
- [ ] Uses delimiters for different sections
- [ ] Includes instruction hierarchy (system > task > context)

### Content
- [ ] No contradictory instructions
- [ ] No ambiguous language ("maybe", "possibly", "might")
- [ ] No overly broad scope
- [ ] Numbers and dates are specific (not "recent", "many")

### Validation
- [ ] Tested with representative inputs
- [ ] Edge cases tested (empty, long, malformed)
- [ ] Output parsed successfully (JSON, structured formats)
- [ ] No prompt injection vulnerabilities detected

### Versioning
- [ ] Prompt registered in version control
- [ ] Previous versions archived
- [ ] Change log maintained
- [ ] A/B test configured for major changes

---

## Agent Design Checklist

### Architecture
- [ ] Single Responsibility Principle applied
- [ ] Agent boundaries clearly defined
- [ ] Inter-agent communication protocol established
- [ ] State management approach selected (stateful vs stateless)

### Capabilities
- [ ] Agent capabilities documented
- [ ] Skill/tool inventory complete
- [ ] Capability boundaries enforced (no god agents)
- [ ] Specialization appropriate for task

### Decision Making
- [ ] Decision logic documented
- [ ] Fallback strategies defined
- [ ] Escalation criteria established
- [ ] Human-in-the-loop points identified

### Lifecycle
- [ ] Initialization defined
- [ ] Execution flow documented
- [ ] Termination conditions specified
- [ ] Cleanup/shutdown handled

---

## Tool Integration Checklist

### Tool Selection
- [ ] Tools chosen based on requirements
- [ ] Tool capabilities documented
- [ ] Tool dependencies identified
- [ ] Fallback tools defined

### Implementation
- [ ] Tool interfaces are consistent
- [ ] Input validation implemented
- [ ] Output schemas defined
- [ ] Error handling comprehensive

### Safety
- [ ] Timeouts configured
- [ ] Retry logic implemented
- [ ] Circuit breakers configured (where appropriate)
- [ ] Resource limits set

### Testing
- [ ] Tool contracts defined
- [ ] Contract tests written
- [ ] Failure scenarios tested
- [ ] Integration tests pass

---

## Context Management Checklist

### Budget Management
- [ ] Token budget calculated for context window
- [ ] Budget allocation defined (system > task > history > context)
- [ ] Truncation strategy implemented
- [ ] Overflow handling defined

### Content
- [ ] Relevant context identified
- [ ] Irrelevant information excluded
- [ ] Context sources documented
- [ ] Context freshness requirements defined

### Conversation Management
- [ ] Conversation history policy established
- [ ] Summarization trigger points defined
- [ ] Context compression approach selected
- [ ] Long-conversation handling tested

### Versioning
- [ ] Context sources versioned
- [ ] Context changes tracked
- [ ] Rollback capability verified

---

## Memory System Checklist

### Design
- [ ] Memory types identified (episodic, semantic, working, procedural)
- [ ] Memory capacity limits set
- [ ] Eviction policy defined
- [ ] Persistence strategy selected

### Implementation
- [ ] Memory store initialized
- [ ] Storage interface implemented
- [ ] Retrieval logic implemented
- [ ] Consolidation strategy defined

### Quality
- [ ] Memory relevance scoring tested
- [ ] Retrieval accuracy measured
- [ ] Memory leakage prevented (session isolation)
- [ ] Memory corruption recovery tested

---

## Error Handling Checklist

### Categorization
- [ ] Error types categorized (transient, input, model, system)
- [ ] Retry strategy defined per error type
- [ ] Maximum retry limits set
- [ ] Backoff strategy configured

### Recovery
- [ ] Fallback behaviors defined
- [ ] Circuit breakers configured
- [ ] Graceful degradation paths identified
- [ ] User notification approach defined

### Logging
- [ ] Error logging comprehensive
- [ ] Stack traces captured appropriately
- [ ] Error metrics collected
- [ ] Alerting thresholds configured

### Testing
- [ ] Error scenarios tested
- [ ] Recovery from errors tested
- [ ] Timeout behavior tested
- [ ] Cascading failure prevention tested

---

## Security Checklist

### Input Security
- [ ] Input validation implemented
- [ ] Prompt injection detection active
- [ ] Input length limits enforced
- [ ] Malicious pattern filtering enabled

### Output Security
- [ ] Output content filtering configured
- [ ] PII detection and redaction active
- [ ] Harmful content detection enabled
- [ ] Output length limits enforced

### Access Control
- [ ] Authentication required
- [ ] Authorization checks implemented
- [ ] API keys rotated regularly
- [ ] Rate limiting configured per user

### Data Protection
- [ ] Sensitive data not logged
- [ ] Encryption in transit
- [ ] Encryption at rest
- [ ] Data retention policies enforced

---

## Performance Checklist

### Latency
- [ ] P50 latency measured and documented
- [ ] P95 latency measured and documented
- [ ] P99 latency measured and documented
- [ ] Time-to-first-token measured
- [ ] Latency SLOs defined

### Throughput
- [ ] Maximum concurrent requests tested
- [ ] Throughput measured under load
- [ ] Rate limiting configured
- [ ] Queue depth limits set

### Resource Usage
- [ ] Memory usage profiled
- [ ] CPU usage measured
- [ ] GPU utilization monitored
- [ ] Connection pool sizes optimized

### Optimization
- [ ] Caching strategy implemented
- [ ] Batch processing used where applicable
- [ ] Connection pooling configured
- [ ] Unnecessary API calls eliminated

---

## Testing Checklist

### Unit Tests
- [ ] All public methods tested
- [ ] Edge cases covered
- [ ] Error paths tested
- [ ] Mock external dependencies
- [ ] Test coverage > 85%

### Integration Tests
- [ ] Component interactions tested
- [ ] API contracts verified
- [ ] Database operations tested
- [ ] External service integrations tested

### End-to-End Tests
- [ ] Critical user flows tested
- [ ] Multi-turn conversations tested
- [ ] Error recovery flows tested
- [ ] Performance criteria met

### AI-Specific Tests
- [ ] Accuracy tests pass on golden dataset
- [ ] Safety tests pass (red team)
- [ ] Regression tests pass
- [ ] Bias/fairness tests pass
- [ ] Hallucination rate below threshold

---

## Monitoring Checklist

### Metrics
- [ ] Request count tracked
- [ ] Latency histograms collected
- [ ] Error rates monitored
- [ ] Token usage tracked
- [ ] Cost per request tracked

### Logging
- [ ] Structured JSON logging enabled
- [ ] Correlation IDs included
- [ ] Model version logged
- [ ] Prompt hashes logged (not raw PII)
- [ ] Error details captured

### Alerting
- [ ] Error rate alerts configured
- [ ] Latency spike alerts configured
- [ ] Cost anomaly alerts configured
- [ ] Safety violation alerts configured
- [ ] On-call escalation defined

### Dashboards
- [ ] Real-time dashboard deployed
- [ ] Key metrics visible
- [ ] Historical trends available
- [ ] SLO compliance tracked

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Rollback plan documented

### Deployment
- [ ] Canary deployment started
- [ ] Metrics validating success
- [ ] Gradual rollout staged
- [ ] No rollback triggers hit

### Post-Deployment
- [ ] SLOs met for 24 hours
- [ ] No P0/P1 incidents
- [ ] Monitoring active
- [ ] Alerts quiet or acknowledged
- [ ] Team notified of successful deployment

---

## Documentation Checklist

### Technical Documentation
- [ ] Architecture diagram up to date
- [ ] API documentation complete
- [ ] Deployment runbooks written
- [ ] Troubleshooting guide available

### User Documentation
- [ ] User guide published
- [ ] Example prompts provided
- [ ] Limitations documented
- [ ] Support contact identified

### Operational Documentation
- [ ] Runbooks for common failures
- [ ] Escalation procedures defined
- [ ] On-call rotation documented
- [ ] Incident response plan current

---

## Cost Management Checklist

### Tracking
- [ ] Cost per request tracked
- [ ] Daily/monthly cost monitored
- [ ] Cost per user tracked
- [ ] Budget alerts configured

### Optimization
- [ ] Model routing implemented (cheap vs expensive)
- [ ] Caching for common queries
- [ ] Prompt compression enabled
- [ ] Batch processing used where applicable

### Governance
- [ ] Approval required for expensive models
- [ ] Cost review cadence established
- [ ] Cost optimization roadmap created

---

## Sign-Off Checklist

### Engineering
- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Security concerns addressed
- [ ] Performance validated
- [ ] Documentation complete

### QA
- [ ] Test plan executed
- [ ] All pass criteria met
- [ ] Defects documented
- [ ] Regression results accepted
- [ ] Release criteria verified

### Security
- [ ] Security scan passed
- [ ] Secrets audit passed
- [ ] Threat model reviewed
- [ ] Access controls validated

### Product
- [ ] Requirements met
- [ ] User experience validated
- [ ] Launch criteria satisfied
- [ ] Support team trained

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)
