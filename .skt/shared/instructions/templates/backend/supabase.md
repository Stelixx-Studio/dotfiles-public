# Supabase Best Practices

## Core Principles
1.  **RLS (Row Level Security)**: Enable RLS on ALL tables. Never expose a table without RLS.
2.  **Types**: Generate TypeScript types from your schema using `supabase gen types`.

## Client Usage
- Use `createClientComponentClient` for client components.
- Use `createServerComponentClient` for server components.

### Example (Server Component)
```tsx
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import type { Database } from '@/types/supabase';

export default async function Page() {
  const supabase = createServerComponentClient<Database>({ cookies });
  const { data } = await supabase.from('posts').select();
  
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```
