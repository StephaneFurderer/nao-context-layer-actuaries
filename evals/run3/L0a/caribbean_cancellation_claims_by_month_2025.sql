select date_trunc('month',c.loss_date)::date as loss_month, count(*) as claim_count
from mart.claims c join mart.policies p using(policy_id)
where p.partner_code<>'ZZTEST' and p.destination_region='Caribbean' and c.coverage='trip_cancellation' and year(c.loss_date)=2025
group by 1 order by 1;
