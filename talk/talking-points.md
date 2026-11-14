# Talking points: Building the context layer (demo segment, v2)

Session: *From Actuarial Knowledge to Trusted AI Analytics: Building the Context Layer*. Actuarial Technology Summit, December 15, 2026, prerecorded.

Each point fits in 60 seconds or less. `python3 talk/check_talk.py` enforces this, counting numbers as they are spoken, at 120 wpm, plus any stated demo time. The segment budget is 12 minutes, excluding the interview clips. Every number is asserted by `make check-sql`; every outside claim traces to `sources/source-bank.md`.

Fields:
- **Doing**: what the audience should understand
- **Say**: the script
- **Show**: what is on screen
- **Demo**: seconds of screen time without speech
- **Proof**: repo evidence
- **Sources**: source-bank ids

The through-line, said at TP-02 and again at TP-06: *"The AI can read your data. It cannot read your decisions."*
The closing line, said aloud at TP-15: *"The model is fast. Your definitions make it right."*

v2 changes after the review round are listed in `reviews/README.md`.

---

## Act 1: Why

### TP-01 — Same question, two answers
**Doing:** Open with one actuarial question whose two runnable answers differ by nine points.
**Say:** What was our accident-year 2025 loss ratio? Here are two answers from the same data. Fifty-eight point one percent. And forty-nine point four. Both queries run. Both numbers look fine on a slide. Only one is right. The gap is three rules that every actuary knows. Use earned premium, not written. Subtract recoveries. Remove the test partner. Three rules, nine points. Today I want to show you where those rules should live, so that an AI analyst reads them before it answers. It all runs on a synthetic travel insurer, so you can download it and try it yourself.
**Show:** "Two answers" slide: 58.1% and 49.4%, then the three rules.
**Proof:** `sql/waterfall_2025.sql`, `sql/naive_loss_ratio_2025.sql`, `evals/check_reference_sql.py`
**Sources:** R1

### TP-02 — The AI can read your data
**Doing:** Show that the model handles the data well, so the real gap is our decisions.
**Say:** Now, I expected the AI to fail here. Mostly, it did not. I gave a model only the tables and the data. It worked out that code forty is a recovery. It found the test partner, because the partner list labels it internal. Impressive. Then I asked questions that depend on our decisions. What exactly is attritional? Where is our large-loss threshold? Here, it had to guess. And its guesses looked right. That is the dangerous kind. So here is the idea for today. The AI can read your data. It cannot read your decisions.
**Show:** "Read vs decide" slide: what it inferred on the left, what it had to guess on the right, with the through-line as a banner.
**Proof:** `evals/blind-agent-results.md`
**Sources:** R3, C2

### TP-03 — A context layer is the new analyst's binder
**Doing:** Define a context layer as the onboarding pack for a new analyst, kept as files.
**Say:** Think about a brilliant new analyst. They know SQL on day one. What they don't know is us: which premium, which threshold, which partner is fake. So we hand them a binder. A context layer is that binder, kept as plain text files. Nao is an open-source analytics agent built around this idea. One short rule sheet is read with every question. The agent looks up the other pages when it needs them. And because it is files, you can review it, version it, and test it.
**Show:** The binder slide, then the nao project folder.
**Proof:** `context/RULES.md`, `context/nao_config.yaml`
**Sources:** A2, A4, B5, H2

> **CLIP A** (Claire: why data teams should become context teams) 3 min

---

## Act 2: Build it in five steps

### TP-04 — Step 1: scope, then sync
**Doing:** Give the agent five clean tables, lock out raw feeds, and let nao describe them.
**Say:** Step one: be boring on purpose. One question your team asks every quarter, and only the clean tables that answer it. Five here. Nao suggests no more than twenty to start. I lock out the raw feeds, so the agent cannot query them even by accident. Then one command, nao sync, writes a short description of every table: the columns, a few sample rows, the value counts. One warning: those sample rows go to the model. On real claims data, hide the personal columns first.
**Show:** Scope card (in / out / locked), then the terminal running `nao sync`.
**Demo:** 6s
**Proof:** `context/nao_config.yaml`, `context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/profiling.md`
**Sources:** A3, A6, B4

### TP-05 — Step 2: write down what the data means
**Doing:** Annotate each table with its grain, codes and pitfalls, so answers are repeatable rather than guessed.
**Say:** Step two: write down what the data means. Next to each table there is a notes file that nao never overwrites. Code ten is a payment, twenty a reserve change, forty a recovery, which reduces the loss. Free-look cancellations earn nothing. The test partner is not real business. Ideally you fix that last one upstream; until then, you write it down. The model guessed some of this right today. Tomorrow it may guess differently. Written down, it is the same answer every time.
**Show:** The claim_transactions notes as a card, with the recovery line highlighted.
**Proof:** `context/databases/type=duckdb/database=travel/schema=mart/table=claim_transactions/annotations.md`, `CODEOWNERS`
**Sources:** A3, B3

### TP-06 — Step 3: write down your decisions
**Doing:** Write one owned definition per metric, including conventions only the company can decide.
**Say:** Step three is the heart of it: our decisions. One definition per metric, with an owner. Loss ratio: incurred, net of recoveries, gross of reinsurance, over gross earned premium, accident-year basis, no IBNR. Then the choices only we can make. A large loss is five thousand dollars or more. Attritional removes the hurricane claims and caps every other claim at five thousand. Another company might drop large claims instead. That gives thirty-two point eight. Ours gives thirty-eight point two. Both are defensible. The AI can read your data. It cannot read your decisions.
**Show:** Two definition cards side by side, then the 38.2% vs 32.8% callout.
**Proof:** `context/semantics/loss_ratio.md`, `context/semantics/large_and_cat_losses.md`, `sql/attritional_dropped_variant_2025.sql`
**Sources:** A4, A5

### TP-07 — Step 4: the rule sheet, and when to ask
**Doing:** Keep one short rule sheet: where definitions live, what always applies, and when to ask.
**Say:** Step four is a one-page rule sheet. The agent reads it with every question, so it stays short. It points to the definitions instead of copying them. It lists the rules that always apply: earned premium, no test partner. It says that "today" means our valuation date: the end of September. And the most important rule: when the question is unclear, ask. If someone types "what's the loss ratio?", with no year and no basis, a good analyst asks one question back.
**Show:** The rule sheet as five plain-language bullets, with "When unclear, ask" in bold.
**Proof:** `context/RULES.md`
**Sources:** A4

### TP-08 — Step 5: write the answer key, then test
**Doing:** Turn each question into a test with signed-off SQL, then compare agents with and without context.
**Say:** Step five: before you trust the agent, write the answer key. Each test is a question in plain English, plus the SQL an actuary signs. Nao runs the agent and compares its numbers with yours. One lesson: my first definitions included sample SQL, and a reviewer caught it. That is giving the answers away, so I removed it. Then I simulated this outside nao, with AI analysts at three levels of context. Tables only: five or six out of nine. Plus table notes: six. Plus our decisions: nine out of nine, twice. Synthetic data, small test, my own grader.
**Show:** The results grid (three levels, with the attritional and large-loss rows highlighted).
**Proof:** `context/tests/attritional_loss_ratio_ay2025.yml`, `evals/blind-agent-results.md`, `evals/grade.py`
**Sources:** A7, R2, R3

> **CLIP B** (Claire: when an answer is wrong, is it the context, the data, the query or the test?) 3 min

### TP-09 — Diagnose before you fix
**Doing:** Label each failure as context, data, query or test before changing anything.
**Say:** So when a test fails, label it first. Context, data, query, or the test itself. In my runs, every agent without definitions gave Asia's frequency as zero point zero eight. The answer key said eighty-two per thousand. Same number, different unit. Is that a wrong answer, or a vague question? Claire saw the same in her study. Some failures came from badly written tests. But most of her gain came from fixing the data model, not the prompts.
**Show:** Four buckets: Context, Data, Query, Test.
**Proof:** `evals/blind-agent-results.md`, `evals/grade.py`
**Sources:** B3, A7

---

## Act 3: Use it, and keep it true

### TP-10 — The investigation
**Doing:** Follow the deterioration from portfolio to cause with the tested context, step by step.
**Say:** Now let's use it. All-in, forty-nine point four. Attritional, thirty-eight point two. Something big sits in the gap. By region, the Caribbean runs at one hundred percent. The others are between twenty-three and forty-eight. By month, Caribbean trip cancellations go from about thirteen a month to about a hundred, from August to October. The claims team tagged them as the 2025 hurricane season. To be clear: I planted that pattern in the data. The point is how fast you can follow it, with every query visible.
**Show:** nao chat recording with jump-cuts: three questions, three charts.
**Demo:** 12s
**Proof:** `context/tests/loss_ratio_by_region_ay2025.yml`, `context/tests/caribbean_cancellation_claims_by_month_2025.yml`, `slides/charts.py`
**Sources:** R4

### TP-11 — Judgement stays with the actuary
**Doing:** Separate what the agent found from what an actuary must decide and record.
**Say:** Here is where I stop the agent. It found the spike in minutes and showed its work. It cannot decide what the spike means. Is this a one-off event, or a cat exposure we must now price for in the Caribbean? Do we revisit the cruise partner? Those decisions carry your signature. What the context layer does is remember the decision once you make it. The next person who asks gets your answer, not a fresh guess.
**Show:** Two columns: "Found by the agent" and "Decided by you".
**Proof:** `context/semantics/large_and_cat_losses.md`
**Sources:** H2, H1

### TP-12 — Corrections become reviewed changes
**Doing:** Show how a user's correction becomes a reviewed, tested change to the shared context.
**Say:** Context goes stale the day you ship it. Nao has a feedback loop for that. On a schedule, it reviews real usage: errors, thumbs down, corrections. It ranks where the context is missing or wrong, and shows the conversations behind each suggestion. It can open the change as a pull request: a proposed edit that someone must approve. There is a mode that opens those requests automatically, with no one reviewing the suggestion first. For actuarial definitions, I would leave it off.
**Show:** Four boxes: correction → suggestion → reviewed change → new test.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`
**Sources:** A8, A9, H3

### TP-13 — Ownership is the real deliverable
**Doing:** Give every definition a named owner and an automatic check, like any actuarial model.
**Say:** We already do this for reserving models. Someone owns the assumption, someone reviews the change, and there is evidence it still works. Do the same for the words the AI reads. In this repository, the reserving actuary approves any change to the loss ratio definition, and pricing owns frequency. Every proposed change re-checks the answer key automatically, and the full agent test runs on a schedule. If nobody owns a definition, the agent will happily invent one.
**Show:** Owner table: definition → owner → check.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`, `evals/check_reference_sql.py`
**Sources:** A6, B1, C6

> **CLIP C** (Claire: who should own context, and what shows it is getting better) 3 min

---

## Close

### TP-14 — What to do on Monday
**Doing:** Give a four-step starting checklist the audience can apply this week.
**Say:** If you want to start on Monday, do four things. One: choose one question your team argues about. Two: write down what it means and what you decided, in plain words, with an owner. Three: write the answer key, the SQL you would sign. Four: test the agent against it, before anyone else uses it. Nao suggests twenty tables and twenty questions. I would start with one question, and earn the next nineteen.
**Show:** The four-step checklist.
**Proof:** `context/tests/loss_ratio_ay2025.yml`, `README.md`
**Sources:** A6, B4

### TP-15 — Close
**Doing:** Call back to the opening, say the closing line, and point to the repository.
**Say:** Let me finish where I started. Same question, two answers, nine points apart. The models are already fast, and they are good at SQL. They will get better. But on their own, they will never know which premium you use, which partner is fake, or where you cap a large loss. That is your knowledge. Today it lives in people's heads. A context layer writes it down, gives it an owner, and tests it. So, if you remember one line: the model is fast. Your definitions make it right. Everything is in the repository. Run it, break it, and tell me what you find.
**Show:** Closing line, repo link and QR code.
**Proof:** `README.md`, `slides/public/qr.svg`
**Sources:** R1, R3
