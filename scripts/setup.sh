#!/usr/bin/env bash
#
# LLM & Agentic Rules Framework - Setup Script (Bash)
#
# This script sets up the framework environment on Unix-like systems.
#
# Usage:
#   chmod +x scripts/setup.sh
#   ./scripts/setup.sh [options]
#
# Options:
#   --check         Check system requirements
#   --install       Install dependencies
#   --validate      Validate framework structure
#   --configure     Configure framework settings
#   --all           Run all setup steps (default)
#   --help          Show this help message
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Framework metadata
FRAMEWORK_NAME="LLM & Agentic Rules Framework"
FRAMEWORK_VERSION="2.0.0"
FRAMEWORK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Required directories
REQUIRED_DIRECTORIES=(
    "domains"
    "agents"
    "skills"
    "memory"
    "storage"
    "evaluation"
    "loop"
    "tools"
    "incident-response"
    "deployment"
    "monitoring"
    "cost-management"
    "vendor-management"
    "governance"
    "docs"
    "scripts"
    "adapters"
    "assets"
    "commands"
    "examples"
)

# Required domains
REQUIRED_DOMAINS=(
    "01-core"
    "02-security"
    "03-development"
    "04-data"
    "05-integration"
    "06-operations"
    "07-testing"
    "08-documentation"
    "09-performance"
    "10-compliance"
)

# Required domain files
REQUIRED_DOMAIN_FILES=(
    "fundamentals.md"
    "best-practices.md"
    "anti-patterns.md"
    "checklist.md"
    "examples.md"
    "troubleshooting.md"
    "advanced.md"
)

# Counters
SUCCESS_COUNT=0
WARNING_COUNT=0
ERROR_COUNT=0

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}${FRAMEWORK_NAME} v${FRAMEWORK_VERSION}${NC}"
    echo "============================================"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((SUCCESS_COUNT++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNING_COUNT++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((ERROR_COUNT++))
}

print_results() {
    echo ""
    echo "============================================"
    echo "Results"
    echo "============================================"
    echo -e "${GREEN}Success: ${SUCCESS_COUNT}${NC}"
    echo -e "${YELLOW}Warnings: ${WARNING_COUNT}${NC}"
    echo -e "${RED}Errors: ${ERROR_COUNT}${NC}"
    echo "============================================"
    
    if [ $ERROR_COUNT -eq 0 ]; then
        echo -e "${GREEN}Setup completed successfully!${NC}"
    else
        echo -e "${RED}Setup completed with errors. Please fix the issues above.${NC}"
    fi
    echo "============================================"
}

check_python() {
    echo ""
    echo "--- Checking Python ---"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python ${PYTHON_VERSION} found"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_success "Python ${PYTHON_VERSION} found"
    else
        print_error "Python not found. Please install Python 3.9 or higher."
        return 1
    fi
}

check_directories() {
    echo ""
    echo "--- Checking Directories ---"
    
    for dir in "${REQUIRED_DIRECTORIES[@]}"; do
        if [ -d "${FRAMEWORK_ROOT}/${dir}" ]; then
            print_success "Directory exists: ${dir}"
        else
            print_error "Missing directory: ${dir}"
        fi
    done
}

check_domains() {
    echo ""
    echo "--- Checking Domains ---"
    
    for domain in "${REQUIRED_DOMAINS[@]}"; do
        if [ -d "${FRAMEWORK_ROOT}/domains/${domain}" ]; then
            print_success "Domain exists: ${domain}"
            
            for file in "${REQUIRED_DOMAIN_FILES[@]}"; do
                if [ -f "${FRAMEWORK_ROOT}/domains/${domain}/${file}" ]; then
                    print_success "  File exists: ${file}"
                else
                    print_error "  Missing file: ${domain}/${file}"
                fi
            done
        else
            print_error "Missing domain: ${domain}"
        fi
    done
}

check_scripts() {
    echo ""
    echo "--- Checking Scripts ---"
    
    scripts=(
        "check_rules.py"
        "install_agent_adapters.py"
        "validate-framework.ps1"
        "setup.py"
        "setup.sh"
        "setup.ps1"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "${FRAMEWORK_ROOT}/scripts/${script}" ]; then
            print_success "Script exists: ${script}"
        else
            print_warning "Missing script: ${script}"
        fi
    done
}

run_check() {
    print_header
    echo "System Check"
    echo "============================================"
    
    check_python
    check_directories
    check_domains
    check_scripts
    
    print_results
}

install_dependencies() {
    print_header
    echo "Installing Dependencies"
    echo "============================================"
    
    if [ -f "${FRAMEWORK_ROOT}/requirements.txt" ]; then
        if command -v pip3 &> /dev/null; then
            pip3 install -r "${FRAMEWORK_ROOT}/requirements.txt"
            print_success "Dependencies installed"
        elif command -v pip &> /dev/null; then
            pip install -r "${FRAMEWORK_ROOT}/requirements.txt"
            print_success "Dependencies installed"
        else
            print_error "pip not found"
            return 1
        fi
    else
        print_warning "No requirements.txt found, skipping"
    fi
    
    print_results
}

validate_framework() {
    print_header
    echo "Validating Framework"
    echo "============================================"
    
    if [ -f "${FRAMEWORK_ROOT}/scripts/check_rules.py" ]; then
        python3 "${FRAMEWORK_ROOT}/scripts/check_rules.py" --summary || true
        print_success "Framework validation completed"
    else
        print_warning "check_rules.py not found, skipping"
    fi
    
    print_results
}

configure_framework() {
    print_header
    echo "Configuring Framework"
    echo "============================================"
    
    if [ ! -f "${FRAMEWORK_ROOT}/config.json" ]; then
        cat > "${FRAMEWORK_ROOT}/config.json" << EOF
{
  "name": "${FRAMEWORK_NAME}",
  "version": "${FRAMEWORK_VERSION}",
  "framework_root": "${FRAMEWORK_ROOT}",
  "domains": [$(printf '"%s", ' "${REQUIRED_DOMAINS[@]}" | sed 's/, $//')],
  "settings": {
    "auto_validate": true,
    "strict_mode": false,
    "log_level": "INFO"
  }
}
EOF
        print_success "Configuration file created"
    else
        print_success "Configuration file already exists"
    fi
    
    print_results
}

run_all() {
    print_header
    echo "Full Setup"
    echo "============================================"
    
    run_check
    install_dependencies
    validate_framework
    configure_framework
}

show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --check         Check system requirements"
    echo "  --install       Install dependencies"
    echo "  --validate      Validate framework structure"
    echo "  --configure     Configure framework settings"
    echo "  --all           Run all setup steps (default)"
    echo "  --help          Show this help message"
}

# Main
main() {
    if [ $# -eq 0 ]; then
        run_all
        exit $ERROR_COUNT
    fi
    
    case "$1" in
        --check)
            run_check
            ;;
        --install)
            install_dependencies
            ;;
        --validate)
            validate_framework
            ;;
        --configure)
            configure_framework
            ;;
        --all)
            run_all
            ;;
        --help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    
    exit $ERROR_COUNT
}

main "$@"
