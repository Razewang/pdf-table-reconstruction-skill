---
name: pdf-table-reconstruction
description: Convert scanned, image-based, or complex PDF tables into traceable Excel workbooks. Use when Codex needs to normalize a source PDF to input.pdf, run a PDF table reconstruction pipeline, inspect status/log files, verify reconstructed_tables.xlsx and review_notes.xlsx, preserve intermediate evidence, and report low-confidence OCR or possible column-shift warnings.
---

# PDF Table Reconstruction

## Overview

Use this skill to run and report a PDF-to-Excel table reconstruction workflow where traceability matters. The expected deliverables are `output/reconstructed_tables.xlsx`, `output/review_notes.xlsx`, and `output/intermediate/`.

## Standard Workflow

1. Work in the project directory that contains the reconstruction scripts.
2. Normalize the source PDF to `input.pdf`. If the user provides another PDF path, copy it to `input.pdf` before running.
3. Prefer the wrapper:

```bash
python run_pipeline.py
```

4. If the wrapper is unavailable, run:

```bash
python reconstruct_tables.py
```

5. Always inspect `run_status.json` or `output/run_status.json` after running.
6. If the status is missing or failed, inspect `pipeline_run.log` or `output/pipeline_run.log`.
7. Open or summarize `output/review_notes.xlsx` before calling the result complete.

## Dependencies

Install common dependencies if they are missing:

```bash
python -m pip install pymupdf opencv-python numpy pandas openpyxl pytesseract
```

Use lighter OCR first when available, such as RapidOCR if the project already requires it. Do not install PaddleOCR or `paddlepaddle` unless the user explicitly accepts heavier OCR dependencies.

## Validation

Validate these artifacts:

- `output/reconstructed_tables.xlsx` exists and can be opened.
- `output/review_notes.xlsx` exists and contains traceable review rows.
- `output/intermediate/` contains page renders, table crops, OCR JSON, or debug images.
- Status is `done`, or the blocker is clearly explained.
- Any timestamped fallback workbook is reported if the standard Excel path was locked.

Use `scripts/summarize_run.py` from this skill when a concise machine-readable run summary is useful:

```bash
python path/to/pdf-table-reconstruction/scripts/summarize_run.py --workdir .
```

## Review Rules

Treat OCR output as provisional when:

- `review_notes.xlsx` contains `low_confidence_cell`.
- The status or notes mention possible column shifts, region mixing, header alignment, or structure warnings.
- Text appears mojibaked or visibly garbled.
- Table row/column counts look implausible for the source image.

Preserve traceability. Do not silently correct OCR text without recording the original text, corrected text, reason, confidence, and source location in review notes.

## Reporting

Return a concise summary with:

- Working directory
- Source PDF path
- Excel output path
- Review notes path
- Intermediate directory path
- Status/log path
- Pages, tables, and notes count when available
- Low-confidence or manual-review warnings

If outputs cannot be generated, report the blocker and the exact next command or file to inspect.
