# Evolution Process

This process keeps the framework current as AI systems, model providers, regulations, and production lessons change.

## Change Sources

Framework updates should come from:

- production incidents;
- failed evaluations;
- audit findings;
- security reviews;
- model or provider changes;
- new laws, standards, or organizational policies;
- repeated contributor questions or adoption friction.

## Change Types

| Type | Description | Required Updates |
|------|-------------|------------------|
| Rule update | Adds or changes guidance in a domain file | Domain file, related links, changelog |
| Checklist update | Adds or changes review requirements | Checklist file, checklist pack if relevant, changelog |
| Template update | Adds or changes reusable review/evidence artifacts | Template, validator, README if supported |
| Tooling update | Changes validation or export behavior | Script, CI workflow, docs |
| Structural update | Changes the repository contract | README, validator, roadmap, contributing guide |

## Release Cadence

- Patch updates: typo fixes, link fixes, small clarifications.
- Minor updates: new rules, templates, examples, or validation behavior.
- Major updates: structure changes, domain changes, or compatibility-breaking tooling changes.

## Required Review Questions

- What user or reviewer problem does this change solve?
- Which target audience benefits?
- Does the change affect the repository contract?
- Does validation need to be updated?
- Should this create or update a checklist item?
- Should this create or update an anti-pattern or troubleshooting entry?

## Changelog Rules

Every non-trivial change should update `CHANGELOG.md` under one of:

- Added
- Changed
- Fixed
- Deprecated
- Removed
- Security
