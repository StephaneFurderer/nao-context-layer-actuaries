SELECT SUM(e.earned_premium_usd) AS earned_premium_usd
FROM mart.earned_premium_monthly e
JOIN mart.policies p USING (policy_id)
WHERE YEAR(e.accounting_month) = 2026 AND p.partner_code <> 'ZZTEST';
