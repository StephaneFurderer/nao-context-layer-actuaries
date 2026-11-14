---
owner: pricing actuary (see CODEOWNERS)
status: approved
last_reviewed: 2026-11-14
---
# Claim frequency (canonical definition)

**Claim frequency = reported claims per 1,000 policies**, on a **departure-year** basis.

- Numerator: count of distinct `claim_id` on policies departing in the year. Denied claims count (they were reported). Exclude `ZZTEST`.
- Denominator: count of policies with `departure_date` in the year, excluding free-look cancellations (`policy_status = 'CX'`) and `ZZTEST`.
- Express per 1,000 policies, rounded to 1 decimal.
- Only use departure years whose trips have all returned by the valuation date (2026-09-30) unless the user asks otherwise; flag immaturity.
