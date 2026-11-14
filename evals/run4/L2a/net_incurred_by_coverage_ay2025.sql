WITH inc AS (
  SELECT c.claim_id, c.coverage, c.cat_event_code, p.destination_region,
         COALESCE(SUM(CASE t.txn_code WHEN '10' THEN t.amount_usd WHEN '20' THEN t.amount_usd WHEN '40' THEN -t.amount_usd ELSE 0 END),0) AS incurred
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  LEFT JOIN mart.claim_transactions t USING (claim_id)
  WHERE YEAR(c.loss_date)=2025 AND p.partner_code<>'ZZTEST'
  GROUP BY ALL)
SELECT coverage, SUM(incurred) AS net_incurred_usd FROM inc GROUP BY 1 ORDER BY 1;
