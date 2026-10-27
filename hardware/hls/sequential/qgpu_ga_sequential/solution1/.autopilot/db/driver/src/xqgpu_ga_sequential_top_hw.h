// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
// control
// 0x00 : Control signals
//        bit 0  - ap_start (Read/Write/COH)
//        bit 1  - ap_done (Read/COR)
//        bit 2  - ap_idle (Read)
//        bit 3  - ap_ready (Read/COR)
//        bit 7  - auto_restart (Read/Write)
//        bit 9  - interrupt (Read)
//        others - reserved
// 0x04 : Global Interrupt Enable Register
//        bit 0  - Global Interrupt Enable (Read/Write)
//        others - reserved
// 0x08 : IP Interrupt Enable Register (Read/Write)
//        bit 0 - enable ap_done interrupt (Read/Write)
//        bit 1 - enable ap_ready interrupt (Read/Write)
//        others - reserved
// 0x0c : IP Interrupt Status Register (Read/TOW)
//        bit 0 - ap_done (Read/TOW)
//        bit 1 - ap_ready (Read/TOW)
//        others - reserved
// 0x10 : Data signal of opcode
//        bit 31~0 - opcode[31:0] (Read/Write)
// 0x14 : reserved
// 0x80 : Data signal of status
//        bit 31~0 - status[31:0] (Read)
// 0x84 : Control signal of status
//        bit 0  - status_ap_vld (Read/COR)
//        others - reserved
// 0x20 ~
// 0x3f : Memory 'a' (8 * 32b)
//        Word n : bit [31:0] - a[n]
// 0x40 ~
// 0x5f : Memory 'b' (8 * 32b)
//        Word n : bit [31:0] - b[n]
// 0x60 ~
// 0x7f : Memory 'c' (8 * 32b)
//        Word n : bit [31:0] - c[n]
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL     0x00
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_GIE         0x04
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER         0x08
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_ISR         0x0c
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_OPCODE_DATA 0x10
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_BITS_OPCODE_DATA 32
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_STATUS_DATA 0x80
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_BITS_STATUS_DATA 32
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_STATUS_CTRL 0x84
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE      0x20
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH      0x3f
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_A          32
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_A          8
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE      0x40
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH      0x5f
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_B          32
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_B          8
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE      0x60
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH      0x7f
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_C          32
#define XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_C          8

