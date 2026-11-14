# Talking points: Building the context layer (demo segment, v3)

Session: *From Actuarial Knowledge to Trusted AI Analytics: Building the Context Layer*. Actuarial Technology Summit, December 15, 2026, prerecorded.

Each point fits in 60 seconds or less. `python3 talk/check_talk.py` enforces this, counting numbers as they are spoken, at 120 wpm, plus any stated demo time. The segment runs about 14.4 minutes (budget 15.5), excluding the interview clips. Every number is asserted by `make check-sql`; every outside claim traces to `sources/source-bank.md`.

Fields:
- **Doing**: what the audience should understand
- **Say**: the script
- **Show**: what is on screen
- **Demo**: seconds of screen time without speech
- **Proof**: repo evidence
- **Sources**: source-bank ids

The through-line, said at TP-02 and again at TP-06: *"The AI can read your data. It cannot read your decisions."*
The closing line, said aloud at TP-19: *"The model is fast. Your definitions make it right."*

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

## Act 2b: When an answer is wrong (failure deep-dive)

Full detail and the validation checklist: `docs/failure-points-and-validation.md`.

### TP-09 — When it fails: five suspects
**Doing:** Name the five places a wrong answer can come from, and the three facts you need first.
**Say:** So what happens when an answer is wrong? Last week I wrote that there are three suspects: the knowledge, the runtime, and the checks. Building this demo, I found two more: the data, and the test itself. Before you fix anything, you need three facts. Which version of the knowledge was official? What did the agent actually see? Which check ran? Git gives you the version. Nao's chat replay shows the SQL and the files behind every answer. The test results show the checks. Let's take the suspects one by one.
**Show:** Five suspects, plus the three audit questions.
**Proof:** `docs/failure-points-and-validation.md`
**Sources:** D1, A8, A7

### TP-10 — Suspect 1: the knowledge was wrong
**Doing:** Show a wrong definition producing a plausible wrong number, and who fixes it.
**Say:** Suspect one: the knowledge itself is wrong. Imagine someone writes "written premium" in the loss ratio definition. The answer becomes forty-seven point eight instead of forty-nine point four. Nothing breaks. It looks reasonable. It is like a GPS with an old map: confident, and wrong. The fix belongs to the owner of that definition. Change the file, date the change, and run the answer key on the draft before you approve it. Nao now records an owner on each context file, and can test a draft against the current version.
**Show:** The definition card with "written" crossed out, then 47.8% vs 49.4%.
**Proof:** `sql/failures/f1_knowledge_wrong_written_premium.sql`, `context/semantics/loss_ratio.md`
**Sources:** D1, D2, N1, N2

### TP-11 — Suspect 2: the data was wrong
**Doing:** Show the right definition applied to the wrong rows or the wrong clock.
**Say:** Suspect two: the right definition, on the wrong data. Leave the test partner in, and the loss ratio jumps to fifty-four point nine. Or ask for "the last twelve months", and let the agent count from today, the fourteenth of November. Our data stops at the end of September, so the window quietly loses seventeen percent of its premium. The SQL runs. The number is wrong. The real fix belongs upstream, with the data owner. Until then: lock the tables, and write down which clock to use.
**Show:** 54.9% (test partner in), then the two clocks: today vs the valuation date.
**Proof:** `sql/failures/f2_wrong_data_test_partner.sql`, `sql/failures/f2b_wrong_data_today_not_valuation.sql`, `context/RULES.md`
**Sources:** D3, A3

### TP-12 — Suspect 3: the agent never saw it
**Doing:** Show correct knowledge that never reached the agent, and who fixes the delivery.
**Say:** Suspect three: the knowledge was right, but the agent never saw it. In my test, one group of agents had table notes that pointed to the definitions file. But the file was not in their folder. So they guessed: a ten thousand dollar threshold, and they dropped the large claims. Thirty-nine point one instead of thirty-eight point two. It is like a student who studied the wrong chapter. The fix belongs to whoever runs the system: route to the right file, keep files short, and check that permissions don't hide a definition.
**Show:** The routing map: RULES.md → semantics file, with one broken link.
**Proof:** `evals/run4/L1a/notes.md`, `context/RULES.md`
**Sources:** D1, D6, A8

### TP-13 — Suspects 4 and 5: used it wrong, or the test was wrong
**Doing:** Show silent misuse caught only by checks, and a failure caused by the answer key itself.
**Say:** Suspect four: the agent saw the rule, used it wrong, and nobody noticed. One agent answered "what's the loss ratio?" without asking which year. Others gave frequency per policy, not per thousand. Right numbers, wrong problem. The fix is checks: an answer key, and each question run three times, because one lucky answer is not reliability. Suspect five: the test itself. One agent failed only because my answer key expected a date and got a month number. I fixed the test, not the context.
**Show:** Two cards: "used it wrong → checks" and "the test was wrong → fix the test".
**Proof:** `evals/run4/L0b/ambiguous_loss_ratio.txt`, `evals/run2-coded/results.json`
**Sources:** A7, D7, B3

---

## Act 3: Use it, and keep it true

### TP-14 — The investigation
**Doing:** Follow the deterioration from portfolio to cause with the tested context, step by step.
**Say:** Now let's use it. All-in, forty-nine point four. Attritional, thirty-eight point two. Something big sits in the gap. By region, the Caribbean runs at one hundred percent. The others are between twenty-three and forty-eight. By month, Caribbean trip cancellations go from about thirteen a month to about a hundred, from August to October. The claims team tagged them as the 2025 hurricane season. To be clear: I planted that pattern in the data. The point is how fast you can follow it, with every query visible.
**Show:** nao chat recording with jump-cuts: three questions, three charts.
**Demo:** 12s
**Proof:** `context/tests/loss_ratio_by_region_ay2025.yml`, `context/tests/caribbean_cancellation_claims_by_month_2025.yml`, `slides/charts.py`
**Sources:** R4

### TP-15 — Judgement stays with the actuary
**Doing:** Separate what the agent found from what an actuary must decide and record.
**Say:** Here is where I stop the agent. It found the spike in minutes and showed its work. It cannot decide what the spike means. Is this a one-off event, or a cat exposure we must now price for in the Caribbean? Do we revisit the cruise partner? Those decisions carry your signature. Once you decide, write it into the context, and certify the analysis so others reuse the approved version. The next person who asks gets your answer, not a fresh guess.
**Show:** Two columns: "Found by the agent" and "Decided by you".
**Proof:** `context/semantics/large_and_cat_losses.md`
**Sources:** H2, H1

### TP-16 — Corrections become reviewed changes
**Doing:** Show how a user's correction becomes a reviewed, tested change to the shared context.
**Say:** Context goes stale the day you ship it. Nao has a feedback loop for that. On a schedule, it reviews real usage: errors, thumbs down, corrections. It ranks where the context is missing or wrong, and shows the conversations behind each suggestion. It can open the change as a pull request: a proposed edit that someone must approve. There is a mode that opens those requests automatically, with no one reviewing the suggestion first. For actuarial definitions, I would leave it off.
**Show:** Four boxes: correction → suggestion → reviewed change → new test.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`
**Sources:** A8, A9, H3

### TP-17 — Ownership is the real deliverable
**Doing:** Give every definition a named owner and an automatic check, like any actuarial model.
**Say:** We already do this for reserving models. Someone owns the assumption, someone reviews the change, and there is evidence it still works. Do the same for the words the AI reads. In this repository, the reserving actuary approves any change to the loss ratio definition, and pricing owns frequency. Nao now records those owners on the files, and on the tests. Every proposed change re-checks the answer key automatically, and the full agent test runs on a schedule. If nobody owns a definition, the agent will happily invent one.
**Show:** Owner table: definition → owner → check.
**Proof:** `CODEOWNERS`, `.github/workflows/context-tests.yml`, `evals/check_reference_sql.py`
**Sources:** A6, B1, C6

> **CLIP C** (Claire: who should own context, and what shows it is getting better) 3 min

---

## Close

### TP-18 — What to do on Monday
**Doing:** Give a four-step starting checklist the audience can apply this week.
**Say:** If you want to start on Monday, do four things. One: choose one question your team argues about. Two: write down what it means and what you decided, in plain words, with an owner. Three: write the answer key, the SQL you would sign. Four: test the agent against it, before anyone else uses it. Nao suggests twenty tables and twenty questions. I would start with one question, and earn the next nineteen.
**Show:** The four-step checklist.
**Proof:** `context/tests/loss_ratio_ay2025.yml`, `README.md`
**Sources:** A6, B4

### TP-19 — Close
**Doing:** Call back to the opening, say the closing line, and point to the repository.
**Say:** Let me finish where I started. Same question, two answers, nine points apart. The models are already fast, and they are good at SQL. They will get better. But on their own, they will never know which premium you use, which partner is fake, or where you cap a large loss. That is your knowledge. Today it lives in people's heads. A context layer writes it down, gives it an owner, and tests it. So, if you remember one line: the model is fast. Your definitions make it right. Everything is in the repository. Run it, break it, and tell me what you find.
**Show:** Closing line, repo link and QR code.
**Proof:** `README.md`, `slides/public/qr.svg`
**Sources:** R1, R3
