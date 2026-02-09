# Card Component Rules

**Component**: `packages/ui/src/components/ui/card.tsx`  
**Design Tokens**: See `packages/tailwind-preset/TOKENS.md`

---

## 🎯 Quick Rules

1. **Card has padding** - Responsive: 16px mobile, 24px desktop
2. **Subcomponents have NO padding** - CardHeader, CardContent, CardFooter inherit from Card
3. **Don't add px-* classes** - Creates duplication (root cause of padding issues)

---

## 📋 Usage Patterns

### ✅ Correct Usage

```tsx
// Default - padding applied automatically
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>

// No padding - for custom layouts
<Card noPadding>
  <div className="p-4">Custom padding</div>
</Card>
```

### ❌ Incorrect Usage

```tsx
// Wrong - duplicated padding
<Card>
  <CardHeader className="px-6">Title</CardHeader> {/* Already has padding from Card! */}
</Card>

// Wrong - overriding design system
<Card className="p-8">Content</Card> {/* Use design tokens instead */}
```

---

## 🔍 AI Discovery Pattern

Before modifying Card component:

1. Read this file for rules
2. Check `packages/tailwind-preset/TOKENS.md` for token values
3. Read JSDoc in `card.tsx` for inline documentation
4. Verify changes with: `grep -r "px-6" packages/ui/src/components/ui/card.tsx`

---

## 🎨 Design Tokens

**Source**: `apps/web/styles/tailwind.css` @theme block

- `--card-padding-mobile`: 1rem (16px)
- `--card-padding-desktop`: 1.5rem (24px)
- `--card-gap`: 0.75rem (12px)

**Implementation**: Card uses `p-[var(--card-padding-mobile)] md:p-[var(--card-padding-desktop)]`

---

## 📚 Related

- [TOKENS.md](../../tailwind-preset/TOKENS.md) - All design tokens
- [ALL-RULES.md](../development/ALL-RULES.md) - Development guidelines
- [file-organization.md](../development/patterns/file-organization.md) - Component structure
