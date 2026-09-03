# Refactoring Design: [Target File(s)]
## Date: [Current Date]
## Map Reference: [Link to REFACTOR_MAP.md]

### Extraction Strategy
**Selected Strategy**: [Facade / Direct Move / Internal Split]
- **Rationale**: [Why this approach]
- **Import Stability**: [How we maintain existing import paths]

### File Organization

#### New Files
| File | Responsibility | Exports? | Depends On |
|------|---------------|----------|------------|
| [MenuModule.psc] | [Menu rendering] | Yes | [Original facade, store] |
| [BoardHUD.psc] | [Board + HUD] | Yes | [Original facade, store] |
| [Original.psc] | [Facade/thin re-exports] | Yes (unchanged) | [New modules] |

#### Import Structure
```
MenuModule.psc:
  - import from [types/constants file]
  - import from [state module]
  - Implementation
```

### Interface Contracts

#### Internal Module API (Module Boundaries)
```
// MenuModule exposes to Original:
function ShowMenu(int option)
// Additive only - no existing parameters changed
```

#### Public API Preservation (Critical)
| Exported Item | Location After Refactor | Verification Method |
|---------------|------------------------|---------------------|
| `GameUI` | Stays in Original.psc (wrapper) | Import check in Consumer.psc |
| `Board` | Stays in Board.psc | Direct import unaffected |

**Constraint**: No exported item interface changes. Parameter types, order, and optionality must be identical.

### State Migration
| State Variable | Current Location | New Location | Migration Strategy |
|----------------|------------------|--------------|--------------------|
| `menuOpen` | Original.psc local | Lifted to store | Add to state module |
| `selectedCell` | Original.psc local | BoardHUD.psc local | Move with module |

### Build System Changes
**Build Tool Updates**:
- New files must be registered in build configuration if required
- Verify compiler/import paths cover new files

### Migration Strategy (Incremental Steps)
1. **Step 1**: Create new file headers, move private helpers (no API change)
2. **Step 2**: Move module implementations to new files, Original becomes wrapper
3. **Step 3**: Verify build (0 errors)
4. **Step 4**: Verify runtime behaves identically

### Rollback Plan
- **Trigger**: Build breaks, runtime errors, regressions
- **Procedure**: Git revert to pre-refactor state (single commit per phase)
- **Data Safety**: No persistent data affected (in-memory state only)
