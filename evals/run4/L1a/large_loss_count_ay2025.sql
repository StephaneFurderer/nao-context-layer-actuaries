WITH inc AS (
  SELECT c.claim_id, c.coverage, c.cat_event_code, p.destination_region,
         SUM(CASE t.txn_code WHEN '10' THEN t.amount_usd WHEN '20' THEN t.amount_usd WHEN '40' THEN -t.amount_usd ELSE 0 END) AS net_incurred
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  LEFT JOIN mart.claim_transactions t USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND p.policy_status <> 'CX' AND year(c.loss_date) = 2025
  GROUP BY ALL
)
SELECT COUNT(*) AS large_loss_count FROM inc WHERE net_incurred >= 10000;
