# Contributing to LLM & Agentic Rules Framework

Thank you for your interest in contributing to the LLM & Agentic Rules Framework! This document provides comprehensive guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Getting Started](#-getting-started)
- [Contribution Guidelines](#-contribution-guidelines)
- [Domain Structure](#-domain-structure)
- [File Format](#-file-format)
- [Naming Conventions](#-naming-conventions)
- [Writing Style Guide](#-writing-style-guide)
- [Pull Request Process](#-pull-request-process)
- [Issue Types](#-issue-types)
- [Development Setup](#-development-setup)
- [Testing Guidelines](#-testing-guidelines)
- [Documentation Standards](#-documentation-standards)
- [Review Process](#-review-process)
- [Recognition Program](#-recognition-program)
- [Getting Help](#-getting-help)
- [Acknowledgments](#-acknowledgments)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate.

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

| Type | Description | Priority |
|------|-------------|----------|
| **New Rules** | Adding new rules to existing or new domains | High |
| **Improvements** | Enhancing existing rules and documentation | Medium |
| **Bug Fixes** | Fixing incorrect or outdated information | High |
| **Translations** | Adding translations for non-English speakers | Medium |
| **Examples** | Adding real-world examples and use cases | Medium |
| **Reviews** | Reviewing and validating existing rules | Low |
| **Tool Integrations** | Creating integrations with development tools | Medium |
| **Documentation** | Improving overall documentation quality | Medium |

### Contribution Workflow

```
┌─────────────────┐
│   Find or       │
│   Create Issue  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Fork & Clone  │
│   Repository    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Create Branch │
│   (feature/fix) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Make Changes  │
│   Follow Guide  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Test Changes  │
│   Validate      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Submit PR     │
│   Wait Review   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Address       │
│   Feedback      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Merge! 🎉     │
└─────────────────┘
```

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git** installed and configured
- **GitHub account** with SSH keys set up
- **Text editor** with Markdown support (VS Code recommended)
- **Basic knowledge** of LLM/agentic systems
- **Familiarity** with the framework structure

### Initial Setup

1. **Fork the repository:**
   ```bash
   # Navigate to https://github.com/llm-agentic-rules/framework
   # Click "Fork" in the top right
   ```

2. **Clone your fork locally:**
   ```bash
   git clone git@github.com:YOUR_USERNAME/llm-agentic-rules.git
   cd llm-agentic-rules
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream git@github.com:llm-agentic-rules/framework.git
   ```

4. **Set up development environment:**
   ```bash
   # Install recommended VS Code extensions
   code --install-extension davidanson.vscode-markdownlint
   code --install-extension streetsidesoftware.code-spell-checker
   
   # Configure Git hooks (if available)
   npm install  # or your package manager equivalent
   ```

5. **Verify setup:**
   ```bash
   # Run validation script
   ./scripts/validate-setup.sh
   ```

### Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## Contribution Guidelines

### What Makes a Good Contribution?

A good contribution is:
- **Focused**: Addresses a single, specific issue or improvement
- **Well-Documented**: Includes clear descriptions and examples
- **Tested**: Validated against real-world scenarios
- **Aligned**: Follows existing patterns and conventions
- **Valuable**: Provides meaningful benefit to users

### Contribution Size Guidelines

| Size | Lines Changed | Examples | Review Time |
|------|---------------|----------|-------------|
| Small | < 50 lines | Typo fixes, clarifications | 1-2 days |
| Medium | 50-200 lines | New rules, expanded examples | 3-5 days |
| Large | 200-500 lines | New domain files, major rewrites | 1-2 weeks |
| Extra Large | > 500 lines | Multiple domains, architecture changes | 2-4 weeks |

### Before You Start

1. **Check existing issues** to avoid duplicate work
2. **Discuss significant changes** in an issue first
3. **Review similar contributions** for patterns
4. **Read the domain fundamentals** for context

## Domain Structure

### Standard Domain Organization

Each domain folder must contain exactly 7 files:

```
domain-name/
├── fundamentals.md      # Core concepts and basics
├── best-practices.md    # Recommended approaches
├── anti-patterns.md     # Patterns to avoid
├── checklist.md         # Verification checklist
├── examples.md          # Implementation examples
├── troubleshooting.md   # Common issues & solutions
└── advanced.md          # Advanced concepts
```

### File Purposes

| File | Content Type | Target Length |
|------|--------------|---------------|
| `fundamentals.md` | Definitions, concepts, architecture | 400+ lines |
| `best-practices.md` | Patterns, recommendations, standards | 400+ lines |
| `anti-patterns.md` | Warnings, pitfalls, corrections | 400+ lines |
| `checklist.md` | Actionable items, verification steps | 400+ lines |
| `examples.md` | Code snippets, configurations | 400+ lines |
| `troubleshooting.md` | Issues, diagnoses, resolutions | 400+ lines |
| `advanced.md` | Deep-dives, optimizations, edge cases | 400+ lines |

### Creating a New Domain

When proposing a new domain:

1. **Open a proposal issue** with:
   - Proposed domain name and number
   - Justification for the domain
   - Overview of the 7 files' content
   - Cross-domain relationships

2. **Wait for approval** from maintainers

3. **Create the domain** following the standard structure

4. **Submit for review** with all 7 files complete

## File Format

### Required Sections

All rule files must follow this format:

```markdown
# Domain Name - Task Type

> Brief description of this file's purpose (1-2 sentences)

## Overview

Detailed description of what this task covers, including:
- Scope and boundaries
- Target audience
- Prerequisites
- Related files

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

## Section 1

Content organized with clear hierarchy...

### Subsection 1.1

Additional details...

## Section 2

More content...

## Quick Reference

| Item | Description |
|------|-------------|
| ... | ... |

## See Also

- [Related File 1](./related-file-1.md)
- [Related File 2](./related-file-2.md)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial version |
```

### Markdown Formatting Rules

| Element | Format | Example |
|---------|--------|---------|
| Headers | ATX style with spacing | `## Header` |
| Lists | Hyphen for unordered, `1.` for ordered | `- Item` |
| Code blocks | Fenced with language | ` ```python ` |
| Links | Reference style preferred | `[text](url)` |
| Emphasis | Bold for important, italic for terms | `**bold**` |
| Tables | GFM tables | `\| col1 \| col2 \|` |
| Images | With alt text | `![alt text](path)` |

### Code Block Guidelines

```markdown
Good code block example:

​```python
def validate_rule(rule: dict) -> bool:
    """
    Validate a rule dictionary structure.
    
    Args:
        rule: Dictionary containing rule definition
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['id', 'name', 'description', 'priority']
    return all(key in rule for key in required_keys)
​```
```

## Naming Conventions

### Folder Naming

Domain folders follow this pattern:
```
XX-domain-name/
```

Where:
- `XX` = Two-digit number (01-99)
- `domain-name` = Lowercase, hyphen-separated

**Examples:**
- ✅ `01-core/`
- ✅ `02-security/`
- ✅ `10-compliance/`
- ❌ `core/` (missing number)
- ❌ `01_Core/` (wrong separator)
- ❌ `01-core-rules/` (too verbose)

### File Naming

Task files follow this pattern:
```
task-type.md
```

Where:
- `task-type` = One of the 7 standard types
- Lowercase, hyphen-separated

**Examples:**
- ✅ `fundamentals.md`
- ✅ `best-practices.md`
- ✅ `anti-patterns.md`
- ❌ `Fundamentals.md` (wrong case)
- ❌ `best_practices.md` (wrong separator)
- ❌ `bp.md` (abbreviation)

### Content Naming

Within files, use these conventions:

| Element | Convention | Example |
|---------|------------|---------|
| Rule IDs | `DOMAIN-TYPE-###` | `CORE-BP-001` |
| Section IDs | lowercase-hyphen | `#my-section` |
| Code variables | snake_case | `user_input` |
| Constants | UPPER_SNAKE | `MAX_TOKENS` |

## Writing Style Guide

### Voice and Tone

| Aspect | Guideline |
|--------|-----------|
| Voice | Active voice preferred |
| Tone | Professional but approachable |
| Perspective | Second person ("you") for instructions |
| Tense | Present tense for facts, future for outcomes |

### Writing Principles

1. **Be Clear**: Avoid jargon; define terms when necessary
2. **Be Concise**: One idea per sentence; one topic per paragraph
3. **Be Consistent**: Use the same terminology throughout
4. **Be Complete**: Don't assume prior knowledge
5. **Be Current**: Reflect latest best practices

### Example Rewrites

**Before:**
> In order to ensure that the system functions properly, it is recommended that users should validate their inputs before submission.

**After:**
> Validate all inputs before submission to ensure proper system function.

### Formatting for Readability

- Use **bullet points** for lists of 3+ items
- Use **tables** for structured comparisons
- Use **code blocks** for any code or commands
- Use **callouts** for important notes

```markdown
> ⚠️ **Warning**: This action cannot be undone.

> 💡 **Tip**: Use the `--dry-run` flag to preview changes.

> 📝 **Note**: This feature requires version 2.0 or later.
```

## Pull Request Process

### Before Submitting

#### Checklist

- [ ] Changes address a documented issue
- [ ] Code/docs follow style guidelines
- [ ] All new content has been self-reviewed
- [ ] Documentation updated if needed
- [ ] No unnecessary files included
- [ ] Commit messages follow conventions
- [ ] Branch is up-to-date with upstream

#### Pre-submission Validation

```bash
# Run validation script
./scripts/validate-pr.sh

# Check markdown formatting
npx markdownlint-cli "domains/**/*.md"

# Validate links
npx markdown-link-check README.md
```

### Submitting PRs

#### PR Title Format

```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Scopes: domain name or "core"
```

**Examples:**
- `feat(security): Add prompt injection prevention rules`
- `fix(core): Correct fundamentals formatting`
- `docs(readme): Update installation instructions`

#### PR Description Template

```markdown
## Description
Clear description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
How were these changes tested?

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests where applicable

## Related Issues
Fixes #123
Related to #456
```

### PR Review Criteria

Maintainers evaluate PRs against these criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Content is accurate and up-to-date |
| Completeness | 25% | All required sections included |
| Style | 15% | Follows formatting guidelines |
| Value | 20% | Provides meaningful benefit |
| Documentation | 10% | Includes clear explanations |

### Addressing Feedback

1. **Read carefully**: Understand all feedback before responding
2. **Respond to each point**: Address every comment
3. **Ask questions**: If feedback is unclear, ask for clarification
4. **Make targeted changes**: Don't change unrelated content
5. **Mark resolved**: Use "Resolve conversation" feature

## Issue Types

### Issue Labels

#### Domain Labels

| Label | Description |
|-------|-------------|
| `domain:core` | Core domain issues |
| `domain:security` | Security domain issues |
| `domain:development` | Development domain issues |
| `domain:data` | Data domain issues |
| `domain:integration` | Integration domain issues |
| `domain:operations` | Operations domain issues |
| `domain:testing` | Testing domain issues |
| `domain:documentation` | Documentation domain issues |
| `domain:performance` | Performance domain issues |
| `domain:compliance` | Compliance domain issues |

#### Type Labels

| Label | Description |
|-------|-------------|
| `enhancement` | New feature suggestions |
| `bug` | Bug reports |
| `documentation` | Documentation improvements |
| `question` | Questions and discussions |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |

#### Priority Labels

| Label | Description |
|-------|-------------|
| `priority:critical` | Blocking issues |
| `priority:high` | Important but not blocking |
| `priority:medium` | Normal priority |
| `priority:low` | Nice to have |

### Creating Effective Issues

**Bug Report Template:**
```markdown
## Description
Clear description of the issue.

## Location
File(s) affected: `domains/XX-name/file.md`
Section(s) affected: [Specific sections]

## Current Behavior
What currently happens.

## Expected Behavior
What should happen instead.

## Additional Context
Screenshots, references, etc.
```

**Feature Request Template:**
```markdown
## Problem Statement
What problem does this solve?

## Proposed Solution
How should this be addressed?

## Alternatives Considered
Other approaches you've thought of.

## Additional Context
Examples, references, etc.
```

## Development Setup

### Recommended Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| VS Code | Editor | [Download](https://code.visualstudio.com/) |
| markdownlint | Linting | `npm install -g markdownlint-cli` |
| Code Spell Checker | Spelling | VS Code extension |

### VS Code Settings

```json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
  "markdownlint.config": {
    "default": true,
    "MD013": false
  }
}
```

### Useful Scripts

```bash
# Validate all markdown files
find domains -name "*.md" -exec markdownlint {} \;

# Count lines in domain files
wc -l domains/*/*.md

# Check for broken links
npx markdown-link-check README.md
```

## Testing Guidelines

### What to Test

- **Link validation**: All internal and external links work
- **Formatting compliance**: Markdown is properly formatted
- **Content accuracy**: Information is correct and current
- **Cross-references**: Related files reference each other correctly

### Testing Checklist

```markdown
## Pre-Commit Tests
- [ ] All links validated
- [ ] Markdown formatted correctly
- [ ] No spelling errors
- [ ] Tables properly formatted
- [ ] Code blocks have language specified

## Domain Tests
- [ ] All 7 files present
- [ ] File naming correct
- [ ] Required sections included
- [ ] Cross-references valid

## Content Tests
- [ ] Information is accurate
- [ ] Examples are runnable
- [ ] No contradictions between files
```

## Documentation Standards

### Documentation Types

| Type | Location | Purpose |
|------|----------|---------|
| Framework docs | `README.md` | Project overview |
| Domain docs | `domains/*/` | Domain-specific content |
| Contributing docs | `CONTRIBUTING.md` | Contribution guidelines |
| API docs | `docs/api/` | API reference |

### Documentation Principles

1. **Write for your audience**: Consider reader's knowledge level
2. **Show, don't just tell**: Include examples and code
3. **Keep it updated**: Remove outdated information
4. **Link related content**: Help readers find more information

## Review Process

### Review Timeline

| PR Size | Initial Review | Follow-up Reviews |
|---------|----------------|-------------------|
| Small | 1-2 business days | Same day |
| Medium | 2-3 business days | 1 business day |
| Large | 3-5 business days | 2 business days |
| Extra Large | 1-2 weeks | 3 business days |

### Review Process Flow

```
PR Submitted → Automated Checks → Human Review → Feedback → Changes → Approval → Merge
```

### Reviewer Responsibilities

- Check for technical accuracy
- Verify style compliance
- Assess completeness
- Provide constructive feedback
- Approve or request changes

## Recognition Program

### Contributor Levels

| Level | Requirements | Benefits |
|-------|--------------|----------|
| Contributor | 1+ merged PRs | Listed in contributors file |
| Regular Contributor | 5+ merged PRs | Reviewer privileges |
| Core Contributor | 20+ merged PRs | Maintainer privileges |
| Domain Expert | Significant domain contributions | Domain ownership |

### Hall of Fame

Top contributors are recognized in:
- README.md acknowledgments
- Annual contributor report
- Community Discord roles

## Getting Help

### Support Channels

| Channel | Use For | Response Time |
|---------|---------|---------------|
| Discord | Quick questions | Minutes to hours |
| GitHub Discussions | In-depth questions | 1-2 days |
| GitHub Issues | Bug reports, features | 2-3 days |
| Email | Sensitive issues | 1-3 days |

### Asking Good Questions

1. **Search first**: Check existing discussions and issues
2. **Be specific**: Include relevant details and context
3. **Show effort**: Describe what you've already tried
4. **Be patient**: Maintainers are volunteers

### Resources

- **Documentation**: Start with `README.md` and domain fundamentals
- **Examples**: Review `examples.md` files in relevant domains
- **Community**: Join Discord for real-time help
- **Issues**: Search closed issues for similar problems

## Acknowledgments

Thank you to all contributors who help make this framework better!

### Contributors

We appreciate every contribution, whether it's:
- A single typo fix
- A new rule proposal
- An example submission
- A review comment
- A feature suggestion

### How to Get Acknowledged

All contributors are automatically added to our contributors file. Significant contributions may be highlighted in:
- Release notes
- Social media
- Community showcases

---

<p align="center">
  <strong>Your contributions make a difference!</strong>
</p>

<p align="center">
  <a href="https://github.com/llm-agentic-rules/framework/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=llm-agentic-rules/framework" alt="Contributors">
  </a>
</p>
