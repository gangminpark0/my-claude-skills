# PPTX Preservation and Validation

Use this reference whenever an existing PPTX contains manual edits or when completion must be proven rather than assumed.

## Freeze the current baseline

Before editing:

1. identify the exact current PPTX and any companion Markdown, builder, source record, and assets
2. check for PowerPoint lock files and running processes
3. copy the current artifacts to a timestamped backup
4. record absolute path, size, modification time, and SHA-256
5. render a fresh baseline if existing renders predate the user's manual edits
6. identify protected slides, shapes, images, notes, and relationships

Fail closed when the live file changes after the baseline was recorded. Re-read and re-plan instead of applying a patch to stale bytes.

## Choose rebuild or surgical revision

A full rebuild is appropriate for a new deck or when the user explicitly accepts template regeneration. It is dangerous when PowerPoint contains manual edits that the builder does not reproduce.

For an existing user-edited deck:

- work on a staged copy
- make a semantic diff against the last reproducible version when available
- identify exact target slides/shapes by stable text, shape ID, geometry, and expected count
- use `python-pptx` saves only on disposable copies when possible
- transplant only allow-listed OOXML parts into the staged copy
- verify that all non-allow-listed package members remain byte-identical
- commit atomically only after a final live-hash check; keep rollback copies

Record each retained slide with a stable manifest rather than relying on its title alone:

| Original index | Current index | presentation rel ID | slide part | content fingerprint | protected shape IDs/assets | notes part | source-record key | action |
|---:|---:|---|---|---|---|---|---|---|

Titles are useful evidence but are not stable identifiers: titles can repeat or change during revision.

Use the manifest as a machine-verifiable release artifact. Version 2 binds both an immutable baseline and the current candidate, then permits only declared package-part changes. The following is an explanatory, abbreviated schema and will not pass the auditor as copied; always generate the complete inventories and replace every placeholder with an actual value:

```json
{
  "version": 2,
  "decks": [
    {
      "file": "lecture.pptx",
      "baseline_file": "lecture.pptx",
      "baseline_sha256": "<baseline-deck-sha256>",
      "baseline_slide_count": 2,
      "baseline_member_sha256": {
        "[Content_Types].xml": "<part-sha256>",
        "ppt/slides/slide1.xml": "<part-sha256>"
      },
      "current_sha256": "<current-deck-sha256>",
      "current_slide_count": 2,
      "allowed_changed_parts": [
        "ppt/slides/slide1.xml",
        "ppt/notesSlides/notesSlide1.xml"
      ],
      "protected_assets": [
        {"part": "ppt/media/image1.png", "sha256": "<asset-sha256>"}
      ],
      "editable_assets": [],
      "protected_relationships": [
        {
          "source_part": "ppt/slides/slide1.xml",
          "relationship_id": "rId7",
          "type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
          "target_mode": "internal",
          "target": "ppt/media/image1.png"
        }
      ],
      "editable_relationships": [],
      "protected_shapes": [
        {"slide_uid": "opening-question", "shape_id": "12", "sha256": "<canonical-shape-sha256>"}
      ],
      "protected_slide_shells": [
        {"slide_uid": "opening-question", "sha256": "<non-drawing-slide-xml-sha256>"}
      ],
      "editable_shapes": [
        {
          "slide_uid": "opening-question",
          "shape_id": "12",
          "operation": "modify",
          "reason": "Revise the opening question approved by the course owner",
          "reviewed_by": "course-owner",
          "reviewed_at": "2026-08-26"
        }
      ],
      "slides": [
        {
          "slide_uid": "opening-question",
          "action": "keep",
          "source_keys": ["SRC-001", "IMG-001"],
          "baseline": {
            "index": 1,
            "presentation_rel_id": "rId2",
            "slide_part": "ppt/slides/slide1.xml",
            "notes_part": "ppt/notesSlides/notesSlide1.xml",
            "slide_sha256": "<baseline-slide-xml-sha256>"
          },
          "current": {
            "index": 1,
            "presentation_rel_id": "rId2",
            "slide_part": "ppt/slides/slide1.xml",
            "notes_part": "ppt/notesSlides/notesSlide1.xml",
            "slide_sha256": "<slide-xml-sha256>"
          }
        }
      ]
    }
  ]
}
```

`slide_uid` identifies a slide only inside one revision batch; release manifests in this bundled batch-local workflow contain `action: keep` only. `source_keys` ties every claim or asset to the provenance ledger. A slide without external evidence needs a reviewed `source_exemption` whose type is one of `navigation`, `activity`, `instructor_synthesis`, or `original_course_instruction`. `baseline` records the batch's immutable starting point and `current` records the candidate. The baseline member map proves what the frozen source contained, and `allowed_changed_parts` must equal the actual package-part diff. `protected_assets` must be the complete baseline `ppt/media/*` inventory. Every actual media insertion, replacement, or deletion needs a matching `editable_assets` record with before/after hashes, exact `baseline_owner_slide_uids` and `current_owner_slide_uids` reached through typed package dependencies, reason, reviewer, and valid review date. `protected_relationships` must be the complete normalized baseline relationship inventory. Every inserted, deleted, or modified binding—including a target-only image swap—needs an exact `editable_relationships` record. `protected_shapes` covers every baseline drawing owner; `editable_shapes` must exactly match actual `modify`, `insert`, or `delete` operations. `protected_slide_shells` protects non-drawing slide XML such as background, transition, timing, and color-map overrides.

The following records show the complete action-specific null rules. Include a record only when the corresponding change actually occurred; these are not blanket permissions:

```json
{
  "editable_assets": [
    {
      "action": "modify",
      "part": "ppt/media/image1.png",
      "baseline_sha256": "<64-hex-before>",
      "current_sha256": "<64-hex-after>",
      "baseline_owner_slide_uids": ["opening-question"],
      "current_owner_slide_uids": ["opening-question"],
      "reason": "Replace the image after the course owner approved the new asset",
      "reviewed_by": "course-owner",
      "reviewed_at": "2026-08-26"
    },
    {
      "action": "insert",
      "part": "ppt/media/image2.png",
      "baseline_sha256": null,
      "current_sha256": "<64-hex-after>",
      "baseline_owner_slide_uids": [],
      "current_owner_slide_uids": ["opening-question"],
      "reason": "Add the owner-approved diagram used by the opening slide",
      "reviewed_by": "course-owner",
      "reviewed_at": "2026-08-26"
    },
    {
      "action": "delete",
      "part": "ppt/media/image3.png",
      "baseline_sha256": "<64-hex-before>",
      "current_sha256": null,
      "baseline_owner_slide_uids": ["opening-question"],
      "current_owner_slide_uids": [],
      "reason": "Remove the superseded asset after the course owner approved deletion",
      "reviewed_by": "course-owner",
      "reviewed_at": "2026-08-26"
    }
  ],
  "editable_relationships": [
    {
      "action": "modify",
      "source_part": "ppt/slides/slide1.xml",
      "relationship_id": "rId7",
      "baseline": {
        "type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
        "target_mode": "internal",
        "target": "ppt/media/image1.png"
      },
      "current": {
        "type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
        "target_mode": "internal",
        "target": "ppt/media/image2.png"
      },
      "baseline_owner_slide_uids": ["opening-question"],
      "current_owner_slide_uids": ["opening-question"],
      "reason": "Retarget the image relationship after explicit owner review",
      "reviewed_by": "course-owner",
      "reviewed_at": "2026-08-26"
    }
  ]
}
```

For `editable_relationships`, use `baseline: null` only with `insert` and `current: null` only with `delete`; `modify` requires both complete bindings. A relationship-only retarget does not require a fake media-byte change, but it always requires its own reviewed relationship record. Any slide insertion, deletion, reorder, or slide-identity rebinding is outside this batch schema and must fail with `structural_change_requires_new_batch`.

First make an immutable backup and close PowerPoint. Initialize with `python -B scripts/create_pptx_manifest.py DECK.pptx --baseline-root BASELINE_FOLDER --output manifest.json`. Add `--require-notes` only if the baseline already has exactly one nonempty note per slide. A deck without notes can be initialized without that flag; adding notes later is a relationship/topology change that requires explicit review, and the delivery audit should then use `--require-notes`. At initialization, current and baseline must be separate, byte-identical files. The generator hashes every member, inventories every baseline media asset, relationship binding, drawing owner, and non-drawing slide shell, rejects machine-local external file links, checks lock/process state, and never overwrites an existing output. It leaves source classification unresolved, so assign `source_keys` or a reviewed `source_exemption` before release. Avoid `--allow-powerpoint-process`. If release ownership explicitly requires it, also supply `--approval-record approval.json`; the record must use `version: 1`, scope `manifest-initialization-with-powerpoint-open`, and nonempty `accepted_by`, valid `accepted_at` date, and rationale. The generator freezes its hash and records the approval fields in the manifest.

Typical allow-lists are:

- **notes-only:** the mapped `ppt/notesSlides/notesSlide*.xml` parts only
- **text/shape edit:** explicitly named `ppt/slides/slide*.xml` parts only
- **asset replacement:** only package parts whose bytes actually changed; for example, the relationship part and exact old/new media members, with slide XML included only when it also changed
- **insert/delete/reorder:** not permitted inside an existing batch manifest; owner-approve the crosswalk, freeze the accepted candidate, and initialize a new batch

Anything outside the chosen allow-list is an error until deliberately explained.

For ordinary text or note edits, relationships, media, masters, layouts, themes, fonts, and document properties should not change. A slide insertion, deletion, or reorder is an explicit topology change. Because this skill does not bundle a general lineage updater, do not claim that it mechanically proves an old-to-new mapping. Keep the candidate delivery-pending until the course owner approves an exact crosswalk of old index/UID, new index, notes, page label, and source keys. Then freeze the accepted candidate as a new immutable baseline, initialize a new batch manifest with new batch-scoped UIDs, rebind canonical notes and sources, and retain the previous baseline, previous manifest, and approved crosswalk as frozen dependencies.

## Notes-only synchronization

When the canonical notes live in Markdown or a builder:

1. validate consecutive slide sections and nonempty bodies
2. generate notes in a disposable PPTX if a library is needed
3. follow slide relationship files to identify the correct notes part; do not assume `notesSlideN.xml` always maps to slide N
4. transplant only the required notesSlide XML parts
5. preserve all slide, media, master, layout, theme, and relationship parts
6. confirm embedded notes equal the canonical text after a declared normalization: Unicode NFC; `CRLF`, `CR`, and PowerPoint vertical tabs (`VT`) converted to `LF`; outer whitespace trimmed; internal empty paragraphs retained; internal words, spaces, and paragraph order otherwise unchanged
7. confirm Korean text language metadata when the environment requires it

Read note text objects once in shape-tree document order, including grouped shapes and tables. Exclude only slide-image, slide-number, header, footer, and date placeholders. Preserve explicit DrawingML breaks and tabs. Normalize every `mc:AlternateContent` branch independently. If branch results differ—including empty versus nonempty—fail with `ambiguous_alternatecontent_notes`; if every branch normalizes to the same empty result, treat the AlternateContent as empty. Never concatenate Choice and Fallback text.

If the existing notes-part topology differs from the candidate, stop and handle it as a structural edit rather than silently creating relationships.

For machine verification, export the canonical manuscript to a small UID-based JSON file:

```json
{
  "version": 1,
  "decks": [
    {
      "file": "lecture.pptx",
      "notes": [
        {"slide_uid": "opening-question", "text": "강사가 실제로 읽을 본문"},
        {"slide_uid": "concept-bridge", "text": "다음 개념으로 이어지는 본문"}
      ]
    }
  ]
}
```

The auditor applies the same NFC and line-ending normalization to this file and the embedded notes, then requires the current UID set and every note body to match exactly. Keep the richer Markdown manuscript if it is useful for editing, but generate this JSON deterministically from that canonical source rather than hand-copying it.

## Structural changes

After adding, deleting, or reordering slides, verify:

- presentation slide order
- page markers
- slide and notes counts
- one-to-one reciprocal slide ↔ notes relationships
- source footer and source-record mapping
- internal links and section references
- builder/Markdown indices
- Content Types and relationship targets

Re-number by slide identity and intent, not by blind numeric offset.

Do not hand-edit a large manifest by guessing identities. Before accepting a structural candidate, build a task-specific crosswalk from the old baseline and candidate: exact slide-hash matches first, unmatched old and new indices listed separately, and an explicit course-owner decision for every edited or ambiguous slide. A generic fuzzy title match is not safe enough. The bundled initializer verifies a fresh batch; it does not certify the prior-batch crosswalk.

## Package audit

At minimum check:

- ZIP CRC, duplicate or unsafe member names
- every XML and relationship part parses
- Content Types defaults and overrides are nonempty and unique, every override points to a member, every member is covered, render-critical presentation parts use their expected MIME types, and every `.rels` part resolves to the fixed OPC relationships MIME type
- internal relationship targets exist
- XML relationship IDs resolve to the companion `.rels` file
- slide/notes mapping is reciprocal
- expected slide and notes counts
- no unexpected audio, video, or embedded files
- package can be opened by PowerPoint and the chosen library
- start and end hashes match during read-only audit

For a release candidate, a stronger package command is:

```bash
python -B scripts/audit_pptx_package.py DECK.pptx --manifest manifest.json --baseline-root BASELINE_FOLDER --source-ledger source-ledger.json --canonical-notes canonical-notes.json --frozen-dependency rights-manifest.json --require-source-keys --require-notes --forbid-note-metadata --forbid-audio --forbid-video --forbid-external-file-links --forbid-embeddings --forbid-activex --forbid-macros --expected-slides N --rounds 2 --redact-paths
```

Use `--exclude-regex` when auditing a directory that also contains backups or prior deliverables. Set an explicit expected count or manifest so a structurally consistent missing slide cannot pass unnoticed. Repeat `--frozen-dependency` for a rights ledger, asset manifest, approval record, or other release input that must not change during the audit. The script freezes current decks, immutable baselines, manifest, source ledger, canonical notes, and those additional dependencies; rediscovers directory inputs on every round; enforces ZIP size/member/ratio limits before CRC decompression; and writes only to a new `.json` path. It never replaces an existing report, manifest, source file, or deck. With `--redact-paths`, local paths and deck filenames in normal fields and error details become redaction tokens. Non-sensitive web URI bytes remain unchanged even when the same diagnostic also contains a local path, while nested percent-encoded local paths inside URI path, query, fragment, or mail body components are redacted.

The optional machine ledger is a JSON object with either `{"source_keys": ["SRC-001", "IMG-001"]}` or `{"sources": [{"key": "SRC-001"}]}`. The auditor confirms that every manifest key exists in that ledger. Human source review must still verify that the cited item actually supports the slide.

The included `scripts/audit_pptx_package.py` covers Transitional OOXML only and fails explicitly on Strict OOXML. It rejects unsafe, trailing-dot, non-pchar, or canonically aliased OPC part names, relationship targets, and `[Content_Types].xml` override names; validates render-critical part root QNames and MIME types, the fixed `.rels` MIME, relationship-list membership, every slide-layout-to-master backlink against an exact single reverse owner, presentation reachability for every layout master, master theme cardinality, and numeric or relationship ID schemas; and rejects malformed `mc:AlternateContent` structures, including missing Choice/Requires, undeclared or invalid Requires prefixes, duplicate or misplaced Fallback, and empty branches. It parses both XML and VML relationship sources, accepts relationship-reference attributes only at schema-aware element/attribute locations, and validates the source/target roles used by typed asset-ownership traversal. It detects audio, video, embedded objects, ActiveX, and VBA evidence through package parts plus relationship/content types. The manifest initializer imports the same package validators. For each package inspection, the validator streams the package once into a private spooled snapshot; package SHA, ZIP members, and XML payloads all come from that same snapshot, so it cannot freeze a baseline that the auditor would reject under these rules. It does not prove visual or factual correctness.

Keep generated `__pycache__/` and `*.pyc` files outside version control and release hashes. Run reusable checks with `python -B` or in an isolated test copy, and compute a source-only release manifest so interpreter caches cannot create false hash drift.

For Strict OOXML, preserve the original and stop. Either use a Strict-capable Open XML SDK audit or obtain explicit approval to make a staged copy through PowerPoint's normal `.pptx` save path. Never convert the live file in place. A converted copy remains provisional until slide and note counts, stable manifest mapping, protected edits/assets, source records, package relationships, and full PowerPoint renders are compared with the original. Without that comparison, delivery validation is pending.

The strong command above assumes the delivery deck should contain no audio, video, OLE package, or ActiveX control. If intentional media is required, omit only the relevant forbid flag and maintain a separate allow-list containing the package part, SHA-256, media type, owning slide UID, and expected relationship. Verify that old shared media has no remaining inbound relationship before deleting it.

## PowerPoint rendering and visual QA

Use the actual PowerPoint renderer for a delivery deck. Export every slide at a fixed resolution and verify that the PNG count equals the slide count. Record the PowerPoint build, operating system, export resolution, installed fonts, and any font substitution. Use one of three explicit states:

- `delivery-complete`: native PowerPoint rendering passed
- `delivery-complete-with-renderer-exception`: a named alternative renderer/build/scope was accepted by the user or release owner, with `accepted_by` and `accepted_at`; never describe this state as “PowerPoint validated”
- `PowerPoint-validation-pending`: native rendering remains a P1 or delivery gate

Without native PowerPoint, do not claim native five-layer or five-full-audit saturation. Report a separately named `alternative-renderer audit` even when the exception permits delivery.

Check:

- text overflow using rendered bounds and text-box margins
- shapes outside slide bounds, with explicit exceptions for intentional cover bleed
- overlap that obscures text or changes relationship meaning
- run-level foreground/background contrast; use 4.5:1 for ordinary text and 3:1 for large text as a practical screen target
- orphan lines, single particles, lone symbols, and awkward word breaks
- alignment, equal gaps, optical centering, and arrow attachment
- captions, page numbers, source footers, and image credits
- title wrapping and density at normal viewing size
- alt text for meaningful images, logical reading order, color-independent meaning, and captions/transcripts for required media

An overflow count of zero does not prove contrast, orphan-line, or overlap quality. Inspect individual slides and contact sheets.

Automated PowerPoint scripts must record skipped shapes and exceptions. Do not hide errors with an empty `catch` block.

## Severity

- **P0:** unusable or dangerous output, corrupted deck, missing required content, major factual/legal error
- **P1:** material learner misunderstanding, lost user edit, major visual obstruction, incorrect claim scope, failed synchronization
- **P2:** real but localized clarity, wording, contrast, alignment, provenance, or reproducibility defect

Do not label subjective preferences as defects without an observable learner, factual, visual, or preservation consequence.

## Hash stability versus saturation

Repeated hash reads prove stability, not revision saturation. When the user requests saturation or the release is high risk, audit the same frozen candidate through independent layers:

1. actual PowerPoint rendering and visual geometry
2. learner flow, comprehension, and instructor read-aloud quality
3. facts, law, sources, rights, and claim strength
4. OOXML/ZIP/notes/source synchronization
5. explicit user-instruction checklist

Each layer records start and end hashes and reports P0/P1/P2. Any issue or file-hash change resets the clean streak. Repeating one deterministic script five times does not count as five independent audits.

Define the requested finish line explicitly:

- **five-layer pass:** each of the five independent layers runs once on the same frozen hash
- **five consecutive full audits:** the complete required audit bundle runs five times; a layer is not a substitute for a full round

Do not use the phrases interchangeably.

Require a five-layer pass for a high-risk release. Require five consecutive full audits only when the user explicitly requests that stronger finish line. Keep ordinary revisions proportional.

Record the evidence in an audit matrix rather than a prose-only claim:

| Round | Layer | Reviewer/tool and version | Start SHA-256 | End SHA-256 | P0 | P1 | P2 | Exception | Pass |
|---:|---|---|---|---|---:|---:|---:|---|---|

For five consecutive full audits, every required layer must appear in every round. A changed hash, missing layer, unapproved exception, or nonzero severity resets the streak.

## Handoff evidence

Report:

- final absolute paths and slide counts
- final SHA-256 values
- which manual edits were protected
- slide/notes/source synchronization result
- render and package results
- whether learner review was virtual or involved actual participants
- whether TTS or timing optimization was run
- unresolved rights, approval, or distribution gates

Delivery completion means no P0 or P1 remains, the declared renderer state is satisfied, and any accepted P2 is explicitly listed. Record every accepted P2 with `accepted_by`, `accepted_at`, `rationale`, and `release_scope`; the person accepting it must be the user or named release owner, not the authoring agent. Saturation means P0/P1/P2 are all zero under the requested audit definition and renderer class. Public distribution is blocked whenever a required asset permission or legal-use basis remains unresolved; do not downgrade that state to a generic warning. Apply the organization's retention and access policy to backups and temporary clones, and redact local paths or personal data from reports that leave the working environment.
