# Accessibility Rules (WCAG AA)

## Semantic HTML

### Use Semantic Elements

**Rule**: Use semantic HTML elements

**Example**:
```html
<article>
  <h1>Title</h1>
  <p>Content</p>
</article>
```

## ARIA

### ARIA Labels

**Rule**: Add ARIA labels for screen readers

**Example**:
```html
<button aria-label="Close menu">
  <IconX />
</button>
```

### Alt Text

**Rule**: Add alt text for all images

**Example**:
```html
<img src="logo.png" alt="Company logo" />
```

## Keyboard Navigation

### Keyboard Support

**Rule**: Ensure keyboard navigation works

**Example**:
```typescript
onKeyDown={(e) => e.key === 'Enter' && handleClick()}
```

## Color Contrast

### WCAG AA Compliance

**Rule**: Meet WCAG AA contrast ratio 4.5:1

**Example**:
```
Use color contrast checker tools
```
