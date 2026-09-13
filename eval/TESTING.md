# FlyByWire Skill — Testing Status

Last updated: 2026-07-30

> **How to read this file.** These evaluations were run as *internal validation* during development and are published for transparency, not as benchmark claims. They measure: (a) routing-classification accuracy, (b) process-discipline adherence (does the model investigate before fixing, gate on contracts, pause at checkpoints), and (c) autonomous patch-bot execution on a Multi-SWE-bench slice. They do **not** measure: benefit on frontier models, code-quality improvement, or the skill's actual design target — multi-turn, checkpointed human-agent collaboration (no standard benchmark for this exists; see Phase 4b). All runs used small free-tier models (Gemini flash-lite, Mistral small) at temperature 0, mostly single runs — treat deltas as directional, not statistically powered. The headline numbers: routing 21/21 and 41/44; A/B process discipline +50pp; Multi-SWE-bench −2/28 (null result, honestly interpreted in Phase 4). Generated A/B reports under `eval/ab-workspace/` are gitignored as regenerable.

## Phase 0 — Static Audit (done)

Full write-up: [`phase0-audit.md`](.\phase0-audit.md).

- **Spec compliance: PASS.** `SKILL.md` meets the agentskills.io standard and Kimi's directory-form requirements (name/description constraints, valid YAML, ~700-token body, progressive disclosure). Only deviation: 3-level reference chain (accepted, deliberate).
- **Security (OWASP AST10): strong.** Pure markdown, zero dependencies, no runtime fetches. One finding, **F1** — `Exploration.md` ingested untrusted web content with no prompt-injection guard — **fixed** (`CORE_PROTOCOLS.md` §5.8 + guard lines in `Exploration.md`).
- **Pre-publish items (open):** license file + `license` frontmatter field, version tags, changelog, reconsider name distinctiveness vs FlyByWire Simulations.

## Phase 1 — Routing Accuracy (done)

The skill's core job is classifying requests into 11 workflow classes. Test set: [`routing-tests.jsonl`](.\routing-tests.jsonl) — 21 prompts covering all classes plus deliberate boundary traps (investigate-don't-fix, plan-arriving-as-feature, greenfield-subsystem, ambiguous-request).

Runner: [`run_routing_tests.py`](.\run_routing_tests.py) (stdlib-only Python; provider-agnostic).

| Provider | Model | Score |
|---|---|---|
| Gemini | gemini-3.1-flash-lite | **21/21** |
| Mistral | mistral-small-latest | **21/21** |

Raw responses preserved in `eval/results/`. Edge-case reasoning was spot-checked manually on both providers — genuine correct classification, not parser artifacts.

Re-run commands (Git Bash):

```bash
GEMINI_API_KEY=... python eval/run_routing_tests.py
MISTRAL_API_KEY=... FLYBYWIRE_EVAL_PROVIDER=mistral python eval/run_routing_tests.py
```

## Phase 2 — A/B Quality Test (done)

Tool: `agent-skills-eval` (npm; installed at `~/source/repos\node_modules` — npm walked up to a `package.json` in the `repos` parent folder). Config: [`agent-skills-eval.yaml`](.\agent-skills-eval.yaml). Fixture: [`ab/flybywire/`](.\ab\flybywire) — SKILL.md + the protocol files staged under `references/` (the harness inlines `references/` recursively into the with_skill context; **stage only what the tested routes load progressively** — see the staging lesson in the v2-validation section below — and **refresh these copies if the protocols change**).

Four tasks graded on process assertions the bare model should fail: bug triage (investigation before fix), feature (contract-first, checkpoint gating), plan execution (feasibility check + verifiable chunks), changelog (categorized human-readable notes). Target and judge both `gemini-3.1-flash-lite` (`gemini-2.5-pro` judge had no usable free quota — 429s), temperature 0.

**Final result (iteration-4, frozen assertions): with_skill 16/16 (100%) vs without_skill 8/16 (50%) — +50pp.**

| Eval | with_skill | without_skill |
|---|---|---|
| Bug triage | 4/4 | 2/4 |
| Feature contract-first | 4/4 | 0/4 |
| Plan execution | 4/4 | 2/4 |
| Changelog | 4/4 | 4/4 (tie — baselines write good changelogs unaided) |

HTML report: `eval/ab-workspace/iteration-4/report/index.html`. Raw outputs in `eval/ab-workspace/iteration-4/eval-*/`.

Methodology notes (read before trusting the number):

- Assertions were calibrated across iterations 2→4 (75% → 81.3% → 100% with_skill; baseline 43.8% → 50%). Early assertions demanded artifacts (contract, frozen gates) that the protocol deliberately defers behind user-approval checkpoints — they tested behavior the skill *prohibits*. The frozen set tests stage-appropriate value: correct routing, investigation/scope-check before code, implementation gated behind design + approval, checkpoint pausing. Iteration-4's number is the honest one to quote; earlier iterations are calibration history.
- Judge = target model (self-grading risk). Mitigated by objective, process-shaped assertions; per-assertion evidence was read manually.
- The harness is single-shot: it measures response structure and process discipline, not the full multi-turn workflow (progressive file loading, real checkpoints, sub-agents). Loading discipline was verified separately with live subagent smoke tests.
- The changelog tie is informative: the skill's lift is largest on tasks where bare models jump straight to code (feature: 0/4 baseline) and smallest where the baseline is already strong.

Efficiency data point: with_skill calls averaged ~20.3k tokens vs ~0.7k baseline (harness inlines all references; real progressive loading is ~15k for a typical route: CORE_PROTOCOLS + Router + one workflow file).

## Phase 3 — Adversarial Routing Tests (done)

Added 23 hostile cases (A01–A23) to [`routing-tests.jsonl`](.\routing-tests.jsonl) (44 total; original R01–R21 kept intact as the regression baseline). Categories: class name-dropping with mismatched intent (A01–A04), multi-intent (A05–A06), two-tasks-in-one (A07–A08), plan-shaped traps (A09–A10), boundary rewrite (A11), routing-bypass instruction (A12), UX-flavored bug (A13), and non-gaming phrasing across all 11 classes (A14–A23).

| Provider | Model | Baseline (R01–R21) | Adversarial (A01–A23) | Total |
|---|---|---|---|---|
| Gemini | gemini-3.1-flash-lite | 21/21 | **20/23** | **41/44** |
| Mistral | mistral-small-latest | 21/21 | **18/23** | **39/44** |

(Scores above are the original Router.md; see the hardening experiment below for the post-fix numbers.)

Raw responses: `eval/results/routing-{gemini,mistral}-*-20260730T181947Z.json`. (Note: the runner exits 1 whenever any case fails, so a "failed" shell status on a completed 44-case run means test failures, not infra errors.)

Failure analysis (raw responses read manually):

- **A03 (both providers → Changelog):** "Run the changelog process … which commit introduced the regression." Both models took the process name-drop. Culprit-hunting in git history is Detective work (Bug); Changelog's trigger is producing release notes from a range. Genuine misroute, and the fact that both models failed identically makes it the strongest finding: naming a workflow in the request overrides intent.
- **A01 (Mistral → Cleanup):** took the "quick cleanup" framing; rationalized a defective formula as "behavior-preserving maintenance," which is self-contradictory (fixing negative regen values changes behavior). Genuine misroute.
- **A02 (Mistral → Bug):** took the "small bug fix" framing for adding a pause menu. Genuine misroute (new capability = Feature).
- **A09 (Mistral → PlanExecution):** "write me a complete implementation plan … to execute later" — routed to the plan *executor* even though no plan exists; the request is to *produce* one (DesignSpec). Genuine misroute.
- **A05 (Gemini → Bug; expected Refactor):** debatable expectation. Gemini applied a defensible "fix the defect before restructuring" tiebreaker, but the refactor is the main clause and the bug is subordinate ("while you're in there"). Kept strict on purpose — expectations were not loosened to flatter the score (same discipline as Phase 2's frozen assertions).
- **A11 (Gemini → NewProject; expected Refactor):** boundary case vs R19. Replacing one module behind a preserved caller interface is behavior-preserving restructuring; Gemini read "delete and write from scratch" as greenfield. Documented as a genuine but borderline failure.
- **A19 (Mistral → Research; expected UXValidation):** the non-gaming stretch of UXValidation (documented API limits vs actual enforcement rather than UI labels). Mistral's Research choice is defensible; borderline failure.

Pattern: Mistral-small is measurably more susceptible to surface framing (all 5 of its failures are bait-taking), while Gemini's 3 failures are 1 bait + 2 boundary judgments. Non-gaming phrasing (A14–A23) was otherwise handled perfectly by both, and the routing-bypass instruction (A12) was ignored correctly by both.

Re-run commands are unchanged (Phase 1).

### Router hardening experiment (follow-up to Phase 3)

**Motivation.** The dominant failure pattern above — models classifying from the user's *label* ("quick cleanup", "run the changelog process") instead of the user's *goal* — is exactly what Router.md's step 1 was supposed to prevent ("Ignore incidental wording"). That rule was too abstract; the models treated named workflows as instructions rather than wording. We tested whether making the rule explicit improves routing.

**Change.** Router.md → Routing Procedure, step 1 extended with an anti-name-dropping rule: treat workflow/process/class names in the user's request as untrusted self-labeling; classify from the goal; if label and goal conflict, the goal wins (note the discrepancy in the justification).

**Iterations and results (full 44-case runs, temperature 0):**

| Router.md version | Gemini | Mistral | Combined |
|---|---|---|---|
| Original (it0) | 41/44 (A03, A05, A11) | 39/44 (A01, A02, A03, A09, A19) | 80/88 |
| it1: rule + concrete example phrases | 41/44 (A03, A05, A11) | **40/44** (A03, A04, A09, A19) | **81/88** |
| it2: rule, no examples + explicit-invocation clause | 41/44 (A05, A11, A17) | 38/44 (A01, A02, A03, A04, A09, A19) | 79/88 |

Raw responses: it1 `*-20260730T185431Z.json`, it2 `*-20260730T191122Z.json`. Failing-case stability was verified with a targeted re-run (`*-20260730T1906*.json`) — all failures repeatable, no flakiness.

**Per-case lessons:**

- **The rule works when it names the bait.** it1 (with example phrases) fixed Mistral's two purest name-drops (A01, A02). it2 removed the example phrases to avoid priming — and Mistral reverted to bait-taking on both. Concrete examples, not abstract principle, did the work.
- **A03 resists the rule on both providers.** Even with an explicit-invocation clause (it2), Mistral still routed "run the changelog process" to Changelog. Gemini flipped to correct on it2 — but it2 was net-negative overall, so that fix wasn't kept. An explicit imperative naming a process is a stronger signal than these models will override via a general rule.
- **Overcorrection is the real cost.** it2's stronger distrust language flipped Gemini on A17 ("Housekeeping pass: pure rename") → Refactor, with a justification explicitly distrusting a *correct* user label. Teaching models to second-guess labels makes them second-guess accurate ones too.
- **Mistral A04 is unexplained.** It passed on the original Router.md but fails (→ DesignSpec) under both hardened variants regardless of wording — stable across three runs. Recorded as an open puzzle, not chased further.
- **A05, A11 (Gemini) and A09, A19 (Mistral) are unaffected by routing-rule wording** — boundary judgments / misread intent, not label-taking. Different fix needed (taxonomy clarification), if any.

**Decision: kept it1** (best combined score, zero new regressions on Gemini, fixes the two clearest bugs). it2 was reverted. Stopped at two iterations deliberately: further tuning against this exact test set risks overfitting the skill to 44 prompts. Remaining failures are documented above as either boundary cases (A05, A11, A19) or rule-resistant (A03, A09, Mistral A04) and are candidates for taxonomy-level clarification rather than more step-1 wording.

**Fixture-staleness warning:** Router.md changed in this experiment. Copies staged for other harnesses must be refreshed before reuse: `eval/ab/flybywire/references/Router.md` (Phase 2 A/B fixture) and `~/source/repos\SkillBenchmark\skills\flybywire\SKILL.md` (Phase 3b bundle).

## Phase 3b — Standardized Routing Eval via SkillBenchmark (done)

Tool: [SkillBenchmark](https://github.com/TiesPetersen/SkillBenchmark) (paired with/without-skill runs, blind rubric judge, CI statistics), cloned to `~/source/repos\SkillBenchmark` and **patched from Anthropic-only to multi-provider**: new `src/llm.py` client factory (Gemini + Mistral via their OpenAI-compatible endpoints, `SB_PROVIDER`/`SB_RUNNER_MODEL`/`SB_JUDGE_MODEL` env vars, 6s request pacing + 429 retries for free tiers); ~63 lines changed across 6 files. All 44 routing cases ported to rubric task YAMLs (`tasks/flybywire_*.yml`, leveled criteria: 80 pts classification+template, 20 pts routing-decision structure; AMBIGUOUS cases scored on question-asking behavior). The injected skill is a generated bundle (`skills/flybywire/SKILL.md` = SKILL.md body + full Router.md) — **refresh it when the protocols change**. Gotcha: `PYTHONUTF8=1` is required on Windows or `rich` crashes.

**Results (44 tasks, runs=1, judges=1, temp 0):**

| Provider | With skill (mean/100) | Without skill | With-skill task failures |
|---|---|---|---|
| Gemini flash-lite | **95.2** | 1.7 | A03 (14), A11 (18), R21 (63), A10 (95) |
| Mistral small | **90.0** | 8.6 | A01 (45), A02 (46), A03 (14), A04 (20), A09 (14), A19 (20) |

Results: `SkillBenchmark\results\flybywire__20260730_172459` (Gemini) and `flybywire__20260730_174646` (Mistral); per-task `.md`/`.json` include judge reasoning per criterion.

**Cross-validation against Phase 1/3 (same prompts, different harness):**

- **Confirms the core findings.** Gemini fails A03 and A11 here too (judge reasoning matches our manual analysis verbatim); Mistral fails the same bait cases (A01–A04, A09, A19).
- **The Router.md hardening did not transfer across harness framings.** Mistral failed A01/A02 here despite the hardened rule being injected — SkillBenchmark wraps the skill in its own system-prompt phrasing, and the it1 fix apparently depends on framing. Gemini's A05 flipped the other way (routes Refactor correctly here, scored 100, vs consistent failure in our runner). Lesson: small-model routing behavior is sensitive to how the skill is presented, not just its content.
- **Judge integrity finding (important).** Mistral-small as judge *hallucinated rubric compliance* on three without-skill outputs (A05, A09, A20 scored 100). Verified on A09: the bare model wrote a plain implementation plan with no routing decision, and the judge awarded 80/80 claiming it "clearly commits to class DesignSpec and selects template DesignSpecRefinement.md" — fabricated. The Gemini judge showed no such behavior (all without-skill scores 0–25, grounded). **Treat Mistral's with/without deltas as unreliable; its with-skill absolute scores are still credible** (its with-skill failures show it discriminates when real routing content exists). This is concrete evidence for the self-grading risk noted in Phase 2 — small judges can be captured by fluent text.

**Methodology caveats:** runs=1/judges=1 → CIs are degenerate (±inf); bump `number_of_runs_per_task` to 3 in `config.yml` for real intervals (~2h/provider at free-tier pacing). The with/without delta on routing tasks is partly tautological (a baseline model can't know an 11-class taxonomy), so per-case with-skill scores are the meaningful number. The 3 shipped caveman demo tasks were moved to `tasks_disabled/`.

Re-run (from `~/source/repos\SkillBenchmark`, keys inline, never in files):

```bash
PYTHONUTF8=1 GEMINI_API_KEY=... .venv/Scripts/python run.py
PYTHONUTF8=1 SB_PROVIDER=mistral MISTRAL_API_KEY=... .venv/Scripts/python run.py
```

## Phase 4 — Real-World Execution Eval: Multi-SWE-bench (done)

Paired A/B on real GitHub issues, deterministic execution-verified scoring (no LLM judge). Tooling: **mini-swe-agent** (LiteLLM, `mistral/mistral-small-latest`, temp 0, step_limit 100) driving Docker containers per instance; official **Multi-SWE-bench** harness for scoring (F2P/P2P test comparison). Skill injected into arm B's system prompt (same generated bundle as Phase 3b, incl. the it1-hardened Router.md); arms otherwise identical. Dataset: **Multi-SWE-bench flash** easy-tier slice — 28 instances, 4 per language × 7 languages (Go, Java, JS, TS, Rust, C, C++; flash has no Python). All runtime inside WSL2 (Docker is WSL-only on this machine). Full artifacts, scripts, configs, per-instance trajectories: `eval/track2/` (checkpoint) and `~/flybywire-track2/` (WSL).

**Result: with skill 12/28 (42.9%) vs without skill 14/28 (50.0%) — delta −2, i.e. neutral-to-slightly-negative, within noise (paired flips: 4 losses vs 2 wins).**

| Language | Arm A (no skill) | Arm B (skill) |
|---|---|---|
| Go (cli) | 2/4 | 3/4 |
| Java | 3/4 | 1/4 |
| JS | 2/4 | 2/4 |
| TS | 3/4 | 2/4 |
| Rust | 1/4 | 2/4 |
| C | 1/4 | 0/4 |
| C++ | 2/4 | 2/4 |
| **Total** | **14/28** | **12/28** |

(Absolute rates are NOT comparable to the flash leaderboard's ~25% frontier-model figure — our slice is cherry-picked easiest-tier.)

Paired flips (trajectory-verified, full evidence in `eval/track2/PHASE_D_FLIP_ANALYSIS.md`):

- **Skill losses:** gson-1093 (instant RepeatedFormatError — model answered with routing prose instead of a bash tool call; the only turn-1 death in 56 runs, in the only arm whose system prompt demands printed routing output → skill-attributable); xml-544 + jq-2839 (LimitsExceeded; one wasn't converging anyway, one was converging but slower); vuejs-11813 (both arms wrote the *identical correct fix* — arm B additionally added a test file that collided with the official test_patch, `git apply` failed → packaging error, skill-neutral).
- **Skill wins:** clap-4667, cli-402 (cli-402 examined closely: no skill fingerprint in the trajectory — arm A outsmarted itself rejecting the PR's spec text; judged luck, not discipline).

**Interpretation (read before quoting the number):**

- **The benchmark pre-consumes the skill's value.** SWE-bench tasks arrive as pre-digested, correctly-scoped problem statements — exactly what the skill's investigation/clarification/scope-check phases exist to produce. The remaining work ("write the patch") is what the skill deliberately says least about.
- **The environment disables the skill's core moves.** Clarifying questions, user-approval checkpoints, re-routing — the phase machinery — have no one to talk to in a bash-only autonomous loop. The skill was mostly inert: only 3/27 arm-B trajectories ever emitted routing text (always one block at message 2, ~1 step of overhead).
- **Format death is mostly NOT the skill.** Arm A suffered two RepeatedFormatErrors unaided (late-run, long-context mistral-small degradation); all 51 trajectories contain ≥1 format retry. The skill's only clear attributable harm is the single turn-1 death.
- **Bottom line:** measured effect of the skill in autonomous patch-bot mode ≈ 0 (−2/28, noise). This answers "does the skill help an autonomous patch-bot?" (no) — it does not answer "does it help a human-agent collaboration," which is what the skill is designed for (see Phase 4b).

**Harness bugs found and fixed during the run (all documented in `eval/track2/`):**

1. **Report-cache collision** — the harness caches per-instance reports keyed by image name under `workdir`; two arms sharing a workdir means the second arm's eval silently reuses the first arm's verdicts. Fix: isolated workdir per arm. (The pilot's initial identical 5/9 scores were this bug.)
2. **Uppercase image names** — `mswebench/catchorg_m_Catch2` → docker `invalid reference format`, killing 2 instances per arm before step 1 (CalledProcessError). Fixed in `make_dataset.py` (`.lower()`); instances rescued and scored.
3. **gen_report joins on PR number across repos** — phantom error rows (e.g. `simdjson:pr-543`) in every final report; harmless noise, real instances all scored.
4. **Stale-report aggregation** — final reports aggregate every cached report in the workdir, including older runs' (a smoke instance inflated arm A's count until workdirs were isolated).

Re-run (WSL, from `~/flybywire-track2`; scripts `phase_c.sh` / `rescue2.sh` show the full sequence; keys inline only):

```bash
wsl -d Ubuntu -- bash -lc "cd ~/flybywire-track2 && MISTRAL_API_KEY=... venv/bin/mini-extra swebench \
  --subset data/slice28_ds --split train -c configs/stock_mistral.yaml [-c configs/skill_mistral.yaml] -o runs/X -w 2"
```

Not run (deferred): Gemini arm (free tier = 500 req/day; needs multi-day resume or a paid key — configs ready: `stock.yaml`/`skill.yaml`); full 300-instance bench; the **adapted-wrapper arm** (instruct the model to keep routing decisions inside tool calls — the most promising follow-up given the gson-1093 death mechanism).

## Phase 4b — Evaluating what the skill is actually for (open)

Phase 4 confirmed a structural gap: no standardized benchmark measures FlyByWire's actual niche — multi-turn, checkpointed human-agent collaboration on underspecified tasks. The closest evidence remains Phase 2 (+50pp on process assertions) and the routing phases. Options for closing the gap: multi-turn simulation with a scripted/simulated user who answers checkpoints; underspecified-task suites where wrong-direction work is penalized; scope-creep scenarios where re-routing is the winning move. Sensei ([github.com/mondaycom/sensei](https://github.com/mondaycom/sensei), conversational-reasoning layer) and SkillTester ([arXiv:2603.28815](https://arxiv.org/pdf/2603.28815), paired utility + security probes) remain candidates; SWE-Skills-Bench ([arXiv:2603.15401](https://arxiv.org/abs/2603.15401)) was evaluated and rejected for now (repo 404 at eval time, Claude-Code-only harness, days of per-skill onboarding).

## Phase 5 — Efficiency Measurement (deferred)

Deferred — more correctness/robustness testing is higher priority. When resumed: capture per-call token usage (both APIs return it) to quantify the skill's context overhead per request, and the progressive-load chain vs loading everything upfront. Preliminary data point from Phase 2: ~20.3k tokens with skill vs ~0.7k baseline per call (harness inlines all references; real progressive loading is ~15k for a typical route).

## v2 Efficiency Rework — Validation and Promotion (2026-07-31)

v2 (W1–W5 + W9 per `EFFICIENCY_V2_PLAN.md`: cache-first environment onboarding, shared implementer-prompt skeleton `reference\06`, frozen-gates fragment `reference\07`, artifact skeletons externalized to `reference\templates\`, CORE compression, checkpoint protocol centralized in CORE §8) passed its regression gates and was **promoted to root**; `versions\v2\` is the frozen baseline. Static checks (T1), directive-preservation greps (T3), live loading-discipline smoke tests (T4), and the §7 model probe (T6) were green pre-promotion.

**T2 — routing re-run** (raw responses: `eval/results/routing-*-20260731T200724Z.json`, targeted re-run `*-20260731T201424Z.json`):

- **Gemini: 41/44 — baseline holds exactly** (residuals A03, A05, A11, unchanged).
- **Mistral: 38/44 vs 40/44 baseline** — failures A02, A03, A04, A09, A11, A19. SKILL.md and Router.md are byte-identical to the 2026-07-30 baseline runs (v2 did not touch them), so the delta is **provider drift on `mistral-small-latest`**, not the skill. Targeted re-run: A02 fails stably (the current Mistral build reverted to bait-taking on the "small bug fix" label despite the it1 rule — same framing-sensitivity seen in Phase 3b); A11 is flaky (passed on re-run; documented boundary case both providers wobble on). Per the Phase 3 stop-rule, no further Router tuning — candidate for taxonomy-level clarification if pursued at all.

**T5 — A/B re-run on v2** (`eval/ab-workspace/iteration-{5,6,7}/`):

- iteration-5: invalid — run concurrently with the Gemini routing run; 9 assertion "failures" were judge/target HTTP 429s, not behavior. Do not run Gemini harnesses in parallel on the free tier.
- iteration-6: with_skill 15/16. The single miss (bug-triage assertion #4, "creates or references a session artifact structure") was diagnosed as **fixture dilution**, not a v2 regression: the fixture had been over-staged with `reference\01/04/06/07` + all artifact templates (with_skill context 24.3k vs v1's 20.3k tokens), and the model answered with a Phase 0 summary instead of rendering the INVESTIGATION_LOG skeleton. The directive and skeleton are byte-identical in v1/v2 (`BugfixPlanning.md` Phase 0 step 4); an isolated bug-route probe at proper staging passed 4/4.
- **iteration-7: with_skill 16/16 (100%) vs without_skill 8/16 — iteration-4 baseline reproduced on v2.** With_skill context also dropped to ~17.4k tokens avg (from ~20.3k), a direct measurement of the v2 savings on these routes.

**Fixture staging rule (lesson):** the harness inlines `references/` recursively, so stage only what the tested routes load *progressively* — SKILL.md + CORE + Router + the exercised workflows (BugfixPlanning, PlanImplementation, ChangelogInvestigator), plus `references/templates/CHANGELOG.md` because the changelog eval asks for the artifact itself (v1 had that scaffold inline). Inlining fragments/templates that v2 deliberately defers (06, 07, templates for later phases) both erases the measured efficiency win and perturbs small-model output framing. Current fixture reflects this rule.

**Per-route bytes (CORE + Router + workflow, v1 → v2):** PlanImplementation 51,149 → 40,147 (−21%); Refactoring 50,069 → 39,999 (−20%); Housekeeping 45,200 → 37,833 (−16%); DesignSpecRefinement 44,554 → 39,379 (−11%); Exploration 38,131 → 35,334 (−7%); ProjectBootstrap 35,166 → 32,990 (−6%); BugfixPlanning 48,189 → 46,946 (−2%); ArtifactSecretary/UXClarity/ChangelogInvestigator/FeaturePlanning ≈ ±0–1% (CORE grew +434 B for the cache mechanism).

## Environment Notes

- API keys are supplied via env vars (`GEMINI_API_KEY`, `MISTRAL_API_KEY`); never written to files. Keys that appeared in chat during setup were rotated after evaluation wrapped up.
- Git Bash `curl` fails on all HTTPS due to a schannel revocation-check issue (AVG Web Shield suspect); workaround: `curl --ssl-no-revoke`. Node/npm/Python are unaffected.
- Docker (Desktop 4.84, Engine 29.6.2, linux/amd64) works ONLY inside WSL2 Ubuntu on this machine — not Git Bash, not PowerShell. All Phase 4 runtime is in WSL (`wsl -d Ubuntu -- bash -lc "..."`), working dir `~/flybywire-track2`. Gemini free tier is 500 requests/day/project/model (exhausts fast with agent loops + retries); Mistral free tier has no daily call cap.
