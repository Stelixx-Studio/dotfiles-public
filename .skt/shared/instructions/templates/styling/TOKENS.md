# Design Tokens Reference

**Quick reference for AI agents and developers**

> **Source of Truth**: `apps/web/styles/tailwind.css` @theme block  
> **Updated**: January 13, 2026

---

## 🎨 Card Component

**Tokens**:
- `--card-padding-mobile`: `1rem` (16px) - Mobile padding
- `--card-padding-desktop`: `1.5rem` (24px) - Desktop padding (md: breakpoint)
- `--card-gap`: `0.75rem` (12px) - Internal gap between sections

**Component Structure**:
```tsx
<Card>                    // Has padding: p-[var(--card-padding-mobile)] md:p-[var(--card-padding-desktop)]
  <CardHeader>...</CardHeader>   // NO padding (inherits from Card)
  <CardContent>...</CardContent> // NO padding (inherits from Card)
  <CardFooter>...</CardFooter>   // NO padding (inherits from Card)
</Card>
```

**Usage Rules**:
- ✅ **DO**: Use `<Card>` - padding applied automatically
- ✅ **DO**: Use `<Card noPadding>` for custom layouts
- ❌ **DON'T**: Add `px-*` or `p-*` to CardHeader/Content/Footer (creates duplication)
- ❌ **DON'T**: Override Card padding with className (breaks design system)

**Examples**:
```tsx
// ✅ Good - Default padding
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>

// ✅ Good - No padding for custom layout
<Card noPadding>
  <div className="p-4">Custom padding</div>
</Card>

// ❌ Bad - Duplicated padding
<Card>
  <CardHeader className="px-6">Title</CardHeader> {/* Wrong! Already has padding from Card */}
</Card>
```

---

## 📚 Stack Component

**Tokens**:
- `--stack-gap-sm`: `0.5rem` (8px)
- `--stack-gap-md`: `1rem` (16px)
- `--stack-gap-lg`: `1.5rem` (24px)

**Usage Rules**:
- ✅ **DO**: Use `gap` prop for vertical spacing
- ✅ **DO**: Add padding to wrapper div, not Stack
- ❌ **DON'T**: Add `padding` classes to Stack (mixing concerns)
- ❌ **DON'T**: Use `className` for spacing (use gap prop)

**Examples**:
```tsx
// ✅ Good - Gap on Stack, padding on wrapper
<div className="p-4">
  <Stack gap="md">
    <Card>Section 1</Card>
    <Card>Section 2</Card>
  </Stack>
</div>

// ❌ Bad - Padding on Stack
<Stack gap="md" className="p-4">  {/* Wrong! Mixing concerns */}
  <Card>Section 1</Card>
</Stack>
```

---

## 🏗️ Container & Section

**Tokens**:
- `--container-max-width`: `1280px` - Max content width
- (Section tokens to be added later)

---

## 🤖 AI Agent Workflow

When working with UI components:

1. **Check this file first** - Get token values and usage rules
2. **Read component JSDoc** - Components have inline documentation
3. **Verify in code** - Check `apps/web/styles/tailwind.css` @theme block
4. **Follow rules** - Don't add padding to subcomponents

**Quick verification**:
```bash
# Should return 0 matches (no padding duplication)
grep -r "px-6" packages/ui/src/components/ui/card.tsx
```

---

## 📖 Related Documentation

- Component implementations: `packages/ui/src/components/ui/`
- Design system tokens: `apps/web/styles/tailwind.css`
- AI instructions: `.agent/instructions/components/`
- Development rules: `.agent/instructions/development/ALL-RULES.md`
