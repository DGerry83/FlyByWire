# Output Format Template

Your final deliverable must be a single implementation plan document following this exact structure. Populate every section. If a section is not applicable, write "Not applicable" followed by a one-sentence explanation.

Use clear, precise language. Name every component, interface, file, and responsibility explicitly. Do not write pseudocode or source code. Do not leave sections vague.

---

## 1. Overview

### 1.1 Project Name
[Short descriptive name]

### 1.2 Description
[2-3 sentence description of what the application does and its primary purpose]

### 1.3 Target Platform & Runtime
- OS: [e.g., Windows 10+, cross-platform]
- Runtime: [e.g., .NET 8, Python 3.11, Node.js 20, Unity 2022]
- Distribution: [e.g., standalone executable, command-line tool, mod DLL, browser extension]

### 1.4 Language & Dependencies
- Primary language: [e.g., C#, Python, TypeScript]
- Core framework/engine: [e.g., none, Unity, PyQt 6, .NET MAUI]
- External libraries: [List with versions and purpose]
- Forbidden/restricted technologies: [If any]

### 1.5 Scope
- **In scope**: [Bullet list of features and capabilities]
- **Out of scope**: [Bullet list of explicitly excluded features]
- **MVP**: [Minimum subset that constitutes a working deliverable]
- **Deferred**: [Features planned for future iterations]

---

## 2. State Model (Step 1 Output)

List every entity in the application. For each entity, provide:

```
### Entity: [Name]
- Identity: [what uniquely identifies it]
- Lifetime: [persistent / transient]
- Attributes:
  - [field name]: [type/purpose]
  - [field name]: [type/purpose]
- Relationships:
  - [owns / references / contained-by] → [Other Entity]
```

List value objects and enumerations separately:

```
### Value Object / Enum: [Name]
- [description and fields/values]
```

---

## 3. Component Responsibilities (Step 2 Output)

List every behavior component. For each:

```
### Component: [Name]
- Responsibility: [single-sentence description]
- Layer: [Core / Application / Infrastructure]
- Type: [Service / System / Controller / Repository / etc.]
- Collaborators: [list of other components this one interacts with]
- State access: [read / write / none — which entities it touches]
```

---

## 4. Data Flow Diagram (Step 3 Output)

Describe the flow of data through the system. Use a text-based directed graph format:

```
[Source] --(data type)--> [Component A] --(data type)--> [Component B] --(data type)--> [Sink]
                                    |
                                    +--(data type)--> [Component C] --(data type)--> [Sink 2]
```

Include all major flows. Label each arrow with the data being passed.

---

## 5. Interface Definitions (Step 4 Output)

List every cross-boundary interface. For each:

```
### Interface: [IInterfaceName]
- Defined in layer: [Core / Application]
- Implemented by: [ConcreteClass] (Infrastructure)
- Consumed by: [Component1], [Component2] (list all consumers)
- Methods:
  - [MethodName]([parameters]) -> [return type / output]: [purpose]
```

---

## 6. Pattern Selection (Step 5 Output)

Table of every architectural decision:

| Problem / Concern | Selected Pattern | Justification |
|---|---|---|
| [e.g., Game objects have mixable behaviors] | Component-Based | Entities need different behavior combinations at runtime |
| [e.g., Menu → Gameplay → Pause modes] | State Machine | Distinct modes with different update/render logic |
| [e.g., Save/load player progress] | Repository | Need swappable persistence for testing |
| [e.g., Simple config reading] | None (direct) | Single consumer, no extension needed |

---

## 7. Project Structure (Step 6 Output)

Complete file tree. Every planned source file must appear here.

```
src/
  Core/
    [FeatureName]/
      [FileName].cs
      ...
  Application/
    [FeatureName]/
      [FileName].cs
      ...
  Infrastructure/
    [FeatureName]/
      [FileName].cs
      ...
tests/
  Core.Tests/
    ...
assets/
  ...
```

After the tree, add a table mapping each file to its Step 2 component or Step 1 entity:

| File Path | Contains | Responsibility |
|---|---|---|
| `src/Core/Player/Player.cs` | Entity | Player state model |
| `src/Core/Player/PlayerMovement.cs` | Component | Movement logic and physics queries |

---

## 8. Dependencies & Error Handling (Step 7 Output)

### External Dependencies
| Library / API | Version | Purpose | Risk Level |
|---|---|---|---|
| [e.g., Newtonsoft.Json] | [13.0.3] | [JSON serialization] | [Low / Med / High] |

### Error Handling Strategy
| Failure Scenario | Detection | Response | User Notification |
|---|---|---|---|
| [e.g., Save file corrupted] | [Invalid JSON parse] | [Delete corrupt file, start fresh] | [Log warning, silent] |
| [e.g., Asset file missing] | [File.Exists check] | [Fail fast with message] | [Show error dialog] |

### Logging
- Target: [none / console / file / both]
- Level: [error / warning / info / debug]
- Format: [structured JSON / plain text]

---

## 9. Milestones (Step 8 Output)

| # | Milestone | Components Implemented | Verification Method | Success Criteria |
|---|---|---|---|---|
| 1 | [e.g., Project skeleton builds] | Entry point, DI wiring, empty interfaces | Compile and run | Prints version string to console |
| 2 | [e.g., Core state model loads] | Entities, repository, file loader | Unit test | Loading a test file produces correct state |
| ... | ... | ... | ... | ... |

Dependencies between milestones must be acyclic. Milestone N must only depend on milestones < N.

---

## 10. Open Questions / Assumptions

List any assumptions made due to remaining ambiguity, and any follow-up questions for the user:

- [Assumption: The user will provide test data files in format X]
- [Question: Should the application support drag-and-drop file input, or command-line only?]

---

## Plan Checklist (Agent Self-Verification)

Before delivering, verify:
- [ ] Every entity in Section 2 has a clear identity and lifetime classification
- [ ] Every component in Section 3 has a single-responsibility description without "and" / "or"
- [ ] Every cross-boundary dependency in Section 5 has an interface in Core or Application
- [ ] Dependency direction (Core ← Application ← Infrastructure) is never violated in Section 7
- [ ] Every pattern in Section 6 has a stated justification matching its "Use When" condition
- [ ] Every milestone in Section 9 has an observable, testable success criterion
- [ ] No God Classes, no global mutable state, no deep inheritance trees
- [ ] The MVP in Section 1.5 is achievable with Milestones 1 through [N] only
