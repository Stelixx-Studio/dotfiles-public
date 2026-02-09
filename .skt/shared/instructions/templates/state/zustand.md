# Zustand State Management Rules

## Store Patterns

### Create Stores

**Rule**: Use `create` with TypeScript

**Example**:

```typescript
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));
```

### Selectors

**Rule**: Use selectors for derived state

**Example**:

```typescript
// ✅ Good - selector
const userName = useUserStore((state) => state.user?.name);

// ❌ Bad - whole state
const { user } = useUserStore();
const userName = user?.name;
```

## Best Practices

### Immer for Nested Updates

**Rule**: Use immer middleware for complex state

**Example**:

```typescript
import { immer } from 'zustand/middleware/immer';

export const useStore = create<State>()(
  immer((set) => ({
    nested: { value: 0 },
    increment: () => set((state) => {
      state.nested.value++;
    }),
  }))
);
```

### Persist Middleware

**Rule**: Use persist for localStorage sync

**Example**:

```typescript
import { persist } from 'zustand/middleware';

export const useStore = create<State>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'app-storage' }
  )
);
```

### Slice Pattern

**Rule**: Split large stores into slices

**Example**:

```typescript
const createUserSlice = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
});

const createSettingsSlice = (set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
});

export const useStore = create((set) => ({
  ...createUserSlice(set),
  ...createSettingsSlice(set),
}));
```
