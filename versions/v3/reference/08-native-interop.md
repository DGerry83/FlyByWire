# Native Interop & Hot-Path Checklist

Conditional-load reference for any chunk, design, or audit that touches **P/Invoke or native library loading**, or code that runs **once per frame/tick**. Loaded only when `CORE_PROTOCOLS.md` §5.9 or a chunk contract points here — it is not part of the default routing context.

Each check is a question that must be answered in the chunk contract or audit notes. "Not applicable" with a one-line reason is a valid answer; silence is not.

## Check 1 — Process-Global State

> Does this call change anything outside the module's own memory — DLL search path, environment variables, current working directory, global OS hooks or handles, registry entries?

Native interop calls (`SetDllDirectory`, `SetEnvironmentVariable`, `SetCurrentDirectory`, `SetWindowsHookEx`, and equivalents on other platforms) mutate **process-wide or OS-wide state** that does not appear as a code smell in a diff. In a shared-process host (game mods, plugins, in-process extensions), other components may depend on that state staying put.

If the answer is yes, exactly one of these must hold:

- **Scoped and restored** (preferred): the state is captured before mutation and restored as soon as the dependent operation completes (e.g. `SetDllDirectory(path)` → `LoadLibrary` → `SetDllDirectory(null)`). Where the API offers a scoped alternative (`AddDllDirectory` / `LoadLibraryEx` with `LOAD_LIBRARY_SEARCH_*` instead of `SetDllDirectory`), use it instead of the global mutation.
- **Documented as permanent-for-session**: the side effect is intentional, recorded in the design spec's failure-modes or constraints section, and the reason it cannot harm co-hosted components is stated.

## Check 2 — Hot-Path Allocation

> Is this method invoked once per frame/tick/update? If yes, trace every line for heap allocation: `new` collections, boxing, string concatenation or interpolation, closures capturing locals, LINQ, enumerator allocations.

Per-frame allocation is steady-state GC pressure; on generational or conservative collectors (e.g. Unity's Mono) it surfaces as periodic frame hitches, and it is invisible to cadence-focused review questions ("what's the FPS target?") because nothing is *slow* — the garbage collector fires later, elsewhere.

If the answer is yes, either:

- Allocation per call is **zero** — reuse cached buffers, iterate sources directly instead of materializing lists, or pre-compute on state change rather than per frame; or
- The allocation is **explicitly justified** in the design spec or chunk contract (why it cannot be hoisted, and measured cost).

## Check 3 — Resource-Acquisition Symmetry

> For every native handle, `IDisposable`, engine object, or subscription acquired during a multi-step initialization: name the release point on **every** exit path — including each early-return-on-failure, not just the success path and the top-level failure path.

The classic failure shape: `Initialize()` acquires A, then B, then C; step 3 fails; the top-level handler releases C's prerequisites but A — acquired two steps earlier — is orphaned for the session. Nothing in feature-level edge-case analysis ("what happens when input is missing?") prompts this trace.

For each acquired resource, the contract or audit must show:

- the release call on the success-teardown path (shutdown/dispose), and
- the release call on every partial-failure return between its acquisition and init completion.
