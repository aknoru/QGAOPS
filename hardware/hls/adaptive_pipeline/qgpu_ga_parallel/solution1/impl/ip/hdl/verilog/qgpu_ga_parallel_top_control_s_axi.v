// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
`timescale 1ns/1ps
(* DowngradeIPIdentifiedWarnings="yes" *) module qgpu_ga_parallel_top_control_s_axi
#(parameter
    C_S_AXI_ADDR_WIDTH = 9,
    C_S_AXI_DATA_WIDTH = 32
)(
    input  wire                          ACLK,
    input  wire                          ARESET,
    input  wire                          ACLK_EN,
    input  wire [C_S_AXI_ADDR_WIDTH-1:0] AWADDR,
    input  wire                          AWVALID,
    output wire                          AWREADY,
    input  wire [C_S_AXI_DATA_WIDTH-1:0] WDATA,
    input  wire [C_S_AXI_DATA_WIDTH/8-1:0] WSTRB,
    input  wire                          WVALID,
    output wire                          WREADY,
    output wire [1:0]                    BRESP,
    output wire                          BVALID,
    input  wire                          BREADY,
    input  wire [C_S_AXI_ADDR_WIDTH-1:0] ARADDR,
    input  wire                          ARVALID,
    output wire                          ARREADY,
    output wire [C_S_AXI_DATA_WIDTH-1:0] RDATA,
    output wire [1:0]                    RRESP,
    output wire                          RVALID,
    input  wire                          RREADY,
    output wire                          interrupt,
    output wire [31:0]                   a_0,
    output wire [31:0]                   a_1,
    output wire [31:0]                   a_2,
    output wire [31:0]                   a_3,
    output wire [31:0]                   a_4,
    output wire [31:0]                   a_5,
    output wire [31:0]                   a_6,
    output wire [31:0]                   a_7,
    output wire [31:0]                   b_0,
    output wire [31:0]                   b_1,
    output wire [31:0]                   b_2,
    output wire [31:0]                   b_3,
    output wire [31:0]                   b_4,
    output wire [31:0]                   b_5,
    output wire [31:0]                   b_6,
    output wire [31:0]                   b_7,
    input  wire [31:0]                   c_0,
    input  wire                          c_0_ap_vld,
    input  wire [31:0]                   c_1,
    input  wire                          c_1_ap_vld,
    input  wire [31:0]                   c_2,
    input  wire                          c_2_ap_vld,
    input  wire [31:0]                   c_3,
    input  wire                          c_3_ap_vld,
    input  wire [31:0]                   c_4,
    input  wire                          c_4_ap_vld,
    input  wire [31:0]                   c_5,
    input  wire                          c_5_ap_vld,
    input  wire [31:0]                   c_6,
    input  wire                          c_6_ap_vld,
    input  wire [31:0]                   c_7,
    input  wire                          c_7_ap_vld,
    output wire [31:0]                   opcode,
    input  wire [31:0]                   status,
    input  wire                          status_ap_vld,
    output wire [31:0]                   dma_len,
    output wire                          ap_start,
    input  wire                          ap_done,
    input  wire                          ap_ready,
    input  wire                          ap_idle
);
//------------------------Address Info-------------------
// Protocol Used: ap_ctrl_hs
//
// 0x000 : Control signals
//         bit 0  - ap_start (Read/Write/COH)
//         bit 1  - ap_done (Read/COR)
//         bit 2  - ap_idle (Read)
//         bit 3  - ap_ready (Read/COR)
//         bit 7  - auto_restart (Read/Write)
//         bit 9  - interrupt (Read)
//         others - reserved
// 0x004 : Global Interrupt Enable Register
//         bit 0  - Global Interrupt Enable (Read/Write)
//         others - reserved
// 0x008 : IP Interrupt Enable Register (Read/Write)
//         bit 0 - enable ap_done interrupt (Read/Write)
//         bit 1 - enable ap_ready interrupt (Read/Write)
//         others - reserved
// 0x00c : IP Interrupt Status Register (Read/TOW)
//         bit 0 - ap_done (Read/TOW)
//         bit 1 - ap_ready (Read/TOW)
//         others - reserved
// 0x010 : Data signal of a_0
//         bit 31~0 - a_0[31:0] (Read/Write)
// 0x014 : reserved
// 0x018 : Data signal of a_1
//         bit 31~0 - a_1[31:0] (Read/Write)
// 0x01c : reserved
// 0x020 : Data signal of a_2
//         bit 31~0 - a_2[31:0] (Read/Write)
// 0x024 : reserved
// 0x028 : Data signal of a_3
//         bit 31~0 - a_3[31:0] (Read/Write)
// 0x02c : reserved
// 0x030 : Data signal of a_4
//         bit 31~0 - a_4[31:0] (Read/Write)
// 0x034 : reserved
// 0x038 : Data signal of a_5
//         bit 31~0 - a_5[31:0] (Read/Write)
// 0x03c : reserved
// 0x040 : Data signal of a_6
//         bit 31~0 - a_6[31:0] (Read/Write)
// 0x044 : reserved
// 0x048 : Data signal of a_7
//         bit 31~0 - a_7[31:0] (Read/Write)
// 0x04c : reserved
// 0x050 : Data signal of b_0
//         bit 31~0 - b_0[31:0] (Read/Write)
// 0x054 : reserved
// 0x058 : Data signal of b_1
//         bit 31~0 - b_1[31:0] (Read/Write)
// 0x05c : reserved
// 0x060 : Data signal of b_2
//         bit 31~0 - b_2[31:0] (Read/Write)
// 0x064 : reserved
// 0x068 : Data signal of b_3
//         bit 31~0 - b_3[31:0] (Read/Write)
// 0x06c : reserved
// 0x070 : Data signal of b_4
//         bit 31~0 - b_4[31:0] (Read/Write)
// 0x074 : reserved
// 0x078 : Data signal of b_5
//         bit 31~0 - b_5[31:0] (Read/Write)
// 0x07c : reserved
// 0x080 : Data signal of b_6
//         bit 31~0 - b_6[31:0] (Read/Write)
// 0x084 : reserved
// 0x088 : Data signal of b_7
//         bit 31~0 - b_7[31:0] (Read/Write)
// 0x08c : reserved
// 0x090 : Data signal of c_0
//         bit 31~0 - c_0[31:0] (Read)
// 0x094 : Control signal of c_0
//         bit 0  - c_0_ap_vld (Read/COR)
//         others - reserved
// 0x0a0 : Data signal of c_1
//         bit 31~0 - c_1[31:0] (Read)
// 0x0a4 : Control signal of c_1
//         bit 0  - c_1_ap_vld (Read/COR)
//         others - reserved
// 0x0b0 : Data signal of c_2
//         bit 31~0 - c_2[31:0] (Read)
// 0x0b4 : Control signal of c_2
//         bit 0  - c_2_ap_vld (Read/COR)
//         others - reserved
// 0x0c0 : Data signal of c_3
//         bit 31~0 - c_3[31:0] (Read)
// 0x0c4 : Control signal of c_3
//         bit 0  - c_3_ap_vld (Read/COR)
//         others - reserved
// 0x0d0 : Data signal of c_4
//         bit 31~0 - c_4[31:0] (Read)
// 0x0d4 : Control signal of c_4
//         bit 0  - c_4_ap_vld (Read/COR)
//         others - reserved
// 0x0e0 : Data signal of c_5
//         bit 31~0 - c_5[31:0] (Read)
// 0x0e4 : Control signal of c_5
//         bit 0  - c_5_ap_vld (Read/COR)
//         others - reserved
// 0x0f0 : Data signal of c_6
//         bit 31~0 - c_6[31:0] (Read)
// 0x0f4 : Control signal of c_6
//         bit 0  - c_6_ap_vld (Read/COR)
//         others - reserved
// 0x100 : Data signal of c_7
//         bit 31~0 - c_7[31:0] (Read)
// 0x104 : Control signal of c_7
//         bit 0  - c_7_ap_vld (Read/COR)
//         others - reserved
// 0x110 : Data signal of opcode
//         bit 31~0 - opcode[31:0] (Read/Write)
// 0x114 : reserved
// 0x118 : Data signal of status
//         bit 31~0 - status[31:0] (Read)
// 0x11c : Control signal of status
//         bit 0  - status_ap_vld (Read/COR)
//         others - reserved
// 0x128 : Data signal of dma_len
//         bit 31~0 - dma_len[31:0] (Read/Write)
// 0x12c : reserved
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

//------------------------Parameter----------------------
localparam
    ADDR_AP_CTRL        = 9'h000,
    ADDR_GIE            = 9'h004,
    ADDR_IER            = 9'h008,
    ADDR_ISR            = 9'h00c,
    ADDR_A_0_DATA_0     = 9'h010,
    ADDR_A_0_CTRL       = 9'h014,
    ADDR_A_1_DATA_0     = 9'h018,
    ADDR_A_1_CTRL       = 9'h01c,
    ADDR_A_2_DATA_0     = 9'h020,
    ADDR_A_2_CTRL       = 9'h024,
    ADDR_A_3_DATA_0     = 9'h028,
    ADDR_A_3_CTRL       = 9'h02c,
    ADDR_A_4_DATA_0     = 9'h030,
    ADDR_A_4_CTRL       = 9'h034,
    ADDR_A_5_DATA_0     = 9'h038,
    ADDR_A_5_CTRL       = 9'h03c,
    ADDR_A_6_DATA_0     = 9'h040,
    ADDR_A_6_CTRL       = 9'h044,
    ADDR_A_7_DATA_0     = 9'h048,
    ADDR_A_7_CTRL       = 9'h04c,
    ADDR_B_0_DATA_0     = 9'h050,
    ADDR_B_0_CTRL       = 9'h054,
    ADDR_B_1_DATA_0     = 9'h058,
    ADDR_B_1_CTRL       = 9'h05c,
    ADDR_B_2_DATA_0     = 9'h060,
    ADDR_B_2_CTRL       = 9'h064,
    ADDR_B_3_DATA_0     = 9'h068,
    ADDR_B_3_CTRL       = 9'h06c,
    ADDR_B_4_DATA_0     = 9'h070,
    ADDR_B_4_CTRL       = 9'h074,
    ADDR_B_5_DATA_0     = 9'h078,
    ADDR_B_5_CTRL       = 9'h07c,
    ADDR_B_6_DATA_0     = 9'h080,
    ADDR_B_6_CTRL       = 9'h084,
    ADDR_B_7_DATA_0     = 9'h088,
    ADDR_B_7_CTRL       = 9'h08c,
    ADDR_C_0_DATA_0     = 9'h090,
    ADDR_C_0_CTRL       = 9'h094,
    ADDR_C_1_DATA_0     = 9'h0a0,
    ADDR_C_1_CTRL       = 9'h0a4,
    ADDR_C_2_DATA_0     = 9'h0b0,
    ADDR_C_2_CTRL       = 9'h0b4,
    ADDR_C_3_DATA_0     = 9'h0c0,
    ADDR_C_3_CTRL       = 9'h0c4,
    ADDR_C_4_DATA_0     = 9'h0d0,
    ADDR_C_4_CTRL       = 9'h0d4,
    ADDR_C_5_DATA_0     = 9'h0e0,
    ADDR_C_5_CTRL       = 9'h0e4,
    ADDR_C_6_DATA_0     = 9'h0f0,
    ADDR_C_6_CTRL       = 9'h0f4,
    ADDR_C_7_DATA_0     = 9'h100,
    ADDR_C_7_CTRL       = 9'h104,
    ADDR_OPCODE_DATA_0  = 9'h110,
    ADDR_OPCODE_CTRL    = 9'h114,
    ADDR_STATUS_DATA_0  = 9'h118,
    ADDR_STATUS_CTRL    = 9'h11c,
    ADDR_DMA_LEN_DATA_0 = 9'h128,
    ADDR_DMA_LEN_CTRL   = 9'h12c,
    WRIDLE              = 2'd0,
    WRDATA              = 2'd1,
    WRRESP              = 2'd2,
    WRRESET             = 2'd3,
    RDIDLE              = 2'd0,
    RDDATA              = 2'd1,
    RDRESET             = 2'd2,
    ADDR_BITS                = 9;

//------------------------Local signal-------------------
    reg  [1:0]                    wstate = WRRESET;
    reg  [1:0]                    wnext;
    reg  [ADDR_BITS-1:0]          waddr;
    wire [C_S_AXI_DATA_WIDTH-1:0] wmask;
    wire                          aw_hs;
    wire                          w_hs;
    reg  [1:0]                    rstate = RDRESET;
    reg  [1:0]                    rnext;
    reg  [C_S_AXI_DATA_WIDTH-1:0] rdata;
    wire                          ar_hs;
    wire [ADDR_BITS-1:0]          raddr;
    // internal registers
    reg                           int_ap_idle = 1'b0;
    reg                           int_ap_ready = 1'b0;
    wire                          task_ap_ready;
    reg                           int_ap_done = 1'b0;
    wire                          task_ap_done;
    reg                           int_task_ap_done = 1'b0;
    reg                           int_ap_start = 1'b0;
    reg                           int_interrupt = 1'b0;
    reg                           int_auto_restart = 1'b0;
    reg                           auto_restart_status = 1'b0;
    wire                          auto_restart_done;
    reg                           int_gie = 1'b0;
    reg  [1:0]                    int_ier = 2'b0;
    reg  [1:0]                    int_isr = 2'b0;
    reg  [31:0]                   int_a_0 = 'b0;
    reg  [31:0]                   int_a_1 = 'b0;
    reg  [31:0]                   int_a_2 = 'b0;
    reg  [31:0]                   int_a_3 = 'b0;
    reg  [31:0]                   int_a_4 = 'b0;
    reg  [31:0]                   int_a_5 = 'b0;
    reg  [31:0]                   int_a_6 = 'b0;
    reg  [31:0]                   int_a_7 = 'b0;
    reg  [31:0]                   int_b_0 = 'b0;
    reg  [31:0]                   int_b_1 = 'b0;
    reg  [31:0]                   int_b_2 = 'b0;
    reg  [31:0]                   int_b_3 = 'b0;
    reg  [31:0]                   int_b_4 = 'b0;
    reg  [31:0]                   int_b_5 = 'b0;
    reg  [31:0]                   int_b_6 = 'b0;
    reg  [31:0]                   int_b_7 = 'b0;
    reg                           int_c_0_ap_vld;
    reg  [31:0]                   int_c_0 = 'b0;
    reg                           int_c_1_ap_vld;
    reg  [31:0]                   int_c_1 = 'b0;
    reg                           int_c_2_ap_vld;
    reg  [31:0]                   int_c_2 = 'b0;
    reg                           int_c_3_ap_vld;
    reg  [31:0]                   int_c_3 = 'b0;
    reg                           int_c_4_ap_vld;
    reg  [31:0]                   int_c_4 = 'b0;
    reg                           int_c_5_ap_vld;
    reg  [31:0]                   int_c_5 = 'b0;
    reg                           int_c_6_ap_vld;
    reg  [31:0]                   int_c_6 = 'b0;
    reg                           int_c_7_ap_vld;
    reg  [31:0]                   int_c_7 = 'b0;
    reg  [31:0]                   int_opcode = 'b0;
    reg                           int_status_ap_vld;
    reg  [31:0]                   int_status = 'b0;
    reg  [31:0]                   int_dma_len = 'b0;

//------------------------Instantiation------------------


//------------------------AXI write fsm------------------
assign AWREADY = (wstate == WRIDLE);
assign WREADY  = (wstate == WRDATA);
assign BVALID  = (wstate == WRRESP);
assign BRESP   = 2'b00;  // OKAY
assign wmask   = { {8{WSTRB[3]}}, {8{WSTRB[2]}}, {8{WSTRB[1]}}, {8{WSTRB[0]}} };
assign aw_hs   = AWVALID & AWREADY;
assign w_hs    = WVALID & WREADY;

// wstate
always @(posedge ACLK) begin
    if (ARESET)
        wstate <= WRRESET;
    else if (ACLK_EN)
        wstate <= wnext;
end

// wnext
always @(*) begin
    case (wstate)
        WRIDLE:
            if (AWVALID)
                wnext = WRDATA;
            else
                wnext = WRIDLE;
        WRDATA:
            if (WVALID)
                wnext = WRRESP;
            else
                wnext = WRDATA;
        WRRESP:
            if (BREADY & BVALID)
                wnext = WRIDLE;
            else
                wnext = WRRESP;
        default:
            wnext = WRIDLE;
    endcase
end

// waddr
always @(posedge ACLK) begin
    if (ACLK_EN) begin
        if (aw_hs)
            waddr <= {AWADDR[ADDR_BITS-1:2], {2{1'b0}}};
    end
end

//------------------------AXI read fsm-------------------
assign ARREADY = (rstate == RDIDLE);
assign RDATA   = rdata;
assign RRESP   = 2'b00;  // OKAY
assign RVALID  = (rstate == RDDATA);
assign ar_hs   = ARVALID & ARREADY;
assign raddr   = ARADDR[ADDR_BITS-1:0];

// rstate
always @(posedge ACLK) begin
    if (ARESET)
        rstate <= RDRESET;
    else if (ACLK_EN)
        rstate <= rnext;
end

// rnext
always @(*) begin
    case (rstate)
        RDIDLE:
            if (ARVALID)
                rnext = RDDATA;
            else
                rnext = RDIDLE;
        RDDATA:
            if (RREADY & RVALID)
                rnext = RDIDLE;
            else
                rnext = RDDATA;
        default:
            rnext = RDIDLE;
    endcase
end

// rdata
always @(posedge ACLK) begin
    if (ACLK_EN) begin
        if (ar_hs) begin
            rdata <= 'b0;
            case (raddr)
                ADDR_AP_CTRL: begin
                    rdata[0] <= int_ap_start;
                    rdata[1] <= int_task_ap_done;
                    rdata[2] <= int_ap_idle;
                    rdata[3] <= int_ap_ready;
                    rdata[7] <= int_auto_restart;
                    rdata[9] <= int_interrupt;
                end
                ADDR_GIE: begin
                    rdata <= int_gie;
                end
                ADDR_IER: begin
                    rdata <= int_ier;
                end
                ADDR_ISR: begin
                    rdata <= int_isr;
                end
                ADDR_A_0_DATA_0: begin
                    rdata <= int_a_0[31:0];
                end
                ADDR_A_1_DATA_0: begin
                    rdata <= int_a_1[31:0];
                end
                ADDR_A_2_DATA_0: begin
                    rdata <= int_a_2[31:0];
                end
                ADDR_A_3_DATA_0: begin
                    rdata <= int_a_3[31:0];
                end
                ADDR_A_4_DATA_0: begin
                    rdata <= int_a_4[31:0];
                end
                ADDR_A_5_DATA_0: begin
                    rdata <= int_a_5[31:0];
                end
                ADDR_A_6_DATA_0: begin
                    rdata <= int_a_6[31:0];
                end
                ADDR_A_7_DATA_0: begin
                    rdata <= int_a_7[31:0];
                end
                ADDR_B_0_DATA_0: begin
                    rdata <= int_b_0[31:0];
                end
                ADDR_B_1_DATA_0: begin
                    rdata <= int_b_1[31:0];
                end
                ADDR_B_2_DATA_0: begin
                    rdata <= int_b_2[31:0];
                end
                ADDR_B_3_DATA_0: begin
                    rdata <= int_b_3[31:0];
                end
                ADDR_B_4_DATA_0: begin
                    rdata <= int_b_4[31:0];
                end
                ADDR_B_5_DATA_0: begin
                    rdata <= int_b_5[31:0];
                end
                ADDR_B_6_DATA_0: begin
                    rdata <= int_b_6[31:0];
                end
                ADDR_B_7_DATA_0: begin
                    rdata <= int_b_7[31:0];
                end
                ADDR_C_0_DATA_0: begin
                    rdata <= int_c_0[31:0];
                end
                ADDR_C_0_CTRL: begin
                    rdata[0] <= int_c_0_ap_vld;
                end
                ADDR_C_1_DATA_0: begin
                    rdata <= int_c_1[31:0];
                end
                ADDR_C_1_CTRL: begin
                    rdata[0] <= int_c_1_ap_vld;
                end
                ADDR_C_2_DATA_0: begin
                    rdata <= int_c_2[31:0];
                end
                ADDR_C_2_CTRL: begin
                    rdata[0] <= int_c_2_ap_vld;
                end
                ADDR_C_3_DATA_0: begin
                    rdata <= int_c_3[31:0];
                end
                ADDR_C_3_CTRL: begin
                    rdata[0] <= int_c_3_ap_vld;
                end
                ADDR_C_4_DATA_0: begin
                    rdata <= int_c_4[31:0];
                end
                ADDR_C_4_CTRL: begin
                    rdata[0] <= int_c_4_ap_vld;
                end
                ADDR_C_5_DATA_0: begin
                    rdata <= int_c_5[31:0];
                end
                ADDR_C_5_CTRL: begin
                    rdata[0] <= int_c_5_ap_vld;
                end
                ADDR_C_6_DATA_0: begin
                    rdata <= int_c_6[31:0];
                end
                ADDR_C_6_CTRL: begin
                    rdata[0] <= int_c_6_ap_vld;
                end
                ADDR_C_7_DATA_0: begin
                    rdata <= int_c_7[31:0];
                end
                ADDR_C_7_CTRL: begin
                    rdata[0] <= int_c_7_ap_vld;
                end
                ADDR_OPCODE_DATA_0: begin
                    rdata <= int_opcode[31:0];
                end
                ADDR_STATUS_DATA_0: begin
                    rdata <= int_status[31:0];
                end
                ADDR_STATUS_CTRL: begin
                    rdata[0] <= int_status_ap_vld;
                end
                ADDR_DMA_LEN_DATA_0: begin
                    rdata <= int_dma_len[31:0];
                end
            endcase
        end
    end
end


//------------------------Register logic-----------------
assign interrupt         = int_interrupt;
assign ap_start          = int_ap_start;
assign task_ap_done      = (ap_done && !auto_restart_status) || auto_restart_done;
assign task_ap_ready     = ap_ready && !int_auto_restart;
assign auto_restart_done = auto_restart_status && (ap_idle && !int_ap_idle);
assign a_0               = int_a_0;
assign a_1               = int_a_1;
assign a_2               = int_a_2;
assign a_3               = int_a_3;
assign a_4               = int_a_4;
assign a_5               = int_a_5;
assign a_6               = int_a_6;
assign a_7               = int_a_7;
assign b_0               = int_b_0;
assign b_1               = int_b_1;
assign b_2               = int_b_2;
assign b_3               = int_b_3;
assign b_4               = int_b_4;
assign b_5               = int_b_5;
assign b_6               = int_b_6;
assign b_7               = int_b_7;
assign opcode            = int_opcode;
assign dma_len           = int_dma_len;
// int_interrupt
always @(posedge ACLK) begin
    if (ARESET)
        int_interrupt <= 1'b0;
    else if (ACLK_EN) begin
        if (int_gie && (|int_isr))
            int_interrupt <= 1'b1;
        else
            int_interrupt <= 1'b0;
    end
end

// int_ap_start
always @(posedge ACLK) begin
    if (ARESET)
        int_ap_start <= 1'b0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_AP_CTRL && WSTRB[0] && WDATA[0])
            int_ap_start <= 1'b1;
        else if (ap_ready)
            int_ap_start <= int_auto_restart; // clear on handshake/auto restart
    end
end

// int_ap_done
always @(posedge ACLK) begin
    if (ARESET)
        int_ap_done <= 1'b0;
    else if (ACLK_EN) begin
            int_ap_done <= ap_done;
    end
end

// int_task_ap_done
always @(posedge ACLK) begin
    if (ARESET)
        int_task_ap_done <= 1'b0;
    else if (ACLK_EN) begin
        if (task_ap_done)
            int_task_ap_done <= 1'b1;
        else if (ar_hs && raddr == ADDR_AP_CTRL)
            int_task_ap_done <= 1'b0; // clear on read
    end
end

// int_ap_idle
always @(posedge ACLK) begin
    if (ARESET)
        int_ap_idle <= 1'b0;
    else if (ACLK_EN) begin
            int_ap_idle <= ap_idle;
    end
end

// int_ap_ready
always @(posedge ACLK) begin
    if (ARESET)
        int_ap_ready <= 1'b0;
    else if (ACLK_EN) begin
        if (task_ap_ready)
            int_ap_ready <= 1'b1;
        else if (ar_hs && raddr == ADDR_AP_CTRL)
            int_ap_ready <= 1'b0;
    end
end

// int_auto_restart
always @(posedge ACLK) begin
    if (ARESET)
        int_auto_restart <= 1'b0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_AP_CTRL && WSTRB[0])
            int_auto_restart <= WDATA[7];
    end
end

// auto_restart_status
always @(posedge ACLK) begin
    if (ARESET)
        auto_restart_status <= 1'b0;
    else if (ACLK_EN) begin
        if (int_auto_restart)
            auto_restart_status <= 1'b1;
        else if (ap_idle)
            auto_restart_status <= 1'b0;
    end
end

// int_gie
always @(posedge ACLK) begin
    if (ARESET)
        int_gie <= 1'b0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_GIE && WSTRB[0])
            int_gie <= WDATA[0];
    end
end

// int_ier
always @(posedge ACLK) begin
    if (ARESET)
        int_ier <= 1'b0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_IER && WSTRB[0])
            int_ier <= WDATA[1:0];
    end
end

// int_isr[0]
always @(posedge ACLK) begin
    if (ARESET)
        int_isr[0] <= 1'b0;
    else if (ACLK_EN) begin
        if (int_ier[0] & ap_done)
            int_isr[0] <= 1'b1;
        else if (w_hs && waddr == ADDR_ISR && WSTRB[0])
            int_isr[0] <= int_isr[0] ^ WDATA[0]; // toggle on write
    end
end

// int_isr[1]
always @(posedge ACLK) begin
    if (ARESET)
        int_isr[1] <= 1'b0;
    else if (ACLK_EN) begin
        if (int_ier[1] & ap_ready)
            int_isr[1] <= 1'b1;
        else if (w_hs && waddr == ADDR_ISR && WSTRB[0])
            int_isr[1] <= int_isr[1] ^ WDATA[1]; // toggle on write
    end
end

// int_a_0[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_0[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_0_DATA_0)
            int_a_0[31:0] <= (WDATA[31:0] & wmask) | (int_a_0[31:0] & ~wmask);
    end
end

// int_a_1[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_1[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_1_DATA_0)
            int_a_1[31:0] <= (WDATA[31:0] & wmask) | (int_a_1[31:0] & ~wmask);
    end
end

// int_a_2[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_2[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_2_DATA_0)
            int_a_2[31:0] <= (WDATA[31:0] & wmask) | (int_a_2[31:0] & ~wmask);
    end
end

// int_a_3[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_3[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_3_DATA_0)
            int_a_3[31:0] <= (WDATA[31:0] & wmask) | (int_a_3[31:0] & ~wmask);
    end
end

// int_a_4[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_4[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_4_DATA_0)
            int_a_4[31:0] <= (WDATA[31:0] & wmask) | (int_a_4[31:0] & ~wmask);
    end
end

// int_a_5[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_5[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_5_DATA_0)
            int_a_5[31:0] <= (WDATA[31:0] & wmask) | (int_a_5[31:0] & ~wmask);
    end
end

// int_a_6[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_6[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_6_DATA_0)
            int_a_6[31:0] <= (WDATA[31:0] & wmask) | (int_a_6[31:0] & ~wmask);
    end
end

// int_a_7[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_a_7[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_A_7_DATA_0)
            int_a_7[31:0] <= (WDATA[31:0] & wmask) | (int_a_7[31:0] & ~wmask);
    end
end

// int_b_0[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_0[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_0_DATA_0)
            int_b_0[31:0] <= (WDATA[31:0] & wmask) | (int_b_0[31:0] & ~wmask);
    end
end

// int_b_1[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_1[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_1_DATA_0)
            int_b_1[31:0] <= (WDATA[31:0] & wmask) | (int_b_1[31:0] & ~wmask);
    end
end

// int_b_2[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_2[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_2_DATA_0)
            int_b_2[31:0] <= (WDATA[31:0] & wmask) | (int_b_2[31:0] & ~wmask);
    end
end

// int_b_3[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_3[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_3_DATA_0)
            int_b_3[31:0] <= (WDATA[31:0] & wmask) | (int_b_3[31:0] & ~wmask);
    end
end

// int_b_4[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_4[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_4_DATA_0)
            int_b_4[31:0] <= (WDATA[31:0] & wmask) | (int_b_4[31:0] & ~wmask);
    end
end

// int_b_5[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_5[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_5_DATA_0)
            int_b_5[31:0] <= (WDATA[31:0] & wmask) | (int_b_5[31:0] & ~wmask);
    end
end

// int_b_6[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_6[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_6_DATA_0)
            int_b_6[31:0] <= (WDATA[31:0] & wmask) | (int_b_6[31:0] & ~wmask);
    end
end

// int_b_7[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_b_7[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_B_7_DATA_0)
            int_b_7[31:0] <= (WDATA[31:0] & wmask) | (int_b_7[31:0] & ~wmask);
    end
end

// int_c_0
always @(posedge ACLK) begin
    if (ARESET)
        int_c_0 <= 0;
    else if (ACLK_EN) begin
        if (c_0_ap_vld)
            int_c_0 <= c_0;
    end
end

// int_c_0_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_0_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_0_ap_vld)
            int_c_0_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_0_CTRL)
            int_c_0_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_1
always @(posedge ACLK) begin
    if (ARESET)
        int_c_1 <= 0;
    else if (ACLK_EN) begin
        if (c_1_ap_vld)
            int_c_1 <= c_1;
    end
end

// int_c_1_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_1_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_1_ap_vld)
            int_c_1_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_1_CTRL)
            int_c_1_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_2
always @(posedge ACLK) begin
    if (ARESET)
        int_c_2 <= 0;
    else if (ACLK_EN) begin
        if (c_2_ap_vld)
            int_c_2 <= c_2;
    end
end

// int_c_2_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_2_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_2_ap_vld)
            int_c_2_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_2_CTRL)
            int_c_2_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_3
always @(posedge ACLK) begin
    if (ARESET)
        int_c_3 <= 0;
    else if (ACLK_EN) begin
        if (c_3_ap_vld)
            int_c_3 <= c_3;
    end
end

// int_c_3_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_3_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_3_ap_vld)
            int_c_3_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_3_CTRL)
            int_c_3_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_4
always @(posedge ACLK) begin
    if (ARESET)
        int_c_4 <= 0;
    else if (ACLK_EN) begin
        if (c_4_ap_vld)
            int_c_4 <= c_4;
    end
end

// int_c_4_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_4_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_4_ap_vld)
            int_c_4_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_4_CTRL)
            int_c_4_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_5
always @(posedge ACLK) begin
    if (ARESET)
        int_c_5 <= 0;
    else if (ACLK_EN) begin
        if (c_5_ap_vld)
            int_c_5 <= c_5;
    end
end

// int_c_5_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_5_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_5_ap_vld)
            int_c_5_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_5_CTRL)
            int_c_5_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_6
always @(posedge ACLK) begin
    if (ARESET)
        int_c_6 <= 0;
    else if (ACLK_EN) begin
        if (c_6_ap_vld)
            int_c_6 <= c_6;
    end
end

// int_c_6_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_6_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_6_ap_vld)
            int_c_6_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_6_CTRL)
            int_c_6_ap_vld <= 1'b0; // clear on read
    end
end

// int_c_7
always @(posedge ACLK) begin
    if (ARESET)
        int_c_7 <= 0;
    else if (ACLK_EN) begin
        if (c_7_ap_vld)
            int_c_7 <= c_7;
    end
end

// int_c_7_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_c_7_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (c_7_ap_vld)
            int_c_7_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_C_7_CTRL)
            int_c_7_ap_vld <= 1'b0; // clear on read
    end
end

// int_opcode[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_opcode[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_OPCODE_DATA_0)
            int_opcode[31:0] <= (WDATA[31:0] & wmask) | (int_opcode[31:0] & ~wmask);
    end
end

// int_status
always @(posedge ACLK) begin
    if (ARESET)
        int_status <= 0;
    else if (ACLK_EN) begin
        if (status_ap_vld)
            int_status <= status;
    end
end

// int_status_ap_vld
always @(posedge ACLK) begin
    if (ARESET)
        int_status_ap_vld <= 1'b0;
    else if (ACLK_EN) begin
        if (status_ap_vld)
            int_status_ap_vld <= 1'b1;
        else if (ar_hs && raddr == ADDR_STATUS_CTRL)
            int_status_ap_vld <= 1'b0; // clear on read
    end
end

// int_dma_len[31:0]
always @(posedge ACLK) begin
    if (ARESET)
        int_dma_len[31:0] <= 0;
    else if (ACLK_EN) begin
        if (w_hs && waddr == ADDR_DMA_LEN_DATA_0)
            int_dma_len[31:0] <= (WDATA[31:0] & wmask) | (int_dma_len[31:0] & ~wmask);
    end
end

//synthesis translate_off
always @(posedge ACLK) begin
    if (ACLK_EN) begin
        if (int_gie & ~int_isr[0] & int_ier[0] & ap_done)
            $display ("// Interrupt Monitor : interrupt for ap_done detected @ \"%0t\"", $time);
        if (int_gie & ~int_isr[1] & int_ier[1] & ap_ready)
            $display ("// Interrupt Monitor : interrupt for ap_ready detected @ \"%0t\"", $time);
    end
end
//synthesis translate_on

//------------------------Memory logic-------------------

endmodule
