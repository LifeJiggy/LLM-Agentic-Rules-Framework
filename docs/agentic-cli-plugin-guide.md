# Agentic CLI And IDE Plugin Guide

This guide explains how to use the framework as a portable plugin or instruction pack for coding agents and IDE assistants.

The adapter model follows the useful conventions from the Claude reference projects:

- `skills/` for reusable capability instructions;
- `commands/` for slash-command prompts;
- `agents/` for specialized roles;
- install scripts for user-level setup;
- always-on rules and safety checks.

## Supported Targets

| Target | Support Type |
|--------|--------------|
| Codex | Native plugin manifest plus skill |
| Claude Code | Skill and command files |
| OpenCode | Instruction and agent files |
| Aider | Instruction pack |
| Gemini CLI | Context/instruction pack |
| Goose | Recipe/instruction pack |
| Cursor | Project rule pack |
| Windsurf | Workspace rule pack |
| Cline | Custom instruction pack |
| Roo Code | Mode and rules pack |
| Continue | Assistant context pack |
| Zed | Agent instruction pack |
| Sourcegraph Cody | Custom command/context pack |
| GitHub Copilot | Repository instruction pack |
| JetBrains AI | Project guideline pack |

## Core Files

- `.codex-plugin/plugin.json`
- `skills/llm-agentic-rules/SKILL.md`
- `commands/rules-audit.md`
- `commands/rules-plan.md`
- `commands/rules-release.md`
- `agents/rules-architect.md`
- `agents/rules-reviewer.md`
- `agents/rules-release-gate.md`
- `adapters/manifest.json`
- `scripts/install_agent_adapters.py`

## Install Preview

Always preview first:

```bash
python scripts/install_agent_adapters.py --target all --dry-run
```

List supported targets:

```bash
python scripts/install_agent_adapters.py --list-targets
```

Install for Claude Code:

```bash
python scripts/install_agent_adapters.py --target claude-code --apply
```

Install for Codex:

```bash
python scripts/install_agent_adapters.py --target codex --apply
```

Install for all supported targets:

```bash
python scripts/install_agent_adapters.py --target all --apply
```

Install only the shared skill:

```bash
python scripts/install_agent_adapters.py --target all --component skill --apply
```

Stop on the first install error:

```bash
python scripts/install_agent_adapters.py --target all --apply --fail-fast
```

Stage an install into a review directory:

```bash
python scripts/install_agent_adapters.py --target all --target-root ./adapter-preview --apply
```

## Reliability And Recovery

- The installer validates its source payload before planning an install.
- Dry-run mode reports the same target paths without writing files.
- Existing files are copied only when content changes.
- Overwrites use timestamped backups unless `--no-backup` is passed.
- Writes are staged through a temporary file and then replaced atomically.
- Destination directories and symlink targets are rejected to prevent unsafe overwrite behavior.
- Failed copy operations are counted in the final summary and return a non-zero exit code.
- Use `--fail-fast` in CI or managed rollouts when partial adapter installation is unacceptable.
- Use `--target-root` to stage an install for review before copying into user config directories.
- Roll back by restoring the matching `.bak` file beside the overwritten target.

## Windows, macOS, And Linux

The installer uses Python's `Path.home()` and standard config directories:

- Windows: user profile paths such as `%USERPROFILE%\.claude` and `%USERPROFILE%\.cursor`.
- macOS/Linux: home and `.config` paths such as `~/.claude`, `~/.config/opencode`, and `~/.continue`.

If a tool uses project-local configuration in your environment, run the installer in dry-run mode and copy the generated files into that project-specific location.

## Adapter Review Checklist

- [ ] Run `--dry-run` before `--apply`.
- [ ] Confirm the target paths match your tool's expected config location.
- [ ] Use `--component skill` when the target only supports one instruction file.
- [ ] Use `--target-root` to package adapters for another machine or team.
- [ ] Keep backups unless you are running in a disposable staging directory.
- [ ] Use `--fail-fast` for release automation or fleet setup.
- [ ] Confirm the final summary has `failed 0` before treating the install as complete.

## Recommended Commands

- `rules-audit`: review a repository against the framework.
- `rules-plan`: plan AI, agentic, RAG, MCP, or coding-agent work.
- `rules-release`: run a production readiness gate.

## Recommended Agents

- `rules-architect`: design and risk-tier systems.
- `rules-reviewer`: review implementation, tests, and evidence.
- `rules-release-gate`: decide pass, conditional pass, or block before release.
