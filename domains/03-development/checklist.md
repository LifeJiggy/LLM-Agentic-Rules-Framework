# Development Domain - Checklist

## Overview

This checklist verifies development best practices are followed throughout the agent lifecycle, covering architecture, implementation, testing, deployment, and maintenance phases.

---

## Priority Guide

| Priority | Description |
|----------|-------------|
| P0 | Required for production stability and security |
| P1 | Required for maintainable production delivery |
| P2 | Recommended for code quality |
| P3 | Useful refinement for developer experience |

---

## Pre-Development Checklist

### Requirements and Planning
- [ ] P0: Functional requirements clearly defined
- [ ] P0: Non-functional requirements specified (performance, scalability, security)
- [ ] P1: API contracts documented before implementation
- [ ] P1: Data models designed and reviewed
- [ ] P1: Architecture diagram created and validated
- [ ] [ ] P1: Security requirements identified (see security domain)
- [ ] P2: Technology stack chosen with justification
- [ ] P2: Development environment setup documented

---

## Implementation Checklist

### Code Quality
- [ ] P0: All code follows project style guide
- [ ] P0: Functions are small and focused (< 50 lines)
- [ ] P0: Error handling implemented for all external calls
- [ ] P0: No hardcoded secrets or configuration
- [ ] P0: Input validation on all external boundaries
- [ ] P1: Type hints used consistently
- [ ] P1: Docstrings for all public functions and classes
- [ ] P1: No global mutable state
- [ ] P2: DRY principles followed (no copy-paste code)
- [ ] P2: Appropriate design patterns used
- [ ] P3: Code complexity metrics within thresholds

---

## Testing Checklist

### Test Coverage
- [ ] P0: Unit tests for all business logic
- [ ] P0: Integration tests for external service interactions
- [ ] P1: Property-based tests for edge cases
- [ ] P1: Security tests for injection attacks
- [ ] P2: End-to-end tests for critical workflows
- [ ] P2: Performance tests for latency requirements
- [ ] P2: Load tests for throughput requirements

---

## Deployment Checklist

### Pre-Deployment
- [ ] P0: All tests passing
- [ ] P0: Code builds successfully
- [ ] P0: No critical security vulnerabilities
- [ ] P1: Documentation updated
- [ ] P1: Migration scripts tested if database changes
- [ ] P1: Rollback plan documented
- [ ] P2: Smoke tests defined for post-deployment

---

## Maintenance Checklist

### Ongoing Care
- [ ] P1: Regular dependency updates
- [ ] P1: Periodic security audits
- [ ] P2: Performance monitoring in place
- [ ] P2: Technical debt tracked

---

## Code Review Checklist

### Before Merge
- [ ] P0: No placeholder code
- [ ] P0: No hardcoded values
- [ ] P0: Proper naming conventions
- [ ] P1: Tests included for changes
- [ ] P1: Documentation updated
- [ ] P2: Code complexity appropriate
- [ ] P2: Security considerations addressed

---

## Sign-Off

Before marking as complete:
- [ ] All P0 items verified
- [ ] P1 items addressed or documented exceptions
- [ ] Peer review completed
- [ ] Tests passing

---

## Phase 2: LLM-Specific Development Checklist

### 2.1 Prompt Engineering Review

- [ ] P0: System prompts hardened against extraction
- [ ] P0: User input isolation enforced in prompt construction
- [ ] P0: Context window limits implemented
- [ ] P0: Temperature settings appropriate for use case
- [ ] P1: Prompt versioning implemented
- [ ] P1: A/B testing framework for prompts
- [ ] P1: Prompt templates parameterized correctly
- [ ] P2: Multi-turn context handling tested
- [ ] P2: Prompt injection tests included

### 2.2 Tool Integration Review

- [ ] P0: All tool invocations authorized
- [ ] P0: Tool arguments validated before execution
- [ ] P0: Tool execution sandboxed appropriately
- [ ] P0: Tool errors don't leak sensitive information
- [ ] P1: Tool allowlist enforced
- [ ] P1: Tool rate limiting implemented
- [ ] P1: Tool timeout handling configured
- [ ] P2: Tool result sanitization before context
- [ ] P2: Tool circuit breaker configured

### 2.3 Memory and State Review

- [ ] P0: Session isolation between users enforced
- [ ] P0: Memory expiration configured
- [ ] P0: Sensitive data excluded from memory
- [ ] P1: Memory size limits enforced
- [ ] P1: Memory backup/recovery tested
- [ ] P2: Memory encryption at rest

---

## Phase 3: Production Readiness Checklist

### 3.1 Observability

- [ ] P1: Structured logging implemented
- [ ] P1: Metrics for key operations collected
- [ ] P1: Tracing for request flow available
- [ ] P2: Dashboard for key metrics defined
- [ ] P2: Alerting thresholds configured
- [ ] P2: Health check endpoints implemented

### 3.2 Resilience

- [ ] P1: Circuit breaker for external services
- [ ] P1: Retry logic with exponential backoff
- [ ] P1: Graceful degradation for failures
- [ ] P2: Bulkhead pattern for isolation
- [ ] P2: Timeout enforcement on all calls

### 3.3 Performance

- [ ] P2: Caching strategy defined
- [ ] P2: Connection pooling configured
- [ ] P2: Async processing where appropriate
- [ ] P3: Performance benchmarks established

---

## Phase 4: Security Development Checklist

### 4.1 Input Security

- [ ] P0: All external inputs validated
- [ ] P0: Prompt injection patterns blocked
- [ ] P0: SQL injection prevented
- [ ] P0: XSS attacks prevented in outputs
- [ ] P1: File upload validation implemented
- [ ] P1: URL validation and allowlisting
- [ ] P1: Unicode normalization applied
- [ ] P2: Content-type validation enforced

### 4.2 Output Security

- [ ] P0: PII detection in outputs
- [ ] P0: Secret detection in outputs
- [ ] P1: Output filtering implemented
- [ ] P1: Response redaction for sensitive data
- [ ] P2: Output length limits enforced

### 4.3 Configuration Security

- [ ] P0: Secrets loaded from secure sources
- [ ] P0: No secrets in logs
- [ ] P1: Secrets rotation implemented
- [ ] P1: Environment variable validation
- [ ] P2: Configuration encryption at rest

---

## Phase 5: Testing Strategy Checklist

### 5.1 Unit Testing

- [ ] P1: All pure functions tested
- [ ] P1: All public methods tested
- [ ] P1: Edge cases covered
- [ ] P2: Property-based tests for validation
- [ ] P2: Mutation testing for critical paths

### 5.2 Integration Testing

- [ ] P1: External API mocked appropriately
- [ ] P1: Database migrations tested
- [ ] P1: Authentication flow tested
- [ ] P2: Cross-system integration tested

### 5.3 Security Testing

- [ ] P1: Injection attack tests
- [ ] P1: Authentication bypass tests
- [ ] P1: Authorization testing
- [ ] P2: Fuzzing on inputs
- [ ] P2: Dependency vulnerability scanning

---

## Phase 6: Code Review Checklist

### 6.1 Functional Correctness

- [ ] P0: Requirements traceability verified
- [ ] P0: Edge cases handled
- [ ] P1: Error paths tested
- [ ] P1: Logging adequate but not excessive
- [ ] P2: Performance implications assessed

### 6.2 Code Quality

- [ ] P1: Naming conventions consistent
- [ ] P1: Functions under 50 lines
- [ ] P1: Cyclomatic complexity reasonable
- [ ] P2: DRY principles followed
- [ ] P2: YAGNI principles honored

### 6.3 Security Review

- [ ] P0: OWASP Top 10 considered
- [ ] P0: No hardcoded credentials
- [ ] P1: Authz checks on all endpoints
- [ ] P1: Encryption for sensitive data
- [ ] P2: Security scan integration

---

## Phase 7: Performance and Scaling Checklist

### 7.1 Caching Strategy

- [ ] P1: Response caching implemented
- [ ] P1: Cache TTL configured appropriately
- [ ] P2: Cache key strategy defined
- [ ] P2: Cache miss logging for optimization
- [ ] P2: Cache warming strategy for peak hours

### 7.2 Rate Limiting

- [ ] P0: Per-user rate limiting enforced
- [ ] P0: Per-IP rate limiting enforced
- [ ] P1: Global rate limiting for protection
- [ ] P1: Graceful degradation on rate limit
- [ ] P2: Rate limit override for admin users
- [ ] P2: Rate limit metrics exposed

### 7.3 Timeout Management

- [ ] P0: Model call timeout configured
- [ ] P0: Tool call timeout configured
- [ ] P1: Database query timeout set
- [ ] P1: HTTP request timeout set
- [ ] P2: Timeout propagation across services
- [ ] P2: Timeout metrics collected

---

## Phase 8: Observability Checklist

### 8.1 Logging Standards

- [ ] P1: Structured logging implemented
- [ ] P1: Log levels used appropriately
- [ ] P1: No sensitive data in logs
- [ ] P2: Request correlation IDs
- [ ] P2: Log sampling for high-volume endpoints
- [ ] P2: Log retention policies defined

### 8.2 Metrics Collection

- [ ] P1: Request latency tracked
- [ ] P1: Error rates tracked
- [ ] P1: Resource utilization tracked
- [ ] P2: Business metrics tracked
- [ ] P2: Anomaly detection configured
- [ ] P2: Metric dashboards created

### 8.3 Tracing

- [ ] P2: Request tracing implemented
- [ ] P2: Cross-service trace propagation
- [ ] P2: Trace sampling configured
- [ ] P2: Trace analysis tools available

---

## Phase 9: Data Protection Checklist

### 9.1 Data at Rest

- [ ] P0: Sensitive data encrypted
- [ ] P0: Database connection encrypted
- [ ] P1: File storage encrypted
- [ ] P1: Backup encryption enabled
- [ ] P2: Key rotation implemented
- [ ] P2: Key management audited

### 9.2 Data in Transit

- [ ] P0: TLS for all external calls
- [ ] P0: mTLS for internal calls
- [ ] P1: Certificate pinning for critical APIs
- [ ] P1: HTTPs enforcement in code
- [ ] P2: TLS version restrictions
- [ ] P2: Cipher suite restrictions

### 9.3 PII Handling

- [ ] P0: PII detection in inputs
- [ ] P0: PII redaction in outputs
- [ ] P1: PII access logging
- [ ] P1: PII retention policies
- [ ] P2: PII anonymization options
- [ ] P2: Right-to-delete implementation

---

## Phase 10: Testing Strategy Checklist

### 10.1 Unit Testing

- [ ] P1: All public functions tested
- [ ] P1: All error paths tested
- [ ] P2: Property-based tests added
- [ ] P2: Branch coverage > 80%
- [ ] P3: Mutation testing performed

### 10.2 Integration Testing

- [ ] P1: External API mocks
- [ ] P1: Database transaction tests
- [ ] P1: Message queue integration
- [ ] P2: Cross-service tests
- [ ] P2: Contract tests for APIs
- [ ] P3: Chaos testing

### 10.3 Security Testing

- [ ] P1: Injection attack tests
- [ ] P1: Authentication flow tests
- [ ] P1: Authorization tests
- [ ] P2: Fuzz testing on inputs
- [ ] P2: Vulnerability scanning
- [ ] P3: Penetration testing

---

## Phase 11: Documentation Checklist

### 11.1 API Documentation

- [ ] P1: OpenAPI spec generated
- [ ] P1: Endpoint examples provided
- [ ] P2: Error response documented
- [ ] P2: Authentication documented
- [ ] P2: Rate limits documented

### 11.2 Architecture Documentation

- [ ] P2: Component diagrams
- [ ] P2: Data flow diagrams
- [ ] P2: Deployment diagrams
- [ ] P3: Sequence diagrams for key flows
- [ ] P3: Architecture decision records

### 11.3 Operational Documentation

- [ ] P2: Runbooks for incidents
- [ ] P2: Rollback procedures
- [ ] P2: Scaling procedures
- [ ] P3: Disaster recovery plan
- [ ] P3: Upgrade procedures

---

## Phase 12: Deployment Checklist

### 12.1 Container Security

- [ ] P1: Non-root user in container
- [ ] P1: Minimal base image
- [ ] P2: Distroless image considered
- [ ] P2: Image scanning enabled
- [ ] P2: SBOM generated

### 12.2 Infrastructure

- [ ] P1: Resource limits set
- [ ] P1: Health checks configured
- [ ] P2: Auto-scaling configured
- [ ] P2: Network policies defined
- [ ] P2: Secrets injection configured

### 12.3 Release Validation

- [ ] P1: Smoke tests pass
- [ ] P1: Migration tests pass
- [ ] P2: Canary deployment used
- [ ] P2: Rollback tested
- [ ] P3: Blue-green deployment used

---

## Phase 13: Incident Response Checklist

### 13.1 Detection

- [ ] P1: Alert thresholds defined
- [ ] P1: Escalation contacts listed
- [ ] P2: Anomaly detection configured
- [ ] P2: Log alert queries defined
- [ ] P3: Automated escalation configured

### 13.2 Response

- [ ] P1: Runbook for critical alerts
- [ ] P1: Communication plan documented
- [ ] P2: War room setup procedure
- [ ] P2: Stakeholder notification list
- [ ] P3: External communication template

### 13.3 Post-Incident

- [ ] P2: Post-mortem template
- [ ] P2: Root cause analysis process
- [ ] P3: Action item tracking
- [ ] P3: Incident metrics dashboard

---

## Phase 14: Code Quality Checklist

### 14.1 Naming Conventions

- [ ] P1: Class names are PascalCase
- [ ] P1: Function names are snake_case
- [ ] P1: Constants are UPPER_SNAKE_CASE
- [ ] P2: Variable names are descriptive
- [ ] P2: Abbreviations documented
- [ ] P3: Domain-specific terminology consistent

### 14.2 Code Organization

- [ ] P1: Files under 400 lines
- [ ] P1: Functions under 50 lines
- [ ] P1: Cyclomatic complexity < 10
- [ ] P2: Module cohesion high
- [ ] P2: Circular dependencies avoided
- [ ] P3: Code duplication < 5%

---

## Phase 15: Refactoring Checklist

### 15.1 Before Refactoring

- [ ] P1: Tests coverage > 80% for changed code
- [ ] P1: Performance baselines captured
- [ ] P2: Business stakeholders informed
- [ ] P2: Refactoring branch created

### 15.2 During Refactoring

- [ ] P1: Small, incremental changes
- [ ] P1: Tests pass after each change
- [ ] P2: Code review on each PR
- [ ] P2: Performance not degraded

### 15.3 After Refactoring

- [ ] P1: All tests passing
- [ ] P1: Code coverage maintained
- [ ] P2: Documentation updated
- [ ] P2: Stakeholder sign-off

---

## Phase 16: Technical Debt Checklist

### 16.1 Debt Identification

- [ ] P2: Code smells documented
- [ ] P2: Performance bottlenecks tracked
- [ ] P2: Manual testing areas noted
- [ ] P2: Known limitations recorded

### 16.2 Debt Management

- [ ] P2: Technical debt register maintained
- [ ] P2: Debt repayment planned quarterly
- [ ] P2: New features account for existing debt
- [ ] P3: Debt metrics tracked

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)