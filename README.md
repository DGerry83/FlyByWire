# FlyByWire — Protocol-Driven Workflow Skill

FlyByWire is an agent skill that turns a set of meta-prompt workflow templates into a progressive-loading skill for AI coding agents (Kimi Code CLI, Claude Code, or any Agent-Skills-compatible tool).

The agent acts as a **Workflow Router**: it loads the shared core protocols, classifies your request into one of 11 task classes, loads exactly one specialized workflow template, and begins its first phase. Work stays consistent, auditable, and minimal in scope.

## Repository Layout

This repository is the FlyByWire **project** — the skill itself lives in a versioned folder, not at the root.

```
FlyByWire/
├── versions/
│   ├── v2/            ← current canonical skill (point agents here)
│   │   ├── SKILL.md       skill entry point
│   │   ├── Router.md      classification taxonomy
│   │   ├── CORE_PROTOCOLS.md + workflow templates
│   │   ├── reference/     planning guides and artifact skeletons
│   │   └── README.md      skill documentation (usage, template index)
│   └── v1/            ← archived snapshot
├── notes/             ← project working documents (plans, design notes)
└── eval/              ← evaluation harnesses and test results
```

## Using the Skill

Point your agent at the current version's entry file:

> "Read `C:\Users\Matt\source\repos\FlyByWire\versions\v2\SKILL.md` and follow its loading sequence for this task: ..."

To install it as a proper skill, copy (or symlink) `versions\v2` into a skills scan location under the name `flybywire`:

```powershell
# Kimi Code CLI — user level (available in every project)
Copy-Item -Recurse versions\v2 "$env:USERPROFILE\.kimi-code\skills\flybywire"

# Claude Code — personal (all projects)
Copy-Item -Recurse versions\v2 "$env:USERPROFILE\.claude\skills\flybywire"
```

Full usage documentation, the template index, and the shared-rules description live in [`versions/v2/README.md`](.\versions\v2\README.md).

## Versioning Policy

- The **highest-numbered folder** under `versions\` is the live, canonical skill. Changes to workflows are made there in place.
- When a set of changes is substantial enough to matter to consumers already pointing at the current version, snapshot the folder as the next version (`v3`, etc.) and leave the previous one untouched as an archive.
- External projects should point at a specific version folder so upgrades are explicit.

## Project Notes

`notes\` holds project-level working documents that are not part of the shipped skill — e.g. [`notes/EFFICIENCY_V2_PLAN.md`](.\notes\EFFICIENCY_V2_PLAN.md), the design record for the v2 efficiency rework.
