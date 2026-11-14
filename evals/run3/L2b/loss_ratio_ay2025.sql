WITH inc AS (
  SELECT SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST'
), ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE YEAR(e.accounting_month) = 2025 AND p.partner_code <> 'ZZTEST'
)
SELECT net_incurred / earned AS loss_ratio FROM inc, ep;
