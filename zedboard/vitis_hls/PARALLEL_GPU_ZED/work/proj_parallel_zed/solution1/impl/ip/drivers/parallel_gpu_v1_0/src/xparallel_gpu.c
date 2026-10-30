// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
/***************************** Include Files *********************************/
#include "xparallel_gpu.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XParallel_gpu_CfgInitialize(XParallel_gpu *InstancePtr, XParallel_gpu_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XParallel_gpu_Start(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL) & 0x80;
    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XParallel_gpu_IsDone(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XParallel_gpu_IsIdle(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XParallel_gpu_IsReady(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XParallel_gpu_EnableAutoRestart(XParallel_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XParallel_gpu_DisableAutoRestart(XParallel_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_AP_CTRL, 0);
}

void XParallel_gpu_Set_a_0(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_0_DATA, Data);
}

u32 XParallel_gpu_Get_a_0(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_0_DATA);
    return Data;
}

void XParallel_gpu_Set_a_1(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_1_DATA, Data);
}

u32 XParallel_gpu_Get_a_1(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_1_DATA);
    return Data;
}

void XParallel_gpu_Set_a_2(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_2_DATA, Data);
}

u32 XParallel_gpu_Get_a_2(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_2_DATA);
    return Data;
}

void XParallel_gpu_Set_a_3(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_3_DATA, Data);
}

u32 XParallel_gpu_Get_a_3(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_3_DATA);
    return Data;
}

void XParallel_gpu_Set_a_4(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_4_DATA, Data);
}

u32 XParallel_gpu_Get_a_4(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_4_DATA);
    return Data;
}

void XParallel_gpu_Set_a_5(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_5_DATA, Data);
}

u32 XParallel_gpu_Get_a_5(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_5_DATA);
    return Data;
}

void XParallel_gpu_Set_a_6(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_6_DATA, Data);
}

u32 XParallel_gpu_Get_a_6(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_6_DATA);
    return Data;
}

void XParallel_gpu_Set_a_7(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_7_DATA, Data);
}

u32 XParallel_gpu_Get_a_7(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_A_7_DATA);
    return Data;
}

void XParallel_gpu_Set_b_0(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_0_DATA, Data);
}

u32 XParallel_gpu_Get_b_0(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_0_DATA);
    return Data;
}

void XParallel_gpu_Set_b_1(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_1_DATA, Data);
}

u32 XParallel_gpu_Get_b_1(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_1_DATA);
    return Data;
}

void XParallel_gpu_Set_b_2(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_2_DATA, Data);
}

u32 XParallel_gpu_Get_b_2(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_2_DATA);
    return Data;
}

void XParallel_gpu_Set_b_3(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_3_DATA, Data);
}

u32 XParallel_gpu_Get_b_3(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_3_DATA);
    return Data;
}

void XParallel_gpu_Set_b_4(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_4_DATA, Data);
}

u32 XParallel_gpu_Get_b_4(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_4_DATA);
    return Data;
}

void XParallel_gpu_Set_b_5(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_5_DATA, Data);
}

u32 XParallel_gpu_Get_b_5(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_5_DATA);
    return Data;
}

void XParallel_gpu_Set_b_6(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_6_DATA, Data);
}

u32 XParallel_gpu_Get_b_6(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_6_DATA);
    return Data;
}

void XParallel_gpu_Set_b_7(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_7_DATA, Data);
}

u32 XParallel_gpu_Get_b_7(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_B_7_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_0(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_0_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_0_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_0_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_1(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_1_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_1_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_1_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_2(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_2_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_2_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_2_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_3(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_3_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_3_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_3_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_4(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_4_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_4_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_4_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_5(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_5_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_5_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_5_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_6(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_6_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_6_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_6_CTRL);
    return Data & 0x1;
}

u32 XParallel_gpu_Get_c_7(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_7_DATA);
    return Data;
}

u32 XParallel_gpu_Get_c_7_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_C_7_CTRL);
    return Data & 0x1;
}

void XParallel_gpu_Set_opcode(XParallel_gpu *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_OPCODE_DATA, Data);
}

u32 XParallel_gpu_Get_opcode(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_OPCODE_DATA);
    return Data;
}

u32 XParallel_gpu_Get_status(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_STATUS_DATA);
    return Data;
}

u32 XParallel_gpu_Get_status_vld(XParallel_gpu *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_STATUS_CTRL);
    return Data & 0x1;
}

void XParallel_gpu_InterruptGlobalEnable(XParallel_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_GIE, 1);
}

void XParallel_gpu_InterruptGlobalDisable(XParallel_gpu *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_GIE, 0);
}

void XParallel_gpu_InterruptEnable(XParallel_gpu *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_IER);
    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_IER, Register | Mask);
}

void XParallel_gpu_InterruptDisable(XParallel_gpu *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_IER);
    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_IER, Register & (~Mask));
}

void XParallel_gpu_InterruptClear(XParallel_gpu *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XParallel_gpu_WriteReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_ISR, Mask);
}

u32 XParallel_gpu_InterruptGetEnabled(XParallel_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_IER);
}

u32 XParallel_gpu_InterruptGetStatus(XParallel_gpu *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XParallel_gpu_ReadReg(InstancePtr->Control_BaseAddress, XPARALLEL_GPU_CONTROL_ADDR_ISR);
}

