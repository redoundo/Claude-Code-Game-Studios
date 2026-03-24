---
name: "team-narrative"
description: "Orchestrate the narrative team: coordinates narrative-director, writer, world-builder, and level-designer to create cohesive story content, world lore, and narrative-driven level design."
---

# Team Narrative

Synced from `.claude/skills/team-narrative/SKILL.md`.

## Codex Notes

- Invoke this workflow with `$team-narrative`.
- Ask choice questions directly in conversation using 2-4 labeled options.
- For role-specific delegation, load `.codex/references/agents/<role>.md` on demand instead of relying on Claude-only agent types.
- Read `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md` when the work crosses domains.

When this skill is invoked, orchestrate the narrative team through a structured pipeline.

**Decision Points:** At each phase transition, use plain-text option prompts to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase or file edit.

## Team Composition
- **narrative-director** — Story arcs, character design, dialogue strategy, narrative vision
- **writer** — Dialogue writing, lore entries, item descriptions, in-game text
- **world-builder** — World rules, faction design, history, geography, environmental storytelling
- **level-designer** — Level layouts that serve the narrative, pacing, environmental storytelling beats

## How to Delegate

Spawn Codex subagents for each team member and load the matching role profile from `.codex/references/agents/<role>.md` when you delegate:
- load `.codex/references/agents/narrative-director.md` — Story arcs, character design, narrative vision
- load `.codex/references/agents/writer.md` — Dialogue writing, lore entries, in-game text
- load `.codex/references/agents/world-builder.md` — World rules, faction design, history, geography
- load `.codex/references/agents/level-designer.md` — Level layouts that serve the narrative, pacing

Always provide full context in each agent's prompt (narrative brief, lore dependencies, character profiles). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 2 agents can run simultaneously).

## Pipeline

### Phase 1: Narrative Direction
Delegate to **narrative-director**:
- Define the narrative purpose of this content: what story beat does it serve?
- Identify characters involved, their motivations, and how this fits the overall arc
- Set the emotional tone and pacing targets
- Specify any lore dependencies or new lore this introduces
- Output: narrative brief with story requirements

### Phase 2: World Foundation (parallel)
Delegate in parallel:
- **world-builder**: Create or update lore entries for factions, locations, and history relevant to this content. Cross-reference against existing lore for contradictions. Set canon level for new entries.
- **writer**: Draft character dialogue using voice profiles. Ensure all lines are under 120 characters, use named placeholders for variables, and are localization-ready.

### Phase 3: Level Narrative Integration
Delegate to **level-designer**:
- Review the narrative brief and lore foundation
- Design environmental storytelling elements in the level
- Place narrative triggers, dialogue zones, and discovery points
- Ensure pacing serves both gameplay and story

### Phase 4: Review and Consistency
Delegate to **narrative-director**:
- Review all dialogue against character voice profiles
- Verify lore consistency across new and existing entries
- Confirm narrative pacing aligns with level design
- Check that all mysteries have documented "true answers"

### Phase 5: Polish
- Writer reviews all text for localization readiness
- Verify no line exceeds dialogue box constraints
- Confirm all text uses string keys (localization pipeline ready)
- World-builder finalizes canon levels for all new lore

## Output
A summary report covering: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results, and any unresolved contradictions.
