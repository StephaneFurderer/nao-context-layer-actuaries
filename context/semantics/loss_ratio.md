---
owner: reserving actuary (see CODEOWNERS)
status: approved
last_reviewed: 2026-11-14
---
# Loss ratio (canonical definition)

**Loss ratio = net incurred losses / earned premium**, on an **accident-year** basis.

| Piece | Definition | Source |
|---|---|---|
| Accident year (AY) | `YEAR(claims.loss_date)` | `mart.claims` |
| Net incurred | payments (`txn_code '10'`) + case reserve changes (`'20'`) - recoveries (`'40'`) for claims with loss in the AY | `mart.claim_transactions` |
| Earned premium | `SUM(earned_premium_usd)` for `accounting_month` in the same calendar year | `mart.earned_premium_monthly` |
| Exclusions | `partner_code = 'ZZTEST'` on both numerator and denominator | `mart.policies` |

Rules
- "2025 loss ratio" means AY 2025 unless the user says report year or underwriting year. State the basis in the answer.
- Never use `written_premium_usd` for a loss ratio.
- For a segment (region, product, partner), filter numerator and denominator by the same policy attribute, joined through `mart.policies`.
- Losses are valued as at 2026-09-30 and include case reserves but **no IBNR**. Recent accident periods are immature: say so when AY 2026 is shown.

Pattern
```sql
WITH inc AS (
  SELECT SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c   USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = :year AND p.partner_code <> 'ZZTEST'
), ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(e.accounting_month) = :year AND p.partner_code <> 'ZZTEST'
)
SELECT net_incurred / earned AS loss_ratio FROM inc, ep;
```
