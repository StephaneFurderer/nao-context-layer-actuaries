WITH pol AS (
  SELECT policy_id, destination_region FROM mart.policies
  WHERE YEAR(departure_date)=2025 AND policy_status<>'CX' AND partner_code<>'ZZTEST'),
cl AS (SELECT pol.destination_region, COUNT(DISTINCT c.claim_id) AS n FROM mart.claims c JOIN pol USING (policy_id) GROUP BY 1),
d AS (SELECT destination_region, COUNT(*) AS n FROM pol GROUP BY 1)
SELECT d.destination_region, ROUND(COALESCE(cl.n,0)*1000.0/d.n,1) AS claims_per_1000_policies
FROM d LEFT JOIN cl USING (destination_region) ORDER BY 1;
