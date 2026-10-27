/*
 * qgpu_driver.h
 * QGAOPS-QGPU PS-Side Driver Header
 */

#ifndef QGPU_DRIVER_H
#define QGPU_DRIVER_H

#include <stdint.h>
#include <stddef.h>
#include "../hls/include/qgpu_descriptor.h"

#ifdef __cplusplus
extern "C" {
#endif

/* =========================================================================
 * STATUS CODES
 * ========================================================================= */

typedef enum {
    QGPU_OK                  = 0,
    QGPU_ERR_INVALID_ARG     = 1,
    QGPU_ERR_DEVICE_NOT_FOUND= 2,
    QGPU_ERR_MMAP_FAILED     = 3,
    QGPU_ERR_TIMEOUT         = 4,
    QGPU_ERR_HW_ERROR        = 5,
    QGPU_ERR_NOT_INITIALIZED = 6,
    QGPU_ERR_UNSUPPORTED_OP  = 7,
} QGPU_Status;

/* =========================================================================
 * HANDLE
 * ========================================================================= */

#define QGPU_AXILITE_MAP_SIZE  0x10000u   /* 64 KB mapping */

typedef struct {
    volatile uint32_t *reg_base;    /* AXI-Lite register base (virtual)   */
    volatile uint8_t  *ddr_virt;   /* DDR region base (virtual)           */
    uint32_t           axilite_base; /* Physical AXI-Lite base             */
    uint32_t           ddr_base;    /* Physical DDR base                   */
    uint32_t           ddr_size;    /* DDR region size in bytes            */
    int                mem_fd;      /* /dev/mem file descriptor (Linux)    */
    int                irq_enabled; /* 1 = use interrupt, 0 = polling      */
    uint32_t           hw_version;  /* Hardware IP version                 */
    uint32_t           capability;  /* Hardware capability flags           */
} QGPU_Handle;

/* =========================================================================
 * INIT CONFIG
 * ========================================================================= */

typedef struct {
    uint32_t axilite_base;   /* Physical: default 0x43C00000             */
    uint32_t ddr_base;       /* Physical: default QGPU_DDR_BASE          */
    uint32_t ddr_size;       /* Size: default 64MB                       */
    int      use_interrupt;  /* 0=polling, 1=interrupt                   */
} QGPU_InitConfig;

#define QGPU_DEFAULT_CONFIG { \
    .axilite_base  = QGPU_AXILITE_BASE, \
    .ddr_base      = QGPU_DDR_BASE, \
    .ddr_size      = 0x04000000u, \
    .use_interrupt = 0 \
}

/* =========================================================================
 * METRICS
 * ========================================================================= */

typedef struct {
    uint64_t cycle_count;
    uint64_t op_count;
    uint64_t read_bytes;
    uint64_t write_bytes;
    uint64_t stall_cycles;
    float    cycles_per_op;
    float    ops_per_second;
    float    compute_utilization;
} QGPU_Metrics;

/* =========================================================================
 * REGISTER ACCESS MACROS
 * ========================================================================= */

#define QGPU_REG_WRITE(h, offset, val) \
    ((h)->reg_base[(offset)/4] = (uint32_t)(val))

#define QGPU_REG_READ(h, offset) \
    ((h)->reg_base[(offset)/4])

/* Platform delay */
#ifdef QGPU_LINUX
#  include <time.h>
#  define QGPU_DELAY_US(us) do { \
       struct timespec ts = {0, (us)*1000L}; nanosleep(&ts, NULL); } while(0)
#else
#  define QGPU_DELAY_US(us) do { volatile int _i; \
       for(_i=0; _i<(us)*10; _i++); } while(0)
#endif

/* =========================================================================
 * API
 * ========================================================================= */

QGPU_Status qgpu_init(QGPU_Handle *h, const QGPU_InitConfig *cfg);
QGPU_Status qgpu_submit(QGPU_Handle *h, QGPU_Descriptor *desc,
                        const int16_t *mv_A, const int16_t *mv_B);
QGPU_Status qgpu_wait(QGPU_Handle *h, uint32_t timeout_us);
QGPU_Status qgpu_read_result(QGPU_Handle *h, int16_t *result_mv, uint32_t addr);
QGPU_Status qgpu_get_metrics(QGPU_Handle *h, QGPU_Metrics *metrics);
void        qgpu_print_metrics(const QGPU_Metrics *m);
void        qgpu_close(QGPU_Handle *h);

/* High-level wrappers */
QGPU_Status qgpu_compute_gp(QGPU_Handle *h, const int16_t *mv_A,
                             const int16_t *mv_B, int16_t *mv_out);
QGPU_Status qgpu_compute_sandwich(QGPU_Handle *h, const int16_t *rotor,
                                  const int16_t *vector, int16_t *mv_out);

#ifdef __cplusplus
}
#endif
#endif /* QGPU_DRIVER_H */
