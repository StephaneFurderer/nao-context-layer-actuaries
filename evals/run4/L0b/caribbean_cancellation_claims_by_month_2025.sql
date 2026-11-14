with pol as (select * from mart.policies where partner_code<>'ZZTEST'),
ci as (select claim_id,
  sum(case when txn_code in ('10','20') then amount_usd else 0 end) gross_incurred,
  sum(case when txn_code='10' then amount_usd when txn_code='20' then amount_usd when txn_code='40' then -amount_usd else 0 end) net_incurred
  from mart.claim_transactions group by 1),
cl as (select c.claim_id,c.coverage,c.loss_date,c.cat_event_code,p.destination_region,p.departure_date,p.policy_id,
  coalesce(ci.gross_incurred,0) gross_incurred, coalesce(ci.net_incurred,0) net_incurred
  from mart.claims c join pol p using(policy_id) left join ci using(claim_id))
select m::date as loss_month, count(cl.claim_id) as claim_count from generate_series(date '2025-01-01', date '2025-12-01', interval 1 month) t(m) left join cl on date_trunc('month',cl.loss_date)=m and cl.coverage='trip_cancellation' and cl.destination_region='Caribbean' group by 1 order by 1;
