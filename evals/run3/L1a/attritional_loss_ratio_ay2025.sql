WITH ni AS (
  SELECT t.claim_id, SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS net_incurred
  FROM mart.claim_transactions t GROUP BY 1),
cl AS (
  SELECT c.claim_id, ni.net_incurred, c.cat_event_code
  FROM mart.claims c JOIN mart.policies p USING (policy_id) JOIN ni USING (claim_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(c.loss_date) = 2025),
ep AS (
  SELECT SUM(e.earned_premium_usd) AS ep
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST' AND year(e.accounting_month) = 2025)
SELECT (SELECT SUM(net_incurred) FROM cl WHERE cat_event_code IS NULL AND net_incurred < 10000) / (SELECT ep FROM ep) AS attritional_loss_ratio
