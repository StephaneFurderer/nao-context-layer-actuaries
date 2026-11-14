WITH ni AS (
  SELECT claim_id, SUM(CASE txn_code WHEN '40' THEN -amount_usd ELSE amount_usd END) AS net_incurred
  FROM mart.claim_transactions GROUP BY 1)
SELECT c.coverage, SUM(ni.net_incurred) AS net_incurred_usd
FROM mart.claims c JOIN mart.policies p USING (policy_id) JOIN ni USING (claim_id)
WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025
GROUP BY 1 ORDER BY 1
