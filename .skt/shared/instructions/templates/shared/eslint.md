# ESLint Rules

## Configuration

### Strict Mode

**Rule**: Enable all strict rules

**Example**:

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

## Common Rules

### No Any

**Rule**: Never use any type

**ESLint**: `@typescript-eslint/no-explicit-any: error`

### No Unused Vars

**Rule**: Remove unused variables

**ESLint**: `@typescript-eslint/no-unused-vars: error`

### Explicit Return Types

**Rule**: Specify return types for functions

**ESLint**: `@typescript-eslint/explicit-function-return-type: warn`
