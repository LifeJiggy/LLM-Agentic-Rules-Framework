# Getting Started

This guide helps teams adopt the LLM & Agentic Rules Framework in a new or existing project.

## 1. Identify Your System Type

| System Type | Recommended Domains |
|-------------|---------------------|
| User-facing chatbot | Core, Security, Data, Testing, Operations, Compliance |
| Agentic automation | Core, Development, Integration, Operations, Testing |
| Retrieval-augmented generation | Core, Data, Security, Testing, Performance |
| AI API platform | Core, Integration, Operations, Performance, Security |
| Regulated workflow | Core, Security, Data, Testing, Operations, Compliance |

## 2. Start With Core

Read:

- `domains/01-core/fundamentals.md`
- `domains/01-core/best-practices.md`
- `domains/01-core/checklist.md`

Use Core to define baseline expectations for prompts, context, tools, state, errors, and agent loops.

## 3. Add Risk Domains

Add domains based on what the system can affect.

- Handles secrets, private data, or external users: add Security.
- Stores, retrieves, or transforms data: add Data.
- Calls APIs or tools: add Integration.
- Runs in production: add Operations.
- Needs release confidence: add Testing.
- Has latency or cost requirements: add Performance.
- Affects rights, money, safety, eligibility, or regulated advice: add Compliance.

## 4. Use Checklists In Reviews

Do not copy every checklist item blindly. Select the items that match your risk tier, then add them to:

- pull request templates;
- release review templates;
- architecture decision records;
- incident review documents;
- audit evidence folders.

## 5. Keep Evidence

For production systems, keep durable records for:

- intended use and prohibited use;
- model and prompt changes;
- data sources and retention;
- evaluation results;
- tool permissions;
- release approvals;
- incidents and corrective actions.

## 6. Validate The Repository

Run:

```powershell
./scripts/validate-framework.ps1
```

Then run:

```bash
python scripts/check_rules.py --summary
```
