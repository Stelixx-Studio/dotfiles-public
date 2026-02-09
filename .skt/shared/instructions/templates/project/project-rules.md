# Core Instructions - Always Loaded

**Purpose**: Quick reference for critical rules and architectural decision-making.

**Size**: <200 lines | **Load Time**: <1 second

---

## 🚨 Critical Rules (Never Skip)

### 1. Internationalization (i18n)

**Rule**: ALL user-facing text MUST use `m.key()` from `@repo/i18n`

**Quick Check**:

```bash
# ❌ This should return 0
grep -r '<h1>"' apps/web/features/
```

**Load detailed**: `.agent/instructions/features/i18n.md`

---

### 2. Navigation

**Rule**: ALWAYS use `useAppNavigation` for routing

**Pattern**:

```typescript
// ✅ DO
const { navigateTo, routes } = useAppNavigation()
navigateTo(routes.dashboard)

// ❌ DON'T
const router = useRouter()
router.push("/dashboard")
```

**Load detailed**: `.agent/instructions/features/navigation/overview.md`

---

### 3. Type Safety

**Rules**:

- Never `any` → Use proper types
- Explicit return types → Always
- Import API types → From `@/app/actions/` (Server Actions) or `@/lib/types`

**Quick Check**:

```bash
# ❌ This should return 0
grep -r ": any" apps/web/features/
```

**Load detailed**: `.agent/instructions/development/typescript.md`

---

### 4. API & Data Fetching

**Rule**: ALWAYS use `apiClient` (Ky) - NEVER `fetch()` or `axios`

- ✅ `import { apiClient } from "@/lib/api/client"`
- ✅ `apiClient.get(API_CONFIG.ENDPOINTS.AUTH.ME).json()`
- ❌ NO hardcoded `/api/v1/` in URLs
- ❌ NO `fetch('endpoint')`

---

### 5. Library Configuration

**Pattern**: Provider in `packages/ui/src/providers/` or `apps/web/lib/providers/`

- Always `"use client"` for providers
- Use `useState` for initialization
- 📖 [Library Config Guide](./infrastructure/library-config.md)

---

## 🏗️ Feature Architecture Patterns

### Quick Pattern Selection

```
WHAT ARE YOU BUILDING?
│
├─ Linear flow with multiple steps?
│   → Multi-Step Wizard
│   Examples: Audit, Onboarding
│   Load: features/overview.md
│   Path: apps/web/features/<name>/
│
├─ Metrics and data visualization?
│   → Dashboard/Analytics
│   Examples: Analytics, Insights
│   Load: features/overview.md
│   Path: apps/web/features/<name>/
│
├─ Manage entities (list, create, edit, delete)?
│   → CRUD Interface
│   Examples: Reports, Settings
│   Load: features/overview.md
│   Path: apps/web/features/<name>/
│
└─ Simple single-purpose feature?
    → Simple Feature
    Examples: Contact, Pricing
    Load: features/overview.md
    Path: apps/web/features/<name>/
```

**Load full guide**: `.agent/instructions/features/README.md`

---

## 🎯 Quick Decision Trees

### Where does this code go?

```
WHAT ARE YOU CREATING?
│
├─ UI Component
│   ├─ Used by ONE feature?
│   │   → apps/web/features/<name>/components/
│   ├─ Used by MULTIPLE features?
│   │   → packages/ui/src/components/ (if generic)
│   │   → apps/web/components/ui/ (if app-specific)
│   └─ Layout component?
│       → apps/web/components/layouts/
│
├─ Logic (Hook/Utility)
│   ├─ Feature-specific?
│   │   → apps/web/features/<name>/hooks/
│   └─ Shared across features?
│       → apps/web/lib/
│
├─ Types
│   ├─ API types?
│   │   → Import from apps/web/app/actions/<name>.ts
│   ├─ Feature types?
│   │   → apps/web/features/<name>/types/
│   └─ Shared types?
│       → apps/web/lib/types.ts
│
└─ Data/Config
│   ├─ Feature data?
│   │   → apps/web/features/<name>/content/
│   └─ Global config?
│       → apps/web/lib/config/
```

### Server or Client Component?

```
DOES IT NEED...
│
├─ Data fetching?           → Server Component
├─ Browser APIs?            → Client Component
├─ Event handlers?          → Client Component
├─ React hooks?             → Client Component
├─ localStorage/window?     → Client Component
└─ None of the above?       → Server Component (default)
```

---

## 📋 Feature Integration Rules

### Rule 1: Type Imports

```typescript
// ✅ DO: Import from server actions
import type { User } from "@/app/actions/auth"

// ❌ DON'T: Redefine types
interface User {
  id: string
} // Wrong!
```

### Rule 2: Component Reuse

```typescript
// ✅ DO: Export via index
// apps/web/features/audit/index.ts
export { BrandOverviewCard } from "./components/audit-cards"

// ✅ DO: Import from feature index
import { BrandOverviewCard } from "@/features/audit"

// ❌ DON'T: Deep imports
import { BrandOverviewCard } from "@/features/audit/components/audit-cards/brand-overview-card"
```

### Rule 3: Feature Boundaries

```typescript
// ✅ DO: Clear separation
apps/web/features/audit/        # Audit execution
apps/web/features/analytics/    # Audit data analysis

// ❌ DON'T: Mix concerns
apps/web/features/audit/components/analytics-trend.tsx  // Wrong!
```

---

## ✅ Pre-Commit Checklist

**Run these commands** (copy-paste):

```bash
pnpm lint:fix && pnpm lint && pnpm type-check && pnpm test
```

**Must show**:

- ✅ 0 lint errors, 0 warnings
- ✅ 0 type errors
- ✅ All tests passing
- [ ] No `any` types
- [ ] Imported API types
- [ ] Server Component by default
- [ ] `"use client"` only when needed
- [ ] Files in correct location (apps/web/features/...)

---

**Version**: 1.1.1 (Monorepo Aware)
