#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = REPO_ROOT / ".codex" / "scripts" / "sync_from_claude.py"
INSTALL_SCRIPT = REPO_ROOT / ".codex" / "scripts" / "install_skills.py"
EXECUTABLE_PATHS = [
    REPO_ROOT / ".githooks" / "pre-commit",
    REPO_ROOT / ".githooks" / "pre-push",
    REPO_ROOT / ".codex" / "scripts" / "session_context.sh",
    REPO_ROOT / ".codex" / "scripts" / "session_close.sh",
]


def run(*args: str) -> None:
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def ensure_executable(path: Path) -> None:
    if not path.exists():
        return
    mode = path.stat().st_mode
    path.chmod(mode | 0o111)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Codex support for this repository.")
    parser.add_argument("--skip-install", action="store_true", help="Do not copy skills into $CODEX_HOME/skills.")
    parser.add_argument("--skip-hooks", action="store_true", help="Do not configure git to use .githooks.")
    parser.add_argument("--dest", help="Override the Codex skills destination directory.")
    parser.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / ".codex"),
        help="Where to generate the Codex skill source tree before installation.",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing installed skills.")
    args = parser.parse_args()

    run(sys.executable, str(SYNC_SCRIPT), "--out-dir", args.out_dir)

    if not args.skip_install:
        install_args = [
            sys.executable,
            str(INSTALL_SCRIPT),
            "--source",
            str(Path(args.out_dir).expanduser() / "skills"),
        ]
        if args.dest:
            install_args.extend(["--dest", args.dest])
        if args.force:
            install_args.append("--force")
        run(*install_args)

    for path in EXECUTABLE_PATHS:
        ensure_executable(path)

    if not args.skip_hooks:
        run("git", "config", "--local", "core.hooksPath", ".githooks")
        print("Configured git hooks: core.hooksPath=.githooks")

    print("Codex bootstrap complete.")
    if args.skip_install:
        print("Skills were generated locally only. Install them later with .codex/scripts/install_skills.py.")
    else:
        print("Restart Codex to pick up the installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
