# When an answer is wrong: failure points, and what to validate

The deep-dive behind talk section TP-09 to TP-13. It builds on Stéphane's post *"When an agent gets an assumption wrong, who fixes it?"* (LinkedIn, November 13, 2026), which names three suspects: **the knowledge, the runtime, the checks**. Here that becomes five suspects. Every example below is measured in this repo. File paths are shown, and every number is asserted by `make check-sql`.

## The five suspects

| # | Suspect | What happened | Example in this repo | What it does to the answer | Who fixes it | nao features that help |
|---|---|---|---|---|---|---|
| 1 | **The knowledge was wrong** | The definition itself is wrong, outdated or ambiguous | `semantics/loss_ratio.md` edited to say "written premium" (`sql/failures/f1_…`) | AY 2025 loss ratio **47.8%** instead of **49.4%**, and it looks perfectly plausible | The definition's **owner** updates it and dates the change | Owners on context docs; filter tests by owner and tag; context recommendations; draft-vs-main test comparison |
| 2 | **The data was wrong** | Right definition, wrong rows: test data, the wrong table, a stale clock | ZZTEST left in (`f2_…`): **54.9%**. "Last 12 months" anchored on *today* instead of the valuation date (`f2b_…`): **41.1%** vs **42.8%**, silently dropping **17%** of the premium | Wrong, but SQL that runs | **Data owner** fixes it upstream; until then, the context states it | `include`/`exclude`, `allow_listed_only`, `exclude_columns`, profiling, a date-filtering rule anchored on the valuation date |
| 3 | **The knowledge was right, but the agent never saw it** | The file existed but was not loaded: not routed, not readable, truncated, or hidden by permissions | Blind agents at level L1 had table notes that *referred to* `semantics/large_and_cat_losses.md`, but the file wasn't in their folder. They guessed $10k and dropped large claims: **39.1%** vs **38.2%** (`evals/run4/L1a`) | A confident guess | **Whoever runs the system**: routing in `RULES.md`, file access, file size | RULES.md context map; table annotations attached when `columns.md` is read; `truncated_on_read` flag in recommendations; chat replay shows the files read |
| 4 | **The agent saw it, used it wrong, and nobody noticed** | Correct knowledge, wrong application: wrong unit, wrong join, answered when it should have asked | One agent answered "What's the loss ratio?" without asking (`evals/run4/L0b`). Every agent without definitions gave frequency per policy (0.082) instead of per 1,000 (82.1) | Right numbers, wrong problem | **Whoever designs the checks**: tests plus human review | `nao test` (SQL + clarification assertions), `-k` pass^k, multi-model runs, thumbs feedback, admin-certified stories |
| 5 | **The test was wrong** | The answer key was ambiguous or wrong, so a correct answer failed (or a wrong one passed) | Run 2: the best agent returned the month as an integer, the key as a date (`evals/run2-coded`). Run 3: 2-decimal comparison let a wrong attritional method pass | False alarm or false comfort | **Test owner** fixes the test, not the context | Output column naming (`*_float_0_1`, `*_date_yyyy_mm_dd`), `test.comparison.decimals`, test owners and tags |

Rule of thumb: **label the failure before you change anything.** Most bad fixes come from editing the context when the data, the routing or the test was at fault. Claire Gouze's own study found most of her reliability gain came from the data model, not the prompts (source B3).

## The audit trail: after a bad answer, can you answer three questions?

From the Thursday post: after a bad answer, you must be able to say:

1. **Which version of the knowledge was the official one?** The git commit of `context/` at the time of the answer: CODEOWNERS approval, PR history, and the `last_reviewed` date in each definition's front matter.
2. **What did the agent actually see?** nao chat replay shows the SQL and the files behind every answer. RULES.md is always loaded; everything else must appear in the trace.
3. **Which check ran?** The `nao test` results (`tests/outputs/results_*.json`, or test runs in admin mode), the CI run on the context PR, and any human sign-off.

If you can't answer one of these, you can't tell suspect 1 from suspect 3, and you will fix the wrong thing.

## Validation checklist: keeping the solution sane

### Before the first user (once)
- [ ] One bounded question, ≤ 20 clean tables, staging excluded, `allow_listed_only: true`
- [ ] Personal and health columns hidden with `exclude_columns` *before* `nao sync`: sample rows go to the LLM and into git
- [ ] Each table has `annotations.md`: grain, codes, pitfalls, test data
- [ ] Each metric has exactly **one** definition in `semantics/`, in prose, with an owner, a status and a review date. No SQL that copies the answer key
- [ ] Company conventions are written down: thresholds, caps vs drops, units, year basis, valuation date
- [ ] `RULES.md`: context map, always-rules, date filtering anchored on the valuation date, when to ask
- [ ] Answer key: one test per metric at minimum, plus a clarification test; output columns name their unit; `decimals: 4` for ratios
- [ ] Baseline `nao test -k 3` recorded (pass rate, cost, time)

### On every context change (CI, every PR)
- [ ] The owner of the changed file approves (CODEOWNERS)
- [ ] Reference SQL still runs, and the numbers quoted in reports still reproduce (`make check-sql`)
- [ ] `nao test` against the draft and against main, compared, before merge
- [ ] No duplicated definition: a metric defined in two places is the most common cause of inconsistent answers (nao docs, Rules)
- [ ] Each fixed failure becomes a new test

### Every week
- [ ] `nao test -k 3` on schedule. Watch pass^k (consistency), not just pass@1
- [ ] Review context recommendations: tool errors, downvotes, corrections, coverage gaps. Label each with its suspect (1–5) before acting
- [ ] Check read-cost flags (`truncated_on_read`, `frequent_and_expensive`): an unread file is suspect 3
- [ ] Re-sync after schema changes; check that annotations still match the columns

### Every answer someone will act on
- [ ] The basis is stated: accident / report / underwriting year, valuation date, incl./excl. IBNR, net/gross
- [ ] The SQL and the files used are visible (chat replay)
- [ ] It reconciles to a known total (ledger, earned premium control total, prior report)
- [ ] A named person signs it off. The agent prepares; the actuary decides (ASOP 56 framing)

### Every quarter
- [ ] Re-review every definition with its owner (`last_reviewed`)
- [ ] Retire tests for questions nobody asks; add tests for questions people do ask (from chat replay)
- [ ] Re-run with the current default model and a cheaper one. If context saturates accuracy, choose on cost

## Sources

- Stéphane Furderer, *When an agent gets an assumption wrong, who fixes it?* (LinkedIn, 2026-11-13): the three suspects and the audit-trail questions. https://lnkd.in/p/gBQVA9sg
- Stéphane Furderer, comment *"Every definition needs a keeper"* (lighthouse rule), TLDR pipeline 2026-11-05.
- Ilho Ye, Wei Li, Jianlong Zhong, *Inside LinkedIn's data context layer* (2026-10-09): working SQL can still select the wrong dataset; curated context survives automated refreshes.
- Bonnie Xu, Aravind Suresh, Emma Tang, *Inside OpenAI's in-house data agent* (2026-01-29): table knowledge, business context, saved corrections, tests against reference queries.
- Harrison Chase, *Introducing LangSmith Context Hub*; Anthropic, *Effective context engineering for AI agents*; Birgitta Böckeler, *Harness engineering for coding agent users*: one each for suspects 1, 3 and 4.
- Claire Gouze, *Launching nao context recommendations* (2026-06-22), and the nao docs on Recommendations, Evaluation and Rules (source bank A4, A7, A8).
- Trang NT, analytics model comparison: "correct" is not the same as "ready to send".
