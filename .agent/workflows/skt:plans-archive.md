<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/claudekit/data/workflows.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/claudekit/ -->
---
description: Archive completed implementation plans
capability: common
---
# Workflow: plans-archive

## AI Context
This workflow uses execution logic from `.skt/shared/claudekit/`.
Before execution, verify the project rules in `.agent/instructions.md`.


### 1. Context
!python3 .skt/shared/workflows/scripts/context_loader.py

## Execution
!python3 .skt/shared/claudekit/scripts/query-workflow.py plans-archive $argv
