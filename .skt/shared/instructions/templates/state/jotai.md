# Jotai Best Practices

## Core Concepts
- **Atoms**: Small, independent pieces of state.
- **Derived Atoms**: Compute values from other atoms.

## Rules
1.  **Granularity**: Keep atoms small. Split large objects if parts change independently.
2.  **Separation**: Define atoms in `store/atoms.ts` or close to usage if local.
3.  **Persistence**: Use `atomWithStorage` for persisting state to localStorage/sessionStorage.

### Example
```ts
import { atom } from 'jotai';

// Primitive atom
export const countAtom = atom(0);

// Derived atom (read-only)
export const doubleCountAtom = atom((get) => get(countAtom) * 2);

// Write-only derived atom
export const incrementAtom = atom(
  null, // initial value (unused)
  (get, set, update) => set(countAtom, get(countAtom) + 1)
);
```
