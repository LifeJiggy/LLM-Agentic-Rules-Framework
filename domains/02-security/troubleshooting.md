# Security Domain - Troubleshooting

## Overview

This document covers common security issues and their solutions for LLM/agentic systems.

## Common Security Issues and Solutions

### Issue 1: SQL Injection

**Symptoms:**
- Unexpected database queries
- Data leaks
- Unauthorized access

**Solutions:**
- Use parameterized queries
- Use ORM frameworks
- Validate input strictly

### Issue 2: Prompt Injection

**Symptoms:**
- Agent ignores instructions
- Unexpected behavior
- System instructions leaked

**Solutions:**
- Isolate user input
- Use input sanitization
- Implement output validation

### Issue 3: API Key Exposure

**Symptoms:**
- Keys found in logs
- Unauthorized API access
- Rate limit abuse

**Solutions:**
- Use environment variables
- Implement key rotation
- Monitor API usage

### Issue 4: Rate Limit Bypass

**Symptoms:**
- High API costs
- Service degradation
- Denial of service

**Solutions:**
- Implement multiple rate limit layers
- Use token bucket algorithm
- Monitor unusual patterns

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
