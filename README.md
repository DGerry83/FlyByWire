# FlyByWire — Protocol-Driven Workflow Skill

FlyByWire is an agent skill that turns a set of meta-prompt workflow templates into a progressive-loading skill for AI coding agents (Kimi Code CLI, Claude Code, or any Agent-Skills-compatible tool).

The agent acts as a **Workflow Router**: it loads the shared core protocols, classifies your request into one of 11 task classes, loads exactly one specialized workflow template, and begins its first phase. Work stays consistent, auditable, and minimal in scope.

## Repository Layout

This repository is the FlyByWire **project** — the skill itself lives in a versioned folder, not at the root.

```
FlyByWire/
├── versions/
│   ├── v3/            ← current canonical skill (install this one)
│   │   ├── SKILL.md       skill entry point
│   │   ├── Router.md      classification taxonomy
│   │   ├── CORE_PROTOCOLS.md + workflow templates
│   │   ├── reference/     planning guides and artifact skeletons
│   │   └── README.md      skill documentation (usage, template index)
│   ├── v2/            ← archived snapshot
│   └── v1/            ← archived snapshot
├── notes/             ← project working documents (plans, design notes)
└── eval/              ← evaluation harnesses, fixtures, and results (generated reports gitignored)
```

## Installation

Copy (or symlink) `versions/v3` into a skills scan location under the name `flybywire`:

```bash
# Kimi Code CLI — user level, macOS/Linux/Git Bash (available in every project)
cp -R versions/v3 ~/.kimi-code/skills/flybywire

# Claude Code — personal, macOS/Linux/Git Bash (all projects)
cp -R versions/v3 ~/.claude/skills/flybywire
```

```powershell
# Kimi Code CLI — user level, Windows PowerShell
Copy-Item -Recurse versions\v3 "$env:USERPROFILE\.kimi-code\skills\flybywire"

# Claude Code — personal, Windows PowerShell
Copy-Item -Recurse versions\v3 "$env:USERPROFILE\.claude\skills\flybywire"
```

Full usage documentation, the template index, and the shared-rules description live in [`versions/v3/README.md`](./versions/v3/README.md).

### No installation (manual)

Point your agent at the current version's entry file:

> "Read `versions/v3/SKILL.md` in this repo and follow its loading sequence for this task: ..."

## What to Expect

FlyByWire is a **heavyweight, interactive** skill — know this before installing:

- **Every phase ends in a checkpoint.** The agent saves its working artifacts, summarizes, and waits for your approval before proceeding. Even "generate a changelog" becomes a short gated session rather than a one-shot answer.
- **It writes artifacts into your project** (see below). Sessions are meant to be auditable and resumable, not disposable.
- **Escape hatch:** for trivial tasks, just tell the agent to skip the skill ("answer directly, no workflow") — or invoke it explicitly only when you want the full process.

## What It Creates in Your Repo

Routed sessions write Markdown artifacts under an **artifact root**, which defaults to `.flybywire/` in your project:

```
.flybywire/
├── active/     in-flight session folders (contracts, logs, reports)
├── finished/   completed sessions (moved after 7 days)
├── archive/    long-term storage (after 30 days)
├── knowledge/  consolidated docs, incl. the ENVIRONMENT.md cache
├── plans/      plans, research, investigation outputs
└── indices/    master index linking sessions to work
```

A project can relocate the tree by declaring a different artifact root in its `AGENTS.md`. Add `.flybywire/` to your `.gitignore` if you don't want to commit session artifacts.

## Evaluation

The skill has been evaluated several ways — full details, raw data, and honest caveats in [`eval/TESTING.md`](./eval/TESTING.md):

- **Routing accuracy:** 21/21 on the initial classification suite and 41/44 (Gemini flash-lite) on the adversarial 44-case set, on small free-tier models.
- **Process discipline (A/B):** with the skill, a small model passed 16/16 process assertions (investigate-before-fix, contract-first, checkpoint gating) vs 8/16 without — +50pp.
- **Autonomous patch-bot execution (Multi-SWE-bench slice):** 12/28 with vs 14/28 without — a **null result**, within noise.

What these do **not** show: benefit on frontier models, code-quality improvement, or statistically powered deltas (small samples, free-tier models, single runs). Notably, the Multi-SWE-bench result says the skill doesn't help an autonomous patch-bot — it says nothing about the human-agent collaboration it is designed for, which no standard benchmark measures. Treat the evals as internal validation shared for transparency, not as benchmark claims.

## Versioning Policy

- The **highest-numbered folder** under `versions/` is the live, canonical skill. Changes to workflows are made there in place.
- When a set of changes is substantial enough to matter to consumers already pointing at the current version, snapshot the folder as the next version (`v4`, etc.) and leave the previous one untouched as an archive.
- External projects should point at a specific version folder so upgrades are explicit. Git tags (e.g. `v3.1.0`) mark promotion points; see [`CHANGELOG.md`](./CHANGELOG.md).

## Project Notes

`notes/` holds project-level working documents that are not part of the shipped skill — e.g. [`notes/EFFICIENCY_V2_PLAN.md`](./notes/EFFICIENCY_V2_PLAN.md), the design record for the v2 efficiency rework, and [`notes/V3_PLAN.md`](./notes/V3_PLAN.md), the plan and rationale for the v3 native-interop & hot-path checklist.

## Contributing and License

Maintainer-facing documentation (versioning mechanics, upstream sync procedure, adaptation history) lives in [`CONTRIBUTING.md`](./CONTRIBUTING.md). FlyByWire is released under the [MIT License](./LICENSE).
