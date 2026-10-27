from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = ["README.md", "pyproject.toml", "docs", "references", "scripts"]
missing = [item for item in required if not (ROOT / item).exists()]
if missing:
    raise SystemExit(f"missing required repository paths: {', '.join(missing)}")
print(f"environment OK: Python {sys.version.split()[0]}; root={ROOT}")
