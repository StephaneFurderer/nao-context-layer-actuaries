select m::date as loss_month, count(c.claim_id) as claim_count
from generate_series(date '2025-01-01', date '2025-12-01', interval 1 month) t(m)
left join (select c.* from mart.claims c join mart.policies p using(policy_id)
 where p.destination_region='Caribbean' and p.partner_code<>'ZZTEST' and c.coverage='trip_cancellation') c
 on date_trunc('month',c.loss_date)=t.m
group by 1 order by 1
