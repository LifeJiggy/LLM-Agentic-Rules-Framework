# Audit Automation and Tooling

Use this guide to automate audits using the LLM & Agentic Rules Framework, including recommended tools, CI/CD integration, and custom automation scripts.

## Automation Philosophy

Automation is essential for maintaining continuous compliance and reducing the manual burden of audits. However, automation should complement, not replace, human judgment. The goal is to automate repetitive, objective checks while preserving human expertise for subjective, context-dependent assessments.

### Automation Principles

**Automate What Can Be Automated**
- Dependency scanning
- Secret detection
- Static code analysis
- Linting and style checks
- Code coverage analysis
- Configuration validation

**Preserve Human Judgment For**
- Architecture and design reviews
- Business logic assessment
- Risk tier determination
- Finding severity classification
- Exception handling and acceptance
- Root cause analysis

**Continuous Over Periodic**
- Integrate checks into CI/CD
- Run on every commit
- Provide immediate feedback
- Enable fast iteration

**Actionable Output**
- Generate structured findings
- Link to evidence automatically
- Assign severity based on rules
- Provide concrete fix suggestions

## Tool Categories

### 1. Dependency Scanning

**Purpose:** Identify vulnerabilities in dependencies.

**Tools:**

**npm audit (Node.js)**
```bash
npm audit --audit-level=high --json > audit/dependency-scan.json
```

**pip-audit (Python)**
```bash
pip-audit --format=json > audit/dependency-scan.json
```

**Snyk**
```bash
snyk test --json > audit/snyk-scan.json
```

**Dependabot (GitHub)**
- Configured in `.github/dependabot.yml`
- Automatically creates PRs for vulnerable dependencies

**OWASP Dependency-Check**
```bash
dependency-check --scan . --format JSON --out audit/dependency-check.json
```

**Automation Integration:**
```yaml
# GitHub Actions example
- name: Dependency Scan
  run: npm audit --audit-level=high --json > audit/dependency-scan.json
- name: Upload Scan Results
  uses: actions/upload-artifact@v3
  with:
    name: dependency-scan
    path: audit/dependency-scan.json
```

### 2. Secret Scanning

**Purpose:** Detect hardcoded secrets, credentials, and sensitive data.

**Tools:**

**gitleaks**
```bash
gitleaks detect --source . --report-path audit/secret-scan.json --report-format json
```

**truffleHog**
```bash
truffleHog --json --regex --entropy=False . > audit/secret-scan.json
```

**git-secrets**
```bash
git secrets --scan-history > audit/secret-scan.json
```

**Automation Integration:**
```yaml
- name: Secret Scan
  uses: gitleaks/gitleaks-action@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 3. Static Code Analysis (SAST)

**Purpose:** Identify security vulnerabilities, code smells, and bugs.

**Tools:**

**Semgrep**
```bash
semgrep --config auto --severity=ERROR --json -o audit/sast-scan.json .
```

**SonarQube**
```bash
sonar-scanner -Dsonar.projectKey=my-project -Dsonar.sources=.
```

**CodeQL (GitHub)**
```bash
codeql database create codeql-db --language=javascript,python
codeql database analyze codeql-db --format=sarif-latest --output=audit/codeql-results.sarif
```

**ESLint (JavaScript/TypeScript)**
```bash
eslint . --format json > audit/eslint-report.json
```

**pylint (Python)**
```bash
pylint src/ --output-format=json > audit/pylint-report.json
```

**golangci-lint (Go)**
```bash
golangci-lint run --out-format=json > audit/golangci-report.json
```

### 4. Code Coverage Analysis

**Purpose:** Measure test coverage and identify untested code.

**Tools:**

**pytest-cov (Python)**
```bash
pytest --cov=src --cov-report=json --cov-report=html
```

**Istanbul/Jest (JavaScript/TypeScript)**
```bash
jest --coverage --coverageReporters=json
```

**JaCoCo (Java)**
```bash
mvn test jacoco:report
```

**Automation Integration:**
```yaml
- name: Test Coverage
  run: npm run test:coverage -- --coverageReporters=json
- name: Coverage Report
  uses: actions/upload-artifact@v3
  with:
    name: coverage-report
    path: coverage/coverage-final.json
```

### 5. Infrastructure Scanning

**Purpose:** Identify security issues in infrastructure as code.

**Tools:**

**Checkov (Terraform, CloudFormation, Kubernetes)**
```bash
checkov -d . --output json > audit/infra-scan.json
```

**tfsec (Terraform)**
```bash
tfsec . --format=json > audit/tfsec-scan.json
```

**kube-score (Kubernetes)**
```bash
kube-score score -o json > audit/kube-score.json
```

**trivy (Container, Kubernetes)**
```bash
trivy fs . --format json > audit/trivy-scan.json
```

### 6. Configuration Validation

**Purpose:** Validate configuration files for syntax and security issues.

**Tools:**

**yamllint**
```bash
yamllint config/ -f json > audit/yaml-lint.json
```

**jsonlint**
```bash
find config/ -name "*.json" -exec jsonlint -q {} \; > audit/json-lint.txt
```

**kubeval (Kubernetes)**
```bash
kubeval -d k8s/ -o json > audit/kubeval.json
```

### 7. License Compliance

**Purpose:** Verify license compliance for dependencies.

**Tools:**

**FOSSA**
```bash
fossa analyze
```

**SCAN (License Checker)**
```bash
npx license-checker --json > audit/licenses.json
```

**LicenseFinder**
```bash
license_finder --json > audit/licenses.json
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: LLM-Agentic-Rules Audit
on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:  # Manual trigger

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          npm install
          pip install -r requirements.txt

      - name: Create Audit Directory
        run: mkdir -p audit

      - name: Dependency Scan
        run: npm audit --audit-level=high --json > audit/dependency-scan.json
        continue-on-error: true

      - name: Secret Scan
        uses: gitleaks/gitleaks-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: SAST Scan
        run: semgrep --config auto --severity=ERROR --json -o audit/sast-scan.json .
        continue-on-error: true

      - name: Lint Check
        run: npm run lint > audit/lint-report.txt 2>&1
        continue-on-error: true

      - name: Test Coverage
        run: npm run test:coverage -- --coverageReporters=json
        continue-on-error: true

      - name: Generate Audit Report
        run: python scripts/generate-audit-report.py
        env:
          SYSTEM_NAME: ${{ github.repository }}
          VERSION: ${{ github.sha }}
          RISK_TIER: ${{ vars.RISK_TIER || 'Tier 3' }}

      - name: Upload Evidence
        uses: actions/upload-artifact@v4
        with:
          name: audit-evidence-${{ github.sha }}
          path: audit/
          retention-days: 90

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('audit/summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });

      - name: Fail on P0 Findings
        run: |
          P0_COUNT=$(jq '[.findings[] | select(.severity == "P0")] | length' audit/findings.json)
          if [ "$P0_COUNT" -gt 0 ]; then
            echo "P0 findings detected: $P0_COUNT"
            exit 1
          fi
```

### GitLab CI Workflow

```yaml
stages:
  - audit
  - report

variables:
  AUDIT_DIR: "audit"
  RISK_TIER: "Tier 3"

dependency_scan:
  stage: audit
  image: node:20
  script:
    - npm install
    - npm audit --audit-level=high --json > $AUDIT_DIR/dependency-scan.json
  artifacts:
    paths:
      - $AUDIT_DIR/
    expire_in: 90 days
  allow_failure: true

secret_scan:
  stage: audit
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --report-path $AUDIT_DIR/secret-scan.json --report-format json
  artifacts:
    paths:
      - $AUDIT_DIR/
    expire_in: 90 days

sast_scan:
  stage: audit
  image: returntocorp/semgrep:latest
  script:
    - semgrep --config auto --severity=ERROR --json -o $AUDIT_DIR/sast-scan.json .
  artifacts:
    paths:
      - $AUDIT_DIR/
    expire_in: 90 days
  allow_failure: true

lint_check:
  stage: audit
  image: node:20
  script:
    - npm install
    - npm run lint > $AUDIT_DIR/lint-report.txt 2>&1
  artifacts:
    paths:
      - $AUDIT_DIR/
    expire_in: 90 days
  allow_failure: true

test_coverage:
  stage: audit
  image: node:20
  script:
    - npm install
    - npm run test:coverage -- --coverageReporters=json
  artifacts:
    paths:
      - coverage/
    expire_in: 90 days
  allow_failure: true

generate_report:
  stage: report
  image: python:3.11
  script:
    - pip install -r scripts/requirements.txt
    - python scripts/generate-audit-report.py
  artifacts:
    paths:
      - $AUDIT_DIR/
    expire_in: 90 days
  dependencies:
    - dependency_scan
    - secret_scan
    - sast_scan
    - lint_check
    - test_coverage
```

## Custom Automation Scripts

### Audit Runner Script

```python
#!/usr/bin/env python3
"""
Audit Runner - Orchestrates all audit scans and generates findings.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class AuditRunner:
    def __init__(self, output_dir: str = "audit"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.findings: List[Dict] = []
        self.metadata = {
            "audit_date": datetime.now().isoformat(),
            "system_name": os.getenv("SYSTEM_NAME", "unknown"),
            "version": os.getenv("VERSION", "unknown"),
            "risk_tier": os.getenv("RISK_TIER", "Tier 3"),
            "auditor": os.getenv("AUDITOR", "automated"),
        }

    def run_command(self, cmd: List[str], output_file: str) -> bool:
        """Run a command and save output to file."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            output_path = self.output_dir / output_file
            output_path.write_text(result.stdout)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"Command timed out: {' '.join(cmd)}")
            return False
        except Exception as e:
            print(f"Error running command: {e}")
            return False

    def dependency_scan(self) -> List[Dict]:
        """Run dependency vulnerability scan."""
        print("Running dependency scan...")
        success = self.run_command(
            ["npm", "audit", "--audit-level=high", "--json"],
            "dependency-scan.json"
        )
        if not success:
            print("Warning: Dependency scan failed")
        return self.parse_dependency_scan()

    def secret_scan(self) -> List[Dict]:
        """Run secret scanning."""
        print("Running secret scan...")
        success = self.run_command(
            ["gitleaks", "detect", "--source", ".", "--report-path",
             str(self.output_dir / "secret-scan.json"), "--report-format", "json"],
            "secret-scan.json"
        )
        if not success:
            print("Warning: Secret scan failed")
        return self.parse_secret_scan()

    def sast_scan(self) -> List[Dict]:
        """Run static code analysis."""
        print("Running SAST scan...")
        success = self.run_command(
            ["semgrep", "--config", "auto", "--severity=ERROR", "--json",
             "-o", str(self.output_dir / "sast-scan.json"), "."],
            "sast-scan.json"
        )
        if not success:
            print("Warning: SAST scan failed")
        return self.parse_sast_scan()

    def lint_check(self) -> List[Dict]:
        """Run linting."""
        print("Running lint check...")
        success = self.run_command(
            ["npm", "run", "lint"],
            "lint-report.txt"
        )
        if not success:
            print("Warning: Lint check failed")
        return self.parse_lint_report()

    def coverage_check(self) -> Dict:
        """Check test coverage."""
        print("Running coverage check...")
        success = self.run_command(
            ["npm", "run", "test:coverage", "--", "--coverageReporters=json"],
            "coverage-report.json"
        )
        if not success:
            print("Warning: Coverage check failed")
        return self.parse_coverage_report()

    def parse_dependency_scan(self) -> List[Dict]:
        """Parse dependency scan results."""
        findings = []
        try:
            scan_data = json.loads(
                (self.output_dir / "dependency-scan.json").read_text()
            )
            for vuln in scan_data.get("vulnerabilities", []):
                if vuln.get("severity") in ["critical", "high"]:
                    findings.append({
                        "id": f"DEP-{len(findings)+1:03d}",
                        "severity": "P0" if vuln["severity"] == "critical" else "P1",
                        "domain": "Development",
                        "title": f"Vulnerable dependency: {vuln.get('name', 'unknown')}",
                        "description": vuln.get("title", ""),
                        "location": vuln.get("dependency", {}).get("name", "unknown"),
                        "violated_rule": "Development P0 - Dependencies Scanned",
                        "production_risk": vuln.get("severity", "unknown").upper(),
                        "evidence": "dependency-scan.json",
                        "fix": f"Update {vuln.get('name', 'dependency')} to version {vuln.get('fixAvailable', {}).get('name', 'latest')}",
                    })
        except Exception as e:
            print(f"Error parsing dependency scan: {e}")
        return findings

    def parse_secret_scan(self) -> List[Dict]:
        """Parse secret scan results."""
        findings = []
        try:
            scan_data = json.loads(
                (self.output_dir / "secret-scan.json").read_text()
            )
            for finding in scan_data:
                findings.append({
                    "id": f"SEC-{len(findings)+1:03d}",
                    "severity": "P0",
                    "domain": "Security",
                    "title": f"Hardcoded secret detected: {finding.get('rule', 'unknown')}",
                    "description": finding.get("description", ""),
                    "location": finding.get("file", "unknown"),
                    "violated_rule": "Security P0 - Credential Management",
                    "production_risk": "CRITICAL - Credential exposure",
                    "evidence": "secret-scan.json",
                    "fix": "Remove secret from code and use secret management system. Rotate exposed credentials.",
                })
        except Exception as e:
            print(f"Error parsing secret scan: {e}")
        return findings

    def parse_sast_scan(self) -> List[Dict]:
        """Parse SAST scan results."""
        findings = []
        try:
            scan_data = json.loads(
                (self.output_dir / "sast-scan.json").read_text()
            )
            for result in scan_data.get("results", []):
                severity = result.get("extra", {}).get("severity", "MEDIUM")
                if severity in ["ERROR", "CRITICAL", "HIGH"]:
                    findings.append({
                        "id": f"SAST-{len(findings)+1:03d}",
                        "severity": "P0" if severity in ["ERROR", "CRITICAL"] else "P1",
                        "domain": "Development",
                        "title": result.get("check_id", "unknown"),
                        "description": result.get("extra", {}).get("message", ""),
                        "location": result.get("path", "unknown"),
                        "violated_rule": "Development P0 - Code Quality Standards",
                        "production_risk": severity,
                        "evidence": "sast-scan.json",
                        "fix": result.get("extra", {}).get("fix", "Review and fix manually"),
                    })
        except Exception as e:
            print(f"Error parsing SAST scan: {e}")
        return findings

    def parse_lint_report(self) -> List[Dict]:
        """Parse lint report."""
        findings = []
        try:
            report_path = self.output_dir / "lint-report.txt"
            if report_path.exists():
                content = report_path.read_text()
                if "error" in content.lower() or "✖" in content:
                    findings.append({
                        "id": f"LINT-{len(findings)+1:03d}",
                        "severity": "P1",
                        "domain": "Development",
                        "title": "Linting errors detected",
                        "description": "Code does not pass linting checks",
                        "location": "Multiple files",
                        "violated_rule": "Development P0 - Code Quality Standards",
                        "production_risk": "MEDIUM - Code quality issues",
                        "evidence": "lint-report.txt",
                        "fix": "Fix linting errors according to project style guide",
                    })
        except Exception as e:
            print(f"Error parsing lint report: {e}")
        return findings

    def parse_coverage_report(self) -> Dict:
        """Parse coverage report."""
        coverage_data = {"lines": 0, "branches": 0, "functions": 0}
        try:
            report_path = self.output_dir / "coverage-report.json"
            if report_path.exists():
                data = json.loads(report_path.read_text())
                total = data.get("total", {})
                coverage_data["lines"] = total.get("lines", {}).get("pct", 0)
                coverage_data["branches"] = total.get("branches", {}).get("pct", 0)
                coverage_data["functions"] = total.get("functions", {}).get("pct", 0)
        except Exception as e:
            print(f"Error parsing coverage report: {e}")
        return coverage_data

    def collect_all_findings(self) -> List[Dict]:
        """Collect findings from all scans."""
        all_findings = []
        all_findings.extend(self.dependency_scan())
        all_findings.extend(self.secret_scan())
        all_findings.extend(self.sast_scan())
        all_findings.extend(self.lint_check())
        self.findings = all_findings
        return all_findings

    def generate_findings_json(self):
        """Generate findings JSON file."""
        findings_data = {
            "metadata": self.metadata,
            "findings": self.findings,
            "summary": {
                "total": len(self.findings),
                "p0": len([f for f in self.findings if f["severity"] == "P0"]),
                "p1": len([f for f in self.findings if f["severity"] == "P1"]),
                "p2": len([f for f in self.findings if f["severity"] == "P2"]),
                "p3": len([f for f in self.findings if f["severity"] == "P3"]),
            }
        }
        output_path = self.output_dir / "findings.json"
        output_path.write_text(json.dumps(findings_data, indent=2))

    def generate_summary_markdown(self):
        """Generate summary markdown for PR comments."""
        summary = f"""# Audit Summary

**System:** {self.metadata['system_name']}
**Date:** {self.metadata['audit_date']}
**Risk Tier:** {self.metadata['risk_tier']}

## Findings Summary

| Severity | Count |
|----------|-------|
| P0 (Critical) | {len([f for f in self.findings if f['severity'] == 'P0'])} |
| P1 (High) | {len([f for f in self.findings if f['severity'] == 'P1'])} |
| P2 (Medium) | {len([f for f in self.findings if f['severity'] == 'P2'])} |
| P3 (Low) | {len([f for f in self.findings if f['severity'] == 'P3'])} |

## Key Findings

"""
        for finding in self.findings[:5]:  # Top 5 findings
            summary += f"- **{finding['severity']}**: {finding['title']} ({finding['location']})\n"

        summary += "\n[View full report](audit-evidence) for details.\n"
        output_path = self.output_dir / "summary.md"
        output_path.write_text(summary)

    def run(self):
        """Run complete audit."""
        print("Starting audit...")
        self.collect_all_findings()
        self.generate_findings_json()
        self.generate_summary_markdown()

        # Print summary
        print("\nAudit Complete!")
        print(f"Total findings: {len(self.findings)}")
        print(f"P0: {len([f for f in self.findings if f['severity'] == 'P0'])}")
        print(f"P1: {len([f for f in self.findings if f['severity'] == 'P1'])}")
        print(f"P2: {len([f for f in self.findings if f['severity'] == 'P2'])}")
        print(f"P3: {len([f for f in self.findings if f['severity'] == 'P3'])}")

        # Exit with error if P0 findings exist
        if any(f["severity"] == "P0" for f in self.findings):
            print("\nERROR: P0 findings detected! Build failed.")
            sys.exit(1)

        print("\nAudit passed!")
        sys.exit(0)


if __name__ == "__main__":
    runner = AuditRunner()
    runner.run()
```

### Report Generator Script

```python
#!/usr/bin/env python3
"""
Audit Report Generator - Generates comprehensive audit reports from scan results.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class AuditReportGenerator:
    def __init__(self, audit_dir: str = "audit"):
        self.audit_dir = Path(audit_dir)
        self.findings: List[Dict] = []
        self.metadata: Dict = {}

    def load_findings(self):
        """Load findings from JSON file."""
        findings_path = self.audit_dir / "findings.json"
        if findings_path.exists():
            data = json.loads(findings_path.read_text())
            self.findings = data.get("findings", [])
            self.metadata = data.get("metadata", {})

    def load_scan_results(self):
        """Load all scan results."""
        self.scans = {}
        scan_files = {
            "dependency": "dependency-scan.json",
            "secrets": "secret-scan.json",
            "sast": "sast-scan.json",
            "lint": "lint-report.txt",
            "coverage": "coverage-report.json",
        }
        for scan_type, filename in scan_files.items():
            scan_path = self.audit_dir / filename
            if scan_path.exists():
                if scan_path.suffix == ".json":
                    self.scans[scan_type] = json.loads(scan_path.read_text())
                else:
                    self.scans[scan_type] = scan_path.read_text()

    def generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        p0_count = len([f for f in self.findings if f["severity"] == "P0"])
        p1_count = len([f for f in self.findings if f["severity"] == "P1"])

        if p0_count > 0:
            status = "BLOCKED"
        elif p1_count > 0:
            status = "CONDITIONAL"
        else:
            status = "APPROVED"

        return f"""# Audit Executive Summary

**System:** {self.metadata.get('system_name', 'Unknown')}
**Version:** {self.metadata.get('version', 'Unknown')}
**Audit Date:** {self.metadata.get('audit_date', 'Unknown')}
**Risk Tier:** {self.metadata.get('risk_tier', 'Unknown')}
**Overall Status:** {status}

## Findings Summary

| Severity | Count |
|----------|-------|
| P0 (Critical) | {p0_count} |
| P1 (High) | {p1_count} |
| P2 (Medium) | {len([f for f in self.findings if f['severity'] == 'P2'])} |
| P3 (Low) | {len([f for f in self.findings if f['severity'] == 'P3'])} |

## Key Findings

{self._format_key_findings()}

## Recommendations

{self._format_recommendations()}

## Next Steps

1. Address all P0 findings immediately
2. Review and accept or fix P1 findings
3. Schedule P2/P3 findings for future sprints
"""

    def _format_key_findings(self) -> str:
        """Format key findings for summary."""
        lines = []
        for finding in self.findings[:5]:
            lines.append(f"- **{finding['severity']}**: {finding['title']}")
        return "\n".join(lines) if lines else "No critical findings."

    def _format_recommendations(self) -> str:
        """Format recommendations."""
        return """1. **Security:** Address all P0 security findings immediately
2. **Reliability:** Implement missing error handling and retry logic
3. **Testing:** Increase test coverage for critical paths
4. **Documentation:** Complete missing runbooks and API docs"""

    def generate_detailed_findings(self) -> str:
        """Generate detailed findings section."""
        lines = ["# Detailed Findings\n"]

        for severity in ["P0", "P1", "P2", "P3"]:
            severity_findings = [f for f in self.findings if f["severity"] == severity]
            if severity_findings:
                lines.append(f"\n## {severity} Findings\n")
                for finding in severity_findings:
                    lines.append(self._format_finding(finding))

        return "\n".join(lines)

    def _format_finding(self, finding: Dict) -> str:
        """Format a single finding."""
        return f"""### {finding.get('id', 'N/A')}: {finding.get('title', 'Untitled')}

- **Severity:** {finding.get('severity', 'N/A')}
- **Domain:** {finding.get('domain', 'N/A')}
- **Location:** {finding.get('location', 'N/A')}
- **Violated Rule:** {finding.get('violated_rule', 'N/A')}
- **Production Risk:** {finding.get('production_risk', 'N/A')}

**Evidence:** {finding.get('evidence', 'N/A')}

**Fix:** {finding.get('fix', 'N/A')}

---

"""

    def generate_compliance_matrix(self) -> str:
        """Generate compliance matrix."""
        lines = [
            "# Compliance Matrix",
            "",
            "| Domain | P0 | P1 | P2 | Status |",
            "|--------|----|----|-----|--------|"
        ]

        domains = {}
        for finding in self.findings:
            domain = finding.get("domain", "Unknown")
            if domain not in domains:
                domains[domain] = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
            severity = finding.get("severity", "P3")
            if severity in domains[domain]:
                domains[domain][severity] += 1

        for domain, counts in sorted(domains.items()):
            status = "PASS" if counts["P0"] == 0 and counts["P1"] == 0 else "CONDITIONAL"
            lines.append(f"| {domain} | {counts['P0']} | {counts['P1']} | {counts['P2']} | {status} |")

        return "\n".join(lines)

    def generate_full_report(self) -> str:
        """Generate complete audit report."""
        self.load_findings()
        self.load_scan_results()

        report = f"""# Full Audit Report

**System:** {self.metadata.get('system_name', 'Unknown')}
**Version:** {self.metadata.get('version', 'Unknown')}
**Audit Date:** {self.metadata.get('audit_date', 'Unknown')}
**Auditor:** {self.metadata.get('auditor', 'Unknown')}
**Risk Tier:** {self.metadata.get('risk_tier', 'Unknown')}

{self.generate_executive_summary()}

{self.generate_compliance_matrix()}

{self.generate_detailed_findings()}

---

*Report generated on {datetime.now().isoformat()}*
"""
        return report

    def save_report(self, filename: str = "audit-report.md"):
        """Save report to file."""
        report = self.generate_full_report()
        report_path = self.audit_dir / filename
        report_path.write_text(report)
        print(f"Report saved to {report_path}")


def main():
    generator = AuditReportGenerator()
    generator.save_report()


if __name__ == "__main__":
    main()
```

## Scheduled Audits

### Cron-Based Scheduled Audits

**GitHub Actions Scheduled Workflow:**
```yaml
name: Weekly Audit
on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday at midnight UTC
  workflow_dispatch:

jobs:
  weekly-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Audit
        run: python scripts/audit-runner.py
      - name: Generate Report
        run: python scripts/audit-report-generator.py
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: weekly-audit-report
          path: audit/
      - name: Notify Team
        if: always()
        run: |
          if [ -f audit/findings.json ]; then
            P0_COUNT=$(jq '.summary.p0' audit/findings.json)
            if [ "$P0_COUNT" -gt 0 ]; then
              echo "::warning::P0 findings detected in weekly audit"
              # Send notification to team
            fi
          fi
```

### GitLab Scheduled Pipelines

```yaml
stages:
  - scheduled-audit

weekly_audit:
  stage: scheduled-audit
  image: python:3.11
  only:
    - schedules
  script:
    - pip install -r scripts/requirements.txt
    - python scripts/audit-runner.py
    - python scripts/audit-report-generator.py
  artifacts:
    paths:
      - audit/
    expire_in: 90 days
```

## Custom Automation Patterns

### Pattern 1: Finding Deduplication

```python
def deduplicate_findings(findings: List[Dict]) -> List[Dict]:
    """Remove duplicate findings based on location and rule."""
    seen = set()
    deduplicated = []

    for finding in findings:
        key = (finding.get("location"), finding.get("violated_rule"))
        if key not in seen:
            seen.add(key)
            deduplicated.append(finding)

    return deduplicated
```

### Pattern 2: Finding Aggregation

```python
def aggregate_findings(findings: List[Dict]) -> Dict:
    """Aggregate findings by domain and severity."""
    aggregated = {
        "by_domain": {},
        "by_severity": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
        "by_rule": {},
    }

    for finding in findings:
        # By domain
        domain = finding.get("domain", "Unknown")
        aggregated["by_domain"].setdefault(domain, 0)
        aggregated["by_domain"][domain] += 1

        # By severity
        severity = finding.get("severity", "P3")
        aggregated["by_severity"][severity] += 1

        # By rule
        rule = finding.get("violated_rule", "Unknown")
        aggregated["by_rule"].setdefault(rule, 0)
        aggregated["by_rule"][rule] += 1

    return aggregated
```

### Pattern 3: Automated Triage

```python
def triage_finding(finding: Dict) -> str:
    """Automatically triage finding based on rules."""
    severity = finding.get("severity", "P3")

    # Auto-accept P2/P3 findings
    if severity in ["P2", "P3"]:
        return "auto-accepted"

    # Auto-escalate P0 findings
    if severity == "P0":
        finding["auto_escalated"] = True
        finding["escalation_reason"] = "P0 finding requires immediate attention"
        return "escalated"

    # P1 findings need review
    return "needs-review"
```

### Pattern 4: Evidence Auto-Collection

```python
def auto_collect_evidence(finding: Dict) -> List[Dict]:
    """Automatically collect evidence for a finding."""
    evidence = []

    # Collect code snippet
    location = finding.get("location")
    if location and Path(location).exists():
        evidence.append({
            "type": "code",
            "description": f"Code at {location}",
            "content": Path(location).read_text(),
        })

    # Collect related scan results
    scan_type = finding.get("scan_type")
    if scan_type:
        scan_file = f"{scan_type}-scan.json"
        scan_path = self.audit_dir / scan_file
        if scan_path.exists():
            evidence.append({
                "type": "scan",
                "description": f"{scan_type} scan results",
                "content": scan_path.read_text(),
            })

    return evidence
```

### Pattern 5: Notification Automation

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_audit_notification(findings: List[Dict], recipients: List[str]):
    """Send email notification with audit results."""
    p0_count = len([f for f in findings if f["severity"] == "P0"])
    p1_count = len([f for f in findings if f["severity"] == "P1"])

    subject = f"Audit Results: {p0_count} P0, {p1_count} P1 findings"

    body = f"""
Audit completed with the following findings:

P0 (Critical): {p0_count}
P1 (High): {p1_count}
P2 (Medium): {len([f for f in findings if f['severity'] == 'P2'])}
P3 (Low): {len([f for f in findings if f['severity'] == 'P3'])}

Top findings:
"""

    for finding in findings[:5]:
        body += f"- {finding['severity']}: {finding['title']}\n"

    body += "\nView full report at: [link]"

    msg = MIMEMultipart()
    msg['From'] = os.getenv("AUDIT_EMAIL_FROM")
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)
```

## Dashboard and Reporting

### Audit Dashboard

Create a dashboard to track audit metrics:

```python
import json
from datetime import datetime, timedelta
from pathlib import Path

class AuditDashboard:
    def __init__(self, audit_dir: str = "audit"):
        self.audit_dir = Path(audit_dir)
        self.history_file = self.audit_dir / "audit-history.json"

    def load_history(self) -> List[Dict]:
        """Load audit history."""
        if self.history_file.exists():
            return json.loads(self.history_file.read_text())
        return []

    def save_history(self, history: List[Dict]):
        """Save audit history."""
        self.history_file.write_text(json.dumps(history, indent=2))

    def record_audit(self, findings: List[Dict], metadata: Dict):
        """Record audit results in history."""
        history = self.load_history()
        history.append({
            "date": datetime.now().isoformat(),
            "metadata": metadata,
            "summary": {
                "total": len(findings),
                "p0": len([f for f in findings if f["severity"] == "P0"]),
                "p1": len([f for f in findings if f["severity"] == "P1"]),
                "p2": len([f for f in findings if f["severity"] == "P2"]),
                "p3": len([f for f in findings if f["severity"] == "P3"]),
            },
            "findings": findings,
        })
        self.save_history(history)

    def generate_dashboard_data(self) -> Dict:
        """Generate data for dashboard."""
        history = self.load_history()
        last_30_days = [
            h for h in history
            if datetime.fromisoformat(h["date"]) >= datetime.now() - timedelta(days=30)
        ]

        return {
            "total_audits": len(history),
            "audits_last_30_days": len(last_30_days),
            "total_findings_all_time": sum(h["summary"]["total"] for h in history),
            "findings_last_30_days": sum(h["summary"]["total"] for h in last_30_days),
            "p0_trend": [h["summary"]["p0"] for h in last_30_days],
            "p1_trend": [h["summary"]["p1"] for h in last_30_days],
            "compliance_trend": self._calculate_compliance_trend(history),
        }

    def _calculate_compliance_trend(self, history: List[Dict]) -> List[Dict]:
        """Calculate compliance trend over time."""
        trend = []
        for entry in history:
            total = entry["summary"]["total"]
            p0 = entry["summary"]["p0"]
            compliance_score = max(0, 100 - (p0 * 10) - (entry["summary"]["p1"] * 2))
            trend.append({
                "date": entry["date"],
                "score": compliance_score,
                "p0": p0,
                "p1": entry["summary"]["p1"],
            })
        return trend
```

## Automation Best Practices

### 1. Fail Fast on Critical Issues

Configure CI/CD to fail on P0 findings:
```yaml
- name: Check for P0 Findings
  run: |
    P0_COUNT=$(jq '[.findings[] | select(.severity == "P0")] | length' audit/findings.json)
    if [ "$P0_COUNT" -gt 0 ]; then
      echo "ERROR: P0 findings detected!"
      exit 1
    fi
```

### 2. Provide Actionable Feedback

Include fix suggestions in automation output:
```json
{
  "finding": "SQL injection vulnerability",
  "location": "src/db/query.ts:45",
  "severity": "P0",
  "fix": "Use parameterized queries instead of string concatenation",
  "example": "db.query('SELECT * FROM users WHERE id = ?', [userId])"
}
```

### 3. Track Metrics Over Time

Store audit history and track trends:
- P0/P1 finding trends
- Time to resolve findings
- Evidence completeness
- Compliance scores

### 4. Integrate with Issue Trackers

Automatically create tickets for findings:
```python
def create_ticket(finding: Dict):
    """Create ticket in issue tracker for finding."""
    # Example: GitHub issue
    import requests

    ticket_data = {
        "title": f"[{finding['severity']}] {finding['title']}",
        "body": f"""
## Finding
{finding.get('description', '')}

## Location
{finding.get('location', '')}

## Fix
{finding.get('fix', '')}

## Evidence
{finding.get('evidence', '')}
        """,
        "labels": [finding["severity"].lower(), finding["domain"].lower()],
    }

    response = requests.post(
        f"https://api.github.com/repos/{os.getenv('GITHUB_REPOSITORY')}/issues",
        json=ticket_data,
        headers={
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json",
        }
    )
```

### 5. Enable Continuous Auditing

Run audits continuously, not just periodically:
- On every commit (fast checks)
- On every PR (comprehensive checks)
- Nightly (deep scans)
- Weekly (full audit)

## Automation Limitations

### What Automation Cannot Do

- **Architecture Review**: Automated tools cannot assess architectural soundness.
- **Business Logic**: Automated tools cannot verify business logic correctness.
- **Risk Assessment**: Automated tools cannot determine risk tier or severity.
- **Exception Handling**: Automated tools cannot determine if exception handling is appropriate.
- **Design Decisions**: Automated tools cannot evaluate design trade-offs.
- **Context Understanding**: Automated tools lack understanding of business context.

### Human Review Requirements

Always require human review for:
- P0 finding classification
- Risk tier determination
- Architecture decisions
- Exception handling assessment
- Business logic validation
- Final audit report approval

## Automation Metrics

Track these metrics to improve automation:

**Automation Effectiveness**
- Percentage of P0 findings found by automation
- False positive rate
- False negative rate
- Time saved by automation

**Automation Efficiency**
- Time to run scans
- Time to generate report
- Resource utilization
- Cost of automation

**Automation Adoption**
- Percentage of scans that pass
- Developer satisfaction
- Finding resolution time
- Recurrence of findings

## Appendix: Automation Scripts Index

| Script | Purpose | Usage |
|--------|---------|-------|
| `audit-runner.py` | Orchestrate all scans | `python scripts/audit-runner.py` |
| `audit-report-generator.py` | Generate audit reports | `python scripts/audit-report-generator.py` |
| `audit-dashboard.py` | Generate dashboard data | `python scripts/audit-dashboard.py` |
| `create-tickets.py` | Create tickets for findings | `python scripts/create-tickets.py` |
| `notify-team.py` | Send notifications | `python scripts/notify-team.py` |
| `collect-evidence.py` | Collect evidence for findings | `python scripts/collect-evidence.py` |
