SELECT DATE_TRUNC('month', c.loss_date)::DATE AS loss_month, COUNT(DISTINCT c.claim_id) AS claim_count
FROM mart.claims c JOIN mart.policies p USING (policy_id)
WHERE YEAR(c.loss_date) = 2025 AND c.coverage = 'trip_cancellation'
  AND p.destination_region = 'Caribbean' AND p.partner_code <> 'ZZTEST'
GROUP BY 1 ORDER BY 1;
