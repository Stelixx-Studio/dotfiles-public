# Next.js Rules

## Server Components

### Server First

**Rule**: Default to Server Components, use Client Components only when needed

**Example**:

```typescript
// ✅ Server Component (default)
export async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}

// Only use "use client" when needed
"use client"
export function InteractiveButton() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Use Client First Line

**Rule**: 'use client' must be the first line

**Example**:

```typescript
"use client"

import { FC } from "react"
```

## React Patterns

### Explicit Props

**Rule**: Define Props interface with FC<Props>

**Example**:

```typescript
interface Props {
  data: DataType
}

export const Component: FC<Props> = ({ data }) => {
  return <div>{data}</div>
}
```

### Extract Business Logic

**Rule**: Keep components focused on rendering, extract logic to hooks

**Example**:

```typescript
// ✅ Good - logic in hook
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null)
  
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])
  
  return user
}

export function UserProfile({ userId }: Props) {
  const user = useUserData(userId)
  return <div>{user?.name}</div>
}
```

## Performance

### Next Image

**Rule**: Always use next/image for images

**Example**:

```typescript
import Image from 'next/image'

// ✅ Good
<Image
  src="/photo.jpg"
  alt="Photo"
  width={500}
  height={300}
  priority
/>

// ❌ Bad
<img src="/photo.jpg" alt="Photo" />
```

### Code Splitting

**Rule**: Use dynamic imports for heavy components

**Example**:

```typescript
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>
})
```

## Best Practices

### Metadata API

**Rule**: Use Next.js 13+ Metadata API

**Example**:

```typescript
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description'
}
```

### Route Handlers

**Rule**: Use Route Handlers for API routes

**Example**:

```typescript
// app/api/users/route.ts
export async function GET() {
  const users = await fetchUsers()
  return Response.json(users)
}

export async function POST(request: Request) {
  const data = await request.json()
  const user = await createUser(data)
  return Response.json(user)
}
```
