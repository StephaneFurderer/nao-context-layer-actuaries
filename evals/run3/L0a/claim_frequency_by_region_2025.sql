with pol as (select policy_id, destination_region from mart.policies where partner_code<>'ZZTEST' and year(departure_date)=2025),
cc as (select policy_id, count(*) n from mart.claims group by 1)
select destination_region, coalesce(sum(n),0)/count(*) as claim_frequency
from pol left join cc using(policy_id) group by 1 order by 1;
