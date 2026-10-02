# DatavionOS SaaS Invoice -> Enterprise Finance

## Canonical ownership

### SaaS billing

`apps/platform/saas_billing`

Owns:

- SaaS subscriptions
- SaaS plans
- SaaS invoices
- SaaS billing lifecycle
- subscription billing status

### Healthcare billing

`apps/revenue_cycle/billing`

Owns:

- patient/clinical billing
- healthcare claims
- healthcare revenue-cycle workflows
- healthcare-specific invoices

Healthcare billing must remain independent from SaaS financial billing.

### Enterprise finance

`apps/billing/finance`

Owns:

- financial transactions
- financial ledger/accounting boundaries
- enterprise payment records
- financial settlement records
- cross-domain financial reporting

## Integration contract

A SaaS invoice may create an enterprise finance transaction.

The integration should carry:

- SaaS invoice identifier
- organization identifier
- subscription identifier
- invoice number
- invoice date
- due date
- currency
- subtotal
- tax amount
- total amount
- payment status
- payment method
- Razorpay order identifier when applicable
- Razorpay payment identifier when applicable
- Razorpay signature verification state when applicable
- source domain
- source document type

## Domain separation

SaaS billing is the billing source.

Enterprise finance is the financial accounting destination.

Healthcare billing is a separate domain and must not be used as the
financial destination for SaaS subscription invoices.

## Free subscriptions

For a zero-value SaaS invoice:

- no Razorpay order is required
- invoice may be auto-settled
- enterprise finance may record the zero-value transaction if the
  canonical finance policy requires it

## Paid subscriptions

For a paid SaaS invoice:

1. SaaS billing creates the invoice.
2. Razorpay TEST/LIVE payment flow handles payment according to the
   configured environment.
3. Payment verification establishes the payment reference.
4. SaaS billing records settlement.
5. Enterprise finance receives the financial transaction/reference.
6. Organization activation follows the existing subscription workflow.

## Important

Do not duplicate invoice models between SaaS billing and enterprise
finance unless the existing canonical architecture explicitly requires
a financial document model.

Do not merge healthcare billing with SaaS billing.


## Runtime integration

The canonical SaaS invoice is the source document.

When a SaaS invoice reaches `paid` or `settled`, the SaaS billing
domain may call:

`apps.platform.saas_billing.services.enterprise_finance_integration.settle_saas_invoice_in_finance`

The integration:

1. Resolves the organization's open fiscal period.
2. Resolves the configured SaaS revenue ledger account.
3. Resolves the configured Razorpay/payment ledger account.
4. Creates a balanced enterprise finance journal entry.
5. Posts the journal entry.
6. Uses the canonical FinanceIdempotencyKey service to prevent duplicate posting.
7. Records a FinanceAuditLog entry.
8. Preserves the original SaaS invoice as the billing source of truth.

### Required environment configuration

`DATAVIONOS_FINANCE_SAAS_REVENUE_ACCOUNT_CODE`

`DATAVIONOS_FINANCE_RAZORPAY_ACCOUNT_CODE`

These values are organization chart-of-account codes and must not be
hard-coded in application source.

Healthcare billing remains independent.
