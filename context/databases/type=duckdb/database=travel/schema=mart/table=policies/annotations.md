---
type: manual
comment: These are manual notes you want the agent to keep in mind, safe to edit.
owner: reserving actuary (see CODEOWNERS)
---

# policies: one row per travel policy sold

- Grain: one row per `policy_id`, sold through a partner (`partner_code` -> `mart.partners`).
- `written_premium_usd` is the premium charged at sale. It is **not** the premium for loss ratios: use `mart.earned_premium_monthly` (see `semantics/loss_ratio.md`).
- `policy_status`: `IF` = in force (trip not yet returned), `EX` = expired (trip completed), `CX` = cancelled.
- Every `CX` has `cancel_reason_code = 'FL'`: cancelled in the 14-day free-look window and **fully refunded**. It has written premium but earns nothing and carries no claims. Exclude it from policy counts.
- `partner_code = 'ZZTEST'` is the QA test partner. It is not real business: exclude it from every metric.
- Coverage period: cancellation cover starts at `purchase_date`; trip covers run `departure_date` to `return_date`.
