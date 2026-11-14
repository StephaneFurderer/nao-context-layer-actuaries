with ci as (
  select c.claim_id, c.coverage, c.loss_date, c.cat_event_code, p.destination_region,
         sum(case when t.txn_code in ('10','20') then t.amount_usd else 0 end)
         - sum(case when t.txn_code='40' then t.amount_usd else 0 end) as net_incurred,
         sum(case when t.txn_code in ('10','20') then t.amount_usd else 0 end) as gross_incurred
  from mart.claims c
  join mart.policies p using(policy_id)
  left join mart.claim_transactions t using(claim_id)
  where p.partner_code <> 'ZZTEST'
  group by all
)
select coverage, round(sum(net_incurred),2) as net_incurred_usd
from ci where year(loss_date)=2025
group by coverage order by coverage;
