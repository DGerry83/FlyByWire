# Frozen Gates: [Target File(s)]
## Date Frozen: [Current Date]
## Session: [SessionFolder]
## Frozen By: [Agent / User]

| Gate ID | Criterion | Evidence Required | Verdict |
|---------|-----------|-------------------|---------|
| G1 | Build passes with 0 errors before any code moves | Clean build log | [PASS / FAIL / INVALID] |
| G2 | Every public export has an identical post-refactor signature or a facade at its original location | Export comparison table | [PASS / FAIL / INVALID] |
| G3 | No circular imports introduced by the new module structure | Import graph check | [PASS / FAIL / INVALID] |
| G4 | Functional parity verified on core user flows | Runtime/integration test log | [PASS / FAIL / INVALID] |

**Session Verdict**: [KILL / CONTINUE]
