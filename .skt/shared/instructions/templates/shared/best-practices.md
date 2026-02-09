# Best Practices

## Code Quality

### No Magic Values

**Rule**: Use constants instead of magic values

**Example**:

```typescript
// ✅ Good
const MAX_RETRIES = 3
const TIMEOUT_MS = 5000

// ❌ Bad
if (retries > 3) { }
setTimeout(fn, 5000)
```

### Error Handling

**Rule**: Always handle errors explicitly

**Example**:

```typescript
// ✅ Good
try {
  await fetchData()
} catch (error) {
  console.error('Failed to fetch:', error)
  throw new Error('Data fetch failed')
}

// ❌ Bad
await fetchData() // No error handling
```

## Performance

### Avoid Premature Optimization

**Rule**: Optimize only when needed, measure first

### Use Memoization Wisely

**Rule**: Only memoize expensive computations

**Example**:

```typescript
// ✅ Good - expensive computation
const expensiveValue = useMemo(() => {
  return heavyComputation(data)
}, [data])

// ❌ Bad - simple computation
const sum = useMemo(() => a + b, [a, b])
```

## Security

### Environment Variables

**Rule**: Never commit secrets

**Example**:

```typescript
// ✅ Good
const apiKey = process.env.API_KEY

// ❌ Bad
const apiKey = 'sk-1234567890'
```

### Input Validation

**Rule**: Always validate user input

**Example**:

```typescript
// ✅ Good
const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(120)
})

const validated = schema.parse(input)
```
