# Vitest Best Practices

## Core Principles
1.  **Speed**: Vitest is fast; keep tests fast by mocking heavy dependencies.
2.  **Integration**: Test components and hooks in integration where possible (`render(<Component />)`).
3.  **Mocking**: Use `vi.mock()` for external modules.

## Helper Library
- Use `@testing-library/react` for component testing.
- Use `@testing-library/user-event` for user interactions.

### Example
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';
import { vi } from 'vitest';

test('increments counter', async () => {
  const user = userEvent.setup();
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /count is/i });
  await user.click(button);
  
  expect(button).toHaveTextContent(/count is 1/i);
});
```
