# Contributing / Maintainer Notes

This file is for people working on the FlyByWire **project** (this repo). If you only want to *use* the skill, see [`versions/v3/README.md`](./versions/v3/README.md) — everything below is maintainer-facing and is deliberately kept out of the installable skill folder.

## Versioning Mechanics

- The highest-numbered folder under `versions/` is the live skill; edit it in place.
- To promote: snapshot the current folder as the next version number, leave the previous folder untouched as an archive, tag the commit (`v3.1.0` style), and add a `CHANGELOG.md` entry.
- Archived versions (`v1`, `v2`) are frozen baselines — the routing-test and A/B eval baselines in `eval/TESTING.md` were measured against specific snapshots, so retroactive edits devalue the eval record.

## Adaptation History (skill vs. upstream source library)

The workflow templates are based on verbatim copies of the author's meta-prompt library, with these intentional adaptations:

- `SKILL.md` added as the skill entry point.
- `..\SCRATCH\` references repointed to `./reference/`.
- Shell handling made shell-agnostic (`CORE_PROTOCOLS.md` §3–4 and all sub-agent prompt templates): detect the active shell during onboarding instead of assuming PowerShell.
- Feature-mode entry aligned: `Router.md` matches `BugfixPlanning.md`'s rule that features run an abbreviated Phase 0 (scope/risk check) before Phase 1.
- `BugfixPlanning.md` retitled to match its filename.
- `CORE_PROTOCOLS.md` §7 (sub-agent model selection) added for hosts with a two-tier sub-agent model profile (Kimi CLI's `[secondary_model]` + Agent-tool `model` parameter). Host-conditional and inert on hosts without a secondary-model profile.
- v2 efficiency rework (2026-07-31): cache-first environment onboarding via the `ENVIRONMENT.md` cache (`CORE_PROTOCOLS.md` §4); implementer sub-agent scaffolding extracted to `reference/06-implementer-prompt-skeleton.md`; frozen-gates protocol extracted to `reference/07-frozen-gates.md`; artifact skeletons externalized to `reference/templates/`; `CORE_PROTOCOLS.md` §5.5/§5.7/§3 compressed and §8 checkpoint protocol centralized; artifact-taxonomy restatements in workflows replaced with pointers.
- v3 native-interop & hot-path checklist (2026-09-03): `reference/08-native-interop.md` added and wired in via `CORE_PROTOCOLS.md` §5.9, `reference/01-core-principles.md` §10, and the `CHUNK_N_CONTRACT.md` Constraints section; `DESIGN_SPEC.md` §3.2 extended to record intentional partial coverage as known limitations. Plan: `notes/V3_PLAN.md`.
- v3.1 public-release prep (2026-09): artifact root moved from `notes/` to `.flybywire/`; game-modding-specific vocabulary generalized (UXClarity keeps a provenance note); relative doc references converted to forward slashes; `whenToUse` frontmatter dropped, `license` field added.

To sync upstream changes, copy the updated files over and re-apply (or merge around) these adaptations.

## Frozen Surfaces

- **Do not change `Router.md` or `SKILL.md` classification/routing logic** without re-running the routing baselines (`eval/TESTING.md` Phase 1/3). The +50pp A/B result and the 41/44 routing score are only meaningful against the frozen taxonomy.
- **Cut prose, never directives** when editing workflows — the A/B result came from process discipline (checkpoints, frozen gates, mandatory disagreement, raw-results), which must survive any compression verbatim.

## Fixture Staleness

Copies of skill files staged for eval harnesses must be refreshed when the protocols change:

- `eval/ab/flybywire/references/` (Phase 2 A/B fixture — stage only what the tested routes load progressively; see the staging lesson in `eval/TESTING.md`)
- The SkillBenchmark bundle (`skills/flybywire/SKILL.md` = SKILL.md body + full Router.md) in a SkillBenchmark clone — see `eval/TESTING.md` Phase 3b.

## Eval Artifacts

`eval/ab-workspace/` is gitignored — it holds generated HTML reports and raw model outputs, regenerable via `eval/agent-skills-eval.yaml` per `eval/TESTING.md` Phase 2. Everything else under `eval/` (docs, scripts, fixtures, result JSONs, track2 configs/notes) is committed.
