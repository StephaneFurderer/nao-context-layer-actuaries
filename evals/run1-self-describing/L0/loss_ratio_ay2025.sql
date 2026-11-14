WITH inc AS (
  SELECT SUM(CASE WHEN t.txn_type='recovery' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  JOIN mart.claim_transactions t USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025
), ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e
  JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(e.accounting_month) = 2025
)
SELECT inc.net_incurred / ep.earned AS loss_ratio FROM inc, ep;
