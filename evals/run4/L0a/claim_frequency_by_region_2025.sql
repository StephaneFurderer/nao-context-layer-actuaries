select p.destination_region,
       count(c.claim_id)::double / count(distinct p.policy_id) as claim_frequency
from mart.policies p left join mart.claims c using(policy_id)
where p.partner_code <> 'ZZTEST' and p.policy_status <> 'CX' and year(p.departure_date)=2025
group by 1 order by 1;
