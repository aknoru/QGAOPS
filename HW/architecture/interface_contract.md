# QGAOPS-QGPU Hardware Interface Contract Specification

## 1. Scope and Compliance

This document defines the normative hardware interface contract for the QGAOPS-QGPU accelerators (`SEQ_GPU` and `PARALLEL_GPU`). It maintains 100% mathematical and operational consistency with the software reference model ([`software/hardware_interface/contract.py`](file:///d:/QGPU/software/hardware_interface/contract.py) and [`software/reference_model/qgaops_reference/fixed_point.py`](file:///d:/QGPU/software/reference_model/qgaops_reference/fixed_point.py)).

---

## 2. Operation Identifiers (Opcodes)

The accelerator hardware supports 12 operations:

| Opcode | Mnemonic | Operation Description | Formula / Semantics | Operand A | Operand B |
|:---:|:---|:---|:---|:---|:---|
| **0x01** | `OPCODE_GP` | Geometric Product | $C = A B$ | Multivector $A$ | Multivector $B$ |
| **0x02** | `OPCODE_WEDGE` | Outer / Wedge Product | $C = A \wedge B$ | Multivector $A$ | Multivector $B$ |
| **0x03** | `OPCODE_INNER` | Hestenes Inner Product | $C = A \cdot B$ | Multivector $A$ | Multivector $B$ |
| **0x04** | `OPCODE_ADD` | Multivector Addition | $C = A + B$ | Multivector $A$ | Multivector $B$ |
| **0x05** | `OPCODE_SUB` | Multivector Subtraction | $C = A - B$ | Multivector $A$ | Multivector $B$ |
| **0x06** | `OPCODE_SCALAR_MUL` | Scalar Multiplication | $C = B_0 \cdot A$ | Multivector $A$ | $B_0$ in $B[0]$ |
| **0x07** | `OPCODE_GRADE_PROJ` | Grade Projection | $C = \langle A \rangle_k$ | Multivector $A$ | $k \in \{0,1,2,3\}$ in $B[0]$ |
| **0x08** | `OPCODE_REVERSE` | Reversion | $C = \widetilde{A}$ | Multivector $A$ | Ignored |
| **0x09** | `OPCODE_GRADE_INVOLUTION` | Grade Involution | $C = \widehat{A}$ | Multivector $A$ | Ignored |
| **0x0A** | `OPCODE_CLIFFORD_CONJ` | Clifford Conjugation | $C = \overline{A} = \widetilde{\widehat{A}}$ | Multivector $A$ | Ignored |
| **0x0B** | `OPCODE_SANDWICH` | Rotor Sandwich Product | $C = A B \widetilde{A}$ | Rotor $A$ | Target $B$ |
| **0x0C** | `OPCODE_ROTOR_NORM` | Rotor Norm Squared | $C[0] = \langle A \widetilde{A} \rangle_0$ | Rotor $A$ | Ignored |

---

## 3. Status and Error Codes

The 32-bit `status` output register returns execution diagnostics:

| Code | Bitmask | Identifier | Definition |
|:---:|:---:|:---|:---|
| **0x00** | `0b0000` | `STATUS_OK` | Operation completed normally without numerical overflow. |
| **0x01** | `0b0001` | `STATUS_ERR_OP` | Invalid or unsupported opcode supplied. Output multivector is zeroed. |
| **0x02** | `0b0010` | `STATUS_ERR_LEN` | Reserved / invalid vector length requested. |
| **0x04** | `0b0100` | `STATUS_OVERFLOW`| Intermediate product sum exceeded signed Q16.16 storage boundary. Output saturated to boundary. |

---

## 4. AXI4-Lite Register Map (`s_axilite`)

Base address is determined by Vivado address assignment (typically `0xA000_0000` for Zynq UltraScale+ or `0x43C0_0000` for Zynq-7000).

| Offset (Hex) | Register Name | Access | Width | Description / Field Encoding |
|:---|:---|:---:|:---:|:---|
| `0x00` | `AP_CTRL` | R/W | 32 | Bit 0: `ap_start` (W1S)<br>Bit 1: `ap_done` (R/COR)<br>Bit 2: `ap_idle` (RO)<br>Bit 3: `ap_ready` (RO)<br>Bit 7: `auto_restart` |
| `0x04` | `GIE` | R/W | 32 | Global Interrupt Enable (Bit 0: Enable) |
| `0x08` | `IER` | R/W | 32 | IP Interrupt Enable (Bit 0: Done Interrupt, Bit 1: Ready) |
| `0x0C` | `ISR` | R/W | 32 | IP Interrupt Status (Bit 0: Done Pending) |
| `0x10` | `OPCODE_DATA` | R/W | 32 | Bits [7:0]: Operation code (`0x01`–`0x0C`) |
| `0x14` | *Reserved* | - | 32 | - |
| `0x18` | `STATUS_DATA` | RO | 32 | Bits [7:0]: Accelerator status code (`0x00`, `0x01`, `0x04`) |
| `0x1C` | `STATUS_CTRL` | RO | 32 | Bit 0: `status_ap_vld` |
| `0x40` | `OPERAND_A_0` | R/W | 32 | Blade 0 ($1$) signed Q16.16 coefficient |
| `0x44` | `OPERAND_A_1` | R/W | 32 | Blade 1 ($e_1$) signed Q16.16 coefficient |
| `0x48` | `OPERAND_A_2` | R/W | 32 | Blade 2 ($e_2$) signed Q16.16 coefficient |
| `0x4C` | `OPERAND_A_3` | R/W | 32 | Blade 3 ($e_3$) signed Q16.16 coefficient |
| `0x50` | `OPERAND_A_4` | R/W | 32 | Blade 4 ($e_{12}$) signed Q16.16 coefficient |
| `0x54` | `OPERAND_A_5` | R/W | 32 | Blade 5 ($e_{13}$) signed Q16.16 coefficient |
| `0x58` | `OPERAND_A_6` | R/W | 32 | Blade 6 ($e_{23}$) signed Q16.16 coefficient |
| `0x5C` | `OPERAND_A_7` | R/W | 32 | Blade 7 ($e_{123}$) signed Q16.16 coefficient |
| `0x60` | `OPERAND_B_0` | R/W | 32 | Blade 0 ($1$) signed Q16.16 coefficient (or scalar/grade) |
| `0x64` | `OPERAND_B_1` | R/W | 32 | Blade 1 ($e_1$) signed Q16.16 coefficient |
| `0x68` | `OPERAND_B_2` | R/W | 32 | Blade 2 ($e_2$) signed Q16.16 coefficient |
| `0x6C` | `OPERAND_B_3` | R/W | 32 | Blade 3 ($e_3$) signed Q16.16 coefficient |
| `0x70` | `OPERAND_B_4` | R/W | 32 | Blade 4 ($e_{12}$) signed Q16.16 coefficient |
| `0x74` | `OPERAND_B_5` | R/W | 32 | Blade 5 ($e_{13}$) signed Q16.16 coefficient |
| `0x78` | `OPERAND_B_6` | R/W | 32 | Blade 6 ($e_{23}$) signed Q16.16 coefficient |
| `0x7C` | `OPERAND_B_7` | R/W | 32 | Blade 7 ($e_{123}$) signed Q16.16 coefficient |
| `0x80` | `RESULT_C_0` | RO | 32 | Result Blade 0 ($1$) signed Q16.16 coefficient |
| `0x84` | `RESULT_C_1` | RO | 32 | Result Blade 1 ($e_1$) signed Q16.16 coefficient |
| `0x88` | `RESULT_C_2` | RO | 32 | Result Blade 2 ($e_2$) signed Q16.16 coefficient |
| `0x8C` | `RESULT_C_3` | RO | 32 | Result Blade 3 ($e_3$) signed Q16.16 coefficient |
| `0x90` | `RESULT_C_4` | RO | 32 | Result Blade 4 ($e_{12}$) signed Q16.16 coefficient |
| `0x94` | `RESULT_C_5` | RO | 32 | Result Blade 5 ($e_{13}$) signed Q16.16 coefficient |
| `0x98` | `RESULT_C_6` | RO | 32 | Result Blade 6 ($e_{23}$) signed Q16.16 coefficient |
| `0x9C` | `RESULT_C_7` | RO | 32 | Result Blade 7 ($e_{123}$) signed Q16.16 coefficient |

---

## 5. Numerical Rules and Boundary Conditions

1. **Storage Format**: Signed 32-bit two's-complement integer with 16 integer bits and 16 fractional bits:
   $$\text{Real Value} = \frac{\text{Raw Integer}}{65536.0}$$
2. **Dynamic Range**:
   * Minimum: $-32768.0$ (`0x80000000`, $-2^{31}$)
   * Maximum: $+32767.99998474121$ (`0x7FFFFFFF`, $+2^{31} - 1$)
   * Precision: $2^{-16} \approx 1.5258789 \times 10^{-5}$
3. **Multiplication Rescaling**:
   * Two 32-bit Q16.16 operands produce a 64-bit Q32.32 product.
   * Rescaling back to Q16.16 requires division by $2^{16}$ (right shift by 16 bits).
   * Tie-breaking: **Round-to-Nearest-Even** (banker's rounding). If the 16 fractional bits being shifted off equal exactly `0x8000`, the result is rounded towards the nearest even integer.
4. **Saturation**:
   * Values exceeding `+2147483647` saturate strictly to `+2147483647` (`0x7FFFFFFF`).
   * Values falling below `-2147483648` saturate strictly to `-2147483648` (`0x80000000`).
   * Upon saturation, `status` bit 2 (`0x04`) is asserted.
