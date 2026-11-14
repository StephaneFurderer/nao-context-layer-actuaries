WITH pol AS (
  SELECT policy_id, destination_region FROM mart.policies
  WHERE partner_code <> 'ZZTEST' AND policy_status <> 'cancelled_free_look'
    AND departure_date >= DATE '2025-01-01' AND departure_date < DATE '2026-01-01'
)
SELECT pol.destination_region, COUNT(DISTINCT c.claim_id) * 1.0 / COUNT(DISTINCT pol.policy_id) AS claim_frequency
FROM pol LEFT JOIN mart.claims c USING (policy_id)
GROUP BY 1 ORDER BY 1;
