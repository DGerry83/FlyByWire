# Chunk Contract: [Chunk Name]
## Plan: [Plan Name]
## Date: [Current Date]
## Chunk ID: C[N]
## Advances Milestone: [M#]

### Scope
- [Specific changes from the plan]

### Inputs (must exist before starting)
- [Files/records/contracts from prior chunks]
- [Milestone prerequisites verified]

### Outputs (must be created/changed)
- [Files/records changed]
- [New functions/properties/globals]

### Constraints
- [Project invariants applicable to this chunk]
- [If the chunk touches P/Invoke, native library loading, or per-frame code: state that the `reference/08-native-interop.md` checklist applies and record its three verdicts — process-global state, hot-path allocation, resource-acquisition symmetry. Otherwise omit this bullet.]

### Verification
- [How to verify the chunk independently]
- [Compile commands, runtime tests, inspections]
- [How this verifies the milestone it advances]

### Rollback
- [Which files to revert if the chunk fails]
