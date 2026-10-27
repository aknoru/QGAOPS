// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
/***************************** Include Files *********************************/
#include "xqgpu_ga_parallel_top.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XQgpu_ga_parallel_top_CfgInitialize(XQgpu_ga_parallel_top *InstancePtr, XQgpu_ga_parallel_top_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Control_BaseAddress = ConfigPtr->Control_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XQgpu_ga_parallel_top_Start(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL) & 0x80;
    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}

u32 XQgpu_ga_parallel_top_IsDone(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL);
    return (Data >> 1) & 0x1;
}

u32 XQgpu_ga_parallel_top_IsIdle(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL);
    return (Data >> 2) & 0x1;
}

u32 XQgpu_ga_parallel_top_IsReady(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL);
    // check ap_start to see if the pcore is ready for next input
    return !(Data & 0x1);
}

void XQgpu_ga_parallel_top_EnableAutoRestart(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL, 0x80);
}

void XQgpu_ga_parallel_top_DisableAutoRestart(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_AP_CTRL, 0);
}

void XQgpu_ga_parallel_top_Set_a_0(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_0_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_0(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_0_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_1(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_1_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_1(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_1_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_2(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_2_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_2(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_2_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_3(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_3_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_3(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_3_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_4(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_4_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_4(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_4_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_5(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_5_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_5(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_5_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_6(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_6_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_6(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_6_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_a_7(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_7_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_a_7(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_A_7_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_0(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_0_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_0(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_0_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_1(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_1_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_1(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_1_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_2(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_2_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_2(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_2_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_3(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_3_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_3(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_3_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_4(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_4_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_4(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_4_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_5(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_5_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_5(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_5_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_6(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_6_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_6(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_6_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_Set_b_7(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_7_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_b_7(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_B_7_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_0(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_0_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_0_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_0_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_1(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_1_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_1_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_1_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_2(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_2_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_2_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_2_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_3(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_3_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_3_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_3_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_4(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_4_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_4_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_4_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_5(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_5_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_5_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_5_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_6(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_6_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_6_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_6_CTRL);
    return Data & 0x1;
}

u32 XQgpu_ga_parallel_top_Get_c_7(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_7_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_c_7_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_C_7_CTRL);
    return Data & 0x1;
}

void XQgpu_ga_parallel_top_Set_opcode(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_OPCODE_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_opcode(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_OPCODE_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_status(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_STATUS_DATA);
    return Data;
}

u32 XQgpu_ga_parallel_top_Get_status_vld(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_STATUS_CTRL);
    return Data & 0x1;
}

void XQgpu_ga_parallel_top_Set_dma_len(XQgpu_ga_parallel_top *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_DMA_LEN_DATA, Data);
}

u32 XQgpu_ga_parallel_top_Get_dma_len(XQgpu_ga_parallel_top *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_DMA_LEN_DATA);
    return Data;
}

void XQgpu_ga_parallel_top_InterruptGlobalEnable(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_GIE, 1);
}

void XQgpu_ga_parallel_top_InterruptGlobalDisable(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_GIE, 0);
}

void XQgpu_ga_parallel_top_InterruptEnable(XQgpu_ga_parallel_top *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER);
    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER, Register | Mask);
}

void XQgpu_ga_parallel_top_InterruptDisable(XQgpu_ga_parallel_top *InstancePtr, u32 Mask) {
    u32 Register;

    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Register =  XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER);
    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER, Register & (~Mask));
}

void XQgpu_ga_parallel_top_InterruptClear(XQgpu_ga_parallel_top *InstancePtr, u32 Mask) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XQgpu_ga_parallel_top_WriteReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_ISR, Mask);
}

u32 XQgpu_ga_parallel_top_InterruptGetEnabled(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_IER);
}

u32 XQgpu_ga_parallel_top_InterruptGetStatus(XQgpu_ga_parallel_top *InstancePtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    return XQgpu_ga_parallel_top_ReadReg(InstancePtr->Control_BaseAddress, XQGPU_GA_PARALLEL_TOP_CONTROL_ADDR_ISR);
}

