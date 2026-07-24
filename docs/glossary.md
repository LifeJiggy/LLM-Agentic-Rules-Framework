# Glossary

## Overview

This glossary defines key terms used throughout the LLM & Agentic Rules Framework.

## Framework Terms

| Term | Definition |
|------|------------|
| Framework | The LLM & Agentic Rules Framework - a structured collection of rules, practices, examples, and checklists |
| Domain | A focused area of rules within the framework (e.g., Security, Testing, Compliance) |
| Module | An operational area with 7 rule files (e.g., Evaluation, Deployment, Monitoring) |
| Agent | A specialized role that implements specific parts of the framework lifecycle |
| Skill | A specialized workflow or pattern for implementing framework guidance |
| Rule | A specific guideline or requirement within a domain |
| Checklist | A list of verification steps for a specific area |
| Anti-pattern | A common mistake or failure mode to avoid |

## AI/LLM Terms

| Term | Definition |
|------|------------|
| LLM | Large Language Model - a neural network trained on large text datasets |
| Agentic | Systems that can autonomously take actions to achieve goals |
| RAG | Retrieval-Augmented Generation - combining retrieval with generation |
| MCP | Model Context Protocol - protocol for tool integration |
| Prompt Injection | Attack that manipulates model behavior through malicious inputs |
| Jailbreak | Attempt to bypass model safety restrictions |
| Hallucination | Model generating factually incorrect information |
| Fine-tuning | Training a model on specific data to customize behavior |
| Embedding | Vector representation of text for similarity search |
| Tokenization | Breaking text into tokens for model processing |

## Operational Terms

| Term | Definition |
|------|------------|
| SLI | Service Level Indicator - measured metric of service performance |
| SLO | Service Level Objective - target for SLI performance |
| SLA | Service Level Agreement - contractual commitment for service levels |
| MTTR | Mean Time To Recovery - average time to recover from incidents |
| RTO | Recovery Time Objective - target time for system recovery |
| RPO | Recovery Point Objective - target data loss in time |
| CI/CD | Continuous Integration / Continuous Deployment |
| Observability | Ability to understand system state from external outputs |

## Governance Terms

| Term | Definition |
|------|------------|
| DPIA | Data Protection Impact Assessment |
| DPO | Data Protection Officer |
| DPA | Data Processing Agreement |
| DSAR | Data Subject Access Request |
| ADR | Architecture Decision Record |
| P0/P1/P2/P3 | Priority levels for rules and controls |
| Evidence | Artifact demonstrating control implementation |
| Exception | Formal approval to deviate from a requirement |

## Security Terms

| Term | Definition |
|------|------------|
| RBAC | Role-Based Access Control |
| ABAC | Attribute-Based Access Control |
| MFA | Multi-Factor Authentication |
| WAF | Web Application Firewall |
| IDS | Intrusion Detection System |
| SOC | Security Operations Center |
| CVE | Common Vulnerabilities and Exposures |
| SBOM | Software Bill of Materials |

## Compliance Terms

| Term | Definition |
|------|------------|
| GDPR | General Data Protection Regulation |
| HIPAA | Health Insurance Portability and Accountability Act |
| SOC 2 | Service Organization Control 2 |
| PCI DSS | Payment Card Industry Data Security Standard |
| EU AI Act | European Union Artificial Intelligence Act |
| ISO 27001 | Information Security Management System Standard |
| NIST AI RMF | NIST AI Risk Management Framework |

## Performance Terms

| Term | Definition |
|------|------------|
| Latency | Time to respond to a request |
| Throughput | Number of requests processed per unit time |
| P50/P95/P99 | Percentile measurements of latency |
| Error Rate | Percentage of failed requests |
| Cost per Request | Average cost to process one request |
| Token Usage | Number of tokens consumed per request |
| Context Window | Maximum tokens the model can process |

## Deployment Terms

| Term | Definition |
|------|------------|
| Blue-Green Deployment | Two identical environments for zero-downtime deployment |
| Canary Deployment | Gradual rollout to a small percentage of users |
| Rolling Deployment | Incremental update across instances |
| Feature Flag | Toggle for enabling/disabling features without deployment |
| Rollback | Reverting to a previous version |
| Hotfix | Emergency patch for critical issues |
| Shadow Deployment | Running new version alongside old without user impact |
