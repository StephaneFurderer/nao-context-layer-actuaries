with ci as (select t.claim_id, sum(case when txn_code in ('10','20') then amount_usd when txn_code='40' then -amount_usd end) inc from mart.claim_transactions t group by 1),
cl as (select c.*, p.destination_region, coalesce(ci.inc,0) inc from mart.claims c join mart.policies p using(policy_id) left join ci using(claim_id) where p.partner_code<>'ZZTEST'),
ep as (select sum(earned_premium_usd) ep from mart.earned_premium_monthly e join mart.policies p using(policy_id) where p.partner_code<>'ZZTEST' and year(accounting_month)=2025)
select (select sum(inc) from cl where year(loss_date)=2025)/ep.ep as loss_ratio from ep;
