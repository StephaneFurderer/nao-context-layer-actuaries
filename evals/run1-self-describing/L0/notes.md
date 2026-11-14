1. Loss ratio AY2025 = net incurred (payments + case_reserve_change - recoveries) on claims with loss_date in 2025 / earned premium with accounting_month in 2025; excludes test partner ZZTEST; denied claims included (net zero).
2. Same as 1, grouped by policies.destination_region; regions with no claims get 0.
3. Net incurred = payments + case reserve changes (open reserve) - recoveries, by claims.coverage, loss_date year 2025, ZZTEST excluded.
4. Sum earned_premium_usd for accounting_month in 2026 (data through Sep 2026), ZZTEST excluded.
5. Frequency = claim count (all statuses incl. denied) / policy count for policies departing in 2025, by destination_region; excluded ZZTEST and cancelled_free_look (no exposure/earned premium).
6. Claims count with coverage=trip_cancellation, destination Caribbean, by month of loss_date in 2025, ZZTEST excluded; months with zero claims absent.
7. Ambiguous (basis, period, grouping unspecified) so clarify.
Note: context docs had no definitions; ZZTEST exclusion and recovery sign/net-incurred formula were inferred from the data (partner name "QA test partner - do not use").
