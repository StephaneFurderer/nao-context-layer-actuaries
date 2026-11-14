semantics/ and docs/ folders were empty; definitions below are from annotations.md plus inference.
Global: exclude partner ZZTEST (stated); exclude CX/free-look policies from claim/policy counts (stated; they have no claims or premium anyway).
Net incurred = txn 10 + txn 20 - txn 40 per claim (stated in annotations); AY = year(loss_date) (stated).
loss_ratio_ay2025: net incurred of AY2025 claims / earned premium with accounting_month in calendar 2025 (inferred: AY numerator over calendar-year earned denominator); includes cat and large losses.
attritional_loss_ratio_ay2025: as above excluding cat claims (cat_event_code not null) and large losses; large threshold = net incurred >= 10,000 per claim (inferred; undefined in context).
large_loss_count_ay2025: AY2025 claims with net incurred >= 10,000 (inferred threshold).
net_incurred_by_coverage_ay2025: AY2025 net incurred by claims.coverage, incl. cat and large (inferred).
loss_ratio_by_region_ay2025: same as loss_ratio_ay2025 grouped by policies.destination_region (inferred).
earned_premium_2026_ytd: sum earned_premium_usd for accounting_month in 2026 (through valuation 2026-09-30), non-test (stated/inferred).
claim_frequency_by_region_2025: claims (all statuses, incl. denied - stated) per non-CX, non-test policy departing in 2025, by destination_region; per policy, not exposure-adjusted (inferred).
caribbean_cancellation_claims_by_month_2025: claims with coverage=trip_cancellation, policy destination Caribbean, loss_date in 2025, grouped by loss month; all statuses incl. denied; all 12 months shown (inferred).
ambiguous_loss_ratio: CLARIFY (basis/period/cat treatment undefined).
