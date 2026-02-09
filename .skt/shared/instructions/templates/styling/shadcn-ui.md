# Shadcn UI Best Practices

## Philosophy
Shadcn UI is not a component library; it's a collection of reusable components that you verify and copy into your project.

## Usage Rules
1.  **Do Not Modify Core unnecessarily**: Try to customize via `components.json` or props first.
2.  **Composition over Configuration**: Build complex UIs by composing primitives (e.g., `Card`, `CardHeader`, `CardContent`).
3.  **Accessibility First**: Do not remove `Radix UI` accessibility primitives or props.

## Component Structure
Components live in `components/ui`.

### Example Check
When adding a new component (e.g., `Select`):
1.  Run `npx shadcn@latest add select`.
2.  Verify it loads correctly in a playground page.
3.  Check `tailwind.config.ts` for any missing animations (e.g., `accordion-down`).

## Customization
Customize theme tokens in `app/globals.css` (CSS variables), not hardcoded hex values in components.

```css
:root {
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}
```
