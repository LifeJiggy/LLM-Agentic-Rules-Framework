#!/usr/bin/env python3
"""
LLM & Agentic Rules Framework CLI

A unified command-line interface for framework operations.

Usage:
    python scripts/cli.py [command] [options]

Commands:
    check           Check system requirements
    validate        Validate framework structure
    report          Generate framework report
    export          Export checklists
    install         Install adapter for a target
    list            List available targets and components
    help            Show this help message
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).parent.parent


def cmd_check(args):
    """Check system requirements."""
    from setup import SetupManager
    manager = SetupManager(FRAMEWORK_ROOT)
    success = manager.run_check()
    sys.exit(0 if success else 1)


def cmd_validate(args):
    """Validate framework structure."""
    from validate_framework import FrameworkValidator
    validator = FrameworkValidator(FRAMEWORK_ROOT, verbose=args.verbose)
    results = validator.validate_all()
    validator.print_results()
    
    failed = sum(1 for r in results if r.status == "fail")
    sys.exit(1 if failed > 0 else 0)


def cmd_report(args):
    """Generate framework report."""
    from generate_report import ReportGenerator
    generator = ReportGenerator(FRAMEWORK_ROOT)
    report = generator.generate_summary_report()
    
    if args.format == "json":
        generator.print_json_report(report)
    elif args.format == "markdown":
        generator.print_markdown_report(report)
    else:
        generator.print_text_report(report)


def cmd_export(args):
    """Export checklists."""
    from export_checklists import ChecklistExporter
    exporter = ChecklistExporter(FRAMEWORK_ROOT)
    sections = exporter.collect_checklists(filter_priority=args.filter)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == "json":
        exporter.export_json(sections, output_path)
    else:
        exporter.export_markdown(sections, output_path)
    
    print(f"Exported {len(sections)} sections to {output_path}")


def cmd_install(args):
    """Install adapter for a target."""
    import subprocess
    
    cmd = [sys.executable, str(FRAMEWORK_ROOT / "scripts" / "install_agent_adapters.py")]
    
    if args.target:
        cmd.extend(["--target", args.target])
    else:
        cmd.extend(["--target", "all"])
    
    if args.component:
        cmd.extend(["--component", args.component])
    
    if args.dry_run:
        cmd.append("--dry-run")
    
    if args.apply:
        cmd.append("--apply")
    
    subprocess.run(cmd)


def cmd_list(args):
    """List available targets and components."""
    import json
    
    manifest_path = FRAMEWORK_ROOT / "adapters" / "manifest.json"
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print("\nAvailable Targets:")
        print("-" * 40)
        for target in manifest.get("supportedTargets", []):
            print(f"  - {target}")
        
        print("\nComponents:")
        print("-" * 40)
        for comp, path in manifest.get("components", {}).items():
            print(f"  - {comp}: {path}")
    else:
        print("Manifest not found")


def main():
    parser = argparse.ArgumentParser(
        description="LLM & Agentic Rules Framework CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cli.py check
  python scripts/cli.py validate --verbose
  python scripts/cli.py report --format markdown
  python scripts/cli.py export --output build/checklists.md
  python scripts/cli.py install --target claude-code --apply
  python scripts/cli.py list
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Check command
    subparsers.add_parser("check", help="Check system requirements")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate framework structure")
    validate_parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate framework report")
    report_parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export checklists")
    export_parser.add_argument("--output", default="build/checklists.md")
    export_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    export_parser.add_argument("--filter", choices=["P0", "P1", "P2", "P3"])
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install adapter for a target")
    install_parser.add_argument("--target", help="Target to install for")
    install_parser.add_argument("--component", help="Component to install")
    install_parser.add_argument("--dry-run", action="store_true", help="Preview without installing")
    install_parser.add_argument("--apply", action="store_true", help="Apply changes")
    
    # List command
    subparsers.add_parser("list", help="List available targets and components")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "check": cmd_check,
        "validate": cmd_validate,
        "report": cmd_report,
        "export": cmd_export,
        "install": cmd_install,
        "list": cmd_list,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
