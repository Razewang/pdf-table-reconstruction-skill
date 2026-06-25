from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def first_existing(base: Path, names: list[str]) -> Path | None:
    for name in names:
        path = base / name
        if path.exists():
            return path
    return None


def workbook_notes_count(path: Path) -> tuple[int | None, int | None]:
    try:
        import pandas as pd
    except Exception:
        return None, None

    try:
        df = pd.read_excel(path)
    except Exception:
        return None, None

    low_count = int((df.get("confidence", "") == "low").sum()) if "confidence" in df else 0
    return int(len(df)), low_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a PDF table reconstruction run.")
    parser.add_argument("--workdir", default=".", help="Project directory containing input.pdf and output/.")
    args = parser.parse_args()

    base = Path(args.workdir).resolve()
    status_path = first_existing(base, ["output/run_status.json", "run_status.json"])
    log_path = first_existing(base, ["output/pipeline_run.log", "pipeline_run.log"])
    notes_path = base / "output" / "review_notes.xlsx"
    evidence_path = base / "output" / "model_review_evidence.json"

    status: dict[str, Any] = read_json(status_path) if status_path else {}
    evidence: dict[str, Any] = read_json(evidence_path) if evidence_path.exists() else {}
    notes_count, low_notes_count = workbook_notes_count(notes_path) if notes_path.exists() else (None, None)

    outputs = status.get("outputs", {})
    warnings = status.get("warnings") or evidence.get("warnings") or []
    summary = {
        "workdir": str(base),
        "status": status.get("status"),
        "source_pdf": status.get("source_pdf") or status.get("input") or str((base / "input.pdf").resolve()),
        "excel": outputs.get("excel_actual") or outputs.get("excel") or str((base / "output" / "reconstructed_tables.xlsx").resolve()),
        "review_notes": outputs.get("notes") or str(notes_path.resolve()),
        "intermediate": outputs.get("intermediate") or str((base / "output" / "intermediate").resolve()),
        "status_path": str(status_path.resolve()) if status_path else None,
        "log_path": str(log_path.resolve()) if log_path else None,
        "pages": status.get("pages") or evidence.get("pages"),
        "tables": status.get("tables") or evidence.get("tables"),
        "review_notes_rows": status.get("review_notes_rows") or notes_count,
        "low_confidence_notes": status.get("low_confidence_notes") or low_notes_count,
        "warnings_count": len(warnings),
        "warnings_sample": warnings[:10],
        "excel_note": outputs.get("excel_note"),
        "error": status.get("error"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "done" else 1


if __name__ == "__main__":
    raise SystemExit(main())
