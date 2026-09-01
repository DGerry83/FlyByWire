# Chunk Map: [Plan Name]
## Date: [Current Date]
## Digest Reference: [Link to PLAN_DIGEST.md]

### Chunk List
| ID | Name | Type | Files/Records | Est. Complexity | Milestone | Status |
|----|------|------|---------------|-----------------|-----------|--------|
| C1 | SAKR Helper & Globals | Foundation | F4B_SAKRHelper.psc, F4B_Library.psc, FO4_Basics.esp | Med | M1 | Pending |
| C2 | Container Trading | Consumer | F4B_container.psc | Low | M2 | Pending |
| C3 | Morphing State Machine | Vertical slice | F4B_MorphingQuestScript.psc | High | M2 | Pending |

### Dependency Graph
```
C1 ──► C2 ──► C5
 │    │
 ▼    ▼
C3 ──► C6
 │
 ▼
C4
```
- Arrow means "must be completed before" (hard dependency).
- Dashed lines for soft dependencies / stubs acceptable.

### Interface Contracts Between Chunks
| From | To | Contract | Rationale |
|------|----|----------|-----------|
| C1 | C2/C3/C5 | `F4B:F4B_SAKRHelper` quest with `is_exposed()`, `get_skimpy_rating()`, etc. | Single source of truth for SAKR |
| C1 | C4/C7 | Globals `F4B_PlayerIsExposed`, `F4B_PlayerFullyExposed`, `F4B_PlayerSkimpyRating` | Perk conditions cannot call Papyrus |

### Milestone Mapping
| Milestone | Chunks Advancing It | Verification Gate |
|-----------|---------------------|-------------------|
| M1 | [C1, ...] | [Build passes, helper functions resolve] |
| M2 | [C2, C3, ...] | [Container trading reacts to exposure] |

### Cross-Cutting Concerns
- [e.g., "All chunks must preserve legacy fallback when SAKR is absent"]

### Chunking Decisions & Rationale
- [Why C3 is a vertical slice rather than split by script/MCM]
- [Why C5 and C6 are separate]
