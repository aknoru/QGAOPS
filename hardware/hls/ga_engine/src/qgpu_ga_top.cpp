/**
 * qgpu_ga_top.cpp
 * Top-Level Synthesizable Vitis HLS Entry Point for QGAOPS-QGPU
 *
 * Interface Directives:
 * - AXI4-Lite slave interface (`s_axilite bundle=control`) for registers, operands, and results.
 * - Supports selectable execution between Variant A (Resource-Shared) and Variant B (Parallel).
 */

#include "qgpu_ga_engine.h"

void qgpu_ga_engine(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status,
    uint32_t arch_variant
) {
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    #pragma HLS INTERFACE s_axilite port=a bundle=control
    #pragma HLS INTERFACE s_axilite port=b bundle=control
    #pragma HLS INTERFACE s_axilite port=c bundle=control
    #pragma HLS INTERFACE s_axilite port=opcode bundle=control
    #pragma HLS INTERFACE s_axilite port=status bundle=control
    #pragma HLS INTERFACE s_axilite port=arch_variant bundle=control

    if (arch_variant == ARCH_PARALLEL) {
        qgpu_ga_engine_parallel(a, b, c, opcode, status);
    } else {
        qgpu_ga_engine_shared(a, b, c, opcode, status);
    }
}
