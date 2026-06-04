# Security Domain - Checklist

## Overview

This checklist verifies that security controls are applied to prompts, tools, data handling, authentication, authorization, and runtime operations. It is organized into pre-implementation, implementation, operational, and post-implementation phases. Every item must be addressed before a system is considered production-ready.

## Priority Guide

| Priority | Description | Acceptance Criteria |
|----------|-------------|---------------------|
| P0 | Required for preventing data exposure, unauthorized access, or unsafe tool use. | Must be fully implemented and tested before production deployment. No exceptions without documented risk acceptance from CISO. |
| P1 | Required for production hardening unless explicitly accepted. | Must be implemented or have a documented mitigation plan with a defined remediation date. |
| P2 | Recommended for defense in depth. | Should be implemented to reduce attack surface and improve security posture. |
| P3 | Useful refinement for mature security programs. | Beneficial for advanced threat protection and compliance maturity. |

---

## Phase 1: Pre-Implementation Security Checklist

### 1.1 Security Requirements Definition

- [ ] P0: Security requirements documented in the project charter or security specification
- [ ] P0: Regulatory compliance requirements identified (GDPR, CCPA, HIPAA, SOC 2, PCI DSS, etc.)
- [ ] P0: Data classification schema defined (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED)
- [ ] P1: Security acceptance criteria defined for each feature
- [ ] P1: Security risk appetite documented and approved by stakeholders
- [ ] P2: Minimum security standards for all dependencies established
- [ ] P2: Secure coding standards and code review requirements documented
- [ ] P2: Security training requirements for development team defined
- [ ] P3: Security metrics and KPIs established for ongoing monitoring

### 1.2 Threat Modeling

- [ ] P0: Threat model created using STRIDE or equivalent methodology
- [ ] P0: All trust boundaries identified (user-to-agent, agent-to-tool, agent-to-agent, agent-to-external-API)
- [ ] P0: Attack surface inventory completed (entry points, exit points, data flows)
- [ ] P1: Data flow diagrams (DFDs) created for all major workflows
- [ ] P1: Threat model reviewed and approved by security team
- [ ] P1: Threats prioritized by likelihood and impact
- [ ] P2: Threat model includes LLM-specific threats (prompt injection, jailbreak, tool abuse, memory poisoning, context overflow)
- [ ] P2: Mitigation strategies documented for identified threats
- [ ] P2: Software Bill of Materials (SBOM) strategy defined
- [ ] P3: Threat model includes supply chain threats (poisoned training data, malicious plugins, compromised model hosting)
- [ ] P3: Red team exercise plan documented for high-risk features

### 1.3 Security Architecture Documentation

- [ ] P0: High-level security architecture diagram created
- [ ] P0: Authentication and authorization architecture documented
- [ ] P0: Encryption strategy documented (at rest, in transit, in use)
- [ ] P0: Secrets management architecture documented
- [ ] P1: Logging and monitoring architecture defined
- [ ] P1: Incident response architecture documented
- [ ] P1: Network security controls documented (segmentation, firewalls, WAF, network policies)
- [ ] P1: Zero trust architecture principles applied and documented
- [ ] P2: Rate limiting and resource control architecture designed
- [ ] P2: Circuit breaker patterns defined for all external API calls
- [ ] P2: Multi-agent communication security architecture designed
- [ ] P3: Backup and disaster recovery security controls documented

### 1.4 Dependency and Supply Chain Audit

- [ ] P0: All dependencies inventoried with exact versions pinned
- [ ] P0: Automated dependency vulnerability scanning configured
- [ ] P0: License compliance audit completed
- [ ] P1: SBOM generated for all software components
- [ ] P1: Container image scanning configured in CI/CD pipeline
- [ ] P1: Dependency update policy established (monthly reviews, emergency patching process)
- [ ] P2: SAST (Static Application Security Testing) tools configured
- [ ] P2: DAST (Dynamic Application Security Testing) process defined
- [ ] P2: Third-party model integrity verification process defined
- [ ] P3: Software composition analysis (SCA) tool configured
- [ ] P3: Dependency allowlist established for new packages

### 1.5 Security Team and Process Setup

- [ ] P1: Security champion assigned to the development team
- [ ] P1: Security review process defined and communicated
- [ ] P1: Security incident response team identified
- [ ] P2: Security training completed for all developers
- [ ] P2: Bug bounty program considered for production systems
- [ ] P2: Regular security review cadence established (bi-weekly or monthly)

---

## Phase 2: Implementation Security Checklist

### 2.1 Input Validation

- [ ] P0: All user inputs validated at every boundary (API gateway, agent boundary, tool boundary, persistence boundary)
- [ ] P0: Input length limits enforced (text max 4000 chars by default, configurable up to 50000)
- [ ] P0: JSON input validated for depth (max 10) and key count (max 50)
- [ ] P0: File uploads validated for size (max 20MB images, 50MB general), type, and content
- [ ] P0: Audio/video inputs validated for duration and format
- [ ] P0: Prompt injection patterns detected and blocked at input boundary
- [ ] P1: SQL injection prevented (parameterized queries or ORM only)
- [ ] P1: XSS prevented (output encoding, Content-Security-Policy headers)
- [ ] P1: Command injection prevented in tool execution (allowlist-based command validation)
- [ ] P1: Path traversal prevented in file system operations
- [ ] P1: Type confusion prevented with strict type checking at boundaries
- [ ] P1: Template injection prevented in all templated output generation
- [ ] P2: Multimodal inputs validated (OCR text extraction with security awareness, image content validation)
- [ ] P2: XML/HTML entity injection prevented in XML processing
- [ ] P2: Regular expression DoS (ReDoS) patterns prevented in validation logic
- [ ] P2: Null byte and control character injection prevented
- [ ] P2: Unicode normalization applied to all text inputs
- [ ] P3: Input canonicalization enforced to prevent encoding-based attacks
- [ ] P3: Context-specific validation applied based on tool being invoked
- [ ] P3: Semantic validation beyond syntactic validation for structured inputs

### 2.2 Authentication

- [ ] P0: Strong password policies enforced (minimum length 12, complexity requirements)
- [ ] P0: Multi-factor authentication (MFA) implemented for all privileged accounts
- [ ] P0: Session management secure (cryptographically random session IDs, secure cookie flags)
- [ ] P0: Tokens properly managed (short-lived access tokens, refresh token rotation)
- [ ] P0: Account lockout implemented after failed login attempts (5 failures in 15 minutes)
- [ ] P0: JWT tokens validated with proper algorithms (RS256 or HS256), expiration checked
- [ ] P1: Password hashing uses Argon2, bcrypt, or PBKDF2 with sufficient work factor
- [ ] P1: Session timeout implemented (idle timeout 30 min, absolute timeout 8 hours)
- [ ] P1: OAuth2/OIDC integration follows best practices
- [ ] P1: API keys properly authenticated and scoped
- [ ] P1: Service-to-service authentication implemented (mTLS or token-based)
- [ ] P1: Adaptive authentication based on risk signals (new device, new location, unusual time)
- [ ] P2: Credential stuffing protection implemented (rate limiting, breach password checking)
- [ ] P2: Session fixation prevention implemented
- [ ] P2: Cross-site request forgery (CSRF) protection implemented
- [ ] P2: Brute force protection with exponential backoff or CAPTCHA
- [ ] P2: Concurrent session limits enforced per user
- [ ] P2: Authentication events logged with full context (timestamp, IP, user agent, outcome)
- [ ] P3: Passwordless authentication options available (WebAuthn, magic links)
- [ ] P3: Risk-based step-up authentication for sensitive operations

### 2.3 Authorization

- [ ] P0: Least privilege principle applied to all users, services, and agents
- [ ] P0: Role-based access control (RBAC) implemented with clearly defined roles
- [ ] P0: Permission checks enforced on all resources and tool invocations
- [ ] P0: Authorization decisions logged for audit purposes
- [ ] P1: Attribute-based access control (ABAC) considered for fine-grained policies
- [ ] P1: Policy enforcement point (PEP) and policy decision point (PDP) separation implemented
- [ ] P1: Row-level security implemented for database access
- [ ] P1: Field-level access control implemented for sensitive data fields
- [ ] P1: Authorization cached with appropriate TTL for performance
- [ ] P2: Just-in-time (JIT) provisioning for elevated access
- [ ] P2: Least privilege enforced for service accounts and API keys
- [ ] P2: Break-glass procedures documented for emergency access
- [ ] P2: Cross-tenant data isolation enforced in multi-tenant systems
- [ ] P2: Authorization bypass prevention tested with negative test cases
- [ ] P3: Relationship-based access control (ReBAC) for complex organizational hierarchies
- [ ] P3: Continuous authorization re-evaluation for long-running operations

### 2.4 Data Protection

- [ ] P0: Sensitive data encrypted at rest (AES-256-GCM or equivalent)
- [ ] P0: Data encrypted in transit (TLS 1.3 minimum, TLS 1.2 minimum required)
- [ ] P0: Secrets properly managed (vault integration, no hardcoded secrets, no secrets in logs)
- [ ] P0: Data retention policies enforced with automatic deletion
- [ ] P0: PII detection and redaction implemented across all data flows
- [ ] P1: Key derivation uses Argon2, scrypt, or PBKDF2 with appropriate work factors
- [ ] P1: Key rotation policy implemented and automated (90 days for API keys, 180 days for signing keys)
- [ ] P1: Secrets never logged, even in debug mode
- [ ] P1: Database connections encrypted (TLS for database connections)
- [ ] P1: Backup data encrypted with separate keys from production
- [ ] P1: Data classification labels applied to all stored data
- [ ] P1: Encryption keys stored separately from encrypted data
- [ ] P2: Field-level encryption for highly sensitive fields (SSN, credit card, health data)
- [ ] P2: Data masking/tokenization used for non-production environments
- [ ] P2: Right to erasure (GDPR) functionality implemented
- [ ] P2: Data access audit logging implemented with immutable storage
- [ ] P2: Secure data deletion verified (crypto-shredding for encrypted data)
- [ ] P2: Cross-border data transfer controls implemented
- [ ] P3: Homomorphic encryption considered for highly sensitive computations
- [ ] P3: Privacy-enhancing technologies (PETs) evaluated for applicable use cases

### 2.5 API Security

- [ ] P0: Rate limiting implemented at multiple layers (API gateway, application, per-user)
- [ ] P0: API keys rotated regularly (90-day maximum, automated rotation preferred)
- [ ] P0: HTTPS enforced for all external and internal communications
- [ ] P0: CORS properly configured (restrictive origin policy, no wildcard in production)
- [ ] P0: API authentication required for all endpoints
- [ ] P1: Input validation implemented on all API endpoints
- [ ] P1: Output encoding applied to all API responses
- [ ] P1: API versioning strategy defined and implemented
- [ ] P1: Circuit breaker patterns implemented for all external API calls
- [ ] P1: Retry logic with exponential backoff and jitter
- [ ] P1: Request and response size limits enforced
- [ ] P1: API gateway deployed as security enforcement point
- [ ] P2: Web Application Firewall (WAF) rules configured
- [ ] P2: API keys scoped to specific permissions and resources
- [ ] P2: API call auditing implemented (who called what, when, with what parameters)
- [ ] P2: GraphQL-specific security controls evaluated if applicable
- [ ] P2: GraphQL query depth limiting and complexity analysis
- [ ] P2: API throttling per user/tier with grace periods
- [ ] P3: API security testing integrated into CI/CD pipeline
- [ ] P3: API contract testing ensures security invariants are maintained

### 2.6 Logging and Monitoring

- [ ] P0: Security events logged (authentication success/failure, authorization denied, injection attempts, tool invocations)
- [ ] P0: Audit trail maintained with immutable storage (append-only logs, WORM storage)
- [ ] P0: Alerts configured for critical security events (brute force, privilege escalation, data exfiltration)
- [ ] P0: Logs protected from tampering (hash chaining, digital signatures, separate log storage)
- [ ] P1: Structured logging implemented (JSON format, consistent schema)
- [ ] P1: Log retention policies implemented (minimum 1 year for security logs)
- [ ] P1: Sensitive data never logged (credentials, PII, session tokens)
- [ ] P1: Timestamps use UTC consistently across all systems
- [ ] P1: User context included in relevant log entries (user ID, session ID, IP address)
- [ ] P1: Log correlation IDs implemented for distributed tracing
- [ ] P2: Real-time security monitoring dashboards created
- [ ] P2: Anomaly detection configured for unusual patterns (unusual times, unusual API calls)
- [ ] P2: Log aggregation and analysis platform deployed (ELK, Splunk, Datadog, etc.)
- [ ] P2: SIEM integration for security event correlation
- [ ] P2: Automated alerting with escalation policies
- [ ] P2: Log access restricted to authorized personnel only
- [ ] P3: Security metrics and KPIs tracked (MTTR, detection rate, false positive rate)
- [ ] P3: Threat hunting conducted on a regular basis

### 2.7 Prompt Security

- [ ] P0: System prompt hardened against extraction attempts
- [ ] P0: User input isolated from system instructions with clear delimiters
- [ ] P0: Direct and indirect prompt injection patterns detected and blocked
- [ ] P0: Jailbreak attempt detection implemented (role-playing, token smuggling, hypothetical framing)
- [ ] P1: Context window isolation enforced between users and sessions
- [ ] P1: Tool results validated for injection markers before adding to context
- [ ] P1: Chain-of-thought output separated from user-facing response
- [ ] P1: Context size limits enforced to prevent overflow attacks
- [ ] P1: Multi-modal prompt injection detection implemented (images, PDFs, audio transcripts)
- [ ] P2: Prompt injection taxonomy implemented and regularly updated
- [ ] P2: Rate limiting on prompt complexity (token count, request frequency)
- [ ] P2: Session isolation with no cross-session context leakage
- [ ] P3: Semantic prompt injection detection using classifier models

### 2.8 Tool Execution Security

- [ ] P0: Tool invocation authorization enforced before execution
- [ ] P0: Tool arguments validated against schema
- [ ] P0: Dangerous tools restricted to authorized roles only
- [ ] P0: Tool execution sandboxed (restricted working directory, no network by default, timeout enforced)
- [ ] P1: Tool allowlist implemented (only approved tools can be invoked)
- [ ] P1: Tool result sanitization before inclusion in context
- [ ] P1: File system access restricted to allowed directories
- [ ] P1: Network access restricted for tool execution (explicit allowlist for allowed destinations)
- [ ] P2: Tool execution audit logging (who invoked what tool, with what arguments, what was the result)
- [ ] P2: Tool permission versioning and change tracking
- [ ] P2: Tool invocation rate limiting per user/per tool
- [ ] P2: Memory poisoning prevention (validate all tool results before context inclusion)
- [ ] P3: Tool execution in isolated containers with resource limits

### 2.9 Error Handling and Information Disclosure

- [ ] P0: Internal error details never returned to external clients
- [ ] P0: Stack traces and internal paths redacted from API responses
- [ ] P0: Informative but safe error messages returned to users
- [ ] P1: Error IDs generated for correlation with internal logs
- [ ] P1: Security-relevant errors logged with full context
- [ ] P1: Error handling does not leak timing information useful for timing attacks
- [ ] P2: Graceful degradation implemented for component failures
- [ ] P2: Circuit breaker error responses do not expose internal architecture
- [ ] P3: Error response schema standardized and validated

---

## Phase 3: Operational Security Checklist

### 3.1 Deployment Security

- [ ] P0: Containers run as non-root user
- [ ] P0: Container filesystem set to read-only where possible
- [ ] P0: All capabilities dropped except those explicitly required
- [ ] P0: Network policies implemented for micro-segmentation
- [ ] P1: Container images scanned for vulnerabilities
- [ ] P1: Container images signed and verified at deployment
- [ ] P1: Secrets injected at runtime (not built into images)
- [ ] P1: Health checks implemented for all services
- [ ] P1: Resource limits (CPU, memory) defined for all containers
- [ ] P2: Security contexts applied to all pods (runAsNonRoot, readOnlyRootFilesystem)
- [ ] P2: Pod security policies or OPA Gatekeeper enforced
- [ ] P2: Immutable infrastructure pattern followed
- [ ] P2: Deployment rollback capability tested
- [ ] P3: Runtime security monitoring (Falco, Sysdig) deployed

### 3.2 Runtime Security

- [ ] P0: Observe and monitor all security-relevant runtime behavior
- [ ] P1: Intrusion detection systems configured for container environment
- [ ] P1: File integrity monitoring enabled for critical files
- [ ] P1: Network traffic monitoring and anomaly detection
- [ ] P2: Runtime self-protection mechanisms implemented
- [ ] P2: Automated response to detected threats (session termination, IP blocking)
- [ ] P2: Security health checks performed regularly
- [ ] P3: Behavioral anomaly detection for agent operations

### 3.3 Key and Certificate Management

- [ ] P1: TLS certificates managed with automated renewal
- [ ] P1: Certificate pinning implemented for critical connections
- [ ] P1: mTLS configured for service-to-service communication
- [ ] P2: Private keys stored in HSM or TPM where possible
- [ ] P2: Key rotation automated with zero-downtime transitions
- [ ] P2: Certificate revocation process defined and tested
- [ ] P3: Post-quantum cryptography readiness evaluated

---

## Phase 4: Post-Implementation Security Checklist

### 4.1 Security Testing

- [ ] P0: Penetration testing performed before production deployment
- [ ] P0: Automated security test suite integrated into CI/CD pipeline
- [ ] P0: Prompt injection defense tested with comprehensive payloads
- [ ] P0: Tool abuse prevention tested with negative test cases
- [ ] P1: Vulnerability scanning completed on deployed infrastructure
- [ ] P1: Fuzzing performed on all input boundaries
- [ ] P1: Authorization bypass attempts tested
- [ ] P1: Session hijacking prevention tested
- [ ] P1: Data exfiltration prevention tested
- [ ] P2: Memory poisoning scenarios tested
- [ ] P2: Cross-session leakage tested under concurrent load
- [ ] P2: Jailbreak detection tested with latest known payloads
- [ ] P2: Rate limit bypass attempts tested
- [ ] P2: Error handling security tested (no information leakage)
- [ ] P3: Chaos engineering for security scenarios
- [ ] P3: Continuous security validation in production

### 4.2 Security Code Review

- [ ] P0: Security code review completed for all security-critical code
- [ ] P1: All input validation and sanitization code reviewed
- [ ] P1: All authentication and authorization code reviewed
- [ ] P1: All cryptographic implementations reviewed
- [ ] P1: All secret handling code reviewed
- [ ] P1: All tool execution code reviewed
- [ ] P2: Regular security review cadence established (quarterly for active projects)
- [ ] P2: Security review checklist used for consistency
- [ ] P2: Security findings tracked to resolution in issue tracker
- [ ] P3: External security audit conducted for high-risk systems

### 4.3 Compliance and Documentation

- [ ] P1: Security documentation updated to reflect current implementation
- [ ] P1: Data protection impact assessment (DPIA) completed if required
- [ ] P1: Privacy policy and terms of service aligned with data handling practices
- [ ] P1: Incident response plan documented and communicated
- [ ] P1: Data breach notification procedures defined
- [ ] P2: Compliance evidence collected and stored
- [ ] P2: Security controls mapped to compliance frameworks (SOC 2, ISO 27001, etc.)
- [ ] P2: Regular compliance reporting established
- [ ] P3: Security architecture review completed by external party

---

## Phase 5: Ongoing Security Operations Checklist

### 5.1 Continuous Monitoring

- [ ] P1: Security event monitoring active 24/7
- [ ] P1: Automated alerting configured for critical events
- [ ] P1: Weekly security review of logs and alerts
- [ ] P2: Monthly security metrics review
- [ ] P2: Quarterly threat model review and update
- [ ] P2: Dependency vulnerability scanning runs daily
- [ ] P2: Security patch management process active
- [ ] P3: Continuous security validation in production

### 5.2 Incident Response Readiness

- [ ] P1: Incident response team on-call rotation established
- [ ] P1: Incident severity classification defined
- [ ] P1: Escalation procedures documented
- [ ] P1: Communication plan for security incidents
- [ ] P2: Incident response playbooks created for common scenarios
- [ ] P2: Tabletop exercises conducted quarterly
- [ ] P2: Post-incident review process established
- [ ] P3: Threat intelligence integration for proactive defense

### 5.3 Training and Awareness

- [ ] P1: Security training completed for all team members
- [ ] P1: Secure coding practices reviewed in team meetings
- [ ] P2: Regular security newsletters or updates shared with team
- [ ] P2: New hire security onboarding process established
- [ ] P2: Cross-training on security responsibilities
- [ ] P3: Security champions program active in all teams

---

## Phase 6: AI-Specific Security Checklist

### 6.1 Model Security

- [ ] P0: Model source verified (official provider, not compromised mirror)
- [ ] P0: Model integrity verified via checksum or digital signature
- [ ] P0: No sensitive data in model training set that could be extracted
- [ ] P1: Model version pinned and immutable
- [ ] P1: Model fine-tuning security reviewed
- [ ] P2: Model behavior tested for safety across diverse inputs
- [ ] P2: Model output distribution monitored for anomalies
- [ ] P2: Adversarial robustness evaluated
- [ ] P3: Model watermarking or fingerprinting considered

### 6.2 Prompt Injection Defense Depth

- [ ] P0: Input-layer prompt injection detection
- [ ] P0: System prompt hardening applied
- [ ] P0: Context isolation enforced
- [ ] P1: Output-layer prompt injection detection
- [ ] P1: Behavioral guardrails enforced (refusal patterns, topic restrictions)
- [ ] P1: Semantic similarity checking for input/output against known attack patterns
- [ ] P2: Machine learning-based injection detection
- [ ] P2: Cross-session contamination prevention
- [ ] P3: Real-time prompt injection defense adaptation

### 6.3 Agent Tool Use Security

- [ ] P0: All tool invocations authorized before execution
- [ ] P0: Tool arguments validated against schema
- [ ] P0: Dangerous tools restricted to authorized roles only
- [ ] P0: Tool execution sandboxed (restricted working directory, no network by default, timeout enforced)
- [ ] P1: Tool allowlist implemented (only approved tools can be invoked)
- [ ] P1: Tool result sanitization before inclusion in context
- [ ] P1: File system access restricted to allowed directories
- [ ] P1: Network access restricted for tool execution (explicit allowlist for allowed destinations)
- [ ] P2: Tool execution audit logging (who invoked what tool, with what arguments, what was the result)
- [ ] P2: Tool permission versioning and change tracking
- [ ] P2: Tool invocation rate limiting per user/per tool
- [ ] P2: Memory poisoning prevention (validate all tool results before context inclusion)
- [ ] P3: Tool execution in isolated containers with resource limits

### 6.4 Multi-Agent Security

- [ ] P0: Agent identity cryptographically verified
- [ ] P0: Inter-agent messages authenticated (HMAC or digital signature)
- [ ] P0: Inter-agent messages encrypted
- [ ] P0: Replay protection implemented (nonce + timestamp validation)
- [ ] P1: Agent trust levels defined and enforced
- [ ] P1: Agent capability restrictions enforced by receiving agent
- [ ] P1: Inter-agent communication logged and auditable
- [ ] P2: Agent federation security model defined
- [ ] P2: Agent-to-agent authorization policies defined
- [ ] P3: Zero-trust model applied to all agent-to-agent communication

---

## Phase 7: Compliance and Governance Checklist

### 7.1 Regulatory Compliance

- [ ] P1: GDPR compliance verified (data minimization, right to erasure, consent management)
- [ ] P1: CCPA/CPRA compliance verified (data deletion, opt-out mechanisms)
- [ ] P1: HIPAA compliance verified if handling PHI (BAA requirements, encryption, access controls)
- [ ] P1: PCI DSS compliance verified if handling payment data
- [ ] P1: SOC 2 compliance verified for service organizations
- [ ] P2: Industry-specific regulations identified and addressed
- [ ] P2: Cross-border data transfer controls implemented
- [ ] P2: Data localization requirements met
- [ ] P3: Emerging AI regulations evaluated (EU AI Act, etc.)

### 7.2 Audit and Evidence

- [ ] P1: Audit logs retained per regulatory requirements
- [ ] P1: Audit log integrity verified (tamper detection)
- [ ] P1: Access logs collected for all sensitive data
- [ ] P1: Change management process documented
- [ ] P2: Automated evidence collection for compliance
- [ ] P2: Third-party audit readiness maintained
- [ ] P2: Security control effectiveness tested
- [ ] P3: Continuous compliance monitoring implemented

### 7.3 Policy and Governance

- [ ] P1: Security policies documented and published
- [ ] P1: Acceptable use policy defined for AI systems
- [ ] P1: Data classification policy enforced
- [ ] P1: Incident response plan documented
- [ ] P2: Security governance committee established
- [ ] P2: Regular security policy review schedule established
- [ ] P2: Exception process defined for security controls
- [ ] P2: Vendor security assessment process established
- [ ] P3: Security metrics reported to executive leadership

---

## Sign-Off

### Complete Sign-Off

Before marking the security review as complete, the following must be verified:

- [ ] P0: All P0 checklist items checked and verified
- [ ] P0: No critical security vulnerabilities identified
- [ ] P0: Security review documented with evidence
- [ ] P0: Team trained on all implemented security controls
- [ ] P1: All P1 checklist items checked or mitigation documented
- [ ] P1: Security code review completed
- [ ] P1: Security test suite passing with acceptable coverage
- [ ] P1: Penetration test report reviewed and findings addressed
- [ ] P2: All P2 items reviewed with go/no-go decision documented
- [ ] P2: Security documentation updated
- [ ] P2: Monitoring and alerting operational
- [ ] P2: Incident response procedures tested
- [ ] P3: All P3 recommendations evaluated with disposition documented

### Traceability and Evidence

- [ ] P0: Evidence collected for each checklist item
- [ ] P0: Security test results documented and stored
- [ ] P0: Threat model review meeting minutes recorded
- [ ] P1: Security code review findings tracked to closure
- [ ] P1: Penetration test report stored with remediation plan
- [ ] P1: Dependency scan results stored
- [ ] P2: Compliance gap analysis documented
- [ ] P2: Security architecture review sign-off obtained

---

## Appendix A: Security Checklist Validation Process

### Validation Steps

1. **Pre-Deployment Gate**: All P0 items must pass before any deployment to production.
2. **Review Cadence**: Quarterly re-validation of all P0 and P1 items.
3. **Change Trigger**: Security checklist re-validation triggered by significant architectural changes, new features, or identified threats.
4. **Evidence Requirements**: Each checked item must have associated evidence (test results, configuration screenshots, scan outputs, code review records).
5. **Exception Process**: Any exception to a P0/P1 item requires: risk assessment, compensating controls, documented approval from security team, and defined remediation timeline.

### Validation Roles

- **Developer**: Validates implementation-level items and provides code/test evidence.
- **Security Champion**: Validates security design items and reviews evidence.
- **Security Team**: Validates P0 items and provides final sign-off.
- **Product Owner**: Accepts residual risk for any exceptions.

---

## Appendix B: Common Security Checklist Gaps

### Frequently Missed Items

1. **Secrets in logs**: Often missed in logging reviews
2. **Tool result sanitization**: Agent-specific gap not covered in traditional security reviews
3. **Prompt injection defense**: Novel attack surface often overlooked
4. **Circuit breakers**: Resilience gap in external API integration
5. **Context isolation**: Session and user data leakage between conversations
6. **Multimodal inputs**: Security review often covers text but not images, audio, PDFs
7. **Supply chain**: Dependency and model integrity verification often skipped
8. **Log integrity**: Log protection from tampering often an afterthought

---

## Appendix C: Quick Reference - Minimum Viable Security

Systems that cannot immediately implement all P1/P2 items should at minimum ensure:

- All user inputs validated and sanitized
- Strong authentication with MFA for admin access
- Authorization checks on all sensitive operations
- Secrets loaded from secured vault, never hardcoded
- TLS 1.2+ for all external communications
- Structured logging of all security-relevant events
- Rate limiting on all user-facing endpoints
- Prompt injection detection and blocking
- Regular dependency scanning
- Error handling that does not leak sensitive information

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Advanced Concepts](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
- [Examples](./examples.md)
