SELECT DATE_TRUNC('month', c.loss_date)::DATE AS loss_month, COUNT(*) AS claim_count
FROM mart.claims c JOIN mart.policies p USING(policy_id)
WHERE p.partner_code <> 'ZZTEST' AND p.destination_region='Caribbean' AND c.coverage='trip_cancellation' AND YEAR(c.loss_date)=2025
GROUP BY 1 ORDER BY 1;
