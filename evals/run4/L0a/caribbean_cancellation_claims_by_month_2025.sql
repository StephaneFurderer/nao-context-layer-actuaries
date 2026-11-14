with m as (select cast(unnest(generate_series(date '2025-01-01', date '2025-12-01', interval 1 month)) as date) as loss_month),
c as (
  select date_trunc('month', c.loss_date)::date as loss_month, count(*) as n
  from mart.claims c join mart.policies p using(policy_id)
  where p.partner_code <> 'ZZTEST' and p.destination_region='Caribbean'
    and c.coverage='trip_cancellation' and year(c.loss_date)=2025
  group by 1
)
select m.loss_month, coalesce(c.n,0) as claim_count from m left join c using(loss_month) order by 1;
