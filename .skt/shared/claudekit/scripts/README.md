# Parallel Research Script

Helper script for running parallel research using GitHub Copilot CLI.

## Usage

```bash
.agent/workflows/scripts/parallel-research.sh "feature description"
```

## What It Does

1. Spawns 3 parallel Copilot CLI queries:

   - Best practices
   - Common patterns
   - Security considerations

2. Aggregates results

3. Outputs combined research

## Requirements

- GitHub CLI: `brew install gh`
- Copilot extension: `gh extension install github/gh-copilot`
- Authenticated: `gh auth login`

## Fallback

If Copilot CLI not available, shows installation instructions and exits gracefully.
