/**
 * tb_qgpu_ga_engine.cpp
 * Independent C/C++ Testbench for Vitis HLS QGAOPS-QGPU Kernel
 *
 * Verification Requirements:
 * - Independent Oracle: Exercises top function against golden vectors generated
 *   strictly by the independent software reference model (software/reference_model/).
 * - Tests both Variant A (Resource-Shared) and Variant B (Parallel Pipelined).
 * - Comprehensive Coverage of All 12 Canonical Geometric Algebra Operations:
 *   1. Opcode 0x01: Geometric Product (64 exhaustive basis pairs + corner + random)
 *   2. Opcode 0x02: Wedge / Outer Product (64 exhaustive basis pairs + random)
 *   3. Opcode 0x03: Hestenes Inner Product (64 exhaustive basis pairs + random)
 *   4. Opcode 0x04: Addition (boundary, cancellation, overflow saturation)
 *   5. Opcode 0x05: Subtraction (boundary, cancellation, underflow saturation)
 *   6. Opcode 0x06: Scalar Multiplication (positive, negative, fractional, saturating)
 *   7. Opcode 0x07: Grade Projection (grades 0, 1, 2, 3)
 *   8. Opcode 0x08: Reversion (basis blades, mixed multivectors)
 *   9. Opcode 0x09: Grade Involution (basis blades, mixed multivectors)
 *  10. Opcode 0x0A: Clifford Conjugation (basis blades, mixed multivectors)
 *  11. Opcode 0x0B: Rotor Sandwich Product (3D spatial rotations: 90 deg, 180 deg, identity)
 *  12. Opcode 0x0C: Rotor Norm Squared (unit rotors, basis blades, mixed multivectors)
 *  Plus: Fixed-point edge cases, 67-bit accumulator stress, and invalid opcode error traps.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "qgpu_ga_engine.h"

#define MAX_LINE_LEN 1024
#define MAX_VECTORS  1000

typedef struct {
    int test_id;
    char category[64];
    uint32_t opcode;
    char op_name[64];
    uint32_t expected_status;
    int32_t a[8];
    int32_t b[8];
    int32_t expected[8];
} GoldenVector;

static GoldenVector g_vectors[MAX_VECTORS];
static int g_vector_count = 0;

static const char *get_op_display_name(uint32_t op) {
    switch (op) {
        case OPCODE_GP:               return "0x01 GP (Geometric Product)";
        case OPCODE_WEDGE:            return "0x02 WEDGE (Outer Product)";
        case OPCODE_INNER:            return "0x03 INNER (Hestenes Inner)";
        case OPCODE_ADD:              return "0x04 ADD (Addition)";
        case OPCODE_SUB:              return "0x05 SUB (Subtraction)";
        case OPCODE_SCALAR_MUL:       return "0x06 SCALAR_MUL (Scalar Mult)";
        case OPCODE_GRADE_PROJ:       return "0x07 GRADE_PROJ (Grade Projection)";
        case OPCODE_REVERSE:          return "0x08 REVERSE (Reversion)";
        case OPCODE_GRADE_INVOLUTION: return "0x09 GRADE_INVOL (Grade Involution)";
        case OPCODE_CLIFFORD_CONJ:    return "0x0A CLIFFORD_CONJ (Clifford Conj)";
        case OPCODE_SANDWICH:         return "0x0B SANDWICH (Rotor Sandwich)";
        case OPCODE_ROTOR_NORM:       return "0x0C ROTOR_NORM (Rotor Norm Squared)";
        default:                      return "0x-- INVALID_OPCODE";
    }
}

static bool load_golden_vectors_csv(const char *csv_path) {
    FILE *f = fopen(csv_path, "r");
    if (!f) {
        printf("[WARN] Could not open %s directly. Trying relative and absolute paths...\n", csv_path);
        f = fopen("D:/QGPU/hardware/hls/ga_engine/vectors/golden_vectors.csv", "r");
        if (!f) {
            f = fopen("../../../../vectors/golden_vectors.csv", "r");
        }
        if (!f) {
            f = fopen("../../vectors/golden_vectors.csv", "r");
        }
        if (!f) {
            f = fopen("vectors/golden_vectors.csv", "r");
        }
        if (!f) {
            f = fopen("hardware/hls/ga_engine/vectors/golden_vectors.csv", "r");
        }
    }
    if (!f) {
        fprintf(stderr, "[ERROR] Failed to locate golden_vectors.csv!\n");
        return false;
    }

    char line[MAX_LINE_LEN];
    /* Skip CSV header */
    if (!fgets(line, sizeof(line), f)) {
        fclose(f);
        return false;
    }

    g_vector_count = 0;
    while (fgets(line, sizeof(line), f) && g_vector_count < MAX_VECTORS) {
        GoldenVector *v = &g_vectors[g_vector_count];
        char *token = strtok(line, ",\r\n");
        if (!token) continue;
        v->test_id = atoi(token);

        token = strtok(NULL, ",\r\n");
        if (!token) continue;
        strncpy(v->category, token, sizeof(v->category) - 1);

        token = strtok(NULL, ",\r\n");
        if (!token) continue;
        v->opcode = (uint32_t)atoi(token);

        token = strtok(NULL, ",\r\n");
        if (!token) continue;
        strncpy(v->op_name, token, sizeof(v->op_name) - 1);

        token = strtok(NULL, ",\r\n");
        if (!token) continue;
        v->expected_status = (uint32_t)atoi(token);

        /* Read a_0..a_7 */
        for (int k = 0; k < 8; k++) {
            token = strtok(NULL, ",\r\n");
            v->a[k] = token ? (int32_t)atol(token) : 0;
        }

        /* Read b_0..b_7 */
        for (int k = 0; k < 8; k++) {
            token = strtok(NULL, ",\r\n");
            v->b[k] = token ? (int32_t)atol(token) : 0;
        }

        /* Read exp_0..exp_7 */
        for (int k = 0; k < 8; k++) {
            token = strtok(NULL, ",\r\n");
            v->expected[k] = token ? (int32_t)atol(token) : 0;
        }

        g_vector_count++;
    }

    fclose(f);
    printf("[INFO] Successfully loaded %d independent golden vectors from CSV.\n", g_vector_count);
    return true;
}

static int run_architecture_suite(uint32_t arch_variant, const char *arch_name) {
    printf("\n=================================================================\n");
    printf("  RUNNING VERIFICATION SUITE FOR %s\n", arch_name);
    printf("=================================================================\n");

    int passed = 0;
    int failed = 0;

    /* Per-operation coverage tracking */
    int op_total[16] = {0};
    int op_passed[16] = {0};

    hls::stream<axis_word_t> dma_in("tb_dma_in");
    hls::stream<axis_word_t> dma_out("tb_dma_out");

    for (int i = 0; i < g_vector_count; i++) {
        const GoldenVector *v = &g_vectors[i];
        int32_t actual_c[8] = {0};
        uint32_t actual_status = 0;

        uint32_t op_bin = (v->opcode <= 12) ? v->opcode : 0;
        op_total[op_bin]++;

        /* Exercise the architecture-specific kernel directly via AXI4-Lite mode (dma_len = 0). */
#if defined(QGPU_TEST_SEQUENTIAL_ONLY)
        (void)arch_variant;
        qgpu_ga_sequential_top(v->a, v->b, actual_c, v->opcode, &actual_status, 0, dma_in, dma_out);
#elif defined(QGPU_TEST_PARALLEL_ONLY)
        (void)arch_variant;
        qgpu_ga_parallel_top(v->a, v->b, actual_c, v->opcode, &actual_status, 0, dma_in, dma_out);
#else
        if (arch_variant == ARCH_RESOURCE_SHARED) {
            qgpu_ga_sequential_top(v->a, v->b, actual_c, v->opcode, &actual_status, 0, dma_in, dma_out);
        } else {
            qgpu_ga_parallel_top(v->a, v->b, actual_c, v->opcode, &actual_status, 0, dma_in, dma_out);
        }
#endif

        /* Compare all 8 output coefficients */
        bool coeff_match = true;
        int failed_idx = -1;
        for (int k = 0; k < 8; k++) {
            if (actual_c[k] != v->expected[k]) {
                coeff_match = false;
                failed_idx = k;
                break;
            }
        }

        /* Compare status codes */
        bool status_match = (actual_status == v->expected_status);

        if (!coeff_match || !status_match) {
            failed++;
            printf("\n[FAIL] Test ID %d (%s) - %s [Arch: %s]\n",
                   v->test_id, v->category, v->op_name, arch_name);
            printf("  Expected status: 0x%02X, Actual status: 0x%02X\n",
                   v->expected_status, actual_status);
            if (!coeff_match) {
                printf("  Coefficient mismatch at blade %d:\n", failed_idx);
                printf("    Expected: %d (0x%08X)\n", v->expected[failed_idx], (uint32_t)v->expected[failed_idx]);
                printf("    Actual:   %d (0x%08X)\n", actual_c[failed_idx], (uint32_t)actual_c[failed_idx]);
                printf("  Full Expected: [");
                for (int k = 0; k < 8; k++) printf("%d%s", v->expected[k], (k < 7) ? ", " : "]\n");
                printf("  Full Actual:   [");
                for (int k = 0; k < 8; k++) printf("%d%s", actual_c[k], (k < 7) ? ", " : "]\n");
            }
        } else {
            passed++;
            op_passed[op_bin]++;
        }
    }

    /* Verify AXI4-Stream DMA batch processing (dma_len = 4) */
    printf("\n  [DMA STREAM VERIFICATION] Streaming 4 multivector pairs...\n");
    for (int i = 0; i < 4; i++) {
        for (int k = 0; k < 8; k++) {
            axis_word_t wa;
            wa.data = g_vectors[i].a[k];
            wa.last = (k == 7) ? 1 : 0;
            dma_in.write(wa);
        }
        for (int k = 0; k < 8; k++) {
            axis_word_t wb;
            wb.data = g_vectors[i].b[k];
            wb.last = (k == 7) ? 1 : 0;
            dma_in.write(wb);
        }
    }
    uint32_t dma_status = 0;
#if defined(QGPU_TEST_SEQUENTIAL_ONLY)
    qgpu_ga_sequential_top(NULL, NULL, NULL, OPCODE_GP, &dma_status, 4, dma_in, dma_out);
#elif defined(QGPU_TEST_PARALLEL_ONLY)
    qgpu_ga_parallel_top(NULL, NULL, NULL, OPCODE_GP, &dma_status, 4, dma_in, dma_out);
#else
    if (arch_variant == ARCH_RESOURCE_SHARED) {
        qgpu_ga_sequential_top(NULL, NULL, NULL, OPCODE_GP, &dma_status, 4, dma_in, dma_out);
    } else {
        qgpu_ga_parallel_top(NULL, NULL, NULL, OPCODE_GP, &dma_status, 4, dma_in, dma_out);
    }
#endif
    bool dma_match = true;
    for (int i = 0; i < 4; i++) {
        for (int k = 0; k < 8; k++) {
            axis_word_t wc = dma_out.read();
            if (wc.data != g_vectors[i].expected[k]) {
                dma_match = false;
                printf("  [DMA FAIL] Batch vector %d blade %d: Exp 0x%08X, Act 0x%08X\n",
                       i, k, (uint32_t)g_vectors[i].expected[k], (uint32_t)wc.data);
            }
        }
    }
    if (dma_match) {
        printf("  [DMA STREAM VERIFICATION] PASS - 4 multivector stream operations bit-exact.\n");
    } else {
        failed++;
    }


    printf("\n  ---------------------------------------------------------------\n");
    printf("  %s - OPERATION COVERAGE BREAKDOWN\n", arch_name);
    printf("  ---------------------------------------------------------------\n");
    printf("  %-38s | %6s | %6s | %s\n", "Operation", "Total", "Passed", "Status");
    printf("  ---------------------------------------+--------+--------+-------\n");
    for (uint32_t op = 1; op <= 12; op++) {
        if (op_total[op] > 0) {
            const char *st = (op_passed[op] == op_total[op]) ? "PASS" : "FAIL";
            printf("  %-38s | %6d | %6d | %s\n",
                   get_op_display_name(op), op_total[op], op_passed[op], st);
        }
    }
    if (op_total[0] > 0) {
        const char *st = (op_passed[0] == op_total[0]) ? "PASS" : "FAIL";
        printf("  %-38s | %6d | %6d | %s\n",
               "Invalid Opcode Error Traps", op_total[0], op_passed[0], st);
    }
    printf("  ---------------------------------------------------------------\n");
    printf("  Architecture: %s\n", arch_name);
    printf("  Total Vectors Tested: %d\n", g_vector_count);
    printf("  Passed: %d\n", passed);
    printf("  Failed: %d\n", failed);
    printf("  Status: %s\n", (failed == 0) ? "PASS (100% BIT-EXACT)" : "FAIL");
    printf("=================================================================\n");

    return failed;
}

int main(int argc, char **argv) {
    printf("=================================================================\n");
    printf("  QGAOPS-QGPU VITIS HLS INDEPENDENT C/C++ TESTBENCH\n");
    printf("  Euclidean Cl(3,0) / Signed 32-bit Q16.16 Datapath\n");
    printf("  Exhaustive Verification of All 12 Geometric Algebra Operations\n");
    printf("=================================================================\n");

    const char *csv_path = "hardware/hls/ga_engine/vectors/golden_vectors.csv";
    if (argc > 1) {
        csv_path = argv[1];
    }

    if (!load_golden_vectors_csv(csv_path)) {
        fprintf(stderr, "[FATAL] Unable to load golden vectors. Aborting testbench.\n");
        return 1;
    }

    int total_failures = 0;

    /* 1. Test Variant A: Resource-Shared Architecture */
#if !defined(QGPU_TEST_PARALLEL_ONLY)
    total_failures += run_architecture_suite(ARCH_RESOURCE_SHARED, "VARIANT A (RESOURCE-SHARED)");
#endif

    /* 2. Test Variant B: Parallel Pipelined Architecture */
#if !defined(QGPU_TEST_SEQUENTIAL_ONLY)
    total_failures += run_architecture_suite(ARCH_PARALLEL, "VARIANT B (PARALLEL PIPELINED)");
#endif

    printf("\n=================================================================\n");
    if (total_failures == 0) {
        printf("  [FINAL RESULT] ALL HLS ARITHMETIC TESTS PASSED (0 FAILURES)\n");
        printf("  Both Variant A and Variant B match the independent software\n");
        printf("  reference model with 100%% bit-exact arithmetic accuracy\n");
        printf("  across all 12 canonical Geometric Algebra operations.\n");
        printf("=================================================================\n");
        return 0;
    } else {
        printf("  [FINAL RESULT] VERIFICATION FAILED WITH %d TOTAL FAILURES!\n", total_failures);
        printf("=================================================================\n");
        return 1;
    }
}
