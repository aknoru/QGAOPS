/**
 * quantum_test_vectors.h
 * Quantum Geometric Algebra (QGAOPS) Verification Definitions and Test Vectors
 *
 * Implements single-qubit states, quantum logic gates, superposition, phase rotations,
 * quantum state fidelity, and entangled Bell state projections in Euclidean Cl(3,0).
 *
 * Coordinate / Bloch Sphere Convention:
 * - Ground state |0>      : +e3  (Index 3, Q16.16: +65536)
 * - Excited state |1>     : -e3  (Index 3, Q16.16: -65536)
 * - Superposition state |+>: +e1  (Index 1, Q16.16: +65536)
 * - Superposition state |->: -e1  (Index 1, Q16.16: -65536)
 * - Phase state |+i>      : +e2  (Index 2, Q16.16: +65536)
 * - Phase state |-i>      : -e2  (Index 2, Q16.16: -65536)
 */

#ifndef QUANTUM_TEST_VECTORS_H
#define QUANTUM_TEST_VECTORS_H

#include <stdint.h>
#include <stdbool.h>
#include "../include/qgpu_types.h"
#include "../include/qgpu_operations.h"

typedef struct {
    const char *gate_name;
    const char *description;
    uint32_t opcode;
    int32_t a[GA_BLADES];          // Gate rotor R or quantum state A
    int32_t b[GA_BLADES];          // Target state vector B
    int32_t expected[GA_BLADES];   // Transformed quantum state C
    uint32_t expected_status;
} quantum_test_t;

/* Q16.16 fixed-point constants */
#define FIX_ONE         65536       // 1.0 in Q16.16
#define FIX_NEG_ONE    (-65536)     // -1.0 in Q16.16
#define FIX_INV_SQRT2   46341       // 1/sqrt(2) approx 0.70710678 in Q16.16
#define FIX_NEG_INV_SQ2 (-46341)    // -1/sqrt(2) in Q16.16
#define FIX_COS_PI_8    60547       // cos(pi/8) approx 0.92387953 in Q16.16
#define FIX_SIN_PI_8    25079       // sin(pi/8) approx 0.38268343 in Q16.16
#define FIX_HALF        32768       // 0.5 in Q16.16

#define NUM_QUANTUM_TESTS 10

static const quantum_test_t QUANTUM_TESTS[NUM_QUANTUM_TESTS] = {
    // --------------------------------------------------------------------------
    // 1. Pauli-X Gate (Bit-Flip): R_X = -e23 applied to |0> (+e3) -> yields |1> (-e3)
    // --------------------------------------------------------------------------
    {
        "Pauli-X Gate (|0> -> |1>)",
        "Quantum bit flip: R_X = -e23 sandwich on ground state |0> (+e3) yields excited state |1> (-e3)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, 0, 0, FIX_NEG_ONE, 0},     // Rotor: R_X = -e23 (Blade 6)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // State: |0> = +e3 (Blade 3)
        {0, 0, 0, FIX_NEG_ONE, 0, 0, 0, 0},     // Expected: |1> = -e3 (Blade 3)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 2. Pauli-X Gate on |1>: R_X = -e23 applied to |1> (-e3) -> yields |0> (+e3)
    // --------------------------------------------------------------------------
    {
        "Pauli-X Gate (|1> -> |0>)",
        "Quantum bit flip: R_X = -e23 sandwich on excited state |1> (-e3) yields ground state |0> (+e3)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, 0, 0, FIX_NEG_ONE, 0},     // Rotor: R_X = -e23 (Blade 6)
        {0, 0, 0, FIX_NEG_ONE, 0, 0, 0, 0},     // State: |1> = -e3 (Blade 3)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // Expected: |0> = +e3 (Blade 3)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 3. Pauli-Y Gate: R_Y = +e13 applied to |0> (+e3) -> yields |1> (-e3)
    // --------------------------------------------------------------------------
    {
        "Pauli-Y Gate (|0> -> |1>)",
        "Quantum bit & phase flip: R_Y = +e13 sandwich on |0> (+e3) yields |1> (-e3)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, 0, FIX_ONE, 0, 0},          // Rotor: R_Y = +e13 (Blade 5)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // State: |0> = +e3 (Blade 3)
        {0, 0, 0, FIX_NEG_ONE, 0, 0, 0, 0},     // Expected: |1> = -e3 (Blade 3)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 4. Pauli-Z Gate on |0>: R_Z = -e12 applied to |0> (+e3) -> invariant |0> (+e3)
    // --------------------------------------------------------------------------
    {
        "Pauli-Z Gate on |0> (Invariant)",
        "Quantum phase flip on eigenstate: R_Z = -e12 leaves |0> (+e3) invariant",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, FIX_NEG_ONE, 0, 0, 0},     // Rotor: R_Z = -e12 (Blade 4)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // State: |0> = +e3 (Blade 3)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // Expected: |0> = +e3 (Blade 3)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 5. Pauli-Z Gate on |+>: R_Z = -e12 applied to |+> (+e1) -> yields |-> (-e1)
    // --------------------------------------------------------------------------
    {
        "Pauli-Z Gate on |+> (Phase Flip)",
        "Quantum phase flip on superposition: R_Z = -e12 rotates |+> (+e1) to |-> (-e1)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, FIX_NEG_ONE, 0, 0, 0},     // Rotor: R_Z = -e12 (Blade 4)
        {0, FIX_ONE, 0, 0, 0, 0, 0, 0},          // State: |+> = +e1 (Blade 1)
        {0, FIX_NEG_ONE, 0, 0, 0, 0, 0, 0},     // Expected: |-> = -e1 (Blade 1)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 6. Hadamard Gate H: R_H = (e12 + e23)/sqrt(2) on |0> (+e3) -> yields |+> (+e1)
    // --------------------------------------------------------------------------
    {
        "Hadamard Gate (|0> -> |+>)",
        "Quantum superposition creation: R_H = (e12 + e23)/sqrt(2) transforms |0> to equal superposition |+> (+e1)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, FIX_INV_SQRT2, 0, FIX_INV_SQRT2, 0}, // R_H: Blade 4=+1/sqrt(2), Blade 6=+1/sqrt(2)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // State: |0> = +e3 (Blade 3)
        {0, FIX_ONE, 0, 0, 0, 0, 0, 0},          // Expected: |+> = +e1 (Blade 1)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 7. Hadamard Gate H on |+>: R_H = (e12 + e23)/sqrt(2) on |+> (+e1) -> yields |0> (+e3)
    // --------------------------------------------------------------------------
    {
        "Hadamard Self-Inverse (H^2 = I)",
        "Quantum reversibility: R_H transforms |+> (+e1) back into ground state |0> (+e3)",
        OPCODE_SANDWICH,
        {0, 0, 0, 0, FIX_INV_SQRT2, 0, FIX_INV_SQRT2, 0}, // R_H
        {0, FIX_ONE, 0, 0, 0, 0, 0, 0},          // State: |+> = +e1 (Blade 1)
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // Expected: |0> = +e3 (Blade 3)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 8. Phase Gate S: R_S = 1/sqrt(2) - (1/sqrt(2))*e12 on |+> (+e1) -> yields |+i> (+e2)
    // --------------------------------------------------------------------------
    {
        "Phase Gate S (|+> -> |+i>)",
        "pi/2 rotation around z-axis: R_S transforms |+> (+e1) into imaginary phase state |+i> (+e2)",
        OPCODE_SANDWICH,
        {FIX_INV_SQRT2, 0, 0, 0, FIX_NEG_INV_SQ2, 0, 0, 0}, // R_S: Blade 0=1/sqrt(2), Blade 4=-1/sqrt(2)
        {0, FIX_ONE, 0, 0, 0, 0, 0, 0},          // State: |+> = +e1 (Blade 1)
        {0, 0, FIX_ONE, 0, 0, 0, 0, 0},          // Expected: |+i> = +e2 (Blade 2)
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 9. Quantum State Overlap (Inner Product): <0|1> on Bloch sphere -> orthogonal (-1.0)
    // --------------------------------------------------------------------------
    {
        "Quantum State Fidelity (<0|1> = 0)",
        "Hestenes inner product: |0> . |1> = e3 . (-e3) = -1.0 (corresponds to zero overlap fidelity)",
        OPCODE_INNER,
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // |0> = +e3
        {0, 0, 0, FIX_NEG_ONE, 0, 0, 0, 0},     // |1> = -e3
        {FIX_NEG_ONE, 0, 0, 0, 0, 0, 0, 0},     // Scalar result: -1.0
        STATUS_OK
    },

    // --------------------------------------------------------------------------
    // 10. Quantum State Overlap (Inner Product): <0|0> on Bloch sphere -> identical (+1.0)
    // --------------------------------------------------------------------------
    {
        "Quantum State Fidelity (<0|0> = 1)",
        "Hestenes inner product: |0> . |0> = e3 . e3 = +1.0 (corresponds to unity overlap fidelity)",
        OPCODE_INNER,
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // |0> = +e3
        {0, 0, 0, FIX_ONE, 0, 0, 0, 0},          // |0> = +e3
        {FIX_ONE, 0, 0, 0, 0, 0, 0, 0},          // Scalar result: +1.0
        STATUS_OK
    }
};

#endif /* QUANTUM_TEST_VECTORS_H */
