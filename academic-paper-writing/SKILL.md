---
name: academic-paper-writing
description: Author conventions for writing, revising, and verifying rigorous empirical research papers across fields (economics, management, finance, sociology, public policy, IS, OB, marketing, accounting). Use when drafting or revising any journal submission. Does NOT cover journal-specific formatting (page limits, citation style, abstract format variants) — defer those to the target journal's author guidelines.
---

# Academic paper-writing conventions

How to write, revise, and verify empirical research manuscripts so they survive top-tier editorial review. These conventions are field-agnostic. Apply them to any empirical paper regardless of discipline.

**Korean-speaking authors:** respond in Korean for explanation and discussion; keep technical strings (variable names, code, audit labels, section labels, journal names) in English.

---

# PART 1 — Workflow philosophy

## 1.1 Plan → execute → verify

Every substantive revision follows three steps:

1. **Plan.** Read the affected sections. Identify every paragraph, table, footer, and cross-reference touched by the change. Lay out the specific edits BEFORE making them. For large changes, show the plan to the user first.
2. **Execute.** Apply the edits.
3. **Verify.** Re-run audits. Check the regenerated document. Report PASS/FAIL explicitly.

User signal phrases: "계획 먼저 세우고", "전략을 세우고", "검증하고 실행하고 검증해". Treat any mention of plan / strategy as a request to surface the plan first.

## 1.2 Multi-round verification

After a single audit pass, run again at a different angle. One pass typically catches the issues it was designed for; a second pass at a different angle catches structural drift the first pass missed.

Standard audit angles to cycle through:
- Section-by-section structural check
- Cross-section duplication / consistency
- Method ↔ Result commitment alignment
- Logical flow and paragraph adjacency
- Sentence length per section
- Numerical consistency (script outputs vs body vs tables vs footers)
- Memo resolution (every Word comment addressed)
- Editor walkthrough (read as an editor would)

User signal: "여러번 검증", "10번 검증", "꼼꼼히 검증".

## 1.3 Audit-driven revision

Never claim a revision is complete without running an audit. "I think it's fixed" is not the same as "the audit passes." When reporting back, lead with the specific audit result (`12/12 PASS` or list the specific failures), not with subjective claims.

## 1.4 Integrity over speed

The user's primary concern is **integrity**: claims, numbers, hypotheses, and framing all align internally and with the underlying analyses. Integrity failures to watch for:
- Hypothesis says X but result paragraph says Y.
- Body cites coefficient 1.04 but table cell shows 1.042.
- Abstract claims "supported" but limitations section admits marginal.
- Cover letter sharper than abstract.
- Stale prior-version sample sizes lurking in some appendix sentence.
- Method commits to estimator X but a result paragraph implies estimator Y.

User signal phrases: "integrity 측면이 중요해", "critical issue".

When the user flags "critical issue" repeatedly: the root cause is systemic, not surface-level. Add an audit type, do a full re-read, restructure the workflow — don't just patch the surface.

## 1.5 Question vs revision request

The user often asks substantive questions without wanting a rewrite. Signal phrases:
- "이건 질문인데..." / "Just a question..."
- "그냥 물어보는건데..." / "Just asking..."
- "수정하지말고 대답만 해봐" / "Don't revise, just answer."

When you see these phrases: answer the question precisely. Do NOT immediately start editing. After answering, you can ask whether to apply the answer as a revision. Do not assume.

## 1.6 Autonomous execution + option-based branching

The user prefers autonomous execution for routine edits. Default to action, not to asking. Signal: "권한 묻지말고 계속 진행해."

**Routine edits — just do them:**
- Trim a long sentence.
- Fix a typo.
- Resolve a memo with obvious intent.
- Re-run an audit.
- Rebuild the document.
- Update a table footer to match a body number.

**Substantive branching decisions — present options and ask:**
- Should we keep hypothesis X or replace it with Y?
- Destructive operations (delete tables, remove sections, drop hypotheses).
- Major restructuring (move section, renumber tables).
- Reframing that changes the paper's theoretical anchor.

**Option-presentation format:**
```
Option A: [specific change] — pros: [...] / cons: [...]
Option B: [alternative] — pros: [...] / cons: [...]
Option C: [combination or hybrid] — pros: [...] / cons: [...]
```
User typically picks by letter or number: "옵션 A로", "1번으로 해줘", "a로 하자".

## 1.7 "잠깐" pause pattern

When the user types "잠깐" / "잠깐만" / "wait":
1. They are pausing the active revision flow.
2. They want to ask a sanity-check question or raise a concern.
3. Do NOT continue editing or rebuilding until you've answered the pause-question.
4. After answering, wait for explicit direction to resume.

## 1.8 Compact-summarize before context overflow

For long revision tasks that might exceed the context window: before working, write a stable summary of the methodology / workflow / constraints / audit-pass criteria into a single block. This summary survives a compact and gives the post-compact session a recoverable plan.

User signal: "혹시 컨텍스트창 끊길것 같으면 압축하고 먼저 압축하고 반영해."

---

# PART 2 — Paper architecture

## 2.1 Title

- Short, plain, ≤12 words.
- Avoid stacked noun phrases ("X, Y, and Z").
- Question form is welcome — a clear research question hooks the reader.
- Avoid generic terms when more specific options exist. Choose terms that signal the substantive concept, not the data source.
- Include the new core finding or contribution in the title or subtitle, not just a generic descriptor of the empirical setting.
- When proposing title candidates, offer 5–10 options as a short table with word-count and emphasis tags so the user can compare.

## 2.2 Abstract

**Format varies by journal.** Common formats:
- Single unstructured abstract (most economics, finance, sociology journals; 150–250 words).
- Structured abstract with explicit sub-headings (some health, IS, OB journals).
- Dual abstracts — academic summary + practitioner summary (some management journals).
- Graphical / visual abstract or "Highlights" bullets (some Elsevier journals).

**General principles regardless of format:**
1. Open with the puzzle as a question or a sharp claim (not "This paper investigates...").
2. State the argument / what conditions the outcome.
3. Sketch the empirical engine in one clause.
4. Report the headline finding qualitatively (not numerically).
5. Indicate mechanism or boundary if space permits.

**Never in any abstract:**
- Cite literature (in the academic / research summary).
- Use numbered hypothesis labels (H1, H2, P1, P2).
- Report specific coefficients, p-values, or sample sizes.
- Forward-reference sections ("developed in Section X.Y").

## 2.3 Introduction

A 7–9 paragraph arc that earns the reader's continued attention:

1. **Puzzle** — a question that motivates the field's readers (not "the literature has a gap"). Lead with a substantive question.
2. **Prior literature positioning** — two or three angles existing literature has taken, with explicit limits. Be sharp about what existing work does NOT do (e.g., "stops at the X margin: does not link Y to Z").
3. **Our argument** — what we propose, distinguishing from prior work.
4. **Construct gap / data gap** — why the answer has been hard to observe.
5. **Data design** — the novel data combination or empirical engine.
6. **Findings preview** (split into 2–3 paragraphs, not one giant block):
   - First paragraph: baseline + central contribution.
   - Second paragraph: mechanism / boundary tests.
   - Third paragraph: synthesis.
7. **Contributions** — typically three, with a unifying premise sentence at the top: "The unifying premise is that X is a Y question, not a Z question."

**Critical rules for the introduction:**
- **Do NOT use explicit hypothesis labels** (H1, H2, P1, P2). Preview findings semantically.
- **Do NOT use specific coefficient numbers** in the introduction. Numbers belong in the Results section.
- **Do NOT forward-reference** specific sections ("developed in Section 7.2"). Trust the reader to find the discussion.
- **Lead each finding-preview paragraph with the substantive claim**, not "We test..." or "Table N reports...".

## 2.4 Hypothesis development logic comes BEFORE the hypothesis statement

The paragraph IMMEDIATELY preceding a hypothesis statement must:
1. State the theoretical mechanism in plain prose.
2. Apply it to the empirical context.
3. Derive the directional prediction.

Then the hypothesis statement crystallizes the prediction into one declarative sentence.

If a hypothesis appears without a preceding development paragraph, add one. If the development paragraph is too thin (e.g., just "We expect X"), expand it with the actual reasoning chain.

User signal: "가설을 만들어내는 논리가 없는것 같지? 그것도 추가."

## 2.5 Hypothesis statement format

- One- or two-sentence declarative statements.
- Use prose: "Hypothesis (H1). In X settings, A is associated with higher B."
- Never use math operators in hypothesis prose: ×, ≥, ≤, ∈. Replace with "interacts with", "at or above", "at or below", "in the set of".
- The mathematical specification belongs in the methods section, not in the hypothesis statement.

**Mechanism hypotheses** (often labeled H3, H4) use a channel template:
> "The [main effect] in [main hypothesis] operates through [mediating variable Y]. The [outcome] is amplified in firms / settings where Y is present, and muted where Y is absent."

Avoid academic-jargon-heavy phrasings. The reader should grasp the mechanism in one read.

## 2.6 Methods section

**Typical structure (adjust to field conventions):**
- Research design overview
- Data sources and sample construction
- Sample matching / linkage procedures
- Independent variable construction
- Mediating / moderating variable construction
- Dependent variable and controls
- Empirical models (specifications + identification + sample design)
- Descriptive statistics

**Equation handling:**
- Each equation paragraph is followed by a "where X is..., Y is..., μ is..." explanation paragraph.
- For multiple specifications, present sequentially.

**Identification:**
- Explain instrument or design choice substantively (what threat does each instrument address?).
- Report standard weak-instrument and over-identification diagnostics.
- For interaction-term endogeneity, run a separate validity check on the main interaction specification and report it in an appendix.

**Nested-sample design:**
- When hypotheses use slightly different subsamples, explicitly note that all hypotheses share a common base panel, with each hypothesis nesting via specific variable observability.
- State the nesting in the methods section AND in the results section (preferably in table footers).
- This needs explicit defense — reviewers will ask.

**Equation-rendering caveat (Word docx):** Native Word equations via OMML are hard to generate programmatically. The `pyommlbuilder` Python library produces minimal OMML that Word rejects. If the user wants native equations, the safest paths are (a) keep equations as plaintext in the script and let the user paste them into Word's equation editor manually, or (b) use a Pandoc-based LaTeX → docx pipeline.

## 2.7 Results section — deductive structure

**The deductive ("두괄식") rule**: every result subsection starts with the punchline, then explains.

Template for each hypothesis subsection:
```
Hypothesis X is supported: [headline coefficient and contrast in one sentence].
Table N reports [the test specification].

[INSERT TABLE N HERE]

[detailed walk-through of the estimates]

[Two observations follow: First, ... Second, ...]
```

**Never** start a result subsection with "Table N reports the H_x mechanism test." That's inductive (미괄식) and forces the reader to read to the end to find out whether the hypothesis is supported.

**Numbers belong here:** Results is where coefficients, p-values, sample sizes are reported in prose. NOT in abstract, NOT in introduction.

**Negative results / null exceptions:**
- Report honestly. Don't hide them.
- Use language like "null exception" or "imprecisely identified" rather than evasive phrasing.
- If 3 of 4 mechanism panels support a prediction, say "supported in three of the four panels" — don't claim universal support.

## 2.8 Robustness checks — prediction-test framing

**Frame as prediction tests, not cherry-pick disclosures.**

Bad framing (cherry-pick risk):
> "Our result attenuates under alternative residual X; we therefore use residual Y as the headline."

Good framing (prediction-test):
> "The measurement argument in Section 3.6 generates a testable prediction: under alternative residuals that do not net out X, the coefficients should attenuate. Appendix C confirms this prediction; the attenuation pattern independently supports the measurement choice rather than indicating fragility."

This converts "our result might fail" → "our theory passes its own predicted falsification test."

**Section structure:**
- 5–8 enumerated items (First, Second, ...).
- Each item references the appendix where it's reported in detail.
- Closing summary table explicitly says "robust across all N dimensions."

**Sentence-level discipline:** single-sentence items are fine if the appendix carries the detail. Don't bloat the robustness prose.

## 2.9 Further analyses / extended results

For analyses beyond the pre-registered hypotheses:
- Industry / sector / context heterogeneity is a strong addition.
- Be explicit when an imprecisely-identified split qualifies the main story (don't bury it).
- Don't promote these findings to "headline" status; they extend, qualify, or contextualize.

## 2.10 Discussion / Conclusion

**Structure varies by field:**
- Single Conclusion section (economics, finance — often combines summary, implications, limitations).
- Discussion → Theoretical implications → [Practical / Policy / Managerial implications] → Limitations → Future research (management, OB, IS, policy).
- Discussion → Implications → Limitations (sociology, education).

**Regardless of structure, include:**
- **Summary paragraph**: restate the puzzle, the answer, and the central message. Echo the introduction's framing language so the cover letter, introduction, and conclusion all use the same key terms.
- **Theoretical contribution**: tie each contribution to a literature stream. Use a unifying-premise sentence.
- **Practical / policy / managerial implication** if relevant to the field. Open with a one-sentence message.
- **Limitations**: honest about real limitations. For marginally significant findings, acknowledge precision limits explicitly.

---

# PART 3 — Cross-section consistency

## 3.1 Method ↔ Results commitments

Every commitment in the methods section must be honored in the results section.

Items to audit:
- Sample size declared in §3.X nested-sample design ↔ table cells and prose in §4.
- Sample restriction (e.g., NAICS 51 excluded, sector restriction) ↔ table footers.
- Estimator promise (TWFE OLS, IV 2SLS) ↔ table column labels.
- Headline outcome variable ↔ table dependent variable rows.
- Control variables ↔ table footers.
- SE clustering ↔ table footers.
- Z-standardization / transformations ↔ table column or footer.
- Instrument set ↔ table footer diagnostic rows.
- Hypothesis sign prediction ↔ reported coefficient sign.

## 3.2 Cover letter ↔ paper framing parity

Whatever framing the cover letter promises (puzzle, key concept, takeaway phrase), the abstract / introduction / discussion must deliver in the same language. A sharper cover letter than the body is a desk-reject risk — the editor opens the manuscript expecting the cover-letter framing and feels misled if it's softer in the body.

Match the key phrases verbatim across:
- Cover letter
- Research / academic abstract
- Introduction puzzle paragraph
- Introduction contributions paragraph
- Discussion summary paragraph

## 3.3 Numerical consistency 4-way audit

Whenever a number appears in the manuscript, verify it matches across all four locations:

1. **Source script** (regression outputs, lock files).
2. **Body prose** (paragraphs that report the number).
3. **Table cells** (the table that displays the number).
4. **Table footers / notes** (sample sizes, diagnostic stats).

Common failures:
- Body says "10,553 firm-years" but the table footer says "10,550" because of a re-run.
- Body says "F = 59.0" but the table cell says "59.02".
- Appendix intro claims "supports H1" but the appendix table shows a ns coefficient.

Build a numerical-consistency audit. Don't trust manual proof-reading for this.

## 3.4 Self-contradiction detection

Common self-contradictions to audit:
- Appendix intro claims a finding "supports H1" but the appendix table shows a ns coefficient.
- Body says one sector is strongest but the table shows another sector strongest.
- Sample size in prose differs from sample size in table footer.
- Hypothesis statement uses different sign / direction language from the result paragraph.

## 3.5 Leftover detection (stale prior-version content)

When a paper goes through major revisions, leftover prior-version content tends to remain hidden in:
- Sub-section openings (e.g., "third and fourth test demand-side mechanisms" when H4 has been changed to a supply-side mechanism).
- Hypothesis preview paragraphs.
- Appendix intros.
- Robustness summary statements.
- Cover letter framing.

Run a leftover-detection scan: search for terms used in the old version but no longer applicable. Common targets: old hypothesis labels, old sample sizes, old coefficient values, old framework names.

User signal: "leftover가 없는지 섹션별로 문단별로 꼼꼼히 살펴보고."

## 3.6 "Important parts can repeat" rule

This is a calibration signal from the user. The user does NOT want every repetition stripped — only redundant restates within the same section or between Method and Results sections.

**Always preserve these repeats:**
- Hypothesis statements ↔ result narrative (necessary linkage).
- Methods-section measurement argument referenced in multiple appendix preambles (each appendix needs self-contained context).
- Citation blocks of standard sets of references (standard reuse).
- Cover letter framing echoed in abstract, introduction opener, and conclusion summary (consistency is critical).

**Acceptable to trim:**
- Within-section paragraph-pair near-verbatim restates.
- Method-section content restated in Results without need.
- Discussion-section content restated in Conclusion without need.
- Appendix-internal restates within the same appendix subsection.

User signal: "중요한 부분은 여러번 해도 되니까 그런 부분은 빼면 안되."

## 3.7 Concept-discovery audit

When the author introduces or invents a novel construct, audit where it appears in the manuscript:
- Is it defined clearly when first introduced?
- Is it elevated to a key role in the contributions / mechanism story?
- Is it consistently named across sections (not slightly different labels)?
- Is it referenced in the cover letter / abstract?

When a novel construct is under-emphasized, elevate it.

User discovery pattern: "[novel construct] 써있긴 했는데 이거 어디에 썼는데?" — the user realizes a key construct is buried.

---

# PART 4 — Prose craft

## 4.1 Concise sentences

- Target median sentence length ≤ 25 words.
- Flag sentences > 40 words for splitting.
- Avoid sentences with 3+ independent clauses joined by semicolons or em-dashes.

**Splitting rules:**
- When splitting, do NOT drop substantive content. Split one long sentence into 2–3 shorter ones.
- Coefficient-heavy sentences are acceptably long because the density is necessary; just ensure the surrounding prose introduces and concludes them cleanly.

User signal: "줄여" / "shorten" / "간결한 문장 스타일."

## 4.2 Paragraph "bumper" detection

When reviewing prose, scan for paragraph pairs where the next paragraph's first sentence has neither a transition cue (However, First, Second, Together, Specifically, Therefore) nor a shared topical keyword with the previous paragraph's last sentence. Add a bridge.

Bumper patterns to fix:
- Methodological setup paragraph → result paragraph without a "Table N reports..." or "We turn to..." bridge.
- Theory paragraph → empirical paragraph without a "We test this prediction..." bridge.

## 4.3 AI-fingerprint cleanup

When revising AI-generated or AI-assisted prose, watch for and remove:
- Random bold formatting where no emphasis is needed.
- Excessive hedge words ("perhaps", "potentially", "in some sense").
- Generic transition phrases ("Furthermore", "Moreover", "Additionally") used where a content-bearing connector would be sharper.
- "It is important to note that..." / "It should be emphasized that..." preambles — delete and put the content directly.
- Repeating the same point in slightly different words across adjacent sentences.
- Overuse of em-dashes for parenthetical insertion when commas or new sentences would do.
- Listing the obvious as if it's insight ("the data show that..." when followed by a result already stated in the table).

User signal: "AI가 쓴 것 같은 문장 다듬어" / "갑작스러운 bold 삭제."

## 4.4 No mathematical notation in body prose

Do NOT write formal notation like `X_i = 1[∃ past job with signal]` in body paragraphs. Use prose:
> "X is an indicator that equals one when the worker's career history contains at least one job classified with the relevant signal."

Reserve formal notation for **equation blocks only** (between equation and "where..." paragraph). In body prose, write the same content as natural English.

In hypothesis statements: NEVER use ×, ≥, ≤, ∈. Use prose equivalents.

## 4.5 Forward-reference discipline

Keep cross-references genuine (Section 3.7 IF the reader actually needs to jump there) but minimize them. Avoid forward references in:
- Introduction contributions paragraph (don't say "developed in Section 7.2").
- Abstract.
- Cover letter.

Cross-references are fine in Methods, Results, Robustness — where they help the reader navigate. They're noise in the front-matter, where the reader is still deciding whether to read on.

## 4.6 Variable italicization

Italicize variable names, regression terms, and short code-like tokens when they appear in body prose: *X_imp*, *log_ppent*, *bg_x_hybrid*.

Tables, footers, and equation blocks have their own conventions; italicize variables in body prose.

## 4.7 No author-name branding for methods

Do NOT brand your own paper's methods or variables with another author's name. For example, rename "Park-imputed controls" → "imputed controls" or "industry-year median fill." Cite the source paper for the method in the methods section, but don't make the source author's name part of your variable label.

User signal: "이런식으로 쓰지말아줘. [author]-imputed 이런거."

---

# PART 5 — Empirical conventions

## 5.1 Lock-file methodology

For papers with substantial empirical content, adopt a lock-file pattern:
- Save key numerical results (coefficients, SEs, p-values, sample sizes, F-stats, diagnostic stats) to versioned JSON files (e.g., `_phase4_main_lock.json`).
- Audit scripts cross-check that prose claims and table cells in the manuscript match the lock-file values exactly.
- Whenever a regression is re-run, the lock file updates and audits re-verify.

This catches the most common reviewer-killer: prose says "β = 0.981" but the table says "β = 0.987" because someone updated one and forgot the other.

## 5.2 Sample-shrinkage default → imputation

When introducing a new control variable shrinks the sample significantly (e.g., R&D-to-sales is missing for 40% of firm-years), the default response is to impute, not to accept the sample loss.

Standard imputation pattern:
- Industry × year median fill (the granular cell).
- Year-median fallback when the industry-year cell is itself empty.
- Winsorize at 1st and 99th percentiles to limit outlier influence.

When a sample shrinks unexpectedly, propose imputation BEFORE the user has to ask.

User signal: "sample을 많이 까먹지 않아? imputation을 진행하면 어때?"

## 5.3 Sample restriction must match the outcome variable

When the outcome variable changes across hypotheses (e.g., outcome A = continuous productivity measure, outcome B = bounded share), reconsider the sample:
- Continuous outcomes can use the full base panel.
- Share outcomes typically require the sample where the denominator is nonzero.

When changing the outcome, audit the sample-restriction logic.

User signal: "[hypothesis] dependent가 share인데, ai intensity가 0보다 큰 sample에서 진행해야 되는건 아닌가?"

## 5.4 Time-window consistency across hypotheses

All hypotheses should use the same time window unless there's a theoretical reason for different windows. If H1/H2 use 2014–2023 and H3 uses 2016–2023 without substantive justification, reviewers will note the inconsistency.

When a sub-window or restriction differs, justify substantively in the methods section.

User signal: "h1, h2와 time이 다른건 이상해. h1, h2와 가장 유사하게 하는 방향에서 찾아봐."

## 5.5 Domain (sample-universe) consistency

If the paper restricts to a domain (e.g., "AI-using industries"), this restriction should apply uniformly across all main hypotheses unless theoretically motivated otherwise.

If H2 restricts to the domain but H1 doesn't, H1 is identified on a different universe than H2 and the comparison is muddled. Apply uniformly.

User signal: "h1에도 [domain restriction]이 들어가야겠지."

## 5.6 Significance-threshold honesty

The user is aware of conventional thresholds (p < .05, p < .10) and reacts when a coefficient sits clearly outside them.

- p = .149 → not significant at any conventional level. Don't fudge as "marginal" or "approaching."
- p = .077 → can be called marginal (10% level), but always present with caveats.
- p = .046 → cleanly significant at 5% level.

Don't oversell. If a coefficient is not significant at any conventional level, say so plainly.

User signal: "[p-value]면 * 하나도 못띄우는거 아냐?"

## 5.7 Coefficient sign / hypothesis prediction sanity check

For every hypothesis, audit: does the sign + ranking of the reported coefficient match the hypothesis prediction?

- "H2 says X > Y" → table must show X coefficient larger than Y coefficient.
- "H4 says high-Z firms amplify the X effect" → high-Z subsample coefficient must exceed baseline.

If the predicted sign reverses, EITHER the hypothesis must be re-stated OR the specification must be re-examined. Don't continue with stale hypothesis statements after regeneration.

User signal: "[H_x]는 hybrid보다 specialist가 coef가 더작은데 지금 그러면 가설이 성립 안되는거 아냐?"

## 5.8 Within R² for fixed-effects regressions

For FE regression tables, report:
- Coefficients with SE in parentheses and exact p-value in brackets (convention varies by journal).
- Fixed-effect indicators (Firm FE: Yes; Year FE: Yes).
- Cluster type (firm × year clustered, firm-clustered, etc.).
- Sample restrictions.
- Sample size: Observations + Firms (or other grouping unit).
- **Within R²** (especially important for FE regressions).

Don't skip Within R² for FE specifications — reviewers will ask.

## 5.9 "Best split" methodology for sample partitions

When choosing a sample-partition criterion (quartile vs median, threshold like ≥5 vs ≥10):

1. Run several reasonable splits.
2. Identify the cut(s) with clean theoretical interpretation AND clean significance.
3. Use the cleanest cut as the main-text headline.
4. Report the alternative cuts as robustness checks in the appendix.

This is NOT cherry-picking when:
- The chosen cut has a substantive theoretical justification.
- All alternative cuts are reported transparently in the appendix.
- The ranking pattern is preserved across alternatives (even if precision varies).

User pattern: "둘 다 해보고 잘나오는 것으로. 안나오는건 robustness check로 appendix로."

## 5.10 Reuse existing analyses; don't invent results

When asked for a new analysis, FIRST inspect the project folder for existing regression outputs, lock files, or supplementary scripts. The user has typically already run dozens of robustness specifications.

Never generate fictional regression numbers. If a needed regression hasn't been run, say so explicitly: "I don't see this specification in the existing outputs — should I run it via the script, or use a placeholder until it's run?"

User signal: "지금 이 폴더에 있는 여러 분석들 잘 보고 그 분석에서 추가하는 형태로 지정해야되."

## 5.11 Control-variable citation convention

When introducing control variables, cite the prior papers that have used the same controls in similar settings. This signals to reviewers that the control set follows established conventions and isn't ad hoc.

Add citations from the field's leading exemplars for each control type.

User signal: "controls를 설명하는 부분에는 참고문헌이 이것밖에 없는건 이상하니..."

---

# PART 6 — Robustness and honest framing

## 6.1 Cherry-pick perception management

When a finding is identified at one specific specification but attenuates under alternatives, the natural framing — "our result only works under this specification" — sounds like cherry-picking.

The reframe: convert the attenuation pattern into a **prediction test of the underlying theory**. If your measurement / horizon argument predicts attenuation under alternative residuals or horizons, then observing that attenuation SUPPORTS the underlying argument rather than undermining the main result.

User flag phrase: "이거 cherry picking 같자나."

When you see this concern, NEVER simply add more robustness; reframe the existing robustness as predicted by the paper's own theory.

## 6.2 Marginal significance acknowledgment

When a key finding sits at p ≈ .07 or p ≈ .10:
- Acknowledge in Limitations explicitly — sample size limits, partition mechanics, etc.
- Reframe as directional pattern + ranking reversal if a clean rank ordering across subsamples exists.
- Add complementary robustness (e.g., a median-split alternative that preserves the directional pattern with larger subsamples).
- In the cover letter, own the precision limitation but emphasize the structural pattern.
- Don't oversell. Reviewers will catch it.

## 6.3 Tone-down for over-interpretation

When a finding stretches beyond what the data shows, soften the language. Common reviewer-red-flag patterns to avoid:

| Over-claim | Tone-down |
|---|---|
| "X channel runs through Y" | "Y carries the identification" |
| "ranking reversal" | "ranking differs across subsamples" |
| "markedly amplified" | "point estimate is larger" |
| "supports a causal interpretation" | "is consistent with the mechanism" |
| "demonstrates" | "shows" / "is consistent with" |

User signals: "리뷰어가 뭐라 하지 않겠어?", "이렇게 해석하는게 가능한거야?", "이것도 해석의 비약은 없는지 살펴봐줘."

When the user asks these questions, soften the interpretation to match the data's actual precision.

## 6.4 Negative result honesty

If 3 of 4 mechanism panels support a prediction and 1 doesn't, say "supported in three of the four panels" — don't claim universal support. Use "null exception" or "imprecisely identified" rather than evasive phrasing.

---

# PART 7 — Figures and tables

## 7.1 Figure necessity check

Every figure must satisfy: does this figure strengthen the paper's claim? If yes, keep in the main paper at a deliberate location. If only illustrative, move to appendix. If no purpose, delete.

User signal: "이거 의미가 있는건가? 논문에 주장을 강화할 의미가?"

If you can't articulate WHY the figure is in the main paper in one sentence, it shouldn't be in the main paper.

## 7.2 Figure design rules

- No overlapping legends and data series.
- When comparing multiple series, align Y-axis scales (e.g., 0.05 increments across panels). When magnitudes differ across series, still align the step size if possible.
- "0" tick should sit at the X-axis baseline, not floating above it.
- Panel separation for crowded plots — when 2-3 series visually crowd each other, split into separate panels.
- Match figure-caption format to the table-note convention used elsewhere in the paper.

## 7.3 Table format conventions

- Match table format to a recent exemplar paper in the same field (citation density, row order, footer style).
- Coefficient cell convention: coefficient / (SE) / [p-value] is one common pattern; another is coefficient with significance stars.
- Sample size and firm count as separate rows.
- Within R² (and overall R² if relevant) for FE regressions.
- Standard footer items: fixed-effects indicators, cluster type, sample restrictions, control variables.

## 7.4 Bundle / composite-index skepticism

Composite indices and bundles often appear in early drafts (because they're easy to compute) but rarely carry theoretical weight. Question every composite in a table.

A composite is justified ONLY if:
- The constituent variables are theoretically argued to combine into one construct.
- The composite tells a different story than the components do separately.
- The components are not separately interpretable in their own right.

Otherwise, remove the bundle and report the components directly.

User instinct: "이 표에 bundle이 들어갈 필요가 있을까?"

## 7.5 Reference-paper format matching

When asked to match the format of a related paper, inspect the reference paper's:
- Table structure (which rows are reported, in what order, which footers).
- Equation notation conventions.
- Section ordering.
- Hypothesis-statement format.
- Citation density.

User signal: "[reference paper]과 모양 맞추고."

---

# PART 8 — Submission package

## 8.1 Cover letter — editor's perspective

Write from the editor's perspective: what helps the editor positively decide to send the paper for review?

**6-paragraph structure (≈500 words, A4 single page at 1.15 line spacing):**

1. **Hook** — open with the puzzle in the literature (not "I am pleased to submit"). Cite 2–4 prior works as positioning.
2. **What this paper does** — the novel angle + headline finding with specific numbers.
3. **Mechanism / theoretical anchor** — nested mechanism tests + extension of established frameworks.
4. **Method credibility** — brief mention of identification design + diagnostics (F-stat, over-id test).
5. **Why journal readers will care** — open new analytical layer + field relevance.
6. **Standard declarations** — author count, no prior publication, no review elsewhere, no conflicts.

**Italicization conventions:**
- Title (italic).
- Journal name (italic).
- Key technical concepts on first mention (italic).

**Letterhead and signature:**
- Right-aligned letterhead with author info at top (include degree such as "Ph.D." after name where appropriate).
- Date, recipient block, salutation.
- Body paragraphs.
- Signature block at bottom matching the letterhead format.

## 8.2 Title page (separate file for double-blind submission)

Only relevant if the journal uses double-blind review. Check the target journal's guidelines.

For double-blind: prepare a SEPARATE title page document with author info; the manuscript itself stays blind.

Typical contents:
- Title (large, centered).
- Author name with degree.
- Affiliation (department, school, institution, address).
- Email, ORCID.
- Corresponding author block.
- Acknowledgments (separate from manuscript).
- Funding statement.
- Conflicts of interest.
- Cross-reference to Data Availability Statement.

For blind submission, also anonymize document properties (`dc:creator`, `cp:lastModifiedBy` in docx metadata). No author info, no acknowledgments, no funding mentions in the manuscript itself.

## 8.3 Data availability statement

Many journals now require this either as a separate file or as a submission-portal field. Standard sections:
- Manuscript title + author.
- Data sources (each commercial/restricted source listed with access details).
- Code availability (e.g., public repository upon acceptance).
- Replication conditions.
- Restrictions (NDA terms, redistribution limits).

## 8.4 Self-citation handling in blind submission

If the author cites their own prior work in a double-blind submission, verify with the user:
- If self-citation, anonymize in references ("[Anonymized for review] et al., YYYY") OR cite in third person to avoid revealing authorship.
- If different author with same name, leave as-is.

When the author's surname appears in references, always check.

## 8.5 Acceptance-probability framing

When the user asks "what's the chance of acceptance?":
- Top journals typically have base accept rates of 7–10%.
- A paper that meets standard publication quality starts at the base rate, not below.
- Specific risks (marginal significance, weak fit) lower the probability; strong novelty / rigor / fit raise it.
- Don't catastrophize. The 7–10% base rate is the field's normal selection ratio.

When the user asks "is it under 10%?", give the base-rate context first, then the paper-specific assessment.

## 8.6 Journal-fit framing trade-offs

Different top journals favor different framings of the same empirical content:
- Strategy-leaning journals favor theory-driven / resource-based / capability framing.
- Methodology-leaning journals favor identification rigor / causal-inference / structural-modeling framing.

The same paper can be reframed for different journals by shifting which framework anchors the contributions paragraph and the discussion.

When deciding journal fit, consider both the theoretical anchor of the paper AND the editorial board's typical preferences.

---

# PART 9 — Workflow tools

## 9.1 Word-comments memo extraction

The user often leaves Word comments on a docx and asks for them to be resolved.

Extract comments via `word/comments.xml` (a member of the docx ZIP). Each `<w:comment>` element has:
- `w:id` — comment ID.
- `w:author` — comment author.
- `w:date` — timestamp.
- Inner text — the comment content.

Anchor text is in the main document via `<w:commentRangeStart w:id="N"/>` ... `<w:commentRangeEnd w:id="N"/>` markers. Extract the text between these markers to know what the comment refers to.

Resolve each comment substantively in the source script; re-run audits; report which memos were resolved.

## 9.2 Script-regen workflow caveat

When the manuscript is generated by a script (python-docx or similar), **script regeneration WIPES Word comments / track changes / manual edits.**

Workflow:
1. User opens v_n.docx, makes manual edits + adds memos.
2. User saves as v_n_NEW.docx (or similar backup name).
3. Before regenerating, EXTRACT comments from v_n_NEW.docx.
4. Apply resolution edits to the source script.
5. Regenerate the docx.
6. Communicate this rebuild loop explicitly to the user.

If you accidentally overwrite the annotated docx, be honest about the loss and ask the user to either restore from OneDrive / Windows File History or re-paste the memos.

## 9.3 md vs docx ground truth

When a manuscript exists in both `.md` and `.docx` forms, treat the docx as ground truth. The md is typically the older form-of-content; the docx has the user's manual edits + memos.

When the two diverge: read the docx for the current state. Update the md (or treat the md as obsolete) — never go the other direction.

User signal: "md와 두개가 똑같지 않아. 이 메모들은 docx기준으로 봐야되."

## 9.4 Save key state to md for future sessions

When a major decision is made or a key analysis is completed, save the rationale + findings to a markdown file in the project directory. This survives compact summaries and provides recoverable context.

What to save:
- The decision (e.g., "replaced H4 from role-demand to translator-supply").
- The substantive reasoning.
- The key numerical outputs (coefficient, p-value, sample).
- A pointer to the lock file or script that generated the numbers.

User instruction pattern: "지금 이 내용도 md로 저장해주고."

## 9.5 Version naming

Standard pattern: `v1.docx`, `v2.docx`, ..., `v17.docx` (or similar incrementing).

When the user makes manual edits + adds memos:
- Save as `vN_NEW.docx` (or `vN_with_memo_replies.docx`).
- Use the NEW file for memo extraction.
- After resolution, save as `v(N+1).docx`.

Keep both files until the user confirms the resolution is complete.

---

# PART 10 — Audit script catalog

For complex empirical manuscripts, build a battery of automated audits. Each audit is a self-contained Python script under a `scripts/` subdirectory with naming convention `_*_audit.py`.

**Audit types to consider:**

| Audit | What it checks |
|---|---|
| Section-by-section | Each section has expected content; hypothesis declarations; table mentions. |
| Body coherence | Claim consistency (H supported claim present, hypothesis-statement-precedes-result-claim, no stale prior-version language). |
| Appendix consistency | Appendix cross-references resolve; appendix tables match main-text framing. |
| Comprehensive lock | Every locked coefficient appears in the manuscript at the correct cell. |
| User style | Specific user-preference checks (acronym expansion, italic conventions, naming). |
| Logic flow | Section sequence; hypothesis sequence; forward-ref resolution; paragraph adjacency. |
| Method ↔ Result consistency | Every methods commitment honored in results. |
| Sentence length + paragraph bumper | Per-section sentence statistics + paragraph transition checks. |
| Cross-section duplication | Token-shingle 8-gram scan to flag near-verbatim restates. |
| Memo resolution | Each Word comment resolved and verified. |
| Journal-format | Page count, abstract length, margins, fonts for target journal. |
| Editor walkthrough | Print title, abstract, intro paragraphs, results section openings, robustness items, discussion contributions, in order. |

**Audit script structure:**
```python
"""<one-line description>"""
import sys, io, re
from docx import Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DOCX = r"<absolute path>"
doc = Document(DOCX)
paras = [(i, p.text.strip()) for i, p in enumerate(doc.paragraphs)]
BODY = "\n".join(t for _, t in paras)

results = []
def check(label, cond, info=""):
    status = "[PASS]" if cond else "[FAIL]"
    print(f"  {status} {label}" + (f" — {info}" if info else ""))
    results.append((label, cond))

# ... checks ...

passed = sum(1 for _, ok in results if ok)
print(f"\n{passed} / {len(results)} checks passed")
```

---

# PART 11 — Pre-submission checklist

Before declaring a manuscript ready for submission:

- [ ] All numbered hypotheses declared in the hypotheses subsection with brief declarative statements.
- [ ] Results subsections open with deductive punchlines, not "Table N reports...".
- [ ] Robustness items framed as prediction tests.
- [ ] Introduction contains NO hypothesis labels, NO specific coefficient numbers, NO "developed in Section X.Y" forward refs.
- [ ] Discussion echoes introduction framing language.
- [ ] Cover letter ↔ paper framing parity verified.
- [ ] Marginally significant findings honestly acknowledged in Limitations.
- [ ] Cross-section duplication scan run, only acceptable repeats remain.
- [ ] Method ↔ Results consistency audit passes.
- [ ] Numerical 4-way consistency audit passes.
- [ ] Sentence-length per-section median ≤ 25 words.
- [ ] Title page, cover letter, data availability statement prepared as separate files (if journal requires).
- [ ] docx metadata anonymized for blind submission.
- [ ] Self-citations handled appropriately for blind submission.
- [ ] All audit suites pass.

---

# PART 12 — User feedback pattern reference

| User signal | Meaning | Response |
|---|---|---|
| "줄여" / "shorten" | Sentences or paragraphs are too long. | Split long sentences (>40w). Trim filler. Do NOT drop substance. |
| "잘 안 와닿는데" / "doesn't connect" | A claim or distinction is unclear. | Make the distinction more explicit. Add a "stops at the X margin" or "does not link Y to Z" clause. |
| "별로다" / "not great" | Specific stylistic preference being violated. | Ask which aspect, OR examine context for specific issue (hypothesis labels in intro, numbers in intro, forward refs, jargon). |
| "두괄식으로" / "deductive" | Section/paragraph starts with setup but should start with punchline. | Move the headline claim to the opening sentence. |
| "수정해" with no detail | Comment usually has an anchor — read the anchored text. | Extract the comment's anchored text. Look at the surrounding paragraph. Infer what's wrong. |
| "확인해" / "verify" | The user wants an audit, not a re-write. | Run audits. Report results honestly. Don't re-edit unless the audit fails. |
| "에디터 입장에서 봐줘" / "editor perspective" | Check for desk-reject risk; strengthen fit/novelty/rigor framings. | Walk through title → abstract → intro → results → discussion as an editor. Identify fit, novelty, rigor, reviewability, red flags. Report. |
| "한번 더" / "one more time" | Re-verify; changes might not have taken effect. | Re-run the relevant audit. Show specific PASS/FAIL outcomes, not "looks good". |
| "잠깐" / "wait" | Pause the active revision flow for a sanity check. | Stop editing. Answer the pause-question. Wait for direction. |
| "이건 질문인데" / "just a question" | Information request, not revision request. | Answer precisely. Do NOT start editing unless asked. |
| "권한 묻지말고" / "don't ask permission" | Routine edits — just do them. | Default to action for typos, sentence trims, memo resolution, audit runs, rebuilds. |
| "옵션 [A/B/C]로" / "option [A/B/C]" | Picking from a presented list of options. | Apply the chosen option. |
| "이거 cherry picking 같자나" | Worried current framing reads as cherry-pick. | Reframe attenuation as prediction-test of the underlying theory. |
| "integrity 측면이 중요해" | Internal consistency is the priority. | Add an integrity audit. Cross-check claims, numbers, hypotheses, framing for alignment. |
| "[number]면 * 하나도 못띄우는거 아냐?" | Significance threshold awareness. | Don't oversell. Match language to actual significance level. |
| "AI가 쓴 것 같은 문장" | AI-fingerprint cleanup request. | Remove random bold, hedge words, generic transitions, repetition padding. |
| "리뷰어가 뭐라 하지 않겠어?" | Worried about over-interpretation. | Soften causal/strong claims to match data's actual precision. |
| "다른 컴퓨터에서도 활용하고 싶어" | Wants portable skill. | Skill is at `~/.claude/skills/`; user copies the directory to the new machine. |

---

# Installation on another computer

This skill lives at `~/.claude/skills/academic-paper-writing/SKILL.md` (user-level, not project-local).

**To use on another computer:**
1. Copy the entire `academic-paper-writing/` directory to `~/.claude/skills/` on the new machine.
2. The skill is auto-discovered by Claude Code on the new machine.
3. Auto-trigger: when a user asks for help with empirical paper drafting, revision, or audit work, the skill description matches and the skill becomes available.
4. Manual invocation: `/academic-paper-writing` (if Claude exposes it as a slash command in your environment).

**Path on different operating systems:**
- Windows: `C:\Users\<username>\.claude\skills\academic-paper-writing\`
- macOS / Linux: `~/.claude/skills/academic-paper-writing/`

**To sync via cloud:** put the skill in a Git repository or a cloud-synced folder (Dropbox, OneDrive, iCloud) and symlink from `~/.claude/skills/`.
