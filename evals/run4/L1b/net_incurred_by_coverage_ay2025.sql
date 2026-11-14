WITH inc AS (SELECT t.claim_id, SUM(CASE t.txn_code WHEN '10' THEN t.amount_usd WHEN '20' THEN t.amount_usd WHEN '40' THEN -t.amount_usd ELSE 0 END) AS net_incurred FROM mart.claim_transactions t GROUP BY 1),
cl AS (SELECT c.claim_id, c.coverage, c.loss_date, c.cat_event_code, p.destination_region, COALESCE(i.net_incurred,0) AS net_incurred FROM mart.claims c JOIN mart.policies p USING(policy_id) LEFT JOIN inc i USING(claim_id) WHERE p.partner_code <> 'ZZTEST')
SELECT coverage, SUM(net_incurred) AS net_incurred_usd FROM cl WHERE YEAR(loss_date)=2025 GROUP BY 1 ORDER BY 1;
