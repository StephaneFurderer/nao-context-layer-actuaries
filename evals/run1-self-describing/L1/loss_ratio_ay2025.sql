WITH inc AS (
  SELECT SUM(CASE t.txn_type WHEN 'recovery' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  JOIN mart.claim_transactions t USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND c.loss_date >= DATE '2025-01-01' AND c.loss_date < DATE '2026-01-01'
), ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e
  JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND e.accounting_month >= DATE '2025-01-01' AND e.accounting_month < DATE '2026-01-01'
)
SELECT inc.net_incurred / ep.earned AS loss_ratio FROM inc, ep;
