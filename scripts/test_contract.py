import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from software.hardware_interface.contract import OperationRequest, deserialize, serialize
from software.reference_model.qgaops_reference import FixedPointMultivector

zero = tuple([0] * 8)
request = OperationRequest("geometric_product", zero, zero)
assert deserialize(serialize(request)) == request
try:
    deserialize(b"\0")
except ValueError:
    pass
else:
    raise SystemExit("malformed request was accepted")
print("hardware contract tests OK")
