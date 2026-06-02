# Migration Guide

Use this guide to migrate an existing AI project onto the framework.

## Step 1: Inventory The System

Document:

- model providers and model versions;
- prompt templates;
- retrieval sources;
- tools and external APIs;
- stored data and logs;
- evaluation suites;
- deployment environments;
- user groups and risk tier.

## Step 2: Select Domains

Start with the domains that reflect the highest risk. Most production systems should begin with:

- `01-core`
- `02-security`
- `04-data`
- `06-operations`
- `07-testing`
- `10-compliance`

## Step 3: Run A Gap Review

For each selected domain:

1. Read `fundamentals.md`.
2. Check `anti-patterns.md` for existing risks.
3. Apply `checklist.md` to the current system.
4. Record gaps as issues.
5. Prioritize P0 and P1 gaps first.

## Step 4: Add Controls Incrementally

Recommended order:

1. Data and secret protection.
2. Tool permission boundaries.
3. Evaluation and regression tests.
4. Production monitoring and incident response.
5. Compliance evidence and human oversight.
6. Performance and cost optimization.

## Step 5: Institutionalize The Framework

Add the framework into:

- architecture reviews;
- pull request templates;
- release checklists;
- onboarding plans;
- incident review process;
- compliance evidence folders.
