-- F2 (bis) · Stale clock: "loss ratio, last 12 months" anchored on TODAY (2026-11-14) instead of the valuation date (2026-09-30).
-- The last 6 weeks have no data yet, so the window silently loses premium and claims.
WITH w AS (SELECT DATE '2026-11-14' - INTERVAL 12 MONTH AS start_today, DATE '2026-09-30' - INTERVAL 12 MONTH AS start_val),
inc AS (
  SELECT
    SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) FILTER (WHERE c.loss_date > (SELECT start_today FROM w)) AS inc_today,
    SUM(CASE t.txn_code WHEN '40' THEN -t.amount_usd ELSE t.amount_usd END) FILTER (WHERE c.loss_date > (SELECT start_val FROM w))   AS inc_val
  FROM mart.claim_transactions t JOIN mart.claims c USING (claim_id) JOIN mart.policies p USING (policy_id)
  WHERE p.partner_code <> 'ZZTEST'
), ep AS (
  SELECT
    SUM(earned_premium_usd) FILTER (WHERE accounting_month > (SELECT start_today FROM w)) AS ep_today,
    SUM(earned_premium_usd) FILTER (WHERE accounting_month > (SELECT start_val FROM w))   AS ep_val
  FROM mart.earned_premium_monthly e JOIN mart.policies p USING (policy_id) WHERE p.partner_code <> 'ZZTEST'
)
SELECT ROUND(inc_today / ep_today, 4) AS lr_12m_anchored_today, ROUND(inc_val / ep_val, 4) AS lr_12m_anchored_valuation,
       ROUND(ep_today / ep_val, 4) AS share_of_premium_kept
FROM inc, ep;
