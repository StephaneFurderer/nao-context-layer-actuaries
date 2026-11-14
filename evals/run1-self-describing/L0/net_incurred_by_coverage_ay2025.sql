SELECT c.coverage, SUM(CASE WHEN t.txn_type='recovery' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
FROM mart.claims c
JOIN mart.policies p USING (policy_id)
JOIN mart.claim_transactions t USING (claim_id)
WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025
GROUP BY 1 ORDER BY 1;
