# TypeScript Rules

## Type Safety

### No Any Type

**Rule**: Never use `any` type - use `unknown` or proper types

**Example**:

```typescript
// ❌ Bad
function process(data: any) {
  return data.value;
}

// ✅ Good
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: string }).value;
  }
  throw new Error('Invalid data');
}
```

### Explicit Return Types

**Rule**: Always specify return types for functions

**Example**:

```typescript
// ❌ Bad
function calculate(a: number, b: number) {
  return a + b;
}

// ✅ Good
function calculate(a: number, b: number): number {
  return a + b;
}
```

### Type Keyword

**Rule**: Use `type` for unions/intersections, `interface` for object shapes

**Example**:

```typescript
// ✅ Use type for unions
type Status = 'pending' | 'success' | 'error';

// ✅ Use interface for objects
interface User {
  id: string;
  name: string;
}
```

## Type Assertions

### Safe Assertions

**Rule**: Use type guards instead of assertions when possible

**Example**:

```typescript
// ❌ Avoid assertions
const value = data as string;

// ✅ Use type guards
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

if (isString(data)) {
  // TypeScript knows data is string here
  console.log(data.toUpperCase());
}
```

## Enums

### Const Enums

**Rule**: Use const enums for better tree-shaking

**Example**:

```typescript
// ✅ Good
const enum Status {
  Pending = 'PENDING',
  Success = 'SUCCESS',
  Error = 'ERROR'
}

// Usage
const status: Status = Status.Pending;
```

### String Enums

**Rule**: Prefer string enums over numeric for better debugging

**Example**:

```typescript
// ✅ Good - values are clear
enum LogLevel {
  Debug = 'DEBUG',
  Info = 'INFO',
  Error = 'ERROR'
}

// ❌ Avoid - numeric values unclear
enum LogLevel {
  Debug,
  Info,
  Error
}
```

## Import Patterns

### Type Imports

**Rule**: Use `import type` for type-only imports

**Example**:

```typescript
// ✅ Good
import type { User } from './types';
import { fetchUser } from './api';

// ❌ Bad - imports value when only type needed
import { User } from './types';
```

### Import Order

**Rule**: Group imports: external → internal → types

**Example**:

```typescript
// ✅ Good order
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import type { User } from '@/types';
```

## Common Patterns

### Utility Types

**Rule**: Use built-in utility types

**Example**:

```typescript
// ✅ Use Partial for optional fields
type PartialUser = Partial<User>;

// ✅ Use Pick for subset
type UserPreview = Pick<User, 'id' | 'name'>;

// ✅ Use Omit to exclude fields
type UserWithoutPassword = Omit<User, 'password'>;
```

### Generic Constraints

**Rule**: Constrain generics when needed

**Example**:

```typescript
// ✅ Good - constrained generic
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Usage
const user = { id: '1', name: 'John' };
const name = getProperty(user, 'name'); // Type: string
```

### Discriminated Unions

**Rule**: Use discriminated unions for state management

**Example**:

```typescript
// ✅ Good pattern
type LoadingState = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: string };

function handleState(state: LoadingState) {
  switch (state.status) {
    case 'success':
      // TypeScript knows state.data exists
      return state.data;
    case 'error':
      // TypeScript knows state.error exists
      return state.error;
  }
}
```

## API Type Patterns

### Response Types

**Rule**: Define clear API response types

**Example**:

```typescript
// ✅ Good - clear response structure
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

interface ApiError {
  error: string;
  code: string;
  details?: Record<string, string>;
}

type Result<T> = ApiResponse<T> | ApiError;
```

### Request Types

**Rule**: Type API request parameters

**Example**:

```typescript
// ✅ Good - typed request
interface CreateUserRequest {
  name: string;
  email: string;
  role?: 'admin' | 'user';
}

async function createUser(data: CreateUserRequest): Promise<User> {
  // Implementation
}
```

## Best Practices

### Avoid Unnecessary Fallbacks

**Rule**: Don't use fallback values for required fields

**Example**:

```typescript
// ❌ Bad - hides missing data
const name = user?.name || 'Unknown';

// ✅ Good - handle missing data explicitly
if (!user?.name) {
  throw new Error('User name is required');
}
const name = user.name;
```

### Strict Null Checks

**Rule**: Enable strictNullChecks in tsconfig.json

**Example**:

```json
{
  "compilerOptions": {
    "strictNullChecks": true,
    "strict": true
  }
}
```
