# Blind-agent experiment: what does the context layer change?

**This is a simulation, not a nao run.** Independent LLM analysts (Claude Sonnet sub-agents, 2026-11-14) each got a copy of the warehouse plus one context level, and nothing else. Each worked in an isolated folder and could run any exploratory SQL. Their final SQL is graded by `evals/grade.py`, which imitates the `nao test` comparison at **4 decimals** (row order ignored, row counts must match) and flags answers that are the same value in a different unit.

| Level | What the agent had (built with nao-core 0.4.2) |
|---|---|
| L0, tables only | `nao sync` output: columns, preview rows and profiling per table |
| L1, plus table notes | L0 + hand-written `annotations.md` per table: codes, grain, pitfalls |
| L2, plus our decisions | L1 + `semantics/*.md` (definitions and company conventions, prose only, no SQL) + `RULES.md` |

## Run 4: final (`evals/run4/`)

| Test | L0 a | L0 b | L1 a | L1 b | L2 a | L2 b | What decides it |
|---|---|---|---|---|---|---|---|
| loss_ratio_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | inferable from the data |
| loss_ratio_by_region_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| net_incurred_by_coverage_ay2025 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| earned_premium_2026_ytd | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| caribbean_cancellation_claims_by_month_2025 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | inferable |
| large_loss_count_ay2025 | ❌ 9 | ❌ 9 | ❌ 9 | ❌ 9 | ✅ 48 | ✅ 48 | **decision**: every agent guessed $10k; ours is $5k |
| attritional_loss_ratio_ay2025 | ❌ 39.1% | ❌ 39.1% | ❌ 39.1% | ❌ 39.1% | ✅ 38.2% | ✅ 38.2% | **decision**: they *dropped* large claims (at $10k); we *cap* at $5k |
| claim_frequency_by_region_2025 | ⚠️ 0.082 | ⚠️ 0.082 | ⚠️ 0.082 | ⚠️ 0.082 | ✅ 82.1 | ✅ 82.1 | **unit**: same value, per policy instead of per 1,000 |
| ambiguous_loss_ratio (should ask) | ✅ asked | ❌ answered | ✅ asked | ✅ asked | ✅ asked | ✅ asked | behaviour rule in `RULES.md` |
| **Passed** | **6/9** | **5/9** | **6/9** | **6/9** | **9/9** | **9/9** | |
| Passed if unit-only answers count as right | 7/9 | 6/9 | 7/9 | 7/9 | 9/9 | 9/9 | |

### Reading it honestly

- **The data-meaning rules were mostly inferred.** Even with tables only, agents worked out that code `40` is a recovery and that `ZZTEST` is test data, from evidence in the data (reserves net to zero; the partner list labels ZZTEST as `internal`). Note: several agents said the $9,999.99 test claims looked like a cap cluster, which may have nudged their $10k large-loss guess.
- **The table notes (L1) changed nothing on this test set.** They make inferred rules *explicit and repeatable*, but every L1 miss was a company **decision**.
- **The decisions were never inferred.** None of the four agents without `semantics/` found the $5k threshold or the cap-vs-drop convention. Their 39.1% looks entirely plausible.
- **The unit failure is debatable** (see TP-09). It could be a wrong answer or a vague question. We count it as a failure because the reported number would be wrong by 1,000×, and flag it separately.
- **Limits:** synthetic data designed by the presenter; one model family; n = 2 per level; 9 questions; the presenter's own grader. The profiling files the agents read came from the previous data version (value counts about 0.5% off). Agents queried the live data, so this does not change any result.

## History: how the experiment was hardened (each run kept in `evals/`)

1. **Run 1, self-describing data** (`run1-self-describing/`). The first dataset spelled things out (`txn_type = 'recovery'`, a partner named "QA test partner - do not use"). The schema-only agent simply read the answers. We recoded the data the way legacy systems store it.
2. **Run 2, coded data** (`run2-coded/`). The agents *inferred* the codes anyway. One L2 failure was a test defect (month as an integer vs a date); we fixed the test.
3. **Run 3** (`run3/`). This run added conventions: L0/L1 scored 6–7/9 and L2 scored 9/9. The review round then found three problems:
   - the metric files contained **SQL patterns close to the reference answers** (leakage);
   - the grader compared at **2 decimals**, which let a wrong attritional method pass;
   - the "$10k retention" was implausible for travel, and every agent guessed it anyway.

   Fixes: the definitions are now prose only, the grader compares at 4 decimals, and the threshold is a $5k *reporting* threshold. Hurricane loss dates now cluster just before departure. Everything was regenerated.
4. **Run 4** (above): the final run, on the final data and context.

## Reproduce

```bash
make data context                       # regenerate the warehouse and sync the nao context
python3 evals/grade.py evals/run4/L2a   # re-grade any run
make check-sql                          # assert every number quoted in the talk
```
Each agent's SQL and `notes.md` (what it inferred) are kept in `evals/run4/<run>/`.
