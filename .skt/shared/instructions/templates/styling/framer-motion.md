# Framer Motion Best Practices

## Core Concepts
1.  **Declarative Animations**: Use the `animate` prop for simple states.
2.  **Layout Animations**: Use `layout` prop for automatic smooth transitions when DOM order changes.
3.  **Performance**: Animate `transform` and `opacity` only. Avoid animating `height` or `width` if possible (use `layout` instead).

## Optimization
- Use `LazyMotion` to reduce bundle size.
- Export complex variants to a separate file `animations.ts`.

### Example
```tsx
import { motion } from 'framer-motion';

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 20 }
};

export function FadeCard({ children }) {
  return (
    <motion.div
      variants={fadeIn}
      initial="initial"
      animate="animate"
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```
