---
name: korean-administrative-documents
description: "Create, revise, and verify Korean administrative documents such as official letters (공문·시행문), commencement/completion forms (착수계·완료계·준공계), submission lists, attachment forms, and contract deliverable tables in DOCX, HWP/HWPX, XLSX, and PDF. Use when a Korean public-sector or research-institute submission must follow formal document structure, restrained gray/black styling, precise table widths and alignment, page numbering, attachment alignment, source preservation, and repeated frozen-output validation. Do not use for the substantive body of policy/research reports; use korean-policy-report for that content and this skill only for its administrative cover documents."
---

# Korean Administrative Documents

Create submission-ready documents from verified facts and supplied templates. Preserve the source package, write revised deliverables to a separate final folder, and never invent a telephone number, address, contract number, representative title, approval, seal, signature, or submission date.

## Route the task

- Read [official-letter-structure.md](references/official-letter-structure.md) for 공문·시행문, recipient lines, attachments, sender/seal, and closing metadata
- Read [table-layout-and-ooxml.md](references/table-layout-and-ooxml.md) when the task contains tables, DOCX, or XLSX
- Read [hwp-hwpx-template-workflow.md](references/hwp-hwpx-template-workflow.md) when HWP/HWPX or a dispatcher template is involved
- Read [validation-protocol.md](references/validation-protocol.md) before rendering or declaring completion

## Work in this order

1. Inventory every source and output format, including attachments, query lists, spreadsheets, reports, and PDFs that inherit the instruction “all tables” or “apply this to the following documents too”
2. Extract verified facts and template rules into a small manifest; mark unknown contact and approval fields as unresolved instead of fabricating values
3. Derive a file-specific layout specification before editing: document structure, font hierarchy, table widths, semantic alignment, shading, repeated headers, page numbering, and expected page count
4. Modify a reproducible builder or normalizer; keep source data, formulas, values, and row counts unchanged unless the user explicitly requests content changes
5. Render DOCX/HWP/HWPX/XLSX to PDF where applicable and inspect every page automatically plus representative first, middle, last, dense, and boundary pages visually
6. Fix every discovered issue, freeze the artifact hashes, and run the complete audit five consecutive times with zero issues; reset the streak to zero after any issue or hash change
7. Keep validation JSON, artifact hashes, and a concise README beside the final package

## Mandatory visual system

- Use the supplied template fonts. If the completion-form template establishes the system, normally use `HY헤드라인M` for major titles and `휴먼명조` for Korean body text; use an available documented fallback only when the font is unavailable
- Use black text by default. Do not use blue or red text for ordinary administrative content
- Use white page backgrounds and restrained neutral grays such as `D9D9D9`, `E7E6E6`, or `F2F2F2` for header/label cells; do not use blue fills
- Center table headers and form labels. Center short identifiers, dates, counts, contract numbers, company names, representative names, and other compact form values when the template calls for it. Left-align prose, addresses, descriptions, and long evidence text
- Use fixed table layout. Keep narrow label columns near 20–30% and content columns near 70–80% unless the content requires another documented ratio. Update both OOXML `tblGrid/gridCol` and cell `tcW`; setting cell width alone is insufficient
- Keep cell left/right margins compact, normally 90–180 twips. Repeat table headers and prevent inappropriate row splits
- Left-align `붙임 1`, `붙임 2`, and similar subsection headings. For an attachment list, use real tab stops or a borderless label/number/content table; never align numbers with runs of spaces
- Add centered continuous page numbers to all deliverables, including one-page documents when requested

## Document-specific rules

### Official letter

Use: sender organization → 수신/(경유 or 참조 if needed)/제목 → numbered body → 붙임 → sender name and seal position → 시행/contact closing block. Do not use a standalone title such as `문서`. Keep the title short and descriptive. Put each attachment on its own aligned row, and place `끝.` after the final item. Keep `(직인)` adjacent to the authorized sender name; do not approximate placement with many spaces.

### Commencement, completion, and submission forms

Keep the title and substantive form on the same first page. Remove accidental title-only pages and excessive spacer rows. Center the form's identity labels and compact values; keep addresses and long descriptions left-aligned. Use only verified dates and black text. Preserve the dispatcher wording and required recipient line.

### Query lists and supporting spreadsheets

Keep workbook cell values, formulas, row order, and sheet names unchanged. Use gray headers, black text, centered header/label cells, bounded column widths, repeated print-title rows, landscape/fit-to-width settings where useful, and footer page fields. In derived DOCX tables, make the label column visibly narrower than the value column and verify the rendered PDF rather than trusting the library width object.

## Validation and handoff

Run `python -B scripts/audit_administrative_documents.py FINAL_FOLDER --rounds 5` against the final folder. Add `--baseline SOURCE_FOLDER` when a parallel source tree exists and XLSX values, formulas, sheet order, dimensions, and merges must remain invariant. The auditor modifies no deliverable artifact; it writes only its JSON report. A one-to-four-round clean run is explicitly incomplete, never a final pass. Its report is evidence, not a substitute for visual inspection. A valid handoff includes the source-preservation statement, final artifact folder, file/page counts, issue count, five-round zero-issue streak, all-file tree hash, and any fields that still require human seal/signature/approval.

Do not publish real contracts, company details, personal data, dispatcher files, or deliverables inside this skill. Store only generalized rules and scripts.
