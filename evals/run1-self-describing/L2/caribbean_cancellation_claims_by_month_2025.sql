WITH m AS (SELECT UNNEST(range(1,13)) AS loss_month),
cl AS (
  SELECT MONTH(c.loss_date) AS loss_month, COUNT(DISTINCT c.claim_id) AS n_claims
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND c.coverage = 'trip_cancellation'
    AND p.destination_region = 'Caribbean' AND p.partner_code <> 'ZZTEST'
  GROUP BY 1
)
SELECT m.loss_month, COALESCE(cl.n_claims,0) AS claim_count
FROM m LEFT JOIN cl USING (loss_month)
ORDER BY 1;
