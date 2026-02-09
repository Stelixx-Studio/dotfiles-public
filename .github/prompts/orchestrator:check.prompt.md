<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/agents/data/commands.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/agents/ -->
---
name: agents:orchestrator:check
description: Run conflict assessment across active tracks
---
# Workflow: orchestrator:check

## AI Context
This is a specialized prompt for GitHub Copilot to execute the `agents:orchestrator:check` capability.
Execution logic is located in `.skt/shared/agents/`.

## Conductor Logic
Before starting, check the project state:
1. Read `ACTIVE_PLAN.md` (Beacon) to understand the current Track and Status.
2. If this task is part of the active plan, update the status using:
   - `orchestrator:task "Executing orchestrator:check" --status in-progress`
3. Upon completion:
   - Mark the task as done: `orchestrator:task "Completed orchestrator:check" --status completed`

## Execution
!python3 .skt/shared/agents/scripts/orchestrator_check.py $argv
