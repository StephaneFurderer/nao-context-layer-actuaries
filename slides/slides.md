---
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

---
---

# "What was our accident-year 2025 loss ratio?"

<img src="/waterfall.svg" class="mx-auto h-96" />

<div class="text-center opacity-70">Three rules, nine points. Same data; both queries run. Valued 2026-09-30 · incurred net of recoveries, gross of reinsurance, excl. LAE · no IBNR · synthetic travel insurer</div>

<!--
[TP-01] What was our accident-year 2025 loss ratio? Here are two answers from the same data. Fifty-eight point one percent. And forty-nine point four. Both queries run. Both numbers look fine on a slide. Only one is right. The gap is three rules that every actuary knows. Use earned premium, not written. Subtract recoveries. Remove the test partner. Three rules, nine points. Today I want to show you where those rules should live, so that an AI analyst reads them before it answers. It all runs on a synthetic travel insurer, so you can download it and try it yourself.
-->

---
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

<!--
[TP-02] Now, I expected the AI to fail here. Mostly, it did not. I gave a model only the tables and the data. It worked out that code forty is a recovery. It found the test partner, because the partner list labels it internal. Impressive. Then I asked questions that depend on our decisions. What exactly is attritional? Where is our large-loss threshold? Here, it had to guess. And its guesses looked right. That is the dangerous kind. So here is the idea for today. The AI can read your data. It cannot read your decisions.
-->

---
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

<!--
[TP-03] Think about a brilliant new analyst. They know SQL on day one. What they don't know is us: which premium, which threshold, which partner is fake. So we hand them a binder. A context layer is that binder, kept as plain text files. Nao is an open-source analytics agent built around this idea. One short rule sheet is read with every question. The agent looks up the other pages when it needs them. And because it is files, you can review it, version it, and test it.
-->

---
layout: center
class: text-center
---

<div class="text-7xl mb-6">🎙️</div>

# Claire Gouze · CEO, nao Labs

### Why should data teams become context teams?

---
---

# Step 1 · Scope, then sync

<div class="grid grid-cols-3 gap-6 mt-8 text-center text-xl">
<div class="border-2 rounded-lg p-6"><div class="text-4xl">✅</div><b>In</b><br/>5 clean tables<br/><span class="text-base opacity-70">policies, premium, claims, transactions, partners</span></div>
<div class="border-2 rounded-lg p-6"><div class="text-4xl">🚫</div><b>Out</b><br/>raw feeds, staging<br/><span class="text-base opacity-70">nao suggests ≤ 20 tables to start</span></div>
<div class="border-2 rounded-lg p-6"><div class="text-4xl">🔒</div><b>Locked</b><br/>queries outside the 5<br/>are blocked</div>
</div>

<div class="mt-10 text-xl"><code>nao sync</code> → per table: columns · sample rows · value counts</div>
<div class="mt-3 text-lg">⚠️ Sample rows go to the model: <b>hide personal columns first.</b></div>

<!--
[TP-04] Step one: be boring on purpose. One question your team asks every quarter, and only the clean tables that answer it. Five here. Nao suggests no more than twenty to start. I lock out the raw feeds, so the agent cannot query them even by accident. Then one command, nao sync, writes a short description of every table: the columns, a few sample rows, the value counts. One warning: those sample rows go to the model. On real claims data, hide the personal columns first.
-->

---
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

<!--
[TP-05] Step two: write down what the data means. Next to each table there is a notes file that nao never overwrites. Code ten is a payment, twenty a reserve change, forty a recovery, which reduces the loss. Free-look cancellations earn nothing. The test partner is not real business. Ideally you fix that last one upstream; until then, you write it down. The model guessed some of this right today. Tomorrow it may guess differently. Written down, it is the same answer every time.
-->

---
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
**large loss** ≥ \$5,000 (reporting threshold)<br/>**attritional** = hurricane claims out,<br/>every other claim **capped** at \$5,000<br/>
<span class="opacity-70">owner: reserving actuary</span>

</div>
</div>

<div class="mt-10 text-2xl text-center">Cap: <b>38.2%</b> · Drop instead: <b>32.8%</b> · both defensible, only one is ours</div>

<!--
[TP-06] Step three is the heart of it: our decisions. One definition per metric, with an owner. Loss ratio: incurred, net of recoveries, gross of reinsurance, over gross earned premium, accident-year basis, no IBNR. Then the choices only we can make. A large loss is five thousand dollars or more. Attritional removes the hurricane claims and caps every other claim at five thousand. Another company might drop large claims instead. That gives thirty-two point eight. Ours gives thirty-eight point two. Both are defensible. The AI can read your data. It cannot read your decisions.
-->

---
---

# Step 4 · One short rule sheet

<div class="text-2xl mt-8 leading-12">

- 📍 **Where** each definition lives (point to it, don't copy it)
- 🔁 **Always**: earned premium · no test partner · recoveries reduce losses
- 📅 **"Today"** means the valuation date, 30 September 2026
- ❓ **When the question is unclear, ask.**

</div>

<div class="mt-8 text-xl opacity-80">"What's the loss ratio?" → <i>"For which accident year, and all-in or attritional?"</i></div>

<!--
[TP-07] Step four is a one-page rule sheet. The agent reads it with every question, so it stays short. It points to the definitions instead of copying them. It lists the rules that always apply: earned premium, no test partner. It says that "today" means our valuation date: the end of September. And the most important rule: when the question is unclear, ask. If someone types "what's the loss ratio?", with no year and no basis, a good analyst asks one question back.
-->

---
---

# Step 5 · Write the answer key, then test

<div class="text-base mt-2">

| 9 questions, signed-off answers | tables only | + table notes | + decisions |
|---|:-:|:-:|:-:|
| loss ratio, by region, by coverage, earned, monthly | ✅ | ✅ | ✅ |
| **large losses** (≥ \$5k) | ❌ \$10k | ❌ \$10k | ✅ |
| **attritional loss ratio** | ❌ 39.1% *(dropped ≥ \$10k)* | ❌ 39.1% | ✅ 38.2% |
| frequency (per 1,000) | ⚠️ per policy | ⚠️ per policy | ✅ |
| "What's the loss ratio?" → ask | ✅ / ❌ | ✅ | ✅ |
| **passed** (two runs each) | **6 · 5** | **6 · 6** | **9 · 9** |

</div>

<div class="text-xs opacity-60 mt-1">SIMULATION, not nao output: blind Claude Sonnet analysts, one context level each, graded at 4 decimals by evals/grade.py (mimics nao test). Synthetic data, small n, presenter's own grader. Not a production result.</div>

<!--
[TP-08] Step five: before you trust the agent, write the answer key. Each test is a question in plain English, plus the SQL an actuary signs. Nao runs the agent and compares its numbers with yours. One lesson: my first definitions included sample SQL, and a reviewer caught it. That is giving the answers away, so I removed it. Then I simulated this outside nao, with AI analysts at three levels of context. Tables only: five or six out of nine. Plus table notes: six. Plus our decisions: nine out of nine, twice. Synthetic data, small test, my own grader.
-->

---
layout: center
class: text-center
---

<div class="text-7xl mb-6">🎙️</div>

# Claire Gouze · CEO, nao Labs

### When an answer is wrong: is it the context, the data, the query, or the test?

---
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

<!--
[TP-09] So when a test fails, label it first. Context, data, query, or the test itself. In my runs, every agent without definitions gave Asia's frequency as zero point zero eight. The answer key said eighty-two per thousand. Same number, different unit. Is that a wrong answer, or a vague question? Claire saw the same in her study. Some failures came from badly written tests. But most of her gain came from fixing the data model, not the prompts.
-->

---
---

# All-in 49.4% · attritional 38.2%: what's in the gap?

<div class="grid grid-cols-2 gap-4 mt-2">
<img src="/region.svg" class="h-76 mx-auto" />
<img src="/caribbean_monthly.svg" class="h-76 mx-auto" />
</div>

<div class="mt-2 text-lg">Caribbean AY 2025: <b>100%</b> · trip cancellations: ~13/month → <b>~100/month, Aug–Oct</b> · tagged <code>HU25</code> · <i>pattern planted in the synthetic data</i></div>

<!--
[TP-10] Now let's use it. All-in, forty-nine point four. Attritional, thirty-eight point two. Something big sits in the gap. By region, the Caribbean runs at one hundred percent. The others are between twenty-three and forty-eight. By month, Caribbean trip cancellations go from about thirteen a month to about a hundred, from August to October. The claims team tagged them as the 2025 hurricane season. To be clear: I planted that pattern in the data. The point is how fast you can follow it, with every query visible.
-->

---
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

<!--
[TP-11] Here is where I stop the agent. It found the spike in minutes and showed its work. It cannot decide what the spike means. Is this a one-off event, or a cat exposure we must now price for in the Caribbean? Do we revisit the cruise partner? Those decisions carry your signature. What the context layer does is remember the decision once you make it. The next person who asks gets your answer, not a fresh guess.
-->

---
---

# Corrections become reviewed changes

<div class="grid grid-cols-4 gap-4 mt-14 text-center text-xl">
<div class="border-2 rounded-lg p-5">👎<br/><b>Correction</b><br/><span class="text-base">a user downvotes or fixes an answer</span></div>
<div class="border-2 rounded-lg p-5">📋<br/><b>Suggestion</b><br/><span class="text-base">nao ranks the gap and shows the chats behind it</span></div>
<div class="border-2 rounded-lg p-5">✅<br/><b>Reviewed change</b><br/><span class="text-base">a pull request the owner approves</span></div>
<div class="border-2 rounded-lg p-5">🧪<br/><b>New test</b><br/><span class="text-base">so it never comes back</span></div>
</div>

<div class="mt-10 text-xl">Automatic mode opens the changes without review. <b>For actuarial definitions: off.</b></div>

<!--
[TP-12] Context goes stale the day you ship it. Nao has a feedback loop for that. On a schedule, it reviews real usage: errors, thumbs down, corrections. It ranks where the context is missing or wrong, and shows the conversations behind each suggestion. It can open the change as a pull request: a proposed edit that someone must approve. There is a mode that opens those requests automatically, with no one reviewing the suggestion first. For actuarial definitions, I would leave it off.
-->

---
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

<!--
[TP-13] We already do this for reserving models. Someone owns the assumption, someone reviews the change, and there is evidence it still works. Do the same for the words the AI reads. In this repository, the reserving actuary approves any change to the loss ratio definition, and pricing owns frequency. Every proposed change re-checks the answer key automatically, and the full agent test runs on a schedule. If nobody owns a definition, the agent will happily invent one.
-->

---
layout: center
class: text-center
---

<div class="text-7xl mb-6">🎙️</div>

# Claire Gouze · CEO, nao Labs

### Who should own the context, and how do you know it's getting better?

---
---

# Monday morning

<div class="text-3xl mt-10 leading-16">

1. **One question** your team argues about
2. **Write it down**: meaning + decisions + owner
3. **Write the answer key**: the SQL you would sign
4. **Test the agent** before anyone else uses it

</div>

<div class="mt-8 text-xl opacity-80">Start with one question, and earn the next nineteen.</div>

<!--
[TP-14] If you want to start on Monday, do four things. One: choose one question your team argues about. Two: write down what it means and what you decided, in plain words, with an owner. Three: write the answer key, the SQL you would sign. Four: test the agent against it, before anyone else uses it. Nao suggests twenty tables and twenty questions. I would start with one question, and earn the next nineteen.
-->

---
layout: center
class: text-center
---

# The model is fast.<br/>Your definitions make it right.

<img src="/qr.svg" class="mx-auto h-40 mt-8" />

<div class="mt-4 text-xl"><code>github.com/StephaneFurderer/nao-context-layer-actuaries</code></div>
<div class="mt-2 opacity-70">Synthetic data · run it · break it · tell me what you find</div>

<!--
[TP-15] Let me finish where I started. Same question, two answers, nine points apart. The models are already fast, and they are good at SQL. They will get better. But on their own, they will never know which premium you use, which partner is fake, or where you cap a large loss. That is your knowledge. Today it lives in people's heads. A context layer writes it down, gives it an owner, and tests it. So, if you remember one line: the model is fast. Your definitions make it right. Everything is in the repository. Run it, break it, and tell me what you find.
-->
