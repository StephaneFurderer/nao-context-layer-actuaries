# nao fact-check: talk, slides, repo (nao-core 0.4.2)

Checked against the fetched docs in /home/claude/naodocs, extra pages fetched from docs.getnao.io (admin/setup), the installed CLI (`nao ... --help`, and the nao_core source under /usr/local/lib/python3.13/site-packages/nao_core), and an experiment on a copy of the project in /tmp/naocheck/ (nothing in /home/claude/repo was modified; `nao chat` and `nao test` were not run).

Verdict key: **correct** / **wrong** / **imprecise** / **unverifiable**.

---

## A. Wrong or imprecise items (fix these)

### A1. TP-15 "There's an auto-merge mode" (talk/talking-points.md TP-15; slides.md line 402 speaker note)
- **Verdict: wrong.**
- Evidence: https://docs.getnao.io/nao-agent/context-engineering/recommendations : YOLO mode "opens pull requests automatically after each run, without human review". Later on the same page: "nao opens these PRs automatically after each run for you to review and merge." It opens PRs and marks the recommendations as applied. Nothing in the docs says it merges anything. (The slide line 399, "YOLO mode auto-opens PRs", and source-bank A8 are correct.)
- Fix (Say): "There's a mode, nao calls it YOLO mode, that opens the pull requests automatically after every run, with nobody reviewing the recommendation first. For actuarial definitions, I'd leave it off."

### A2. CI workflow `agent` job would not work (.github/workflows/context-tests.yml lines 17-30)
- **Verdict: wrong.** It fails for three separate reasons:
  1. **Wrong model.** No `-m` flag and no `test:` block in nao_config.yaml, so `nao test` uses its default model, `openai:gpt-4.1`. Evidence: evaluation page, "Run each test against the configured models, `openai:gpt-4.1` by default". Also the CLI source: `DEFAULT_TEST_MODELS = ["openai:gpt-4.1"]` (nao_core/config/test). Only `ANTHROPIC_API_KEY` is provided, so every run fails.
  2. **`NAO_API_KEY` cannot be valid here.** `nao test` does accept `NAO_API_KEY` (`nao test --help`: "Organization API key for authentication, replaces the login. Falls back to NAO_API_KEY env var."). But that key is an *organization API key created inside a running nao instance*. Docs: "Create one from Settings -> Organization Settings -> Organization API Keys." `nao test` sends it to `BACKEND_URL` (default `http://localhost:5005`, per commands/test/client.py). The `nao chat` started in CI is brand new: its SQLite DB (`DB_URI` default `sqlite:./db.sqlite` in the server's bin dir) has no users, no organization and no keys. A key from any other instance gets a 401. With an API key there is no fallback login (`_handle_auth_retry` returns False when api_key is set).
  3. **Startup is fragile.** `(nao chat &) && sleep 20` assumes the FastAPI and Node servers are up within 20 s and gives no readiness check. Also, nothing saves `tests/outputs/`.
- Things that are fine: `nao test` exits 1 on any failure (runner.py: `sys.exit(1)` after "failed"), so the job does gate PRs. Bare `nao test -k 3` is valid: `run` is the default subcommand. `nao chat` passes the environment through, so `ANTHROPIC_API_KEY` reaches the server.
- Fix: see the corrected workflow in section C.

### A3. TP-16 / slide 17 "Every pull request reruns the reference questions" (TP-16 Say; slides.md line 421)
- **Verdict: imprecise.** On every PR, only the `offline` job runs. It re-executes the reference SQL (`make check-sql`); it does not ask the agent anything. The agent job runs only when the repo variable `NAO_AGENT_TESTS == 'true'`, and as written it fails (A2).
- Fix (Say): "Every pull request re-executes the reference SQL, and, with the agent job switched on, re-asks the questions to the agent with nao test." Slide line 421: "Every pull request re-runs the reference SQL; the agent job re-asks the questions with `nao test`."

### A4. TP-11 "Then you run nao test, and you get a grid" (TP-11 Say)
- **Verdict: imprecise / misleading.** The grid on slide 12 was produced by `evals/grade.py` with blind sub-agents, not by `nao test`. `nao test` prints a "Pass / Fail by Test and Model" grid only for multi-model runs, and it has no notion of context levels. Evidence: evaluation page, the "Pass / Fail by Test and Model ... one column per model" section. The disclaimer at the end of the TP softens this, but the opening sentence says nao produced the grid.
- Fix (Say): "Then you run the tests and read the results as a grid. For this slide I ran the same nine questions with blind AI analysts at three levels of context, graded by a script that copies nao test's comparison rules." Keep the closing disclaimer.

### A5. TP-08 "two definitions of the same metric are the most common cause of inconsistent answers" (TP-08 Say)
- **Verdict: imprecise.** Evidence: https://docs.getnao.io/nao-agent/context-builder/rules-context : "Duplicating it in `RULES.md` and a semantic layer is the most common cause of inconsistent answers." The docs' claim is about *duplicating* a definition across files. The slide quote "Each metric should have exactly one canonical definition." is verbatim and correct.
- Fix (Say): "Nao's docs are blunt here: duplicating a metric's definition, say in the rules file and again in a metrics file, is the most common cause of inconsistent answers."

### A6. TP-07 / slide 8 "an annotations file ... that sync never overwrites" (TP-07; slides.md line 187)
- **Verdict: correct, with one caveat worth knowing for Q&A.** Docs (databases page): "`annotations.md` is created empty below the header, and **never overwritten**". I confirmed it: after `nao sync` on the copy, the annotations, semantics and RULES.md checksums were unchanged.
- **Caveat (verified by experiment):** if a table leaves the sync scope, the whole table folder is deleted, *including its hand-written annotations.md*. I changed `include` to `mart.claims`, ran `nao sync -p databases`, and got "4 stale removed". Only `table=claims/` was left. The configuration page warns about this: "`nao sync` removes any previously-synced table or schema that was not part of the run" unless you pass `--select`.
- Fix: no change to the Say is needed. Optionally add to the speaker notes: "Never overwritten, but deleted if you drop the table from scope, so keep it in git."

### A7. TP-03 "the AI reads the relevant pages before every answer" (TP-03 Say)
- **Verdict: imprecise.** Evidence: https://docs.getnao.io/nao-agent/context-engineering/contributing says only the system prompt and `RULES.md` are always loaded: "Everything else in the repository is invisible until the agent decides to go looking."
- Fix: "...and the AI always reads the first page, the rules, and looks up the other pages it needs before it answers."

### A8. TP-06 "For every table it writes three markdown files ... This is what any agent sees out of the box" (TP-06 Say)
- **Verdict: imprecise.** `profiling` is optional. Databases page: "`profiling` (optional; column-level statistics)". If you omit `templates`, the defaults are "`columns`, `query_history`, and `preview`", and `nao init` scaffolds only `columns` and `preview`. This project turned profiling on. Sync also creates the empty `annotations.md`. The code-40 claim is correct: profiling.md shows `txn_code` as `string`, `distinct_count: 3`.
- Fix: "Step two is one command: nao sync. For every table it writes the columns, a few sample rows and, because I switched it on, a profile of the values. That's structure only."

### A9. TP-12 / slide 13 Claire's 45% → 86% study (TP-12 Say; slides.md line 335)
- **Verdict: correct but under-weighted. Make it precise, since Claire is on the bill.** Source: https://thenewaiorder.substack.com/p/how-i-improved-my-analytics-agent . She lists the four steps as "fix data model, add more documentation, add date selection rules and fix ambiguous tests". Of the 28 weak tests, "4 Test issues ... One solution was actually wrong. And the others gave too few formatting indications" (for example, how to format a percentage). That matches the month-as-int case well. But the test fix was worth only **49 → 51%** ("1️⃣ Fix tests errors 49 → 51%"). The baseline re-run accounted for 45 → 49, and the data model for **65 → 86%** ("improved data modeling had the most impact").
- Fix, slide 13: "Claire's study: 4 of her 28 failing tests were test problems. Fixing them was a small step (49 → 51%); the data model did the heavy lifting (65 → 86%)." Fix, Say: "Claire found the same in her own study: a few of her failures were the test's fault, not the agent's. Fixing them was a small step; most of her gain came from the data model."

### A10. nao_config.yaml commented `llm:` block (context/nao_config.yaml, last 8 lines)
- **Verdict: imprecise (works, but not doc syntax, and not sufficient for tests).**
  - The line `api_key: ${{ env('ANTHROPIC_API_KEY') }}` uses a `$` prefix. The docs always write `{{ env('ANTHROPIC_API_KEY') }}` (configuration page). In 0.4.2 both forms load: I tested both on the copy and both resolve to the key, and the server regex is `/\$?\{\{\s*env\(...\)\s*\}\}/`. Use the documented form anyway.
  - The comment "Needed for `nao chat` / `nao test`" overstates it. The docs say credentials resolve "**admin UI** -> `nao_config.yaml` -> environment variables", so an exported `ANTHROPIC_API_KEY` alone is enough for `nao chat`. What `nao test` does need is a model: either `-m anthropic:...` or a `test.models` entry, because the default is `openai:gpt-4.1`.
- Fix: replace the block with the snippet in section D.

### A11. README "Known limits" and Makefile `test` target (README.md line ~75; Makefile `test:` comment)
- **Verdict: imprecise.** "The real `nao test` needs `nao chat` running and an LLM key" leaves out two things. You must log in: docs say "On the first `nao test` run, the CLI will prompt you to log in". And you must choose the model, or it defaults to `openai:gpt-4.1`.
- Fix (README): "The real `nao test` needs `nao chat` running, a login on that instance (browser, `NAO_USERNAME`/`NAO_PASSWORD`, or an org API key created in that instance), and an Anthropic model selected (`test.models` in nao_config.yaml or `-m anthropic:claude-sonnet-4-5`)." Makefile: `cd context && nao test -m anthropic:claude-sonnet-4-5 -k 3`, or rely on the `test:` block.

### A12. Source bank A7 puts a non-verbatim string in quotes (sources/source-bank.md row A7)
- **Verdict: imprecise.** It says "Advice: 'Avoid leakage: don't put exact answers in your context.'" The doc's actual wording: "**Avoid overfitting and leakage**: Avoid including exact answers or overly specific details in your context". The TP-10 paraphrase ("never paste the answers into the context") is fine as a paraphrase.
- Fix: quote it verbatim, or drop the quote marks.

### A13. Source bank R2 says "Seven reference questions" (sources/source-bank.md row R2)
- **Verdict: wrong (internal inconsistency).** context/tests/ has 9 YAML files, and TP-10, TP-11 and the README all say nine.
- Fix: "Nine reference questions".

### A14. TP-09 Show "RULES.md, about thirty lines" (TP-09 Show)
- **Verdict: imprecise (not a nao claim).** context/RULES.md is 45 lines (2,887 chars).
- Fix: "about forty-five lines", or "one screen".

---

## B. Claims checked and correct

| Location | Claim | Evidence |
|---|---|---|
| TP-09, README, source A4 | RULES.md loaded with every message | rules-context: "It is loaded with **every** message to the agent, so keep it lean." Contributor guide: "`RULES.md` - in full, every time." |
| TP-09 | Rules file as router / orchestrator | rules-context: "**Orchestrator**: point the agent to the right context fast" |
| TP-05, slide 6, A3 | `allow_listed_only` blocks SQL on tables not synced | databases: "any SQL that touches a table not present in this database's synced context is blocked before it runs". It also covers SQL a user edits by hand. Default `false`. |
| TP-05, slide 6, A6 | Start with no more than 20 tables | playbook: "**Maximum 20 tables** to begin with", mart/gold layer, "avoid raw staging tables" |
| TP-17, slide 18, A6 | 20 tables and 20 questions | playbook Step 5: "Develop a **test suite** of 20 key questions" |
| TP-10, A7 | Test = YAML with prompt + SQL; final data compared with reference | evaluation: "`sql`: ... Used to verify the agent's **final output** (dataframe equality)" |
| A7 | Row order ignored, 2 decimals, rtol 1e-5, row counts must match | evaluation "Data Comparison Process" (rtol 1e-5, atol 1e-8, `decimals: 2`) |
| TP-10, slide 11, ambiguous_loss_ratio.yml | Clarification assertion | evaluation: `tool_call` + `tool: clarification` is the exact doc example. "calling the clarification tool ends the run". File format matches. |
| README, Makefile, A7 | `nao test -k 3` = pass^k | `nao test --help`: "-k Number of times to run each test case, used to compute pass@k and pass^k". Docs: pass^k = "`1` if **all** `k` attempts passed" |
| README, Makefile, A1 | `nao chat` at localhost:5005 | `nao chat --help`: "Defaults to SERVER_PORT env var and 5005". Quickstart: "`http://localhost:5005`". (Internal FastAPI is on 8005.) |
| README, A7 | `nao test server` at :8765 | `nao test server --help`: "[default: 8765]"; evaluation: "`http://localhost:8765`" |
| TP-15, A8 | Recommendations: scheduled audit of errors, downvotes, corrections; ranked; provenance; PRs | recommendations: "On a schedule you choose (daily, weekly, or monthly), or on demand with **Run now**". Signals listed: tool errors, negative feedback, "Regenerations and corrections", coverage gaps. "Impact-ordered cards", "**Provenance** - the chat the friction came from". PRs need GitHub/GitLab connected and a target `owner/name` repo. |
| slide 16, A8 | "YOLO mode auto-opens PRs" | recommendations (see A1) |
| TP-06, slide 7 | Code 40 is just a string with three values | profiling.md: `"type": "string" ... "distinct_count": 3` |
| TP-03, A11, B6 | nao is open source | github.com/getnao/nao; YC page |
| workflow comment | Weekly test run "as the nao playbook suggests" | playbook Step 8: "**Run `nao test` frequently** (e.g., weekly or after major changes)" |
| context/.naoignore | `tests/` ignored | It is the `nao init` default (`init.py`: `templates/\n*.j2\ntests/`). The chat server's file tools load `.naoignore`, so the agent can't read the answer key, which supports the leakage advice. |
| B3 source row | Four steps; data modeling had most impact; "context engineering is mostly data engineering" | Substack article (quote matches) |
| B4 source row | 10–20 tables, plug in dbt docs, baseline | dbt Roundup: "reduce the scope to maybe 10 or 20 tables. Plug in what you already have, usually your dbt docs" |
| B2 source row | 30 experiments | Substack: "I ran 30 context experiments" (10 configs × 3 runs) |

---

## C. Project layout vs. nao conventions (context/)

- **Folder structure: correct.** `nao_config.yaml`, `RULES.md`, `agent/{mcps,prompts,skills,tools}`, `databases/`, `docs/`, `repos/`, `semantics/` and `tests/` match the overview and contributor-guide trees. The `agent/prompts/README.md` and `slack.md` (`{{ nao_prompt }}`) are standard scaffolding.
- **semantics/ with hand-written markdown metric definitions: correct for this project.**
  - The "Semantic Layer" page is specifically **dbt MetricFlow**. It needs a `semantic_layer:` block plus a `semantic_manifest.json`. `nao sync` then *generates* `semantics/README.md`, `semantics/dimensions.md` and `semantics/metrics/*.md` ("Do not edit the generated files: they are rewritten on every sync"). This project has no `semantic_layer:` block, so sync never touches semantics/. I confirmed this: checksums were unchanged after `nao sync`.
  - The contributor guide lists `semantics/` as **Manual**: "Domain knowledge: metric definitions, funnel stages, business terminology". For a canonical metric definition it says: "Your semantic layer if you have one, otherwise `semantics/<domain>.md` - **once, in one place only**".
  - Recommendations audits exactly `semantics/*.md` and opens PRs for "human-written files like `RULES.md` or `semantics/**`". So `semantics/` beats the `agent/semantics/` path used in the rules-context page's sub-rules example (the docs are inconsistent here; the repo picked the better option).
  - Caveat for the future: if a MetricFlow layer is added later, nao would write generated files into the same `semantics/` folder. No file names collide today (README.md, dimensions.md, metrics/), but generated and manual files would then sit side by side.
  - Q&A prep: Claire's stated view (dbt Roundup) is that docs should be maintained upstream: "I say the dbt docs, because it has to live as close to your daily work as possible". The honest answer is "no dbt in this sandbox; in production, put these in dbt or a MetricFlow layer and let nao sync them."
- **annotations.md: correct.** It carries the `type: manual` frontmatter, and the extra `owner:` key is harmless. Unverifiable: whether Recommendations opens a PR for an annotations.md fix or only shows "How to fix" guidance. The page says "For fixes that belong in generated files (`databases/**`, which `nao sync` rewrites) ... nao instead hands you clear guidance", and annotations.md lives under `databases/**`. Don't promise a PR for an annotation fix on stage.
- **Test-design risk (not a claim, but it affects real `nao test` results):** the ratio tests return fractions (0.499), and `nao test` rounds to `decimals: 2` before comparing. That makes 0.495 and 0.499 equal (both 0.50), so a 0.5-point loss-ratio error passes. An agent that returns 49.9 (percent) fails. Suggestion: add `test: comparison: decimals: 4`, and either have the prompts ask for a decimal fraction or have the reference SQL return a rounded percent.

---

## D. Minimal `llm:` block for Anthropic, and the test defaults

Per https://docs.getnao.io/nao-agent/context-builder/configuration ("LLM providers and models": "Leave `models` out to expose the provider's built-in model list"):

```yaml
llm:
  providers:
    - provider: anthropic
      api_key: {{ env('ANTHROPIC_API_KEY') }}
```

Recommended for this repo (pins the chat default and makes `nao test` use Anthropic; the keys are documented in the evaluation page's "Defaults in nao_config.yaml"):

```yaml
llm:
  providers:
    - provider: anthropic
      api_key: {{ env('ANTHROPIC_API_KEY') }}
      models:
        - id: claude-sonnet-4-5
          default: true

test:
  models:
    - anthropic:claude-sonnet-4-5
  k: 3
  comparison:
    decimals: 4
```

Strictly, `nao chat` also works with no `llm:` block if `ANTHROPIC_API_KEY` is exported, because of the env-var fallback. The `test:` block, or `-m`, is the part that matters for `nao test`.

---

## E. Corrected CI `agent` job

Approach: start a **fresh, throwaway local nao chat**, create its first user (docs, admin/setup: "The first user to sign up after deployment automatically becomes an admin"), then authenticate `nao test` with `NAO_USERNAME`/`NAO_PASSWORD`. These are documented for CI: "Or via environment variables (recommended in CI ...)". Drop `NAO_API_KEY`: a key from another instance is meaningless to a fresh local server.

**Not executed here** (I was told not to run nao chat/test). The sign-up call uses the server's better-auth endpoint `/api/auth/sign-up/email`. The string is present in the server binary, and the CLI's own login posts to `/api/auth/sign-in/email`, but no doc page covers it. Run the job once on a branch before relying on it.

```yaml
  agent:
    # Runs nao test against a throwaway local nao instance. Needs ANTHROPIC_API_KEY.
    runs-on: ubuntu-latest
    needs: offline
    if: ${{ vars.NAO_AGENT_TESTS == 'true' }}
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      BACKEND_URL: http://localhost:5005
      NAO_USERNAME: ci@example.com
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt && make data context
      - name: Throwaway password for the ephemeral instance
        run: echo "NAO_PASSWORD=$(openssl rand -hex 16)" >> "$GITHUB_ENV"
      - name: Start nao chat and wait until it answers
        working-directory: context
        run: |
          nohup nao chat > "$RUNNER_TEMP/nao-chat.log" 2>&1 &
          for i in $(seq 1 90); do
            curl -fsS -o /dev/null "$BACKEND_URL" && exit 0
            sleep 2
          done
          cat "$RUNNER_TEMP/nao-chat.log"; exit 1
      - name: Create the CI user (first sign-up becomes admin)
        run: |
          curl -fsS -X POST "$BACKEND_URL/api/auth/sign-up/email" \
            -H "Content-Type: application/json" -H "Origin: $BACKEND_URL" \
            -d "{\"email\":\"$NAO_USERNAME\",\"password\":\"$NAO_PASSWORD\",\"name\":\"CI\"}"
      - name: nao test (Anthropic, pass^3)
        working-directory: context
        run: nao test -m anthropic:claude-sonnet-4-5 -k 3 -t 3
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: nao-test-results
          path: |
            context/tests/outputs/
            ${{ runner.temp }}/nao-chat.log
```

Plus the `llm:` and `test:` blocks from section D in context/nao_config.yaml. With those in place, `-m` and `-k` on the command line are redundant but harmless.

Alternative: run against a persistent deployed nao instance with an org API key created *there* (`NAO_API_KEY` + `BACKEND_URL`). That tests whatever context is deployed under `project_name`, not the PR's files. The nao deploy skill also warns "no `pull_request` trigger (forks could exfiltrate the key)". So the local throwaway instance is the better fit for PR checks. GitHub doesn't pass secrets to fork PRs, so on forks this job won't have its keys and won't work either way.
