with pol as (select * from mart.policies where partner_code<>'ZZTEST'),
ci as (select claim_id,
  sum(case when txn_code in ('10','20') then amount_usd else 0 end) gross_incurred,
  sum(case when txn_code='10' then amount_usd when txn_code='20' then amount_usd when txn_code='40' then -amount_usd else 0 end) net_incurred
  from mart.claim_transactions group by 1),
cl as (select c.claim_id,c.coverage,c.loss_date,c.cat_event_code,p.destination_region,p.departure_date,p.policy_id,
  coalesce(ci.gross_incurred,0) gross_incurred, coalesce(ci.net_incurred,0) net_incurred
  from mart.claims c join pol p using(policy_id) left join ci using(claim_id))
select ep.destination_region, coalesce(l.inc,0)/ep.ep as loss_ratio from (select p.destination_region, sum(e.earned_premium_usd) ep from mart.earned_premium_monthly e join pol p using(policy_id) where year(accounting_month)=2025 group by 1) ep left join (select destination_region, sum(net_incurred) inc from cl where year(loss_date)=2025 group by 1) l using(destination_region) order by 1;
