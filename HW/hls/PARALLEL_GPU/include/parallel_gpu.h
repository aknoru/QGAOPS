#ifndef PARALLEL_GPU_H
#define PARALLEL_GPU_H

#include <stdint.h>
#include <stdbool.h>
#include "../../common/include/qgpu_types.h"
#include "../../common/include/qgpu_operations.h"
#include "../../common/include/qgpu_fixed_point.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * PARALLEL_GPU Top-Level Synthesizable HLS Entry Point
 *
 * Parallel, pipelined geometric algebra accelerator optimizing execution
 * latency and initiation interval via unrolled blade trees and array partitioning.
 *
 * @param a       Input multivector A (8 signed 32-bit Q16.16 coefficients)
 * @param b       Input multivector B (8 signed 32-bit Q16.16 coefficients or scalar/grade)
 * @param c       Output multivector C (8 signed 32-bit Q16.16 coefficients)
 * @param opcode  Operation selector (OPCODE_GP .. OPCODE_ROTOR_NORM)
 * @param status  Output execution status register (STATUS_OK, STATUS_ERR_OP, STATUS_OVERFLOW)
 */
void parallel_gpu(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status
);

#ifdef __cplusplus
}
#endif

#endif /* PARALLEL_GPU_H */
