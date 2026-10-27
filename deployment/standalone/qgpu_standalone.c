/**
 * qgpu_standalone.c
 * Bare-metal / Standalone C driver implementation for QGAOPS-QGPU Cl(3,0) Accelerator.
 */

#include "qgpu_standalone.h"

#define REG_WRITE(addr, val) (*(volatile uint32_t *)(addr) = (uint32_t)(val))
#define REG_READ(addr)       (*(volatile uint32_t *)(addr))

void qgpu_init(qgpu_inst_t *dev, uintptr_t base_addr) {
    dev->base_addr = base_addr;
    REG_WRITE(base_addr + QGPU_REG_DMA_LEN, 0);
}

int qgpu_execute(qgpu_inst_t *dev, const int32_t a[8], const int32_t b[8], int32_t c[8], uint32_t opcode, uint8_t slot, uint32_t *status) {
    uintptr_t base = dev->base_addr;

    /* Ensure direct register mode */
    REG_WRITE(base + QGPU_REG_DMA_LEN, 0);

    /* 1. Write operand A (8 blades) */
    for (int i = 0; i < 8; i++) {
        REG_WRITE(base + QGPU_REG_A_BASE + i * 8, a[i]);
    }

    /* 2. Write operand B (8 blades) */
    for (int i = 0; i < 8; i++) {
        REG_WRITE(base + QGPU_REG_B_BASE + i * 8, b[i]);
    }

    /* 3. Write opcode and AAMF buffer slot */
    uint32_t full_op = (opcode & 0xFFFF) | (((uint32_t)slot & 0x3F) << 16);
    REG_WRITE(base + QGPU_REG_OPCODE, full_op);

    /* 4. Trigger start: AP_START = 1 */
    REG_WRITE(base + QGPU_REG_CTRL, 0x01);

    /* 5. Poll AP_DONE (Bit 1) with timeout */
    uint32_t timeout = 1000000;
    while (!(REG_READ(base + QGPU_REG_CTRL) & 0x02)) {
        if (--timeout == 0) {
            return -1; /* Timeout */
        }
    }

    /* 6. Read back result C (8 blades) */
    for (int i = 0; i < 8; i++) {
        c[i] = (int32_t)REG_READ(base + QGPU_REG_C_BASE + i * 16);
    }

    /* 7. Read status */
    if (status) {
        *status = REG_READ(base + QGPU_REG_STATUS);
    }

    return 0;
}
