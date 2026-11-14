# Travel insurance actuarial agent: rules

## Business overview
Synthetic travel insurer. It sells trip cancellation, medical, baggage and delay cover through an airline, an online travel agency, a cruise line and a direct channel, and earns premium per trip. All amounts are in USD. **Data is valued as at 2026-09-30.**

## Data architecture
One DuckDB warehouse, gold/mart layer only (`mart.*`). Staging is excluded and blocked. Codes come from a legacy claims system: see each table's `annotations.md`.

## Context map
- **Metric definitions** live in `semantics/`. Read the file before computing the metric. Each metric has exactly one definition there; do not re-derive it.
  - Loss ratio, net incurred, earned premium -> `semantics/loss_ratio.md`
  - Claim counts and frequency -> `semantics/claim_frequency.md`
  - Large losses, cat losses, attritional loss ratio -> `semantics/large_and_cat_losses.md`
- **Table meaning, grain, codes, pitfalls** -> `databases/.../table=<name>/annotations.md`
- **Actual column values** -> `profiling.md` next to each table. Read it before filtering on any value.

## Most used tables
`mart.claims` (claims, accident date, cat code) · `mart.claim_transactions` (amounts by code) · `mart.earned_premium_monthly` (premium base) · `mart.policies` (segments, partner, status) · `mart.partners`

## Always
- Exclude partner `ZZTEST` (QA test data) from every metric.
- Recoveries (`txn_code '40'`) reduce losses. Never a plain `SUM(amount_usd)` across transaction codes.
- Premium for any ratio is **earned** premium, never written.
- Free-look cancellations (`policy_status 'CX'`) are not policies in force.

## Date filtering
"Today" for this data is the valuation date **2026-09-30**, not the calendar date.
- Year to date: `accounting_month >= DATE '2026-01-01'` (for losses: `loss_date >= DATE '2026-01-01'`)
- Last 12 months: `loss_date > DATE '2026-09-30' - INTERVAL 12 MONTH`
- A "year" for a loss metric is an accident year (`YEAR(loss_date)`) unless the user says otherwise.

## Analysis process
1. Identify the metric, the period, the year basis and the segment.
2. Open the metric's file in `semantics/`. If no definition exists, state the one you will use and ask the user to confirm it.
3. Check `annotations.md` and `profiling.md` for the tables and values involved.
4. Query, then sanity-check: totals reconcile and orders of magnitude are plausible.

## Clarify before analysing
If the metric, the period or the year basis (accident / report / underwriting) is missing and would change the answer, ask one short question. If the user gave a year but no basis, use the default in the metric file and say which one you used.

## Answer format
1. Answer first, with the basis (e.g. "AY 2025, valued 2026-09-30, excl. IBNR").
2. Supporting table or chart.
3. Show the SQL.
4. Caveats: immaturity, small volumes, anything you assumed.
