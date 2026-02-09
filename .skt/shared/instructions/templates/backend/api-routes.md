# API Route Rules

## Route Handlers (App Router)

### Request/Response

**Rule**: Use standard `Request` and `Response` objects where possible, or `NextRequest/NextResponse` for advanced features.

**Example**:

```typescript
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  
  if (!id) {
    return NextResponse.json({ error: 'Missing ID' }, { status: 400 });
  }

  const data = await db.query(id);
  return NextResponse.json(data);
}
```

### Validation

**Rule**: VALIDATE ALL INPUTS using Zod. Never trust client data.

**Example**:

```typescript
import { z } from 'zod';

const bodySchema = z.object({
  email: z.string().email(),
  role: z.enum(['user', 'admin']),
});

export async function POST(req: Request) {
  const body = await req.json();
  const result = bodySchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(result.error.flatten(), { status: 400 });
  }

  // Proceed with result.data
}
```

### Error Handling

**Rule**: Use try/catch blocks and return standardized error responses.

**Example**:

```typescript
export async function POST(req: Request) {
  try {
    // ... logic
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

### Http Methods

**Rule**: Export named functions for each HTTP method (GET, POST, PUT, DELETE).

```typescript
export async function GET() {}
export async function POST() {}
export async function PUT() {}
export async function DELETE() {}
```
