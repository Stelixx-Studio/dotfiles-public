# Git Workflow Rules

## File Organization

### Feature First

**Rule**: Organize by features, not by type

**Example**:

```
✅ Good:
features/
  auth/
    components/
    hooks/
    utils/
  dashboard/
    components/
    hooks/

❌ Bad:
components/
  AuthForm.tsx
  Dashboard.tsx
hooks/
  useAuth.ts
  useDashboard.ts
```

### Kebab Case

**Rule**: Use kebab-case for file names

**Example**:

```
✅ Good: user-profile.tsx, api-client.ts
❌ Bad: UserProfile.tsx, apiClient.ts
```

## Import Patterns

### Absolute Imports

**Rule**: Use absolute imports with @ alias

**Example**:

```typescript
// ✅ Good
import { Button } from '@/components/ui/button'
import { useAuth } from '@/features/auth/hooks'

// ❌ Bad
import { Button } from '../../../components/ui/button'
```

## Commit Messages

### Conventional Commits

**Rule**: Use conventional commit format

**Example**:

```
feat(auth): add login form
fix(api): handle timeout errors
docs(readme): update installation steps
```
