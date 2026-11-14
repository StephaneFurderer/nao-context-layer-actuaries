with ni as (select claim_id, sum(case when txn_code in ('10','20') then amount_usd when txn_code='40' then -amount_usd else 0 end) n from mart.claim_transactions group by 1)
select count(*) as large_loss_count from mart.claims c join ni using(claim_id) join mart.policies p using(policy_id)
where year(c.loss_date)=2025 and p.partner_code<>'ZZTEST' and ni.n>=10000
