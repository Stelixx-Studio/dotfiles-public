# Planning Management Standards

This document defines implementation planning standards, status tracking, and archival procedures for the SKT project.

---

## Technical Planning Standards

### Plan Structure

- **Objective**: Clear context and high-level goal of the change.
- **Detailed Tasks**: Breakdown of work across components.
- **Verification Plan**: Steps to validate the implementation.
- **Status Tracking**: Draft, In Progress, Completed, or Archived.

### Naming Conventions

- **File Name**: `YYMMDD-topic-description.md` (e.g., `260126-plans-workflows.md`).
- **Domain Categories**: features, core, infrastructure, design-system.

---

## Directory Strategy

| Directory | Purpose | Status |
|-----------|---------|--------|
| `plans/features/` | Feature-specific plans | Active |
| `plans/infrastructure/` | Setup, CI/CD, DevOps | Active |
| `plans/design-system/` | UI/UX and styling | Active |
| `plans/core/` | Library logic and engine | Active |
| `plans/archive/` | Completed or obsolete plans | Inactive |

---

## Maintenance Procedures

### When to Update Plans

1. **Before implementation**: Create a new plan and get approval.
2. **During execution**: Check off tasks as they are completed.
3. **Upon completion**: Move the plan to the `archive/` directory.
4. **Knowledge Transfer**: Ensure critical architectural decisions are moved to `docs/`.

### Archival logic

When a plan is moved to `archive/`:
- It should follow the same category structure (e.g., `plans/archive/features/`).
- The status must be updated to `Completed` or `Obsolete`.
- A link to the final implementation (PR or Docs) should be added.

---

## Tools

- `skt:plans-init`: Initialize and organize the `plans/` structure.
- `skt:plans-update`: Sync task progress from code.
- `skt:plans-summarize`: Generate a roadmap of active work.
- `skt:plans-archive`: Automate the archival process.
