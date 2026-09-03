# Core Principles

Enforce these as hard constraints on every component in the implementation plan. If a component violates a principle, redesign it.

## 1. Single Responsibility Principle (SRP)
- **Rule**: Every module, class, or function has exactly one reason to change.
- **Test**: Describe the component's job in one sentence without using "and" or "or." If you cannot, split it.
- **Smell**: Names containing `Manager`, `Handler`, `Utils`, `Helper`, `Processor` (when overloaded), or `System` (when monolithic). Question every one.
- **Practice**: Name components after their single responsibility. `CollisionDetector` > `PhysicsManager`.

## 2. Don't Repeat Yourself (DRY)
- **Rule**: Every piece of knowledge or logic has a single, unambiguous representation in the system.
- **Application**: If the same logic or data structure appears in two places, extract it. If two types share fields, extract a common base.
- **Exception**: Two similar-looking pieces that change for *different reasons* should NOT be merged. Similarity by coincidence != shared knowledge.

## 3. Separation of Concerns (SoC)
- **Rule**: Distinct sections of code address distinct, non-overlapping concerns.
- **Mandatory Concern Boundaries**:
  - **Domain Logic**: Core rules, calculations, state transitions specific to the problem.
  - **Presentation/UI**: Rendering, formatting, display logic, input capture.
  - **Data Access**: File I/O, network, serialization, external API calls.
  - **Infrastructure**: Logging, configuration parsing, dependency wiring, platform abstractions.
- **Test**: You must be able to describe any layer without referencing another layer's implementation details.

## 4. Dependency Inversion
- **Rule**: Core logic depends on abstractions (interfaces, protocols, abstract classes), not concrete implementations.
- **Application**: For every external dependency (file system, renderer, input device, clock, random source, network), define an interface in the core layer. Concrete implementations live in infrastructure.
- **Benefit**: Testability with mocks, swappable implementations, plugin architectures.
- **Method**: Constructor injection. Do not use service locators or global singletons unless the user explicitly requires them.

## 5. Open/Closed Principle
- **Rule**: Components are open for extension, closed for modification.
- **Application**: New features are added by creating new files that plug into existing extension points — not by editing tested, working code.
- **Mechanisms**: Strategy pattern, component composition, event subscriptions, plugin loading.

## 6. Composition Over Inheritance
- **Rule**: Assemble behavior by composing objects, not inheriting from parent classes.
- **Application**: Model relationships as "has-a", not "is-a." An entity has a renderer, has physics, has AI — it is not a subclass of a renderer.
- **Limit**: Inheritance depth should not exceed 1 (base → concrete). Deeper hierarchies require justification.

## 7. Encapsulation & Information Hiding
- **Rule**: Internal state and implementation details are hidden. Only a well-defined public interface is exposed.
- **Application**: Default to the most restrictive access. Expose fields or methods only when another component has a legitimate, documented need.
- **Smell**: Frequent access to another object's internal fields, especially mutable ones.

## 8. Loose Coupling / High Cohesion
- **Coupling**: Degree of inter-module knowledge. Minimize. Interact through narrow, stable interfaces only.
- **Cohesion**: Degree of intra-module focus. Maximize. Everything inside a module works toward one purpose.
- **Test**: If changing module A requires changes in B, C, and D, coupling is too tight. If a module contains unrelated logic, cohesion is too low.

## 9. KISS / YAGNI
- **KISS**: The simplest solution that satisfies requirements is the correct solution.
- **YAGNI**: Do not build abstraction layers, configuration systems, or extensibility hooks "just in case."
- **Application**: For small tools and mods, a plain function call is better than an event system if there is only one caller. A plain data class is better than a factory if there is only one variant. Refactor when a second use case actually appears, not before.

## 10. Explicit Over Implicit
- **Rule**: Code clearly states what it does. No hidden mechanisms, magic values, global mutable state, or side effects.
- **Application**: Pass dependencies and state explicitly through constructors and parameters. Use named constants, not literals. Avoid mutable globals. "Global state" includes OS- and process-level state mutated through native interop calls — DLL search paths, environment variables, current working directory, global hooks — which never appear as mutable fields in a diff; see `08-native-interop.md` Check 1 when a change touches P/Invoke or native loading.
