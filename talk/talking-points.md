# Talking points: Building the context layer (demo segment)

Session: *From Actuarial Knowledge to Trusted AI Analytics: Building the Context Layer*, Actuarial Technology Summit, December 15, 2026.

Each point is ≤ 60 seconds. `python talk/check_talk.py` enforces this at 130 wpm, adding the stated demo time. Every number traces to a file in this repo; every outside claim traces to `sources/source-bank.md`.

Field legend:
- **Doing**: what the audience should understand we are doing
- **Say**: the script
- **Show**: slide or screen
- **Demo**: seconds of silent screen time
- **Proof**: repo evidence
- **Sources**: source-bank ids

The interview clips with Claire Gouze slot in where marked. The clip timings are placeholders: cut them from the 20-minute recording.

---

## Act 1: Why the context layer

### TP-01 — Same question, two answers
**Doing:** Open with one actuarial question whose two runnable answers differ by nine points.
**Say:** What was our 2025 loss ratio? I asked that of a synthetic travel insurer I built for this talk, and I got two answers. 58.9 percent, and 49.9 percent. Both come from SQL that runs. Both look reasonable on a slide. The gap is three sentences that every actuary in this room knows: use earned premium, subtract recoveries, ignore the test partner. Today is about where those three sentences live, and how an AI analyst finds them before it answers.
**Show:** Slide 2: the waterfall from 58.9% to 49.9%.
**Proof:** `sql/waterfall_2025.sql`, `sql/reference_loss_ratio_2025.sql`
**Sources:** R1

### TP-02 — The model is not the problem
**Doing:** Show that frontier models already write good SQL, so the gap is conventions, not capability.
**Say:** I expected an AI to get this wrong. It didn't, mostly. I gave a model only the schema and the data. It worked out that code 40 is a recovery, because reserves net to zero and recoveries don't. It spotted the test partner from the round 9,999.99 claims. That's impressive. But on the questions that depend on *our* conventions (what we call a large loss, what attritional means, frequency per thousand), it guessed. And a guess that looks right is the dangerous kind.
**Show:** Slide 3: the pass rate grid for schema only vs. full context.
**Proof:** `evals/blind-agent-results.md`
**Sources:** R3, C2

### TP-03 — What a context layer is
**Doing:** Define a context layer as the onboarding pack for a new analyst, stored as files.
**Say:** Think about onboarding a brilliant new analyst. They know SQL on day one. What they don't know is us: which premium to use, what a large loss is, which partner is fake. So we hand them a binder. A context layer is that binder, kept as plain files in git, and the AI reads the relevant pages before every answer. Nao is an open-source analytics agent built around exactly that idea: the context is a folder you can read, review and test.
**Show:** Slide 4: the binder analogy, then the nao folder tree.
**Proof:** `context/RULES.md`, `context/nao_config.yaml`
**Sources:** A2, B5, H2

> **CLIP A** (Claire: why data teams should become context teams) 3 min

---

## Act 2: Build it, step by step

### TP-04 — The sandbox
**Doing:** Introduce the synthetic travel-insurance warehouse everyone can download and rerun.
**Say:** Everything you'll see runs on synthetic data, so I can share all of it. It's a travel insurer: sixty thousand policies, about four thousand claims, sold through airlines, an online travel agency, a cruise line and direct. Like a real legacy system, transactions carry codes, not words: 10 is a payment, 20 a reserve change, 40 a recovery. It's valued at September 30, 2026. One command regenerates it, and the repo link is on the last slide.
**Show:** Slide 5: the five mart tables and their row counts.
**Proof:** `data/generate.py`, `README.md`
**Sources:** R1

### TP-05 — Step 1: scope one question
**Doing:** Choose a bounded question and give the agent only the five clean tables it needs.
**Say:** Step one is to be boring on purpose. Pick one question your team asks every quarter: the accident-year loss ratio. Give the agent only the clean mart tables that answer it, five here. Nao's own playbook says to start with no more than twenty. In the config I include the mart schema, exclude staging, and set allow-listed-only, so the agent can't query a raw feed even if it wanted to.
**Show:** Slide 6: `nao_config.yaml` with include, exclude and allow_listed_only highlighted.
**Proof:** `context/nao_config.yaml`
**Sources:** A3, A6, B4

### TP-06 — Step 2: sync what the machine can see
**Doing:** Run nao sync to generate per-table schema, previews and profiling as markdown files.
**Say:** Step two is one command: nao sync. For every table it writes three markdown files: the columns, a few sample rows, and a profile of the values. This is what any agent sees out of the box. Notice what it says about code 40: nothing. It's a string with three values. The machine has the structure. It doesn't have the meaning.
**Show:** Terminal: `nao sync`, then open `claim_transactions/profiling.md`.
**Demo:** 12s
**Proof:** `context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/profiling.md`
**Sources:** A1, A3

### TP-07 — Step 3: annotate the tables
**Doing:** Write each table's grain, codes and pitfalls into annotation files owned by an actuary.
**Say:** Step three is where actuaries come in. Next to each table, nao keeps an annotations file, plain markdown, that sync never overwrites. Here I write what each code means, the grain, and the pitfalls. Recoveries are stored positive but reduce the loss. Free-look cancellations earn nothing. ZZTEST is test data. Each line is something you'd tell a new hire in their first week. Now it's written down once, and the reserving actuary owns it.
**Show:** Slide 8: `claim_transactions/annotations.md`, with the recovery line highlighted.
**Proof:** `context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/annotations.md`, `CODEOWNERS`
**Sources:** A3, A4

### TP-08 — Step 4: define each metric once
**Doing:** Write one canonical, owned definition per metric, including our company conventions.
**Say:** Step four: define each metric once. The loss ratio file says net incurred over earned premium, accident-year basis, valued September 30, no IBNR. A second file holds decisions only we can make. A large loss is ten thousand dollars or more, our per-risk retention. Attritional means cat claims out and every other claim capped at ten thousand. Nao's docs are blunt here: two definitions of the same metric are the most common cause of inconsistent answers.
**Show:** Slide 9: `semantics/loss_ratio.md` and `semantics/large_and_cat_losses.md`, side by side.
**Proof:** `context/semantics/loss_ratio.md`, `context/semantics/large_and_cat_losses.md`
**Sources:** A4, A5

### TP-09 — Step 5: a lean RULES file as a router
**Doing:** Keep RULES.md short: route to definitions, state the always-rules, and say when to ask.
**Say:** Step five is the rules file. It's loaded with every single message, so it stays short. It does three jobs. It routes: for a loss ratio, read this file. It states the always-rules: exclude the test partner, use earned premium. And it says when to ask: if someone says "the loss ratio" with no year or basis, the agent should ask one question instead of picking one. That last rule is how you get an analyst who knows what it doesn't know.
**Show:** Slide 10: `RULES.md`, about thirty lines.
**Proof:** `context/RULES.md`
**Sources:** A4

> **CLIP B** (Claire: how to tell a context problem from a data, model or query problem) 3 min

### TP-10 — Step 6: write the reference answers first
**Doing:** Turn each question into a test: the prompt plus the SQL an actuary signs off.
**Say:** Step six is the one I'd keep if you forget everything else. Before you trust the agent, write the answer key. A nao test is a small YAML file: the question in plain English and the SQL the actuary signs off. Nao runs the agent, takes its final numbers, and compares them with your reference. I wrote nine, including one where the right behaviour is to ask a question back. One warning from the docs: never paste the answers into the context, or you're testing memory.
**Show:** Slide 11: `tests/attritional_loss_ratio_ay2025.yml`.
**Proof:** `context/tests/attritional_loss_ratio_ay2025.yml`, `context/tests/ambiguous_loss_ratio.yml`
**Sources:** A7

### TP-11 — Step 7: run the tests, read the grid
**Doing:** Show the pass rate rising with each context layer, measured against the reference answers.
**Say:** Then you run nao test, and you get a grid. I ran the same nine questions with blind AI analysts at three levels of context: schema only, plus annotations, plus definitions. Schema only passed six or seven of nine. With the full context, nine of nine, on both runs. The misses were all conventions. Attritional caps large claims; the blind agents dropped them, and got 39.3 instead of 41.6. Frequency is per thousand. And one agent answered when it should have asked. To be clear: this used my own grader on synthetic data, not a production claim.
**Show:** Slide 12: the pass/fail grid by context level.
**Proof:** `evals/blind-agent-results.md`, `evals/grade.py`
**Sources:** R3, A7

### TP-12 — Diagnose before you fix
**Doing:** Classify each failure as context, data, query or test before changing anything.
**Say:** A failing test doesn't automatically mean missing context. In my second run, the best-informed agent failed the Caribbean monthly question. Its numbers were right; it returned the month as a number and my reference returned a date. That was my test's fault, so I fixed the test, not the context. Claire found the same in her own study: part of the gain came from fixing ambiguous tests. So label every failure first: context, data, query, or test.
**Show:** Slide 13: four failure buckets with the real example.
**Proof:** `evals/run2-coded/results.json`, `context/tests/caribbean_cancellation_claims_by_month_2025.yml`
**Sources:** B3, A7

---

## Act 3: Use it, and keep it true

### TP-13 — The investigation
**Doing:** Use the tested context to follow a real deterioration from the portfolio down to its cause.
**Say:** Now the fun part. The all-in loss ratio is 49.9 percent, but attritional is 41.6. Something big sits in the gap. By region, the Caribbean runs at 95.7 percent; everyone else is between 35 and 51. By loss month, Caribbean trip cancellations jump from about twenty a month to a hundred in August, and stay high through October. It's hurricane season, already tagged HU25 by the claims team. Every step shows its SQL.
**Show:** Live in nao chat, or recorded backup: three questions, three charts.
**Demo:** 15s
**Proof:** `context/tests/loss_ratio_by_region_ay2025.yml`, `context/tests/caribbean_cancellation_claims_by_month_2025.yml`, `context/tests/attritional_loss_ratio_ay2025.yml`
**Sources:** R4

### TP-14 — Judgement stays with the actuary
**Doing:** Separate what the agent found from what an actuary must decide.
**Say:** Here's where I stop the agent. It found the spike in minutes and showed its work. It can't decide what the spike means. Is HU25 a one-off cat we load for, or a trend we should price into Caribbean trips? Do we revisit the cruise partner? Those are judgements with your name on them. What the context layer does is remember the decision once you make it, so the next person who asks gets your answer, not a fresh guess.
**Show:** Slide 15: "found by the agent" vs. "decided by the actuary".
**Proof:** `context/semantics/large_and_cat_losses.md`
**Sources:** H2, H1

### TP-15 — Close the loop: corrections become pull requests
**Doing:** Show how a user's correction becomes a reviewed change to the shared context.
**Say:** Context goes stale the day you ship it. Nao's answer is a feedback loop. It audits real usage on a schedule, including errors, downvotes and corrections, and ranks where the context is missing or wrong. Each recommendation shows the chats behind it and can open a pull request against the context repo. A human reviews it, merges it, and adds a test so it never regresses. There's an auto-merge mode. For actuarial definitions, I'd leave it off.
**Show:** Slide 16: correction → recommendation → pull request → review → new test.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`
**Sources:** A8, A9, H3

### TP-16 — Ownership is the real deliverable
**Doing:** Assign a named owner and a test to every definition, enforced on every change.
**Say:** The technology is the easy part. The real deliverable is ownership. In this repo, a CODEOWNERS file says the reserving actuary approves any change to the loss ratio definition, and pricing owns frequency. Every pull request reruns the reference questions. That's the same governance we already apply to reserving models, applied to the words the AI reads. If nobody owns a definition, the agent will happily invent one.
**Show:** Slide 17: `CODEOWNERS` and the CI check on a pull request.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`
**Sources:** A6, B1

> **CLIP C** (Claire: who should own context, and what evidence shows it is improving) 3 min

---

## Close

### TP-17 — What to do on Monday
**Doing:** Give the audience a four-step starting checklist they can apply this week.
**Say:** If you want to start on Monday, do four things. One: choose one bounded question your team argues about. Two: write down what it means, in plain words, with an owner. Three: write the reference answer, the SQL you would sign. Four: test the agent against it before anyone else uses it. Nao suggests twenty tables and twenty questions. I'd start with one question and earn the next nineteen.
**Show:** Slide 18: the four-step checklist.
**Proof:** `talk/talking-points.md`, `context/tests/loss_ratio_ay2025.yml`
**Sources:** A6, B4

### TP-18 — Close
**Doing:** Restate the core idea and point to the open repository.
**Say:** The models are already fast, and they're getting very good at SQL. What they will never have on their own is your institutional knowledge: which premium, which partner, which threshold, which year. A context layer is how that knowledge stops living in people's heads and starts being written, owned and tested. Everything I showed you is in this repository, on synthetic data. Rerun it, break it, and tell me what you find. Thank you.
**Show:** Slide 19: the repo link and QR code.
**Proof:** `README.md`
**Sources:** R1, R3
