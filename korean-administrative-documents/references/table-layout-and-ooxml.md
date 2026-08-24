# Table layout and OOXML checks

## Semantic alignment

- Header and label cells: horizontal and vertical center
- Short identifiers, dates, counts, names, contract numbers: usually center when used as form values
- Addresses, descriptions, titles that read as prose, evidence, and long lists: left
- Attachment subsection titles: left
- Numeric data columns: follow the document's stated convention, usually right for comparable quantities and center for simple counts

## Widths and margins

Use fixed layout for administrative tables. Typical two-column form ratios are 20–30% label and 70–80% value. For a 17 cm content width, a practical query mapping table is roughly 3.6 cm + 13.4 cm.

In DOCX, update all of the following:

- `w:tblLayout w:type="fixed"`
- `w:tblW`
- every `w:tblGrid/w:gridCol`
- each cell's `w:tcW`

If `tblGrid` remains 50:50, Word or Hancom may ignore the visible library width settings. Inspect the rendered PDF.

Keep cell left/right margins compact, usually 90–180 twips. Use `w:tblHeader` for repeating header rows and `w:cantSplit` to prevent unsuitable row splits.

## Color policy

Use black text and a small gray palette:

- `D9D9D9`: primary header
- `E7E6E6`: label cell
- `F2F2F2`: secondary or signature placeholder

Treat blue fills and blue/red text as issues unless the user or controlling template explicitly requires them. Check both theme colors and explicit RGB values in OOXML, HWPX XML, and XLSX styles.

## XLSX print layout

- Preserve values, formulas, row order, and sheet names
- Repeat the header row with `print_title_rows`
- Freeze the first data row below the header on every populated sheet (normally `A2`)
- Use landscape and `fitToWidth=1` for wide mapping sheets
- Use A4, `fitToHeight=0`, and add `&P` or `&[Page]` to a centered footer
- Bound text-heavy columns; approximately 45 characters is a practical upper bound unless a documented exception is necessary
- Verify that merged cells, filters, freeze panes, and formulas remain intact
