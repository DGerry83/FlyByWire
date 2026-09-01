# Planning Workflow: The 8-Step Procedure

Execute these steps in order. Do not skip steps. Do not write code. The output of each step feeds into the next.

---

## Step 1: Identify Core Entities and State

**Prompt**: "What are the main nouns in this application, and what data describes them?"

- List all primary entities (e.g., Player, Inventory, Map, Document, Node, Config).
- For each entity, define:
  - **Identity**: Unique identifier (ID, name, path, UUID).
  - **Attributes**: All data fields with their types and purposes.
  - **Relationships**: Ownership, containment, or reference links to other entities.
- Classify each entity as **persistent** (saved between sessions) or **transient** (computed at runtime).
- Define any enumeration types or value objects (types defined by their data alone, no identity).

**Deliverable**: A state model — plain data structures with fields. No logic, no methods.

---

## Step 2: Identify Behaviors and Responsibilities

**Prompt**: "What does the application DO? What actions transform the state?"

- List all primary operations (e.g., Move, Parse, Render, Save, Validate, Transform).
- Group related operations into logical units. Name each unit with a single-responsibility noun.
- Apply SRP: If a unit's description requires "and" or "or," split it.
- Identify which operations are **commands** (mutate state), **queries** (read state), or **both**.

**Deliverable**: A responsibility list — each behavior class/module with its one-sentence purpose.

---

## Step 3: Map Data Flow

**Prompt**: "Where does data enter, how does it move, and where does it exit?"

- **Sources**: User input, file reads, network, APIs, randomness, clock/time.
- **Processing chain**: Which components touch the data, in what order?
- **Sinks**: Screen rendering, file writes, network responses, logs.
- Draw directed arrows from source to sink. Label each arrow with the data type.
- Flag any arrow that splits to multiple destinations — determine if an event bus is warranted or if direct calls suffice.

**Deliverable**: A data flow diagram (text representation is acceptable).

---

## Step 4: Define Boundaries and Interfaces

**Prompt**: "What are the natural seams where one layer ends and another begins?"

- Identify the main layers: UI/Presentation, Domain Logic, Data Access, External Services.
- For every cross-boundary dependency, define an interface in the **lower** layer.
  - Example: If domain logic saves data, define `ISaveStore` in Core. The domain depends on `ISaveStore`. Infrastructure provides `FileSystemSaveStore : ISaveStore`.
- List each interface with:
  - Name and layer location
  - Methods and their signatures (conceptual, not language-specific)
  - Which concrete class implements it (in Infrastructure)
  - Which classes consume it (in Core or Application)

**Deliverable**: Interface inventory with producer/consumer mapping.

---

## Step 5: Select Patterns

**Prompt**: "What patterns naturally fit the problems identified?"

- Review `02-architecture-patterns.md`.
- Map each identified problem to a pattern. State the match explicitly.
- If no pattern fits a problem, state that it will use direct, simple code.
- **Do not apply a pattern just because it exists.** Apply it only if the "Use When" condition is satisfied.

**Deliverable**: Pattern selection table — problem → pattern → justification.

---

## Step 6: Design Project Layout

**Prompt**: "Where do the files go?"

- Create the folder structure following `03-project-structure.md`.
- Place every entity (Step 1), behavior (Step 2), and interface (Step 4) into a specific folder.
- Verify dependency direction: Core must not reference Application or Infrastructure.
- Name each file. Use the single-responsibility name from Step 2 as the filename.

**Deliverable**: A complete file tree showing every planned source file in its correct folder.

---

## Step 7: Assess Dependencies and Risks

**Prompt**: "What does this depend on externally? What could fail?"

- List all external libraries, frameworks, file formats, and APIs with versions.
- For each integration point, define the error handling strategy:
  - What happens on failure? (fail fast / retry / degrade / ignore)
  - How is the user or calling code informed? (exception / Result<T,E> / return code / event)
- Define the logging approach: none, console, structured log file.
- Identify any platform-specific code or assumptions.

**Deliverable**: Dependency matrix + error handling strategy + logging plan.

---

## Step 8: Define Verification Checkpoints

**Prompt**: "How do I verify each part works before the whole is complete?"

- Define development milestones in dependency order. Earlier milestones have fewer dependencies.
- For each milestone, specify:
  - **What is implemented**: Specific components.
  - **What is verified**: A concrete, observable outcome (e.g., "Loading a test file produces the expected state model").
  - **How it is verified**: Manual test, unit test, or integration test.
- The first milestone should produce a "hello world" level output to confirm the build pipeline works.

**Deliverable**: Sequenced milestone list with verification criteria for each.

---

## Anti-Patterns Reference

If you observe any of these in your plan, redesign the affected component.

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| **God Class** | One class has >5 responsibilities or >300 lines (conceptually) | Split by responsibility; compose |
| **Spaghetti Code** | Cyclic imports; modules A→B→C→A | Enforce layers; introduce interfaces |
| **Golden Hammer** | Same pattern applied everywhere regardless of fit | Match pattern to problem size |
| **Premature Optimization** | Abstractions with no second consumer; complex caches for trivial data | Write clear code; profile before optimizing |
| **Magic Numbers/Strings** | Unexplained literals in logic | Named constants |
| **Callback Hell** | Deeply nested event handlers or callbacks | Sequential pipeline or async/await pattern |
| **Global Mutable State** | Static fields modified from multiple locations | Pass state explicitly; use immutable state snapshots |
| **Leaky Abstraction** | Consumer code checks implementation type (`if (impl is ConcreteType)`) | Redesign interface to be self-contained |
| **Anemic Domain Model** | Entities are pure data bags with all logic in external "service" classes | Move behavior onto the entities that own the data |
| **Feature Envy** | A function primarily operates on data from another module | Move the function to the module whose data it uses |
