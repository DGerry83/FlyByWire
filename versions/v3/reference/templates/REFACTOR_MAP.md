# Refactoring Map: [Target File(s)]
## Date: [Current Date]
## Target: [Filename(s) to decompose]

### Current State Analysis
- **Lines of Code**: [Count]
- **Responsibilities Identified**: [List: menu rendering, domain logic, etc.]
- **Exported Items**: [List of exported components/functions]
- **Local State**: [Variables that persist across calls/updates]

### Dependency Graph

#### External Dependencies (What Target Needs)
| Dependency | Type | Used For | Notes |
|------------|------|----------|-------|
| [state module] | internal | State management | Shape must remain stable |
| [utility lib] | internal | Helpers | Safe to split |

#### Dependents (What Needs Target)
| Consumer | Usage | Impact of Split |
|----------|-------|-----------------|
| [Main.ts] | Imports [Target] | Must update import path if file moves |
| [Other.ts] | None | N/A |

#### Internal Call Graph (Simplified)
```
[Main Module] → [renderMenu()] → [MenuButton helper]
             ↘ [renderBoard()] → [Board sub-module]
```

### Extraction Candidates (Seams)

#### Candidate 1: [Name/Responsibility]
- **Components/Functions**: [List to move]
- **Helpers**: [Helpers moving]
- **State Dependencies**: [Local state required]
- **Coupling to Remainder**: [Low/Med/High - specific dependencies]
- **API Impact**: [None/Internal only/Exports affected]
- **Risk Level**: [Low/Med/High]
- **Recommended**: [Yes/No - with rationale]

#### Candidate 2: [Name/Responsibility]
[Same structure]

### Risk Analysis Summary
| Risk Category | Severity | Mitigation Strategy |
|---------------|----------|---------------------|
| Interface Breakage | Critical | Keep exported items in main file as thin wrappers, move implementation to new files (safest) |
| Local State Split | High | Lift state to shared store or pass via parameters carefully |
| Circular Imports | Medium | Forward references avoided by state slices or parameter passing |
| Build Breakage | Low | Update imports immediately after file creation |

### Proposed Architecture (Visual)
```
Original: [Main.ts] ←→ [Consumer.ts]

Proposed: 
[Main.ts] ←→ [Consumer.ts] (thin facade, re-exports)
   ↓
[MenuModule.ts] (menu rendering)
[BoardModule.ts] (board + overlay)
[shared/] (common helpers)
```

**Note**: Facade pattern keeps import paths stable while allowing internals to move freely.
