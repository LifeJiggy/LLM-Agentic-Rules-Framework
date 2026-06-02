# Security Domain - Checklist

## Overview

This checklist verifies that security controls are applied to prompts, tools, data handling, authentication, authorization, and runtime operations.

## Priority Guide

- P0: Required for preventing data exposure, unauthorized access, or unsafe tool use.
- P1: Required for production hardening unless explicitly accepted.
- P2: Recommended for defense in depth.
- P3: Useful refinement for mature security programs.

## Pre-Implementation Security Checklist

- [ ] Security requirements defined
- [ ] Threat model created
- [ ] Security architecture documented
- [ ] Dependencies audited for vulnerabilities

## Implementation Security Checklist

### Input Validation
- [ ] All user inputs validated
- [ ] Input length limits enforced
- [ ] Special characters sanitized
- [ ] SQL injection prevented
- [ ] XSS prevented

### Authentication
- [ ] Strong password policies enforced
- [ ] Multi-factor authentication implemented
- [ ] Session management secure
- [ ] Tokens properly managed

### Authorization
- [ ] Least privilege principle applied
- [ ] Role-based access control implemented
- [ ] Permission checks on all resources

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Data encrypted in transit
- [ ] Secrets properly managed
- [ ] Data retention policies enforced

### API Security
- [ ] Rate limiting implemented
- [ ] API keys rotated regularly
- [ ] HTTPS enforced
- [ ] CORS properly configured

### Logging & Monitoring
- [ ] Security events logged
- [ ] Audit trail maintained
- [ ] Alerts configured for suspicious activity
- [ ] Logs protected from tampering

## Post-Implementation Security Checklist

- [ ] Security code review completed
- [ ] Penetration testing performed
- [ ] Vulnerability scanning completed
- [ ] Security documentation updated

## Sign-Off

Before marking as complete, verify:

- [ ] All checklist items checked
- [ ] No security vulnerabilities identified
- [ ] Security review documented
- [ ] Team trained on security practices

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
