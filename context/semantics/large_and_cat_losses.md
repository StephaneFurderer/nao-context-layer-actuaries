---
owner: reserving actuary (see CODEOWNERS)
status: approved
last_reviewed: 2026-11-14
---
# Large losses, catastrophe losses, attritional loss ratio

Company conventions. These are decisions, not facts you can derive from the data.

- **Large loss** = a single claim whose net incurred (see `loss_ratio.md`) is **≥ $10,000**. This is our per-risk reinsurance retention.
- **Catastrophe (cat) loss** = a claim tagged with a `claims.cat_event_code`. `HU25` is the 2025 Caribbean hurricane season event, declared by the claims committee.
- **Attritional loss ratio** = loss ratio after removing:
  1. every cat-coded claim, entirely;
  2. the part of any remaining claim above $10,000. The claim is **capped** at $10,000, not dropped.

  The denominator is unchanged: earned premium, same year, ZZTEST excluded.
- Report attritional and all-in loss ratios side by side. When the gap between them is large, say what drives it.

Pattern (attritional, AY :year)
```sql
WITH per_claim AS (
  SELECT c.claim_id,
         SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c   USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = :year AND p.partner_code <> 'ZZTEST' AND c.cat_event_code IS NULL
  GROUP BY 1
)
SELECT SUM(LEAST(net_incurred, 10000)) AS attritional_incurred FROM per_claim;
```
