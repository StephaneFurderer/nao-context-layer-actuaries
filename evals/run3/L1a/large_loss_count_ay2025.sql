WITH ni AS (
  SELECT claim_id, SUM(CASE txn_code WHEN '40' THEN -amount_usd ELSE amount_usd END) AS net_incurred
  FROM mart.claim_transactions GROUP BY 1)
SELECT count(*) AS large_loss_count
FROM mart.claims c JOIN mart.policies p USING (policy_id) JOIN ni USING (claim_id)
WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025 AND ni.net_incurred >= 10000
