WITH per_claim AS (
  SELECT c.claim_id,
         SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t
  JOIN mart.claims c USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST'
  GROUP BY 1
)
SELECT COUNT(*) AS large_loss_count FROM per_claim WHERE net_incurred >= 10000;
