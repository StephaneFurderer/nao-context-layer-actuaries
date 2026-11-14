WITH pol AS (SELECT policy_id, destination_region FROM mart.policies WHERE partner_code <> 'ZZTEST' AND policy_status <> 'CX' AND departure_date >= DATE '2025-01-01' AND departure_date < DATE '2026-01-01'),
cl AS (SELECT pol.destination_region, COUNT(DISTINCT c.claim_id) AS n FROM mart.claims c JOIN pol USING(policy_id) GROUP BY 1),
pc AS (SELECT destination_region, COUNT(*) AS np FROM pol GROUP BY 1)
SELECT pc.destination_region, ROUND(COALESCE(cl.n,0) * 1000.0 / pc.np, 1) AS claims_per_1000_policies FROM pc LEFT JOIN cl USING(destination_region) ORDER BY 1;
