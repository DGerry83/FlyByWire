# FlyByWire — Protocol-Driven Workflow Skill

FlyByWire is an agent skill that turns a set of meta-prompt workflow templates into a progressive-loading skill for AI coding agents (Kimi Code CLI, Claude Code, or any Agent-Skills-compatible tool).

The agent acts as a **Workflow Router**: it loads the shared core protocols, classifies your request into one of 11 task classes, loads exactly one specialized workflow template, and begins its first phase. Work stays consistent, auditable, and minimal in scope.

## Installation

The whole repository *is* the skill — install by cloning (or copying) this directory into a skills scan location under the name `flybywire`.

### Kimi Code CLI

```powershell
# User level (available in every project)
git clone <repo-url> "$env:USERPROFILE\.kimi-code\skills\flybywire"

# or the tool-shared location (also scanned by other agents)
git clone <repo-url> "$env:USERPROFILE\.agents\skills\flybywire"

# Project level (only this repo)
git clone <repo-url> .agents\skills\flybywire
```

Invoke manually with `/skill:flybywire`, or let the model auto-invoke it from the skill description.

### Claude Code

```powershell
# Personal (all projects)
git clone <repo-url> "$env:USERPROFILE\.claude\skills\flybywire"

# Project level
git clone <repo-url> .claude\skills\flybywire
```

### No installation (manual)

Point your agent at the entry file directly:

> "Read `SKILL.md` in this directory and follow its loading sequence for this task: ..."

## Usage

Once loaded, the skill follows a strict sequence:

1. Reads `CORE_PROTOCOLS.md` (shared rules: artifact taxonomy, session naming, shell constraints, principles).
2. Reads `Router.md` and classifies your request.
3. Prints a **Routing Decision**, then loads the single selected template and begins its first phase.

Example prompts:

- "Fix the database connection timeout in the sync worker" → routes to `BugfixPlanning.md`
- "I want to add user authentication with OAuth" → routes to `BugfixPlanning.md` (feature mode)
- "Execute the migration plan in `notes\plans\migration.md`" → routes to `PlanImplementation.md`

## Template Index

| Template | Purpose |
|---|---|
| [`SKILL.md`](.\SKILL.md) | Skill entry point: progressive loading sequence and routing rules. |
| [`Router.md`](.\Router.md) | Classification taxonomy and routing procedure (loaded by SKILL.md). |
| [`BugfixPlanning.md`](.\BugfixPlanning.md) | Unified Architectural Change Workflow for bugfixes and features. |
| [`FeaturePlanning.md`](.\FeaturePlanning.md) | Thin wrapper that delegates feature requests to `BugfixPlanning.md` in feature mode. |
| [`Exploration.md`](.\Exploration.md) | Research and technology-choice investigations with external precedent analysis. |
| [`Refactoring.md`](.\Refactoring.md) | Structural decomposition and high-risk refactoring with API preservation. |
| [`Housekeeping.md`](.\Housekeeping.md) | Behavior-preserving cleanup: comments, strings, magic numbers, logging. |
| [`PlanImplementation.md`](.\PlanImplementation.md) | Execute a pre-written plan in small, sequential, verified chunks. |
| [`DesignSpecRefinement.md`](.\DesignSpecRefinement.md) | Refine a high-level idea or vision into a complete, implementation-ready design specification. |
| [`ProjectBootstrap.md`](.\ProjectBootstrap.md) | Create a new codebase or major greenfield subsystem from a design spec. |
| [`ChangelogInvestigator.md`](.\ChangelogInvestigator.md) | Generate a human-readable changelog from a commit range. |
| [`UXClarity.md`](.\UXClarity.md) | Validate settings/UX labels against actual behavior using blind comprehension tests. |
| [`ArtifactSecretary.md`](.\ArtifactSecretary.md) | Reorganize accumulated workflow artifacts and recommend hygiene improvements. |

## Shared Rules

All templates reference [`.\CORE_PROTOCOLS.md`](.\CORE_PROTOCOLS.md) for cross-cutting concerns:

- Artifact taxonomy and placement (`notes\active\`, `notes\knowledge\`, `notes\plans\`, `notes\indices\`)
- Session folder naming conventions
- Shell constraints (detect the active shell, use its native syntax)
- Sub-agent onboarding template
- Sub-agent model selection (host-conditional primary/secondary split; inert on hosts without a secondary-model profile)
- Shared principles: minimal change, similar-bugs sweep, facade pattern, and risk classifications

Do not duplicate these rules inside individual templates; link to `CORE_PROTOCOLS.md` instead.

## Planning Reference

The `.\reference\` directory contains the canonical planning guides that underpin the templates above:

- `00-agent-instructions.md` — standalone planning-agent entry point for the guide set.
- `01-core-principles.md` — software engineering principles.
- `02-architecture-patterns.md` — pattern catalog with "Use When" guards.
- `03-project-structure.md` — layered architecture and folder conventions.
- `04-planning-workflow.md` — 8-step planning procedure.
- `05-output-format.md` — implementation plan deliverable template.

These are not routed templates; they are referenced by `CORE_PROTOCOLS.md`, `BugfixPlanning.md`, `DesignSpecRefinement.md`, and `ProjectBootstrap.md`, and are loaded only when a workflow directs the agent to them.

## Updating

The workflow templates are based on verbatim copies of the source library, with these intentional adaptations:

- `SKILL.md` added as the skill entry point.
- `..\SCRATCH\` references repointed to `.\reference\`.
- Shell handling made shell-agnostic (`CORE_PROTOCOLS.md` §3–4 and all sub-agent prompt templates): detect the active shell during onboarding instead of assuming PowerShell.
- Feature-mode entry aligned: `Router.md` now matches `BugfixPlanning.md`'s rule that features run an abbreviated Phase 0 (scope/risk check) before Phase 1.
- `BugfixPlanning.md` retitled to match its filename.
- `CORE_PROTOCOLS.md` §7 (sub-agent model selection) added for hosts with a two-tier sub-agent model profile (Kimi CLI's `[secondary_model]` + Agent-tool `model` parameter): verifiable-output delegations omit the model parameter (secondary default); judgment-output delegations specify `primary`. Host-conditional and inert on hosts without a secondary-model profile.

To sync upstream changes, copy the updated files over and re-apply (or merge around) these adaptations.
