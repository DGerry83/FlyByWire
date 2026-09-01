# Implementer Sub-Agent Prompt Skeleton

Shared scaffolding for implementer sub-agent delegation prompts. Used by `BugfixPlanning.md`, `PlanImplementation.md`, `Refactoring.md`, and `Housekeeping.md`.

**How to use this file:** When a workflow template says to insert a block, copy that block from this file into the delegation prompt **verbatim** and fill the `[PLACEHOLDERS]` as the workflow directs. Do not paraphrase, summarize, or reorder. This file is loaded only when composing a delegation prompt — it is not part of the base route.

---

## Block A — Onboarding (cache-first)

The cache-first environment procedure is defined in `..\CORE_PROTOCOLS.md` §4; this block is its delegation-prompt form.

```markdown
MANDATORY ONBOARDING - Complete before any implementation work:
1. **Read Project Context**:
   - Read the project onboarding docs (AGENTS.md, README.md) for build commands and project structure
   - Read this scope's contract file ([SCOPE_CONTRACT])
   - [EXTRA_CONTEXT_DOCS — one bullet per extra document; omit this line if none]
   - Read CORE_PROTOCOLS.md for shared rules (artifact placement, session naming, shell syntax, minimal change, parallel policy)

2. **Environment Setup (cache-first)**:
   - Read `notes\knowledge\ENVIRONMENT.md` (the environment cache); adopt its shell, chaining operator, and quirks
   - Run the single verify probe: one trivial command chained with the cached operator (e.g., `ls && ls` in bash, `ls; ls` in PowerShell)
   - If the cache is missing, its project root does not match, or the probe fails: run full onboarding per CORE_PROTOCOLS.md §4.2 and rewrite the cache
   - Verify you can access your assigned scope directory
   - [EXTRA_ENVIRONMENT_CHECKS — one bullet per extra check; omit this line if none]

3. **Capability Check**:
   - Confirm you can read/write files in the workspace
   - Note any build tools you will need ([compiler, packager, etc.])

4. **Acknowledge**: Reply with "[ACKNOWLEDGMENT]"

Only after completing the above may you begin implementation.
```

Standard acknowledgment (use unless the workflow overrides):

`Onboarding complete. Shell: [cached shell and version]. Build tool: [X]. Ready to proceed with [SCOPE].`

---

## Block B — Mandatory Disagreement

```markdown
PHASE 0 — MANDATORY DISAGREEMENT:
Before writing or changing any code, compare the provided contract documents ([CONTRACT_DOCS]) against the actual project files.
1. Re-read the relevant files in your scope.
2. List every disagreement, contradiction, or ambiguity you find between the contract and reality. Cite real file paths, function names, and line-level evidence.
3. If you have no disagreements, explicitly state: "No disagreements found — contract matches files [list]." Silent compliance is a failure.
4. Submit your disagreement list to the parent agent and wait for a ruling: ACCEPT / REJECT / MODIFY for each item, plus one line explaining why. Do not proceed until ruled.
```

---

## Block C — Raw-Results Discipline and Final Status

Two variants. The workflow template names which one to insert.

### Variant C1 — Verification status (PlanImplementation, Refactoring)

```markdown
RAW-RESULTS DISCIPLINE:
- All progress reports, verification evidence, and status updates must contain raw data only: tables, numbers, file paths, command output, and diffs.
- Do not include interpretation, narrative, summary paragraphs, or conclusions in execution reports.
- End every status report with exactly one final line in this form:
  `STATUS: [PASS|FAIL|INVALID] — [single factual note]`
```

### Variant C2 — Completion status (BugfixPlanning)

```markdown
RAW-RESULTS DISCIPLINE:
- Report tables, numbers, and command output exactly. Do not interpret or summarize them.
- When you finish, end your response with exactly one of:
  - STATUS: COMPLETE
  - STATUS: COMPLETE_WITH_CONCERNS (list them)
  - STATUS: BLOCKED (exact blocker + what you tried)
```
