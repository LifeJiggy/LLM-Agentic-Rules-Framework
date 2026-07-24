#!/usr/bin/env python3
"""
Framework Report Generator

Generates comprehensive reports about the framework structure,
coverage, and metrics.

Usage:
    python scripts/generate_report.py [options]

Options:
    --type TYPE     Report type: summary, coverage, metrics, full
    --output FILE   Output file path
    --format FORMAT Output format: text, json, markdown
    --help          Show this help message
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

FRAMEWORK_ROOT = Path(__file__).parent.parent


@dataclass
class FileStats:
    path: str
    lines: int
    size_bytes: int


@dataclass
class ComponentStats:
    name: str
    file_count: int
    total_lines: int
    total_size: int
    files: list[FileStats]


@dataclass
class FrameworkReport:
    timestamp: str
    version: str
    components: list[ComponentStats]
    total_files: int
    total_lines: int
    total_size: int


class ReportGenerator:
    """Generates framework reports."""
    
    def __init__(self, root: Path):
        self.root = root
    
    def count_file_lines(self, path: Path) -> int:
        """Count lines in a file."""
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0
    
    def get_file_stats(self, path: Path) -> FileStats:
        """Get stats for a single file."""
        return FileStats(
            path=str(path.relative_to(self.root)),
            lines=self.count_file_lines(path),
            size_bytes=path.stat().st_size if path.exists() else 0
        )
    
    def get_component_stats(self, name: str, path: Path, pattern: str = "*.md") -> ComponentStats:
        """Get stats for a component directory."""
        files = []
        
        if path.exists():
            for file_path in sorted(path.rglob(pattern)):
                files.append(self.get_file_stats(file_path))
        
        return ComponentStats(
            name=name,
            file_count=len(files),
            total_lines=sum(f.lines for f in files),
            total_size=sum(f.size_bytes for f in files),
            files=files
        )
    
    def generate_summary_report(self) -> FrameworkReport:
        """Generate summary report."""
        components = [
            ("Domains", self.root / "domains"),
            ("Evaluation", self.root / "evaluation"),
            ("Loop", self.root / "loop"),
            ("Tools", self.root / "tools"),
            ("Incident Response", self.root / "incident-response"),
            ("Deployment", self.root / "deployment"),
            ("Monitoring", self.root / "monitoring"),
            ("Cost Management", self.root / "cost-management"),
            ("Vendor Management", self.root / "vendor-management"),
            ("Governance", self.root / "governance"),
            ("Agents", self.root / "agents"),
            ("Skills", self.root / "skills"),
            ("Memory", self.root / "memory"),
            ("Storage", self.root / "storage"),
            ("Documentation", self.root / "docs"),
        ]
        
        component_stats = []
        for name, path in components:
            component_stats.append(self.get_component_stats(name, path))
        
        total_files = sum(c.file_count for c in component_stats)
        total_lines = sum(c.total_lines for c in component_stats)
        total_size = sum(c.total_size for c in component_stats)
        
        return FrameworkReport(
            timestamp=datetime.now().isoformat(),
            version="2.0.0",
            components=component_stats,
            total_files=total_files,
            total_lines=total_lines,
            total_size=total_size
        )
    
    def print_text_report(self, report: FrameworkReport):
        """Print text format report."""
        print("\nLLM & Agentic Rules Framework Report")
        print("=" * 60)
        print(f"Generated: {report.timestamp}")
        print(f"Version: {report.version}")
        print("=" * 60)
        
        print("\nComponent Summary:")
        print("-" * 60)
        print(f"{'Component':<25} {'Files':<10} {'Lines':<12} {'Size':<12}")
        print("-" * 60)
        
        for comp in report.components:
            size_kb = comp.total_size / 1024
            print(f"{comp.name:<25} {comp.file_count:<10} {comp.total_lines:<12} {size_kb:<10.1f} KB")
        
        print("-" * 60)
        total_size_kb = report.total_size / 1024
        print(f"{'TOTAL':<25} {report.total_files:<10} {report.total_lines:<12} {total_size_kb:<10.1f} KB")
        print("=" * 60)
    
    def print_json_report(self, report: FrameworkReport):
        """Print JSON format report."""
        print(json.dumps(asdict(report), indent=2))
    
    def print_markdown_report(self, report: FrameworkReport):
        """Print markdown format report."""
        print("# Framework Report")
        print(f"\nGenerated: {report.timestamp}")
        print(f"Version: {report.version}\n")
        
        print("## Component Summary\n")
        print("| Component | Files | Lines | Size |")
        print("|-----------|-------|-------|------|")
        
        for comp in report.components:
            size_kb = comp.total_size / 1024
            print(f"| {comp.name} | {comp.file_count} | {comp.total_lines} | {size_kb:.1f} KB |")
        
        total_size_kb = report.total_size / 1024
        print(f"| **TOTAL** | **{report.total_files}** | **{report.total_lines}** | **{total_size_kb:.1f} KB** |")
    
    def save_report(self, report: FrameworkReport, output_path: Path, format: str):
        """Save report to file."""
        import io
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        if format == "json":
            self.print_json_report(report)
        elif format == "markdown":
            self.print_markdown_report(report)
        else:
            self.print_text_report(report)
        
        sys.stdout = old_stdout
        
        # Write to file
        output_path.write_text(buffer.getvalue(), encoding='utf-8')
        print(f"\nReport saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Framework Report Generator")
    parser.add_argument("--type", choices=["summary", "full"], default="summary", help="Report type")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    generator = ReportGenerator(FRAMEWORK_ROOT)
    report = generator.generate_summary_report()
    
    if args.output:
        output_path = Path(args.output)
        generator.save_report(report, output_path, args.format)
    else:
        if args.format == "json":
            generator.print_json_report(report)
        elif args.format == "markdown":
            generator.print_markdown_report(report)
        else:
            generator.print_text_report(report)


if __name__ == "__main__":
    main()
