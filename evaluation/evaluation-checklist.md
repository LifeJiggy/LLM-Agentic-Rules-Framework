# Evaluation Checklist - LLM & Agentic Rules Framework

## Overview

This checklist provides actionable verification steps for evaluating LLM and agentic systems.

## P0 Critical Checks

### Evaluation Policy

- [ ] Evaluation policy defined and documented
- [ ] Evaluation types identified (safety, quality, performance, regression)
- [ ] Thresholds defined for each evaluation type
- [ ] Roles and responsibilities assigned
- [ ] Evaluation schedule established
- [ ] Policy approved by appropriate authority

### Safety Evaluation

- [ ] Safety evaluation suite defined
- [ ] Harmful content refusal tests included
- [ ] Prompt injection resistance tests included
- [ ] Jailbreak resistance tests included
- [ ] Policy compliance tests included
- [ ] Safety thresholds set to appropriate levels
- [ ] Safety evaluation runs before every release
- [ ] Safety failures are blocking

### Quality Evaluation

- [ ] Quality evaluation suite defined
- [ ] Task performance tests included
- [ ] Instruction following tests included
- [ ] Coherence tests included
- [ ] Relevance tests included
- [ ] Quality thresholds set appropriately
- [ ] Quality evaluation runs before every release

### Regression Evaluation

- [ ] Regression test suite defined
- [ ] Functional regression tests included
- [ ] Performance regression tests included
- [ ] Safety regression tests included
- [ ] Baseline established and documented
- [ ] Regression evaluation runs before every release
- [ ] Regressions are blocking

## P1 High Priority Checks

### Test Data Management

- [ ] Test datasets defined and documented
- [ ] Test data is realistic and representative
- [ ] Test data is version controlled
- [ ] Test data is refreshed regularly
- [ ] Test data includes edge cases
- [ ] Test data includes adversarial examples
- [ ] Test data quality is validated

### Evaluation Automation

- [ ] Evaluation automation implemented
- [ ] CI/CD integration configured
- [ ] Evaluation runs automatically on triggers
- [ ] Results are captured automatically
- [ ] Reports are generated automatically
- [ ] Alerting is configured for failures

### Performance Evaluation

- [ ] Performance benchmarks defined
- [ ] Latency benchmarks included
- [ ] Throughput benchmarks included
- [ ] Error rate benchmarks included
- [ ] Cost benchmarks included
- [ ] Performance SLOs documented
- [ ] Performance evaluation runs regularly

### Evaluation Reporting

- [ ] Evaluation reports generated
- [ ] Reports distributed to stakeholders
- [ ] Failure analysis included
- [ ] Recommendations included
- [ ] Reports archived for audit
- [ ] Trend analysis included

## P2 Medium Priority Checks

### Red-Team Evaluation

- [ ] Red-team evaluation conducted
- [ ] Prompt injection attacks tested
- [ ] Jailbreak attempts tested
- [ ] Data exfiltration attempts tested
- [ ] Tool misuse attempts tested
- [ ] Findings documented and remediated
- [ ] Red-team evaluation repeated quarterly

### Human Evaluation

- [ ] Human evaluation process defined
- [ ] Human evaluators trained
- [ ] Human evaluation samples selected
- [ ] Human evaluation criteria defined
- [ ] Human evaluation results documented
- [ ] Human evaluation informs automated metrics

### Evaluation Governance

- [ ] Evaluation policy reviewed quarterly
- [ ] Thresholds reviewed quarterly
- [ ] Test cases reviewed monthly
- [ ] Test data reviewed monthly
- [ ] Automation maintained regularly
- [ ] Evaluation process improved continuously

### Evaluation Metrics

- [ ] Coverage metrics tracked
- [ ] Quality metrics tracked
- [ ] Performance metrics tracked
- [ ] Process metrics tracked
- [ ] Metrics reported regularly
- [ ] Metrics used for improvement

## P3 Low Priority Checks

### Evaluation Documentation

- [ ] Evaluation procedures documented
- [ ] Test case documentation maintained
- [ ] Threshold rationale documented
- [ ] Failure analysis documented
- [ ] Improvement actions documented
- [ ] Evaluation history archived

### Evaluation Training

- [ ] Evaluation training materials created
- [ ] Team members trained on evaluation
- [ ] Training effectiveness measured
- [ ] Training updated based on findings
- [ ] Training records maintained

### Evaluation Tooling

- [ ] Evaluation tools selected and configured
- [ ] Evaluation tools maintained
- [ ] Evaluation tools upgraded regularly
- [ ] Evaluation tool costs tracked
- [ ] Evaluation tool alternatives evaluated

## Evaluation Lifecycle Checklist

### Design Phase

- [ ] System requirements documented
- [ ] Evaluation requirements derived
- [ ] Evaluation types selected
- [ ] Test cases designed
- [ ] Thresholds defined
- [ ] Policy documented

### Implementation Phase

- [ ] Test datasets created
- [ ] Automation implemented
- [ ] CI/CD integration configured
- [ ] Reporting configured
- [ ] Alerting configured
- [ ] Infrastructure provisioned

### Execution Phase

- [ ] Evaluation runs successfully
- [ ] Results captured correctly
- [ ] Failures logged properly
- [ ] Metrics collected
- [ ] Logs preserved
- [ ] Artifacts archived

### Analysis Phase

- [ ] Results analyzed
- [ ] Failures investigated
- [ ] Root causes identified
- [ ] Impact assessed
- [ ] Patterns identified
- [ ] Recommendations made

### Reporting Phase

- [ ] Reports generated
- [ ] Reports distributed
- [ ] Stakeholders informed
- [ ] Decisions documented
- [ ] Action items created
- [ ] Results archived

### Improvement Phase

- [ ] Improvements identified
- [ ] Test cases updated
- [ ] Thresholds refined
- [ ] Automation enhanced
- [ ] Process improved
- [ ] Learnings shared

## Domain-Specific Checklists

### Safety Evaluation Checklist

- [ ] Harmful content refusal tests: 100% coverage
- [ ] Prompt injection tests: 100% coverage
- [ ] Jailbreak tests: 100% coverage
- [ ] Policy compliance tests: 100% coverage
- [ ] Safety score > 0.95
- [ ] No critical safety failures
- [ ] Safety evaluation blocking on failure

### Quality Evaluation Checklist

- [ ] Task performance tests: > 80% coverage
- [ ] Instruction following tests: > 80% coverage
- [ ] Coherence tests: > 80% coverage
- [ ] Relevance tests: > 80% coverage
- [ ] Quality score > 0.85
- [ ] No quality regressions
- [ ] Quality evaluation blocking on failure

### Performance Evaluation Checklist

- [ ] Latency p95 < 500ms
- [ ] Throughput > 100 rps
- [ ] Error rate < 0.1%
- [ ] Cost per request < $0.01
- [ ] All SLOs met
- [ ] No performance regressions
- [ ] Performance evaluation blocking on failure

### Regression Evaluation Checklist

- [ ] Functional regression tests: 100% pass
- [ ] Performance regression tests: 100% pass
- [ ] Safety regression tests: 100% pass
- [ ] No regressions from baseline
- [ ] Regression evaluation blocking on failure

## Evaluation Evidence Checklist

### Policy Evidence

- [ ] Evaluation policy document
- [ ] Policy approval record
- [ ] Policy review history

### Test Evidence

- [ ] Test case documentation
- [ ] Test dataset documentation
- [ ] Test data version history
- [ ] Test configuration

### Execution Evidence

- [ ] Evaluation execution logs
- [ ] Raw evaluation results
- [ ] Execution timestamps
- [ ] Execution environment details

### Results Evidence

- [ ] Evaluation reports
- [ ] Failure analysis reports
- [ ] Trend analysis reports
- [ ] Comparison reports

### Decision Evidence

- [ ] Release decision records
- [ ] Threshold compliance evidence
- [ ] Exception approvals
- [ ] Action item tracking

## Evaluation Sign-off Checklist

### Pre-Release Sign-off

- [ ] Safety evaluation passed
- [ ] Quality evaluation passed
- [ ] Performance evaluation passed
- [ ] Regression evaluation passed
- [ ] No P0 or P1 failures open
- [ ] All evidence collected
- [ ] Report generated and distributed

### Release Decision Sign-off

- [ ] Evaluation results reviewed
- [ ] Failures analyzed and accepted
- [ ] Risks assessed and documented
- [ ] Stakeholders informed
- [ ] Decision recorded
- [ ] Post-release monitoring configured

### Post-Release Sign-off

- [ ] 24-hour monitoring review completed
- [ ] No production issues detected
- [ ] User feedback monitored
- [ ] Metrics tracked
- [ ] Lessons learned documented
