-- How each piece of institutional knowledge moves the AY2025 loss ratio
WITH tx AS (
  SELECT t.*, c.loss_date, p.partner_code
  FROM mart.claim_transactions t
  JOIN mart.claims c USING (claim_id)
  JOIN mart.policies p USING (policy_id)
  WHERE YEAR(c.loss_date) = 2025
),
wp  AS (SELECT SUM(written_premium_usd) v FROM mart.policies WHERE YEAR(purchase_date) = 2025),
ep  AS (SELECT SUM(earned_premium_usd) v FROM mart.earned_premium_monthly WHERE YEAR(accounting_month) = 2025),
ep_x AS (SELECT SUM(e.earned_premium_usd) v FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id)
         WHERE YEAR(e.accounting_month) = 2025 AND p.partner_code <> 'ZZTEST'),
l_raw AS (SELECT SUM(amount_usd) v FROM tx),
l_rec AS (SELECT SUM(CASE txn_code WHEN '40' THEN -amount_usd ELSE amount_usd END) v FROM tx),
l_x   AS (SELECT SUM(CASE txn_code WHEN '40' THEN -amount_usd ELSE amount_usd END) v FROM tx WHERE partner_code <> 'ZZTEST')
SELECT * FROM (VALUES
  (0, 'Naive: all transactions / written premium',    (SELECT v FROM l_raw) / (SELECT v FROM wp)),
  (1, '+ earned premium, not written',                (SELECT v FROM l_raw) / (SELECT v FROM ep)),
  (2, '+ recoveries subtracted',                      (SELECT v FROM l_rec) / (SELECT v FROM ep)),
  (3, '+ ZZTEST test partner excluded = reference',   (SELECT v FROM l_x)   / (SELECT v FROM ep_x))
) AS w(step, rule, loss_ratio) ORDER BY step;
