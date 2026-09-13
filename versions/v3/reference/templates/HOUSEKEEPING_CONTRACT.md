# Housekeeping Contract: [Scope Description]
## Date: [Current Date]
## Discovery Reference: [Link to DISCOVERY_LOG.md]

### Frozen Gates (must be green before Phase 2)
- [ ] All tests pass / build green
- [ ] No behavior changes intended
- [ ] Scope approved and signed off
- [ ] Public interfaces and state fields locked
- [ ] Workspace committed/backed up

### Approved Housekeeping Targets

#### Phase 1a: Comment & Logging Cleanup (Risk: Low)
| Target | Action | Verification Method |
|--------|--------|---------------------|
| [File comments] | Remove redundant "what" comments, preserve "why" | Code review diff |
| [Debug logs] | Remove spam logs per list | Log output comparison |

#### Phase 1b: Magic Numbers (Risk: Low)
| Target | Action | Verification |
|--------|--------|------------|
| [engine.ts literals] | Extract to named constants in constants file | Compile check |
| [File.ext sizing] | Name and centralize | No public interface impact |

#### Phase 1c: UI String Centralization (Risk: Low)
**Source File**: [Path to central constants]

| Source Location | String Value | Constant Name | Context |
|-----------------|--------------|---------------|---------|
| [src/ui/MenuScreen.ts:45] | "TEST CIRCUIT" | TestCircuitLabel | Test button |

**Rationale**: Centralize for easy text editing without navigating implementation code.

#### Phase 1d: Pattern Consolidation (Risk: Low)
**Source**: [Files with repeated patterns]

| Source Location | Repeated Code | Extracted Pattern | Description |
|-----------------|---------------|-------------------|-------------|
| [File.ext:30] | Repeated bounds check | ClampValue helper | Value clamping |

**Rationale**: Centralize for consistent behavior and easier changes.

### Structural Recommendations (For Feature Workflow)
**These items are identified but NOT executed in housekeeping. Review and implement via Feature Implementation Workflow if desired.**

| Item | File/Method | Concern | Proposed Change | Effort | Risk |
|------|-------------|---------|----------------|--------|------|
| [MenuScreen.ts] | 400 lines, mixed concerns | Split into screen modules | High | Medium |

### Migration/Compatibility
- **String Constants**: Named exports from constants file - no API changes
- **Pattern Helpers**: Helper functions - no runtime behavior change
- **Magic Numbers**: Named constants where possible - compile-time safety

### Sub-Agent Scopes
- **Agent A**: Comment and logging cleanup (Phase 1a)
- **Agent B**: Magic number consolidation (Phase 1b)
- **Agent C**: UI string centralization (Phase 1c)
- **Agent D**: Pattern consolidation (Phase 1d)
- **Agent E**: Document structural recommendations (Phase 1e) - create summary for user review

**Note**: All housekeeping phases may run in parallel (max 3 agents) as they touch different aspects. Structural recommendations are documentation-only.
