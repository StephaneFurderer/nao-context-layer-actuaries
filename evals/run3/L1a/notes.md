semantics/ and docs/ folders were empty; loss ratio, attritional and large-loss definitions were not provided, so those were inferred by me.
- ambiguous_loss_ratio: clarify; period, basis (net incurred vs paid, cat/large treatment) and scope are undefined.
- attritional_loss_ratio_ay2025: inferred. AY by loss_date year; net incurred / earned premium (accounting year 2025); excludes cat (cat_event_code not null) and large (>=10k) claims from numerator; premium not adjusted. ZZTEST excluded.
- caribbean_cancellation_claims_by_month_2025: policy destination_region='Caribbean', coverage='trip_cancellation', loss_date month, all statuses (denied counted), ZZTEST excluded; documented.
- claim_frequency_by_region_2025: inferred. Claims (all statuses incl. denied) per policy, policies with 2025 departure_date, excluding CX free-look and ZZTEST; per-policy count, not exposure-adjusted.
- earned_premium_2026_ytd: sum earned_premium_monthly with accounting_month in 2026 (through 2026-09-30 valuation), ZZTEST excluded; documented.
- large_loss_count_ay2025: inferred threshold: net incurred >= 10,000 USD per claim (including cat claims; none exceed it); net incurred = 10+20-40 (documented).
- loss_ratio_ay2025: inferred. Net incurred (as at 2026-09-30) of claims with loss year 2025 / premium earned in calendar 2025 accounting months; all claims incl. cat; ZZTEST excluded.
- loss_ratio_by_region_ay2025: same as above, grouped by policy destination_region; premium and losses both by region.
- net_incurred_by_coverage_ay2025: documented net incurred formula, loss_date year 2025, ZZTEST excluded, includes cat and large.
