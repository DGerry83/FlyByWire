# Workflow Assessment — FlyByWire v3 vs the DearImGui-KSP External Review

**Date:** 2026-09-07
**Input:** `DearImGui-KSP\notes\active\2026-09-07_Bug_OpusReviewTriage\TRIAGE_SWEEP.md` (~270 triaged findings from a Claude Opus review; 3 severe, 16 medium WORK, ~47 low WORK, ~33 doc fixes, 7 cross-cutting themes).
**Question:** which of these issue *classes* would a generic change to the FlyByWire v3 workflow documents plausibly have prevented or caught earlier — where "generic" means no project-specific (KSP/ImGui/Unity/modding) and no language-specific (C++/C#/P/Invoke) content beyond what `reference\08-native-interop.md` already covers.
**Constraint honored:** this is assessment only; nothing under `versions\` was modified.

The project was built with DesignSpecRefinement → ProjectBootstrap → PlanImplementation, so those three templates plus CORE_PROTOCOLS and `reference\` are the surfaces examined. Note there is precedent for this loop: the 2026-09-03 external review of the same project produced v3's `08-native-interop.md` (see `DearImGui-KSP\notes\knowledge\EXTERNAL_REVIEW_2026-09-03.md`, "Workflow follow-up"). This assessment is the second iteration of that loop.

---

## Per-theme analysis

### Theme 1 — NDEBUG-stripped upstream asserts shift validation responsibility to the caller
*(G2-10, G3-22/23/24/30, O18)*

The shipped native library compiles out the vendored UI library's internal asserts, so every unvalidated enum/count/size forwarded across the boundary is undefined behavior instead of a debug assert. Several managed APIs forward caller-controlled ordinals and counts unchecked.

**Generic core:** "when you wrap or forward calls into a dependency whose safety net exists only in debug builds, the wrapping layer owns input validation." This is not language-specific — any project that vendors a library and ships a release configuration that strips that library's contracts has the same exposure.

**Verdict: genuine workflow gap, fixable generically.** `08-native-interop.md` has three checks (process-global state, hot-path allocation, resource-acquisition symmetry) but none asks "what validation did the callee rely on that your build configuration removes?" Proposed amendment A1 below. The fix's *content* (which ordinals, which ranges) stays project-specific — that part went to a project knowledge note.

### Theme 2 — Consumer-code-at-the-frame-boundary fault model
*(S1, S2, S3, G2-05, M10 — all three severe items live here)*

All three severe bugs are the same shape: a framework that invokes external (consumer/plugin) code enumerated its callback containment incompletely.

- **S1:** the exception barrier wraps the callback body but not the collection enumerator the callback can mutate; and the begin/end pair around the frame has no try/finally, so a throw skips the end call and deadlocks.
- **S2:** the "is it safe to call" predicate distinguishes session-active from session-inactive, but not operation-in-flight from operation-not-in-flight — public entry points callable in the wrong state reach native code unguarded.
- **S3:** a consumer-code invocation point (an animation setter callback) was simply never counted as a callback, so it got no containment, and a throw there re-fires every frame forever.

**Generic core:** any plugin/callback architecture must (a) enumerate *every* site where external code runs — not just the obvious registered callback, (b) define exception containment per site, (c) guarantee paired begin/end cleanup under exceptions, (d) protect iteration over registries that callbacks can mutate, (e) guard public entry points with a predicate for the *operation* state, not just the *session* state. None of this is KSP- or language-specific; it is the standard fault model for any host that runs third-party callbacks.

**Why v3 missed it:** `02-architecture-patterns.md` describes the Plugin/Mod and Event Bus patterns structurally but says nothing about callback containment. DesignSpecRefinement asks about failure modes (Q22) and edge cases (Q21) in the abstract, but never requires an *inventory of external invocation points*. PlanImplementation chunk contracts ask for verification steps, but nothing forces an adversarial-consumer test. And critically, the `08-native-interop.md` trigger (CORE_PROTOCOLS §5.9: "touches P/Invoke, native loading, or per-frame code") does not include "invokes external/plugin code" — the callback-boundary components could pass every conditional checklist without ever being asked these questions.

**Verdict: the most important gap this review exposes. Fixable generically.** Proposed amendments A2 (containment inventory) and A3 (trigger condition + adversarial gates).

### Theme 3 — Per-frame write amplification
*(G3-08/09/14/16 — one fix closes four items)*

A UI slider drag rewrote a config file from scratch, non-atomically, inside a held frame lock, on every changed frame — plus rebuilt and re-applied a whole theme per frame.

**Generic core:** Check 2 of `08-native-interop.md` asks only about heap *allocation* on hot paths. The actual family is broader: hot-path *side effects* — I/O, persistence, full rebuilds of derived state, and work done inside held locks, triggered per input event rather than coalesced. "Debounce/dirty-flag/coalesce, and persist atomically" is generic engineering guidance applicable to any UI-driven settings system.

**Verdict: workflow gap, fixable generically.** Proposed amendment A4 broadens Check 2. The atomic-write half (temp-file-then-rename) is a one-line generic addition to the configuration strategy guidance in `03-project-structure.md` §6.

### Theme 4 — Docs drift
*(~33 doc fixes; the damaging subset promises behavior the code doesn't have — guards, end-of-frame asserts, disposal safety)*

Two sub-classes:

1. **Stale small claims** (build recipes, file listings, attributions, line citations). Inherent to any fast-moving project; a workflow can sweep for them but not prevent them.
2. **Docs promising nonexistent behavior** — these are worse because consumers rely on them (e.g. a documented "no-op, never an exception" guarantee that S2 showed false; a documented empty-ID guard only one widget implements; an end-of-frame assert that the release build compiles out).

**Generic core for sub-class 2:** a behavioral promise in user-facing docs is an acceptance criterion and should be held to the same standard as one: traceable to a gate, a test, or deleted. PlanImplementation's Phase 5 audit verifies the *plan's* gates but has no step that re-verifies *documentation claims* against shipped code at closure.

**Verdict: partially addressable.** Proposed amendment A5 (docs-truthfulness sweep at session closure). Sub-class 1 is inherent to AI-assisted development — see "Not addressable" below.

### Theme 5 — Hand-mirrored constants across the ABI without pins
*(I18 handshake version, N13/T19 enum ordinals, I23 render-event id literal, T18/T23 missing pin tests)*

The same value is hand-maintained in two places that must agree, with no build-time cross-check anywhere. This exact risk was already flagged as a "nice-to-have" in the 2026-09-03 review and was not converted into a rule.

**Generic core:** "any constant, ordinal, identifier, or layout duplicated across a component boundary must have a mechanical agreement check (pin test, static assertion, or generated single source) or be explicitly recorded as an accepted risk." Fully generic — applies to any two-component system with a stable interface, in any language pair.

**Verdict: workflow gap, fixable generically.** Proposed amendment A6: a fifth check in `08-native-interop.md` plus a contract-template field so the answer is recorded per chunk rather than swept under "NOTE".

### Theme 6 — Latent/unreachable findings and how to record them
*(large share of NOTEs: real mechanism, unreachable today)*

Not a prevention problem — a record-keeping problem. The triage itself says these need "a single knowledge note on how to record these so they don't get re-litigated." Without a standard format, every future review re-derives the same latent findings and spends triage effort re-classifying them.

**Generic core:** audit/review workflows should have a standing "accepted latent risk" record convention: mechanism, why it is unreachable today, what change would activate it, where it is recorded. This slots naturally into the frozen-gates/audit artifacts (verdict taxonomy already has NOTE-like concepts implicitly; it lacks an activation-condition field).

**Verdict: small generic amendment worth making.** Proposed amendment A7. The project's own instance went to a knowledge note.

### Theme 7 — Demo/reference code teaches by example
*(D-series demo bugs; G2-12 where docs recommend the same bad constant the demo ships)*

Consumers copy example code and doc-recommended constants verbatim, so bugs in samples amplify into every consumer.

**Generic core:** "shipped example/sample/template code is production code for review purposes" — one sentence, universally applicable. Plus its corollary: documentation must never recommend a value or pattern that diverges from the shipped example.

**Verdict: worth a one-line generic principle** (amendment A8). The *detection* of any specific demo bug (orbital mechanics, staging math) is domain knowledge — not workflow-addressable.

---

## Proposed generic workflow-doc amendments

All phrased to be project- and language-neutral. File paths relative to `versions\v3\`.

- **A1 — `reference\08-native-interop.md`, new Check 4 "Callee validation stripped by build configuration":**
  > *When this chunk forwards values into a dependency (vendored library, external component, engine API) whose internal validation exists only in a debug/development configuration that the shipped build removes: every forwarded enum, ordinal, index, count, and size must be validated at the boundary, or the chunk contract must record an explicit trust decision with its rationale.*
  Why: theme 1. Six findings in one family; the release build's stripped asserts were known at design time but no checklist question made any chunk answer for it.

- **A2 — `reference\02-architecture-patterns.md` (Plugin/Mod Architecture + Event Bus sections) and `reference\templates\CHUNK_N_CONTRACT.md`: external-callback containment inventory.**
  Any design, chunk, or audit for a component that invokes external/plugin/callback code must include an inventory of **every** invocation site, and for each site answer four questions: (1) Is an exception from the external code contained (caught, logged, isolated from other consumers)? (2) Can the external code mutate a collection currently being iterated — if so, is iteration over a snapshot or are mutations deferred? (3) Is every begin/end or acquire/release pair around the invocation protected so the end half runs even when the external code throws? (4) What state predicate guards each public entry point, and does it distinguish "operation in flight" from merely "session active"? Why: theme 2 — all three severe findings are instances of an unanswered inventory question (S1 = Q2+Q3, S2 = Q4, S3 = Q1 at an unenumerated site).

- **A3 — `CORE_PROTOCOLS.md` §5.9 trigger extension + gate requirement.**
  Add "invokes external, plugin, or consumer-supplied code" as a trigger condition alongside P/Invoke/native-loading/per-frame, pointing at the A2 inventory. For any such component, frozen gates must include at least one adversarial-caller test: a callback that throws, a callback that re-enters the framework (register/unregister/reentrant calls), and a public call made outside its valid window. Why: the severe items survived because verification was "compile + happy-path test"; no gate ever exercised a hostile caller. Generic — any plugin host benefits.

- **A4 — `reference\08-native-interop.md`, broaden Check 2 from "Hot-Path Allocation" to "Hot-Path Cost", plus `reference\03-project-structure.md` §6.**
  Extend the per-frame/per-tick question beyond heap allocation: *Does any per-frame or high-frequency-event path perform I/O, persist state, rebuild derived structures wholesale, or do work inside a held lock? State changes arriving at high frequency (e.g. continuous UI input) must be coalesced (debounce / dirty-flag / apply-on-commit), and any state persistence triggered from such a path must be atomic (write-then-rename) and must not run inside a frame/render lock.* Why: theme 3 — four findings closed by one debounce+atomic-save fix; the allocation-only wording of Check 2 let all four pass.

- **A5 — `PlanImplementation.md` Phase 5 / Session Closure Checklist (and `BugfixPlanning.md` closure): documentation-truthfulness sweep.**
  At session close, for every user-facing documentation claim inside the session's scope that promises *behavior* (guards, no-throw contracts, asserts, disposal safety, defaults), verify it against the shipped code or a test; fix the doc or the code before closure. Claims that promise protective behavior must trace to a gate or test, not prose. Why: theme 4 sub-class 2 — the doc fixes that matter are the ones consumers build against (including one that directly contradicted severe finding S2).

- **A6 — `reference\08-native-interop.md`, new Check 5 "Boundary-mirrored values", plus a `CHUNK_N_CONTRACT.md` field.**
  > *List every constant, enum ordinal, identifier, version number, or data layout that is defined on both sides of a boundary and must agree. Each must have a mechanical agreement check (a pin test, a compile-time assertion, or generation from a single source) or be recorded here as an accepted risk with rationale.*
  Why: theme 5 — flagged as nice-to-have in the 2026-09-03 review, never rule-ified, and it recurred in four independent places in this review.

- **A7 — `reference\07-frozen-gates.md` verdict taxonomy / audit templates: accepted-latent-risk record format.**
  When an audit or review classifies a finding as "real mechanism, unreachable today", the record must state: the mechanism, the condition that makes it unreachable, the change that would activate it, and where the record lives. Why: theme 6 — prevents re-litigation of the same latent findings in every subsequent review; cheap to add.

- **A8 — `CORE_PROTOCOLS.md` §5.5 principles: example code is production code.**
  Shipped samples, templates, and documentation-recommended values are held to the same gates and review rigor as the library itself, because consumers copy them verbatim. Why: theme 7 — demo bugs and a doc-recommended constant amplified into consumer code.

- **A9 — (modest, optional) `PlanImplementation.md` gates guidance: release-artifact contents gate.**
  When a milestone ships a distributable artifact, gates must cover the artifact's *contents*: no user-state or machine-local files, required license/readme files present, metadata (version ranges, URLs) accurate, and archive-creation errors fatal rather than silent. Why: G2-16, G3-37/42/44 — packaging defects invisible to code-level gates. Kept deliberately vague; the specific checks are project tooling.

---

## What the workflow could NOT catch (without becoming overly specific)

Recorded here honestly; each cluster's project-specific lesson was written to the project's `notes\knowledge\` folder instead.

1. **Domain-API semantics errors** — G2-13/14 (orbital elements already in degrees fed through degree conversion / trig), G2-15/G3-34/35 (staging math: multi-mode engines summed, locked tanks counted, upper-stage propellant omitted). These are "know the engine API's units and semantics" issues. No generic workflow question surfaces them; they belong to the project's external knowledge library and domain review. *Project knowledge note: `ksp-api-semantics-pitfalls.md`.*

2. **Runtime-only behaviors** — G2-U1/U2, G3-U1/U2/U3 and similar UNCERTAIN items hinge on host-application runtime behavior (scene-change UI reshow, config parser culture handling, zero-size screen). The workflow already handles these correctly by deferring to in-game/runtime gates; no static rule helps.

3. **The bulk of docs drift and stale comments** — theme 4 sub-class 1 (~25 small stale claims), plus stale log lines and code comments (G3-06/11/15/31/32/47). A5 reduces the harmful subset; the long tail is inherent to AI-assisted development (text written at design time decays as code evolves). No plausible generic rule prevents it; periodic Housekeeping/UXClarity passes are the mitigation that already exists.

4. **Deliberate tradeoffs and NOTE-class items** — by definition not preventable and mostly correctly recorded already. The improvement is A7's record format, not prevention.

5. **Toolchain-environment scripting quirks** — G3-02 (hard-coded compiler-environment path), G3-44 (archive cmdlet's non-terminating errors exit 0). These are specific to one machine's build tooling; a generic "make build scripts robust" rule would be too vague to bite. Partially covered by A9's "archive errors fatal" line; the rest is project knowledge (`release-packaging-pitfalls.md`).

6. **Engine time-source semantics** — G2-06/G3-40 (scaled vs unscaled time driving UI timing differently under pause/warp). "Which clock does your per-frame code use?" is arguably a hot-path question, but the *answer* is entirely engine-specific; a generic prompt would not have caught the wrong choice. Recorded in the project knowledge notes.

7. **Review-verifier false positives** — G2-X1/X2, G3-X1, G4 INVALIDs. External AI review itself produced confidently wrong claims that triage disproved. This cuts the other way: it validates the workflow's existing verify-before-work discipline rather than exposing a gap.

---

## Bottom line

Of seven cross-cutting themes, five (1, 2, 3, 5, 7) trace to gaps closable with genuinely generic rules — the largest being the missing **external-callback containment inventory** (A2/A3), which accounts for all three severe findings. One (4) is half-addressable. One (6) is a record-format improvement, not prevention. The proposed amendments are nine small, generic additions — four of them localized to `reference\08-native-interop.md` and the chunk-contract template, which is where the 2026-09-03 review loop already proved this mechanism works.
