select sum(e.earned_premium_usd) as earned_premium_usd
from mart.earned_premium_monthly e join mart.policies p using(policy_id)
where year(e.accounting_month)=2026 and p.partner_code<>'ZZTEST'
