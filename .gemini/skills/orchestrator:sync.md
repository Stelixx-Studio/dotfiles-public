<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
description: Update ACTIVE_PLAN.md beacon
---
# Workflow: orchestrator:sync

## AI Context
This workflow executes the `agents:orchestrator:sync` capability from `.skt/shared/agents/`.
Before execution, verify the project rules in `.agent/instructions.md`.

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_sync.py $argv
