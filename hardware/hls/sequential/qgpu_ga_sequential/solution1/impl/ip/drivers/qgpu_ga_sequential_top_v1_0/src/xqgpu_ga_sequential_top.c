// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
/***************************** Include Files *********************************/
#include "xqgpu_ga_sequential_top.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XQgpu_ga_sequential_top_CfgInitialize(XQgpu_ga_sequential_top *InstancePtr, XQgpu_ga_sequential_top_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XQgpu_ga_sequential_top_Start(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL) & 0x80;
    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XQgpu_ga_sequential_top_IsDone(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XQgpu_ga_sequential_top_IsIdle(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XQgpu_ga_sequential_top_IsReady(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XQgpu_ga_sequential_top_EnableAutoRestart(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XQgpu_ga_sequential_top_DisableAutoRestart(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_AP_CTRL, 0);
}

void XQgpu_ga_sequential_top_Set_opcode(XQgpu_ga_sequential_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_OPCODE_DATA, Data);
}

u32 XQgpu_ga_sequential_top_Get_opcode(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_OPCODE_DATA);
    return Data;
}

void XQgpu_ga_sequential_top_Set_dma_len(XQgpu_ga_sequential_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_DMA_LEN_DATA, Data);
}

u32 XQgpu_ga_sequential_top_Get_dma_len(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_DMA_LEN_DATA);
    return Data;
}

u32 XQgpu_ga_sequential_top_Get_status(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_STATUS_DATA);
    return Data;
}

u32 XQgpu_ga_sequential_top_Get_status_vld(XQgpu_ga_sequential_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_STATUS_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_sequential_top_Get_a_BaseAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE);
}

u32 XQgpu_ga_sequential_top_Get_a_HighAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH);
}

u32 XQgpu_ga_sequential_top_Get_a_TotalBytes(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + 1);
}

u32 XQgpu_ga_sequential_top_Get_a_BitWidth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_A;
}

u32 XQgpu_ga_sequential_top_Get_a_Depth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_A;
}

u32 XQgpu_ga_sequential_top_Write_a_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_a_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + (offset + i)*4);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Write_a_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_a_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_A_BASE + offset + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Get_b_BaseAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE);
}

u32 XQgpu_ga_sequential_top_Get_b_HighAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH);
}

u32 XQgpu_ga_sequential_top_Get_b_TotalBytes(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + 1);
}

u32 XQgpu_ga_sequential_top_Get_b_BitWidth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_B;
}

u32 XQgpu_ga_sequential_top_Get_b_Depth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_B;
}

u32 XQgpu_ga_sequential_top_Write_b_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_b_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + (offset + i)*4);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Write_b_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_b_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_B_BASE + offset + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Get_c_BaseAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE);
}

u32 XQgpu_ga_sequential_top_Get_c_HighAddress(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH);
}

u32 XQgpu_ga_sequential_top_Get_c_TotalBytes(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + 1);
}

u32 XQgpu_ga_sequential_top_Get_c_BitWidth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_WIDTH_C;
}

u32 XQgpu_ga_sequential_top_Get_c_Depth(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQGPU_GA_SEQUENTIAL_TOP_CONTROL_DEPTH_C;
}

u32 XQgpu_ga_sequential_top_Write_c_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_c_Words(XQgpu_ga_sequential_top *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + (offset + i)*4);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Write_c_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XQgpu_ga_sequential_top_Read_c_Bytes(XQgpu_ga_sequential_top *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_HIGH - XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_C_BASE + offset + i);
    }
    return length;
}

void XQgpu_ga_sequential_top_InterruptGlobalEnable(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_GIE, 1);
}

void XQgpu_ga_sequential_top_InterruptGlobalDisable(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_GIE, 0);
}

void XQgpu_ga_sequential_top_InterruptEnable(XQgpu_ga_sequential_top *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER);
    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER, Register | Mask);
}

void XQgpu_ga_sequential_top_InterruptDisable(XQgpu_ga_sequential_top *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER);
    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER, Register & (~Mask));
}

void XQgpu_ga_sequential_top_InterruptClear(XQgpu_ga_sequential_top *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_sequential_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_ISR, Mask);
}

u32 XQgpu_ga_sequential_top_InterruptGetEnabled(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_IER);
}

u32 XQgpu_ga_sequential_top_InterruptGetStatus(XQgpu_ga_sequential_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQgpu_ga_sequential_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_SEQUENTIAL_TOP_CONTROL_ADDR_ISR);
}

