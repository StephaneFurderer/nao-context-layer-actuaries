-- What a capable analyst writes from the schema alone (no institutional knowledge)
WITH losses AS (
  SELECT SUM(t.amount_usd) AS losses_usd
  FROM mart.claim_transactions t
  JOIN mart.claims c USING (claim_id)
  WHERE YEAR(c.loss_date) = 2025
), premium AS (
  SELECT SUM(written_premium_usd) AS premium_usd
  FROM mart.policies
  WHERE YEAR(purchase_date) = 2025
)
SELECT ROUND(losses_usd / premium_usd, 4) AS loss_ratio
FROM losses, premium;
