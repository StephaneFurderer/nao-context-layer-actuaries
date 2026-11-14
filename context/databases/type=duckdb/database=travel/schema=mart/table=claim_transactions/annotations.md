---
type: manual
comment: These are manual notes you want the agent to keep in mind, safe to edit.
owner: reserving actuary (see CODEOWNERS)
---

# claim_transactions: financial movements on claims

- Grain: one row per transaction. `txn_code` (legacy claims-system codes):
  - `10` = payment: money paid out (positive).
  - `20` = case reserve change: positive is an increase, negative is a release. The running sum is the outstanding case reserve.
  - `40` = recovery: money recovered from airlines or third parties. **Stored as a positive amount but reduces the loss**, so subtract it.
- Net incurred to date = SUM(code 10) + SUM(code 20) - SUM(code 40). Never a plain SUM(amount_usd).
- Transactions are valued as at 2026-09-30.
