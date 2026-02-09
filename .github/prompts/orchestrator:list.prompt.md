<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
name: agents:orchestrator:list
description: Show active tracks dashboard
---
# Workflow: orchestrator:list

## AI Context
This is a specialized prompt for GitHub Copilot to execute the `agents:orchestrator:list` capability.
Execution logic is located in `.skt/shared/agents/`.

## Conductor Logic
Before starting, check the project state:
1. Read `ACTIVE_PLAN.md` (Beacon) to understand the current Track and Status.
2. If this task is part of the active plan, update the status using:
   - `orchestrator:task "Executing orchestrator:list" --status in-progress`
3. Upon completion:
   - Mark the task as done: `orchestrator:task "Completed orchestrator:list" --status completed`

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_list.py $argv
