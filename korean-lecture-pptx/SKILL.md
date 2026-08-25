---
name: korean-lecture-pptx
description: "Create, revise, and verify Korean lecture PPTX decks and speaker notes when course flow, spoken-Korean narration, evidence discipline, preservation of instructor edits, and rendered-slide quality matter. Use for new or existing university, K-MOOC, training, and multi-session course decks; do not use for ordinary business pitch decks whose primary goal is persuasion rather than teaching."
---

# Korean Lecture PPTX

Build a teachable argument, not a decorated outline. A completed deck should let students understand why each idea appears, let the instructor read the notes naturally, and remain technically reproducible without overwriting manual PowerPoint edits.

## Route the task

- Read [course-architecture.md](references/course-architecture.md) when planning a course, changing slide order, adding or deleting slides, or repairing a weak narrative arc.
- Read [speaker-notes.md](references/speaker-notes.md) whenever writing or revising narration.
- Read [prompt-library.md](references/prompt-library.md) when the user wants reusable prompts or when a large deck needs a structured planning/revision contract.
- Read [sources-and-rights.md](references/sources-and-rights.md) when facts, statistics, law, company cases, images, or citation policy are involved.
- Read [pptx-preservation-and-validation.md](references/pptx-preservation-and-validation.md) before editing an existing PPTX, synchronizing embedded notes, rendering, or declaring completion.
- Read [learner-review.md](references/learner-review.md) for learner-perspective review or saturation testing.

## Core contract

1. **Start from the learner outcome.** State the course's governing question and what the learner should be able to explain, judge, or design afterward. Treat target time and slide count as constraints, not as the educational objective.
2. **Give every substantive slide one primary educational job.** Use a claim or question, not merely a topic label. Add a bridge slide when a concept is required before it can be used. Remove a slide when it repeats information without advancing the learner's judgment. Covers, section breaks, activity instructions, and references may serve navigational or operational roles.
3. **Make transitions causal.** When the time period, analytical lens, unit of analysis, or evidence type changes, explain what changes and why. Do not rely on “다음 슬라이드를 보겠습니다.”
4. **Separate screen, speech, and evidence.** Keep the screen concise, the speaker notes natural and self-contained, and detailed citations/provenance in a separate record unless the user specifies another policy.
5. **Explain before naming when the term carries the argument.** At first consequential use, briefly explain unfamiliar terms, acronyms, institutions, people, metrics, and hard-to-pronounce names. Calibrate detail to learner prior knowledge and prefer the learner's language over production shorthand.
6. **Match claim strength to evidence.** Preserve the measured object, denominator, date, conditions, exceptions, and whether a number is observed, estimated, forecast, self-reported, or vendor-reported. Explain limitations as part of the story, not as defensive boilerplate.
7. **Preserve the user's current PPTX.** Freeze the latest file and identify manual edits before changing it. For an existing deck, prefer a minimal allow-listed patch over a full rebuild. Abort on concurrent drift or an unexpected package change.
8. **Verify what learners actually see and hear.** Exact note/source synchronization and package checks are necessary but insufficient. Render every slide in PowerPoint, inspect geometry and contrast, and review the full spoken flow.

## Working sequence

1. Inventory the source files, current PPTX, notes, templates, assets, citation rules, and requested structural changes. Back up and hash any user-edited baseline.
2. Draft the course arc and slide-function map before polishing prose. Identify missing prerequisites, duplicate slides, likely misconceptions, and the unresolved question that leads to the next session.
3. Build a claim/evidence ledger. Verify facts and rights before placing them on screen.
4. Revise the screen and notes together while keeping their roles distinct. Do not regenerate an existing deck wholesale merely because a builder exists.
5. Synchronize canonical notes across the authoring source, Markdown script when present, and embedded PowerPoint notes.
6. Run package checks, actual PowerPoint rendering, visual review, and learner review. If PowerPoint is unavailable, label an alternative render provisional and do not claim PowerPoint-render validation. If the user requests saturation or a high-risk multi-deck release, use the independent frozen-output protocol in the validation reference.
7. Hand off final deck paths, slide counts, validation evidence, preserved manual edits, and unresolved rights or approval gates.

## Boundaries

- Do not invent citations, image licenses, legal conditions, survey denominators, or permissions.
- Do not call a virtual learner review an actual student survey.
- Do not treat repeated execution of one deterministic checker as independent saturation.
- Do not publish private teaching materials or third-party assets inside this skill. Store only generalized instructions and reusable code.
- Do not optimize narration to TTS timing unless the user explicitly requests it.
- The included package scripts support Transitional OOXML only. If a Strict OOXML deck is detected, stop and use the approval-based staged-conversion path in the validation reference; do not rewrite the user's original automatically.

The bundled scripts require Python 3.10 or newer and use only the standard library. Run them with `-B` so validation does not create `__pycache__` inside the skill.

For a read-only package check, run:

```bash
python -B scripts/audit_pptx_package.py DECK_OR_FOLDER --require-notes --forbid-note-metadata
```

The script checks package integrity and note hygiene; it does not compare a project-specific canonical manuscript or replace PowerPoint rendering, fact review, or learner review.

For one revision batch on an existing deck, first make a byte-identical immutable baseline copy, then initialize the batch manifest with `python -B scripts/create_pptx_manifest.py DECK.pptx --baseline-root BASELINE_FOLDER --output manifest.json`. Add `--require-notes` only when the baseline already has one nonempty note per slide. Batch UIDs are not permanent course identifiers. After an owner-approved slide insertion, deletion, or reorder, freeze the accepted candidate as a new baseline and start a new batch while retaining the prior baseline, manifest, and approved crosswalk as frozen evidence.
