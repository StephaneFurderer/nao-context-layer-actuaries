WITH m AS (SELECT CAST(unnest(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH)) AS DATE) AS loss_month),
c AS (
  SELECT date_trunc('month', c.loss_date)::DATE AS loss_month, COUNT(*) AS n
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND p.destination_region = 'Caribbean'
    AND c.coverage = 'trip_cancellation' AND year(c.loss_date) = 2025
  GROUP BY 1
)
SELECT m.loss_month, COALESCE(c.n,0) AS claim_count FROM m LEFT JOIN c USING (loss_month) ORDER BY 1;
