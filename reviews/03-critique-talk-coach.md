# Talk-coach review: "Building the context layer" demo segment

Reviewer stance: TED-style speaker coach plus technical-demo producer. Audience: actuaries, mostly not engineers, some sceptical of AI. Format: prerecorded, about 11 min of Stéphane interleaved with 3 x 3 min clips of Claire Gouze.

Material read: `talk/talking-points.md`, `slides/slides.md`, all 22 rendered PNGs, `evals/blind-agent-results.md`, `README.md`, `talk/check_talk.py` (validator passes: 11.1 min plus 9 min of clips = 20.1 min), `sources/source-bank.md` (to check claims).

---

## 0. Verdict in one paragraph

The content is honest, well sourced and has a real insight: models infer facts from data but cannot infer your decisions. The hook (58.9 vs 49.9) is strong and the close is strong. Three things hold it back. (1) Act 2 is nine talking points of "a file on a slide", seven of them numbered steps, mostly shown as raw YAML, Markdown, SQL or CODEOWNERS text that an actuary cannot read in 5 seconds. Three of these slides physically overflow the right edge. (2) The story contradicts itself: TP-02 says the model worked out code 40, then TP-06 and TP-07 say "the machine doesn't know what code 40 is" and use it as the reason to annotate. A sceptic will notice. (3) The best line ("The model is fast. Your definitions make it right.") is on the last slide but is never said aloud, and nothing is repeated, so nothing sticks. Also: this is the "nao demo", but the audience does not see nao's own UI until TP-13, minute ~17 of the session.

---

## 1. Talking points, one by one

Timing note. The validator counts "58.9" or "9,999.99" as one word. Spoken, those are 4 to 8 words. Re-estimating with numbers spoken out, at 130 wpm everything still fits in 60 s, but TP-13 lands at about 53 s and TP-11 at about 48 s. At a more realistic 115 wpm for a second-language speaker with pauses after punchlines, the total is about 12.5 min, not 11.1. **The individual points fit. The total is about 1.5 min over.** That is another reason to merge in Act 2.

| TP | One clear idea? | "What we are doing" obvious? | Fit / delivery | Jargon and fixes |
|---|---|---|---|---|
| 01 Same question, two answers | Yes, strong | Yes | 41 s spoken out. OK | **Honesty risk:** "I asked that of a synthetic travel insurer ... and I got two answers" implies the AI gave 58.9. It did not: the schema-only agents got the loss ratio right (run 3). The 58.9 is a hand-written naive query. Sceptics who hear TP-02 will feel tricked. Also "every actuary **in this room**" is wrong for a prerecorded talk. Rewritten below. |
| 02 Model is not the problem | Yes, the best twist in the talk | Yes | 42 s. "9,999.99" is a tongue-twister ("nine thousand nine hundred ninety-nine dollars and ninety-nine cents"): say "just under ten thousand dollars" | It needs a closing line that sets up the rest of the talk. Right now it ends on "dangerous kind" and TP-03 jumps to binders. Rewritten below with the through-line "The AI can read your data. It cannot read your decisions." |
| 03 What a context layer is | Yes (binder analogy is excellent) | Yes | 38 s. OK | "kept as plain files in git": gloss git as "version-controlled, like your model code" or drop it. "open-source analytics agent": say "an open-source AI analyst". |
| 04 Sandbox | Weak: it is housekeeping, not an idea | Yes | 36 s | Low value for 36 s. "online travel agency" fine. Merge its two useful facts (synthetic, downloadable; codes not words) into TP-01 and TP-06. **Cut as a standalone point.** |
| 05 Step 1 scope | Yes ("be boring on purpose" is good) | Mostly | 32 s | "mart schema", "staging", "allow-listed-only", "raw feed", "config" = 5 engineering words in 70. Say: "I give it only the five clean tables. The raw feeds are locked out." Drop "allow-listed-only" from speech. |
| 06 Step 2 sync | Yes | Yes | 40 s incl. 12 s terminal | **Contradiction** with TP-02 ("it worked out that code 40 is a recovery"). Fix the last lines: "The file doesn't say. A good model may guess it. A guess is not a rule." "profile of the values" fine. |
| 07 Step 3 annotate | Yes | Yes | 34 s | Same contradiction: you are writing down what TP-02 said the model already inferred. Add the "repeatable" argument from `blind-agent-results.md`: "The model guessed right today. Tomorrow it may guess differently. Written down, it's the same answer every time." Mentions free-look and ZZTEST, which are **not on slide 9**. |
| 08 Step 4 define once | Yes, and it carries the attritional payoff | Yes | 35 s | Strongest Act 2 point. "per-risk retention", "IBNR", "cat" are fine for actuaries. Say "attritional" slowly (a-TRISH-un-ul). Consider merging with TP-07 as "Write down what only you know". |
| 09 Step 5 RULES as router | Two ideas (routing and asking). The "asking" idea is the gem | Partly. "Router" means nothing to actuaries | 38 s | Drop "router". Say "a one-page rule sheet the AI reads with every question". Lead with the "ask when unclear" rule. That is the line that wins sceptics. |
| 10 Step 6 reference answers | Yes ("write the answer key first") | Yes | 40 s | "YAML file": say "a small text file". "testing memory" is unclear: say "or you're testing whether it can copy". "behaviour" (British) fine. |
| 11 Step 7 grid | Yes, the payoff | Yes, but slide has 5 columns vs "three levels" spoken | 48 s spoken out: densest point | Too many numbers in one breath (6, 7, 9, 9, 39.3, 41.6, per thousand). "blind AI analysts" needs a gloss. Rewritten below. |
| 12 Diagnose before you fix | Yes | Yes | 36 s | "Returned the month as a number and my reference returned a date" is fine. **Overlaps Clip B** (Claire: context vs data vs model vs query). Let Claire carry it. Cut or shrink to 2 sentences right after Clip B. |
| 13 Investigation | Yes, and it is the only "fun" product moment | Yes | **~53 s incl. a 15 s demo for three chat questions. Unrealistic**: each nao answer takes 20 to 60 s live. In a prerecorded video, edit with visible jump-cuts and budget 25 s | "Every step shows its SQL": the slide shows no SQL. Show the nao chat with the SQL drawer open. Numbers: chart shows ~5 to 20 claims per month before July 2025, and **July is already 54** (grey). Say "from under twenty a month to around a hundred in August" and colour July too, or start the story in July. |
| 14 Judgement stays with the actuary | Yes. **This is what the sceptics need to hear** | Yes | 37 s | Clean. "judgements with your name on them" is a strong line. Keep. |
| 15 Close the loop | Yes | Mostly | 36 s | **Factual error:** says "There's an auto-merge mode". Source A8 says YOLO mode *auto-opens PRs*, not auto-merges. Fix to "an automatic mode that opens the change for you". "pull request", "regresses": say "a proposed change", "so it never breaks again". |
| 16 Ownership | Yes | Yes | 31 s | Good closing line ("the agent will happily invent one"). "CODEOWNERS", "CI check": say "a file that says who must approve" and "an automatic check". Analogy to reserving model governance is excellent: lead with it. |
| 17 Monday | Yes | Yes | 32 s | Good. Make it echo the Act 2 structure (see section 2). "earn the next nineteen" is nice. |
| 18 Close | Yes, but it does not land the line | Yes | 34 s | The slide's line "The model is fast. Your definitions make it right." is **never spoken**. Callback to the opening is missing. Rewritten below. |

### Jargon glossary (say this instead)

| On script or slide | Plain spoken version |
|---|---|
| schema / mart / staging | "the tables" / "the clean tables" / "the raw feeds" |
| allow_listed_only | "locked to those tables" |
| YAML / config | "a small settings file" |
| nao sync / profiling | "one command reads the tables and writes a summary" |
| RULES.md as a "router" | "a one-page rule sheet that points to the right definition" |
| git / pull request / merge | "version control, like your model code" / "a proposed change" / "approved" |
| CODEOWNERS / CI | "who must approve" / "an automatic check on every change" |
| pass^k (README only) | do not mention |
| YOLO mode | "automatic mode". "YOLO" reads as flippant to a risk audience |
| blind AI analysts | "AI analysts that saw only what I gave them" |
| ‰ | "per thousand" |

### Pronunciation flags for a French speaker

- "9,999.99": replace with "just under ten thousand dollars".
- "three sentences ... these three": dense "th" + "s". Use "three rules".
- "attritional", "institutional knowledge", "regresses", "accident-year basis": slow down or simplify. "Institutional knowledge" becomes "what your team knows".
- "thirty lines", "thousand", "the threshold": fine if slow. Avoid stacking ("three thousand things").
- "forty-one point six" vs "fourteen": stress "FOR-ty". Put the numbers on screen when you say them.

---

## 2. Narrative arc

**Current shape.** Hook (TP-01) → twist (TP-02) → definition (TP-03) → Clip A → **9 build points** (TP-04 to TP-12) with Clip B in the middle → payoff demo (TP-13) → judgement → governance x2 → Clip C → Monday → close.

**What works**
- The opening is a question every actuary has answered. Good. It starts mid-problem with no throat-clearing.
- TP-02's twist is the most credible moment for sceptics: "I expected it to fail; it mostly didn't." It earns trust.
- TP-14 "judgement stays with you" is exactly what the AI-sceptical half needs.

**What breaks**
1. **The twist is not carried forward.** After TP-02, the build reverts to "the machine doesn't know code 40" (TP-06, TP-07). The twist should change what follows: the context layer is for *decisions and consistency*, not for teaching the model SQL. Use one through-line and repeat it three times:
   > **"The AI can read your data. It cannot read your decisions."**
   Say it at the end of TP-02, at TP-08 (attritional = a decision), and set up the final line in TP-18.
2. **TP-02's slide spoils the payoff.** Slide 3 shows "39.3% vs 41.6%" before the grid. Hold it for TP-11.
3. **Act 2 is too long and too samey.** That is 9 points in a row, ~5.5 min of "file on screen", with a 3-min clip in the middle. Each step has the same rhythm ("Step N is ... here is the file"). Merge seven steps into **four**, and make them the *same four* as the Monday checklist, so the close repeats a structure the audience already knows:
   | New step | Merges | Monday echo |
   |---|---|---|
   | 1. Scope it and let nao read the tables | TP-04 (1 line) + TP-05 + TP-06 | "One bounded question" |
   | 2. Write down what only you know | TP-07 + TP-08 | "Write what it means, with an owner" |
   | 3. Tell it when to ask | TP-09 (ask-rule only) | (add to Monday as part of 2) |
   | 4. Write the answer key, then test | TP-10 + TP-11 | "Write the reference answer / Test the agent" |
   This saves ~1.5 to 2 min, which fixes the total overrun and buys time for a real nao screen moment.
4. **The product is invisible until minute ~17.** The project brief is a "20-minute demo of nao". Bookend with nao chat: in TP-02 or right after TP-03, ask nao (schema-only) "What was the 2025 attritional loss ratio?" and show **39.3%**. At the end of Act 2, ask again with full context and show **41.6%**, plus its reasoning citing `large_and_cat_losses.md`. Both numbers are evidenced in `evals/run3`. Optionally also show "What's the loss ratio?" getting a question back. A before/after on the *same screen* is the demo moment people remember.
5. **No memorable line is repeated.** Two candidates already exist: "A guess that looks right is the dangerous kind" and "The model is fast. Your definitions make it right." Pick the second as *the* line (it is on the final slide), say it aloud in TP-18, and seed it earlier with the through-line above.

**Clip placement**
- **Clip A** (data teams → context teams), after TP-03: good. Keep.
- **Clip B** (how to tell context vs data vs model vs query problems), currently *before* the tests. The audience has not seen a failure yet, so the question has no anchor. **Move it to right after the grid (TP-11)**, then let TP-12 shrink to two sentences ("Here's my own example: it was my test's fault"). It also breaks the build at a natural "we just saw failures" moment.
- **Clip C** (ownership and evidence), after TP-16: good. Optionally move it after TP-15 so TP-16 (ownership) answers Claire directly.

**Proposed running order**
TP-01 (hook, absorbs sandbox) → TP-02 (twist + through-line) → [nao chat: 39.3%] → TP-03 → **Clip A** → Step 1 (05+06) → Step 2 (07+08) → Step 3 (09 ask) → Step 4a (10) → Step 4b (11 grid) + [nao chat: 41.6%] → **Clip B** → TP-12 (2 sentences) → TP-13 → TP-14 → TP-15 → TP-16 → **Clip C** → TP-17 → TP-18.

---

## 3. Slide by slide (looked at every PNG at 1920x1080)

Global issues: every content slide uses only the top half to two-thirds, leaving the bottom 30 to 45% blank, while body text is ~28 to 32 px and code is ~22 px. On a video thumbnail or a conference stream at 720p, mono code at that size is unreadable. **Rule: no slide shows more than ~5 lines of raw code. Render files as "cards" in plain words, and move real code to the repo.**

| # | Slide | Verdict | Concrete fix |
|---|---|---|---|
| 1 | Title | **Keep** | Fine. Optional: add the nao logo and "with Claire Gouze, nao Labs" so the viewer knows a co-voice is coming. |
| 2 | "What was our 2025 loss ratio?" (bars) | **Fix** | It is not a waterfall. It is four absolute bars, and the second one *goes up* (58.9 → 61.0), which confuses on first look. The label "Naive (written prem., all txns, all partners)" is jargon. Build it in two clicks: first only two huge numbers, **58.9%** vs **49.9%**. Then a true waterfall with signed deltas (+2.1 earned premium, −5.5 recoveries, −5.6 test partner), each labelled with the plain rule. Enlarge the footnote or drop it into speech. |
| 3 | The model is not the problem | **Fix** | Remove "39.3% vs 41.6%" (save for the grid). Plain words, no code chips: left "It worked out (from the data)": transaction code 40 = recovery; one partner = test data. Right "It had to guess (our decisions)": attritional caps, not drops; frequency per 1,000; ask when unclear. Put the through-line big at the bottom: *"It can read your data. It can't read your decisions."* Use the empty space for a bigger font. |
| 4 | Context layer = binder + folder tree | **Fix** | Two ideas at once, and the tree is small mono with jargon ("router + always-rules"). Click 1: a binder graphic with 4 tabs, *Tables · Definitions · Rules · Answer key*. Click 2: the same 4 tabs mapped to folder names, large, with no `table=claims/` path detail. |
| 5 | Clip A card | **Keep** | Use Claire's photo or a video still instead of the mic emoji, and keep "CEO, nao Labs" on all three clip cards (B and C drop it). |
| 6 | Sandbox table | **Cut** (or shrink) | Mono table names (`mart.earned_premium_monthly`) and "grain" mean nothing to the audience. If kept: one "fact card": *60,000 policies · 4,200 claims · 4 partners + 1 test partner · codes, not words: 10 pay · 20 reserve · 40 recovery · valued 30 Sep 2026 · all synthetic*. |
| 7 | Step 1 YAML | **Fix** | YAML wall. An actuary will not read it in 5 s. Show three large statements with icons: **In:** 5 clean tables. **Out:** raw feeds. **Locked:** nothing outside the list. Keep a small faded YAML thumbnail in the corner as proof. |
| 8 | Step 2 nao sync | **Fix** | The important line (txn_code profile) is the smallest text. Make it the hero: a big three-row mini-table *code 20: 8,102 · code 10: 4,953 · code 40: 666 · meaning: ?* Drop "Databases: 5 tables across 1 datasets". Change the bottom line to match the fixed narrative: "Structure, not meaning. A model may guess. A guess isn't a rule." |
| 9 | Step 3 annotations | **Fix (urgent)** | **Overflows the right edge** ("outstanding case…", "reduces the loss**" cut off), shows raw markdown (`**`, backticks), and has an empty first line. Render as formatted text, 3 big lines: 10 = payment · 20 = reserve change · **40 = recovery: stored positive, subtract it** (highlighted). Badge: "Written by the reserving actuary. Never overwritten." Add the free-look and ZZTEST lines if the script keeps them. |
| 10 | Step 4 define once | **Keep, small fixes** | Most readable Act 2 slide. The right-hand file-name chip runs slightly past the right margin: shorten to "Large & cat losses". Replace `YEAR(loss_date)` with "year of loss date". Colour-highlight **capped** (it is the punchline). Make "Decisions, not facts" larger: it *is* the through-line. |
| 11 | Step 5 RULES.md | **Fix (urgent)** | Code wall, **overflows right edge on 3 lines**, raw markdown. Replace with three cards: **Point:** "loss ratio → read the loss ratio definition". **Always:** exclude test partner · earned premium · subtract recoveries. **Ask:** "'the loss ratio?' with no year → ask which year and basis". Retitle: "Step 3: a one-page rule sheet". |
| 12 | Clip B card | **Keep, move** | Move after the grid (see arc). Same card style fixes as slide 5. |
| 13 | Step 6 test YAML + SQL | **Fix (urgent)** | 20-line SQL wall, and **truncated**: the final `SELECT ... LEAST(net_incurred, 10000)`, the actual "cap" line and the one that matters, is hidden by `maxHeight`. Replace with an "answer key" card: **Question:** What was the 2025 attritional loss ratio? **Signed-off answer:** 41.6% · **Owner:** reserving actuary · *(SQL in the repo)*. Second small card: "What's the loss ratio?" → **passes only if it asks back**. If you must show SQL, show the one line `LEAST(net_incurred, 10000)  -- cap at $10k`. |
| 14 | Step 7 grid | **Fix** | Readable, but 5 columns with (a)/(b) and the "‰" symbol overload. Collapse to 3 columns (*Tables only · + table notes · + definitions & rules*), show scores **6–7/9 · 7/9 · 9/9**, and only the 3 rows that differ. Highlight the attritional row: **39.3% vs 41.6%**. Write "82.1 per 1,000". Raise the footnote from ~20 px to ≥ 24 px. Honesty is good, keep it. |
| 15 | Diagnose before you fix | **Fix or cut** | Two of four boxes have no example. "bad model" is ambiguous for actuaries (data model? AI model? reserving model?). If Clip B moves here, cut the slide or keep a 2-box version: *Context problem (frequency per 1,000)* vs *Test problem (month as number vs date → I fixed my test)*. Attribute "45% → 86%" to "Claire Gouze, nao Labs blog". |
| 16 | Investigation (2 charts) | **Fix** | Axis and label text ~14 to 16 px. Too small for video. Large empty band between charts and caption. Build in 3 beats matching the 3 questions: (1) big number 49.9 vs 41.6, (2) region bar alone and full-width, (3) monthly bar alone and full-width. July 2025 (54) is grey but already part of the spike. Colour it or say "from July". Better still: show it inside the nao chat UI with the SQL visible, because the script says "every step shows its SQL". |
| 17 | Judgement stays with the actuary | **Keep, enlarge** | Bottom 55% empty. Increase font ~1.4x. Make "then write the decision into the context" a full-width banner under the two columns. |
| 18 | Close the loop (mermaid) | **Fix** | Six small boxes, the last one **touches the right edge**, and the words are jargon ("Recommendations audit", "Ranked card + drafted patch"). Cut to 4 large steps: *Someone corrects an answer → nao proposes a change → an actuary approves → change + new test*. Replace "YOLO mode auto-opens PRs" with "Automatic mode: **off** for actuarial definitions". A real screenshot of a nao recommendation card would be far stronger than boxes. |
| 19 | Ownership (CODEOWNERS) | **Fix** | Raw file with `@handles` and a `.github/...` path. Replace with a 3-column table, large: *Definition · Owner · Check* → Loss ratio · Reserving actuary · re-tested on every change / Frequency · Pricing actuary · same / Rule sheet · Analytics lead · same. Subtitle: "Same governance as our reserving models." |
| 20 | Clip C card | **Keep** | Same card fixes. |
| 21 | Monday morning | **Keep, enlarge** | Fine content. Text at ~32 px with 50% empty space: go bigger. If Act 2 becomes 4 steps, reuse the same icons and numbering here. |
| 22 | Close | **Fix** | **No QR code** although TP-18 says "the repo link and QR code". **Placeholder text "Sponsor acknowledgement slide: supplied by the organizer" is visible**: remove it. Add a QR code and a short URL. The headline is great: say it aloud. |

---

## 4. Alignment: slide vs talking point

**Slide numbers in `**Show:**` are wrong from TP-04 on.** They ignore the three clip cards and the title. Actual PNG numbers:

| TP | Show says | Actual slide |
|---|---|---|
| 01–03 | 2, 3, 4 | 2, 3, 4 ✓ |
| 04 | 5 | **6** (5 is Clip A) |
| 05 | 6 | **7** |
| 06 | Terminal | 8 exists. Say "Terminal, then slide 8" |
| 07 | 8 | **9** |
| 08 | 9 | **10** |
| 09 | 10 | **11** |
| 10 | 11 | **13** (12 is Clip B) |
| 11 | 12 | **14** |
| 12 | 13 | **15** |
| 13 | nao chat | 16 is the backup |
| 14 | 15 | **17** |
| 15 | 16 | **18** |
| 16 | 17 | **19** |
| 17 | 18 | **21** (20 is Clip C) |
| 18 | 19 | **22** |

**Content mismatches**
- TP-01 vs slide 2: script says "two answers". The slide shows four bars, including a 61.0 that is never mentioned.
- TP-02 vs slide 3: slide shows 39.3 vs 41.6, which the script never says (and which spoils TP-11).
- TP-03 vs slide 4: script says "binder, then folder tree". The slide shows both at once (no click build).
- TP-06/07 vs TP-02: the code-40 contradiction (see sections 1 and 2).
- TP-07 vs slide 9: script names free-look cancellations and ZZTEST. The slide shows neither.
- TP-09 vs slide 11: script says "about thirty lines". The slide shows ~16 lines, clipped on the right.
- TP-10 vs slide 13: the cap logic that the whole talk depends on is cut off the slide.
- TP-11 vs slide 14: script says "three levels". The slide has five columns.
- TP-13 vs slide 16: "every step shows its SQL". No SQL on the slide. "about twenty a month" vs the chart showing ~5 to 20, with July already at 54.
- TP-15 vs slide 18 vs source A8: the script says "auto-merge mode", the slide says "YOLO mode auto-opens PRs", and the source says it *opens* PRs. **The script is factually wrong. Fix the script.**
- TP-18 vs slide 22: QR code promised but missing. The slide headline is not spoken.

---

## 5. Rewrites of the four points that most need it

All ≤ 115 words, short sentences, numbers spelled the way they should be said, no "in this room".

### TP-01 — Same question, two answers (100 words)
**Why:** removes the implication that the AI produced 58.9, fixes "in this room" for a recording, replaces "three sentences" (hard "th/s" cluster) with "three rules", and absorbs the sandbox point so TP-04 can go.

> **Say:** What was our 2025 loss ratio? Here are two answers from the same data. Fifty-eight point nine percent. And forty-nine point nine. Both queries run. Both numbers look fine on a slide. Only one is right. The gap is three rules that every actuary knows. Use earned premium, not written. Subtract recoveries. Remove the test partner. Three rules, nine points. Today I want to show you where those rules should live, so that an AI analyst reads them before it answers. Everything you will see runs on a synthetic travel insurer, so you can download it and try it yourself.

### TP-02 — The model is not the problem (103 words)
**Why:** removes the "9,999.99" tongue-twister, keeps the honest twist, and ends with the through-line the rest of the talk needs.

> **Say:** Now, I expected the AI to fail here. Mostly, it did not. I gave a model only the tables and the data. It worked out that code forty is a recovery. It found the test partner, because its claims were all just under ten thousand dollars. Impressive. Then I asked questions that depend on our decisions. What is attritional? How do we quote frequency? Here, it had to guess. And its guesses looked right. That is the dangerous kind. So here is the idea for today. The AI can read your data. It cannot read your decisions. You have to write them down.

*(Slide 3: remove "39.3% vs 41.6%"; add the through-line as the bottom banner.)*

### TP-11 — Run the tests, read the grid (108 words)
**Why:** the densest point. Glosses "blind analysts" and the three levels, spaces the numbers out, and spends its emphasis on the one row that matters.

> **Say:** Then you run the tests, and you get a grid. I ran the same nine questions with AI analysts at three levels of context. Level one: only the tables. Level two: plus my table notes. Level three: plus the definitions and the rules. With only the tables, they passed six or seven out of nine. With everything, nine out of nine, twice. Look at the attritional row. Without our definition, the agents removed the large claims instead of capping them. Their answer: thirty-nine point three. The right answer: forty-one point six. Nobody would notice. To be fair: this is synthetic data, a small test, and my own grader.

*(Slide 14: 3 columns, 3 rows, attritional row highlighted. Follow with the nao chat "after" clip showing 41.6%, then Clip B.)*

### TP-18 — Close (111 words)
**Why:** calls back to the opening, replaces "institutional knowledge" (hard to say, abstract) with concrete examples, and **says the one line out loud**.

> **Say:** Let me finish where I started. Same question, two answers, nine points apart. The models are already fast, and they are good at SQL. They will get better. But on their own, they will never know which premium you use, which partner is fake, or where you cap a large loss. That is your knowledge. Today it lives in people's heads. A context layer writes it down, gives it an owner, and tests it. So if you remember one line, remember this. The model is fast. Your definitions make it right. Everything is in this repository, on synthetic data. Run it, break it, and tell me what you find. Thank you.

### Line edits for the other points (no full rewrite needed)
- **TP-06**, last three sentences: "Notice what it says about code forty: nothing. A good model may guess. But a guess is not a rule."
- **TP-07**, add: "The model guessed right today. Tomorrow it may guess differently. Written down, it is the same answer every time."
- **TP-09**: drop "router". Open with: "Step three is a one-page rule sheet. The most important rule: when the question is unclear, ask."
- **TP-13**: "from under twenty a month to around a hundred in August". Set Demo to 25 s with jump-cuts, and trim words to stay under 60 s.
- **TP-15**: replace "There's an auto-merge mode" with "There is an automatic mode that opens the change for you."
- **TP-16**: lead with "We already do this for reserving models."
- **TP-05**: replace "include the mart schema, exclude staging, and set allow-listed-only" with "I give it only the clean tables, and I lock out the raw feeds."

---

## 6. Top 10 changes, in priority order

1. **Fix the three overflowing or truncated code slides (9, 11, 13).** Text is cut off the right edge, raw markdown is visible, and the key `LEAST(…,10000)` cap line is hidden. Replace them with plain-language cards.
2. **Resolve the code-40 contradiction** (TP-02 says the model inferred it, TP-06/07 say it can't know). Reframe annotations as "a guess is not a rule; written down, the answer is repeatable".
3. **Fix TP-01's honesty risk and "in this room".** The AI did not produce 58.9. A hand-written naive query did. Use the rewrite.
4. **Show nao itself early: a before/after on the same question** (attritional: 39.3% schema-only → 41.6% with context, both in `evals/run3`). Today the product UI first appears at TP-13.
5. **Compress Act 2 from 7 steps to 4, mirroring the Monday checklist.** Cut TP-04 as standalone, merge 05+06, 07+08, 10+11. This also fixes the ~1.5 min overrun at a realistic pace.
6. **Adopt one through-line and one closing line, said aloud.** "The AI can read your data. It cannot read your decisions." (TP-02, TP-08) → "The model is fast. Your definitions make it right." (TP-18, currently never spoken).
7. **Move Clip B to right after the grid (TP-11)** and shrink TP-12 to two sentences so Claire carries the diagnosis idea.
8. **Correct the factual error in TP-15**: YOLO mode auto-*opens* PRs (source A8). It does not auto-merge. Drop the word "YOLO" on slide 18 and simplify the flow to 4 boxes.
9. **Replace the remaining raw-config slides (7, 19) and simplify the grid (14) and the hook chart (2).** YAML becomes three statements. CODEOWNERS becomes an owner table. The grid goes to 3 columns and 3 rows. Slide 2 becomes a two-number reveal, then a signed waterfall (no unexplained 61.0 bar). Remove 39.3/41.6 from slide 3.
10. **Housekeeping:** renumber every `**Show:**` slide reference (off by 1 to 3 from TP-04), add the promised QR code, delete the visible sponsor placeholder on slide 22, enlarge fonts to use the empty bottom third of every slide, set TP-13 demo to ~25 s with jump-cuts, and gloss or drop jargon (router, YAML, allow-listed-only, CODEOWNERS, CI, ‰).
