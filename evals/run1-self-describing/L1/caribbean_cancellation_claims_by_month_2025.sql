WITH m AS (SELECT UNNEST(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH))::DATE AS loss_month),
cl AS (
  SELECT DATE_TRUNC('month', c.loss_date)::DATE AS loss_month, COUNT(*) AS n
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND p.destination_region = 'Caribbean' AND c.coverage = 'trip_cancellation'
    AND c.loss_date >= DATE '2025-01-01' AND c.loss_date < DATE '2026-01-01'
  GROUP BY 1
)
SELECT m.loss_month, COALESCE(cl.n,0) AS claim_count FROM m LEFT JOIN cl USING (loss_month) ORDER BY 1;
