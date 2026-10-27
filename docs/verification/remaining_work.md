# Remaining Work in Dependency Order

1. **Stage 14: RTL Simulation and Hardware Implementation**:
   - Synthesize and implement the Stage 13 integrated block design (`qgpu_system_bd`) through Vivado place & route, timing closure at 100 MHz, and generate the final bitstream (`.bit`) and hardware handoff (`.xsa`).
   - *(Note: Deferred until explicitly requested per current execution directives).*

2. **Stage 15: On-Board Transaction Validation**:
   - Transfer bitstream, hardware handoff, and PYNQ overlay driver to target PYNQ-Z2 board.
   - Execute MMIO transactions against the 285 independent golden vectors for both `0x40000000` (sequential) and `0x40010000` (parallel) IP registers; capture hardware transaction logs.

3. **Stage 16: Hardware Benchmarking**:
   - Measure real hardware latency, clock cycle counts, throughput (MOPS / GOPS), and power consumption on the PYNQ-Z2.

4. **Stages 17-20: Advanced Extensions & Application Integration**:
   - Stage 17: Adaptive Memory Fabric (AAMF) ablations.
   - Stage 18: Live camera / gesture backend integration.
   - Stage 19: End-to-end classification latency and accuracy evaluation.
   - Stage 20: Hardware-backed production dashboard deployment.

5. **Stages 21-22: Final Reproducibility & Manuscript**:
   - Complete multi-stage automated reproduction script.
   - Compile paper / technical report with real hardware evidence tables.
