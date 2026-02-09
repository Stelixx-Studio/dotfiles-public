# ClaudeKit Database

This directory contains the workflow database for the monolithic ClaudeKit system.

## Files

### workflows.csv

Main workflow database containing all 31 workflows.

**Schema:**

- `id` - Unique workflow ID
- `name` - Workflow name (used in `/claudekit <name>`)
- `category` - Category (core, design, fix, git, docs, content, bootstrap, skill, other)
- `description` - Brief description
- `phases` - Phase names (pipe-separated)
- `tools` - Required tools (pipe-separated)
- `template` - Template file name (if any)
- `complexity` - Complexity level (low, medium, high)
- `auto_execution` - Auto-execution mode (1-3)

**Total:** 31 workflows

### phases.csv

Detailed phase definitions for each workflow.

**Schema:**

- `workflow_id` - References workflows.csv id
- `phase_order` - Execution order (1, 2, 3...)
- `phase_name` - Phase name
- `description` - Phase description
- `commands` - Commands to execute (semicolon-separated)
- `outputs` - Expected outputs

**Total:** 60+ phases

### best-practices.csv

Development best practices applicable to workflows.

**Schema:**

- `category` - Practice category (typescript, react, i18n, etc.)
- `practice` - Practice name
- `description` - Detailed description
- `applies_to` - Applicable workflows (pipe-separated)
- `priority` - Priority level (high, medium, low)

**Total:** 40 practices

## Usage

### Query Workflow

```bash
python3 ../scripts/query-workflow.py plan
```

Returns JSON with workflow metadata, phases, and best practices.

### List All Workflows

```bash
python3 ../scripts/query-workflow.py --list
```

Returns all workflows grouped by category.

## Adding New Workflow

1. **Add to workflows.csv:**

   ```csv
   32,my-workflow,core,"Description",Phase1|Phase2,tool1.sh,,medium,2
   ```

2. **Add phases to phases.csv:**

   ```csv
   32,1,Phase1,"Description","command1; command2","Output description"
   32,2,Phase2,"Description","","Output description"
   ```

3. **Add best practices (optional):**

   ```csv
   category,practice,"Description","my-workflow|other-workflow",high
   ```

4. **Test:**
   ```bash
   python3 ../scripts/query-workflow.py my-workflow
   ```

No prompt file changes needed!

## Maintenance

### Updating Workflow

Edit CSV files directly. Changes take effect immediately.

### Removing Workflow

1. Remove from workflows.csv
2. Remove phases from phases.csv
3. Update best practices if needed

### Data Validation

```bash
# Check CSV syntax
python3 -c "import csv; csv.DictReader(open('workflows.csv'))"
python3 -c "import csv; csv.DictReader(open('phases.csv'))"
python3 -c "import csv; csv.DictReader(open('best-practices.csv'))"
```

## Architecture

```
.shared/claudekit/
├── data/
│   ├── workflows.csv (31 workflows)
│   ├── phases.csv (60+ phases)
│   ├── best-practices.csv (40 practices)
│   └── README.md (this file)
└── scripts/
    └── query-workflow.py (query engine)

.github/prompts/
└── claudekit.prompt.md (monolithic prompt)
```

**Pattern:** Database-driven workflow system inspired by UI/UX Pro Max.

## Benefits

- ✅ Easy to add workflows (update CSV)
- ✅ No prompt file changes needed
- ✅ Consistent structure
- ✅ Scalable to 100+ workflows
- ✅ Version controlled
- ✅ Searchable and queryable

---

Last updated: 2026-01-05
Total workflows: 31
Total phases: 60+
Total practices: 40
