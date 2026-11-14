---
owner: reserving actuary (see /CODEOWNERS)
status: approved
last_reviewed: 2026-11-14
---
# Large losses, catastrophe losses, attritional loss ratio

These are company conventions, decided by the reserving committee. Other companies make different, equally defensible choices, so do not substitute a textbook definition.

- **Large loss:** a single claim whose incurred loss (see `loss_ratio.md`) is **$5,000 or more**. This is our large-loss *reporting threshold*. It is not a reinsurance retention.
- **Catastrophe (cat) loss:** any claim with a non-null `claims.cat_event_code`. `HU25` is the 2025 Caribbean hurricane season, as declared by the claims committee.
- **Attritional loss ratio:** the loss ratio after two adjustments.
  1. Remove every cat-coded claim entirely.
  2. **Cap** every remaining claim at $5,000. The excess above $5,000 is removed; the claim itself stays in.

  The denominator does not change: earned premium for the same year, ZZTEST excluded.
- When you report an attritional loss ratio, show the all-in loss ratio beside it and say what drives the gap.
