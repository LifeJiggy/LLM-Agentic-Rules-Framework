#!/usr/bin/env python3
"""Rule inventory, catalog, coverage, and export tooling for the framework."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
import sys


REQUIRED_DOMAIN_FILES = [
    "fundamentals.md",
    "best-practices.md",
    "anti-patterns.md",
    "checklist.md",
    "examples.md",
    "troubleshooting.md",
    "advanced.md",
]


REQUIRED_DOMAINS = [
    "01-core",
    "02-security",
    "03-development",
    "04-data",
    "05-integration",
    "06-operations",
    "07-testing",
    "08-documentation",
    "09-performance",
    "10-compliance",
]


REQUIRED_SECTIONS = {
    "fundamentals.md": ["Overview"],
    "best-practices.md": ["Overview"],
    "anti-patterns.md": ["Overview"],
    "checklist.md": ["Overview"],
    "examples.md": ["Overview"],
    "troubleshooting.md": ["Overview"],
    "advanced.md": ["Overview"],
}


PRIORITY_PATTERN = re.compile(r"\bP[0-3]\b")
CHECKBOX_PATTERN = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.+)$")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")


@dataclass
class RuleFile:
    domain: str
    file: str
    path: str
    title: str
    lines: int
    headings: list[str]
    checklist_items: int
    priority_markers: list[str]
    links: list[str]


@dataclass
class RuleReport:
    domains: int
    files: int
    total_lines: int
    failures: list[str]
    warnings: list[str]
    inventory: list[RuleFile]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise RuntimeError(f"Unable to read {path}: {error}") from error


def parse_file(root: Path, domain: str, file_path: Path) -> RuleFile:
    text = read_text(file_path)
    lines = text.splitlines()
    headings = [match.group(2).strip() for line in lines if (match := HEADING_PATTERN.match(line))]
    title = headings[0] if headings else ""
    priorities = sorted(set(PRIORITY_PATTERN.findall(text)))
    link_text = markdown_without_code(text)
    links = [match.group(1).strip() for match in LINK_PATTERN.finditer(link_text)]
    checklist_items = sum(1 for line in lines if CHECKBOX_PATTERN.match(line))
    return RuleFile(
        domain=domain,
        file=file_path.name,
        path=file_path.relative_to(root).as_posix(),
        title=title,
        lines=len(lines),
        headings=headings,
        checklist_items=checklist_items,
        priority_markers=priorities,
        links=links,
    )


def markdown_without_code(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lines.append(INLINE_CODE_PATTERN.sub("", line))
    return "\n".join(lines)


def collect(root: Path, strict_sections: bool = False) -> RuleReport:
    failures: list[str] = []
    warnings: list[str] = []
    inventory: list[RuleFile] = []

    domains_root = root / "domains"
    if not domains_root.is_dir():
        failures.append("Missing domains directory")
        return RuleReport(0, 0, 0, failures, warnings, inventory)

    for domain in REQUIRED_DOMAINS:
        domain_path = domains_root / domain
        if not domain_path.is_dir():
            failures.append(f"Missing domain: {domain}")
            continue

        for filename in REQUIRED_DOMAIN_FILES:
            file_path = domain_path / filename
            if not file_path.is_file():
                failures.append(f"Missing file: domains/{domain}/{filename}")
                continue

            item = parse_file(root, domain, file_path)
            inventory.append(item)

            if item.lines < 20:
                warnings.append(f"Thin file: {item.path} has {item.lines} lines; expected at least 20")

            if not item.title:
                warnings.append(f"Missing title heading: {item.path}")

            required_sections = REQUIRED_SECTIONS.get(filename, [])
            missing_sections = [section for section in required_sections if section not in item.headings]
            if missing_sections:
                message = f"Missing required sections in {item.path}: {', '.join(missing_sections)}"
                if strict_sections:
                    failures.append(message)
                else:
                    warnings.append(message)

    return RuleReport(
        domains=len({item.domain for item in inventory}),
        files=len(inventory),
        total_lines=sum(item.lines for item in inventory),
        failures=failures,
        warnings=warnings,
        inventory=inventory,
    )


def validate_links(root: Path, report: RuleReport) -> list[str]:
    failures: list[str] = []
    known_anchors: dict[str, set[str]] = {}
    for item in report.inventory:
        known_anchors[item.path] = {slugify_heading(heading) for heading in item.headings}
    for item in report.inventory:
        source = root / item.path
        for link in item.links:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_text = link.split("#", 1)[0]
            if not target_text:
                continue
            target = (source.parent / target_text).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                failures.append(f"Link escapes repository: {item.path} -> {link}")
                continue
            if not target.exists():
                failures.append(f"Broken local link: {item.path} -> {link}")
                continue
            if "#" in link and target.is_file():
                anchor = link.split("#", 1)[1].strip()
                if anchor:
                    target_relative = target.relative_to(root).as_posix()
                    anchors = known_anchors.get(target_relative)
                    if anchors is None:
                        headings = [
                            match.group(2).strip()
                            for line in read_text(target).splitlines()
                            if (match := HEADING_PATTERN.match(line))
                        ]
                        anchors = {slugify_heading(heading) for heading in headings}
                        known_anchors[target_relative] = anchors
                    if anchor not in anchors:
                        failures.append(f"Broken local anchor: {item.path} -> {link}")
    return failures


def slugify_heading(heading: str) -> str:
    value = heading.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    return value


def summary_by_domain(report: RuleReport) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for domain in REQUIRED_DOMAINS:
        items = [item for item in report.inventory if item.domain == domain]
        result[domain] = {
            "files": len(items),
            "lines": sum(item.lines for item in items),
            "checklist_items": sum(item.checklist_items for item in items),
            "files_with_priority_markers": sum(1 for item in items if item.priority_markers),
        }
    return result


def print_summary(report: RuleReport) -> None:
    print("Rule inventory")
    print("==============")
    print(f"Domains: {report.domains}")
    print(f"Files: {report.files}")
    print(f"Total lines: {report.total_lines}")
    print()
    print("| Domain | Files | Lines | Checklist Items | Files With Priority Markers |")
    print("|--------|-------|-------|-----------------|-----------------------------|")
    for domain, values in summary_by_domain(report).items():
        print(
            f"| {domain} | {values['files']} | {values['lines']} | "
            f"{values['checklist_items']} | {values['files_with_priority_markers']} |"
        )


def write_json(path: Path, report: RuleReport) -> None:
    ensure_output_file(path)
    data = asdict(report)
    data["by_domain"] = summary_by_domain(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_catalog(path: Path, report: RuleReport) -> None:
    ensure_output_file(path)
    catalog = {
        "schema": "llm-agentic-rules/catalog/v1",
        "domains": REQUIRED_DOMAINS,
        "required_files": REQUIRED_DOMAIN_FILES,
        "rules": [asdict(item) for item in report.inventory],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")


def write_checklist_export(path: Path, root: Path, report: RuleReport) -> None:
    ensure_output_file(path)
    lines = ["# Exported Framework Checklists", ""]
    for item in report.inventory:
        if item.file != "checklist.md":
            continue
        source = root / item.path
        checklist_lines = [
            line for line in read_text(source).splitlines() if CHECKBOX_PATTERN.match(line)
        ]
        lines.extend([f"## {item.domain}", "", f"Source: `{item.path}`", ""])
        lines.extend(checklist_lines if checklist_lines else ["No checklist items found."])
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_coverage(path: Path, report: RuleReport) -> None:
    ensure_output_file(path)
    lines = [
        "# Domain Coverage Report",
        "",
        "| Domain | Files | Lines | Checklist Items | Files With Priority Markers |",
        "|--------|-------|-------|-----------------|-----------------------------|",
    ]
    for domain, values in summary_by_domain(report).items():
        lines.append(
            f"| {domain} | {values['files']} | {values['lines']} | "
            f"{values['checklist_items']} | {values['files_with_priority_markers']} |"
        )
    lines.extend(
        [
            "",
            "## Warnings",
            "",
            *(f"- {warning}" for warning in report.warnings),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def ensure_output_file(path: Path) -> None:
    if path.exists() and path.is_dir():
        raise RuntimeError(f"Output path is a directory, expected file: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--summary", action="store_true", help="Print inventory summary")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as failures")
    parser.add_argument("--strict-sections", action="store_true", help="Fail when required sections are missing")
    parser.add_argument("--validate-links", action="store_true", help="Validate local Markdown links")
    parser.add_argument("--json", dest="json_output", help="Write full JSON report")
    parser.add_argument("--catalog", help="Write machine-readable rule catalog JSON")
    parser.add_argument("--export-checklists", help="Write combined checklist Markdown")
    parser.add_argument("--coverage", help="Write domain coverage Markdown report")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = collect(root, strict_sections=args.strict_sections)

    if args.validate_links:
        report.failures.extend(validate_links(root, report))

    if args.summary:
        print_summary(report)

    if args.json_output:
        write_json(Path(args.json_output), report)

    if args.catalog:
        write_catalog(Path(args.catalog), report)

    if args.export_checklists:
        write_checklist_export(Path(args.export_checklists), root, report)

    if args.coverage:
        write_coverage(Path(args.coverage), report)

    active_failures = list(report.failures)
    if args.strict:
        active_failures.extend(report.warnings)

    if active_failures:
        print("\nValidation failed:", file=sys.stderr)
        for failure in active_failures:
            print(f" - {failure}", file=sys.stderr)
        return 1

    if not args.summary:
        print("Rule inventory passed.")
    elif report.warnings:
        print("\nWarnings:")
        for warning in report.warnings:
            print(f" - {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
