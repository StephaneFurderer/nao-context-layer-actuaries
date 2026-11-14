select sum(e.earned_premium_usd) as earned_premium_usd
from mart.earned_premium_monthly e join mart.policies p using(policy_id)
where p.partner_code <> 'ZZTEST' and year(e.accounting_month)=2026;
