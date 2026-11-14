# nao feature review: what the talk shows, what it should mention, what's on the roadmap

Reviewed 2026-11-14. Sources:
- nao docs (fetched 2026-11-14)
- the getnao/nao README and commit history on `main` (latest commit 2026-11-14)
- nao-core 0.4.2 (the PyPI version used in this repo)
- Claire's interviews and podcasts (hub research note, 2026-10-26)

Features marked **main** are merged on GitHub but may not be in your installed version or in nao Cloud yet. Check before you show them live.

## 1. Coverage: every major feature against the talk

| Area | Feature | In nao since | In the talk? | Where / suggestion |
|---|---|---|---|---|
| **Build context** | `nao init` / `nao sync`, file-system context (`databases/`, `semantics/`, `docs/`, `repos/`) | core | ✅ | TP-03, TP-04 |
| | `include` / `exclude` / `allow_listed_only` | core | ✅ | TP-04 (scope card) |
| | `exclude_columns` (hide PII before sync) | core | ✅ (privacy warning) | TP-04. Name the feature on the slide |
| | Profiling, preview, query history, AI summary templates | core | ⚠️ partly | TP-04 says "value counts"; query history is worth a mention for Snowflake / Databricks / Fabric shops |
| | Table `annotations.md`, never overwritten by sync | 0.4.x | ✅ | TP-05 |
| | **Annotations attached automatically when the agent reads `columns.md`** | main, 2026-11-10 | ➕ add | TP-12 (suspect 3: "the agent never saw it"). nao now makes it harder to miss your notes |
| | RULES.md, sub-rule files, group-conditional rules | core | ✅ | TP-07 |
| | Semantic layer: dbt MetricFlow sync and `execute_semantic_query` | 2026-09/10 | ➖ Q&A only | Mention as "if you have dbt MetricFlow, plug it in" (Claire: keep definitions upstream where they exist) |
| | Notion / Confluence / Obsidian sync into `docs/` | core / 2026-09 | ➖ | Optional: "your methodology docs can be synced, not copied" |
| | Skills: `setup-context`, `write-context-rules`, `create-context-tests`, `audit-context`, `add-semantic-layer`, `deploy-context` | 2026-10 | ⚠️ not shown | Add one line to TP-04 or the README: "nao's own skills audited this repo" (`reviews/01-nao-skills-audit.md`) |
| | Warehouses incl. **Fabric**, MSSQL with **Entra ID auth**, Snowflake, Databricks, DuckDB/DuckLake | core / main 2026-11-09 | ➖ | Relevant for an Azure / Fabric shop. Q&A |
| **Evaluate** | `nao test` with reference SQL, row-order-insensitive comparison, tolerances | core | ✅ | TP-08 |
| | Assertions: the agent must call `clarification` | 2026-09-30 | ✅ | TP-07 / TP-08 |
| | `-k` pass@k and pass^k (consistency) | 2026-09-30 | ⚠️ in README only | **TP-13**: "run each question three times; one lucky answer isn't reliability" |
| | Multi-model and reasoning-effort comparison | 2026-11-04 | ➖ | Q&A: "once context is right, pick the model on cost" |
| | **Server-side context tests with draft comparison** (test a context change before merging) | main, 2026-11-04 | ➕ add | TP-10 (suspect 1): "test the draft against main before the owner approves" |
| | **Filter tests by owner and tag**; test runs visible to admins | main, 2026-11-10/11 | ➕ add | TP-17 ownership: tests have owners too |
| **Observe and improve** | Chat replay (every conversation, answer time, chat owner) | 2026-11-02 | ➕ add | Audit trail: "what did the agent actually see?" (TP-09) |
| | Thumbs up/down feedback (chats and stories) | core / 2026-10-21 | ⚠️ implied | TP-16 "thumbs down" |
| | Context recommendations: ranked, with provenance, drafted patch, PR; YOLO mode | beta 2026-06 → GA | ✅ | TP-16 |
| | Recommendations over MCP (`list_recommendations`, …) | 2026-10-27 | ➖ | Q&A: "your coding agent can work the recommendation backlog" |
| | Automations, incl. a **feedback trigger** (act on a downvote) | 2026-10/11 | ➖ | Optional in TP-16 |
| | **Owners on context docs** (Context Explorer; assign one owner to every doc of a table) | main, 2026-11-14 | ➕ add | TP-10 + TP-17: nao now records the keeper, which fits the lighthouse rule |
| | Context Explorer: File Explorer, Changes panel, branches, header editing | main, 2026-11-13/14 | ➖ | Nice for the recording: actuaries can edit definitions without git |
| **Use** | Chat with visible SQL and files ("transparent reasoning") | core | ✅ | TP-14 |
| | Stories / live stories (dashboards, data apps, slides), filters, parameters, admin-**certified** stories | 2026-09 → 11 | ➕ add | TP-15: "once the actuary signs off, certify the story so others reuse the approved version" |
| | Slack, Teams, Discord, WhatsApp, Telegram; nao MCP for Claude and other clients | core / 2026-10 | ➖ | One line in the close: "same context layer, wherever people ask" |
| | Migrate Metabase / Tableau to stories | 2026-09-30 | ➖ | Skip |
| **Govern** | User groups: context permissions (`filesAccess`), row-level security, per-group MCP tools and skills | 2026-09 → 10 | ⚠️ not shown | TP-17 or Q&A. **Watch out:** permissions can *hide* a definition from a group, which is suspect 3 |
| | SSO (Entra ID, OIDC), identity passthrough, Redshift RLS | enterprise | ➖ | Q&A |
| | Budgets per user / group / provider; CSV export | 2026-10 | ➖ | Q&A on cost |
| | Self-host (Docker, Helm, AWS); nao Cloud; SOC 2 Type II; BYO LLM key | core | ➖ | Q&A on security |

Legend: ✅ covered · ⚠️ partly · ➕ should add (directly supports the story) · ➖ Q&A or optional.

## 2. Roadmap themes (from Claire's public statements, as of Oct 2026)

These are statements of direction, not commitments; source: hub research note, 2026-10-26.
1. **Evals and governance as the product.** CI/CD tests and conversation analytics. *Already visible:* server-side tests, test owners and tags, chat replay.
2. **Automated context upkeep.** Recommendations that open PRs for human review. *Shipped (beta → GA).*
3. **Context as organizational memory, one source of truth across Slack and MCP** ("context needs its own stack", "nao-os" company brain). *Partly shipped:* MCP context-layer mode, Slack, Teams.
4. **Enterprise readiness**: security, access, cost. *Shipped:* group permissions, budgets, SSO, licensing.
5. **Semantic-layer integration** (MetricFlow). *Shipped.*
6. **Vibe-coded apps / custom stories inside nao.** *Shipped (Oct–Nov).*

**Good questions for Claire's clips or for Q&A:** owners on context docs and draft comparison are days old. Ask her how she expects data teams to use *owner + test + recommendation* together, which is exactly this talk's ownership argument.

## 3. Changes made to the talk from this review

- TP-10 (knowledge) mentions draft-vs-main testing and owners on context docs.
- TP-12 (runtime) mentions annotations now auto-attached when columns are read, and the permissions caveat.
- TP-13 (checks) adds pass^k: run each question three times.
- TP-09 (audit trail) mentions chat replay.
- TP-15 (judgement) mentions certified stories.
- The other ➖ items stay out of the script and live in Q&A prep.
