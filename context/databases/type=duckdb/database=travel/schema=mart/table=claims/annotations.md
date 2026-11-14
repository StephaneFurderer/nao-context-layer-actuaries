---
type: manual
comment: These are manual notes you want the agent to keep in mind, safe to edit.
owner: reserving actuary (see CODEOWNERS)
---

# claims: one row per reported claim

- Grain: one row per `claim_id`. Join to policies on `policy_id`.
- `loss_date` is the date of the insured event and defines the **accident year**. `report_date` is when the claim was reported to us.
- `claim_status`: `open`, `closed_paid`, `closed_denied`. Denied claims are still reported claims (they count in claim counts) but have no payments.
- Claims on partner `ZZTEST` are QA test claims (round $9,999.99 payments). Exclude them.
- `cat_event_code`: set when the claims committee ties the claim to a declared catastrophe. `HU25` = 2025 Caribbean hurricane season. NULL = not a cat claim. See `semantics/large_and_cat_losses.md`.
- Amounts are not on this table: they live in `mart.claim_transactions`.
