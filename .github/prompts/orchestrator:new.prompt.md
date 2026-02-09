<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
name: agents:orchestrator:new
description: Start new track with auto-conflict detection
---
# Workflow: orchestrator:new

## AI Context
This is a specialized prompt for GitHub Copilot to execute the `agents:orchestrator:new` capability.
Execution logic is located in `.skt/shared/agents/`.

## Conductor Logic
Before starting, check the project state:
1. Read `ACTIVE_PLAN.md` (Beacon) to understand the current Track and Status.
2. If this task is part of the active plan, update the status using:
   - `orchestrator:task "Executing orchestrator:new" --status in-progress`
3. Upon completion:
   - Mark the task as done: `orchestrator:task "Completed orchestrator:new" --status completed`

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_new.py $argv
