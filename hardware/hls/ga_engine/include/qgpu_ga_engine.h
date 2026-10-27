#ifndef QGPU_GA_ENGINE_H
#define QGPU_GA_ENGINE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =========================================================================
 * OPERATION IDENTIFIERS
 * ========================================================================= */
#define OPCODE_NOP               0x00
#define OPCODE_GP                0x01  /* Geometric Product: C = A * B */
#define OPCODE_WEDGE             0x02  /* Outer / Wedge Product: C = A ^ B */
#define OPCODE_INNER             0x03  /* Hestenes Inner Product: C = A . B */
#define OPCODE_ADD               0x04  /* Multivector Addition: C = A + B */
#define OPCODE_SUB               0x05  /* Multivector Subtraction: C = A - B */
#define OPCODE_SCALAR_MUL        0x06  /* Scalar Multiplication: C = B[0] * A */
#define OPCODE_GRADE_PROJ        0x07  /* Grade Projection: C = <A>_k, where k = B[0] */
#define OPCODE_REVERSE           0x08  /* Reversion: C = ~A */
#define OPCODE_GRADE_INVOLUTION  0x09  /* Grade Involution: C = ^A */
#define OPCODE_CLIFFORD_CONJ     0x0A  /* Clifford Conjugation: C = ~^A */
#define OPCODE_SANDWICH          0x0B  /* Rotor Sandwich: C = A * B * ~A */
#define OPCODE_ROTOR_NORM        0x0C  /* Rotor Norm Squared: C[0] = <A * ~A>_0 */

/* =========================================================================
 * STATUS AND ERROR CODES
 * ========================================================================= */
#define STATUS_OK         0x00
#define STATUS_ERR_OP     0x01  /* Unsupported / invalid operation */
#define STATUS_ERR_LEN    0x02  /* Invalid batch length */
#define STATUS_OVERFLOW   0x04  /* Sticky saturation / overflow occurred */

/* =========================================================================
 * ARCHITECTURAL VARIANTS
 * ========================================================================= */
#define ARCH_RESOURCE_SHARED  0  /* Variant A: Time-multiplexed shared accumulator */
#define ARCH_PARALLEL         1  /* Variant B: Pipelined parallel adder-tree */

/* Number of basis blades in Euclidean Cl(3,0) */
#define GA_BLADES         8

/* Fixed-point Q16.16 bounds */
#define Q16_SCALE         65536LL
#define Q16_MAX           2147483647LL
#define Q16_MIN           (-2147483648LL)

/* =========================================================================
 * ALGEBRA-AWARE MEMORY FABRIC (AAMF) SPECIFICATION
 * On-chip Block RAM (BRAM18K) multivector operand and result storage.
 * Capacity: 64 multivectors (512 words of 32-bit Q16.16 = 16,384 bits = 1x BRAM18K per bank).
 * ========================================================================= */
#define AAMF_BUFFER_MV_COUNT   64
#define AAMF_BUFFER_WORDS      (AAMF_BUFFER_MV_COUNT * GA_BLADES)

/* =========================================================================
 * FUNCTION DECLARATIONS
 * ========================================================================= */

/**
 * Top-level synthesizable Vitis HLS entry point.
 *
 * @param a             Input multivector A (8 signed 32-bit Q16.16 words)
 * @param b             Input multivector B (8 signed 32-bit Q16.16 words)
 * @param c             Output multivector C (8 signed 32-bit Q16.16 words)
 * @param opcode        Operation code (1=GP, 2=WEDGE, 3=INNER, 4=ADD, 5=SUB)
 * @param status        Status register output (bit 0: overflow, bit 1: invalid op)
 * @param arch_variant  0 = Resource-Shared (Variant A), 1 = Parallel (Variant B)
 */
void qgpu_ga_engine(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status,
    uint32_t arch_variant
);

/* Variant A: Resource-Shared arithmetic kernel */
void qgpu_ga_engine_shared(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status
);

/* Variant B: Parallel pipelined arithmetic kernel */
void qgpu_ga_engine_parallel(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status
);

#ifdef __cplusplus
}

#if defined(__SYNTHESIS__) || defined(USE_XILINX_HLS) || defined(__VITIS_HLS__) || defined(HLS_STREAM_THREAD_SAFE) || defined(XILINX_HLS) || (defined(__has_include) && __has_include(<hls_stream.h>))
#include "ap_axi_sdata.h"
#include "hls_stream.h"
typedef ap_axiu<32, 0, 0, 0> axis_word_t;
#else
struct axis_word_t {
    int32_t data;
    uint8_t keep;
    uint8_t strb;
    uint8_t user;
    uint8_t last;
    uint8_t id;
    uint8_t dest;
};
namespace hls {
    template<typename T>
    class stream {
    public:
        T read() { return T(); }
        void write(const T &val) { (void)val; }
        bool empty() const { return true; }
        bool full() const { return false; }
    };
}
#endif

/* Distinct IP top functions with AXI4-Lite control and AXI4-Stream DMA ports */
void qgpu_ga_sequential_top(
    const int32_t a[GA_BLADES], const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES], uint32_t opcode, uint32_t *status,
    uint32_t dma_len,
    hls::stream<axis_word_t> &dma_in,
    hls::stream<axis_word_t> &dma_out);

void qgpu_ga_parallel_top(
    const int32_t a[GA_BLADES], const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES], uint32_t opcode, uint32_t *status,
    uint32_t dma_len,
    hls::stream<axis_word_t> &dma_in,
    hls::stream<axis_word_t> &dma_out);

#else
/* C-linkage prototypes without C++ stream templates */
void qgpu_ga_sequential_top(
    const int32_t a[GA_BLADES], const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES], uint32_t opcode, uint32_t *status,
    uint32_t dma_len);
void qgpu_ga_parallel_top(
    const int32_t a[GA_BLADES], const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES], uint32_t opcode, uint32_t *status,
    uint32_t dma_len);
#endif

#endif /* QGPU_GA_ENGINE_H */

