# Testing Rules Summary - LLM & Agentic Rules Framework

## Overview

This document summarizes the testing rules for LLM and agentic systems. The Testing domain establishes requirements for quality assurance, evaluation, and verification throughout the AI system lifecycle.

## P0 Critical Rules

### TEST-001: Evaluation Coverage Thresholds

**Rule**: AI systems must have evaluation suites that meet defined coverage thresholds for safety, quality, and performance.

**Why It Matters**: Without evaluation, system quality is unknown. Coverage thresholds ensure critical areas are tested before production deployment.

**Coverage Requirements**:
- Safety evaluation: 100% of critical scenarios covered
- Quality evaluation: > 80% of intended use cases covered
- Performance evaluation: All SLOs tested
- Regression evaluation: All previous failures covered

**Implementation Requirements**:
- Define evaluation policy with suite selection
- Maintain evaluation datasets with versioning
- Run evaluation suite before each release
- Track coverage metrics over time
- Update evaluation suites when system changes
- Document coverage gaps and mitigations

**Evidence Required**:
- Evaluation policy document
- Evaluation dataset documentation
- Coverage metrics reports
- Gap analysis and mitigation documentation

### TEST-002: Regression Suite Maintenance

**Rule**: Regression test suites must be maintained to prevent quality degradation across releases.

**Why It Matters**: Without regression testing, previously working functionality can break without detection. Regression suites protect against quality degradation.

**Implementation Requirements**:
- Maintain regression test suite
- Update regression tests when functionality changes
- Run regression suite before each release
- Track regression test results over time
- Investigate and fix regressions promptly
- Archive regression test history

**Regression Test Types**:
- Functional regression: Verify functionality works as expected
- Performance regression: Verify performance meets SLOs
- Safety regression: Verify safety controls remain effective
- Integration regression: Verify integrations work correctly

**Evidence Required**:
- Regression test suite documentation
- Regression test results
- Regression investigation records
- Fix verification records

### TEST-003: Safety Test Inclusion

**Rule**: All releases must include safety tests that verify harmful content prevention and policy compliance.

**Why It Matters**: Safety is non-negotiable. Safety tests verify that system guardrails work correctly and prevent harmful outputs.

**Safety Test Categories**:
- Harmful content refusal: System refuses to generate harmful content
- Toxicity prevention: System avoids generating toxic content
- Prompt injection resistance: System resists prompt injection attacks
- Jailbreak resistance: System resists jailbreak attempts
- Policy compliance: System adheres to defined policies

**Implementation Requirements**:
- Define safety test suite
- Maintain safety test datasets
- Run safety tests before each release
- Track safety test results
- Investigate safety test failures immediately
- Update safety tests based on new threats

**Evidence Required**:
- Safety test suite documentation
- Safety test results
- Safety failure investigation records
- Safety test update history

## P1 High Priority Rules

### TEST-004: Performance Benchmarks

**Rule**: AI systems must have performance benchmarks that verify SLO compliance.

**Why It Matters**: Performance directly impacts user experience. Benchmarks provide objective evidence of performance characteristics.

**Performance Metrics to Benchmark**:
- Latency (p50, p95, p99)
- Throughput (requests per second)
- Error rate
- Token throughput
- Cost per request
- Availability

**Implementation Requirements**:
- Define performance benchmarks
- Establish performance baselines
- Run benchmarks before each release
- Compare results against baselines
- Alert on performance regression
- Track performance trends

**Evidence Required**:
- Performance benchmark definitions
- Baseline documentation
- Benchmark results
- Trend analysis

### TEST-005: Test Environment Parity

**Rule**: Test environments must closely match production environments to ensure test validity.

**Why It Matters**: Tests in environments that differ from production may not accurately predict production behavior. Environment parity reduces surprises.

**Parity Requirements**:
- Same infrastructure configuration
- Same dependencies and versions
- Similar data volume and patterns
- Similar network conditions
- Similar security controls

**Implementation Requirements**:
- Document production environment configuration
- Mirror configuration in test environments
- Validate environment parity regularly
- Use infrastructure as code for consistency
- Monitor environment drift

**Evidence Required**:
- Environment configuration documentation
- Parity validation results
- Drift monitoring reports

## P2 Medium Priority Rules

### TEST-006: Test Data Management

**Rule**: Test data must be managed to ensure privacy, quality, and reproducibility.

**Why It Matters**: Test data affects test validity and may contain sensitive information. Proper management ensures tests are reliable and compliant.

**Implementation Requirements**:
- Use synthetic data where possible
- Anonymize production data for testing
- Version test datasets
- Document test data provenance
- Control test data access
- Refresh test data periodically

**Evidence Required**:
- Test data management policy
- Anonymization procedures
- Data versioning records
- Access control documentation

### TEST-007: Test Reporting

**Rule**: Test results must be documented and reported to relevant stakeholders.

**Why It Matters**: Test results inform release decisions. Without reporting, stakeholders cannot assess system quality.

**Implementation Requirements**:
- Generate test reports for each test run
- Include pass/fail status and metrics
- Report test coverage
- Highlight failures and regressions
- Distribute reports to stakeholders
- Archive test reports

**Evidence Required**:
- Test report templates
- Sample test reports
- Distribution records
- Archive location

### TEST-008: Test Automation CI/CD

**Rule**: Test automation must be integrated into CI/CD pipelines to ensure consistent execution.

**Why It Matters**: Manual testing is slow, error-prone, and doesn't scale. Automation ensures tests run consistently and quickly.

**Implementation Requirements**:
- Automate unit tests in CI pipeline
- Automate integration tests in CI/CD pipeline
- Automate evaluation suite in release pipeline
- Automate security scans in CI pipeline
- Track automation coverage
- Maintain automation scripts

**Evidence Required**:
- CI/CD pipeline configuration
- Automation script repository
- Automation coverage metrics
- Automation maintenance records

## Evaluation Types

### Safety Evaluation

**Purpose**: Verify system prevents harmful outputs and resists attacks

**Test Categories**:
- Harmful content refusal
- Toxicity prevention
- Prompt injection resistance
- Jailbreak resistance
- Policy compliance

**Success Criteria**:
- Safety score > 0.95
- No critical safety failures
- All attack vectors tested

### Quality Evaluation

**Purpose**: Verify system produces accurate, relevant, and coherent outputs

**Test Categories**:
- Task performance
- Instruction following
- Coherence and relevance
- Factual accuracy
- Context handling

**Success Criteria**:
- Quality score > 0.85
- No quality regressions
- All use cases covered

### Performance Evaluation

**Purpose**: Verify system meets performance SLOs

**Test Categories**:
- Latency testing
- Throughput testing
- Load testing
- Stress testing
- Cost testing

**Success Criteria**:
- All SLOs met
- No performance regressions
- Cost within budget

### Regression Evaluation

**Purpose**: Verify new changes don't break existing functionality

**Test Categories**:
- Functional regression
- Performance regression
- Safety regression
- Integration regression

**Success Criteria**:
- No regressions detected
- All previous failures covered
- Baseline comparison passed

### Red-Team Evaluation

**Purpose**: Test system defenses against adversarial attacks

**Test Categories**:
- Prompt injection attacks
- Jailbreak attempts
- Data exfiltration attempts
- Tool misuse attempts
- Social engineering

**Success Criteria**:
- Defense success rate > 0.95
- No critical vulnerabilities
- All attack vectors tested

## Testing Anti-Patterns

### Skipping Safety Tests

**Anti-Pattern**: Releasing without running safety tests due to time pressure.

**Why It Fails**: Safety failures can cause harm, legal liability, and reputational damage. Time pressure doesn't reduce safety requirements.

**Correct Approach**: Include safety tests in mandatory release pipeline. Never skip safety tests. Escalate if safety tests fail.

### Inadequate Test Data

**Anti-Prompt**: Using unrealistic or insufficient test data that doesn't represent production conditions.

**Why It Fails**: Tests may pass in development but fail in production. Edge cases and real-world patterns are missed.

**Correct Approach**: Use realistic test data that represents production conditions. Include edge cases and adversarial examples. Refresh test data regularly.

### Ignoring Test Failures

**Anti-Pattern**: Ignoring test failures or marking them as known issues without investigation.

**Why It Fails**: Uninvestigated failures may indicate real problems. Known issues can accumulate and cause incidents.

**Correct Approach**: Investigate all test failures. Determine root cause. Fix issues or document accepted risks with mitigation.

### Manual Testing Only

**Anti-Pattern**: Relying solely on manual testing without automation.

**Why It Fails**: Manual testing is slow, error-prone, and doesn't scale. It cannot keep up with release frequency.

**Correct Approach**: Automate tests in CI/CD pipeline. Use manual testing for exploratory and usability testing only.

## Testing Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Evaluation coverage | > 80% | Coverage report |
| Regression test pass rate | 100% | Test results |
| Safety test pass rate | 100% | Test results |
| Performance benchmarks met | 100% | Benchmark results |
| Test automation coverage | > 90% | CI/CD metrics |
| Test execution time | < 30 minutes | Pipeline metrics |
| Test data freshness | < 30 days | Data management |
| Test report completion | 100% | Reporting metrics |

## Cross-Domain Dependencies

The Testing domain interacts with other domains:

| Domain | Testing Dependency | Interaction |
|--------|-------------------|-------------|
| Core | TEST-001 | Evaluation requirements inform core testing |
| Security | TEST-003 | Safety testing is security testing |
| Data | TEST-006 | Test data management affects data governance |
| Integration | TEST-005 | Environment parity affects integration testing |
| Operations | TEST-008 | CI/CD automation supports operations |
| Documentation | TEST-007 | Test reporting requires documentation |
| Performance | TEST-004 | Performance benchmarks are performance testing |
| Compliance | TEST-001, TEST-003 | Evaluation and safety tests support compliance |

## References

- Testing domain fundamentals: `domains/07-testing/fundamentals.md`
- Testing domain best practices: `domains/07-testing/best-practices.md`
- Testing domain anti-patterns: `domains/07-testing/anti-patterns.md`
- Testing domain checklist: `domains/07-testing/checklist.md`
- Testing domain examples: `domains/07-testing/examples.md`
- Testing domain troubleshooting: `domains/07-testing/troubleshooting.md`
- Testing domain advanced: `domains/07-testing/advanced.md`
