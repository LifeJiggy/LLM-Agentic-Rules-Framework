# Evaluation Fundamentals - LLM & Agentic Rules Framework

## Overview

This document establishes the fundamental concepts, principles, and requirements for evaluating LLM and agentic systems. Evaluation provides objective evidence of system capabilities, limitations, and compliance with requirements.

## Why Evaluation Matters

### Without Evaluation

- System quality is unknown
- Release decisions are based on gut feeling
- Regressions go undetected
- Safety issues surface in production
- User trust erodes
- Compliance cannot be demonstrated

### With Evaluation

- System quality is measured objectively
- Release decisions are data-driven
- Regressions are caught before release
- Safety issues are identified early
- User trust is built on evidence
- Compliance is demonstrable

## Evaluation Principles

### 1. Comprehensive Coverage

Every aspect of system behavior that matters must be evaluated. Coverage gaps become production surprises.

**Coverage Dimensions**:
- Safety: System prevents harmful outputs
- Quality: System produces accurate, relevant outputs
- Performance: System meets latency and throughput requirements
- Regression: No degradation from baseline
- Edge Cases: System handles unusual inputs gracefully

### 2. Objective Measurement

Evaluation must produce measurable results that can be compared, tracked, and reported.

**Measurement Requirements**:
- Quantitative metrics (scores, rates, times)
- Defined thresholds for pass/fail
- Statistical significance where applicable
- Comparison against baselines
- Trend tracking over time

### 3. Reproducibility

Evaluation results must be reproducible across runs and environments.

**Reproducibility Requirements**:
- Version-controlled test data
- Deterministic evaluation where possible
- Documented evaluation configuration
- Environment parity between runs
- Seed control for random processes

### 4. Timeliness

Evaluation must provide results when decisions need to be made.

**Timeliness Requirements**:
- Pre-release evaluation completes before release decisions
- Continuous monitoring provides real-time visibility
- Regression detection identifies issues immediately
- Performance benchmarks complete within SLA

### 5. Actionability

Evaluation results must lead to clear actions.

**Actionability Requirements**:
- Pass/fail criteria are clear
- Failure analysis identifies root causes
- Remediation guidance is provided
- Follow-up actions are tracked

## Evaluation Types

### Safety Evaluation

**Purpose**: Verify system prevents harmful outputs and resists attacks

**What It Tests**:
- Harmful content refusal
- Toxicity prevention
- Prompt injection resistance
- Jailbreak resistance
- Policy compliance

**When To Run**:
- Before every release
- After prompt changes
- After model updates
- After security incidents

**Success Criteria**:
- Safety score > 0.95
- No critical safety failures
- All attack vectors tested

### Quality Evaluation

**Purpose**: Verify system produces accurate, relevant, and coherent outputs

**What It Tests**:
- Task performance
- Instruction following
- Coherence and relevance
- Factual accuracy
- Context handling

**When To Run**:
- Before every release
- After prompt changes
- After model updates
- Periodically for monitoring

**Success Criteria**:
- Quality score > 0.85
- No quality regressions
- All use cases covered

### Performance Evaluation

**Purpose**: Verify system meets performance SLOs

**What It Tests**:
- Latency (p50, p95, p99)
- Throughput (requests per second)
- Error rate
- Cost per request
- Resource utilization

**When To Run**:
- Before every release
- After infrastructure changes
- Under load testing
- Periodically for monitoring

**Success Criteria**:
- All SLOs met
- No performance regressions
- Cost within budget

### Regression Evaluation

**Purpose**: Verify new changes don't break existing functionality

**What It Tests**:
- Functional regression
- Performance regression
- Safety regression
- Integration regression

**When To Run**:
- Before every release
- After every code change
- After configuration changes
- After dependency updates

**Success Criteria**:
- No regressions detected
- All previous failures covered
- Baseline comparison passed

### Red-Team Evaluation

**Purpose**: Test system defenses against adversarial attacks

**What It Tests**:
- Prompt injection attacks
- Jailbreak attempts
- Data exfiltration attempts
- Tool misuse attempts
- Social engineering

**When To Run**:
- Before initial production deployment
- Quarterly for high-risk systems
- After security incidents
- When new attack vectors emerge

**Success Criteria**:
- Defense success rate > 0.95
- No critical vulnerabilities
- All attack vectors tested

## Evaluation Framework

### Evaluation Policy

```yaml
evaluation_policy:
  system_id: string
  version: string
  owner: string
  
  requirements:
    pre_release:
      - evaluation: string
        threshold: number
        blocking: boolean
    
    continuous:
      - evaluation: string
        frequency: string
        sample_rate: number
  
  coverage:
    safety: number
    quality: number
    performance: number
    regression: number
```

### Evaluation Suite Structure

```yaml
evaluation_suite:
  suite_id: string
  name: string
  type: safety | quality | performance | regression | red_team
  description: string
  
  datasets:
    - name: string
      version: string
      location: string
      samples: integer
  
  tests:
    - test_id: string
      name: string
      input: string
      expected: string
      threshold: number
      priority: string
  
  thresholds:
    overall: number
    by_category: object
```

### Evaluation Results

```yaml
evaluation_results:
  evaluation_id: string
  system_id: string
  version: string
  executed_at: string
  status: pass | fail
  
  summary:
    total_tests: integer
    passed: integer
    failed: integer
    pass_rate: number
  
  suite_results:
    - suite_id: string
      status: pass | fail
      score: number
      threshold: number
  
  failures:
    - test_id: string
      category: string
      severity: string
      description: string
      remediation: string
```

## Evaluation Roles

### ML Engineer

**Responsibilities**:
- Design evaluation suites
- Implement evaluation automation
- Analyze evaluation results
- Investigate failures
- Update evaluation based on findings

### Security Engineer

**Responsibilities**:
- Design safety evaluation
- Conduct red-team evaluation
- Analyze security findings
- Validate security fixes
- Update attack patterns

### QA Engineer

**Responsibilities**:
- Maintain regression suite
- Execute evaluation suites
- Report evaluation results
- Track failure resolution
- Validate fixes

### Product Manager

**Responsibilities**:
- Define quality requirements
- Review evaluation results
- Make release decisions
- Accept or reject risks
- Communicate to stakeholders

## Evaluation Lifecycle

```
Design → Implement → Execute → Analyze → Report → Improve
   ↑                                                   |
   └───────────────────────────────────────────────────┘
```

### 1. Design Phase

**Activities**:
- Define evaluation requirements
- Select evaluation types
- Design test cases
- Define thresholds
- Document evaluation policy

**Outputs**:
- Evaluation policy
- Test case designs
- Threshold definitions
- Dataset requirements

### 2. Implement Phase

**Activities**:
- Create test datasets
- Implement evaluation automation
- Configure evaluation infrastructure
- Set up reporting
- Validate evaluation setup

**Outputs**:
- Automated evaluation suites
- Test datasets
- Evaluation infrastructure
- Reporting dashboards

### 3. Execute Phase

**Activities**:
- Run evaluation suites
- Collect results
- Handle failures
- Retry flaky tests
- Validate execution

**Outputs**:
- Raw evaluation results
- Execution logs
- Failure records

### 4. Analyze Phase

**Activities**:
- Analyze results
- Identify patterns
- Investigate failures
- Determine root causes
- Assess impact

**Outputs**:
- Analysis reports
- Failure investigations
- Root cause analysis
- Impact assessment

### 5. Report Phase

**Activities**:
- Generate reports
- Distribute to stakeholders
- Present findings
- Document decisions
- Archive results

**Outputs**:
- Evaluation reports
- Stakeholder communications
- Decision records
- Archived results

### 6. Improve Phase

**Activities**:
- Identify improvements
- Update test cases
- Refine thresholds
- Enhance automation
- Share learnings

**Outputs**:
- Improvement actions
- Updated test cases
- Refined thresholds
- Enhanced automation
- Knowledge base updates

## Evaluation Metrics

### Coverage Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Test coverage | Percentage of scenarios tested | > 80% |
| Code coverage | Percentage of code exercised | > 80% |
| Requirement coverage | Percentage of requirements tested | 100% P0, > 90% P1 |

### Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Pass rate | Percentage of tests passing | > 95% |
| False positive rate | Incorrectly failed tests | < 5% |
| False negative rate | Incorrectly passed tests | < 1% |
| Flaky test rate | Intermittently failing tests | < 2% |

### Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Evaluation duration | Time to run full suite | < 30 minutes |
| Evaluation cost | Cost per evaluation run | < $10 |
| Evaluation frequency | How often evaluation runs | Per release |

### Process Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Time to report | Time from execution to report | < 1 hour |
| Time to investigate | Time to investigate failures | < 24 hours |
| Time to fix | Time to fix failures | < 72 hours |

## Evaluation Anti-Patterns

### Evaluating Too Late

**Anti-Pattern**: Running evaluation only at release time

**Why It Fails**: Issues discovered late are expensive to fix and delay releases

**Correct Approach**: Run evaluation continuously throughout development

### Skipping Safety Evaluation

**Anti-Pattern**: Skipping safety evaluation due to time pressure

**Why It Fails**: Safety issues in production cause harm and liability

**Correct Approach**: Never skip safety evaluation, escalate if it fails

### Using Unrealistic Test Data

**Anti-Pattern**: Using synthetic data that doesn't represent production

**Why It Fails**: Tests pass in development but fail in production

**Correct Approach**: Use realistic test data that represents production conditions

### Ignoring Flaky Tests

**Anti-Pattern**: Ignoring intermittently failing tests

**Why It Fails**: Flaky tests erode confidence in evaluation and mask real issues

**Correct Approach**: Fix or quarantine flaky tests promptly

### Not Tracking Trends

**Anti-P-pattern**: Looking at evaluation results in isolation

**Why It Fails**: Gradual degradation goes undetected

**Correct Approach**: Track evaluation metrics over time and alert on trends

## Evaluation Checklist

### Policy and Planning

- [ ] Evaluation policy defined
- [ ] Evaluation types selected
- [ ] Thresholds defined
- [ ] Roles assigned
- [ ] Schedule established

### Test Design

- [ ] Test cases designed
- [ ] Test data prepared
- [ ] Expected outputs defined
- [ ] Edge cases included
- [ ] Adversarial cases included

### Automation

- [ ] Evaluation automation implemented
- [ ] CI/CD integration configured
- [ ] Reporting configured
- [ ] Alerting configured
- [ ] Archival configured

### Execution

- [ ] Evaluation runs successfully
- [ ] Results are reproducible
- [ ] Failures are captured
- [ ] Logs are preserved
- [ ] Metrics are collected

### Analysis and Reporting

- [ ] Results are analyzed
- [ ] Failures are investigated
- [ ] Reports are generated
- [ ] Stakeholders are informed
- [ ] Decisions are documented

### Continuous Improvement

- [ ] Test cases updated based on findings
- [ ] Thresholds refined based on data
- [ ] Automation enhanced based on needs
- [ ] Learnings shared with team
- [ ] Evaluation process improved

## References

- Evaluation best practices: `evaluation-best-practices.md`
- Evaluation anti-patterns: `evaluation-anti-patterns.md`
- Evaluation checklist: `evaluation-checklist.md`
- Evaluation examples: `evaluation-examples.md`
- Evaluation troubleshooting: `evaluation-troubleshooting.md`
- Evaluation advanced: `evaluation-advanced.md`
