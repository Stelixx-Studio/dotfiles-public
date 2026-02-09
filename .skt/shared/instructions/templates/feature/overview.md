## ${FeatureName} Feature

**Purpose**: Define the purpose of this feature here.

### Architecture

**Components**:
- State: `hooks/use-${kebabName}.ts`
- UI: `components/`

### Patterns

**Rule**: Keep components focused and reusable

**Example**:

```typescript
// Feature-specific component patterns
export const ${FeatureName}Component: FC<Props> = ({ data }) => {
  return <div>{data}</div>
}
```

### Hooks

**Rule**: Extract reusable logic into custom hooks

**Example**:

```typescript
function use${FeatureName}() {
  // Custom hook logic
}
```

### API Integration

**Rule**: Use consistent API patterns

### Types

**Rule**: Define clear type interfaces
