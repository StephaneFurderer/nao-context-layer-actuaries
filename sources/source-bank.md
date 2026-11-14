# Source bank

Every claim in the talking points and slides traces to a row here. Tags:
- **[doc]**: official nao documentation, fetched 2026-11-14
- **[ext]**: external article or benchmark
- **[hub]**: Stéphane's own context-hub notes
- **[repo]**: produced and verified in this repo

Rule: anything that comes from a vendor is labelled as the vendor's claim. Synthetic-data results are never presented as production outcomes.

## A. nao documentation (primary, fetched 2026-11-14 with nao-core 0.4.2)

| # | Source | What we use it for |
|---|---|---|
| A1 | [Quickstart](https://docs.getnao.io/nao-agent/quickstart) | Three setup paths (coding-agent skills, nao Cloud, manual CLI). The CLI path is `pip install nao-core` → `nao init` → `nao debug` → `nao sync` → `nao chat` (localhost:5005) → `nao test`. |
| A2 | [Context builder overview](https://docs.getnao.io/nao-agent/context-builder/overview) | Context is a file system: `nao_config.yaml`, `RULES.md`, `databases/`, `docs/`, `repos/`, `semantics/`, `agent/`. |
| A3 | [Databases](https://docs.getnao.io/nao-agent/context-builder/databases) | DuckDB is supported. `include`/`exclude` globs, `exclude_columns` for PII, and `allow_listed_only: true`, which blocks SQL on tables that were not synced. Templates: `columns`, `preview`, `profiling`, `query_history`, `ai_summary`. |
| A4 | [Rules](https://docs.getnao.io/nao-agent/context-builder/rules-context) | `RULES.md` is loaded with every message. Keep it lean: it acts as an orchestrator and a context map. "Each metric should have exactly one canonical definition", and duplicating a definition is "the most common cause of inconsistent answers". Group conditionals are not an authorization boundary. |
| A5 | [Principles](https://docs.getnao.io/nao-agent/context-engineering/principles) | The three metrics are reliability, speed and cost. Context should be MECE, modular and not bloated. Too little or too much context both hurt. |
| A6 | [Playbook](https://docs.getnao.io/nao-agent/context-engineering/playbook) | Phase 1: ≤20 clean mart tables, docs, company and domain rules. Phase 2: 20 key questions, iterate until they pass, roll out to a small group, version in git, run `nao test` in CI. Phase 3: scale one domain at a time. |
| A7 | [Evaluation](https://docs.getnao.io/nao-agent/context-engineering/evaluation) | A test is YAML with `name` and `prompt` plus `sql` and/or `assertions`. The agent's final data is compared with the reference SQL result: row order ignored, 2 decimals by default (`test.comparison.decimals`), rtol 1e-5, row counts must match. A `clarification` tool-call assertion is available. Supports `-m` multi-model and `-k` for pass^k; `nao test server` runs on :8765. `nao test` needs `nao chat` running, a nao login, and a model (default `openai:gpt-4.1`). Advice, paraphrased: don't include exact answers in your context. |
| A8 | [Recommendations](https://docs.getnao.io/nao-agent/context-engineering/recommendations) | Online evals: a scheduled audit of tool errors, downvotes, corrections and coverage gaps. Produces ranked cards with provenance, can draft a patch and open a PR to the context repo. "YOLO mode" opens PRs automatically after each run, without human review of the recommendation. It does **not** merge them. We recommend leaving it off for actuarial context. |
| A9 | [Recommendations demo video](https://youtu.be/ybdNfvGXPjQ) | The feedback-loop demo Stéphane already wrote about (see H3). |
| A10 | [User groups](https://docs.getnao.io/nao-agent/chat/admin/user-groups) | Context permissions and row-level security by group. |
| A11 | [nao GitHub](https://github.com/getnao/nao) | Open source. |

## B. Claire Gouze / nao Labs (external, author is the interviewee)

| # | Source | Key point (paraphrased) | Caution |
|---|---|---|---|
| B1 | [Data teams should become context teams](https://thenewaiorder.substack.com/p/data-teams-should-become-context) | Context engineering = governance + engineering + science. Data teams should first prove context engineering works on their own scope. | Opinion piece |
| B2 | [First context engineering study: are semantic layers worth it?](https://thenewaiorder.substack.com/p/first-context-engineering-study-are) | 30 context experiments comparing metadata, sampling, profiling, dbt and rules. She asks readers to run their own tests rather than trust hers. | Her own benchmark, her own data |
| B3 | [How I improved my analytics agent reliability from 45% to 86%](https://thenewaiorder.substack.com/p/how-i-improved-my-analytics-agent) | Four steps: fix the data model, add documentation, add date-selection rules, fix ambiguous tests. Fixing tests was worth only 49→51%; the data model drove most of the gain (65→86%). Her conclusion: "context engineering is mostly data engineering". | Vendor study, not independently replicated. Claire is in the clips: quote the sizes correctly |
| B4 | [dbt Roundup: The context engineering playbook (Claire Gouze)](https://roundup.getdbt.com/p/the-context-engineering-playbook) | Start with the team that asks the most questions, scope 10–20 tables, plug in existing dbt docs, run tests to get a baseline. | Podcast summary |
| B5 | [Agentic analytics in production: conversation with Claire Gouze](https://thefulldatastack.substack.com/p/agentic-analytics-in-production) | nao's differentiator is building the context layer as a folder structure. | Interview |
| B6 | [YC company page](https://www.ycombinator.com/companies/nao-labs) | nao Labs (YC X25): an open-source framework to build and deploy analytics agents. | |

## C. Independent / third-party evidence

| # | Source | Key point | Caution |
|---|---|---|---|
| C1 | [dbt Labs: Semantic Layer vs Text-to-SQL, 2026 update](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026) | Run on an ACME **Insurance** dataset (11 questions, 20 runs per model). With a modeled semantic layer, accuracy approaches 100%. Better modeling also helps raw text-to-SQL. | Vendor (dbt) benchmark; small question set |
| C2 | [Semantic layers for reliable LLM analytics: paired benchmark (arXiv 2604.25149)](https://www.emergentmind.com/papers/2604.25149) | Curated semantic documentation raises first-shot accuracy by 17–23 pp across three frontier models. Context matters more than model choice. | Preprint, read via a summary page |
| C3 | [EntSQL benchmark review](https://www.themoonlight.io/es/review/entsql-a-benchmark-for-grounding-text-to-sql-in-long-context-enterprise-knowledge) | When private business rules are buried in long documents, the best system reached only 15.9% execution accuracy. Long unstructured docs are not a context layer. | Read via a review summary |
| C4 | [Hex: effective context engineering for AI agents](https://hex.tech/blog/effective-context-engineering-for-ai-agents/) | "Confident, cleanly formatted, completely wrong": the typical failure is missing context, not missing capability. | Vendor blog |
| C5 | [Collate: your text-to-SQL problem is not the LLM](https://www.getcollate.io/blog/your-text-to-sql-problem-is-not-the-llm) | The same LLM gives wrong or defensible answers depending on the context it reads. | Vendor claim (10.8% → 76.5%); do not quote the number on stage |

| C6 | [ASOP No. 56, Modeling (Actuarial Standards Board)](https://www.actuarialstandardsboard.org/?p=20987) | Applies to actuaries who design, develop, use or review models, including models built by others. Effective October 1, 2020. Used for the TP-13 framing: "we already govern reserving models this way". | US standard. Name it only in Q&A or on a slide footer, and let actuaries draw the parallel |

## H. Stéphane's hub (internal, context only, not for public claims)

| # | File in context-hub | Use |
|---|---|---|
| H1 | `projects/Actuarial Technology Summit 2026/context.md` | Organizer requirements, evidence reconciliation, and the rule: no invented quotes, no production ROI claims |
| H2 | `projects/Nao As A Context Layer/overview.md` | The 4-layer framing (data, semantics, context, agent), the "new analyst onboarding" analogy and the exoskeleton metaphor |
| H3 | `writing/context-layer/2026-09-30-nao-context-improvement-published.md` | Published LinkedIn post on the correction → PR feedback loop |
| H4 | `writing/context-layer/sources.md` | Previously verified quotes (playbook "restricted perimeter", OpenAI Frontier semantic-layer quote) |
| H5 | `projects/Nao As A Context Layer/output/presentation_playbook.md` | The March demo script (A/E investigation). Its "2 weeks → 1 hour" figure is **not** a measured saving |

## R. Produced in this repo (reproducible: `make all`)

| # | Artifact | Finding |
|---|---|---|
| R1 | `sql/waterfall_2025.sql` | The AY2025 loss ratio moves from a naive **58.1%** to a reference **49.4%** as three rules are applied. Earned premium *raises* it slightly (58.1→60.1); recoveries (→54.9) and dropping ZZTEST (→49.4) bring it down. Asserted by `evals/check_reference_sql.py`. |
| R2 | `context/tests/*.yml` + `evals/grade.py` | Nine reference questions (one must trigger a clarifying question), graded like `nao test` at 4 decimals |
| R3 | `evals/blind-agent-results.md` | Run 4, final: tables only 6/9 and 5/9; plus table notes 6/9 and 6/9; full context 9/9 and 9/9. A simulation, not a nao run. |
| R4 | `context/tests/loss_ratio_by_region_ay2025.yml` | Caribbean AY2025 loss ratio is **100.3%**, against 23–48% for every other region. Cancellations jump from about 13 a month (Jan–Jun average) to about 100 from August to October 2025. **Planted** in the synthetic data, and disclosed on stage. |

## TL;DRs (one line each, for quick reuse on stage or in posts)

- **A4:** RULES.md is a router, not an encyclopedia: one definition per metric, stored once.
- **A6:** Start with 20 tables and 20 questions. Don't add more until all 20 pass.
- **A7:** A test is a question plus the SQL an actuary signs off. nao checks that the agent's numbers match that SQL's result.
- **A8:** Every downvote becomes a ranked, traceable proposal to change the context, reviewed as a pull request.
- **B3:** Most of the reliability gain came from data modeling and documentation, not from prompts.
- **C1:** On an insurance dataset, giving the model governed metric definitions moved accuracy toward 100%.
- **C2:** Better context beat switching models in a paired benchmark.
- **R1:** Three rules every actuary knows moved our loss ratio by 9 points (58.1% → 49.4%).
- **R3:** Without the written conventions, every blind agent guessed a $10k large-loss threshold (ours is $5k) and dropped large claims instead of capping them.
- **C6:** We already govern reserving models (ASOP 56); the context the AI reads deserves the same.
