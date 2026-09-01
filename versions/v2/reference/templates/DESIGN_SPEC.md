# Design Specification: [Project/Feature Name]

## 1. Overview

### 1.1 Project Name
[Short descriptive name.]

### 1.2 One-Sentence Pitch
[What this project/feature does for the user.]

### 1.3 Target Platform & Runtime
- Platform: [e.g., Windows 10/11, cross-platform, web]
- Runtime: [e.g., Fallout 4 + F4SE, Node.js 20, Python 3.11]
- Version constraints: [e.g., game version 1.10.163+, .NET 8]

### 1.4 Distribution
[Folder/archive name, install location, and required files.]

---

## 2. Design Intent

### 2.1 Core Experience
[What the user should feel and the moment-to-moment experience.]

### 2.2 Success Criteria
[Observable conditions that define "done."]

### 2.3 Inspiration & References
[Links, images, GIFs, or descriptions of reference material.]

---

## 3. Scope

### 3.1 In Scope
- [Feature or capability]
- [Feature or capability]

### 3.2 Out of Scope
- [Explicitly excluded thing]
- [Explicitly excluded thing]

### 3.3 Minimum Viable Product (MVP)
[Smallest subset that is a complete, testable, releasable experience.]

### 3.4 Deferred / Future Work
[Nice-to-have features planned for later iterations.]

---

## 4. Technical Architecture

### 4.1 Technology Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| [e.g., Core logic] | [e.g., C++ F4SE plugin] | [Why] |
| [e.g., UI] | [e.g., PrismaUI F4 + React] | [Why] |
| [e.g., Settings] | [e.g., MCM + INI] | [Why] |

### 4.2 Data Sources
[What data is read, how, and how often.]

### 4.3 Update Cadence & Performance
[Timers, event triggers, FPS targets, maximum counts, throttling rules.]

### 4.4 Persistence
[What state survives restart/save/load and where it is stored.]

### 4.5 Pattern Selection
| Problem / Concern | Selected Pattern | Justification ("Use When" match) |
|---|---|---|
| [e.g., Entities have mixable behaviors] | [Component-Based] | [Entities need different behavior combinations at runtime] |
| [e.g., Distinct UI modes] | [State Machine] | [Distinct modes with different update/render logic] |

---

## 5. Mechanics & Behavior

### 5.1 Activation & Triggers
[How the feature starts, stops, and becomes available.]

### 5.2 State Machine
[States, transitions, and conditions.]

### 5.3 Core Algorithms
[Math, filtering, and rules — described in prose, not code.]

### 5.4 Edge Cases & Failure Modes
[Behavior when inputs are missing, invalid, or extreme.]

---

## 6. User Experience & Interface

### 6.1 Access Method
[Hotkey, menu, command, automatic, etc.]

### 6.2 Layout & Positioning
[Exact size, position, anchor, and z-order.]

### 6.3 Visual Design System
| Element | Color | Size/Shape | Font | Effects |
|---------|-------|------------|------|---------|
| [Background] | [#000000] | [400x300px rectangle] | [N/A] | [50% opacity] |
| [Sweep line] | [#00FFFF] | [2px line] | [N/A] | [glow] |
| [Alert blip] | [#FF0000] | [6px circle] | [N/A] | [fade over 3s] |

### 6.4 Animation & Timing
[What moves, for how long, and how it loops or responds.]

### 6.5 Audio Feedback
[Sounds and when they play.]

### 6.6 Accessibility
[Colorblind safety, scaling, motion reduction, etc.]

---

## 7. Content & Strings

### 7.1 User-Facing String Table
| Context | String ID | English Text | Notes |
|---------|-----------|--------------|-------|
| [Settings page title] | [DS_SettingsTitle] | [Motion Tracker] | [Noun, title case] |
| [Setting label] | [DS_UpdateRateLabel] | [Update Rate] | [Seconds between scans] |

### 7.2 Notifications & Feedback Messages
| Trigger | Message |
|---------|---------|
| [Feature enabled] | ["Motion tracker online."] |

### 7.3 Voice / Tone Guidelines
[Lore-friendly, clinical, arcadey, etc.]

---

## 8. Assets

### 8.1 Asset Inventory
| Asset ID | Type | File Path | Source | Format | Status |
|----------|------|-----------|--------|--------|--------|
| [DS_RadarBg] | Texture | [Interface/MotionTracker/bg.dds] | [New] | [DDS BC7] | [Required] |
| [DS_PingSfx] | Sound | [Sound/fx/DS_Ping.wav] | [New] | [WAV 48kHz mono] | [Required] |

### 8.2 Placeholder Policy
[What can be a placeholder for the MVP and what must be final.]

---

## 9. Configuration

### 9.1 User Settings
| Setting ID | Type | Default | Range | Description |
|------------|------|---------|-------|-------------|
| [DS_UpdateRate] | Slider | [0.5] | [0.1–2.0s] | [Seconds between scans] |
| [DS_MaxRange] | Slider | [50.0] | [10–200m] | [Maximum detection range] |
| [DS_ShowHostilesOnly] | Toggle | [true] | [true/false] | [Only show hostile actors] |

### 9.2 Default Presets
[Any bundled presets and what values they set.]

---

## 10. Compatibility & Distribution

### 10.1 Hard Dependencies
| Dependency | Version | Purpose |
|------------|---------|---------|
| [F4SE] | [0.6.23+] | [Runtime hooks] |

### 10.2 Soft Dependencies
| Dependency | Fallback Behavior |
|------------|-------------------|
| [iHUD] | [User disables compass manually] |

### 10.3 Known Conflicts
[Systems that conflict and recommended mitigations.]

### 10.4 Environment Guidance
[Load order, install order, recommended companions.]

### 10.5 Update Path
[How existing users update between versions.]

---

## 11. Testing & Acceptance Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| [AC1] | [MVP feature works in a clean environment] | [In-game / runtime test] |
| [AC2] | [Settings save and load correctly] | [Open/close settings test] |

---

## 12. Open Questions / Assumptions

- [Assumption: player can rebind the hotkey through settings]
- [Question: should blips persist through save/load?]

---

## 13. Revision History

| Date | Author | Change |
|------|--------|--------|
| [YYYY-MM-DD] | [Agent/User] | [Initial specification] |
