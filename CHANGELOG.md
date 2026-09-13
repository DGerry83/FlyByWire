# Changelog

All notable changes to the FlyByWire skill and project. The live skill is the highest-numbered folder under `versions/`; tags mark promotion points.

## [v3.1.0] — 2026-09-13

Public-release preparation. All changes are in `versions/v3/` (the canonical skill) unless noted.

- **Artifact root moved: `notes/` → `.flybywire/`** (breaking for existing consumers). Session artifacts, the knowledge base, plans, indices, and the `ENVIRONMENT.md` cache now live under `.flybywire/` in the target project. A project may declare a different artifact root in its `AGENTS.md`. *Migration for existing users:* move your `notes/active|finished|archive|knowledge|plans|indices` trees under `.flybywire/`, or declare `notes/` as the artifact root in `AGENTS.md` to keep the old behavior.
- **Generated `AGENTS.md` no longer references a private path.** `ProjectBootstrap.md`'s template previously pointed new projects at the author's local meta-prompt library; it now references the installed skill's `Router.md`. Check any projects bootstrapped with v1–v3.0 and fix their `AGENTS.md` Workflow Entry Point line.
- **Domain-generalized vocabulary.** Fallout/Papyrus-era examples (`.psc`/`.esp`/`.pex`, `F4B_*`, `SAKR`) replaced with neutral software examples; "players" → "users". `UXClarity.md` keeps a provenance note — it was forged on video-game settings interfaces.
- **Portability:** relative doc references converted from `.\` to `./` (literal file reads now work on POSIX); macOS/Linux install commands added to both READMEs.
- **Frontmatter:** nonstandard `whenToUse` field dropped (its content folded into `description`); `license: MIT` added.
- **Repo:** MIT `LICENSE` added; `CONTRIBUTING.md` added (maintainer docs moved out of the installable skill folder); `eval/` committed with a scope header (`eval/ab-workspace/` generated reports gitignored); v1/v2 marked as archived snapshots.

## [v3.0.0] — 2026-09-03

- Native Interop & Hot-Path Checklist: `reference/08-native-interop.md` added (process-global state, hot-path allocation, resource-acquisition symmetry), wired in via `CORE_PROTOCOLS.md` §5.9, `reference/01-core-principles.md` §10, and the `CHUNK_N_CONTRACT.md` Constraints section; `DESIGN_SPEC.md` §3.2 extended for intentional partial coverage. Plan: `notes/V3_PLAN.md`.

## [v2.0.0] — 2026-07-31

- Efficiency rework (plan: `notes/EFFICIENCY_V2_PLAN.md`): cache-first environment onboarding (`CORE_PROTOCOLS.md` §4); implementer sub-agent scaffolding extracted to `reference/06-implementer-prompt-skeleton.md`; frozen-gates protocol extracted to `reference/07-frozen-gates.md`; artifact skeletons externalized to `reference/templates/`; CORE compression; checkpoint protocol centralized (§8). ~15k tokens per typical route, down ~7–21% per route from v1. Regression gates: routing 41/44 (Gemini) holds; A/B 16/16 vs 8/16 reproduced.

## [v1.0.0] — 2026-07-30

- Initial skill: `SKILL.md` + `Router.md` + 11 workflow classes over the meta-prompt template library, with `CORE_PROTOCOLS.md` shared rules. Baselines: routing 21/21 (both providers), A/B process discipline +50pp (16/16 vs 8/16).
