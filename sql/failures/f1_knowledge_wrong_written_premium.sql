-- F1 · The knowledge was wrong: someone wrote "loss ratio uses WRITTEN premium" in the definition.
-- Everything else is correct (recoveries netted, ZZTEST excluded, accident year).
WITH inc AS (
  SELECT SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS incurred
  FROM mart.claim_transactions t JOIN mart.claims c USING (claim_id) JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025 AND p.partner_code <> 'ZZTEST'
), wp AS (
  SELECT SUM(written_premium_usd) AS written FROM mart.policies
  WHERE YEAR(purchase_date) = 2025 AND partner_code <> 'ZZTEST'
)
SELECT ROUND(incurred / written, 4) AS loss_ratio_wrong_definition FROM inc, wp;
