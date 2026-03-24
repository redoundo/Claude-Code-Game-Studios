#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_dest(custom_dest: str | None) -> Path:
    if custom_dest:
        return Path(custom_dest).expanduser()
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def install(force: bool, dest_root: Path, source_dir: Path) -> int:
    if not source_dir.is_dir():
        raise SystemExit(f"No generated skills found at {source_dir}. Run .codex/scripts/sync_from_claude.py first.")

    dest_root.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    skipped: list[str] = []

    for skill_dir in sorted(path for path in source_dir.iterdir() if path.is_dir()):
        dest = dest_root / skill_dir.name
        if dest.exists():
            if not force:
                skipped.append(skill_dir.name)
                continue
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)
        installed.append(skill_dir.name)

    if installed:
        print(f"Installed {len(installed)} skills into {dest_root}")
        for name in installed:
            print(f"  - {name}")

    if skipped:
        print("Skipped existing skills:")
        for name in skipped:
            print(f"  - {name}")
        print("Re-run with --force to replace them.")

    print("Restart Codex to pick up new skills.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install repo-local Codex skills into $CODEX_HOME/skills.")
    parser.add_argument("--dest", help="Override the destination skills directory.")
    parser.add_argument(
        "--source",
        default=str(REPO_ROOT / ".codex" / "skills"),
        help="Directory containing the generated skill folders.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace any existing skill directories with the same name.",
    )
    args = parser.parse_args()
    return install(
        force=args.force,
        dest_root=resolve_dest(args.dest),
        source_dir=Path(args.source).expanduser(),
    )


if __name__ == "__main__":
    raise SystemExit(main())
