# FlyByWire v2 — Efficiency Rework: Session Handoff

**Date:** 2026-07-31
**Status:** **v2 PROMOTED (2026-07-31).** W1–W5 + W9 done; all regression gates green. Root is now v2 (verified byte-identical to `versions\v2\`, 48 files); `versions\v2\` is the frozen baseline going forward (treat like `versions\v1\`: never edit; future work starts as `versions\v3\`). `eval\ab` fixture refreshed to v2 with progressive-load staging. T2: Gemini 41/44 (exact documented residuals); Mistral 38/44 — delta is `mistral-small-latest` provider drift on byte-identical routing files (see `eval\TESTING.md` v2-validation section). T5: 16/16 with_skill (iteration-7). W6–W8 not started.
**Purpose:** Self-contained starting point for a new session to plan and execute the token-efficiency rework identified in the 2026-07-31 audit. Read this file first; it contains the version layout, the work items, and the regression-test plan.

**Progress notes (2026-07-31):**
- W1: cache-first onboarding in `CORE_PROTOCOLS.md` §3–4 with three-tier invalidation; cache template at `reference\templates\ENVIRONMENT.md`; five workflow templates rewired. T4 cache lifecycle (create → read → corrupt → self-heal) verified live.
- W2: `reference\06-implementer-prompt-skeleton.md` (Blocks A/B/C1/C2); four implementer workflows use verbatim-copy directives. T4 pointer compliance verified.
- W3: CORE §5.5 → audit-checklist form (full text stays in `reference\01-core-principles.md`), §5.7 detection column dropped, §3 compressed. CORE net +434 bytes vs v1 (cache mechanism cost ≈ compression savings).
- W4: 24 artifact skeletons externalized to `reference\templates\` (all verified verbatim against v1 except ENVIRONMENT.md, which is new). Two GATES variants disambiguated: `GATES.md` (PlanImplementation) vs `GATES_BOOTSTRAP.md`.
- W5: `reference\07-frozen-gates.md` created; BugfixPlanning keeps its stricter KILL rule as a stated override. Refactoring gates skeleton → `reference\templates\GATES_REFACTOR.md`. Checkpoint protocol centralized in CORE §8; end-of-file sections replaced with one-line pointers. Taxonomy restatements pointer-ized in 5 files.
- W9: `eval\ab\flybywire\references\` refreshed (CORE, BugfixPlanning, PlanImplementation, ChangelogInvestigator); v2 README updated. Note for T5: fixture may also need `reference\06`, `07`, and `templates\` staged if the harness resolves pointers from disk.
- T6: default sub-agent → `kimi-code/kimi-for-coding`, `primary` → `kimi-code/k3`. Confirmed.
- Route totals (CORE+Router+workflow, v1→v2): PlanImplementation −21%, Refactoring −20%, Housekeeping −16%, DesignSpecRefinement −11%, Exploration −7%, ProjectBootstrap −6%, BugfixPlanning −2%, others ≈0%.

---

## 1. Version Layout and Freeze Rules

This project is **not a git repository** — folder snapshots are the only version control. The layout is:

| Location | Role | Rule |
|---|---|---|
| Repo root (`*.md`, `reference\`) | **Live v1 skill** — the version currently installed/used. | Do not edit for v2 work. Only emergency fixes. |
| `versions\v1\` | **Frozen snapshot** of the 2026-07-31 state (15 root markdown files + `reference\`). Byte-identical to root at freeze time. | **Never edit.** This is the diff baseline and rollback path. |
| `versions\v2\` | **Frozen baseline** (promoted to root 2026-07-31; root verified byte-identical). | **Never edit.** New diff baseline and rollback path. Future work starts as `versions\v3\`. |
| `eval\` | Test infrastructure (not part of the shipped skill). | Lives at root only; not snapshotted. |

Promotion path when v2 is validated: copy `versions\v2\` files over the root files, refresh `eval\ab\flybywire\references\` (see §5), and snapshot `versions\v2\` as the new frozen baseline.

Change inventory at any point: `diff -r versions/v1 versions/v2` (Git Bash).

---

## 2. Audit Background (condensed)

Method: 11 parallel per-file audits of the workflow markdowns (full reports were reviewed; findings below are the cross-file synthesis). Line numbers refer to **v1** files.

**Token baseline (bytes on disk; ≈ tokens/4).** Every route loads CORE_PROTOCOLS + Router + one workflow:

| File | Bytes | | File | Bytes |
|---|---|---|---|---|
| CORE_PROTOCOLS.md | 16,922 | | DesignSpecRefinement.md | 20,621 |
| Router.md | 7,011 | | Exploration.md | 14,198 |
| PlanImplementation.md | 27,216 | | ProjectBootstrap.md | 11,233 |
| Refactoring.md | 26,136 | | ArtifactSecretary.md | 10,945 |
| BugfixPlanning.md | 24,256 | | UXClarity.md | 7,306 |
| Housekeeping.md | 21,267 | | ChangelogInvestigator.md | 4,983 |

Heaviest route today (PlanExecution): ~51 KB loaded before any project files are read. Target: 30–40% reduction on heavy routes, ~3–4 KB off every route via CORE_PROTOCOLS compression, and ~5–7 fewer tool calls per sub-agent delegation via the environment cache.

**Key structural findings:**

1. **Onboarding ritual repeated per delegation.** CORE_PROTOCOLS §4's sub-agent onboarding (shell detect, workspace listing, scope access, syntax check, capability check) is copied into every implementer sub-agent prompt and costs ~5–7 tool calls per delegation: BugfixPlanning:273–291, PlanImplementation:338–357, Refactoring:312–324, Housekeeping:254–258, Exploration:142–153.
2. **Sub-agent prompt scaffolding duplicated.** Four templates carry a 50–86-line delegation prompt that is ~70% identical (onboarding + mandatory disagreement + raw-results discipline): BugfixPlanning:267–335, PlanImplementation:323–397, Refactoring:298–383, Housekeeping:246–299.
3. **Frozen-gates protocol + verdict taxonomy** near-verbatim in four files: BugfixPlanning:39–52, PlanImplementation:36–67, Refactoring:40–71, ProjectBootstrap:220–241 (plus a Housekeeping variant at 30–42).
4. **Artifact taxonomy restated** despite "do not duplicate" pointers: PlanImplementation:21–34, Refactoring:25–38, ArtifactSecretary:76–82 + 90–109 + 211–215, UXClarity:19–29, ChangelogInvestigator:7–16.
5. **Embedded artifact skeletons are the largest single-file sinks:** DesignSpecRefinement:260–471 (211-line DESIGN_SPEC template = 40% of the file), PlanImplementation ~120–150 lines across 7 artifact templates, Housekeeping ~160 lines across 3, Refactoring ~130 (REFACTOR_MAP + REFACTOR_DESIGN), Exploration ~120 across 5, ProjectBootstrap:69–117, ChangelogInvestigator:69–96.
6. **CORE_PROTOCOLS carries textbook prose** charged to every route: §5.5 principles (~47 lines), §5.7 anti-patterns (~16 lines), §3 shell examples (~27 lines), §5.4 three overlapping risk tables.
7. **Checkpoint/stop-and-report phrasing** repeated ~5× per file plus a redundant end-of-file "Checkpoint Protocol" section (e.g., BugfixPlanning:451–458, Refactoring:523–529, PlanImplementation:589–595).
8. **Checkpoint-free files are fine:** UXClarity and ChangelogInvestigator are already lean; DesignSpecRefinement and ProjectBootstrap correctly use pointers. Do not "fix" them into uniformity.

---

## 3. Work Items

Ordered by tier. Each lists target files (v2 copies), implementation notes, and risks. **Do not start W6+ before W1–W3 settle.**

### W1 (Tier 1) — Lazy-init environment cache

The motivating example: shell/environment onboarding should run fully once, cache to a document, and thereafter be read instead of re-executed.

- **Cache file:** `notes\knowledge\ENVIRONMENT.md` (per-project; `notes\` already lives in the user's projects). Contents: OS, host shell + version, correct chaining operator, project root absolute path, build/test commands, detection date, machine quirks.
- **Flow:** first onboarding in a project runs the full §4 procedure and writes the cache. Every later onboarding (main agent or sub-agent) reads the cache instead of probing.
- **Invalidation protocol (three tiers — this is the critical design element):**
  1. **Verify-on-read (self-healing):** after reading the cache, run exactly one probe command using the cached chaining operator (e.g., a chained `ls`). Failure → full re-onboarding, rewrite cache.
  2. **Force refresh:** deleting `ENVIRONMENT.md` forces re-onboarding next session. Document a user phrase ("re-run environment onboarding") mapping to this.
  3. **Zero-cost staleness check:** cached project-root path vs. current working directory — mismatch → regenerate. Optionally record source mtimes (e.g., `AGENTS.md`) for finer invalidation.
- **Files to change (v2):** `CORE_PROTOCOLS.md` §3–4 (cache-first procedure + invalidation), the sub-agent prompt templates in BugfixPlanning / PlanImplementation / Refactoring / Housekeeping / Exploration (replace probing steps with "read ENVIRONMENT.md, run the verify probe").
- **Risks:** (a) stale cache is worse than no cache — tier-1 verify mitigates; (b) this machine is multi-shell: Git Bash host, Docker only via `wsl -d Ubuntu -- bash -lc "..."`, curl needs `--ssl-no-revoke`, `PYTHONUTF8=1` for `rich` — the cache must record which shell the *agent host* uses plus exceptions, not just "the machine's shell."
- **Regression tests:** T1, T4, T5.

### W2 (Tier 1) — Shared implementer prompt skeleton

Extract the ~70%-identical delegation scaffolding into a new fragment, e.g. `reference\06-implementer-prompt-skeleton.md`, loaded only by the four implementing templates.

- **Goes into the fragment:** onboarding ritual (post-W1 cache version), MANDATORY DISAGREEMENT phase, RAW-RESULTS DISCIPLINE + final-status taxonomy, acknowledgment format.
- **Stays in each template:** scope-specific constraints (BugfixPlanning's contract/gates sections, Refactoring's interface-stability rules, Housekeeping's parity rules, PlanImplementation's chunk contract).
- **Do NOT put this in CORE_PROTOCOLS.md** — CORE is loaded on every route; this material is only needed by implementer routes. Progressive loading must be preserved (the audit's accepted 3-level chain already covers workflow → reference).
- **Pointer wording must be explicit** ("copy blocks B and C from `reference\06-...` into the delegation prompt verbatim") — the Phase 3 it1/it2 experiment proved small models follow concrete instructions and degrade on abstract indirection.
- **Files:** BugfixPlanning:267–335, PlanImplementation:323–397, Refactoring:298–383, Housekeeping:246–299 (~60–70 lines saved per file).
- **Regression tests:** T1, T3, T4, T5.

### W3 (Tier 1) — Compress CORE_PROTOCOLS.md

Highest-leverage single file (loaded on every route).

- §5.5 principles: compress ~47 lines of SOLID/KISS/DRY teaching to names + project-specific twists (smell tests, inheritance-depth limit, one-sentence test). **Keep the audit-checklist phrasing** — BugfixPlanning Phase 3 and Housekeeping/Refactoring auditors cite these as authority.
- §5.7 anti-patterns: names + fix directive only.
- §3 shell constraints: one rule + one example per shell; shrinks further once W1 lands ("use the cached environment doc").
- §5.4: consider unifying the three overlapping risk tables.
- **Risk:** over-compression removes the concreteness that drives small-model compliance. Cut explanation, never directives.
- **Regression tests:** T1, T3, T5.

### W4 (Tier 2) — Externalize artifact skeletons

Move embedded markdown artifact templates to `reference\templates\*.md`; workflows reference them ("create X from `reference\templates\X.md`"). Progressive disclosure at the artifact level: skeleton read only at creation time.

- Biggest wins in order: DesignSpecRefinement:260–471 (~200 lines), PlanImplementation artifact templates (~120–150), Housekeeping (~160), Refactoring MAP+DESIGN (~130), Exploration skeletons (~120), ProjectBootstrap worksheet (~50), ChangelogInvestigator output scaffold (~28).
- **Faithfulness risk is low-to-positive** — agents copy an exact file instead of reproducing a template from context.
- **Regression tests:** T1, T3, T4.

### W5 (Tier 2) — Frozen-gates fragment + pointer-ize restatements

- Extract frozen-gates protocol + verdict taxonomy to a shared fragment (same home as W2's, or its own `reference\07-frozen-gates.md`): BugfixPlanning:39–52, PlanImplementation:36–67, Refactoring:40–71, ProjectBootstrap:220–241.
- Replace artifact-taxonomy restatements with one-line pointers: PlanImplementation:21–34, Refactoring:25–38, ArtifactSecretary:76–82 + 90–109 + 211–215, UXClarity:19–29, ChangelogInvestigator:7–16.
- Collapse each file's redundant end-of-file "Checkpoint Protocol" section into the per-phase STOP AND REPORT instructions (one canonical phrasing, referenced).
- **Regression tests:** T1, T3, T5.

### W6 (Tier 3) — Optional script accelerators

Pure markdown is a security-audit asset (Phase 0: AST01/02/08 clean by construction). Scripts must be **optional accelerators, never the normative path**: markdown instructions remain the spec ("if `scripts\` is present and Python is available, run X; otherwise do it manually as follows"). Deleting `scripts\` must lose nothing. Python stdlib only (matches `eval\run_routing_tests.py`; survives the Windows/Git Bash/PowerShell/WSL mix).

- **Best candidate — `scripts\hygiene.py`:** ArtifactSecretary's deterministic work: index generation by header-parsing across N files (currently N read calls), manifest + hashes, circular markdown-link detection, age-based folder moves (7/30-day lifecycle). Refs: ArtifactSecretary:142–178, CORE_PROTOCOLS §1.1.
- **Second candidate — session scaffolding:** dated session folder + artifact stubs from W4's `reference\templates\`.
- **Not worth scripting:** date stamps, freeze timestamps (one cheap `date` call already).
- **Also update:** `eval\phase0-audit.md` posture notes and README when scripts land.
- **Regression tests:** T1, T6.

### W7 (Tier 3) — Project-context digest

`notes\knowledge\PROJECT_DIGEST.md` (build/test commands, layout map, docs library path) with recorded source mtimes for invalidation. Moderate value: overlaps with a well-maintained `AGENTS.md`. Do after W1 proves the cache pattern.

### W8 (Tier 4) — Custom-fit guide (FITTING.md)

Document the "fit the skill to your environment" process for a general release: **generalize the mechanism, customize the content.**

- The cache docs (ENVIRONMENT.md, PROJECT_DIGEST.md) are the fitting surface: generated per user/project.
- Migrate the machine quirks currently stranded in `eval\TESTING.md` "Environment Notes" (Git Bash host shell, WSL-only Docker, `curl --ssl-no-revoke`, `PYTHONUTF8=1`, Gemini 500 req/day pacing, sub-agent concurrency cap, §7 model split) into the local ENVIRONMENT.md as the worked example.
- Cover: how to generate the docs, how to refresh/invalidate, which knobs are safe to customize.

### W9 (Housekeeping, required with every tier)

- Refresh `eval\ab\flybywire\references\` staged copies whenever a staged file changes in v2 (currently staged: SKILL.md, Router.md, CORE_PROTOCOLS.md, BugfixPlanning.md, PlanImplementation.md, ChangelogInvestigator.md).
- Update README "Updating" adaptations list for each structural change.
- The SkillBenchmark bundle at `~/source/repos\SkillBenchmark\skills\flybywire\SKILL.md` bundles only SKILL.md + Router.md — refresh only if those two change (they shouldn't; see Guardrails).

---

## 4. Guardrails (read before changing anything)

1. **Do not change `Router.md` or `SKILL.md` classification/routing logic.** Keeping them stable preserves the meaning of the routing-test baseline (T2). Cosmetic edits are acceptable but unnecessary — skip them.
2. **Cut prose, never directives.** The Phase 2 A/B result (+50pp) came from process discipline baselines skip: checkpoints, frozen gates, mandatory disagreement, raw-results. These survive compression verbatim (possibly moved, never deleted). T5 enforces this mechanically.
3. **Small-model concreteness.** Phase 3 it1/it2: concrete examples beat abstract rules; overcorrection/regression risk is real when rewording operational instructions. Prefer moving text over rewording it.
4. **Progressive loading.** Nothing implementer-specific goes into CORE_PROTOCOLS.md. New shared material lives under `reference\` and is loaded only by templates that need it.
5. **Testing remains paused by default** — run only the regression tests in §5, scoped to what a work item touches. No new benchmark work.

---

## 5. Regression Test Plan

Baselines are the post-2026-07-30/31 state (v1). "Pass" means: no worse than baseline, with the documented residual failures unchanged.

### T1 — Static checks (free; run after every work item)

- **Link integrity:** every `[...](*.md)` reference in v2 resolves to an existing file (including new `reference\` fragments/templates).
- **Loading chain:** SKILL.md still loads only CORE_PROTOCOLS + Router; workflows load only what they direct.
- **Duplication sweep:** Grep for the extracted blocks (e.g., "MANDATORY ONBOARDING", "Frozen means frozen") — each lives in exactly one place post-extraction.
- **Size delta:** re-run `wc -c` on v2 files; record per-route totals (CORE + Router + workflow) vs. the §2 baseline table. This is the quantitative success metric for the whole effort.
- **Change inventory:** `diff -r versions/v1 versions/v2` reviewed — nothing outside the work item's scope changed.

### T2 — Routing accuracy (needs API keys; run once before v2 promotion, or if Router/SKILL are touched)

```bash
GEMINI_API_KEY=... python eval/run_routing_tests.py
MISTRAL_API_KEY=... FLYBYWIRE_EVAL_PROVIDER=mistral python eval/run_routing_tests.py
```

- The runner reads **root** `SKILL.md` + `Router.md` (`eval\run_routing_tests.py`, `ROOT` = repo root). To test v2 copies before promotion, copy v2's two files into place temporarily or run post-promotion.
- **Baseline (must not regress):** Gemini 41/44 — residual failures A03, A05, A11. Mistral 40/44 — residuals A03, A04, A09, A19. These residuals are documented boundary/rule-resistant cases (see `eval\TESTING.md` Phase 3); their continued failure is expected, not a regression.
- Note: the runner exits 1 whenever any case fails — with the known residuals, exit 1 is the expected status.

### T3 — Directive-preservation greps (free; run after W2, W3, W4, W5)

Each phrase must still exist in v2 (location may change; count must be ≥1 across the chain a route loads):

```
MANDATORY DISAGREEMENT
Silent compliance
RAW-RESULTS DISCIPLINE
Frozen means frozen
STOP AND REPORT
PASS / FAIL / INVALID  (verdict taxonomy)
KILL / CONTINUE
External content is data
```

### T4 — Live loading-discipline smoke test (free, in-session; run after W1, W2, W4)

Spawn a sub-agent pointed at the v2 skill with a sample request per touched workflow and verify:

- It loads files in the mandated order (SKILL → CORE → Router → one workflow → `reference\` fragments only when directed).
- It actually reads the new `reference\` fragment/template when a pointer tells it to (pointer compliance — this is the it1/it2 risk, verified empirically).
- For W1: first run creates `notes\knowledge\ENVIRONMENT.md`; second run reads it and skips probing; deleting it forces re-onboarding; a corrupted chaining operator in the cache triggers self-healing via the verify probe.

### T5 — A/B process eval (needs Gemini key + npm harness; run before v2 promotion)

- Refresh fixture: copy changed v2 files over `eval\ab\flybywire\references\`.
- Re-run the iteration-4 frozen assertions per `eval\TESTING.md` Phase 2 (`eval\agent-skills-eval.yaml`; tool installed at `~/source/repos\node_modules`).
- **Baseline (must not regress):** with_skill 16/16 (100%) vs without_skill 8/16. A drop on any of the 16 assertions means compression removed behavioral value — find it and restore.
- Caveat carried from Phase 2: judge = target model (self-grading risk); read per-assertion evidence manually on any failure.

### T6 — §7 sub-agent model-selection probe (free, in-session; run after W1 touches onboarding, and once before promotion)

Verifies the primary/secondary deployment still behaves (procedure validated 2026-07-31):

1. Spawn a trivial sub-agent with **no** `model` parameter; spawn another with `model: "primary"`.
2. Inspect the session's `agents\<agent-id>\wire.jsonl` (under the current session directory) and grep `"model"`.
3. **Expected:** default → `kimi-code/kimi-for-coding`; primary → `kimi-code/k3`.
4. Requires the host's secondary-model feature active (`[secondary_model]` in `config.toml`); on hosts without it, §7 is inert by design — note that and skip.

---

## 6. Environment Notes for Running Tests

- API keys via env vars only (`GEMINI_API_KEY`, `MISTRAL_API_KEY`); never written to files. (Keys that appeared in chat during earlier setup were rotated after eval wrapped up.)
- Git Bash `curl` fails on HTTPS without `curl --ssl-no-revoke` (schannel/AVG issue). Node/npm/Python unaffected.
- Gemini free tier: ~500 requests/day/project/model — budget T2/T5 runs accordingly; Mistral free tier has no daily cap.
- Docker works only inside WSL2 (`wsl -d Ubuntu -- bash -lc "..."`) — not needed for any test above.
- `PYTHONUTF8=1` required on Windows for anything using `rich` (SkillBenchmark only).

---

## 7. Definition of Done for v2

- All Tier 1 items (W1–W3) implemented in `versions\v2\`; Tier 2+ scoped by the planning session.
- T1 static checks green; T3 preservation greps green; T4 smoke tests pass on every touched workflow.
- T2 routing baselines hold (41/44 Gemini, 40/44 Mistral with the documented residuals only).
- T5 A/B holds 16/16 with_skill.
- Per-route token table (§2 format) regenerated for v2 showing the reduction.
- `eval\ab` fixture refreshed; README updated; v2 promoted to root and re-frozen.
