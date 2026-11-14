"""Generate slides/slides.md: visual content here, speaker notes pulled from talk/talking-points.md.

    python slides/build_slides.py && cd slides && npx slidev slides.md
Keeping notes generated means the deck can never drift from the validated talking points.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tp_text = (ROOT / "talk" / "talking-points.md").read_text()
heads = list(re.finditer(r"^### (TP-\d+)\s*[—-]\s*(.+)$", tp_text, re.M))
NOTES = {}
for i, h in enumerate(heads):
    block = tp_text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(tp_text)]
    say = re.search(r"^\*\*Say:\*\*\s*(.*?)(?=^\*\*\w+:\*\*)", block, re.M | re.S).group(1).strip()
    NOTES[h.group(1)] = say


def read(p, start=None, end=None):
    lines = (ROOT / p).read_text().splitlines()
    return "\n".join(lines[start:end])


ANN = "context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/annotations.md"
PROF = "context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/profiling.md"
prof_line = [l for l in read(PROF).splitlines() if '"txn_code"' in l][0]

SLIDES = [
    (None, """---
theme: default
title: Building the Context Layer
info: Actuarial Technology Summit 2026. Synthetic data. github.com/StephaneFurderer/nao-context-layer-actuaries
class: text-left
drawings:
  persist: false
transition: fade
mdc: true
---

# From actuarial knowledge<br/>to trusted AI analytics

## Building the context layer, step by step, with nao

<div class="mt-12 opacity-70">
Stéphane Furderer · Actuarial Technology Summit · December 15, 2026<br/>
<span class="text-sm">All data in this talk is synthetic.</span>
</div>
"""),
    ("TP-01", """---
layout: default
---

# "What was our 2025 loss ratio?"

<img src="/waterfall.svg" class="mx-auto h-88" />

<div class="text-center text-sm opacity-70">Same warehouse, SQL that runs both times. AY 2025, valued 2026-09-30, case incurred (no IBNR).</div>
"""),
    ("TP-02", """---
---

# The model is not the problem

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

### Inferred from the data ✅
- code `40` = recovery *(reserves net to 0, recoveries don't)*
- partner `ZZTEST` = test data *(60 claims at \\$9,999.99)*
- accident year = year of `loss_date`

</div>
<div>

### Conventions it had to guess ❌
- attritional: **cap** large claims, don't drop them
- frequency **per 1,000** policies
- ask before answering an ambiguous question

</div>
</div>

<div class="mt-10 text-xl">A guess that looks right is the dangerous kind: <b>39.3%</b> vs <b>41.6%</b>.</div>
"""),
    ("TP-03", """---
layout: two-cols
---

# A context layer is<br/>the new analyst's binder

- which premium, which year, which partner is fake
- written once, in plain words
- owned by a named actuary
- **read by the agent before every answer**
- tested like a model

::right::

```text
context/                  # a nao project = a folder
├── nao_config.yaml       # scope
├── RULES.md              # router + always-rules
├── semantics/            # one definition per metric
│   ├── loss_ratio.md
│   ├── claim_frequency.md
│   └── large_and_cat_losses.md
├── databases/…/table=claims/
│   ├── columns.md        # nao sync
│   ├── profiling.md      # nao sync
│   └── annotations.md    # you
└── tests/*.yml           # reference answers
```
"""),
    (None, """---
layout: center
class: text-center
---

# 🎙️ Claire Gouze, CEO, nao Labs

### Why data teams should become context teams
"""),
    ("TP-04", """---
---

# The sandbox: a synthetic travel insurer

| table | rows | grain |
|---|---:|---|
| `mart.policies` | 60,000 | policy, 4 partners + 1 test partner |
| `mart.earned_premium_monthly` | ~159k | policy × accounting month |
| `mart.claims` | ~4,200 | claim, `loss_date`, `cat_event_code` |
| `mart.claim_transactions` | ~13,700 | `txn_code` 10 / 20 / 40 |
| `mart.partners` | 5 | airline, OTA, cruise, direct, *ZZ* |

<div class="mt-6">Legacy-style codes · valued <b>2026-09-30</b> · one command: <code>make data</code></div>
"""),
    ("TP-05", """---
---

# Step 1: scope one question

```yaml
# context/nao_config.yaml
project_name: travel-actuarial
databases:
  - name: travel_warehouse
    type: duckdb
    include: [mart.*]          # gold / mart layer only
    exclude: [staging.*]       # raw feeds never reach the agent
    allow_listed_only: true    # SQL outside synced tables is blocked
    templates: [columns, preview, profiling]
```

**One question:** accident-year loss ratio. **Five tables.** nao's playbook: start with ≤ 20.
"""),
    ("TP-06", f"""---
---

# Step 2: `nao sync`: structure, not meaning

```bash
$ nao sync
✓ Sync Complete
  Databases: 5 tables across 1 datasets
```

`profiling.md` for `claim_transactions`:

```text
txn_code · distinct 3 · top values: "20" 8,102 · "10" 4,953 · "40" 666
```

<div class="text-xl mt-6">What is code <code>40</code>? The machine doesn't say.</div>
"""),
    ("TP-07", f"""---
---

# Step 3: annotate the tables

```markdown
{read(ANN, 7, 16)}
```

<div class="text-sm opacity-70">Hand-written, never overwritten by sync · owner: reserving actuary (CODEOWNERS)</div>
"""),
    ("TP-08", f"""---
---

# Step 4: define each metric once

<div class="grid grid-cols-2 gap-8">
<div>

### `semantics/loss_ratio.md`
- **Loss ratio** = net incurred ÷ **earned** premium
- **Accident year** = `YEAR(loss_date)`, the default basis
- net incurred = code `10` + `20` − `40`
- `ZZTEST` out of numerator *and* denominator
- valued 2026-09-30, **no IBNR**: say so

</div>
<div>

### `semantics/large_and_cat_losses.md`
*Decisions, not facts*
- **Large loss** ≥ \\$10,000 (our per-risk retention)
- **Cat** = any `cat_event_code` (HU25)
- **Attritional** = cat out, every other claim **capped** at \\$10,000
- owner: reserving actuary

</div>
</div>

> "Each metric should have exactly one canonical definition." (nao docs, Rules)
"""),
    ("TP-09", f"""---
---

# Step 5: `RULES.md` is a router, not an encyclopedia

```markdown
{read('context/RULES.md', 5, 22)}
```
"""),
    (None, """---
layout: center
class: text-center
---

# 🎙️ Claire Gouze

### Context, data, model or query: how do you tell?
"""),
    ("TP-10", f"""---
---

# Step 6: write the reference answers first

```yaml {{maxHeight:'330px'}}
# context/tests/attritional_loss_ratio_ay2025.yml
{read('context/tests/attritional_loss_ratio_ay2025.yml')}
```

<div class="text-sm">+ <code>ambiguous_loss_ratio.yml</code>: "What's the loss ratio?" passes only if the agent <b>asks a question back</b>.</div>
"""),
    ("TP-11", """---
---

# Step 7: run the tests, read the grid

<div class="text-sm">

| reference question | schema only (a) | schema only (b) | + annotations | full context (a) | full context (b) |
|---|:-:|:-:|:-:|:-:|:-:|
| loss ratio, by region, by coverage, earned, Caribbean monthly | ✅ | ✅ | ✅ | ✅ | ✅ |
| large losses (≥ \\$10k) | ✅ *guessed* | ✅ *guessed* | ✅ | ✅ | ✅ |
| attritional loss ratio | ❌ 39.3% | ❌ 39.3% | ❌ 39.3% | ✅ 41.6% | ✅ 41.6% |
| frequency by region | ❌ 0.079 | ❌ 0.082 | ❌ 0.082 | ✅ 82.1 ‰ | ✅ 82.1 ‰ |
| "What's the loss ratio?" → ask | ✅ | ❌ answered | ✅ | ✅ | ✅ |
| **passed** | **7/9** | **6/9** | **7/9** | **9/9** | **9/9** |

</div>

<div class="text-xs opacity-60 mt-4">Blind Claude Sonnet analysts, one context level each, graded by evals/grade.py (mimics nao test). Synthetic data, small n. Not a production result.</div>
"""),
    ("TP-12", """---
---

# Diagnose before you fix

<div class="grid grid-cols-4 gap-4 mt-8 text-center">
<div class="border rounded p-4"><h3>Context</h3><p class="text-sm">missing or ambiguous definition</p><p class="text-xs opacity-70">frequency "per 1,000"</p></div>
<div class="border rounded p-4"><h3>Data</h3><p class="text-sm">wrong or late data, bad model</p></div>
<div class="border rounded p-4"><h3>Query</h3><p class="text-sm">right definition, wrong SQL</p></div>
<div class="border rounded p-4 border-blue-500"><h3>Test</h3><p class="text-sm">the reference was ambiguous</p><p class="text-xs opacity-70">month as int vs date → fixed the test</p></div>
</div>

<div class="mt-10">Claire's own study: part of the 45% → 86% gain came from <b>fixing ambiguous tests</b>.</div>
"""),
    ("TP-13", """---
---

# The investigation: all-in 49.9%, attritional 41.6%

<div class="grid grid-cols-2 gap-4 mt-2">
<img src="/region.svg" class="h-72 mx-auto" />
<img src="/caribbean_monthly.svg" class="h-72 mx-auto" />
</div>

<div class="mt-4">Caribbean AY 2025: <b>95.7%</b> · trip-cancellation claims ~20 / month → <b>100</b> in August · tagged <code>HU25</code></div>
"""),
    ("TP-14", """---
---

# Judgement stays with the actuary

<div class="grid grid-cols-2 gap-10 mt-8 text-lg">
<div>

### Found by the agent
- the spike, the region, the months
- every query, visible
- minutes, not weeks

</div>
<div>

### Decided by you
- one-off cat, or a trend to price?
- load for it? revisit the cruise partner?
- **then write the decision into the context**

</div>
</div>
"""),
    ("TP-15", """---
---

# Close the loop: corrections become pull requests

```mermaid {scale: 0.62}
flowchart LR
  A[Correction<br/>or downvote] --> B[Recommendations<br/>audit]
  B --> C[Ranked card<br/>+ drafted patch]
  C --> D[Pull request]
  D --> E[Actuary review]
  E --> F[Merge +<br/>new test]
```

<div class="mt-6">"YOLO mode" auto-opens PRs. For actuarial definitions: <b>off</b>.</div>
"""),
    ("TP-16", f"""---
---

# Ownership is the real deliverable

```text
{read('CODEOWNERS')}
```

<div class="mt-4">Every pull request reruns the reference questions: <code>.github/workflows/context-tests.yml</code></div>
"""),
    (None, """---
layout: center
class: text-center
---

# 🎙️ Claire Gouze

### Who owns the context, and how do you know it's getting better?
"""),
    ("TP-17", """---
---

# Monday morning

1. **One bounded question** your team argues about
2. **Write what it means**, in plain words, with an owner
3. **Write the reference answer**: the SQL you would sign
4. **Test the agent** against it, before anyone else uses it

<div class="mt-10 opacity-80">nao suggests 20 tables and 20 questions. Start with one, and earn the next nineteen.</div>
"""),
    ("TP-18", """---
layout: center
class: text-center
---

# The model is fast.<br/>Your definitions make it right.

<div class="mt-10 text-xl"><code>github.com/StephaneFurderer/nao-context-layer-actuaries</code></div>
<div class="mt-2 opacity-70">Synthetic data · rerun it · break it · tell me what you find</div>

<div class="mt-8 text-sm opacity-60">Sponsor acknowledgement slide: supplied by the organizer</div>
"""),
]

out = []
for tp, body in SLIDES:
    s = body.strip("\n")
    if tp:
        s += f"\n\n<!--\n[{tp}] {NOTES[tp]}\n-->"
    out.append(s)
# first slide carries headmatter; join the rest with Slidev's separator style (each starts with ---)
(ROOT / "slides" / "slides.md").write_text("\n\n".join(out) + "\n")
print(f"wrote slides.md: {len(SLIDES)} slides, {sum(1 for t, _ in SLIDES if t)} with talking-point notes")
