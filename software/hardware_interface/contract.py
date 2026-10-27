"""Deterministic serialization and validation for the Stage 9 hardware contract.

Reconciled Specification:
- Standard 76-byte DMA packet (12-byte aligned header + 64 bytes operands)
- Legacy 72-byte compact packet (8-byte header + 64 bytes operands)
"""

from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Iterable

from software.reference_model.qgaops_reference import FixedPointMultivector, FixedPointFormat

VERSION = 1
OPERATION_IDS = {
    "geometric_product": 1,
    "wedge": 2,
    "hestenes_inner": 3,
    "add": 4,
    "subtract": 5,
}
ID_OPERATIONS = {value: key for key, value in OPERATION_IDS.items()}
ERROR_CODES = {
    "ok": 0,
    "invalid_operation": 1,
    "invalid_length": 2,
    "version_mismatch": 3,
    "overflow": 4,
}

# 8-byte compact header and 12-byte DMA-aligned header
HEADER_8B = struct.Struct("<BBBBI")       # version, op_id, flags, reserved, batch_length
HEADER_12B = struct.Struct("<BBBBII")     # version, op_id, flags, reserved, batch_length, pad
COEFFICIENTS = struct.Struct("<8i")       # 8 x 32-bit signed Q16.16 (32 bytes)

HEADER = HEADER_12B  # Primary normative format is 12-byte header (76-byte request)


@dataclass(frozen=True)
class OperationRequest:
    operation: str
    left: tuple[int, ...]
    right: tuple[int, ...]
    version: int = VERSION


def _coefficients(values: Iterable[int]) -> tuple[int, ...]:
    result = tuple(values)
    if len(result) != 8 or any(not isinstance(value, int) or isinstance(value, bool) for value in result):
        raise ValueError("each operand requires exactly eight integer coefficients")
    fmt = FixedPointFormat()
    if any(value < fmt.minimum or value > fmt.maximum for value in result):
        raise ValueError("coefficient is outside signed Q16.16 storage range")
    return result


def serialize(request: OperationRequest, aligned_12b: bool = True) -> bytes:
    """Serialize an OperationRequest into a binary packet.
    
    If aligned_12b is True, produces the normative 76-byte packet with 12-byte header.
    If aligned_12b is False, produces the 72-byte compact packet with 8-byte header.
    """
    if request.version != VERSION:
        raise ValueError("unsupported interface version")
    if request.operation not in OPERATION_IDS:
        raise ValueError("unsupported operation")
    left, right = _coefficients(request.left), _coefficients(request.right)
    
    if aligned_12b:
        hdr = HEADER_12B.pack(VERSION, OPERATION_IDS[request.operation], 0, 0, 1, 0)
    else:
        hdr = HEADER_8B.pack(VERSION, OPERATION_IDS[request.operation], 0, 0, 1)
        
    return hdr + COEFFICIENTS.pack(*left) + COEFFICIENTS.pack(*right)


def deserialize(payload: bytes) -> OperationRequest:
    """Deserialize a 76-byte (12-byte header) or 72-byte (8-byte header) payload."""
    size_12b = HEADER_12B.size + 2 * COEFFICIENTS.size  # 12 + 64 = 76 bytes
    size_8b = HEADER_8B.size + 2 * COEFFICIENTS.size    # 8 + 64 = 72 bytes
    
    if len(payload) == size_12b:
        version, operation_id, _flags, _reserved, batch_length, _pad = HEADER_12B.unpack_from(payload)
        offset = HEADER_12B.size
    elif len(payload) == size_8b:
        version, operation_id, _flags, _reserved, batch_length = HEADER_8B.unpack_from(payload)
        offset = HEADER_8B.size
    else:
        raise ValueError(f"invalid request length: expected {size_12b} or {size_8b} bytes, got {len(payload)}")
        
    if version != VERSION:
        raise ValueError("unsupported interface version")
    if operation_id not in ID_OPERATIONS:
        raise ValueError("unsupported operation identifier")
    if batch_length != 1:
        raise ValueError("Stage 9 scalar request format requires batch length one")
        
    left = COEFFICIENTS.unpack_from(payload, offset)
    right = COEFFICIENTS.unpack_from(payload, offset + COEFFICIENTS.size)
    return OperationRequest(ID_OPERATIONS[operation_id], left, right, version)


def execute_contract(request: OperationRequest) -> tuple[FixedPointMultivector, int]:
    left = FixedPointMultivector(request.left)
    right = FixedPointMultivector(request.right)
    if request.operation == "add":
        result = left + right
    elif request.operation == "subtract":
        result = left - right
    else:
        result = getattr(left, request.operation)(right)
    return result, ERROR_CODES["overflow"] if result.overflowed else ERROR_CODES["ok"]
