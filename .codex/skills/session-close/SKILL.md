---
name: "session-close"
description: "Archive active session state and append a session log for this Game Studios repo when you intentionally end a Codex work session."
---

# Session Close

Use this skill when you intentionally want to close out a Codex work session.

## Workflow

1. Review `production/session-state/active.md` if it exists so you know what will be archived.
2. Run `bash .codex/scripts/session_close.sh`.
3. Summarize what was archived, which log file changed, and whether uncommitted work remains.
4. If no active state exists, still report recent commits and modified files from the session log output.
