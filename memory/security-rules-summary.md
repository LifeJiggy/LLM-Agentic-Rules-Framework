# Security Rules Summary - LLM & Agentic Rules Framework

## Overview

This document summarizes the security rules for LLM and agentic systems. The Security domain establishes requirements for protecting systems against threats, vulnerabilities, and attacks.

## P0 Critical Rules

### SEC-001: Threat Modeling

**Rule**: Every AI system must have a threat model that identifies potential threats, attack vectors, and mitigations.

**Why It Matters**: Without threat modeling, security controls are implemented reactively rather than proactively. Threat modeling identifies risks before they become incidents.

**Threat Categories for AI Systems**:
- Prompt injection (direct and indirect)
- Data exfiltration through tool misuse
- Model manipulation or jailbreaking
- Unauthorized access to system capabilities
- Supply chain attacks via dependencies
- Insider threats and misuse
- Denial of service through resource exhaustion

**Implementation Requirements**:
- Conduct threat modeling during design phase
- Document threats, likelihood, and impact
- Identify mitigations for each threat
- Review threat model when system changes
- Update threat model after incidents
- Share threat model with security team

**Evidence Required**:
- Threat model document
- Threat register with status
- Review history
- Update records

### SEC-002: Input Validation and Sanitization

**Rule**: All user inputs must be validated and sanitized before processing by AI models.

**Why It Matters**: AI systems are vulnerable to prompt injection, where malicious inputs manipulate model behavior. Input validation is the first line of defense.

**Implementation Requirements**:
- Define input schema for all entry points
- Validate input format and content
- Sanitize inputs to remove injection attempts
- Implement input length limits
- Log validation failures
- Alert on repeated validation failures

**Input Validation Techniques**:
- Schema validation for structured inputs
- Content filtering for malicious patterns
- Length limits to prevent context overflow
- Character encoding normalization
- Separation of instructions and data

**Evidence Required**:
- Input validation configuration
- Validation test results
- Sample validation logs
- Alert configuration

### SEC-003: Output Filtering

**Rule**: All model outputs must be filtered before delivery to users or systems.

**Why It Matters**: AI models can generate harmful, biased, or policy-violating content. Output filtering prevents such content from reaching users.

**Implementation Requirements**:
- Define output safety criteria
- Implement content filtering for harmful content
- Filter PII from outputs where required
- Validate outputs against policy
- Log filtering decisions
- Alert on filtering activations

**Output Filtering Categories**:
- Harmful content (violence, self-harm, illegal activity)
- Toxic content (hate speech, harassment)
- PII leakage (names, emails, phone numbers)
- Policy violations (off-topic, unauthorized actions)
- Factual errors (when verifiable)

**Evidence Required**:
- Output filtering configuration
- Filtering test results
- Sample filtering logs
- Alert configuration

### SEC-004: Secret Management

**Rule**: All secrets (API keys, credentials, tokens) must be stored securely with rotation and access control.

**Why It Matters**: Exposed secrets enable unauthorized access, data breaches, and system compromise. Proper secret management prevents credential leakage.

**Implementation Requirements**:
- Store secrets in dedicated secret management system
- Never store secrets in code or configuration files
- Implement secret rotation on schedule
- Control secret access with least privilege
- Audit all secret access
- Implement emergency secret revocation

**Secret Management Standards**:
- Use HashiCorp Vault, AWS Secrets Manager, or equivalent
- Rotate secrets at least quarterly
- Use unique secrets per environment
- Implement secret scanning in CI/CD
- Log all secret access attempts

**Evidence Required**:
- Secret management configuration
- Secret rotation schedule
- Access audit logs
- Secret scanning results

### SEC-005: Access Control Enforcement

**Rule**: All system resources must have access controls enforced with least-privilege principle.

**Why It Matters**: Without access controls, unauthorized users can access sensitive data or capabilities. Least privilege limits blast radius of compromises.

**Implementation Requirements**:
- Implement authentication for all access points
- Implement authorization for all resources
- Use role-based or attribute-based access control
- Enforce least-privilege principle
- Review access regularly
- Implement access logging

**Access Control Models**:
- Role-Based Access Control (RBAC): Access based on user roles
- Attribute-Based Access Control (ABAC): Access based on attributes
- Policy-Based Access Control (PBAC): Access based on policies

**Evidence Required**:
- Access control configuration
- Role and permission definitions
- Access review records
- Access audit logs

## P1 High Priority Rules

### SEC-006: Security Monitoring

**Rule**: AI systems must have security monitoring that detects and alerts on suspicious activity.

**Why It Matters**: Security incidents can occur at any time. Without monitoring, incidents go undetected, increasing damage and response time.

**Implementation Requirements**:
- Monitor authentication events
- Monitor authorization failures
- Monitor input validation failures
- Monitor output filtering activations
- Monitor tool invocations
- Monitor configuration changes
- Implement anomaly detection
- Configure alert routing

**Security Monitoring Metrics**:
- Failed authentication attempts
- Authorization failure rate
- Input validation failure rate
- Output filtering activation rate
- Unusual tool invocation patterns
- Configuration change frequency

**Evidence Required**:
- Monitoring configuration
- Alert rules and thresholds
- Alert routing configuration
- Sample alerts

### SEC-007: Penetration Testing

**Rule**: High-risk AI systems must undergo penetration testing before production and periodically thereafter.

**Why It Matters**: Penetration testing identifies vulnerabilities that automated scanning may miss. It provides realistic assessment of system security.

**Implementation Requirements**:
- Conduct penetration testing before production
- Test for AI-specific vulnerabilities (prompt injection, jailbreaking)
- Test for standard web vulnerabilities
- Test for API vulnerabilities
- Document findings and remediation
- Retest after remediation
- Conduct periodic retesting

**Penetration Testing Scope**:
- Prompt injection attacks
- Jailbreak attempts
- Data exfiltration attempts
- Tool misuse attempts
- API abuse
- Authentication bypass
- Authorization escalation

**Evidence Required**:
- Penetration test report
- Findings remediation tracking
- Retest results
- Testing schedule

### SEC-008: Security Review Gates

**Rule**: Security review must be conducted before production deployment and major changes.

**Why It Matters**: Security review catches issues before they reach production. It provides independent assessment of security controls.

**Implementation Requirements**:
- Conduct security review before production deployment
- Review threat model and mitigations
- Review access controls
- Review secret management
- Review input/output handling
- Document review findings
- Track findings to resolution

**Security Review Checklist**:
- [ ] Threat model current
- [ ] Input validation implemented
- [ ] Output filtering implemented
- [ ] Secret management proper
- [ ] Access controls enforced
- [ ] Security monitoring active
- [ ] Incident response ready

**Evidence Required**:
- Security review report
- Findings and remediation
- Review sign-off

## P2 Medium Priority Rules

### SEC-009: Security Training

**Rule**: Team members working on AI systems must receive security training relevant to their roles.

**Why It Matters**: Security is a team effort. Without training, team members may inadvertently create vulnerabilities or miss security issues.

**Implementation Requirements**:
- Define training requirements by role
- Provide AI-specific security training
- Provide secure coding training
- Provide incident response training
- Track training completion
- Update training based on incidents

**Training Topics**:
- Prompt injection attacks and defenses
- Secure AI system design
- Secret management practices
- Incident response procedures
- Secure coding practices
- Data protection requirements

**Evidence Required**:
- Training curriculum
- Training completion records
- Training effectiveness assessment

### SEC-010: Security Metrics

**Rule**: Security metrics must be tracked to measure effectiveness and guide improvements.

**Why It Matters**: Without metrics, security posture is unknown. Metrics enable data-driven security decisions and demonstrate compliance.

**Security Metrics to Track**:
- Vulnerability count and severity
- Time to remediate vulnerabilities
- Security incident count
- Mean time to detect incidents
- Mean time to respond to incidents
- Training completion rate
- Security review completion rate
- Penetration test findings

**Evidence Required**:
- Metrics definition
- Metrics collection configuration
- Metrics reports
- Improvement actions based on metrics

## Security Control Categories

### Preventive Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Input validation | Validate and sanitize inputs | Schema validation, content filtering |
| Output filtering | Filter harmful outputs | Content safety checks, PII filtering |
| Access control | Control resource access | Authentication, authorization |
| Secret management | Protect credentials | Vault, rotation, access control |
| Network security | Protect network communications | TLS, firewalls, segmentation |

### Detective Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Security monitoring | Detect suspicious activity | Log analysis, anomaly detection |
| Audit logging | Record system activity | Comprehensive logging, integrity |
| Intrusion detection | Detect attacks | IDS/IPS, behavioral analysis |
| Vulnerability scanning | Detect weaknesses | Automated scanning, manual review |

### Corrective Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Incident response | Respond to incidents | Runbooks, escalation, communication |
| Patch management | Fix vulnerabilities | Patch testing, deployment |
| Recovery | Restore from incidents | Backups, restoration procedures |

## Security Anti-Patterns

### Hardcoded Secrets

**Anti-Pattern**: Storing API keys, credentials, or tokens directly in code or configuration files.

**Why It Fails**: Secrets in code are exposed in version control, logs, and backups. They cannot be rotated without code changes. Access cannot be controlled.

**Correct Approach**: Use secret management system. Store secrets in vault. Rotate regularly. Control access with least privilege.

### Missing Input Validation

**Anti-Pattern**: Processing user inputs without validation or sanitization.

**Why It Fails**: Enables prompt injection, data exfiltration, and other attacks. Malicious inputs can manipulate model behavior.

**Correct Approach**: Validate all inputs against schema. Sanitize inputs to remove injection attempts. Log validation failures.

### Broad Tool Permissions

**Anti-Pattern**: Granting tools broad permissions without scoping to specific use cases.

**Why It Fails**: Tools with broad permissions can be misused for unauthorized actions, data exfiltration, or privilege escalation.

**Correct Approach**: Scope tool permissions to specific use cases. Implement least privilege. Require approval for high-impact tools.

### Missing Security Monitoring

**Anti-Prompt**: Deploying AI systems without security monitoring or alerting.

**Why It Fails**: Security incidents go undetected. Response time increases. Damage accumulates without visibility.

**Correct Approach**: Implement comprehensive security monitoring. Configure alerts for suspicious activity. Route alerts to appropriate teams.

## Security Metrics Dashboard

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Critical vulnerabilities | 0 | - | - |
| High vulnerabilities | < 5 | - | - |
| Mean time to detect | < 5 min | - | - |
| Mean time to respond | < 1 hour | - | - |
| Training completion | > 95% | - | - |
| Security reviews complete | 100% | - | - |

## Cross-Domain Dependencies

The Security domain interacts with all other domains:

| Domain | Security Dependency | Interaction |
|--------|---------------------|-------------|
| Core | SEC-001, SEC-005 | Threat model and access control inform core design |
| Data | SEC-004, SEC-005 | Secret management and access control protect data |
| Integration | SEC-005, SEC-007 | Access control and penetration testing secure integrations |
| Operations | SEC-006, SEC-008 | Monitoring and review gates support operations |
| Testing | SEC-007 | Penetration testing is a testing activity |
| Documentation | SEC-009 | Security training requires documentation |
| Performance | - | Security controls may impact performance |
| Compliance | SEC-001, SEC-006, SEC-008 | Threat model, monitoring, and review support compliance |

## References

- Security domain fundamentals: `domains/02-security/fundamentals.md`
- Security domain best practices: `domains/02-security/best-practices.md`
- Security domain anti-patterns: `domains/02-security/anti-patterns.md`
- Security domain checklist: `domains/02-security/checklist.md`
- Security domain examples: `domains/02-security/examples.md`
- Security domain troubleshooting: `domains/02-security/troubleshooting.md`
- Security domain advanced: `domains/02-security/advanced.md`
