# Prisma ORM Rules

## Schema Patterns

### Model Definitions

**Rule**: Use clear, consistent naming

**Example**:

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Relations

**Rule**: Define bidirectional relations

**Example**:

```prisma
model Post {
  id       String @id @default(cuid())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
}
```

## Query Patterns

### Type-Safe Queries

**Rule**: Use Prisma Client with TypeScript

**Example**:

```typescript
const user = await prisma.user.findUnique({
  where: { id },
  include: { posts: true },
});
```

### Transactions

**Rule**: Use transactions for related operations

**Example**:

```typescript
await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.post.create({ data: postData }),
]);
```

## Best Practices

### Soft Deletes

**Rule**: Use soft deletes for important data

**Example**:

```prisma
model User {
  id        String    @id @default(cuid())
  deletedAt DateTime?
}
```

```typescript
// Soft delete
await prisma.user.update({
  where: { id },
  data: { deletedAt: new Date() },
});

// Query non-deleted
const users = await prisma.user.findMany({
  where: { deletedAt: null },
});
```

### Pagination

**Rule**: Use cursor-based pagination for large datasets

**Example**:

```typescript
const posts = await prisma.post.findMany({
  take: 10,
  skip: 1,
  cursor: { id: lastPostId },
  orderBy: { createdAt: 'desc' },
});
```
