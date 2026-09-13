# Final Audit: [Plan Name]
## Date: [Current Date]
## Gates Reference: [Link to GATES.md]

### Frozen Gates Audit
| Gate ID | Criterion | Evidence | Verdict |
|---------|-----------|----------|---------|
| G1 | [Criterion text from GATES.md] | [Artifact / log excerpt] | [PASS / FAIL / INVALID] |
| G2 | ... | ... | ... |

**Session Verdict**: [KILL / CONTINUE]
**If KILL**: [Specific reason and recommended next step]

### Plan Coverage Check
| Plan Section | Implemented By | Verified | Notes |
|--------------|----------------|----------|-------|
| [3. Helper service] | C1 | Yes | ... |
| [6. Rate limiter] | C3 | Yes | ... |

### Invariant Check Results
- [ ] Public interfaces preserved
- [ ] Shared state shape stable
- [ ] Language/runtime compliance
- [ ] Minimal change principle followed

### Testing Checklist Status
| Category | Tests Passed | Tests Failed | Skipped |
|----------|--------------|--------------|---------|
| Sync plumbing | [X] | [Y] | [Z] |
| Sync state checks | ... | ... | ... |

### Deviations from Plan
- [Any intentional deviations and rationale]

### Known Limitations / Follow-Up Work
- [e.g., "Offline fallback behavior not fully tested"]

### Recommendation
[Clear to proceed / Needs fixes: list]
