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
    domains         List and info about domains
    modules         List and info about modules
    agents          List and info about agents
    stats           Show framework statistics
    help            Show this help message
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

FRAMEWORK_ROOT = Path(__file__).parent.parent

# Framework metadata
FRAMEWORK_NAME = "LLM & Agentic Rules Framework"
FRAMEWORK_VERSION = "2.0.0"

# ASCII Banner
BANNER = r"""
 ██╗      ██████╗ ███╗   ██╗██████╗     ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗
 ██║     ██╔═══██╗████╗  ██║██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
 ██║     ██║   ██║██╔██╗ ██║██║  ██║    ██████╔╝███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
 ██║     ██║   ██║██║╚██╗██║██║  ██║    ██╔══██╗██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
 ███████╗╚██████╔╝██║ ╚████║██████╔╝    ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
 ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
"""

FRAMEWORK_INFO = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  {FRAMEWORK_NAME} v{FRAMEWORK_VERSION}                              ║
║  A production-grade rules framework for AI systems                         ║
║  16 Domains | 194 Files | 12 Agents | 9 Modules                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Domain information
DOMAINS = {
    "01-core": {"name": "Core", "focus": "Architecture, context, tools, state", "files": 7},
    "02-security": {"name": "Security", "focus": "Prompt injection, data protection, access control", "files": 7},
    "03-development": {"name": "Development", "focus": "Code quality, maintainability, reviews", "files": 7},
    "04-data": {"name": "Data", "focus": "Privacy, governance, pipelines", "files": 7},
    "05-integration": {"name": "Integration", "focus": "APIs, webhooks, tool contracts", "files": 7},
    "06-operations": {"name": "Operations", "focus": "CI/CD, observability, scaling", "files": 7},
    "07-testing": {"name": "Testing", "focus": "Unit, integration, E2E, regression", "files": 7},
    "08-documentation": {"name": "Documentation", "focus": "API docs, runbooks, guides", "files": 7},
    "09-performance": {"name": "Performance", "focus": "Latency, throughput, caching", "files": 7},
    "10-compliance": {"name": "Compliance", "focus": "Governance, risk controls, audit", "files": 7},
}

# Module information
MODULES = {
    "evaluation": {"name": "Evaluation", "focus": "AI system evaluation", "files": 7},
    "loop": {"name": "Loop", "focus": "Agent loop implementation", "files": 7},
    "tools": {"name": "Tools", "focus": "Tool integration patterns", "files": 7},
    "incident-response": {"name": "Incident Response", "focus": "Incident handling", "files": 7},
    "deployment": {"name": "Deployment", "focus": "CI/CD, release management", "files": 7},
    "monitoring": {"name": "Monitoring", "focus": "Observability, alerting", "files": 7},
    "cost-management": {"name": "Cost Management", "focus": "Budget, optimization", "files": 7},
    "vendor-management": {"name": "Vendor Management", "focus": "Third-party assessment", "files": 7},
    "governance": {"name": "Governance", "focus": "Policy, audit readiness", "files": 7},
}

# Agent information
AGENTS = {
    "rules-architect": {"name": "Rules Architect", "phase": "Design", "role": "System design and architecture"},
    "rules-implementer": {"name": "Rules Implementer", "phase": "Implementation", "role": "System implementation"},
    "rules-reviewer": {"name": "Rules Reviewer", "phase": "Review", "role": "Code and artifact review"},
    "rules-release-gate": {"name": "Rules Release Gate", "phase": "Release", "role": "Release decisions"},
    "rules-eval": {"name": "Rules Eval", "phase": "Evaluation", "role": "Evaluation execution"},
    "rules-compliance-auditor": {"name": "Rules Compliance Auditor", "phase": "Compliance", "role": "Compliance evidence"},
    "rules-data-steward": {"name": "Rules Data Steward", "phase": "Data", "role": "Data governance"},
    "rules-enforcer": {"name": "Rules Enforcer", "phase": "Enforcement", "role": "Policy enforcement"},
    "rules-documentation": {"name": "Rules Documentation", "phase": "Documentation", "role": "Documentation standards"},
    "rules-tracker": {"name": "Rules Tracker", "phase": "Operations", "role": "Metrics and monitoring"},
    "rules-orchestrator": {"name": "Rules Orchestrator", "phase": "Coordination", "role": "Multi-agent coordination"},
    "rules-security": {"name": "Rules Security", "phase": "Security", "role": "Security controls"},
}


def print_banner():
    """Print the framework banner."""
    print(BANNER)
    print(FRAMEWORK_INFO)


def print_color(text: str, color: str):
    """Print colored text."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


def cmd_check(args):
    """Check system requirements."""
    print_banner()
    print_color("Checking system requirements...", "cyan")
    print("=" * 60)
    
    from setup import SetupManager
    manager = SetupManager(FRAMEWORK_ROOT)
    success = manager.run_check()
    sys.exit(0 if success else 1)


def cmd_validate(args):
    """Validate framework structure."""
    print_banner()
    print_color("Validating framework structure...", "cyan")
    print("=" * 60)
    
    from validate_framework import FrameworkValidator
    validator = FrameworkValidator(FRAMEWORK_ROOT, verbose=args.verbose)
    results = validator.validate_all()
    validator.print_results()
    
    failed = sum(1 for r in results if r.status == "fail")
    sys.exit(1 if failed > 0 else 0)


def cmd_report(args):
    """Generate framework report."""
    print_banner()
    print_color("Generating framework report...", "cyan")
    print("=" * 60)
    
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
    print_banner()
    print_color("Exporting checklists...", "cyan")
    print("=" * 60)
    
    from export_checklists import ChecklistExporter
    exporter = ChecklistExporter(FRAMEWORK_ROOT)
    sections = exporter.collect_checklists(filter_priority=args.filter)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == "json":
        exporter.export_json(sections, output_path)
    else:
        exporter.export_markdown(sections, output_path)
    
    print_color(f"Exported {len(sections)} sections to {output_path}", "green")


def cmd_install(args):
    """Install adapter for a target."""
    print_banner()
    print_color("Installing adapter...", "cyan")
    print("=" * 60)
    
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
    print_banner()
    
    import json
    
    manifest_path = FRAMEWORK_ROOT / "adapters" / "manifest.json"
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print_color("Available Targets:", "cyan")
        print("-" * 50)
        for i, target in enumerate(manifest.get("supportedTargets", []), 1):
            print(f"  {i:2d}. {target}")
        
        print_color("\nComponents:", "cyan")
        print("-" * 50)
        for comp, info in manifest.get("components", {}).items():
            if isinstance(info, dict):
                print(f"  - {comp}: {info.get('description', 'N/A')}")
            else:
                print(f"  - {comp}: {info}")
    else:
        print_color("Manifest not found", "red")


def cmd_domains(args):
    """List and info about domains."""
    print_banner()
    
    if args.info:
        # Show info for specific domain
        domain = args.info
        if domain in DOMAINS:
            info = DOMAINS[domain]
            print_color(f"Domain: {info['name']}", "cyan")
            print(f"  ID: {domain}")
            print(f"  Focus: {info['focus']}")
            print(f"  Files: {info['files']}")
            print(f"  Path: domains/{domain}/")
            
            # List files
            domain_path = FRAMEWORK_ROOT / "domains" / domain
            if domain_path.exists():
                print_color("\n  Files:", "yellow")
                for f in sorted(domain_path.glob("*.md")):
                    print(f"    - {f.name}")
        else:
            print_color(f"Domain not found: {domain}", "red")
    else:
        # List all domains
        print_color("Core Domains (10):", "cyan")
        print("-" * 60)
        print(f"  {'ID':<20} {'Name':<20} {'Focus':<30}")
        print("-" * 60)
        for domain_id, info in DOMAINS.items():
            print(f"  {domain_id:<20} {info['name']:<20} {info['focus']:<30}")
        print("-" * 60)
        print(f"  Total: {len(DOMAINS)} domains, {sum(d['files'] for d in DOMAINS.values())} files")


def cmd_modules(args):
    """List and info about modules."""
    print_banner()
    
    if args.info:
        # Show info for specific module
        module = args.info
        if module in MODULES:
            info = MODULES[module]
            print_color(f"Module: {info['name']}", "cyan")
            print(f"  ID: {module}")
            print(f"  Focus: {info['focus']}")
            print(f"  Files: {info['files']}")
            print(f"  Path: {module}/")
            
            # List files
            module_path = FRAMEWORK_ROOT / module
            if module_path.exists():
                print_color("\n  Files:", "yellow")
                for f in sorted(module_path.glob("*.md")):
                    print(f"    - {f.name}")
        else:
            print_color(f"Module not found: {module}", "red")
    else:
        # List all modules
        print_color("Operational Modules (9):", "cyan")
        print("-" * 60)
        print(f"  {'ID':<25} {'Name':<25} {'Focus':<30}")
        print("-" * 60)
        for module_id, info in MODULES.items():
            print(f"  {module_id:<25} {info['name']:<25} {info['focus']:<30}")
        print("-" * 60)
        print(f"  Total: {len(MODULES)} modules, {sum(m['files'] for m in MODULES.values())} files")


def cmd_agents(args):
    """List and info about agents."""
    print_banner()
    
    if args.info:
        # Show info for specific agent
        agent = args.info
        if agent in AGENTS:
            info = AGENTS[agent]
            print_color(f"Agent: {info['name']}", "cyan")
            print(f"  ID: {agent}")
            print(f"  Phase: {info['phase']}")
            print(f"  Role: {info['role']}")
            print(f"  Path: agents/{agent}.md")
        else:
            print_color(f"Agent not found: {agent}", "red")
    else:
        # List all agents
        print_color("Agents (12):", "cyan")
        print("-" * 70)
        print(f"  {'ID':<30} {'Phase':<15} {'Role':<30}")
        print("-" * 70)
        for agent_id, info in AGENTS.items():
            print(f"  {agent_id:<30} {info['phase']:<15} {info['role']:<30}")
        print("-" * 70)
        print(f"  Total: {len(AGENTS)} agents")


def cmd_stats(args):
    """Show framework statistics."""
    print_banner()
    print_color("Framework Statistics", "cyan")
    print("=" * 60)
    
    # Count files
    stats = {
        "domains": {"count": 0, "files": 0},
        "modules": {"count": 0, "files": 0},
        "agents": {"count": 0, "files": 0},
        "skills": {"count": 0, "files": 0},
        "memory": {"count": 0, "files": 0},
        "storage": {"count": 0, "files": 0},
        "docs": {"count": 0, "files": 0},
        "scripts": {"count": 0, "files": 0},
        "examples": {"count": 0, "files": 0},
    }
    
    # Count domain files
    domains_path = FRAMEWORK_ROOT / "domains"
    if domains_path.exists():
        for d in domains_path.iterdir():
            if d.is_dir():
                stats["domains"]["count"] += 1
                stats["domains"]["files"] += len(list(d.glob("*.md")))
    
    # Count module files
    for module in MODULES.keys():
        module_path = FRAMEWORK_ROOT / module
        if module_path.exists():
            stats["modules"]["count"] += 1
            stats["modules"]["files"] += len(list(module_path.glob("*.md")))
    
    # Count agent files
    agents_path = FRAMEWORK_ROOT / "agents"
    if agents_path.exists():
        stats["agents"]["count"] = len(list(agents_path.glob("*.md")))
        stats["agents"]["files"] = stats["agents"]["count"]
    
    # Count skill files
    skills_path = FRAMEWORK_ROOT / "skills"
    if skills_path.exists():
        for d in skills_path.iterdir():
            if d.is_dir():
                stats["skills"]["count"] += 1
                stats["skills"]["files"] += len(list(d.glob("*.md")))
    
    # Count memory files
    memory_path = FRAMEWORK_ROOT / "memory"
    if memory_path.exists():
        stats["memory"]["files"] = len(list(memory_path.glob("*.md")))
    
    # Count storage files
    storage_path = FRAMEWORK_ROOT / "storage"
    if storage_path.exists():
        stats["storage"]["files"] = len(list(storage_path.glob("*.md")))
    
    # Count docs files
    docs_path = FRAMEWORK_ROOT / "docs"
    if docs_path.exists():
        stats["docs"]["files"] = len(list(docs_path.glob("*.md")))
    
    # Count script files
    scripts_path = FRAMEWORK_ROOT / "scripts"
    if scripts_path.exists():
        stats["scripts"]["files"] = len(list(scripts_path.glob("*.py"))) + len(list(scripts_path.glob("*.ps1"))) + len(list(scripts_path.glob("*.sh")))
    
    # Count example files
    examples_path = FRAMEWORK_ROOT / "examples"
    if examples_path.exists():
        for d in examples_path.iterdir():
            if d.is_dir():
                stats["examples"]["count"] += 1
                stats["examples"]["files"] += len(list(d.glob("*.md")))
    
    # Print stats
    total_files = 0
    print(f"\n  {'Category':<20} {'Items':<10} {'Files':<10}")
    print("  " + "-" * 40)
    for category, data in stats.items():
        print(f"  {category:<20} {data['count']:<10} {data['files']:<10}")
        total_files += data['files']
    print("  " + "-" * 40)
    print(f"  {'TOTAL':<20} {'':<10} {total_files:<10}")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=f"{FRAMEWORK_NAME} CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cli.py check
  python scripts/cli.py validate --verbose
  python scripts/cli.py report --format markdown
  python scripts/cli.py export --output build/checklists.md
  python scripts/cli.py install --target claude-code --apply
  python scripts/cli.py list
  python scripts/cli.py domains
  python scripts/cli.py domains --info 01-core
  python scripts/cli.py modules
  python scripts/cli.py agents
  python scripts/cli.py stats
        """
    )
    
    parser.add_argument("--no-banner", action="store_true", help="Disable banner display")
    
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
    
    # Domains command
    domains_parser = subparsers.add_parser("domains", help="List and info about domains")
    domains_parser.add_argument("--info", help="Show info for specific domain")
    
    # Modules command
    modules_parser = subparsers.add_parser("modules", help="List and info about modules")
    modules_parser.add_argument("--info", help="Show info for specific module")
    
    # Agents command
    agents_parser = subparsers.add_parser("agents", help="List and info about agents")
    agents_parser.add_argument("--info", help="Show info for specific agent")
    
    # Stats command
    subparsers.add_parser("stats", help="Show framework statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        if not args.no_banner:
            print_banner()
        parser.print_help()
        sys.exit(1)
    
    if not args.no_banner:
        print_banner()
    
    commands = {
        "check": cmd_check,
        "validate": cmd_validate,
        "report": cmd_report,
        "export": cmd_export,
        "install": cmd_install,
        "list": cmd_list,
        "domains": cmd_domains,
        "modules": cmd_modules,
        "agents": cmd_agents,
        "stats": cmd_stats,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
