# Audit of `/tmp/naoskills/mine` against nao's published skills

Date: 2026-11-14. nao-core 0.4.2, duckdb 1.5.6.

How this audit was done:
- Installed the skills with `nao skills add getnao/nao` from `/tmp/naoskills`. They landed in `/tmp/naoskills/.agents/skills/<name>/SKILL.md`, with symlinks in `/tmp/naoskills/.claude/skills/`. The docs say they land in `.claude/skills/`, so that is out of date: the real files live in `.agents/skills/` and `.claude/skills/` only holds symlinks.
- Read all 9 SKILL.md files and the three templates (`write-context-rules/templates/RULES.md`, `create-context-tests/templates/test.yaml`, `add-semantic-layer/templates/semantic.yaml`).
- Fetched `docs/.../context-engineering/skills.md`, `docs/.../context-builder/rules-context.md` and, to check the step order, `docs/.../context-engineering/playbook.md` (copies are in `/tmp/naoskills/docs_fetch/`).
- Ran `nao debug` and `nao sync` in `/tmp/naoskills/check`, a copy of `mine`. `mine` was not modified.
- Ran each test's expected SQL against `travel.duckdb`, and read the nao-core source for the test loader, the result comparator and the annotations handling.

---

## (a) The nao skills

| Skill (exact name) | What it does, in one line |
|---|---|
| `setup-context` | First-time setup only. Asks one batch of questions (warehouse, scope of 100 tables or fewer with about 20 as the target, repos, LLM), writes `nao_config.yaml` from the warehouse docs, runs `nao init --no-tty` and `nao sync`, hands off to `write-context-rules`, wires the LLM key through `${{ env(...) }}`, then runs `nao debug`. |
| `write-context-rules` | The only skill that writes `RULES.md`. Takes an inventory first, then works section by section from the template (Business overview, Data architecture, Context map, Core data models, Key Metrics Reference, Date filtering, Analysis Process, and an optional Chart section). It points to existing context instead of copying it, and has an audit-and-fill flow for a `RULES.md` that already has content. |
| `create-context-tests` | Builds the NL-to-SQL benchmark: one flat YAML per test under `tests/`, at least one test per key metric. Prompts should read like real chat (Rule 1) and output column names should encode format or unit (Rule 2). Then runs `nao test -m <model> -t 10` and records the baseline. |
| `audit-context` | Diagnosis only. Runs six checks in order (synced context and scope, RULES.md structure, per-table coverage, MECE, test failures by category, token bloat) and ends with a ranked plan that names the skill for each fix. |
| `add-semantic-layer` | Adds a semantic layer only after `nao test` shows metric-reliability failures. The options are dbt MetricFlow MCP, Snowflake views or semantic views MCP, other tools through MCP, or Path D: a single `semantics/semantic.yaml` with `dimensions:` and `metrics:`. Routes RULES.md to it, then re-tests against the baseline. |
| `deploy-context` | A GitHub Actions workflow that runs `nao deploy` on every push to `main`. Covers the org API key in GitHub Secrets, `.naoignore` hardening, the rule that config holds no literal secrets, and the fact that every deploy fully replaces the remote project. |
| `build-custom-charts` | Writes browser-rendered chart modules at `agent/charts/<type>.js` that export `render(element, context)`, for chart types nao does not ship. |
| `migrate-metabase` | Moves Metabase questions, dashboards and collections into nao charts or stories. The nao CLI does the export and the nao MCP does the delivery. |
| `migrate-tableau-workbook` | Moves Tableau workbooks, dashboards and worksheets into nao charts or stories through the nao CLI (`nao migrate tableau ...`) and the nao MCP. |

The context-AUDIT skill is **`audit-context`**. The other skills that apply to this project are `setup-context`, `write-context-rules`, `create-context-tests` and `add-semantic-layer`. `deploy-context` applies only to the deploy-readiness findings.

### The skills and docs disagree with each other in places

Where they conflict, I treated the SKILL.md files as authoritative, because they are what nao ships.

1. **Number of RULES.md sections.** `write-context-rules` and its template have 8 sections, including `## Context map` and an optional Chart section. `audit-context` check 2 still says "six standard sections" and leaves out Context map. The `skills.md` docs page describes the older 6-section, 5-step Analysis Process. `rules-context.md` matches the 8-section version. I scored `mine` against the 8-section version and also report the 6-section score that `audit-context` asks for.
2. **The Tables detail block.** `audit-context` check 3 asks of each table "Does it have a `## Tables detail` block?". `write-context-rules` says to write Tables detail only when no richer table docs exist. I followed `write-context-rules`: `mine` has per-table `annotations.md`, so leaving out Tables detail is correct.
3. **`annotations.md` is not mentioned in any skill.** nao-core 0.4.2 does support it natively: `commands/sync/markers.py::ensure_annotations_file` creates `annotations.md` with `type: manual` frontmatter and never overwrites it. I confirmed that `nao sync` in `check/` left all five annotations untouched. The skills' inventory tables (Step 0 of `write-context-rules`, and the Context map template) do not list it.
4. **Semantic files.** `add-semantic-layer` Path D says "One file: `semantics/semantic.yaml` ... do not split into per-metric files". `rules-context.md` recommends modular "sub rules" `.md` files such as `agent/semantics/finance.md`, and playbook Step 4 puts per-domain metric definitions before testing.
5. **Folders created by `nao init`.** `setup-context` says it creates `queries/`. nao-core 0.4.2 does not; it creates `agent/prompts/` instead. `mine` matches the real 0.4.2 layout.
6. **Test file extension.** The test template is named `tests/<test_name>.yaml`. `nao init` itself creates `tests/test_example.yml`, and the loader globs both `*.yml` and `*.yaml`. So `.yml` is fine.

---

## (b) Where `mine` deviates from nao's recommended practice

### `audit-context` summary paragraph, in the format the skill asks for

**Sync state:** clean. `nao debug` connects to the DuckDB file, and `nao sync` in the copy synced 5 tables in 0.7 s. The only diff against `mine` was the `Computed at` timestamps in `profiling.md`. `nao debug` also printed "No LLM configured" and "Connected successfully (0 tables found)"; the second looks like a quirk of the debug probe, since sync found all 5 tables.
**Scope:** 5 tables, against a ceiling of 100 and a target of 20 or fewer. It is mart-only, and `staging.raw_policy_feed` is correctly kept out of scope.
**Rules quality:** against `audit-context`'s six sections, 1 is substantive (Key Metrics, routed through the Context map), 1 is thin (Business overview) and 4 are missing (Data architecture, Core data models, Date filtering, Analysis Process). Against `write-context-rules`' eight, Context map is also present and Chart is correctly left out.
**Test coverage:** 9 tests, 8 with SQL and 1 that asserts a clarification. All 8 SQLs run against the warehouse, but **the tests have never been run with `nao test`**: there is no `tests/outputs/` and no `llm:` block, so the pass rate is unknown.

### Findings, ranked by severity

| # | Severity | Check | Deviation | Concrete fix (skill that owns it) |
|---|---|---|---|---|
| 1 | **High** | 1, 5 | **No `llm:` block in `nao_config.yaml`.** `nao debug` prints "No LLM configured", so `nao chat` and `nao test` cannot run. That breaks `setup-context` Step 5 and blocks every test-driven step after it. | Add `llm: providers: [{provider: anthropic, api_key: "${{ env('ANTHROPIC_API_KEY') }}"}]` and export the key in the shell. Never use a literal key. Re-run `nao debug`. (`setup-context`) |
| 2 | **High** | 5 | **No baseline.** There is no `tests/outputs/`, so failures cannot be put into categories and no RULES.md change can be measured. nao's guardrail is "Tests are the source of truth." | Run `nao chat &` then `nao test -m <model_id> -t 10`, and record the pass rate, token cost and wall-clock time as the baseline. (`create-context-tests`) |
| 3 | **High** | 2 | **RULES.md has no `## Analysis Process`.** The "Clarify before analysing" and "Answer format" sections cover parts of steps 1 and 8. Missing are: resolve the metric definition before choosing a table, the table-routing map, the **unconditional "read `profiling.md` before filtering on any column value"** rule, query style, and validation. | Add the template's 8-step Analysis Process. In step 2, route to `semantics/`. In step 4, map questions to tables: losses go to `claim_transactions`+`claims`+`policies`, premium to `earned_premium_monthly`+`policies`, counts and frequency to `claims`+`policies`, partner and channel to `partners`. In step 5, add the profiling rule verbatim. (`write-context-rules`) |
| 4 | **High** | 2, 4 | **No `## Date filtering`, and the data is valued at 2026-09-30 while `CURRENT_DATE` is 2026-11-14.** A question like "last 30 days" or "this month" anchored on `CURRENT_DATE` would land on a window with no data. The template asks for a week convention and three example formulas. | Add the convention (for example "Week starts Monday; 'last X' is anchored on the valuation date `DATE '2026-09-30'`, not `CURRENT_DATE`; the current incomplete period is excluded") and the three formulas: last X weeks, last X days, current month. Confirm the convention with the user (Step 9). (`write-context-rules`) |
| 5 | Medium | 2 | **No `## Core data models` / `### Most Used Tables`.** The template says to always include it. `partners` and `claim_transactions` are never named in RULES.md as table pointers. | Add one line per table, for example `` `mart.claims` — one row per reported claim; loss_date = accident date. See `databases/type=duckdb/database=travel/schema=mart/table=claims/`. `` Leave out `### Tables detail`, because the annotations already cover it. (`write-context-rules`) |
| 6 | Medium | 2 | **No `## Data architecture`.** | Add the warehouse (DuckDB file `travel.duckdb`, connection `travel_warehouse`), the layers (`mart` is in scope; `staging` holds raw feeds and is excluded), the sources (policy admin, claims system with legacy txn codes, earned premium engine), and the valuation date. (`write-context-rules`) |
| 7 | Medium | 2 | **The Context map sends column-value checks to `annotations.md` instead of `profiling.md`.** RULES.md says annotations are "Read before filtering on a column", but nao's rule is to read `profiling.md` and use the exact `top_values`. The Context map also does not list `columns.md` and `preview.md`. | List all four per-table files and what each is for: `columns.md` for the schema, `preview.md` for sample rows, `profiling.md` for `top_values` (**read before any filter**), and `annotations.md` for meaning, grain and pitfalls (read before choosing the table). (`write-context-rules`) |
| 8 | Medium | 5 | **Most test output columns break Rule 2.** They should encode format or unit. This matters in nao-core 0.4.2: `compare.py` / `runner.py` fails a test with "missing columns" unless the agent's result contains the expected column names, then rounds floats to 2 dp and requires exact equality on non-numeric columns. A name like `loss_month` gives the agent no hint to return a DATE rather than a TIMESTAMP, and `loss_ratio` gives no hint between 0-1 and 0-100. | Rename the columns: `loss_ratio` to `loss_ratio_float_0_1` (in 2 tests); `attritional_loss_ratio` to `attritional_loss_ratio_float_0_1`; `large_losses` to `large_loss_count`; `claims` to `claim_count`; `loss_month` to `loss_month_date_yyyy_mm_dd`, with `::DATE` added in the SQL (it currently returns a TIMESTAMP); `claims_per_1000` to `claims_per_1000_policies_float`; `net_incurred_usd` to `net_incurred_usd_dollars`; `earned_premium_usd` to `earned_premium_usd_dollars`. (`create-context-tests`) |
| 9 | Medium | 5 | **Prompt in `caribbean_cancellation_claims_by_month_2025.yml` breaks Rule 1.** It contains "Return the month as a date (first day of the month)", an instruction about output format that no real user would type. Rule 2 says the column name should carry that information instead. | Change the prompt to "How many Caribbean cancellation claims did we get each month in 2025?" and let `loss_month_date_yyyy_mm_dd` carry the format. (`create-context-tests`) |
| 10 | Medium | 5 | **Test coverage is below the floor.** nao asks for at least one test per key metric, and the playbook targets 20 questions. The defined metrics with no test are **cat losses (HU25)**, plain **claim count**, and the denied-claims-count rule. There are no time-window tests ("last 3 months", "Q3"), no edge or NULL tests, no basis-switch tests ("report-year 2025 loss ratio"), and no partner or channel tests. | Add about 11 tests to reach 20, including `cat_loss_incurred_2025`, `claim_count_2025`, `loss_ratio_q3_2026` (should flag immaturity), `loss_ratio_by_channel_ay2025`, `report_year_loss_ratio_2025`, `free_look_cancellations_2025`, and `ambiguous_frequency` (clarification assertion). (`create-context-tests`) |
| 11 | Medium | 4 | **Collectively exhaustive gap: report-year and underwriting-year bases** are mentioned in RULES.md and `loss_ratio.md` as alternatives but are **not defined anywhere**. Neither file says whether UY means `YEAR(purchase_date)`, or whether RY means `YEAR(report_date)` with RY earned premium. The agent will improvise. | Define both bases in `semantics/loss_ratio.md`, or state that they are not supported and tell the agent to say so. Validate with the user (`write-context-rules` Step 8). |
| 12 | Medium | 4 | **Mutually exclusive risk: "claim count" has two implicit bases.** `claim_frequency.md` counts claims by policy **departure year**. The Caribbean test counts by **loss date**. No file says which basis to use for "how many claims in 2025". | Add a one-line default for plain claim counts (for example "by loss_date, i.e. accident year, unless frequency is asked") to `claim_frequency.md`. (`write-context-rules`) |
| 13 | Medium | 3 | **Columns with no description anywhere.** Every `columns.md` says "_No description available._" because the DuckDB tables have no `COMMENT`s. Undocumented: `policies.product` (Basic/Plus/Premier), `traveler_age_band`, `trip_cost_usd`, `cancel_date`, `claims.report_date` (only one line), `claim_transactions.txn_date`, `txn_id`, `partners.partner_name`, `channel`. | Add `COMMENT ON TABLE` / `COMMENT ON COLUMN` in the warehouse so `columns.md` fills in on sync, which is the better option. Otherwise add one line per column to the relevant `annotations.md`. (Fix belongs to the data owner; check with `audit-context` after.) |
| 14 | Medium | 1 / deploy | **`path: ../travel.duckdb` points outside the project folder.** The remote unpacks only the project folder, so a `nao deploy` will not carry the warehouse with it. | For deployment, use MotherDuck (`path: md:...`) or another reachable warehouse, with credentials through `${{ env() }}`. For local demos it works as is. (`deploy-context`) |
| 15 | Low | 6 / MECE | **Net incurred is defined in three places**: the `semantics/loss_ratio.md` table, the `claim_transactions/annotations.md` formula line, and RULES.md "Always" ("never a plain SUM"). The ZZTEST exclusion is repeated in RULES.md, 3 annotations and 3 semantics files. `write-context-rules` treats this duplication as a finding because it goes stale. | Keep the formula in `semantics/loss_ratio.md` only. Have the annotation say "see `semantics/loss_ratio.md`". Keep the short "Always" guardrails in RULES.md, which are broad rules and not formulas. (`write-context-rules`) |
| 16 | Low | 2 | **Business overview is thin.** It has one paragraph, not the template's **Product** and **Business model** paragraphs. Revenue, distribution economics and the claims journey are missing. | Split it into a Product paragraph (cover types, partners) and a Business model paragraph (premium earned pro rata, partner channels, claims cycle, recoveries from airlines). (`write-context-rules` Step 1) |
| 17 | Low | semantic layer | **The semantic layer is three `.md` files, not `semantics/semantic.yaml`, and it was added before any test run.** The guardrails of `add-semantic-layer` say "Only after tests show metric failures" and require a single YAML file with `dimensions:` and `metrics:`. | Keep the `.md` files: the playbook calls these "sub-rules" and they are well written. Once the baseline exists, decide based on the failures whether to also emit a Path D `semantics/semantic.yaml`. If you do, make the YAML the single canonical source and turn the `.md` files into notes that point to it, so there are never two competing definitions. Don't convert before the baseline. (`add-semantic-layer`) |
| 18 | Low | 1 | **Config hygiene.** `ai_summary:` refresh settings are configured but `ai_summary` is not in `templates` (dead config). `exclude: [staging.*]` is redundant with `include: [mart.*]` (harmless). `profiling.refresh_policy: always` rewrites `profiling.md` on every sync, which makes noisy git or PR diffs (seen in `check/`). | Remove the `ai_summary:` block or add `ai_summary` to the templates. Use `refresh_policy: interval` with `interval_days: 7` for profiling. (`setup-context`) |
| 19 | Low | 5 | **The tests have no optional metadata** (`category`, `difficulty`, `notes`, `owner`, `tags`). These drive filtering in the Tests drawer. | Add `category: loss_ratio \| frequency \| premium \| large_loss`, a `difficulty` level, and a `notes:` line that names the trap each test catches. (`create-context-tests`) |
| 20 | Low | — | **Ownership references a `CODEOWNERS` file that does not exist.** Several frontmatters say "owner: ... (see CODEOWNERS)". | Add `.github/CODEOWNERS` that maps `semantics/` and `databases/**/annotations.md` to the owners, or remove the reference. |

### Not deviations, but worth knowing

- `.naoignore` contains `tests/`. That is the default `nao init` writes in 0.4.2 (`commands/init.py`), so it is expected. It does mean the tests are not included in the `nao deploy` tarball.
- Test files ending in `.yml` are accepted, as noted in conflict 6 above.
- `templates: [columns, preview, profiling]` goes beyond `setup-context`'s default of `[columns, preview]`. That is an allowed opt-in, and `write-context-rules` depends on `profiling` for the filter rule.
- `allow_listed_only: true` is a valid 0.4.2 field ("SQL may only query tables present in synced context"). No skill mentions it.
- All 8 expected SQLs run. Their results: AY2025 LR 0.4993, attritional LR 0.4156, 10 large losses, EP 2026 YTD $3,304,647, Caribbean frequency 139.3 per 1,000 versus about 60–82 elsewhere.
- **The tests catch the planted traps even after nao's 2-dp rounding.** Including ZZTEST gives a loss ratio of 0.555, a plain `SUM` gives 0.554, and written premium gives 0.483, all against 0.499. Keeping CX policies in the frequency denominator gives 81.8 against 84.8. So the benchmark can tell a correct answer from a common wrong one.
- No file is larger than 4 KB, so check 6 (token bloat) is clean.

### Plan, in `audit-context` format

```
## Plan
1. (easy / 5 min)      Add llm: block with env-var key; nao debug                 → setup-context
2. (easy / 10 min)     Rename test output columns (Rule 2), fix caribbean prompt  → create-context-tests
3. (small / 30 min)    Add Data architecture, Most Used Tables, Context map file
                       list, Analysis Process (profiling rule), Date filtering
                       anchored on 2026-09-30                                     → write-context-rules
4. (small / 30 min)    Run nao test; record baseline; categorize failures        → create-context-tests
5. (medium / 1-2 hr)   Define RY/UY bases + plain claim-count basis; dedupe net
                       incurred; add ~11 tests to reach 20                        → write-context-rules / create-context-tests
6. (medium)            Column COMMENTs in warehouse; config hygiene; CODEOWNERS   → (data owner) then audit-context rerun
7. (large, only if baseline shows metric failures) semantics/semantic.yaml        → add-semantic-layer
8. (when shipping)     Reachable warehouse path + deploy workflow                 → deploy-context
```

---

## (c) Where `mine` goes beyond the skills' guidance

1. **Per-table `annotations.md` files** carry grain, enum meanings (`IF/EX/CX`, `txn_code 10/20/40`), sign conventions and traps. This uses a native nao-core 0.4.2 feature that no skill mentions, and the files survive `nao sync`, which I verified. It is a cleaner home for per-table pitfalls than the `### Tables detail` block the skills suggest.
2. **Metric files carry ownership frontmatter** (`owner`, `status: approved`, `last_reviewed`). This adds governance and review dates. Only `create-context-tests` has an `owner:` field.
3. **The metric files explain where each definition comes from.** `large_and_cat_losses.md` says "These are decisions, not facts you can derive from the data", ties the $10k threshold to the reinsurance retention, and ties `HU25` to a claims-committee declaration. It gives SQL patterns, and spells out that attritional caps a claim at $10k rather than dropping it. That is the kind of "why" the skills ask for but never show.
4. **A clarification assertion test** (`ambiguous_loss_ratio.yml` with `assertions: - type: tool_call, tool: clarification`). The template only mentions assertions in a comment; `mine` actually uses one, and pairs it with a RULES.md rule on when to ask and when to fall back to the default basis.
5. **Domain-specific broad rules** in RULES.md: the year basis (accident, report or underwriting), and an answer format that states the basis, the valuation date and "excl. IBNR". The skills' generic template does not cover these, and they fit actuarial users well.
6. **Data traps are documented and the tests catch them**: a QA test partner with $9,999.99 claims sitting just under the large-loss threshold, recoveries stored as positive amounts, and free-look cancellations. Each one moves a test result past nao's 2-dp tolerance, so the benchmark can tell a correct answer from a common wrong one.
7. **Data maturity is spelled out**: valued as at 2026-09-30, no IBNR, AY2026 immature, and frequency restricted to departure years whose trips have all returned.
8. **Scope discipline**: 5 mart tables, `allow_listed_only: true` so SQL cannot reach `staging`, and `profiling` enabled. This sits well inside the 20-table target.

---

## (d) Step order

The order under review: **scope → sync → annotate tables → define metrics in semantics/ → RULES.md router → tests → run/diagnose → recommendations/PR**

**Verdict: it is close to nao's order, but not the same.** There are three differences.

1. **nao writes RULES.md straight after sync, before metrics.** `setup-context` Step 4 says "Hand off directly to `write-context-rules`. Don't ask." The order there is init/config, then sync, then RULES.md, then LLM key and `nao debug`, then a smoke test with `nao chat`, then tests. In the order under review, RULES.md comes after the metrics and is treated as the final router. `write-context-rules` then has its own audit-and-fill flow to keep RULES.md up to date as context is added.
2. **nao says a formal semantic layer comes after tests, not before.** `add-semantic-layer` and the skills doc both say "only after `nao test` shows metric-reliability failures". The playbook does put "sub-rules" with metric definitions at Step 4, before tests at Steps 5–6. So **markdown metric definitions before tests is consistent with the playbook, but a `semantics/` semantic layer before tests goes against the skill.**
3. **Rollout, CI and deploy sit between run/diagnose and recommendations.** In the playbook, Recommendations is Step 9: it runs after rollout to users (Step 7) and after version control with `nao test` in CI (Step 8, `deploy-context`). It is driven by production usage, not by the test run.

Two further points: nao's order has a smoke test with `nao chat` before tests, and it has no separate "annotate tables" step. The skills never mention `annotations.md`, and the playbook only says "add data context", then "add documentation repo (dbt / semantic layer)", then "company & domain rules".

**nao's recommended order** (combining the skills' "When to use which" diagram, the setup-context steps and the playbook):

```
1. Scope (≤20 gold/mart tables) + nao_config.yaml + nao init --no-tty          [setup-context]
2. nao sync (+ connect dbt/doc repos so their docs/semantic layer sync too)    [setup-context / playbook step 2]
3. RULES.md generated immediately (inventory → section by section)             [write-context-rules]
   + domain sub-rules / metric definitions as referenced .md files             [playbook step 4]
4. LLM key → nao debug → nao chat smoke test (3-5 real questions)              [setup-context]
5. Tests: ~20 key questions, ≥1 per metric                                     [create-context-tests]
6. nao test → baseline → diagnose failures → one fix at a time, re-run         [create-context-tests / audit-context anytime]
7. ONLY IF failures are metric-reliability → semantic layer → back to rules    [add-semantic-layer → write-context-rules]
8. Roll out to a small group; version in git; nao test in CI; deploy on main   [playbook 7-8 / deploy-context]
9. Recommendations from production usage → fix as PR → re-run nao test         [playbook step 9]
10. Scale gradually                                                            [playbook step 10]
```

For this project, a nao-compliant version of the order under review would be: **scope → sync → annotate tables (a reasonable addition) → RULES.md → metric definitions as sub-rule .md files → RULES.md routing updated → smoke test → tests → run/diagnose → (semantic.yaml only if tests demand it) → rollout/CI/deploy → recommendations/PR.**
