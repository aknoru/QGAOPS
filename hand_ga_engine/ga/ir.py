"""
LIVE HAND GA ENGINE — ga/ir.py
QGAOPS Intermediate Representation (IR) for GA operations.

[IMPLEMENTED] JSON and binary serialization/deserialization.
[ARCH]        This IR is the interface between the software golden model
              and a future FPGA backend.

Each IR record describes one GA operation in a machine-readable format
suitable for hardware dispatch.
"""
from __future__ import annotations

import json
import struct
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

# Supported opcodes
OPCODES = {
    "GP":        0x01,   # Geometric Product
    "WEDGE":     0x02,   # Outer Product
    "INNER":     0x03,   # Inner Product
    "DOT":       0x04,   # Scalar Dot Product
    "REVERSE":   0x05,   # Reverse ~A
    "SANDWICH":  0x06,   # Sandwich R*v*~R
    "ROTOR":     0x07,   # Rotor construction
    "NORM":      0x08,   # Norm
    "DUAL":      0x09,   # Dual A*
    "COMMUT":    0x0A,   # Commutator [A,B]
    "ANTI_COMM": 0x0B,   # Anticommutator {A,B}
    "DISTANCE":  0x0C,   # Euclidean distance
    "VECTOR":    0x0D,   # Vector extraction
    "GRADE":     0x0E,   # Grade extraction
    "ADD":       0x10,   # Addition
    "SUB":       0x11,   # Subtraction
    "SCALE":     0x12,   # Scalar multiply
    "CROSS":     0x13,   # Cross product
}

ALGEBRA_IDS = {
    "G3":   0x01,
    "CGA":  0x02,
    "PGA":  0x03,
    "G4_1": 0x04,
}

PRECISION_IDS = {
    "FLOAT32": 0x01,
    "FIX16":   0x02,
    "FLOAT64": 0x03,
}

# Binary packet format:
# [MAGIC:2][VERSION:1][OPCODE:1][ALGEBRA:1][PRECISION:1][OP_ID:4][N_OPS:2]
# [N_INPUTS:1][INPUT_MASKS:8*N_INPUTS][OUTPUT_NAME_LEN:1][OUTPUT_NAME:N]
# [RESERVED:4]
MAGIC = bytes([0x51, 0x47])  # "QG" magic bytes for QGAOPS command packets
VERSION = 0x01
HEADER_FMT = ">2sBBBBI H B"  # magic(2), version(1), opcode(1), algebra(1), precision(1), op_id(4), n_operands(2), n_inputs(1)


@dataclass
class OperationIR:
    """A single QGAOPS IR operation record.

    [IMPLEMENTED] Full JSON and binary serialization.
    [ARCH]        Compatible with future FPGA command packet format.

    Attributes:
        opcode:       Operation name (e.g., 'GP', 'WEDGE').
        algebra:      Algebra name (e.g., 'G3').
        signature:    Metric signature tuple (e.g., [1,1,1]).
        precision:    'FLOAT32' or 'FIX16'.
        inputs:       List of input operand names/labels.
        output:       Output operand name/label.
        operation_id: Unique sequential ID.
        expression:   Gesture/expression that triggered this (optional).
        metadata:     Extra key-value info.
        timestamp:    Unix timestamp when created.
    """
    opcode:       str
    algebra:      str = "G3"
    signature:    List[int] = field(default_factory=lambda: [1, 1, 1])
    precision:    str = "FLOAT32"
    inputs:       List[str] = field(default_factory=list)
    output:       str = "result"
    operation_id: int = 0
    expression:   str = ""
    metadata:     Dict[str, Any] = field(default_factory=dict)
    timestamp:    float = field(default_factory=time.time)

    # ------------------------------------------------------------------
    # JSON serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a JSON-serializable dictionary."""
        return {
            "operation_id": self.operation_id,
            "opcode":       self.opcode,
            "algebra":      self.algebra,
            "signature":    self.signature,
            "precision":    self.precision,
            "inputs":       self.inputs,
            "output":       self.output,
            "expression":   self.expression,
            "metadata":     self.metadata,
            "timestamp":    self.timestamp,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OperationIR":
        """Deserialize from dict."""
        return cls(
            opcode=d["opcode"],
            algebra=d.get("algebra", "G3"),
            signature=d.get("signature", [1, 1, 1]),
            precision=d.get("precision", "FLOAT32"),
            inputs=d.get("inputs", []),
            output=d.get("output", "result"),
            operation_id=d.get("operation_id", 0),
            expression=d.get("expression", ""),
            metadata=d.get("metadata", {}),
            timestamp=d.get("timestamp", time.time()),
        )

    @classmethod
    def from_json(cls, s: str) -> "OperationIR":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(s))

    # ------------------------------------------------------------------
    # Binary serialization (for future FPGA DMA transfer)
    # ------------------------------------------------------------------

    def encode_command(self) -> bytes:
        """Encode IR to binary command packet.

        [PROPOSED for FPGA DMA] Format:
            Offset  Size  Field
            0       2     Magic "QG" (0x51 0x47)
            2       1     Version
            3       1     Opcode ID
            4       1     Algebra ID
            5       1     Precision ID
            6       4     Operation ID (uint32 big-endian)
            10      2     Number of inputs (uint16)
            12      1     Number of coefficients per operand (uint8)
            13+     var   Output name (length-prefixed UTF-8)
            ...     4     Reserved (0x00000000)

        Returns:
            Bytes object.
        """
        opcode_id    = OPCODES.get(self.opcode, 0xFF)
        algebra_id   = ALGEBRA_IDS.get(self.algebra, 0xFF)
        precision_id = PRECISION_IDS.get(self.precision, 0x01)
        n_inputs     = len(self.inputs)
        n_coeffs     = 8  # G3 always has 8 coefficients

        out_name = self.output.encode("utf-8")[:255]

        header = struct.pack(
            ">2sBBBBIHB",
            MAGIC,
            VERSION,
            opcode_id,
            algebra_id,
            precision_id,
            self.operation_id & 0xFFFFFFFF,
            n_inputs,
            n_coeffs,
        )
        name_block = struct.pack("B", len(out_name)) + out_name
        reserved   = struct.pack(">I", 0x00000000)

        return header + name_block + reserved

    @classmethod
    def decode_command(cls, data: bytes) -> "OperationIR":
        """Decode a binary command packet.

        [PROPOSED for FPGA DMA]

        Returns:
            Reconstructed OperationIR (metadata limited to what fits in packet).
        """
        if len(data) < 13:
            raise ValueError(f"Packet too short: {len(data)} bytes")

        magic = data[0:2]
        if magic != MAGIC:
            raise ValueError(f"Invalid magic bytes: {magic!r}")

        (magic_, ver, opcode_id, algebra_id, precision_id,
         op_id, n_inputs, n_coeffs) = struct.unpack(">2sBBBBIHB", data[:13])

        # Reverse-lookup opcode name
        opcode = next((k for k, v in OPCODES.items() if v == opcode_id), "UNKNOWN")
        algebra = next((k for k, v in ALGEBRA_IDS.items() if v == algebra_id), "G3")
        precision = next((k for k, v in PRECISION_IDS.items() if v == precision_id), "FLOAT32")

        name_len = data[13]
        out_name = data[14: 14 + name_len].decode("utf-8", errors="replace")

        return cls(
            opcode=opcode,
            algebra=algebra,
            precision=precision,
            inputs=[f"in{i}" for i in range(n_inputs)],
            output=out_name,
            operation_id=op_id,
        )

    def __repr__(self) -> str:
        return (
            f"OperationIR(id={self.operation_id}, opcode={self.opcode}, "
            f"algebra={self.algebra}, prec={self.precision}, "
            f"inputs={self.inputs}, out={self.output})"
        )


# ---------------------------------------------------------------------------
# IR sequence serialization
# ---------------------------------------------------------------------------

def save_ir_sequence(ops: List[OperationIR], path: str) -> None:
    """Save a list of IR operations to a JSON file."""
    import pathlib
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([op.to_dict() for op in ops], f, indent=2)


def load_ir_sequence(path: str) -> List[OperationIR]:
    """Load a list of IR operations from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    return [OperationIR.from_dict(d) for d in data]


# ---------------------------------------------------------------------------
# Counter for operation IDs
# ---------------------------------------------------------------------------

class _OpCounter:
    def __init__(self) -> None:
        self._n = 0

    def next(self) -> int:
        self._n += 1
        return self._n

_op_counter = _OpCounter()


def make_ir(
    opcode: str,
    inputs: List[str],
    output: str = "result",
    algebra: str = "G3",
    precision: str = "FLOAT32",
    expression: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> OperationIR:
    """Convenience factory for creating IR operations."""
    return OperationIR(
        opcode=opcode,
        algebra=algebra,
        signature=[1, 1, 1],
        precision=precision,
        inputs=inputs,
        output=output,
        operation_id=_op_counter.next(),
        expression=expression,
        metadata=metadata or {},
    )
