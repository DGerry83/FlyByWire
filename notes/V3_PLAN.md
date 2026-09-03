# FlyByWire v3 Plan — Native Interop & Hot-Path Checklist

Date: 2026-09-03
Driver: external code review of DearImGui-KSP (a project run entirely under FlyByWire v2), followed by a meta-review of whether the workflow should have caught the findings. DearImGui-KSP review recorded at `DearImGui-KSP\notes\knowledge\EXTERNAL_REVIEW_2026-09-03.md`.

## What the meta-review concluded

**Genuine workflow gap (fix in v3):**

1. **Hot-path allocation** — DearImGui-KSP's `InputCaptureTracker.Update` allocated a `List<string>` every frame. `DESIGN_SPEC.md` §4.3 ("Update Cadence & Performance") covers *cadence* (timers, FPS targets, throttling) but nothing prompts the question "is this called per-frame, and if so, does it allocate?"
2. **Process-global side effects via native calls** — `NativeBridge.Initialize` set the process-wide DLL search path and never restored it. Core principle #10 ("Explicit Over Implicit", `reference\01-core-principles.md:56`) bans global mutable state, but it's written for C#/OOP smells (singletons, mutable statics); a Win32 call mutating OS-level process state doesn't *look* like that smell in a diff, and no template asks "does this P/Invoke have effects outside this module's own memory?"
3. **Resource-acquisition symmetry on partial failure** — `_deviceTexture` leaks if init fails after texture creation but before completion. `DESIGN_SPEC.md` §5.4 ("Edge Cases & Failure Modes") is populated at the feature level ("what happens when input is missing"), not the resource-lifecycle level ("init acquires A, then B, then C — if step 3 fails, what releases A?").

**Not a workflow gap (no template change, or minor reinforcement only):**

4. **Missing Shift/Alt modifiers** — a documentation-discipline miss. `DESIGN_SPEC.md` §3.2 "Out of Scope" already exists for exactly this; it just wasn't used. Execution miss, not template flaw — but the §3.2 prompt can be strengthened to make intentional partial coverage harder to skip (step 5 below).
5. **No automated tests** — an explicit, dated, deferred decision in `IMPLEMENTATION_PLAN.md`. The workflow working as intended. Test timing is a judgment call; no template should settle it.

## v3 changes

All work happens in a new `versions\v3\` folder, created as a full copy of `versions\v2\` (step 0). v2 stays untouched as the archive.

### Step 0 — Create the v3 folder

- Copy `versions\v2` → `versions\v3` (including `reference\` and `reference\templates\`).
- Update repo-root `README.md`: layout map and "point agents at" path now reference `versions\v3`; v2 becomes the archive entry.

### Step 1 — New reference doc: `reference\08-native-interop.md`

"Native Interop & Hot-Path Checklist" — a short, conditional-load reference in the style of `06`/`07`. Three checks, each phrased as a concrete prompt a reviewer/agent must answer:

1. **Process-global state.** Does this call change anything outside the module's own memory — DLL search path, environment variables, current working directory, global OS hooks/handles? If yes: is it scoped and restored (preferred), or explicitly documented as permanent-for-session?
2. **Hot-path allocation.** Is this method invoked once per frame/tick? If yes, trace every line for heap allocation (new collections, boxing, string concatenation, closures). The answer must be zero, or explicitly justified in the design spec.
3. **Resource-acquisition symmetry.** For every native handle / `IDisposable` / Unity object acquired in a multi-step init: name the release point on *every* exit path — each early-return-on-failure included, not just success and top-level failure.

### Step 2 — Wire it into `CORE_PROTOCOLS.md` §5

Add a short subsection (§5.9) to `versions\v3\CORE_PROTOCOLS.md` (§5 "Shared Definitions and Principles", line ~120): one paragraph stating that chunks touching P/Invoke, native library loading, or per-frame code must apply the checklist in `reference\08-native-interop.md`, linked the same way `07-frozen-gates.md` is linked from gated workflows. Do not inline the checklist — progressive loading stays intact.

### Step 3 — Extend core principle #10

In `versions\v3\reference\01-core-principles.md` §10 "Explicit Over Implicit" (line 56): add one sentence clarifying that "global mutable state / side effects" includes OS- and process-level state mutated through native interop calls (DLL search paths, environment variables, working directory), with a pointer to `08-native-interop.md`.

### Step 4 — `reference\templates\CHUNK_N_CONTRACT.md` Constraints section

Current text (line 18–19): `[Project invariants applicable to this chunk]` — only surfaces what the design spec already contains. Add a second bullet: if the chunk touches P/Invoke, native loading, or per-frame code, the contract must state that the `08-native-interop.md` checklist applies and record its verdicts.

### Step 5 — Strengthen `DESIGN_SPEC.md` §3.2 prompt (minor)

In `versions\v3\reference\templates\DESIGN_SPEC.md` §3.2 "Out of Scope": extend the prompt so intentional *partial* coverage of an in-scope feature (e.g. "Ctrl modifier fed, Shift/Alt not") must be listed as a known limitation, not just whole excluded features. This addresses finding #4 without pretending the template was missing.

### Step 6 — README updates

- `versions\v3\README.md`: add `08-native-interop.md` to the Planning Reference list, and add a v3 entry to the "Updating" section (in the style of the existing v2 entry, line ~114) describing the checklist addition and its origin in the DearImGui-KSP review.
- Repo-root `README.md`: layout + usage paths point at v3 (done in step 0).

## Explicit non-goals

- No template change for automated-testing timing (finding #5 — judgment call by design).
- No change to Router.md, SKILL.md, or any workflow's phase structure — this is an additive reference + two one-line template prompts.
- No retroactive edits to v2.

## Verification

- `diff -rq versions\v2 versions\v3` shows only the intended edits.
- Every new link target exists; `grep -rn "08-native-interop" versions\v3` shows the reference wired from `CORE_PROTOCOLS.md` §5.9, `01-core-principles.md` §10, `CHUNK_N_CONTRACT.md`, and `README.md`.
- Repo-root README points at v3; v2 folder untouched (`git status` clean under `versions\v2`).
