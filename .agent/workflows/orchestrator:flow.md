<!-- 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/claudekit/data/workflows.csv -->
<!-- 💡 AI Navigation: Shared resources are at .skt/shared/claudekit/ -->
---
description: Coordinate multiple agents into strict Plan-Approve-Execute protocol
capability: advanced
---
# Workflow: orchestrator:flow

## AI Context
This workflow uses execution logic from `.skt/shared/claudekit/`.
Before execution, verify the project rules in `.agent/instructions.md`.


### Phase 1: Context & Planning
1. **Load Context**:
   !python3 .skt/shared/workflows/scripts/context_loader.py

2. **Check Beacon**:
   - Read `ACTIVE_PLAN.md` to identify the current Track and Status.
   - If no active track, run `orchestrator:new "<goal>"` to initialize one.

3. **Analyze Request**:
   - If User Request is complex, check the linked Plan in `ACTIVE_PLAN.md`.
   - If NO Plan exists in the Track:
     - Activate `skt:plan` logic.
     - **STOP** and ask for User Approval.
   - If Plan Exists:
     - Update Track Status: `orchestrator:status "Executing Phase X"`
     - Proceed to Phase 2.

### Phase 2: Execution (Orchestration)
1. **Execute**:
   - Call `skt:cook` (or relevant sub-workflows) to implement the changes.
   - Pass the full context (Plan + Project State).

2. **Update Progress**:
   - After each significant step, update the Track:
   - `orchestrator:task "Completed X" --status completed`

3. **Exit Gate (Verification)**:
   - **MANDATORY**: Verify the implementation.
   - Run `npm run lint` (or project equivalent).
   - Run `npm test` (if available).
   - Only complete the task if checks PASS.

## Execution
!python3 .skt/shared/claudekit/scripts/query-workflow.py orchestrator:flow $argv
