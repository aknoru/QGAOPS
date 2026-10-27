# Hardware Interface Closure Report: QGAOPS-QGPU

## 1. Overview
This report documents the verification and closure of the software/hardware interface contract for both Project A (Sequential) and Project B (Parallel) variants on the PYNQ-Z2 (Zynq-7000 XC7Z020).

---

## 2. Memory Map & Address Editor Alignment
Both accelerators are mapped to the Zynq Processing System via `M_AXI_GP0` through the AXI Interconnect:

| IP Instance | Block Design Path | Base Address | High Address | Range | Interface Bus |
|---|---|---|---|---|---|
| **Parallel Accelerator** | `/qgpu_par_0/s_axi_control` | `0x4000_0000` | `0x4000_FFFF` | 64 KB | AXI4-Lite |
| **Sequential Accelerator**| `/qgpu_seq_0/s_axi_control` | `0x4001_0000` | `0x4001_FFFF` | 64 KB | AXI4-Lite |
| **AXI DMA** | `/axi_dma_0/S_AXI_LITE` | `0x4040_0000` | `0x4040_FFFF` | 64 KB | AXI4-Lite |
| **AXI VDMA (HDMI)** | `/axi_vdma_0/S_AXI_LITE` | `0x4300_0000` | `0x4300_FFFF` | 64 KB | AXI4-Lite |
| **Video Timing Controller**| `/v_tc_0/ctrl` | `0x43C0_0000` | `0x43C0_FFFF` | 64 KB | AXI4-Lite |

---

## 3. Register Map Closure
Reconciliation between `qgpu_ga_engine.h`, HLS RTL export, and PYNQ Python Driver (`qgpu_overlay.py`):

| Offset | Register Name | Width | Access | Functional Description | Driver Mapping |
|---|---|---|---|---|---|
| `0x00` | `CTRL` | 32 | RW | Bit 0: AP_START, Bit 1: AP_DONE, Bit 2: AP_IDLE, Bit 3: AP_READY | `OFFSET_CTRL` |
| `0x04` | `GIER` | 32 | RW | Global Interrupt Enable (Bit 0) | `OFFSET_GIER` |
| `0x08` | `IP_IER` | 32 | RW | Channel Interrupt Enable | `OFFSET_IP_IER` |
| `0x0C` | `IP_ISR` | 32 | RW | Channel Interrupt Status | `OFFSET_IP_ISR` |
| `0x10 + i*8` | `a_i` ($i=0..7$) | 32 | W | Input multivector operand A blade $i$ (Q16.16) | `OFFSET_A_BASE` |
| `0x50 + i*8` | `b_i` ($i=0..7$) | 32 | W | Input multivector operand B blade $i$ (Q16.16) | `OFFSET_B_BASE` |
| `0x90 + i*16`| `c_i` ($i=0..7$) | 32 | R | Output multivector result C blade $i$ (Q16.16) | `OFFSET_C_BASE` |
| `0x110` | `opcode` | 32 | W | Bits 0..15: Opcode (0x01..0x0C); Bits 16..21: AAMF Buffer Slot | `OFFSET_OPCODE` |
| `0x118` | `status` | 32 | R | Bit 0: Overflow; Bit 1: Invalid Opcode; Bit 2: Division by Zero | `OFFSET_STATUS` |

---

## 4. IP Component XML Validation
Inspecting `component.xml` for both variants:
- **Parallel IP**:
  - VLNV: `qgpu:hls:qgpu_ga_parallel_ip:1.0`
  - Bus Interface: `s_axi_control` (Slave, AXI4-Lite)
  - Memory Map: `s_axi_control`, address range 512 bytes (`0x200`)
- **Sequential IP**:
  - VLNV: `qgpu:hls:qgpu_ga_sequential_top:1.0`
  - Bus Interface: `s_axi_control` (Slave, AXI4-Lite)
  - Memory Map: `s_axi_control`, address range 512 bytes (`0x200`)

---

## 5. Verification Conclusion
The C/C++ interface, HLS pragmas, synthesized HDL ports, Vivado block designs, and PYNQ driver agree 100% with zero register map or bitfield discrepancies.
