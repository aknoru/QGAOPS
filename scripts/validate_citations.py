from pathlib import Path
import re
import csv

ROOT = Path(__file__).resolve().parents[1]
bib = (ROOT / "references/references.bib").read_text(encoding="utf-8")
keys = set(re.findall(r"@\w+\{([^,]+),", bib))
manifest = list(csv.DictReader((ROOT / "references/paper_manifest.csv").open(encoding="utf-8", newline="")))
manifest_keys = {row["citation_key"] for row in manifest}
if keys != manifest_keys:
    raise SystemExit(f"BibTeX/manifest mismatch: bib-only={keys - manifest_keys}, manifest-only={manifest_keys - keys}")
used_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "docs/research").glob("*.md"))
used = set(re.findall(r"\[([A-Za-z][A-Za-z0-9]+)\]", used_text))
unknown = used - keys
if unknown:
    raise SystemExit(f"unknown citation keys: {sorted(unknown)}")
print(f"citation OK: {len(keys)} bibliography entries, {len(used & keys)} cited keys")
