WITH pol AS (SELECT policy_id, destination_region FROM mart.policies WHERE partner_code <> 'ZZTEST' AND policy_status <> 'CX' AND YEAR(departure_date)=2025),
n AS (SELECT p.destination_region, COUNT(c.claim_id) AS claims, COUNT(DISTINCT p.policy_id) AS pols FROM pol p LEFT JOIN mart.claims c USING(policy_id) GROUP BY 1)
SELECT destination_region, claims::DOUBLE / pols AS claim_frequency FROM n ORDER BY 1;
