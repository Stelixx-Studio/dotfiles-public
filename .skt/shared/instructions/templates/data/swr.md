# SWR Best Practices

## Core Principles
1.  **Stale-While-Revalidate**: Show cached data first (fast), then revalidate (up-to-date).
2.  **Keys**: Use array keys for arguments `['/api/user', id]`.

## Usage
- Create custom hooks for reusable data fetching (e.g., `useUser(id)`).
- Use `mutate` for optimistic updates.

### Example
```ts
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useUser(id: string) {
  const { data, error, isLoading } = useSWR(['/api/users', id], ([url, id]) => fetcher(`${url}/${id}`));

  return {
    user: data,
    isLoading,
    isError: error,
  };
}
```
