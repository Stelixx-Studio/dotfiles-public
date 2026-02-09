<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
description: Run conflict assessment across active tracks
---
# Workflow: orchestrator:check

## AI Context
This workflow executes the `agents:orchestrator:check` capability from `.skt/shared/agents/`.
Before execution, verify the project rules in `.agent/instructions.md`.

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_check.py $argv
