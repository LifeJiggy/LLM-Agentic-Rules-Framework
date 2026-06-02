# Compliance Domain - Troubleshooting

> Common compliance issues in LLM and agentic systems and how to resolve them.

## Overview

Use this file during audits, incident reviews, or release blockers where the issue is missing evidence, unclear ownership, sensitive data exposure, or unmanaged policy exceptions.

## Missing Approval Evidence

**Symptom:** A reviewer asks why a system was approved, but the team can only point to chat messages or informal notes.

**Likely cause:** The release process lacks a durable evidence location.

**Resolution:**

1. Create a release review record.
2. Attach evaluation, privacy, security, and risk review evidence.
3. Link the record from the system register.
4. Require the same record for future releases.

## Sensitive Data Appears In Logs

**Symptom:** Prompt or completion traces contain secrets, personal data, or regulated records.

**Likely cause:** Logging was designed for debugging without data classification.

**Resolution:**

1. Restrict access to affected logs.
2. Redact or purge records according to policy.
3. Add redaction before persistence.
4. Reduce trace retention.
5. Add a regression test for the leakage pattern.

## Model Upgrade Changes Regulated Output

**Symptom:** A model upgrade changes refusals, advice, tone, or classification decisions.

**Likely cause:** Model versions are not treated as behavior-affecting dependencies.

**Resolution:**

1. Roll back if user impact is unacceptable.
2. Run the approved evaluation suite against both versions.
3. Review changed cases with the system owner.
4. Update the model register and release evidence.

## Unclear Human Review Requirements

**Symptom:** Operators disagree about when AI output can be sent or acted on.

**Likely cause:** Oversight rules are implicit or only described in training.

**Resolution:**

1. Define review thresholds in documentation.
2. Add product controls that enforce review where possible.
3. Log approvals and overrides.
4. Train reviewers with examples of borderline cases.

## Policy Exceptions Accumulate

**Symptom:** Many releases rely on temporary exceptions that are never revisited.

**Likely cause:** Exceptions have no owner, expiration, or remediation plan.

**Resolution:**

1. Assign each exception an owner.
2. Add an expiration date.
3. Document the accepted risk.
4. Track remediation to closure.
