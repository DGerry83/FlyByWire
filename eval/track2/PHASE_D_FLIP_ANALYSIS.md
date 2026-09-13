# Phase D — Flip Analysis: FlyByWire skill A/B on 28 Multi-SWE-bench flash instances

Date: 2026-07-30. Setup: mini-swe-agent + `mistral/mistral-small-latest`, step_limit 100, arm A = stock template, arm B = stock + FlyByWire skill in system prompt. Overall: **A = 12/28, B = 11/28**. Trajectories: `runs/pilot_{A,B}`, `runs/slice_{A,B}`; resolved sets: `runs/eval_slice_{A,B}/final_report.json`.

## 1. cli__cli-402 — skill WIN (A unresolved, B resolved)

Issue: segfault previewing an issue with no description. Gold fix: substitute `"_No description provided._"` for empty `issue.Body` in `api/queries_issue.go` (data layer).

- **Arm A** did a thorough root-cause analysis (20+ steps inside `go-termd`/`blackfriday` library internals), then guarded `utils.RenderMarkdown` to return `""` for empty input. Crucially, A **noticed the expected behavior and rejected it**:
  - step 39: *"Let me look at the PR description again … it mentions: `_No description provided._` comes from GitHub default value."*
  - step 43: *"The PR description mentions that `_No description provided._` comes from GitHub, but based on the bug report, the actual issue is the segmentation fault … Let me verify that our fix is complete by running all the tests."*
  - Its patch (guard in `RenderMarkdown`) fixes the crash but prints nothing, so the f2p tests asserting the placeholder failed.
- **Arm B** anchored on the PR description's expected behavior at step 8: *"The fix is to check if `issue.Body` is empty and provide a default value. According to the PR title, the default should be `_No description provided._`"* — then checked existing tests (steps 9–14: `issue_test.go`, fixtures) before editing, and applied the placeholder at the presentation layer (`command/issue.go`, `command/pr.go`). Semantically equivalent to gold for the tests → resolved.
- **Judgment: not demonstrably skill-driven.** B's trajectory contains zero routing/ceremony text (verified by marker scan). Both arms investigated and tested comparably. B won because it treated the PR description as the spec; A outsmarted itself with root-cause purity. That is a judgment difference — plausibly nudged by the skill's "follow the request" discipline, but indistinguishable from luck at n=1.

## 2. vuejs__core-11813 — skill LOSS (both Submitted; A resolved, B unresolved)

Issue: `computed` getter not receiving oldValue. Both arms found the upstream fix commit (`98864a7ef`) via `git log --all --grep="11812"` and both made the **identical, correct** source change: `computed.fn()` → `computed.fn(computed._value)` in `packages/reactivity/src/effect.ts`.

- **The difference: B also copied the commit's test change into its patch.** B step 15: *"Based on the commit diff, I need to: 1. Modify `packages/reactivity/src/effect.ts` … 2. Add a test in `packages/reactivity/__tests__/computed.spec.ts`"* — step 28: *"Now I need to add the test case to the test file as shown in the commit."*
- Eval consequence: B's `fix_patch` touches `computed.spec.ts`, which the official `test_patch` also modifies → `git apply` conflict. `runs_evalB/vuejs/core/evals/pr-11813/fix-patch-run.log`: `error: patch failed: packages/reactivity/__tests__/computed.spec.ts:33 … patch does not apply` → fix stage captured 0 tests → unresolved. The eval container died in ~1.6 s.
- **Judgment: skill-neutral, self-inflicted packaging error.** No skill ceremony in B's trajectory (step 1 goes straight to work). Both templates explicitly forbid modifying test files; B violated the shared rule out of over-faithfulness to the upstream commit, not because of the skill text. This is the single most expensive mistake in the run — a resolved instance thrown away at patch-packaging time.

## 3. jqlang__jq-2839 & fasterxml__jackson-dataformat-xml-544 — skill LOSSES via LimitsExceeded (A resolved both)

**jq-2839** (B: 98 steps → LimitsExceeded; A: 70 steps → Submitted, resolved):
- A's fix: one line in `src/jv.c` (`ctx->digits = INT32_MAX - (ctx->emax - ctx->emin - 1);`), matching the gold location.
- B targeted `src/decNumber/decNumber.c` instead (different fix location), lost **21 of 98 steps fighting the build system** (`./configure` failures, `cp /usr/share/automake-1.16/install-sh config/`, `config.guess` hunting), and its last steps were stuck on edit tooling (container has no `python`, `patch -p1` rejects, restore-from-backup loops at steps 93–98). B was **not** on the verge of success: wrong file, unvalidated build, tooling failures. No skill ceremony (step 1 is a long THOUGHT, no Routing Decision).

**dataformat-xml-544** (B: 97 steps → LimitsExceeded; A: 87 steps → Submitted, resolved):
- A fixed it in `ToXmlGenerator.java` (`checkNextIsUnwrapped()` branch for raw values) with 7 `mvn` iterations.
- B iterated mostly with manual `javac`/`java` harness compiles (only 3 `mvn` runs) and at steps 94–97 was **genuinely converging on the same insight as A** — *"The real solution is to prevent the `RawSerializer` from being used for XML properties. Let me look at how to do this properly"* while reading `ToXmlGenerator.java` — but ran out of steps before landing it. Real progress, not looping.
- B's step 1 does contain skill ceremony: *"## Routing Decision — **Classification**: Bug — **Selected Template**: BugfixPlanning.md"* — but that costs ~1 step, not 10.
- **Judgment: skill-neutral to mildly negative.** The losses come from slower/less-effective iteration (build fights, manual compile loops) against a hard 100-step budget, not from skill-induced derailment. Ceremony overhead is real but tiny (~1 step per instance where it appears).

## 4. CalledProcessError instances — infra/dataset bug, not agent behavior

All five failures are `docker run … sleep 2h` returning **exit 125** before any agent step (traceback in `runs/slice_{A,B}/minisweagent.log`, raised in `DockerEnvironment._start_container`):

- **catchorg__Catch2-2288 and BurntSushi__ripgrep-954 (both arms): deterministic dataset bug.** `make_dataset.py` built `image_name` as `mswebench/{org}_m_{repo}` preserving case → `mswebench/catchorg_m_Catch2:pr-2288` and `mswebench/BurntSushi_m_ripgrep:pr-954`. Docker repository names must be lowercase: reproduced manually — `docker run mswebench/BurntSushi_m_ripgrep:pr-954` → `docker: invalid reference format: repository name (mswebench/BurntSushi_m_ripgrep) must be lowercase`. The eval harness pulls the lowercase names fine (both images present locally), which is why scoring them worked. **Fix: lowercase `image_name` in `make_dataset.py`** (`f"mswebench/{org}_m_{repo}:pr-{number}".lower()`).
- **iamkun__dayjs-1953 (arm A only): transient.** Lowercase name, failed once at 20:17:30 while a second container was concurrently auto-pulling (-w 2); the same instance ran and **resolved** in arm B. Consistent with a concurrent-pull race / Docker Hub throttle, not a naming bug.
- None of these produced trajectories; none reflect agent behavior.

## 5. Format-death check

- **google__gson-1093 (B): died at 6 messages** — the model's first three responses each contained no tool call (`<error>No tool calls found in the response</error>` ×3 → RepeatedFormatError). Assistant content is not stored for failed parses, so the responses can't be quoted; but dying instantly on the very first turn, only in the arm whose system prompt demands *"classify the request … print the **Routing Decision** in its required format"*, points strongly at the model emitting routing prose instead of a tool call. **Best inference: skill-induced format death.** (Arm A on the same instance: Submitted, resolved.)
- **fmtlib__fmt-3158 and ponylang__ponyc-2203 (A, no skill): late deaths** — RepeatedFormatError at 198 and 160 messages respectively, i.e. after ~80–95 successful steps. ponyc-2203 even had its patch generated (last tool output is the `genbox.c` diff) but died without submitting. These are mistral-small degradation in long contexts, unrelated to the skill.
- **Baseline:** *every* trajectory in all four run dirs (51/51) contains at least one "Tool call error" retry — format flakiness is a general mistral-small behavior. Deaths: A = 2 (both late), B = 1 (immediate).
- **Skill-ceremony prevalence:** only **3 of 27** arm-B trajectories contain `Routing Decision` / `Classification:` in assistant messages: `fasterxml__jackson-dataformat-xml-544`, `anuraghazra__github-readme-stats-99`, `clap-rs__clap-4667` (all at message #2 only). gson-1093's unstored first responses would likely make it 4.
- **Judgment:** format death is predominantly a mistral-small behavior; the skill adds one specific failure mode (first-turn routing prose without a tool call) that materialized once in 27 instances.

## Bottom line

| Instance | Flip | Verdict |
|---|---|---|
| cli__cli-402 | skill win | B followed the PR description as spec; A rejected it for root-cause purity. No visible skill discipline — judgment/luck, weakly attributable. |
| vuejs__core-11813 | skill loss | Identical correct fix in both; B packaged a test-file change → patch conflict → unresolved. Skill-neutral self-inflicted error. |
| jqlang__jq-2839 | skill loss | B: wrong file + 21 steps of build fights + tooling failures; not converging. Skill-neutral. |
| fasterxml__jackson-dataformat-xml-544 | skill loss | B converging on A's fix but too slow for 100 steps; ceremony cost ~1 step. Skill-neutral to mildly negative. |
| Catch2-2288 / ripgrep-954 (both arms) | infra | Uppercase `image_name` dataset bug → docker exit 125. Fix `make_dataset.py`. |
| dayjs-1953 (A) | infra | Transient concurrent-pull failure; resolved in B. |
| google__gson-1093 (B) | skill loss | Immediate format death; skill-induced routing prose is the best inference. |

**Overall: the skill was ~neutral on this slice (A 12/28, B 11/28), and the delta is noise-shaped.** The only plausibly skill-attributable effects are both negative and rare: one instant format death (gson-1093) and ~1 step of ceremony in 3/27 instances. The biggest observed losses (vuejs-11813 packaging error, jq-2839 build fights) are generic mistral-small weaknesses that hit arm B by chance. The single win (cli-402) shows no skill fingerprint. A larger n and a first-turn format constraint in the skill text ("your Routing Decision must accompany a tool call") would be the cheapest improvements.
