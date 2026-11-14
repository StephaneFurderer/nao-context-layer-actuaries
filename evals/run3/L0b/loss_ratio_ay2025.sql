with ni as (select claim_id, sum(case when txn_code in ('10','20') then amount_usd when txn_code='40' then -amount_usd else 0 end) n from mart.claim_transactions group by 1),
l as (select sum(ni.n) n from mart.claims c join ni using(claim_id) join mart.policies p using(policy_id)
 where year(c.loss_date)=2025 and p.partner_code<>'ZZTEST'),
e as (select sum(e.earned_premium_usd) ep from mart.earned_premium_monthly e join mart.policies p using(policy_id)
 where year(e.accounting_month)=2025 and p.partner_code<>'ZZTEST')
select l.n/e.ep as loss_ratio from l,e
