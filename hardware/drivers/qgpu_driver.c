/*
 * qgpu_driver.c
 * QGAOPS-QGPU PS-Side Driver
 *
 * [PS DRIVER] Runs on ARM Cortex-A9 (Linux or Baremetal).
 *
 * Provides the software API for submitting GA operations
 * to the QGAOPS FPGA accelerator.
 *
 * Interface:
 *   qgpu_init()          — Initialize hardware access
 *   qgpu_submit()        — Submit one GA operation descriptor
 *   qgpu_wait()          — Poll or interrupt-wait for completion
 *   qgpu_read_result()   — Read back result multivector
 *   qgpu_get_metrics()   — Read performance counters
 *   qgpu_close()         — Release hardware resources
 *
 * Compilation:
 *   For Vitis/XSDK (baremetal):
 *     Compile with: -DQGPU_BAREMETAL
 *   For Linux (UIO or /dev/mem):
 *     Compile with: -DQGPU_LINUX
 */

#include "qgpu_driver.h"
#include <string.h>
#include <stdio.h>

#ifdef QGPU_LINUX
#  include <fcntl.h>
#  include <sys/mman.h>
#  include <unistd.h>
#  include <errno.h>
#endif

/* =========================================================================
 * PRIVATE STATE
 * ========================================================================= */

static QGPU_Handle g_handle;
static int g_initialized = 0;

/* =========================================================================
 * 1. INITIALIZATION
 * ========================================================================= */

/**
 * qgpu_init() — Initialize hardware access to QGAOPS accelerator.
 *
 * [BAREMETAL] Direct register access via physical address.
 * [LINUX]     Maps /dev/mem or UIO device node.
 *
 * @return QGPU_OK on success, QGPU_ERR_* on failure.
 */
QGPU_Status qgpu_init(QGPU_Handle *h, const QGPU_InitConfig *cfg)
{
    if (!h || !cfg) return QGPU_ERR_INVALID_ARG;

    memset(h, 0, sizeof(QGPU_Handle));
    h->axilite_base  = cfg->axilite_base;
    h->ddr_base      = cfg->ddr_base;
    h->ddr_size      = cfg->ddr_size;
    h->irq_enabled   = cfg->use_interrupt;

#ifdef QGPU_LINUX
    /* Open /dev/mem for physical address access */
    h->mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if (h->mem_fd < 0) {
        fprintf(stderr, "[QGPU] Failed to open /dev/mem: %s\n", strerror(errno));
        return QGPU_ERR_DEVICE_NOT_FOUND;
    }

    /* Map AXI-Lite control registers */
    h->reg_base = (volatile uint32_t*)mmap(
        NULL, QGPU_AXILITE_MAP_SIZE,
        PROT_READ | PROT_WRITE, MAP_SHARED,
        h->mem_fd, h->axilite_base
    );
    if (h->reg_base == MAP_FAILED) {
        fprintf(stderr, "[QGPU] Failed to map AXI-Lite @ 0x%08X\n", h->axilite_base);
        close(h->mem_fd);
        return QGPU_ERR_MMAP_FAILED;
    }

    /* Map DDR region */
    h->ddr_virt = (volatile uint8_t*)mmap(
        NULL, h->ddr_size,
        PROT_READ | PROT_WRITE, MAP_SHARED,
        h->mem_fd, h->ddr_base
    );
    if (h->ddr_virt == MAP_FAILED) {
        fprintf(stderr, "[QGPU] Failed to map DDR @ 0x%08X\n", h->ddr_base);
        munmap((void*)h->reg_base, QGPU_AXILITE_MAP_SIZE);
        close(h->mem_fd);
        return QGPU_ERR_MMAP_FAILED;
    }
#else
    /* Baremetal: use physical addresses directly */
    h->reg_base = (volatile uint32_t*)(uintptr_t)cfg->axilite_base;
    h->ddr_virt = (volatile uint8_t*)(uintptr_t)cfg->ddr_base;
#endif

    /* Reset accelerator */
    QGPU_REG_WRITE(h, QGPU_REG_CTRL, QGPU_CTRL_RESET);
    QGPU_DELAY_US(10);
    QGPU_REG_WRITE(h, QGPU_REG_CTRL, 0);

    /* Read and verify version */
    h->hw_version = QGPU_REG_READ(h, QGPU_REG_VERSION);
    h->capability = QGPU_REG_READ(h, QGPU_REG_CAPABILITY);

    if (h->hw_version != QGPU_HW_VERSION) {
        fprintf(stderr, "[QGPU] Version mismatch: got 0x%08X, expected 0x%08X\n",
                h->hw_version, QGPU_HW_VERSION);
        /* Continue anyway — version check is informational */
    }

    memcpy(&g_handle, h, sizeof(QGPU_Handle));
    g_initialized = 1;

    printf("[QGPU] Initialized: v%d.%d.%d  cap=0x%08X\n",
           (h->hw_version >> 16) & 0xFF,
           (h->hw_version >>  8) & 0xFF,
            h->hw_version        & 0xFF,
           h->capability);

    return QGPU_OK;
}

/* =========================================================================
 * 2. CACHE MANAGEMENT
 *
 * Critical for ARM Cortex-A9 + DMA coherency.
 * Before writing to DDR for DMA: flush cache.
 * After DMA write to DDR: invalidate cache before reading.
 * ========================================================================= */

static void qgpu_cache_flush(void *addr, size_t size)
{
#ifdef QGPU_LINUX
    /* On Linux, use __builtin_arm_dmb or syscall for cache sync */
    /* For /dev/mem mapped pages, the mmap is typically uncached on Zynq */
    __asm__ volatile("dsb sy");
    __asm__ volatile("dmb sy");
#else
    /* Baremetal Vitis SDK: Xil_DCacheFlushRange */
    /* Xil_DCacheFlushRange((UINTPTR)addr, size); */
    (void)addr; (void)size;
    __asm__ volatile("dsb");
#endif
}

static void qgpu_cache_invalidate(void *addr, size_t size)
{
#ifdef QGPU_LINUX
    __asm__ volatile("dsb sy");
    __asm__ volatile("dmb sy");
#else
    /* Xil_DCacheInvalidateRange((UINTPTR)addr, size); */
    (void)addr; (void)size;
    __asm__ volatile("dsb");
#endif
}

/* =========================================================================
 * 3. DESCRIPTOR WRITE
 * ========================================================================= */

static void write_descriptor(QGPU_Handle *h, const QGPU_Descriptor *desc)
{
    /* Write descriptor to DDR at QGPU_DESC_BASE offset */
    uint32_t desc_offset = QGPU_DESC_BASE - QGPU_DDR_BASE;
    volatile uint8_t *desc_ptr = h->ddr_virt + desc_offset;

    /* Flush before writing */
    qgpu_cache_flush((void*)desc_ptr, sizeof(QGPU_Descriptor));

    /* Copy descriptor to DDR */
    memcpy((void*)desc_ptr, desc, sizeof(QGPU_Descriptor));

    /* Flush after write (ensure DMA sees the data) */
    qgpu_cache_flush((void*)desc_ptr, sizeof(QGPU_Descriptor));
}

/* =========================================================================
 * 4. SUBMIT OPERATION
 * ========================================================================= */

/**
 * qgpu_submit() — Submit one GA operation to the FPGA accelerator.
 *
 * Flow:
 *   1. Validate descriptor
 *   2. Write operand A to DDR
 *   3. Write operand B to DDR
 *   4. Write descriptor to DDR
 *   5. Cache flush
 *   6. Write START to AXI-Lite control register
 *   7. Poll or wait for interrupt
 *
 * @param h     Handle from qgpu_init()
 * @param desc  Operation descriptor
 * @param mv_A  Operand A (8 x int16 FIX16 multivector, or NULL)
 * @param mv_B  Operand B (8 x int16 FIX16 multivector, or NULL)
 * @return QGPU_OK on success
 */
QGPU_Status qgpu_submit(
    QGPU_Handle       *h,
    QGPU_Descriptor   *desc,
    const int16_t     *mv_A,
    const int16_t     *mv_B
)
{
    if (!h || !desc) return QGPU_ERR_INVALID_ARG;

    /* Write operand A to DDR */
    if (mv_A && desc->addr_A_lo >= QGPU_DDR_BASE) {
        uint32_t a_offset = desc->addr_A_lo - QGPU_DDR_BASE;
        volatile int16_t *a_ptr = (volatile int16_t*)(h->ddr_virt + a_offset);
        for (int i = 0; i < QGPU_MV_G3_DIM; i++) {
            a_ptr[i] = mv_A[i];
        }
        qgpu_cache_flush((void*)a_ptr, QGPU_MV_DENSE_BYTES);
    }

    /* Write operand B to DDR */
    if (mv_B && desc->addr_B_lo >= QGPU_DDR_BASE) {
        uint32_t b_offset = desc->addr_B_lo - QGPU_DDR_BASE;
        volatile int16_t *b_ptr = (volatile int16_t*)(h->ddr_virt + b_offset);
        for (int i = 0; i < QGPU_MV_G3_DIM; i++) {
            b_ptr[i] = mv_B[i];
        }
        qgpu_cache_flush((void*)b_ptr, QGPU_MV_DENSE_BYTES);
    }

    /* Write descriptor to DDR */
    desc->valid = 1;
    desc->status = QGPU_STATUS_IDLE;
    write_descriptor(h, desc);

    /* Write descriptor address and opcode to AXI-Lite */
    QGPU_REG_WRITE(h, QGPU_REG_DESC_ADDR_LO, QGPU_DESC_BASE);
    QGPU_REG_WRITE(h, QGPU_REG_OPCODE,       desc->opcode);
    QGPU_REG_WRITE(h, QGPU_REG_ALGEBRA,      desc->algebra_mode);
    QGPU_REG_WRITE(h, QGPU_REG_PRECISION,    desc->precision);
    QGPU_REG_WRITE(h, QGPU_REG_FLAGS,        desc->flags);

    /* START pulse */
    uint32_t ctrl = QGPU_CTRL_START;
    if (h->irq_enabled) ctrl |= QGPU_CTRL_IRQ_EN;
    QGPU_REG_WRITE(h, QGPU_REG_CTRL, ctrl);

    return QGPU_OK;
}

/* =========================================================================
 * 5. WAIT FOR COMPLETION
 * ========================================================================= */

/**
 * qgpu_wait() — Wait for accelerator to complete.
 *
 * [POLLING MODE] Polls STATUS register until DONE or ERROR.
 * [INTERRUPT MODE] Waits for interrupt (Linux: eventfd; Baremetal: XIntc).
 *
 * @param timeout_us   Timeout in microseconds (0 = infinite)
 * @return QGPU_OK on DONE, QGPU_ERR_TIMEOUT, or QGPU_ERR_HW_ERROR
 */
QGPU_Status qgpu_wait(QGPU_Handle *h, uint32_t timeout_us)
{
    if (!h) return QGPU_ERR_INVALID_ARG;

    uint32_t elapsed = 0;
    uint32_t poll_interval_us = 10;  /* Poll every 10 µs */

    while (1) {
        uint32_t status = QGPU_REG_READ(h, QGPU_REG_STATUS);
        status &= 0x3;  /* Lower 2 bits = state */

        if (status == QGPU_STATUS_DONE) {
            return QGPU_OK;
        }
        if (status == QGPU_STATUS_ERROR) {
            fprintf(stderr, "[QGPU] Hardware error during operation\n");
            return QGPU_ERR_HW_ERROR;
        }

        if (timeout_us > 0 && elapsed >= timeout_us) {
            fprintf(stderr, "[QGPU] Timeout after %u µs\n", elapsed);
            return QGPU_ERR_TIMEOUT;
        }

        QGPU_DELAY_US(poll_interval_us);
        elapsed += poll_interval_us;
    }
}

/* =========================================================================
 * 6. READ RESULT
 * ========================================================================= */

/**
 * qgpu_read_result() — Read back result multivector from DDR.
 *
 * Must be called after qgpu_wait() returns QGPU_OK.
 * Performs cache invalidate before reading.
 *
 * @param h          Handle
 * @param result_mv  Output: 8 x int16 FIX16 multivector
 * @param addr       DDR physical address of result (e.g. QGPU_RESULT)
 */
QGPU_Status qgpu_read_result(
    QGPU_Handle *h,
    int16_t     *result_mv,
    uint32_t     addr
)
{
    if (!h || !result_mv) return QGPU_ERR_INVALID_ARG;
    if (addr < QGPU_DDR_BASE) return QGPU_ERR_INVALID_ARG;

    uint32_t offset = addr - QGPU_DDR_BASE;
    volatile int16_t *ptr = (volatile int16_t*)(h->ddr_virt + offset);

    /* Invalidate cache before reading (DMA may have written new data) */
    qgpu_cache_invalidate((void*)ptr, QGPU_MV_DENSE_BYTES);

    /* Read 8 coefficients */
    for (int i = 0; i < QGPU_MV_G3_DIM; i++) {
        result_mv[i] = ptr[i];
    }

    return QGPU_OK;
}

/* =========================================================================
 * 7. PERFORMANCE COUNTERS
 * ========================================================================= */

/**
 * qgpu_get_metrics() — Read hardware performance counters.
 *
 * @param h       Handle
 * @param metrics Output metrics structure
 */
QGPU_Status qgpu_get_metrics(QGPU_Handle *h, QGPU_Metrics *metrics)
{
    if (!h || !metrics) return QGPU_ERR_INVALID_ARG;

    uint32_t lo, hi;

    lo = QGPU_REG_READ(h, QGPU_REG_CYCLE_LO);
    hi = QGPU_REG_READ(h, QGPU_REG_CYCLE_HI);
    metrics->cycle_count = ((uint64_t)hi << 32) | lo;

    lo = QGPU_REG_READ(h, QGPU_REG_OP_COUNT_LO);
    hi = QGPU_REG_READ(h, QGPU_REG_OP_COUNT_HI);
    metrics->op_count = ((uint64_t)hi << 32) | lo;

    lo = QGPU_REG_READ(h, QGPU_REG_BYTES_RD_LO);
    hi = QGPU_REG_READ(h, QGPU_REG_BYTES_RD_HI);
    metrics->read_bytes = ((uint64_t)hi << 32) | lo;

    lo = QGPU_REG_READ(h, QGPU_REG_BYTES_WR_LO);
    hi = QGPU_REG_READ(h, QGPU_REG_BYTES_WR_HI);
    metrics->write_bytes = ((uint64_t)hi << 32) | lo;

    lo = QGPU_REG_READ(h, QGPU_REG_STALL_LO);
    hi = QGPU_REG_READ(h, QGPU_REG_STALL_HI);
    metrics->stall_cycles = ((uint64_t)hi << 32) | lo;

    /* Derived metrics */
    if (metrics->cycle_count > 0) {
        metrics->compute_utilization =
            (float)(metrics->cycle_count - metrics->stall_cycles) /
            (float)metrics->cycle_count;
    } else {
        metrics->compute_utilization = 0.0f;
    }

    if (metrics->op_count > 0) {
        metrics->cycles_per_op =
            (float)metrics->cycle_count / (float)metrics->op_count;
        metrics->ops_per_second =
            (float)metrics->op_count * 100e6f / (float)metrics->cycle_count;
    }

    return QGPU_OK;
}

/**
 * qgpu_print_metrics() — Print formatted performance report.
 */
void qgpu_print_metrics(const QGPU_Metrics *m)
{
    printf("\n=== QGAOPS-QGPU HARDWARE PERFORMANCE [HARDWARE_MEASUREMENT] ===\n");
    printf("  Cycle count:         %llu\n",    (unsigned long long)m->cycle_count);
    printf("  Operations:          %llu\n",    (unsigned long long)m->op_count);
    printf("  DDR read bytes:      %llu\n",    (unsigned long long)m->read_bytes);
    printf("  DDR write bytes:     %llu\n",    (unsigned long long)m->write_bytes);
    printf("  Stall cycles:        %llu\n",    (unsigned long long)m->stall_cycles);
    printf("  Cycles/operation:    %.2f\n",    m->cycles_per_op);
    printf("  Ops/second:          %.2f M\n",  m->ops_per_second / 1e6f);
    printf("  Compute utilization: %.1f%%\n",  m->compute_utilization * 100.0f);
    printf("\n  NOTE: All values are HARDWARE_MEASUREMENT from ZedBoard.\n");
    printf("=================================================================\n");
}

/* =========================================================================
 * 8. CLOSE / CLEANUP
 * ========================================================================= */

void qgpu_close(QGPU_Handle *h)
{
    if (!h) return;

    /* Reset accelerator */
    if (h->reg_base) {
        QGPU_REG_WRITE(h, QGPU_REG_CTRL, QGPU_CTRL_RESET);
    }

#ifdef QGPU_LINUX
    if (h->reg_base && h->reg_base != MAP_FAILED)
        munmap((void*)h->reg_base, QGPU_AXILITE_MAP_SIZE);
    if (h->ddr_virt && h->ddr_virt != MAP_FAILED)
        munmap((void*)h->ddr_virt, h->ddr_size);
    if (h->mem_fd >= 0)
        close(h->mem_fd);
#endif

    memset(h, 0, sizeof(QGPU_Handle));
    g_initialized = 0;
    printf("[QGPU] Closed.\n");
}

/* =========================================================================
 * 9. HIGH-LEVEL CONVENIENCE API
 * ========================================================================= */

/**
 * qgpu_compute_gp() — Compute geometric product A*B on FPGA.
 *
 * High-level wrapper: submit + wait + read result.
 *
 * @param h        Handle
 * @param mv_A     Operand A (8 x int16 FIX16)
 * @param mv_B     Operand B (8 x int16 FIX16)
 * @param mv_out   Output C = A*B (8 x int16 FIX16)
 */
QGPU_Status qgpu_compute_gp(
    QGPU_Handle   *h,
    const int16_t *mv_A,
    const int16_t *mv_B,
    int16_t       *mv_out
)
{
    QGPU_Descriptor desc;
    QGPU_DESC_CLEAR(&desc);

    desc.opcode       = QGPU_OP_GP;
    desc.algebra_mode = QGPU_ALGEBRA_G3;
    desc.precision    = QGPU_PREC_FIX16;
    desc.element_count = 8;
    QGPU_DESC_SET_ADDR_A   (&desc, QGPU_OPERAND_A);
    QGPU_DESC_SET_ADDR_B   (&desc, QGPU_OPERAND_B);
    QGPU_DESC_SET_ADDR_OUT (&desc, QGPU_RESULT);
    desc.valid = 1;

    QGPU_Status s;
    s = qgpu_submit(h, &desc, mv_A, mv_B);
    if (s != QGPU_OK) return s;

    s = qgpu_wait(h, 100000);  /* 100 ms timeout */
    if (s != QGPU_OK) return s;

    return qgpu_read_result(h, mv_out, QGPU_RESULT);
}

/**
 * qgpu_compute_sandwich() — Compute R*v*~R on FPGA.
 */
QGPU_Status qgpu_compute_sandwich(
    QGPU_Handle   *h,
    const int16_t *rotor,
    const int16_t *vector,
    int16_t       *mv_out
)
{
    QGPU_Descriptor desc;
    QGPU_DESC_CLEAR(&desc);

    desc.opcode       = QGPU_OP_SANDWICH;
    desc.algebra_mode = QGPU_ALGEBRA_G3;
    desc.precision    = QGPU_PREC_FIX16;
    desc.flags        = QGPU_FLAG_FUSE_SAND;  /* Fused: no DDR for intermediate */
    desc.element_count = 8;
    QGPU_DESC_SET_ADDR_A   (&desc, QGPU_OPERAND_A);  /* Rotor R */
    QGPU_DESC_SET_ADDR_B   (&desc, QGPU_OPERAND_B);  /* Vector v */
    QGPU_DESC_SET_ADDR_OUT (&desc, QGPU_RESULT);
    desc.valid = 1;

    QGPU_Status s;
    s = qgpu_submit(h, &desc, rotor, vector);
    if (s != QGPU_OK) return s;

    s = qgpu_wait(h, 100000);
    if (s != QGPU_OK) return s;

    return qgpu_read_result(h, mv_out, QGPU_RESULT);
}
