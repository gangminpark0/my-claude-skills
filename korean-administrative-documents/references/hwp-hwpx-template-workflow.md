# HWP and HWPX template workflow

## Preserve the controlling template

When the dispatcher supplied a HWP/HWPX form, treat its wording, field order, font hierarchy, and recipient line as controlling unless the user instructs otherwise. Extract the template structure before editing. Preserve the original separately.

Typical Korean administrative-form typography may use `HY헤드라인M` for major titles and `휴먼명조` for body text. Reuse the actual supplied template fonts when available. Do not silently substitute fonts without documenting the fallback.

## Conversion

Prefer a reproducible conversion route and record it. On Windows, Hancom automation may be used for DOCX → HWP/HWPX/PDF, but validate the result because imports can alter table grids, footer fields, page breaks, and fonts.

For HWPX:

- Verify ZIP integrity
- Parse every XML member
- Check `mimetype`, section files, style references, and page-number auto fields
- Confirm that gray fills and black text survived conversion
- Confirm that title and body remain on the intended page

For binary HWP:

- Extract or inspect `DocInfo` character shapes when possible
- Confirm that red contract-date styles and oversized wrapper rows are absent
- Validate the rendered PDF for pagination and footer page numbers

## Visual review

Render every PDF page. Automatically check blank pages, overflow, missing footers, and inconsistent page sizes. Visually inspect at least first, last, densest, sparsest, transition, and table-boundary pages for each document. For short administrative documents, inspect every page directly.
