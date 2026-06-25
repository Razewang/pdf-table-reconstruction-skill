# PDF Table Reconstruction Skill

Codex skill for converting scanned, image-based, or complex PDF tables into traceable Excel outputs.

This skill is designed for projects that reconstruct PDF tables into:

```text
output/reconstructed_tables.xlsx
output/review_notes.xlsx
output/intermediate/
```

It emphasizes traceability: OCR corrections, low-confidence cells, possible column shifts, table crops, debug images, and status files should remain inspectable after each run.

## What It Does

- Normalizes a source PDF to `input.pdf`.
- Runs the preferred reconstruction wrapper, usually `python run_pipeline.py`.
- Falls back to `python reconstruct_tables.py` when no wrapper exists.
- Checks `run_status.json` or `output/run_status.json` after execution.
- Points Codex to logs when a run fails.
- Requires review of `output/review_notes.xlsx` before treating the workbook as final.
- Provides `scripts/summarize_run.py` to produce a concise JSON summary of a completed run.

## Skill Contents

```text
pdf-table-reconstruction/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- scripts/
    `-- summarize_run.py
```

## Use Cases

Use this skill when you need Codex to:

- Convert scanned or image-heavy PDF tables into editable Excel.
- Preserve intermediate evidence for manual review.
- Report low-confidence OCR cells clearly.
- Avoid silently accepting garbled text or shifted columns.
- Produce a concise handoff summary with output paths and warning counts.

## Basic Usage

Place or copy the target PDF into the working project as:

```text
input.pdf
```

Then ask Codex:

```text
Use $pdf-table-reconstruction to convert input.pdf into Excel and summarize the result.
```

The skill instructs Codex to prefer:

```bash
python run_pipeline.py
```

If unavailable, Codex should run:

```bash
python reconstruct_tables.py
```

## Summary Script

After a pipeline run, the bundled summary script can read status files and produce a compact JSON report:

```bash
python scripts/summarize_run.py --workdir /path/to/pdf-table-project
```

The summary includes:

- Working directory
- Source PDF path
- Excel output path
- Review notes path
- Intermediate directory path
- Status/log paths
- Page, table, and review-note counts
- Low-confidence warning count and a small warning sample

## Dependencies

Typical reconstruction projects need:

```bash
python -m pip install pymupdf opencv-python numpy pandas openpyxl pytesseract
```

Do not require PaddleOCR unless the user explicitly accepts heavier OCR dependencies.

## Privacy

This repository contains only the reusable Codex skill instructions and helper script. It does not include source PDFs, reconstructed Excel files, OCR logs, intermediate images, or private project outputs.
