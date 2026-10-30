// =============================================================================
// qgpu_led_controller.v
// QGAOPS-QGPU: 4-LED Progress Controller for PARALLEL_GPU_PYNQZU
// Target: AMD PYNQ-ZU Rev B (xczu5eg-sfvc784-1-e), Bank 66, LVCMOS12
//
// LED Semantics:
//   LED0 (B5) = IDLE / READY    -- solid ON when server is alive, no op in flight
//   LED1 (A6) = AP_START / BUSY -- pulses for >= 40 ms on every new operation start
//   LED2 (B8) = AP_DONE / OK    -- pulses for >= 40 ms on every successful completion
//   LED3 (A7) = ERROR / OVERFLOW-- latches ON when status[overflow|invalid_op] set;
//                                  cleared by writing 1 to clear_error_i
//
// Clock:  100 MHz from pl_clk0 (Zynq UltraScale+ PS)
// Reset:  Active-low synchronous reset from proc_sys_reset
//
// The 40 ms stretch is implemented with a 22-bit counter at 100 MHz:
//   2^22 / 100e6 = 41.9 ms  -- well above 30 ms persistence-of-vision threshold
// =============================================================================

`timescale 1ns / 1ps

module qgpu_led_controller (
    input  wire        clk,             // 100 MHz
    input  wire        rstn,            // Active-low synchronous reset

    // Signals from parallel_gpu AXI4-Lite AP control register (mirrored)
    input  wire        ap_start,        // Pulsed high for 1 cycle when AP_CTRL[0] written
    input  wire        ap_done,         // Pulsed high for 1 cycle when AP_CTRL[1] asserted
    input  wire        ap_idle,         // AP_CTRL[2] -- accelerator is waiting

    // Status from parallel_gpu status register
    input  wire        status_overflow, // STATUS[2] = overflow occurred
    input  wire        status_err_op,   // STATUS[0] = invalid opcode
    input  wire        clear_error,     // Software writes 1 to clear error latch

    // Physical outputs to Bank 66 pins
    output reg         led0,           // IDLE / READY
    output reg         led1,           // BUSY / AP_START
    output reg         led2,           // DONE / AP_DONE
    output reg         led3            // ERROR / OVERFLOW
);

    // -------------------------------------------------------------------------
    // 40 ms pulse stretcher constants (100 MHz clock)
    // 100e6 * 0.04 = 4_000_000 ticks => use 22-bit counter
    // -------------------------------------------------------------------------
    localparam STRETCH_BITS = 22;
    localparam STRETCH_ZERO = {STRETCH_BITS{1'b0}};

    reg [STRETCH_BITS-1:0] busy_timer;
    reg [STRETCH_BITS-1:0] done_timer;

    // Error latch -- sticky until cleared
    reg error_latch;

    // -------------------------------------------------------------------------
    // LED0: IDLE/READY -- combinatorially driven from ap_idle
    // -------------------------------------------------------------------------
    always @(posedge clk) begin
        if (!rstn)
            led0 <= 1'b0;
        else
            led0 <= ap_idle; // solid when nothing is computing
    end

    // -------------------------------------------------------------------------
    // LED1: BUSY -- stretched pulse on ap_start
    // -------------------------------------------------------------------------
    always @(posedge clk) begin
        if (!rstn) begin
            busy_timer <= STRETCH_ZERO;
            led1 <= 1'b0;
        end else begin
            if (ap_start) begin
                // Reload the 40 ms stretch counter
                busy_timer <= {STRETCH_BITS{1'b1}};
                led1       <= 1'b1;
            end else if (busy_timer != STRETCH_ZERO) begin
                busy_timer <= busy_timer - 1'b1;
                led1       <= 1'b1;
            end else begin
                led1 <= 1'b0;
            end
        end
    end

    // -------------------------------------------------------------------------
    // LED2: DONE -- stretched pulse on ap_done
    // -------------------------------------------------------------------------
    always @(posedge clk) begin
        if (!rstn) begin
            done_timer <= STRETCH_ZERO;
            led2 <= 1'b0;
        end else begin
            if (ap_done) begin
                done_timer <= {STRETCH_BITS{1'b1}};
                led2       <= 1'b1;
            end else if (done_timer != STRETCH_ZERO) begin
                done_timer <= done_timer - 1'b1;
                led2       <= 1'b1;
            end else begin
                led2 <= 1'b0;
            end
        end
    end

    // -------------------------------------------------------------------------
    // LED3: ERROR -- sticky latch cleared by software
    // -------------------------------------------------------------------------
    always @(posedge clk) begin
        if (!rstn) begin
            error_latch <= 1'b0;
            led3        <= 1'b0;
        end else begin
            if (clear_error) begin
                error_latch <= 1'b0;
                led3        <= 1'b0;
            end else if (status_overflow || status_err_op) begin
                error_latch <= 1'b1;
                led3        <= 1'b1;
            end else begin
                led3 <= error_latch;
            end
        end
    end

endmodule
