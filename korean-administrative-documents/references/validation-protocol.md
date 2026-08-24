# Frozen-output validation protocol

## Required checks

1. Required artifact inventory and extensions
2. Source preservation and content invariants
3. ZIP/XML integrity for DOCX/HWPX/XLSX
4. Black text and approved gray fills; no unexplained blue/red
5. Table header/label alignment, fixed widths, compact cell margins, repeated header rows, and row-split control
6. Left-aligned attachment headings and mechanically aligned attachment numbers
7. Page-number fields and visible PDF page numbers
8. No standalone `문서` title in an official letter
9. Completion/commencement title and body on the same first page
10. PDF page count, nonblank pages, page bounds, and visual review
11. XLSX values/formulas/sheet names/row counts unchanged and print settings applied
12. SHA-256 manifest and deterministic validation results

## Saturation rule

Validation is complete only after the same frozen artifact tree passes the complete audit five consecutive times with zero issues.

- Compute the tree hash of every file below the final folder before every round, excluding only the current audit report itself
- Run the full audit, not one rotating subset
- Record each round's tree hash, issue count, issues, and clean-streak value, plus cumulative issues across rounds
- Reset the clean streak to zero after any issue
- Reset the clean streak to zero if any artifact hash changes
- Do not hard-code `streak=5` merely because one execution passed
- Treat one to four clean rounds as `incomplete_clean_streak`, not a successful final audit

Use `python -B scripts/audit_administrative_documents.py FINAL_FOLDER --rounds 5`. When a parallel source tree exists, add `--baseline SOURCE_FOLDER` to compare XLSX sheet order, dimensions, merged ranges, cell values, data types, and formulas. The auditor leaves artifacts read-only and writes only the selected JSON report. Result ordering and hashes are deterministic; the report timestamp intentionally changes between executions.

Different visual focus labels may be added to the five rounds, but they supplement rather than replace the complete audit.

## Human-only fields

Keep seals, signatures, final approval, and submission authority outside automated validation. Report them as explicit handoff actions. A successful technical audit must never imply that a human seal or approval exists.
