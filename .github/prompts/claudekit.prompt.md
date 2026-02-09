---
name: skt
description: "Comprehensive development workflow system with 31+ workflows for planning, coding, testing, design, git, docs, and deployment"
agent: "agent"
---

# skt

Development workflow intelligence system with database-driven workflow management.

**31 workflows available** across 8 categories: core, design, fix, git, docs, content, bootstrap, skill

## Prerequisites

Check Python installation:

```bash
python3 --version || python --version
```

If not installed, install based on OS:

- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt update && sudo apt install python3`
- **Windows**: `winget install Python.Python.3.12`

---

## How to Use

Invoke with workflow name and description:

```
/skt plan "authentication system"
/skt cook "user dashboard component"
/skt fix "login timeout bug"
/skt design-fast "landing page mockup"
```

**Syntax**: `/skt <workflow> <description>` or `/skt:<workflow> <description>`

Both space and colon separators are supported.

---

## Quick Start Example

**User types:** `/skt:cook "login form"`

**AI executes:**

1. **Detect**: Parse workflow name `cook` and description `login form`
2. **Load**: Read `.agent/workflows/skt:cook.md`
3. **Query**: Run `python3 .skt/shared/skt/scripts/query-workflow.py cook`
4. **Display**: Show workflow info (name, description, phases)
5. **Execute Phases**:
   - Phase 1: Research - Run `parallel-research.sh "implementation patterns for: login form"`
   - Phase 2: Context - Run `query-rules.py --workflow cook --format markdown`
   - Phase 3: Structure - Run `find apps/web/features -type d | head -10`
   - Phase 4: Plan - Create implementation strategy
   - Phase 5: Implement - Write code following all rules
   - Phase 6: Test - Run `pnpm i18n:compile && pnpm test && pnpm tsc --noEmit && pnpm lint`
   - Phase 7: Review - Run `auto-check.sh` and verify quality
6. **Best Practices**: Show checklist of all applicable rules
7. **Output**: Deliver implemented feature with tests

**Result**: Complete, tested, production-ready login form component

---

## Available Workflows

### Core Workflows (6)

- **plan** - Create implementation plan with research
- **cook** - Implement feature with testing
- **code** - Execute existing plan
- **review** - Code review against standards
- **test** - Run test suite and report
- **brainstorm** - Explore solution approaches

### Design Workflows (4)

- **design** - UI/UX dispatcher
- **design-fast** - Quick mockups
- **design-good** - Production quality design
- **design-3d** - 3D component design

### Fix Workflows (6)

- **fix** - General bug fix
- **fix-fast** - Quick fix
- **fix-hard** - Complex bug fix
- **fix-ci** - Fix CI/CD issues
- **fix-logs** - Fix from error logs
- **fix-test** - Fix failing tests

### Git Workflows (4)

- **git-commit** - Create commit message
- **git-commit-push** - Commit and push
- **git-pr** - Create pull request
- **git-cherry-pick** - Cherry-pick commits

### Docs Workflows (3)

- **docs-init** - Initialize docs
- **docs-summarize** - Summarize docs
- **docs-update** - Update docs

### Content Workflows (2)

- **content-good** - Marketing copy
- **content-cro** - Conversion optimization

### Bootstrap Workflows (2)

- **bootstrap** - Bootstrap new project
- **bootstrap-auto** - Autonomous bootstrap

### Skill Workflows (3)

- **skill** - Create/optimize skill
- **skill-create** - Create new skill
- **skill-optimize** - Optimize skill

### Other (1)

- **ask** - Context-aware Q&A

---

## Step 1: Detect and Execute Workflow

**CRITICAL**: When user invokes a workflow with `/skt:workflow` or `/skt workflow`, you MUST:

1. **Parse workflow name** from user input:
   - From `/skt:fix-hard` → extract `fix-hard`
   - From `/skt fix-hard "bug description"` → extract `fix-hard`
   - Description is everything after workflow name

2. **Check if workflow file exists**:
   - Look for `.agent/workflows/skt:{workflow}.md`
   - Example: `.agent/workflows/skt:fix-hard.md`

3. **If workflow file exists**:
   - **Load and read the workflow file**
   - Execute the command inside (usually `!python3 .skt/shared/skt/scripts/query-workflow.py {workflow} "$@"`)
   - Replace `$@` with user's description
   - Continue to Step 2

4. **If workflow file doesn't exist**:
   - Show error: "Workflow '{workflow}' not found"
   - List available workflows
   - Exit

**Example detection:**
- User types: `/skt:cook`
- AI detects: workflow = `cook`, description = (none)
- AI loads: `.agent/workflows/skt:cook.md`
- AI executes: `python3 .skt/shared/skt/scripts/query-workflow.py cook`

---

## Step 2: Load Workflow Data

After detecting workflow invocation, load workflow data by running the command from the workflow file:

```bash
python3 .skt/shared/skt/scripts/query-workflow.py {workflow}
```

**The script returns JSON with:**

- `workflow` - Metadata (name, description, complexity, auto_execution, tools)
- `phases` - Array of phases with order, name, description, commands, outputs
- `best_practices` - Array of applicable rules with category, practice, description, priority
- `metadata` - Summary (total_phases, total_practices, has_research, has_template)

**Process the JSON:**
1. Parse the JSON output
2. Extract workflow metadata
3. Extract phases array
4. Extract best practices

**If query fails:**
- Show error message
- List available workflows (run with `--list` flag)
- Exit

---

## Step 3: Display Workflow Info

Show workflow information to user:

```
🔧 Workflow: {name}
📝 Description: {description}
⚡ Complexity: {complexity}
📊 Phases: {total_phases}
✅ Best Practices: {total_practices}
```

**Important**: Always display this header before executing phases.

---

---

## Rule-First Framework (CRITICAL)

**Rule**: AI agents must treat project instructions as "Executive Code" to follow, not just "Passive Documentation".

### Risk Levels
Before starting any task, identify its **Risk Level** to determine the level of governance required:

| Risk Level | Category | Requirement |
|------------|----------|-------------|
| **Level 1** | Infrastructure (Docker, VPS, Nginx, CI/CD) | **High Risk**: Mandatory Architecture Audit + Research Doc. |
| **Level 2** | API, DB, Auth, Core Logic, I18n | **Medium Risk**: Mandatory Rule Compliance Audit in Plan. |
| **Level 3** | UI, Styling, Docs, Utils, Content | **Low Risk**: Standard Rule Loading. |

### Mandatory Rule Audit (Phase 1)
For Level 1 and Level 2 tasks, you MUST perform an active **Rule Audit**:
1. Run `python3 .shared/instructions/scripts/query-rules.py --workflow <name>`.
2. List the 3 most critical rules identified for the task.
3. Explicitly state how your implementation complies with these rules in your plan.

---

## How Workflows Load Context

All workflows now use **CSV database-driven context loading**:

**Phase 1 (Audit & Context Loading)**:

```bash
python3 .shared/instructions/scripts/query-rules.py --workflow <name> --format markdown
```

This loads:

- ✅ Relevant coding rules matching the task's context
- ✅ Quick decision trees for architecture
- ✅ Best practices grouped by priority
- ✅ Project-specific patterns (Design System, etc.)

**Governance**: Use the output above to categorize the **Risk Level** and list mandatory rules.

---

## Step 4: Execute Workflow Phases

**CRITICAL**: Execute ALL phases in order. For each phase:

### Phase Execution Pattern

**1. Display Phase Header**

```markdown
## Phase {order}: {phase_name}

{phase_description}
```

**2. Execute Phase Commands** (if any)

**Parse and run commands from the `commands` array:**

- Remove leading `!` if present
- Replace `$1` or `$@` with user's description (if provided)
- Run each command using `run_in_terminal` tool
- Commands separated by `;` should be run in sequence

**Example phase commands:**
```json
"commands": [
  "python3 .shared/instructions/scripts/query-rules.py --workflow cook --format markdown",
  "find apps/web/features -type d | head -10"
]
```

**Execution:**
```bash
# Command 1
python3 .shared/instructions/scripts/query-rules.py --workflow cook --format markdown

# Command 2
find apps/web/features -type d | head -10
```

**If command contains `$1` and user provided description:**
```json
"commands": ["parallel-research.sh \"implementation patterns for: $1\""]
```

**Replace $1:**
```bash
# User invoked: /skt:cook "authentication system"
# Execute:
parallel-research.sh "implementation patterns for: authentication system"
```

**3. Collect and Display Outputs**

After executing commands, show outputs:

```markdown
**Command Outputs:**
{outputs from executed commands}
```

**4. Perform Phase Work**

Based on phase description and outputs:
- **Context/Research phases**: Load and display the information
- **Planning phases**: Create detailed plans
- **Implementation phases**: Write code following all rules
- **Testing phases**: Run tests and show results
- **Review phases**: Verify quality and show checklist

**5. Pass Context to Next Phase**

Maintain all context from previous phases for use in subsequent phases.

---

## Step 5: Apply Best Practices

After executing all phases, display applicable best practices:

```
## 📋 Best Practices Checklist

Review these practices for this workflow:
```

Group by priority (high → medium → low):

**High Priority:**

- [ ] {practice} - {description}

**Medium Priority:**

- [ ] {practice} - {description}

**Low Priority:**

- [ ] {practice} - {description}

---

## Step 6: Generate Output

Format final output based on workflow type:

### For Planning Workflows (plan, brainstorm)

Save to file:

```
plans/YYMMDD-HHmm-{feature-name}.md
```

### For Implementation Workflows (cook, code)

- Implement code following all rules
- Run quality checks
- Display verification checklist

### For Review Workflows (review, test)

- Generate review report
- Display checklist
- No code changes

### For Fix Workflows (fix-\*)

- Implement fix
- Run tests
- Verify fix resolves issue

### For Git Workflows (git-\*)

- **Changeset Handling**:
  - ALWAYS check for `.changeset` directory.
  - If present, map changed files to packages and generate a changeset file.
  - **Rules**:
    - Use `patch` for `fix:`, `minor` for `feat:`.
    - Never create empty changesets.
    - Write the file directly using `write_to_file`.
- Generate commit message/PR description
- Execute git commands (if auto-execution enabled)

### For Docs Workflows (docs-\*)

- Update/create documentation
- Verify completeness

---

## Example Workflows

### Example 1: Planning

**Input:**

```
/skt plan "user authentication with OAuth"
```

**Execution:**

1. Query database → Get "plan" workflow
2. Phase 1: Context → Load rules via query-rules.py
3. Phase 2: Structure → Load project structure
4. Phase 3: Analyze → Combine context with requirements
5. Phase 4: Plan → Create detailed plan
6. Phase 5: Verify → Load auto-check template
7. Apply best practices → Show checklist
8. Save to `plans/260105-1015-user-auth.md`

---

### Example 2: Implementation

**Input:**

```
/skt cook "login form component"
```

**Execution:**

1. Query database → Get "cook" workflow
2. Phase 1: Context → Load rules via query-rules.py
3. Phase 2: Structure → Load project directory structure
4. Phase 3: Plan → Create implementation strategy
5. Phase 4: Implement → Write code following rules
6. Phase 5: Test → Run i18n:compile, test, tsc, lint
7. Phase 6: Review → Load auto-check.sh
8. Apply best practices → Verify all rules
9. Display verification results

---

### Example 3: Bug Fix

**Input:**

```
/skt fix-hard "session timeout after 5 minutes"
```

**Execution:**

1. Query database → Get "fix-hard" workflow
2. Phase 1: Context → Load debugging rules via query-rules.py
3. Phase 2: Analyze → Deep analysis of bug
4. Phase 3: Debug → Detailed investigation
5. Phase 4: Fix → Implement comprehensive fix
6. Phase 5: Test → Thorough testing
7. Phase 6: Verify → Check for regressions
8. Apply best practices → Security, error handling
9. Display fix summary

---

## Workflow Customization

### Auto-Execution Mode

Each workflow has `auto_execution` level (1-3):

- **1** - Manual confirmation for each step
- **2** - Auto-execute safe commands
- **3** - Fully autonomous execution

### Template Usage

If workflow has template:

- Load template from `.shared/skt/templates/`
- Use as structure for output
- Fill in with workflow results

### Tool Integration

Workflows can use these tools:

- `query-rules.py` - CSV database query engine (context loading)
- `auto-check.sh` - Quality verification
- `generate_image` - Image generation
- Custom scripts in `.shared/skt/scripts/`

---

## Database Management

### Adding New Workflow

1. Add entry to `.shared/skt/data/workflows.csv`
2. Define phases in `.shared/skt/data/phases.csv`
3. Add best practices if needed
4. **No prompt file changes needed!**

### Updating Workflow

1. Edit CSV files
2. Changes take effect immediately
3. No deployment needed

### Querying Workflows

List all workflows:

```bash
!python3 .shared/skt/scripts/query-workflow.py --list
```

Query specific workflow:

```bash
!python3 .shared/skt/scripts/query-workflow.py plan
```

---

## Error Handling

### Workflow Not Found

```
❌ Error: Workflow 'xyz' not found

Available workflows:
- Core: plan, cook, code, review, test, brainstorm
- Design: design, design-fast, design-good, design-3d
- Fix: fix, fix-fast, fix-hard, fix-ci, fix-logs, fix-test
...

Usage: /skt <workflow> <description>
```

### Missing Description

```
⚠️ Warning: No description provided

Usage: /skt {workflow} <description>
Example: /skt plan "user authentication"
```

### Command Execution Error

```
❌ Error executing command: {command}
Error: {error_message}

Continuing with next phase...
```

---

## Quality Assurance

All workflows follow project standards:

- ✅ TypeScript strict mode
- ✅ No `any` types
- ✅ Server Components by default
- ✅ kebab-case file naming
- ✅ Absolute imports (@/)
- ✅ i18n for all user-facing text
- ✅ Accessibility (WCAG AA)
- ✅ Error handling
- ✅ Testing (80%+ coverage)
- ✅ Security best practices

---

## Tips

**For best results:**

1. Be specific in descriptions
2. Include context when relevant
3. Review best practices checklist
4. Run quality checks before committing
5. Use appropriate workflow for task

**Common patterns:**

- Planning → `/skt plan`
- Quick implementation → `/skt cook`
- Following existing plan → `/skt code`
- Bug fixing → `/skt fix` or `/skt fix-hard`
- Code review → `/skt review`
- Design work → `/skt design-fast` or `/skt design-good`

---

**Powered by SKT Database** - 31 workflows, infinitely extensible
