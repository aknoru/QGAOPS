"""
qgpu_overlay.py - PYNQ Overlay Driver for QGAOPS-QGPU Cl(3,0) Geometric Algebra Accelerator
Supports both Project A (Sequential) and Project B (Parallel) variants on PYNQ-Z2.

Primary numerical format: Signed Q16.16 fixed-point.
Algebra: Cl(3,0) Euclidean Geometric Algebra.
Canonical basis ordering: [1, e1, e2, e3, e12, e13, e23, e123]
"""

import os
import time
import numpy as np

# Canonical Register Offsets (AXI4-Lite Control Bus)
OFFSET_CTRL       = 0x00
OFFSET_GIER       = 0x04
OFFSET_IP_IER     = 0x08
OFFSET_IP_ISR     = 0x0C
OFFSET_A_BASE     = 0x10  # a_0..a_7 at 0x10, 0x18, 0x20, 0x28, 0x30, 0x38, 0x40, 0x48
OFFSET_B_BASE     = 0x50  # b_0..b_7 at 0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88
OFFSET_C_BASE     = 0x90  # c_0..c_7 at 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x100
OFFSET_OPCODE     = 0x110 # Opcode register (Bits 0..15: op, Bits 16..21: slot)
OFFSET_STATUS     = 0x118 # Status register (Bit 0: overflow, Bit 1: invalid op, Bit 2: div0)
OFFSET_DMA_LEN    = 0x128 # DMA streaming batch count (0 = direct register mode)

# Canonical Opcode Definitions
OPCODE_NOP             = 0x0000
OPCODE_GEOMETRIC       = 0x0001
OPCODE_WEDGE           = 0x0002
OPCODE_INNER           = 0x0003
OPCODE_ADD             = 0x0004
OPCODE_SUB             = 0x0005
OPCODE_SCALAR_MUL      = 0x0006
OPCODE_GRADE_PROJECT   = 0x0007
OPCODE_REVERSE         = 0x0008
OPCODE_GRADE_INVOLUTION= 0x0009
OPCODE_CLIFFORD_CONJ   = 0x000A
OPCODE_ROTOR_SANDWICH  = 0x000B
OPCODE_ROTOR_NORM      = 0x000C

Q16_SCALE = 65536.0


def float_to_q16(val: float) -> int:
    """Convert float to signed 32-bit Q16.16 fixed point with round-half-even and saturation."""
    scaled = round(val * Q16_SCALE)
    if scaled > 2147483647:
        scaled = 2147483647
    elif scaled < -2147483648:
        scaled = -2147483648
    return int(np.int32(scaled))


def q16_to_float(val: int) -> float:
    """Convert signed 32-bit Q16.16 integer to Python float."""
    raw = np.int32(val)
    return float(raw) / Q16_SCALE


class QGPUAccelerator:
    """
    PYNQ Driver for QGPU Hardware Accelerator.
    Works either with real PYNQ Overlay (on-board) or Mock MMIO (for off-board verification).
    """

    def __init__(self, bitstream_path=None, ip_name="qgpu_par_0"):
        self.ip = None
        self.is_mock = False

        if bitstream_path and os.path.exists(bitstream_path):
            try:
                from pynq import Overlay
                self.ol = Overlay(bitstream_path)
                self.ip = getattr(self.ol, ip_name)
                print(f"[QGPU] Successfully loaded overlay: {bitstream_path}")
            except ImportError:
                print("[QGPU] Warning: PYNQ library not found. Running in simulation/mock mode.")
                self.is_mock = True
        else:
            self.is_mock = True

        if self.is_mock:
            self._mock_regs = {}

    def _write_reg(self, offset: int, data: int):
        if self.is_mock:
            self._mock_regs[offset] = int(data) & 0xFFFFFFFF
        else:
            self.ip.write(offset, int(data) & 0xFFFFFFFF)

    def _read_reg(self, offset: int) -> int:
        if self.is_mock:
            return self._mock_regs.get(offset, 0)
        else:
            return self.ip.read(offset)

    def execute_op(self, a_mv, b_mv, opcode: int, slot: int = 0, timeout_ms: int = 100):
        """
        Execute an operation on 8-blade multivectors a_mv and b_mv.
        
        Args:
            a_mv: List/array of 8 floats or Q16 integers
            b_mv: List/array of 8 floats or Q16 integers
            opcode: Operation opcode (0x0001 - 0x000C)
            slot: AAMF on-chip BRAM memory buffer slot (0 - 63)
            timeout_ms: Maximum wait time for AP_DONE in milliseconds
            
        Returns:
            c_mv: List of 8 floats (result multivector)
            status: Status bitfield (Bit 0: overflow, Bit 1: invalid, Bit 2: div0)
        """
        # Pack inputs
        a_q16 = [float_to_q16(x) if isinstance(x, float) else int(x) for x in a_mv]
        b_q16 = [float_to_q16(x) if isinstance(x, float) else int(x) for x in b_mv]

        # Ensure direct register mode (dma_len = 0)
        self._write_reg(OFFSET_DMA_LEN, 0)

        # 1. Write operand A (8 blades)
        for i in range(8):
            self._write_reg(OFFSET_A_BASE + i * 8, a_q16[i])

        # 2. Write operand B (8 blades)
        for i in range(8):
            self._write_reg(OFFSET_B_BASE + i * 8, b_q16[i])

        # 3. Write opcode and AAMF slot
        full_opcode = (opcode & 0xFFFF) | ((slot & 0x3F) << 16)
        self._write_reg(OFFSET_OPCODE, full_opcode)

        # 4. Start execution: AP_START = 1 (Bit 0 of CTRL)
        self._write_reg(OFFSET_CTRL, 0x01)

        # 5. Poll for completion: AP_DONE = 1 (Bit 1 of CTRL)
        if not self.is_mock:
            t_start = time.time()
            done = False
            while (time.time() - t_start) * 1000.0 < timeout_ms:
                ctrl = self._read_reg(OFFSET_CTRL)
                if ctrl & 0x02:
                    done = True
                    break
            if not done:
                raise TimeoutError(f"[QGPU] Hardware accelerator timed out after {timeout_ms} ms!")
        else:
            # In mock mode, immediately set AP_DONE
            self._write_reg(OFFSET_CTRL, 0x02)

        # 6. Read back result C (8 blades)
        c_q16 = []
        for i in range(8):
            raw = self._read_reg(OFFSET_C_BASE + i * 16)
            c_q16.append(np.int32(raw))

        # 7. Read status register
        status = self._read_reg(OFFSET_STATUS)

        c_mv = [q16_to_float(x) for x in c_q16]
        return c_mv, status

    def execute_dma_stream(self, a_batch, b_batch, opcode: int):
        """
        High-throughput DMA batch processing.
        a_batch: (N, 8) float array or Q16 array
        b_batch: (N, 8) float array or Q16 array
        Returns: (N, 8) float array
        """
        N = len(a_batch)
        if self.is_mock:
            results = []
            for i in range(N):
                c, _ = self.execute_op(a_batch[i], b_batch[i], opcode)
                results.append(c)
            return results

        from pynq import allocate
        in_buf = allocate(shape=(N * 16,), dtype=np.int32)
        out_buf = allocate(shape=(N * 8,), dtype=np.int32)

        # Pack input buffer: interleaved [A_0..A_7, B_0..B_7] for each pair
        for i in range(N):
            a_q16 = [float_to_q16(x) if isinstance(x, float) else int(x) for x in a_batch[i]]
            b_q16 = [float_to_q16(x) if isinstance(x, float) else int(x) for x in b_batch[i]]
            for k in range(8):
                in_buf[i * 16 + k] = a_q16[k]
                in_buf[i * 16 + 8 + k] = b_q16[k]

        # Configure accelerator for DMA batch streaming mode
        self._write_reg(OFFSET_DMA_LEN, N)
        self._write_reg(OFFSET_OPCODE, opcode & 0xFFFF)
        self._write_reg(OFFSET_CTRL, 0x01)

        # Trigger DMA MM2S and S2MM transfers
        dma = self.ol.axi_dma_0
        dma.recvchannel.transfer(out_buf)
        dma.sendchannel.transfer(in_buf)
        dma.sendchannel.wait()
        dma.recvchannel.wait()

        # Unpack results
        res_batch = []
        for i in range(N):
            mv = [q16_to_float(out_buf[i * 8 + k]) for k in range(8)]
            res_batch.append(mv)
        return res_batch

    def geometric_product(self, a, b, slot=0):
        return self.execute_op(a, b, OPCODE_GEOMETRIC, slot)[0]

    def wedge_product(self, a, b, slot=0):
        return self.execute_op(a, b, OPCODE_WEDGE, slot)[0]

    def inner_product(self, a, b, slot=0):
        return self.execute_op(a, b, OPCODE_INNER, slot)[0]

    def add(self, a, b, slot=0):
        return self.execute_op(a, b, OPCODE_ADD, slot)[0]

    def sub(self, a, b, slot=0):
        return self.execute_op(a, b, OPCODE_SUB, slot)[0]

    def rotor_sandwich(self, r, v, slot=0):
        """Compute R * v * ~R (sandwich product)."""
        return self.execute_op(r, v, OPCODE_ROTOR_SANDWICH, slot)[0]
