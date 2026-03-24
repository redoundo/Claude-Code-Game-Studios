---
name: "team-polish"
description: "Orchestrate the polish team: coordinates performance-analyst, technical-artist, sound-designer, and qa-tester to optimize, polish, and harden a feature or area for release quality."
---

# Team Polish

Synced from `.claude/skills/team-polish/SKILL.md`.

## Codex Notes

- Invoke this workflow with `$team-polish`.
- Ask choice questions directly in conversation using 2-4 labeled options.
- For role-specific delegation, load `.codex/references/agents/<role>.md` on demand instead of relying on Claude-only agent types.
- Read `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md` when the work crosses domains.

When this skill is invoked, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, use plain-text option prompts to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase or file edit.

## Team Composition
- **performance-analyst** — Profiling, optimization, memory analysis, frame budget
- **technical-artist** — VFX polish, shader optimization, visual quality
- **sound-designer** — Audio polish, mixing, ambient layers, feedback sounds
- **qa-tester** — Edge case testing, regression testing, soak testing

## How to Delegate

Spawn Codex subagents for each team member and load the matching role profile from `.codex/references/agents/<role>.md` when you delegate:
- load `.codex/references/agents/performance-analyst.md` — Profiling, optimization, memory analysis
- load `.codex/references/agents/technical-artist.md` — VFX polish, shader optimization, visual quality
- load `.codex/references/agents/sound-designer.md` — Audio polish, mixing, ambient layers
- load `.codex/references/agents/qa-tester.md` — Edge case testing, regression testing, soak testing

Always provide full context in each agent's prompt (target feature/area, performance budgets, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phases 3 and 4 can run simultaneously).

## Pipeline

### Phase 1: Assessment
Delegate to **performance-analyst**:
- Profile the target feature/area using `$perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with prioritized optimization list

### Phase 2: Optimization
Delegate to **performance-analyst** (with relevant programmers as needed):
- Fix performance hotspots identified in Phase 1
- Optimize draw calls, reduce overdraw
- Fix memory leaks and reduce allocation pressure
- Verify optimizations don't change gameplay behavior
- Output: optimized code with before/after metrics

### Phase 3: Visual Polish (parallel with Phase 2)
Delegate to **technical-artist**:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

### Phase 4: Audio Polish (parallel with Phase 2)
Delegate to **sound-designer**:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels — nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Delegate to **qa-tester**:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality
- Test on minimum spec hardware (if available)
- Output: test results with any remaining issues

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- Report: READY FOR RELEASE / NEEDS MORE WORK
- List any remaining issues with severity and recommendations

## Output
A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.
