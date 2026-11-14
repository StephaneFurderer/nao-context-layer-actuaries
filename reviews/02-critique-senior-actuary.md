# Critique: "Building the context layer" demo segment
Reviewer stance: skeptical FCAS-level P&C actuary (reserving and pricing, short-tail incl. travel). Read-only review of /home/claude/repo, every number re-run against `warehouse/travel.duckdb` (read_only) on 2026-11-14.

Bottom line: the arithmetic reproduces. Where the talk is exposed is wording. Some definitions use terms that mean something else to a P&C actuary, the experiment is presented more strongly than its design supports, and two "the agent got it wrong" examples are really convention or formatting differences. A sharp audience member will spot all of these within 30 seconds of the grid slide.

---

## A. Number verification (my SQL vs the script)

| Script claim | Where | Reproduces? | Notes |
|---|---|---|---|
| 58.9% naive | TP-01, slide 2 | Yes, 58.95% | Waterfall: 58.9, then 61.0 (earned), then 55.5 (recoveries), then 49.9 (ZZTEST). Moving to earned premium *raises* the ratio. ZZTEST is the biggest single step (5.6 pts): 37 AY2025 claims, $271k incurred, on $45.7k EP. |
| 49.9% reference | TP-01, TP-13 | Yes, 49.93% | AY, CY and PY 2025 come out at 49.9%, 49.9% and 49.8%: they agree within 0.1 pt (see B5). |
| 41.6% attritional | TP-11, TP-13 | Yes, 41.56% | Cat removal alone gives 42.2%. Capping takes off only 0.6 pt more. |
| 39.3% blind answer | TP-02, TP-11 | Yes, 39.28% | This is cat removed **plus large claims dropped**, a standard definition in many shops (see B3). |
| 95.7% Caribbean | TP-13 | Yes, 95.73% | Caribbean **ex-cat is 50.6%**, in line with North America (51.4%). The whole excess is HU25. That's a better line than the one in the script. |
| Others 35–51% | TP-13 | Yes, 34.6%–51.4% | Fine. |
| "~20/month → 100 in August" | TP-13, slide 16 | **Partly** | Aug = 100 checks out. The baseline is about **13/month** (Jan 2024–Jun 2025 average 12.9; non-cat H1 2025 around 13), not 20. The rise **starts in July (54)**, not August. Sep 90, Oct 51, Nov 6, Dec 11. "Stay high through October" is fair. "About twenty" overstates the baseline by roughly 50%. |
| 60k policies | TP-04 | Yes, 60,000 | Includes 613 ZZTEST and 2,099 free-look cancellations. |
| ~4k claims | TP-04 | Yes, 4,206 | Includes 91 ZZTEST claims (60 QA claims at $9,999.99, plus 31 organic). |
| 10 large losses | test | Yes | ≥ and > $10k give the same 10. All are medical. **Largest claim on the whole book is $22,588.** |
| 82.1 per 1,000 | slide 14 | Yes, but it's **Asia's row** | The grid shows one number for a by-region test. The portfolio frequency is 84.8. Caribbean is 139.3. The single "82.1 ‰" figure reads as the portfolio figure and isn't. |
| ~13,700 transactions | slide 5 | Yes, 13,721 | |

Also found in the data:
- **AY2024 and AY2025 have zero open claims and zero outstanding case reserves** at 2026-09-30. Only AY2026 has open claims (190 of 1,073).
- **18 HU25 cat claims have loss dates in April–June 2025.** The earliest is 2025-04-10, which means a hurricane-season cat claim before the season started. The cause is `generate.py`: cancellation loss dates are drawn uniformly between purchase and departure.

---

## B. Actuarial correctness: where a reserving or pricing actuary will say "that's not how we'd define it"

**B1. "Net incurred" (TP-08, slide 9, loss_ratio.md, annotations).** To most P&C actuaries "net" means **net of reinsurance**. Here it means net of salvage and subrogation (recoveries), gross of reinsurance. Expect the heckle: "Net of what? You just told us $10k is your per-risk retention." Fix: call it "incurred, net of recoveries (gross of reinsurance)" everywhere, or "S&S-net incurred".

**B2. The loss ratio basis is incomplete (slide 2 footer, TP-08).** It doesn't say:
- that LAE is excluded (pure loss ratio, no ALAE or ULAE);
- that the denominator is **gross** earned premium, before partner commission. In travel, distribution commission is often a large share of premium, so a 50% gross pure loss ratio can sit inside an unprofitable combined ratio. A pricing actuary will ask straight away.

Suggested footer: *"AY 2025 pure loss ratio: incurred net of recoveries, gross of reinsurance, excl. LAE, over gross earned premium; case reserves only, no IBNR; valued 2026-09-30."*

**B3. Attritional "capped vs dropped" is presented as right vs wrong, and it isn't (TP-02, TP-11, slide 3, blind-agent-results.md).** In many London-market and reinsurance-pricing shops, attritional means *excluding* large and cat losses entirely, with large losses modelled separately. Capping at the threshold is also common, for example in capped or basic-limits pricing. Both are defensible. Calling 39.3% "the most dangerous kind of error" will draw: "That's my definition, and it's not an error." The impact is also small: 2.3 pts between the two, and capping vs cat-only is 0.6 pt. Reframe it as "two defensible definitions; the house chose one; the agent can't know which unless you write it down." That's actually the stronger argument for a context layer.

**B4. "$10,000 = our per-risk retention" (TP-08, slide 9).** For travel medical (medevac, ICU abroad), per-risk XL retentions are usually far higher than $10k. The synthetic book also has no severity tail: max claim $22.6k and only 10 large losses out of 1,755. Anyone who prices travel will notice. Fix: drop "per-risk retention" and say "our large-loss reporting threshold". Optionally add a medevac tail in `generate.py`.

**B5. "Accident-year loss ratio with calendar-year earned premium" is described correctly.** AY incurred over CY earned for the same year is the standard construction, so no problem there. Three related issues:
- **Opening question vs basis default.** TP-01 asks "What was our 2025 loss ratio?" To a CFO or in annual-report language, "2025 loss ratio" is often calendar-year. Your RULES.md defaults to AY *without asking* when a year is given. That's defensible, but say it out loud, or a reserving actuary will say your own opening question is the ambiguous one.
- **The basis choice has no effect here.** In this data, AY, CY and PY 2025 all give 49.9% / 49.9% / 49.8%, because there's no development. The "ask which basis" rule can't change any answer in this warehouse. Don't imply it does.
- **Mixed bases.** Frequency uses departure year and the loss ratio uses accident year. That's fine (pricing vs reserving views), but expect "why two exposure bases?" Have one sentence ready.

**B6. Maturity of AY2025 at 2026-09-30 (21 months).** For real short-tail travel, that's broadly mature for reported counts. It is *not* fully mature for:
- late airline and third-party recoveries, which are negative IBNR;
- disputed medical claims;
- occasional late reporting.

In the synthetic data it is 100% closed, with zero case reserves. So "case incurred, no IBNR" is really **paid net of recoveries**: case reserves contribute nothing to any number in the talk. A reserving actuary may say: "You've shown me the easy part. The hard part is the reserves, and the agent never touches them." Say this explicitly (see B9).

**B7. Earned premium pro-rata from purchase date to return date (earned_premium_monthly annotations).** This is non-standard for travel. Cancellation exposure runs purchase→departure and tends to increase as departure approaches; trip covers run departure→return. Many carriers earn at or around departure, or use a risk-weighted curve. A straight-line purchase→return earning pattern is a reasonable simplification for a demo but should be labelled one: "simplified straight-line earning; your earning pattern goes in this file." It's also a good example of a convention that belongs in the context layer.

**B8. Other definition points:**
- **Frequency (claim_frequency.md):** per policy, not per exposure-day or per trip-day, and denied claims are included in the numerator. Both are defensible; say "reported claims, incl. denied, per 1,000 policies". Cat claims are also included in frequency, so Caribbean shows 139.3 ‰. Fine, but flag it.
- **Free-look:** handled correctly. CX policies have no earned premium and are excluded from counts. The naive written premium in step 0 includes free-look written premium that would normally be reversed as negative written premium. Minor, but "naive written" is gross of cancellations, which nobody's ledger reports. One word on the slide fixes it: "gross written, before cancellations".
- **Recoveries:** correct direction. Note that net incurred excludes *anticipated* salvage and subrogation, which is standard but worth stating.

**B9. ZZTEST is a data-quality defect, not context (TP-01, TP-07, RULES.md).** Expect: "If QA test claims are in your production mart, fix the pipeline. Don't teach the AI to ignore them." Your own source B3 (Claire: "context engineering is mostly data engineering") supports that heckle. And under **ASOP 23 (Data Quality)** the actuary would be expected to address it at the data level. Fix: "In a real shop you'd filter ZZTEST upstream. I left it in because every warehouse has one of these that nobody has fixed yet, and until it's fixed, it has to be written down."

---

## C. Credibility of the blind-agent experiment

What a skeptic will attack, in order of damage:

1. **The answers are in the context (contradicts TP-10).**
   - `semantics/loss_ratio.md` contains a SQL "Pattern" that is essentially `tests/loss_ratio_ay2025.yml` with `:year` in place of 2025.
   - `semantics/large_and_cat_losses.md` contains the attritional numerator from `tests/attritional_loss_ratio_ay2025.yml` almost verbatim.
   - TP-10 says: "never paste the answers into the context, or you're testing memory." The repo is public, and someone will diff it. L2's 9/9 is then partly "can it copy a template". Fix one of two ways:
     - (a) remove the SQL patterns from semantics (keep prose definitions), re-run L2, and report the result whatever it is; or
     - (b) keep them and say so in TP-10/TP-11: "my definitions include SQL patterns, so L2 measures whether it applies them, not whether it can work them out." Option (a) is much stronger.
2. **Grader tolerance is ±0.5 loss-ratio points.** `grade.py` rounds both values to 2 decimals before comparing, so 0.4218 and 0.4156 both round to 0.42.
   - **An agent that removes cat and does no capping at all (42.2%) passes the attritional test.** I checked this with the grader's comparison logic.
   - So the one "convention" test that separates L0 from L2 would also pass a third, wrong-by-your-definition answer.
   - Fix: compare loss ratios at 4 decimals, or in basis points.
3. **The frequency failure is graded inconsistently with the month failure.**
   - L0b and L1 returned 0.082, which is *exactly* 82.1 per 1,000 expressed per policy.
   - Slide 13 classifies "per 1,000" as a **context** failure, but "month as int vs date" as a **test** failure that you fixed.
   - A skeptic: "Same thing: a correct number in a different unit. You fixed the test when it hurt L2 and kept it when it hurt L0."
   - Only L0a (0.079, free-look policies left in the denominator) is a real miss.
   - Fix: say "L0b's number was right in a different unit; I count it as a fail because our convention says per 1,000, and a report reader would misread 0.08." Better still, move per-1,000 to the "convention you must state" column and change the frequency test's prompt to say "per 1,000", as you did with the month test. That makes the true L0 result 7–8/9.
4. **n and design.**
   - Two runs per level (L1 has **one**), nine questions, one model family (Claude Sonnet).
   - The same person designed the traps, wrote the data, the context, the tests and the grader.
   - There are no held-out questions, and all nine tests were written alongside the context they evaluate.
   - "Large losses ✅ guessed" counts as a pass for L0 even though the agent guessed.
5. **The data was changed when the agent succeeded.** Run 1 → Run 3 history: the schema-only agent got the loss ratio right on Run 1, so the data was recoded to be harder, then two conventions were added. Being open about this is good (it's in the results file), but if it comes out in Q&A rather than from you, it sounds like moving the goalposts. Say it first.
6. **The "investigation" was planted.** R4 in your own source bank says so. TP-13 presents it as discovery. Say "planted" on stage.

**Is it oversold or undersold?** The grid slide's footer is honest, so the caveats are there. TP-11's spoken framing ("The misses were all conventions") is slightly oversold for the reasons above. The genuine findings are more interesting and are undersold:
- the two schema-only runs disagreed with each other (0.079 vs 0.082, different denominators);
- one schema-only run answered when it should have asked;
- the agent *inferred* code 40 and ZZTEST from the evidence in the data.

Lead with **consistency and ask-vs-answer**, not accuracy.

Suggested replacement wording for the grid footer:
> *Simulation, not a nao run: Claude Sonnet sub-agents, 2 runs per level (1 for annotations), 9 questions written by the presenter on presenter-designed synthetic data, graded by presenter's script at 2-dp tolerance. Illustrative, not evidence of accuracy.*

---

## D. What's missing for this audience

1. **Governance and actuarial standards.** One slide or one sentence in TP-16:
   - ASOP 23 (Data Quality): ZZTEST, earned premium mart.
   - ASOP 56 (Modeling): reliance on a model developed by others, understanding its limitations, validation.
   - ASOP 41 (Actuarial Communications): disclosing basis and limitations. Your answer-format rule (basis, SQL, caveats) is effectively ASOP 41 discipline; say so, it will resonate.
   - The NAIC Model Bulletin on insurers' use of AI systems (adopted in many states) expects a written AI program, governance, and third-party vendor oversight.
   - Map CODEOWNERS + CI tests to the "model validation and change control" language they already use.
2. **Reconciliation to the books.** "Does your earned premium tie to the GL and to Schedule P / the statutory statements?" The reference SQL is only as good as the mart. Add one sentence: "the reference answers are reconciled to booked earned and incurred each quarter-close, or the test is meaningless."
3. **Data privacy.**
   - `nao sync` writes **preview.md with sample rows** into the context folder. That content goes to the LLM provider and gets committed to git.
   - With real travel-medical claims, that's health data and possibly EU-traveller personal data (GDPR).
   - Say what you'd do: disable previews on claim tables, mask the columns, keep the model under an enterprise / zero-retention agreement or in-tenant.
4. **Fit with existing reserving tools.** Be explicit that this is for ad-hoc analytical Q&A on the mart. It is not reserving: no triangles, no IBNR, no selected ultimates. The agent doesn't replace Arius/ResQ/chainladder. Better: it could *answer questions about* their outputs if those are in the mart.
5. **Cost and effort.**
   - How many hours did the context take to write?
   - What does a question cost in tokens?
   - What does running `nao test -k` on every pull request cost?
   - A one-line answer ("about a day for five tables and nine tests; cents per question") disarms the "what's the TCO" question.
6. **Failure modes beyond conventions.** What happens when the agent is confidently wrong on a question *not* in the tests? The tests cover nine questions; users will ask the 10th. Say "tests are a floor, not coverage."
7. **Who signs.** If an agent-produced number reaches a reserving committee, who is the responsible actuary? TP-14 hints at it. Make it explicit: "the agent is an analyst; the actuary still signs."

---

## E. The 3 weakest talking points, rewritten (each ≤ 120 words)

### TP-11 (weakest: oversells a self-graded, small-n simulation and conflicts with TP-10)
Problems: C1, C2, C3, C4. The phrase "the misses were all conventions" doesn't hold up under scrutiny, and "nine of nine" is the line skeptics will quote back.

**Say (rewrite, ~110 words):**
> Then you run the tests and read the grid. I simulated this outside nao: Claude Sonnet analysts, working blind, at three levels of context, graded by my own script. Schema only passed six or seven of nine; full context passed nine of nine, on two runs. Read that carefully: two runs, one model family, nine questions I wrote, on data I designed, and my definitions include SQL patterns. So this is not evidence the agent is accurate. It's evidence the tests catch the failures that matter: two blind runs that disagreed with each other, a convention it couldn't know, and one answer where it should have asked. Rerun it on your data.

### TP-13 (planted finding presented as discovery; baseline overstated; misses the best line)
Problems: "about twenty a month" (actually around 13), "jump ... in August" (the rise starts in July at 54), not disclosed as planted (R4 says it was), and it skips the strongest fact: Caribbean ex-cat is 50.6%.

**Say (rewrite, ~110 words):**
> Now the investigation, with a confession: I planted this in the synthetic data, so watch the workflow, not the discovery. All-in AY 2025 is 49.9 percent; attritional is 41.6. Almost all of that gap is cat. By region, the Caribbean runs at 95.7 percent; every other region is between 35 and 51. Take out the HU25 claims and the Caribbean drops to about 51, in line with North America. By loss month, Caribbean cancellations run around a dozen a month, climb in July, peak at a hundred in August and stay high through October. Every step shows its SQL, and each one matches a reference answer I'd signed off.

(Also fix slide 16's caption to "~13 / month → 54 in July → 100 in August". And fix `generate.py` so HU25 loss dates fall within or just before the storm window, not in April. A claims person will spot an April hurricane cat claim on the chart's tooltip or in Q&A.)

### TP-08 (terminology that triggers the room)
Problems: "net incurred" (B1), missing LAE and gross-premium basis (B2), "$10k = per-risk retention" (B4), and attritional framed as *the* definition (B3).

**Say (rewrite, ~115 words):**
> Step four: define each metric once. The loss ratio file says incurred losses, net of recoveries but gross of reinsurance, excluding LAE, over gross earned premium; accident-year basis; valued September 30; case reserves only, no IBNR. A second file holds decisions only we can make. A large loss is ten thousand dollars or more. Attritional means cat claims out and every other claim capped at ten thousand. Some of you drop large claims instead of capping them. Both are defensible, and that's the point: it's a choice, so it gets written down, owned and tested. Nao's docs say two definitions of one metric are the most common cause of inconsistent answers.

---

## F. Smaller wording fixes, by TP

- **TP-01:** "every actuary in this room knows" → "every actuary in this room would apply". Add after "49.9 percent": "on an accident-year basis, which is itself a choice". That pre-empts the CY heckle (B5).
- **TP-02:**
  - "It guessed" is fair for large loss, but the large-loss guess was *right* and was graded a pass. Say: "On large loss it guessed ten thousand and happened to be right. On attritional and frequency, its guesses didn't match our convention."
  - Drop "the dangerous kind" for 39.3%, or say "a different, defensible convention that looks just as plausible" (B3).
- **TP-04:** "sixty thousand policies" → "sixty thousand policies, about two thousand of them cancelled in the free-look window". That sets up TP-07.
- **TP-07:** add "In a real shop you'd fix ZZTEST upstream; until someone does, it has to be written down" (B9).
- **TP-10:** either remove the SQL patterns from `semantics/` and re-run, or replace the last sentence with: "One warning: never paste the reference answers into the context. My definitions do include SQL templates, so treat my L2 score as an upper bound."
- **TP-12:** reconcile with the frequency case (C3): "I fixed the month test because the question didn't specify a format. I didn't fix frequency because 'per 1,000' *is* our convention, and an unlabelled 0.08 in a report would be misread. That's a judgement call, and I'll show you both."
- **TP-14:** "a trend we should price into Caribbean trips". Ex-cat, Caribbean is 50.6%, so the pricing question is cat load and accumulation (cruise partner CRUZ concentration), not attritional trend. Say "a cat load and an accumulation question for Caribbean cruise business".
- **TP-16:** add one sentence: "This is the same change control ASOP 56 and the NAIC AI bulletin already expect for models, applied to the words the AI reads."
- **Slide 2 footer:** use the full basis line from B2.
- **Slide 14:** replace "82.1 ‰" with "by-region table, per 1,000" or show the portfolio figure, 84.8 ‰.
- **Slide 3:** "60 claims at $9,999.99" is correct for all years; the AY2025 effect is 37 ZZTEST claims and 5.6 LR points. Using "5.6 points from 1% of policies" is more striking.

---

## G. Top 10 issues, priority order

1. **Answers in the context.** The semantics files contain SQL near-identical to the test SQL, which contradicts TP-10's own warning; L2's 9/9 is partly template-copying. Remove the patterns and re-run, or disclose.
2. **Grader tolerance ±0.5 LR pts.** 2-dp rounding lets an uncapped ex-cat answer (42.2%) pass the attritional test. Tighten to 4 dp.
3. **Inconsistent failure labelling.** 0.082/policy (= 82.1 ‰) is a "context failure" but month-as-int is a "test defect". Treat them the same; true L0 is closer to 7–8/9.
4. **"Dropped vs capped" attritional framed as an error.** Excluding large losses entirely is a standard definition; reframe as "two defensible conventions" (TP-02, TP-11, slide 3).
5. **"Net incurred" means net of reinsurance to this audience.** Rename it, and add "excl. LAE, gross earned premium before commission" to the basis (TP-08, slide 2).
6. **TP-13 accuracy and disclosure.** Baseline is about 13/month, not 20; the rise starts in July; the finding was planted (R4); 18 HU25 claims carry April–June loss dates. Use "Caribbean ex-cat = 50.6%".
7. **No development in the data.** AY2024–25 are 100% closed with zero case reserves, and AY, CY and PY ratios all equal 49.9%. "Case incurred, no IBNR" is really paid net of recoveries. Say the demo doesn't touch reserving, and why AY2025 at 21 months is (mostly) mature for travel.
8. **Experiment design.** n = 2 (1 for L1), one model family, presenter-built data, tests, context and grader, no held-out questions, data recoded after Run 1 succeeded. Say all of this first, in TP-11.
9. **Implausible conventions.** A $10k "per-risk retention" for travel medical, a max claim of $22.6k, and straight-line purchase→return earning. Relabel as threshold / simplification.
10. **Missing governance, privacy and fit.**
    - ASOP 23/41/56 and the NAIC AI bulletin.
    - Reconciliation to the GL / Schedule P.
    - preview.md rows sent to the LLM.
    - ZZTEST as an upstream data fix.
    - Cost and hours.
    - "Not a reserving tool."
