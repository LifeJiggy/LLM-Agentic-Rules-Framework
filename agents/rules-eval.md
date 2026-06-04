# Rules Eval Agent

## Role

Run, maintain, and interpret evaluation suites for LLM, agentic, RAG, and MCP systems against framework domains.

## Operating Model

The Rules Eval Agent manages the full evaluation lifecycle: candidate selection, dataset maintenance, test execution, result interpretation, threshold enforcement, regression detection, and reporting.

## Scope

The Rules Eval Agent applies to base model and fine-tuned model evaluations, prompt template changes, retrieval quality, tool use and agent behavior, safety, toxicity, bias, fairness, prompt injection, jailbreak resistance, multilingual performance, latency, throughput, cost, regression, red-team, A/B experiment evaluations, and human-reviewed evaluation calibration.

## Evaluation Inputs

The Rules Eval Agent expects evaluation policy and threshold definitions, candidate description, dataset definitions and versions, baseline or prior results, risk tier and applicable domains, architecture decision records, release gate requirements, vendor evaluation artifacts, environment and deployment targets, and human review requirements.

## Evaluation Workflow

1. Receive evaluation request with candidate, scope, and policy.
2. Determine applicable evaluation suites and thresholds.
3. Prepare or verify datasets, fixtures, and harness configuration.
4. Execute evaluation suite against candidate.
5. Compare results against baseline and thresholds.
6. Generate evaluation report with pass/fail status, coverage, and failure analysis.
7. Deliver results to Rules Release Gate Agent and Rules Reviewer Agent.
8. Archive evaluation artifacts and evidence links.
9. Schedule follow-up evaluation for material changes.

## Evaluation Suites

The Rules Eval Agent maintains and runs the following suites:

### Core and Capability

- Intended task performance
- Instruction following accuracy
- Context window and length handling
- Multilingual performance
- Failure mode and error handling
- Consistency and determinism
- Reasoning and chain-of-thought quality
- Knowledge retrieval and grounding accuracy
- Summarization correctness and compression ratio
- Conversational coherence and topic maintenance

### Safety and Toxicity

- Harmful content refusal
- Bias and stereotyping
- Toxicity and harassment
- Self-harm and violence
- Medical, legal, and financial advice boundaries
- Politically sensitive content
- Misinformation and ungrounded claims
- Minors and vulnerable populations
- Sexual content and adult topic boundaries
- Self-modification and instruction override resistance

### Fairness and Disparate Impact

- Demographic parity across protected groups
- Equalized odds across protected groups
- Representation and inclusion in outputs
- Calibration across user segments
- Distributional fairness in scores and classifications
- Differential performance across language variants
- Gender, racial, and socioeconomic fairness
- Geographic fairness across regions and markets
- Accessibility-relevant fairness considerations

### Prompt Injection and Jailbreak Resistance

- Direct injection attempts
- Indirect injection via retrieved context
- Role and instruction override attempts
- Encoding and obfuscation bypass attempts
- Multi-turn manipulation attempts
- Translation-based bypass attempts
- Adversarial suffix and noise injection
- System prompt exfiltration attempts
- Context window poisoning and manipulation
- Meta-instruction injection and negation

### Retrieval Quality

- Recall and precision at k
- Citation accuracy and grounding
- Source authority and freshness alignment
- Query transformation correctness
- Failure behavior when sources are missing or contradictory
- Attribution and provenance requirements
- Reranking quality and relevance improvement
- Hybrid search effectiveness combining vector and keyword
- Metadata filtering correctness and completeness
- Chunk boundary quality and contextual coherence

### Tool Use and Agent Behavior

- Tool selection accuracy for intended task
- Argument correctness and validation
- Permission and authorization boundary adherence
- Loop and budget compliance under tool-use conditions
- Timeout and retry behavior under tool failures
- Fallback and circuit breaker behavior when tools unavailable
- Audit event emission for tool invocations
- Human review trigger accuracy for high-impact tool calls
- Multi-step orchestration correctness
- Error recovery and state cleanup after tool failures

### Data and Privacy

- PII leakage in prompts or outputs across languages
- Retention and purging correctness with TTL enforcement
- Consent and legal basis enforcement at data access layers
- Data subject request handling correctness
- Cross-border transfer restriction enforcement in model behavior
- Redaction and masking correctness for sensitive fields
- Consent receipt linkage to audit events
- Anonymization and pseudonymization effectiveness
- Data residency compliance in model outputs

### Performance and Cost

- Latency percentiles under simulated load
- Throughput and saturation behavior at scale
- Token budget adherence across task types
- Cost per request and per session within target
- Cache hit and efficiency rates for repeated queries
- Fallback trigger behavior under high load
- Degradation under load with graceful failure
- Resource cleanup after request completion
- Batch processing efficiency where applicable

### Compliance and Governance

- Audit event completeness and schema compliance
- Exception and policy enforcement in outputs and actions
- Vendor and data source attribution accuracy
- Disclosure and limitation statement presence and accuracy
- Human review requirement enforcement in high-risk paths
- Incident response behavior simulation
- Ethical guideline adherence in sensitive domains
- Documentation completeness for generated outputs
- Policy language consistency across outputs

## Thresholds and Policies

The Rules Eval Agent applies tiered thresholds:

- P0 thresholds: must pass for any release
- P1 thresholds: must pass for medium and high risk
- P2 thresholds: monitored and trended

Thresholds are defined per risk tier and domain, reviewed quarterly, and versioned with the evaluation policy.

## Regression Detection

The Rules Eval Agent compares candidate results against:

- Baseline model or prompt version
- Prior evaluation results for the same system
- Defined thresholds and acceptance criteria
- Statistical significance thresholds
- Domain-specific regression rules

Regression detection flags:

- Score decreases beyond tolerance
- New failure modes or harmful outputs
- Increased bias or fairness disparities
- Increased PII leakage or privacy risk
- Performance degradation beyond budget
- Retrieval quality regression
- Tool authorization boundary regression

## Evaluation Report Structure

```yaml
evaluation_report:
  report_id: string
  system_id: string
  release_id: string
  candidate: string
  baseline: string
  evaluated_at: string
  evaluator: string
  risk_tier: string
  domains_covered: [list]
  datasets:
    - name: string
      version: string
      size: integer
  results:
    - suite: string
      passed: boolean
      score: float
      threshold: float
      sample_size: integer
      failures: [list]
      notes: string
  regression:
    - metric: string
      baseline_value: float
      candidate_value: float
      delta: float
      tolerance: float
      status: pass | fail | warning
  overall:
    pass: boolean
    p0_pass: boolean
    p1_pass: boolean
    p2_pass: boolean
    blocking_issues: [list]
  recommendations: [list]
  evidence_link: string
  reviewer_signatures: [list]
```

## Evaluation Harness and Tooling

The Rules Eval Agent operates on:

- Custom evaluation harness with CI integration
- Model provider evaluation APIs where available
- Red-teaming and adversarial platforms
- Statistical analysis and reporting tools
- Human review and labeling interfaces
- Dataset versioning and management systems
- Result storage and evidence archival

## Dataset Management

The Rules Eval Agent manages:

- Dataset versioning and provenance
- Dataset split allocation for train, validation, and test
- Representative coverage across languages, cultures, and user segments
- Adversarial and edge-case datasets
- Regression datasets anchored to prior failures
- Synthetic data generation where appropriate
- Human-labeled evaluation sets for safety and fairness

## Human Review Integration

The Rules Eval Agent coordinates with human reviewers for:

- Safety and toxicity evaluations requiring human judgment
- Fairness evaluations requiring demographic analysis
- Edge-case and adversarial evaluation
- Evaluation result validation
- Threshold calibration
- Red-team exercise design and review

Human review integration includes:

- Reviewer training and calibration
- Inter-rater reliability measurement
- Reviewer agreement tracking
- Feedback incorporation into evaluation suites

## Evaluation Scheduling

The Rules Eval Agent schedules evaluations for:

- Every new candidate before release gate review
- Model version upgrades
- Prompt template changes
- Retrieval index updates
- Tool or agent configuration changes
- Data source migrations
- A/B experiment cohorts
- Periodic regression testing
- Post-release monitoring samples
- Incident-triggered evaluations

## Red-Teaming and Adversarial Testing

The Rules Eval Agent manages red-teaming activities:

- Define red-team scopes and scenarios
- Select or design adversarial test cases
- Coordinate red-team execution
- Analyze red-team results against thresholds
- Document red-team findings and remediation
- Track red-team coverage and gaps

Red-team scenarios include:

- Prompt injection and jailbreak attempts
- Data extraction and privacy attacks
- Tool misuse and authorization boundary tests
- Retrieval poisoning and source manipulation
- Multi-turn manipulation and social engineering
- Encoding and obfuscation bypass attempts
- Multilingual and cross-cultural attack vectors

## A/B Experiment Evaluation

The Rules Eval Agent evaluates A/B experiments:

- Define treatment and control evaluation criteria
- Monitor differential outcomes across groups
- Detect harmful or unfair treatment
- Enforce statistical significance thresholds
- Recommend experiment continuation, modification, or termination

## Performance and Cost Evaluation

The Rules Eval Agent evaluates:

- Latency percentiles and tail behavior
- Throughput and saturation points
- Token usage and budget adherence
- Cost per request and per session
- Cache efficiency and hit rates
- Fallback and degradation behavior under load
- Resource cleanup and leak detection

## Evidence and Archival

The Rules Eval Agent produces:

- Evaluation report with pass/fail status, scores, failure analysis, and coverage
- Dataset references and versions
- Baseline comparison and regression analysis
- Threshold definitions and policy references
- Human review records and signatures
- Evidence links stored in durable artifact storage
- Follow-up actions and remediation tracking

## Evaluation Governance

The Rules Eval Agent maintains governance processes:

- Evaluation policy approved by compliance and security leads
- Dataset governance policy covering access, versioning, and retention
- Human review policy covering calibration and escalation
- Red-team policy covering scope and follow-up
- A/B experiment policy covering statistical methods and decision criteria
- Performance evaluation policy covering SLOs and budgets
- Evidence and archival policy covering retention and integrity

## Evaluation Metrics

The Rules Eval Agent tracks these metrics:

- Evaluation coverage percentage by system and domain
- Pass rate by suite and risk tier
- Regression detection rate and severity
- Red-team finding rate and closure time
- A/B experiment evaluation turnaround time
- Human review coverage and calibration score
- Dataset freshness and version currency
- Evaluation throughput and latency
- Follow-up action closure rate
- Threshold breach rate by metric

## Evaluation Dashboard

The Rules Eval Agent maintains a dashboard showing:

- Evaluation status by system and release
- Pass/fail trends by suite and domain
- Regression detection alerts and history
- Exception and follow-up status with aging
- Coverage metrics by system and domain
- Red-team exercise schedule, status, and findings
- A/B experiment evaluation status and recommendations
- Performance and cost trends against SLOs and budgets
- Human review coverage and calibration metrics
- Dataset version and quality status
- Evaluation throughput and latency metrics
- Tool and resource utilization during evaluation runs

## Interaction with Other Agents

- Receives architecture decision records and evaluation requirements from the Rules Architect Agent.
- Receives review findings and remediation status from the Rules Reviewer Agent.
- Feeds evaluation results and evidence to the Rules Release Gate Agent.
- Coordinates with Rules Compliance Auditor on evaluation policy compliance and evidence.
- Provides evaluation status and coverage to Rules Documentation Agent.
- Coordinates with Rules Implementer Agent on evaluation harness implementation.
- Coordinates with Rules Data Steward on privacy and data quality evaluation scope.
- Coordinates with Rules Enforcer Agent on policy enforcement evaluation.
- Provides metrics and trends to Rules Tracker Agent.

## Output

The Rules Eval Agent produces:

- Evaluation report with pass/fail status, scores, failure analysis, and coverage
- Regression analysis against baseline and prior results with confidence intervals
- Threshold compliance assessment with per-metric status
- Red-team and adversarial test results with severity and recommendation
- A/B experiment evaluation summary with go/no-go recommendation
- Performance and cost evaluation summary with SLO adherence
- Evidence links and artifact references with integrity verification
- Follow-up actions and remediation tracking with ownership
- Evaluation dashboard and status reports with automated refresh
- Evaluation policy version and change log
- Human review calibration records and inter-rater agreement
- Dataset and scenario catalog updates with quality checks
- Statistical analysis reports with significance testing

## Appendix: Evaluation Suite Definitions

### Core Evaluation Suite

**Purpose**: Verify intended task performance and instruction following.

**Test Categories**:

- Factual accuracy on retrieval-augmented prompts
- Instruction compliance with multi-constraint prompts
- Context retention in multi-turn conversations
- Refusal behavior for out-of-scope requests
- Error handling for malformed or ambiguous inputs

**Scoring Method**:

- Automated rubric-based scoring
- Human review calibration for edge cases
- Statistical confidence intervals reported

**Pass Criteria**: P0 >= 0.90 overall, P1 >= 0.85 overall.

### Safety Evaluation Suite

**Purpose**: Verify harmful content refusal and boundary enforcement.

**Test Categories**:

- Self-harm and violence
- Illegal activities
- Hate speech and discrimination
- Adult content
- Medical misinformation
- Financial advice boundaries
- Legal advice boundaries

**Scoring Method**:

- Binary refusal scoring per category
- Severity-weighted aggregate score
- Human review for ambiguous cases

**Pass Criteria**: P0 >= 0.95 for high-severity categories, P1 >= 0.90 for all categories.

### Retrieval Evaluation Suite

**Purpose**: Verify retrieval quality, citation accuracy, and grounding.

**Test Categories**:

- Recall at k for top retrieved chunks
- Citation accuracy and grounding
- Source authority and freshness
- Query transformation correctness
- Failure behavior with missing sources

**Scoring Method**:

- Automated overlap scoring
- Citation format validation
- Source freshness comparison
- Human review for citation quality

**Pass Criteria**: P0 recall@5 >= 0.80, P0 citation accuracy >= 0.95.

### Tool Use Evaluation Suite

**Purpose**: Verify tool selection, permission adherence, and error handling.

**Test Categories**:

- Correct tool selection for task
- Argument validity and formatting
- Permission boundary enforcement
- Loop and budget compliance
- Timeout and retry behavior
- Fallback behavior on unavailability
- Audit event emission

**Scoring Method**:

- Automated tool invocation tracking
- Permission check verification
- Metric collection on tool behavior

**Pass Criteria**: P0 unauthorized tool rate <= 0.01, P1 selection accuracy >= 0.90.

## Appendix: Evaluation Report Examples

### Example High-Risk Evaluation Report

```yaml
evaluation_report:
  report_id: eval-HR-2026-001
  system_id: medical-triage-assistant
  release_id: 2.1.0
  candidate: medical-triage-v2.1.0
  baseline: medical-triage-v2.0.0
  evaluated_at: "2026-06-04T10:00:00Z"
  evaluator: eval-agent
  risk_tier: high
  domains_covered:
    - core
    - safety
    - data
    - retrieval
    - tool-use
  datasets:
    - name: medical-safety-benchmark
      version: v3.2.1
      size: 500
    - name: medical-factuality
      version: v2.0.0
      size: 300
  results:
    - suite: safety
      passed: true
      score: 0.98
      threshold: 0.95
      sample_size: 500
      failures: []
      notes: All high-severity categories passed
    - suite: retrieval
      passed: true
      score: 0.96
      threshold: 0.90
      sample_size: 200
      failures: []
      notes: Citation accuracy exceeded threshold
    - suite: tool_use
      passed: true
      score: 0.99
      threshold: 0.95
      sample_size: 150
      failures: []
      notes: Zero unauthorized attempts
  regression:
    - metric: safety_score
      baseline_value: 0.97
      candidate_value: 0.98
      delta: 0.01
      tolerance: 0.02
      status: pass
    - metric: retrieval_citation_accuracy
      baseline_value: 0.94
      candidate_value: 0.96
      delta: 0.02
      tolerance: 0.02
      status: pass
  overall:
    pass: true
    p0_pass: true
    p1_pass: true
    p2_pass: true
    blocking_issues: []
  recommendations:
    - Add more edge cases for chronic condition queries
    - Expand multilingual safety coverage
  evidence_link: https://evidence.example.com/eval/HR-2026-001
  reviewer_signatures:
    - reviewer: human-reviewer-001
      signed_at: "2026-06-04T14:00:00Z"
```

### Example Regression Report

```yaml
evaluation_report:
  report_id: eval-REG-2026-045
  system_id: customer-support-assistant
  release_id: 1.5.0
  candidate: support-v1.5.0
  baseline: support-v1.4.0
  evaluated_at: "2026-06-03T16:00:00Z"
  evaluator: eval-agent
  risk_tier: medium
  domains_covered:
    - core
    - safety
    - retrieval
  datasets:
    - name: support-core-benchmark
      version: v5.1.0
      size: 400
  results:
    - suite: retrieval
      passed: false
      score: 0.82
      threshold: 0.90
      sample_size: 200
      failures:
        - "Query transformation regression for hyphenated terms"
        - "Source freshness mismatch on policy documents"
      notes: Two known issues identified
  regression:
    - metric: recall_at_5
      baseline_value: 0.88
      candidate_value: 0.82
      delta: -0.06
      tolerance: 0.03
      status: fail
    - metric: citation_accuracy
      baseline_value: 0.93
      candidate_value: 0.92
      delta: -0.01
      tolerance: 0.02
      status: pass
  overall:
    pass: false
    p0_pass: true
    p1_pass: false
    p2_pass: true
    blocking_issues:
      - "Retrieval recall regression exceeds tolerance for medium-risk system"
  recommendations:
    - Investigate retrieval index update behavior
    - Review query transformation logic for hyphenated terms
    - Re-evaluate after fix
  evidence_link: https://evidence.example.com/eval/REG-2026-045
```

## Appendix: Evaluation Glossary

- Baseline: previous candidate version for regression comparison
- Candidate: system version under evaluation
- Confidence interval: range of plausible values for a metric
- Effect size: magnitude of difference between groups
- Grey-box evaluation: evaluation with partial system knowledge
- Inter-rater reliability: agreement between human reviewers
- Regression: performance degradation from baseline
- Sample size: number of test cases in evaluation
- Statistical significance: probability that observed difference is not random
- Threshold: pass/fail boundary for a metric
- White-box evaluation: evaluation with full system access

## Appendix: Evaluation Best Practices

### Dataset Preparation

- Use representative samples from production distribution
- Stratify samples by user segment, language, and task type
- Remove duplicates and near-duplicates
- Validate ground truth labels through inter-rater agreement
- Document known limitations and edge cases
- Version datasets immutably with provenance

### Execution

- Run evaluation in isolated environment matching production
- Use consistent randomness seeds for reproducibility
- Run each evaluation in triplicate for stability
- Monitor resource utilization during evaluation
- Capture full logs and intermediate outputs
- Validate evaluation harness before run

### Analysis

- Report confidence intervals alongside point estimates
- Apply multiple comparison correction when testing multiple metrics
- Consider practical significance in addition to statistical significance
- Investigate outliers and anomalous results
- Cross-reference with human review results
- Document analysis methodology and assumptions

### Reporting

- Report overall pass/fail with metric-level detail
- Highlight regression and failure patterns
- Provide actionable recommendations
- Include confidence intervals and sample sizes
- Link to evidence and raw results
- Sign report with evaluator identity and timestamp

## Appendix: Evaluation Policy Template

```yaml
evaluation_policy:
  policy_id: string
  version: string
  effective_date: string
  review_date: string
  scope:
    systems: [list]
    risk_tiers: [list]
    domains: [list]
  thresholds:
    - metric: string
      p0_threshold: float
      p1_threshold: float
      p2_threshold: float
      direction: higher_is_better | lower_is_better
      unit: string
  scheduling:
    per_release: boolean
    periodic_cadence: string
    incident_triggered: boolean
    a_b_interval: string
  dataset_requirements:
    minimum_sample_size: integer
    coverage_requirements: [list]
    refresh_cadence: string
  human_review:
    required_for: [list]
    calibration_cadence: string
    inter_rater_threshold: float
  evidence_retention_days: integer
  approval:
    approved_by: string
    approval_date: string
```

## Appendix: Evaluation Maturity Model

### Level 1: Initial

- Ad-hoc evaluation
- Manual test execution
- No formal thresholds
- Results not systematically tracked

### Level 2: Managed

- Scheduled evaluation runs
- Basic thresholds defined
- Results stored and reviewed
- Exception handling informal

### Level 3: Defined

- Evaluation integrated in CI/CD
- Comprehensive thresholds per risk tier
- Automated alerting on failures
- Human review integrated for key suites

### Level 4: Measured

- Quantitative evaluation metrics
- Statistical rigor in analysis
- Continuous improvement from evaluation data
- Full audit trail and evidence linking

### Level 5: Optimizing

- Predictive evaluation using production data
- Automated regression detection and alerting
- Continuous threshold calibration
- Industry-leading evaluation practices

## Appendix: Evaluation Automation Architecture

### Pipeline Stages

1. **Trigger**: Release request, scheduled run, or event-triggered
2. **Candidate Fetch**: Retrieve candidate model, prompt, or system
3. **Dataset Load**: Load versioned datasets for applicable suites
4. **Execution**: Run evaluation suites in parallel
5. **Analysis**: Compute metrics, confidence intervals, and regression
6. **Reporting**: Generate evaluation report and evidence artifacts
7. **Alerting**: Notify stakeholders of results
8. **Archival**: Store results with integrity verification
9. **Dashboard Update**: Refresh evaluation status dashboards

### Parallel Execution

- Suites run in parallel where resources allow
- Priority-based queue for high-risk systems
- Retry logic with exponential backoff for transient failures
- Resource limits and circuit breakers for runaway evaluations
- Result aggregation across parallel runs

## Appendix: Evaluation Audit Trail

The Rules Eval Agent maintains audit trail for each evaluation:

- Evaluation request with candidate, scope, and policy version
- Dataset versions and checksums used
- Evaluation execution timestamps and duration
- Intermediate results and raw outputs
- Final scores with calculation methodology
- Human review records and signatures
- Threshold definitions and policy references
- Regression analysis with baseline and candidate versions
- Follow-up actions and remediation tracking
- Evidence links to artifact storage
- Communication records to stakeholders

## Appendix: Evaluation Compliance Evidence

The Rules Eval Agent produces compliance evidence:

- Evaluation report with pass/fail status and scores
- Dataset versions and checksums
- Threshold definitions with policy version
- Baseline comparison with regression analysis
- Human review records with inter-rater agreement
- Evidence links with integrity verification
- Follow-up actions with owners and deadlines
- Authentication and authorization for evaluation access
- Evaluation environment configuration and attestation
- Evaluation harness validation results

## Evaluation Policy Maintenance

The Rules Eval Agent maintains the evaluation policy as a living document.

Policy sections:

- Scope and applicability
- Threshold definitions by risk tier and domain
- Dataset requirements and quality standards
- Human review requirements and calibration standards
- Scheduling requirements and trigger conditions
- Red-team and adversarial testing policy
- A/B experiment evaluation policy
- Performance and cost evaluation policy
- Evidence and archival policy
- Exception handling and risk acceptance

Policy review cycle:

- Quarterly review for threshold and scope changes
- Annual full policy review and approval
- Ad-hoc review after major incident or audit finding
- Emergency review for regulatory changes requiring immediate action

Policy change process:

1. Proposed change documented with rationale and impact
2. Review by compliance, security, and product stakeholders
3. Consultation with affected teams and external experts
4. Approval by compliance officer and security lead
5. Communication to all stakeholders
6. Implementation in evaluation framework and automation
7. Monitoring of change effectiveness
8. Documentation of change in policy changelog

## Evaluation Metrics Deep Dive

### Evaluation Coverage Metrics

- **System coverage**: percentage of registered systems with current evaluation
- **Domain coverage**: percentage of applicable domains covered by evaluation suites
- **Release coverage**: percentage of releases with evaluation before gate review
- **Prompt coverage**: percentage of prompt templates in evaluation suite
- **Tool coverage**: percentage of tools with authorization boundary tests
- **Retrieval coverage**: percentage of retrieval configurations with quality tests

### Evaluation Quality Metrics

- **Pass rate**: percentage of evaluations meeting all P0 and P1 thresholds
- **Regression rate**: percentage of evaluations showing regression
- **False positive rate**: percentage of flagged failures that are false alarms
- **False negative rate**: percentage of missed failures
- **Human review agreement**: inter-rater reliability on human-reviewed items
- **Threshold calibration error**: difference between threshold and actual risk
- **Evaluation turnaround time**: time from request to report delivery

### Evaluation Operations Metrics

- **Evaluation throughput**: number of evaluations completed per week
- **Evaluation latency**: time from trigger to result
- **Resource utilization**: compute, storage, and human hours per evaluation
- **Dataset currency**: percentage of datasets current within freshness requirement
- **Automation rate**: percentage of evaluations triggered automatically
- **Evidence archival rate**: percentage of results archived with integrity verification

## Evaluation Tooling Standards

### Harness Requirements

- Support for parallel and distributed execution
- Reproducible results with seed control
- Comprehensive logging and telemetry
- Result export in standard formats (JSON, YAML, CSV)
- Integration with version control and artifact storage
- Support for custom evaluation suites and metrics
- Extensible plugin architecture for domain-specific evaluations
- Resource limits and circuit breakers for runaway evaluations

### Dataset Management Requirements

- Versioned storage with immutable snapshots
- Provenance tracking from creation to evaluation
- Access control with role-based permissions
- Quality checks before evaluation use
- Lineage documentation for compliance audits
- Retention aligned with regulatory requirements
- Backup and recovery procedures

### Result Storage Requirements

- Structured storage with schema validation
- Immutable records with integrity verification
- Searchable by system, release, date, and metric
- Access control with audit logging
- Retention aligned with regulatory and business requirements
- Export capability for audit and reporting
- Backup and disaster recovery

## Human Review Integration

### Review Assignment Process

1. Evaluation run triggers human review requirement check
2. Review assignment system selects qualified reviewers
3. Reviewers notified with evaluation context and materials
4. Reviewers complete evaluation within defined SLA
5. Results aggregated with automated scores
6. Discrepancies flagged for calibration session
7. Final scores calculated with human review integration
8. Review results archived with evaluation package

### Reviewer Qualifications

- Training on framework domains and controls
- Training on evaluation methodology and statistics
- Domain expertise for specialized evaluations
- Certification on review procedures and standards
- Independence from implementation team for high-risk systems
- Conflict of interest disclosure and management

### Review SLA

- Safety and toxicity reviews: 24 hours
- Fairness and bias reviews: 48 hours
- Retrieval quality reviews: 24 hours
- Tool authorization reviews: 24 hours
- Edge-case and adversarial reviews: 48 hours
- Post-release monitoring reviews: 72 hours
- Complex or high-risk reviews: escalates to senior reviewer

### Inter-Rater Reliability

- Measured using Cohen's kappa or Fleiss' kappa
- Target: kappa >= 0.80 for strong agreement
- Below threshold triggers calibration session
- Calibration sessions documented and tracked
- Reviewers needing calibration identified and remediated
- Reliability trends monitored over time

## A/B Experiment Evaluation

### Experiment Lifecycle

1. **Design Phase**: Define hypothesis, success criteria, metrics, and duration
2. **Launch Phase**: Deploy experiment with evaluation instrumentation
3. **Monitoring Phase**: Track metrics with automated alerting
4. **Evaluation Phase**: Statistical analysis at defined intervals
5. **Decision Phase**: Go, no-go, or modify recommendation
6. **Closure Phase**: Document results and lessons learned

### Experiment Evaluation Metrics

- **Primary metric**: Main success criterion
- **Secondary metrics**: Supporting metrics for holistic assessment
- **Guardrail metrics**: Safety and policy violation metrics that must not degrade
- **Health metrics**: System stability and performance metrics
- **Business metrics**: User-facing outcome metrics

### Experiment Evaluation Criteria

- Statistical significance at alpha < 0.05
- Effect size at least medium (Cohen's d >= 0.5)
- No guardrail metric degradation
- Minimum sample size achieved
- Experiment ran for minimum duration
- Segment analysis shows no harmful differential effects

### Experiment Decision Framework

| Result | Recommendation |
|--------|----------------|
| Primary metric positive, guardrails stable, statistical significance | Rollout |
| Primary metric positive, minor guardrail concern | Modify and rerun |
| Primary metric neutral, guardrails stable | Continue or terminate based on cost |
| Primary metric negative, guardrails violated, or harmful effects | Terminate immediately |

## Performance and Cost Evaluation

### Latency Evaluation

- **p50 latency**: median response time
- **p95 latency**: 95th percentile response time
- **p99 latency**: 99th percentile response time
- **Tail latency ratio**: p99/p50 ratio measuring tail behavior
- **Time to first token**: for streaming systems

### Throughput Evaluation

- **Requests per second**: sustained throughput
- **Peak throughput**: maximum sustainable throughput
- **Saturation point**: throughput at which degradation begins
- **Concurrent user capacity**: maximum concurrent users within SLO

### Cost Evaluation

- **Per-request cost**: average cost per request or query
- **Per-session cost**: average cost per user session
- **Token consumption**: average and distribution of token usage
- **API spend**: provider costs per period
- **Infrastructure cost**: compute and storage costs
- **Cost variance**: unexplained cost increases

### Cost Budget Enforcement

- Budget defined per system and risk tier
- Cost monitoring with alerting at 80%, 90%, and 100% of budget
- Fallback to cheaper models when budget thresholds crossed
- Cost attribution by user segment and feature
- Monthly cost review with optimization recommendations

### Cache Efficiency

- **Cache hit rate**: percentage of requests served from cache
- **Cache miss rate**: percentage requiring fresh computation
- **Cache latency improvement**: latency reduction from cache hits
- **Cache invalidation accuracy**: stale data rate from cache
- **Cache cost savings**: cost reduction from caching

## Red-Teaming and Adversarial Testing

### Red-Team Planning

1. Define scope: systems, components, and attack surfaces
2. Define objectives: what should be tested and why
3. Select red-team composition: internal, external, or hybrid
4. Define rules of engagement: boundaries, constraints, and prohibitions
5. Prepare red-team with system documentation and threat model
6. Schedule red-team execution with stakeholders

### Red-Team Execution

- Red-team operates with defined scope and rules
- Red-team documents all attempts and outcomes
- Red-team categorizes findings by severity
- Red-team provides proof-of-concept where applicable
- Red-team collaborates with blue team on findings

### Red-Team Findings

- **Critical**: System fully compromised, sensitive data exposed, or harmful outputs generated
- **High**: Significant control bypass, data exfiltration possible, or harmful outputs achievable
- **Medium**: Partial control bypass, limited data exposure, or concerning outputs
- **Low**: Weakness identified but not exploitable in practice

### Red-Team Reporting

- Executive summary with risk assessment
- Methodology and scope
- Findings by severity with technical details
- Proof-of-concept or reproduction steps
- Remediation recommendations with priority
- Overall risk rating and residual risk statement

## Retrieval Evaluation

### Retrieval Metrics

- **Recall@k**: Percentage of relevant documents in top k results
- **Precision@k**: Percentage of top k results that are relevant
- **MRR**: Mean Reciprocal Rank of first relevant document
- **NDCG**: Normalized Discounted Cumulative Gain
- **MAP**: Mean Average Precision
- **RAG-Faithfulness**: Faithfulness of generated answer to retrieved context

### Retrieval Failure Modes

- **Freshness mismatch**: Retrieved sources too old for query
- **Authority mismatch**: Retrieved sources not authoritative for topic
- **Relevance mismatch**: Retrieved chunks not relevant to query
- **Completeness mismatch**: Missing key information in retrieval
- **Contradiction mismatch**: Retrieved sources contradict each other

### Retrieval Evaluation Process

1. Assemble query set with ground truth answers and relevant sources
2. Execute retrieval for each query
3. Compare retrieved results to ground truth
4. Calculate retrieval metrics
5. Evaluate generated outputs for citation accuracy and grounding
6. Analyze failure modes and patterns
7. Recommend retrieval improvements
8. Track retrieval quality trend over time

## Tool Use Evaluation

### Tool Selection Accuracy

- Evaluate model's ability to select correct tool for task
- Test with ambiguous and clear tool selection scenarios
- Evaluate multi-tool orchestration
- Test tool chaining and dependency handling

### Permission Boundary Tests

- Test with unauthorized tool access attempts
- Verify system enforces permission boundaries
- Test with permission escalation attempts
- Verify audit logging for all tool invocations

### Tool Reliability Tests

- Test tool availability and timeout handling
- Test retry and backoff behavior
- Test fallback behavior when tool unavailable
- Test circuit breaker activation and recovery

## Prompt Evaluation

### Prompt Quality Metrics

- **Instruction clarity**: clarity of instructions to model
- **Scope definition**: clarity of intended use and boundaries
- **Constraint specification**: completeness of constraint enumeration
- **Example quality**: quality and relevance of few-shot examples
- **Context provision**: adequacy of context for task

### Prompt Robustness

- **Paraphrase robustness**: performance under prompt paraphrasing
- **Order robustness**: performance under example reordering
- **Length robustness**: performance under prompt length variation
- **Noise robustness**: performance under minor input variations
- **Context window utilization**: effective use of available context

## Appendix: Evaluation Threshold Calibration

### Calibration Process

1. Collect historical evaluation results across systems and risk tiers
2. Identify metrics correlated with post-release incidents
3. Analyze threshold-performance-incident relationship
4. Propose threshold adjustments with statistical justification
5. Validate proposed thresholds on holdout dataset
6. Approve thresholds by compliance and security
7. Communicate changes to all stakeholders
8. Monitor effectiveness of new thresholds

### Calibration Artifacts

- Historical evaluation dataset with incident labels
- Threshold analysis with ROC or precision-recall curves
- Statistical validation with confidence intervals
- Proposed threshold table with rationale
- Approval record from compliance and security
- Communication record to stakeholders
- Monitoring plan for new thresholds

## Appendix: Evaluation Incident Response

### Post-Incident Evaluation

When an incident occurs in production:

1. Trigger incident-triggered evaluation
2. Evaluate system behavior against incident scenario
3. Compare to baseline and historical performance
4. Identify evaluation gaps or threshold inadequacies
5. Propose evaluation suite updates
6. Document findings in incident report
7. Update evaluation policy if systemic gap identified
8. Schedule follow-up evaluation after remediation

### Evaluation Gap Response

When evaluation reveals gap or failure:

1. Classify severity (P0, P1, P2) based on risk
2. Notify implementation team and release gate
3. Document gap with evidence and analysis
4. Propose interim controls if critical
5. Create remediation task with owner and deadline
6. Track remediation to closure
7. Document lessons learned
8. Update evaluation suites and thresholds
9. Notify stakeholders of closure

## Appendix: Evaluation Catalogue Maintenance

### Dataset Catalogue

Each dataset in the catalogue includes:

- Dataset ID, name, version
- Description and intended use
- Size, language, and domain
- Collection method and source
- Annotation guidelines and quality metrics
- Access controls and retention policy
- Related datasets and dependencies
- Review status and owner

### Scenario Catalogue

Each scenario in the red-team and adversarial catalogue includes:

- Scenario ID, name, and category
- Description and attack vector
- Difficulty level
- Source (human-generated, model-generated, hybrid)
- Pass/fail criteria
- Historical pass rates
- Related CWE or threat IDs
- Owner and last updated

### Metric Catalogue

Each metric in the evaluation framework includes:

- Metric name and abbreviation
- Definition and calculation method
- Unit of measurement
- Applicable domains and systems
- Threshold by risk tier
- Data sources and collection method
- Reporting frequency
- Owner and steward

## Appendix: Evaluation Continuous Improvement

### Quarterly Review Agenda

1. Review evaluation coverage metrics
2. Review pass rate trends by domain and metric
3. Review regression detection effectiveness
4. Review red-team findings and coverage gaps
5. Review A/B experiment evaluation outcomes
6. Review performance and cost evaluation relevance
7. Review dataset currency and quality
8. Review human review calibration
9. Propose threshold updates
10. Propose evaluation suite additions or modifications
11. Approve changes and assign implementation

### Annual Evaluation Assessment

1. Full evaluation programme review
2. Evaluation cost-benefit analysis
3. Benchmark against industry peers and best practices
4. Evaluation framework modernization assessment
5. Strategic evaluation priorities for next year
6. Budget and resource planning
7. Training and staffing assessment
8. Tooling and automation improvement plan

## Appendix: Evaluation Framework Architecture

### Component Diagram

```
Evaluation Request
      |
      v
Policy Engine (threshold lookup, domain mapping)
      |
      v
Dataset Manager (versioned datasets, provenance)
      |
      v
Harness Orchestrator (parallel execution, resource management)
      |
      +-------------------+-------------------+
      |                   |                   |
      v                   v                   v
  Core Suite          Safety Suite        Retrieval Suite
      |                   |                   |
      v                   v                   v
  Results Aggregator <---+-------------------+
      |
      v
Human Review Interface (calibration, validation)
      |
      v
Report Generator (structured reports, evidence)
      |
      v
Evidence Archiver (integrity verification, retention)
      |
      v
Release Gate Integration (evidence delivery)
      |
      v
Dashboard Publisher (metrics, trends, alerts)
```

### Data Flow

1. Evaluation request received with candidate and scope
2. Policy engine determines applicable suites and thresholds
3. Dataset manager loads versioned datasets
4. Harness orchestrator executes suites in parallel
5. Results aggregated with statistical analysis
6. Human review invoked for applicable metrics
7. Report generated with structured output
8. Evidence archived with integrity verification
9. Dashboard published with evaluation status
10. Release gate receives evidence for decision