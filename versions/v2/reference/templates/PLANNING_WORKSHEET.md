# Planning Worksheet: [Project Name]
## Date: [Current Date]
## Design Spec Reference: [Link to DESIGN_SPEC.md]

### Step 1 — Core Entities and State
| Entity | Identity | Attributes | Relationships | Lifetime |
|--------|----------|------------|---------------|----------|
| [Name] | [ID/Key] | [Field: type/purpose] | [owns/references] | [persistent/transient] |

### Step 2 — Behaviors and Responsibilities
| Component | Single-Sentence Responsibility | Command / Query / Both | Layer |
|-----------|-------------------------------|------------------------|-------|
| [Name] | [One sentence, no "and"/"or"] | [C/Q/Both] | [Core/Application/Infrastructure] |

### Step 3 — Data Flow
```
[Source] --(data type)--> [Component A] --(data type)--> [Component B] --(data type)--> [Sink]
```

### Step 4 — Boundaries and Interfaces
| Interface | Defined In | Implemented By | Consumed By | Purpose |
|-----------|------------|----------------|-------------|---------|
| [IName] | [Core/Application] | [ConcreteClass] | [Consumer] | [Why it exists] |

### Step 5 — Pattern Selection
| Problem / Concern | Selected Pattern | Justification |
|---|---|---|
| [Problem] | [Pattern] | [Why the "Use When" condition is met] |

### Step 6 — Project Layout
```
[File tree]
```

### Step 7 — Dependencies and Risks
| Dependency | Version | Purpose | Risk Level |
|---|---|---|---|
| [Name] | [Version] | [Purpose] | [Low/Med/High] |

### Step 8 — Verification Checkpoints (Sequential Milestones)

Milestones are **sequential gates**. Do not start milestone *N* until milestone *N-1* has passed verification. Each milestone should be small enough to verify in isolation and should map to one or more chunk groups in [`PlanImplementation.md`](.\PlanImplementation.md).

| # | Milestone | Components | Verification | Success Criteria | PlanImplementation Chunk Group |
|---|---|---|---|---|---|
| 1 | [Build pipeline works] | [Entry point, DI root] | [Compile/run] | [Prints version] | [G1] |
| 2 | [Core domain logic compiles] | [Entities, rules] | [Unit tests] | [Tests pass] | [G2] |
