---
name: "studio-context"
description: "Load branch, sprint, active session state, and documentation-gap context for this Game Studios repo before starting other work."
---

# Studio Context

Use this skill when you want the Codex equivalent of the Claude session-start hooks.

## Workflow

1. Run `bash .codex/scripts/session_context.sh`.
2. Summarize the current branch, recent commits, sprint or milestone context, bug count, and code-health signals.
3. If `production/session-state/active.md` exists, read it before recommending next steps.
4. Translate any workflow suggestions to `$skill-name` form.
5. Do not edit files in this skill.
