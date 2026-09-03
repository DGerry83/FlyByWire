# Frozen Gates Protocol and Verdict Taxonomy

Shared protocol for `GATES.md` in every gated workflow (BugfixPlanning, PlanImplementation, Refactoring, ProjectBootstrap). Each workflow's gate *criteria* live in its own skeleton under `reference\templates\` (`GATES.md`, `GATES_REFACTOR.md`, `GATES_BOOTSTRAP.md`); this file is the authority for how gates are frozen and judged. Loaded only when a workflow points here.

## The Protocol

Before any implementation work begins (before dispatching implementer sub-agents):

1. Derive acceptance criteria from the session's contract or plan. Each gate must be independently verifiable and tied to a specific artifact, build command, or integration test.
2. Write the gates to `notes\active\[SessionFolder]\GATES.md` from the workflow's GATES template.
3. Freeze the file: record the freeze timestamp and declare "GATES.md is frozen."

**Frozen means frozen.** After `GATES.md` is written and the user approves moving into the implementation phase, do not modify it. Any post-freeze modification — including retroactive wording changes, scope narrowing, or criterion relaxation — renders the affected gate `INVALID` and is an automatic audit failure.

## Verdict Taxonomy

- **Per-gate:**
  - `PASS` — criterion met with raw evidence attached.
  - `FAIL` — criterion not met.
  - `INVALID` — criterion was altered after freezing, evidence is missing or unreliable, or the verification process was compromised.
- **Session-level:**
  - `KILL` — stop, roll back, or return to planning; the session cannot proceed safely.
  - `CONTINUE` — all gates are `PASS` (or documented `FAIL`s are accepted as follow-up work) and the session may proceed or close.

Workflows may tighten the session-level rule; the workflow file states the override when it does (e.g., BugfixPlanning requires `KILL` if any gate is `FAIL`).
