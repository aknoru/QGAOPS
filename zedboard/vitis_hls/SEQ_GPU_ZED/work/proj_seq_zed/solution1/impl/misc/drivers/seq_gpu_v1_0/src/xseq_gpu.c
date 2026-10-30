// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
/***************************** Include Files *********************************/
#include "xseq_gpu.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XSeq_gpu_CfgInitialize(XSeq_gpu *InstancePtr, XSeq_gpu_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XSeq_gpu_Start(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL) & 0x80;
    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XSeq_gpu_IsDone(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XSeq_gpu_IsIdle(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XSeq_gpu_IsReady(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XSeq_gpu_EnableAutoRestart(XSeq_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XSeq_gpu_DisableAutoRestart(XSeq_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_AP_CTRL, 0);
}

void XSeq_gpu_Set_opcode(XSeq_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_OPCODE_DATA, Data);
}

u32 XSeq_gpu_Get_opcode(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_OPCODE_DATA);
    return Data;
}

u32 XSeq_gpu_Get_status(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_STATUS_DATA);
    return Data;
}

u32 XSeq_gpu_Get_status_vld(XSeq_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_STATUS_CTRL);
    return Data & 0x1;
}

u32 XSeq_gpu_Get_a_BaseAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_BASE);
}

u32 XSeq_gpu_Get_a_HighAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_HIGH);
}

u32 XSeq_gpu_Get_a_TotalBytes(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XSEQ_GPU_CONTROL_ADDR_A_HIGH - XSEQ_GPU_CONTROL_ADDR_A_BASE + 1);
}

u32 XSeq_gpu_Get_a_BitWidth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_WIDTH_A;
}

u32 XSeq_gpu_Get_a_Depth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_DEPTH_A;
}

u32 XSeq_gpu_Write_a_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_A_HIGH - XSEQ_GPU_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_a_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_A_HIGH - XSEQ_GPU_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_BASE + (offset + i)*4);
    }
    return length;
}

u32 XSeq_gpu_Write_a_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_A_HIGH - XSEQ_GPU_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_a_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_A_HIGH - XSEQ_GPU_CONTROL_ADDR_A_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_A_BASE + offset + i);
    }
    return length;
}

u32 XSeq_gpu_Get_b_BaseAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_BASE);
}

u32 XSeq_gpu_Get_b_HighAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_HIGH);
}

u32 XSeq_gpu_Get_b_TotalBytes(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XSEQ_GPU_CONTROL_ADDR_B_HIGH - XSEQ_GPU_CONTROL_ADDR_B_BASE + 1);
}

u32 XSeq_gpu_Get_b_BitWidth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_WIDTH_B;
}

u32 XSeq_gpu_Get_b_Depth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_DEPTH_B;
}

u32 XSeq_gpu_Write_b_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_B_HIGH - XSEQ_GPU_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_b_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_B_HIGH - XSEQ_GPU_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_BASE + (offset + i)*4);
    }
    return length;
}

u32 XSeq_gpu_Write_b_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_B_HIGH - XSEQ_GPU_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_b_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_B_HIGH - XSEQ_GPU_CONTROL_ADDR_B_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_B_BASE + offset + i);
    }
    return length;
}

u32 XSeq_gpu_Get_c_BaseAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_BASE);
}

u32 XSeq_gpu_Get_c_HighAddress(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_HIGH);
}

u32 XSeq_gpu_Get_c_TotalBytes(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return (XSEQ_GPU_CONTROL_ADDR_C_HIGH - XSEQ_GPU_CONTROL_ADDR_C_BASE + 1);
}

u32 XSeq_gpu_Get_c_BitWidth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_WIDTH_C;
}

u32 XSeq_gpu_Get_c_Depth(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSEQ_GPU_CONTROL_DEPTH_C;
}

u32 XSeq_gpu_Write_c_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_C_HIGH - XSEQ_GPU_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_BASE + (offset + i)*4) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_c_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length)*4 > (XSEQ_GPU_CONTROL_ADDR_C_HIGH - XSEQ_GPU_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(int *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_BASE + (offset + i)*4);
    }
    return length;
}

u32 XSeq_gpu_Write_c_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_C_HIGH - XSEQ_GPU_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_BASE + offset + i) = *(data + i);
    }
    return length;
}

u32 XSeq_gpu_Read_c_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr -> IsReady == XIL_COMPONENT_IS_READY);

    int i;

    if ((offset + length) > (XSEQ_GPU_CONTROL_ADDR_C_HIGH - XSEQ_GPU_CONTROL_ADDR_C_BASE + 1))
        return 0;

    for (i = 0; i < length; i++) {
        *(data + i) = *(char *)(InstancePtr->Control_BaseAddress + XSEQ_GPU_CONTROL_ADDR_C_BASE + offset + i);
    }
    return length;
}

void XSeq_gpu_InterruptGlobalEnable(XSeq_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_GIE, 1);
}

void XSeq_gpu_InterruptGlobalDisable(XSeq_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_GIE, 0);
}

void XSeq_gpu_InterruptEnable(XSeq_gpu *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_IER);
    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_IER, Register | Mask);
}

void XSeq_gpu_InterruptDisable(XSeq_gpu *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_IER);
    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_IER, Register & (~Mask));
}

void XSeq_gpu_InterruptClear(XSeq_gpu *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XSeq_gpu_WriteReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_ISR, Mask);
}

u32 XSeq_gpu_InterruptGetEnabled(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_IER);
}

u32 XSeq_gpu_InterruptGetStatus(XSeq_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XSeq_gpu_ReadReg(InstancePtr->Control_BaseAddress, XSEQ_GPU_CONTROL_ADDR_ISR);
}

