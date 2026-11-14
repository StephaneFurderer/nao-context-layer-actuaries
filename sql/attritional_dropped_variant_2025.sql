-- The OTHER defensible convention: drop large claims entirely instead of capping them at $5,000.
-- This is what blind agents tend to do when the convention is not written down.
WITH per_claim AS (
  SELECT c.claim_id, c.cat_event_code,
         SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c   USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST'
  GROUP BY 1, 2
), ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE YEAR(e.accounting_month) = 2025 AND p.partner_code <> 'ZZTEST'
)
SELECT SUM(incurred) FILTER (WHERE cat_event_code IS NULL AND incurred < 5000) / MAX(earned) AS attritional_dropped
FROM per_claim, ep;
