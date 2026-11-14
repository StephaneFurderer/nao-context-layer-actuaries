-- Reference answer, signed off by the reserving actuary (definitions in semantics/loss_ratio.md)
WITH incurred AS (
  SELECT SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS incurred_usd
  FROM mart.claim_transactions t
  JOIN mart.claims   c USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025
    AND p.partner_code <> 'ZZTEST'
), earned AS (
  SELECT SUM(e.earned_premium_usd) AS earned_premium_usd
  FROM mart.earned_premium_monthly e
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(e.accounting_month) = 2025
    AND p.partner_code <> 'ZZTEST'
)
SELECT ROUND(incurred_usd / earned_premium_usd, 4) AS loss_ratio
FROM incurred, earned;
