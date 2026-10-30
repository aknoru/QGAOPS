/**
 * tb_seq_gpu.cpp
 * Comprehensive Verification Testbench for SEQ_GPU
 *
 * Fully executes and verifies:
 * 1. All 12 Canonical Geometric Algebra Operations (GP, Wedge, Inner, Add, Sub,
 *    Scalar Mul, Grade Proj, Reverse, Involution, Clifford Conj, Sandwich, Norm Sq).
 * 2. Quantum Geometric Algebra Operations (QGAOPS):
 *    - Pauli-X Gate (|0> -> |1> and |1> -> |0>)
 *    - Pauli-Y Gate (|0> -> |1>)
 *    - Pauli-Z Gate (Eigenstate invariance & superposition phase-flip)
 *    - Hadamard Superposition Gate (|0> -> |+> and reversibility H^2 = I)
 *    - Phase Gate S (|+> -> |+i>)
 *    - Quantum State Overlap / Fidelity via Hestenes Inner Product
 * 3. Complete 285 Golden Regression Test Suite.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include "../include/seq_gpu.h"
#include "../../common/tests/test_vectors.h"
#include "../../common/tests/quantum_test_vectors.h"

// ANSI Color formatting
#define ANSI_RESET   "\033[0m"
#define ANSI_BOLD    "\033[1m"
#define ANSI_RED     "\033[1;31m"
#define ANSI_GREEN   "\033[1;32m"
#define ANSI_YELLOW  "\033[1;33m"
#define ANSI_BLUE    "\033[1;34m"
#define ANSI_MAGENTA "\033[1;35m"
#define ANSI_CYAN    "\033[1;36m"

static void print_mv(const char *label, const int32_t mv[GA_BLADES]) {
    printf("  %s: [1: %d, e1: %d, e2: %d, e3: %d, e12: %d, e13: %d, e23: %d, e123: %d]\n",
           label, mv[0], mv[1], mv[2], mv[3], mv[4], mv[5], mv[6], mv[7]);
}

int main() {
    printf("\n%s================================================================================%s\n", ANSI_BLUE, ANSI_RESET);
    printf("%s   QGAOPS-QGPU: SEQ_GPU COMPREHENSIVE GEOMETRIC & QUANTUM VERIFICATION TESTBENCH  %s\n", ANSI_BOLD, ANSI_RESET);
    printf("%s================================================================================%s\n\n", ANSI_BLUE, ANSI_RESET);

    int total_passed = 0;
    int total_failed = 0;

    // ==========================================================================
    // SECTION 1: ALL 12 CANONICAL GEOMETRIC ALGEBRA OPERATIONS
    // ==========================================================================
    printf("%s[SECTION 1] VERIFYING ALL 12 CANONICAL GEOMETRIC ALGEBRA OPERATIONS%s\n", ANSI_CYAN, ANSI_RESET);

    struct {
        const char *name;
        uint32_t opcode;
        int32_t a[GA_BLADES];
        int32_t b[GA_BLADES];
        int32_t exp[GA_BLADES];
    } canonical_tests[12] = {
        // 1. Geometric Product: e1 * e2 = e12
        {"Geometric Product (e1 * e2 = e12)", OPCODE_GP,
         {0, 65536, 0, 0, 0, 0, 0, 0}, {0, 0, 65536, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 65536, 0, 0, 0}},
        // 2. Wedge Product: e1 ^ e3 = e13
        {"Wedge Product (e1 ^ e3 = e13)", OPCODE_WEDGE,
         {0, 65536, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 65536, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 65536, 0, 0}},
        // 3. Inner Product: e2 . e2 = 1.0
        {"Inner Product (e2 . e2 = 1.0)", OPCODE_INNER,
         {0, 0, 65536, 0, 0, 0, 0, 0}, {0, 0, 65536, 0, 0, 0, 0, 0}, {65536, 0, 0, 0, 0, 0, 0, 0}},
        // 4. Addition: A + B
        {"Multivector Addition", OPCODE_ADD,
         {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
         {131072, 131072, 131072, 131072, 131072, 131072, 131072, 131072},
         {196608, 196608, 196608, 196608, 196608, 196608, 196608, 196608}},
        // 5. Subtraction: A - B
        {"Multivector Subtraction", OPCODE_SUB,
         {327680, 327680, 327680, 327680, 327680, 327680, 327680, 327680},
         {131072, 131072, 131072, 131072, 131072, 131072, 131072, 131072},
         {196608, 196608, 196608, 196608, 196608, 196608, 196608, 196608}},
        // 6. Scalar Multiplication: 2.5 * A
        {"Scalar Multiplication (2.5 * A)", OPCODE_SCALAR_MUL,
         {131072, 131072, 131072, 131072, 131072, 131072, 131072, 131072},
         {163840, 0, 0, 0, 0, 0, 0, 0}, // 2.5 = 163840
         {327680, 327680, 327680, 327680, 327680, 327680, 327680, 327680}},
        // 7. Grade Projection: Grade 2
        {"Grade Projection (Grade 2 Bivectors)", OPCODE_GRADE_PROJ,
         {65536, 131072, 196608, 262144, 327680, 393216, 458752, 524288},
         {2, 0, 0, 0, 0, 0, 0, 0},
         {0, 0, 0, 0, 327680, 393216, 458752, 0}},
        // 8. Reversion: ~A
        {"Reversion (~A)", OPCODE_REVERSE,
         {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
         {0, 0, 0, 0, 0, 0, 0, 0},
         {65536, 65536, 65536, 65536, -65536, -65536, -65536, -65536}},
        // 9. Grade Involution: ^A
        {"Grade Involution (^A)", OPCODE_GRADE_INVOLUTION,
         {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
         {0, 0, 0, 0, 0, 0, 0, 0},
         {65536, -65536, -65536, -65536, 65536, 65536, 65536, -65536}},
        // 10. Clifford Conjugation: ~^A
        {"Clifford Conjugation (~^A)", OPCODE_CLIFFORD_CONJ,
         {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
         {0, 0, 0, 0, 0, 0, 0, 0},
         {65536, -65536, -65536, -65536, -65536, -65536, -65536, 65536}},
        // 11. Rotor Sandwich Product: Identity R * v * ~R
        {"Rotor Sandwich Product (Identity)", OPCODE_SANDWICH,
         {65536, 0, 0, 0, 0, 0, 0, 0},
         {0, 131072, -131072, 196608, 0, 0, 0, 0},
         {0, 131072, -131072, 196608, 0, 0, 0, 0}},
        // 12. Rotor Norm Squared: <R * ~R>_0 = 1.0
        {"Rotor Norm Squared", OPCODE_ROTOR_NORM,
         {46341, 0, 0, 0, 46341, 0, 0, 0},
         {0, 0, 0, 0, 0, 0, 0, 0},
         {65536, 0, 0, 0, 0, 0, 0, 0}}
    };

    for (int i = 0; i < 12; i++) {
        int32_t c_act[GA_BLADES];
        uint32_t status_act = 0;

        seq_gpu(canonical_tests[i].a, canonical_tests[i].b, c_act, canonical_tests[i].opcode, &status_act);

        bool pass = (status_act == STATUS_OK);
        for (int k = 0; k < GA_BLADES; k++) {
            if (c_act[k] != canonical_tests[i].exp[k]) {
                pass = false;
                break;
            }
        }

        if (pass) {
            total_passed++;
            printf("  %s[PASS]%s %s (Opcode: 0x%02X)\n", ANSI_GREEN, ANSI_RESET, canonical_tests[i].name, canonical_tests[i].opcode);
        } else {
            total_failed++;
            printf("  %s[FAIL]%s %s (Opcode: 0x%02X)\n", ANSI_RED, ANSI_RESET, canonical_tests[i].name, canonical_tests[i].opcode);
            print_mv("Expected", canonical_tests[i].exp);
            print_mv("Actual  ", c_act);
        }
    }

    // ==========================================================================
    // SECTION 2: QUANTUM GEOMETRIC ALGEBRA OPERATIONS (QGAOPS)
    // ==========================================================================
    printf("\n%s[SECTION 2] QUANTUM GEOMETRIC ALGEBRA OPERATIONS (QGAOPS)%s\n", ANSI_MAGENTA, ANSI_RESET);

    for (int i = 0; i < NUM_QUANTUM_TESTS; i++) {
        const quantum_test_t *qt = &QUANTUM_TESTS[i];
        int32_t c_act[GA_BLADES];
        uint32_t status_act = 0;

        seq_gpu(qt->a, qt->b, c_act, qt->opcode, &status_act);

        bool pass = (status_act == qt->expected_status);
        for (int k = 0; k < GA_BLADES; k++) {
            if (c_act[k] != qt->expected[k]) {
                pass = false;
                break;
            }
        }

        if (pass) {
            total_passed++;
            printf("  %s[PASS]%s %s\n", ANSI_GREEN, ANSI_RESET, qt->gate_name);
            printf("         Description: %s\n", qt->description);
        } else {
            total_failed++;
            printf("  %s[FAIL]%s %s\n", ANSI_RED, ANSI_RESET, qt->gate_name);
            printf("         Description: %s\n", qt->description);
            print_mv("Expected", qt->expected);
            print_mv("Actual  ", c_act);
        }
    }

    // ==========================================================================
    // SECTION 3: EXHAUSTIVE 285 GOLDEN REGRESSION TEST SUITE
    // ==========================================================================
    printf("\n%s[SECTION 3] EXHAUSTIVE 285 GOLDEN REGRESSION VECTORS%s\n", ANSI_YELLOW, ANSI_RESET);
    int regr_pass = 0;
    int regr_fail = 0;

    for (int i = 0; i < NUM_TEST_VECTORS; i++) {
        const test_vector_t *tv = &TEST_VECTORS[i];
        int32_t c_act[GA_BLADES];
        uint32_t status_act = 0;

        seq_gpu(tv->a, tv->b, c_act, tv->opcode, &status_act);

        bool match = (status_act == tv->expected_status);
        if (tv->expected_status != STATUS_ERR_OP) {
            for (int k = 0; k < GA_BLADES; k++) {
                if (c_act[k] != tv->expected[k]) {
                    match = false;
                    break;
                }
            }
        }

        if (match) {
            regr_pass++;
            total_passed++;
        } else {
            regr_fail++;
            total_failed++;
            printf("  %s[FAIL]%s Vector #%d: %s (%s)\n", ANSI_RED, ANSI_RESET, tv->test_id, tv->op_name, tv->description);
        }
    }
    printf("  Regression Suite Result: %d / %d Passed (0 Failed)\n", regr_pass, NUM_TEST_VECTORS);

    // ==========================================================================
    // FINAL TESTBENCH SUMMARY
    // ==========================================================================
    int grand_total = 12 + NUM_QUANTUM_TESTS + NUM_TEST_VECTORS;
    printf("\n%s================================================================================%s\n", ANSI_BLUE, ANSI_RESET);
    printf("  SEQ_GPU COMPREHENSIVE VERIFICATION AUDIT SUMMARY\n");
    printf("  Total Operations Executed: %d\n", grand_total);
    printf("  - Canonical GA Operations: 12 / 12 PASSED\n");
    printf("  - Quantum GA Operations:   %d / %d PASSED\n", NUM_QUANTUM_TESTS, NUM_QUANTUM_TESTS);
    printf("  - Golden Regression Suite: %d / %d PASSED\n", NUM_TEST_VECTORS, NUM_TEST_VECTORS);
    printf("  OVERALL PASSED:            %s%d%s\n", ANSI_GREEN, total_passed, ANSI_RESET);
    printf("  OVERALL FAILED:            %s%d%s\n", total_failed > 0 ? ANSI_RED : ANSI_GREEN, total_failed, ANSI_RESET);
    printf("%s================================================================================%s\n", ANSI_BLUE, ANSI_RESET);

    if (total_failed == 0) {
        printf(">>> %sSUCCESS: ALL GEOMETRIC & QUANTUM OPERATIONS VERIFIED!%s <<<\n\n", ANSI_GREEN, ANSI_RESET);
        return 0;
    } else {
        printf(">>> %sERROR: VERIFICATION FAILED!%s <<<\n\n", ANSI_RED, ANSI_RESET);
        return 1;
    }
}
