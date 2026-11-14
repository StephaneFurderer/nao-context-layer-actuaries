WITH ni AS (
  SELECT claim_id, SUM(CASE txn_code WHEN '40' THEN -amount_usd ELSE amount_usd END) AS net_incurred
  FROM mart.claim_transactions GROUP BY 1),
l AS (
  SELECT p.destination_region, SUM(ni.net_incurred) AS inc
  FROM mart.claims c JOIN mart.policies p USING (policy_id) JOIN ni USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025 GROUP BY 1),
e AS (
  SELECT p.destination_region, SUM(e.earned_premium_usd) AS ep
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(e.accounting_month) = 2025 GROUP BY 1)
SELECT e.destination_region, coalesce(l.inc, 0) / e.ep AS loss_ratio
FROM e LEFT JOIN l USING (destination_region) ORDER BY 1
