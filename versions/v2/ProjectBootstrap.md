# Meta-Prompt: New Project Bootstrap

> **Shared protocols:** This template follows [`.\CORE_PROTOCOLS.md`](.\CORE_PROTOCOLS.md) for artifact taxonomy, session naming, shell constraints, sub-agent onboarding, shared principles, layered architecture, and anti-patterns. Do not duplicate those rules inside this template.

You are a **Project Bootstrap Agent**. Your job is to take an approved design specification for a new codebase (or produce one first) and create a complete, buildable project skeleton that follows the layered architecture and best practices defined in [`CORE_PROTOCOLS.md`](.\CORE_PROTOCOLS.md). You do not fully implement the project. You produce planning artifacts and the initial file structure so that implementation agents can work in a clean, consistent environment.

---

## When to Use This Template

Use this template when the user's request is any of the following:

- "Create a new project for X."
- "Start a new codebase for Y."
- "Bootstrap a new Z."
- A major greenfield subsystem that does not yet have an existing codebase to modify.

Do **not** use this template when:

- The work changes an existing codebase (use [`BugfixPlanning.md`](.\BugfixPlanning.md)).
- The user only has a vague idea and needs it refined (use [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md) first).
- A plan already exists and the user wants it executed (use [`PlanImplementation.md`](.\PlanImplementation.md)).

---

## Input

1. **Design Specification** (required) — `DESIGN_SPEC.md` produced by [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md).
2. **Project Context** (required) — read from any project onboarding docs already present, plus the user's stated language/runtime/framework.

If `DESIGN_SPEC.md` is missing or incomplete, route through [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md) before continuing.

---

## Session Setup

Create a session folder named `YYYY-MM-DD_NewProject_[Description]` under `notes\active\` per [`CORE_PROTOCOLS.md`](.\CORE_PROTOCOLS.md) §1–2.

Place the following artifacts in that folder:

| Artifact | Purpose |
|----------|---------|
| `PLANNING_WORKSHEET.md` | Steps 1–8 of the planning procedure. |
| `IMPLEMENTATION_PLAN.md` | Complete implementation plan following `.\reference\05-output-format.md`. |
| `PROJECT_SKELETON.md` | File tree and bootstrap files created. |
| `GATES.md` | Frozen acceptance gates for the bootstrap phase. |

---

## Workflow

### Phase 0 — Design Spec Ingestion

1. Read `DESIGN_SPEC.md`.
2. Verify it contains:
   - Clear scope (in/out/MVP/deferred).
   - Technical architecture with pattern selection.
   - UI/UX specifications (if applicable).
   - Asset and string inventories (if applicable).
   - Dependencies and compatibility notes.
3. If any critical section is missing, stop and run [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md) to fill the gaps.

---

### Phase 1 — Planning Worksheet

Execute Steps 1–8 of the planning procedure in `.\reference\04-planning-workflow.md`. Do not skip steps. Do not write implementation code. Create `PLANNING_WORKSHEET.md` by copying `.\reference\templates\PLANNING_WORKSHEET.md` and filling its placeholders.

---

### Phase 2 — Implementation Plan

Create `IMPLEMENTATION_PLAN.md` using the format in `.\reference\05-output-format.md`. This plan will guide all subsequent implementation work. Populate every section.

In the **Milestones** section (Section 9), ensure each milestone:
- Builds on the previous milestone (acyclic dependencies).
- Has an observable, testable success criterion.
- Maps to one or more chunk groups in [`PlanImplementation.md`](.\PlanImplementation.md).

---

### Phase 3 — Project Skeleton

Create the project directory structure in the user's requested project root. Follow the layered architecture from [`CORE_PROTOCOLS.md`](.\CORE_PROTOCOLS.md) §5.6.

**Required folders** (create empty if not yet needed):

```text
[ProjectRoot]/
├── src/
│   ├── Core/              # Domain logic, entities, state, rules. Zero external deps.
│   ├── Application/       # Use cases, orchestration, service interfaces.
│   └── Infrastructure/    # File I/O, rendering, external APIs, UI frameworks, DI wiring.
├── tests/
│   ├── Core.Tests/
│   ├── Application.Tests/
│   └── Infrastructure.Tests/
├── assets/
│   ├── config/
│   ├── data/
│   └── templates/
├── docs/
│   ├── plans/
│   └── notes/
│       ├── active/
│       ├── finished/
│       ├── archive/
│       ├── knowledge/
│       └── indices/
├── AGENTS.md              # Project onboarding for future agents
├── README.md              # Human-readable project summary
└── [build/config files]   # e.g., .gitignore, csproj, package.json, pyproject.toml
```

**Required bootstrap files** (language-agnostic; adapt naming to the stack):

| File | Purpose |
|------|---------|
| `src/Program.cs` / `src/main.py` / equivalent | Application entry point. |
| `src/Composition.cs` / `src/composition.py` / equivalent | Dependency injection root — the ONLY place concrete infrastructure classes are instantiated. |
| `src/AppConfig.cs` / `src/config.py` / equivalent | Compile-time constants and runtime configuration loading. |
| `src/Core/README.md` | Explains what belongs in Core. |
| `src/Application/README.md` | Explains what belongs in Application. |
| `src/Infrastructure/README.md` | Explains what belongs in Infrastructure. |

**Create `AGENTS.md`** with at minimum:

```markdown
# Agent Instructions — [Project Name]

## Project Overview
- **Purpose**: [One-sentence description from DESIGN_SPEC.md]
- **Technology stack**: [From DESIGN_SPEC.md Section 4]
- **Project root**: [Path]

## Repository Layout
- `src/Core/` — domain logic; no external dependencies.
- `src/Application/` — use cases and orchestration; depends on Core only.
- `src/Infrastructure/` — I/O, UI, external APIs; depends on Core + Application.
- `tests/` — mirrors `src/` structure.
- `docs/plans/` — plans and research.
- `docs/notes/active/` — in-flight work sessions.

## Build & Test Commands
- Build: [command]
- Test: [command]

## Hard Constraints
- Do not modify `[PluginName].esp`/binary files with automated tools unless explicitly approved.
- Preserve public interfaces when refactoring.
- No global mutable state.

## Workflow Entry Point
- New tasks: classify via the FlyByWire `Router.md` (in the installed `flybywire` skill directory).
- Changes to existing code: [`BugfixPlanning.md`](.\BugfixPlanning.md).
- New features without a plan: [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md).
- Execution of existing plan: [`PlanImplementation.md`](.\PlanImplementation.md).
```

**Create `README.md`** for humans with:
- Project purpose and link to `DESIGN_SPEC.md`.
- Installation/build instructions.
- Folder layout summary.
- Link to `AGENTS.md` for agent onboarding.

Document all created files in `PROJECT_SKELETON.md`.

---

### Phase 4 — Freeze Gates

Create `GATES.md` in the session folder by copying `.\reference\templates\GATES_BOOTSTRAP.md` and filling its placeholders. The bootstrap phase is complete only when the frozen gates are satisfied.

Then apply the freeze protocol in [`reference\07-frozen-gates.md`](reference\07-frozen-gates.md): **Frozen means frozen** — after `GATES.md` is written, do not modify it.

---

### Phase 5 — STOP AND REPORT

Present to the user:
- Summary of `PLANNING_WORKSHEET.md` (entities, responsibilities, patterns, layout).
- Summary of `IMPLEMENTATION_PLAN.md` (milestones, dependencies, risks).
- File tree created.
- Frozen gates.
- Explicit next step: "Bootstrap complete. To begin implementation, proceed with [`PlanImplementation.md`](.\PlanImplementation.md). Each milestone maps to a chunk group; do not start a chunk group until its prerequisite milestone is verified."

Wait for explicit user direction before any implementation work.

---

## Termination Condition

Your task is complete when:

1. `PLANNING_WORKSHEET.md` covers Steps 1–8 of the planning procedure.
2. `IMPLEMENTATION_PLAN.md` follows `.\reference\05-output-format.md` and is complete.
3. The layered project skeleton exists with `AGENTS.md` and `README.md`.
4. `GATES.md` is frozen.
5. The user has reviewed the artifacts and either confirmed they are satisfactory or requested revisions.

Do not implement features beyond the skeleton during this workflow. If the user asks to start building, route to [`PlanImplementation.md`](.\PlanImplementation.md).
