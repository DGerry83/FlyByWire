# Integration Contract: [Plan Name]
## Date: [Current Date]
## Chunk Map Reference: [Link to CHUNK_MAP.md]

### Execution Order
| Order | Chunk ID | Name | Why This Position | Parallel Group |
|-------|----------|------|-------------------|----------------|
| 1 | C1 | SAKR Helper & Globals | All other chunks consume it | - |
| 2 | C2 | Container Trading | Safe consumer, validates helper | A |
| 3 | ... | ... | ... | ... |

**Parallel Group**: Chunks in the same group have no hard dependencies on each other and may be delegated in parallel. Chunks in different groups or marked "-" must run sequentially.

### Stub / Scaffolding List
| Stub | Location | Replaced By | Remove In |
|------|----------|-------------|-----------|
| `F4B_SAKRHelper` empty quest record | FO4_Basics.esp | Full C1 implementation | C1 |
| Placeholder global values | FO4_Basics.esp | Live updates from helper | C1 |

### Inter-Chunk Contracts (Locked)
| Contract Element | Definition | Owner | Consumers |
|-------------------|------------|-------|-----------|
| `is_player_exposed()` | Returns `bool`; true if any private part uncovered | C1 (F4B_Library) | C2, C3, C5 |
| `F4B_PlayerIsExposed` global | `1` when exposed, updated by helper event | C1 | C4 (perk conditions) |

### Build/Test Sequence
| After Chunk | Verification |
|-------------|--------------|
| C1 | Helper compiles; game loads without SAKR errors |
| C2 | Trading restrictions react to SAKR exposure |
| ... | ... |

### Rollback Plan
- If a chunk fails verification, revert only that chunk's files.
- If reverting breaks downstream stubs, restore stubs and re-implement from that point.
- Keep a git checkpoint before each chunk.
