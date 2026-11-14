select p.destination_region, count(c.claim_id)*1.0/count(distinct p.policy_id) as claim_frequency
from mart.policies p left join mart.claims c using(policy_id)
where year(p.departure_date)=2025 and p.partner_code<>'ZZTEST' and p.policy_status<>'CX'
group by 1 order by 1
