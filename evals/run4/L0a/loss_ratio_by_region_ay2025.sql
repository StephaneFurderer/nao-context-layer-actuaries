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
, inc as (select destination_region, sum(net_incurred) as inc from ci where year(loss_date)=2025 group by 1),
ep as (
  select p.destination_region, sum(e.earned_premium_usd) as ep
  from mart.earned_premium_monthly e join mart.policies p using(policy_id)
  where p.partner_code <> 'ZZTEST' and year(e.accounting_month)=2025
  group by 1
)
select ep.destination_region, coalesce(inc.inc,0)/ep.ep as loss_ratio
from ep left join inc using(destination_region) order by 1;
