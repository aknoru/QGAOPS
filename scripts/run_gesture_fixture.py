from pathlib import Path
from software.gesture_pipeline.pipeline import load_fixture, nearest_centroid

root = Path(__file__).resolve().parents[1]
result = nearest_centroid(load_fixture(root / "software/gesture_pipeline/fixtures.json"))
(root / "results/processed/gesture_fixture_result.json").write_text(
    __import__("json").dumps(result, indent=2) + "\n", encoding="utf-8"
)
print(result)
