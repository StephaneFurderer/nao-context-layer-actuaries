---
owner: reserving actuary (see /CODEOWNERS)
status: approved
last_reviewed: 2026-11-14
---
# Loss ratio (canonical definition)

**Loss ratio = incurred losses ÷ earned premium, on an accident-year basis.**

- **Accident year (AY):** the year of the claim's `loss_date`. This is the default whenever someone says "2025 loss ratio".
- **Incurred losses:** payments (`txn_code '10'`) plus case reserve changes (`'20'`), minus recoveries (`'40'`). Include every transaction on claims whose loss falls in the accident year.
  - Incurred is net of **recoveries** (airline and third-party), but **gross of reinsurance**.
  - LAE is not included; it is not in this warehouse.
- **Earned premium:** gross earned premium from `mart.earned_premium_monthly`, for accounting months in the same calendar year. It is before partner commission.
  - Our earning is a simplification: straight line from purchase to return.
- **Exclusions:** partner `ZZTEST` is removed from both incurred and earned premium.
- **Valuation:** 2026-09-30. Case reserves only, **no IBNR**. Recent accident periods are immature; say so whenever AY 2026 appears.
- **Other bases:** report year (`YEAR(report_date)`) and underwriting year (`YEAR(purchase_date)`) are used only when the user asks for them. Name the basis in the answer.
- **Never:** use written premium in a loss ratio, or sum transaction amounts without signing the recoveries.
- **Segments** (region, product, partner): filter incurred and earned premium on the same policy attribute, through `mart.policies`.
