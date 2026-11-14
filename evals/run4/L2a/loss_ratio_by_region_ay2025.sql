WITH inc AS (
  SELECT c.claim_id, c.coverage, c.cat_event_code, p.destination_region,
         COALESCE(SUM(CASE t.txn_code WHEN '10' THEN t.amount_usd WHEN '20' THEN t.amount_usd WHEN '40' THEN -t.amount_usd ELSE 0 END),0) AS incurred
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  LEFT JOIN mart.claim_transactions t USING (claim_id)
  WHERE YEAR(c.loss_date)=2025 AND p.partner_code<>'ZZTEST'
  GROUP BY ALL),
ep AS (
  SELECT p.destination_region, SUM(e.earned_premium_usd) AS ep
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE e.accounting_month >= DATE '2025-01-01' AND e.accounting_month < DATE '2026-01-01' AND p.partner_code<>'ZZTEST'
  GROUP BY ALL),
i AS (SELECT destination_region, SUM(incurred) AS inc FROM inc GROUP BY 1)
SELECT ep.destination_region, COALESCE(i.inc,0)/ep.ep AS loss_ratio FROM ep LEFT JOIN i USING (destination_region) ORDER BY 1;
