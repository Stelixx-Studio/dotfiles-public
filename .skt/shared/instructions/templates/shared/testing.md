# Testing Rules

## Test Organization

### Co-Located Tests

**Rule**: Place tests next to source files

**Example**:
```
user-profile.tsx
user-profile.test.tsx
```

### All Passing

**Rule**: Ensure all tests pass

**Example**:
```bash
pnpm test
```

### Minimum Coverage

**Rule**: Aim for 80%+ coverage on critical paths

**Example**:
```bash
pnpm test:coverage
```
