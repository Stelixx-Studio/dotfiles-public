# tRPC API Rules

## Router Patterns

### Define Routers

**Rule**: Use type-safe routers

**Example**:

```typescript
import { router, publicProcedure } from './trpc';
import { z } from 'zod';

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      return await db.user.findUnique({ where: { id: input.id } });
    }),
});
```

### Client Usage

**Rule**: Use tRPC client hooks

**Example**:

```typescript
import { trpc } from '@/utils/trpc';

function UserProfile({ userId }: Props) {
  const { data: user } = trpc.user.getById.useQuery({ id: userId });
  
  return <div>{user?.name}</div>;
}
```

## Best Practices

### Input Validation

**Rule**: Always validate inputs with Zod

**Example**:

```typescript
const createUserInput = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export const userRouter = router({
  create: publicProcedure
    .input(createUserInput)
    .mutation(async ({ input }) => {
      return await db.user.create({ data: input });
    }),
});
```

### Error Handling

**Rule**: Use TRPCError for consistent errors

**Example**:

```typescript
import { TRPCError } from '@trpc/server';

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      const user = await db.user.findUnique({ where: { id: input.id } });
      
      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'User not found',
        });
      }
      
      return user;
    }),
});
```

### Middleware

**Rule**: Use middleware for auth and logging

**Example**:

```typescript
const isAuthed = middleware(async ({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  
  return next({
    ctx: {
      user: ctx.session.user,
    },
  });
});

export const protectedProcedure = publicProcedure.use(isAuthed);
```
