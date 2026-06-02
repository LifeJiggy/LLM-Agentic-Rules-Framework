# Adoption Playbook

This playbook turns the framework into a repeatable team workflow.

## Phase 1: Establish The Baseline

1. Assign a framework owner.
2. Choose the domains that apply to each AI system.
3. Create an AI system register for every production system.
4. Add the framework links to onboarding and architecture docs.
5. Run the repository validation scripts.
6. Select a checklist pack from `docs/checklist-packs.md`.

## Phase 2: Integrate Into Delivery

1. Add selected checklist items to pull request templates.
2. Require release evidence for P0 and P1 controls.
3. Use the model and prompt change template for behavior-changing releases.
4. Add evaluations for critical workflows.
5. Track accepted exceptions with owners and expiration dates.

## Phase 3: Operate And Improve

1. Review incidents against troubleshooting files.
2. Add new failure modes after incidents.
3. Review model, prompt, retrieval, and tool changes monthly.
4. Expand test coverage for recurring defects.
5. Publish domain ownership and review responsibilities.
6. Update `CHANGELOG.md` for non-trivial framework changes.

## Adoption Metrics

| Metric | Why It Matters |
|--------|----------------|
| Systems with owners | Prevents unmanaged AI services |
| Systems with risk tier | Aligns controls to impact |
| Releases with evaluation evidence | Improves confidence before deployment |
| Open P0/P1 gaps | Tracks production readiness |
| Expired exceptions | Reveals unmanaged accepted risk |
| Incident actions closed | Confirms lessons become controls |
