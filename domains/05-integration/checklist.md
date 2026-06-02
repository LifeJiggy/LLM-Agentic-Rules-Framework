# Integration Domain - Checklist

## Overview

This checklist verifies that APIs, tools, webhooks, and external dependencies are integrated with clear contracts and failure handling.

## Priority Guide

- P0: Required for integrations that can expose data or perform irreversible actions.
- P1: Required for reliable production integrations unless explicitly accepted.
- P2: Recommended for compatibility, observability, and maintainability.
- P3: Useful refinement for developer and partner experience.

## API Checklist

- [ ] RESTful conventions followed
- [ ] Versioning implemented
- [ ] Error handling in place
- [ ] Rate limiting configured
- [ ] Pagination implemented
- [ ] Authentication secured

## External Services Checklist

- [ ] Timeouts configured
- [ ] Retry logic implemented
- [ ] Circuit breakers in place
- [ ] Logging enabled

## Sign-Off

- [ ] API tested
- [ ] Integration tests passed

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
