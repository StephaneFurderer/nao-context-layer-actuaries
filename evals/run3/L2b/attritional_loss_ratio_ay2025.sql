WITH per_claim AS (
  SELECT c.claim_id,
         SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST' AND c.cat_event_code IS NULL
  GROUP BY 1
), inc AS (SELECT SUM(LEAST(net_incurred, 10000)) AS x FROM per_claim),
ep AS (
  SELECT SUM(e.earned_premium_usd) AS earned
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE YEAR(e.accounting_month) = 2025 AND p.partner_code <> 'ZZTEST'
)
SELECT x / earned AS attritional_loss_ratio FROM inc, ep;
