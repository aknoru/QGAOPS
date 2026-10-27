/**
 * qgpu_standalone.h
 * Bare-metal / Standalone C driver for QGAOPS-QGPU Cl(3,0) Accelerator on Zynq-7000.
 */

#ifndef QGPU_STANDALONE_H
#define QGPU_STANDALONE_H

#include <stdint.h>
#include <stdbool.h>

#define QGPU_PARALLEL_BASE_ADDR   0x40000000
#define QGPU_SEQUENTIAL_BASE_ADDR 0x40010000

/* Register offsets */
#define QGPU_REG_CTRL         0x00
#define QGPU_REG_GIER         0x04
#define QGPU_REG_IP_IER       0x08
#define QGPU_REG_IP_ISR       0x0C
#define QGPU_REG_A_BASE       0x10
#define QGPU_REG_B_BASE       0x50
#define QGPU_REG_C_BASE       0x90
#define QGPU_REG_OPCODE       0x110
#define QGPU_REG_STATUS       0x118
#define QGPU_REG_DMA_LEN      0x128

/* Opcodes */
#define QGPU_OPCODE_NOP             0x0000
#define QGPU_OPCODE_GEOMETRIC       0x0001
#define QGPU_OPCODE_WEDGE           0x0002
#define QGPU_OPCODE_INNER           0x0003
#define QGPU_OPCODE_ADD             0x0004
#define QGPU_OPCODE_SUB             0x0005
#define QGPU_OPCODE_SCALAR_MUL      0x0006
#define QGPU_OPCODE_GRADE_PROJECT   0x0007
#define QGPU_OPCODE_REVERSE         0x0008
#define QGPU_OPCODE_GRADE_INVOLUTION 0x0009
#define QGPU_OPCODE_CLIFFORD_CONJ   0x000A
#define QGPU_OPCODE_ROTOR_SANDWICH  0x000B
#define QGPU_OPCODE_ROTOR_NORM      0x000C

typedef struct {
    uintptr_t base_addr;
} qgpu_inst_t;

void qgpu_init(qgpu_inst_t *dev, uintptr_t base_addr);
int qgpu_execute(qgpu_inst_t *dev, const int32_t a[8], const int32_t b[8], int32_t c[8], uint32_t opcode, uint8_t slot, uint32_t *status);

#endif /* QGPU_STANDALONE_H */
