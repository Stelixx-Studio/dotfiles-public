# Playwright Best Practices

## Core Principles
1.  **User-Centric**: Test user-visible behavior (clicks, role checks), not implementation details.
2.  **Resilience**: Use `page.getByRole`, `page.getByText` locators over CSS selectors (`.btn-primary`).
3.  **Isolation**: Tests should run independently. Isolate state per test.

## Locators
- ✅ `getByRole('button', { name: 'Submit' })`
- ✅ `getByTestId('user-profile')` (Only if no role is applicable)
- ❌ `page.locator('.submit-btn')`

### Example
```ts
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Stelixx App/);
});

test('can login', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL('/dashboard');
});
```
