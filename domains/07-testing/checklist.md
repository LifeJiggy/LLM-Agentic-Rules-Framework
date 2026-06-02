# Testing Domain - Checklist

## Overview

This comprehensive checklist verifies testing best practices for LLM/agentic systems. Use this during code review, pre-deployment, and audit.

## Table of Contents

1. [Unit Testing](#unit-testing)
2. [Integration Testing](#integration-testing)
3. [End-to-End Testing](#end-to-end-testing)
4. [LLM/Model Testing](#llmmodel-testing)
5. [Prompt Testing](#prompt-testing)
6. [Agent Behavior Testing](#agent-behavior-testing)
7. [Tool Use Testing](#tool-use-testing)
8. [RAG Testing](#rag-testing)
9. [Safety and Alignment Testing](#safety-and-alignment-testing)
10. [Performance and Latency Testing](#performance-and-latency-testing)
11. [Security Testing](#security-testing)
12. [Regression Testing](#regression-testing)
13. [Contract Testing](#contract-testing)
14. [Chaos Engineering](#chaos-engineering)
15. [CI/CD Integration](#cicd-integration)
16. [Monitoring and Observability](#monitoring-and-observability)
17. [A/B Testing](#ab-testing)
18. [Cost Management](#cost-management)
19. [Test Data Management](#test-data-management)
20. [Streaming Tests](#streaming-tests)
21. [Multi-Modal Tests](#multi-modal-tests)
22. [Human Evaluation](#human-evaluation)
23. [Explainability](#explainability)
24. [Fairness](#fairness)
25. [Production Readiness](#production-readiness)
26. [Deployment Gates](#deployment-gates)

---

## Unit Testing

### Core Principles

- [ ] Tests are isolated and order-independent
- [ ] Each test has a single clear assertion (or logical group)
- [ ] AAA pattern (Arrange-Act-Assert) is followed
- [ ] Test functions and classes use descriptive names (`test_<behavior>_when_<condition>`)
- [ ] No external API calls in unit tests (use mocks)
- [ ] No database writes in unit tests (use mocks or transactions)
- [ ] No file system dependencies (use in-memory or tmp_path fixtures)

### Coverage and Quality

- [ ] Unit test coverage exceeds 85% for business logic
- [ ] Complex branching logic is fully covered
- [ ] Error handling paths are tested
- [ ] Edge cases are covered (empty inputs, boundary values)
- [ ] No test depends on execution order
- [ ] Fixtures are scoped appropriately (function/class/module)
- [ ] Tests complete within 30 seconds per suite
- [ ] No flaky tests (flaky tests must be fixed or quarantined)

### Specific to LLM/Agentic Systems

- [ ] LLM client is mocked in unit tests
- [ ] Tool calls are mocked at the interface boundary
- [ ] Prompt templates are tested for syntax and variable substitution
- [ ] Tokenizers are tested for boundary conditions
- [ ] Embeddings are mocked for unit tests of retrieval logic
- [ ] Memory/state is reset between tests
- [ ] Configuration loading is tested without side effects

### Sign-Off

- [ ] All unit tests pass locally
- [ ] Coverage report reviewed
- [ ] No skipped tests without explanation

---

## Integration Testing

### Core Principles

- [ ] Tests verify interaction between components
- [ ] External services are mocked or use dedicated test instances
- [ ] Database state is reset between tests
- [ ] Network calls are mocked or use wiremock/pact
- [ ] Tests are deterministic and repeatable

### LLM/Agentic Specific

- [ ] Real LLM API is tested with a small, fixed dataset
- [ ] Tool integrations are tested with mock servers
- [ ] Data pipelines (ingestion, chunking, embedding) are tested end-to-end
- [ ] Vector store connections are tested
- [ ] API contracts with LLM providers are validated
- [ ] Authentication and rate limiting are tested
- [ ] Retry logic is tested with simulated failures

### Sign-Off

- [ ] Integration tests pass in CI
- [ ] Test environment mirrors production configuration
- [ ] Tests run in under 10 minutes

---

## End-to-End Testing

### Core Principles

- [ ] E2E tests cover critical user journeys
- [ ] Tests run against a staging environment
- [ ] Tests are independent and can run in any order
- [ ] Test data is seeded before suite execution
- [ ] Cleanup runs after each test or suite

### LLM/Agentic Specific

- [ ] Chat flows are tested turn-by-turn
- [ ] Tool-using agents are tested with real or semi-real tools
- [ ] RAG pipelines are tested with production-like data
- [ ] Long-context conversations are tested
- [ ] Error recovery flows are tested
- [ ] Multi-step reasoning chains are validated
- [ ] Response times are measured and within SLO

### Sign-Off

- [ ] E2E tests pass in staging
- [ ] Performance criteria met
- [ ] Test data is production-like

---

## LLM/Model Testing

### Accuracy and Quality

- [ ] Model accuracy measured on golden dataset
- [ ] Accuracy meets or exceeds baseline threshold
- [ ] Task-specific metrics evaluated (F1, BLEU, ROUGE, etc.)
- [ ] Human evaluation sampled for high-risk tasks
- [ ] A/B tests show improvement over baseline

### Non-Determinism

- [ ] Temperature=0 outputs are deterministic and tested
- [ ] Non-zero temperatures use probabilistic assertions
- [ ] Variance is measured across multiple generations
- [ ] Seeds are logged for reproducibility

### Behavioral Testing

- [ ] Refusal behavior tested for harmful prompts
- [ ] Instruction-following tested across prompt complexity
- [ ] Format adherence tested (JSON, XML, markdown)
- [ ] Context utilization tested for long prompts
- [ ] System prompt leaks are tested against

### Sign-Off

- [ ] Model evaluation report generated
- [ ] Regression tests pass
- [ ] Safety tests pass

---

## Prompt Testing

### Template Validation

- [ ] All prompt templates render without errors
- [ ] Required variables are validated before rendering
- [ ] Missing variables produce clear errors
- [ ] Prompt injection patterns are detected and blocked

### Versioning

- [ ] Prompts are versioned in registry
- [ ] Old versions preserved for rollback
- [ ] Performance compared across versions
- [ ] A/B testing used for prompt changes

### Evaluation

- [ ] Each prompt template has associated test cases
- [ ] Expected outputs defined (keywords, semantic similarity, or classification)
- [ ] Negative test cases defined
- [ ] Evaluation runs in CI on every prompt change

### Sign-Off

- [ ] All prompt tests pass
- [ ] No prompt syntax errors
- [ ] No prompt injection vulnerabilities

---

## Agent Behavior Testing

### Decision Making

- [ ] Agent routes to correct tools for given inputs
- [ ] Agent asks for clarification when ambiguous
- [ ] Agent terminates appropriately when task complete
- [ ] Agent refuses harmful or out-of-scope requests

### Loop Control

- [ ] Max iteration limit enforced
- [ ] Agent terminates on completion without extra loops
- [ ] Agent recovers from tool failures
- [ ] Agent state transitions follow valid state machine

### Memory and Context

- [ ] Memory persists across turns within a session
- [ ] Memory does not leak between sessions
- [ ] Context window limits respected
- [ ] Summarization triggered at appropriate thresholds
- [ ] Old messages evicted correctly

### Sign-Off

- [ ] Agent decision tests pass
- [ ] Memory tests pass
- [ ] Loop termination tests pass

---

## Tool Use Testing

### Invocation

- [ ] Correct tools called for intended tasks
- [ ] Tool arguments validated against schema
- [ ] Required parameters present in calls
- [ ] Optional parameters handled correctly
- [ ] Tool outputs parsed correctly

### Failure Handling

- [ ] Timeout triggers retry or graceful degradation
- [ ] Tool unavailable fallback tested
- [ ] Invalid tool output handled
- [ ] Partial results handled
- [ ] Circuit breaker activates after repeated failures

### Sign-Off

- [ ] All tool call tests pass
- [ ] Failure scenarios handled
- [ ] Performance within latency budget

---

## RAG Testing

### Retrieval Quality

- [ ] Relevant documents retrieved for test queries
- [ ] Precision at K measured (P@1, P@5, P@10)
- [ ] Recall at K measured (R@1, R@5, R@10)
- [ ] Embedding quality validated
- [ ] Vector store index refreshed after updates

### Generation Quality

- [ ] Responses grounded in retrieved context
- [ ] Hallucinations measured on test set
- [ ] Citation accuracy tested
- [ ] Response relevance to query tested

### Pipeline Performance

- [ ] End-to-end latency within SLO
- [ ] Retrieval latency within budget
- [ ] Generation latency within budget
- [ ] Pipeline fails gracefully on retrieval failure

### Sign-Off

- [ ] RAG accuracy meets threshold
- [ ] Hallucination rate below limit
- [ ] Latency SLOs met

---

## Safety and Alignment Testing

### Harmful Content

- [ ] Refuses requests for dangerous instructions
- [ ] No unsafe content in responses
- [ ] PII redaction tested
- [ ] Toxicity below threshold

### Jailbreak Resistance

- [ ] Common jailbreak patterns blocked
- [ ] Instruction override attempts fail
- [ ] Context manipulation attempts fail
- [ ] Translation-based jailbreaks blocked
- [ ] Multi-turn jailbreak attempts fail

### Bias and Fairness

- [ ] Demographic parity tested across gender, race, age
- [ ] Stereotype association measured
- [ ] Equalized odds verified
- [ ] Fairness metrics tracked over time

### Sign-Off

- [ ] Safety test suite passes
- [ ] No critical or high-severity violations
- [ ] Red team review completed for major changes

---

## Performance and Latency Testing

### Latency

- [ ] Average latency measured and within SLO
- [ ] P95 latency measured and within SLO
- [ ] P99 latency measured and within SLO
- [ ] Time to first token measured
- [ ] Token generation rate measured

### Throughput

- [ ] Maximum concurrent requests tested
- [ ] Throughput measured under load
- [ ] Request queueing behavior tested
- [ ] Rate limiting enforced

### Resource Usage

- [ ] CPU usage under load measured
- [ ] Memory usage profiled
- [ ] GPU utilization measured (if applicable)
- [ ] Connection pool exhaustion tested

### Sign-Off

- [ ] Latency SLOs met
- [ ] Throughput meets requirements
- [ ] Load tests pass

---

## Security Testing

### Input Validation

- [ ] Prompt injection patterns blocked
- [ ] Input length limits enforced
- [ ] Special characters handled safely
- [ ] SQL injection blocked (if using text-to-SQL)
- [ ] Command injection blocked

### Output Safety

- [ ] No secrets in outputs
- [ ] No PII in outputs unless intended
- [ ] Output length limits enforced
- [ ] Markdown/HTML sanitization applied
- [ ] Code output sandboxed if executed

### Authentication and Authorization

- [ ] API keys validated
- [ ] User permissions checked
- [ ] Rate limits per user enforced
- [ ] Audit logging enabled

### Sign-Off

- [ ] Security scan passed
- [ ] No hardcoded credentials
- [ ] Secrets rotated

---

## Regression Testing

### Scope

- [ ] Accuracy regression tested against golden dataset
- [ ] Safety regression tested against red-team cases
- [ ] Latency regression tested against baselines
- [ ] Cost regression tested against targets
- [ ] Behavioral regression tested against user scenarios

### Execution

- [ ] Regression tests run on every model change
- [ ] Regression tests run on every prompt change
- [ ] Regression tests run on every dependency update
- [ ] Thresholds set with statistical rigor
- [ ] Failed regressions block deployment

### Sign-Off

- [ ] All regression tests pass
- [ ] No unexpected degradations
- [ ] Baseline updated if regression is expected

---

## Contract Testing

### Definition

- [ ] Contracts defined for all tool interfaces
- [ ] Contracts define input/output schemas
- [ ] Contracts define latency expectations
- [ ] Contracts define error responses

### Validation

- [ ] Consumer-driven contracts verified
- [ ] Provider compliance tested
- [ ] Contract changes communicated
- [ ] Breaking changes flagged
- [ ] Contract tests run in CI

### Sign-Off

- [ ] All contracts verified
- [ ] No unhandled schema changes
- [ ] Documentation updated

---

## Chaos Engineering

### Scenarios

- [ ] LLM provider outage tested
- [ ] Tool timeouts tested
- [ ] Database failure tested
- [ ] Network latency injection tested
- [ ] Partial response corruption tested
- [ ] Rate limit exhaustion tested
- [ ] Memory pressure tested

### Validation

- [ ] Circuit breakers activate correctly
- [ ] Fallbacks engage automatically
- [ ] Errors are graceful and informative
- [ ] System recovers without manual intervention
- [ ] Monitoring alerts fire correctly

### Sign-Off

- [ ] Chaos tests pass
- [ ] Blast radius contained
- [ ] Runbooks updated

---

## CI/CD Integration

### Pipeline Stages

- [ ] Linting and formatting checks
- [ ] Unit tests with coverage
- [ ] Integration tests
- [ ] Safety and red-team tests
- [ ] Regression tests
- [ ] Performance benchmarks
- [ ] Security scanning
- [ ] Artifact publishing

### Quality Gates

- [ ] Tests must pass to merge
- [ ] Coverage threshold enforced (e.g., 85%)
- [ ] Security findings block deployment
- [ ] Performance regression blocks deployment
- [ ] Manual approval required for production release

### Sign-Off

- [ ] Pipeline green on main branch
- [ ] No broken builds
- [ ] All quality gates passing

---

## Monitoring and Observability

### Metrics

- [ ] Request count tracked
- [ ] Latency histograms (p50, p95, p99)
- [ ] Error rates tracked
- [ ] Token usage tracked
- [ ] Cost tracked per model/user/project
- [ ] Tool call success rates tracked
- [ ] Cache hit rates tracked

### Logging

- [ ] Structured JSON logging
- [ ] Prompt hashes logged (not raw prompts with PII)
- [ ] Model version logged
- [ ] Session IDs logged
- [ ] User IDs logged (if available)
- [ ] Error traces logged

### Alerting

- [ ] Error rate alerts configured
- [ ] Latency spike alerts configured
- [ ] Cost anomaly alerts configured
- [ ] Safety violation alerts configured
- [ ] Drift detection alerts configured

### Sign-Off

- [ ] Dashboards created
- [ ] Alerts configured and tested
- [ ] On-call runbooks written

---

## A/B Testing

### Experiment Design

- [ ] Hypothesis clearly stated
- [ ] Sample size calculated before test
- [ ] Randomization method defined
- [ ] Success metrics defined
- [ ] Guardrail metrics defined
- [ ] Test duration determined

### Execution

- [ ] Traffic split configured
- [ ] Metrics collection automated
- [ ] Statistical significance checked daily
- [ ] Early stopping criteria defined
- [ ] Results documented

### Sign-Off

- [ ] Results statistically significant
- [ ] Winner deployed to all traffic
- [ ] Loser analyzed for learnings

---

## Cost Management

### Monitoring

- [ ] Cost per request tracked
- [ ] Cost per user tracked
- [ ] Cost per feature tracked
- [ ] Budget alerts configured

### Optimization

- [ ] Model routing based on complexity
- [ ] Caching of common queries
- [ ] Prompt compression used
- [ ] Batch processing used where possible
- [ ] Unnecessary API calls eliminated

### Sign-Off

- [ ] Cost projections reviewed
- [ ] Budget alerts tested
- [ ] Cost optimization opportunities documented

---

## Test Data Management

### Golden Datasets

- [ ] Golden dataset exists for all major tasks
- [ ] Dataset versioned in version control
- [ ] Dataset reviewed by domain experts
- [ ] Dataset split into train/val/test
- [ ] Dataset size sufficient for statistical power

### Synthetic Data

- [ ] Synthetic data used for augmentation
- [ ] Synthetic data validated for quality
- [ ] Synthetic data does not leak into golden sets

### Versioning

- [ ] Data schema versioned
- [ ] Data changes tracked in changelog
- [ ] Old versions archived

### Sign-Off

- [ ] Dataset quality validated
- [ ] No data leakage between splits
- [ ] Dataset documentation complete

---

## Streaming Tests

### Correctness

- [ ] Streaming responses complete
- [ ] Chunk ordering is correct
- [ ] No duplicate or missing content
- [ ] Final output matches non-streaming (where applicable)

### Latency

- [ ] Time to first token measured
- [ ] Inter-token latency measured
- [ ] Streaming latency within SLO

### Resilience

- [ ] Handles client disconnects
- [ ] Handles server restarts mid-stream
- [ ] Handles empty chunks
- [ ] Handles slow consumers

### Sign-Off

- [ ] Streaming tests pass
- [ ] Latency SLOs met
- [ ] Edge cases handled

---

## Multi-Modal Tests

### Input Validation

- [ ] Text inputs tested
- [ ] Image inputs tested
- [ ] Audio inputs tested
- [ ] Video inputs tested (if applicable)
- [ ] Mixed modality inputs tested

### Cross-Modal Consistency

- [ ] Text and image queries produce consistent answers
- [ ] Audio transcription and text query produce consistent results
- [ ] Multi-modal reasoning validated

### Quality

- [ ] Image descriptions accurate
- [ ] Audio transcriptions accurate
- [ ] Video captions accurate
- [ ] OCR accuracy measured

### Sign-Off

- [ ] All modality tests pass
- [ ] Cross-modal consistency verified
- [ ] Quality thresholds met

---

## Human Evaluation

### Process

- [ ] Evaluation criteria defined
- [ ] Evaluator guidelines documented
- [ ] Sufficient number of evaluators per item
- [ ] Inter-rater reliability measured
- [ ] Evaluation results aggregated and analyzed

### Integration

- [ ] Human evaluation integrated into launch process
- [ ] High-risk outputs flagged for review
- [ ] Feedback loop to model training documented
- [ ] Evaluation costs tracked

### Sign-Off

- [ ] Human evaluation completed for launch
- [ ] Inter-rater reliability acceptable
- [ ] Issues addressed before deployment

---

## Explainability

### Requirements

- [ ] Explainability requirements defined per use case
- [ ] Reasoning chains tested for completeness
- [ ] Source attribution tested for RAG
- [ ] Confidence scores calibrated
- [ ] Explanations are intelligible to users

### Validation

- [ ] Explanations generated for critical decisions
- [ ] Explanations reviewed by humans
- [ ] Explanation quality metrics tracked

### Sign-Off

- [ ] Explainability requirements met
- [ ] Explanations verified by domain experts

---

## Fairness

### Testing

- [ ] Fairness metrics computed for all protected attributes
- [ ] Tests run on every model update
- [ ] Disparate impact measured
- [ ] Equalized odds verified
- [ ] Bias mitigated to acceptable levels

### Monitoring

- [ ] Fairness metrics tracked in production
- [ ] Alerts configured for fairness drift
- [ ] Mitigation strategies documented

### Sign-Off

- [ ] Fairness tests pass
- [ ] No disparate impact beyond threshold
- [ ] Bias mitigation applied where needed

---

## Production Readiness

### Monitoring

- [ ] SLOs defined and documented
- [ ] Dashboards deployed
- [ ] Alerts configured and tested
- [ ] Runbooks written for common failures

### Operations

- [ ] Rollback procedure tested
- [ ] Canary deployment process defined
- [ ] Incident response plan documented
- [ ] On-call rotation established

### Sign-Off

- [ ] Production readiness review completed
- [ ] All SLOs met in staging
- [ ] Runbooks tested

---

## Deployment Gates

### Pre-Deployment

- [ ] All tests pass (unit, integration, e2e)
- [ ] Code review approved
- [ ] Security scan passed
- [ ] Performance benchmarks met
- [ ] Cost estimate reviewed
- [ ] Documentation updated

### Deployment

- [ ] Canary deployed
- [ ] Canary metrics validated
- [ ] Gradual rollout to 25%, 50%, 100%
- [ ] No rollback triggers hit
- [ ] Release notes published

### Post-Deployment

- [ ] Production monitoring active
- [ ] SLOs met for 24 hours
- [ ] No P0/P1 incidents
- [ ] Team notified of successful deployment

### Sign-Off

- [ ] All gates passed
- [ ] Deployment approved
- [ ] Post-deployment review scheduled

---

## Roles Sign-Off

### Engineer

- [ ] Code written and reviewed
- [ ] Tests implemented
- [ ] Documentation updated
- [ ] Performance validated
- [ ] Security concerns addressed

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
- [ ] Attack surface minimized

### MLOps

- [ ] Model deployed and monitored
- [ ] Infrastructure healthy
- [ ] Rollback tested
- [ ] Cost projections accurate

### Product

- [ ] Requirements met
- [ ] User experience validated
- [ ] Launch criteria satisfied

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
