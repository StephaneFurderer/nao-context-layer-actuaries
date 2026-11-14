# Review round 1: what the independent reviewers found, and what changed (v1 → v2)

Five independent agents reviewed v1. None of them had seen the work being produced.

| # | Reviewer | Report |
|---|---|---|
| 0 | Cold start: fresh clone, follow the README | summarized below (the agent could not write files) |
| 1 | nao's own skills (`nao skills add getnao/nao`, audit-context) | `01-nao-skills-audit.md` |
| 2 | Skeptical senior P&C actuary | `02-critique-senior-actuary.md` |
| 3 | Talk coach (timing, clarity, slides) | `03-critique-talk-coach.md` |
| 4 | nao fact-checker (docs + CLI) | `04-critique-nao-factcheck.md` |

## Accepted and fixed

**Correctness and honesty**
- **Answer leakage** (2): the metric files held SQL patterns almost identical to the reference answers. They are now prose only, and all agents were re-run (run 4).
- **Lenient grader** (2, 4): 2-decimal comparison let a wrong attritional method pass. The grader and `nao_config.yaml` `test.comparison.decimals` are now 4.
- **Unit failures labelled as context failures** (2): the grader now flags unit-only mismatches separately, and TP-09 asks "wrong answer or vague question?".
- **Implausible "$10k per-risk retention"** (2): the threshold is now a $5k *reporting* threshold. Every blind agent still guessed $10k.
- **Capping vs dropping framed as right vs wrong** (2): now "two defensible conventions; only one is ours" (38.2% vs 32.8%).
- **Terminology** (2): "incurred net of recoveries, gross of reinsurance, excl. LAE, gross earned premium, case reserves only, no IBNR".
- **The planted finding presented as a discovery** (2): disclosed on stage in TP-10. Hurricane loss dates now cluster before departure.
- **TP-01 implied the AI produced 58.9%** (3): it was a hand-written naive query. The script now says "two answers from the same data". "In this room" was removed (the talk is prerecorded).
- **"Auto-merge mode" is wrong** (3, 4): YOLO mode auto-*opens* PRs; it does not merge them.
- **Claire's 45→86% study misquoted** (4): fixing tests was worth 49→51%; the data model drove most of the gain.
- **The CI agent job could never pass** (4): no model, no login on a fresh instance. CI now checks the answer key and every quoted number. The agent test is documented as a scheduled local or hosted run.
- **"Every PR reruns the reference questions"** (4): reworded to "re-checks the answer key automatically; the full agent test runs on a schedule".

**Reproducibility** (0)
- `nao-core[duckdb]` extra was missing (no pyarrow), so `make all` failed. Fixed in `requirements.txt`.
- macOS 15+, Python ≥ 3.11 and venv steps documented. The `nao test` login and model requirements documented.
- `check_reference_sql.py` now **asserts** every number quoted in the talk.
- `grade.py` no longer overwrites results when run without arguments.

**nao conventions** (1)
- RULES.md gained Data architecture, Most used tables, Date filtering (anchored on the valuation date, not today) and Analysis process sections, and points to `profiling.md` for value checks.
- Test output columns follow the skill's naming rule (`*_float_0_1`, `*_usd_dollars`, `*_date_yyyy_mm_dd`, `*_count`), and the leaky "return a date" prompt hint was removed.
- A `test:` block was added (model, k = 3, 4 decimals), plus a commented `llm:` block in the docs' syntax.

**Talk** (3)
- Act 2 cut from 7 steps to 5. The script went from 18 to 15 points: 11.0 min at 120 wpm, with numbers counted as spoken.
- One through-line ("The AI can read your data. It cannot read your decisions.") and the closing line are now said aloud.
- Clip B moved to right after the results grid.
- Config and code walls replaced with plain-language cards. Signed waterfall, QR code, sponsor placeholder removed.

## Not done (needs Stéphane)
- **Record nao chat on the Mac** for TP-10 and the grid: this workspace has no LLM key. Commands are in the README.
- **Run the real `nao test -k 3`** and replace the simulated grid with nao's own output, or show both.
- **Cut the Claire clips** to the three questions on the clip slides (about 3 min each).
- **Replace the CODEOWNERS placeholder handles** before showing the file, or keep showing the owner table only.
- **Sponsor slide**: insert the organizer's slide.
- **Q&A prep** (from review 2): GL / Schedule P reconciliation, ASOP 23/41/56, NAIC AI bulletin, privacy of `preview.md` sample rows, and "this is not a reserving tool".

# Review round 2 (v2 → v2.1)

- **Cold start from GitHub** (fresh venv, Python 3.13): `make all`, `slidev build` and re-grading all pass. Every grade matches `evals/blind-agent-results.md`.
- **Final-pass review** (actuary and coach): 8 edits applied.
  - TP-02: the test partner was found through its `internal` label, not round amounts.
  - TP-08: the grid is said aloud to be a simulation outside nao.
  - TP-09: 82.1 per 1,000 is Asia's row.
  - TP-10: the baseline is about 13 a month (the old "under 20" was wrong; July = 20).
  - TP-06: the through-line is now said a second time.
  - The basis now shows excl. LAE and gross earned premium, with AY 2025 fully closed, on slides 2 and 7.
  - French-speaker wording fixes: "end of September", "To be clear", "badly written tests".
