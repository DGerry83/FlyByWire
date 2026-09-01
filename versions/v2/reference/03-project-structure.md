# Project Structure & Organization

Use these rules to define the folder/file tree in the implementation plan. Enforce dependency direction strictly.

## 1. Layered Architecture

Organize by architectural layer. For small applications, three layers are sufficient:

```
src/
  Core/           # Domain logic, entities, state, rules. ZERO external dependencies.
  Application/    # Use cases, orchestration, service interfaces. Depends on Core only.
  Infrastructure/ # File I/O, rendering, external APIs, UI frameworks, DI wiring. Depends on Core + Application.
```

**Dependency Rules (enforced)**:
- `Core` imports nothing from `Application` or `Infrastructure`.
- `Application` imports from `Core` only.
- `Infrastructure` imports from `Core` and `Application`.
- Violating these rules creates circular dependencies and untestable code.

## 2. Feature-Based Organization

Within each layer, organize by **feature**, not by file type:

```
# Correct (by feature)
src/Core/Player/
  Player.cs
  PlayerState.cs
  PlayerMovement.cs

# Incorrect (by type)
src/Core/Entities/
  Player.cs
  Enemy.cs
src/Core/Systems/
  MovementSystem.cs
  CombatSystem.cs
```

**Rationale**: Features change together. Co-locating related files makes boundaries visible and reduces navigation overhead.

## 3. Shared / Common

Extract truly shared code into a `Shared/` folder, but keep it minimal and generic:

```
src/Shared/
  Result.cs         # Error-handling wrapper (e.g., Result<T, E>)
  Guard.cs          # Input validation helpers
  Extensions.cs     # Language-level extensions
```

**Rule**: If a utility is used by only one feature, it stays in that feature's folder. Do not centralize prematurely.

## 4. Entry Point & Composition Root

Every application needs a single entry point that wires all dependencies:

```
src/
  Program.cs          # or main.py, App.java — application bootstrap
  AppConfig.cs        # Configuration constants and environment detection
  Composition.cs      # Manual dependency injection: instantiates concrete implementations and wires them
```

**Rule**: `Composition.cs` (or equivalent) is the ONLY place where concrete infrastructure classes are instantiated. All other components receive their dependencies through constructors.

## 5. Asset & Resource Management

For applications with external assets:

```
assets/
  config/         # Runtime configuration files
  data/           # Static datasets, lookup tables
  templates/      # File templates, UI layouts
```

**Rules**:
- All file access goes through a single `IAssetLoader` or `IFileSystem` interface defined in Core, implemented in Infrastructure.
- Validate asset availability at load time, not during gameplay/logic execution.
- Separate read-only bundled assets from user-generated content.

## 6. Configuration Strategy

Distinguish three categories of values. Do not mix them.

| Category | Example | Location |
|----------|---------|----------|
| Compile-time constant | Max packet size, version string | Named constant in source code |
| Runtime config | Window size, keybinds, paths | Config file loaded at startup, read-only after |
| Dynamic state | Player health, current document, selection | In-memory state model, never in config files |

## 7. Testing Structure

Mirror the source structure:

```
tests/
  Core.Tests/
  Application.Tests/
  Infrastructure.Tests/
```

**Rules**:
- Unit tests target Core and Application layers (fast, no I/O).
- Infrastructure tests verify external integration (file system, network, rendering).
- Tests exercise public interfaces, not private methods or internal state.
- Do not test the language standard library or third-party frameworks.

## 8. Mod / Plugin Content

If the application supports external content:

```
mods/               # User-provided mod folders
  <mod-name>/
    manifest.json   # Mod metadata, dependencies, version
    assets/         # Mod-specific assets
    scripts/        # Mod code or configurations
```

**Rules**:
- The core application must not depend on any mod content.
- Mods are loaded dynamically by the infrastructure layer via the plugin API defined in Core.
- Validate mod manifests before loading content.
