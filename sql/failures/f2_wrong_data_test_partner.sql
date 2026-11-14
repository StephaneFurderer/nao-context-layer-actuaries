-- F2 · The data was wrong: the right definition, applied to the wrong rows.
-- The QA test partner (ZZTEST) is left in, on both incurred and earned premium.
WITH inc_all AS (
  SELECT SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) AS incurred
  FROM mart.claim_transactions t JOIN mart.claims c USING (claim_id)
  WHERE YEAR(c.loss_date) = 2025
), ep_all AS (
  SELECT SUM(earned_premium_usd) AS earned FROM mart.earned_premium_monthly WHERE YEAR(accounting_month) = 2025
)
SELECT ROUND(incurred / earned, 4) AS loss_ratio_with_test_data FROM inc_all, ep_all;
