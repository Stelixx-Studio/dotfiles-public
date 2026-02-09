# React Query (TanStack Query) Best Practices

## Core Principles
1.  **Query Keys**: Use a consistent key structure (e.g., `['todos', { status, page }]`).
2.  **Prefetching**: Prefetch data on server (Hydration boundaries) or hover for best UX.

## Mutation Rules
- **Optimistic Updates**: Update UI immediately before server response.
- **Invalidation**: Always invalidate relevant query keys after a successful mutation using `queryClient.invalidateQueries`.

### Example
```ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });
}

export function useAddTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: addTodo,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```
