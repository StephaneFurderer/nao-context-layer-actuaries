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

CLIP = lambda title, q: f"""---
layout: center
class: text-center
---

<div class="text-7xl mb-6">🎙️</div>

# Claire Gouze · CEO, nao Labs

### {q}
"""

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

<div class="mt-12 opacity-70 text-lg">
Stéphane Furderer · Actuarial Technology Summit · December 15, 2026<br/>
<span class="text-base">All data in this talk is synthetic.</span>
</div>
"""),
    ("TP-01", """---
---

# "What was our accident-year 2025 loss ratio?"

<img src="/waterfall.svg" class="mx-auto h-96" />

<div class="text-center opacity-70">Three rules, nine points. Same data; both queries run. Valued 2026-09-30 · incurred net of recoveries, gross of reinsurance, excl. LAE · no IBNR · synthetic travel insurer</div>
"""),
    ("TP-02", """---
---

# The AI can read your data

<div class="grid grid-cols-2 gap-12 mt-8 text-xl">
<div>

### ✅ It worked out
- code **40** is a recovery
- the **test partner** is fake
- the **accident year** is the loss year

</div>
<div>

### ❓ It had to guess
- what **attritional** means here
- where our **large-loss threshold** is
- how we **quote frequency**

</div>
</div>

<div class="mt-14 text-3xl text-center font-bold">It cannot read your decisions.</div>
"""),
    ("TP-03", """---
layout: two-cols
---

# A context layer is<br/>the new analyst's binder

<div class="text-xl mt-6 leading-10">

- which premium, which threshold, which partner is fake
- written once, in plain words
- one short **rule sheet**, read every time
- other pages looked up **when needed**
- reviewed, versioned, **tested**

</div>

::right::

<div class="mt-20 text-lg">

```text
context/              ← a nao project = a folder
├── RULES.md          ← the rule sheet
├── semantics/        ← our decisions
├── databases/…       ← what the data means
└── tests/            ← the answer key
```

</div>
"""),
    (None, CLIP("A", "Why should data teams become context teams?")),
    ("TP-04", """---
---

# Step 1 · Scope, then sync

<div class="grid grid-cols-3 gap-6 mt-8 text-center text-xl">
<div class="border-2 rounded-lg p-6"><div class="text-4xl">✅</div><b>In</b><br/>5 clean tables<br/><span class="text-base opacity-70">policies, premium, claims, transactions, partners</span></div>
<div class="border-2 rounded-lg p-6"><div class="text-4xl">🚫</div><b>Out</b><br/>raw feeds, staging<br/><span class="text-base opacity-70">nao suggests ≤ 20 tables to start</span></div>
<div class="border-2 rounded-lg p-6"><div class="text-4xl">🔒</div><b>Locked</b><br/>queries outside the 5<br/>are blocked</div>
</div>

<div class="mt-10 text-xl"><code>nao sync</code> → per table: columns · sample rows · value counts</div>
<div class="mt-3 text-lg">⚠️ Sample rows go to the model: <b>hide personal columns first.</b></div>
"""),
    ("TP-05", """---
---

# Step 2 · Write down what the data means

<div class="text-2xl mt-8 leading-12">

| code | means |
|---|---|
| `10` | payment |
| `20` | case reserve change |
| `40` | **recovery: stored positive, reduces the loss** |

</div>

<div class="mt-8 text-xl">+ free-look cancellations earn nothing · <code>ZZTEST</code> is test data (fix it upstream when you can)</div>
<div class="mt-6 text-xl opacity-80">A guess may change tomorrow. Written down, the answer is the same every time.</div>
"""),
    ("TP-06", """---
---

# Step 3 · Write down your decisions

<div class="grid grid-cols-2 gap-10 mt-6 text-lg">
<div class="border-2 rounded-lg p-5">

### Loss ratio
incurred **net of recoveries, gross of reinsurance**, excl. LAE<br/>÷ **gross earned** premium<br/>accident year · valued 30 Sep 2026 · **no IBNR** (AY 2025 fully closed)<br/>
<span class="opacity-70">owner: reserving actuary</span>

</div>
<div class="border-2 rounded-lg p-5">

### Our conventions
**large loss** ≥ \\$5,000 (reporting threshold)<br/>**attritional** = hurricane claims out,<br/>every other claim **capped** at \\$5,000<br/>
<span class="opacity-70">owner: reserving actuary</span>

</div>
</div>

<div class="mt-10 text-2xl text-center">Cap: <b>38.2%</b> · Drop instead: <b>32.8%</b> · both defensible, only one is ours</div>
"""),
    ("TP-07", """---
---

# Step 4 · One short rule sheet

<div class="text-2xl mt-8 leading-12">

- 📍 **Where** each definition lives (point to it, don't copy it)
- 🔁 **Always**: earned premium · no test partner · recoveries reduce losses
- 📅 **"Today"** means the valuation date, 30 September 2026
- ❓ **When the question is unclear, ask.**

</div>

<div class="mt-8 text-xl opacity-80">"What's the loss ratio?" → <i>"For which accident year, and all-in or attritional?"</i></div>
"""),
    ("TP-08", """---
---

# Step 5 · Write the answer key, then test

<div class="text-base mt-2">

| 9 questions, signed-off answers | tables only | + table notes | + decisions |
|---|:-:|:-:|:-:|
| loss ratio, by region, by coverage, earned, monthly | ✅ | ✅ | ✅ |
| **large losses** (≥ \\$5k) | ❌ \\$10k | ❌ \\$10k | ✅ |
| **attritional loss ratio** | ❌ 39.1% *(dropped ≥ \\$10k)* | ❌ 39.1% | ✅ 38.2% |
| frequency (per 1,000) | ⚠️ per policy | ⚠️ per policy | ✅ |
| "What's the loss ratio?" → ask | ✅ / ❌ | ✅ | ✅ |
| **passed** (two runs each) | **6 · 5** | **6 · 6** | **9 · 9** |

</div>

<div class="text-xs opacity-60 mt-1">SIMULATION, not nao output: blind Claude Sonnet analysts, one context level each, graded at 4 decimals by evals/grade.py (mimics nao test). Synthetic data, small n, presenter's own grader. Not a production result.</div>
"""),
    (None, CLIP("B", "When an answer is wrong: is it the context, the data, the query, or the test?")),
    ("TP-09", """---
---

# Diagnose before you fix

<div class="grid grid-cols-4 gap-5 mt-10 text-center text-xl">
<div class="border-2 rounded-lg p-5"><b>Context</b><p class="text-base">a missing or unclear definition</p></div>
<div class="border-2 rounded-lg p-5"><b>Data</b><p class="text-base">wrong, late or badly modelled tables</p></div>
<div class="border-2 rounded-lg p-5"><b>Query</b><p class="text-base">right definition, wrong SQL</p></div>
<div class="border-2 rounded-lg p-5 border-blue-500"><b>Test</b><p class="text-base">a vague question or answer key</p></div>
</div>

<div class="mt-10 text-xl">Asia 2025: 0.082 per policy vs 82 per 1,000: <b>wrong answer, or vague question?</b></div>
<div class="mt-3 text-lg opacity-80">Claire's study: most of the gain came from the data model; fixing tests mattered, but less.</div>
"""),
    ("TP-10", """---
---

# All-in 49.4% · attritional 38.2%: what's in the gap?

<div class="grid grid-cols-2 gap-4 mt-2">
<img src="/region.svg" class="h-76 mx-auto" />
<img src="/caribbean_monthly.svg" class="h-76 mx-auto" />
</div>

<div class="mt-2 text-lg">Caribbean AY 2025: <b>100%</b> · trip cancellations: ~13/month → <b>~100/month, Aug–Oct</b> · tagged <code>HU25</code> · <i>pattern planted in the synthetic data</i></div>
"""),
    ("TP-11", """---
---

# Judgement stays with the actuary

<div class="grid grid-cols-2 gap-12 mt-10 text-2xl">
<div>

### 🔎 Found by the agent
- the spike, the region, the months
- every query visible
- in minutes

</div>
<div>

### ✍️ Decided by you
- a one-off cat, or a trend to price?
- revisit the cruise partner?
- **then write the decision down**

</div>
</div>
"""),
    ("TP-12", """---
---

# Corrections become reviewed changes

<div class="grid grid-cols-4 gap-4 mt-14 text-center text-xl">
<div class="border-2 rounded-lg p-5">👎<br/><b>Correction</b><br/><span class="text-base">a user downvotes or fixes an answer</span></div>
<div class="border-2 rounded-lg p-5">📋<br/><b>Suggestion</b><br/><span class="text-base">nao ranks the gap and shows the chats behind it</span></div>
<div class="border-2 rounded-lg p-5">✅<br/><b>Reviewed change</b><br/><span class="text-base">a pull request the owner approves</span></div>
<div class="border-2 rounded-lg p-5">🧪<br/><b>New test</b><br/><span class="text-base">so it never comes back</span></div>
</div>

<div class="mt-10 text-xl">Automatic mode opens the changes without review. <b>For actuarial definitions: off.</b></div>
"""),
    ("TP-13", """---
---

# Ownership is the real deliverable

<div class="text-xl mt-6">

| what the AI reads | owner | check |
|---|---|---|
| loss ratio, large & cat losses | reserving actuary | answer key, every change |
| claim frequency | pricing actuary | answer key, every change |
| table notes | reserving + data engineering | answer key, every change |
| the whole agent | analytics lead | full agent test, on a schedule |

</div>

<div class="mt-8 text-xl opacity-80">We already govern reserving models this way (ASOP 56). Do the same for the words the AI reads.</div>
"""),
    (None, CLIP("C", "Who should own the context, and how do you know it's getting better?")),
    ("TP-14", """---
---

# Monday morning

<div class="text-3xl mt-10 leading-16">

1. **One question** your team argues about
2. **Write it down**: meaning + decisions + owner
3. **Write the answer key**: the SQL you would sign
4. **Test the agent** before anyone else uses it

</div>

<div class="mt-8 text-xl opacity-80">Start with one question, and earn the next nineteen.</div>
"""),
    ("TP-15", """---
layout: center
class: text-center
---

# The model is fast.<br/>Your definitions make it right.

<img src="/qr.svg" class="mx-auto h-40 mt-8" />

<div class="mt-4 text-xl"><code>github.com/StephaneFurderer/nao-context-layer-actuaries</code></div>
<div class="mt-2 opacity-70">Synthetic data · run it · break it · tell me what you find</div>
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
