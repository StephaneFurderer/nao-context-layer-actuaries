# Blind-agent experiment: does the context layer change the answers?

**This is a simulation, not a nao run.** Independent LLM analysts (Claude Sonnet sub-agents, 2026-11-14) each got a copy of the warehouse and one context level, and nothing else. They were told to stay inside their folder and could run any exploratory SQL. Their final SQL was graded by `evals/grade.py`, which imitates the `nao test` comparison: row order ignored, 2 decimals, row counts must match. Small n: treat these as illustrations, not statistics.

Context levels (all built with nao-core 0.4.2):

| Level | What the agent had |
|---|---|
| L0 | `nao sync` output only: columns, preview rows and profiling per table |
| L1 | L0 + hand-written `annotations.md` per table (codes, grain, pitfalls) |
| L2 | L1 + `semantics/*.md` (canonical metric definitions and company conventions) + `RULES.md` |

## Run 3: final dataset, 9 questions (`evals/run3/`)

| Test | L0 a | L0 b | L1 | L2 a | L2 b | What decides it |
|---|---|---|---|---|---|---|
| loss_ratio_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | inferable from the data |
| loss_ratio_by_region_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| net_incurred_by_coverage_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| earned_premium_2026_ytd | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| caribbean_cancellation_claims_by_month_2025 | ✅ | ✅ | ✅ | ✅ | ✅ | inferable (once the test said "return a date") |
| large_loss_count_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | **convention, but guessed**: every agent picked $10k, the obvious round number |
| attritional_loss_ratio_ay2025 | ❌ 39.3% | ❌ 39.3% | ❌ 39.3% | ✅ 41.6% | ✅ 41.6% | **convention**: we *cap* large claims at $10k; without context the agents *dropped* them |
| claim_frequency_by_region_2025 | ❌ 0.079 | ❌ 0.082 | ❌ 0.082 | ✅ 82.1 | ✅ 82.1 | **convention**: we report per 1,000 policies |
| ambiguous_loss_ratio (should ask) | ✅ asked | ❌ answered | ✅ asked | ✅ asked | ✅ asked | behaviour rule in `RULES.md` |
| **Total** | **7/9** | **6/9** | **7/9** | **9/9** | **9/9** | |

L0a's frequency answer (0.079) also differs from L0b's (0.082): it used a different denominator. Two runs at the same context level gave two different answers. That is the consistency problem `nao test -k` (pass^k) exists to catch.

## What we learned (in order of discovery)

1. **Run 1, self-describing data** (`evals/run1-self-describing/`). The first dataset named things too helpfully: `txn_type = 'recovery'`, and a partner literally called "QA test partner - do not use". The schema-only agent got the loss ratio right. Lesson: our synthetic data was unrealistically kind, so we recoded it the way legacy systems store it (numeric transaction codes, status codes, a neutral partner name).
2. **Run 2, coded data, 7 questions** (`evals/run2-coded/results.json`). L0 5/7, L1 6/7, L2 6/7. Frontier models still **inferred** the codes, from evidence in the data: reserves net to zero on closed claims, and round $9,999.99 claims on one partner. Their only consistent miss was a **convention** (frequency per 1,000). L2 failed one test because it returned the month as an integer where the reference returned a date: **that was a test defect, not a context defect**. We fixed the test prompt.
3. **Run 3, final** (table above). Adding two company conventions (attritional definition, large-loss threshold) produces a clean split. Rules that leave evidence in the data are mostly inferred. Rules that are *decisions* are not.

## The honest takeaway for the talk

- Do not claim "AI can't write actuarial SQL". On this data it mostly can.
- The context layer earns its keep on **conventions, consistency and knowing when to ask**. In this experiment that was the difference between 6–7/9 and 9/9.
- An agent that infers a rule from the data today can infer something different tomorrow. Writing the rule down makes the answer **repeatable**, and the test proves it.
- The `dropped vs capped` attritional miss is the most dangerous kind of error: 39.3% looks perfectly plausible.

## Reproduce

```bash
make data context            # regenerate the warehouse and sync the nao context
python evals/grade.py <answers_dir>...
```
Every agent's answers and notes are kept in `evals/run3/<run>/` (`notes.md` lists what each agent inferred).
