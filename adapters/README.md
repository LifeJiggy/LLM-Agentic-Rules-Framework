# Agentic CLI And IDE Adapters

This directory makes the framework portable across coding agents and IDE assistants. It follows the same shape seen in the Claude reference projects:

- skill-style reusable instructions;
- slash-command-style task prompts;
- specialized agent profiles;
- install scripts;
- always-on rule references;
- cross-platform setup notes.

## Supported Targets

| Target | Mode | Adapter Strategy |
|--------|------|------------------|
| Codex | Plugin | `.codex-plugin/plugin.json` plus `skills/` |
| Claude Code | Skills and commands | Copy `skills/`, `commands/`, and optional `agents/` |
| OpenCode | Agent instructions | Reference `skills/llm-agentic-rules/SKILL.md` and commands |
| KiloCode | Agent instructions | Copy framework skill, commands, docs, and agent roles |
| Kimi Code | Agent instructions | Copy framework skill, commands, docs, and agent roles |
| Hermes Agent | Agent instructions | Copy framework skill, commands, docs, and agent roles |
| Aider | Repo convention | Add framework instruction file to project root or `.aider` docs |
| Gemini CLI | Context file | Reference framework skill and command prompts |
| Goose | Recipe/instruction | Use skill as recipe and agents as roles |
| Cursor | IDE rules | Convert skill to project rules |
| Windsurf | IDE rules | Convert skill to workspace rules |
| Cline | Custom instructions | Use skill and command prompts as custom instructions |
| Roo Code | Mode rules | Use agents as modes and skill as shared rules |
| Continue | Assistant context | Add skill and domain docs as context |
| Zed | Agent instructions | Add framework instruction reference |
| Sourcegraph Cody | Custom commands/context | Add command prompts and framework docs |
| GitHub Copilot | Repository instructions | Add framework guidance as repo instructions |
| JetBrains AI | Project guidelines | Add framework guidance as project context |

## Install

Dry run first:

```bash
python scripts/install_agent_adapters.py --target all --dry-run
```

Apply for one target:

```bash
python scripts/install_agent_adapters.py --target claude-code --apply
```

Apply for all known targets:

```bash
python scripts/install_agent_adapters.py --target all --apply
```

The installer is conservative. It creates backups before overwriting files and supports Windows, macOS, and Linux path conventions.

## Installer Enhancements

- List supported targets with `--list-targets`.
- Install one component group with `--component skill`, `--component commands`, `--component agents`, `--component docs`, or `--component codex`.
- Redirect installs into a staging directory with `--target-root ./adapter-preview`.
- Skip files whose content is already identical.
- Create timestamped backups before overwriting by default.
- Disable backups explicitly with `--no-backup`.
- Stop after the first write failure with `--fail-fast`.
- Print a final summary of planned, copied, skipped, and failed files.

Examples:

```bash
python scripts/install_agent_adapters.py --list-targets
python scripts/install_agent_adapters.py --target all --component skill --dry-run
python scripts/install_agent_adapters.py --target claude-code --target-root ./adapter-preview --apply
python scripts/install_agent_adapters.py --target all --apply --fail-fast
```

## Safety Model

- The installer refuses to write unless `--apply` is passed.
- Dry-run mode is the expected first step.
- Existing files are backed up with timestamped `.bak` suffixes before overwrite.
- Existing directories and symlink destinations are refused instead of overwritten.
- Changed files are written through a temporary file and atomically replaced.
- Installer source files are checked before the run starts.
- Any failed copy returns a non-zero process exit code.
- The adapter payload is documentation and prompt content only; it does not install external binaries.

## Recovery Playbook

1. Re-run the command with `--dry-run` and the same targets.
2. Check the final summary for failed operations.
3. Restore any overwritten file from the adjacent `.bak` file if needed.
4. Re-run with `--fail-fast` after fixing permissions or path conflicts.
5. Use `--target-root ./adapter-preview` to reproduce the install without touching live tool config.

## Manual Use

If a tool does not support plugins directly, paste or reference:

- `skills/llm-agentic-rules/SKILL.md` as the main instruction;
- `commands/rules-audit.md`, `commands/rules-plan.md`, and `commands/rules-release.md` as command prompts;
- `agents/*.md` as role profiles;
- `docs/checklist-packs.md` to pick the right review pack.
