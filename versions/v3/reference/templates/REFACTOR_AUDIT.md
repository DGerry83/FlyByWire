# Refactoring Audit: [Target File(s)]
## Date: [Current Date]
## Design Reference: [Link to REFACTOR_DESIGN.md]
## Gates Reference: [Link to GATES.md]

### Frozen Gates Audit
| Gate ID | Criterion | Evidence | Verdict |
|---------|-----------|----------|---------|
| G1 | [Criterion text from GATES.md] | [Build log excerpt] | [PASS / FAIL / INVALID] |
| G2 | ... | ... | ... |

**Session Verdict**: [KILL / CONTINUE]
**If KILL**: [Specific reason and recommended next step]

### Build Verification
- [ ] Production build successful (0 errors, 0 new warnings)
- [ ] Runtime starts without errors
- [ ] New files included in build

### API Stability Verification (Critical)
**Pre-Refactor Exports**: [Count] items
**Post-Refactor Exports**: [Count] items

Export Comparison:
| Item | Pre-Location | Post-Location | Status |
|--------------------|--------------|-----------------|--------|
| `GameUI` | Original.ts | Original.ts (facade) | Verified |
| `MenuScreen` | Original.ts | MenuScreen.ts (new) | Verified |
| [Internal helper] | Original.ts | shared/helpers.ts | N/A |

**API Check Result**: [PASS / FAIL]
**Integration Test**: [PASS / FAIL / Skipped]

### Structural Integrity
- [ ] No circular imports detected
- [ ] All new files have appropriate imports
- [ ] Project import conventions followed
- [ ] No files >300 lines (target metric achieved)
- [ ] Separation of concerns improved (logic separated from rendering, etc.)

### State Management Verification
| State Variable | Migration Verified | Parent/Store Integration Preserved |
|----------------|-------------------|-----------------------------------|
| `menuOpen` | [Yes/No] | [Yes/No] |
| `selectedCell` | [Yes/No] | [Yes/No] |

### Functional Parity
- [ ] Manual integration test successful
- [ ] All core functionality accessible and functional
- [ ] No errors during operation
- [ ] Performance within 5% of pre-refactor (measure if critical path affected)

### Violations Found
- [List any API changes, build warnings, circular imports, etc. with searchable context]

### Recommendations
- [Clear to proceed / Fix required: [specific issues]]
- [Future improvements: e.g., "Consider extracting BoardOverlay further into sub-modules"]
