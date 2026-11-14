WITH pol AS (
  SELECT destination_region, COUNT(*) AS policies
  FROM mart.policies
  WHERE partner_code <> 'ZZTEST' AND policy_status <> 'cancelled_free_look' AND year(departure_date) = 2025
  GROUP BY 1
), cl AS (
  SELECT p.destination_region, COUNT(*) AS claims
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND p.policy_status <> 'cancelled_free_look' AND year(p.departure_date) = 2025
  GROUP BY 1
)
SELECT pol.destination_region, COALESCE(cl.claims,0)::DOUBLE / pol.policies AS claim_frequency
FROM pol LEFT JOIN cl USING (destination_region) ORDER BY 1;
