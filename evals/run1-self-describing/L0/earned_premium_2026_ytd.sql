SELECT SUM(e.earned_premium_usd) AS earned_premium_usd
FROM mart.earned_premium_monthly e
JOIN mart.policies p USING (policy_id)
WHERE p.partner_code <> 'ZZTEST' AND year(e.accounting_month) = 2026;
