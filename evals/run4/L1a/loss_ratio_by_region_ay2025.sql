WITH inc AS (
  SELECT c.claim_id, c.coverage, c.cat_event_code, p.destination_region,
         SUM(CASE t.txn_code WHEN '10' THEN t.amount_usd WHEN '20' THEN t.amount_usd WHEN '40' THEN -t.amount_usd ELSE 0 END) AS net_incurred
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  LEFT JOIN mart.claim_transactions t USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND p.policy_status <> 'CX' AND year(c.loss_date) = 2025
  GROUP BY ALL
),
l AS (SELECT destination_region, SUM(net_incurred) AS inc FROM inc GROUP BY 1),
ep AS (
  SELECT p.destination_region, SUM(e.earned_premium_usd) AS ep
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(e.accounting_month) = 2025
  GROUP BY 1
)
SELECT ep.destination_region, COALESCE(l.inc,0) / ep.ep AS loss_ratio
FROM ep LEFT JOIN l USING (destination_region) ORDER BY 1;
