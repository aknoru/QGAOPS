/**
 * qgpu_ga_sequential_top.cpp
 * Dedicated top-level synthesizable function for Variant A: Resource-Shared IP.
 * Exposes AXI4-Lite control/register ports and AXI4-Stream DMA ports.
 */
#include "qgpu_ga_engine.h"

void qgpu_ga_sequential_top(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status,
    uint32_t dma_len,
    hls::stream<axis_word_t> &dma_in,
    hls::stream<axis_word_t> &dma_out
) {
#pragma HLS INTERFACE s_axilite port=return bundle=control
#pragma HLS INTERFACE s_axilite port=a bundle=control
#pragma HLS INTERFACE s_axilite port=b bundle=control
#pragma HLS INTERFACE s_axilite port=c bundle=control
#pragma HLS INTERFACE s_axilite port=opcode bundle=control
#pragma HLS INTERFACE s_axilite port=status bundle=control
#pragma HLS INTERFACE s_axilite port=dma_len bundle=control
#pragma HLS INTERFACE axis port=dma_in register
#pragma HLS INTERFACE axis port=dma_out register

    if (dma_len == 0) {
        // Direct AXI4-Lite register access mode
        qgpu_ga_engine_shared(a, b, c, opcode, status);
    } else {
        // High-throughput AXI4-Stream DMA mode
        uint32_t agg_status = STATUS_OK;

        SEQ_DMA_BATCH_LOOP:
        for (uint32_t i = 0; i < dma_len; i++) {
            int32_t in_a[GA_BLADES];
            int32_t in_b[GA_BLADES];
            int32_t out_c[GA_BLADES];
            uint32_t cur_status = STATUS_OK;

            SEQ_DMA_READ_A:
            for (int k = 0; k < GA_BLADES; k++) {
                #pragma HLS PIPELINE II=1
                axis_word_t w = dma_in.read();
                in_a[k] = w.data;
            }

            SEQ_DMA_READ_B:
            for (int k = 0; k < GA_BLADES; k++) {
                #pragma HLS PIPELINE II=1
                axis_word_t w = dma_in.read();
                in_b[k] = w.data;
            }

            qgpu_ga_engine_shared(in_a, in_b, out_c, opcode, &cur_status);
            agg_status |= cur_status;

            SEQ_DMA_WRITE_C:
            for (int k = 0; k < GA_BLADES; k++) {
                #pragma HLS PIPELINE II=1
                axis_word_t w;
                w.data = out_c[k];
                w.keep = -1;
                w.strb = -1;
                w.last = (k == (GA_BLADES - 1) && i == (dma_len - 1)) ? 1 : 0;
                dma_out.write(w);
            }
        }
        *status = agg_status;
    }
}
