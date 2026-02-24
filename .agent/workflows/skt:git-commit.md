<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/claudekit/data/workflows.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/claudekit/ -->
---
description: Create conventional commit message
capability: common
---
# Workflow: git-commit

## AI Context
This workflow uses execution logic from `.skt/shared/claudekit/`.
Before execution, verify the project rules in `.agent/instructions.md`.


## Execution Instructions

> **Agent**: Antigravity — follow each phase sequentially using `run_command` for shell commands.
> **Template**: `.skt/shared/claudekit/templates/` (if applicable)
> **Artifact Dir**: Create artifacts in your brain directory using `write_to_file`.

### Phase 1: Analyze Changes
Analyze staged and unstaged changes

```bash
git status --porcelain
```
```bash
git diff --cached --stat
```

**Expected Output**: Changed files list

### Phase 2: Agentic Quality Assurance
Perform contextual quality checks and autonomous repair.

1. **Rule Discovery**: Load project standards and quality mandates.
   ```bash
   python3 .skt/shared/instructions/scripts/query-rules.py --tags project-rules,quality --format markdown
   ```
2. **Capability Analysis**: Check `package.json` and project structure to identify available quality tools.
3. **Execution**: Run `.skt/shared/claudekit/scripts/auto-check.sh`.
4. **Autonomous Fix**: If issues are found:
   - Analyze the specific error logs to identify failing files and root causes.
   - **Fix Everything**: Proactively fix all lint errors, warnings, and deprecated patterns using your coding tools.
   - **Alignment**: If a fix is ambiguous or potentially breaking, pause and align with the user.
   - **Verification**: Re-run Phase 2 until `auto-check.sh` returns success.

**Expected Output**: Clean verification. All fixable issues resolved.

### Phase 3: Generate Message
Create conventional commit message following format

**Expected Output**: Commit message

### Phase 4: Handle Changeset
Detect and generate changeset if needed

```bash
python3 .skt/shared/skt-core/scripts/smart-changeset.py
```

**Expected Output**: Changeset file

### Phase 5: Commit
Commit changes with message

```bash
git commit -m "$MESSAGE"
```

**Expected Output**: Commit hash

### Phase 6: Sync Beacon
Update project beacon for multi-agent visibility

```bash
skt orchestrator:sync
```

**Expected Output**: Beacon synchronized

