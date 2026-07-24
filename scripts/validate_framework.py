#!/usr/bin/env python3
"""
Framework Structure Validator

Validates the complete framework structure including domains, modules,
agents, skills, memory, and storage files.

Usage:
    python scripts/validate_framework.py [options]

Options:
    --verbose       Show detailed output
    --json          Output results as JSON
    --fix           Attempt to fix issues automatically
    --help          Show this help message
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).parent.parent


@dataclass
class ValidationResult:
    component: str
    status: str
    message: str
    details: list[str]


class FrameworkValidator:
    """Validates the complete framework structure."""
    
    def __init__(self, root: Path, verbose: bool = False):
        self.root = root
        self.verbose = verbose
        self.results: list[ValidationResult] = []
    
    def validate_domains(self) -> ValidationResult:
        """Validate domain structure."""
        domains_path = self.root / "domains"
        details = []
        
        required_domains = [
            "01-core", "02-security", "03-development", "04-data",
            "05-integration", "06-operations", "07-testing",
            "08-documentation", "09-performance", "10-compliance"
        ]
        
        required_files = [
            "fundamentals.md", "best-practices.md", "anti-patterns.md",
            "checklist.md", "examples.md", "troubleshooting.md", "advanced.md"
        ]
        
        missing_domains = []
        missing_files = []
        
        for domain in required_domains:
            domain_path = domains_path / domain
            if not domain_path.exists():
                missing_domains.append(domain)
                continue
            
            for file in required_files:
                if not (domain_path / file).exists():
                    missing_files.append(f"{domain}/{file}")
        
        if missing_domains:
            details.append(f"Missing domains: {', '.join(missing_domains)}")
        if missing_files:
            details.append(f"Missing files: {', '.join(missing_files)}")
        
        status = "pass" if not missing_domains and not missing_files else "fail"
        message = f"Domains: {len(required_domains) - len(missing_domains)}/{len(required_domains)} complete"
        
        return ValidationResult("domains", status, message, details)
    
    def validate_modules(self) -> ValidationResult:
        """Validate module structure."""
        details = []
        
        required_modules = [
            "evaluation", "loop", "tools", "incident-response",
            "deployment", "monitoring", "cost-management",
            "vendor-management", "governance"
        ]
        
        module_files = [
            "-fundamentals.md", "-best-practices.md", "-anti-patterns.md",
            "-checklist.md", "-examples.md", "-troubleshooting.md", "-advanced.md"
        ]
        
        missing_modules = []
        missing_files = []
        
        for module in required_modules:
            module_path = self.root / module
            if not module_path.exists():
                missing_modules.append(module)
                continue
            
            for suffix in module_files:
                expected_file = f"{module}{suffix}"
                if not (module_path / expected_file).exists():
                    missing_files.append(f"{module}/{expected_file}")
        
        if missing_modules:
            details.append(f"Missing modules: {', '.join(missing_modules)}")
        if missing_files:
            details.append(f"Missing files: {', '.join(missing_files)}")
        
        status = "pass" if not missing_modules and not missing_files else "fail"
        message = f"Modules: {len(required_modules) - len(missing_modules)}/{len(required_modules)} complete"
        
        return ValidationResult("modules", status, message, details)
    
    def validate_agents(self) -> ValidationResult:
        """Validate agent structure."""
        agents_path = self.root / "agents"
        details = []
        
        required_agents = [
            "rules-architect.md", "rules-implementer.md", "rules-reviewer.md",
            "rules-release-gate.md", "rules-eval.md", "rules-compliance-auditor.md",
            "rules-data-steward.md", "rules-enforcer.md", "rules-documentation.md",
            "rules-tracker.md", "rules-orchestrator.md", "rules-security.md"
        ]
        
        missing_agents = []
        
        for agent in required_agents:
            if not (agents_path / agent).exists():
                missing_agents.append(agent)
        
        if missing_agents:
            details.append(f"Missing agents: {', '.join(missing_agents)}")
        
        status = "pass" if not missing_agents else "fail"
        message = f"Agents: {len(required_agents) - len(missing_agents)}/{len(required_agents)} complete"
        
        return ValidationResult("agents", status, message, details)
    
    def validate_skills(self) -> ValidationResult:
        """Validate skill structure."""
        skills_path = self.root / "skills"
        details = []
        
        required_skills = [
            "llm-agentic-rules/evaluation-workflows.md",
            "llm-agentic-rules/loop-patterns.md",
            "llm-agentic-rules/domain-routing-guide.md",
            "llm-agentic-rules/review-gates-criteria.md",
            "llm-agentic-rules/compliance-evidence-standards.md",
            "system/tool-integration.md",
            "system/performance-optimization.md",
            "system/deployment-safety.md",
            "system/observability-standards.md",
            "system/recovery-playbook.md"
        ]
        
        missing_skills = []
        
        for skill in required_skills:
            if not (skills_path / skill).exists():
                missing_skills.append(skill)
        
        if missing_skills:
            details.append(f"Missing skills: {', '.join(missing_skills)}")
        
        status = "pass" if not missing_skills else "fail"
        message = f"Skills: {len(required_skills) - len(missing_skills)}/{len(required_skills)} complete"
        
        return ValidationResult("skills", status, message, details)
    
    def validate_memory(self) -> ValidationResult:
        """Validate memory structure."""
        memory_path = self.root / "memory"
        details = []
        
        required_memory = [
            "framework-context.md", "agent-catalog.md", "domain-reference.md",
            "integration-patterns.md", "decision-matrix.md",
            "core-rules-summary.md", "security-rules-summary.md",
            "data-rules-summary.md", "testing-rules-summary.md",
            "compliance-rules-summary.md"
        ]
        
        missing_memory = []
        
        for mem in required_memory:
            if not (memory_path / mem).exists():
                missing_memory.append(mem)
        
        if missing_memory:
            details.append(f"Missing memory files: {', '.join(missing_memory)}")
        
        status = "pass" if not missing_memory else "fail"
        message = f"Memory: {len(required_memory) - len(missing_memory)}/{len(required_memory)} complete"
        
        return ValidationResult("memory", status, message, details)
    
    def validate_storage(self) -> ValidationResult:
        """Validate storage structure."""
        storage_path = self.root / "storage"
        details = []
        
        required_storage = [
            "rule-templates.md", "checklist-templates.md",
            "evaluation-templates.md", "incident-templates.md",
            "architecture-templates.md", "core-domain-rules.md",
            "security-domain-rules.md", "data-domain-rules.md",
            "testing-domain-rules.md", "compliance-domain-rules.md"
        ]
        
        missing_storage = []
        
        for store in required_storage:
            if not (storage_path / store).exists():
                missing_storage.append(store)
        
        if missing_storage:
            details.append(f"Missing storage files: {', '.join(missing_storage)}")
        
        status = "pass" if not missing_storage else "fail"
        message = f"Storage: {len(required_storage) - len(missing_storage)}/{len(required_storage)} complete"
        
        return ValidationResult("storage", status, message, details)
    
    def validate_readmes(self) -> ValidationResult:
        """Validate README files."""
        details = []
        
        required_readmes = [
            "README.md",
            "evaluation/README.md",
            "loop/README.md",
            "tools/README.md",
            "skills/README.md",
            "skills/llm-agentic-rules/README.md",
            "skills/system/README.md",
            "memory/README.md",
            "storage/README.md",
            "agents/README.md"
        ]
        
        missing_readmes = []
        
        for readme in required_readmes:
            if not (self.root / readme).exists():
                missing_readmes.append(readme)
        
        if missing_readmes:
            details.append(f"Missing READMEs: {', '.join(missing_readmes)}")
        
        status = "pass" if not missing_readmes else "warn"
        message = f"READMEs: {len(required_readmes) - len(missing_readmes)}/{len(required_readmes)} complete"
        
        return ValidationResult("readmes", status, message, details)
    
    def validate_all(self) -> list[ValidationResult]:
        """Run all validations."""
        self.results = [
            self.validate_domains(),
            self.validate_modules(),
            self.validate_agents(),
            self.validate_skills(),
            self.validate_memory(),
            self.validate_storage(),
            self.validate_readmes(),
        ]
        return self.results
    
    def print_results(self):
        """Print validation results."""
        print("\nFramework Validation Results")
        print("=" * 60)
        
        for result in self.results:
            status_symbol = "✓" if result.status == "pass" else "⚠" if result.status == "warn" else "✗"
            print(f"\n{status_symbol} {result.component}: {result.message}")
            
            if self.verbose and result.details:
                for detail in result.details:
                    print(f"  - {detail}")
        
        print("\n" + "=" * 60)
        
        passed = sum(1 for r in self.results if r.status == "pass")
        warned = sum(1 for r in self.results if r.status == "warn")
        failed = sum(1 for r in self.results if r.status == "fail")
        
        print(f"Summary: {passed} passed, {warned} warnings, {failed} failed")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Framework Structure Validator")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
    
    args = parser.parse_args()
    
    validator = FrameworkValidator(FRAMEWORK_ROOT, verbose=args.verbose)
    results = validator.validate_all()
    
    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        validator.print_results()
    
    failed = sum(1 for r in results if r.status == "fail")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
