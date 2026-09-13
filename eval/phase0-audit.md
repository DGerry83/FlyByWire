# Phase 0 Audit — flybywire skill

Date: 2026-07-30
Method: static inspection only (no model calls). Spec compliance against [agentskills.io specification](https://agentskills.io/specification) and Kimi Code CLI skill docs; security review against the [OWASP Agentic Skills Top 10 (AST10)](https://owasp.org/www-project-agentic-skills-top-10/).

## 1. Spec Compliance

| Check | Result | Notes |
|---|---|---|
| Directory form with `SKILL.md` | PASS | Standard layout. |
| `name` present, 1–64 chars, lowercase + hyphens | PASS | `flybywire` (9 chars). |
| `name` matches parent directory name | PASS (with caveat) | Install folder must be exactly `flybywire` — README install commands do this. The dev repo folder is `FlyByWire`; copying it verbatim (capital letters) would fail strict validators. See F2. |
| `description` present, 1–1024 chars | PASS | 278 chars; states what + when. |
| Frontmatter is valid YAML | PASS | Flat `key: value` pairs, no colon-space sequences inside values. |
| Body size (< 500 lines, < 5000 tokens recommended) | PASS | 30 lines, ~700 tokens. |
| Progressive disclosure structure | PASS | Metadata at startup; SKILL.md on activation; workflow files loaded on demand. |
| File references one level deep (recommendation) | DEVIATION (accepted) | Chain is SKILL.md → Router.md → workflow → `reference/` (3 levels). This is deliberate: each hop is conditional and shrinks context. The spec text is a soft recommendation ("avoid deeply nested chains"), not a requirement. |
| Kimi-specific fields | PASS | `whenToUse` is a Kimi extension; other clients ignore unknown frontmatter fields. No conflict. |
| Optional fields (`license`, `compatibility`, `metadata`) | MISSING | Not required. Worth adding `license` before publishing. See F4. |

External validator: the spec points to the `skills-ref` reference library for automated validation. Not run here (this machine's shell has no outbound network); run it when npm access is available.

## 2. OWASP AST10 Walk-Through

Context: this skill is **pure markdown** — no `scripts/`, no executables, no runtime dependencies. That eliminates the most severe risk categories by construction.

| # | Risk | Status | Assessment |
|---|---|---|---|
| AST01 | Malicious Skills | CLEAN | No code, no payloads. All content is author-controlled prose. The "attack surface" of a markdown skill is its instructions; these contain no credential access, no exfiltration, no obfuscation. |
| AST02 | Supply Chain Compromise | CLEAN | Zero dependencies — no packages, no nested skills, no external repos referenced at runtime. Distribution is `git clone` from your own repo. |
| AST03 | Over-Privileged Skills | ACCEPTED RISK | Neither the Agent Skills spec (beyond experimental `allowed-tools`) nor Kimi frontmatter supports scoped permission manifests. The skill inherits the host agent's full toolset. It genuinely needs shell + file write (it is a coding-workflow skill), so least-privilege scoping would not reduce much. Mitigation: intended scope is documented in README (writes under `notes\…`, reads project files, runs build/test commands). |
| AST04 | Insecure Metadata | PASS | Frontmatter is minimal and honest; description does not overstate. One brand note — see F6. |
| AST05 | Untrusted External Instructions | **FINDING (F1)** | The skill itself fetches nothing at runtime. However, `Exploration.md` directs agents to run web searches and ingest external sources during research sessions, with no instruction to treat that content as untrusted data. A malicious page could attempt indirect prompt injection. |
| AST06 | Weak Isolation | N/A (runtime) | Isolation is the host agent's responsibility, not the skill's. Optional: README note recommending sandboxed/permission-mode runs. |
| AST07 | Update Drift | PASS (for now) | Git distribution. Before publishing: cut tagged releases so users can pin versions; consider noting a content hash in release notes. |
| AST08 | Poor Scanning | PASS | Plain markdown is maximally scanner-friendly — no archives, binaries, or encoding tricks that evade scanners. |
| AST09 | No Governance | PASS (for now) | Personal use. Before publishing: add a CHANGELOG and version tags so downstream users can inventory what they installed. |
| AST10 | Cross-Platform Reuse | PASS | Frontmatter uses only standard fields plus one ignored Kimi extension; relative paths throughout; no platform-specific constructs. |

## 3. Findings and Recommended Actions

| ID | Severity | Finding | Recommended action |
|---|---|---|---|
| F1 | Medium | `Exploration.md` ingests untrusted web content (searches, precedent analysis) with no prompt-injection guard. | **FIXED 2026-07-30**: added §5.8 "External Content Is Data" to `CORE_PROTOCOLS.md` and guard lines in `Exploration.md` (Phase 2 + Research Agent template). |
| F2 | Low | Spec requires `name` to match the install directory; dev folder is `FlyByWire`. | No change needed — README clone commands already target `flybywire`. Keep it that way in all install docs. |
| F3 | Low | Reference chain depth (3 levels) exceeds spec's soft recommendation. | None. Deliberate design; loading discipline was verified by smoke tests. |
| F4 | Low (pre-publish) | No `license` field, no LICENSE file, no version tags or changelog. | Before publishing: choose a license (MIT is typical for skills), add `license: MIT` to frontmatter + LICENSE file, tag releases, start a CHANGELOG. |
| F5 | Info | No runtime permission scoping exists to adopt. | Revisit when `allowed-tools` / OWASP Universal Skill Format matures. Documenting scope in README (already done) is the current best practice. |
| F6 | Info (brand) | `flybywire` collides with FlyByWire Simulations (well-known flight-sim mod group). | Harmless for personal use. If publishing to a public registry, consider a more distinctive name (e.g., `flybywire-workflows`) to avoid impersonation/typosquat flags under AST04. |

## 4. Verdict

Structurally compliant with the Agent Skills standard and Kimi's directory-form requirements. Security posture is strong by construction (pure markdown, zero dependencies); the single substantive finding (F1) is a one-line content guard. Nothing here blocks proceeding to Phase 1 testing; F4/F6 only matter at publish time.
