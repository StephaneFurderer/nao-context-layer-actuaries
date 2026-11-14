WITH pol AS (
  SELECT destination_region, COUNT(*) AS policies FROM mart.policies
  WHERE YEAR(departure_date)=2025 AND policy_status<>'CX' AND partner_code<>'ZZTEST' GROUP BY 1
), cl AS (
  SELECT p.destination_region, COUNT(DISTINCT c.claim_id) AS claims
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  WHERE YEAR(p.departure_date)=2025 AND p.partner_code<>'ZZTEST' GROUP BY 1
)
SELECT pol.destination_region, ROUND(COALESCE(cl.claims,0)*1000.0/pol.policies,1) AS claims_per_1000_policies
FROM pol LEFT JOIN cl USING (destination_region) ORDER BY 1;
