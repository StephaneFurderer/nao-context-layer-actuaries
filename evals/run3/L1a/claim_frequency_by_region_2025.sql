WITH pol AS (
  SELECT policy_id, destination_region FROM mart.policies
  WHERE partner_code <> 'ZZTEST' AND policy_status <> 'CX' AND year(departure_date) = 2025),
cl AS (SELECT policy_id, count(*) AS n FROM mart.claims GROUP BY 1)
SELECT pol.destination_region, coalesce(sum(cl.n), 0)::DOUBLE / count(*) AS claim_frequency
FROM pol LEFT JOIN cl USING (policy_id) GROUP BY 1 ORDER BY 1
