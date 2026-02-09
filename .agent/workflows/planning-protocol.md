# Technical Planning Protocol

This protocol defines how implementation plans should be created, managed, and linked to the project's documentation.

---

## Planning Lifecycle & Synergies

### 1. Initialization (`skt:plan` / `skt:plans-init`)
- **Action**: Define the "Objective" and "Why".
- **Doc-Link**: Check `docs/architecture/` for existing constraints before starting the plan.

### 2. Execution (`skt:cook` / `skt:code`)
- **Action**: Implement features following the plan.
- **Sync**: Use `skt:plans-update` to track progress. If implementation deviates from the plan, update the plan immediately.

### 3. Verification & Archival (`skt:plans-archive`)
- **Action**: Move the plan to `plans/archive/`.
- **Mandatory**: Before archival, verify if architectural decisions need to be merged into `docs/architecture/`.
- **Check**: Use the `management_bridge.py` report to ensure documentation coverage.

---

## Domain Organization

| Domain | Plans Path | Docs Sync Target |
|--------|------------|------------------|
| Features | `plans/features/` | `docs/features/` |
| Infrastructure | `plans/infrastructure/` | `docs/architecture/` |
| Design System | `plans/design-system/` | `docs/design-system/` |
| Core Library | `plans/core/` | `docs/architecture/` |

---

## Best Practices

1. **Link, don't duplicate**: If a detail is already in `docs/`, link to it from the plan.
2. **Capture Reasoning**: Plans are for "How" and "Why". If a "Why" is permanently relevant, move it to `docs/` upon completion.
3. **Keep it Fresh**: Use `skt:plans-summarize` to identify stale or orphaned plans.
