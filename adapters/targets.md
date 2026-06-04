# Adapter Targets

The framework targets 18 coding-agent and IDE assistant environments.

| # | Target | Primary Files |
|---|--------|---------------|
| 1 | Codex | `.codex-plugin/plugin.json`, `skills/llm-agentic-rules/SKILL.md` |
| 2 | Claude Code | `skills/`, `commands/`, `agents/` |
| 3 | OpenCode | `skills/llm-agentic-rules/SKILL.md`, `agents/` |
| 4 | KiloCode | framework instruction file, commands, and agent roles |
| 5 | Kimi Code | framework instruction file, commands, and agent roles |
| 6 | Hermes Agent | framework instruction file, commands, and agent roles |
| 7 | Aider | framework instruction file and command prompts |
| 8 | Gemini CLI | framework context file and command prompts |
| 9 | Goose | framework recipe/instruction |
| 10 | Cursor | project rules |
| 11 | Windsurf | workspace rules |
| 12 | Cline | custom instructions |
| 13 | Roo Code | modes and rules |
| 14 | Continue | assistant context |
| 15 | Zed | agent instruction context |
| 16 | Sourcegraph Cody | custom commands/context |
| 17 | GitHub Copilot | repository instructions |
| 18 | JetBrains AI | project guideline context |

## Common Payload

Every adapter should expose the same core behavior:

1. Identify the system type and risk tier.
2. Select the right framework domains.
3. Apply P0/P1 rules first.
4. Require tests and evidence for behavior-changing AI work.
5. Use templates for release, evaluation, incident, and compliance records.
