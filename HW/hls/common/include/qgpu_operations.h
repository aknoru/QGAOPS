#ifndef QGPU_OPERATIONS_H
#define QGPU_OPERATIONS_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =========================================================================
 * QGAOPS-QGPU CANONICAL OPERATION IDENTIFIERS (OPCODES)
 * Strictly aligned with software/hardware_interface/contract.py
 * ========================================================================= */
#define OPCODE_NOP               0x00  /* No Operation */
#define OPCODE_GP                0x01  /* Geometric Product: C = A * B */
#define OPCODE_WEDGE             0x02  /* Outer / Wedge Product: C = A ^ B */
#define OPCODE_INNER             0x03  /* Hestenes Inner Product: C = A . B */
#define OPCODE_ADD               0x04  /* Multivector Addition: C = A + B */
#define OPCODE_SUB               0x05  /* Multivector Subtraction: C = A - B */
#define OPCODE_SCALAR_MUL        0x06  /* Scalar Multiplication: C = B[0] * A */
#define OPCODE_GRADE_PROJ        0x07  /* Grade Projection: C = <A>_k, k = B[0] */
#define OPCODE_REVERSE           0x08  /* Reversion: C = ~A */
#define OPCODE_GRADE_INVOLUTION  0x09  /* Grade Involution: C = ^A */
#define OPCODE_CLIFFORD_CONJ     0x0A  /* Clifford Conjugation: C = ~^A */
#define OPCODE_SANDWICH          0x0B  /* Rotor Sandwich: C = A * B * ~A */
#define OPCODE_ROTOR_NORM        0x0C  /* Rotor Norm Squared: C[0] = <A * ~A>_0 */

/* =========================================================================
 * ACCELERATOR STATUS AND ERROR CODES
 * ========================================================================= */
#define STATUS_OK         0x00  /* Execution successful, no overflow */
#define STATUS_ERR_OP     0x01  /* Invalid or unsupported opcode */
#define STATUS_ERR_LEN    0x02  /* Invalid batch or multivector length */
#define STATUS_OVERFLOW   0x04  /* Sticky saturation / overflow occurred */

#ifdef __cplusplus
}
#endif

#endif /* QGPU_OPERATIONS_H */
