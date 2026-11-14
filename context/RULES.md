# Travel insurance actuarial agent - rules

## Business overview
Synthetic travel insurer selling trip cancellation, medical, baggage and delay cover through airline, OTA, cruise and direct partners. Data valued as at **2026-09-30**. All amounts in USD.

## Context map
- Metric definitions live in `semantics/`. **Read the file before computing the metric.** Each metric has exactly one definition; do not re-derive it.
  - Loss ratio, incurred, earned premium -> `semantics/loss_ratio.md`
  - Claim counts and frequency -> `semantics/claim_frequency.md`
  - Large losses, cat losses, attritional loss ratio -> `semantics/large_and_cat_losses.md`
- Per-table meaning, grain and pitfalls: `databases/.../table=<name>/annotations.md`. Read before filtering on a column.
- Value distributions: `profiling.md` next to each table.

## Always
- Exclude partner `ZZTEST` (QA test data) from every metric.
- Recoveries (`txn_code '40'`) reduce losses. Never a plain `SUM(amount_usd)` across transaction codes.
- Premium for any ratio is **earned** premium, never written.
- Free-look cancellations (`policy_status 'CX'`) are not policies in force.

## Clarify before analysing
Ask one short question when the metric, the period or the year basis (accident / report / underwriting) is missing and changes the answer. If the user gave a year but not a basis, use the default in the metric file and say which basis you used.

## Answer format
1. Answer first, with the basis (e.g. "AY 2025, valued 2026-09-30, excl. IBNR").
2. Supporting table or chart.
3. Show the SQL.
4. Caveats: immaturity, small volumes, anything you assumed.
