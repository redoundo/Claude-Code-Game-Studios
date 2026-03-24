---
name: "team-combat"
description: "Orchestrate the combat team: coordinates game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, and qa-tester to design, implement, and validate a combat feature end-to-end."
---

# Team Combat

Synced from `.claude/skills/team-combat/SKILL.md`.

## Codex Notes

- Invoke this workflow with `$team-combat`.
- Ask choice questions directly in conversation using 2-4 labeled options.
- For role-specific delegation, load `.codex/references/agents/<role>.md` on demand instead of relying on Claude-only agent types.
- Read `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md` when the work crosses domains.

When this skill is invoked, orchestrate the combat team through a structured pipeline.

**Decision Points:** At each phase transition, use plain-text option prompts to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase or file edit.

## Team Composition
- **game-designer** — Design the mechanic, define formulas and edge cases
- **gameplay-programmer** — Implement the core gameplay code
- **ai-programmer** — Implement NPC/enemy AI behavior for the feature
- **technical-artist** — Create VFX, shader effects, and visual feedback
- **sound-designer** — Define audio events, impact sounds, and ambient combat audio
- **qa-tester** — Write test cases and validate the implementation

## How to Delegate

Spawn Codex subagents for each team member and load the matching role profile from `.codex/references/agents/<role>.md` when you delegate:
- load `.codex/references/agents/game-designer.md` — Design the mechanic, define formulas and edge cases
- load `.codex/references/agents/gameplay-programmer.md` — Implement the core gameplay code
- load `.codex/references/agents/ai-programmer.md` — Implement NPC/enemy AI behavior
- load `.codex/references/agents/technical-artist.md` — Create VFX, shader effects, visual feedback
- load `.codex/references/agents/sound-designer.md` — Define audio events, impact sounds, ambient audio
- load `.codex/references/agents/qa-tester.md` — Write test cases and validate implementation

Always provide full context in each agent's prompt (design doc path, relevant code files, constraints). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Design
Delegate to **game-designer**:
- Create or update the design document in `design/gdd/` covering: mechanic overview, player fantasy, detailed rules, formulas with variable definitions, edge cases, dependencies, tuning knobs with safe ranges, and acceptance criteria
- Output: completed design document

### Phase 2: Architecture
Delegate to **gameplay-programmer** (with **ai-programmer** if AI is involved):
- Review the design document
- Design the code architecture: class structure, interfaces, data flow
- Identify integration points with existing systems
- Output: architecture sketch with file list and interface definitions

### Phase 3: Implementation (parallel where possible)
Delegate in parallel:
- **gameplay-programmer**: Implement core combat mechanic code
- **ai-programmer**: Implement AI behaviors (if the feature involves NPC reactions)
- **technical-artist**: Create VFX and shader effects
- **sound-designer**: Define audio event list and mixing notes

### Phase 4: Integration
- Wire together gameplay code, AI, VFX, and audio
- Ensure all tuning knobs are exposed and data-driven
- Verify the feature works with existing combat systems

### Phase 5: Validation
Delegate to **qa-tester**:
- Write test cases from the acceptance criteria
- Test all edge cases documented in the design
- Verify performance impact is within budget
- File bug reports for any issues found

### Phase 6: Sign-off
- Collect results from all team members
- Report feature status: COMPLETE / NEEDS WORK / BLOCKED
- List any outstanding issues and their assigned owners

## Output
A summary report covering: design completion status, implementation status per team member, test results, and any open issues.
