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
- Close on a defensive retreat. Scope caveats ("These associations do not identify causal effects", "though sparse capacity limits the test") must NOT be the abstract's closing move — the abstract closes on substantive content: the contribution, the mechanism, or the thesis (e.g., "That composition accumulates slowly through careers, making it hard for competitors to replicate."). Scope caveats live in the methods and limitations sections; if one is truly essential in the abstract, fold it into a mid-abstract clause, never the final sentence.

User signal: "지금 물러서는 defensive한거 말고 다른 중요한 내용을 넣는게 좋겠어."

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

### 2.4a Theory section (§2.x) is a literature review, NOT hypothesis prep

§2.x (theory) and §2.3 (hypothesis development) play distinct roles. Don't blur them:

**§2.x — Literature review:**
- What the field has documented about the phenomenon (adoption trends, workforce patterns, prior empirical findings).
- What existing research designs have done (demand-side surveys, supply-side resume work, exposure indices).
- The observed gap that this paper fills.
- Cite the literature; describe its findings; characterize its limits.

**§2.3 — Hypothesis motivation:**
- "We expect X to be related to Y" reasoning lives HERE, not in §2.x.
- Theoretical foundations applied to the specific prediction (ACAP, complementary-assets, KBV, etc.).
- One development paragraph per hypothesis, then the hypothesis statement.

A common drift: theory section starts as a lit review but slides into "We expect domain-background workers to be more productive..." That's hypothesis-prep prose; move it to §2.3.

User signal: "이 아래 부분은 가설에 나올만한 얘기같지. 지금 [§2.x]에서 나올만한 얘기는 그런게 아닌것 같은데."

### 2.4b No specific industry-name lists in the theory section

In theory paragraphs, prefer general phrases ("AI-using industries", "data-intensive sectors", "regulated services") to specific industry enumerations ("manufacturing, healthcare, finance, and retail").

The specific industries belong in the sectoral results subsection, not in the theoretical setup. Theory should be abstract enough to apply across the empirical contexts the paper actually tests.

User signal: "이런 구체적인 industry name이 필요하진 않겠어."

### 2.4c Concrete classification examples belong with the hypothesis, not buried in method

When the paper introduces a typology (Specialist vs Hybrid vs Translator, exploit vs explore, junior vs senior), the concrete worker/firm-level example that pins down the distinction should sit in §2.x near where the typology is introduced or in §2.3 near the relevant hypothesis — NOT buried in §3 method.

The reader needs the concrete distinction *before* reading the hypothesis. If the example only appears in §3.5, readers absorb the hypothesis with an abstract typology and have to flip forward to disambiguate. Move the example up; leave §3 with a brief cross-reference.

For multi-category typologies, reinforce the distinction repeatedly: §1 intro mention → §2.x example → §2.3 hypothesis re-emphasis → §4.x result-paragraph reminder → §7.2 discussion framing. Repetition makes the distinction stick.

User signal: "지금 예시가 그 method에 있을텐데 그거 hypothesis 설명하는 쪽으로 올리는게 좋겠어. 반복적으로 쓰는게 중요하겠네."

### 2.4d Causal direction explicit when summarizing prior literature

When summarizing prior empirical findings, write the causal arrow explicitly. "When firms invest in AI, they subsequently grow faster" — NOT "firms that grow faster have AI investments." The first sentence preserves the direction the prior literature established (AI → growth); the second sentence reads as if growing firms are selected on AI investment, reversing the arrow.

User signal: "이건 좀 이상해. 그러니까 ai를 투자하는 기업이 조직을 빠르게 확장한다라고 나와야지. 지금은 조직을 확장하는 기업이 포착되는 것처럼 서술된것 같아."

### 2.4e Each hypothesis subsection stays in its own lane; theory cites no data

When the theory section is organized one-subsection-per-hypothesis (§2.2 = H1, §2.3 = H2, §2.4 = H3):
- A hypothesis subsection develops ONLY its own hypothesis. Do not pre-empt the others there — no "H2 will be larger", no inverted-U / H3 prediction, no naming the technology-transfer-vs-general contrast inside the H1 subsection. The H1 subsection argues only that the tie, in itself, helps.
- The theory section makes NO reference to the analysis data or its coding — e.g. "SDC codes licensing and joint development under one flag", "rarely coincide in our data", "the dimension our records measure". Data-construction caveats live in §3.2 (Variables); the theory stays conceptual.
- The theory section does NOT forward-reference specific regression columns ("column (4) of Table 3 isolates…"). State the idea conceptually; the column belongs in Results.
- A bridging "empirical-signature map" that pre-announces which result distinguishes each mechanism is itself H2/H3 material; keep it out of the H1 subsection and let Results carry the discrimination (rephrase any later "the Section 2.2 signature map" back-reference to "the mechanisms of Section 2.2").

User signals: "2.2는 H1 설명 섹션인데 H2, H3 얘기가 들어있다 — 다 지워"; "2에서는 분석 데이터(예: SDC) 얘긴 하면 안돼."

### 2.4f Post-exploratory papers: rival explanation, provenance note, never a reversed hypothesis

When a paper is built on data that was already explored (a second paper from an archived candidate analysis, a null that became the headline), the HARKing guardrails are:

- **Never reverse a failed prediction.** If the original documented hypothesis predicted positive and the data returned null, do NOT restate it as "we predicted no effect." That is textbook HARKing and it is checkable against the archive.
- **The theoretically favored direction stays the hypothesis; the post-hoc account becomes the rival explanation** in adjacent prose, with its evidence assigned to an RQ (full form in §2.5a). Do not bundle the two into one "competing-predictions hypothesis."
- **Provenance note** in the methods: a short paragraph stating (i) the paper's data genre, (ii) that hypotheses and analysis plan were documented before the estimation reported, (iii) which single framing was developed after seeing a result, and (iv) any shared-dataset/companion-paper overlap. Write it per §2.4g.
- Supported original hypotheses can be presented as-is when a documented pre-estimation record exists; the interesting null carries the discussion, not a retrofitted prediction.
- The fully honest upgrade path is a new confirmatory study (new data wave, pre-registered); when that is out of scope, an interpretive qualitative study (population-peer validation, mechanism adjudication) can carry the "why" question but must not be called confirmation.

User signal: "가설을 재밌게 바꿔도 되는지" — the answer is: reframe, never reverse.

### 2.4g Disclose the fact, not the confession

Provenance and limitation prose states what is true about the paper; it does not narrate the author's workflow in self-incriminating terms. Ordinary research practice is not a confession item: secondary analysis of existing survey or panel data is a legitimate genre, and nobody writing on a public panel discloses "I looked at correlations before choosing a topic." Draft the paragraph so a fair reader learns the facts they need and nothing performs guilt.

| Confessional (cut) | Factual (keep) |
|---|---|
| "its data were first analyzed in a candidate-generation exercise in which stage-outcome associations, among other patterns, were examined" | "This paper reports a secondary analysis of a survey conducted for a broader institutional assessment." |
| "All hypotheses are therefore disclosed-exploratory-origin tests on non-independent data, not preregistered confirmatory tests." | "The hypotheses and the analysis plan were documented before the estimation reported here." |
| heading: "Transparency statement." | heading: "Data and analysis provenance." |
| abstract closer: "…with hypotheses of exploratory origin" | (nothing; the methods note carries it) |

Rules of thumb:
- **Frame by genre, not by autobiography.** Name what kind of study this is; do not narrate how the topic was chosen.
- **Never self-label in the accusation's vocabulary.** State positively what IS documented instead of announcing which purity standard the paper fails.
- **Scope the post-hoc admission to the one item that needs it, and only where it is load-bearing.** A rival explanation developed after a null is disclosed *because that is why the follow-up study exists* and why the results section says "awaiting independent test" — not as penance. If a disclosure supports no claim anywhere in the paper, it is decoration; cut it.
- **Keep unconditionally: shared-dataset and companion-paper overlap.** That is a publication-ethics duty (duplicate-publication screening), not a stylistic choice, and it belongs in the cover letter too.
- **Do not restate caveats that live elsewhere.** "Associations, not causal effects" belongs in limitations; archive inventories belong in the data-availability statement.

Test: would a fair reader learn a fact they need in order to weigh the claims? Keep it. Does the sentence mainly narrate process or perform humility? Cut it. (Adjacent bans: §4.8 stage directions; §2.2 defensive abstract closers.)

User signals: "이건 내 논문 작성 방식인데"; "자기 고발적 서술 안하도록 해줘."

## 2.5 Hypothesis statement format

- One- or two-sentence declarative statements.
- Use prose: "Hypothesis (H1). In X settings, A is associated with higher B."
- Never use math operators in hypothesis prose: ×, ≥, ≤, ∈. Replace with "interacts with", "at or above", "at or below", "in the set of".
- The mathematical specification belongs in the methods section, not in the hypothesis statement.

**Lean statements: the statement carries the core prediction only.** Scope conditions, operational definitions, and design context migrate into the surrounding theory prose:
- A scope condition shared by the hypothesis set (e.g., "outside the information-producing industry") is stated ONCE in the theory section as an applies-throughout sentence ("One scope condition applies throughout: ...") — not repeated at the head of every statement.
- Operational glosses ("tilts toward Hybrids, meaning Hybrids outnumber Specialists") live in the development paragraph before the statement; paired hypotheses can share one bridge sentence ("Both predictions compare Hybrid-tilted with Specialist-tilted firms.").
- Keep inside the statement only what is constitutive of the prediction: direction, construct names, and — for comparative hypotheses — the comparison group ("than Specialist-tilted firms" stays).

Worked example (one session's evolution):
- Overloaded: "Among firms outside the information-producing industry that hold an observed AI capability workforce, productivity is higher when Hybrids outnumber Specialists in that workforce than when they do not."
- Lean: "Productivity is higher when a firm's AI capability workforce tilts toward Hybrids rather than Specialists." (scope → the applies-throughout sentence; operational tilt definition → the development paragraph)

Calibration: when a statement reads ambiguous — a missing comparator, an undefined term — the FIRST fix is the development paragraph, not loading the statement. The hypothesis↔result-lede repetition of the core clause remains required (§3.6).

User signals: "가설 서술을 좀 명확하게 해야하지 않나?" then "가설에 너무 모든걸 담기보다는 핵심만 남기고 나머지는 가설을 설명하는 쪽에 쓰는게 어때?" — clarity comes from relocating context, not stuffing the statement.

**Mechanism hypotheses** (often labeled H3, H4) use a channel template:
> "The [main effect] in [main hypothesis] operates through [mediating variable Y]. The [outcome] is amplified in firms / settings where Y is present, and muted where Y is absent."

Avoid academic-jargon-heavy phrasings. The reader should grasp the mechanism in one read.

## 2.5a Research-question and hypothesis architecture

How RQs and hypotheses are formed, ordered, and related — hammered out across one full paper session; apply as the default.

**RQ form.** One interrogative sentence per RQ. No multi-barreled questions ("where does it create value, of what kind, at which stage, and where does it fail?" → "How does the perceived value researchers obtain from X vary across the stages of Y?"). No enumerated candidate lists inside the question — "(security, computing, verification, or capability)" belongs in the prose after the RQ, not in it. An RQ that presupposes a result ("Why does X fail to...?" before the null is shown) gets a neutral identification form instead ("Which constraints do researchers identify as binding...?").

**Ordering.** ALL research questions precede ALL hypotheses. RQ1 is the overarching question the hypothesis set decomposes (it should mirror the paper's opening question in the Introduction); narrower RQs (mechanism, qualitative-strand questions) follow it immediately, then H1...Hn. Do not interleave an RQ between hypotheses even when it logically attaches to one of them — attach it in prose instead ("RQ2 supplies the constraint logic's evidence through...").

**Hypothesis form is uniform.** Every hypothesis is a single declarative association/direction claim in the same grammatical shape ("X use at stage S is positively associated with Y, over and above Z"). Do NOT build a "competing-predictions hypothesis" that bundles two rival outcomes under one label (no H3-aug/H3-con sub-tokens — a reader meeting "aug/con" cold cannot parse them). The theoretically favored (and, in a disclosed-exploratory paper, the pre-specified) direction IS the hypothesis; the rival account lives in adjacent prose as "the rival explanation," with its evidence assigned to an RQ and its verdict language fixed in Results: "H3 is not supported; the observed signature is consistent with the [rival] logic," plus the post-hoc disclosure where applicable. This is also the honest alignment when the archived analysis plan pre-specified the positive direction.

**Multi-part hypotheses split.** H4a and H4b are separately stated, each preceded by its OWN one-paragraph derivation (mechanism → consequence → ordering claim), separated by blank lines. Never pack "(H4a) ... (H4b) ..." into one statement paragraph.

**Structure is shown, not narrated** (see §4.8): no "the overarching question is stated first," no "the hypotheses that follow decompose it," no "stated as a research question rather than a hypothesis." Headings, ordering, and labels carry all of that.

**Audit hooks.** Encode as script checks: all RQ paragraph indices < all hypothesis indices; expected count of "Hypothesis "-prefixed statements; no banned sub-tokens (H3-aug etc.); RQ labels absent from abstract/intro.

User signals: "rq가 좀 rq 스럽지 않네. 가설3번 좀 이상하고."; "모든 rq먼저"; "Aug con 이런건 뭔지 모르겠고"; "h4a, h4b처럼 두개의 가설로 되어있더라도 엔터쳐서 두개로 분리해주고 이에 대한 논리도 펴야지."

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

**Equation-rendering caveat (Word docx):** Native Word equations via OMML are hard to generate programmatically. The `pyommlbuilder` Python library produces minimal OMML that Word rejects. If the user wants native equations, the safest paths are (a) keep equations as plaintext in the script and let the user paste them into Word's equation editor manually, or (b) use a Pandoc-based LaTeX → docx pipeline. (Update: the pipeline latex2mathml → Microsoft Office's own `MML2OMML.XSL` via lxml XSLT produces OMML Word accepts, for both display `m:oMathPara` and inline `m:oMath`; give every `m:r` a `w:rPr` with Cambria Math and the body point size, placed after `m:rPr` and before `m:t`.)

### 2.6a Method subsection headings name the artifact, not the activity

Run-in heads (and method headings generally) inside the methods section must name **what the step produces for the paper** — the artifact or purpose — not the processing activity performed while building it.

Bad (work-log style — reads like notes taken while doing the work):
> Current-role classification
> Career-background classification
> Data cleaning and merging

Good (artifact/purpose style — names the output):
> Identifying the observed AI workforce
> Measuring hybrid and specialist composition
> Firm-year AI intensity

Heuristic: if the head could caption a step in a processing pipeline ("...classification", "...preprocessing", "...merging"), rename it to the measure, sample, or construct that the step delivers. Standard data-source heads ("Job postings", "Firm financials") and variable-name heads ("Firm-year AI intensity") already pass.

This is the methods-section counterpart of §2.9a (further-analysis headings preview the result).

User signal: "이렇게 달지말고 결과적으로 우리가 뭘 만드는지 목적에 맞는 소제목을 다는게 좋겠어. 이거는 지금 작업할때 한 얘기같은 소제목이자나."

### 2.6b Small-N qualitative components in mixed-methods papers

For an explanatory sequential design whose qualitative arm is a handful of interviews (3-5), the defensible framing stack is:

- **Name the role precisely**: interpretive triangulation / member checking / mechanism adjudication — never "confirmation," never a saturation claim. Result language caps at "consistent with."
- **Sample adequacy via information power** (Malterud et al. 2016), not saturation: narrow aim + population already characterized by the survey + theory-guided interviews all raise information power.
- **Theoretical purposive sampling matrix**: each informant profile tests a different face of the argument (the null's protagonist, the boundary condition, the beneficiary, the limit case, the rival-explanation holder). A "why 5?" reviewer question is answered by the matrix, not the count.
- **Structure each interview** as workflow walk-through → critical incidents (most recent success AND most recent abandonment) → member checking with the quantitative pattern shown on one page.
- **Re-contact consent check**: survey contact info collected "for prize fulfillment, destroyed after" CANNOT be used to recruit interviewees; recruit fresh from the same population, and keep the population definition identical to the survey's (a broader institute family is a population mismatch reviewers will catch).
- **Secondary use of qualitative data** (open-ended survey text already used in a companion paper): disclose the first use explicitly (salami-slicing defense), recode with the new paper's lens rather than re-reporting old codes, and reconcile count definitions in print (e.g., "171 non-empty fields, 149 substantive after removing placeholder entries" — the companion paper's count and yours must be derivable from each other).

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

### 2.9-note Descriptive / robustness tables are not a "Further analysis" dump

When pulling supplement content into the body, do NOT lump everything under one "Further analysis" heading. A matched-sample descriptive-statistics table belongs where the matched sample is described (§3.x identification); a robustness/sensitivity table belongs in the robustness subsection (§4.x) that discusses it. "Further analysis" is for genuinely additional analyses, not for descriptives or for robustness already narrated in Results. If the journal allows, dissolve a thin separate supplement and place each table at its natural discussion point. User signal: "매칭 표본 기술통계는 further analysis가 아니네 … 3nn 민감도도 그런것 같은데."

### 2.9a Further-analysis subsection headings use result-summary style

Subsection headings within "further analyses" (or extended results) sections preview the finding, not the test name.

Bad (test-descriptive):
> 6.1 Industry heterogeneity within the H2 composition test
> 6.2 AI use orientation
> 6.3 Junior–senior pairing within AI roles

Good (result-summary):
> 6.1 The hybrid advantage concentrates in manufacturing
> 6.2 Hybrid talent's payoff concentrates in exploration-oriented AI use
> 6.3 Cross-experience pairing matters in manufacturing

The reader sees the substantive result before reading the prose. This is the same deductive convention as §2.7 results subsections.

User signal: "어떤 test 이러지 말고 결과 요약을 소제목으로 쓰는건 어때?"

### 2.9b Sectoral / industry implications are "further analysis," NOT "theoretical implications"

Sectoral split results belong in §6 (further analyses) and should be mentioned in the limitations section if relevant, but they should NOT be cast as a separate "theoretical contribution" in §7.2. Theoretical contributions are paper-wide claims that extend or qualify literatures; sectoral splits are scope/heterogeneity claims that contextualize the headline finding.

A common drift: §7.2 lists a Third contribution as "the paper sharpens the interpretation of industry heterogeneity in AI returns..." This is dressing up a §6 finding as a §7.2 contribution. Replace with a main-analysis-driven theoretical implication (e.g., strategic human capital framing) and let the sector result speak for itself in §6.

User signal: "이건 지금 further analysis에 대한 거자나. 이거 말고 main 분석에서 시사점을 하나더."

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

### 2.10a Intro contributions and Discussion contributions must use the same ordering

The list of contributions in the Introduction's contributions paragraph (last paragraph of §1) and the list of contributions in the Discussion's theoretical-implications subsection (§7.2 or equivalent) must be the SAME contributions in the SAME ORDER.

If you reorder one (e.g., ACAP-first instead of utilization-shift-first in §7.2), reorder the other to match. Readers compare these two lists; mismatched orderings or substituted entries read as inconsistency.

When applying paper-wide reframing, audit both lists side by side.

### 2.10b Managerial / practical implications use plain language, not hypothesis labels

In §7.3 (managerial implications) or equivalent, drop the "(H3)" / "(H4)" trailing tags and the "the H4 evidence shows that..." phrasings. Use plain prose that the managerial audience can absorb without flipping back to §2.3.

Bad:
> "Second, firms should attend to the organizational skill bundles surrounding AI roles. The strongest mechanism evidence is project-management skill demand in AI vacancies (H3)."

Good:
> "Second, firms should attend to the organizational skill bundles surrounding AI roles. The strongest demand-side mechanism evidence is stronger demand for coordination, analysis, and project-management skills within AI vacancies."

Hypothesis labels are operational shorthand for the results section, not for managerial communication.

User signal: "여기에는 굳이 H2, H3, 이런 기호를 쓰지않고 plain하게 가야하지 않겠어?"

### 2.10c Limitations should NOT list items handled in robustness

If §5 (robustness) addresses a concern (alternative IV, alternative time window, alternative threshold), do not also list it as a limitation in §7.4. Listing in both places signals "we know this is a problem and didn't fix it" rather than "we fixed it."

Limitations should be items the paper genuinely cannot address: unmeasured selection, unobserved governance, time-invariant constructs that need a future panel to test causally.

Don't list speculative future-dynamics limitations either ("the post-2022 generative-AI era may reshape these patterns") — they invite skepticism without strengthening the paper.

User signal: "이건 robust 분석 했으니까 limitation에서 빼주고. … 이 얘기도 빼줘. 좀 불안하네."

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

## 3.8 Reference existence / fabrication check

AI-assisted drafts can contain plausible-but-FABRICATED references, or real works cited with the wrong volume/issue/page/year. Before submission, verify EVERY reference exists and is cited correctly:
- Web-search each entry by title + first author; confirm via the DOI, the publisher page, or Crossref / RePEc / Google Scholar. Fan this out (one check per reference) for speed.
- Highest fabrication risk: very recent / forthcoming items (last 1-2 years) and the volume/issue/page numbers.
- **Online-first vs volume year.** A work cited with full volume/issue/pages must carry the YEAR OF THAT VOLUME, not the earlier online-first year (an article printed in Vol 34(1) of 2023 is "2023" even if it appeared online in 2021). If you change the year, change every in-text citation too.
- Orphan check both ways: every in-text (Author, year) has a list entry, and every list entry is cited at least once. Dropping a vignette or a merged section can orphan its only citation — then delete that reference as well.
- **Retraction / withdrawal check.** A topically perfect, widely circulated paper can be WITHDRAWN (e.g., the MIT "AI, Scientific Discovery, and Product Innovation" working paper, disavowed 2025 for data integrity). Search "[title] retracted OR withdrawn" for every load-bearing reference; a retracted citation is worse than a missing one.
- **Fan-out collection pattern.** For a new paper's reference base, launch parallel search agents by theme cluster (theory anchors / empirical evidence / mechanism / context / methods), each instructed to verify every item against publisher pages or Crossref and to return structured records (title, authors, year, venue, DOI, OA-PDF link, 2-sentence claims summary, 1-sentence relevance). Duplicates surfacing across independent clusters are a signal of core references, not an error. Then curate to ~30 by argument-strength, with each entry's role in the paper written down.

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

### 4.1a Typography rules (body, captions, table notes, cover letter)

These typography conventions apply paper-wide. Apply them as a sweep before final submission and verify in the audit script.

- **No em-dashes (—, U+2014) in body prose.** Rewrite each occurrence as a comma, parenthetical, or sentence break. Em-dashes as N/A markers inside regression-table cells are exempt (different convention). The cover letter follows the same rule.
- **No "§" symbol in body prose; write "Section" instead.** "See §3.6" → "See Section 3.6." Many template generators emit "§" by default; sweep at the end.
- **No slash-pair shorthand for paired-named methods.** Replace "Bartik / shift-share" with "Bartik shift-share" (or one term alone). Same for any "X / Y" composite-name pattern in body prose.
- **References heading carries no section number.** Write "REFERENCES" — not "8. REFERENCES." Body sections are numbered; References is a back-matter heading.
- **Variable names in body prose are italicized** (carried over from §4.6).
- **Spelling standardisation is scoped to author-written text.** When standardising British vs American (pick from the target journal's house style; Taylor & Francis -> British), convert the body, abstract, keywords, captions, and table/figure notes — but do NOT touch reference-list entries (a cited title keeps its ORIGINAL published spelling, e.g. "…reorganization…", "interorganizational learning") and do NOT touch proper nouns in the body (e.g. the official "US Outbound Investment Security Program", "DataStream"). Verify with a both-directions scan (`per cent`/`percent`, `organis`/`organiz`, `-neighbour`/`-neighbor`, `favour`/`favor`).
- **Spell out cryptic statistical acronyms** the reader will not know (SUTVA -> "no spillover across acquirers"); standard defined ones (DiD, PSM, ATT, ATE, DDD) are fine once introduced.
- **Compound-modifier hyphens are consistent paper-wide:** "technology-transfer alliance", "joint-venture premium", "staged-acquisition strategy" when modifying a noun; left open as bare nouns ("involves technology transfer"). Title, keywords, and body must agree; if the title also sits on a separate title page / cover letter, change all copies together.
- **Squared regressors read as the concept with a true superscript** ("KnowledgeSimilarity²", vertAlign, not "KnowSim2" or "^2"); descriptive-table Min/Max keep decimals consistent ("0.000"/"1.000" for a binary variable, not "0"/"1").
- **Negative numbers: spell "minus" in prose and in table/figure NOTES, but keep the glyph "-" inside numeric TABLE CELLS.** Flag a hyphen-minus before a number only when it appears in running text, never in a data cell.
- **DOIs/URLs all-or-none.** Either every reference that has a DOI shows it, or none do. The low-risk way to make a mostly-DOI-free list consistent is to REMOVE the stray DOIs (never invent missing ones); if the target journal's style mandates DOIs, that is the author's call, so flag it.
- **"versus" not "vs"; "column (N)" not "column N"; parenthesise consistently** once the long/parenthesised form is established anywhere. A lone bare "vs", a bare-numeral column reference ("columns 3 and 4"), or a comma where sibling titles use parentheses ("Descriptive statistics, X" versus "Descriptive statistics (X)") is usually the only outlier.

User signal: "이런 em dash를 쓰지 말아줘. 본문 전체에 해당되는 얘기." / "논문 전체에서 이 기호 쓰지말고 Section이라고 쓰는게 좋겠어."

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

## 4.4 Mathematical notation in body prose — use it, define it, keep it consistent

**CORRECTED 2026-08-15.** An earlier version of this section prohibited notation in body prose. The author explicitly reversed that: "본문에는 수학 표기를 해야되." Methods prose SHOULD use mathematical notation where it makes definitions precise and compact. Do not "clean up" defined notation into words.

What good notation use looks like:
- Define symbols at first use in prose: "Let P be all observed active profiles, H the Hybrid count, S the Specialist count, ..."
- Formulas built from defined symbols are welcome in running text: "The AI workforce share is (H + S)/P", "Hybrid-tilted (High) when H exceeds S", "capability = Hybrid + Specialist".
- Division slashes inside formulas ("Explore/(Explore + Exploit)") are formulas, NOT the §4.1a slash-pair composite-name pattern; leave them alone.
- Keep prose symbols consistent with the tables and equation blocks that use them (construct-definition table, appendix algebra table, estimating equations). A symbol used in prose must be defined before use, or in an adjacent labeled table.

Boundaries that still hold:
- Hypothesis STATEMENTS stay in prose: no ×, ≥, ≤, ∈ inside the hypothesis sentence itself (§2.5); the mathematical specification lives in the methods section.
- Equation blocks still get a "where X is ..., Y is ..." explanation paragraph (§2.6).

User signal: "본문에는 수학 표기를 해야되" (notation belongs in the body — do not strip it).

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

## 4.8 No reviewer-facing meta-commentary or authorial stage directions

Manuscript prose describes the research, never the act of writing or reviewing it. This failure mode is bred by revision loops: each defensive fix tempts a sentence whose only audience is the referee. Keep the disclosure CONTENT; delete the meta-WRAPPER.

| Meta-wrapper (delete) | Content (keep) |
|---|---|
| "we state this rather than omit it" | "No invitation denominator was recorded, so a response rate cannot be computed." |
| "X deserves direct confrontation rather than a reviewer's discovery:" | "Two item-content proximities require direct testing:" |
| "We state the interval's meaning precisely:" | "The interval excludes ..." |
| "we state its reach honestly:" | (start with the substance) |
| "we surface the discordance rather than let each section cite its convenient component" | "The two evidence strands do not point at the same component." |
| "we describe their standing at zero order transparently:" | "At zero order, ..." |
| "we use the language of support rather than confirmation throughout" | (just use it; don't announce it) |
| "The verdict: H3-aug is not supported." | "H3-aug is therefore not supported." |

Related bans already covered elsewhere: "It is important to note" (§4.3), work-log subsection heads (§2.6a). Adverbs of virtue — honestly, transparently, candidly, precisely — attached to reporting verbs are the telltale; so are contrast clauses about what a lazier author would have done ("rather than omit / rather than leave to a reviewer / rather than forcing one prediction"). First-person METHODOLOGICAL voice is fine ("we treat the scores as formative", "the stage mapping is ours"); first-person EDITORIAL voice is not.

A subspecies: **structure-narration signposts**. Sentences that narrate the document's own layout — "The overarching question is stated first; the hypotheses that follow decompose it...", "The design question is stated as a research question rather than a hypothesis", "posed informally in the Introduction" — are stage directions too. Headings, ordering, and labels carry the structure; delete the sentence that re-announces it. (RQ/hypothesis architecture itself: §2.5a.)

User signal: "이런거 또 그 무대 그거자나. 이런 문장들은 쓰지말고."

Further removals from a second manuscript's sweep (before → after):
- "Three qualifications keep this reading honest." → "Three qualifications apply."
- "Two diagnostics bound the reading." → delete the sentence; the diagnostics that follow speak for themselves.
- "...and we state the boundary rather than average over it." → end the sentence before the clause.
- "...which is itself informative: [content]" / "The contrast is informative: [content]" → drop the wrapper, keep the content.
- "The signature still disciplines interpretation: it gives no support to..." → "They still give no support to..."
- "...within limits the design makes explicit." → name the actual limit ("though its reach is bounded by sparse Translator capacity").
- "Exception rows are reported as named exceptions." (table note) → delete; "carries/robust with named exceptions" → "has/robust with exceptions".
- "so we read them side by side: [content]" / "we read the evidence as X" → state the content directly ("the evidence is X").

KEEP statements that look similar but carry substance — claim scope ("we do not claim the fine-industry comparison"), data properties ("zero is an informative feature of the measured workforce"), design function ("the matched design keeps them apart"), test properties ("the test bounds the alternative rather than settles it"). The test: if the sentence performs how careful the paper is being, delete or convert; if it states what is claimed, measured, or bounded, keep.

Add the ban list to the audit script as regex patterns so revision rounds cannot reintroduce them.

User signals: "작업지시나 리뷰어는 몰라도 되는 문장들이 들어갈 필요는 없어."; "리뷰어에게 말을거는 무대지시문 같은거 빼줘."

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

## 5.12 Stable citation keys in source files; numeric order assigned at build

For numbered-citation journals (IEEE and similar), do NOT hand-number citations in the source manuscript. Instead:

- Source md/text files cite with stable keys (`[R07]`, `[R23]`) that never change.
- The docx generator maps keys to numbers by FIRST APPEARANCE in reading order, emits `[n]` in text, and writes the reference list in that order from a single reference dictionary inside the generator.
- The audit asserts: used keys == defined keys (both directions), numbers span 1..N with no gaps, and the printed list is ordered 1..N.
- Reordering sections or adding a citation then costs one rebuild, not a manual renumbering cascade (the numbered-citation analogue of §7.3b).

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
- **Caption is bold; "Note." prefix on table notes is italic.** Same for "Notes:" on figure captions. When scripting a table-note edit, the default `add_run()` strips italic — restore it explicitly.
- **Column-N formatting must match Column-1 formatting.** When swapping content of a column via `cell.text = …` in python-docx, the cell's bold, center alignment, font name, font size, and multi-line break structure all get wiped. Copy the source-column formatting explicitly after the content swap.

### 7.3a [INSERT TABLE N HERE] markers go at the end of their subsection

In manuscripts that place all tables at the back (typical journal-submission practice), the in-body marker `[INSERT TABLE N HERE]` indicates to the typesetter where the table should appear in the final printed version. Conventional placement:

- **Marker sits at the end of the subsection that discusses the table**, right before the next subsection heading.
- NOT in the middle of a paragraph.
- NOT between the introductory result-sentence paragraph and the detailed walk-through paragraph.

Example layout for §4.1:
```
4.1 Baseline relation between X and Y

[Lede paragraph: H1 is supported. Table 4 reports …]

[Detailed paragraph: IV diagnostics, magnitude interpretation, …]

[INSERT TABLE 4 HERE]

4.2 Next subsection …
```

User signal: "이 subsection 즉, 4.1 마지막에 table이 오는게 자연스럽지 않겠어?"

### 7.3b Table-renumbering cascade discipline

Inserting, moving, or renumbering one table sets off a cascade. Handle ALL of:
1. **Plural / range reference forms.** A single-token replace ("Table 3"->"Table 4") MISSES "Tables 3 and 4", "Tables 3 to 5", "Sections 3.3 and 5.5". After any renumber, scan separately for plural "Tables N and/to M" and "Sections N and M" forms.
2. **Figures that embed a table number IN THE IMAGE.** A coefficient plot titled "(Table 3, columns 1-3)" must be REGENERATED when the DiD table becomes Table 4 — editing the caption is not enough, the number is baked into the raster. Keep the figure-generation script so you can re-emit with the new label, then re-embed at the same display width.
3. **Monotonic first-mention order.** Tables are numbered in order of first in-text citation. If you move a descriptive/robustness table's discussion to an earlier section, renumber so it is not cited before a lower-numbered table, and physically reorder the end-matter table blocks to match. Confirm the [INSERT TABLE N HERE] markers read 1..N in document order.
4. **3-cycle renumbers** (A->B, B->C, C->A) need a placeholder pass (A->@@TMP@@, B->A, C->B, @@TMP@@->C) to avoid collisions.
5. **Table-note cross-refs.** Re-check each note's "same controls as Table X" / "not comparable to the Table Y estimates" still points to the right table.

### 7.3c Re-derive every reported statistic from the paper's own numbers; respect the estimator

A late "numbers" pass should recompute each headline figure from the values the manuscript itself reports, and fix any that do not reconcile, but only after checking the figure is not a different, legitimate quantity.
- **Percentages must match the table's reported N.** If the text says "62.0 per cent of panel observations are missing" but the Table 1 note reports total N = 330,902 and the variable's own N = 125,977, the rate is (330,902 - 125,977)/330,902 = 61.9 per cent. A reader divides the paper's own numbers and gets 61.9; internal consistency, not the author's loose rounding, governs. The same figure often recurs 2-3 times: change every instance.
- **Bounded-variable sanity checks.** A [0,1] share with mean m cannot have variance above m(1 - m). A stated "variance 0.24" for a mean-0.317 overlap share is impossible (max 0.2165); the value implied by the reported moments is E[X^2] - mean^2 = 0.310 - 0.317^2 = 0.21 (SD 0.46). Such bounds catch errors no cross-reference check would.
- **Respect log vs level (Jensen's inequality).** When a count is modelled as ln(1 + count), do NOT "correct" a stated average count to exp(mean of logs) - 1. The arithmetic mean of counts is strictly larger than that back-transform, so a base like "about three patents" can be right even though exp(1.124) - 1 is about 2. If the subsample's arithmetic mean is not reported, FLAG it for the author to confirm rather than silently changing it toward a lower bound.
- A figure that cannot be reproduced from any reported number is a FLAG, not an automatic edit: ask the author, or change it only when one resolution is unambiguous (matches the table) and the alternative is mathematically impossible.

### 7.3d Main-table architecture: one wide table whose columns get progressively stricter

The default results architecture in empirical management and finance journals is **one main regression table, read left to right from the least to the most demanding specification**, with everything else demoted to robustness. A results section built as a long tidy table (one row per model, columns `Outcome | Specification | Coefficient | SE | 95% CI | p | q | N`) is a machine-readable grid, not a journal table, and reviewers read it as an unfinished specification dump.

Convert to the column layout:

- **Rows are variables**, in the order: variable of interest first, then controls, in the same order they enter the model.
- **Columns are models**, headed `(1)`, `(2)`, `(3)` with a one-line spec label under the number (the outcome name, or the estimator).
- Columns move **baseline → richer**: e.g. (1) firm + year FE, (2) firm + industry×year FE, (3) + lagged controls. When there are two outcomes, run the same three columns twice: (1)-(3) outcome A, (4)-(6) outcome B. The reader then sees attenuation across a row instead of hunting across a stack of separate tables.
- **A rule separates the estimates from the specification block** beneath: FE indicators (`Yes`/`No` per column), a controls indicator, Observations, number of firms/clusters, Within R², and R² including the fixed effects. Everything a referee checks first lives in that block.

Everything that is not the main model — alternative horizons, alternative samples, alternative outcome constructions, multiplicity adjustment, exposure/denominator variants, sector cuts, deduplication — moves into a single robustness section that names, in its opening sentence, the list of design choices it varies and in what order. The paragraphs then follow that order exactly.

User signal: "메인 모델이 위로 올라가고 거기에 추가되는 main table이 나와야 해. 나머지는 robustness로 넘어가는 거고."

The supporting main tables run in the reference order before the regression table: sample construction / observation flow → summary statistics → correlation matrix → construct composition (if the paper builds a measure) → main regression → any head-to-head comparison of alternative measures. **If the paper has no summary-statistics table and no correlation matrix, that is a finding, not a style choice** — a referee will ask for both, and the correlation matrix usually earns its place by justifying a control (e.g. treatment correlates .60 with the denominator control) or by motivating a direct coefficient test (e.g. two outcomes correlate .76, so a difference between their coefficients has to be tested, not eyeballed across two regressions).

### 7.3e p-value reporting: stars in the main table, exact values in its appendix twin

The convention these journals actually use is **coefficient with significance markers, standard error in parentheses directly beneath**, and the thresholds defined in the note (`*** p < 0.01, ** p < 0.05, * p < 0.10`). Not the coefficient alone, not a p-value column, not a bare CI column.

```
ESG vacancy demand      0.0157**        0.0086          0.0071
                        (0.0075)        (0.0069)        (0.0065)
```

A paper that has principled reasons to distrust stars (exploratory design, multiplicity, small cluster counts) does **not** solve the problem by refusing the convention — that just makes the main table unreadable. Report both, in two places:

- **Main table:** stars + SE, so the pattern is legible at a glance.
- **Appendix twin table, same estimates:** coefficient, SE, 95% CI, exact p-value, and the multiplicity-adjusted q-value. Caption it as such ("Main specifications with exact p-values and intervals") and point to it from the main table's paragraph.

Then say once, in the methods, what the paper leans on: *the main tables mark conventional significance so they can be read at a glance, every marked estimate is repeated in the appendix with its interval and exact p-value, and no conclusion rests on a star.* That keeps §5.6 significance-threshold honesty intact while still giving the reader the table shape they expect. See §5.6 and §6.2 for how to describe marginal results in the prose.

### 7.3f Three-line format, and the DOCX traps that silently break it

The three-line academic table is: a rule above the header row, a rule under the header row, a rule under the last row, **no vertical rules and no interior horizontal rules** — with one exception, a single rule marking a panel break or the start of the specification block. Caption above the table (`**Table N.** Title`, label bold, title not), small flush-left `Note.` paragraph below, table centred, one font throughout.

Traps that produce a table which passes visual inspection at small size but is wrong:

- **The body first-line indent leaks into cells and captions.** Table cell paragraphs, captions, and notes inherit the Normal style's `first_line_indent`. The caption drifts off centre and a narrow column force-breaks a word mid-token (`Hori` / `zon`). Reset first-line, left, and right indent on every generated paragraph.
- **Theme fonts silently override the font you set.** In WordprocessingML a `w:asciiTheme` attribute beats the explicit `w:ascii` name that python-docx writes, so `Heading 1`, `Heading 2`, `Caption`, and `Title` keep rendering in the theme font. Delete the `asciiTheme`/`hAnsiTheme`/`eastAsiaTheme`/`cstheme` attributes after setting a style's font.
- **A declared font Word cannot bind falls back silently.** Variable fonts (e.g. STIX Two Text) are not bindable by Word; every table and caption renders in the theme fallback instead. Verify by exporting to PDF and reading back the span font names — do not trust the DOCX declaration.
- **Cell padding written as `w:start`/`w:end` is ignored**; Word honours `w:left`/`w:right`.
- **Column widths from character counts do not bound the longest unbreakable word.** Derive widths from measured glyph advances (PIL `ImageFont.getlength` on the actual TTF), take the largest font size at which every token still fits, and treat hyphen/slash as break opportunities. For a two-line cell (`coef***` over `(SE)`), measure each line separately.
- **Decimals belong to the column, not the value.** Deciding per value prints `1` next to `0.0571`. Fix four decimals for the column; widen only when the column's typical magnitude is below 0.001 (a standard-deviation column of `0.0002` carries one significant digit), and use the integer dtype — not "max value ≥ 2" — to decide that a horizon column of 0/1 is an index, not a share.
- **Default `Title` style is blue with a rule under it.** Set the colour to black and remove the paragraph border.
- Use the typographic minus (U+2212) for negative numbers so the tables match the body prose. Korean sans fonts (Malgun Gothic) have no U+2212 glyph — in figure labels drawn with matplotlib, fall back to the hyphen there.

### 7.3g Generate display tables from the estimator, with a full-estimates audit file

Build the main table with a script that **re-runs the estimator and emits both the display table and a long-format file with every coefficient, SE, p-value, N, and R² it used**. Two consequences worth the effort:

- The main table and the robustness tables cannot drift apart, because they come from one estimation path. Reproducing the existing published numbers exactly (to the last digit) is the acceptance test for the new script.
- The audit file makes every cell traceable, and it is what you check the prose against: extract each coefficient the text attributes to a column and assert it equals the table cell.

A statistic that applies to all columns at once (a joint equality test across four measures) has no cell to live in — a row can only be written into the first column, where it misreads as belonging to that column. **Put it in the note**, not in a row.

### 7.3h Render-verification loop, page-spanning tables, and p-value cell format

- **Verify the render, not the declaration, without opening Word**: convert a COPY of the docx to PDF (docx2pdf; never the live file, §9.6), rasterize the pages containing tables (PyMuPDF `get_pixmap`), and visually inspect the images. This catches what structural audits cannot: cramped first columns wrapping labels onto three lines, tables split across pages, wrong caption placement. Also read back the PDF's embedded font list — it is the ground truth for §7.3f font binding.
- **Page-spanning tables repeat the header row**: set `w:tblHeader` on the first row of every numbered table. A correlation matrix that breaks across pages without a repeated header is unreadable.
- **Default column widths**: wide first column for row labels (≈4.2 cm at ≤6 columns, ≈3.4 cm for wider tables), equal split for the rest. Auto-fit equal widths is what causes the three-line label wrap.
- **"R2" renders as R + superscript 2** — build the superscript run in the generator; a literal "R2" in a stub row survives every text-level audit.
- **p-value cells never print ".000"**: format as "< .001" below .0005. A ".000" cell in an exact-p appendix table contradicts the table's own purpose.
- **Exact-p appendix twin (§7.3e) is generated from the same lock file** as the starred main table, so the two cannot disagree.

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

**Extract the format mechanically, do not eyeball it.** Open the reference DOCX and dump, per table: style name, alignment, autofit, grid widths, table-level borders, per-cell borders, cell margins, vertical alignment, header run font/size/bold, and the paragraphs immediately before and after (which tell you whether the caption sits above and the note below). Render the reference PDF alongside it and read back the span fonts and sizes — the declared font and the rendered font differ more often than not (§7.3f). Then encode the extracted format once, in the generator, and add an audit script that re-checks it on every build so a later edit cannot quietly undo it.

The realized format, not the declared one, is the target: if the reference's own PDF renders its tables in the body font because its declared table font never bound, match the body font.

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
- Named worker / firm categories that the paper coins (italic on first mention): e.g., *hybrid*, *specialists*, *translator workers*.
- Theoretical frameworks (italic on first mention): *absorptive-capacity*, *complementary-assets*.

**Typography in the cover letter mirrors the body:**
- No em-dashes (—). Rewrite as comma, parenthetical, or sentence break — same body rule applies here.
- No "§" symbol; write "Section" if cross-referencing.
- No slash-pair shorthand (e.g., "Bartik / shift-share" → "Bartik shift-share").

The cover letter is part of the submission package and the editor reads it back-to-back with the abstract; tonal/typographical mismatches between them are immediately visible.

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

Author identity hides in MORE docx members than `dc:creator` / `cp:lastModifiedBy`. Before a blind submission, scrub ALL of:
- `docProps/core.xml` — `dc:creator`, `cp:lastModifiedBy`.
- `word/people.xml` — the comment-author registry; it stores each commenter's display name AND often their email / tenant userId (`w15:userId="S::name@univ.ac.kr::..."`). A file literally named `..._anonymised.docx` routinely still leaks the author here.
- `word/comments.xml` (+ `commentsExtended/Ids/Extensible.xml`) — the comment bodies and their `w:author`.
- `docProps/app.xml` — `Company`, `Manager`.
Once the author's memos are resolved, REMOVE the comments entirely (the `commentRangeStart/End` + `commentReference` markers in `document.xml`, and strip the comment parts), then grep every ZIP member for the surname, given name, email, and institution to confirm zero hits. Leave the (non-blind) title page untouched.

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

### 9.2a Formatting-preservation caveats when editing docx in place

When the workflow shifts from "regenerate the whole docx from a script" to "edit the docx in place via python-docx" (typical for memo resolution where the user wants comments preserved while specific paragraphs are rewritten), the following formatting wipes happen silently:

- **`replace_paragraph_text()` style helpers strip the first run's bold/italic/font/size unless you snapshot them and re-apply.** Headings, captions, and the "REFERENCES" line lose bold this way. Always snapshot `r.bold / r.font.size / r.font.name / r.italic` from the first non-empty pre-existing run and re-apply on the new run.
- **`cell.text = "new content"` strips all run formatting in a table cell.** When updating a column's numeric content, also copy the source-column's `bold`, `paragraph.alignment`, font size, and font name onto the destination column. Re-add multi-line break structure (coef / (SE) / [p = .xxx]) explicitly with `.add_break()`.
- **Word comments embedded in a paragraph survive a python-docx rewrite UNLESS you remove them along with the runs.** Decide up front whether to preserve or strip; if preserving, save the `commentRangeStart` / `commentReference` XML elements before clearing the paragraph and re-insert them after the new run.
- **End-of-edit audit:** after any in-place edit pass, sweep the whole doc for heading bold, caption bold, "Note." italic, em-dash residue, "§" residue, and slash-pair residue. These are the most common formatting regressions.

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

### 9.5b Italic variable-name runs split a sentence; edit per-run, never rebuild across italics

In an empirical paper, italicised variable names (lnRnd, priorAlliance, KnowledgeSimilarity) break a paragraph into many runs. A plain-text substring that spans an italic boundary (e.g. "(62.0 per cent of panel observations)" sitting on either side of an italic token, or "crosses the ten per cent threshold" next to an italic var) lives in NO single run, so a run-level `old in run.text` search fails.
- Do NOT fall back to rebuilding the whole paragraph (concatenate text, wipe it into run[0]): that DESTROYS the italic formatting of every variable name in the paragraph.
- Instead: (i) target the shortest token that lives inside one run ("crosses" -> "clears", not the whole clause); or (ii) replace per-run, iterating runs with run.text = run.text.replace(old, new) and asserting the total replacement count equals what you expect (catches both 0-hits and accidental extra hits, e.g. when "62.0" must change in two places but not a third).
- Beware substring collisions inside a word: replacing the bare token "on" also hits "c(on)centrates". When a word is its own run, match run.text == exact_old and assign, rather than a substring replace.
- Headings can be fully italic and split mid-phrase ("...concentrates " | "on" | " partial..."), so the same per-run discipline applies outside body paragraphs.
- Build the apply script fail-safe: collect a status per edit and save() ONLY if zero failures, so a single bad anchor never leaves the file half-edited. Back up the docx before each stage.

## 9.6 The docx has another writer: never assume single-writer access

The human collaborator usually keeps the manuscript OPEN in Word and edits it intermittently WHILE you are editing it programmatically (python-docx). The two writers then collide: whichever side saves last silently overwrites the other's work — your python-docx save can wipe the human's in-Word edits, and a later Word save can wipe an entire batch of your fixes. In one session a four-paragraph block (Disclosure / Data-availability) vanished exactly this way; the cause was concurrent Word editing, not the edit script. (Author's own words: "그건 내가 중간중간 Word를 수정해서 그래.")

Treat the file as shared, single-writer:
- RE-READ the live file at the start of every edit batch — never trust an in-memory `Document` loaded earlier. Verify paragraph / section / table / image counts against the last known-good state; a mismatch means someone else wrote to it, so reconcile before editing.
- Check for the `~$<name>.docx` lock file: its presence means the file is open in Word RIGHT NOW. Ask the human to close Word (or pause) before you run a batch, and tell them when you are done so they can resume. Warn them that saving from a stale Word window will discard your latest edits.
- Keep a timestamped backup before every stage so a paragraph-list diff (old vs new) instantly shows what changed and lets you recover an overwritten block.

Separately (a related but distinct trap): converting a docx to PDF with a Word-backed tool (`docx2pdf`, Word COM) can make Word "repair" slightly non-canonical python-docx XML and drop content. Convert a COPY, never the live file, and re-verify counts after any Word round-trip.
- Diagnostic: a plain python-docx load+save round-trip does NOT lose content. If content vanished, suspect an external Word write (or a Word/PDF step), not your edit script.

## 9.7 Final review as a multi-round adversarial loop until convergence

For a "read it five more times" final pass, run a fan-out review workflow repeatedly, not once.
- Each round = one reader per section (sentence by sentence) PLUS cross-cutting lenses (numbers; cross-references; citations vs reference list; British-spelling/typography), then an ADVERSARIAL verify stage in which a separate agent must confirm each finding is verbatim, real (not taste), safe (preserves every number/citation/defined term, British spelling, no em-dash), and introduces no new error. Default the verifier to REJECT taste-only rewrites.
- Re-dump the docx to a fresh text file BETWEEN rounds so the next round sees the applied edits.
- Feed SETTLED decisions back into the next round's context so it stops re-flagging them (an intentionally open title, table-cell minus glyphs, a deliberately DOI-free reference list, an arithmetic-mean base the author confirmed). Otherwise every round re-surfaces the same non-issues and buries the real ones.
- Stop when a round yields only taste-level or already-settled items. Expect the count to fall but not monotonically (each fresh read finds different polish): one real session ran 28 -> 17 -> 12 -> 16 -> 8 -> 6.
- Genuine errors hide until late: an impossible variance and a "not X nor Y" correlative surfaced only in rounds 4 and 6. The extra passes earn their cost.

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
