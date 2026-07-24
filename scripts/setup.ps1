<#
.SYNOPSIS
    LLM & Agentic Rules Framework - Setup Script (PowerShell)

.DESCRIPTION
    This script sets up the framework environment on Windows systems.

.PARAMETER Check
    Check system requirements

.PARAMETER Install
    Install dependencies

.PARAMETER Validate
    Validate framework structure

.PARAMETER Configure
    Configure framework settings

.PARAMETER All
    Run all setup steps (default)

.EXAMPLE
    .\scripts\setup.ps1 -All

.EXAMPLE
    .\scripts\setup.ps1 -Check
#>

param(
    [switch]$Check,
    [switch]$Install,
    [switch]$Validate,
    [switch]$Configure,
    [switch]$All,
    [switch]$Help
)

# Framework metadata
$FrameworkName = "LLM & Agentic Rules Framework"
$FrameworkVersion = "2.0.0"
$FrameworkRoot = Split-Path -Parent $PSScriptRoot

# Counters
$script:SuccessCount = 0
$script:WarningCount = 0
$script:ErrorCount = 0

# Required directories
$RequiredDirectories = @(
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
    "examples"
)

# Required domains
$RequiredDomains = @(
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

# Required domain files
$RequiredDomainFiles = @(
    "fundamentals.md",
    "best-practices.md",
    "anti-patterns.md",
    "checklist.md",
    "examples.md",
    "troubleshooting.md",
    "advanced.md"
)

# Functions
function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "$FrameworkName v$FrameworkVersion" -ForegroundColor Cyan
    Write-Host "============================================"
    Write-Host $Title
    Write-Host "============================================"
}

function Write-Success {
    param([string]$Message)
    Write-Host "  + $Message" -ForegroundColor Green
    $script:SuccessCount++
}

function Write-Warning {
    param([string]$Message)
    Write-Host "  ! $Message" -ForegroundColor Yellow
    $script:WarningCount++
}

function Write-Error {
    param([string]$Message)
    Write-Host "  - $Message" -ForegroundColor Red
    $script:ErrorCount++
}

function Write-Results {
    Write-Host ""
    Write-Host "============================================"
    Write-Host "Results" -ForegroundColor Cyan
    Write-Host "============================================"
    Write-Host "  Success: $script:SuccessCount" -ForegroundColor Green
    Write-Host "  Warnings: $script:WarningCount" -ForegroundColor Yellow
    Write-Host "  Errors: $script:ErrorCount" -ForegroundColor Red
    Write-Host "============================================"
    
    if ($script:ErrorCount -eq 0) {
        Write-Host "  Setup completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "  Setup completed with errors. Please fix the issues above." -ForegroundColor Red
    }
    Write-Host "============================================"
}

function Test-Python {
    Write-Host ""
    Write-Host "--- Checking Python ---" -ForegroundColor Cyan
    
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python found: $pythonVersion"
            return $true
        }
    } catch {
        # Python not found
    }
    
    try {
        $pythonVersion = python3 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python found: $pythonVersion"
            return $true
        }
    } catch {
        # Python3 not found
    }
    
    Write-Error "Python not found. Please install Python 3.9 or higher."
    return $false
}

function Test-Directories {
    Write-Host ""
    Write-Host "--- Checking Directories ---" -ForegroundColor Cyan
    
    foreach ($dir in $RequiredDirectories) {
        $path = Join-Path -Path $FrameworkRoot -ChildPath $dir
        if (Test-Path -Path $path -PathType Container) {
            Write-Success "Directory exists: $dir"
        } else {
            Write-Error "Missing directory: $dir"
        }
    }
}

function Test-Domains {
    Write-Host ""
    Write-Host "--- Checking Domains ---" -ForegroundColor Cyan
    
    foreach ($domain in $RequiredDomains) {
        $domainPath = Join-Path -Path $FrameworkRoot -ChildPath "domains\$domain"
        if (Test-Path -Path $domainPath -PathType Container) {
            Write-Success "Domain exists: $domain"
            
            foreach ($file in $RequiredDomainFiles) {
                $filePath = Join-Path -Path $domainPath -ChildPath $file
                if (Test-Path -Path $filePath -PathType Leaf) {
                    Write-Success "  File exists: $file"
                } else {
                    Write-Error "  Missing file: $domain/$file"
                }
            }
        } else {
            Write-Error "Missing domain: $domain"
        }
    }
}

function Test-Scripts {
    Write-Host ""
    Write-Host "--- Checking Scripts ---" -ForegroundColor Cyan
    
    $scripts = @(
        "check_rules.py",
        "install_agent_adapters.py",
        "validate-framework.ps1",
        "setup.py",
        "setup.sh",
        "setup.ps1"
    )
    
    foreach ($script in $scripts) {
        $path = Join-Path -Path $FrameworkRoot -ChildPath "scripts\$script"
        if (Test-Path -Path $path -PathType Leaf) {
            Write-Success "Script exists: $script"
        } else {
            Write-Warning "Missing script: $script"
        }
    }
}

function Invoke-Check {
    Write-Header "System Check"
    
    Test-Python | Out-Null
    Test-Directories
    Test-Domains
    Test-Scripts
    
    Write-Results
}

function Install-Dependencies {
    Write-Header "Installing Dependencies"
    
    $requirementsPath = Join-Path -Path $FrameworkRoot -ChildPath "requirements.txt"
    if (Test-Path -Path $requirementsPath -PathType Leaf) {
        try {
            pip install -r $requirementsPath
            Write-Success "Dependencies installed"
        } catch {
            Write-Error "Failed to install dependencies: $_"
        }
    } else {
        Write-Warning "No requirements.txt found, skipping"
    }
    
    Write-Results
}

function Invoke-Validate {
    Write-Header "Validating Framework"
    
    $checkRulesPath = Join-Path -Path $FrameworkRoot -ChildPath "scripts\check_rules.py"
    if (Test-Path -Path $checkRulesPath -PathType Leaf) {
        try {
            python $checkRulesPath --summary
            Write-Success "Framework validation completed"
        } catch {
            Write-Warning "Framework validation completed with warnings"
        }
    } else {
        Write-Warning "check_rules.py not found, skipping"
    }
    
    Write-Results
}

function Set-Configuration {
    Write-Header "Configuring Framework"
    
    $configPath = Join-Path -Path $FrameworkRoot -ChildPath "config.json"
    if (-not (Test-Path -Path $configPath -PathType Leaf)) {
        $config = @{
            name = $FrameworkName
            version = $FrameworkVersion
            framework_root = $FrameworkRoot
            domains = $RequiredDomains
            settings = @{
                auto_validate = $true
                strict_mode = $false
                log_level = "INFO"
            }
        } | ConvertTo-Json -Depth 10
        
        $config | Out-File -FilePath $configPath -Encoding UTF8
        Write-Success "Configuration file created"
    } else {
        Write-Success "Configuration file already exists"
    }
    
    Write-Results
}

function Invoke-All {
    Write-Header "Full Setup"
    
    Invoke-Check
    Install-Dependencies
    Invoke-Validate
    Set-Configuration
}

function Show-Help {
    Write-Host "Usage: .\setup.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Check         Check system requirements"
    Write-Host "  -Install       Install dependencies"
    Write-Host "  -Validate      Validate framework structure"
    Write-Host "  -Configure     Configure framework settings"
    Write-Host "  -All           Run all setup steps (default)"
    Write-Host "  -Help          Show this help message"
}

# Main
if ($Help) {
    Show-Help
    exit 0
}

if (-not ($Check -or $Install -or $Validate -or $Configure)) {
    $All = $true
}

if ($All) {
    Invoke-All
} else {
    if ($Check) { Invoke-Check }
    if ($Install) { Install-Dependencies }
    if ($Validate) { Invoke-Validate }
    if ($Configure) { Set-Configuration }
}

exit $script:ErrorCount
