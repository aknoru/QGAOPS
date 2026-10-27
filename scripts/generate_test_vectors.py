import json
from pathlib import Path
from software.hardware_interface.contract import OperationRequest, serialize
from software.reference_model.qgaops_reference import FixedPointMultivector, blade

root = Path(__file__).resolve().parents[1]
vectors = []
for operation in ("geometric_product", "wedge", "hestenes_inner"):
    left = FixedPointMultivector.from_reals(blade("e1").coefficients)
    right = FixedPointMultivector.from_reals(blade("e2").coefficients)
    request = OperationRequest(operation, left.coefficients, right.coefficients)
    vectors.append({"operation": operation, "payload_hex": serialize(request).hex()})
path = root / "docs/verification/hardware_test_vectors/stage9_vectors.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(vectors, indent=2) + "\n", encoding="utf-8")
print(f"wrote {path}")
