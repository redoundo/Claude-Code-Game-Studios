---
name: "team-audio"
description: "Orchestrate audio team: audio-director + sound-designer + technical-artist + gameplay-programmer for full audio pipeline from direction to implementation."
---

# Team Audio

Synced from `.claude/skills/team-audio/SKILL.md`.

## Codex Notes

- Invoke this workflow with `$team-audio`.
- Ask choice questions directly in conversation using 2-4 labeled options.
- For role-specific delegation, load `.codex/references/agents/<role>.md` on demand instead of relying on Claude-only agent types.
- Read `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md` when the work crosses domains.

When this skill is invoked, orchestrate the audio team through a structured pipeline.

**Decision Points:** At each step transition, use plain-text option prompts to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target feature or area (e.g., `combat`,
   `main menu`, `forest biome`, `boss encounter`).

2. **Gather context**:
   - Read relevant design docs in `design/gdd/` for the feature
   - Read the sound bible at `design/gdd/sound-bible.md` if it exists
   - Read existing audio asset lists in `assets/audio/`
   - Read any existing sound design docs for this area

## How to Delegate

Spawn Codex subagents for each team member and load the matching role profile from `.codex/references/agents/<role>.md` when you delegate:
- load `.codex/references/agents/audio-director.md` — Sonic identity, emotional tone, audio palette
- load `.codex/references/agents/sound-designer.md` — SFX specifications, audio events, mixing groups
- load `.codex/references/agents/technical-artist.md` — Audio middleware, bus structure, memory budgets
- load `.codex/references/agents/gameplay-programmer.md` — Audio manager, gameplay triggers, adaptive music

Always provide full context in each agent's prompt (feature description, existing audio assets, design doc references).

3. **Orchestrate the audio team** in sequence:

### Step 1: Audio Direction (audio-director)
Spawn the `audio-director` agent to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design (sound-designer)
Spawn the `sound-designer` agent to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

### Step 3: Technical Implementation (technical-artist)
Spawn the `technical-artist` agent to:
- Design the audio middleware integration (Wwise/FMOD/native)
- Define audio bus structure and routing
- Specify memory budgets for audio assets per platform
- Plan streaming vs preloaded asset strategy
- Design any audio-reactive visual effects

### Step 4: Code Integration (gameplay-programmer)
Spawn the `gameplay-programmer` agent to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers

4. **Compile the audio design document** combining all team outputs.

5. **Save to** `design/gdd/audio-[feature].md`.

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.
