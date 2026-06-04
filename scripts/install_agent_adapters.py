#!/usr/bin/env python3
"""Install LLM Agentic Rules adapters for coding agents and IDE assistants."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import platform
import shutil
import sys
import tempfile


TARGETS = [
    "codex",
    "claude-code",
    "opencode",
    "kilocode",
    "kimi-code",
    "hermes-agent",
    "aider",
    "gemini-cli",
    "goose",
    "cursor",
    "windsurf",
    "cline",
    "roo-code",
    "continue",
    "zed",
    "sourcegraph-cody",
    "github-copilot",
    "jetbrains-ai",
]


@dataclass
class PlannedCopy:
    source: Path
    destination: Path
    component: str


class AdapterInstallError(RuntimeError):
    """Raised when adapter installation cannot safely continue."""


def repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "skills" / "llm-agentic-rules" / "SKILL.md",
        root / "commands" / "rules-audit.md",
        root / "agents" / "rules-reviewer.md",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise AdapterInstallError("Repository root is missing adapter sources: " + ", ".join(missing))
    return root


def home_dir() -> Path:
    return Path.home()


def target_base(target: str, home: Path, target_root: Path | None = None) -> Path:
    if target_root is not None:
        return target_root / target

    system = platform.system().lower()
    config = home / ".config"

    if target == "codex":
        return home / ".codex" / "plugins" / "llm-agentic-rules"
    if target == "claude-code":
        return home / ".claude"
    if target == "opencode":
        return config / "opencode" / "llm-agentic-rules"
    if target == "kilocode":
        return config / "kilocode" / "llm-agentic-rules"
    if target == "hermes-agent":
        return config / "hermes-agent" / "llm-agentic-rules"
    if target == "kimi-code":
        return config / "kimi-code" / "llm-agentic-rules"
    if target == "aider":
        return home / ".aider" / "llm-agentic-rules"
    if target == "gemini-cli":
        return config / "gemini-cli" / "llm-agentic-rules"
    if target == "goose":
        return config / "goose" / "llm-agentic-rules"
    if target == "cursor":
        return home / ".cursor"
    if target == "windsurf":
        return config / "windsurf" / "llm-agentic-rules"
    if target == "cline":
        return config / "cline" / "llm-agentic-rules"
    if target == "roo-code":
        return config / "roo-code" / "llm-agentic-rules"
    if target == "continue":
        return home / ".continue" / "llm-agentic-rules"
    if target == "zed":
        return config / "zed" / "llm-agentic-rules"
    if target == "sourcegraph-cody":
        return config / "sourcegraph-cody" / "llm-agentic-rules"
    if target == "github-copilot":
        return config / "github-copilot" / "llm-agentic-rules"
    if target == "jetbrains-ai":
        return config / "JetBrains" / "llm-agentic-rules"
    raise ValueError(f"Unsupported target: {target}")


def plan_for_target(root: Path, target: str, home: Path) -> list[PlannedCopy]:
    base = target_base(target, home)
    common = [
        PlannedCopy(root / "skills" / "llm-agentic-rules" / "SKILL.md", base / "llm-agentic-rules.md", "skill"),
        PlannedCopy(root / "docs" / "checklist-packs.md", base / "checklist-packs.md", "docs"),
        PlannedCopy(root / "docs" / "risk-tiering.md", base / "risk-tiering.md", "docs"),
        PlannedCopy(root / "docs" / "domain-index.md", base / "domain-index.md", "docs"),
    ]

    if target == "codex":
        return [
            PlannedCopy(root / ".codex-plugin" / "plugin.json", base / ".codex-plugin" / "plugin.json", "codex"),
            PlannedCopy(root / "skills" / "llm-agentic-rules" / "SKILL.md", base / "skills" / "llm-agentic-rules" / "SKILL.md", "skill"),
        ]

    if target == "claude-code":
        return [
            PlannedCopy(root / "skills" / "llm-agentic-rules" / "SKILL.md", base / "skills" / "llm-agentic-rules" / "SKILL.md", "skill"),
            PlannedCopy(root / "commands" / "rules-audit.md", base / "commands" / "rules-audit.md", "commands"),
            PlannedCopy(root / "commands" / "rules-plan.md", base / "commands" / "rules-plan.md", "commands"),
            PlannedCopy(root / "commands" / "rules-release.md", base / "commands" / "rules-release.md", "commands"),
        ]

    return common + [
        PlannedCopy(root / "commands" / "rules-audit.md", base / "commands" / "rules-audit.md", "commands"),
        PlannedCopy(root / "commands" / "rules-plan.md", base / "commands" / "rules-plan.md", "commands"),
        PlannedCopy(root / "commands" / "rules-release.md", base / "commands" / "rules-release.md", "commands"),
        PlannedCopy(root / "agents" / "rules-architect.md", base / "agents" / "rules-architect.md", "agents"),
        PlannedCopy(root / "agents" / "rules-reviewer.md", base / "agents" / "rules-reviewer.md", "agents"),
        PlannedCopy(root / "agents" / "rules-release-gate.md", base / "agents" / "rules-release-gate.md", "agents"),
    ]


def same_file_content(source: Path, destination: Path) -> bool:
    return destination.exists() and source.read_bytes() == destination.read_bytes()


def ensure_destination_safe(destination: Path) -> None:
    if destination.exists() and destination.is_dir():
        raise AdapterInstallError(f"Destination is a directory, expected file: {destination}")
    if destination.is_symlink():
        raise AdapterInstallError(f"Refusing to overwrite symlink destination: {destination}")


def backup_path_for(destination: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = destination.with_suffix(destination.suffix + f".{stamp}.bak")
    counter = 1
    while candidate.exists():
        candidate = destination.with_suffix(destination.suffix + f".{stamp}.{counter}.bak")
        counter += 1
    return candidate


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, dir=str(destination.parent)) as handle:
        temp_path = Path(handle.name)
    try:
        shutil.copy2(source, temp_path)
        temp_path.replace(destination)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def copy_file(source: Path, destination: Path, apply: bool, backup: bool) -> str:
    if not source.is_file():
        raise FileNotFoundError(source)
    ensure_destination_safe(destination)
    if same_file_content(source, destination):
        print(f"SKIP unchanged {destination}")
        return "skipped"
    if not apply:
        print(f"DRY-RUN copy {source} -> {destination}")
        return "planned"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and backup:
        backup_path = backup_path_for(destination)
        shutil.copy2(destination, backup_path)
        print(f"Backed up {destination} -> {backup_path}")
    atomic_copy(source, destination)
    print(f"Copied {source} -> {destination}")
    return "copied"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["all", *TARGETS])
    parser.add_argument("--home", type=Path, default=home_dir())
    parser.add_argument("--target-root", type=Path, help="Install into <target-root>/<target> instead of user config paths")
    parser.add_argument(
        "--component",
        choices=["all", "codex", "skill", "docs", "commands", "agents"],
        default="all",
        help="Install only one component group",
    )
    parser.add_argument("--apply", action="store_true", help="Write files")
    parser.add_argument("--dry-run", action="store_true", help="Show planned writes")
    parser.add_argument("--list-targets", action="store_true", help="Print supported targets and exit")
    parser.add_argument("--no-backup", action="store_true", help="Do not create timestamped backups when overwriting")
    parser.add_argument("--fail-fast", action="store_true", help="Stop at the first copy error")
    args = parser.parse_args()

    if args.list_targets:
        print("\n".join(TARGETS))
        return 0

    if not args.target:
        print("--target is required unless --list-targets is used", file=sys.stderr)
        return 2

    if not args.apply and not args.dry_run:
        print("Refusing to write without --apply. Use --dry-run to preview.", file=sys.stderr)
        return 2

    try:
        root = repo_root()
    except AdapterInstallError as error:
        print(f"Installer preflight failed: {error}", file=sys.stderr)
        return 1

    if args.target_root:
        args.target_root = args.target_root.resolve()

    targets = TARGETS if args.target == "all" else [args.target]
    totals = {"planned": 0, "copied": 0, "skipped": 0, "failed": 0}
    for target in targets:
        print(f"\n[{target}]")
        try:
            plan = plan_for_target(root, target, args.home)
        except Exception as error:
            totals["failed"] += 1
            print(f"ERROR planning {target}: {error}", file=sys.stderr)
            if args.fail_fast:
                return 1
            continue
        if args.target_root:
            default_base = target_base(target, args.home)
            override_base = target_base(target, args.home, args.target_root)
            plan = [
                PlannedCopy(item.source, override_base / item.destination.relative_to(default_base), item.component)
                for item in plan
            ]
        if args.component != "all":
            plan = [item for item in plan if item.component == args.component]
        if not plan:
            print(f"No files selected for component: {args.component}")
            continue
        for item in plan:
            try:
                result = copy_file(item.source, item.destination, apply=args.apply, backup=not args.no_backup)
                totals[result] += 1
            except Exception as error:
                totals["failed"] += 1
                print(f"ERROR copying {item.source} -> {item.destination}: {error}", file=sys.stderr)
                if args.fail_fast:
                    print("\nStopped because --fail-fast was set.", file=sys.stderr)
                    return 1
    print(
        "\nSummary: "
        f"planned={totals['planned']} copied={totals['copied']} "
        f"skipped={totals['skipped']} failed={totals['failed']}"
    )
    return 1 if totals["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
