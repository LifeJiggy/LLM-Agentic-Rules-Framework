# Adapter Targets

The framework targets 15 coding-agent and IDE assistant environments.

| # | Target | Primary Files |
|---|--------|---------------|
| 1 | Codex | `.codex-plugin/plugin.json`, `skills/llm-agentic-rules/SKILL.md` |
| 2 | Claude Code | `skills/`, `commands/`, `agents/` |
| 3 | OpenCode | `skills/llm-agentic-rules/SKILL.md`, `agents/` |
| 4 | Aider | framework instruction file and command prompts |
| 5 | Gemini CLI | framework context file and command prompts |
| 6 | Goose | framework recipe/instruction |
| 7 | Cursor | project rules |
| 8 | Windsurf | workspace rules |
| 9 | Cline | custom instructions |
| 10 | Roo Code | modes and rules |
| 11 | Continue | assistant context |
| 12 | Zed | agent instruction context |
| 13 | Sourcegraph Cody | custom commands/context |
| 14 | GitHub Copilot | repository instructions |
| 15 | JetBrains AI | project guideline context |

## Common Payload

Every adapter should expose the same core behavior:

1. Identify the system type and risk tier.
2. Select the right framework domains.
3. Apply P0/P1 rules first.
4. Require tests and evidence for behavior-changing AI work.
5. Use templates for release, evaluation, incident, and compliance records.
