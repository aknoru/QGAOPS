from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
required = [
    "docs/requirements/requirements_specification.md",
    "docs/requirements/traceability_matrix.csv",
    "docs/mathematics/cl30_specification.md",
    "docs/research/literature_review.md",
    "docs/research/related_work_comparison.md",
    "docs/architecture/system_architecture.md",
    "docs/architecture/project_flow.md",
    "docs/architecture/hardware_transaction_flow.md",
    "docs/architecture/implementation_variants.md",
    "docs/planning/project_gantt.md",
    "docs/verification/verification_plan.md",
    "references/references.bib",
    "references/paper_manifest.csv",
]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("missing required documents: " + ", ".join(missing))
for path in ROOT.joinpath("docs").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if "\x00" in text or not text.strip():
        raise SystemExit(f"invalid or empty document: {path}")
with (ROOT / "references/paper_manifest.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
if len(rows) != 9:
    raise SystemExit(f"expected 9 manifest rows, found {len(rows)}")
print(f"documentation OK: {len(list(ROOT.joinpath('docs').rglob('*.md')))} Markdown files")
