#!/usr/bin/env python3
"""
Checklist Exporter

Exports checklists from all domains and modules into a single consolidated file.

Usage:
    python scripts/export_checklists.py [options]

Options:
    --output FILE   Output file path
    --format FORMAT Output format: markdown, json
    --filter FILTER Filter by priority: P0, P1, P2, P3
    --help          Show this help message
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).parent.parent

CHECKBOX_PATTERN = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.+)$")
PRIORITY_PATTERN = re.compile(r"\bP[0-3]\b")


@dataclass
class ChecklistItem:
    text: str
    checked: bool
    priority: str | None
    source_file: str
    source_domain: str


@dataclass
class ChecklistSection:
    domain: str
    file: str
    items: list[ChecklistItem]


class ChecklistExporter:
    """Exports checklists from framework files."""
    
    def __init__(self, root: Path):
        self.root = root
    
    def extract_checklist_items(self, file_path: Path, domain: str) -> list[ChecklistItem]:
        """Extract checklist items from a markdown file."""
        items = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    match = CHECKBOX_PATTERN.match(line)
                    if match:
                        text = match.group(1).strip()
                        checked = line.strip().startswith("- [x]") or line.strip().startswith("- [X]")
                        
                        # Extract priority
                        priority_match = PRIORITY_PATTERN.search(text)
                        priority = priority_match.group(0) if priority_match else None
                        
                        items.append(ChecklistItem(
                            text=text,
                            checked=checked,
                            priority=priority,
                            source_file=str(file_path.relative_to(self.root)),
                            source_domain=domain
                        ))
        except Exception as e:
            print(f"Warning: Error reading {file_path}: {e}", file=sys.stderr)
        
        return items
    
    def collect_checklists(self, filter_priority: str | None = None) -> list[ChecklistSection]:
        """Collect all checklists from the framework."""
        sections = []
        
        # Domain checklists
        domains_path = self.root / "domains"
        if domains_path.exists():
            for domain_dir in sorted(domains_path.iterdir()):
                if domain_dir.is_dir():
                    checklist_path = domain_dir / "checklist.md"
                    if checklist_path.exists():
                        items = self.extract_checklist_items(checklist_path, domain_dir.name)
                        if filter_priority:
                            items = [i for i in items if i.priority == filter_priority]
                        if items:
                            sections.append(ChecklistSection(
                                domain=domain_dir.name,
                                file="checklist.md",
                                items=items
                            ))
        
        # Module checklists
        modules = [
            "evaluation", "loop", "tools", "incident-response",
            "deployment", "monitoring", "cost-management",
            "vendor-management", "governance"
        ]
        
        for module in modules:
            module_path = self.root / module
            if module_path.exists():
                checklist_file = f"{module}-checklist.md"
                checklist_path = module_path / checklist_file
                if checklist_path.exists():
                    items = self.extract_checklist_items(checklist_path, module)
                    if filter_priority:
                        items = [i for i in items if i.priority == filter_priority]
                    if items:
                        sections.append(ChecklistSection(
                            domain=module,
                            file=checklist_file,
                            items=items
                        ))
        
        return sections
    
    def export_markdown(self, sections: list[ChecklistSection], output_path: Path):
        """Export checklists as markdown."""
        lines = [
            "# Consolidated Checklists",
            "",
            "This document contains all checklists from the LLM & Agentic Rules Framework.",
            "",
            "---",
            "",
        ]
        
        for section in sections:
            lines.append(f"## {section.domain}")
            lines.append("")
            lines.append(f"*Source: {section.file}*")
            lines.append("")
            
            for item in section.items:
                checkbox = "[x]" if item.checked else "[ ]"
                lines.append(f"- {checkbox} {item.text}")
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Summary
        total_items = sum(len(s.items) for s in sections)
        checked_items = sum(sum(1 for i in s.items if i.checked) for s in sections)
        
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total checklist items**: {total_items}")
        lines.append(f"- **Checked items**: {checked_items}")
        lines.append(f"- **Completion rate**: {checked_items/total_items*100:.1f}%")
        lines.append("")
        
        output_path.write_text("\n".join(lines), encoding='utf-8')
    
    def export_json(self, sections: list[ChecklistSection], output_path: Path):
        """Export checklists as JSON."""
        data = {
            "sections": [asdict(s) for s in sections],
            "summary": {
                "total_sections": len(sections),
                "total_items": sum(len(s.items) for s in sections),
                "checked_items": sum(sum(1 for i in s.items if i.checked) for s in sections),
            }
        }
        
        output_path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Checklist Exporter")
    parser.add_argument("--output", type=str, default="build/checklists.md", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--filter", choices=["P0", "P1", "P2", "P3"], help="Filter by priority")
    
    args = parser.parse_args()
    
    exporter = ChecklistExporter(FRAMEWORK_ROOT)
    sections = exporter.collect_checklists(filter_priority=args.filter)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == "json":
        exporter.export_json(sections, output_path)
    else:
        exporter.export_markdown(sections, output_path)
    
    print(f"Exported {len(sections)} sections to {output_path}")
    
    total_items = sum(len(s.items) for s in sections)
    print(f"Total checklist items: {total_items}")


if __name__ == "__main__":
    main()
