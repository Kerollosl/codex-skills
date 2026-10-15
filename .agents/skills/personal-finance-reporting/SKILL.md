---
name: personal-finance-reporting
description: Update Kero's Monthly Finances Budget spreadsheet using data from the Finances plugin. Use when Kero asks to update, sync, refresh, or reconcile the Monthly Finances Budget. Invoke as `/personal-finance-reporting`.
---

# Personal Finance Reporting

This workflow requires the connected Finances data source and spreadsheet access. If Finances is unavailable or incomplete, do not scrape bank websites or infer missing data; report the limitation and leave affected totals unmodified.

Use **Finances** as the authoritative source for account and transaction data.

Use **Spreadsheets** to read and update the existing **Monthly Finances Budget** workbook.

Do not log directly into bank websites, scrape financial institutions, request CSV exports, or maintain a separate financial ledger outside Finances.

## Workflow

1. Open the existing `Monthly Finances Budget` spreadsheet.
2. Inspect the relevant existing sheet structure before making changes.
3. Use Finances to retrieve the financial data needed for the update.
4. Update only:
   - `Monthly Tracking`
   - `Expense Tracking`
5. Never modify `Reference` unless Kero explicitly requests it.
6. Verify the resulting spreadsheet before finishing.
7. Give Kero a short summary of changes and anything requiring review.

## Expense Tracking

Treat `Expense Tracking` as the detailed transaction ledger.

Pull transactions from Finances covering enough history to identify anything not already represented in the sheet.

Append only transactions that are not already present.

Prefer Finances transaction ID for deduplication. If an ID is unavailable, compare:
- date
- amount
- account
- merchant/original description

Store useful transaction details including:
- Date
- Merchant
- Original Description
- Amount
- Category
- Account
- Status
- Transaction ID

Use Finances' merchant enrichment, categories, transfer identification, and saved financial rules.

Pending transactions may appear in Expense Tracking but must be marked `Pending`.

Do not count these as economic spending:
- transfers between Kero's own accounts
- credit-card repayments
- investment funding transfers

Do not double-count both an underlying credit-card purchase and its subsequent card payment.

If a transaction's categorization or treatment is genuinely ambiguous, flag it for review rather than guessing.

## Monthly Tracking

Update the current month's column using posted Finances data.

Update the existing rows for:
- Income
- Expenses
- Tithe and Travel Portion
- Savings
- Savings %

### Income

Use confirmed cash-flow income only.

Do not count as income:
- internal transfers
- refunds
- reimbursements
- investment sales/proceeds
- loan proceeds
- ambiguous deposits unless Finances or Kero confirms them as income

### Expenses

Use actual economic spending.

Exclude:
- internal transfers
- credit-card repayments
- investment funding

Apply refunds/reimbursements appropriately so spending is not overstated.

Use posted transactions only for the Monthly Tracking totals.

## Existing spreadsheet logic

Preserve:
- formatting
- formulas
- historical values
- row/column structure
- existing calculation logic

For `Tithe and Travel Portion`, `Savings`, and `Savings %`, preserve and extend the workbook's existing formulas rather than inventing new calculations.

Do not overwrite formula-driven cells with hardcoded values unless the existing workbook clearly stores that value manually.

## Accuracy checks

Before finishing:

- verify no transaction was duplicated
- verify pending transactions are excluded from monthly totals
- verify transfers are not counted as spending or income
- verify credit-card payments are not double-counted
- verify Monthly Tracking agrees with the classified Finances transactions
- verify existing formulas still work
- verify no unrelated tabs or historical periods were altered

If Finances reports incomplete or partially synced data, do not present the spreadsheet as fully updated. Explain what data is missing.

## Final response

Keep the response concise.

Report:
- number of transactions added
- current month's income
- current month's expenses
- resulting savings / savings percentage if calculated by the sheet
- any pending or ambiguous items
- whether the update reconciled successfully
