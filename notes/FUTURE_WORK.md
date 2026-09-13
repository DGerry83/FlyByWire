# Future Work

Ideas not yet scheduled, recorded so they don't get lost. Not part of the shipped skill.

## Lighter-interaction variant

FlyByWire is deliberately heavyweight: every phase ends in a user-approval checkpoint (`CORE_PROTOCOLS.md` §8), which makes even small tasks a gated session. Worth exploring: a reduced-interaction profile — e.g. checkpoints only at phase boundaries that change scope or risk (contract approval, mid-execution review), auto-proceed on mechanical phases — possibly as a SKILL.md-declared mode or a per-project `AGENTS.md` knob. Open questions: does the +50pp A/B process-discipline result survive fewer gates (the checkpoints are plausibly *why* it works), and how would the eval fixtures assert the difference. Public docs intentionally do not promise this; it is an exploration item only.

## Closing the Phase 4b eval gap

No standardized benchmark measures the skill's actual niche (multi-turn, checkpointed human-agent collaboration on underspecified tasks). Candidate directions are listed in `eval/TESTING.md` Phase 4b (scripted/simulated user, underspecified-task suites, scope-creep scenarios).
