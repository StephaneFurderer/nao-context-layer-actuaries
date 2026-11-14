SELECT c.coverage,
       SUM(CASE t.txn_type WHEN 'recovery' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
FROM mart.claim_transactions t
JOIN mart.claims c USING (claim_id)
JOIN mart.policies p USING (policy_id)
WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST'
GROUP BY 1
ORDER BY 1;
