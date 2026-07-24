# Adapter Targets

The framework targets 18 coding-agent and IDE assistant environments.

## Target List

| # | Target | Config File | Primary Files |
|---|--------|-------------|---------------|
| 1 | Codex | `.codex-plugin/plugin.json` | `skills/`, `agents/` |
| 2 | Claude Code | `.claude/settings.json` | `skills/`, `commands/`, `agents/` |
| 3 | OpenCode | `.opencode/config.json` | `skills/`, `agents/` |
| 4 | KiloCode | `.kilocode/config.json` | Framework instruction file, commands, agent roles |
| 5 | Kimi Code | `.kimi/config.json` | Framework instruction file, commands, agent roles |
| 6 | Hermes Agent | `.hermes/config.json` | Framework instruction file, commands, agent roles |
| 7 | Aider | `.aider.conf.yml` | Framework instruction file and command prompts |
| 8 | Gemini CLI | `.gemini/config.json` | Framework context file and command prompts |
| 9 | Goose | `.goose/config.yaml` | Framework recipe/instruction |
| 10 | Cursor | `.cursorrules` | Project rules |
| 11 | Windsurf | `.windsurfrules` | Workspace rules |
| 12 | Cline | `.cline/rules.md` | Custom instructions |
| 13 | Roo Code | `.roo/config.json` | Modes and rules |
| 14 | Continue | `.continue/config.json` | Assistant context |
| 15 | Zed | `.zed/settings.json` | Agent instruction context |
| 16 | Sourcegraph Cody | `.cody/config.json` | Custom commands/context |
| 17 | GitHub Copilot | `.github/copilot-instructions.md` | Repository instructions |
| 18 | JetBrains AI | `.jb/project.json` | Project guideline context |

## CLI Integration

Install adapters using the CLI:

```bash
# List all available targets
python scripts/cli.py list

# Preview installation
python scripts/cli.py install --target claude-code --dry-run

# Install for specific target
python scripts/cli.py install --target claude-code --apply

# Install specific component
python scripts/cli.py install --target all --component skill --apply

# Install with fail-fast mode
python scripts/cli.py install --target all --apply --fail-fast
```

## Common Payload

Every adapter should expose the same core behavior:

1. Identify the system type and risk tier
2. Select the right framework domains
3. Apply P0/P1 rules first
4. Require tests and evidence for behavior-changing AI work
5. Use templates for release, evaluation, incident, and compliance records

## Target Configuration

Each target has specific configuration requirements:

| Target | Config Location | Skill Format | Agent Format |
|--------|-----------------|--------------|--------------|
| Codex | `.codex-plugin/plugin.json` | SKILL.md | Markdown files |
| Claude Code | `.claude/settings.json` | SKILL.md | Markdown files |
| Cursor | `.cursorrules` | Plain text | Plain text |
| Windsurf | `.windsurfrules` | Plain text | Plain text |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown | N/A |

## Installation Methods

### Method 1: CLI (Recommended)

```bash
python scripts/cli.py install --target <target> --apply
```

### Method 2: Python Script

```bash
python scripts/install_agent_adapters.py --target <target> --apply
```

### Method 3: PowerShell

```powershell
.\scripts\validate-framework.ps1 -Install
```

### Method 4: Bash

```bash
./scripts/setup.sh --install
```
