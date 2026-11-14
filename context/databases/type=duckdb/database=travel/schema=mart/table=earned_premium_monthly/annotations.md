---
type: manual
comment: These are manual notes you want the agent to keep in mind, safe to edit.
owner: reserving actuary (see CODEOWNERS)
---

# earned_premium_monthly: earned premium per policy per accounting month

- Grain: one row per (`policy_id`, `accounting_month`). `accounting_month` is the first day of the month.
- Premium is earned pro rata by day from `purchase_date` to `return_date`, cut at the valuation date (2026-09-30). Unearned premium has no row yet.
- Free-look cancellations have no rows: they earn nothing.
- This is the **only** premium base for loss ratios. Join to `mart.policies` to filter by partner or segment.
