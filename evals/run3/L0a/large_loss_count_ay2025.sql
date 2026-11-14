with ci as (select t.claim_id, sum(case when txn_code in ('10','20') then amount_usd when txn_code='40' then -amount_usd end) inc from mart.claim_transactions t group by 1),
cl as (select c.*, p.destination_region, coalesce(ci.inc,0) inc from mart.claims c join mart.policies p using(policy_id) left join ci using(claim_id) where p.partner_code<>'ZZTEST')
select count(*) as large_loss_count from cl where year(loss_date)=2025 and inc>=10000;
