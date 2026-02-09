# Security Best Practices

## Environment Variables

### No Secrets in Code

**Rule**: Never commit secrets - use .env.local

**Example**:
```bash
# .env.local
NEXT_PUBLIC_API_KEY=xxx
```

## Input Sanitization

### Sanitize User Input

**Rule**: Sanitize before using dangerouslySetInnerHTML

**Example**:
```typescript
import DOMPurify from 'dompurify'
const clean = DOMPurify.sanitize(html)
```

## Server-Side Validation

### Always Validate on Server

**Rule**: Always validate on server

**Example**:
```typescript
// Server Action
export async function createUser(data: FormData) {
  // Validate here
}
```

## CSRF Protection

### Use CSRF Tokens

**Rule**: Implement CSRF protection for forms

**Example**:
```
Use Next.js built-in CSRF protection
```
