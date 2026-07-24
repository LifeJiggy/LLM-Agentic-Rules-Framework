#!/usr/bin/env python3
"""
LLM & Agentic Rules Framework - Setup Script

This script sets up the framework environment, installs dependencies,
and configures the framework for use.

Usage:
    python scripts/setup.py [options]

Options:
    --check         Check system requirements
    --install       Install dependencies
    --validate      Validate framework structure
    --configure     Configure framework settings
    --all           Run all setup steps
    --help          Show this help message
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Framework metadata
FRAMEWORK_NAME = "LLM & Agentic Rules Framework"
FRAMEWORK_VERSION = "2.0.0"
FRAMEWORK_ROOT = Path(__file__).parent.parent

# Required Python version
REQUIRED_PYTHON = (3, 9)

# Required directories
REQUIRED_DIRECTORIES = [
    "domains",
    "agents",
    "skills",
    "memory",
    "storage",
    "evaluation",
    "loop",
    "tools",
    "incident-response",
    "deployment",
    "monitoring",
    "cost-management",
    "vendor-management",
    "governance",
    "docs",
    "scripts",
    "adapters",
    "assets",
    "commands",
    "examples",
]

# Required domain files
REQUIRED_DOMAIN_FILES = [
    "fundamentals.md",
    "best-practices.md",
    "anti-patterns.md",
    "checklist.md",
    "examples.md",
    "troubleshooting.md",
    "advanced.md",
]

# Required domains
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

# Required root files
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "goal.md",
    "purpose.md",
    "brain.md",
    "scope.md",
    "standardized-rules.md",
    "Troubleshooting.md",
    "LLM-Agentic-Rules.md",
]


class SetupManager:
    """Manages framework setup and configuration."""
    
    def __init__(self, root: Path):
        self.root = root
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.success: list[str] = []
    
    def check_python_version(self) -> bool:
        """Check if Python version meets requirements."""
        current = sys.version_info[:2]
        required = REQUIRED_PYTHON
        
        if current >= required:
            self.success.append(f"Python {current[0]}.{current[1]} meets requirements")
            return True
        else:
            self.errors.append(
                f"Python {current[0]}.{current[1]} does not meet requirements. "
                f"Requires Python {required[0]}.{required[1]} or higher."
            )
            return False
    
    def check_directories(self) -> bool:
        """Check if required directories exist."""
        all_exist = True
        
        for directory in REQUIRED_DIRECTORIES:
            path = self.root / directory
            if path.exists():
                self.success.append(f"Directory exists: {directory}")
            else:
                self.errors.append(f"Missing directory: {directory}")
                all_exist = False
        
        return all_exist
    
    def check_domain_files(self) -> bool:
        """Check if all domain files exist."""
        all_exist = True
        domains_path = self.root / "domains"
        
        if not domains_path.exists():
            self.errors.append("Domains directory not found")
            return False
        
        for domain in REQUIRED_DOMAINS:
            domain_path = domains_path / domain
            if not domain_path.exists():
                self.errors.append(f"Missing domain: {domain}")
                all_exist = False
                continue
            
            for file in REQUIRED_DOMAIN_FILES:
                file_path = domain_path / file
                if file_path.exists():
                    self.success.append(f"Domain file exists: {domain}/{file}")
                else:
                    self.errors.append(f"Missing file: {domain}/{file}")
                    all_exist = False
        
        return all_exist
    
    def check_root_files(self) -> bool:
        """Check if required root files exist."""
        all_exist = True
        
        for file in REQUIRED_ROOT_FILES:
            path = self.root / file
            if path.exists():
                self.success.append(f"Root file exists: {file}")
            else:
                self.warnings.append(f"Missing root file: {file}")
        
        return all_exist
    
    def check_scripts(self) -> bool:
        """Check if required scripts exist."""
        scripts = [
            "check_rules.py",
            "install_agent_adapters.py",
            "validate-framework.ps1",
            "setup.py",
            "setup.sh",
            "setup.ps1",
        ]
        
        all_exist = True
        scripts_path = self.root / "scripts"
        
        for script in scripts:
            path = scripts_path / script
            if path.exists():
                self.success.append(f"Script exists: {script}")
            else:
                self.warnings.append(f"Missing script: {script}")
        
        return all_exist
    
    def run_check(self) -> bool:
        """Run all checks."""
        print(f"\n{FRAMEWORK_NAME} v{FRAMEWORK_VERSION} - System Check")
        print("=" * 60)
        
        results = [
            self.check_python_version(),
            self.check_directories(),
            self.check_domain_files(),
            self.check_root_files(),
            self.check_scripts(),
        ]
        
        self.print_results()
        return all(results)
    
    def install_dependencies(self) -> bool:
        """Install required dependencies."""
        print(f"\n{FRAMEWORK_NAME} - Installing Dependencies")
        print("=" * 60)
        
        try:
            # Check if pip is available
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                check=True,
                capture_output=True,
            )
            
            # Install any requirements if they exist
            requirements_file = self.root / "requirements.txt"
            if requirements_file.exists():
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                    check=True,
                )
                self.success.append("Dependencies installed from requirements.txt")
            else:
                self.success.append("No requirements.txt found, skipping dependency installation")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install dependencies: {e}")
            return False
        except FileNotFoundError:
            self.errors.append("pip not found. Please install Python with pip.")
            return False
    
    def validate_framework(self) -> bool:
        """Validate framework structure."""
        print(f"\n{FRAMEWORK_NAME} - Validating Framework")
        print("=" * 60)
        
        try:
            # Run the check_rules.py script
            result = subprocess.run(
                [sys.executable, str(self.root / "scripts" / "check_rules.py"), "--summary"],
                capture_output=True,
                text=True,
            )
            
            if result.returncode == 0:
                self.success.append("Framework validation passed")
                print(result.stdout)
                return True
            else:
                self.warnings.append("Framework validation completed with warnings")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return True
                
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Framework validation failed: {e}")
            return False
        except FileNotFoundError:
            self.warnings.append("check_rules.py not found, skipping validation")
            return True
    
    def configure_framework(self) -> bool:
        """Configure framework settings."""
        print(f"\n{FRAMEWORK_NAME} - Configuring Framework")
        print("=" * 60)
        
        # Create configuration file if it doesn't exist
        config_file = self.root / "config.json"
        
        if not config_file.exists():
            config = {
                "name": FRAMEWORK_NAME,
                "version": FRAMEWORK_VERSION,
                "framework_root": str(self.root),
                "domains": REQUIRED_DOMAINS,
                "settings": {
                    "auto_validate": True,
                    "strict_mode": False,
                    "log_level": "INFO",
                },
            }
            
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)
            
            self.success.append("Configuration file created")
        else:
            self.success.append("Configuration file already exists")
        
        return True
    
    def run_all(self) -> bool:
        """Run all setup steps."""
        print(f"\n{FRAMEWORK_NAME} v{FRAMEWORK_VERSION} - Full Setup")
        print("=" * 60)
        
        steps = [
            ("Check System", self.run_check),
            ("Install Dependencies", self.install_dependencies),
            ("Validate Framework", self.validate_framework),
            ("Configure Framework", self.configure_framework),
        ]
        
        results = []
        for name, func in steps:
            print(f"\n--- {name} ---")
            result = func()
            results.append(result)
        
        self.print_results()
        return all(results)
    
    def print_results(self):
        """Print setup results."""
        print("\n" + "=" * 60)
        print("Results")
        print("=" * 60)
        
        if self.success:
            print(f"\n✓ Success ({len(self.success)}):")
            for item in self.success:
                print(f"  + {item}")
        
        if self.warnings:
            print(f"\n⚠ Warnings ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"  ! {item}")
        
        if self.errors:
            print(f"\n✗ Errors ({len(self.errors)}):")
            for item in self.errors:
                print(f"  - {item}")
        
        print("\n" + "=" * 60)
        
        if not self.errors:
            print("Setup completed successfully!")
        else:
            print("Setup completed with errors. Please fix the issues above.")
        
        print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=f"{FRAMEWORK_NAME} Setup Script"
    )
    parser.add_argument("--check", action="store_true", help="Check system requirements")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--validate", action="store_true", help="Validate framework structure")
    parser.add_argument("--configure", action="store_true", help="Configure framework settings")
    parser.add_argument("--all", action="store_true", help="Run all setup steps")
    
    args = parser.parse_args()
    
    manager = SetupManager(FRAMEWORK_ROOT)
    
    if args.all or not any([args.check, args.install, args.validate, args.configure]):
        success = manager.run_all()
    else:
        success = True
        if args.check:
            success &= manager.run_check()
        if args.install:
            success &= manager.install_dependencies()
        if args.validate:
            success &= manager.validate_framework()
        if args.configure:
            success &= manager.configure_framework()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
