---
name: playwright-builder
description: Build or repair a reusable Playwright script for a third-party website workflow, including scraping or form entry.
---

# Playwright Builder

When you need a runnable Playwright script (not just live browser actions via MCP), this skill structures the build.

## When to Use This Skill vs. The Playwright MCP

| Scenario | Use This | Use Playwright MCP |
|----------|----------|-------------------|
| User wants a `.ts`/`.js` file they can re-run | ✓ | |
| Bulk operation driven by CSV / list (>10 items) | ✓ | |
| Will run unattended / on schedule | ✓ | |
| One-time exploration, "click this for me" | | ✓ |
| User watches the result interactively | | ✓ |

## Workflow

### Step 1: Clarify the Goal

Before writing any code, confirm:
- **Target site(s)** — exact URL(s)
- **Login required?** — if yes, how to handle creds (env vars, prompt at runtime, persistent storage)
- **Input** — manual list, CSV, JSON, hardcoded?
- **Output** — does the script need to save anything (URLs, screenshots, JSON)?
- **Headless or headed?** — debugging is easier headed, production usually headless
- **Selectors known?** — if not, plan to use `playwright codegen` first

### Step 2: Scaffold the Project

Standard layout for a one-off script:

```
~/code-projects/playwright-scripts/<task-name>/
├── package.json
├── tsconfig.json (if TypeScript)
├── .env (if creds — gitignore this)
├── input.csv (or .json)
├── outputs/
└── script.ts
```

Initialize:

```bash
mkdir -p ~/code-projects/playwright-scripts/<task-name>
cd ~/code-projects/playwright-scripts/<task-name>
npm init -y
npm install playwright @playwright/test
npm install -D typescript @types/node tsx
npx playwright install chromium  # browser binary
```

### Step 3: Write the Script

Standard template:

```typescript
import { chromium, Browser, Page } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

interface InputRow { /* shape of input */ }

async function loadInput(): Promise<InputRow[]> {
  const csv = fs.readFileSync('input.csv', 'utf-8');
  // parse CSV → InputRow[]
  return [];
}

async function processItem(page: Page, item: InputRow): Promise<void> {
  // 1. Navigate
  await page.goto('https://target-site.com');
  // 2. Wait for the right element
  await page.waitForSelector('selector-here');
  // 3. Interact (click, fill, etc.)
  await page.click('selector');
  // 4. Verify success or extract data
  const result = await page.textContent('result-selector');
  console.log(`Done: ${item} → ${result}`);
}

async function main() {
  const headless = process.env.HEADLESS !== 'false';
  const browser: Browser = await chromium.launch({ headless });
  const context = await browser.newContext({
    storageState: 'auth.json' // if you saved login state
  });
  const page = await context.newPage();

  const items = await loadInput();
  for (const [i, item] of items.entries()) {
    console.log(`[${i + 1}/${items.length}] processing...`);
    try {
      await processItem(page, item);
    } catch (err) {
      console.error(`Failed on item ${i}:`, err);
      await page.screenshot({ path: `outputs/error-${i}.png` });
    }
  }

  await browser.close();
}

main().catch(console.error);
```

### Step 4: Handle Login (if needed)

For sites requiring auth, save the session state once, then reuse:

```typescript
// One-time login script (run with: tsx login.ts)
const browser = await chromium.launch({ headless: false });
const context = await browser.newContext();
const page = await context.newPage();
await page.goto('https://site.com/login');
console.log('Log in manually, then press Enter...');
await new Promise(resolve => process.stdin.once('data', resolve));
await context.storageState({ path: 'auth.json' });
await browser.close();
```

Then in the main script: `browser.newContext({ storageState: 'auth.json' })`.

### Step 5: Find Selectors Reliably

When you don't know the right selector:

```bash
# Records your manual interactions and outputs Playwright code
npx playwright codegen https://site.com
```

Prefer in this order:
1. **`getByRole`** — `page.getByRole('button', { name: 'Submit' })` — accessible, stable
2. **`getByText`** — `page.getByText('Sign in')` — readable, fragile if text changes
3. **`getByLabel`** for form fields
4. **CSS selector with `data-` attributes** — `page.locator('[data-testid="cart"]')` — best when site uses test IDs
5. **CSS class/tag** — last resort, often breaks on redesign

### Step 6: Make It Re-Runnable

Add a zsh alias so the user can invoke the script easily:

```bash
# In ~/.zshrc or a separate alias file
alias <task-name>='cd ~/code-projects/playwright-scripts/<task-name> && tsx script.ts'
```

For headed runs while debugging:
```bash
HEADLESS=false tsx script.ts
```

### Step 7: Test on Small Input First

Always verify with the first 1-2 items before letting it loose on the full list:

```typescript
const items = (await loadInput()).slice(0, 2);  // dev mode
```

Watch the logs and screenshots in `outputs/` to confirm correctness, then remove the `.slice()`.

## Common Pitfalls

- **Race conditions** — always `waitForSelector` or `waitForLoadState('networkidle')` before interacting
- **Stale selectors** — element references can become invalid after page navigation; re-query
- **Rate limiting** — add `await page.waitForTimeout(1000)` between requests for politeness
- **Headless detection** — some sites block headless browsers; try headed mode or use a stealth plugin
- **Cookies cleared** — use `storageState` to persist auth across runs
- **Modal dialogs** — Playwright pauses on `alert()` etc.; handle with `page.on('dialog', d => d.accept())`

## Reference: Bulk List Creation Pattern (e.g. IMDB)

For tasks like "create N lists from CSV categories":

```typescript
// Group input by category
const byCategory: Record<string, InputRow[]> = {};
for (const row of items) {
  (byCategory[row.category] ??= []).push(row);
}

// Per category: create the list, then add each item
for (const [category, rows] of Object.entries(byCategory)) {
  console.log(`Creating list: ${category}`);
  await page.goto('https://imdb.com/list/create');
  await page.fill('[name="title"]', category);
  await page.click('text=Create');

  for (const row of rows) {
    await page.goto(`https://imdb.com/title/${row.id}`);
    await page.click(`text=Add to list`);
    await page.click(`text=${category}`);
    await page.waitForTimeout(500);
  }
}
```

## Output Discipline

When you finish building, give the user:
1. The script path
2. The exact command to run it (including any env vars)
3. The zsh alias added (if any)
4. What `outputs/` will contain after a run
