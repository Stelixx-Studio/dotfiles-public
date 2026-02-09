# Slash Commands & Workflows

Reference for using the project's AI-driven workflows via ClaudeKit.

## Core Workflow: ClaudeKit

All capabilities are centralized under the `@[/claudekit]` workflow.

**Usage**: `@[/claudekit] <command> <input>`

### Available Commands

| Command | Purpose |
|---------|---------|
| `ask`   | Ask questions about the codebase (context-aware) |
| `plan`  | detailed implementation plan |
| `prioritize` | prioritization plan |
| `cook`  | Implement features/code based on plan |
| `fix`   | Debug and fix issues |
| `fix-hard` | Deep debugging for complex/hard issues |
| `learn` | Update instructions/knowledge base |
| `review` | Code review and feedback |
| `test` | Generate and run tests |

### Examples

```bash
# Planning a new feature
@[/claudekit] plan "Add user profile settings"

# Implementing code
@[/claudekit] cook "Implement profile form component"

# Fixing a bug
@[/claudekit] fix "Profile image upload fails with 403"

# Hard fix (deep analysis)
@[/claudekit] fix-hard "Memory leak in data table"

# Asking questions
@[/claudekit] ask "How does the auth flow work?"
```

## Adding Custom Workflows

You can add project-specific workflows in `.agent/workflows/`.

1. Create a markdown file: `.agent/workflows/my-workflow.md`
2. Define the workflow steps
3. Invoke it: `@[/my-workflow]`

---

**Version**: 1.1.1 (Monorepo Aware)
