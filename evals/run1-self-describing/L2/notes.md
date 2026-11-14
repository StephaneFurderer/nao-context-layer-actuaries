1. loss_ratio_ay2025: AY = YEAR(loss_date)=2025; net incurred = payments + case reserve changes - recoveries; EP = earned_premium_monthly for 2025 accounting months; ZZTEST excluded both sides; no IBNR, valued 2026-09-30.
2. loss_ratio_by_region_ay2025: Same as Q1 split by policies.destination_region on both numerator and denominator.
3. net_incurred_by_coverage_ay2025: AY 2025 by claims.coverage, recoveries subtracted, ZZTEST excluded.
4. earned_premium_2026_ytd: SUM earned_premium_usd for accounting_month in 2026 (data through Sep 2026), ZZTEST excluded.
5. claim_frequency_by_region_2025: departure-year 2025; claims per 1,000 policies (distinct claims incl. denied / policies excl. free-look), ZZTEST excluded, rounded to 1 decimal.
6. caribbean_cancellation_claims_by_month_2025: coverage='trip_cancellation', policy region Caribbean, loss_date month in 2025, distinct claims, zero months included, ZZTEST excluded.
7. ambiguous_loss_ratio: Period/basis/segment missing, so I would clarify (default offered: AY, net incurred/earned).
