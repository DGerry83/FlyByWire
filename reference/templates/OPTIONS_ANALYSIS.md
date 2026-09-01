# Options Analysis: [Feature Name]

## Approach A: Conservative Extension
**Description**: Add new optional interfaces, preserve all existing APIs, extend data structures with new fields only

| Factor | Assessment |
|--------|------------|
| Implementation Effort | Low |
| Risk Level | Low |
| Compatibility | Preserved |
| Technical Debt | Accumulates |
| Future Extensibility | Constrained |

**Structural Implications**:
- [Specific fields would be added to shared structure]
- [Existing interfaces remain untouched]

**Files to Touch**: [List]

---

## Approach B: [Name]
[Repeat structure]

## Approach C: [Name]
[Repeat structure]

## Comparative Summary
| Approach | Effort | Risk | Compatibility | Power |
|----------|--------|------|---------------|-------|
| A | Low | Low | ✓ | Low |
| B | Med | Med | ⚠️ | Med |
| C | High | High | ✗ | High |

## Open Decision Points
- [List questions only the user can answer]

## Sources Consulted
- [Reference key precedents from RESEARCH_SYNTHESIS.md by citation]
