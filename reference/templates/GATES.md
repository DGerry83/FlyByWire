# Frozen Gates: [Plan Name]
## Date Frozen: [Current Date]
## Session: [SessionFolder]
## Frozen By: [Agent / User]

| Gate ID | Criterion | Evidence Required | Verdict |
|---------|-----------|-------------------|---------|
| G1 | Plan digest and chunk map reflect the actual plan file | PLAN_DIGEST.md and CHUNK_MAP.md reviewed | [PASS / FAIL / INVALID] |
| G2 | All chunk contracts define verifiable inputs, outputs, and rollback | CHUNK_*_CONTRACT.md files reviewed | [PASS / FAIL / INVALID] |
| G3 | Each implemented chunk compiles/builds with 0 errors | Build log per chunk | [PASS / FAIL / INVALID] |
| G4 | Integration build passes after stubs removed and wiring connected | Full build log | [PASS / FAIL / INVALID] |
| G5 | Plan coverage check confirms every plan section is implemented or explicitly deferred | FINAL_AUDIT.md coverage table | [PASS / FAIL / INVALID] |

**Session Verdict**: [KILL / CONTINUE]
