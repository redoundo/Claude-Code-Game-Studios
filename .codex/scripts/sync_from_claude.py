#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLAUDE_SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
CLAUDE_AGENTS_DIR = REPO_ROOT / ".claude" / "agents"


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    frontmatter = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}

    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")

    return data, body


def title_case(name: str) -> str:
    special = {
        "qa": "QA",
        "ui": "UI",
        "ux": "UX",
        "ai": "AI",
        "adr": "ADR",
        "vfx": "VFX",
        "sfx": "SFX",
        "api": "API",
        "gdscript": "GDScript",
        "gdextension": "GDExtension",
        "umg": "UMG",
        "gas": "GAS",
        "ecs": "ECS",
        "dots": "DOTS",
    }
    parts = []
    for part in name.split("-"):
        parts.append(special.get(part, part.capitalize()))
    return " ".join(parts)


def collapse_whitespace(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    truncated = text[: limit - 3].rstrip()
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return truncated + "..."


def short_description(text: str) -> str:
    primary = text.split(".")[0].strip() or text
    if len(primary) < 25:
        primary = text.strip()
    return collapse_whitespace(primary, 64)


def default_prompt(name: str, description: str) -> str:
    prompt = description.split(".")[0].strip().rstrip(".")
    if not prompt:
        prompt = f"use the {name} workflow"
    prompt = prompt[0].lower() + prompt[1:] if prompt else prompt
    return f"Use ${name} to {prompt}."


def dump_yaml(data: dict[str, object], indent: int = 0) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.extend(dump_yaml(value, indent + 2))
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {'true' if value else 'false'}")
        else:
            escaped = str(value).replace('"', '\\"')
            lines.append(f'{prefix}{key}: "{escaped}"')
    return lines


def build_command_pattern(skill_names: list[str]) -> re.Pattern[str]:
    ordered = sorted(skill_names, key=len, reverse=True)
    escaped = [re.escape(name) for name in ordered]
    return re.compile(rf"/({'|'.join(escaped)})(?![a-z0-9-])")


def transform_body(text: str, command_pattern: re.Pattern[str]) -> str:
    transformed = text.replace("\r\n", "\n")
    transformed = command_pattern.sub(lambda match: f"${match.group(1)}", transformed)
    transformed = re.sub(
        r"- `subagent_type:\s*([a-z0-9-]+)`",
        lambda match: f"- load `.codex/references/agents/{match.group(1)}.md`",
        transformed,
    )

    replacements = [
        (
            "Use the `AskUserQuestion` tool to present strategic decisions as a selectable UI.",
            "Present strategic decisions directly in conversation with 2-4 labeled options.",
        ),
        (
            "Use the `AskUserQuestion` tool to present decisions as a selectable UI instead of\nfree-form chat when the user is choosing between clear options.",
            "Present decisions directly in conversation with 2-4 labeled options when the user is choosing between clear options.",
        ),
        (
            "Use the `AskUserQuestion` tool to present decisions as a selectable UI instead of",
            "Present decisions directly in conversation with 2-4 labeled options instead of",
        ),
        (
            "Use the `AskUserQuestion` tool to present decisions as a selectable UI.",
            "Present decisions directly in conversation with 2-4 labeled options.",
        ),
        (
            "Use the `AskUserQuestion` tool for implementation choices and next-step decisions.",
            "Ask implementation and next-step questions directly in conversation using 2-4 labeled options.",
        ),
        (
            "Use the `AskUserQuestion` tool to present strategic decisions as a selectable UI instead of free-form chat.",
            "Present strategic decisions directly in conversation with 2-4 labeled options instead of free-form chat.",
        ),
        (
            "Batch up to 4 independent questions in one call",
            "Batch up to 4 independent questions in one message",
        ),
        (
            "Batch up to 4 questions in one call",
            "Batch up to 4 questions in one message",
        ),
        (
            "The user must approve before moving to the next phase.",
            "The user must approve before moving to the next phase or file edit.",
        ),
        (
            "Use the Task tool to spawn each team member as a subagent:",
            "Spawn Codex subagents for each team member and load the matching role profile from `.codex/references/agents/<role>.md` when you delegate:",
        ),
        (
            "Use the Task tool to request sign-off:",
            "Request sign-off explicitly in conversation or from Codex subagents when parallel review is warranted:",
        ),
        (
            "You have access to the Task tool to delegate to your sub-specialists.",
            "You may delegate to Codex subagents using the matching role profiles when the user explicitly asked for team or parallel work.",
        ),
        (
            "If running as a Task subagent, structure text so the orchestrator can present",
            "If running as a Codex subagent, structure text so the orchestrator can present",
        ),
        ("`TodoWrite`", "`update_plan`"),
        ("TodoWrite", "update_plan"),
        ("`AskUserQuestion`", "plain-text option prompts"),
        ("AskUserQuestion", "plain-text option prompts"),
        ("`Task`", "`spawn_agent`"),
        ("Task tool", "subagent tools"),
        ("Task subagent", "Codex subagent"),
    ]

    for old, new in replacements:
        transformed = transformed.replace(old, new)

    transformed = re.sub(
        r"subagent_type:\s*([a-z0-9-]+)",
        lambda match: f"role profile: `.codex/references/agents/{match.group(1)}.md`",
        transformed,
    )
    transformed = re.sub(
        r"- `role profile: `([^`]+)``",
        lambda match: f"- load `{match.group(1)}`",
        transformed,
    )

    transformed = re.sub(
        r"Follow the \*\*Explain → Capture\*\* pattern:",
        "Follow the **Explain -> Decide** pattern:",
        transformed,
    )
    transformed = re.sub(
        r"\*\*Capture the decision\*\* — Call [^\n]+",
        "**Capture the decision** — ask the user to choose one of the labeled options directly in conversation.",
        transformed,
    )
    transformed = re.sub(
        r"allowed-tools:.*\n",
        "",
        transformed,
    )
    transformed = re.sub(r"\n{3,}", "\n\n", transformed)
    return transformed.strip() + "\n"


def build_skill_markdown(name: str, description: str, body: str) -> str:
    title = title_case(name)
    return (
        f"---\n"
        f'name: "{name}"\n'
        f'description: "{description}"\n'
        f"---\n\n"
        f"# {title}\n\n"
        f"Synced from `.claude/skills/{name}/SKILL.md`.\n\n"
        f"## Codex Notes\n\n"
        f"- Invoke this workflow with `${name}`.\n"
        f"- Ask choice questions directly in conversation using 2-4 labeled options.\n"
        f"- For role-specific delegation, load `.codex/references/agents/<role>.md` on demand instead of relying on Claude-only agent types.\n"
        f"- Read `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md` when the work crosses domains.\n\n"
        f"{body}"
    )


def build_agent_markdown(name: str, description: str, body: str) -> str:
    title = title_case(name)
    return (
        f"# {title}\n\n"
        f"Source: `.claude/agents/{name}.md`\n\n"
        f"Use this file as the role prompt when you spawn a Codex subagent for `{name}`.\n\n"
        f"## Codex Notes\n\n"
        f"- Present user decisions directly in conversation with labeled options.\n"
        f"- If this role delegates, use Codex subagents and pass only task-local context.\n"
        f"- Respect `.claude/docs/coordination-rules.md` and `.claude/docs/review-workflow.md`.\n\n"
        f"## Role Summary\n\n"
        f"{description}\n\n"
        f"{body}"
    )


def build_openai_yaml(name: str, description: str) -> str:
    data = {
        "interface": {
            "display_name": title_case(name),
            "short_description": short_description(description),
            "default_prompt": default_prompt(name, description),
        },
        "policy": {
            "allow_implicit_invocation": False,
        },
    }
    return "\n".join(dump_yaml(data)) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_helper_skill(base_dir: Path, name: str, description: str, body: str) -> None:
    skill_dir = base_dir / "skills" / name
    write_text(
        skill_dir / "SKILL.md",
        f"---\nname: \"{name}\"\ndescription: \"{description}\"\n---\n\n{body.strip()}\n",
    )
    write_text(skill_dir / "agents" / "openai.yaml", build_openai_yaml(name, description))


def sync(base_dir: Path, clean: bool) -> None:
    skills_dir = base_dir / "skills"
    agent_refs_dir = base_dir / "references" / "agents"
    base_dir.mkdir(parents=True, exist_ok=True)

    if clean:
        shutil.rmtree(skills_dir, ignore_errors=True)
        shutil.rmtree(agent_refs_dir, ignore_errors=True)

    skill_dirs = sorted(path for path in CLAUDE_SKILLS_DIR.iterdir() if path.is_dir())
    skill_names = [path.name for path in skill_dirs]
    command_pattern = build_command_pattern(skill_names)

    for skill_dir in skill_dirs:
        metadata, body = parse_frontmatter(skill_dir / "SKILL.md")
        name = metadata.get("name", skill_dir.name)
        description = metadata.get("description", f"Codex port of {name}.")
        transformed_body = transform_body(body, command_pattern)
        target_dir = skills_dir / name
        write_text(target_dir / "SKILL.md", build_skill_markdown(name, description, transformed_body))
        write_text(target_dir / "agents" / "openai.yaml", build_openai_yaml(name, description))

    agent_paths = sorted(CLAUDE_AGENTS_DIR.glob("*.md"))
    for agent_path in agent_paths:
        metadata, body = parse_frontmatter(agent_path)
        name = metadata.get("name", agent_path.stem)
        description = metadata.get("description", f"Codex role profile for {name}.")
        transformed_body = transform_body(body, command_pattern)
        write_text(
            agent_refs_dir / f"{name}.md",
            build_agent_markdown(name, description, transformed_body),
        )

    generate_helper_skill(
        base_dir,
        "studio-context",
        "Load branch, sprint, active session state, and documentation-gap context for this Game Studios repo before starting other work.",
        """
# Studio Context

Use this skill when you want the Codex equivalent of the Claude session-start hooks.

## Workflow

1. Run `bash .codex/scripts/session_context.sh`.
2. Summarize the current branch, recent commits, sprint or milestone context, bug count, and code-health signals.
3. If `production/session-state/active.md` exists, read it before recommending next steps.
4. Translate any workflow suggestions to `$skill-name` form.
5. Do not edit files in this skill.
        """,
    )

    generate_helper_skill(
        base_dir,
        "session-close",
        "Archive active session state and append a session log for this Game Studios repo when you intentionally end a Codex work session.",
        """
# Session Close

Use this skill when you intentionally want to close out a Codex work session.

## Workflow

1. Review `production/session-state/active.md` if it exists so you know what will be archived.
2. Run `bash .codex/scripts/session_close.sh`.
3. Summarize what was archived, which log file changed, and whether uncommitted work remains.
4. If no active state exists, still report recent commits and modified files from the session log output.
        """,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Codex-compatible assets from Claude assets.")
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not delete previously generated .codex skills and agent references first.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / ".codex"),
        help="Output directory for generated skills and role profiles.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser()
    sync(base_dir=out_dir, clean=not args.no_clean)
    print(f"Synced Claude assets into {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
