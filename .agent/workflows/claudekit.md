---
description: Gateway to all 31+ SKT workflows (plan, cook, fix, etc.)
---

# SKT - AI Development Workflows

Comprehensive workflow system for AI-assisted development including planning, implementation, debugging, and testing.

## How to Use

SKT is a gateway to specialized workflows. Use this syntax:

```
@[/claudekit] <command> "<description>"
```

The system will automatically route to the appropriate workflow based on your command.

---

## Available Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `plan` | Architecture & feature planning | Before starting new features, designing systems |
| `cook` | Implementation & coding | Building components, writing code |
| `fix` | Debugging & issue resolution | Fixing bugs, resolving errors |
| `fix-hard` | Complex debugging | Memory leaks, performance issues, race conditions |
| `test` | Test generation & validation | Writing tests, validating functionality |
| `review` | Code review & quality check | Before merging, ensuring best practices |
| `refactor` | Code improvement | Cleaning up code, improving structure |
| `optimize` | Performance optimization | Improving speed, reducing bundle size |

---

## Usage Patterns

### Planning a Feature

**When**: Before starting implementation

**Example**:
```
@[/claudekit] plan "user authentication with OAuth and email/password"
```

**What it does**:
- Analyzes requirements
- Suggests architecture
- Identifies dependencies
- Creates implementation plan

### Implementing a Component

**When**: Building new features

**Example**:
```
@[/claudekit] cook "responsive navbar with dark mode toggle"
```

**What it does**:
- Generates code
- Follows best practices
- Implements requested features
- Ensures responsiveness

### Debugging Issues

**When**: Fixing bugs or errors

**Example**:
```
@[/claudekit] fix "form validation not working on submit"
```

**For complex issues**:
```
@[/claudekit] fix-hard "memory leak in data table pagination"
```

**What it does**:
- Analyzes error messages
- Identifies root cause
- Proposes solutions
- Implements fixes

### Writing Tests

**When**: Ensuring code quality

**Example**:
```
@[/claudekit] test "user registration flow with validation"
```

**What it does**:
- Generates test cases
- Covers edge cases
- Ensures proper assertions
- Validates functionality

---

## Best Practices

### 1. Be Specific

❌ **Bad**: `@[/claudekit] plan "auth"`

✅ **Good**: `@[/claudekit] plan "user authentication with OAuth (Google, GitHub) and email/password, including password reset flow"`

### 2. Include Context

❌ **Bad**: `@[/claudekit] cook "button"`

✅ **Good**: `@[/claudekit] cook "primary CTA button with loading state and disabled state for Next.js app"`

### 3. Mention Stack/Framework

❌ **Bad**: `@[/claudekit] fix "routing issue"`

✅ **Good**: `@[/claudekit] fix "Next.js App Router dynamic route not rendering correctly"`

### 4. Use Right Command

Follow the natural workflow:
1. `plan` - Design the solution
2. `cook` - Implement the code
3. `test` - Validate functionality
4. `fix` - Debug issues
5. `review` - Ensure quality

### 5. Provide Error Messages

❌ **Bad**: `@[/claudekit] fix "app broken"`

✅ **Good**: `@[/claudekit] fix "TypeError: Cannot read property 'map' of undefined in UserList component"`

---

## Common Workflows

### Building a New Feature

```
# Step 1: Plan
@[/claudekit] plan "user profile page with avatar upload and bio editing"

# Step 2: Implement
@[/claudekit] cook "user profile page component with form validation"

# Step 3: Test
@[/claudekit] test "user profile update flow"

# Step 4: Review
@[/claudekit] review "user profile implementation"
```

### Fixing a Production Bug

```
# Step 1: Debug
@[/claudekit] fix "users unable to submit payment form - validation error"

# Step 2: Test fix
@[/claudekit] test "payment form submission with various card types"

# Step 3: Review
@[/claudekit] review "payment form fix"
```

### Optimizing Performance

```
# Step 1: Analyze
@[/claudekit] plan "improve page load time for dashboard"

# Step 2: Optimize
@[/claudekit] optimize "dashboard component - reduce bundle size and improve rendering"

# Step 3: Validate
@[/claudekit] test "dashboard performance metrics"
```

---

## Tips for Better Results

1. **Start with plan** - Always plan before implementing complex features
2. **Be descriptive** - More context = better results
3. **Include constraints** - Mention limitations (mobile-first, accessibility, etc.)
4. **Reference existing code** - "similar to UserCard component"
5. **Specify tech stack** - React, Vue, Next.js, TypeScript, etc.
6. **Mention edge cases** - Loading states, error handling, empty states
7. **Use fix-hard for complex issues** - Memory leaks, race conditions, performance

---

## Examples by Use Case

### Frontend Development

```
@[/claudekit] plan "product listing page with filters and pagination"
@[/claudekit] cook "product card component with image, price, and add to cart"
@[/claudekit] fix "product images not loading on mobile Safari"
```

### Backend Development

```
@[/claudekit] plan "REST API for user management with CRUD operations"
@[/claudekit] cook "Express.js route handlers with validation and error handling"
@[/claudekit] test "API endpoints with edge cases and error scenarios"
```

### Full-Stack Features

```
@[/claudekit] plan "real-time chat feature with WebSocket"
@[/claudekit] cook "chat UI component with message history and typing indicators"
@[/claudekit] cook "WebSocket server with message broadcasting"
@[/claudekit] test "chat functionality with multiple users"
```

### Debugging

```
@[/claudekit] fix "React component re-rendering infinitely"
@[/claudekit] fix-hard "memory leak in event listeners"
@[/claudekit] fix "TypeScript type error in generic function"
```

---

## Pre-Execution Checklist

Before running SKT workflows, ensure:

- [ ] Clear description of what you want
- [ ] Relevant context (stack, framework, constraints)
- [ ] Expected outcome defined
- [ ] Error messages included (if debugging)
- [ ] Edge cases mentioned (if applicable)

---

## Advanced Usage

### Chaining Workflows

For complex tasks, chain multiple commands:

```
# 1. Plan the architecture
@[/claudekit] plan "e-commerce checkout flow with Stripe integration"

# 2. Implement cart functionality
@[/claudekit] cook "shopping cart with add/remove items and quantity update"

# 3. Implement checkout
@[/claudekit] cook "checkout form with Stripe payment integration"

# 4. Add tests
@[/claudekit] test "complete checkout flow from cart to payment confirmation"

# 5. Optimize
@[/claudekit] optimize "checkout page performance and bundle size"
```

### Iterative Development

Use workflows iteratively:

```
# Initial implementation
@[/claudekit] cook "user dashboard with stats cards"

# Review and improve
@[/claudekit] review "dashboard implementation"

# Refactor based on feedback
@[/claudekit] refactor "dashboard components for better reusability"

# Final optimization
@[/claudekit] optimize "dashboard rendering performance"
```

---

## Troubleshooting

**Issue**: Workflow not understanding context

**Solution**: Be more specific, include tech stack and constraints

**Issue**: Generated code doesn't match expectations

**Solution**: Provide more details, reference similar existing code

**Issue**: Fix not resolving the issue

**Solution**: Use `fix-hard` for complex problems, include full error stack trace

---

## Related Features

- [Instructions](/features/instructions) - AI instruction templates
- [UI/UX Pro Max](/workflows/ui-ux-pro-max) - Design workflows
