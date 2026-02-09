# Tailwind CSS Best Practices

## Core Principles
1.  **Utility-First**: Use predefined utility classes over arbitrary values (`[123px]`).
2.  **Consistency**: Use the design system tokens (colors, spacing) defined in `tailwind.config.ts`.
3.  **Readability**: Group related utilities (layout -> box model -> typography -> visual).

## Formatting
- Use `prettier-plugin-tailwindcss` for automatic class sorting.
- Use `clsx` or `cn` (shadcn/ui utility) for conditional classes.

### Example
```tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  className?: string;
  variant?: 'primary' | 'secondary';
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        // Layout & Base
        'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors',
        // Interactions
        'hover:opacity-90 focus-visible:outline-none focus-visible:ring-1',
        // Variants
        variant === 'primary' && 'bg-primary text-primary-foreground',
        variant === 'secondary' && 'bg-secondary text-secondary-foreground',
        // External overrides
        className
      )}
      {...props}
    />
  );
}
```

## Anti-Patterns
- ❌ Avoid arbitrary values: `w-[325px]` (Use layout components or percentage).
- ❌ Avoid `@apply` in CSS modules unless absolutely necessary.
- ❌ Avoid string concatenation for classes: `` `btn ${active ? 'active' : ''}` `` (Use `cn()`).
