SELECT SUM(e.earned_premium_usd) AS earned_premium_usd
FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
WHERE e.accounting_month >= DATE '2026-01-01' AND p.partner_code<>'ZZTEST';
