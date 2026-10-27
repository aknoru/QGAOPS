"""
tests/test_ir.py — IR serialization tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import pytest
from ga.ir import OperationIR, make_ir, OPCODES


# ---------------------------------------------------------------------------
# JSON round-trip
# ---------------------------------------------------------------------------

def test_ir_json_round_trip():
    ir = make_ir("GP", ["v1", "v2"], "r1", algebra="G3", precision="FIX16", expression="TWO_FINGER")
    j  = ir.to_json()
    ir2 = OperationIR.from_json(j)
    assert ir2.opcode    == ir.opcode
    assert ir2.algebra   == ir.algebra
    assert ir2.precision == ir.precision
    assert ir2.inputs    == ir.inputs
    assert ir2.output    == ir.output
    assert ir2.expression == ir.expression

def test_ir_dict_round_trip():
    ir = make_ir("WEDGE", ["a", "b"], "wedge_result")
    d  = ir.to_dict()
    ir2 = OperationIR.from_dict(d)
    assert ir2.opcode == "WEDGE"
    assert ir2.inputs == ["a", "b"]


# ---------------------------------------------------------------------------
# Binary round-trip
# ---------------------------------------------------------------------------

def test_binary_round_trip():
    for opcode in ["GP", "WEDGE", "SANDWICH", "REVERSE", "DOT"]:
        ir = make_ir(opcode, ["x", "y"], "result")
        encoded = ir.encode_command()
        decoded = OperationIR.decode_command(encoded)
        assert decoded.opcode == opcode, f"Expected {opcode}, got {decoded.opcode}"

def test_binary_invalid_magic():
    with pytest.raises(ValueError, match="Invalid magic"):
        OperationIR.decode_command(b'\x00\x00' + b'\x01' * 20)

def test_binary_too_short():
    with pytest.raises(ValueError, match="too short"):
        OperationIR.decode_command(b'\x51\x47\x01')


# ---------------------------------------------------------------------------
# make_ir convenience
# ---------------------------------------------------------------------------

def test_make_ir_defaults():
    ir = make_ir("GP", ["a", "b"])
    assert ir.algebra == "G3"
    assert ir.precision == "FLOAT32"
    assert ir.output == "result"
    assert ir.operation_id > 0

def test_make_ir_unique_ids():
    ids = [make_ir("GP", ["a"]).operation_id for _ in range(10)]
    assert len(set(ids)) == 10

def test_all_opcodes_encodable():
    for opname in OPCODES:
        ir = make_ir(opname, ["a", "b"])
        enc = ir.encode_command()
        assert len(enc) >= 13
