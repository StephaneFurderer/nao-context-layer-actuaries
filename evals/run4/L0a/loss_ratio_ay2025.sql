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
, ep as (
  select sum(e.earned_premium_usd) as ep
  from mart.earned_premium_monthly e join mart.policies p using(policy_id)
  where p.partner_code <> 'ZZTEST' and year(e.accounting_month)=2025
)
select (select sum(net_incurred) from ci where year(loss_date)=2025) / ep as loss_ratio from ep;
