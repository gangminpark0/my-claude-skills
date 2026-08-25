# Sources, Claims, Assets, and Rights

Use a source record so that the slide and narration can remain teachable without losing provenance.

## Establish the citation policy

Follow the user's explicit policy. A useful default for a read-aloud course is:

- concise external-source footer on the slide when the claim or asset needs attribution
- full citation, URL, access date, page, and verification note in a separate source record
- no citation list, URL, DOI, or production metadata in the spoken notes
- internal course documents recorded as internal provenance, not disguised as external scholarship

Do not replace an internal source with an unrelated external citation merely to make every slide appear externally sourced. A course objective, instructor framework, or classroom activity may have no external authority; record its provenance honestly.

## Claim ledger

Keep one row per material claim:

| Slide | Claim | Claim type | Source | Page/section | Date/denominator | Allowed wording | Limit or caveat | Verified |
|---:|---|---|---|---|---|---|---|---|

Useful claim types:

- observed statistic
- estimate or forecast
- self-reported survey
- experimental result
- vendor or company case
- legal rule
- historical interpretation
- classroom synthesis or hypothetical example

The allowed wording should match the evidence type. A vendor case may show an implementation pattern but normally cannot establish an independent causal effect. A self-report may show perceived differences but not prove their cause.

Store the ledger in a version-controlled CSV, Markdown table, or project database with explicit status values such as `unverified`, `verified`, `superseded`, and `blocked`. Add verifier and verification date when several people share the release responsibility.

For machine cross-checking, give every ledger row a stable unique key. A small companion JSON may expose those keys as `{"source_keys": ["SRC-001", "IMG-001"]}` while the full human-readable ledger keeps citations, URLs, pages, rights, and verification notes. Map slides to `source_keys[]`. A slide with no external claim or asset may instead use a reviewed exemption of type `navigation`, `activity`, `instructor_synthesis`, or `original_course_instruction`, with a concrete rationale, reviewer, and review date. The reviewer must be the course owner or named source reviewer, not the authoring agent. Do not use `N/A`, `none`, or another placeholder to bypass source review.

## Quantitative claims

Record and preserve:

- measured object
- numerator and denominator
- population and geography
- date or period
- unit
- observed, estimated, forecast, or modeled status
- percentage versus percentage-point change
- sample and task boundary

If two values have different questions or denominators, explain their separate meanings rather than putting them into a false ranking.

## Law and regulation

Use current primary legal text when accuracy matters. Record:

- jurisdiction and official identifier
- version or amendment date
- covered subject and conduct
- effective or application date
- conditions and exceptions
- transition provisions
- statutory maximum versus actual enforcement outcome

If a rule has been enacted but is not yet applicable, say so on the slide or in the narration wherever omission would make students treat it as current.

## Image and media manifest

For each used asset, record:

| Slide | File/SHA-256 | Creator/rightsholder | Source page | Direct asset URL | Caption/context | License or permission | Crop/edit | Distribution status |
|---:|---|---|---|---|---|---|---|---|

Important distinctions:

- a source link is not a redistribution license
- a visible credit is not permission
- a screenshot may contain several separately protected elements
- a user-inserted asset should be preserved unless the user authorizes replacement, but its rights uncertainty must be reported before public distribution
- an unused local asset should not be described as present in the final deck

Keep exact hashes when the same-looking asset could be confused with another photograph or edition.

## Screen/source synchronization

If the authoring source stores a short footer such as `source_short`, verify it against the actual visible footer on every slide. After insertion or deletion, re-map source records by the stable slide-manifest key. Treat title, index, relationship ID, and content fingerprint as supporting evidence rather than a single invariant identity.

Do not narrate production qualifiers that learners do not need. Keep them in the source record unless the qualifier changes interpretation. For example, `회사 발표` may matter; `강의자 재구성` usually does not.

## Release gates

Separate content defects from operational rights gates:

- wrong source, date, denominator, or attribution: content defect
- missing or uncertain permission for public redistribution: public-release blocker
- package integrity: technical defect

Do not report a rights warning as resolved merely because the slide contains a citation.
