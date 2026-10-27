// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
// control
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
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL     0x000
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_GIE         0x004
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER         0x008
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_ISR         0x00c
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_0_DATA    0x010
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_0_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_1_DATA    0x018
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_1_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_2_DATA    0x020
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_2_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_3_DATA    0x028
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_3_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_4_DATA    0x030
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_4_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_5_DATA    0x038
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_5_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_6_DATA    0x040
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_6_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_7_DATA    0x048
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_A_7_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_0_DATA    0x050
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_0_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_1_DATA    0x058
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_1_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_2_DATA    0x060
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_2_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_3_DATA    0x068
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_3_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_4_DATA    0x070
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_4_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_5_DATA    0x078
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_5_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_6_DATA    0x080
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_6_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_7_DATA    0x088
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_B_7_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_0_DATA    0x090
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_0_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_0_CTRL    0x094
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_1_DATA    0x0a0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_1_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_1_CTRL    0x0a4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_2_DATA    0x0b0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_2_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_2_CTRL    0x0b4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_3_DATA    0x0c0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_3_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_3_CTRL    0x0c4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_4_DATA    0x0d0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_4_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_4_CTRL    0x0d4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_5_DATA    0x0e0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_5_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_5_CTRL    0x0e4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_6_DATA    0x0f0
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_6_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_6_CTRL    0x0f4
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_7_DATA    0x100
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_C_7_DATA    32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_7_CTRL    0x104
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_OPCODE_DATA 0x110
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_OPCODE_DATA 32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_STATUS_DATA 0x118
#define XQGPU_GA_PARALLEL_TOP_CONTROL_BITS_STATUS_DATA 32
#define XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_STATUS_CTRL 0x11c

