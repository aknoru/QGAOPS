/**
 * main.c - Standalone self-test application for ARM Cortex-A9 on PYNQ-Z2
 */

#include <stdio.h>
#include "qgpu_standalone.h"

int main() {
    printf("============================================================\n");
    printf("  QGAOPS-QGPU Standalone Hardware Self-Test on PYNQ-Z2\n");
    printf("============================================================\n");

    qgpu_inst_t dev;
    qgpu_init(&dev, QGPU_PARALLEL_BASE_ADDR);

    int32_t a[8] = { 65536, 131072, 0, 0, 0, 0, 0, 0 }; // 1.0 + 2.0*e1
    int32_t b[8] = { 196608, -65536, 0, 0, 0, 0, 0, 0 }; // 3.0 - 1.0*e1
    int32_t c[8] = { 0 };
    uint32_t status = 0;

    int ret = qgpu_execute(&dev, a, b, c, QGPU_OPCODE_ADD, 0, &status);
    if (ret != 0) {
        printf("[FAIL] Accelerator timed out!\n");
        return -1;
    }

    printf("[PASS] QGPU Accelerator responded. Status=0x%08X\n", status);
    printf("Result c[0] = %f (expected 4.0)\n", (double)c[0] / 65536.0);
    printf("Result c[1] = %f (expected 1.0)\n", (double)c[1] / 65536.0);
    printf("============================================================\n");
    printf("  STANDALONE SELF-TEST COMPLETE\n");
    printf("============================================================\n");

    return 0;
}
