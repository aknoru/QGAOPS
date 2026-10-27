# Hardware/Software Interface Specification

## 1. Scope & Execution Boundary
This document specifies the software transaction protocol and its mapping to the Vitis HLS IP top-level function for Stage 9–10.

- **Software Boundary**: Host PS (ARM Cortex-A9 or CPU test harness) serializing transactions into contiguous memory buffers.
- **Hardware Boundary**: AXI4-Lite control interface (`s_axilite`) and AXI DMA stream/memory interfaces on the PL fabric.
- **Precision**: Signed 32-bit Q16.16 (`ap_fixed<32,16>`), little-endian, two's complement.

---

## 2. Host-to-IP Transaction Format (76-Byte Request)

To guarantee 64-bit alignment for high-performance AXI DMA burst transfers, the request packet uses a **12-byte header** followed by **64 bytes of multivector payload** (total 76 bytes):

### Request Header (12 Bytes)
| Byte Offset | Field Name | Data Type | Value / Description |
| :--- | :--- | :--- | :--- |
| `0x00` | `version` | `uint8` | Protocol version (`0x01`) |
| `0x01` | `operation_id` | `uint8` | Opcode: 1=GP, 2=WEDGE, 3=INNER, 4=ADD, 5=SUB |
| `0x02` | `flags` | `uint8` | Control flags (bit 0: clear sticky overflow) |
| `0x03` | `reserved1` | `uint8` | Alignment padding (`0x00`) |
| `0x04 - 0x07` | `batch_length` | `uint32_le` | Number of multivector pairs (scalar mode = `1`) |
| `0x08 - 0x0B` | `reserved2` | `uint32_le` | 4-byte padding aligning operand array to 8-byte boundary |

### Request Payload (64 Bytes)
| Byte Offset | Field Name | Data Type | Representation |
| :--- | :--- | :--- | :--- |
| `0x0C - 0x2B` | `operand_A[8]` | `int32_le[8]` | 8 $\times$ Q16.16 coefficients: `[1, e1, e2, e3, e12, e13, e23, e123]` |
| `0x2C - 0x4B` | `operand_B[8]` | `int32_le[8]` | 8 $\times$ Q16.16 coefficients: `[1, e1, e2, e3, e12, e13, e23, e123]` |

---

## 3. IP-to-Host Response Format (44-Byte Response)

### Response Header (12 Bytes)
| Byte Offset | Field Name | Data Type | Value / Description |
| :--- | :--- | :--- | :--- |
| `0x00` | `version` | `uint8` | Protocol version (`0x01`) |
| `0x01` | `status_code` | `uint8` | 0=OK, 1=INVALID_OP, 2=INVALID_LEN, 3=VERSION_MISMATCH, 4=OVERFLOW |
| `0x02` | `flags` | `uint8` | Status flags (bit 0: overflow occurred during calculation) |
| `0x03` | `reserved` | `uint8` | Padding (`0x00`) |
| `0x04 - 0x07` | `batch_length` | `uint32_le` | Number of results returned |
| `0x08 - 0x0B` | `cycle_count` | `uint32_le` | Hardware execution latency in clock cycles |

### Response Payload (32 Bytes)
| Byte Offset | Field Name | Data Type | Representation |
| :--- | :--- | :--- | :--- |
| `0x0C - 0x2B` | `result_C[8]` | `int32_le[8]` | 8 $\times$ Q16.16 coefficients: `[1, e1, e2, e3, e12, e13, e23, e123]` |

---

## 4. Mapping to Vitis HLS Top-Level C/C++ Signature

In Vitis HLS, the memory transaction packet maps to the hardware registers and ports via `#pragma HLS INTERFACE`:

```cpp
void qgpu_ga_engine(
    const int32_t a[8],       // s_axilite / m_axi offset 0x20..0x3C
    const int32_t b[8],       // s_axilite / m_axi offset 0x40..0x5C
    int32_t c[8],             // s_axilite / m_axi offset 0x60..0x7C
    uint32_t opcode,          // s_axilite offset 0x10
    uint32_t *status,         // s_axilite offset 0x18
    uint32_t architecture    // 0 = Resource-Shared (Variant A), 1 = Parallel (Variant B)
);
```

### AXI4-Lite Register Map (`s_axilite` bundle `control`)
- `0x00`: Control Signals (`AP_START`, `AP_DONE`, `AP_IDLE`, `AP_READY`)
- `0x04`: Global Interrupt Enable (`GIE`)
- `0x08`: IP Interrupt Enable Register (`IER`)
- `0x0C`: IP Interrupt Status Register (`ISR`)
- `0x10`: `opcode` (1=GP, 2=WEDGE, 3=INNER, 4=ADD, 5=SUB)
- `0x18`: `status` (Read-only: bit 0 = overflow sticky flag, bit 1 = invalid opcode)
- `0x20 - 0x3C`: Multivector A coefficients (8 words)
- `0x40 - 0x5C`: Multivector B coefficients (8 words)
- `0x60 - 0x7C`: Multivector C result coefficients (8 words)
