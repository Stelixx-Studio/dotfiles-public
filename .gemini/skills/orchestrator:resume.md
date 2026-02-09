<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
description: Smart session recovery and warm-up
---
# Workflow: orchestrator:resume

## AI Context
This workflow executes the `agents:orchestrator:resume` capability from `.skt/shared/agents/`.
Before execution, verify the project rules in `.agent/instructions.md`.

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_resume.py $argv
