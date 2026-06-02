# Compliance Domain - Checklist

> Verification checklist for releasing or reviewing LLM and agentic systems.

## Overview

Use this checklist before releasing medium-risk or high-risk AI systems, and when reviewing production systems after material model, prompt, data, or tool changes.

## Priority Guide

- P0: Required for legal, regulatory, safety, rights-impacting, or audit-blocking controls.
- P1: Required for medium-risk and high-risk production systems unless explicitly accepted.
- P2: Recommended for governance maturity and review efficiency.
- P3: Useful refinement for evidence quality.

## System Definition

- [ ] System owner is documented.
- [ ] Intended use is documented.
- [ ] Prohibited uses are documented.
- [ ] User groups are documented.
- [ ] Risk tier is assigned.
- [ ] Review cadence is defined.

## Data Governance

- [ ] Data sources are documented.
- [ ] Personal and sensitive data categories are identified.
- [ ] Legal basis or business justification is documented.
- [ ] Data minimization has been applied.
- [ ] Retention period is defined for prompts, completions, traces, and logs.
- [ ] Access to AI logs is restricted.

## Model And Prompt Governance

- [ ] Model provider and model version are recorded.
- [ ] Prompt templates are versioned.
- [ ] High-risk prompt changes require review.
- [ ] Model upgrades trigger regression evaluation.
- [ ] Known limitations are documented.

## Tool And Agent Controls

- [ ] Agent tools are inventoried.
- [ ] Tool permissions follow least privilege.
- [ ] Irreversible or high-impact actions require confirmation or review.
- [ ] Tool calls are logged with enough context for audit.
- [ ] Failure modes and rollback paths are documented.

## Evaluation And Monitoring

- [ ] Compliance-relevant test cases exist.
- [ ] Harmful, biased, misleading, and privacy-risk outputs are tested.
- [ ] Production monitoring covers policy violations.
- [ ] Incident response path is documented.
- [ ] Exceptions and accepted risks are approved.

## Release Decision

- [ ] Security review completed where required.
- [ ] Privacy review completed where required.
- [ ] Legal or compliance review completed for high-impact workflows.
- [ ] Human oversight requirements are implemented.
- [ ] Audit evidence is stored in a durable location.
