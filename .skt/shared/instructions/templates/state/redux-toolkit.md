# Redux Toolkit Best Practices

## Structure
- Use **Feature Slices**: Group reducer logic and actions in a single file per feature (e.g., `features/auth/authSlice.ts`).
- **Store Configuration**: Centralize store setup in `lib/store.ts`.

## Rules
1.  **Immutability**: RTK uses Immer; you can mutate state directly inside reducers.
2.  **Selectors**: Use `createSelector` (Reselect) for memoized derived data.
3.  **Async Logic**: Use `createAsyncThunk` or RTK Query for data fetching.

### Slice Example
```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
}

const initialState: CounterState = { value: 0 };

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1; // Immer handles immutability
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});
```
