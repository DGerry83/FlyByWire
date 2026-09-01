# Architecture Patterns for Local Applications

Select patterns based on the specific problems in the implementation ask. Do not apply a pattern unless the corresponding "Use When" condition is met. Default to direct, simple code when no pattern is called for.

## 1. Component-Based Architecture (Entity-Component)
- **Use When**: Objects in the system share behaviors flexibly. Common in games, simulations, and editors where entities have mixable capabilities.
- **Structure**: An Entity is a lightweight ID or container. Components are data or behavior attached to entities. Systems iterate over entities with specific component sets.
- **Benefits**: Flexible composition, no deep inheritance, runtime add/remove of behaviors.
- **Planning Question**: "What distinct data/behavior sets exist, and which entities need which sets?"

## 2. Plugin / Mod Architecture
- **Use When**: Third-party or runtime extensibility is required (game mods, tool plugins).
- **Structure**: Core defines a public API (interfaces and hook points). Host loads external assemblies/scripts at runtime and registers them.
- **Key Components**: Host API (interfaces + events), Plugin Loader (discovery + instantiation), optional Sandbox.
- **Planning Question**: "What extension points must the core expose, and what is the plugin lifecycle (load, enable, tick, disable, unload)?"

## 3. State Machine
- **Use When**: Objects or the application have distinct behavioral modes (game screens, AI behaviors, UI flow, connection states).
- **Structure**: States encapsulate entry, exit, and update logic. A context holds the current state and delegates. Transitions are explicit.
- **Planning Question**: "What are the distinct behavioral modes, and what events trigger transitions between them?"

## 4. Event Bus / Observer
- **Use When**: Multiple decoupled components react to the same occurrence, and the publisher does not know the subscribers.
- **Structure**: Central bus or per-object event registry. Publishers emit; subscribers register callbacks.
- **Warning**: Do NOT use for direct sequential logic that should be a function call. Overuse creates untraceable implicit control flow.
- **Planning Question**: "Is this communication truly one-to-many and decoupled, or is it actually one-to-one and should be a direct call?"

## 5. Command Pattern
- **Use When**: Operations need to be queued, undone, replayed, or logged (editors, game input recording, transaction systems).
- **Structure**: Each operation is an object with `execute()` and optionally `undo()`. Commands are stored in a history stack.
- **Benefits**: Undo/redo, action replay, deferred execution, macro recording.
- **Planning Question**: "What are the discrete actions, and do any need to be reversed or recorded?"

## 6. Repository / Data Access Pattern
- **Use When**: The application reads/writes persistent data (saves, configs, asset metadata, player data).
- **Structure**: A repository interface abstracts the data source. Domain logic calls repository methods. Concrete implementations handle files, databases, etc.
- **Benefits**: Swappable persistence, centralized data logic, easy in-memory substitution for testing.
- **Planning Question**: "What data entities persist, and what operations (load, save, query, delete) are needed?"

## 7. Pipeline / Chain of Responsibility
- **Use When**: Data or requests need sequential processing through multiple interchangeable stages (asset loading, data transformation, request middleware).
- **Structure**: A chain of processors. Each handles what it can and passes the remainder along.
- **Benefits**: Modular stages, reorderable processing, conditional application.
- **Planning Question**: "What are the processing stages, does order matter, and can stages be skipped?"

## 8. Model-View-* Patterns
- **MVC**: Model holds data. View renders. Controller handles input and mediates. Use when UI logic is complex and input handling needs dedicated mediation.
- **MVP**: Presenter intermediates; View is passive. Use when testability of UI logic is critical.
- **MVVM**: ViewModel exposes bindable properties. Use when the UI framework supports data binding.
- **Recommendation**: For small tools, MVP or MVVM provide the cleanest separation without ceremony.
- **Planning Question**: "How does input flow into the system, and how does state become visible? Is there a clear boundary between display and logic?"

## 9. Factory / Builder Patterns
- **Use When**: Object construction is complex, involves multiple steps, or the concrete type must be determined at runtime.
- **Structure**: A Factory method or Builder class encapsulates construction logic, hiding it from the consumer.
- **Warning**: Do not use for simple `new Object()` construction. YAGNI applies. Use only when construction has real complexity (multiple dependencies, validation, conditional sub-objects).
- **Planning Question**: "Is object construction complex enough to warrant a dedicated builder, or is a direct constructor sufficient?"

## 10. Singleton / Service Container (Use Sparingly)
- **Use When**: Exactly one instance of a resource must exist globally (e.g., a hardware device handle, a central configuration store).
- **Warning**: Global mutable singletons are an anti-pattern. Prefer constructor-injected single instances managed by a simple registry in the composition root.
- **Planning Question**: "Does this truly need global access, or can it be passed explicitly to the components that need it?"
