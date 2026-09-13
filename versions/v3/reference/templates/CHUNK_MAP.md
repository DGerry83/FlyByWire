# Chunk Map: [Plan Name]
## Date: [Current Date]
## Digest Reference: [Link to PLAN_DIGEST.md]

### Chunk List
| ID | Name | Type | Files/Records | Est. Complexity | Milestone | Status |
|----|------|------|---------------|-----------------|-----------|--------|
| C1 | Sync Helper & Shared Config | Foundation | src/sync/helper.ts, src/sync/config.ts, inventory_schema.json | Med | M1 | Pending |
| C2 | Container Trading | Consumer | src/sync/container.ts | Low | M2 | Pending |
| C3 | Morphing State Machine | Vertical slice | src/ui/morphing_state.ts | High | M2 | Pending |

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
| C1 | C2/C3/C5 | `SyncHelper` service with `is_synced()`, `get_sync_status()`, etc. | Single source of truth for sync state |
| C1 | C4/C7 | Shared constants `syncPending`, `syncFailed`, `lastSyncStatus` | Declarative conditions cannot call application code |

### Milestone Mapping
| Milestone | Chunks Advancing It | Verification Gate |
|-----------|---------------------|-------------------|
| M1 | [C1, ...] | [Build passes, helper functions resolve] |
| M2 | [C2, C3, ...] | [Container trading reacts to sync state] |

### Cross-Cutting Concerns
- [e.g., "All chunks must preserve legacy fallback when the sync service is absent"]

### Chunking Decisions & Rationale
- [Why C3 is a vertical slice rather than split by module/settings UI]
- [Why C5 and C6 are separate]
