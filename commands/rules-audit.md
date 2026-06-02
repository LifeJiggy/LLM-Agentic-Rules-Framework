# /rules-audit

Audit the current project using the LLM & Agentic Rules Framework.

## Prompt

Use the framework in this repository to audit the current project. Start by identifying the system type, risk tier, and relevant domains. Then review the strongest applicable P0/P1 controls from:

- Core
- Security
- Data
- Integration
- Operations
- Testing
- Documentation
- Performance
- Compliance

Return findings ordered by severity. For each finding include:

- affected file or workflow;
- violated rule or checklist area;
- production risk;
- concrete fix;
- required evidence or test.

## Severity Format

Use this output shape:

| Severity | Finding | Evidence Gap | Fix | Owner |
|----------|---------|--------------|-----|-------|

Severity must be one of `P0`, `P1`, `P2`, or `P3`.
