from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
expected = {
    "docs/architecture/system_architecture.md": "flowchart",
    "docs/architecture/project_flow.md": "flowchart",
    "docs/architecture/hardware_transaction_flow.md": "sequenceDiagram",
    "docs/architecture/implementation_variants.md": "flowchart",
    "docs/planning/project_gantt.md": "gantt",
}
for rel, kind in expected.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\s*\n(.*?)```", text, flags=re.S)
    if len(blocks) != 1 or not blocks[0].lstrip().startswith(kind):
        raise SystemExit(f"{rel}: expected one Mermaid block starting with {kind}")
print(f"Mermaid source OK: {len(expected)} diagrams")
