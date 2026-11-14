WITH pol AS (
  SELECT destination_region, COUNT(*) AS n_pol
  FROM mart.policies
  WHERE YEAR(departure_date) = 2025 AND partner_code <> 'ZZTEST' AND policy_status <> 'cancelled_free_look'
  GROUP BY 1
), cl AS (
  SELECT p.destination_region, COUNT(DISTINCT c.claim_id) AS n_claims
  FROM mart.claims c
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(p.departure_date) = 2025 AND p.partner_code <> 'ZZTEST'
  GROUP BY 1
)
SELECT pol.destination_region, ROUND(COALESCE(cl.n_claims,0) * 1000.0 / pol.n_pol, 1) AS claims_per_1000_policies
FROM pol LEFT JOIN cl USING (destination_region)
ORDER BY 1;
