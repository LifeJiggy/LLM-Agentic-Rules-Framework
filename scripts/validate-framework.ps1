param(
    [string]$Root = (Resolve-Path "$PSScriptRoot\..").Path
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    Write-Host "Framework validation failed:" -ForegroundColor Red
    Write-Host " - Root directory does not exist: $Root" -ForegroundColor Red
    exit 1
}

$Root = (Resolve-Path -LiteralPath $Root).Path

$requiredRootFiles = @(
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    "ROADMAP.md",
    "mkdocs.yml"
)

$requiredSupportFiles = @(
    ".github/workflows/validate-framework.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/rule_proposal.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".codex-plugin/plugin.json",
    "adapters/README.md",
    "adapters/manifest.json",
    "adapters/targets.md",
    "agents/rules-architect.md",
    "agents/rules-reviewer.md",
    "agents/rules-release-gate.md",
    "commands/rules-audit.md",
    "commands/rules-plan.md",
    "commands/rules-release.md",
    "docs/adoption-playbook.md",
    "docs/agentic-cli-plugin-guide.md",
    "docs/checklist-packs.md",
    "docs/domain-knowledge-map.md",
    "docs/domain-index.md",
    "docs/evolution-process.md",
    "docs/framework-quality-standard.md",
    "docs/glossary.md",
    "docs/getting-started.md",
    "docs/index.md",
    "docs/advanced-usage.md",
    "docs/migration-guide.md",
    "docs/risk-tiering.md",
    "assets/templates/architecture-decision-record.md",
    "assets/templates/rule-template.md",
    "assets/templates/ai-system-register.yml",
    "assets/templates/compliance-review.md",
    "assets/templates/compliance-evidence-pack.md",
    "assets/templates/evaluation-plan.md",
    "assets/templates/evaluation-pack-retrieval.md",
    "assets/templates/evaluation-pack-safety.md",
    "assets/templates/evaluation-pack-tools.md",
    "assets/templates/incident-runbook.md",
    "assets/templates/model-prompt-change-review.md",
    "assets/templates/release-checklist.md",
    "examples/agentic-automation/README.md",
    "examples/production-assistant/README.md",
    "skills/llm-agentic-rules/SKILL.md",
    "skills/system/SKILL.md",
    "skills/system/reliability-checklist.md",
    "skills/system/recovery-playbook.md",
    "scripts/check_rules.py",
    "scripts/install_agent_adapters.py"
)

$requiredDomains = @(
    "01-core",
    "02-security",
    "03-development",
    "04-data",
    "05-integration",
    "06-operations",
    "07-testing",
    "08-documentation",
    "09-performance",
    "10-compliance"
)

$requiredDomainFiles = @(
    "fundamentals.md",
    "best-practices.md",
    "anti-patterns.md",
    "checklist.md",
    "examples.md",
    "troubleshooting.md",
    "advanced.md"
)

$failures = New-Object System.Collections.Generic.List[string]

function Add-DuplicateFailures {
    param(
        [string]$Label,
        [string[]]$Items
    )

    $duplicates = $Items | Group-Object | Where-Object { $_.Count -gt 1 }
    foreach ($duplicate in $duplicates) {
        $failures.Add("Duplicate $Label entry: $($duplicate.Name)")
    }
}

function Test-RequiredFile {
    param(
        [string]$RelativePath,
        [string]$Label
    )

    $path = Join-Path $Root $RelativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $failures.Add("Missing ${Label}: $RelativePath")
        return
    }

    $item = Get-Item -LiteralPath $path
    if ($item.Length -eq 0) {
        $failures.Add("Empty ${Label}: $RelativePath")
    }

    if ([System.IO.Path]::GetExtension($path) -eq ".json") {
        try {
            Get-Content -LiteralPath $path -Raw | ConvertFrom-Json | Out-Null
        } catch {
            $failures.Add("Invalid JSON ${Label}: $RelativePath ($($_.Exception.Message))")
        }
    }
}

Add-DuplicateFailures -Label "root file" -Items $requiredRootFiles
Add-DuplicateFailures -Label "support file" -Items $requiredSupportFiles
Add-DuplicateFailures -Label "domain" -Items $requiredDomains
Add-DuplicateFailures -Label "domain file" -Items $requiredDomainFiles

$allowedDomainFiles = @{}
foreach ($file in $requiredDomainFiles) {
    $allowedDomainFiles[$file] = $true
}

foreach ($file in $requiredRootFiles) {
    Test-RequiredFile -RelativePath $file -Label "root file"
}

foreach ($file in $requiredSupportFiles) {
    Test-RequiredFile -RelativePath $file -Label "support file"
}

$domainsRoot = Join-Path $Root "domains"
if (-not (Test-Path -LiteralPath $domainsRoot -PathType Container)) {
    $failures.Add("Missing domains directory")
} else {
    foreach ($domain in $requiredDomains) {
        $domainPath = Join-Path $domainsRoot $domain
        if (-not (Test-Path -LiteralPath $domainPath -PathType Container)) {
            $failures.Add("Missing domain directory: domains/$domain")
            continue
        }

        foreach ($file in $requiredDomainFiles) {
            Test-RequiredFile -RelativePath "domains/$domain/$file" -Label "domain file"
        }

        $markdownFiles = Get-ChildItem -LiteralPath $domainPath -File -Filter "*.md" -ErrorAction SilentlyContinue
        foreach ($markdownFile in $markdownFiles) {
            if (-not $allowedDomainFiles.ContainsKey($markdownFile.Name)) {
                $relative = "domains/$domain/$($markdownFile.Name)"
                $failures.Add("Unexpected domain markdown file: $relative")
            }
        }

        $legacyFiles = Get-ChildItem -LiteralPath $domainPath -File -Filter "task-*.md" -ErrorAction SilentlyContinue
        foreach ($legacyFile in $legacyFiles) {
            $relative = "domains/$domain/$($legacyFile.Name)"
            $failures.Add("Legacy task-prefixed filename remains: $relative")
        }
    }
}

if ($failures.Count -gt 0) {
    Write-Host "Framework validation failed:" -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host " - $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host "Framework validation passed." -ForegroundColor Green
Write-Host "Checked $($requiredDomains.Count) domains and $($requiredDomainFiles.Count) files per domain."
Write-Host "Checked $($requiredSupportFiles.Count) support files."
